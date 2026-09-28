# CLAUDE.md - Azqato's Prompts

Read `docs/PRD.md` first, section 20 above all: it is the working practice for this repository.

## Default rules

Never use subagents; do all work directly. Use headless Edge only, never Chrome, and only for local checks. Never run state-changing checks against production. Before pushing: fetch, and if docs/TODO.md changed on the remote, keep the author's edits and ask about any ideas in it. After every change, update docs/PRD.md and docs/PATCHNOTES.md.

## Progress dashboard

For any task with more than 5 steps, or likely to take longer than 30 minutes, create and maintain `dashboard/index.html` as the Progress Dashboard prompt describes: one self-contained HTML file that opens by double-click and reloads every 10 seconds, showing the steps and their status, anything stuck, questions waiting for the author with the default you will take, and the latest results. Create it before starting, update it after every step, and keep working on the default when a question waits. Maintain it yourself in the session; do not install any agents, subagents, or plugins. The page is tracked and goes live with the site at https://azqato.github.io/prompts/dashboard/, so put nothing private on it, and keep its `noindex` tag.

Style, chosen 2026-09-27 after the look of 1000xstocks.com:

- Dark: near-black background `#0a0a0a`, panels `#141414`, borders `#2a2a2a`.
- Medium density: between compact and airy.
- Accent gold `#FFB800`, with a gold-to-amber gradient (`#FFB800` to `#f89e22`) on the progress bar and the in-progress badge.
- Panel labels in small uppercase with wide letter spacing, and pill-shaped status badges.
- System fonts only, since the page loads nothing from the network.

Layout, chosen 2026-09-27: the admin-dashboard template from the author's templateinterface repository, rebuilt inline in the palette above (the template's own graphite and amber colors are not used). A left sidebar with the brand, the current task, and section links with counts; a sticky top bar with the task name, a pulsing live dot with the update time, and the percent complete; four summary figures (steps done, in progress, stuck, open questions); a progress card with a gold meter and the summary; then tables for steps, questions, stuck items, and results, and a Roadmap section read from `docs/PRD.md` section 27 each time the page is built (milestones not yet complete, every Future updates entry with its built or proposed status, deferred items, and how many sections the verification checklist has verified), with status pills that carry a word as well as a color. Below 900px the sidebar becomes a strip of section links across the top. No script: the page reloads every 10 seconds instead.
