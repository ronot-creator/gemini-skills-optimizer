# Gemini Skill Factory

**The missing package manager and update guard for Gemini Apps skills.**  
Paste any GitHub or Claude skill URL into Gemini and run it in 30 seconds—with static security screening, portability linting, and zero-loss multi-file updates.

---

## Install in 30 Seconds (Any Gemini Model)

Copy and paste this single prompt into Gemini:

> `Browse https://github.com/ronot-creator/gemini-skill-factory (using raw.githubusercontent.com/ronot-creator/gemini-skill-factory/main/ paths), inspect the files, and install both skill-lifecycle-guardian and gemini-skill-factory into my Gemini Skills library.`

**Using a standard Gemini model without skill-saving tools?**  
1. Click **Code → Download ZIP** on this repository and extract it.
2. Compress `skill-lifecycle-guardian/` and `gemini-skill-factory/` into **two separate `.zip` files** (each `.zip` must contain one skill folder with `SKILL.md` inside it).
3. Upload each `.zip` in **Gemini → Skills Manager**.

---

## Included Skills

| Skill | Version | What It Does |
| :--- | :--- | :--- |
| **`gemini-skill-factory`** | `2.4.0` | Inspects, security-scans, lints Claude-to-Gemini portability, converts, installs, and self-updates skills from GitHub URLs or ZIPs. |
| **`skill-lifecycle-guardian`** | `1.3.0` | Stops multi-file Gemini skills from silently breaking (`has empty blob ID` / `ZIP_NOT_CLEAN`) during updates, and pulls verified self-updates. |

---

## How to Use `gemini-skill-factory`

### 1. Inspect Any GitHub Skill Repo (Safe Default)
> `@gemini-skill-factory https://github.com/<owner>/<repo>`

Runs static security + portability linting (`Bash`, `~/.claude/`, MCP, and OS dependencies are flagged before import) and prints a numbered **Inspection Report (`#1..#N`)**.

### 2. Install or Convert Directly
> `@gemini-skill-factory create a skill from https://github.com/<owner>/<repo>`

Works on both pre-packaged `SKILL.md` repos and general code/doc repositories.

### 3. Selective Import
> `Import #1, #3, and 5-7`

### 4. Import from a Google Drive or Uploaded ZIP
> `@gemini-skill-factory inspect my uploaded skills.zip and install the compatible ones`

### 5. Low-Token Self-Update (`O(1)` Check + `O(Delta)` Pull)
> `@gemini-skill-factory check for updates`

Compares the bundled `references/local_manifest.json` directly against `manifest.json`, downloads only changed files, verifies `sha256_lf` hashes + static security rules, and aborts safely if anything fails.

---

## How to Use `skill-lifecycle-guardian`

### 1. Automatic Protection (Zero Setup)
`skill-lifecycle-guardian` auto-executes whenever you ask Gemini to create, edit, update, or import any skill. It enforces a **Two-Step Pre-Staged + Write-Through Mirroring** protocol (`skills/<name>/` → `skills/user/<name>/` → Cloud Blobstore) so multi-file skills never hit `has empty blob ID` or `ZIP_NOT_CLEAN`.

### 2. Manual Validation & Sync
> `@skill-lifecycle-guardian validate and sync <skill-name>`

### 3. Self-Update `skill-lifecycle-guardian`
> `@skill-lifecycle-guardian check for updates`

---

## Repository Structure

```text
├── .github/workflows/update-manifest.yml
├── manifest.json
├── README.md
├── gemini-skill-factory/
│   ├── SKILL.md
│   ├── references/local_manifest.json
│   └── scripts/audit_repo_zip.py
└── skill-lifecycle-guardian/
    ├── SKILL.md
    ├── references/
    │   ├── local_manifest.json
    │   └── per-turn-snapshot-architecture.md
    └── scripts/skill_sync.py
```
