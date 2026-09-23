---
title: Prompt Audit
description: Find the instructions in a project's prompts, skills, and CLAUDE.md files that were written for older models, and fix the ones that now hold it back.
meta: Claude Code Prompt
---

Runs the `prompt-audit` subcommand of the built-in `claude-api` skill. It inventories the prompt-shaped text in a project, the skills, the `CLAUDE.md` and `AGENTS.md` instruction files, the tool descriptions, and any standalone prompts, then finds the patterns in them that were written for an earlier generation of model and now hold back a current one. The audit is non-interactive: it works out its own scope and target model and states those assumptions in its report rather than stopping to ask. Because the command asks for the changes to be applied, it edits the files directly for every finding it rates high or medium confidence, and leaves low-confidence findings in the report without touching them.

Use it after a model upgrade, or on any project whose instruction files have been accumulating long enough that nobody remembers what each line was working around. Prompting written for an older model does not announce itself. It keeps working, just worse, so nothing surfaces the cost until something goes looking for it. Run it on a committed working tree. Nothing pauses for approval, and the edits can land before the report is on screen, so `git diff` is where you review them and take back any you disagree with. If you only want the report and a proposed diff, with no file changed, drop "and apply the proposed changes" and run `/claude-api prompt-audit` on its own. Unlike the other entries this is a single command, so there is nothing to fill in before running it.

## Prompt

```
/claude-api prompt-audit and apply the proposed changes
```
