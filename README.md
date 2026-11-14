# Gemini Skill Factory

**100% Pure-Markdown, Chat-Safe package manager and update guard for Gemini Apps skills.**  
Works identically in **standard Gemini Chat** and **Task Mode**—with zero `.py`/`.sh`/`.js` scripts, zero terminal setup, and zero external MCP dependencies.

---

## Install in 30 Seconds (Any Gemini Model)

Copy and paste this single prompt into Gemini:

> `Browse https://github.com/ronot-creator/gemini-skill-factory (using raw.githubusercontent.com/ronot-creator/gemini-skill-factory/main/ paths), inspect the files, and install both skill-lifecycle-guardian and gemini-skill-factory into my Gemini Skills library.`

**Manual Upload Fallback:**
1. Click **Code → Download ZIP** on this repository and extract it.
2. Compress `skill-lifecycle-guardian/` and `gemini-skill-factory/` into **two separate `.zip` files**.
3. Upload each `.zip` in **Gemini → Skills Manager**.

---

## Included Skills (100% `.md` and `.json` Only)

| Skill | Version | What It Does |
| :--- | :--- | :--- |
| **`gemini-skill-factory`** | `3.0.0` | Inspects, security-scans, lints Claude-to-Gemini portability, transcodes external scripts into pure Markdown specs, installs, and self-updates skills. |
| **`skill-lifecycle-guardian`** | `2.0.0` | Prevents multi-file skill corruption, empty blob IDs, broken frontmatter, and orphan files across both standard Gemini Chat and Task Mode. |

---

## How to Use `gemini-skill-factory`

### 1. Inspect Any GitHub Skill Repo (Safe Default)
> `@gemini-skill-factory https://github.com/<owner>/<repo>`

Runs static security + portability linting and prints a numbered **Inspection Report (`#1..#N`)**. Any external `.py`/`.sh`/`.js` scripts are automatically flagged for **Chat-Safe Transcoding** into `references/<script_name>_spec.md`.

### 2. Install or Transcode Directly
> `@gemini-skill-factory create a skill from https://github.com/<owner>/<repo>`

### 3. Selective Import
> `Import #1, #3, and 5-7`

### 4. Low-Token Self-Update (`O(1)` Check + `O(Delta)` Pull)
> `@gemini-skill-factory check for updates`

Compares `assets/local_manifest.json` directly against `manifest.json`, fetches only `ADDED`/`MODIFIED` `.md` and `.json` files, screens them statically, and applies updates + orphan deletes safely in place.

---

## How to Use `skill-lifecycle-guardian`

### 1. Automatic Protection (Zero Setup)
`skill-lifecycle-guardian` auto-executes whenever you ask Gemini to create, edit, update, or import any skill—enforcing pre-flight inspection, `.md`/`.json`-only validation, YAML frontmatter checks, orphan cleanup, and post-write verification.

### 2. Self-Update `skill-lifecycle-guardian`
> `@skill-lifecycle-guardian check for updates`

---

## Repository Structure

```text
├── .github/workflows/update-manifest.yml
├── manifest.json
├── README.md
├── gemini-skill-factory/
│   ├── SKILL.md
│   ├── assets/local_manifest.json
│   └── references/
│       ├── output_schemas.md
│       ├── transcoding_rules.md
│       └── update_protocol.md
└── skill-lifecycle-guardian/
    ├── SKILL.md
    ├── assets/local_manifest.json
    └── references/
        ├── lifecycle_rules.md
        └── per-turn-snapshot-architecture.md
```
