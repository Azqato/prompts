# Azqato's Prompts

A static personal library of reusable Claude Code prompts. Built as a personal reference tool and organized knowledge base for prompt patterns that solve recurring development, documentation, and maintenance tasks.

Live site: [azqato.github.io/prompts](https://azqato.github.io/prompts/)

---

## What This Is

This site collects prompts that can be dropped directly into Claude Code. Each prompt is written as its own markdown file in `prompts/`, with a title, a plain-language description of what it does, and the full prompt text. The site reads those markdown files and renders a dedicated page for each one with a one-click copy button.

No frameworks, no build tools, no dependencies. Pure HTML, CSS, and vanilla JavaScript. It runs by opening `index.html` directly in a browser (no server required).

---

## How It Works

Prompts live as markdown files, not as hand-written HTML pages. There is one shared `index.html` shell. It uses hash-based routing (`index.html#/documentation`) to show either the home list or a single prompt.

Browsers block `fetch()` of local files when a page is opened from disk (`file://`), so the prompt markdown is also embedded in `prompts-data.js`, which the browser loads with a normal `<script>` tag. This is what lets the site run with no server and no dependencies. The `.md` files in `prompts/` remain the readable, editable source; `prompts-data.js` mirrors them.

---

## Files

| File | Description |
| --- | --- |
| `index.html` | Single-page shell: sidebar, content area, footer. Renders all views. |
| `css/style.css` | Full design system stylesheet shared across all views. |
| `js/prompts-data.js` | Embedded copy of every prompt markdown file, loaded via `<script>` so the site works offline and on `file://`. |
| `js/script.js` | Parses the embedded markdown, builds the sidebar, handles routing and copy-to-clipboard. |
| `prompts/add-prompt.md` | Add Prompt prompt: add a new prompt to the site by providing the raw text; Claude Code generates the title, description, and updates all required files. |
| `prompts/documentation.md` | Documentation prompt: crawl the codebase, then consolidate all docs into four core files with every supporting document, the house conventions, and the writing style folded into a deeply sectioned PRD. |
| `prompts/mobile-responsive-audit.md` | Mobile Audit prompt: audit every page at multiple breakpoints for overflow and layout bugs, fix root causes, verify with real DOM measurements, then document the fixes. |
| `prompts/github-wiki.md` | GitHub Wiki prompt: review every documentation file, then set up a new GitHub wiki or diff and update an existing one, with curated pages and a maintained sidebar. |

A prompt can set `hidden: true` in its frontmatter to stay reachable by direct link (`index.html#/<slug>`) while dropping out of the sidebar and home list. No prompt currently uses it. Consolidate Documents, Docs Folder Audit, and Documentation Audit were hidden this way from v1.9.0, then deleted in v1.19.0 once the Documentation prompt had fully superseded them. Em Dash Audit and Project Onboarding were retired in v1.23.0 for the same reason, once the Documentation prompt absorbed the writing style rule and the onboarding analysis as PRD sections of its own.

---

## Docs

| File | Description |
| --- | --- |
| `docs/PRD.md` | Product requirements, scope, writing style rules, and content philosophy |
| `docs/DESIGN.md` | Full design specification including color tokens, typography, layout, and components |
| `docs/PATCHNOTES.md` | Changelog updated after every meaningful change to the site |

---

## File Structure

```
prompts/
├── index.html
├── README.md
├── css/
│   └── style.css
├── js/
│   ├── prompts-data.js
│   └── script.js
├── prompts/
│   ├── add-prompt.md
│   ├── documentation.md
│   ├── mobile-responsive-audit.md
│   └── github-wiki.md
└── docs/
    ├── PRD.md
    ├── DESIGN.md
    └── PATCHNOTES.md
```

---

## Prompt Markdown Format

Each file in `prompts/` follows this structure:

```markdown
---
title: Mobile Audit
description: One-line summary shown in the home list.
meta: Claude Code Prompt
---

A paragraph (or more) describing what the prompt does and when to use it.

## Prompt

​```
The full prompt text goes here, inside a fenced code block.
​```
```

The frontmatter supplies the title, the home-list description, and the small meta label. Everything between the frontmatter and the `## Prompt` heading becomes the on-page description. The first fenced code block is the copyable prompt.

---

## Design

- GitHub Dark-inspired palette. Teal accent `#00d4a0`, background `#0d1117`, surface `#161b22`
- System fonts only, no external font loading
- CSS Grid sidebar layout with sticky positioning on desktop
- Responsive: sidebar collapses to sticky top nav below 1024px
- Full design specification in `docs/DESIGN.md`

---

## Running Locally

No build step and no server required. Open `index.html` directly in a browser. It also works unchanged when hosted on GitHub Pages.

---

## Adding a New Prompt

1. Create a new `.md` file in `prompts/` (e.g. `prompts/my-prompt.md`) using the markdown format above
2. Add its content to `prompts-data.js` so the browser can load it without a server, and add its slug to the display-order list in that file
3. Add a row to the Files table in this README if needed
4. Update `docs/PATCHNOTES.md` with a new version entry

## Renaming a Prompt

Rename the `.md` file with `git mv`, update the `slug` in `js/prompts-data.js`, resync its `raw` value from the renamed file, and fix the Files table and tree here. No redirect is needed: the files in `prompts/` are source, not the deployed page, and the router renders the home view for a slug it does not recognize. The full procedure is in `docs/PRD.md` under "Renaming Prompts".

## Removing a Prompt

The public surface of this project is the deployed page, not the source that builds it. Everything in `prompts/` is source, so a prompt is pruned outright: delete the `.md` file, remove its entry from `js/prompts-data.js`, remove its row and tree line here, and grep for any other prompt that mentions it by name. No redirect, no stub. A redirect is only for a genuine public address, meaning the deployed page itself or the paths it serves. The full procedure is in `docs/PRD.md` under "Removing Prompts".

---

## Content Philosophy

Every prompt page contains exactly three things: a title, a description of what the prompt does, and the prompt itself. Descriptions are written in plain language. No marketing copy, no filler. The goal is to find a prompt, understand it in one read, and copy it immediately.

---

## Author

**Azqato**, [azqato.github.io](https://azqato.github.io)
