---
name: gemini-skill-factory
description: Inspect, audit, cross-reference, convert, create, enhance, and self-update Gemini Skills from GitHub repository URLs, npx skills commands, Google Drive ZIP archives, or uploaded files. Supports low-token fleet self-updating via ronot-creator/gemini-skill-factory manifest.json with bundled local_manifest.json comparison and automatically executes skill-lifecycle-guardian for zero-loss multi-file updates.
allowed-tools: drive default_api skills google
---
# Gemini Skill Factory (v2.4.0)

Automate the discovery, static security and malware screening, strict Claude-to-Gemini portability linting, existing-library cross-referencing, synthesis, zero-loss multi-file registration/updating, and **low-token self-updating** of skills from **GitHub repository URLs**, **Google Drive ZIP archives**, or **uploaded packages**.

## When to Use

- The user provides a **GitHub repository URL** (e.g., `https://github.com/<owner>/<repo>`, a subdirectory/tree URL `https://github.com/<owner>/<repo>/tree/<branch>/<path>`, a raw file URL, or `npx skills add <owner>/<repo>`) and asks to inspect it, import skills from it, or create a new skill based on that repository.
- The user provides or points to a `.zip` archive in Google Drive or uploads a repository archive containing one or more skills or reference docs.
- The user references numerical IDs or skill names from a previous Gemini Skill Factory inspection report to import or enhance specific skills.
- The user invokes `@gemini-skill-factory` and asks to **check for updates**, **update skills**, or **sync with `ronot-creator/gemini-skill-factory`** (Mode D).

## General Operating Principles

- **Mandatory Automatic Execution of `skill-lifecycle-guardian`**: Whenever creating or updating any skill in Step 5 or Mode D, always execute the `skill-lifecycle-guardian` Two-Step Pre-Staged + Write-Through Mirroring protocol (`scripts/skill_sync.py`) before calling `skills:save_skill` or `skills:update_skill`.
- **Mandatory Inspection by Default (With Explicit Override Support)**:
  - By default, when a GitHub URL or ZIP archive is provided without an explicit instruction to immediately create/import the skill, run in **Mode C (Inspection Only)** first and present the Standardized Inspection Report so the user can choose what to import.
  - **Explicit Override**: When the user explicitly asks in their prompt to *"create the skill"*, *"install this skill"*, *"batch import"*, or *"import <selection>"* from the provided GitHub link or archive, execute the mandatory security, compatibility, and overlap checks and **proceed directly to creating/updating the skill in the same workflow** without stopping for a redundant confirmation turn.
- **Static Inspection Only**: Never execute untrusted external scripts simply to inspect them. Inspect all retrieved scripts and files statically.
- **Prioritize Quality and Preservation Over Replacement**: Prefer enhancing existing skills (`Categories B & D`) over creating duplicates, and never downgrade or remove useful instructions or reference files from an existing skill.

## Mode D: Low-Token Self-Updating & Fleet Sync (`ronot-creator/gemini-skill-factory`)

To keep token usage near zero on normal conversations while giving non-technical users a seamless, one-step update path for `gemini-skill-factory` and `skill-lifecycle-guardian`:

1. **Lazy / Explicit Trigger Gate (Zero Idle Overhead)**:
   - Do **not** poll GitHub on unrelated turns. Run this check only when the user explicitly asks to check/update skills OR when `@gemini-skill-factory` is invoked for a skill operation.
2. **Bundled `O(1)` Manifest Comparison (Works With or Without a VM)**:
   - Load `references/local_manifest.json` via `get_skill_resources` (no VM hash computation required!) and fetch ONLY the lightweight remote manifest via `google:browse`:
     `https://raw.githubusercontent.com/ronot-creator/gemini-skill-factory/main/manifest.json`
   - Compare the local `version` and per-file `sha256_lf` hashes in `references/local_manifest.json` against the remote `manifest.json`.
   - **Short-Circuit**: If all installed versions and `sha256_lf` hashes match, stop immediately (`0` extra fetches) and confirm everything is up to date.
3. **Delta-Only Fetch & Anti-Torn-Read Verification (`O(Delta)` Cost)**:
   - Fetch **only** files whose `sha256_lf` differs from `references/local_manifest.json` via `google:browse` from `https://raw.githubusercontent.com/ronot-creator/gemini-skill-factory/<ref>/<skill>/<path>` (preferring `commit_sha` if pinned in `manifest.json`, otherwise `main`).
   - Stage the updated files in `/tmp/skill_factory_update/<skill>/` alongside unchanged local files, then run static security + integrity verification:
     ```bash
     python3 /working_dir/<conversation_id>/skills/user/gemini-skill-factory/scripts/audit_repo_zip.py \
       --verify-manifest /tmp/skill_factory_update/manifest.json \
       --dir /tmp/skill_factory_update/<skill> \
       --skill-name <skill>
     ```
