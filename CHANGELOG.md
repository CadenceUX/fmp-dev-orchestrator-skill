# fmp-dev-orchestrator — Changelog

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
