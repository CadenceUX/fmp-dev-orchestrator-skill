# Working agentically with a FileMaker developer

How the agent should run a piece of FileMaker work, and why. The vocabulary comes from Darrin
Southern's posts on cadenceux.com.au (FileMaker Knowledge Delegation, Agentic Time Traveller,
Context Engineer Position Title) and the Train Your FileMaker AI Agent talk.

## Contents
- Knowledge delegation
- Agentic time
- The four hats
- Briefs: context is the currency
- Documentation in agentic time
- Reviewing the agent
- When the harness changes

## Knowledge delegation

Knowledge comes in two piles:

- **Durable**: true for years. How a certificate trust chain works, that FileMaker Server keeps
  its data outside a container's writable layer, why a relationship needs indexed keys. The
  developer carries this; the agent uses it to reason.
- **Perishable**: changes with a release. Exact command flags, error strings, default values,
  which version introduced a step, which providers an AI step accepts. Delegate this pile: check
  it against the live system, ADK's engine or the owning skill every time, never from memory.

What the developer keeps, beyond the durable pile, is judgement: is this install
production-ready, is this fix actually a fix or does it only look like one, will Developer Next
understand what was built. Support that judgement rather than replacing it.

Rules that follow:

- **Expected is not verified.** "This should work" is a hypothesis. Run it, evaluate it on the
  engine, or say plainly that it's untested.
- **Know less about flags, more about verification.** When an answer is perishable, say where it
  was checked.
- **Document where it can be corrected:** a versioned skill, a changelog, a project's standards
  files, not a chat message that disappears.

## Agentic time

When the agent does the building, the clock that matters isn't typing time. Three things move:

- **The critical path moves to decisions.** The agent finishes in minutes and then waits; the
  wait between the agent finishing and a person deciding (decision latency) is now the long pole.
  So: list every decision that needs the developer's yes at the start, ask them together, and
  fill the gaps while they decide.
- **Scope gets cheaper to add, not cheaper to carry.** A feature costs little to build and the
  same as ever to test, train, support and hand over. Say so when a request grows.
- **Feedback loops shorten.** A working draft by the afternoon turns requirements into a
  conversation. Offer a prototype before a specification when that's faster for the developer.

Work as a manager of decisions, not effort:

- Treat every output as a draft, kept somewhere reversible: a copy of the file, a branch, a
  staging server, an unpublished post. A person releases it.
- Protect the developer's review time. Reading is now the long part of the day: keep changes
  small enough to review, and say what to look at first.
- With several agents or sessions in parallel, keep one picture of where each stands, so the
  developer can switch to any thread and arrive briefed.

## The four hats

Every FileMaker project still needs four hats: **analyst, architect, developer and tester**.
What's changed is where the developer's time goes:

| Hat | Where the time goes now |
|---|---|
| **Analyst** | The most time: the needs analysis, the stakeholders, what success looks like |
| **Architect** | The next most: the system design, schema, where logic lives, how it's deployed |
| **Developer** | The thinnest: the agent writes more of the code |
| **Tester** | Real time: QA, edge cases, the exceptions that prove the rule |

So the agent should pull the conversation towards the analyst and architect hats (ask about
the need and the design before building) and leave room for the tester hat (propose how to test
what it built). The years of experience count in knowing what the solution should look like and
do, not in typing it.

## Briefs: context is the currency

Every agent starts cold. A brief for a helper agent, a new session or a teammate carries:

- **The need**: what problem this solves and for whom.
- **The constraints**: FileMaker version, clients (Pro, Go, WebDirect), hosting, conventions
  (the standards pack), what must not change.
- **Definition of done**: how anyone will know it's finished and correct.

The same discipline applies to the developer's own requests: when one lacks the need or the
definition of done, ask for it before building.

The Context Engineer's habits from the post apply to the agent too: deliver what is needed,
not only what was asked for; watch for the exceptions that prove the rule; know the solution
inside and out before changing it; code so a user and Developer Next can troubleshoot it.

## Documentation in agentic time

The agent can draft documentation at every stage, so the cost is reviewing it, not writing it.
Undrafted, unreviewed documentation is a liability with good formatting.

| Stage | What the agent drafts |
|---|---|
| Discovery | Meeting notes turned into the need and the success criteria |
| Design | Schema decisions and the reasons for them |
| Build | Script headers, field comments, custom function descriptions, changelogs |
| Test and deploy | Test evidence, deployment notes, rollback steps |
| Handover | User guides and notes for Developer Next |

FileMaker 26.1's field display names, annotations and custom function descriptions keep this
knowledge inside the file, where it can't drift away; they're also the context the next agent
reads.

## Reviewing the agent

Reviewing the agent's work is the new code review. The skill that doesn't expire is telling a
correct fix from a plausible one. When presenting work:

- Say what was verified and how (engine-evaluated, read back from the file, tested on data), and
  what wasn't.
- Point to the riskiest part first.
- Prompt once, read twice: re-read the result against the brief before reporting done.

## When the harness changes

The same prompt in a different harness gives different work. A new ADK, model, skill version or
FileMaker build is a new contractor joining the team: review its first piece of work carefully
before trusting the second. The stack check says what changed.
