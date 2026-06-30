# fmp-dev-orchestrator

Skill directory and routing reference for the CadenceUX FileMaker development skill ecosystem.
Maps every available skill to its scope so Claude can route any FileMaker topic to the correct
skill. Contains no scripting content of its own.

Current version: **v1.1** — see [CHANGELOG.md](./CHANGELOG.md) for full version history.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

## What it does

Routes FileMaker topics to the right skill. When Claude is uncertain which skill handles a
topic, this skill provides the map. As of v1.1, any response routed through this skill must
disclose which reference skills it consulted and any external URLs it fetched.

## What it does NOT contain

No scripting patterns, boilerplate, or rules — those all live in `fmp-dev-gate`. No function
or step reference data — that lives in the reference skills below.

## Skill ecosystem

| Skill | What it covers |
|---|---|
| `fmp-dev-gate` | All scripting patterns, boilerplate, and project-configured functions |
| `claris-filemaker-pro` | Script step syntax, calculation functions, ExecuteSQL |
| `goya-be-plugin` | BaseElements Plugin `BE_*` functions |
| `monkeybread-mbs-plugin` | MBS Plugin functions |
| `claris-help` | FileMaker Server, Data API, security, WebDirect, Connect, Studio |

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