4. **Fail-Safe Abort & Zero-Loss Persistence**:
   - **If `google:browse` fails, any `sha256_lf` mismatches (torn read), or any static security rule triggers**: abort the update immediately, leave the existing local skill completely untouched, and inform the user in plain, non-technical language that the local version is running safely.
   - **If verification passes**: copy the verified staged files into `skills/<skill>/`, update `references/local_manifest.json` to match, run `skill-lifecycle-guardian/scripts/skill_sync.py --skill-name <skill>` (Tool Step A), and commit in place via `skills:update_skill` (Tool Step B).

## Steps (GitHub / Archive Import & Synthesis)

### Step 1: Determine Operating Mode and Ingest Source (GitHub URL, Drive ZIP, or Upload)

1. Identify the requested operating mode from the user's prompt:
   - **Mode C - Inspection Only (DEFAULT)**: Use when a GitHub repo or ZIP is provided without an explicit command to immediately create/install.
   - **Mode A - Batch Import / Direct Creation**: Use when the user explicitly asks to create, install, or batch-import the skill(s) from the GitHub URL or archive.
   - **Mode B - Selective Import**: Use when the user selects specific skills by numerical ID (`1, 4, 7-10`), exact skill name, unambiguous partial name, or combinations.
   - **Mode D - Self-Update & Fleet Sync**: Use when checking for or applying updates from `ronot-creator/gemini-skill-factory`.
2. Ingest the source into `/tmp/skill_factory_extracted/<source_stem>/`:
   - **Route 1: GitHub Repository URL (`https://github.com/<owner>/<repo>...` or `npx skills add <owner>/<repo>`)**:
     - Because the sandbox VM has no direct outbound internet access (`git clone` and `curl` are blocked inside the VM), use Gemini's native web tools (`google:browse` and `google:search`) to inspect and fetch the repository:
       1. Call `google:browse` on the provided GitHub URL and, in parallel, call `google:search` with queries like `site:github.com/<owner>/<repo> "SKILL.md" OR "README.md"` and `site:github.com/<owner>/<repo>` to map the repository's directory tree, branches, `SKILL.md` files, `scripts/`, `references/`, and core documentation/source files.
       2. For each discovered skill folder or key documentation/source file in the repository, construct the direct raw or blob URLs (`https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` or `https://github.com/<owner>/<repo>/blob/<branch>/<path>`) and fetch their full contents in parallel batches using `google:browse`.
       3. Write the fetched files into `/tmp/skill_factory_extracted/<repo_name>/` preserving their relative directory structure.
       4. **Two GitHub Repository Sub-Types**:
          - **Type 1A (Pre-Packaged Skill / Agent Repository)**: The repository already contains one or more `SKILL.md` files, `.claude/commands/`, `.cursorrules`, or agent prompt markdown files. Reconstruct each discovered skill directory under `/tmp/skill_factory_extracted/<repo_name>/`.
          - **Type 1B (General Codebase, Library, CLI, or Documentation Repository)**: The repository does not contain a pre-existing `SKILL.md`, and the user wants to **turn the GitHub repository itself into a Gemini Skill**. Extract the repository's `README.md`, architecture docs, CLI/API specifications, and reusable helper scripts, and synthesize a structured candidate directory `/tmp/skill_factory_extracted/<repo_name>/<repo-kebab-name>/` containing a draft `SKILL.md` plus `references/` and `scripts/` distilled from the repository.
   - **Route 2: Google Drive or Uploaded ZIP Archive**:
     - Locate the archive in the workspace or Google Drive (`drive:search_files` + `drive:download_file_content`) and extract it statically via `scripts/audit_repo_zip.py --zip <zip_path>`.

### Step 2: Static Extraction, Malware Screening, and Portability Linting

1. Export a JSON map of the user's existing `user:` skills to `/tmp/existing_user_skills.json`.
2. Run `scripts/audit_repo_zip.py` against EITHER the ZIP archive (`--zip`) OR the reconstructed GitHub directory (`--dir`):

