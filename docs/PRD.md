# PRD.md — Prompts

**Version:** 1.0
**Status:** Active
**Author:** Azqato

---

## 1. Overview

Prompts is a static, GitHub Pages-hosted personal library for collecting and reusing Claude Code prompts. It provides a single, always-available reference point for prompt patterns that solve recurring tasks across development, documentation, writing, and maintenance workflows.

---

## 2. Problem

Useful Claude Code prompts are written once and then lost: buried in old chat threads, scattered across notes apps, or simply forgotten. There is no structured way to retrieve, read, or reuse them. The cost is time spent rewriting prompts from scratch or accepting lower-quality output when a known-good prompt cannot be found.

---

## 3. Solution

A minimal static website where each prompt is authored as a markdown file in `prompts/` and rendered into its own dedicated page. Each page provides a plain-language description of what the prompt does and a copyable code block containing the full prompt text. A persistent left sidebar lists all available prompts for instant access.

There are no per-prompt HTML files. A single `index.html` shell reads the prompt markdown and renders every view using hash-based routing.

---

## 4. Goals

- Provide a fast, frictionless way to find and copy any saved prompt
- Keep the site lightweight: no frameworks, no build tools, no dependencies
- Make adding a new prompt as low-effort as possible
- Maintain a consistent page structure across all prompt entries so the site is scannable

---

## 5. Non-Goals

- This is not a prompt marketplace or community resource
- This is not a search engine or tagging system (at v1.0; may be revisited)
- This is not a tool for generating or editing prompts inline
- This does not connect to any API or external service

---

## 6. Audience

Personal use only. The site is public (GitHub Pages default) but is built for a single author who knows what they are looking for.

---

## 7. Technical Requirements

- Pure HTML, CSS, and vanilla JavaScript
- No npm, no build step, no compile step
- No dependencies of any kind. The site must run by opening `index.html` directly from disk (the `file://` protocol) with no server
- Each prompt is a markdown file in `prompts/`. These files are the readable, editable source
- Because browsers block `fetch()` on `file://`, prompt markdown is also embedded in `prompts-data.js` and loaded with a `<script>` tag. This is the only way to read prompt content with no server while keeping markdown as the source format
- Single shared `index.html`, `style.css`, and `script.js`
- No external font loading; system font stack only
- No external JavaScript libraries
- Hosted on GitHub Pages under the azqato account; runs identically there and from local disk
- Works offline (no runtime dependencies, no network calls)

---

## 8. Page Structure

### Home View (index.html, no hash)

- Site title and one-paragraph description of what the library contains
- A scannable list of all prompts with their titles and one-line descriptions
- Each item links to that prompt's view (`index.html#/<slug>`)

### Prompt View (index.html#/<slug>)

Rendered from the matching markdown file in `prompts/`. Each prompt view contains exactly three sections in this order:

1. **Title**: the name of the prompt as an `h1`, from the markdown frontmatter
2. **Description**: one or more paragraphs explaining what the prompt does, when to use it, and any important behavior the user should know before running it
3. **Code Block**: the full prompt text in a `<pre><code>` block with a one-click copy button

No other sections. No decorative content. No padding between the prompt and the rest of the page beyond standard spacing.

### Prompt Markdown Files (prompts/*.md)

The source for each prompt. Frontmatter (`title`, `description`, `meta`, plus an optional `hidden`) plus a body: a description, then a `## Prompt` heading, then the full prompt inside a fenced code block. These files are mirrored into `prompts-data.js` for in-browser loading. Setting `hidden: true` keeps the prompt page live but removes it from the sidebar and home list.

### /docs/ Pages

Not rendered as navigable pages on the site. These are documentation files for contributors and for Claude Code context:

- `docs/PRD.md` — product requirements (this file)
- `docs/DESIGN.md` — full design specification
- `docs/PATCHNOTES.md` — version history

---

## 9. Navigation

- Left sidebar persists on all views on desktop (above 1024px)
- Sidebar contains the site logo, a Home link, one link per visible prompt, and a Support button pinned to the bottom
- Sidebar links are built dynamically from the prompt data; navigation uses hash routing, so switching views does not reload the page
- A prompt whose frontmatter sets `hidden: true` is excluded from both the sidebar and the home list, but its page stays reachable by direct link (`index.html#/<slug>`). This retires a prompt from navigation without breaking any existing link to it
- Active view is visually distinguished (teal text, 3px left border)
- The Support button links to `https://azqato.github.io/support.html` and opens in a new tab
- On mobile (below 1024px), sidebar collapses to a sticky top nav bar; the support button flows inline with the nav links
- In-page anchors are not used at v1.0

