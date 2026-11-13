#!/usr/bin/env python3
"""Static repository, directory & ZIP auditor, compatibility linter, manifest verifier, selector, and skill validator for Gemini Skill Factory v2.4.0."""
import argparse, hashlib, json, os, re, sys, zipfile
from pathlib import Path

def get_security_rules():
    return [
        (r"eval\s*\(", "Dynamic code evaluation pattern"),
        (r"exec\s*\(", "Dynamic code execution pattern"),
        (r"subprocess\.Popen\(.*shell\s*=\s*True", "Unconstrained shell subprocess"),
        (r"curl\s+.*\|\s*(?:sh|bash)", "Piped remote shell execution"),
        (r"ignore\s+previous\s+instructions", "Prompt injection pattern"),
    ]

def get_portability_warnings(txt: str) -> list[str]:
    """Flag Claude/CLI dependencies that require adaptation or may not run in standard non-VM Gemini Apps."""
    checks = [
        (r"\b(Bash|WebFetch|TodoWrite|Skill tool)\b", "Claude tool syntax (map to execute_bash/google:browse/lookup_skills)"),
        (r"(~/\.claude|\.claude/|CLAUDE\.md)", "Claude-specific config/directory path"),
        (r"\b(mcp|fastmcp|stdio)\b", "External MCP server dependency (verify Gemini tool availability)"),
        (r"\b(docker|tmux|systemctl|brew install|apt-get)\b", "Local OS/container dependency (unavailable in standard Gemini)"),
    ]
    found = []
    for pat, label in checks:
        if re.search(pat, txt, re.I):
            found.append(label)
    return found

def sha256_lf(path: Path) -> str:
    """Compute SHA-256 over LF-normalized UTF-8 text (or raw bytes for binary) so web-reader line-ending normalization never breaks verification."""
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8").replace("\r\n", "\n").rstrip("\n") + "\n"
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    except UnicodeDecodeError:
        return hashlib.sha256(raw).hexdigest()

def verify_against_manifest(skill_dir: Path, manifest_path: Path, skill_name: str) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    skill_entry = manifest.get("skills", {}).get(skill_name)
    if not skill_entry:
        return {"valid": False, "errors": [f"Skill '{skill_name}' not found in manifest"]}
    expected_files = skill_entry.get("files", {})
    mismatches, missing, sec_issues = [], [], []
    rules = get_security_rules()
    for rel_path, meta in expected_files.items():
        if rel_path == "references/local_manifest.json":
            continue
        target = skill_dir / rel_path
        if not target.exists():
            missing.append(rel_path)
            continue
        actual_hash = sha256_lf(target)
        if actual_hash != meta.get("sha256_lf"):
            mismatches.append({"file": rel_path, "expected": meta.get("sha256_lf"), "actual": actual_hash})
        txt = target.read_text(encoding="utf-8", errors="ignore")
        for pat, label in rules:
            if re.search(pat, txt, re.I):
                sec_issues.append(f"{rel_path}: {label}")
    ok = not missing and not mismatches and not sec_issues
    return {"valid": ok, "missing": missing, "mismatches": mismatches, "security_issues": sec_issues}

