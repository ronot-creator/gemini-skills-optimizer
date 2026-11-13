# Gemini Skills Library (`ronot-creator/gemini-skills`)

A curated, local-first suite of Gemini Apps skills with **low-token, hash-verified self-updating** designed for non-technical users.

## Included Skills

- **`gemini-skill-factory` (v2.3.0)** — Inspects, audits, converts, and installs skills from GitHub repositories or ZIP archives, and checks `manifest.json` for delta-only updates.
- **`skill-lifecycle-guardian` (v1.1.0)** — Protects multi-file skill updates via Two-Step Pre-Staged + Write-Through Mirroring.
- **`llm-council` (v1.0.0)** — Convenes 5 independent AI advisors, anonymous randomized peer review, and a Chairman verdict for high-stakes decisions.
- **`agency-orchestrator` (v2.0.0)** — Coordinates specialized engineering, security, and research personas.

## How to Update (No Terminal Required)

Simply ask Gemini:
> `@gemini-skill-factory check for updates`

Gemini will read `manifest.json`, compare file hashes locally, download **only** changed files, verify SHA-256 integrity + static security rules, and apply updates safely in place.
