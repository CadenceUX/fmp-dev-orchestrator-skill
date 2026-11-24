# Reviewing security and deployment

Agentic development adds new things to secure (an agent with live access to a file, web viewer
apps, keys for AI providers) and makes deployment more frequent. This guide is what to check
in the solution and the release; the server itself is `cadenceux-fms-security`'s job.

## Contents
- Default: develop on a copy, deploy deliberately
- The solution: accounts, privileges and secrets
- The agent's access
- Before each deployment
- After deployment
- Who owns what

## Default: develop on a copy, deploy deliberately

Development and the agent's access stay off the production server. Changes reach production
through a deliberate step (a migration, an OttoFMS deployment, or a scripted import into a
clean clone), with a backup first and a way back.

## The solution: accounts, privileges and secrets

- Every person and every integration has its own account; no shared logins; no Guest access
  unless the solution is designed for it.
- Privilege sets grant what the job needs. An account for the Data API or OData has only that
  extended privilege (`fmrest` or `fmodata`) and access to only the layouts and records it uses.
- `[Full Access]` is for developers, not for integrations or day-to-day users.
- Secrets (API keys for AI providers, passwords for external services) never sit in script text,
  calculations or field defaults, and are never shown on layouts users can reach. Store them
  where only the account that needs them can read them, and record where in the solution's notes
  script.
- Auto-login, `Get ( AccountName )` checks used as security, and scripts run with full access
  privileges: list each one and why it's there.

`cadenceux-fms-security` reads accounts and privileges from a Save a Copy as XML export when the
developer wants the full check.

## The agent's access

- Agent Access is a FileMaker Pro setting on the developer's machine. Turn it on where the agent
  works, not on users' machines or shared machines.
- The agent signs in with an account like anyone else: give it a development account on the
  development copy, not a production `[Full Access]` account.
- ADK can add components to a file (tables, scripts and layouts for web viewer apps). Check with
  `adk components status --json` which are present, and decide whether production needs them.
- Every change the agent makes is a draft until reviewed: read the diff of scripts and schema
  before deploying.

## Before each deployment

1. The standards review and linter tests pass (this skill's linter-tests guide).
2. Every critical workflow tested on a copy, on each client the users have.
3. Plug-ins, at the versions the solution needs, installed on the server and clients.
4. The server version: hosted files that ADK reaches need FileMaker Server 26.1.1 or later. For a
   production file carrying ADK's web viewer components, confirm the server version ADK's
   release notes require.
5. Web viewer apps built (`adk deploy`) and tested in Go and WebDirect if those are used.
6. A backup of production taken and verified, and the time of the change agreed with users.
7. The way back written down: what to restore, and how long it takes.

If any item isn't done by the agreed time, say so plainly and recommend moving the date; a
deployment deadline is a decision for the developer and the client, not a reason to skip a check.

## After deployment

- Check the server's logs and the critical workflows straight away.
- Record what changed, in the solution's notes script or the project's history.
- Review again when the harness changes: a new ADK, FileMaker or model is a new contractor.

## Who owns what

| Topic | Owner |
|---|---|
| Server exposure, ports, CVEs, logs, backups | `cadenceux-fms-security` |
| Server install or upgrade in Docker; OttoFMS deployments | `cadenceux-fms-docker-setup`; `cadenceux-ottofms-docker-setup` |
| Privilege-set and account syntax, Data API and OData behaviour | `claris-filemaker-pro` |
| Web viewer app build and deploy | ADK's `adk-webviewer-app` |
| Conventions the review checks | `fmp-dev-design-patterns` and the standards pack |
