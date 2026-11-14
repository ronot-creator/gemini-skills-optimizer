# Token-Optimal Mergeability & Mega-Skill Synthesis Strategy (v3.1.0)

Use this deterministic, $O(N)$ pure-Markdown strategy whenever inspecting or importing multi-file or large (50–100+ skill) repositories. It solves both **workflow fragmentation** (Flat Merge) and **skill-library overpopulation** (Sharded Mega-Skill Synthesis) without $O(N^2)$ token waste.

## Stage 1: Metadata-Only Sweep ($O(N)$, Zero Body Reads)
1. Fetch only the repository file tree and the YAML frontmatter (`name`, `description`) + H1 of each `.md` file.
2. Never read full `.md` bodies on Pass 1.

## Stage 2: Controlled-Vocabulary Signature Bucketing ($O(N)$)
1. Assign each file a 3-part signature in a sorted table pass:
   `(Parent_Directory, Canonical_Action, Target_Resource)`
   - Normalize action verbs to a fixed taxonomy: `create`, `audit`, `edit`, `deploy`, `analyze`, `sync`, `convert`, `query`.
2. Group files sharing:
   - The same `Parent_Directory` (catches split-file skills like `SKILL.md` + `rubric.md` + `workflow.md`), OR
   - The same `(Canonical_Action, Target_Resource)`.
3. **Zero-Waste Exit**: Singletons exit at **0 extra tokens**. Any bucket with `> 6` items sub-splits by secondary noun/prefix before intra-bucket scoring.

## Stage 3: Deterministic `0–10` Mergeability Rubric (Flat Merge Gate)
Score each multi-item bucket (never across unrelated buckets):
- **`+4` Split-File / Dependency Coupling**: Shared subfolder without individual `SKILL.md`, `part-*`/`workflow`/`rubric` splits, or mutual cross-links.
- **`+3` Trigger Collision**: Frontmatter/H1s fire on the same user intent.
- **`+2` Shared Tool / Output Surface**: Both target the exact same artifact or toolset.
- **`+1` Context & Archive Fit**: Combined `SKILL.md` stays `<= 4,000` tokens and `< 90` archive entries.
- **`-10` Hard Veto**: Opposite trust/mutation roles (read-only auditor vs. writer), mutually exclusive guardrails (`staging` vs. `prod`), or incompatible platforms.

**Flat Merge Decision**:
- **Score `> 5` (`6–10`)**: Lazy-load bodies for that bucket and merge into one `SKILL.md` + namespaced `references/<source_stem>_*.md` (recording `merged_from` in `assets/local_manifest.json`).
- **Score `<= 5`**: Keep distinct. Evaluate the distinct skills under **Stage 4 (Mega-Skill Synthesis)** below.

## Stage 4: Mega-Skill Synthesis Gate (Preventing Library Overpopulation)
Even when skills are distinct (`Score <= 5`), installing 10–100+ skills individually clutters the user's Skills Manager and bloats top-level skill descriptions.

### Trigger Criteria
Trigger **Sharded Mega-Skill Synthesis** when a repository (or cohesive domain subset) has:
1. **`>= 4` distinct non-merged skills**, AND
2. **`>= 70%` Domain Cohesion** (e.g., all engineering, all video generation, all marketing, or all security).
   - *Multi-domain repos*: Group by primary domain first; emit **1 Mega-Skill per qualifying domain** (`>= 4` skills) rather than mixing unrelated domains.

### Sharded Mega-Skill Architecture (Modeled on `agency-orchestrator`)
1. **`SKILL.md` (Thin Router, `<= 150` lines)**: Lists the domain scope, routing rules, and a compact index pointing to `catalogue/index.json` and `references/shard-*.md`.
2. **`catalogue/index.json` (`O(1)` Metadata Index)**: Stores `id`, `slug`, `name`, `triggers`, `shard_file`, and `summary` for every bundled sub-skill so the model routes without loading shards.
3. **`references/shard-<subdomain>.md` (Lazy-Loaded Shards)**: Pack multiple sub-skills into shard files bounded by deterministic delimiters:
   `<!-- SKILL_RECORD_START id="<slug>" -->` ... `<!-- SKILL_RECORD_END id="<slug>" -->`
   - Keep total archive entries **`<= 90`** (safely under Gemini's 100-entry limit) and allow **only `.md` and `.json` files** (transcoding any external scripts into `_spec.md` sections inside the shard).
4. **`assets/local_manifest.json`**: Record `mega_skill: true` and `merged_from: [...]` for clean provenance.

## Stage 5: Plain-Language User Presentation
- Present merge & mega-skill recommendations in plain language (*"Found 48 video generation skills — I recommend combining them into 1 organized `video-studio-suite` Mega-Skill instead of adding 48 separate tools"*), grouped into a single concise approval prompt.
