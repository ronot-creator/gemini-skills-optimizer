# 4-Source Synthesis & Mode E Autonomous Discovery (`v3.2.0`)

`gemini-skill-factory` operates as a universal **4-Source Pure-Markdown Skill Factory** with **Mode E Autonomous Discovery**. Every synthesized skill must remain **100% Pure-Markdown, Chat-Safe** (`.md` and `.json` only; zero `.py`/`.sh`/`.js`/`.ts` or `scripts/`).

---

## Part 1: The 4-Source Synthesis Matrix

| Source | Input Types | Ingestion & Synthesis Strategy | Verification & Gate |
| :--- | :--- | :--- | :--- |
| **Source 1: Pre-Packaged Skills & Archives** | GitHub skill repos, `npx skills add <owner>/<repo>`, `.claude/commands/*.md`, `.cursorrules`, Drive/uploaded `.zip` | Metadata-first $O(N)$ tree scan -> raw `SKILL.md` fetch -> script-to-Markdown transcoding (`references/transcoding_rules.md`) -> $O(N)$ Mergeability / Mega-Skill pass (`references/merge_strategy.md`). | Static Security Gate + Portability Lint + Cross-Reference (`A–E`). |
| **Source 2: General Codebases & Technical Docs** | Software repos without `SKILL.md`, `README.md`, API/CLI specs, architecture docs | Distill core workflows, commands, schemas, and guardrails into `SKILL.md` + modular `references/*.md` (never dump raw source code). | Verify all commands/flags against fetched docs; transcode any CLI/script examples into Markdown specs. |
| **Source 3: Generic Material** | Unstructured prompts, rubrics, SOPs, study guides, checklists, notes, or pasted workflows | Extract **Trigger Conditions**, **Non-Negotiable Constraints**, **Step-by-Step Execution**, **Edge Cases**, and **Output Templates** into `SKILL.md` + `references/`. | Confirm no missing required inputs; keep instructions concrete, deterministic, and free of filler. |
| **Source 4: Conversational Experience & Retrospectives** | Lessons, bug fixes, edge cases, grouping/fact-checking safety nets, or workflow refinements discovered in an active chat | Distill only **verified, reproducible root-cause rules** into either a new skill or a targeted patch to an existing skill. | **Explicit Retrospective Gate** (see Part 2 below). |

---

## Part 2: Source 4 — Explicit Retrospective Gate (Council-Hardened)

To prevent transient chat noise or hallucinated workarounds from corrupting permanent instructions:

1. **Root-Cause Verification**: Only propose rules backed by an observed failure, edge case, or explicit user correction in the conversation (e.g., *"346 expected vs 313 generated questions -> add count-parity check"*, *"mark-scheme errors -> enforce independent scientific fact-checking"*).
2. **Staging & Tiny Human-Readable Diff**: Never silently mutate an existing `SKILL.md`. Present a concise **Retrospective Patch Preview** (Schema 5 in `references/output_schemas.md`) showing:
   - Target skill (`New` or `Update <skill-name>`)
   - Exact problem observed
   - Exact 1–5 line rule/safety net to add (or diff summary)
3. **User Confirmation**: Wait for explicit user approval (`Apply`, `Yes`, or edits) before calling `skill-lifecycle-guardian` to persist the change.

---

## Part 3: Mode E — Autonomous Skill Discovery (`skills.sh` & GitHub)

Inspired by and crediting [`vercel-labs/skills`](https://github.com/vercel-labs/skills) and [`skills.sh`](https://skills.sh/), **Mode E** discovers high-signal community skills on demand when the user describes a capability need rather than providing a URL.

### Execution Protocol (Zero-Bloat, Raw-Verified)

1. **Query Formulation**: Issue targeted `google:search` queries across:
   - `site:skills.sh <capability keywords>`
   - `site:github.com "SKILL.md" <capability keywords>`
   - `site:github.com "vercel-labs/skills" OR "agent-skills" <capability keywords>`
2. **Raw-File Verification (Mandatory)**:
   - Never score, rank, or transcode from search snippets alone.
   - Fetch the actual `SKILL.md` / repository tree using `google:browse` or raw GitHub URLs before evaluating.
   - Discard dead links, empty stubs, or repos failing the Static Security Gate (`references/transcoding_rules.md`).
3. **Rank & Cross-Reference**:
   - Score top candidates (up to 5) on **Domain Fit**, **Completeness**, **Portability**, and **Overlap Category (`A–E`)** against the user's installed library.
   - If a user wants a standalone discovery skill, `gemini-skill-factory` can also synthesize [`vercel-labs/skills`](https://github.com/vercel-labs/skills) into a dedicated `find-skills` Pure-Markdown skill.
4. **Present Mode E Discovery Report**:
   - Render **Schema 4 (`references/output_schemas.md`)** and ask the user which candidate(s) to import, merge, or inspect further (unless the user explicitly requested immediate auto-import of the top vetted match).
