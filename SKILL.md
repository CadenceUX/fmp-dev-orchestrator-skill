---
name: fmp-dev-orchestrator
description: >-
  The same skill as cadenceux-dx, under its earlier name.
  The developer experience for agentic Claris FileMaker work, with or without Claris's
  FileMaker Agentic Development Kit (ADK). Routes each task to the CadenceUX skill or ADK tool
  that owns it, checks the stack is current (skills, ADK, FileMaker Pro and Server, the ADK
  project), and guides the decisions around the code: native layouts, web viewer apps or
  hybrid; SQL, relationships, Data API or scripts; what FileMaker 26.0.3 and earlier need;
  reviewing an existing system; linter tests; security and deployment. Teaches how agentic
  work runs: knowledge delegation, agentic time, the four hats, briefs and review. Use when
  starting FileMaker work, when unsure which skill or tool owns a task, when a request spans
  several, when asked whether the stack is up to date, or for any of those decisions. Not for
  answering syntax, plug-in or convention questions itself; it hands those to the owning skill.
license: CC-BY-4.0
compatibility: >-
  Claude.ai, Claude Desktop, Cowork and Claude Code, and any harness that reads skills. The
  full stack check needs Python 3 and a shell; without one it checks skill versions only.
metadata:
  author: Darrin Southern, CadenceUX
  version: "3.0.2"
---

# CadenceUX DX (fmp-dev-orchestrator)

The developer experience for agentic FileMaker work. It routes each task to the skill or tool
that owns it, keeps the stack current, and carries the judgement the other skills don't: which
approach to take, how to review, and how the developer's time is spent now that the agent does
more of the building. Load the owning skill for the answer itself; never answer catalog
questions (syntax, plug-in functions) from training data.

## Requirements

| Kind | Name | Used for | Surfaces |
|---|---|---|---|
| CLI | `python3` | `scripts/stack_check.py` | Claude Code or any harness with a shell |
| CLI | `adk`, `filemaker` (ADK, optional) | ADK health, standards and project checks | Any harness with a shell |
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
  needs FileMaker Pro 26.1 or later; for 26.0.3 and earlier, see
  [references/before-adk.md](references/before-adk.md).

## Step 2: route the task

| Task | Owner |
|---|---|
| Reading or changing the file: schema, scripts, layouts, value lists, custom functions, live SQL, running scripts | **ADK** (`fm-mcp-guide`, `fm-cli`) |
| ADK projects and web viewer apps | **ADK** (`adk-project-setup`, `adk-webviewer-app`) |
| Which naming and design rules apply, and following a standards pack | **ADK** (`filemaker-standards`, `adk standards`) |
| CadenceUX conventions, writing and reviewing scripts, a client's own standards | **`fmp-dev-design-patterns`** (with the `cadenceux` pack, `cadenceux-filemaker-standards@cadenceux`) |
| Function and script step syntax, versions, platform support, FileMaker 26.1 additions, Data API, OData, ExecuteSQL, error codes | **`claris-filemaker-pro`** |
| BaseElements (`BE_…`), MBS (`MBS ( "…" )`), bBox (`bBox_…`) functions | **`goya-be-plugin`**, **`monkeybread-mbs-plugin`**, **`beezwax-bbox-plugin`** |
| FileMaker Server in Docker on macOS; OttoFMS on it | **`cadenceux-fms-docker-setup`**; **`cadenceux-ottofms-docker-setup`** |
| Security check of a FileMaker Server: exposure, CVEs, accounts, logs, backups | **`cadenceux-fms-security`** |
| GitHub: publishing skills, known attacks on accounts and repos, scanning skills before install | **`cadenceux-github`** |
| Building or updating a Claude skill | **`cadenceux-skill-creator`** |
| Is the stack current | **This skill**, Step 0 |
| Which approach to take, how to review, how to work (below) | **This skill** |
| FileMaker Server administration beyond these, Admin API, Claris Connect, Claris Studio | No dedicated skill: fetch the live guide from `https://help.claris.com/` |

For naming and conventions, ADK's `filemaker-standards` resolves which rules apply (Baseline,
then the project's pack, then the project's own); `fmp-dev-design-patterns` supplies the
`cadenceux` pack and how to write and review scripts to it. Change the file with ADK's tools as
`fm-mcp-guide` describes, and `fm-cli` for schema and layout edits it routes there.

For counts and versions, read the owning skill's `VERSION` and catalog `meta`, or
`versions.json`; this table carries none.

