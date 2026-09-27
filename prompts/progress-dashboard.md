---
title: Progress Dashboard
description: Keep a public HTML dashboard during a long task: progress, anything stuck, questions waiting for you, and what Claude will do if you do not answer.
meta: Claude Code Prompt
---

Gives a long task a page you can glance at instead of scrolling back through the session. Claude builds one HTML file, `dashboard/index.html`, before the work starts and updates it after every step. It shows the steps and their status, anything stuck and what it is waiting for, the questions waiting for you, each with the default Claude will take if you do not answer, the latest files it changed, and, where the project keeps a roadmap, where the project is going. Every dashboard follows one layout, the one running at https://azqato.github.io/prompts/dashboard/: a sidebar of sections, a top bar with the update time and percent complete, four summary figures, a progress card, and a table for each section. The layout is written out in full in the prompt, so it works without that page. Only layout and structure are taken from it: the colors and fonts are your project's own branding, read from its design doc and styles, so the dashboard looks like part of your project rather than like that page. The page opens with a double-click and reloads itself every ten seconds. It needs no server and makes no network requests, and every time on it comes from the system clock rather than an estimate. The page is part of the project, so it is published with it: on a static site, anyone can watch progress at `/dashboard/`. The copy on disk updates live; the published copy shows the state as of the last time you published the project. Claude keeps anything private off it.

Claude keeps the dashboard itself, in the same session: nothing is installed, and no agents or plugins are set up. When it needs a decision, it adds the question to the page and carries on with whatever does not depend on the answer, so a question you have not seen yet never stalls the whole task. The first time, it takes the palette and fonts from your project's existing branding and records them in `CLAUDE.md` after you confirm, so every later dashboard matches; it asks for colors only if the project has no branding. When the task is done, it asks whether to make this a standing rule for long tasks in the project, and shows you the exact lines before writing them.

## Prompt

```
Keep a live progress dashboard for this task, and maintain it yourself in this session. Do not create or install any agents, subagents, or plugins.

Start
Read the README, CLAUDE.md, and docs/ if they exist, and check whether a dashboard style is already recorded. If not, take it from the project's existing branding, never invent one: its design doc (such as docs/DESIGN.md), its CSS custom properties or theme file, and any brand files. Take the background, panel, border, text, and muted colors, the accent, the status colors if it has them, and the font families, and fill any gap from the nearest brand color rather than a new one. The dashboard changes layout and structure only; the brand stays exactly as it is. Only where the project has no branding at all, ask me once, with your suggested default for each, and wait: light or dark, and one accent color. Then show me the palette with where each color came from, and the lines that record it under a "Progress dashboard" heading in CLAUDE.md (creating the file if needed), and write them once I confirm.
Then tell me the task as you understand it, broken into steps, and the default you will take for each decision you can already foresee. If the task itself is unclear, ask a short follow-up rather than guessing.

Dashboard
- One file, dashboard/index.html, that opens by double-clicking. No server, no network requests, and no external scripts, fonts, or images: everything is inline. Name the brand's fonts first in each font stack, followed by system fonts, and never download or link one: where the brand font is installed it shows, and elsewhere the system font stands in.
- It reloads itself every 10 seconds with <meta http-equiv="refresh" content="10">, which works from a local file.
- Use this layout every time, in this order. The layout is fixed; only the colors and fonts change, and they come from the recorded style, which is the project's own branding. A working example is at https://azqato.github.io/prompts/dashboard/, which you may open to see it, but these lines are the specification, so build from them even if that page cannot be reached, and never copy its gold-on-black colors or its content.
  - Sidebar, on the left: a small brand mark and the word Progress, a box naming the current task, then links to each section below with a count beside each (steps, open questions, stuck items, results, and roadmap items still open). The link to the overview is highlighted in the accent color. At the bottom, a line saying the page is kept by Claude in this session. Below 900px wide the sidebar becomes a strip of section links across the top that scrolls sideways, not a drawer, so the page needs no script.
  - Top bar, sticky: the task name, a small pulsing dot with the time of the last update and "refreshes every 10 seconds", and the percent of steps done in an accent-colored chip.
  - Overview: four summary figures in a row (two across below 1200px, one below 420px): steps done as a fraction with the percent, in progress, stuck, and open questions. Each has a short line under it in green when all is well and red when something needs me. Under them, a Progress card with a meter in the accent color and a short summary of the task, which becomes the final summary when it is done.
  - Steps: a table of number, step, status, and the time each status was set, with the step in progress highlighted.
  - Questions for you: a table of question, the default you will take if I do not answer, and whether it is open or answered by default.
  - Stuck: a table of what is blocked and what it is waiting for.
  - Latest results: a table of file and what changed, with paths relative to the project root.
  - Roadmap, where the project's docs keep one (such as a Roadmap section in docs/PRD.md): re-read it every time you update the page and show the milestones not yet complete, each proposed or planned update with its status, and anything explicitly deferred, above a card counting what is done. Copy nothing into the page by hand that the docs already say, so the two cannot disagree. Leave the section out where there is no roadmap.
  - Footer: one line saying this is a working page, not indexed, and that the published copy shows the state as of the last publish.
  - A section with nothing in it shows a short empty state ("Nothing is blocked.") rather than disappearing, so the layout never shifts.
  - Every status is a pill that carries a word as well as a color (Done, In progress, Waiting, Not started, Proposed, Deferred), never color alone. Tables sit in their own scrolling box, so a wide table never widens the page. Figures use tabular numbers, and panels share one border, radius, and background.
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
