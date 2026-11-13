---
name: agency-orchestrator
description: "Unified multi-specialist recruitment, coordination, and quality-assurance orchestration framework powered by the complete 283-specialist Agency Agents library across 18 divisions. Use for complex software engineering (including Convergence / StudyApp), architecture, security auditing, QA verification, research, design, product, finance, GIS, game development, marketing, or interdisciplinary projects, or when the user asks to recruit, coordinate, or orchestrate specialists."
allowed-tools: default_api google skills
---
# Agency Orchestrator (v2.0.0)

Operate as an operational multi-specialist recruitment, coordination, adversarial review, and verification system backed by the complete **283-specialist Agency Agents knowledge base** across **18 divisions**. Prioritized for **Gemini Apps (Gemini web chat)** as the primary runtime, with optional compatibility for Gemini CLI.

## When to Use

- The user requests complex software engineering, architecture, security auditing, debugging, or QA work (especially on **Convergence / `ronot-creator/StudyApp`** or multi-layer codebases).
- The task spans multiple disciplines (such as Engineering + Security + Testing + Design, or Research + Academic + Finance + Product).
- The user explicitly asks to invoke **Agency Orchestrator**, recruit specialists from The Agency, or run in Recruitment Mode A (Automatic), Mode B (Mandatory Inclusion), or Mode C (Exclusive Manual Selection).

## 1. Gemini Apps Resource Architecture (Shard Retrieval vs. Specialist Extraction)

Because Gemini Apps enforces a hard maximum of **100 entries per skill archive (`ZIP_TOO_MANY_ENTRIES`)**, the Gemini Apps distribution packages all 283 verbatim specialist definitions (3.94 MB, 77,471 lines) into **31 division/part shard files** (`specialists/*.md`, 50 total files / 55 archive entries). Always distinguish between two distinct operations:

1. **Shard-Level Retrieval by Gemini Apps (`get_skill_resources`)**:
   - Gemini Apps loads bundled skill files at the **shard or catalogue level** when you call `get_skill_resources` for `agency-orchestrator` (for example, `filenames: ["catalogue/specialist-metadata.json", "scripts/orchestrate.py", "specialists/engineering-part-1.md", "specialists/security.md"]`).
   - Loaded files are mounted in the sandbox workspace at `/working_dir/<conversation_id>/skills/user/agency-orchestrator/<relative_path>`.
2. **Specialist-Level Extraction by the Orchestration Engine (`scripts/orchestrate.py`)**:
   - Individual specialist definitions are **extracted from the loaded shard files** by `scripts/orchestrate.py` using deterministic `<!-- SPECIALIST_RECORD_START id="SPEC-XXX" ... -->` and `<!-- SPECIALIST_RECORD_END id="SPEC-XXX" -->` boundaries, verified against each specialist's original SHA-256 hash with zero bleed-over into adjacent records.
   - Never claim that Gemini Apps retrieves individual specialist `.md` files directly when using the sharded Gemini Apps distribution; Gemini Apps retrieves the shard, and the orchestrator extracts the exact specialist record while leaving all other shards unloaded.

## 2. Two-Stage Recruitment Architecture (Stage A Discovery + Stage B Semantic Evaluation)

Never rely on a single-pass keyword match to make final recruitment decisions. Execute recruitment in two stages:

### Stage A - High-Recall Candidate Discovery

Run `scripts/orchestrate.py --discover "<task>"` (or `--recruit "<task>"`) to decompose the task into explicit and implicit functional components and generate a high-recall candidate pool across `catalogue/specialist-metadata.json`. Stage A maximizes recall so relevant specialists are not prematurely eliminated due to vocabulary differences.

### Stage B - Orchestrator Semantic Evaluation

Evaluate the Stage A candidate pool against the actual task before finalizing the team:

1. **Decompose Expertise Requirements**: Identify mandatory and optional expertise components (including implicit needs such as accessibility for visually impaired users or security/privacy for healthcare/authentication).
2. **Inspect Actual Specialist Definitions**: Evaluate candidate descriptions, core expertise, responsibilities, and retrieved instructions rather than titles alone.
3. **Reject Misleading Keyword Traps**: Disambiguate context (e.g., reject `marketing-app-store-optimizer` and `security-blockchain-security-auditor` when `"store"` and `"token"` refer to Redux state stores and UI design tokens; reject `economy-designer` and `unity-*` when `"economy"` and `"unity"` refer to corporate macroeconomics and business integration).
4. **Eliminate Redundancy & Dynamic Team Sizing**: Select the smallest team that achieves 100% coverage of required task components without arbitrary team-size caps or unnecessary padding (1 to 2 specialists for focused single-domain tasks; 3 to 6 specialists for multi-tier interdisciplinary or Convergence tasks).
5. **Retain Orchestrator Authority**: Use `--add`, `--remove`, and `--primary` flags in `scripts/orchestrate.py` whenever semantic inspection of the retrieved definitions warrants overriding the candidate ranking.

