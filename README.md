# Azqato's Prompts

A static personal library of reusable Claude Code prompts. Built as a personal reference tool and organized knowledge base for prompt patterns that solve recurring development, documentation, and maintenance tasks.

Live site: [azqato.github.io/prompts](https://azqato.github.io/prompts/)

---

## What This Is

This site collects prompts that can be dropped directly into Claude Code. Each prompt is written as its own markdown file in `prompts/`, with a title, a plain-language description of what it does, and the full prompt text. The site reads those markdown files and renders a dedicated page for each one with a one-click copy button.

No frameworks, no build tools, no dependencies. Pure HTML, CSS, and vanilla JavaScript. It runs by opening `index.html` directly in a browser (no server required).

---

## How It Works

Prompts live as markdown files, not as hand-written HTML pages. There is one shared `index.html` shell. It uses hash-based routing (`index.html#/em-dash-audit`) to show either the home list or a single prompt.

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
| `prompts/em-dash-audit.md` | Em dash audit prompt: find and replace em dashes in all forms across all project files. |
| `prompts/consolidate-documents.md` | Consolidate Documents prompt: consolidate all documentation into four core files and enforce the correct folder structure. |
| `prompts/docs-folder-audit.md` | Docs Folder Audit prompt: crawl the entire codebase, then audit and rewrite every document in /docs to match the current state of the project. |
| `prompts/documentation-audit.md` | Documentation audit prompt: create or update the full documentation suite for any project. |
| `prompts/documentation.md` | Documentation prompt: crawl the codebase, then consolidate all docs into four core files with every supporting document folded into a deeply sectioned PRD. |
| `prompts/mobile-responsive-audit.md` | Mobile Audit prompt: audit every page at multiple breakpoints for overflow and layout bugs, fix root causes, verify with real DOM measurements, then document the fixes. |
| `prompts/github-wiki-setup.md` | GitHub Wiki Sync prompt: review every documentation file, then set up a new GitHub wiki or diff and update an existing one, with curated pages and a maintained sidebar. |
| `prompts/project-onboarding.md` | Project Onboarding prompt: read the codebase, structure, and documentation in a read-only pass, then merge everything learned into `PRD.md`. |

`consolidate-documents`, `docs-folder-audit`, and `documentation-audit` are marked `hidden: true` in their frontmatter. They are kept on the backend and stay reachable by direct link (`index.html#/<slug>`) but no longer appear in the sidebar or home list, since the Documentation prompt supersedes them.

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
│   ├── em-dash-audit.md
│   ├── consolidate-documents.md
│   ├── docs-folder-audit.md
│   ├── documentation-audit.md
│   ├── documentation.md
│   ├── mobile-responsive-audit.md
│   ├── github-wiki-setup.md
│   └── project-onboarding.md
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
title: Em Dash Audit
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

---

## Content Philosophy

Every prompt page contains exactly three things: a title, a description of what the prompt does, and the prompt itself. Descriptions are written in plain language. No marketing copy, no filler. The goal is to find a prompt, understand it in one read, and copy it immediately.

---

## Author

**Azqato**, [azqato.github.io](https://azqato.github.io)
