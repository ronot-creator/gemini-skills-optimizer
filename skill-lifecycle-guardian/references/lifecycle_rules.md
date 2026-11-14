# Lifecycle Safety Rules (Deterministic Pure-Markdown Protocol)

Follow these five sequential gates on every skill creation, update, or deletion.

## Gate 1: Pre-Flight Inspection
1. If updating an existing skill, call `lookup_skills` to read its current `SKILL.md` and `list_skill_resources` / `get_skill_resources` to list all existing files.
2. Record the full existing file list so complementary files are preserved and obsolete files can be explicitly deleted later.
3. Never create duplicate `-archived` or `-v2` clones; always update in place to preserve the skill's identity.

## Gate 2: Chat-Safe Content & Frontmatter Validation
Before writing any file to a skill:
1. **Extension Check**: Confirm every file ends in `.md` or `.json`. Reject or transcode any `.py`, `.sh`, `.js`, `.ts`, or `scripts/` path into `references/<name>_spec.md`.
2. **YAML Frontmatter Check**:
   - `SKILL.md` must start on line 1 with `---` and close with `---`.
   - `name` must be lowercase kebab-case (`^[a-z0-9-]+$`) with no `user:` or `system:` prefix.
   - `description` must be non-empty.
   - Replace any em-dash or en-dash in `SKILL.md` with standard hyphens (`-`).
3. **Archive Entry Limit**: Confirm total files + directories is `<= 100`.
4. **No Base85 / Binary Blobs**: Never embed encoded binary payloads inside Markdown or JSON files.

## Gate 3: Safe In-Place Write & Orphan Cleanup
- **In Standard Gemini Chat**:
  1. Write or update each changed `.md` and `.json` file using `skills:write_skill_file` (or `skills:update_skill` / `skills:save_skill`).
  2. Delete every file in the `DELETED` / obsolete set using `skills:delete_skill_file`.
- **In Task Mode (when staging a directory)**:
  1. Stage the complete clean file tree first, remove obsolete files/folders, and finish all file writes in one step.
  2. Commit the clean directory in the immediately following step via `skills:update_skill` or `skills:save_skill` with zero concurrent writes.

## Gate 4: Same-Turn Snapshot Isolation Handling
- In Gemini Apps, each user turn (`Turn N`) binds a skill snapshot at turn start.
- After committing an update in `Turn N`, `lookup_skills` may continue returning the pre-turn `SKILL.md` until `Turn N+1` begins.
- Do not panic or re-run redundant updates in `Turn N`; starting on `Turn N+1` (and in all new chats), the updated Cloud Blobstore snapshot loads automatically.

## Gate 5: Post-Write Verification
1. Verify via `list_skill_resources` (or inspecting the committed file list) that:
   - Zero `.py`, `.sh`, `.js`, `.ts`, or `scripts/` entries remain.
   - All intended `.md` and `.json` files are present.
   - `assets/local_manifest.json` reflects the newly committed version and file list.
