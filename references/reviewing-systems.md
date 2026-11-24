# Reviewing an existing system: the questions to ask first

An agent can read a whole FileMaker solution in minutes. That makes it easy to produce a long
list of findings nobody asked for. A review is worth what its questions are worth: ask the
analyst's questions before the agent reads a single script.

## Contents
- Default: ask before reading
- The questions, by hat
- Then read the solution
- Presenting findings
- What not to do

## Default: ask before reading

Before any review, ask questions 1, 3, 5 and 10 at least: why, what must not break, what done
looks like, and whether this is a copy. Ask the rest only where the setting doesn't already
answer them (an open development copy with ADK answers 10 and 14). If the developer can't answer
the four yet, the first deliverable is those answers, not findings. Ask in one message, not one
question per step.

## The questions, by hat

**Analyst: why are we looking?**
1. What prompted the review: a bug, slowness, an upgrade, a handover, a security concern, a new
   feature that won't fit?
2. Who uses it, on which clients (Pro, Go, WebDirect, the Data API), and how many at once?
3. What must not break? Which workflows are the business, and which are rarely used?
4. Who maintains it now, and who after this work (Developer Next)?
5. What does done look like: a report, a fix list, a plan, a rebuild decision?

**Architect: what shape is it?**
6. Which FileMaker version is it on, and is it hosted (which FileMaker Server, where)?
7. Which plug-ins, external data sources, integrations and scheduled scripts does it rely on?
8. Is there a written standard, or one the code shows (see `fmp-dev-design-patterns`' audit)?
9. Where is the data that matters most, and how is it backed up?

**Tester: how will we know?**
10. Is there a copy we can work on, never the production file?
11. What does a working system look like for each critical workflow: who does what, and what
    should happen?
12. Are there known problems or complaints, with examples?

**Developer: what can the agent touch?**
13. Read-only review, or may changes be made (to a copy)?
14. Is ADK available against that copy (FileMaker Pro 26.1 or later, Agent Access on)? If not,
    a Save a Copy as XML export (see this skill's guide to FileMaker 26.0.3 and earlier).

## Then read the solution

With ADK, read live: `table_metadata` and `layout_metadata` first, then scripts and custom
functions, through ADK's tools. Without it, parse the XML export with code. Read in the order the
answers point: the critical workflows first, then what the prompt (question 1) named. For
conventions, `fmp-dev-design-patterns` runs the audit; for the server, `cadenceux-fms-security`.

## Presenting findings

- Lead with what answers question 1 and question 5.
- Rank by consequence to the workflows in question 3, not by count.
- Mark each finding as verified (ADK read it, or a test showed it) or inferred (from names or
  structure). Expected is not verified.
- Separate "breaks or risks data" from "convention or tidiness".
- End with the decisions the developer needs to make, in one list.

## What not to do

- Don't review production directly; work on a copy.
- Don't rewrite while reviewing. Changes come after the developer has read the findings.
- Don't treat a missing convention as a defect when the solution predates it; say what
  adopting it would cost.
