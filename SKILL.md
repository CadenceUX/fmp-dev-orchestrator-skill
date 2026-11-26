---
name: fmp-dev-orchestrator
description: >-
  Selects the skill or tool for each Claris FileMaker task, with or without Claris's Agentic
  Development Kit (ADK), and checks the stack is current. Maps each task to the CadenceUX skill
  or ADK tool that owns it, gives the install line for an owning skill that's missing, plans
  requests that span several skills, and runs a read-only check of installed CadenceUX skills,
  ADK, the FileMaker Pro version ADK needs and the ADK project. Use when unsure which skill
  handles a FileMaker task, when a request spans several skills, at the start of FileMaker work
  in a session, or when asked whether skills, ADK or FileMaker are up to date. Not for answering
  the FileMaker question itself, or for running the work (stages, gates, decisions): it hands
  those to the owning skill and to cadenceux-developer-experience.
license: CC-BY-4.0
compatibility: >-
  Claude.ai, Claude Desktop, Cowork and Claude Code, and any harness that reads skills. The
  full stack check needs Python 3 and a shell; without one it checks skill versions only.
metadata:
  author: Darrin Southern, CadenceUX
  version: "4.0.0"
---

# FileMaker Skill Orchestrator

Selects the skills for agentic FileMaker work. For each task it names the skill or ADK tool that
owns it, and it keeps the stack current. It doesn't answer the FileMaker question and it doesn't
run the work: load the owning skill for the answer, and `cadenceux-developer-experience` for
how the work runs (stages, thinking hats, gates before deploy, and the decisions around the
code). Never answer catalog questions (syntax, plug-in functions) from training data.

## Requirements

| Kind | Name | Used for | Surfaces |
|---|---|---|---|
| CLI | `python3` | `scripts/stack_check.py` | Claude Code or any harness with a shell |
| CLI | `adk`, `filemaker` (ADK, optional) | ADK health, standards and project checks | Any harness with a shell |
| CLI | `claude` | Installing an owning skill from the `cadenceux` marketplace, on the user's yes | Claude Code |
| API | `raw.githubusercontent.com`, `downloads.claris.com`, `www.claris.com` (public, no key) | `versions.json`, Claris's ADK manifest, Claris's updates feed | Any surface that can fetch |
| Path | `~/.claude/plugins`, the Claude app's data folder, ADK's folder (`~/Library/Application Support/ADK` on macOS, `%LOCALAPPDATA%\ADK` on Windows) | Finding installed skills and ADK | Claude Code |

## Step 0: stack check (once per session)

On the first FileMaker task in a session, run the read-only stack check, then carry on:

```bash
python3 <this skill's folder>/scripts/stack_check.py
```

It compares installed CadenceUX skills with `versions.json`, checks ADK against Claris's ADK
manifest and `adk doctor`, FileMaker Pro against ADK's minimum (26.1) and Claris's public
release, and the ADK project in the working folder (its standards pack and web viewer apps).
Summarise in one or two lines unless something needs action; give the full report when asked
"is my stack up to date". Never run an update, install or `adk components reconcile` without
the user's yes. No shell: check skill versions only. Reading the results:
[references/stack-check.md](references/stack-check.md).

## Step 1: is ADK available?

ADK is available when any of these is true: the session lists `filemaker-agentic-development:`
skills (`fm-mcp-guide`, `filemaker-help`); MCP tools whose names contain `adk-mcp` are loaded (in
any harness: Claude Code, Cursor, Codex, Gemini CLI); or `adk --version` runs.

- **ADK available:** anything that reads or changes the FileMaker file goes through ADK: schema,
  scripts, layouts and layout objects, value lists, custom functions, SQL against live data,
  running scripts, standards. Never generate clipboard XML or copy-paste snippets for these.
- **No ADK:** give the developer the steps, script text or calculation to enter by hand. ADK
  needs FileMaker Pro 26.1 or later; for 26.0.3 and earlier, `cadenceux-developer-experience`
  guides what a job needs and when to upgrade.

## Step 2: select the skill

