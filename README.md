# fmp-dev-orchestrator

A [Claude skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
that routes Claris FileMaker work to the skill or tool that owns it. With the Claris Agentic
Development Toolkit (ADT) installed, anything that reads or changes the FileMaker file goes
through ADT directly, with no clipboard XML or copy-paste.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

## What it routes

| Topic | Owner |
|---|---|
| Schema, scripts, layouts, value lists, custom functions, live SQL | Claris ADT |
| Functions, script steps, field types, error codes, Data API, OData | `claris-filemaker-pro` |
| Scripting conventions and patterns | `fmp-dev-design-patterns` |
| BaseElements plugin | `goya-be-plugin` |
| MBS plugin | `monkeybread-mbs-plugin` |
| bBox plugin | `beezwax-bbox-plugin` |
| FileMaker Server in Docker | `cadenceux-fms-docker-setup` |
| OttoFMS in Docker | `cadenceux-ottofms-docker-setup` |
| Building Claude skills | `cadenceux-skill-creator` |
| Is the stack current | this skill (`scripts/stack_check.py`) |

It also checks the stack once per session: installed CadenceUX skills against the latest
releases, Claris ADT, the FileMaker Pro version ADT needs, and the ADT project's package
versions, all read from your own install. Read-only: it reports and asks, it never updates anything itself. Ask "is my
FileMaker stack up to date?" for the full report.

Topics with no dedicated skill (Server administration, security, Claris Connect, Claris Studio)
go to the live guides on help.claris.com.

## Install

**Claude Code** (from the `cadenceux` plugin marketplace):

```bash
claude plugin marketplace add https://github.com/CadenceUX/cadenceux-skills.git
claude plugin install fmp-dev-orchestrator@cadenceux
```

**claude.ai and Cowork:** Customize → Plugins → Add marketplace from GitHub →
`CadenceUX/cadenceux-skills`, then install **fmp-dev-orchestrator**.

**Claude desktop app (macOS):** download [`fmp-dev-orchestrator.skill`](https://github.com/CadenceUX/fmp-dev-orchestrator-skill/releases/latest/download/fmp-dev-orchestrator.skill) and
double-click it.

**Claude.ai in a browser, as a single skill:** Customize → Skills → upload
[`fmp-dev-orchestrator.zip`](https://github.com/CadenceUX/fmp-dev-orchestrator-skill/releases/latest/download/fmp-dev-orchestrator.zip).

> Both files are attached to the latest [release](https://github.com/CadenceUX/fmp-dev-orchestrator-skill/releases).
> Don't use GitHub's green **Code → Download ZIP** button or a release's **Source code (zip)**:
> those are snapshots of the repository, not a packaged skill, and Claude won't install them
> as one.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it, fork it, adapt it. Attribute it.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).
