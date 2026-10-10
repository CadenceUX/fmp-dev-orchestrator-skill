---
name: fmp-dev-orchestrator
description: >-
  Routing directory for the CadenceUX Claris FileMaker skill set. Maps each FileMaker
  development topic to the skill or tool that owns it, including the Claris Agentic Development
  Toolkit (ADT) for anything that reads or changes the FileMaker file directly. Use when unsure
  which FileMaker skill handles a topic, when a FileMaker request spans several skills (a script
  that calls a plugin, a server install with OttoFMS), or to see what the skill set covers. Not
  for answering the FileMaker question itself; it hands off to the owning skill.
license: CC-BY-4.0
compatibility: >-
  Claude.ai, Claude Desktop, Cowork and Claude Code. Routes to ADT when the Claris Agentic
  Development Toolkit plugin is installed.
metadata:
  author: Darrin Southern, CadenceUX
  version: "2.0.0"
---

# FileMaker skill directory

Routes FileMaker work to the skill or tool that owns it. Load the owning skill and answer from
it; never answer catalog questions (syntax, plugin functions) from training data.

## Step 1: is ADT available?

Check whether the Claris Agentic Development Toolkit (ADT) plugin is installed (its skills, such
as `fm-mcp-guide` and `filemaker-help`, appear in the skill list, or its MCP tools are loaded).

- **ADT installed:** anything that reads or changes the FileMaker file goes through ADT:
  schema (tables, fields, relationships), scripts, layouts and layout objects, value lists,
  custom functions, SQL against live data, running scripts. ADT works on the file directly, so
  never generate clipboard XML or copy-paste snippets for these.
- **No ADT:** give the developer the steps, script text or calculation to enter by hand, and say
  that ADT can apply changes directly once installed.

## Step 2: route the topic

| Topic | Owner |
|---|---|
| Reading or changing the file: schema, scripts, layouts, value lists, custom functions, live SQL | **ADT** (start with `fm-mcp-guide`) |
| Calculation function syntax, parameters, return types, versions | **`claris-filemaker-pro`** |
| Script step syntax, options, platform support (Go, WebDirect, Server, Cloud, Data API) | **`claris-filemaker-pro`** |
| Field types and options, error codes, ExecuteSQL syntax, Data API, OData | **`claris-filemaker-pro`** |
| Scripting conventions: error handling, variables, loops, sub-scripts, JSON parameters, naming, anti-patterns | **`fmp-dev-design-patterns`** |
| BaseElements plugin functions (`BE_…`) | **`goya-be-plugin`** |
| MBS plugin functions (`MBS ( "Component.Function" … )`) | **`monkeybread-mbs-plugin`** |
| bBox plugin functions (`bBox_…`) | **`beezwax-bbox-plugin`** |
| FileMaker Server in Docker on macOS: install, upgrade, certificates | **`cadenceux-fms-docker-setup`** |
| OttoFMS on a Docker-hosted FileMaker Server | **`cadenceux-ottofms-docker-setup`** (needs `cadenceux-fms-docker-setup` first) |
| Building or updating a Claude skill | **`cadenceux-skill-creator`** (installed separately) |
| FileMaker Server administration, Admin API, security, WebDirect deployment, Claris Connect, Claris Studio | No dedicated skill: fetch the live guide from `https://help.claris.com/` |

For counts and versions, read the owning skill's own `VERSION` and catalog `meta` block; this
table deliberately carries none.

## Requests that span skills

Load each owning skill in turn. Common combinations:

- A script that calls a plugin: `fmp-dev-design-patterns` for structure, the plugin skill for
  the function, `claris-filemaker-pro` for the steps, ADT to write it into the file.
- A new server: `cadenceux-fms-docker-setup`, then `cadenceux-ottofms-docker-setup`.

## Disclosure

End every answer routed through this directory with:

- **Skills consulted:** only the skills actually loaded.
- **Tools and URLs:** ADT tools called and live pages fetched, or "answered from local
  reference files only".

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).