| Task | Owner |
|---|---|
| Reading or changing the file: schema, scripts, layouts, value lists, custom functions, live SQL, running scripts | **ADK** (`fm-mcp-guide`, `fm-cli`) |
| ADK projects and web viewer apps | **ADK** (`adk-project-setup`, `adk-webviewer-app`) |
| Which naming and design rules apply, and following a standards pack | **ADK** (`filemaker-standards`, `adk standards`) |
| How the work runs: which stage, the thinking hats, hand-backs, sprint plans and logs, the gates before deploy, estimates | **`cadenceux-developer-experience`** |
| Decisions around the code: native or web viewer, ExecuteSQL or relationships or the Data API, FileMaker 26.0.3 and earlier, reviewing a system, linter tests, security and deployment review | **`cadenceux-developer-experience`** |
| CadenceUX conventions, writing and reviewing scripts, a client's own standards | **`fmp-dev-design-patterns`** (with the `cadenceux` pack, `cadenceux-filemaker-standards@cadenceux`) |
| Function and script step syntax, versions, platform support, FileMaker 26.1 additions, Data API, OData, ExecuteSQL, error codes | **`claris-filemaker-pro`** |
| BaseElements (`BE_…`), MBS (`MBS ( "…" )`), bBox (`bBox_…`) functions | **`goya-be-plugin`**, **`monkeybread-mbs-plugin`**, **`beezwax-bbox-plugin`** |
| FileMaker Server in Docker on macOS; OttoFMS on it | **`cadenceux-fms-docker-setup`**; **`cadenceux-ottofms-docker-setup`** |
| Security check of a FileMaker Server: exposure, CVEs, accounts, logs, backups | **`cadenceux-fms-security`** |
| GitHub: publishing skills, known attacks on accounts and repos, scanning skills before install | **`cadenceux-github`** |
| Building or updating a Claude skill | **`cadenceux-skill-creator`** |
| A hook or plugin that enforces a rule (such as never changing a linter test with the code it checks) | **`cadenceux-plugin-creator`** |
| Is the stack current | **This skill**, Step 0 |
| FileMaker Server administration beyond these, Admin API, Claris Connect, Claris Studio | No dedicated skill: fetch the live guide from `https://help.claris.com/` |

For naming and conventions, ADK's `filemaker-standards` resolves which rules apply (Baseline,
then the project's pack, then the project's own); `fmp-dev-design-patterns` supplies the
`cadenceux` pack and how to write and review scripts to it. Change the file with ADK's tools as
`fm-mcp-guide` describes, and `fm-cli` for schema and layout edits it routes there.

For counts and versions, read the owning skill's `VERSION` and catalog `meta`, or
`versions.json`; this table carries none.

## Installing an owning skill

Every CadenceUX skill in the table installs from the `cadenceux` marketplace. Whenever you name
a skill to use, give its install line too, in case it isn't installed; don't answer in its place:

```bash
claude plugin marketplace add https://github.com/CadenceUX/cadenceux-skills.git
claude plugin install <skill-name>@cadenceux
```

On claude.ai and Cowork: Customize → Plugins → Add marketplace from GitHub →
`CadenceUX/cadenceux-skills`, then install the skill. ADK and its skills come from Claris, not
this marketplace. Ask before running an install.

## Requests that span skills

Load each owning skill in turn. Common combinations:

- A script that calls a plug-in: `fmp-dev-design-patterns` for structure, the plug-in skill for
  the function, `claris-filemaker-pro` for the steps, ADK to write it into the file.
- A new server: `cadenceux-fms-docker-setup`, then `cadenceux-ottofms-docker-setup`, then
  `cadenceux-fms-security`.
- A web viewer app: `cadenceux-developer-experience` to decide native, web viewer or both
  first, then ADK's `adk-webviewer-app`, with `claris-filemaker-pro` for the scripts it calls.
- Putting changes live: `cadenceux-developer-experience` for the gates before deploy (QA
  testing, review, the release checklist), and `cadenceux-fms-security` for the server side of
  the security sweep.

## Disclosure

End every answer routed through this skill with:

- **Skills consulted:** only the skills actually loaded.
- **Tools and URLs:** ADK tools called and live pages fetched, or "answered from local
  reference files only".

## Skill update self-check

The stack check covers this skill: it reports the running copy against `versions.json`. With no
shell, fetch `https://github.com/CadenceUX/fmp-dev-orchestrator-skill/raw/main/VERSION` once
per session and, if it's newer than 4.0.0, start the answer with:

> ⚠️ **Skill update available:** this skill is v[installed]; v[latest] is at
> https://github.com/CadenceUX/fmp-dev-orchestrator-skill/releases

Skip silently if the fetch fails.

## Relationship to other skills

- **`cadenceux-developer-experience`** runs the work; this skill selects the skills. In its
  model the Orchestrator (the Developer) chooses the skill and the thinking for each stage:
  this skill answers the "which skill" half. They're separate skills that work together:
  install both. The stack check and routing moved here from it in its 3.0.0; when either
  skill changes its routing or the decisions it guides, check the other.
- **`cadenceux-dx`** is retired: `cadenceux-developer-experience` replaces it. If it's still
  installed, suggest uninstalling it.
- Every routed skill owns its own answers. When this skill and an owning skill disagree, the
  owning skill wins for its topic.

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).