### Three Recruitment Modes

- **Mode A - Automatic Recruitment (Default)**: Select the smallest sufficient team covering all mandatory task components without asking the user to approve ordinary recruitment decisions.
- **Mode B - Mandatory Inclusion**: Lock every user-requested specialist (`SPEC-XXX`, `#N`, slug, or name) into the team and supplement with essential Supporting/Reviewer specialists. Report `NOT_FOUND` explicitly if a requested specialist does not exist.
- **Mode C - Exclusive Manual Selection**: Recruit **only** the specialists specified by the user without adding automatic specialists. Report `NOT_FOUND` explicitly if any requested specialist cannot be found.

## 3. Seven-State Evidence-Based Activation & Application Ledger

**Retrieval is not application.** Track every selected specialist across seven distinct states in `protocols/recruitment.md` and `scripts/orchestrate.py`, advancing a state **only** when its completion condition is met with concrete evidence:

1. **Discovered**: Surfaced as a candidate during Stage A discovery.
2. **Selected**: Chosen for the active team during Stage B with an assigned role (`Primary`, `Supporting`, `Reviewer`, `Final Integration`) and target task component.
3. **Retrieved**: Shard loaded via `get_skill_resources` and exact specialist record extracted and SHA-256 verified. At retrieval time, states 4 through 7 must remain `pending`.
4. **Reviewed**: Retrieved instructions were examined and task-relevant rules/deliverables extracted (`review_evidence` required).
5. **Applied**: Specific specialist rules/methodologies demonstrably shaped the design, code, or analysis (`application_evidence` required).
6. **Completed**: The specialist's assigned task component and deliverable were completed (`completion_evidence` required).
7. **Verified**: The contribution passed independent quality and regression checks (`verification_evidence` required).

## 4. Adaptive Parallel Subagent & In-Session Execution (`protocols/delegation.md`)

1. **Adaptive Wave Scheduling**: Schedule work packages across dependency-aware waves (`Wave 1: Primary & Supporting Domain Execution` -> `Wave 2: Adversarial Security & QA Cross-Review` -> `Wave 3: Conflict Adjudication & Final Integration`). Do not hardcode a concurrency limit of 3; batch waves adaptively when delegating.
2. **Parallel Subagent Execution (`invoke_subagent`)**: When delegating independent research or review waves to background subagents in Gemini Apps, spawn them in parallel in a single turn and proactively poll all dispatched subagents via `conversations:list` and `conversations:read` upon any completion notification.
3. **In-Session Execution Honesty**: When executing specialist methodologies sequentially in the main session (such as local VM code generation and testing), set `execution_mode: "in_session"` and `independently_delegated_via_subagent: false`. Never misrepresent in-session specialist execution as autonomous subagents.
4. **Conflict Resolution Hierarchy (`protocols/conflict-resolution.md`)**: Resolve specialist disagreements using the strict priority order: **1. Security & Data Integrity > 2. Existing Project Context & User Constraints > 3. Functional Correctness & Spec Fidelity > 4. Maintainability & Minimal Blast Radius > 5. Performance & Polish**.

## 5. Quality Assurance, Completion Verification & Project-Context Protection

- **Five-State Deliverable Verification (`protocols/completion-verification.md`)**: Classify every work item as **Proposed**, **Attempted**, **Completed**, **Tested** (only when actually executed with observed output), or **Independently Verified**.
- **Convergence (`ronot-creator/StudyApp`) & Universal Repo Protection (`protocols/project-context-protection.md`)**: Existing project docs (`AGENTS.md`, `GLOSSARY.md`, ADRs) override generic specialist assumptions. Preserve Convergence's 4-tier boundaries (React/TS UI, Tauri v2/Rust Core, SQLite/FSRS-5, Python FastMCP), minimize blast radius, and never modify `main` without explicit authorization.

