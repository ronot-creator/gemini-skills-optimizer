# Per-User-Turn Snapshot Isolation & Two-Tier Skill Storage Architecture

## 1. Core Runtime Behavior

1. **In-Place Updates Persist 100% in Cloud Storage**: Updating a skill in place updates `SKILL.md`, updates modified supporting `.md` and `.json` files, and preserves untouched supporting files in Google's Cloud Blobstore.
2. **Per-User-Turn Snapshot Isolation**: At the start of each User Turn (`Turn N`), the Gemini Apps runtime loads an immutable snapshot of the user's skill registry (`SKILL.md` text and archive pointers) into the turn's tool-execution context.
   - When a skill is updated during `Turn N`, `lookup_skills` may continue returning the pre-turn `SKILL.md` until `Turn N` ends.
   - As soon as `Turn N+1` begins (on the user's next message, or inside any newly spawned subagent or new chat), the runtime loads the newly committed snapshot and all updated files resolve natively from Cloud Blobstore.

## 2. Universal Compatibility (Standard Gemini Chat & Task Mode)

| Environment | How `Turn N` (Update Turn) Works | How `Turn N+1` & All Future Chats Work |
| :--- | :--- | :--- |
| **Standard Gemini Chat (No VM)** | Pure-Markdown skills (`.md` + `.json` only) load cleanly without executable-file blocks; updates commit via native `skills:*` tools. | Every turn starts with a fresh cloud snapshot; `lookup_skills` and `get_skill_resources` return full `.md` and `.json` contents natively. |
| **Task Mode (With VM)** | Pre-staged directory commits (`Tool Step A -> Tool Step B`) prevent pre-uploader races. | Native Cloud Blobstore serves all updated `.md` and `.json` files across all sessions and models. |
