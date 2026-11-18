---
name: fmp-dev-orchestrator
description: >-
  Retired. Replaced by cadenceux-dx, which routes Claris FileMaker work to the skill or Claris
  Agentic Development Kit (ADK) tool that owns it and checks the stack is current. Use only to
  tell the user to install cadenceux-dx and remove this skill, when they ask which FileMaker
  skill handles a topic or whether their FileMaker stack is up to date.
license: CC-BY-4.0
compatibility: >-
  Claude.ai, Claude Desktop, Cowork and Claude Code. Retired: install cadenceux-dx instead.
metadata:
  author: Darrin Southern, CadenceUX
  version: "2.2.0"
---

# fmp-dev-orchestrator (retired)

This skill is retired. Its routing and stack check moved to **cadenceux-dx**, rewritten for
Claris's FileMaker Agentic Development Kit (ADK), which replaced the ADT preview.

If `cadenceux-dx` is loaded in this session, use it and say nothing more about this skill.
Otherwise, start the answer with:

> ⚠️ **fmp-dev-orchestrator is retired.** Install `cadenceux-dx` and remove this skill:
> `claude plugin install cadenceux-dx@cadenceux` then
> `claude plugin uninstall fmp-dev-orchestrator`. For the Claude desktop app or claude.ai,
> download it from https://github.com/CadenceUX/cadenceux-dx-skill/releases

Then answer the user's FileMaker question with the skills that are loaded. Anything that reads
or changes the FileMaker file goes through ADK when it's available; never generate clipboard
XML.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Built and maintained by
[Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).
