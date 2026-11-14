# Gemini Skill Factory

**100% Pure-Markdown, Chat-Safe package manager, skill compiler, and update guard for Gemini Apps skills.**  
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
| **`gemini-skill-factory`** | `3.1.0` | Inspects, security-scans, lints Claude-to-Gemini portability, transcodes scripts to pure Markdown, consolidates split/megarepo skills (`O(N)` Mergeability + Sharded Mega-Skills), installs, and self-updates. |
| **`skill-lifecycle-guardian`** | `2.0.0` | Prevents multi-file skill corruption, empty blob IDs, broken frontmatter, and orphan files across both standard Gemini Chat and Task Mode. |

---

## Operating Modes (`gemini-skill-factory`)

| Mode | Trigger | What It Does |
| :--- | :--- | :--- |
| **Mode C — Inspection Only (Default)** | `@gemini-skill-factory <GitHub URL or ZIP>` | Fetches metadata first, runs security + portability + mergeability checks, and prints a numbered **Inspection Report (`#1..#N`)** before installing anything. |
| **Mode A — Batch Import / Direct Creation** | `@gemini-skill-factory create a skill from <URL>` or `batch import` | Runs all security/portability/mergeability checks and immediately creates/updates all compatible skills in the same turn. |
| **Mode B — Selective Import** | `Import #1, #3, and 5-7` (or by skill name) | Installs or merges only the specific items you choose from an inspection report. |
| **Mode D — Low-Token Self-Update** | `@gemini-skill-factory check for updates` | Compares `assets/local_manifest.json` against `manifest.json` (`O(1)`), pulls only changed `.md`/`.json` files (`O(Delta)`), and updates in place. |

**Two Supported Source Types:**
- **Type 1A (Pre-Packaged Skill / Agent Repos)**: Imports existing `SKILL.md`, `.claude/commands/*.md`, or `.cursorrules` packages.
- **Type 1B (General Codebases & Docs Repos)**: Distills any regular GitHub repository's `README.md`, architecture docs, and CLI/API specs into a brand-new Gemini Skill.

---

## Smart Consolidation & Mega-Skill Synthesis (`v3.1.0`)

To prevent token waste and skill-library clutter when importing multi-file or 50–100+ skill repositories, `gemini-skill-factory` uses a **Two-Axis Consolidation Engine** (`references/merge_strategy.md`):

1. **Flat Merge (`O(N)` Mergeability Score `> 5`)**:
   - Reads only frontmatter/headers in Pass 1 and groups files by `(Parent_Directory, Canonical_Action, Target_Resource)`—never running wasteful $O(N^2)$ comparisons.
   - Scores multi-item clusters on a `0–10` rubric (`+4` split-file coupling, `+3` trigger collision, `+2` shared tool/output, `+1` fits `<= 4k` tokens & `< 90` entries, `-10` Hard Veto on opposing roles like read-only auditor vs. writer).
   - Clusters scoring **`6–10`** are automatically merged into one clean `SKILL.md` + namespaced `references/*.md`.
2. **Sharded Mega-Skill Synthesis (`>= 4` Distinct Skills, `>= 70%` Domain Cohesion)**:
   - When a repository contains 4+ distinct skills in one cohesive domain (e.g., 50 video skills or 30 coding skills), it compiles them into **one Sharded Mega-Skill** (`SKILL.md` router + `catalogue/index.json` + lazy-loaded `references/shard-*.md` under `<= 90` total entries)—preventing Skills Manager overpopulation.
3. **Chat-Safe Script Transcoding (`references/transcoding_rules.md`)**:
   - Any `.py`, `.sh`, `.js`, or `.ts` files in an upstream repo are automatically transcoded into readable `references/<script_name>_spec.md` specifications so every installed skill runs in standard Gemini Chat.

### How to Control or Override Consolidation Upfront

You can steer or bypass the consolidation engine directly in your prompt:
- **Force a Mega-Skill:** `@gemini-skill-factory <URL> — combine everything into one Mega-Skill`
- **Bypass Merging (Keep Separate):** `@gemini-skill-factory <URL> — keep all skills separate, do not merge`
- **Force a Specific Merge:** `Import and merge #1 and #2 into a single skill`

---

## How to Use `skill-lifecycle-guardian`

- **Automatic Protection (Zero Setup)**: Auto-executes whenever you create, edit, update, or import any skill—enforcing pre-flight inspection, `.md`/`.json`-only validation, YAML frontmatter checks, orphan cleanup, and post-write verification.
- **Self-Update**: `@skill-lifecycle-guardian check for updates`

---

## Repository Structure

```text
├── .github/workflows/update-manifest.yml
├── llms.txt
├── manifest.json
├── README.md
├── gemini-skill-factory/
│   ├── SKILL.md
│   ├── assets/local_manifest.json
│   └── references/
│       ├── merge_strategy.md
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
