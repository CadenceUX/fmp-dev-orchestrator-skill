# FileMaker 26.0.3 and earlier: before ADK

ADK works with FileMaker Pro 26.1 or later, and files hosted on FileMaker Server need 26.1.1 or
later. On anything older the agent can't reach the file, so the question is what extra code or
tooling a job needs, and when upgrading is the better answer.

## Contents
- Default: upgrade when you can
- What changes without ADK
- What 26.1 does natively that needed extra code before
- Reading a solution without ADK
- When a plug-in is the right answer

## Default: upgrade when you can

Recommend FileMaker 26.1 or later (the stack check reports Claris's current public release) unless something stops it:
a client's IT policy, hardware or OS below 26.1's requirements, a server that can't move to
26.1.1 yet, or a plug-in not yet built for 26.1. The upgrade gives the agent live access to the
file, removes several long-standing workarounds (below), and is the release Claris builds on.
Say what the upgrade costs too: client installs, a server upgrade, and testing every plug-in and
integration first, on a copy.

## What changes without ADK

| Task | With ADK | Without ADK |
|---|---|---|
| Write a script, field, layout change | Written into the file and read back | Readable steps for the developer to enter by hand |
| Check a calculation | Evaluated on the FileMaker engine | Checked against `claris-filemaker-pro`; say it's unverified |
| Read the solution | Live, through ADK | A Save a Copy as XML export, parsed with code |
| Conventions | The project's standards pack | Applied from `fmp-dev-design-patterns`' copy of the pack |

Never fall back to clipboard XML (fmxmlsnippet) generation: it's error-prone, hard to review, and
the CadenceUX skills retired it. Readable steps the developer enters are slower but safe.

## What 26.1 does natively that needed extra code before

On 26.0.3 or earlier these still need the workaround; on 26.1 use the native feature and say so:

| Need | 26.0.3 and earlier | FileMaker 26.1 |
|---|---|---|
| Set a variable whose name comes from data | Branching on the allowed names, or `Evaluate ( "Let ( $" & $name & " = " & Quote ( $value ) & " ; \"\" )" )` after checking `$name` holds only letters, digits and underscores | `Set Variable by Name` |
| Replace contents of a field chosen at runtime | Branching, one Replace Field Contents per field | `Replace Field Contents by Name` |
| Go to related records from a table chosen at runtime | Chains of conditional Go to Related Record | Go to Related Record, Table by Calculation |
| Read and restore the current sort | Track it yourself in variables; some plug-ins can read it | `Get ( SortOrder )` (JSON) |
| A value list from a calculation | Helper fields or relationships feeding a field-based list | Calculated value lists |
| A button icon chosen by data | Several buttons with hide conditions | Calculated SVG icon |
| Tool definitions for an AI model | Written by hand for each provider | `CreateToolDefinitions` from custom functions |
| A dialog that closes itself | A custom layout in a card window with a timer script | Show Custom Dialog with Close after (seconds) |

Check each item's details in `claris-filemaker-pro` before relying on it; several have no Claris
Help page yet. Any workaround built on `Evaluate` runs its text as a calculation: never pass
field data into it unchecked, and prefer branching when the possible names are few.

## Reading a solution without ADK

Use **Save a Copy as XML** (Tools menu, with advanced tools enabled). It holds schema, scripts,
layouts and custom functions, but no data. Exports run to tens of megabytes, so parse them with
code (Claude Code, or a chat with code execution), not by reading. `fmp-dev-design-patterns`'
audit method has the extraction map; the `clockwork-inspector` tool, where installed, analyses an
export for unreferenced items and broken references. An export is a snapshot: say so, and re-export
after changes.

## When a plug-in is the right answer

Before 26.1, and for things FileMaker doesn't do natively at all (shell commands, advanced file
handling, PDF manipulation, some cryptography), a plug-in is often the practical route:
`monkeybread-mbs-plugin`, `goya-be-plugin` (free) or `beezwax-bbox-plugin` (free, macOS and
Ubuntu). Weigh: every client and server needs it installed and licensed where required; it must be
updated with each FileMaker release; and Developer Next has to know it's there (record it in the
solution's notes script). Prefer the native feature when the client's version has one.
