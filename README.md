# fmp-dev-orchestrator

Skill directory and routing reference for the CadenceUX FileMaker development skill ecosystem.
Maps every available skill to its scope so Claude can route any FileMaker topic to the correct
skill. Contains no scripting content of its own.

Current version: **v1.2** — see [CHANGELOG.md](./CHANGELOG.md) for full version history.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

## What it does

Routes FileMaker topics to the right skill. When Claude is uncertain which skill handles a
topic, this skill provides the map. As of v1.1, any response routed through this skill must
disclose which reference skills it consulted and any external URLs it fetched. As of v1.2, the
map also covers the three dedicated skills that generate actual paste-ready XML, not just step
or function syntax.

## What it does NOT contain

No scripting patterns, boilerplate, or rules — those all live in `fmp-dev-design-patterns`. No function
or step reference data — that lives in the reference skills below. No XML generation logic of
its own — that lives in the three XML skills below.

## Skill ecosystem

| Skill | What it covers |
|---|---|
| `fmp-dev-design-patterns` | All scripting patterns, conventions, boilerplate, and project-configured functions |
| `claris-filemaker-pro` | Script step syntax, calculation functions, ExecuteSQL |
| `goya-be-plugin` | BaseElements Plugin `BE_*` functions |
| `monkeybread-mbs-plugin` | MBS Plugin functions |
| `filemaker-xml` | Paste-ready script/custom function XML (`fmxmlsnippet type="FMObjectList"`) |
| `filemaker-field-xml` | Paste-ready field definition XML for Manage Database |
| `filemaker-layout-xml` | Paste-ready layout object XML (`fmxmlsnippet type="LayoutObjectList"`) |
| `fmp-dev-full-script` | Full-surface regression script exercising every step and function |
| `clockwork-xml-inspector` | Auditing FileMaker "Save as XML" exports (schema health, call trees, diffs) |
| `scriptlogic-blog` | ScriptLogic FileMaker blog catalog (FM 26 features, PDF, persistent data) |

Topics with no dedicated skill (FileMaker Server admin, security/privilege sets, WebDirect,
Claris Connect, Claris Studio, Claris MCP) route to live help.claris.com guides — see the
routing table in SKILL.md.

## Files

```
fmp-dev-orchestrator/
├── SKILL.md         — the skill itself
├── VERSION          — bare version string
├── CHANGELOG.md     — version history
└── README.md        — this file
```

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, adapt, and redistribute with attribution.
