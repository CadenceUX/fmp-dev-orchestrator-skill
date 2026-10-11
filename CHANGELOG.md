# fmp-dev-orchestrator — Changelog

## [2.1.1] — 2026-10-11

### Changed

- **No preview version numbers in published files.** Claris ADT, and the FileMaker Pro build it
  needs, are in Claris's preview programs. The stack check no longer compares against a
  published ADT version or FileMaker Pro minimum: it reads ADT's version, the FileMaker Pro
  minimum ADT states, and ADT's template package versions from the user's own install, and
  reports them only in the conversation. `versions.json` keeps public versions only.
- SKILL.md and the reference tell the agent never to write ADT or preview FileMaker Pro version
  numbers into files, commits or anything published. New eval case:
  no-preview-versions-published.
- 2.1.0's changelog, eval prompts and results rewritten without preview version numbers.

## [2.1.0] — 2026-10-11

Adds the stack check: is the FileMaker agentic stack current? Built with
`cadenceux-skill-creator` 2.0.0.

### Added

- **Step 0: stack check.** `scripts/stack_check.py` (standard library, read-only) reports:
  - installed CadenceUX skills against `versions.json` in the cadenceux-skills repo, including
    old copies the Claude desktop app keeps, retired skills to remove, and skills outside the
    set;
  - Claris ADT (no public ADT feed yet; it also looks for an ADT entry in the Claris updates
    feed, so a public comparison starts once Claris publishes one);
  - FileMaker Pro against the minimum ADT needs, with a note when the public feed lists an
    older version, plus Agent Access status from `adt doctor`;
  - the ADT project: the ADT version each web viewer app was created with, `AGENTS.md`
    freshness, `@adt/fmdapi` against what the installed ADT ships, TypeScript, Node and pnpm.
- `references/stack-check.md`: when to run it, the no-shell path, how to read each status, and
  the rule that nothing is updated without the user's yes.
- Four eval cases (stack-full, fmp-minimum, chat-no-shell, update-everything).

### Verified

- Evals on Haiku, Sonnet and Opus: 4/4 each (`evals/results-2026-10-11-v2.1.0.md`).
- Run on macOS against an ADT project created with an earlier ADT: found out-of-date skills in
  the desktop app, the project's instructions and `@adt/fmdapi` behind the installed ADT, and
  Agent Access off. About three seconds.

## [2.0.0] — 2026-10-11

Rebuilt for the Claris Agentic Development Toolkit (ADT) and Anthropic's skill authoring best
practices, using `cadenceux-skill-creator` 2.0.0.

### Changed

- **ADT first.** Anything that reads or changes the FileMaker file (schema, scripts, layouts,
  value lists, custom functions, live SQL) routes to ADT, which works on the file directly.
  No more clipboard XML or copy-paste snippets.
- Frontmatter to the CadenceUX standard (third-person description with "Use when" and "Not for",
  `license`, `metadata.author`); `.claude-plugin/plugin.json` added.
- The routing table carries no counts; each skill's own `VERSION` and catalog meta are the
  source.

### Added

- Routes for `beezwax-bbox-plugin`, `cadenceux-fms-docker-setup`,
  `cadenceux-ottofms-docker-setup` and `cadenceux-skill-creator`.
- "Requests that span skills" section; `evals/evals.json` (4 cases, 2 near-misses).

### Removed

- Routes to the XML skills (`filemaker-xml`, `filemaker-field-xml`, `filemaker-layout-xml`):
  ADT replaces clipboard XML.
- Routes to the retired `fmp-dev-full-script`, and to `clockwork-xml-inspector` and
  `scriptlogic-blog`, which aren't part of the CadenceUX skill set.
- The out-of-date step count (215; Claris now documents 216).

## v1.3 — 2026-07-05 (updated 2026-07-05, pre-release)

- **`fmp-dev-gate` renamed to `fmp-dev-design-patterns`** — every routing reference in the
  description, body, ecosystem map, and disclosure example updated; the row now describes its
  configurable design-pattern layer.
- **Plugin catalog counts made durable.** The BE and MBS rows previously quoted live counts
  that went stale whenever those catalogs were rebuilt (the MBS row still said "7,370
  functions across 233 components" after that skill's v1.3 grew to a larger catalog). Both
  rows now describe the catalogs without exact numbers and point at each skill's own
  reference files for current counts. The `claris-filemaker-pro` rows keep their exact
  counts (215 steps / 368 functions) deliberately — per Developer, that's the one reference
  where the routing table should state the numbers.

## v1.2 — 2026-07-01 (updated 2026-07-04)

### Fixed — 2026-07-04 accuracy pass (no version bump; v1.2 not yet on GitHub)

- **Removed dead routes to a `claris-help` skill that doesn't exist** in the installed skill
  set. Seven rows (Server admin, Data API/Admin API/OData, security, WebDirect, Claris Connect,
  Claris Studio, Claris MCP) routed to it; they now either point at real coverage
  (claris-filemaker-pro's quickrefs for the Data API) or say plainly that no dedicated skill is
  installed and give the live help.claris.com guide to fetch.
- **Added three installed skills missing from the "maps every available skill" table**:
  `fmp-dev-full-script` (full-surface regression script), `clockwork-xml-inspector`
  (Save as XML audits), and `scriptlogic-blog` (third-party FM blog catalog).
- **Step count corrected from 165 to 215**, matching the corrected claris-filemaker-pro catalog
  (verified against a full topic_type sweep of live Claris docs, 2026-07-04 — 215 steps exactly).
- Replaced `claris-help` with `scriptlogic-blog` in the Response Requirements example list.
- Added the standard attribution line to the Licence section.

Added the three FileMaker paste-ready XML skills to the routing table and description:
`filemaker-xml` (scripts and custom functions, `fmxmlsnippet type="FMObjectList"`),
`filemaker-field-xml` (field definitions for Manage Database), and `filemaker-layout-xml`
(layout objects, `fmxmlsnippet type="LayoutObjectList"`). These are distinct from the syntax/
function reference skills already listed — they cover the actual XML deliverable, not step or
function lookup. Added a body note directing any "generate paste-ready XML" request to the
correct object-specific skill instead of `fmp-dev-gate`'s own summary gotchas.

Reviewed `fmp-dev-gate` for sections that referenced XML generation without pointing to these
skills — its "Reference skills", "fmxmlsnippet Authoring Gotchas", and "Delivering Code to
FileMaker" sections were gated to delegate to the three skills above; see `fmp-dev-gate`
CHANGELOG v1.2 for the matching changes.

## v1.1 — 2026-06-30

Added a Response Requirements section: any answer routed through this directory must now
disclose which reference skills were actually consulted and any external URLs fetched (Claris
Help Centre, plugin GitHub doc pages, etc.), or explicitly state that none were fetched and the
answer came from local catalogs only.

## v1.0 — 2026-06-30

Initial release.

Skill directory and routing reference for the CadenceUX FileMaker development skill ecosystem.
Maps every available skill to its scope so Claude can route any FileMaker topic to the correct
skill. Contains no scripting content — all scripting patterns, boilerplate, and project
configuration live in `fmp-dev-gate`; step syntax and function reference live in the reference
skills (`claris-filemaker-pro`, `goya-be-plugin`, `monkeybread-mbs-plugin`).