```bash
python3 /working_dir/<conversation_id>/skills/user/gemini-skill-factory/scripts/audit_repo_zip.py \
  --dir /tmp/skill_factory_extracted/<source_stem> \
  --existing-skills /tmp/existing_user_skills.json \
  --manifest-out /tmp/skill_factory_manifest.json
```

3. Evaluate each discovered or synthesized candidate for:
   - **Security & Malware Gate**: Reject (`Rejected (Security)`) any candidate containing obfuscated shell execution, credential exfiltration, destructive root deletion, reverse shells, or prompt injection.
   - **Gemini Compatibility & Portability Linter**: Classify as `Compatible Directly`, `Requires Modification` (flagging Claude tool syntax like `Bash`/`WebFetch`, `~/.claude/` paths, external MCP servers, or local OS dependencies like `docker`/`tmux`), or `Rejected (Incompatible)`.

### Step 3: Deep Cross-Referencing Against Existing Gemini Skills

Classify every candidate against the user's existing Gemini Skills library into one of five categories:

- **A. Entirely New Capability**: No meaningful overlap exists. Action: create a new skill via `skills:save_skill`.
- **B. Existing Skill with Complementary Capabilities**: Incoming skill adds useful workflows, references, or scripts that the existing skill lacks. Action: merge additions into the existing skill via `skills:update_skill` while preserving all original instructions and supporting files.
- **C. Existing Skill with Superior Information**: Existing skill already provides equal or better capability. Action: skip.
- **D. Substantial Functional Overlap**: Merge non-redundant capabilities into the stronger existing skill via `skills:update_skill`.
- **E. Incoming Skill is Inferior or Redundant**: Action: skip; never downgrade an existing skill.

### Step 4: Present the Standardized Inspection Report

Present the **Standardized Inspection Report** containing:

1. **Summary Metrics**: Total discovered/synthesized skills, directly compatible count, count requiring modifications, and rejected count.
2. **Numbered Evaluation Table (`#1..#N`)**: Stable numerical ID, Skill Name, Functionality & Primary Use Cases, Supporting Files & Dependencies, Compatibility Assessment (with portability warnings), Security Inspection Result, and Overlap Category (`A-E`).
3. **Mode Branch**:
   - If running in **Mode C (Inspection Only - Default)**, stop here and ask the user whether they want **Batch Import** or **Selective Import** (by numbers, exact names, or partial names).
   - If the user explicitly requested creation/import (**Mode A** or **Mode B**), include the inspection summary and proceed directly to Step 5.

### Step 5: Execute Creation / Import via `skill-lifecycle-guardian` & Present Final Report

1. **Resolve Selection**: For Selective Import, run `scripts/audit_repo_zip.py --manifest-out /tmp/skill_factory_manifest.json --select "<selection>"`.
2. **Synthesize or Merge into `skills/<kebab-name>/` (Tool Step A)**:
   - For **Category A (New Skill)**: Write normalized `SKILL.md` (valid frontmatter, space-separated `allowed-tools`, Gemini tool mappings, under 500 lines, no em/en-dashes) and all supporting `references/`, `scripts/`, `assets/` into `skills/<kebab-name>/`.
   - For **Categories B & D (Enhance Existing Skill)**: Load the existing skill via `lookup_skills` and `get_skill_resources`, reconstruct all existing files in `skills/<existing-name>/`, and merge the complementary instructions and supporting files without removing original capabilities.
   - **Execute `skill-lifecycle-guardian` Validation & Write-Through Mirroring**:
     ```bash
     python3 /working_dir/<conversation_id>/skills/user/skill-lifecycle-guardian/scripts/skill_sync.py --skill-name <kebab-name>
     ```
   - End Tool Step A so all staged and mirrored files flush cleanly to disk before the host pre-uploader runs.
3. **Commit to Google Cloud Blobstore (Tool Step B)**:
   - In the next tool step, invoke `skills:save_skill(skill_dir="/working_dir/<conversation_id>/skills/<kebab-name>")` (Category A) or `skills:update_skill(name="<existing-name>", skill_dir="/working_dir/<conversation_id>/skills/<existing-name>")` (Categories B & D) with zero concurrent file writes.
   - Keep `skills/user/<kebab-name>/` intact so same-turn `get_skill_resources` and script calls resolve immediately via Tier 1 while Tier 2 Cloud Blobstore serves all future turns and conversations.
4. **Present Final Operation Report**: Summarize Newly Created (`Category A`), Enhanced (`Categories B & D`), Skipped (`Categories C & E`), Rejected (`Security / Compatibility`), Failed, and any items requiring user clarification.
