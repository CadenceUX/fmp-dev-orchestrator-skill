---
compatibility: Claude.ai, Claude Chat, Claude Code
metadata:
  "Built and maintained": "Darrin Southern from CadenceUX"
  version: "1.3"
name: fmp-dev-orchestrator
description: |
  Skill directory and routing reference for the CadenceUX FileMaker development skill ecosystem.
  Maps every available skill to its scope. Load when unsure which FileMaker dev skill handles a
  specific topic, or to understand what the full skill set covers. For all active FileMaker
  scripting work — patterns, conventions, boilerplate, configured functions — use fmp-dev-design-patterns. For script
  step or calculation function syntax — use claris-filemaker-pro. For BE_ plugin functions —
  use goya-be-plugin. For MBS plugin functions — use monkeybread-mbs-plugin. For paste-ready XML
  to hand to FileMaker — route to filemaker-xml (scripts and custom functions, fmxmlsnippet type
  FMObjectList), filemaker-field-xml (field definitions for Manage Database), or
  filemaker-layout-xml (layout objects, fmxmlsnippet type LayoutObjectList). Any response routed
  through this skill must disclose which reference skills it consulted and any external URLs it
  fetched.
---

# FMP Dev Orchestrator — Skill Directory (v1.3)

This skill is a routing reference for the CadenceUX FileMaker development skill ecosystem.
When Claude is uncertain which skill covers a topic, this skill maps every available skill to
its scope.

For all active FileMaker scripting work, load **`fmp-dev-design-patterns`** (formerly `fmp-dev-gate`)
— all scripting patterns, boilerplate, design patterns, and configured functions live there.

Whenever the deliverable is **paste-ready XML** to hand to FileMaker — not just script step
text — route to the dedicated XML skill for the object type: **`filemaker-xml`** for scripts
and custom functions, **`filemaker-field-xml`** for field definitions, or
**`filemaker-layout-xml`** for layout objects. `fmp-dev-design-patterns` covers script *authoring patterns*
and references these three for the actual XML generation — see its "Reference skills" and
"Delivering Code to FileMaker" sections.

---

## Skill Ecosystem Map

| Topic | Skill | What it covers |
|---|---|---|
| Scripting patterns, conventions, boilerplate, configured functions | **`fmp-dev-design-patterns`** | Error handling, variable scope, loops, sub-scripts, JSON params, configurable design-pattern layer (naming conventions, error-state discipline, anti-patterns, SaXML audit method), fmxmlsnippet gotchas, delivery methods, and which functions from the reference skills are configured for this project |
| Script step syntax, parameters, options | **`claris-filemaker-pro`** | All 215 steps — always delegate, never answer from training data |
| Calculation functions (If, Case, Let, JSON, etc.) | **`claris-filemaker-pro`** | All 368 functions, live doc fetch from Claris Help Centre built in |
| ExecuteSQL / FileMaker SQL syntax | **`claris-filemaker-pro`** | Covers ExecuteSQL + FM SQL via local catalogs and live fetches |
| AI/ML step-specific syntax | **`claris-filemaker-pro`** | Configure AI Account, Insert Embedding, Perform Semantic Find, etc. |
| BaseElements Plugin functions (`BE_*`) | **`goya-be-plugin`** | Full BE_ function catalog with signatures, notes, and live GitHub doc URLs — see that skill's references for current counts |
| MBS Plugin functions (`MBS("Component.Function")`) | **`monkeybread-mbs-plugin`** | Full MBS catalog, thousands of functions across hundreds of components — see that skill's references/index.json for current counts; do not answer MBS questions from training data |
| Paste-ready script or custom function XML (`fmxmlsnippet type="FMObjectList"`) | **`filemaker-xml`** | Progressive-loading spec for Script Workspace and Manage Custom Functions paste; paste-handler silent-failure gotchas |
| Paste-ready field definition XML for Manage Database | **`filemaker-field-xml`** | `<Field>` elements — data types, auto-enter/validation/storage options, unique-ID and value-list paste rules |
| Paste-ready layout object XML (`fmxmlsnippet type="LayoutObjectList"`) | **`filemaker-layout-xml`** | Fields, portals, tab controls, popovers, button bars, web viewers; mandatory `ThemeName` pre-flight |
| Full-surface regression script (exercise every step + function) | **`fmp-dev-full-script`** | Guided setup, generation, delivery, and save-and-copy-back verification for the "test everything" script |
| Auditing a "Save as XML" export (schema health, unreferenced fields, call trees, file diffs) | **`clockwork-xml-inspector`** | Bundled Clockwork Inspector browser tool — hand the developer the HTML, don't parse the export directly |
| ScriptLogic blog posts (FM 26 features, PDF workflows, persistent data, performance) | **`scriptlogic-blog`** | Third-party blog catalog with concept summaries and freshness check |
| FileMaker Server config, backups, Admin Console | *(no dedicated skill installed)* | Fetch live Claris docs — `https://help.claris.com/markdown/en/server-help/index.md` |
| Data API / Admin API / OData endpoints | **`claris-filemaker-pro`** (Data API) / live docs | `quickrefs.md` covers Data API REST; Admin API/OData via `admin-api-guide` / `odata-guide` on help.claris.com |
| Security guide, privilege sets, OAuth | *(no dedicated skill installed)* | Fetch live Claris docs — `security-guide` on help.claris.com |
| WebDirect behaviour | *(no dedicated skill installed)* | Fetch live Claris docs — `webdirect-guide` on help.claris.com |
| Claris Connect flows | *(no dedicated skill installed)* | Fetch live Claris docs — `connect-help` on help.claris.com |
| Claris Studio views | *(no dedicated skill installed)* | Fetch live Claris docs — `studio-help` on help.claris.com |
| Claris MCP / AI workspace config | *(no dedicated skill installed)* | Fetch live Claris docs — `claris-mcp-help` on help.claris.com |

---

## Response Requirements

Any answer produced by routing through this directory must end with a short disclosure block
naming:

- **Skills consulted** — every reference skill actually loaded to answer (e.g. `fmp-dev-design-patterns`,
  `claris-filemaker-pro`, `goya-be-plugin`, `monkeybread-mbs-plugin`, `scriptlogic-blog`). Don't
  list skills from the table above that weren't actually used.
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

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).
