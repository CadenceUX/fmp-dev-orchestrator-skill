# fmp-dev-orchestrator — Changelog

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
