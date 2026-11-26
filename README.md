# fmp-dev-orchestrator

A [Claude skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
that selects the skills for agentic Claris FileMaker work, with or without Claris's FileMaker
Agentic Development Kit (ADK). For each task it names the skill or ADK tool that owns it, and it
checks your stack is current.

It works with [`cadenceux-developer-experience`](https://github.com/CadenceUX/cadenceux-developer-experience-skill),
which runs the work: the stages, the thinking hats, the gates before deploy and the decisions
around the code. This skill selects; that one directs. Install both.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

## What it does

**Selects the skill.** Anything that reads or changes the FileMaker file goes through ADK when
it's available. Everything else goes to the skill that owns it, with its install line if it's
missing:

| Topic | Owner |
|---|---|
| Schema, scripts, layouts, value lists, custom functions, live SQL, web viewer apps, standards | Claris ADK |
| How the work runs (stages, hats, gates) and the decisions around the code | `cadenceux-developer-experience` |
| Functions, script steps, error codes, Data API, OData, ExecuteSQL | `claris-filemaker-pro` |
| CadenceUX conventions and patterns, client standards | `fmp-dev-design-patterns` with the [`cadenceux` pack](https://github.com/CadenceUX/cadenceux-filemaker-standards) |
| BaseElements, MBS and bBox plug-ins | `goya-be-plugin`, `monkeybread-mbs-plugin`, `beezwax-bbox-plugin` |
| FileMaker Server and OttoFMS in Docker | `cadenceux-fms-docker-setup`, `cadenceux-ottofms-docker-setup` |
| Server security checks | `cadenceux-fms-security` |
| GitHub, and scanning skills before you install them | `cadenceux-github` |
| Building Claude skills; hooks that enforce a rule | `cadenceux-skill-creator`; `cadenceux-plugin-creator` |

It plans requests that span several skills (a plug-in script, a new server, a web viewer app,
putting changes live) and says which skills it consulted.

**Checks the stack**, once per session and read-only: installed CadenceUX skills, ADK against
Claris's latest, FileMaker Pro against ADK's minimum (26.1; hosted files need FileMaker Server
26.1.1), and your ADK project's standards pack and packages. Ask "is my FileMaker stack up to
date?" for the full report. It never updates anything without asking.

## Install

**Claude Code** (from the `cadenceux` plugin marketplace):

```bash
claude plugin marketplace add https://github.com/CadenceUX/cadenceux-skills.git
claude plugin install fmp-dev-orchestrator@cadenceux
```

Install `cadenceux-developer-experience@cadenceux` alongside it: that skill runs the work, this one selects the skills. If `cadenceux-dx` is still installed, uninstall it.

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
