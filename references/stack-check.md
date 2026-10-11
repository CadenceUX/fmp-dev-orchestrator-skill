# Stack check

A read-only report on whether the FileMaker agentic stack is current: the CadenceUX skills,
Claris ADT, FileMaker Pro, FileMaker Server, and the ADT project in the working folder.

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
- In full whenever asked: "check my FileMaker stack", "is everything up to date", "what version
  of ADT / FileMaker Pro do I need", or after the user says they updated something.
- Again when a tool fails in a way a version could explain (an ADT tool missing, Agent Access
  refused, typegen failing).

Run it once per session. If it fails or times out, say so in one line and carry on with the task.

## 2. Run it

```bash
python3 scripts/stack_check.py            # text report
python3 scripts/stack_check.py --json     # structured, for follow-up questions
python3 scripts/stack_check.py --project /path/to/adt-project
```

The script is in this skill's folder; run it with its full path. It searches upward from the
current folder for `adt.json` to find a project. Standard library only; about five seconds. It
runs `adt --version`, `adt doctor --json` and, on macOS, `mdfind`, all of them read-only.

## 3. Without a shell

In claude.ai chat or any host with no code execution:

1. Fetch `https://raw.githubusercontent.com/CadenceUX/cadenceux-skills/main/versions.json`.
2. For each CadenceUX skill loaded in this conversation, read `metadata.version` from its
   SKILL.md and compare with `skills.<name>.version`.
3. Report those, then say plainly that ADT, FileMaker Pro and the project weren't checked here,
   and that `adt doctor` (or this skill in Claude Code) checks them. Don't guess their versions.

## 4. Reading the report

**CadenceUX skills.** `UPDATE` means a newer release exists: point to the repo or
`claude plugin update` (plugin installs update themselves when auto-update is on). The Claude
desktop app keeps a copy of each uploaded skill per session, so several copies with old versions
are normal; the newest copy is the one in use. To update an uploaded skill, upload the new
release `.zip` (Customize → Skills). `REMOVE` means a skill on the `retired` list: a retired CadenceUX skill or a
clipboard XML skill that ADT replaces. Suggest removing it and give the reason from the list.
`OUTSIDE SET` means a skill on the `outside_set` list: not part of the CadenceUX set and not
replaced by ADT. Mention it once; the user keeps it if they use it.

**Claris ADT.** ADT is in Claris's preview programs and has no public update feed yet, so the
check reports the installed version as `INSTALLED (preview)` and points to the Developer Preview
hub for new builds (installed by running the new ADT Installer.pkg). `UPDATE` / `AHEAD` / `OK`
appear once a public ADT version is found in the Claris feed.

Preview version numbers (ADT, and the FileMaker Pro build ADT needs) are for the user's eyes
only: report them in the conversation, from their own install. Never write them into skill
files, commits, blog posts, slides or anything published while the programs are in preview.

When Claris releases ADT, expect it in the same Claris updates feed as FileMaker Pro and Server.
The script already looks for an ADT entry there, so the public comparison starts working without
a skill change.

**FileMaker Pro.** ADT needs a minimum FileMaker Pro version for Agent Access. The check reads
that minimum from the installed ADT (its doctor output or its own skill files), so it's always
the minimum for the ADT the user has. Claris's public feed may list an older version as current:
the build ADT needs comes from the preview program, so send the user to the Developer Preview
hub, not the public updater. Several FileMaker Pro versions installed side by side is normal; ADT
uses the one that has the file open. If Agent Access is `blocked`, relay doctor's remediation:
File → Manage → Agents → "Enable Agent Access for this application" (port 19080 by default).

**FileMaker Server.** The script reports the public latest only. For a Docker-hosted server,
`cadenceux-fms-docker-setup` checks the container; otherwise the Admin Console shows the version.

**ADT project.** Each web viewer app records the ADT version that created it
(`adtMetadata.initVersion`). Flags to relay:

- *Created with an older ADT*, or *AGENTS.md is out of date*: `adt update` run in the project
  folder refreshes the project's agent instructions. Ask first; suggest a commit first.
- *@adt/fmdapi behind what the installed ADT ships*: the package is vendored into each app, so
  it moves only when the app is updated: `adt update webviewer-apps/<app>` (run in, or pointed
  at, the app folder) updates that app's vendored packages. Then `pnpm install`, typegen and a
  build to confirm it still compiles. Ask first; suggest a commit first.
- TypeScript, Node and pnpm: compare with the app's `engines` and doctor's versions, and with
  the installed ADT's own project template.
- The FileMaker file's own ADT components (tables, scripts, layouts ADT adds) need the file open:
  `adt components status --json` is read-only; `adt components reconcile` changes the file, so
  ask first and suggest a backup.

End the report with the actions in priority order: anything blocking (Agent Access, FileMaker
Pro below ADT's minimum), then ADT, then the project, then skill updates.

## 5. What never happens

The check and this skill never install, update, reconcile or remove anything on their own. No
`adt update`, `adt install`, `adt components apply` or `reconcile`, `claude plugin update`, or
package installs without the user's yes in this conversation. Don't enter passwords; if a
command needs FileMaker credentials, let the user run it.

## 6. Sources

`versions.json` in `CadenceUX/cadenceux-skills` lists each skill's latest release, the retired
skills, skills outside the set, and `tested_with` for public products (FileMaker Server, plugin
versions). It carries no preview version numbers. It's updated on every skill release. Claris's updates feed:
`https://www.claris.com/cms/resources/downloads/updaters/product-updaters.txt`.