---

## 10. Copy Button Behavior

- Each prompt page has exactly one copy button, positioned above the code block
- On click: copies the full code block contents to clipboard
- Visual feedback: button text changes to "Copied!" for 2 seconds, then resets
- Requires no external library; uses the native Clipboard API

---

## 11. Writing Style

All copy on this site follows these rules. These rules apply to HTML pages, markdown documentation, and inline comments.

### Em Dashes

Em dashes are prohibited in all forms:

- Literal Unicode character: `—`
- HTML entity: `&mdash;`
- Double dash used as punctuation: `--` (note: this does NOT apply to CSS custom properties such as `--color-bg` or `--color-accent`, which are valid CSS variable syntax and must not be changed)

Both the Unicode character and the HTML entity must be searched independently when auditing, because a search for one will not catch the other.

Replace every instance using the most contextually appropriate alternative:

| Replacement | When to use |
| --- | --- |
| Comma | The most natural replacement in most cases; keeps the sentence flowing |
| Colon | Good when introducing a list, explanation, or elaboration after a complete clause |
| Semicolon | Useful when connecting two closely related independent clauses |
| Parentheses | Work well for asides or supplementary information |
| Period | Sometimes the cleanest fix is splitting into two sentences |

### General Tone

- Direct and functional. No marketing language.
- Descriptions explain what a prompt does and when to use it. Nothing more.
- Avoid filler phrases ("This prompt is designed to...", "Feel free to...").
- Write in plain declarative sentences.

### Prompt Content Rules

Prompts on this site are shared publicly and may be reused by anyone. Every prompt must follow these rules:

- **No GitHub push instructions.** Prompts must not instruct the user to push, commit, or publish to any remote repository. The user decides when and whether to push. Audit every new prompt for phrases such as "push everything to GitHub", "push to GitHub", "commit and push", or any equivalent before publishing.
- **No account-specific actions.** Prompts must not reference specific services, accounts, or credentials that belong to the author. Instructions should be portable across any project and any user.

Before adding a new prompt, review the full prompt text and remove any language that would cause it to take actions on behalf of a specific person or external service.

---

## 12. Adding Prompts

This is the canonical process for adding a new prompt, and how additions should be handled moving forward. Every new prompt follows the same steps so the site, the data file, and the docs never drift apart.

1. Create a new `.md` file in `prompts/` (e.g. `prompts/my-prompt.md`)
2. Fill in the frontmatter (`title`, `description`, `meta`), the description body, and the prompt inside a fenced code block under a `## Prompt` heading
3. Audit the prompt text against the Prompt Content Rules in section 11 before publishing. Remove any GitHub push or commit instructions and any account-specific actions. The `.md` file is the readable source of truth
4. Mirror the file's content verbatim into `js/prompts-data.js` as a `{ slug, raw }` entry, appended to the end of the `window.PROMPTS_DATA` array. The array order is the display order, so appending places the new prompt last in the sidebar and home list. Both update automatically with no HTML editing
5. Add a row to the Files table and the file structure tree in `README.md`
6. Add a version entry to `docs/PATCHNOTES.md` using the next semantic version, dated `YYYY-MM-DD`

When publishing the new prompt to GitHub Pages, that push is the author's decision and an action taken on the repository, not an instruction embedded in any prompt. The embedded prompt text must never tell its own reader to push or publish (section 11).

### Renaming Prompts

A prompt's slug is its public URL (`index.html#/<slug>`). Once the site is published, those URLs are outside this repo's control: they sit in bookmarks, chat history, and anywhere the prompt has been shared. Changing a slug therefore breaks links that cannot be found or fixed from here.

The rule is that a slug change is always paired with a redirect, never done bare. Renames are not avoided, since a stale name is a worse cost than a redirect entry, but the old URL must keep working.

When a prompt's title changes in a way that makes its slug or filename wrong:

