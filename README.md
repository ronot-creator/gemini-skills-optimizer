# Gemini Skills (`ronot-creator/gemini-skills`)

Original Gemini Apps skills built for reliable multi-file skill management, GitHub/archive ingestion, and low-token self-updating without requiring terminal access or manual ZIP re-uploads.

## Skill Catalog

| Skill | Version | Purpose |
| :--- | :--- | :--- |
| **`gemini-skill-factory`** | `2.3.1` | Inspect, audit, cross-reference, convert, install, and self-update Gemini Skills from GitHub repositories, Google Drive ZIP archives, or uploaded files. |
| **`skill-lifecycle-guardian`** | `1.2.0` | Automatically protect multi-file skill creations and updates from empty-blob-ID and pre-uploader race conditions, and pull verified self-updates from this repository. |

---

## 1. How to Use `gemini-skill-factory`

### A. Inspect a GitHub Repository Before Installing (Default Safe Mode)
Paste any GitHub repository URL or `npx skills add` command without asking to install yet:
> `@gemini-skill-factory https://github.com/<owner>/<repo>`

Gemini will fetch the repository statically, run security and compatibility checks, compare against your existing skills, and show a numbered **Standardized Inspection Report (`#1..#N`)** so you can choose what to import.

### B. Install or Create a Skill Directly from GitHub
When you already know you want the skill installed:
> `@gemini-skill-factory create a skill from https://github.com/<owner>/<repo>`

Works for both pre-packaged skill repositories (containing `SKILL.md`) and general code/documentation repositories (synthesizes a clean Gemini Skill from the repo's docs and scripts).

### C. Selective Import After Inspection
After reviewing an inspection report, pick specific items by number or name:
> `Import #1, #3, and 5-7`

### D. Import from a Google Drive or Uploaded ZIP Archive
Upload a `.zip` file or reference one in Google Drive:
> `@gemini-skill-factory inspect my uploaded skills-pack.zip and install the compatible ones`

### E. Check for & Pull Updates (Low-Token Self-Updater)
To update `gemini-skill-factory` (and `skill-lifecycle-guardian`) without touching GitHub or re-uploading files:
> `@gemini-skill-factory check for updates`

**How it works under the hood:**
1. **Lazy Trigger**: Never polls GitHub on unrelated chats (0 idle tokens).
2. **`O(1)` Manifest Check**: Reads only `manifest.json` (~2 KB) and compares `version` and LF-normalized SHA-256 (`sha256_lf`) hashes against your local files.
3. **`O(Delta)` Pull + Security Gate**: Downloads only changed files, verifies `sha256_lf` integrity (preventing torn reads), and runs static security checks.
4. **Fail-Safe Fallback**: If anything fails, your existing local skill stays untouched and Gemini notifies you in plain English.

---

## 2. How to Use `skill-lifecycle-guardian`

### A. Automatic Protection (Zero Setup Needed)
`skill-lifecycle-guardian` is configured to **auto-execute** whenever you ask Gemini to create, edit, update, fix, or import any skill. You do not need to mention it by name—simply ask Gemini to update a skill and it will automatically:
1. **Stage & Validate (Step A)**: Write all files into `skills/<skill-name>/`, validate YAML frontmatter and the `<= 100` archive entry limit, and write-through mirror to `skills/user/<skill-name>/` via `scripts/skill_sync.py`.
2. **Commit Atomically (Step B)**: Commit the flushed directory to Google Cloud Blobstore via `skills:update_skill` or `skills:save_skill` in the next step, preventing `ZIP_NOT_CLEAN` and `has empty blob ID` errors.

### B. Manual / Explicit Invocation
If you want to explicitly audit or repair a multi-file skill's sync state:
> `@skill-lifecycle-guardian validate and sync <skill-name>`

### C. Check for & Pull Updates for `skill-lifecycle-guardian`
You can update `skill-lifecycle-guardian` directly using the same `manifest.json` hash-diff methodology:
> `@skill-lifecycle-guardian check for updates`

Gemini will check `manifest.json`, download only changed files for `skill-lifecycle-guardian`, verify `sha256_lf` hashes and static security rules, mirror them locally, and commit the update in place.

---

## Repository Structure

```text
├── manifest.json
├── README.md
├── gemini-skill-factory/
│   ├── SKILL.md
│   └── scripts/
│       └── audit_repo_zip.py
└── skill-lifecycle-guardian/
    ├── SKILL.md
    ├── references/
    │   └── per-turn-snapshot-architecture.md
    └── scripts/
        └── skill_sync.py
```
