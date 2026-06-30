---
compatibility: Claude.ai, Claude Chat, Claude Code
metadata:
  "Built and maintained": "Darrin Southern from CadenceUX"
  version: "1.1"
name: fmp-dev-orchestrator
description: |
  Skill directory and routing reference for the CadenceUX FileMaker development skill ecosystem.
  Maps every available skill to its scope. Load when unsure which FileMaker dev skill handles a
  specific topic, or to understand what the full skill set covers. For all active FileMaker
  scripting work — patterns, boilerplate, configured functions — use fmp-dev-gate. For script
  step or calculation function syntax — use claris-filemaker-pro. For BE_ plugin functions —
  use goya-be-plugin. For MBS plugin functions — use monkeybread-mbs-plugin. Any response routed
  through this skill must disclose which reference skills it consulted and any external URLs it
  fetched.
---

# FMP Dev Orchestrator — Skill Directory (v1.1)

This skill is a routing reference for the CadenceUX FileMaker development skill ecosystem.
When Claude is uncertain which skill covers a topic, this skill maps every available skill to
its scope.

For all active FileMaker scripting work, load **`fmp-dev-gate`** — all scripting patterns,
boilerplate, configured functions, and project rules live there.

---

## Skill Ecosystem Map

| Topic | Skill | What it covers |
|---|---|---|
| Scripting patterns, boilerplate, configured functions | **`fmp-dev-gate`** | Error handling, variable scope, loops, sub-scripts, JSON params, fmxmlsnippet gotchas, delivery methods, and which functions from the reference skills are configured for this project |
| Script step syntax, parameters, options | **`claris-filemaker-pro`** | All 165 steps — always delegate, never answer from training data |
| Calculation functions (If, Case, Let, JSON, etc.) | **`claris-filemaker-pro`** | All 368 functions, live doc fetch from Claris Help Centre built in |
| ExecuteSQL / FileMaker SQL syntax | **`claris-filemaker-pro`** | Covers ExecuteSQL + FM SQL via local catalogs and live fetches |
| AI/ML step-specific syntax | **`claris-filemaker-pro`** | Configure AI Account, Insert Embedding, Perform Semantic Find, etc. |
| BaseElements Plugin functions (`BE_*`) | **`goya-be-plugin`** | 129 active BE_ functions — full catalog with signatures, notes, and live GitHub doc URLs |
| MBS Plugin functions (`MBS("Component.Function")`) | **`monkeybread-mbs-plugin`** | 7,370 functions across 233 components — do not answer MBS questions from training data |
| FileMaker Server config, backups, Admin Console | **`claris-help`** | `server-help` guide |
| Data API / Admin API / OData endpoints | **`claris-help`** | `data-api-guide`, `admin-api-guide`, `odata-guide` |
| Security guide, privilege sets, OAuth | **`claris-help`** | `security-guide` guide |
| WebDirect behaviour | **`claris-help`** | `webdirect-guide` guide |
| Claris Connect flows | **`claris-help`** | `connect-help` guide |
| Claris Studio views | **`claris-help`** | `studio-help` guide |
| Claris MCP / AI workspace config | **`claris-help`** | `claris-mcp-help` guide |

---

## Response Requirements

Any answer produced by routing through this directory must end with a short disclosure block
naming:

- **Skills consulted** — every reference skill actually loaded to answer (e.g. `fmp-dev-gate`,
  `claris-filemaker-pro`, `goya-be-plugin`, `monkeybread-mbs-plugin`, `claris-help`). Don't list
  skills from the table above that weren't actually used.
- **External URLs fetched** — every live doc URL (Claris Help Centre, plugin GitHub doc pages,
  etc.) retrieved while answering, not just the static catalog entries already cached locally.

If no live fetch occurred and the answer came entirely from local catalogs, say so explicitly
rather than omitting the line — the developer needs to know whether the answer reflects the
latest published docs or a cached snapshot.

---

## Version History

See [`CHANGELOG.md`](./CHANGELOG.md) for the full version history.

---

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
