# Exact Output Schemas & Templates

You MUST reproduce these exact section headers, metadata blocks, and table columns when presenting inspection or operation results. Never expose `user:` or `system:` prefixes in user-facing output.

## Schema 1: Standardized Inspection Report (Step 4)

```markdown
### Standardized Inspection Report

* **Summary Metrics**: **<TOTAL>** skills discovered | **<COMPAT_DIRECT>** directly compatible | **<COMPAT_MOD>** requiring adaptation/transcoding | **<REJECTED>** rejected
* **Source**: `<GitHub URL or Archive Name>`

| # | Skill Name | Functionality & Primary Use Cases | Supporting Files & Dependencies | Compatibility & Portability | Security Inspection | Overlap Category |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **#1** | `<kebab-name>` | <concise summary> | <files & external deps> | `Compatible Directly` / `Requires Modification (<flags>)` | `Passed` / `Rejected (<reason>)` | `<A/B/C/D/E>` |
```

* **Mode C Footer (when stopping for user selection)**:
  > Reply with **Batch Import** to install/update all compatible skills, or **Selective Import** with numbers, ranges, or names (e.g., `Import #1, #3, and 5-7`).

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