1. Rename the `.md` file in `prompts/` to match the new slug, using `git mv` so the file's history is preserved
2. Update the `slug` for that entry in `js/prompts-data.js`. The `raw` value is resynced from the renamed `.md` file rather than hand-edited, so the two cannot drift
3. Add the old slug to the `REDIRECTS` map in `js/script.js`, mapping it to the new one. The router rewrites the hash to the current slug, so a reader arriving on an old link lands on the right page with a canonical address bar
4. Update the Files table and the file structure tree in `README.md`
5. Add a version entry to `docs/PATCHNOTES.md` recording the old name, the new name, and the redirect

Rules for the `REDIRECTS` map:

- **Entries are permanent.** There is no point at which removing one becomes safe, because the links it serves are not visible from this repo. The map only grows.
- **Never point a redirect at another redirect.** If a prompt is renamed twice, update the first entry to point at the current slug rather than chaining them. Every entry resolves to a real prompt in one hop.
- **Never reuse a retired slug** for a different prompt. The old URL would silently deliver the wrong content, which is worse than a broken link.
- The router guards every redirect on its target existing, so a stale entry falls through to the home view rather than trapping the reader in a dead end.

Historical records are not rewritten during a rename. Earlier patch notes and version history rows keep the name the prompt had at the time, since they are a record of what happened rather than a description of the current state.

---

## 13. Version History

| Version | Date | Summary |
| --- | --- | --- |
| 1.17.0 | 2026-08-23 | Added a `REDIRECTS` map to the router so renamed prompts keep their old URLs working, and made the redirect practice canonical in section 12. Completed the GitHub Wiki rename (`github-wiki-setup` to `github-wiki`) behind that redirect. Widened the content area to 75vw on wide screens with an 820px floor. |
| 1.16.0 | 2026-08-23 | Renamed the "GitHub Wiki Sync" prompt to "GitHub Wiki". Slug and filename unchanged so existing direct links keep working. |
| 1.15.0 | 2026-08-23 | Added the Project Onboarding prompt (`prompts/project-onboarding.md`), the ninth prompt: an eight-phase read-only intake of an unfamiliar project that merges its findings into `PRD.md` rather than reporting them to chat, additively and flagging contradictions instead of overwriting them. |
| 1.14.0 | 2026-07-06 | Renamed the GitHub Wiki Sync prompt's "Changelog" page to "Patch Notes" (`Patch-Notes.md`) to match this site's own terminology. |
| 1.13.0 | 2026-07-06 | Reworked the GitHub Wiki Setup prompt into GitHub Wiki Sync, adding an update mode (diff existing wiki pages against current docs before editing), open-ended page creation based on wiki information architecture, and a maintained `_Sidebar.md`. |
| 1.12.0 | 2026-07-06 | Added the GitHub Wiki Setup prompt (`prompts/github-wiki-setup.md`), the eighth prompt. |
| 1.11.0 | 2026-07-05 | Fixed a mobile/tablet header bug found by running the Mobile Audit prompt against the live site: `.sidebar-sticky` kept its desktop `height: 100vh` below 1024px, making the collapsed header full-viewport-tall with its content vertically centered inside; `.sidebar-nav` also squeezed into a narrow column beside the logo instead of wrapping full-width. Fixed both in `css/style.css`. |
| 1.10.0 | 2026-07-05 | Added the Mobile Audit prompt (`prompts/mobile-responsive-audit.md`), the seventh prompt. |
| 1.9.0 | 2026-06-27 | Added an optional `hidden` frontmatter flag. Hidden prompts are dropped from the sidebar and home list but stay reachable by direct link. Retired Consolidate Documents, Docs Folder Audit, and Documentation Audit from navigation while preserving their pages. |
| 1.8.0 | 2026-06-27 | Added the Documentation prompt (`prompts/documentation.md`), the most comprehensive of the documentation prompts: crawls the codebase, consolidates docs into four core files, and folds a full doc suite into a single deeply sectioned PRD. Expanded the Adding Prompts section into the canonical add-a-prompt workflow. |
| 1.0 | June 2026 | Initial release. Markdown-driven structure: prompts authored as `.md` files in `prompts/`, rendered by a single `index.html` shell with hash routing. Runs with no server or dependencies (`file://` compatible) via `prompts-data.js`. Em dash audit prompt added as first example. Writing style rules documented. |
