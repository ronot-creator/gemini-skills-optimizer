# Gemini Skill Factory

**100% Pure-Markdown, Chat-Safe package manager, universal 4-source skill compiler, autonomous skill discoverer, and update guard for Gemini Apps skills.**  
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
| **`gemini-skill-factory`** | `3.2.1` | Discovers skills autonomously (`Mode E`), synthesizes Pure-Markdown skills from **4 sources**, runs security & portability checks, cross-references existing skills (`Categories A–E`), consolidates split/megarepo skills (`O(N)` Mergeability + Sharded Mega-Skills), appends a **Plain-English TL;DR & Recommended Strategy** with a copy-pasteable reply, installs, and self-updates. |
| **`skill-lifecycle-guardian`** | `2.0.0` | Prevents multi-file skill corruption, empty blob IDs, broken frontmatter, and orphan files across both standard Gemini Chat and Task Mode. |

---

## Operating Modes (`gemini-skill-factory`)

| Mode | Trigger | What It Does |
| :--- | :--- | :--- |
| **Mode C — Inspection Only (Default)** | `@gemini-skill-factory <GitHub URL or ZIP>` | Fetches metadata first, runs security + portability + mergeability + overlap checks, prints a numbered **Inspection Report (`#1..#N`)** plus a **Plain-English TL;DR & copy-pasteable Recommended Strategy**, and waits for your choice. |
| **Mode A — Batch Import / Direct Creation** | `@gemini-skill-factory create a skill from <source>` or `batch import` | Runs all security/portability/mergeability/overlap checks and immediately creates/updates all compatible skills in the same turn. |
| **Mode B — Selective Import** | `Import #1, #3, and 5-7` (or by skill name) | Installs or merges only the specific items you choose from an inspection or discovery report. |
| **Mode D — Low-Token Self-Update** | `@gemini-skill-factory check for updates` | Compares `assets/local_manifest.json` against `manifest.json` (`O(1)`), pulls only changed `.md`/`.json` files (`O(Delta)`), and updates in place. |
| **Mode E — Autonomous Skill Discovery** | `@gemini-skill-factory find me a skill for <goal>` | Searches [`skills.sh`](https://skills.sh/) and GitHub, fetches and verifies raw `SKILL.md` files (never from snippets alone), and presents ranked candidates with a **Plain-English TL;DR & copy-pasteable Recommended Strategy**. |

### Plain-English TL;DR & Copy-Pasteable Reply (Every Report)
Because technical tables can be dense, every **Mode C** Inspection Report and **Mode E** Discovery Report ends with a jargon-free summary block:
- **TL;DR**: 1–2 plain sentences explaining what is safe/useful and whether merging is recommended.
- **Recommended Strategy**: The best strategy in plain English (while keeping you in full control to merge, keep separate, or cherry-pick).
- **Reply to execute this strategy**: An exact copy-pasteable prompt (e.g., `Batch Import (apply recommended Mega-Skill)` or `Import #1`), alongside quick alternatives (`Keep all separate, do not merge`).

### Mode B Selection Syntax
When replying to an Inspection or Discovery Report, you can select items using:
- **Ranges:** `#1-3` or `1-3`
- **Single IDs:** `#2` or `2`
- **Exact Names or Unique Substrings:** e.g., `Import #1, quiz-generator, and 5-7`

---

## Overlap Categories (`A–E`) in Inspection & Discovery Reports

Every candidate skill is cross-referenced against your already-installed Gemini Skills library and assigned one of five overlap categories:

| Category | Meaning | Default Action |
| :---: | :--- | :--- |
| **`A`** | **Entirely New Capability** — No overlapping skill exists in your library. | Creates a new standalone skill (or Sharded Mega-Skill). |
| **`B`** | **Complementary Additions** — Matches an existing skill and adds useful new workflows/rules. | Merges the new capabilities into your existing skill without deleting original instructions. |
| **`C`** | **Existing Skill is Superior** — Your installed skill already covers this better or more completely. | **Skipped** (preserves your stronger local skill). |
| **`D`** | **Substantial Functional Overlap** — Heavy overlap with an existing skill, with a few non-redundant extras. | Merges only the non-redundant additions into the stronger existing skill. |
| **`E`** | **Inferior or Redundant** — Exact duplicate or lower quality than what you already have. | **Skipped** to prevent library bloat. |

---

## Universal 4-Source Skill Synthesis (`v3.2.0+`)

`gemini-skill-factory` synthesizes 100% Pure-Markdown skills from four distinct source types:

1. **Source 1 — Pre-Packaged Skill / Agent Repos & Archives**: Imports existing `SKILL.md`, `.claude/commands/*.md`, `.cursorrules`, `npx skills add <owner>/<repo>`, or Google Drive / uploaded `.zip` packages.
2. **Source 2 — General Codebases & Technical Docs**: Distills any regular GitHub repository's `README.md`, architecture docs, and CLI/API specs into a clean Gemini Skill.
3. **Source 3 — Generic Material**: Converts unstructured prompts, rubrics, SOPs, study guides, checklists, or notes into deterministic `SKILL.md` + `references/` workflows.
4. **Source 4 — Conversational Experience & Retrospectives (Explicit Gate)**: Distills verified bug fixes, edge cases, and safety nets discovered during a chat session into a new skill or targeted patch—always presenting a short, plain-Markdown **Retrospective Patch Preview** (`Target Skill`, `Observed Issue`, and `1–5 line Proposed Addition`) and waiting for your `Apply` confirmation before editing any `SKILL.md`.

### Ecosystem Discovery & Attribution

Mode E autonomous discovery is inspired by and credits Vercel's open agent-skills ecosystem, [`vercel-labs/skills`](https://github.com/vercel-labs/skills) and [`skills.sh`](https://skills.sh/). You can also point `gemini-skill-factory` directly at `https://github.com/vercel-labs/skills` to synthesize your own Pure-Markdown `find-skills` skill.

---

## Security Gate, Portability Linter & Script Transcoding

1. **Static Security & Malware Gate (`references/transcoding_rules.md`)**:
   - Automatically marks **`Rejected (Security)`** any candidate containing `eval(`, `exec(`, `subprocess.Popen(...shell=True)`, `curl ... | sh` or `| bash`, destructive commands (`rm -rf /`, credential harvesting, token exfiltration), or prompt-injection patterns (`ignore previous instructions`, hidden overrides).
2. **Claude-to-Gemini Portability Linter**:
   - Automatically flags **`Requires Modification`** when an upstream skill uses Claude tool syntax (`Bash`, `WebFetch`, `TodoWrite`, `Skill tool`), Claude config paths (`~/.claude`, `.claude/`, `CLAUDE.md`), external MCP servers (`fastmcp`, `stdio`), or local OS dependencies (`docker`, `tmux`, `systemctl`, `brew`, `apt-get`), and adapts them to native Gemini workflows.
3. **Chat-Safe Script Transcoding**:
   - Any `.py`, `.sh`, `.js`, or `.ts` files in an upstream repo are automatically transcoded into readable `references/<script_name>_spec.md` specifications (`<= 100` entries, `.md` and `.json` only) so every installed skill runs in standard Gemini Chat.

---

## Smart Consolidation & Mega-Skill Synthesis (`v3.1.0+`)

To prevent token waste and skill-library clutter when importing multi-file or 50–100+ skill repositories, `gemini-skill-factory` uses a **Two-Axis Consolidation Engine** (`references/merge_strategy.md`):

1. **Flat Merge (`O(N)` Mergeability Score `> 5`)**:
   - Reads only frontmatter/headers in Pass 1 and groups files by `(Parent_Directory, Canonical_Action, Target_Resource)`—never running wasteful $O(N^2)$ comparisons.
   - Scores multi-item clusters on a `0–10` rubric (`+4` split-file coupling, `+3` trigger collision, `+2` shared tool/output, `+1` fits `<= 4k` tokens & `< 90` entries, `-10` Hard Veto on opposing roles like read-only auditor vs. writer).
   - Clusters scoring **`6–10`** are automatically merged into one clean `SKILL.md` + namespaced `references/*.md`.
2. **Sharded Mega-Skill Synthesis (`>= 4` Distinct Skills, `>= 70%` Domain Cohesion)**:
   - When a repository contains 4+ distinct skills in one cohesive domain (e.g., 50 video skills or 30 coding skills), it compiles them into **one Sharded Mega-Skill** (`SKILL.md` router + `catalogue/index.json` + lazy-loaded `references/shard-*.md` under `<= 90` total entries)—preventing Skills Manager overpopulation.

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
│       ├── discovery_and_synthesis.md
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
