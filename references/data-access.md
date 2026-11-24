# Getting at data: relationships, ExecuteSQL, the Data API or OData, or scripts

Four ways to read and change FileMaker data, each right for different jobs. Exact syntax and
platform limits are in `claris-filemaker-pro`; this guide is about choosing.

## Contents
- The default for each job
- Relationships
- ExecuteSQL
- The Data API and OData
- Native scripts
- What ADK uses, and why it isn't a design choice

## The default for each job

| Job | Default |
|---|---|
| Show or edit related records on a layout; calculations across a relationship | Relationships |
| A total or count shown on a layout or dashboard | A relationship (filtered by match fields where needed) with a summary field or `Sum` / `Count` calculation |
| A read-only lookup or aggregate from a calculation, without adding to the graph | ExecuteSQL |
| Another system reads or writes FileMaker data | The Data API (records and scripts) or OData (queries, BI tools) |
| Change many records, or a multi-step operation | A native script, on the server (Perform Script on Server) for bulk work |

## Relationships

FileMaker's native join: live, indexed, context-dependent. Best for portals, related fields,
lookups and Go to Related Record. Costs: every one adds to the relationship graph, and a graph
nobody can read is a maintenance cost; name every occurrence for what it's for (the standards
pack says how). Keys must be indexed.

## ExecuteSQL

`ExecuteSQL` runs a read-only SELECT from any calculation, independent of layout context, against
table occurrence names. Use it for lookups and aggregates that would otherwise need a new
occurrence. Know its costs:

- It only reads (SELECT); changes go through scripts.
- It returns delimited text, so parse it carefully, and quote occurrence and field names.
- It slows sharply when the current user has uncommitted changes in a table it queries, and on
  unstored calculations; keep it off large tables in frequently evaluated places (layouts,
  conditional formatting).
- A typo returns `?` with no detail; `ExecuteSQLe` returns the error. Test queries on ADK's
  engine or in the Data Viewer.

## The Data API and OData

For other systems, not for FileMaker's own clients:

- **The Data API** (REST): create, read, update and delete records, run scripts, upload to
  containers. Session-based authentication. Use it for web apps and integrations.
- **OData**: standard queries, metadata and batch requests, suited to BI and reporting tools.

Both run on FileMaker Server or Cloud, count against the server's API allowance, and need an
account with the right extended privilege (`fmrest`, `fmodata`) and nothing more. Never use them
from inside a FileMaker client to reach its own file: a script or relationship does that.

## Native scripts

Scripts do what the others can't: multi-step changes, transactions, error handling, user
interaction. For bulk changes, run them on the server with Perform Script on Server (no
round-trips per record) and wrap related changes in a transaction so they succeed or fail
together. Conventions for writing them are in `fmp-dev-design-patterns`.

## What ADK uses, and why it isn't a design choice

ADK's agent reads and writes data through its own tools (read-only SQL, and a Data API style
orchestrator for records) while it develops. That's the agent's access, not the solution's
design: choose the solution's data access from the table above, as you would without ADK.
