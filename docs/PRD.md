# PRD.md - Prompts

**Version:** 1.26.0
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

The whole project is 12 files in four folders. There is no build output, no vendored code, no ignored directory, and no ignore file: `.gitignore`, `.editorconfig`, and `.vscode/` are all absent, so every file in the working tree is tracked.

```
/
├── index.html          Single-page shell. The only HTML file.
├── README.md           Front door: what the site is, file table, add and rename procedures.
├── css/
│   └── style.css       Entire stylesheet, 509 lines, no imports.
├── js/
│   ├── prompts-data.js Hand-maintained mirror of prompts/*.md. Largest file by far.
│   └── script.js       All client logic: parse, render, route, copy.
├── prompts/            Four .md files, one per prompt. The readable source.
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
6. `route()` reads the hash, resolves any entry in the `REDIRECTS` map (guarded on the target existing, and empty as of v1.24.0), finds the prompt, and calls `renderHome()` or `renderDetail()`. An unknown slug silently falls through to the home view. `renderDetail()` also sets `document.title` and wires the copy button.
7. If `PROMPTS_DATA` is missing or `parsePrompt()` throws, `renderError()` paints a `.status-message` panel telling the reader to check that `prompts-data.js` is present and loaded first. This view exists in both `js/script.js` and `css/style.css` but is not described in section 8 or in `docs/DESIGN.md`.

`js/script.js` is the only file with logic. `js/prompts-data.js` is the only data source. There is no state beyond the module-level `PROMPTS` array and the URL hash, nothing is persisted, and there are no network calls, storage APIs, or external services at runtime. The single browser API dependency is `navigator.clipboard.writeText()` in the copy button.

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
| 3 | `docs/DESIGN.md` section 12 shell template shows `.sidebar` containing the logo, nav, and support div directly | `index.html` wraps all three in a `.sidebar-sticky` div, which carries the sticky positioning and the flex column that pins the Support button. `css/style.css` depends on it | The template is stale, and misleadingly so: rebuilding the shell from it would break the sidebar layout. Trust `index.html` |
| 4 | `docs/DESIGN.md` section 11 CSS file structure lists "Layout (site-wrapper flex, site-layout grid)" | There is no `.site-layout` class. `.site-wrapper` is the grid. The listed order also omits the status message block and the focus styles | Trust the stylesheet |
| 5 | Both `docs/PRD.md` and `docs/DESIGN.md` carry `**Version:** 1.0` in their headers | Their own version history tables run to 1.17.0 and 1.5 respectively | **Resolved in v1.18.0:** the field tracks the current release. PRD is now 1.18.0 (site version) and DESIGN is 1.6 (its own document version). Update it with every release |
| 6 | Section 11 of this PRD prohibits em dashes in markdown documentation | `docs/PATCHNOTES.md` uses a literal em dash in all 20 version headings. `docs/PRD.md` uses one in its title and in the three `/docs/` bullets of section 8. `docs/DESIGN.md` uses one in its title | **Resolved in v1.18.0:** all 25 replaced with single hyphens, plus one prose instance in a v1.11.0 patch note and one double dash in `prompts/documentation-audit.md`. Section 11 now states that the single hyphen is permitted and encouraged, and that instances naming the prohibited character are left alone |
| 7 | Section 7 of this PRD: "Single shared `index.html`, `style.css`, and `script.js`" | The assets moved to `css/style.css` and `js/script.js` in v1.6.0 | Wording only. The constraint it expresses still holds |
| 8 | Section 11 of this PRD: prompts must not reference the author's specific services or accounts | `prompts/consolidate-documents.md` and `prompts/documentation-audit.md` both instruct "Link to the currently live site (ex: https://azqato.github.io/)" | **Resolved in v1.19.0:** both prompts were deleted, so the question is moot. If the pattern reappears in a live prompt, it needs deciding then |

Confirmed accurate, checked rather than assumed:

- All four `prompts/*.md` files are mirrored byte for byte in `js/prompts-data.js`, with no orphans in either direction. Nine at the time of the v1.18.0 pass, before three were deleted in v1.19.0 and two more retired in v1.23.0.
- The `hidden: true` behaviour was verified working on the three prompts that used it, before they were deleted in v1.19.0: excluded from the sidebar and home list, still reachable by direct hash, exactly as sections 8 and 9 describe. No prompt uses the flag now.
- The `REDIRECTS` map is empty as of v1.24.0. The mechanism is retained, guarded on the target existing, for a genuine public-facing address; prompt slugs are not one, as section 12 describes.
- The color tokens, typography scale, breakpoints, and copy button states in `docs/DESIGN.md` match `css/style.css`, apart from item 2 above.
- The `--content-max` formula, `max(820px, calc(75vw - 56px))`, matches the section 4 description in `docs/DESIGN.md`.

Implemented but undocumented: the error view (`renderError()` and `.status-message`); the fact that `renderMarkdown()` also handles headings, which the DESIGN subset list omits; the scroll to top on every route change.

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

None. The working tree is clean, `main` matches `origin/main`, there is only one branch, and there are no TODO, FIXME, or HACK markers anywhere in the repository.

### Open questions for the author

1. Item 1 of section 18: should the README "display-order list" wording be corrected to say that array order is display order?
2. Items 3 and 4 of section 18: should the stale DESIGN shell template and the `.site-layout` reference be corrected?

Answered on 2026-08-23 and folded in above: em dashes were audited (single hyphen adopted), the card hover was built, the `**Version:**` header now tracks the release, Pages publishes `main` at the repository root by manual push, the three hidden prompts were deleted outright under the removal policy now in section 12, and the Em Dash Audit and Project Onboarding prompts were retired behind redirects once the Documentation prompt absorbed them.

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
- Never edit `js/prompts-data.js` and the source `.md` separately in a way that could leave them different.
- Never add a `REDIRECTS` entry for a source file. The map is for public addresses only, and any entry in it becomes permanent.
- Never push or publish without being asked. Publishing is the author's decision (section 12).

### Where to look first

| Kind of change | Start here |
| --- | --- |
| New prompt, or prompt text edit | `prompts/*.md`, then `js/prompts-data.js`, then the README table and tree, then `docs/PATCHNOTES.md` |
| Rename | Section 12, "Renaming Prompts", then grep the repository for the old slug and title |
| Deleting a prompt | Section 12, "Removing Prompts", then grep the repository for the slug and the title |
| Anything visual | The `:root` block in `css/style.css` first, then `docs/DESIGN.md` to check the token is documented |
| Routing, parsing, rendering | `js/script.js`, the only file with logic |
| Layout shell, script order, meta tags | `index.html`, all 30 lines of it |
| Understanding a past decision | `docs/PATCHNOTES.md`, then the commit body, which is usually longer than the patch note |

### After any change

Open `index.html` from disk, not from a server, and check the home list, one prompt page, the copy button, and a direct hash link. That is the only test this project has. Then add a `docs/PATCHNOTES.md` entry with the next semantic version and today's date, and record the release in the version history table below.

---

## 21. Version History

| Version | Date | Summary |
| --- | --- | --- |
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
