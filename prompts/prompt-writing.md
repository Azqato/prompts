---
title: Prompt Writing
description: Write a new prompt, or tighten one you already use, so it works with how models actually read, reason, and fail.
meta: Claude Code Prompt
---

Most prompts that go wrong fail in a few predictable ways, and each one comes from how a language model works. A model's trained knowledge is a blurred recollection, while what is in front of it is exact. It thinks a small, fixed amount per word, so a verdict asked for first is a guess. It sees chunks of text rather than letters, so it miscounts. It is trained to sound sure, so it fills gaps instead of admitting them. And its answers vary from run to run, so only a check can show that one worked.

This prompt turns those facts into a working method. Give it a task and it writes a prompt for it, or give it a prompt you already use and it reviews it: it asks the few questions that decide the prompt, then writes or rewrites it so Claude reads what it needs before acting, works things out before concluding, hands counting and exact matching to code, knows what to do when something is missing, shows the shape of its output, and ends on a check that can pass or fail. It explains each change in a line, and saves nothing unless you ask.

## Prompt

```
Help me write a prompt, or improve one I already use. If I have not given you a task or a prompt yet, ask for one and wait.

First, understand the job
- If I gave you an existing prompt, read it in full first, and read any files, pages, or examples it refers to.
- Ask me once, in one message, with your suggested answer for each, and wait:
  - What the prompt is for, and what a good result looks like.
  - Who or what runs it (Claude Code in a project, a chat, an API call), and what it can read or run there.
  - What it must never do (edit files, install things, push, spend money, contact anyone).
  - What the output should look like: a report, a table, edited files, a single answer.
  - How we will know it worked: the check that passes or fails at the end.

Then write or rewrite it against these rules. Apply each where it fits; a small prompt needs fewer of them.
1. Facts from the context, not from memory. A model's trained knowledge is a blurred recollection; what it reads is exact. Tell it to read what it needs (the files, the page, the pasted text, the docs) before acting, and never to rely on remembering something it can read.
2. Investigate before concluding. A model thinks a small, fixed amount per token, so reasoning has to be spread through the answer. Order the steps so reading and checking come first and findings and decisions come after. Never ask for the verdict first and the reasons second.
3. Exact work goes to tools. A model sees chunks of text, not letters, and does arithmetic in its head. Counting, arithmetic, lengths, sizes, dates, exact string matches, and comparisons are done with a command or a script.
4. A way to say "I don't know". A model is trained to sound sure. Say what to do when something cannot be read, found, or checked: stop and ask, or mark it unknown. Never let a gap be filled from memory or guessed from a title or a link.
5. Show the shape of the output. An example steers harder than a description. Where the format matters, name the exact columns, sections, or fields, or give a one-line example.
6. End on a check that can pass or fail. Answers vary from run to run, so the prompt ends with a verifiable finish line and asks for a report of what was checked and what was not.
7. If it scores anything, the measure cannot be gamed. Fix the rubric before scoring, score from the real thing, and forbid raising one number by lowering another.
8. Keep it focused. Put the main instruction first. Link or point to long reference material instead of pasting it when the model can read it. Cut filler, politeness, and repeated emphasis.
9. Supply what the model cannot know about itself. It does not reliably know its own name, version, or today's date. Take dates from the system clock or ask.
10. State the limits plainly. Name anything it must not do, and when it must stop and wait for me. Keep credentials, accounts, and personal details out of the prompt.

Deliver
- The finished prompt in one fenced block, ready to paste.
- Under it, a short list: each change or choice, the rule it follows, and why, in one line each. For an existing prompt, say what you kept and why as well.
- Anything you assumed rather than learned from me, so I can correct it.
- If the prompt will run somewhere you can reach, offer to try it once on a small real case and show me the result against the check. Do not save the prompt to a file unless I ask.
```