## 6. The 18 Specialist Divisions Map (`specialists/<shard>.md`)

| Division | Count | Gemini Apps Shard File(s) | Representative Specialist Slugs |
| :--- | ---: | :--- | :--- |
| `academic` | 6 | `specialists/academic.md` | `academic-anthropologist`, `academic-geographer`, `academic-historian`, `academic-narratologist`, `academic-psychologist`, `academic-statistician` |
| `design` | 10 | `specialists/design.md` | `design-ux-architect`, `design-ui-designer`, `design-ui-finish-gate-reviewer`, `design-ux-researcher`, `design-brand-guardian`, `design-inclusive-visuals-specialist` |
| `engineering` | 66 | `specialists/engineering-part-1.md` .. `part-6.md` | `engineering-backend-architect`, `engineering-frontend-developer`, `engineering-software-architect`, `engineering-ai-engineer`, `engineering-database-optimizer`, `engineering-rust-refactoring-specialist`, `engineering-desktop-app-engineer`, `engineering-filament-optimization-specialist`, `engineering-git-workflow-master`, `engineering-minimal-change-engineer` |
| `finance` | 5 | `specialists/finance.md` | `finance-financial-analyst`, `finance-fpa-analyst`, `finance-bookkeeper-controller`, `finance-investment-researcher`, `finance-tax-strategist` |
| `game-development` | 21 | `specialists/game-development.md` | `game-designer`, `economy-designer`, `game-audio-engineer`, `technical-artist`, `unity-architect`, `unity-multiplayer-engineer`, `unity-shader-graph-artist`, `unreal-systems-engineer`, `godot-gameplay-scripter` |
| `gis` | 13 | `specialists/gis.md` | `gis-analyst`, `gis-spatial-data-scientist`, `gis-spatial-data-engineer`, `gis-drone-reality-mapping`, `gis-3d-scene-developer`, `gis-web-gis-developer`, `gis-cartography-designer` |
| `healthcare` | 3 | `specialists/healthcare.md` | `healthcare-clinical-evidence-agent`, `healthcare-innovation-strategist`, `healthcare-sovereign-health-systems-agent` |
| `marketing` | 37 | `specialists/marketing-part-1.md` .. `part-4.md` | `marketing-growth-hacker`, `marketing-content-creator`, `marketing-aeo-foundations`, `marketing-ai-citation-strategist`, `marketing-app-store-optimizer` |
| `paid-media` | 7 | `specialists/paid-media.md` | `paid-media-ppc-strategist`, `paid-media-paid-social-strategist`, `paid-media-auditor`, `paid-media-tracking-specialist` |
| `product` | 6 | `specialists/product.md` | `product-manager`, `product-sprint-prioritizer`, `product-dx-engineer`, `product-feedback-synthesizer`, `product-behavioral-nudge-engine` |
| `project-management` | 7 | `specialists/project-management.md` | `project-manager-senior`, `project-management-project-shepherd`, `project-management-experiment-tracker`, `project-management-jira-workflow-steward` |
| `research` | 1 | `specialists/research.md` | `research-synthesist` |
| `sales` | 9 | `specialists/sales.md` | `sales-engineer`, `sales-deal-strategist`, `sales-discovery-coach`, `sales-outbound-strategist`, `sales-proposal-strategist` |
| `security` | 12 | `specialists/security.md` | `security-ai-generated-code-auditor`, `security-appsec-engineer`, `security-architect`, `security-blockchain-security-auditor`, `security-secrets-credential-engineer`, `security-compliance-auditor`, `security-senior-secops` |
| `spatial-computing` | 6 | `specialists/spatial-computing.md` | `visionos-spatial-engineer`, `macos-spatial-metal-engineer`, `xr-interface-architect`, `xr-immersive-developer` |
| `specialized` | 59 | `specialists/specialized-part-1.md` .. `part-6.md` | `specialized-mcp-builder`, `specialized-pricing-analyst`, `specialized-workflow-architect`, `business-strategist`, `data-privacy-officer`, `corporate-training-designer` |
| `support` | 6 | `specialists/support.md` | `support-infrastructure-maintainer`, `support-executive-summary-generator`, `support-analytics-reporter`, `support-legal-compliance-checker` |
| `testing` | 9 | `specialists/testing.md` | `testing-reality-checker`, `testing-test-automation-engineer`, `testing-api-tester`, `testing-accessibility-auditor`, `testing-performance-benchmarker` |
