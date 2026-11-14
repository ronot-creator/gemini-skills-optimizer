# Exact Output Schemas & Templates

You MUST reproduce these exact section headers, metadata blocks, and table columns when presenting inspection, discovery, retrospective, or operation results. Never expose `user:` or `system:` prefixes in user-facing output.

## Schema 1: Standardized Inspection Report (Step 4)

```markdown
### Standardized Inspection Report

* **Summary Metrics**: **<TOTAL>** skills discovered | **<COMPAT_DIRECT>** directly compatible | **<COMPAT_MOD>** requiring adaptation/transcoding | **<REJECTED>** rejected
* **Source**: `<GitHub URL, Archive Name, Generic Material, or Chat Retrospective>`

| # | Skill Name | Functionality & Primary Use Cases | Supporting Files & Dependencies | Compatibility & Portability | Security Inspection | Overlap Category |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **#1** | `<kebab-name>` | <concise summary> | <files & external deps> | `Compatible Directly` / `Requires Modification (<flags>)` | `Passed` / `Rejected (<reason>)` | `<A/B/C/D/E>` |
```

* **Plain-English TL;DR & Recommended Strategy (Mandatory in Mode C)**:
  ```markdown
  **TL;DR:** <1–2 plain-language sentences summarizing what is safe/useful here, whether it duplicates anything you already have, and whether merging or a Mega-Skill is recommended.>

  * **Recommended Strategy:** <Best strategy in plain English—e.g., "Combine #1–#5 into one Sharded Mega-Skill to avoid clutter" or "Import #1 and #3 into your existing skills; skip #2 as a duplicate." You still have full freedom to choose otherwise.>
  * **Reply to execute this strategy:** `<exact copy-pasteable prompt, e.g., Batch Import (apply recommended Mega-Skill)>`
  * **Or customize:** `Import #1, #3` | `Keep all separate, do not merge`
  ```

## Schema 2: Final Operation Report (Step 5)

```markdown
### Final Operation Report

* **Newly Created (Category A)**: <comma-separated skill names or `None`>
* **Enhanced (Categories B & D)**: <comma-separated skill names or `None`>
* **Skipped (Categories C & E)**: <comma-separated skill names or `None`>
* **Rejected (Security / Incompatible)**: <comma-separated skill names with reasons or `None`>
* **Transcoded Scripts**: <list of `external_script -> references/<name>_spec.md` mappings or `None`>
* **Failed / Needs Clarification**: <items or `None`>
```

## Schema 3: Self-Update Status Report (Mode D)

```markdown
### Skill Update Check (`ronot-creator/gemini-skill-factory`)

* **<skill-name>**: `v<local>` -> `v<remote>` (`Up to date` / `Updated` / `Aborted cleanly - local copy intact`)
* **File Diff Summary**: `ADDED`: <count> | `MODIFIED`: <count> | `DELETED`: <count> | `UNCHANGED`: <count>
```

## Schema 4: Mode E Autonomous Discovery Report

```markdown
### Autonomous Skill Discovery Report (Mode E)

* **Goal**: `<user capability goal>`
* **Discovery Sources**: [`skills.sh`](https://skills.sh/) & GitHub (inspired by [`vercel-labs/skills`](https://github.com/vercel-labs/skills)) — raw `SKILL.md` verified

| # | Candidate Skill | Source Repo / URL | Summary & Fit | Security & Portability | Overlap Category |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **#1** | `<kebab-name>` | `[<owner/repo>](<URL>)` | <concise fit summary> | `Passed` / `Requires Transcoding` | `<A/B/C/D/E>` |
```

* **Plain-English TL;DR & Recommended Strategy (Mandatory in Mode E)**:
  ```markdown
  **TL;DR:** <1–2 plain-language sentences explaining which candidate fits best and whether any require transcoding or overlap with your library.>

  * **Recommended Strategy:** <Best strategy in plain English—e.g., "Import #1 as a standalone skill" or "Combine #1 and #2 into one skill." You still have full freedom to choose otherwise.>
  * **Reply to execute this strategy:** `<exact copy-pasteable prompt, e.g., Import #1>`
  * **Or customize:** `Import #1, #2` | `Batch Import (keep separate)`
  ```

## Schema 5: Source 4 Retrospective Patch Preview (Explicit Gate)

```markdown
### Retrospective Skill Update Proposal

* **Target Skill**: `<skill-name>` (`New Skill` / `Update v<current>`)
* **Observed Issue / Lesson**: <concise root-cause summary from conversation>
* **Proposed Pure-Markdown Addition**:
  > <1–5 concise, verified lines to add to `SKILL.md` or `references/`>
```

* **Retrospective Footer**:
  > Reply **`Apply`** to persist this update via `skill-lifecycle-guardian`, or specify edits.