## Decisions this skill guides

Read the guide before advising. Each one sets out the options, what each costs, and the
default when nothing points elsewhere. Every answer includes the points in the last column,
however short the answer:

| Decision | Guide | Always say |
|---|---|---|
| FileMaker 26.0.3 or earlier: what extra code or tools a job needs, and when to upgrade | [before-adk.md](references/before-adk.md) | The upgrade option and its cost; the 26.0.3 workaround; that without ADK the steps are entered by hand and unverified |
| Native layouts, a web viewer app, or both | [native-webviewer-hybrid.md](references/native-webviewer-hybrid.md) | Native first unless a named interaction needs the app; the costs (toolchain, two skill sets for Developer Next, testing on every client) |
| ExecuteSQL, relationships, the Data API or OData, or native scripts | [data-access.md](references/data-access.md) | The default for the job; each option's cost; never the Data API from inside a FileMaker client |
| Reviewing an existing system: the questions to ask first | [reviewing-systems.md](references/reviewing-systems.md) | The questions before any reading; why, and what done looks like, first; work on a copy |
| Which linter tests to build, and how | [linter-tests.md](references/linter-tests.md) | One written rule per test; a passing and a failing example for each; `advisory.md` rules only raise notes |
| Security and deployment review | [security-deployment.md](references/security-deployment.md) | Tested on a copy on each client; a verified backup and a way back; the server version (26.1.1 or later for files ADK reaches); the server itself goes to `cadenceux-fms-security` |

## How the work runs

Apply these on every task; [references/working-agentically.md](references/working-agentically.md)
has the detail and the reasons.

- **Delegate the perishable, keep the durable.** Exact flags, error strings, versions and option
  names change every release: check them against the live system or the owning skill every time.
  Expected is not verified.
- **Every output is a draft** until the developer has reviewed it, kept somewhere reversible (a
  copy of the file, a branch, an unpublished post). Development stays off the production server.
- **Decisions are the critical path.** List what needs the developer's yes and ask early, in one
  place, rather than one question per step.
- **The four hats:** analyst, architect, developer and tester. The agent now wears most of the
  developer hat; spend the conversation on needs, design and testing.
- **Brief like a context engineer.** Any helper agent or session gets the need, the constraints
  and what done looks like.
- **Review again when the harness changes.** A new ADK, model or skill version is a new
  contractor: check its first piece of work before trusting the second.

## Requests that span skills

Load each owning skill in turn. Common combinations:

- A script that calls a plug-in: `fmp-dev-design-patterns` for structure, the plug-in skill for
  the function, `claris-filemaker-pro` for the steps, ADK to write it into the file.
- A new server: `cadenceux-fms-docker-setup`, then `cadenceux-ottofms-docker-setup`, then
  `cadenceux-fms-security`.
- A web viewer app: [native-webviewer-hybrid.md](references/native-webviewer-hybrid.md) to
  decide, then ADK's `adk-webviewer-app`, with `claris-filemaker-pro` for the scripts it calls.

## Disclosure

End every answer routed through this skill with:

- **Skills consulted:** only the skills actually loaded.
- **Tools and URLs:** ADK tools called and live pages fetched, or "answered from local
  reference files only".

## Skill update self-check

The stack check covers this skill: it reports the running copy against `versions.json`. With no
shell, fetch `https://github.com/CadenceUX/fmp-dev-orchestrator-skill/raw/main/VERSION` once per session
and, if it's newer than 3.0.2, start the answer with:

> ⚠️ **Skill update available:** this skill is v[installed]; v[latest] is at
> https://github.com/CadenceUX/fmp-dev-orchestrator-skill/releases

Skip silently if the fetch fails.

## Relationship to other skills

- **This is `cadenceux-dx` under its earlier name.** Its files are generated from the
  cadenceux-dx repo, so the two never differ in what they do. If `cadenceux-dx` is also loaded,
  use it and leave this copy alone, and suggest uninstalling one of them (either: they're
  identical).
- **`cadenceux-academy`** teaches people the Train Your FileMaker AI Agent class; this skill
  teaches the agent the behaviour. The class's vocabulary (knowledge delegation, agentic time,
  the four hats) is maintained in the posts and the deck; when they change, update
  `working-agentically.md` to match.
- Every routed skill owns its own answers. When this skill and an owning skill disagree, the
  owning skill wins for its topic.

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).
