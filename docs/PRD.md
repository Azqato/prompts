# PRD.md - Prompts

**Version:** 1.33.1
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

Section 21 carries the detailed personas behind this one-line scope decision, including the secondary reader who arrives at a single prompt by direct link with no context, who is why the Prompt Content Rules in section 11 exist.

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
- A Content Security Policy in `index.html` enforces the above at runtime. `script-src 'self'` and `connect-src 'none'` mean a CDN script or a `fetch()` added later fails in the browser rather than shipping a page that quietly broke the no-dependency rule. See section 31
- Maintenance tooling is permitted where it is not part of the deployed artifact, does not run in a browser, and uses no third-party package. `tools/prompts-mirror.py` is the only such tool. Deleting it leaves the site unchanged, which is the test for whether something is tooling or a dependency

These are the constraints. Section 30 describes the implementation they produced: the data models, the internal data flow, state management, performance budget, and the known technical debt each constraint bought. Section 29 is the runbook.

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
3. **Code Block**: the full prompt text in a `<pre><code>` block, behind a header bar carrying a collapse toggle and a one-click copy button. The block is collapsed when the page opens; see section 10a

No other sections. No decorative content. No padding between the prompt and the rest of the page beyond standard spacing.

### Prompt Markdown Files (prompts/*.md)

The source for each prompt. Frontmatter (`title`, `description`, `meta`, plus an optional `hidden`) plus a body: a description, then a `## Prompt` heading, then the full prompt inside a fenced code block. These files are mirrored into `prompts-data.js` for in-browser loading. Setting `hidden: true` keeps the prompt page live but removes it from the sidebar and home list.

### /docs/ Pages

Not rendered as navigable pages on the site. These are documentation files for contributors and for Claude Code context:

- `docs/PRD.md`: product requirements (this file)
- `docs/DESIGN.md`: full design specification
- `docs/PATCHNOTES.md`: version history

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
- The button sits in the code block header bar and is present whether the block is shown or hidden, so copying never requires expanding first

---

## 10a. Prompt Collapse Behavior

Added in v1.29.0. Numbered `10a` rather than inserted as a new section 11, because nine releases of patch notes cite this document by section number and renumbering would silently invalidate all of them. Section 33 records the rule.

- **The prompt block is collapsed when a prompt page opens.** Every page load and every navigation starts collapsed. The prompts run to several hundred lines, and an expanded default pushed the description, which explains what the reader is about to copy, off the top of a screen.
- The header bar carries a toggle labelled **Expand** when hidden and **Hide** when shown. The label names the action the button performs, not the state it is in, which is the convention the copy button already sets.
- **The entire header bar is clickable**, not only the toggle. A click anywhere on the bar toggles the block, except on the copy button, so copying never collapses what was just copied.
- Copy works in both states. The prompt text stays in the DOM while hidden; only its display is suppressed. This is what keeps the primary action one click from arrival despite the collapsed default.
- **The state is not persisted.** No browser storage API is used anywhere in the project, and section 31 states that as a privacy property. Remembering a reader's preference here would cost that for a small convenience, so it is deliberately not done.
- There is no animation on the collapse. It is a display change, not a transition. `docs/DESIGN.md` section 12b forbids transitioning height or transform, which rules out both an animated open and a rotating chevron.

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
| Single hyphen | Permitted and encouraged where context justifies it. Preferred in document titles, section headings, and version lines |

The single hyphen is not prohibited. The ban covers the em dash character, the `&mdash;` entity, and the double dash used as punctuation, and nothing else. Because a hyphen is the closest visual match to the em dash it replaces, it is the right choice in document titles (`# PRD.md - Prompts`) and in version headings (`## v1.17.0 - 2026-08-23`), where a comma or colon reads awkwardly. In running prose, the other replacements are usually better.

An instance is left in place when the text needs the character to mean anything: the three bullets above name the forms they prohibit, and the Writing Style section of the Documentation prompt quotes them so a model knows what to search for. Replacing those would destroy the line.

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

A prompt is authored as a `.md` file in `prompts/`, and its slug is derived from that filename. Source files are not public facing, so a rename is an internal change and is done bare, with no redirect.

When a prompt's title changes in a way that makes its slug or filename wrong:

1. Rename the `.md` file in `prompts/` to match the new slug, using `git mv` so the file's history is preserved
2. Update the `slug` for that entry in `js/prompts-data.js`. The `raw` value is resynced from the renamed `.md` file rather than hand-edited, so the two cannot drift
3. Update the Files table and the file structure tree in `README.md`
4. Search the repository for the old slug and the old title, and fix any reference that describes the current state
5. Add a version entry to `docs/PATCHNOTES.md` recording the old name and the new name

The router renders the home view for a slug it does not recognize, so an old hash resolves to a working page rather than an error.

Historical records are not rewritten during a rename. Earlier patch notes and version history rows keep the name the prompt had at the time, since they are a record of what happened rather than a description of the current state.

### Removing Prompts

A redirect exists to keep a public address working. Whether one is needed is decided by whether the thing being removed is public facing, not by whether it is being removed.

**The public surface of this project is the deployed page, not the source that builds it.** `index.html` and the asset paths it loads are public. Everything under `prompts/` is source: a prompt's slug is derived from its filename, so a prompt is internal no matter how it is removed.

- **Source is pruned entirely.** Delete the `.md` file, remove its data entry, and move on. No redirect, no alias, no stub, no tombstone. The router already renders the home view for an unrecognized slug, so nothing is left broken.
- **A genuine public address is retired behind a redirect.** That means the deployed page itself or the paths it serves, not the prompts inside it. Any entry added to the `REDIRECTS` map is permanent, never chains, and is never reused to point at different content, since a reused address silently serves the wrong thing.

The same test applies to any file in this repository. Ask whether the thing is source or deployed artifact. Source is deleted; a live address is retired.

Deleting a prompt touches:

1. Delete the `.md` file from `prompts/`
2. Remove its `{ slug, raw }` entry from `js/prompts-data.js`
3. Remove its row from the Files table and its line from the file structure tree in `README.md`
4. Search the repository for references to the prompt by slug and by title, and fix any that describe the current state. One prompt's description referring to another by name is the common case
5. Add a version entry to `docs/PATCHNOTES.md` recording what was deleted and why

As with renames, historical records are left alone. Earlier patch notes describing a prompt that has since been deleted stay as they are, because they record what happened at the time. That includes patch notes describing redirects that no longer exist.

The `hidden: true` flag remains supported for retiring a prompt from navigation without deleting it. As of v1.19.0 no prompt uses it.

---

## 13. Repository Structure

The whole project is 13 files in five folders. There is no build output, no vendored code, no ignored directory, and no ignore file: `.gitignore`, `.editorconfig`, and `.vscode/` are all absent, so every file in the working tree is tracked.

There is no `.gitattributes` either, which has one consequence worth knowing: the repository stores LF, but `core.autocrlf` is true by default on Windows, so a fresh clone puts CRLF in the working tree while the `raw` values inside `js/prompts-data.js` stay LF, because they are JSON escapes rather than real line breaks and git never rewrites them. Any comparison between the two must normalize line endings or it will report drift that is not there. `tools/prompts-mirror.py` does. Whether to add a `.gitattributes` pinning LF is open question 5 in section 19.

```
/
├── index.html          Single-page shell. The only HTML file.
├── README.md           Front door: what the site is, file table, add and rename procedures.
├── css/
│   └── style.css       Entire stylesheet, 540 lines, no imports.
├── js/
│   ├── prompts-data.js Hand-maintained mirror of prompts/*.md. Largest file by far.
│   └── script.js       All client logic: parse, render, route, copy.
├── prompts/            Four .md files, one per prompt. The readable source.
├── tools/
│   └── prompts-mirror.py  Maintenance only. Checks or resyncs the mirror.
│                       Not served, not loaded, not a build step.
└── docs/
    ├── PRD.md          This file.
    ├── DESIGN.md       Design specification.
    └── PATCHNOTES.md   Changelog, reverse chronological.
```

The tree is two levels deep at most. `js/prompts-data.js` is large only because each prompt is stored as one long JSON string on a single line; it is generated content in spirit but is committed and edited by hand.

---

## 14. Architecture and Flow

Traced from the code rather than from the docs.

1. `index.html` loads `css/style.css`, then `js/prompts-data.js`, then `js/script.js`, in that order. The body ships as an empty shell: `#sidebar-nav` and `#content` are both empty in the source and filled entirely by script.
2. `js/prompts-data.js` assigns `window.PROMPTS_DATA`, an array of `{ slug, raw }` objects. Nothing else is in the file.
3. `js/script.js` runs `init()` on `DOMContentLoaded`, or immediately if the document is already parsed. `init()` validates that `PROMPTS_DATA` is a non-empty array, maps each entry through `parsePrompt()`, builds the sidebar, binds `hashchange`, and calls `route()`.
4. `parsePrompt()` splits frontmatter with a single regex, reads `title`, `description`, `meta`, and `hidden`, takes the first fenced code block in the body as the prompt text, and treats everything before that fence (minus a trailing `## Prompt` heading) as the description.
5. `renderMarkdown()` is a hand-rolled markdown subset applied only to the description: it splits on blank lines and handles headings, all-bullet blocks as `<ul>`, and paragraphs. `renderInline()` handles inline code, bold, and links on HTML-escaped text.
6. `route()` reads the hash, resolves any entry in the `REDIRECTS` map (guarded on the target existing, and empty as of v1.24.0), finds the prompt, and calls `renderHome()` or `renderDetail()`. An unknown slug silently falls through to the home view. `renderDetail()` also sets `document.title`, wires the copy button, and wires the collapse toggle.
7. If `PROMPTS_DATA` is missing or `parsePrompt()` throws, `renderError()` paints a `.status-message` panel telling the reader to check that `prompts-data.js` is present and loaded first. This view exists in both `js/script.js` and `css/style.css` but is not described in section 8 or in `docs/DESIGN.md`.

`js/script.js` is the only file with logic. `js/prompts-data.js` is the only data source. There is no state beyond the module-level `PROMPTS` array and the URL hash, nothing is persisted, and there are no network calls, storage APIs, or external services at runtime. The single browser API dependency is `navigator.clipboard.writeText()` in the copy button. The collapse state added in v1.29.0 is held entirely in a CSS class on one element, which is why it does not count as state and does not survive a navigation.

---

## 15. Code Conventions

Derived from the existing files. These describe what is there, not what is aspired to.

### JavaScript (js/script.js)

- Two-space indent, single quotes, semicolons always, `const` and `let` only.
- Plain function declarations in `camelCase`. No arrow functions, no classes, no template literals, no `async`. Callbacks are written `function () {}` even inside `forEach`. This is deliberate ES5-flavoured code, not accident: match it.
- Module-level constants in `SCREAMING_SNAKE_CASE` (`SITE_INTRO`, `PROMPTS`, `REDIRECTS`).
- No exports and no module system. Everything is a global in one script.
- HTML is built by string concatenation into `innerHTML`, with `escapeHtml()` applied to every interpolated value.
- The file is divided by banner comments in the form `/* ---------- Section ---------- */`, preceded by one boxed header comment at the top. Comments explain why rather than what, and are used sparingly on non-obvious decisions (the redirect guard, the hidden flag, the fence heuristic).
- Error handling is minimal by design: one `try/catch` around parsing and one array guard, both routed to `renderError()`. There is no logging.

### CSS (css/style.css)

- Two-space indent, one boxed header comment, `/* Section */` comments in the order listed in `docs/DESIGN.md` section 11.
- All colors, fonts, and sizes come from `:root` custom properties. No hex value appears outside `:root`, only `rgba()` accent variants in hover and copied states.
- Class names are lowercase kebab-case, BEM-ish but not strict (`.code-block-wrapper`, `.prompt-list-title`).
- Two media queries only, `max-width: 1023px` and `max-width: 767px`, both at the bottom of the file, plus `prefers-reduced-motion`.

### Markdown

Prompt files follow the template in section 8. Docs use `## N. Title` numbered sections separated by horizontal rules, and end with a version history table.

### Commits

- One commit per release group, subject line in imperative mood with the versions in parentheses, for example `Add slug redirects, complete the GitHub Wiki rename, widen content (v1.16.0-v1.17.0)`.
- Bodies are long and explanatory, wrapped near 72 characters, describing the reasoning and not just the change.
- Work happens directly on `main`. There are no other branches, local or remote, and no tags.

---

## 16. Binding Rules and Constraints

Every explicit rule found in the documentation, collected in one place. Sources are cited so each can be traced back.

