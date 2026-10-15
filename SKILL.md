---
name: fmp-dev-orchestrator
description: >-
  Routing directory and version check for the CadenceUX Claris FileMaker skill set. Maps each
  FileMaker development topic to the skill or tool that owns it, including the Claris Agentic
  Development Toolkit (ADT) for anything that reads or changes the FileMaker file, and reports
  whether the stack is current: CadenceUX skills, ADT, the FileMaker Pro version ADT needs, and
  the ADT project's packages. Use when unsure which FileMaker skill handles a topic, when a
  request spans several skills, at the start of FileMaker work in a session, or when asked
  whether skills, ADT or FileMaker are up to date. Not for answering the FileMaker question
  itself; it hands off to the owning skill.
license: CC-BY-4.0
compatibility: >-
  Claude.ai, Claude Desktop, Cowork and Claude Code. Routes to ADT when the Claris Agentic
  Development Toolkit plugin is installed. The full stack check needs Python 3 and a shell;
  without one it checks skill versions only.
metadata:
  author: Darrin Southern, CadenceUX
  version: "2.1.3"
---

# FileMaker skill directory

Routes FileMaker work to the skill or tool that owns it, and keeps the stack current. Load the
owning skill and answer from it; never answer catalog questions (syntax, plugin functions) from
training data.

## Step 0: stack check (once per session)

On the first FileMaker task in a session, run the read-only stack check, then carry on:

```bash
python3 <this skill's folder>/scripts/stack_check.py
```

It compares installed CadenceUX skills with `versions.json` in the cadenceux-skills repo, and
reports Claris ADT, FileMaker Pro against the minimum the installed ADT states, Agent Access,
and the ADT project's versions (`adtMetadata`, `@adt/fmdapi`, TypeScript, Node). ADT is in
Claris's preview programs: never write ADT or preview FileMaker Pro version numbers into files,
commits or anything published; report them only to the user, from their own install. Summarise in one or two
lines unless something needs action; give the full report when asked "is my stack up to date".
Never run an update, install or `adt components reconcile` without the user's yes. No shell
(claude.ai chat): check skill versions only, as described in the reference.

Reading the results, the Developer Preview caveats and the no-shell path:
[references/stack-check.md](references/stack-check.md).

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
| Building or updating a Claude skill | **`cadenceux-skill-creator`** (in the `cadenceux` marketplace: `cadenceux-skill-creator@cadenceux`) |
| Is the stack current: skills, ADT, FileMaker Pro version, ADT project packages | **This skill**, Step 0 |
| FileMaker Server administration, Admin API, security, WebDirect deployment, Claris Connect, Claris Studio | No dedicated skill: fetch the live guide from `https://help.claris.com/` |

For counts and versions, read the owning skill's own `VERSION` and catalog `meta` block, or
`versions.json`; this table deliberately carries none.

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
