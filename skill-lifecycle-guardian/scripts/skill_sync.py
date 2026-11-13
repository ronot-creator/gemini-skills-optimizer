#!/usr/bin/env python3
"""Deterministic validator and atomic Write-Through Mirror engine for Skill Lifecycle Guardian."""
import argparse, hashlib, json, re, shutil, sys, time, zipfile
from pathlib import Path

def validate_and_sync(workspace_root: Path, skill_name: str, export_zip: str | None = None) -> dict:
    src = workspace_root / "skills" / skill_name
    dst = workspace_root / "skills" / "user" / skill_name
    tmp = workspace_root / "skills" / "user" / f".{skill_name}.tmp"

    errors = []
    warnings = []

    if not src.exists() or not src.is_dir():
        return {"valid": False, "errors": [f"Source skill directory not found: {src}"]}

    skill_md = src / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing required SKILL.md in skill root.")
    else:
        txt = skill_md.read_text(encoding="utf-8", errors="replace")
        if not txt.startswith("---\n"):
            errors.append("SKILL.md must begin with YAML frontmatter delimiter '---'.")
        if not re.search(r"^name:\s*[a-z0-9-]+\s*$", txt[:800], re.M):
            errors.append("SKILL.md frontmatter must contain a valid lowercase kebab-case 'name' field.")
        if not re.search(r"^description:\s*.+$", txt[:2000], re.M):
            errors.append("SKILL.md frontmatter must contain a non-empty 'description' field.")
        if "\u2014" in txt or "\u2013" in txt:
            warnings.append("SKILL.md contains em-dash or en-dash characters; replace with standard hyphens.")

    all_entries = [p for p in src.rglob("*") if p.name != ".sync_manifest.json"]
    total_entry_count = len(all_entries) + 1  # +1 for root folder entry in zip
    if total_entry_count > 100:
        errors.append(
            f"Archive entry count ({total_entry_count}) exceeds Gemini Apps 100-entry limit (ZIP_TOO_MANY_ENTRIES)."
        )

    file_hashes = {}
    for p in sorted(all_entries):
        if p.is_file():
            rel = str(p.relative_to(src))
            raw = p.read_bytes()
            file_hashes[rel] = {
                "size_bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }

    if errors:
        return {
            "valid": False,
            "skill_name": skill_name,
            "entry_count": total_entry_count,
            "errors": errors,
            "warnings": warnings,
        }

    # Atomic Write-Through Mirror to skills/user/<skill_name>
    dst.parent.mkdir(parents=True, exist_ok=True)
    if tmp.exists():
        shutil.rmtree(tmp)
    shutil.copytree(src, tmp)

    manifest = {
        "skill_name": skill_name,
        "synced_at_epoch": time.time(),
        "entry_count": total_entry_count,
        "file_count": len(file_hashes),
        "files": file_hashes,
    }
    (tmp / ".sync_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if dst.exists():
        shutil.rmtree(dst)
    tmp.rename(dst)

    zip_path_out = None
    if export_zip:
        zpath = Path(export_zip)
        zpath.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(src.rglob("*")):
                if p.is_file() and p.name != ".sync_manifest.json":
                    zf.write(p, arcname=f"{skill_name}/{p.relative_to(src)}")
        zip_path_out = str(zpath)

    return {
        "valid": True,
        "skill_name": skill_name,
        "staged_path": str(src),
        "mirrored_user_mount": str(dst),
        "exported_zip": zip_path_out,
        "entry_count": total_entry_count,
        "file_count": len(file_hashes),
        "warnings": warnings,
        "files": file_hashes,
    }

def main():
    parser = argparse.ArgumentParser(description="Validate and write-through mirror a Gemini Skill directory.")
    parser.add_argument("--skill-name", required=True, help="Kebab-case skill name under skills/<skill-name>.")
    parser.add_argument("--workspace", default=".", help="Workspace root directory (default: current directory).")
    parser.add_argument("--export-zip", default=None, help="Optional output path for a distributable skill ZIP.")
    args = parser.parse_args()

    res = validate_and_sync(Path(args.workspace).resolve(), args.skill_name, args.export_zip)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res.get("valid") else 1)

if __name__ == "__main__":
    main()
