---
title: Prompt Audit
description: Audit a project's skills, instruction files, and prompts for patterns written for older models, and propose changes for the ones that now work against current ones.
meta: Claude Code Prompt
---

Runs the `prompt-audit` subcommand of the built-in `claude-api` skill. It inventories the prompt-shaped text in a project, the skills, the `CLAUDE.md` and `AGENTS.md` instruction files, the tool descriptions, and any standalone prompts, then reports the patterns in them that were written for an earlier generation of model and now hold back a current one. The audit is non-interactive: it works out its own scope and target model, states those assumptions in the report rather than stopping to ask, and finishes by producing the report and the proposed changes.

Use it after a model upgrade, or on any project whose instruction files have been accumulating long enough that nobody remembers what each line was working around. Prompting written for an older model does not announce itself. It keeps working, just worse, so nothing surfaces the cost until something goes looking for it. This is the one entry here that is a command rather than a block of text, so there is nothing to fill in before running it.

## Prompt

```
/claude-api prompt-audit
```
