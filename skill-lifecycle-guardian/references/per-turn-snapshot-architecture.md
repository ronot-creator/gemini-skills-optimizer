# Per-User-Turn Snapshot Isolation & Two-Tier Skill Storage Architecture

## 1. The Empirical Discovery

Controlled experiments on multi-file skills in Gemini Apps established four foundational facts:

1. **In-Place Updates Persist 100% in Cloud Storage**: Calling `skills:update_skill(name="<skill-name>", skill_dir="/working_dir/<cid>/skills/<skill-name>")` updates `SKILL.md`, updates modified supporting files (`references/`, `scripts/`, `protocols/`, `catalogue/`, `specialists/`), and preserves untouched supporting files in Google's cloud blobstore.
2. **Per-User-Turn Snapshot Isolation**: At the start of each User Turn (`Turn N`), the Gemini Apps runtime loads an immutable snapshot of the user's skill registry (`SKILL.md` text and `blob_id` pointers) into the turn's tool-execution context.
   - When `skills:update_skill` is called during `Turn N`, the active turn's `blob_id` binding for that skill is invalidated (`has empty blob ID`) and `default_api:lookup_skills` continues returning the pre-turn `SKILL.md` until `Turn N` ends.
   - As soon as `Turn N+1` begins (on the user's next message, or inside any newly spawned subagent or new chat), the runtime loads the newly committed snapshot and both `lookup_skills` and `get_skill_resources` resolve 100% natively from Google Cloud Blobstore.
3. **Tier-1 Local Mount Precedence**: When `default_api:get_skill_resources(name="user:<skill-name>", filenames=[...])` is invoked, it checks the local VM path `/working_dir/<cid>/skills/user/<skill-name>/<filename>` (Tier 1) **before** querying the turn's `blob_id` pointer (Tier 2).
4. **Host Pre-Uploader Timing**: The host middleware that packages `skill_dir` into a ZIP archive runs at the **start** of the tool execution step before VM commands (`execute_bash`, `write_to_file`) in that same step finish writing to disk. Therefore, staging files in Tool Step A and calling `save_skill` or `update_skill` in Tool Step B guarantees that the host packages the completely flushed directory.

## 2. Compatibility Across Taskmate (VM) and Standard Gemini Models (Non-VM)

| Environment | How `Turn N` (Update Turn) Works | How `Turn N+1` & All Future Chats Work |
| :--- | :--- | :--- |
| **Taskmate / Sandbox VM Chats** | Write-Through Mirror (`skills/user/<name>/`) serves `get_skill_resources` and direct script execution (`python3 skills/user/<name>/scripts/...`) immediately in `Turn N`. | Native Cloud Blobstore (`blob_id`) hydrates `skills/user/<name>/` on demand via `get_skill_resources`. |
| **Standard Gemini Models (Fast / Thinking / Pro without VM)** | *(Skills are already committed to Google Cloud Storage prior to opening the chat.)* | Every turn starts with a fresh cloud snapshot; `lookup_skills` returns `SKILL.md` and `get_skill_resources` unpacks supporting files in Google's backend and returns their full text inside the tool response JSON (`content` field) without needing a VM. |

## 3. Lifecycle State Machine

1. **`STAGED_AND_MIRRORED` (Tool Step A)**:
   - Complete skill directory written to `skills/<name>/`, validated (`<= 100` entries), and mirrored to `skills/user/<name>/` via `scripts/skill_sync.py`.
2. **`COMMITTED_IN_FLIGHT_TURN_N` (Tool Step B)**:
   - `skills:update_skill` (or `skills:save_skill`) returns `status: "updated"` (or `"created"`).
   - Same-turn calls use Tier 1 (`skills/user/<name>/`). Evicting `skills/user/<name>/` during `Turn N` is forbidden.
3. **`CLOUD_BLOBSTORE_LIVE` (`Turn N+1` Onward)**:
   - Cloud `blob_id` and updated `SKILL.md` are live across all sessions and models.