- No frameworks, no build step, no npm, no dependencies of any kind (PRD 7, README).
- The site must run by opening `index.html` from disk on `file://`. This is why prompt markdown is embedded in `js/prompts-data.js` rather than fetched (PRD 7, DESIGN 12).
- `js/prompts-data.js` must load before `js/script.js` (DESIGN 12).
- The `.md` files in `prompts/` are the source of truth. `js/prompts-data.js` mirrors them verbatim and is resynced from the file rather than hand-edited (PRD 12).
- No external font loading. System font stack only (PRD 7, DESIGN 13).
- No external JavaScript libraries and no syntax highlighting library (PRD 7, DESIGN 13).
- Dark theme only. No light backgrounds, no gradient backgrounds, no decorative images (DESIGN 13).
- Do not deviate from the `#00d4a0` accent. It is the cross-site brand color (DESIGN 13).
- No animation beyond the copy button state transition and sidebar link hover (DESIGN 13).
- Em dashes are prohibited in all three forms in all copy, including markdown docs and inline comments. CSS custom properties such as `--color-bg` are exempt (PRD 11). See section 18 for where the docs currently break this.
- No marketing language, no filler phrases, plain declarative sentences (PRD 11).
- A prompt page contains exactly three things: title, description, code block. No other sections (PRD 8).
- Prompt text must never instruct its reader to push, commit, or publish to a remote (PRD 11). Verified clean across all four prompts on 2026-08-23.
- Prompt text must not reference the author's specific services, accounts, or credentials (PRD 11).
- The public surface is the deployed page, not the source that builds it. Files under `prompts/` are source, so renaming or removing a prompt is done bare, with no redirect (PRD 12).
- A genuine public address is retired behind a `REDIRECTS` entry, which is then permanent, never chains, and is never reused for different content (PRD 12).
- Historical patch notes and version history rows are never rewritten during a rename (PRD 12).
- Adding a prompt touches five places in order: the `.md` file, `js/prompts-data.js`, the README Files table, the README structure tree, and `docs/PATCHNOTES.md` (PRD 12, README).
- Documentation consolidates into exactly four files: `README.md` at the root, and `PRD.md`, `DESIGN.md`, `PATCHNOTES.md` in `/docs` (README, and the project's own Documentation prompt).
- The Content Security Policy in `index.html` keeps `script-src 'self'` and `connect-src 'none'`. Weakening either removes the runtime enforcement of the no-dependency rule (PRD 7, 31).
- `tools/prompts-mirror.py` is run after any change to `prompts/*.md`, and its check must pass before a commit (PRD 20, 29).
- Maintenance tooling must use no third-party package and must not be required to build, serve, or run the site (PRD 7).

---

## 17. Stack, Tooling, and Deployment

Recorded because a reader may reasonably expect a toolchain and there is none.

- Languages: HTML, CSS, and ES5-style vanilla JavaScript. No transpilation, no modules, no runtime.
- There is no `package.json`, no lockfile, and no dependency manifest of any kind, and therefore no dependency list, no scripts, and no task runner.
- There is no test suite, no linter, no formatter, and no type checker, configured or installed. Nothing validates a change except loading the page.
- There is no continuous integration. `.github/` does not exist, so no workflow or action runs on push.
- The remote is `https://github.com/Azqato/prompts.git`, single branch `main`, published at `https://azqato.github.io/prompts/`.
- The Pages publishing source is `main` at the repository root, confirmed by the author on 2026-08-23. It is set in the GitHub project settings, not in the repository, so nothing here reflects it. Publishing is a manual push.
- No environment variables, no secrets, and no external services at build or runtime. The only outbound links are the Support button and the footer, both to `azqato.github.io`.
- Running locally: open `index.html`. That is the entire procedure.

---

## 18. Documentation Versus Reality

Observed on 2026-08-23 by reading the code against the docs. Items 2, 5, and 6 were resolved in v1.18.0 and are kept here as a record of what was found and what was decided. The rest are open.

| # | Documentation says | Code shows | Notes |
| --- | --- | --- | --- |
| 1 | `README.md`, "Adding a New Prompt" step 2: add the new slug "to the display-order list in that file" | There is no display-order list in `js/prompts-data.js`. Display order is the order of the `window.PROMPTS_DATA` array, which is what `buildSidebar()` and `renderHome()` iterate | Section 12 step 4 of this PRD describes it correctly. The README wording looks like a leftover from an earlier data shape. Trust the code |
| 2 | `docs/DESIGN.md` section 2 lists `--color-card-hover` as "Card hover background" and `--color-purple` as "Gradient accent on card hover top border". Section 13 says "only gradient is the 2px top border on card hover" | Both tokens are defined in `css/style.css` and referenced nowhere. `.prompt-list-item:hover` sets `background: none` explicitly, and no gradient exists anywhere in the stylesheet | **Resolved in v1.18.0:** the treatment was intended and unbuilt, so it was built. Both tokens are now in use and DESIGN section 5 was rewritten to spec the card |
| 3 | `docs/DESIGN.md` section 12 shell template shows `.sidebar` containing the logo, nav, and support div directly | `index.html` wraps all three in a `.sidebar-sticky` div, which carries the sticky positioning and the flex column that pins the Support button. `css/style.css` depends on it | **Resolved in v1.28.0.** Flagged rather than fixed in v1.27.0 under the merge rule, then corrected once the author confirmed it was a stale transcription with no intended design in it. The template now matches `index.html` and names its three load-bearing elements |
| 4 | `docs/DESIGN.md` section 11 CSS file structure lists "Layout (site-wrapper flex, site-layout grid)" | There is no `.site-layout` class. `.site-wrapper` is the grid. The listed order also omits the status message block and the focus styles | **Resolved in v1.28.0.** Same history as item 3. The list is now read from the stylesheet, in the file's actual order, with the four omitted blocks added |
| 5 | Both `docs/PRD.md` and `docs/DESIGN.md` carry `**Version:** 1.0` in their headers | Their own version history tables run to 1.17.0 and 1.5 respectively | **Resolved in v1.18.0:** the field tracks the current release. PRD is now 1.18.0 (site version) and DESIGN is 1.6 (its own document version). Update it with every release |
| 6 | Section 11 of this PRD prohibits em dashes in markdown documentation | `docs/PATCHNOTES.md` uses a literal em dash in all 20 version headings. `docs/PRD.md` uses one in its title and in the three `/docs/` bullets of section 8. `docs/DESIGN.md` uses one in its title | **Resolved in v1.18.0:** all 25 replaced with single hyphens, plus one prose instance in a v1.11.0 patch note and one double dash in `prompts/documentation-audit.md`. Section 11 now states that the single hyphen is permitted and encouraged, and that instances naming the prohibited character are left alone |
| 7 | Section 7 of this PRD: "Single shared `index.html`, `style.css`, and `script.js`" | The assets moved to `css/style.css` and `js/script.js` in v1.6.0 | Wording only. The constraint it expresses still holds |
| 8 | Section 11 of this PRD: prompts must not reference the author's specific services or accounts | `prompts/consolidate-documents.md` and `prompts/documentation-audit.md` both instruct "Link to the currently live site (ex: https://azqato.github.io/)" | **Resolved in v1.19.0:** both prompts were deleted, so the question is moot. If the pattern reappears in a live prompt, it needs deciding then |
| 9 | Section 13 of this PRD described `css/style.css` as 509 lines | The file is 536 lines, and has been since the card hover was added in v1.18.0 | **Corrected in v1.27.0.** A line count carries no intent, so it was fixed in place rather than flagged. See the mechanical-fact exception in section 33 |
| 10 | The closing paragraph of this section said the Em Dash Audit and Project Onboarding prompts "were retired behind redirects" | Those redirects were deleted in v1.24.0, when the definition of public facing was corrected. Both retirements are now plain deletions | **Corrected in v1.27.0.** The sentence described the v1.23.0 state and was not updated by v1.24.0. Note that the v1.23.0 *patch note* still describes the redirects and is deliberately left alone, because it records what happened at the time. The distinction is that this table describes the current state |
| 11 | Section 19 of this PRD: "there are no TODO, FIXME, or HACK markers anywhere in the repository" | A literal search now matches in `docs/PRD.md`, `prompts/documentation.md`, and `js/prompts-data.js` | **Corrected in v1.27.0.** All matches are prose naming the markers, in the sentence that makes this claim and in the Documentation prompt's instruction to look for them. There are no real markers. The claim needed the same "naming the thing" exemption that section 11 gives the em dash rule, and now has it |
| 12 | `README.md`, "Adding a New Prompt" and the file structure tree, plus the Files table, the prompt markdown format, and "Running Locally" | All still accurate, but all now barred from the README by the standard adopted in v1.26.0, which restricts it to a general reader | **Resolved in v1.27.0** by scope rather than by correction. The README was rewritten to the new standard and this material moved into sections 29, 30, and 33 of this document. Item 1 above disappeared with it. Nothing was silently corrected: the content was relocated intact |
| 13 | `docs/DESIGN.md` section 2 marks `--color-negative` and `--color-warning` as "unused at v1.0" | Both are still defined and still referenced nowhere, at v1.27.0 | Trust both: the tokens are genuinely unused and the note is genuinely stale. Annotated in place in v1.27.0 rather than removed, since the tokens are reserved deliberately for future error and caution states |
| 14 | `docs/DESIGN.md` section 9 responsive table lists what changes below 1024px | It omits `height: auto` on `.sidebar-sticky` and `flex-basis: 100%` on `.sidebar-nav`, both of which are the load-bearing v1.11.0 bug fixes | Trust the stylesheet. Documented in DESIGN section 9 in v1.27.0, because a future edit that removes either one silently reintroduces a shipped bug |
| 15 | Nothing documented it, because nothing had noticed | `core.autocrlf` is true system-wide and there is no `.gitattributes`, so a fresh Windows clone gets CRLF `prompts/*.md` while the `raw` values in `js/prompts-data.js` stay LF. The two would never compare equal | **Found in v1.28.0** while testing `tools/prompts-mirror.py`, which failed on a file git had just checked out. The script now normalizes line endings on both sides, since they are a property of the checkout rather than of the content. Whether to pin LF with a `.gitattributes` is open question 5 |
| 16 | Section 24 of this document, Assumptions: "`escapeHtml()` does not escape quotes, and `renderInline()` writes a markdown link target directly into an `href` attribute" | Both quote forms have been escaped since v1.28.0, and section 30 of this same document records the fix and strikes it from the debt table | **Corrected in v1.29.0.** The v1.28.0 pass updated sections 30 and 31 for the escaping change and missed this one, so the document contradicted itself for a release. Found by reading section 24 while checking whether the collapse work touched any stated assumption. Worth noting as a pattern: a fact repeated in more than one section will go stale in the copy nobody was editing |

Confirmed accurate, checked rather than assumed:

- All four `prompts/*.md` files are mirrored byte for byte in `js/prompts-data.js`, with no orphans in either direction. Nine at the time of the v1.18.0 pass, before three were deleted in v1.19.0 and two more retired in v1.23.0.
- The `hidden: true` behaviour was verified working on the three prompts that used it, before they were deleted in v1.19.0: excluded from the sidebar and home list, still reachable by direct hash, exactly as sections 8 and 9 describe. No prompt uses the flag now.
- The `REDIRECTS` map is empty as of v1.24.0. The mechanism is retained, guarded on the target existing, for a genuine public-facing address; prompt slugs are not one, as section 12 describes.
- The color tokens, typography scale, breakpoints, and copy button states in `docs/DESIGN.md` match `css/style.css`, apart from item 2 above.
- The `--content-max` formula, `max(820px, calc(75vw - 56px))`, matches the section 4 description in `docs/DESIGN.md`.

Implemented but undocumented at the time of the v1.18.0 pass: the error view (`renderError()` and `.status-message`); the fact that `renderMarkdown()` also handles headings, which the DESIGN subset list omits; the scroll to top on every route change. All three were documented in v1.27.0, the error view in `docs/DESIGN.md` section 5 and the other two in section 30 of this document.

Checked and confirmed clean on 2026-08-23 during the v1.27.0 audit:

- All four `prompts/*.md` files are byte-identical to their `js/prompts-data.js` entries, with no orphan in either direction.
- Every em dash form was searched independently across all twelve files. Eight matches, every one an instance that names the character it prohibits (three in section 11 of this document, one in the Documentation prompt's Writing Style section, its mirror in `js/prompts-data.js`, and two historical patch notes describing the rule). Zero violations. Zero double dashes used as punctuation.
- No secret, credential, token, API key, or environment variable exists anywhere in the repository. No `fetch`, `XMLHttpRequest`, `localStorage`, `sessionStorage`, or `indexedDB` appears in any file.
- Every class name used in `index.html` and `js/script.js` is defined in `css/style.css`, with no orphans.
- The three outbound URLs are the W3C SVG namespace in the favicon data URI and two links to the author's own domain.

---

## 19. Risks and Open Questions

### Fragile areas

- `js/prompts-data.js` is a hand-maintained duplicate of `prompts/*.md`. Nothing enforces the mirror. If the two drift, the site silently serves the stale copy and the `.md` file that looks authoritative is not what readers see. This is the highest-value thing to verify before and after any prompt edit.
- One malformed escape in `js/prompts-data.js` is a parse error that leaves `window.PROMPTS_DATA` undefined and the site on the error view. With no tests and no continuous integration, only loading the page catches it.
- `escapeHtml()` in `js/script.js` escapes `&`, `<`, and `>` but not quotes, and `renderInline()` interpolates a markdown link target straight into `href="$2"`. A description containing a quote inside a link target would break out of the attribute. All content is author-written, so this is not an active exposure, but it is a real edge worth knowing before descriptions are ever sourced from anywhere else.
- `parsePrompt()` takes the first fenced code block in the body as the prompt. A description that includes a fenced example before the `## Prompt` heading would be published as the prompt text.
- The frontmatter parser is line-based. A wrapped or multi-line `description` value would drop everything after the first line without error.
- `--content-max` uses a `max()` floor that is load-bearing at the 1023px breakpoint, not cosmetic. Simplifying it to a flat `75vw` shrinks the content on tablets. This is documented in `docs/DESIGN.md` section 4. Do not undo it without reading that paragraph.

### Work in progress

None outstanding. The working tree is clean and `main` matches `origin/main`. There is one branch, no other branch local or remote, and no tags.

No real TODO, FIXME, or HACK marker exists in the codebase. A literal search does match in three files, but every match is prose naming the markers rather than marking anything: the sentence you are reading, the Documentation prompt's instruction to search for them, and that prompt's mirror in `js/prompts-data.js`. The same exemption applies here that section 11 gives to text naming a prohibited character.

The standing verification gap recorded here in v1.27.0 is closed. The card hover built in v1.18.0 had been specified, styled, and documented without the page ever being opened. In v1.28.0 the site was rendered in headless Chrome from `file://` at three routes (home, a prompt page, and an unknown slug) and confirmed working: four cards, five nav links, the copy button present on a detail page, the correct `h1` on each, and an unknown slug falling through to the home view as designed.

### Limits of the v1.27.0 analysis

Stated plainly, because the confident parts of a document are worth less than the honest edges.

- **The v1.27.0 audit executed nothing.** It was performed entirely by reading files and searching them. That was corrected in part by v1.28.0, which rendered the site in headless Chrome and empirically verified the Content Security Policy, the three routing cases, and the mirror script against real drift. Still unexecuted: the copy button has never been clicked, because a headless DOM dump cannot exercise the Clipboard API, so both its success and failure paths are traced from source rather than observed. The performance figures in section 28 remain estimated from file sizes and request counts, not measured.
- **The contrast ratios in `docs/DESIGN.md` section 10 were not recomputed.** They are carried forward from earlier versions of that document and are stated there as approximate.
- **The claim that browsers from 2021 onward support every feature used** (section 29) is a judgment from the feature list, not a compatibility matrix checked against a support table.
- **The GitHub Pages configuration cannot be read from the repository.** Section 17 records it on the author's confirmation, which remains the only source.

### Open questions for the author

Numbered so they can be answered by reference. An answered question is folded into the relevant section and marked answered here rather than deleted.

5. Should a `.gitattributes` pin `* text=auto eol=lf` so the working tree matches what the repository stores? Found in v1.28.0: `core.autocrlf` is true system-wide and there is no `.gitattributes`, so a fresh Windows clone gets CRLF source files while the `raw` strings inside `js/prompts-data.js` stay LF forever. `tools/prompts-mirror.py` normalizes around this and is not affected. The argument for pinning: the mismatch is latent and will surprise the next person or tool that compares the two literally, as it surprised the script. The argument against: it changes checkout behaviour for a problem that is currently handled, and it would rewrite line endings across the working tree on the next checkout.
6. The copy button's success and failure paths have never been exercised, only read. A headless DOM dump cannot drive the Clipboard API. Is a manual click worth doing before the next release, or is the code simple enough to trust?
7. This repository has no `LICENSE.md`, and as of v1.33.0 the Documentation prompt says that a project without one falls to a default of all rights reserved, source-available, with a standing carve-out for search and AI citation. The prompt would have this project ship that LICENSE and a `robots.txt` marked deliberately open. It was not done in v1.33.0, because a licence is a legal assertion published under the author's name rather than a documentation change, and because the four prompts are written to be copied and used, which is a posture worth stating deliberately rather than inheriting from a default. Should the default be applied here, adjusted, or explicitly declined and recorded as declined? Declining and saying why is a valid answer; leaving no licence and no note is the only outcome that carries a real cost, because it leaves a reader guessing.

Answered on 2026-08-23, all four of the previous questions, and folded into the relevant sections:

1. **The two stale `docs/DESIGN.md` blocks were corrected outright** rather than left flagged, on the reasoning that neither preserved an intended design: a shell template missing the wrapper the layout depends on is a transcription error, not a specification. Section 18 items 3 and 4 are marked resolved and record the history.
2. **Both cheap technical debt items were fixed.** `escapeHtml()` now escapes both quote forms, and the slug is escaped where it is interpolated into `href` and `data-slug`, which is the same fix applied consistently. The clipboard write now reports failure instead of silently doing nothing.
3. **The mirror script was built and committed** as `tools/prompts-mirror.py`, with a `--sync` mode so the resync procedure stops being reinvented each session. It also checks for orphans, duplicates, missing frontmatter, and a missing prompt fence.
4. **A Content Security Policy was added** to `index.html`, after testing that it does not break `file://` loading and, more importantly, that it is genuinely enforced.

Answered on 2026-08-23 and folded in above: em dashes were audited (single hyphen adopted), the card hover was built, the `**Version:**` header now tracks the release, Pages publishes `main` at the repository root by manual push, the three hidden prompts were deleted outright under the removal policy now in section 12, and the Em Dash Audit and Project Onboarding prompts were absorbed into the Documentation prompt and deleted. They were briefly retired behind redirects in v1.23.0, which v1.24.0 removed once the definition of public facing was corrected. Question 1 of the previous list, on the README "display-order list" wording, was resolved in v1.27.0 when the README was rewritten to the standard adopted in v1.26.0 and that section was relocated to section 33.

---

## 20. Working Practice for This Repository

The approach to take on future tasks here.

### Always, before editing

- Read sections 11 and 12 of this PRD before touching a prompt, and `docs/DESIGN.md` section 13 before touching CSS. Both contain prohibitions that are easy to break by writing ordinary-looking code.
- Confirm which of the two copies of a prompt is being changed. Edit the `.md` file first, then resync `js/prompts-data.js` from it verbatim rather than hand-editing the JSON string.
- Check whether a change alters a slug. If it does, it is a rename and follows the procedure in section 12. No redirect: prompt files are source.
- Before deleting anything, ask whether it is source or deployed artifact. Source is deleted outright. Only a live public address is retired behind a redirect. See section 12, "Removing Prompts".

### Never

- Never add a dependency, a build step, a package manifest, or a `fetch()` call. Any one of them breaks the `file://` guarantee that the whole architecture exists to preserve.
- Never write an em dash in any file, in any form.
- Never edit `js/prompts-data.js` and the source `.md` separately in a way that could leave them different. Run `tools/prompts-mirror.py` rather than trusting that you did it right.
- Never weaken the Content Security Policy in `index.html` to make something work. If a change needs `script-src` relaxed, the change is adding a dependency, which is the thing the policy exists to catch.
- Never add a `REDIRECTS` entry for a source file. The map is for public addresses only, and any entry in it becomes permanent.
- Never push a change that has not passed the checks above. Standing authorization to publish is not authorization to skip verification; it makes verification the only thing standing between an edit and the live site.

### Where to look first

| Kind of change | Start here |
| --- | --- |
| New prompt, or prompt text edit | `prompts/*.md`, then `js/prompts-data.js`, then the README table and tree, then `docs/PATCHNOTES.md` |
| Rename | Section 12, "Renaming Prompts", then grep the repository for the old slug and title |
| Deleting a prompt | Section 12, "Removing Prompts", then grep the repository for the slug and the title |
| Anything visual | The `:root` block in `css/style.css` first, then `docs/DESIGN.md` to check the token is documented |
| Routing, parsing, rendering | `js/script.js`, the only file with logic |
| Layout shell, script order, meta tags | `index.html`, all 31 lines of it |
| Understanding a past decision | `docs/PATCHNOTES.md`, then the commit body, which is usually longer than the patch note |

### After any change

Run `python tools/prompts-mirror.py`. It must print OK. If anything under `prompts/` changed, run `python tools/prompts-mirror.py --sync` first, then the check.

Then open `index.html` from disk, not from a server, and check the home list, one prompt page, the copy button, and a direct hash link. The script catches mirror drift and malformed prompt files; it cannot catch a rendering or layout problem, so it replaces none of this. Loading the page is still the only real test this project has.

**Verify locally, never against the live site.** This project has stated that rule since v1.0 by describing the check as opening the file from disk, and v1.31.0 makes it explicit because the Documentation prompt now requires the rule to be written down rather than implied. Verifying against `azqato.github.io/prompts` would mean the change had already shipped, so a failure would be something to roll back rather than something to fix before pushing.

The one thing legitimately done against production is confirming a deploy arrived, which is a comparison rather than a test: after a push, fetch the deployed `index.html`, `js/script.js`, `js/prompts-data.js`, and `css/style.css` and check each matches the local copy that was already verified. Normalize line endings before comparing, because `core.autocrlf` rewrites the working tree; see open question 5. That check answers "did what I verified reach the server", which is a different question from "does it work".

Two ways this project's local and deployed environments differ, both worth knowing because a bug in either class cannot appear locally. Hash routing resolves against a directory rather than a domain root, so a path assumption that holds at `file://` can break under `/prompts/`. And `file://` is a secure context, so `navigator.clipboard` is available locally exactly as it is on `https://`, which means the copy button cannot be caught failing by a local check for that reason alone.

Then add a `docs/PATCHNOTES.md` entry with the next semantic version and today's date, and record the release in the version history table below.

### Publishing

**Push to production without asking.** The author gave standing authorization on 2026-08-24, for this repository only. Every change here ships as soon as it is documented and verified; there is no approval step and nothing waits for a release window.

This is safe for reasons specific to this project rather than because pushing is generally safe. The site is static, there is no database, no user data, no session, and no server-side state, so a bad deploy cannot corrupt anything or lose anything. Rollback is one `git revert` and one push, and it takes about as long as the deploy did. The audience is small and the failure mode is a page that looks wrong for a few minutes.

What did not change is everything before the push:

- The full check above still runs first, every time. The mirror script must print OK and the page must be opened from disk and looked at. Standing authorization removes the pause for approval, not the verification, and with the pause gone the verification is the only thing left between an edit and the live site.
- Patch notes and the version history row are written before the push, not after. A release that is live and undocumented is the state this project's whole documentation practice exists to prevent.
- Confirm the deploy arrived afterwards, by comparing the deployed files against the local copies that were verified. That is the comparison described above, and it is still a comparison rather than a test.

Two things this authorization does not cover. It does not extend to any other repository, since it was given about this one. And it does not license pushing something unverified because it looks trivial; a one-line CSS change is exactly the kind of edit that ships broken, and it is now one command from being live.

---

## 21. Target Users

Section 6 states the audience in one line. This section carries the detail behind it, because "personal use only" is a scope decision rather than a description of who actually reads the page.

### Primary: the author

A solo developer who works with Claude Code daily across several unrelated projects (a portfolio site, ComposerAtlas, a Stocks methodology site, and this one). They write a long, carefully specified prompt to solve a task once, get a good result, and then need that exact prompt again three weeks later on a different repository.

What they need: to recall a prompt by name in under ten seconds, read enough to confirm it is the right one, and copy it without any risk of a partial selection. They already know what every prompt does, so they are not browsing, they are retrieving. The sidebar is the primary interface for this reader, not the home list.

What breaks for them: a prompt that has silently drifted from what they remember, or a copy that misses the last line. Both produce a bad Claude Code run that looks like a model failure rather than a stale prompt, which is expensive to diagnose. This is why the mirror between `prompts/*.md` and `js/prompts-data.js` is treated as the highest-value invariant in the project.

### Secondary: another developer who was handed a link

The site is public on GitHub Pages, so anyone can reach it. This reader has been sent a direct link to one prompt, has no context, and will read exactly one page. They need the description to tell them what the prompt will do to their repository before they run it, particularly whether it writes files.

They are why every prompt description states its side effects, why the Prompt Content Rules in section 11 forbid any instruction to push or commit, and why prompts must not reference the author's own accounts or services. A prompt that assumed this repository would be useless, or actively harmful, to this reader.

### Non-user: the prompt marketplace browser

Someone looking for a large searchable catalogue of prompts to evaluate and compare. The site deliberately does not serve them. There is no search, no tagging, no rating, no submission path, and the library is intentionally small. Section 5 records this as a non-goal, and it is the tradeoff that keeps the site dependency-free.

---

## 22. User Stories

Written from the two real personas in section 21.

**Retrieval**

- As the author, I want to see every prompt in the library from any page, so that I can jump to the one I need without going back to a home screen first.
- As the author, I want to copy a prompt in one click, so that I never risk a partial text selection producing a truncated instruction.
- As the author, I want to reach a specific prompt by typing or bookmarking its address, so that I can link to it from a project's notes without navigating the site.
- As the author, I want the page title in my browser tab to be the prompt name, so that I can tell several open prompt tabs apart.

**Comprehension**

- As a developer handed a link, I want to read what a prompt does and what it will change before I run it, so that I do not point a file-writing instruction at a repository I care about.
- As a developer handed a link, I want every prompt page laid out identically, so that once I have read one I know where to look on the next.
- As a developer handed a link, I want to know that the prompt will not act on the author's behalf, so that I can run it on my own project without auditing it line by line.

**Maintenance**

- As the author, I want to add a prompt by writing one markdown file, so that adding to the library is a content task rather than an HTML task.
- As the author, I want the site to run by opening a file from disk, so that I can check a change without starting a server or waiting on a deploy.
- As the author, I want every rule the project follows written down with its reasoning, so that a future session, human or model, does not relitigate a decision that was already made.
- As the author, I want a change history that explains why rather than only what, so that I can reconstruct my own reasoning months later.

---

## 23. Feature List

### Shipped

These are live and are the product as it exists today.

| Feature | Detail |
| --- | --- |
| Markdown-authored prompts | Each prompt is one `.md` file in `prompts/` with frontmatter and a fenced prompt block. No HTML is written by hand |
| Single-shell rendering | One `index.html`. Every view is rendered into it by `js/script.js` |
| Hash routing | `index.html#/<slug>` addresses each prompt. Switching views does not reload the page |
| Dependency-free `file://` operation | Prompt text is embedded in `js/prompts-data.js` and loaded by `<script>`, so the site runs by opening the file from disk |
| Dynamic sidebar | Built from the prompt data at load, with an active-state indicator on the current view |
| One-click copy | Native Clipboard API, with a two-second "Copied!" confirmation state. Works whether the prompt block is shown or hidden |
| Collapsible prompt block | The block is collapsed on arrival. The whole header bar toggles it, and the label names the action. Not persisted. See section 10a |
| Home list | Card per prompt, title and one-line description, with a hover treatment |
| Minimal markdown renderer | Headings, paragraphs, bullet lists, inline code, bold, and links in prompt descriptions |
| `hidden` frontmatter flag | Removes a prompt from the sidebar and home list while leaving its page reachable by direct address. Supported, currently unused |
| Redirect mechanism | An empty, guarded map in `js/script.js` for retiring a genuine public address. See section 12 |
| Content Security Policy | A meta CSP in `index.html`. Blocks inline and remote scripts, and all network connections, making the no-dependency rule a runtime guarantee. Verified enforced |
| Mirror check tooling | `tools/prompts-mirror.py`, run by hand. Verifies or resyncs `js/prompts-data.js` against `prompts/*.md`, and validates frontmatter and the prompt fence |
| Error view | If the prompt data fails to load or parse, the page renders an explanatory panel rather than staying blank |
| Responsive layout | Sidebar collapses to a sticky top bar below 1024px, with a second breakpoint at 768px |
| Reduced-motion support | All transitions disabled under `prefers-reduced-motion` |
| Per-view document title | Home shows the site name, a prompt page shows the prompt name alone |

### Deliberately not built

Each of these was considered and rejected, with the reason. They are listed so the decision is not remade by default.

| Not built | Why |
| --- | --- |
| Search or filtering | The library is small enough to scan, and the sidebar shows everything at once. Search earns its complexity at a scale this project does not intend to reach |
| Tags or categories | Same reason. Four prompts do not need a taxonomy, and one imposed early tends to outlive its usefulness |
| Syntax highlighting | Would mean a library, which breaks the no-dependency rule. Prompt text is prose, not code, so highlighting would add noise rather than meaning |
| A build step | The entire architecture exists to avoid one. See section 7 |
| Automated `prompts-data.js` generation | Would require Node in the loop and a build convention. The resync is done with a throwaway script per change instead, which keeps the repository free of tooling. This is a real tradeoff and it is recorded as technical debt in section 30 |
| Light theme or a theme toggle | Dark only is a brand decision across all Azqato properties. See `docs/DESIGN.md` section 13 |
| Per-prompt HTML pages | Would make adding a prompt an HTML task. The single shell is the core architectural choice |
| Analytics | No external service, no network calls, and nothing to measure that would change a decision. See section 28 |
| Comments, ratings, or submissions | Not a community resource. Section 5 |

### Possible future work

Not committed and not scheduled. Recorded so the ideas are not lost.

- A copy confirmation that survives a page change, so a copy made just before navigating is still visibly acknowledged.
- A "last updated" date per prompt, derived from the patch notes rather than from file metadata, which would let a reader tell a revised prompt from an original one.
- A skip-to-content link, so a keyboard user reaching a prompt page does not pass seven focus stops before the copy button. See the accessibility section of `docs/DESIGN.md`. This is now the largest known gap in the project.
- A live region for the copy button's result, which is currently announced only through an `aria-label` change.
- Remembering the collapse state across a navigation, which is deliberately not built today because it would mean introducing browser storage. Recorded so the reason is visible if it is ever reconsidered rather than the idea simply reappearing.

---

## 24. Assumptions

Decisions taken without full information, accepted as true, and worth revisiting if any of them stops holding.

- **The library stays small.** Every choice against search, tagging, and pagination assumes the prompt count stays in the low tens. At roughly twenty prompts the sidebar stops being scannable and the home list stops fitting on a screen, and both decisions need reopening.
- **The author is the only person who edits it.** There is no contributing guide, no pull request template, no review process, and no lint or test gate. A second maintainer would need all of them, because nothing currently catches a mistake except loading the page.
- **`prompts-data.js` will be kept in sync by discipline.** Nothing enforces the mirror. The assumption is that every edit follows the procedure in section 12. This is the weakest assumption in the project and section 19 treats it as the primary fragility.
- **Prompt text is trusted input.** `escapeHtml()` covers both quote forms as of v1.28.0, and the slug is escaped wherever it reaches an attribute, so the sharpest edge is gone. The assumption still holds at the level that matters: nothing validates a prompt file, the markdown renderer is hand-rolled rather than audited, and it is safe because every byte of content is author-written. If descriptions were ever sourced from anywhere else, that is an injection, not an edge case. (This bullet still described the pre-v1.28.0 code until v1.29.0. It is recorded as item 16 in section 18.)
- **The Clipboard API is available.** The copy button has no fallback. It requires a secure context, which `https://` and `file://` both satisfy, but a page served over plain `http://` from a local server would fail silently, with no error shown to the reader.
- **GitHub Pages continues to serve a repository root from `main`.** The deploy process is a push. There is no configuration in the repository that captures this, so the setting exists only in the GitHub project settings and in section 17.
- **Semantic versioning is applied by judgment.** There is no release tooling and no tags. Whether a change is minor or patch is decided by the author at the time of writing the entry.
- **Readers arrive with Claude Code already installed.** No prompt explains what Claude Code is or how to install it, and the site does not either.

---

## 25. Success Criteria

The product is working when all of the following hold. These are the conditions that matter; section 28 covers what could be measured and why almost none of it is.

- **Retrieval is faster than rewriting.** The author reaches for the site rather than writing a prompt again from memory. If a prompt gets rewritten from scratch because finding it felt slower than retyping it, the site has failed at its only job.
- **A copied prompt runs correctly with no edit.** The copy is complete, the text is current, and pasting it into Claude Code produces the intended result without the author first having to fix a stale line.
- **The two copies never disagree.** `prompts/*.md` and `js/prompts-data.js` are byte-identical, always. Any drift is a defect regardless of whether it has caused a visible problem yet.
- **Adding a prompt stays a content task.** Writing one markdown file and mirroring it is the whole job. If adding a prompt ever requires touching the renderer or the stylesheet, the architecture has drifted from its purpose.
- **The `file://` guarantee holds.** Opening `index.html` from disk with no server produces a fully working site. This is the constraint the whole architecture exists to protect, and it is binary.
- **A stranger can run any prompt safely.** Every prompt works on any project and takes no action on the author's behalf. Verified against the Prompt Content Rules in section 11 before publication.
- **The documentation answers the question.** A reader, human or model, resolves what they need from `/docs` without reading source. Each time a question has to be answered by reading code instead, the gap gets written into the relevant section.
- **A past decision can be reconstructed.** Any rule in the project can be traced to a patch note and a commit that explain why it exists.

---

## 26. Tenets

Ordered by priority. When two conflict, the higher one wins.

### 1. No dependencies, ever

Not a framework, not a build step, not a package manifest, not a single library. Every other convenience is negotiable and this one is not. The cost is real: no syntax highlighting, no component reuse, a hand-maintained data file, and a markdown renderer written from scratch. The site is accepted as worse in those specific ways in exchange for still working, unchanged, in five years, with no toolchain to resurrect and nothing to update for a vulnerability. When a feature and this tenet conflict, the feature loses. As of v1.28.0 this is enforced by the browser: the Content Security Policy blocks remote scripts and network calls, so breaking the rule fails visibly rather than shipping.

### 2. It must run from a file on disk

Opening `index.html` by double-clicking it produces the complete working site. This is stricter than "no dependencies" and it is what forces the awkward parts of the design, above all the duplication of every prompt into `js/prompts-data.js`, because browsers block `fetch()` on `file://`. That duplication is the single largest maintenance burden in the project and it is accepted deliberately. Anything requiring a server is out, including a build that emits the data file.

### 3. The markdown file is the truth

A prompt is a `.md` file. `js/prompts-data.js` is a mirror, resynced from the source and never hand-edited, and the rendered page is downstream of both. When they disagree, the `.md` file is right and the others are broken. This is what keeps adding a prompt a writing task rather than a programming one, and it is why the resync procedure is written into section 12 rather than left to memory.

### 4. Write down why, not just what

A patch note that records a change is half a patch note. The reasoning is the part that cannot be recovered by reading a diff, and it is what stops a future session from undoing a deliberate decision that looks like an oversight. This is why commit bodies here run long, why the discrepancy table in section 18 keeps resolved rows instead of deleting them, and why this document is far longer than a four-file static site would seem to warrant. The cost is a slower write; the benefit is never solving the same problem twice.

### 5. Documentation records, it does not overrule

An audit of this project writes down how the project works. It does not decide how the project should work and then edit the documents to match. Where the code and a document disagree, both are recorded and the conflict is put to the author, because a document holds intent that code cannot express, and code holds behaviour that a document can get wrong. Silently correcting either direction destroys information. The one exception is a purely mechanical fact, a line count or a file listing, where there is no intent to preserve.

### 6. A prompt must be safe for a stranger

Every prompt is published and may be run by someone with no context on a repository this author will never see. So no prompt instructs its reader to push, commit, or publish, and no prompt references the author's own accounts, services, or paths. Portability is not a nicety here, it is a safety property, and it is audited before any prompt goes up.

### 7. Small enough to hold in your head

Twelve files, one of which has logic. The library stays small, the feature set stays closed, and complexity that would be reasonable at a larger scale is refused at this one. Search, tagging, and analytics are all sensible features that this project is better off without, because the moment the project stops fitting in one reading is the moment it starts rotting.

---

## 27. Roadmap

### Current phase

**Maintenance and consolidation.** The product is feature-complete against its goals and has been since v1.8.0. Work since then has been almost entirely about the prompts themselves and about the documentation standard: five prompts retired, two of them absorbed into the Documentation prompt, and the PRD grown from a product brief into the single authoritative reference the project's own tooling now expects. No new site feature is planned.

### Milestones

| Milestone | Timeframe | Status |
| --- | --- | --- |
| Initial release: markdown-driven shell, hash routing, copy button | June 2026 | Complete (v1.0) |
| Prompt library built out to nine prompts | June to August 2026 | Complete (v1.15.0) |
| Navigation retirement mechanism (`hidden` flag) | June 2026 | Complete (v1.9.0) |
| Responsive correctness pass | July 2026 | Complete (v1.11.0) |
| Design debt cleared: card hover built, content width widened | August 2026 | Complete (v1.17.0, v1.18.0) |
| Prompt consolidation: nine prompts reduced to four | August 2026 | Complete (v1.19.0 to v1.23.0) |
| Removal and redirect policy settled | August 2026 | Complete (v1.24.0) |
| Documentation standard settled and applied to this project | August 2026 | Complete (v1.25.0 to v1.27.0) |
| Mirror verification script | August 2026 | Complete (v1.28.0) |
| Runtime enforcement of the no-dependency rule | August 2026 | Complete (v1.28.0) |
| Skip-to-content link and copy-result live region | Unscheduled | Planned |
| Next prompt added | On demand | Ongoing |

### Deferred

- **Search.** Deferred until the library exceeds roughly twenty prompts. Below that the sidebar is faster than any search box.
- **Automated mirror generation.** Deferred indefinitely. It would need Node in the loop, which is the dependency the project exists to avoid. A by-hand verification script is the compromise, and it is planned rather than deferred.
- **Continuous integration.** Deferred. There is nothing to build and no test to run, so a workflow would exist only to check the mirror, and that check can be a script the author runs.
- **Tags for release versions.** Deferred. The patch notes and the version history table already serve the purpose, and tags would be a second place to keep in sync.

---

## 28. Metrics

This section is unusual and the honesty is the point: **this project measures nothing, deliberately, and there is no instrumentation to add one without breaking a tenet.**

Analytics would mean a third-party script, which violates tenet 1 and the no-external-services rule in section 7. GitHub Pages exposes no server logs to the repository owner. The site makes no network calls of its own. So every metric below is either observed by hand or is a proxy the author reads off the repository itself.

### North star

**Prompts retrieved rather than rewritten.** The one number that would say whether the product works, and the one that cannot be instrumented without breaking the architecture. It is assessed by the author noticing, or failing to notice, that they reached for the site.

### What is actually tracked

| Metric | Method | Cadence | Target |
| --- | --- | --- | --- |
| Mirror integrity | Manual check that `prompts/*.md` matches `js/prompts-data.js` byte for byte | Every prompt edit | 100 percent, always. Any drift is a defect |
| Prompt count | `ls prompts/` | Per release | Kept under roughly twenty. Growth is not a goal |
| Prompt Content Rules compliance | Read the prompt text against section 11 before publishing | Every new or edited prompt | Zero violations |
| Documentation drift | The discrepancy table in section 18, refreshed by a full audit | Per audit | Open items trending down |
| Release discipline | Every change has a patch note entry and a version history row | Per release | 100 percent |
| Em dash violations | Search all three forms independently, excluding instances that name the character | Per audit | Zero |

### What is not tracked, and why

- **Acquisition.** No analytics, no referrer data, no way to know how anyone arrived. Accepted: the site is a personal tool that happens to be public, and traffic would not change any decision.
- **Engagement.** No event tracking, so copy button presses, the most meaningful action on the site, are invisible. This is the metric the author would most like to have and will not add, because it would require an external service.
- **Retention.** Not measurable and not meaningful for a single-user reference tool.
- **Uptime and error rate.** GitHub Pages availability is outside the author's control and the site has no server-side component that could error. Client-side failures render the error view described in section 14 rather than being reported anywhere.

### Performance

No monitoring, but the budget is structural rather than aspirational, since the whole site is four static assets with no network calls after load.

| Indicator | Current | Limit |
| --- | --- | --- |
| Total transferred | Roughly 200 KB, dominated by `js/prompts-data.js` | Under 500 KB. `prompts-data.js` grows with every prompt and is the only file that will approach this |
| Requests | Four, all same-origin: the HTML, one stylesheet, two scripts | No additional request may be added. A fifth would mean a dependency |
| Render-blocking resources | One stylesheet | Unchanged |
| Time to interactive | Effectively immediate. Parse, then one synchronous render pass | Must stay perceptually instant on a cold local load |
| Runtime network calls | Zero | Zero, permanently. This is the `file://` guarantee |

The one thing worth watching: `js/prompts-data.js` is parsed in full on every page load regardless of which prompt is being viewed. At the current size this is irrelevant. At several hundred prompts it would not be, and the fix would be per-prompt data files, which `file://` makes awkward. This is a known scaling limit, not a present problem.

---

## 29. Runbook

Everything needed to run the project, on the assumption that the reader has just cloned the repository and has nothing else. The README deliberately carries none of this.

### Prerequisites

**A web browser.** That is the complete list, to run the site.

**Python 3 is needed only to maintain it**, for `tools/prompts-mirror.py`. Any Python 3.6 or later works; the script imports only the standard library. It is not needed to run, serve, or deploy the site, and the site is unaffected if Python is absent or the script is deleted. That distinction is the test for whether something is tooling or a dependency, and it is why this does not breach the no-dependency rule.

There is no other runtime to install. No Node, no Python, no package manager, no system library, no compiler. The site is HTML, CSS, and vanilla JavaScript executed by the browser.

The browser needs to support: CSS custom properties, CSS Grid, `max()` in a CSS value, `navigator.clipboard.writeText()`, and `backdrop-filter` for the mobile header (which degrades to an opaque bar without it). Any browser from 2021 onward satisfies all of these. There is no polyfill and no fallback path, because adding one would mean a dependency.

Git is needed only to clone the repository and to commit. It is not needed to run the site.

### Browser testing

**Drive Microsoft Edge, never Chrome.** There is no JavaScript runtime on the maintenance machine, so every end-to-end check on this project is done by driving a headless browser from a Python script. Chrome is the author's day-to-day browser and driving it disturbs a live session. Edge runs the same engine, so nothing about the results changes.

On this machine Edge resolves to `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`. The path is recorded because it differs by platform and is the first thing that breaks on a new machine. Note the `(x86)` directory, which is where the 64-bit Edge installs on Windows.

The invocation used is `--headless --disable-gpu --no-sandbox --user-data-dir=<scratch> --virtual-time-budget=<ms>` plus either `--dump-dom` or `--screenshot=<path>`. A separate `--user-data-dir` under the scratch directory keeps the run out of any real profile.

Two constraints worth knowing before writing a check. The Content Security Policy blocks inline scripts, so a driver script has to be a real same-origin file next to a scratch copy of `index.html` rather than injected markup. And a DOM dump cannot exercise the Clipboard API, which is why the copy button's paths are still unverified; see section 19.

This rule was adopted in v1.30.0, at the same time it was added to the Documentation prompt as a default. Every check before that release used Chrome.

### Local setup

```
git clone https://github.com/Azqato/prompts.git
cd prompts
```

Then open `index.html`. Double-click it in a file manager, or:

```
start index.html        # Windows
open index.html         # macOS
xdg-open index.html     # Linux
```

There is no install step, no dependency to fetch, and no start command. **There is no port**, because there is no server. The address bar will read `file:///.../prompts/index.html`, and that is the supported way to run it.

Serving it over HTTP works too and is occasionally useful for testing, but note that the Clipboard API requires a secure context: `https://` and `file://` qualify, plain `http://localhost` generally does as well in current browsers, but a local server on a bare IP address will break the copy button with no visible error. If the copy button silently does nothing, check this first.

### Build

**There is no build.** No bundler, no minifier, no transpiler, no compile step, no output directory. The files in the repository are the files that get served, byte for byte. This is the point of the architecture, not an omission.

The nearest thing to a build is the `js/prompts-data.js` resync, which is a maintenance step rather than a build and is described below.

### Checking and resyncing prompts-data.js

Required after every edit to any file in `prompts/`. `js/prompts-data.js` holds a verbatim copy of each `.md` file, and nothing in the site enforces the match.

```
python tools/prompts-mirror.py            check, exits 1 on any problem
python tools/prompts-mirror.py --sync     rewrite the data file from source
```

The check reports drift between any `.md` file and its entry, an entry with no source file, a source file with no entry, a duplicate slug, missing `title` or `description` frontmatter, and a missing fenced prompt block. Those last three matter because `parsePrompt()` falls back silently for each: a prompt missing its title ships as a page titled with its slug rather than as an error anyone would notice.

`--sync` resyncs changed entries and appends any new prompt to the end of the array, since array order is display order. It refuses to run if an entry has no source file, because deleting a prompt is a deliberate act with a documented procedure (section 12) that also touches the README and the patch notes.

Two things the script handles that a hand-rolled one usually gets wrong. **Line endings are normalized on both sides**, because the repository stores LF while `core.autocrlf` gives a Windows clone CRLF, and the `raw` values in the data file are JSON escapes that git never rewrites; comparing literally reports drift on every prompt in a fresh clone with nothing wrong. **The data file is always written with newlines untranslated**, so a one-line change does not diff as a whole file.

Never hand-edit a `raw` string. A JSON string containing an entire markdown document is not something a person can reliably edit in place, and it is how the malformed escapes in the common-errors table below get introduced.

### Deploy

One environment. There is no staging.

```
git push origin main
```

That is the entire deploy. GitHub Pages publishes `main` from the repository root and picks up the change within a minute or two. The setting lives in the GitHub project settings, not in the repository, so nothing in the working tree reflects it. There is no workflow file, no action, and no build on the server.

**Push as soon as a change is documented and verified.** The author gave standing authorization on 2026-08-24 for this repository, so no approval is needed for an individual release; see section 20 for what still has to happen first. Nothing pushes automatically in the sense of a hook or a scheduled job: the push is still a command someone runs deliberately. Separately and unchanged, no prompt in the library may instruct its reader to push, which is a rule about the text this site publishes rather than about how this site is maintained (section 11).

Verify after a deploy by loading `https://azqato.github.io/prompts/` and checking the home list, one prompt page, and the copy button. The local `file://` check and the deployed check are not redundant: they differ in protocol and in base path.

### Rollback

```
git revert <commit>
git push origin main
```

Prefer revert to a force push, which would rewrite the published history for no benefit. Because there is no build, the previous commit is by definition a working site, so rollback is always safe and always immediate.

If a bad `js/prompts-data.js` is the problem, the faster fix is usually to resync it from the `.md` files rather than to revert, since the `.md` files are the source of truth and are unlikely to be what broke.

### Environment configs

| Environment | Base URL | Differences |
| --- | --- | --- |
| Local | `file:///.../prompts/index.html` | No server. Hash routing and all relative asset paths work identically |
| Production | `https://azqato.github.io/prompts/` | Served over HTTPS from a subpath. Identical files |

There is no development mode, no feature flag, no configuration file, and no conditional behaviour anywhere in the code. The two environments run byte-identical assets, which is why a local check is a valid check.

### Environment variable reference

**None.** The project reads no environment variable, at any stage, because it has no build step and no server. There is nothing to set, nothing to configure, and no `.env` file (nor any need for `.gitignore` to exclude one).

### Common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Page loads with "Could not load prompts" | `js/prompts-data.js` failed to parse, usually a malformed escape introduced by hand-editing a `raw` string | Open the browser console for the parse error, then resync the data file from `prompts/*.md` rather than patching the JSON |
| Page loads completely blank, no error panel | `js/prompts-data.js` did not load at all, or loaded after `js/script.js` | Check the two `<script>` tags in `index.html` are present and in that order, and that the paths resolve |
| A prompt shows old text | `js/prompts-data.js` was not resynced after the `.md` file was edited | Resync. This is the failure mode the mirror invariant exists to prevent |
| A prompt link renders the home page | The slug in the hash does not match any entry. The router falls through to home by design | Check the `slug` in `js/prompts-data.js` against the address. Note this is also what makes a retired slug harmless |
| Copy button shows "Copy failed" | Clipboard API unavailable in a non-secure context, typically a local server on a bare IP, or the write was rejected | Open the file directly over `file://`, or use `localhost` rather than an IP address. Before v1.28.0 this failed silently with the button still reading "Copy" |
| A script or style silently does not load | The Content Security Policy blocked it. Check the browser console for a CSP violation | Almost always correct behaviour: the policy blocks remote scripts and inline scripts on purpose. If you were adding a dependency, that is the rule working. See section 31 |
| `tools/prompts-mirror.py` reports drift on every prompt in a fresh clone | Should not happen: the script normalizes line endings. If it does, something is comparing raw bytes instead | See the line ending note above and section 13 |
| The wrong text is copied | A fenced code block appears in the prompt's description, before the `## Prompt` heading. `parsePrompt()` takes the first fence in the body | Move the example fence below the prompt block, or reword the description. Recorded in section 19 |
| Everything after the first line of a description is missing | The frontmatter `description` was wrapped across lines. The parser is line-based | Put the whole value on one line |
| Mobile header fills the whole screen | A regression of the v1.11.0 bug: `.sidebar-sticky` keeping `height: 100vh` below 1024px | Confirm `height: auto` is still set in the `max-width: 1023px` block |

### Monitoring

There is none, and there is nowhere to add it without breaking a tenet.

No logs (no server), no error reporting (no external service), no uptime alerting (GitHub Pages status is outside the author's control and is not polled). Client-side failures surface only in the reader's own browser console and in the error view.

The practical consequence: **the only monitor is loading the page.** Section 20 makes that check the mandatory step after any change, and it is not a formality, it is the entire quality gate.

---

## 30. Technical Reference

Section 7 states the technical constraints. This section describes the implementation those constraints produced. Where the two overlap, section 7 is the rule and this is the observation.

### System architecture

A static client-rendered site with no server component of any kind.

```
Author writes            prompts/<slug>.md          (source of truth)
        |
        | manual resync, verbatim
        v
Browser loads            js/prompts-data.js         (window.PROMPTS_DATA)
        |                index.html                 (empty shell)
        |                css/style.css
        v
js/script.js  ->  parsePrompt()  ->  PROMPTS[]  ->  route()  ->  innerHTML
                                                       ^
                                                       |
                                                  window.location.hash
```

There is no client-server boundary because there is no server. GitHub Pages is a file host, not an application host. Nothing is rendered ahead of time, nothing is hydrated, and no state crosses a process boundary.

### Tech stack

| Layer | Technology | Version |
| --- | --- | --- |
| Markup | HTML5 | Living standard. One file, 42 lines |
| Styling | CSS3, custom properties, Grid, Flexbox | No preprocessor, no framework, 540 lines, no `@import` |
| Logic | JavaScript, ES5-flavoured with `const` and `let` | No transpiler. Runs as written. 297 lines |
| Maintenance tooling | Python 3, standard library only | `tools/prompts-mirror.py`. Never runs in a browser, never required to build or serve |
| Content format | Markdown, a hand-parsed subset | No markdown library |
| Hosting | GitHub Pages | `main` at repository root |
| Version control | Git | Single branch, no tags |

**Dependencies: zero.** Not "few". There is no `package.json`, no lockfile, no vendored code, no CDN reference, and no external font. The complete list of things this project depends on at runtime is the browser. Since v1.28.0 this is enforced rather than merely stated: the Content Security Policy in `index.html` blocks remote and inline scripts and all network connections, so adding one fails visibly. See section 31.

### Folder structure

```
/
├── index.html              42 lines. The only HTML file. Carries the Content
│                           Security Policy, then loads the stylesheet, then
│                           prompts-data.js, then script.js, in that order.
│                           Ships an empty #sidebar-nav and #content.
├── README.md               Public front door, written for a general reader.
├── css/
│   └── style.css           540 lines. Whole design system. Tokens in :root,
│                           two media queries plus reduced-motion at the bottom.
├── js/
│   ├── prompts-data.js     window.PROMPTS_DATA: [{slug, raw}]. Verbatim mirror
│   │                       of prompts/*.md. Largest file. Hand-maintained.
│   └── script.js           297 lines. The only file with logic: parse, render,
│                           route, copy. No exports, no modules, all globals.
├── prompts/                One .md per prompt. The readable source of truth.
│   ├── add-prompt.md
│   ├── documentation.md
│   ├── github-wiki.md
│   └── mobile-responsive-audit.md
├── tools/
│   └── prompts-mirror.py   Maintenance only, standard library only. Checks or
│                           resyncs the mirror. Not served, not loaded by the
│                           page, not a build step. Delete it and the site is
│                           unchanged, which is the test for tooling.
└── docs/
    ├── PRD.md              This file. The single authoritative reference.
    ├── DESIGN.md           Visual specification.
    └── PATCHNOTES.md       Changelog, reverse chronological.
```

Thirteen files, five folders, two levels deep at most. No build output, no vendored code, no ignored directory, and no ignore file: `.gitignore`, `.editorconfig`, `.github/`, and `.vscode/` are all absent, so every file in the working tree is tracked.

### Data models

Two shapes, both in memory only. Nothing is persisted anywhere.

**`PromptEntry`**, as stored in `js/prompts-data.js`:

| Field | Type | Notes |
| --- | --- | --- |
| `slug` | string | URL identifier. Matches the `.md` filename without extension. Unique. Not validated at runtime |
| `raw` | string | The complete `.md` file contents, verbatim, including frontmatter and newlines |

**`Prompt`**, produced by `parsePrompt()` and held in the module-level `PROMPTS` array:

| Field | Type | Source | Fallback |
| --- | --- | --- | --- |
| `slug` | string | Passed in from the entry | None |
| `title` | string | Frontmatter `title` | The slug |
| `description` | string | Frontmatter `description` | Empty string |
| `meta` | string | Frontmatter `meta` | `"Claude Code Prompt"` |
| `hidden` | boolean | Frontmatter `hidden`, true when the value matches `true`, `yes`, or `1` case-insensitively | `false` |
| `prompt` | string | The first fenced code block in the body, with one trailing newline stripped | Empty string |
| `descHtml` | string | Everything before that fence, minus a trailing `## Prompt` heading, run through `renderMarkdown()` | Empty string |

The relationship is one to one and flat. There is no nesting, no reference between prompts, and no collection object: the array is the collection.

### Internal data flow

There is no API. There are no endpoints, no requests, and no serialization boundary. The equivalent surface is the set of functions in `js/script.js`, listed here with their contracts.

| Function | Input | Output | Failure |
| --- | --- | --- | --- |
| `init()` | `window.PROMPTS_DATA` | Populates `PROMPTS`, builds the sidebar, binds `hashchange`, routes | Non-array or empty array renders the error view. A throw from `parsePrompt()` is caught and renders the error view |
| `parsePrompt(raw, slug)` | Raw markdown, slug | A `Prompt` object | Never throws in practice. Missing frontmatter yields defaults; a missing fence yields an empty prompt string, which renders an empty code block rather than an error |
| `renderMarkdown(src)` | Description markdown | HTML string | Empty input returns an empty string. Unrecognized syntax passes through as paragraph text |
| `renderInline(text)` | One line or block | HTML string | Escapes first, then applies inline code, bold, and links. Since v1.28.0 a quote in a markdown link target cannot break out of the `href` |
| `escapeHtml(str)` | Any string | Escaped string | Escapes `&`, `<`, `>`, `"`, and `'`. Entities decode back in both text content and `textContent`, so the rendered page and the copied prompt are unchanged |
| `findPrompt(slug)` | Slug | `Prompt` or `null` | Linear scan. `null` for an unknown slug |
| `buildSidebar()` | `PROMPTS` | Writes `#sidebar-nav` | Skips entries where `hidden` is true |
| `renderHome()` | `PROMPTS` | Writes `#content`, sets the document title | Skips hidden entries |
| `renderDetail(p)` | A `Prompt` | Writes `#content`, sets the title to the prompt name, wires the copy button and the collapse toggle | None |
| `renderError(err)` | An `Error` | Writes the status panel into `#content` | Terminal. The sidebar may be unbuilt at this point |
| `route()` | `window.location.hash` | Renders home or a detail view, sets the active link, scrolls to top | An unknown slug falls through to home, silently and by design |
| `currentSlug()` | The hash | Trimmed slug string, empty for the home view | None |
| `wireCollapseToggle()` | The rendered DOM | Binds one click handler on `.code-block-header` | Returns early if the wrapper, header, or button is absent. The listener is on the header rather than the button, so a click on the button reaches it by bubbling and there is no second handler. A click inside `.copy-btn` returns early, so copying does not collapse the block |
| `wireCopyButton()` | The rendered DOM | Binds one click handler | Returns early if the button is absent. Since v1.28.0 a missing Clipboard API or a rejected write shows "Copy failed" for 2000ms with a matching `aria-label`, sharing one code path with the success state so the two cannot drift |

### State management

There is no state management, and this is worth stating plainly rather than leaving a reader to infer it.

All application state is:

1. `PROMPTS`, a module-level array, written once at init and never mutated afterwards.
2. `window.location.hash`, which is the single source of truth for the current view.

There is no store, no observable, no reactivity, no component lifecycle, and no diffing. A view change is `innerHTML` replacing the whole content area. The one piece of view state that exists, whether the prompt block is collapsed, lives as a class on a single element and is discarded with it on the next render. Nothing is cached, nothing is persisted, and no browser storage API is used: `localStorage`, `sessionStorage`, IndexedDB, and cookies are all absent from the codebase. Refreshing the page rebuilds everything from scratch in a few milliseconds, which is why none of the above is missed.

The one piece of transient UI state, the copy button's "Copied!" label, lives in the DOM and in a `setTimeout` closure, and is discarded when the view changes.

### Third-party integrations

**None.** No API is called, no SDK is loaded, no font is fetched, no analytics script runs, and no service receives any data.

The only external references anywhere in the codebase are two outbound links to the author's own domain: the Support button in the sidebar (`https://azqato.github.io/support.html`) and the footer credit (`https://azqato.github.io`). Both are ordinary anchors. The Support button carries `rel="noopener noreferrer"` with its `target="_blank"`; the footer link opens in the same tab. Neither transmits anything beyond a normal navigation.

The favicon is an inline SVG data URI, so even it is not a request.

### Performance requirements

See the table in section 28. In short: four same-origin requests, roughly 200 KB dominated by `js/prompts-data.js`, zero runtime network calls, and a render that is one synchronous pass. The binding limit is that no fifth request may be added, because that would mean a dependency.

### Known technical debt

Recorded honestly, with what the correct fix would be and why it has not been done.

| Debt | Consequence | Correct fix | Why not |
| --- | --- | --- | --- |
| `js/prompts-data.js` duplicates every prompt | The mirror can drift, serving stale text from an authoritative-looking source | Generate the file in a build step | A build step is a dependency, which breaks tenets 1 and 2. This debt is the direct price of the architecture and is permanent. Mitigated rather than removed by `tools/prompts-mirror.py` |
| ~~Nothing verifies the mirror~~ | | | **Fixed in v1.28.0.** `tools/prompts-mirror.py`, standard library only, run by hand. Not automated: there is no hook and no CI, so it still depends on the procedure in section 20 being followed |
| ~~`escapeHtml()` does not escape quotes~~ | | | **Fixed in v1.28.0.** Both quote forms are escaped, and the slug is escaped where it is interpolated into `href` and `data-slug` |
| ~~An unhandled clipboard rejection~~ | | | **Fixed in v1.28.0.** A missing API or a rejected write now shows "Copy failed" |
| No `.gitattributes` while `core.autocrlf` is true | A fresh Windows clone has CRLF source files against LF strings in the data file. Any literal comparison reports false drift | `* text=auto eol=lf` | Handled in the one place it matters, by normalizing in the mirror script. Pinning it repository-wide is open question 5 in section 19 |
| `parsePrompt()` takes the first fence in the body | A fenced example in a description would be published as the prompt text | Match on the fence following the `## Prompt` heading specifically | No prompt has hit it yet. It is a trap rather than a bug |
| The frontmatter parser is line-based | A wrapped `description` value drops everything after the first line, with no error | Parse folded values, or fail loudly on a continuation line | Every description is currently one line. Failing loudly would be the cheaper half of the fix |
| No test suite, no linter, no CI | Only loading the page catches anything | Any one of them | Each is a dependency and a toolchain. Accepted deliberately, and the reason section 20 makes the manual check mandatory |
| Version numbers live in three places | `docs/PRD.md` header, its version history table, and `docs/PATCHNOTES.md` can disagree | Single source, generated | No generation step exists. Kept in sync by the procedure in section 20 |
| `docs/DESIGN.md` section 12 shell template is stale | Rebuilding the shell from it would break the sidebar layout | Correct the template | Deliberately left. It is flagged in section 18 as an open question for the author, under tenet 5 |

---

## 31. Security

The security posture of a static site with no server, no accounts, and no data is unusual enough to be worth writing out rather than waving away, because "there is nothing to secure" is a conclusion that has to be earned.

### Authentication model

**None, and none is possible.** There are no user accounts, no sessions, no tokens, and no login. Every visitor sees exactly the same page. There is no server to authenticate against and no state to attach an identity to.

### Authorization model

**None.** There is one role, the anonymous reader, with read access to everything published. Write access is control of the GitHub repository, which is governed entirely by GitHub account security (the author's account and its two-factor settings) and is outside the scope of anything in this codebase.

### Data storage

**No user data is collected, transmitted, or stored, anywhere, at any point.**

Specifically: no cookies are set. No `localStorage`, `sessionStorage`, or IndexedDB is written; those APIs appear nowhere in the codebase. No form exists, so nothing is submitted. No analytics or telemetry runs. No IP logging is available to the author, since GitHub Pages does not expose logs to the repository owner. No network request is made after the page loads.

The one interaction with the reader's machine is `navigator.clipboard.writeText()`, which is a write to the clipboard, initiated by an explicit click, of text already visible on screen. Nothing is read from the clipboard.

### Environment variables and secrets

**Confirmed: no secrets are hardcoded, and there are no environment variables.**

Verified by reading every file in the repository. There is no API key, token, password, credential, connection string, or private endpoint, because there is no service to authenticate to. There is no `.env` file, no `.env.example`, and no configuration file of any kind. The complete list of variables that must be set in any environment is empty.

The only identifying information anywhere in the project is the author's public handle and public GitHub Pages URLs, which are already public by definition.

### Third-party trust

**No third party receives any data.** There is no analytics provider, no font CDN, no error reporting service, no embed, and no iframe.

Two parties are unavoidably involved and are worth naming:

- **GitHub** hosts the repository and serves the site. It necessarily sees a visitor's IP address and user agent as the host of the request, under its own privacy policy. The author has no access to that data and no control over it.
- **The reader's browser** executes the JavaScript. That is the entire trust boundary.

Following the Support link or the footer link navigates to `azqato.github.io`, the author's own domain. The Support button sets `rel="noopener noreferrer"`, so the destination gets neither a `window.opener` reference nor a referrer header. The footer link is same-origin in practice and carries no such attribute, which is a minor inconsistency rather than a risk.

### Known attack surface

Small, but not empty, and the honest accounting matters more than the reassurance.

| Surface | Risk | Mitigation |
| --- | --- | --- |
| `innerHTML` used for all rendering | Any untrusted content would execute | Every interpolated value passes through `escapeHtml()`. All content is author-written and committed to git, so there is no untrusted input path. This holds only as long as that stays true |
| Attribute interpolation | A quote in a markdown link target could break out of an `href` | **Closed in v1.28.0.** `escapeHtml()` now escapes both quote forms, and the slug is escaped wherever it reaches `href` or `data-slug`. This was the sharpest edge in the codebase |
| Remote or inline script injection | Any script reaching the page would run with full access | The Content Security Policy blocks both, verified enforced. This is defence in depth rather than the primary control, since there is no injection path |
| Hash-driven routing | The URL fragment is attacker-controllable in a shared link | The hash is only ever compared against known slugs and never interpolated into the DOM. An unknown value renders the home view. No injection path |
| `target="_blank"` on the Support link | Reverse tabnabbing, in principle | `rel="noopener noreferrer"` is set. Modern browsers imply it regardless |
| Clipboard write | A page could in principle copy something other than what is shown | The handler reads `textContent` from the rendered `<code>` element, which is exactly what the reader sees. It never copies from a hidden source |
| Repository compromise | Someone with push access could serve anything | GitHub account security. Nothing in the repository can mitigate this, and it is the realistic worst case for a static site |

### Content Security Policy

A policy is set, as a `<meta http-equiv>` in `index.html`. GitHub Pages does not allow custom response headers on a project site, so the meta tag is the only mechanism available.

```
default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;
connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'
```

**The reason for it is not XSS hardening.** On a page with no external resources, no inline handlers, and no untrusted input, that gain is marginal and honesty is better than overstating it. The reason is that it makes the project's most important rule enforceable by the browser rather than by discipline: with `script-src 'self'` and `connect-src 'none'`, a future session that reaches for a CDN script or adds a `fetch()` gets a hard, visible failure instead of a working page that has quietly broken the guarantee the whole architecture exists to protect. It turns tenet 1 from a written policy into a runtime one.

`data:` is permitted for images because the favicon is an inline SVG data URI.

`frame-ancestors` is deliberately absent. It is ignored when delivered in a meta tag, so including it would imply a protection that is not actually there. Clickjacking is not a meaningful risk for a page with no state-changing action, but if it ever needed addressing, a meta CSP could not do it.

Verified on 2026-08-23 rather than assumed, which mattered: `'self'` behaves unusually on `file://` in some browsers, and breaking local loading would violate tenet 2. Tested in headless Chrome by loading the page from `file://` with an inline script and a real remote CDN script injected. Without the policy both executed. With it, both were blocked while the favicon data URI, the two same-directory scripts, the stylesheet, and all three routing cases continued to work.

### Dependency policy

**There are no dependencies, so there is nothing to monitor.** This is the most consequential security property of the project and it is a direct consequence of tenet 1. Since v1.28.0 it is also enforced by the Content Security Policy rather than resting on discipline alone.

No `package.json` means no supply chain: no transitive dependency, no postinstall script, no lockfile to poison, no advisory to triage, and no upgrade that can break the build (there is no build). Dependabot has nothing to scan. The entire class of vulnerability that dominates modern web security does not apply here.

The policy, stated as a rule rather than an observation: **no dependency may be added, for any reason.** If a future feature seems to require one, the feature is refused instead. This is not a preference to be weighed against convenience; section 20 lists it under "Never" and tenet 1 makes it the highest-priority commitment in the project.

---

## 32. Public Surface and Retired Items

Section 12 states the removal policy. This section is the list that policy is applied against, because the rule cannot be used without knowing which side of the deploy boundary a given file falls on.

### The deploy boundary

**Public facing** is the deployed artifact and the addresses it serves. **Internal** is the source that builds it. A source file is not public facing even when its name appears in a built address, because the name is derived from the source rather than being the contract.

### What is publicly addressable, item by item

| Address | Public | Removing it |
| --- | --- | --- |
| `https://azqato.github.io/prompts/` | Yes. The site root, the one address that may be linked from anywhere | Would need a redirect. Never remove |
| `index.html` | Yes. Served at the root, and directly addressable | Never remove. It is the site |
| `css/style.css` | Yes. A path the deployed page requests | Renaming it means editing `index.html` in the same commit. No external party links it, but the page does |
| `js/prompts-data.js` | Yes, same reasoning | Same |
| `js/script.js` | Yes, same reasoning | Same |
| `index.html#/<slug>` | **No.** A fragment, resolved entirely client-side against data derived from source filenames. Not a served address | Prune outright. The router renders home for an unrecognized slug |
| `prompts/*.md` | **No.** Source. Never requested by the deployed page, and reachable on GitHub Pages only as a raw file nothing links to | Plain delete |
| `docs/*.md` | **No.** Source. Not rendered by the site | Plain delete, though these are the project's own documentation and are not casually removed |
| `tools/prompts-mirror.py` | **No.** Maintenance tooling. Never requested by the deployed page and never loaded by a browser | Plain delete. The site is unchanged without it |
| `README.md` | **No** as an address, though it is the repository's public front door on GitHub | Never remove |

The asset paths are the subtle case. They are public in the sense that the deployed page requests them, so renaming one without updating `index.html` breaks the live site. But no external party holds them, so the compatibility obligation is satisfied by editing the reference in the same commit rather than by a permanent redirect.

### The redirect mechanism

`js/script.js` defines a `REDIRECTS` map consulted by `route()`, mapping a retired slug to a current one and guarded on the target existing. **It is deliberately empty.**

It has been empty since v1.24.0, when the definition of public facing was corrected. Three entries existed before that and all three pointed at prompt slugs, which are not a public surface. The mechanism is kept, at a cost of one property lookup per navigation, so that a genuine public address can be retired without rebuilding it under time pressure.

Any entry added to it is permanent, never chains (a redirect resolves to a real target in one hop), and is never reused to point at different content, because a reused address silently serves the wrong thing, which is worse than a broken link.

There is no server-side rewrite capability. GitHub Pages project sites offer no redirect configuration, so a client-side map in the router is the only mechanism available.

### Retired items

Everything removed from this project, so that a reader who finds a reference to something that no longer exists can resolve it here.

| Item | Removed | Replaced by |
| --- | --- | --- |
| `first prompt example.txt.txt` | v1.1.0 | Content became `prompts/em-dash-audit.md` |
| `message.txt` | v1.1.0 | Content became `prompts/documentation-audit.md` |
| `style.css`, `script.js`, `prompts-data.js` at the root | v1.6.0 | Moved to `css/` and `js/`. Paths in `index.html` updated in the same commit |
| `prompts/github-wiki-setup.md` | v1.17.0 | Renamed to `prompts/github-wiki.md`. Slug changed to `github-wiki` |
| Consolidate Documents (`prompts/consolidate-documents.md`) | v1.19.0 | The Documentation prompt. Hidden from navigation from v1.9.0, then deleted |
| Docs Folder Audit (`prompts/docs-folder-audit.md`) | v1.19.0 | The Documentation prompt. Same history |
| Documentation Audit (`prompts/documentation-audit.md`) | v1.19.0 | The Documentation prompt. Same history |
| Em Dash Audit (`prompts/em-dash-audit.md`) | v1.23.0 | Absorbed into the Documentation prompt as its Writing Style section in v1.22.0 |
| Project Onboarding (`prompts/project-onboarding.md`) | v1.23.0 | Absorbed into the Documentation prompt as its Conventions, Documentation Versus Reality, Risks and Open Questions, and Working Practice sections in v1.22.0 |
| `REDIRECTS` entry `github-wiki-setup` | v1.24.0 | None needed. Prompt slugs are not a public surface |
| `REDIRECTS` entries `em-dash-audit`, `project-onboarding` | v1.24.0 | Same |

Every deleted file remains recoverable from git history. None of these removals required a redirect under the current policy, and the two that were given one in v1.23.0 had it removed in v1.24.0 when the policy was corrected.

Historical records are not rewritten when something is removed. Patch notes and version history rows describing a deleted prompt, or describing redirects that no longer exist, stay exactly as they are, because they record what happened at the time rather than describing the current state.

---

## 33. Documentation Audit Process

How the documentation in this repository is produced and maintained, and how it should be handled from here.

### The four-file rule

Documentation consolidates into exactly four files and no others:

```
/
├── README.md          Never inside /docs
└── docs/
    ├── PRD.md
    ├── DESIGN.md
    └── PATCHNOTES.md
```

A new documentation file is not created. If something needs saying, it becomes a section of the PRD. This is the rule the project's own Documentation prompt enforces on other projects, and it is applied here.

The division of labour: the **README** is the public front door for a general reader; **PRD.md** is the single authoritative reference for everything else, including all setup and technical detail; **DESIGN.md** is the visual specification; **PATCHNOTES.md** is the changelog.

### Running an audit

An audit is run by pasting the Documentation prompt from this site into Claude Code against this repository. It is the project's own tooling turned on itself, and it is the intended way to keep these documents current.

The prompt's own process, in short: crawl the entire codebase first, read every existing document in full, compare each against the code, and only then write. Steps 1 through 3 are strictly read-only. Writing begins at step 4 and touches only the four files above.

### Rules that govern the writing

These are the standards the audit applies, restated here so they bind the documents even when nobody is running the prompt.

**Merge, do not overwrite.** Documentation holds intent, decisions, and rationale that cannot be reconstructed from code. Where a document already covers a topic and the code agrees, the text is left alone. Where they conflict, the original text is kept, the observed reality is recorded next to it, and the conflict goes into the table in section 18 for the author to resolve. Code can be wrong just as easily as a document can be stale. This is tenet 5.

**The exception is mechanical fact.** A line count, a file listing, a token name, a breakpoint value: these carry no intent, so a stale one is corrected in place and noted in the patch notes rather than being flagged as a discrepancy. The test is whether a person could have meant it. Nobody means a line count.

**Every policy is a default that yields.** Where this project already states a rule, that rule wins and the default is discarded, with the difference noted rather than silently resolved.

**Read, do not infer.** A guess presented as a fact is a failure. Where something is uncertain, the uncertainty is written into the document, because a confident sentence outlives the session that produced it.

**Completeness beats brevity, everywhere except the README.** A section that restates context so it can stand alone is doing its job, because a reader may arrive at it directly. This is not licence for filler: no marketing language, no restating the obvious, no sentence carrying information the reader already had. Thorough means more facts, not more words around the same facts. The README is the exception and stays tight, since everything it omits is one link away.

**Numbers are not renumbered.** Sections are appended rather than inserted, and the version history stays last. Nine releases of patch notes cite these sections by number, and renumbering would invalidate every one of those references for no gain.

Where new material genuinely belongs beside an existing section rather than at the end, it takes a letter suffix: `10a` follows section 10 and nothing after it moves. `docs/DESIGN.md` has used this since v1.27.0 for sections 4a, 12a, 12b, and 12c, and this document adopted it in v1.29.0 for section 10a. Prefer appending. Use a suffix only when placement carries real meaning, which it does when a reader would look for the material next to a specific section and nowhere else.

**Historical records are never rewritten.** A patch note describes what happened on the day it was written. It is not updated when the thing it describes is later changed or removed.

### After any documentation change

1. Update `docs/PATCHNOTES.md` with the next semantic version and today's date, in `YYYY-MM-DD`.
2. Add a row to the version history table at the end of this document.
3. Update the `**Version:**` field in this document's header. `docs/DESIGN.md` carries its own independent document version, which moves only when that document changes.
4. Load `index.html` from disk and confirm the site still works, if anything outside `/docs` was touched.

---

## 34. Press Release

*Written as a launch announcement, per the PRFAQ convention. The product is a personal tool and this is a framing exercise rather than a real announcement.*

### Azqato's Prompts puts every Claude Code prompt worth keeping one click away

**A free, open library of complete, tested prompts for the tasks developers keep re-explaining to their AI assistant.**

*Toronto, 23 August 2026*

Azqato today opened Prompts, a public library of ready-to-use instructions for Claude Code, Anthropic's command-line coding assistant. Every prompt in the library is a full, tested instruction for a real maintenance task, available to copy in a single click at azqato.github.io/prompts. It is free, requires no account, and works from the moment the page loads. The library launches with prompts covering documentation rebuilds, responsive layout audits, and GitHub wiki generation, and grows whenever a new prompt proves worth saving.

### The problem

Anyone working seriously with an AI coding assistant has had the same experience. You spend twenty minutes writing a careful, detailed instruction. It works beautifully. Three weeks later, on a different project, you need it again, and it is gone: buried somewhere in a chat history you cannot search, or in a notes app you forgot you used. So you write it again from memory, worse than the first time, and get a worse result. The prompt was the valuable artifact all along, and nothing was treating it that way.

### The solution

Prompts is a shelf for those instructions. Each one has its own page with a plain-language explanation of what it does, when to use it, and what it will change in your project, followed by the full text in a copy block. Read, copy, paste, run.

The prompts are written to be portable. None of them references the author's projects, accounts, or setup, and none instructs your assistant to push or publish anything. Whatever you run, you decide when it ships.

The site itself is deliberately tiny: no accounts, no tracking, no cookies, and no analytics. It does not know you visited, and it never makes a network request after the page loads.

### What a user says

"I had a prompt that rewrote a whole project's docs in one pass, and I lost it. Spent an afternoon trying to reconstruct it and never got it as good. Now it lives on a page I can find in five seconds, and it is the same every time. That is the whole thing, and the whole thing is what I needed."
- Dana Whitfield, freelance developer

### Get started

Visit azqato.github.io/prompts, pick a prompt, and press Copy. There is nothing to install and nothing to sign up for.

### About Azqato

Azqato builds small, fast, dependency-free web tools and publishes them openly. Its projects, including ComposerAtlas and a public stock analysis methodology site, share a common principle: a tool should be simple enough to understand completely, and should still work in five years without anyone maintaining a toolchain to keep it alive.

---

## 35. Frequently Asked Questions

### What is it?

A public library of reusable prompts for Claude Code. Each prompt is a complete instruction for a recurring development task, presented with a description of what it does and a one-click copy button.

### Who is it for?

Anyone who uses Claude Code. It is maintained as a personal reference by a single author, so it is small and opinionated rather than exhaustive, but every prompt is written to work on any project.

### How do I use it?

Open the site, pick a prompt from the sidebar, read the description to confirm it does what you want, press Copy, and paste it into Claude Code. That is the entire flow. There is no account, no setup, and no installation.

### What does it cost?

Nothing. It is free, public, and open source, with no paid tier, no premium prompts, and no plan to add either.

### Do I need an account?

No. There is no login, no sign-up, and no way to create an account.

### What data do you collect about me?

None. No cookies, no analytics, no telemetry, no logging, and no browser storage. The site makes no network request after it loads. It does not know you visited. Because it is hosted on GitHub Pages, GitHub sees the request as the host, under its own privacy policy, and the author has no access to that.

### Is it safe to run these prompts on my own project?

Read the description first, which is why every page has one: some prompts write and delete files, and the description says so. Beyond that, two rules are enforced on every prompt in the library. No prompt instructs your assistant to push, commit, or publish anything, so shipping is always your decision. And no prompt references the author's accounts, services, or paths, so nothing assumes it is running against this repository.

### Will a prompt change my files without asking?

Some are designed to, and their descriptions say which. The Documentation prompt, for instance, is explicitly read-only for its first three steps and only then begins writing, and only to the documentation files it names. Read the description before you run anything, and run it on a repository with a clean git status so you can review the diff.

### Can I modify the prompts?

Yes, and you should. They are written to be complete starting points, not sacred text. Adapt the wording to your project.

### Can I submit a prompt?

There is no submission process. It is a personal library rather than a community one, and keeping it small is deliberate.

### What are the technical requirements?

A web browser from roughly 2021 or later. Nothing else. There is no app, no extension, and no integration to configure. Using the prompts themselves requires Claude Code, which is separate from this site.

### Does it work offline?

Yes. The site has no runtime dependencies and makes no network calls, so once the page is loaded it works with no connection. Cloning the repository and opening `index.html` from disk works too, with no server.

### Why is there no search?

The library is small enough that the sidebar shows everything at once, which is faster than typing. Search will be added if the library grows past roughly twenty prompts, and not before.

### How is this different from a prompt marketplace?

A marketplace optimizes for volume, discovery, and rating across thousands of contributed prompts. This is the opposite: a handful of prompts, each one used repeatedly by the person who wrote it, kept because it earned its place. There is nothing to browse and nothing to compare. If you want breadth, this is the wrong tool.

### How is it different from just saving prompts in a notes app?

Mostly that it is public, addressable, and structured. Each prompt has a permanent link you can drop into a project's notes. The pages are identical in shape, so reading is fast. And because it is a git repository, every revision to every prompt has a recorded reason.

### What does it not do?

It does not run prompts, generate them, edit them for you, or connect to Claude Code in any way. It is a reference page with a copy button. It also has no search, no tags, no ratings, no comments, and no user accounts, all deliberately.

### Why so few prompts?

Because a prompt only gets added once it has proved useful more than once. Five prompts have been removed since launch: three superseded, and two absorbed into a more capable prompt. Shrinking the library is treated as progress.

### How do I know a prompt is current?

Every change to every prompt is recorded in the changelog with a version, a date, and the reasoning. The site is the current state by definition, since it is generated from the same files the repository holds.

### How do I get help?

There is a Support link in the sidebar. Since prompts are plain text with no runtime, most problems are a matter of adapting the wording to your project, and the description on each page is written to make that possible without help.

### Why is the site built with no framework?

So that it still works in five years with nobody maintaining it. No dependencies means no supply chain, no security advisories, no build to resurrect, and nothing to upgrade. The tradeoffs are recorded in full in section 26 of this document.

### Internal: what is the return on the time invested?

The library pays for itself the first time a prompt is retrieved instead of rewritten, which is roughly twenty minutes of writing plus the quality gap between a careful prompt and a remembered one. Against that, adding a prompt costs a few minutes. The larger return is the documentation standard itself: the Documentation prompt developed here is applied to every other Azqato project, so the effort spent refining it compounds across repositories rather than staying with this one.

### Internal: how is success measured?

By the criteria in section 25, not by traffic. The load-bearing ones are that a copied prompt runs correctly without editing, that the two copies of every prompt never disagree, and that the `file://` guarantee holds. Section 28 explains why almost nothing here is instrumented and why that is a deliberate consequence of the architecture rather than an oversight.

### Internal: where is this going?

Nowhere ambitious, deliberately. The site is feature-complete and the roadmap in section 27 contains only two unscheduled items, both small. The active work is on the prompts and on the documentation standard. Growth in prompt count is explicitly not a goal.

---

## 36. Version History

| Version | Date | Summary |
| --- | --- | --- |
| 1.33.1 | 2026-08-24 | The licensing policy now names the licence file as `LICENSE.md` rather than a plain text file, so it joins the same markdown doc set as everything else the audit writes. |
| 1.33.0 | 2026-08-24 | Added a Licensing default policy to the Documentation prompt: all rights reserved, source-available rather than open source, with a standing carve-out permitting search engines and AI systems to crawl, index, quote, and cite. Grants nothing by default on the reasoning that a permission given to everyone cannot be withdrawn from one person. Generalized the author's example issue-tracker URL, since section 11 forbids a prompt from naming the author's own services. This repository has no LICENSE file and so falls under the default; that is recorded as open question 7 rather than acted on, because publishing a licence is a legal assertion and the author's decision. |
| 1.32.0 | 2026-08-24 | Removed the requirement to ask before publishing, on the author's standing authorization for this repository. Every change here now ships as soon as it is documented and verified. The verification that precedes a push is unchanged and is now the only thing between an edit and the live site, which section 20 states explicitly. Scoped deliberately: it covers this repository only, and it is unrelated to the separate rule that no prompt's text may instruct its reader to push. |
| 1.31.0 | 2026-08-24 | Added a Verification Environment default policy to the Documentation prompt: verify locally, never against production, unless a production check is explicitly asked for. Separates verifying functionality, which is local, from confirming a deploy arrived, which is a comparison run against production after the push. This repository already stated the rule implicitly by describing its check as opening the file from disk, so section 20 documents the existing practice and makes it explicit rather than replacing it, and records the two ways local and deployed differ here. |
| 1.30.0 | 2026-08-24 | Added a Browser Testing default policy to the Documentation prompt: drive Microsoft Edge, never Chrome, because the maintenance machine has no JavaScript runtime and Chrome is the owner's day-to-day browser. Like every policy in that prompt it yields to a rule the project already states. Applied the same rule to the Mobile Audit prompt, which had explicitly instructed driving Chrome, and adopted it for this repository in the section 29 Runbook with the resolved Edge path. |
| 1.29.0 | 2026-08-24 | Made the prompt block collapsible and collapsed it by default. The entire header bar toggles it, with a button labelled for the action it performs rather than the state it is in, and the copy button excluded so copying never collapses what was just copied. Copy works in both states because the text stays in the DOM. No persistence, so no browser storage is introduced. Added section 10a, the first lettered section in this document, and recorded the suffix convention in section 33. Corrected the section 24 assumption that still described `escapeHtml()` as it was before v1.28.0, logged as discrepancy 16. `docs/DESIGN.md` to 1.9 with a full spec for the new component. |
| 1.28.0 | 2026-08-23 | Acted on all four open questions from the v1.27.0 audit. Corrected the two stale `docs/DESIGN.md` blocks rather than leaving them flagged, once confirmed neither held an intended design. Fixed both cheap debt items: `escapeHtml()` now escapes quotes and the slug is escaped at every attribute interpolation, and a failed clipboard write now reports itself instead of failing silently. Added `tools/prompts-mirror.py`, a standard-library check and resync for the mirror invariant. Added a Content Security Policy to `index.html`, verified enforced in headless Chrome, which makes the no-dependency rule a runtime guarantee. Found and worked around a latent CRLF mismatch between the working tree and the data file. Rendered the site for the first time since v1.18.0, closing that verification gap. |
| 1.27.0 | 2026-08-23 | Ran the project's own Documentation prompt against this repository. Rewrote `README.md` to the general-reader standard adopted in v1.26.0, moving all setup, structure, and procedure into this document. Added sections 21 through 35, the eleven required sections this PRD had never carried: Target Users, User Stories, Feature List, Assumptions, Success Criteria, Tenets, Roadmap, Metrics, Runbook, Technical Reference, Security, Public Surface and Retired Items, Documentation Audit Process, Press Release, and FAQ. Added six rows to the section 18 discrepancy table and four open questions. Expanded `docs/DESIGN.md` with the spacing scale, an animation and motion section, component patterns, the error view spec, and a rewritten accessibility section. |
| 1.26.0 | 2026-08-23 | Reworked the README standard in the Documentation prompt. The README is now the public front door for a general reader on every project, with all setup and technical detail relocated to the Runbook and Technical Requirements sections of the PRD rather than duplicated into a new PRD section. Replaced the do-not-pad standard: in `/docs`, and `PRD.md` above all, completeness beats brevity, with the README named as the exception. |
| 1.25.0 | 2026-08-23 | Added the read-only constraint from the retired Project Onboarding prompt to the Documentation prompt, scoped to the analysis steps: steps 1 through 3 forbid all writes and state-changing commands, and writing begins at step 4. Numbered the steps so the constraint can name its range. |
| 1.24.0 | 2026-08-23 | Corrected the definition of public facing: the deployed page is public, the source that builds it is not. Files under `prompts/` are source, so renaming or removing a prompt needs no redirect. Emptied the `REDIRECTS` map, dropping all three entries, and rewrote the rename and removal procedures in section 12 accordingly. |
| 1.23.0 | 2026-08-23 | Retired the Em Dash Audit and Project Onboarding prompts, absorbed into the Documentation prompt in v1.22.0. Both were live, so both slugs redirect to `documentation` rather than being pruned. Four prompts remain. |
| 1.22.0 | 2026-08-23 | Folded the Project Onboarding and Em Dash Audit prompts into the Documentation prompt as required PRD sections: Conventions, Writing Style, Documentation Versus Reality, Risks and Open Questions, and Working Practice. Added the merge-rather-than-overwrite standard and made every policy in the prompt a default that yields to a rule the project already states. Both standalone prompts were left in place. |
| 1.21.0 | 2026-08-23 | Made the removal policy in the Documentation prompt a default rather than an override. A project that already states its own removal rule keeps it, and any conflict with the default is flagged for the author rather than silently resolved. |
| 1.20.0 | 2026-08-23 | Made the Deprecation and Removal section of the Documentation prompt prescriptive rather than descriptive: it now instructs the removal policy from section 12 of this document (redirect anything public facing, prune anything internal) rather than asking the model to record whatever rule it finds. |
| 1.19.0 | 2026-08-23 | Deleted the three hidden prompts (Consolidate Documents, Docs Folder Audit, Documentation Audit), superseded by Documentation since v1.9.0. No redirects, because they were not public facing. Added the "Removing Prompts" policy to section 12, which decides redirects by whether the thing has a public address rather than by whether it is being removed. Added a matching Deprecation and Removal section to the required PRD sections in the Documentation prompt. |
| 1.18.0 | 2026-08-23 | Ran a full read-only onboarding pass and folded it into this document as sections 13 through 20. Ran the Em Dash Audit across the project, adopting the single hyphen as the preferred replacement in titles and version headings and documenting it in section 11. Built the card hover treatment on the home prompt list that DESIGN had specified since v1.0 but that was never implemented. The `**Version:**` header now tracks the release. |
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
