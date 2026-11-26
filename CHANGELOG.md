# fmp-dev-orchestrator: Changelog

## [4.0.0] - 2026-11-27

The skill selector again, on its own: it picks the skill or ADK tool for each task and checks
the stack. Running the work (stages, thinking hats, gates before deploy) and the decisions
around the code belong to `cadenceux-developer-experience`, which replaces `cadenceux-dx`.
Major version because the decision guides and the way of working move out.

### Changed

- No longer generated from another repo: this repo is the source again.
- SKILL.md: Steps 0 to 2 (stack check, is ADK available, select the skill), requests that span
  skills, disclosure. The routing table sends how the work runs, and the decisions around the
  code, to `cadenceux-developer-experience`.
- `scripts/stack_check.py` and `references/stack-check.md` are the latest from
  `cadenceux-developer-experience` 2.0.0, with this skill's name.

### Added

- **Installing an owning skill:** whenever it names a skill, it gives the install line from the
  `cadenceux` marketplace, instead of declining to guess the command.
- Routes for putting changes live (`cadenceux-developer-experience` for the gates,
  `cadenceux-fms-security` for the server) and for `cadenceux-plugin-creator`.

### Removed

- The decision guides (`before-adk.md`, `data-access.md`, `linter-tests.md`,
  `native-webviewer-hybrid.md`, `reviewing-systems.md`, `security-deployment.md`) and
  `working-agentically.md`: they stay in `cadenceux-developer-experience`.
- "The same skill as cadenceux-dx": it isn't any more.

### Verified

- Evals: see `evals/results-2026-11-27-v4.0.0.md`, against the released 3.0.2.

## [3.0.2] — 2026-11-24

Back in service as the same skill as [`cadenceux-dx`](https://github.com/CadenceUX/cadenceux-dx-skill)
1.0.2, under its earlier name, so the installs and links that name `fmp-dev-orchestrator` get
the full skill rather than a pointer to install another one.

### Changed

- SKILL.md, `references/`, `scripts/` and `evals/evals.json` are now generated from the
  cadenceux-dx repo by its `maintainer/build_orchestrator.py`. Only the name, version,
  self-check links and the relationship note differ. Everything 2.1.3 did is there, rewritten
  for Claris's ADK, plus the decision guides and Windows support in the stack check.
- Version numbers follow cadenceux-dx's with the major number plus 2 (dx 1.0.2 is 3.0.2), so the
  pair's releases line up.
- If both skills are loaded, this one defers to `cadenceux-dx`, and both suggest uninstalling
  one. The stack check notes when both are installed and doesn't list either as missing while
  the other is there.
- `versions.json` lists this skill again (it was on the `retired` list), so the stack check no
  longer reports it as `REMOVE`.

### Verified

- Evals: `orchestrator-same-skill` passes on Haiku, Sonnet and Opus for both fmp-dev-orchestrator
  3.0.2 and cadenceux-dx 1.0.2 (the released versions fail it on Sonnet), and this copy passes
  `add-field-adk` on all three; see `evals/results-2026-11-24-v3.0.2.md`.
- Stack check run on macOS against the new `versions.json`; the both, one and neither cases
  tested.
- `validate_skill.py` clean; `cadenceux-github` scanners clean.

## [2.2.0] — 2026-11-19

Retired. Replaced by [`cadenceux-dx`](https://github.com/CadenceUX/cadenceux-dx-skill) 1.0.0,
which carries this skill's routing and stack check, rewritten for Claris's FileMaker Agentic
Development Kit (ADK), plus decision guides for agentic FileMaker work.

### Changed

- SKILL.md now only tells the user to install `cadenceux-dx` and remove this skill.
- `references/` and `scripts/` removed; their successors are in `cadenceux-dx`.
- `versions.json` lists this skill as retired, so the stack check reports it as `REMOVE`.

## [2.1.3] — 2026-10-16

Packaging fix for GitHub installs, using `cadenceux-skill-creator` 2.1.2. No change to the skill's instructions or reference data.

### Fixed

- **GitHub source zips no longer install as a plugin.** The repository root carries
  `.claude-plugin/plugin.json` for the plugin marketplace, so GitHub's **Code → Download
  ZIP** and a release's **Source code (zip)** looked like a plugin to the Claude desktop app,
  which pointed to the plugin installer instead of installing the skill. A new `.gitattributes`
  leaves `.claude-plugin/`, `evals/`, `maintainer/` and the git dotfiles out of those archives.
  The marketplace is unaffected: it reads the repository, not the archive.

### Changed

- README install section links straight to the latest release's `.skill` and `.zip`, and
  warns against the source zips.
- Each release now also attaches unversioned copies (`<name>.skill`, `<name>.zip`) so the
  README's `releases/latest/download/…` links don't change between versions.

### Verified

- `validate_skill.py` clean on the folder and on both release archives.
- Evals not re-run: no instruction or data change since the last run.

## [2.1.2] — 2026-10-12

### Changed

- **`cadenceux-skill-creator` is in the `cadenceux` marketplace.** The routing table no longer
  calls it a separate install and gives its plugin name (`cadenceux-skill-creator@cadenceux`).
  `versions.json` lists it with the other skills; the stack check still reads the old
  `separate_installs` key, so older marketplace copies keep working.
- New eval case: skill-creator-route, passed on Haiku 5.5, Sonnet 5.5 and Opus 5.5
  (`evals/results-2026-10-12-v2.1.2.md`).

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