def validate_skill_dir(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    errors = []
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    else:
        txt = skill_md.read_text(encoding="utf-8", errors="replace")
        if not txt.startswith("---\n"):
            errors.append("Missing YAML frontmatter start")
        if "name:" not in txt[:500] or "description:" not in txt[:1500]:
            errors.append("Missing name or description in frontmatter")
    all_entries = [p for p in skill_dir.rglob("*") if p.name != ".sync_manifest.json"]
    if len(all_entries) + 1 > 100:
        errors.append(f"Archive entry count ({len(all_entries)+1}) exceeds Gemini Apps 100-entry limit")
    return {"valid": len(errors) == 0, "entry_count": len(all_entries) + 1, "errors": errors}

def scan_directory_tree(ext_dir: Path, existing: dict) -> dict:
    discovered = []
    rules = get_security_rules()
    skill_mds = sorted(ext_dir.rglob("SKILL.md"))

    candidate_roots = []
    if skill_mds:
        candidate_roots = [(smd.parent, smd) for smd in skill_mds]
    else:
        md_files = [
            p for p in sorted(ext_dir.rglob("*.md"))
            if p.name.lower() not in ("readme.md", "license.md", "contributing.md", "changelog.md")
        ]
        if md_files:
            for mf in md_files:
                candidate_roots.append((mf.parent, mf))
        elif (ext_dir / "README.md").exists():
            candidate_roots.append((ext_dir, ext_dir / "README.md"))

    for idx, (sdir, entry_md) in enumerate(candidate_roots, 1):
        txt = entry_md.read_text(encoding="utf-8", errors="replace")
        name_m = re.search(r"^name:\s*(.+)$", txt, re.M)
        desc_m = re.search(r"^description:\s*(.+)$", txt, re.M)
        raw_name = name_m.group(1).strip().strip("'\"") if name_m else (
            entry_md.stem if entry_md.name != "SKILL.md" and entry_md.name != "README.md" else sdir.name
        )
        sname = re.sub(r"[^a-z0-9-]+", "-", raw_name.lower()).strip("-")
        sdesc = desc_m.group(1).strip().strip("'\"") if desc_m else ""
        if not sdesc:
            lines = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith(("#", "---"))]
            sdesc = lines[0][:240] if lines else f"Skill synthesized from {sdir.name}"

        sec_issues = []
        rel_files = []
        for f in sorted(sdir.rglob("*")):
            if f.is_file() and f.name != ".sync_manifest.json":
                rel_files.append(str(f.relative_to(sdir)))
                ftxt = f.read_text(encoding="utf-8", errors="ignore")
                for pat, label in rules:
                    if re.search(pat, ftxt, re.I):
                        sec_issues.append(f"{f.name}: {label}")

        portability_flags = get_portability_warnings(txt)
        needs_mod = entry_md.name != "SKILL.md" or bool(portability_flags)
        compat = f"Requires Modification ({'; '.join(portability_flags)})" if needs_mod else "Compatible Directly"
        overlap = "B/D (Existing Match: " + sname + ")" if sname in existing else "A (Entirely New Capability)"
        discovered.append({
            "id": idx,
            "name": sname,
            "description": sdesc,
            "entry_file": str(entry_md.relative_to(ext_dir)),
            "path": str(sdir),
            "files": rel_files,
            "compatibility": compat,
            "portability_warnings": portability_flags,
            "security": "Passed" if not sec_issues else f"Rejected ({'; '.join(sec_issues)})",
            "overlap_category": overlap,
        })
    return {"total_discovered": len(discovered), "skills": discovered}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--validate", type=str, help="Validate a staged skill directory")
    p.add_argument("--verify-manifest", type=str, help="Verify staged skill dir against manifest.json")
    p.add_argument("--skill-name", type=str, help="Skill name for --verify-manifest or --hash-dir")
    p.add_argument("--hash-dir", type=str, help="Compute LF-normalized SHA-256 map for a skill directory")
    p.add_argument("--zip", type=str, help="ZIP archive to inspect")
    p.add_argument("--dir", type=str, help="Already-extracted directory or fetched GitHub repo tree to inspect")
    p.add_argument("--extract-to", type=str, help="Extraction directory for --zip")
    p.add_argument("--existing-skills", type=str, help="JSON map of existing skills")
    p.add_argument("--manifest-out", type=str, help="Output manifest JSON path")
    p.add_argument("--select", type=str, help="Resolve selection string against manifest")
    args = p.parse_args()

    if args.hash_dir:
        sdir = Path(args.hash_dir)
        files = {}
        for f in sorted(sdir.rglob("*")):
            if f.is_file() and f.name != ".sync_manifest.json" and str(f.relative_to(sdir)).replace("\\", "/") != "references/local_manifest.json":
                rel = str(f.relative_to(sdir)).replace("\\", "/")
                files[rel] = {"sha256_lf": sha256_lf(f), "bytes": f.stat().st_size}
        print(json.dumps({"skill": args.skill_name or sdir.name, "files": files}, indent=2))
        sys.exit(0)

    if args.verify_manifest and args.dir and args.skill_name:
        res = verify_against_manifest(Path(args.dir), Path(args.verify_manifest), args.skill_name)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["valid"] else 1)

    if args.validate:
        res = validate_skill_dir(Path(args.validate))
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["valid"] else 1)

    if args.select and args.manifest_out:
        manifest = json.loads(Path(args.manifest_out).read_text(encoding="utf-8"))
        skills = manifest.get("skills", [])
        tokens = [t.strip() for t in re.split(r"[,;]+", args.select) if t.strip()]
        selected, not_found, ambiguous = [], [], []
        for tok in tokens:
            m_range = re.match(r"^#?(\d+)\s*-\s*#?(\d+)$", tok)
            if m_range:
                a, b = int(m_range.group(1)), int(m_range.group(2))
                for s in skills:
                    if a <= s["id"] <= b:
                        selected.append(s["name"])
                continue
            m_num = re.match(r"^#?(\d+)$", tok)
            if m_num:
                nid = int(m_num.group(1))
                matches = [s for s in skills if s["id"] == nid]
                if matches:
                    selected.append(matches[0]["name"])
                else:
                    not_found.append(tok)
                continue
            exact = [s for s in skills if s["name"].lower() == tok.lower()]
            if exact:
                selected.append(exact[0]["name"])
                continue
            partial = [s for s in skills if tok.lower() in s["name"].lower()]
            if len(partial) == 1:
                selected.append(partial[0]["name"])
            elif len(partial) > 1:
                ambiguous.append({"token": tok, "candidates": [s["name"] for s in partial]})
            else:
                not_found.append(tok)
        print(json.dumps({"selected": selected, "not_found": not_found, "ambiguous": ambiguous}, indent=2))
        sys.exit(0)

    existing = (
        json.loads(Path(args.existing_skills).read_text(encoding="utf-8"))
        if args.existing_skills and Path(args.existing_skills).exists()
        else {}
    )

    target_dir = None
    if args.zip and args.extract_to:
        target_dir = Path(args.extract_to)
        target_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.zip, "r") as zf:
            zf.extractall(target_dir)
    elif args.dir:
        target_dir = Path(args.dir)

    if target_dir and target_dir.exists():
        out = scan_directory_tree(target_dir, existing)
        if args.manifest_out:
            Path(args.manifest_out).write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(json.dumps(out, indent=2))
        sys.exit(0)

if __name__ == "__main__":
    main()
