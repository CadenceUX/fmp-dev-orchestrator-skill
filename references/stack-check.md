# Stack check

A read-only report on whether the FileMaker agentic stack is current: the CadenceUX skills,
Claris's FileMaker Agentic Development Kit (ADK), FileMaker Pro, FileMaker Server, and the ADK
project in the working folder.

## Contents
1. When to run it
2. Run it (Claude Code, Cowork, any shell)
3. Without a shell (claude.ai chat)
4. Reading the report
5. What never happens
6. Sources

## 1. When to run it

- Once per session, on the first FileMaker task, before routing. Keep it short: one or two
  lines unless something needs action.
- In full whenever asked about versions or updates, even if Step 0 already ran: "check my FileMaker stack", "is everything up to date", or after the user says they updated something.
- Again when a tool fails in a way a version could explain (an ADK tool missing, Agent Access
  refused, typegen failing, a standards pack not found).

If it fails or times out, say so in one line and carry on with the task.

## 2. Run it

```bash
python3 scripts/stack_check.py            # text report
python3 scripts/stack_check.py --json     # structured, for follow-up questions
python3 scripts/stack_check.py --project /path/to/adk-project
```

The script is in this skill's folder; run it with its full path. It searches upward from the
current folder for `adk.json` to find a project. Standard library only; about five seconds. It
runs `adk --version`, `adk doctor --json`, `adk standards --json` and, on macOS, `mdfind`, all
read-only, and fetches `versions.json`, Claris's ADK manifest and Claris's updates feed.

## 3. Without a shell

In claude.ai chat or any host with no code execution:

1. Fetch `https://raw.githubusercontent.com/CadenceUX/cadenceux-skills/main/versions.json`.
2. For each CadenceUX skill loaded in this conversation, read `metadata.version` from its
   SKILL.md and compare with `skills.<name>.version`.
3. Report those, then say plainly that ADK, FileMaker Pro and the project weren't checked here,
   and that `adk doctor` (or this skill in Claude Code) checks them. Don't guess their versions.

## 4. Reading the report

**CadenceUX skills.** `UPDATE` means a newer release exists: `claude plugin update <name>@cadenceux`
for plugin installs, or upload the new release `.zip` (Customize → Skills) for the Claude
desktop app and claude.ai. The desktop app keeps a copy of each uploaded skill per session, so
several old copies are normal; the newest is the one in use. `REMOVE` means a skill on the
`retired` list (such as the clipboard XML skills): suggest removing it, with the reason from the list: `claude plugin uninstall <name>@cadenceux`
for a plugin install, or delete it under Customize → Skills in the desktop app and claude.ai.
Ask first. `OUTSIDE SET` means a skill on the
`outside_set` list: not CadenceUX's and not replaced by ADK. Mention it once.
*Same skill as …* means both `cadenceux-dx` and `fmp-dev-orchestrator`
are installed: they're one skill under two names, so suggest uninstalling either. Only one is
needed, so the other isn't listed as not installed.
`cadenceux-filemaker-standards` is a plugin with no skill: it's the `cadenceux` standards pack.

**Claris ADK.** The installed version (`adk --version`) is compared with Claris's ADK manifest.
`UPDATE` names the release; tell the user and pass on the release notes link, then ask before
running `adk upgrade` (it installs with no confirmation of its own). The report also shows the
Claude Code plugin and MCP server versions from `adk doctor`; a plugin older than the CLI means
the harness hasn't picked up the upgrade yet: restart it. *An old ADT preview install* means the
`adt` command or its folder is still present: it's replaced by ADK and can be removed.

**FileMaker Pro.** ADK needs FileMaker Pro 26.1 or later (the minimum comes from
`versions.json` `requirements.adk.filemaker_pro`). Several versions installed side by side is
normal; ADK uses the one that has the file open. A version newer than Claris's public release
is a testing build: fine for development, but don't ship a solution that depends on it. If
`adk doctor` reports Agent Access off, relay its remediation (FileMaker Pro's Agent Access
setting, with a port, 19080 by default) rather than inventing menu paths.

**FileMaker Server.** The script reports the public latest only. Hosted files reached through
ADK need FileMaker Server 26.1.1 or later. For a Docker-hosted server,
`cadenceux-fms-docker-setup` checks the container; otherwise the Admin Console shows the version.

**ADK project.** The project's standards pack (from `adk.json`) and its resolved layers, its
connected files, and each web viewer app:

- *No standards pack*, or *pack declared but not installed*: for CadenceUX work, install
  `cadenceux-filemaker-standards@cadenceux` and run `adk standards use cadenceux`. Ask first.
- *Uses the old @adt/fmdapi package*, or *@adk/fmdapi behind what the installed ADK ships*:
  the package is vendored into each app and moves only when the app is updated: `adk update` in
  the app folder, then `pnpm install`, typegen and a build. Ask first; suggest a commit first.
- *Created with an older ADK*: `adk update` refreshes the project's agent instructions. Ask
  first.
- The FileMaker file's own ADK components need the file open: `adk components status --json` is
  read-only; `adk components reconcile` changes the file, so ask first and suggest a backup.

End the report with the actions in priority order: anything blocking (Agent Access off,
FileMaker Pro below 26.1), then ADK, then the project, then skill updates.

## 5. What never happens

The check and this skill never install, update, reconcile or remove anything on their own: no
`adk upgrade`, `adk update`, `adk install`, `adk components apply` or `reconcile`,
`adk standards use`, `claude plugin update`, or package installs without the user's yes in this
conversation. Don't enter passwords; if a command needs FileMaker credentials, let the user run
it.

## 6. Sources

- `versions.json` in `CadenceUX/cadenceux-skills`: each skill's latest release, the retired
  skills, skills outside the set, ADK's FileMaker requirements, and `tested_with`. Updated on
  every skill release.
- Claris's ADK manifest: `https://downloads.claris.com/adk/manifest.json`.
- Claris's updates feed:
  `https://www.claris.com/cms/resources/downloads/updaters/product-updaters.txt`.
