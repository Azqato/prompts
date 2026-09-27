---
title: Progress Dashboard
description: Keep a public HTML dashboard during a long task: progress, anything stuck, questions waiting for you, and what Claude will do if you do not answer.
meta: Claude Code Prompt
---

Gives a long task a page you can glance at instead of scrolling back through the session. Claude builds one HTML file, `dashboard/index.html`, before the work starts and updates it after every step. It shows the steps and their status, anything stuck and what it is waiting for, the questions waiting for you, each with the default Claude will take if you do not answer, and the latest files it changed. The page opens with a double-click and reloads itself every ten seconds. It needs no server and makes no network requests, and every time on it comes from the system clock rather than an estimate. The page is part of the project, so it is published with it: on a static site, anyone can watch progress at `/dashboard/`. The copy on disk updates live; the published copy shows the state as of the last time you published the project. Claude keeps anything private off it.

Claude keeps the dashboard itself, in the same session: nothing is installed, and no agents or plugins are set up. When it needs a decision, it adds the question to the page and carries on with whatever does not depend on the answer, so a question you have not seen yet never stalls the whole task. The first time, it asks how you like the page to look (light or dark, dense or airy, one accent color) and records your answer in `CLAUDE.md` so every later dashboard matches. When the task is done, it asks whether to make this a standing rule for long tasks in the project, and shows you the exact lines before writing them.

## Prompt

```
Keep a live progress dashboard for this task, and maintain it yourself in this session. Do not create or install any agents, subagents, or plugins.

Start
Read the README, CLAUDE.md, and docs/ if they exist, and check whether a dashboard style is already recorded. If not, ask me once, with your suggested default for each, and wait: light or dark, dense or airy, and one accent color. Then show me the lines that record the style under a "Progress dashboard" heading in CLAUDE.md (creating the file if needed), and write them once I confirm.
Then tell me the task as you understand it, broken into steps, and the default you will take for each decision you can already foresee. If the task itself is unclear, ask a short follow-up rather than guessing.

Dashboard
- One file, dashboard/index.html, that opens by double-clicking. No server, no network requests, and no external scripts, fonts, or images: everything is inline.
- It reloads itself every 10 seconds with <meta http-equiv="refresh" content="10">, which works from a local file.
- Choose the panels for this task rather than using a fixed template, but always include:
  - Steps and their status: done, in progress, waiting, or not started.
  - Stuck: anything blocked, and what it is waiting for.
  - Questions for me: each with the default you will take if I do not answer.
  - Latest results: the files created or changed, and what each one is, with paths relative to the project root.
- Take every time from the system clock when you write the update. Never estimate one.
- The dashboard is part of the project, tracked like any other file and published wherever the project is published: on a static site it is served at /dashboard/, and otherwise anyone who can see the repository can read it. Put nothing on it you would not publish: no secrets, keys, personal details, private paths, or private matters. Keep a question that involves any of those in the conversation, and put only a neutral line on the page. Include <meta name="robots" content="noindex">, since it is a working page rather than content. The published copy changes only when the project is published, which is my decision; the copy on disk is the live one.
- If dashboard/ already exists for something else, use progress-dashboard/ instead and tell me.

Working
- Create the dashboard before starting the task, and tell me its path, and its public address if the project is published somewhere you can name.
- Update it after every step, and whenever something gets stuck or a question comes up.
- When you need a decision, add it to Questions with your default and keep working on anything that does not depend on it. When you reach work that does, take the default, say so on the dashboard, and mark the question as answered by default.
- When the task is finished, update it one last time with a short summary at the top.

Afterwards
Ask whether I want this as a standing rule. If I do, show me the exact lines for the project's CLAUDE.md, and write them once I confirm: for any task with more than 5 steps, or likely to take longer than 30 minutes, create and maintain dashboard/index.html as described here, using the recorded style. The page is published with the project, so nothing private goes on it.
```
