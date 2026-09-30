# CLAUDE.md - Azqato's Prompts

Read `docs/PRD.md` first, section 20 above all: it is the working practice for this repository.

## Default rules

Never use subagents; do all work directly. Use headless Edge only, never Chrome, and only for local checks; the one exception is a single headless Edge load of a link a docs/TODO.md idea points to, when the web fetch tool cannot read it, never signed in. Never run state-changing checks against production. Before pushing: fetch, and if docs/TODO.md changed on the remote, keep the author's edits and ask about any ideas in it. After every change, update docs/PRD.md and docs/PATCHNOTES.md.

## Progress dashboard

For any task with more than 5 steps, or likely to take longer than 30 minutes, keep `dashboard/state.json` and regenerate `dashboard/index.html` with `python tools/dashboard.py`, as the Progress Dashboard prompt describes. Never edit the page by hand. Before starting, write the task, its steps, and the starting commit into `state.json`; after every step, and whenever something gets stuck or a question comes up, update `state.json` (status times from the system clock) and run the generator. Keep working on the default when a question waits. The generator reads everything else itself: latest results from git, the latest release from `docs/PATCHNOTES.md`, and the whole roadmap from `docs/PRD.md` section 27. Do not install any agents, subagents, or plugins. The page and `state.json` are tracked and go live with the site at https://azqato.github.io/prompts/dashboard/, so put nothing private in either, and keep the page's `noindex` tag.

Style, chosen 2026-09-27 after the look of 1000xstocks.com:

- Dark: near-black background `#0a0a0a`, panels `#141414`, borders `#2a2a2a`.
- Medium density: between compact and airy.
- Accent gold `#FFB800`, with a gold-to-amber gradient (`#FFB800` to `#f89e22`) on the progress bar and the in-progress badge.
- Panel labels in small uppercase with wide letter spacing, and pill-shaped status badges.
- System fonts only, since the page loads nothing from the network.

Layout, chosen 2026-09-27: the admin-dashboard template from the author's templateinterface repository, rebuilt inline in the palette above (the template's own graphite and amber colors are not used). A left sidebar with the brand, the current task, and section links with counts; a sticky top bar with the task name, a pulsing live dot with the time progress was last recorded, and the percent complete; four summary figures (steps done, in progress, stuck, open questions); a progress card with a gold meter and the summary; then tables for steps, questions, stuck items, results, and the latest release, and the full Roadmap from `docs/PRD.md` section 27 (every milestone with its scoped findings, every Future updates entry, deferred items, and every verification checklist row, completed ones dimmed), with status pills that carry a word as well as a color. Below 900px the sidebar becomes a strip of section links across the top. The page reloads every 10 seconds. Its one script, inline and with no network access, shows a "May be stale" banner when no progress has been recorded for the stale limit in `state.json` (30 minutes by default). Styles live in `tools/dashboard.css`. Changed 2026-09-30 from a hand-kept page to a generated one.
