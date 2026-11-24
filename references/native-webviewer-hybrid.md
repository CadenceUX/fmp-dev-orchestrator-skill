# Native layouts, a web viewer app, or hybrid

ADK can scaffold a web viewer app inside a FileMaker solution (`adk app add`: a Vite, React,
Tailwind and shadcn app under `webviewer-apps/`, typed from the file's layouts by `pnpm typegen`,
talking to FileMaker through the web viewer bridge). That makes "should this be a web app?" a
real question on every project. Answer it from the need, not the novelty.

## Contents
- Default: native first
- When a web viewer app earns its place
- Hybrid: the usual answer
- What a web viewer app costs
- Questions to ask before choosing

## Default: native first

Build native FileMaker layouts unless a requirement below points elsewhere. Native layouts work
on every client (Pro, Go, WebDirect) with no build step, every FileMaker developer can maintain
them, and Claris certified WebDirect against WCAG 2.2 Level AA for native layouts. Most data
entry, lists, detail views, finds and reports are native work.

## When a web viewer app earns its place

- An interaction FileMaker layouts can't do well: drag and drop boards, rich charts and
  dashboards, calendars and schedulers, large interactive grids, custom visualisations.
- A user interface that must match a modern web product, or be shared with one.
- A team that already maintains web code and will own the app.

## Hybrid: the usual answer

Keep navigation, data entry and records native, and put one web viewer app where an interaction
needs it (a dashboard on the home layout, a scheduler on the bookings layout). FileMaker stays the
system of record and its scripts stay the business logic; the app calls them through the bridge.
This keeps the web code small and the solution maintainable by a FileMaker developer.

## What a web viewer app costs

Say these before recommending one:

- **A toolchain:** Node and pnpm (ADK checks and installs them), a build and a deploy step
  (`adk deploy`), and package updates over time (`adk update`).
- **Two skill sets for Developer Next:** FileMaker and TypeScript/React.
- **Client behaviour:** a web viewer runs in each client's web engine. WebDirect serves it from a
  `blob:` URL, so the app must use in-memory routing (ADK's `adk-webviewer-app` skill covers it);
  test on every client the users have, Go and WebDirect included.
- **Development needs FileMaker Pro 26.1 or later**, with Agent Access on, for the bridge and
  typegen.

## Questions to ask before choosing

1. Which clients do the users have (Pro, Go, WebDirect), and on what devices?
2. Is there an interaction native layouts can't do acceptably? Name it.
3. Who maintains this in two years, and do they write TypeScript?
4. Does it need to work offline, or on slow connections?
5. Are there accessibility requirements? (Native WebDirect has Claris's WCAG 2.2 AA certification;
   a custom app has whatever you build.)

If question 2 has no answer, build it native.
