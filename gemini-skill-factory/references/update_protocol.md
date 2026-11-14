# Manifest & Self-Update Protocol (Deterministic Pure-Markdown Engine)

Use this exact step-by-step algorithm whenever checking for or applying updates from `https://github.com/ronot-creator/gemini-skill-factory`.

## Step 1: Load Local State (`O(1)`)
1. Call `get_skill_resources` (or `skills:get_skill_resources`) to read `assets/local_manifest.json` for the target skill (`gemini-skill-factory` or `skill-lifecycle-guardian`).
2. Record:
   - `local_version`
   - `local_files` map: `{ "<relative_path>": { "sha256_lf": "...", "bytes": N } }`

## Step 2: Fetch Remote Manifest (`O(1)`)
1. Retrieve `https://raw.githubusercontent.com/ronot-creator/gemini-skill-factory/main/manifest.json` using `google:search` (e.g., querying the raw URL or repo manifest) or `google:browse` if available in the session.
2. If the remote manifest cannot be retrieved or parsed as valid JSON, **abort immediately**, keep all local skill files untouched, and inform the user in plain language that the local version is running safely.

## Step 3: Compute Exact Diff Sets
For the target skill entry under `remote_manifest.skills[<skill_name>]`:
1. Compare `remote_version` vs. `local_version` and compare every key in `remote_files` against `local_files`:
   - **`ADDED`**: Path exists in `remote_files` but not in `local_files`.
   - **`MODIFIED`**: Path exists in both, and `remote_files[path].sha256_lf != local_files[path].sha256_lf` (or `bytes` differs).
   - **`UNCHANGED`**: Path exists in both with identical `sha256_lf` and `bytes`.
   - **`DELETED`**: Path exists in `local_files` (excluding `assets/local_manifest.json`) but not in `remote_files`.
2. **Short-Circuit**: If `ADDED`, `MODIFIED`, and `DELETED` are all empty (and `remote_version == local_version`), stop immediately (`0` extra fetches) and report that the skill is up to date.

## Step 4: Delta-Only Fetch & Security Gate (`O(Delta)`)
1. For each path in `ADDED` and `MODIFIED`:
   - Confirm the path ends strictly in `.md` or `.json` (if any `.py`, `.sh`, `.js`, `.ts`, or `scripts/` path appears, **abort** and reject).
   - Fetch the raw file content from `https://raw.githubusercontent.com/ronot-creator/gemini-skill-factory/main/<skill_name>/<path>`.
   - Screen the fetched content against the Security & Malware Gate in `references/transcoding_rules.md`.
   - Verify the fetched content is complete (not truncated) and matches expected structure/frontmatter.
2. If any fetch fails, is truncated, or triggers a security rule, **abort immediately** with zero mutations to the installed skill.

## Step 5: Atomic Update & Orphan Cleanup (`skill-lifecycle-guardian`)
1. Write each `ADDED` and `MODIFIED` file to the target skill using `skills:write_skill_file` (or stage and commit via `skills:update_skill`).
2. Delete every file in `DELETED` using `skills:delete_skill_file` (or omit from the committed directory).
3. Update `assets/local_manifest.json` with the new `version` and `files` map from the remote manifest.
4. Run Post-Write Verification (`list_skill_resources`) to confirm only `.md` and `.json` files exist.
