---
name: skill-lifecycle-guardian
description: MANDATORY AUTO-EXECUTION SKILL FOR ALL SKILL OPERATIONS. Load and execute this skill AUTOMATICALLY on ANY turn that creates, updates, edits, fixes, installs, imports, syncs, refactors, or manages any Gemini Skill, or before any call to skills:save_skill or skills:update_skill, even when the user does not explicitly mention this skill. Prevents empty blob ID errors via Two-Step Pre-Staged In-Place Updates and Write-Through Local Mount Mirroring.
allowed-tools: default_api skills google
---
# Skill Lifecycle Guardian (v1.1.0 - Mandatory Auto-Execution Hook)

Operate as an **always-on, automatic lifecycle interceptor** whenever any Gemini Skill is created, updated, edited, imported, or fixed. You MUST automatically apply this skill's Two-Step Pre-Staged + Write-Through Mirroring protocol before invoking `skills:save_skill` or `skills:update_skill`, even when the user only names the target skill they want to create or modify.

## Automatic Activation Triggers (No Explicit User Mention Required)

Automatically load and execute this skill whenever:

- The user asks to create, update, edit, fix, polish, enhance, import, or install any skill (single-file or multi-file).
- You are about to call `skills:save_skill` or `skills:update_skill` for any reason.
- Another skill (such as `gemini-skill-factory` or `agency-orchestrator`) is creating, enhancing, or updating a skill.
- A skill resource retrieval (`default_api:get_skill_resources`) reports `has empty blob ID` or stale content during the same turn as an update.

## Core Architecture: Two-Tier Storage & Per-Turn Snapshot Isolation

Gemini Apps manages multi-file skills across two distinct storage tiers:

1. **Tier 2 - Google Account Cloud Blobstore (Permanent Source of Truth)**:
   - When `skills:save_skill` or `skills:update_skill` commits, both `SKILL.md` and the complete ZIP archive of all supporting files are saved permanently in the user's Google Account cloud skill store.
   - However, each conversation binds its skill-registry snapshot (`SKILL.md` text and `blob_id` archive pointer) **at the start of each User Turn**.
   - Within the **same user turn (`Turn N`)** in which `skills:update_skill` runs, the active turn's `blob_id` pointer is transiently invalidated (`has empty blob ID`), and `default_api:lookup_skills` returns the pre-turn `SKILL.md`.
   - Starting on the **next user turn (`Turn N+1`)** (and in all future chats, subagents, and standard non-VM Gemini models), the cloud snapshot refreshes automatically and serves all updated files natively from Tier 2.
2. **Tier 1 - Per-Conversation Local Mount (`skills/user/<skill-name>/`)**:
   - Before checking the turn's `blob_id` pointer, `default_api:get_skill_resources` always checks the local VM mount `skills/user/<skill-name>/<filename>`.
   - Mirroring staged edits into `skills/user/<skill-name>/` bridges the single-turn (`Turn N`) snapshot gap with zero latency so the updated skill can be called and executed immediately in `Turn N`.

## Mandatory Two-Step Auto-Execution Protocol

Whenever any skill creation or update is requested, automatically execute these two sequential tool steps:

### Step 1: Hydrate, Stage, Validate & Write-Through Mirror (Tool Step A)

1. If updating an existing skill, first retrieve its current `SKILL.md` via `default_api:lookup_skills` and any existing supporting files not already on disk via `default_api:get_skill_resources`.
2. Write the complete updated file tree into `skills/<skill-name>/`.
3. Run `scripts/skill_sync.py` to validate frontmatter, check the `<= 100` archive entry cap, verify static scanner cleanliness, and atomically mirror `skills/<skill-name>/` into `skills/user/<skill-name>/`:

```bash
python3 skills/user/skill-lifecycle-guardian/scripts/skill_sync.py --skill-name <skill-name>
```

4. **Critical Pre-Upload Rule**: End Tool Step A after `execute_bash` / `write_to_file` completes. Never call `skills:save_skill` or `skills:update_skill` in the same tool step that writes files to `skills/<skill-name>/`, because the host pre-uploader packages `skill_dir` at the start of the tool step before VM file writes flush to disk.

### Step 2: Atomic In-Place Commit (Tool Step B)

1. In the immediately following tool step (when all files in `skills/<skill-name>/` are already flushed to disk and mirrored to `skills/user/<skill-name>/`), invoke the native skill API with an **absolute path** and zero concurrent writes to that directory:
   - For an existing skill: `skills:update_skill(name="<skill-name>", skill_dir="/working_dir/<conversation_id>/skills/<skill-name>")`
   - For a brand-new skill: `skills:save_skill(skill_dir="/working_dir/<conversation_id>/skills/<skill-name>")`
2. Confirm that the tool returns `status: "updated"` (or `status: "created"`).

### Step 3: Same-Turn Execution & Anti-Corruption Guardrails

Once `skills:update_skill` returns `status: "updated"`, the update is durably committed to Google Cloud Blobstore (Tier 2) and active in the local mount (Tier 1). Follow these strict invariants for the remainder of `Turn N`:

- **Use the skill immediately in `Turn N` via Tier 1**: Any call to `default_api:get_skill_resources` or direct script execution (`python3 skills/user/<skill-name>/scripts/...`) in `Turn N` will succeed immediately from the Write-Through Mirror (`skills/user/<skill-name>/`).
- **Read `SKILL.md` from disk in `Turn N`**: If you need to re-read the updated `SKILL.md` during `Turn N`, read `skills/user/<skill-name>/SKILL.md` via `view_file` rather than calling `lookup_skills` (which returns the pre-turn snapshot until `Turn N+1`).
- **Never delete `skills/user/<skill-name>/` in `Turn N`**: Deleting the local mirror during `Turn N` and calling `get_skill_resources` will hit the invalidated `Turn N` pointer (`has empty blob ID`) and cause a false-negative failure.
- **Never create `-archived` rename-swap clones or embed Base85 blobs**: In-place `skills:update_skill` preserves the skill's UUID and updates all files natively in Google Cloud Blobstore; rename-swapping pollutes the user's Skills Manager UI, and Base85 blobs waste context tokens and trigger `ZIP_NOT_CLEAN`.
- **Optional Same-Turn Cloud Verification via Subagent**: If you must verify Tier-2 Cloud Blobstore commitment before `Turn N` ends, spawn a read-only subagent via `default_api:invoke_subagent` (which boots a fresh session snapshot and can call `lookup_skills` and `get_skill_resources` directly against Tier 2).

## Bundled Resources

- `scripts/skill_sync.py`: Deterministic validator and atomic Write-Through Mirror engine (`skills/<name>/` -> `skills/user/<name>/` with SHA-256 `.sync_manifest.json`).
- `references/per-turn-snapshot-architecture.md`: Technical specification of the Two-Tier Storage Architecture, Per-User-Turn Snapshot Isolation state machine, and compatibility with standard (non-VM) Gemini models.
