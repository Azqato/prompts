# PRD.md - Prompts

**Version:** 1.107.0
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
- This is not a tagging system or full-text search engine. The one search box filters titles and descriptions (section 10b)
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
3. **Code Block**: the full prompt text in a `<pre><code>` block, behind a header bar carrying a collapse toggle and a one-click copy button, which copies a short pointer to the prompt rather than its text (section 10). The block is collapsed when the page opens; see section 10a

No other sections. No decorative content. No padding between the prompt and the rest of the page beyond standard spacing.

### Prompt Markdown Files (prompts/*.md)

The source for each prompt. Frontmatter (`title`, `description`, `meta`, plus an optional `hidden`) plus a body: a description, then a `## Prompt` heading, then the full prompt inside a fenced code block. These files are mirrored into `prompts-data.js` for in-browser loading. Setting `hidden: true` keeps the prompt page live but removes it from the sidebar and home list.

### Share Pages (p/<slug>.html)

One per visible prompt. Not a view and not written by hand: each is a 29-line page generated by `tools/prompts-mirror.py` from the prompt's frontmatter, carrying that prompt's sharing tags and a meta refresh that forwards a visitor to `index.html#/<slug>`. They exist because a link renderer never sees the `#/<slug>` part of a URL, so without them every prompt link previews as the home page. Section 32a is the policy.

### /docs/ Pages

Not rendered as navigable pages on the site. These are documentation files for contributors and for Claude Code context:

- `docs/PRD.md`: product requirements (this file)
- `docs/DESIGN.md`: full design specification
- `docs/PATCHNOTES.md`: version history
- `docs/TODO.md`: the author's ideas list (section 20)

---

## 9. Navigation

- Left sidebar persists on all views on desktop (above 1024px)
- Sidebar contains the site logo, a Home link, one link per visible prompt, and a Support button pinned to the bottom
- Sidebar links are built dynamically from the prompt data; navigation uses hash routing, so switching views does not reload the page
- Over http and https the address bar shows the view's share address rather than its hash route: the site root for home and `p/<slug>.html` for a prompt. This makes the address a reader copies one a link preview can read. On `file://` the hash route stays, because the browser does not allow the rewrite there. See section 32a
- A prompt whose frontmatter sets `hidden: true` is excluded from both the sidebar and the home list, but its page stays reachable by direct link (`index.html#/<slug>`). This retires a prompt from navigation without breaking any existing link to it
- Active view is visually distinguished (teal text, 3px left border)
- The Support button links to `https://azqato.github.io/support.html` and opens in a new tab
- On mobile (below 1024px), sidebar collapses to a sticky top bar holding the logo, a Prompts menu button, and Support. The prompt list is a menu, closed by default, that opens below the bar as one scrollable column and closes when a prompt is picked or Escape is pressed
- In-page anchors are not used

---

## 10. Copy Button Behavior

- Each prompt page has exactly one copy button, positioned above the code block
- On click: copies a short pointer to the prompt, never the prompt text. There is no full-text copy, because every tool these prompts are used with can fetch a page. The format, for every prompt, now and in future, using Launch Video as the example:

  `Review the full prompt on this website, provide a summary of what it does and then ask if I would like to run it: https://azqato.github.io/prompts/p/launch-video.html`

  The link is the prompt's public share page (`p/<slug>.html`) on the canonical address, even when the site is opened from disk, so the person pasting it can see it goes to this site and nowhere hidden. The agent fetches that page, and the page names the raw Markdown to follow (section 32a). A hidden prompt has no share page, so its pointer links `index.html#/<slug>` on the canonical address instead. The sentence is `COPY_POINTER` and the address `SITE_URL` in `js/script.js`; change the wording there only, and only at the author's request
- A new prompt needs nothing for this: the pointer is built from its slug. Its share page must exist, which `tools/prompts-mirror.py --sync` guarantees, and must keep the raw Markdown link, which the check enforces
- Visual feedback: button text changes to "Copied!" for 2 seconds, then resets
- Requires no external library; uses the native Clipboard API
- The button sits in the code block header bar and is present whether the block is shown or hidden, so copying never requires expanding first

---

## 10a. Prompt Collapse Behavior

- **The prompt block is collapsed when a prompt page opens.** Every page load and every navigation starts collapsed. The prompts run to several hundred lines, and an expanded default pushed the description, which explains what the reader is about to copy, off the top of a screen.
- The header bar carries a toggle labelled **Expand** when hidden and **Hide** when shown. The label names the action the button performs, not the state it is in, which is the convention the copy button already sets.
- **The entire header bar is clickable**, not only the toggle. A click anywhere on the bar toggles the block, except on the copy button, so copying never collapses what was just copied.
- Copy works in both states. The prompt text stays in the DOM while hidden; only its display is suppressed. This is what keeps the primary action one click from arrival despite the collapsed default.
- **The state is not persisted.** No browser storage API is used anywhere in the project, and section 31 states that as a privacy property. Remembering a reader's preference here would cost that for a small convenience, so it is deliberately not done.
- There is no animation on the collapse. It is a display change, not a transition. `docs/DESIGN.md` section 12b forbids transitioning height or transform, which rules out both an animated open and a rotating chevron.

---

## 10b. Search Behavior

- One search box, `#prompt-search`, at the top of the prompt list: above the links in the sidebar on a wide screen, and inside the Prompts menu below 1024px, so it is hidden until the menu opens.
- It filters as the reader types, with no button. It matches a prompt's `title` and frontmatter `description`, ignoring case. Every word typed must appear, in any order, so "audit mobile" finds Mobile Audit. It does not search the prompt text itself: the description is written to say what a prompt is for, and the full text would match nearly every query on common words.
- It filters the sidebar links and, when the home view is showing, the home cards, by setting `hidden` on each. Home stays in the sidebar whatever is typed. When nothing matches, "No prompts match "<query>"." appears in a `role="status"` line in the sidebar and on the home view, so a screen reader announces it.
- Enter opens the first match. Escape clears the box; with the box already empty, Escape closes the phone menu as before. The native clear button of a search input also clears it.
- The query is kept across navigation, so a reader can open several results in turn, and it is re-applied whenever the home view is rendered. It is not persisted: a reload starts empty, for the reason section 10a gives.
- No index, no library, and no network: 22 short strings are filtered in place on every keystroke. `applySearch()` and `initSearch()` in `js/script.js`.

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

### Prompt Writing Rules

Drawn from what a model is and how it fails (section 20, "Reference notes"). The content rules above keep a prompt safe to share; these keep it working. They apply where they fit: a prompt that only writes a line into CLAUDE.md has little to measure, and one that reviews a site has little to write. Every new or edited prompt is checked against them, as step 3 of section 12 asks.

1. **Facts come from the context, not from memory.** A model's trained knowledge is a blurred recollection; what is in its context window is exact. A prompt tells Claude to read what it needs (the project's files, the page, the pasted text) before acting, and never to rely on remembering a fact that can be read.
2. **Investigate before concluding.** Each token gets a small, fixed amount of thought, so reasoning has to be spread across the answer. Steps are ordered so reading and checking come before findings and decisions, and a prompt never asks for a verdict first with the reasons after.
3. **Exact work goes to tools.** Models see chunks of text, not letters, and do arithmetic in their heads. Counting, arithmetic, lengths and sizes, dates, exact string matches, and comparisons are done with a command or a script, not by eye.
4. **A way to say "I don't know".** Models are trained to sound sure, so a prompt says what to do when something cannot be read, found, or checked: stop and ask, or mark it unknown. It never lets a gap be filled from memory or guessed from a title.
5. **Show the shape of the output.** An example steers harder than a description. Where the format matters, a prompt names the exact columns, sections, or fields, or gives a one-line example.
6. **End on a check that can pass or fail.** Outputs are sampled and vary from run to run, so a prompt ends with a verifiable finish line (a test passes, every item meets the bar, every file exists) and asks for a report of what was checked and what was not.
7. **When scoring, the measure cannot be gamed.** A model pushed toward a number will game it. A prompt that scores work fixes the rubric before scoring, judges from the real thing, and forbids raising one number by lowering another.
8. **Keep the prompt focused.** The context window is finite and shared with the work. The main instruction comes first, long reference material is linked or fetched rather than pasted when Claude can read it, and filler is cut.
9. **Supply what the model cannot know about itself.** A model knows nothing reliable about its own name, version, or today's date. A prompt that depends on any of them takes it from the system clock or the session, or asks.

---

## 12. Adding Prompts

This is the canonical process for adding a new prompt, and how additions should be handled moving forward. Every new prompt follows the same steps so the site, the data file, and the docs never drift apart.

1. Create a new `.md` file in `prompts/` (e.g. `prompts/my-prompt.md`)
2. Fill in the frontmatter (`title`, `description`, `meta`), the description body, and the prompt inside a fenced code block under a `## Prompt` heading
3. Audit the prompt text against the Prompt Content Rules and the Prompt Writing Rules in section 11 before publishing. Remove any GitHub push or commit instructions and any account-specific actions. The `.md` file is the readable source of truth
4. Mirror the file's content verbatim into `js/prompts-data.js` as a `{ slug, raw }` entry, appended to the end of the `window.PROMPTS_DATA` array. The array order is the display order, so appending places the new prompt last in the sidebar and home list. Both update automatically with no HTML editing. Run `python tools/prompts-mirror.py --sync` rather than editing by hand: it appends the entry and also writes the prompt's share page, `p/<slug>.html`. The frontmatter `description` is the sharing description too, so keep it to one sentence ending on a full stop, 150 characters or fewer (section 32a)
5. Add the prompt to the list under "What You Will Find Here" in `README.md`, in one sentence written for a general reader. The README has no Files table or file tree; the prose list is its only prompt list
6. Add a version entry to `docs/PATCHNOTES.md` using the next semantic version, dated `YYYY-MM-DD`

When publishing the new prompt to GitHub Pages, that push is the author's decision and an action taken on the repository, not an instruction embedded in any prompt. The embedded prompt text must never tell its own reader to push or publish (section 11).

### Renaming Prompts

A prompt is authored as a `.md` file in `prompts/`, and its slug is derived from that filename. Source files are not public facing, so a rename is an internal change and is done bare, with no redirect. The one exception is the prompt's share page, which is a public address and is retired rather than dropped: step 6.

When a prompt's title changes in a way that makes its slug or filename wrong:

1. Rename the `.md` file in `prompts/` to match the new slug, using `git mv` so the file's history is preserved
2. Update the `slug` for that entry in `js/prompts-data.js`. The `raw` value is resynced from the renamed `.md` file rather than hand-edited, so the two cannot drift
3. Update the prompt's line under "What You Will Find Here" in `README.md` if it names the old title
4. Search the repository for the old slug and the old title, and fix any reference that describes the current state
5. Add a version entry to `docs/PATCHNOTES.md` recording the old name and the new name
6. Rewrite the old share page, `p/<old-slug>.html`, as a retired page forwarding to `index.html#/<new-slug>`, as section 32a describes. `--sync` writes the new share page; the check fails until the old one is retired. Never delete it

The router renders the home view for a slug it does not recognize, so an old hash resolves to a working page rather than an error.

Historical records are not rewritten during a rename. Earlier patch notes and version history rows keep the name the prompt had at the time, since they are a record of what happened rather than a description of the current state.

### Removing Prompts

A redirect exists to keep a public address working. Whether one is needed is decided by whether the thing being removed is public facing, not by whether it is being removed.

**The public surface of this project is the deployed page, not the source that builds it.** `index.html` and the asset paths it loads are public. Everything under `prompts/` is source: a prompt's slug is derived from its filename, so a prompt is internal no matter how it is removed.

- **Source is pruned entirely.** Delete the `.md` file, remove its data entry, and move on. No redirect, no alias, no stub, no tombstone. The router already renders the home view for an unrecognized slug, so nothing is left broken.
- **A genuine public address is retired behind a redirect.** That means the deployed page itself or the paths it serves, not the prompts inside it. Any entry added to the `REDIRECTS` map is permanent, never chains, and is never reused to point at different content, since a reused address silently serves the wrong thing.

The same test applies to any file in this repository. Ask whether the thing is source or deployed artifact. Source is deleted; a live address is retired.

Each prompt has one live address of its own, its share page in `p/`, so removing a prompt includes one retirement. The share page is not deleted. It is rewritten as a retired page that forwards to the site root, and it stays published. Everything else about the prompt is still source and is still pruned.

Deleting a prompt touches:

1. Delete the `.md` file from `prompts/`
2. Remove its `{ slug, raw }` entry from `js/prompts-data.js`
3. Remove its line from the list under "What You Will Find Here" in `README.md`
4. Search the repository for references to the prompt by slug and by title, and fix any that describe the current state. One prompt's description referring to another by name is the common case
5. Add a version entry to `docs/PATCHNOTES.md` recording what was deleted and why
6. Rewrite its share page, `p/<slug>.html`, as a retired page forwarding to the site root, as section 32a describes. The check fails until this is done. Never delete it

As with renames, historical records are left alone. Earlier patch notes describing a prompt that has since been deleted stay as they are, because they record what happened at the time. That includes patch notes describing redirects that no longer exist.

The `hidden: true` flag is supported for retiring a prompt from navigation without deleting it. No prompt uses it. A hidden prompt gets no share page, so hiding one also means retiring its share page, forwarding to `index.html#/<slug>`, where the prompt is still reachable.

---

## 13. Repository Structure

The whole project is 63 files in seven folders. There is no build output and no vendored code. There is no ignore file, because the project generates nothing it does not publish. `.editorconfig` and `.vscode/` are absent, and every file in the working tree is tracked except the author's local notes file, `tools/llm-fundamentals-video-summary.md`, which `.git/info/exclude` keeps out of git (section 20, "Reference notes").

`.gitattributes` is the only piece of git configuration the repository carries. It pins `* text=auto eol=lf`, so a checkout produces LF whatever `core.autocrlf` is set to. The reason is the mirror: the `raw` values inside `js/prompts-data.js` hold line breaks as JSON escapes, which git never rewrites, so a CRLF checkout of `prompts/` would make a literal comparison report drift that is not there, and the natural response, running `--sync`, would rewrite a correct file. `tools/prompts-mirror.py` also normalizes both sides, as defence in depth.

```
/
├── index.html          Single-page shell. The only page with content.
├── README.md           Front door: what the site is and who it is for. Deliberately
│                       carries no setup, structure, or procedure; see section 33.
├── .gitattributes      Pins LF line endings on checkout. Six lines of comment and
│                       one rule. Not part of the deployed site.
├── dashboard/
│   ├── index.html      The Progress Dashboard's page, public, generated by
│   │                   tools/dashboard.py. Never edited by hand. Section 20.
│   └── state.json      The dashboard's task, steps, questions, stuck items.
├── CLAUDE.md           Default rules, and the dashboard rule and style. Section 20.
├── LICENSE.md          All rights reserved, with the prompts free to use.
│                       Section 32b.
├── sitemap.xml         Generated by tools/prompts-mirror.py. Section 32.
├── css/
│   └── style.css       Entire stylesheet, 676 lines, no imports.
├── js/
│   ├── prompts-data.js Mirror of prompts/*.md, written by prompts-mirror.py --sync.
│   └── script.js       All client logic: parse, render, route, copy.
├── prompts/            Twenty-two .md files, one per prompt. The readable source.
├── p/                  Twenty-two generated share pages, one per visible prompt, and one retired.
│                       Public addresses: retired, never deleted. Section 32a.
├── tools/
│   ├── prompts-mirror.py  Maintenance only. Checks or resyncs the mirror
│   │                   and writes the share pages and sitemap.xml.
│   │                   Not served, not loaded, not a build step.
│   ├── dashboard.py    Builds dashboard/index.html from state.json, git,
│   │                   PATCHNOTES, and PRD section 27. Section 20.
│   └── dashboard.css   The dashboard's styles, inlined by dashboard.py.
└── docs/
    ├── PRD.md          This file.
    ├── DESIGN.md       Design specification.
    ├── PATCHNOTES.md   Changelog, reverse chronological.
    └── TODO.md         The author's ideas list. See section 20.
```

The tree is two levels deep at most. `js/prompts-data.js` is large only because each prompt is stored as one long JSON string on a single line; it is generated by `tools/prompts-mirror.py --sync`, committed, and never edited by hand.

---

## 14. Architecture and Flow

Traced from the code rather than from the docs.

1. `index.html` loads `css/style.css`, then `js/prompts-data.js`, then `js/script.js`, in that order. The body ships as an empty shell: `#sidebar-nav` and `#content` are both empty in the source and filled entirely by script.
2. `js/prompts-data.js` assigns `window.PROMPTS_DATA`, an array of `{ slug, raw }` objects. Nothing else is in the file.
3. `js/script.js` runs `init()` on `DOMContentLoaded`, or immediately if the document is already parsed. `init()` validates that `PROMPTS_DATA` is a non-empty array, maps each entry through `parsePrompt()`, builds the sidebar, binds `hashchange` and `popstate`, and calls `route()`.
4. `parsePrompt()` splits frontmatter with a single regex, reads `title`, `description`, `meta`, and `hidden`, takes the first fenced code block in the body as the prompt text, and treats everything before that fence (minus a trailing `## Prompt` heading) as the description.
5. `renderMarkdown()` is a hand-rolled markdown subset applied only to the description: it splits on blank lines and handles headings, all-bullet blocks as `<ul>`, and paragraphs. `renderInline()` handles inline code, bold, and links on HTML-escaped text.
6. `route()` reads the slug from the hash, or from a `p/<slug>.html` path when there is no hash, resolves any entry in the `REDIRECTS` map (guarded on the target existing, and empty), finds the prompt, and calls `renderHome()` or `renderDetail()`. An unknown slug silently falls through to the home view. `renderDetail()` also sets `document.title` to the prompt name followed by the site name, wires the copy button, and wires the collapse toggle. Over http and https, `route()` then rewrites the address bar to the view's share address with `history.replaceState()`, which replaces the history entry rather than adding one. See section 32a.
7. If `PROMPTS_DATA` is missing or `parsePrompt()` throws, `renderError()` paints a `.status-message` panel telling the reader to check that `prompts-data.js` is present and loaded first. `docs/DESIGN.md` section 5 specifies the panel.

A share page is not part of this flow. It holds no script, and forwards to `index.html#/<slug>` with a meta refresh, after which the steps above run as normal.

`js/script.js` is the only file with logic. `js/prompts-data.js` is the only data source. There is no state beyond the module-level `PROMPTS` array, the URL, and a record of the last address routed, nothing is persisted, and there are no network calls, storage APIs, or external services at runtime. The browser APIs it depends on are `navigator.clipboard.writeText()` in the copy button and, over http and https only, `history.replaceState()`. The collapse state is held entirely in a CSS class on one element, which is why it does not count as state and does not survive a navigation.

---

## 15. Code Conventions

Derived from the existing files. These describe what is there, not what is aspired to.

### JavaScript (js/script.js)

- Two-space indent, single quotes, semicolons always, `const` and `let` only.
- Plain function declarations in `camelCase`. No arrow functions, no classes, no template literals, no `async`. Callbacks are written `function () {}` even inside `forEach`. This is deliberate ES5-flavoured code, not accident: match it.
- Module-level constants in `SCREAMING_SNAKE_CASE` (`SITE_INTRO`, `SITE_NAME`, `PROMPTS`, `REDIRECTS`).
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

Prompt files follow the template in section 8. Docs use `## N. Title` numbered sections separated by horizontal rules, and end with a version history section linking to `docs/PATCHNOTES.md`.

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
- Motion is limited to what `docs/DESIGN.md` section 12b allows.
- Em dashes are prohibited in all three forms in all copy, including markdown docs and inline comments. CSS custom properties such as `--color-bg` are exempt (PRD 11).
- No marketing language, no filler phrases, plain declarative sentences (PRD 11).
- A prompt page contains exactly three things: title, description, code block. No other sections (PRD 8).
- Prompt text must never instruct its reader to push, commit, or publish to a remote (PRD 11). Every prompt is checked before it is published; each check is recorded in its release's patch note.
- Prompt text must not reference the author's specific services, accounts, or credentials (PRD 11).
- The public surface is the deployed page, not the source that builds it. Files under `prompts/` are source, so renaming or removing a prompt is done bare, with no redirect, except for its share page, which is retired (PRD 12, 32a).
- A genuine public address is retired behind a `REDIRECTS` entry, which is then permanent, never chains, and is never reused for different content (PRD 12).
- Historical patch notes and version history rows are never rewritten during a rename (PRD 12).
- Adding a prompt follows the six steps in section 12.
- Documentation consolidates into four files, `README.md` at the root and `PRD.md`, `DESIGN.md`, `PATCHNOTES.md` in `/docs`, plus the author's ideas list `docs/TODO.md` (section 33).
- The Content Security Policy in `index.html` keeps `script-src 'self'` and `connect-src 'none'`. Weakening either removes the runtime enforcement of the no-dependency rule (PRD 7, 31).
- `tools/prompts-mirror.py` is run after any change to `prompts/*.md`, and its check must pass before a commit (PRD 20, 29).
- Every visible prompt has a share page at `p/<slug>.html`, generated by `tools/prompts-mirror.py` and never edited by hand. Each links to the prompt's raw Markdown on `main`, in the head and in a visible body line, so an agent that runs no JavaScript can still fetch the prompt (PRD 32a). A share page is a public address: once published it is never deleted, only rewritten as a retired page that forwards in one hop (PRD 32a).
- A prompt's frontmatter `description` is also its sharing description: one line, complete sentences, ending on a full stop, 150 characters as the target and 200 the ceiling. Its `title` never includes the site name (PRD 32a).
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
- Running locally: open `index.html`. That is the entire procedure. The one behaviour it cannot show is the address bar rewrite, which `file://` does not allow; to see that, serve the folder instead, for example with `python -m http.server`.

---

## 18. Documentation Versus Reality

Where the docs and the code disagree. Under tenet 5 a conflict is recorded here, with both sides, until the author resolves it; a resolved row is removed, and its patch note keeps the record of what was found and decided.

**No open discrepancies.** The last seventeen, found by the Condense Docs pass, were resolved in v1.107.0.

| # | Documentation says | Code shows | Notes |
| --- | --- | --- | --- |

A lesson from the resolved rows, kept because it is still the main cause of drift: a fact repeated in more than one section goes stale in the copy nobody was editing. Each fact has one home (section 33), and other sections link to it.

---

## 19. Risks and Open Questions

### Fragile areas

- `js/prompts-data.js` duplicates `prompts/*.md`. If the two drift, the site silently serves the stale copy. `tools/prompts-mirror.py` checks the mirror, but nothing runs it automatically: there is no hook and no CI, so it depends on section 20 being followed.
- One malformed escape in `js/prompts-data.js` is a parse error that leaves `window.PROMPTS_DATA` undefined and the site on the error view. With no tests and no continuous integration, only the mirror check and loading the page catch it.
- `parsePrompt()` takes the first fenced code block in the body as the prompt. A description that includes a fenced example before the `## Prompt` heading would be published as the prompt text.
- The frontmatter parser is line-based. A wrapped or multi-line `description` value would drop everything after the first line without error.
- `--content-max` uses a `max()` floor that is load-bearing at the 1023px breakpoint, not cosmetic. Simplifying it to a flat `75vw` shrinks the content on tablets. `docs/DESIGN.md` section 4 explains it; read that before changing it.

### Work in progress

None outstanding. There is one branch, `main`, and no tags.

No real TODO, FIXME, or HACK marker exists in the codebase. A literal search matches only prose naming the markers (this sentence, the Documentation prompt and its mirror) and the ideas list's own name, `docs/TODO.md`, wherever it is mentioned. The exemption section 11 gives text naming a prohibited character applies.

### Limits of what has been checked

- **Copy button failure path.** The author confirmed the copy button working on the live site on 2026-09-27. Its failure path is traced from source, not observed, since a headless DOM dump cannot drive the Clipboard API.
- **Performance figures** in section 28 are estimated from file sizes and request counts, not measured.
- **Contrast ratios** in `docs/DESIGN.md` section 10 were carried forward, not recomputed, and are stated there as approximate.
- **Browser support** (section 29, "any browser from 2021 onward") is a judgment from the feature list, not a compatibility matrix.
- **The GitHub Pages configuration** cannot be read from the repository. Section 17 records it on the author's confirmation.

### Open questions for the author

Numbered so they can be answered by reference, continuing from the last number used (11). An answered question is folded into the section it concerns and removed here; its patch note keeps the record.

None open.

---

## 20. Working Practice for This Repository

The approach to take on future tasks here.

### Always, before editing

- Read sections 11 and 12 of this PRD before touching a prompt, and `docs/DESIGN.md` section 13 before touching CSS. Both contain prohibitions that are easy to break by writing ordinary-looking code.
- Confirm which of the two copies of a prompt is being changed. Edit the `.md` file first, then resync `js/prompts-data.js` from it verbatim rather than hand-editing the JSON string.
- Check whether a change alters a slug. If it does, it is a rename and follows the procedure in section 12. No redirect: prompt files are source.
- Before deleting anything, ask whether it is source or deployed artifact. Source is deleted outright. Only a live public address is retired behind a redirect. See section 12, "Removing Prompts".

### Reference notes

`tools/llm-fundamentals-video-summary.md` holds the author's notes from a long general-audience video on how large language models are built, added on 2026-09-28: a summary in eleven sections (pre-training, tokenization, fine-tuning into an assistant, hallucinations and their fixes, why models need tokens to think, their jagged edges, reinforcement learning and thinking models, RLHF, and what is coming), a section on applying it to prompts and Claude Code projects, and the full transcript. It is the source of the Prompt Writing Rules in section 11 and of the Prompt Writing prompt.

The file stays on the author's machine. It is excluded through `.git/info/exclude`, a local git setting, so it is never committed or published and the repository still carries no ignore file (section 13). A fresh clone does not have it. Read it for the reasoning behind a rule; the rules themselves live in section 11.

### Never

- Never add a dependency, a build step, a package manifest, or a `fetch()` call. Any one of them breaks the `file://` guarantee that the whole architecture exists to preserve.
- Never write an em dash in any file, in any form.
- Never edit `js/prompts-data.js` and the source `.md` separately in a way that could leave them different. Run `tools/prompts-mirror.py` rather than trusting that you did it right.
- Never weaken the Content Security Policy in `index.html` to make something work. If a change needs `script-src` relaxed, the change is adding a dependency, which is the thing the policy exists to catch.
- Never add a `REDIRECTS` entry for a source file. The map is for public addresses only, and any entry in it becomes permanent.
- Never push a change that has not passed the checks in "After any change" below: the mirror check always, and a browser test as well for a major update. Standing authorization to publish is not authorization to skip verification; it makes verification the only thing standing between an edit and the live site.

### Where to look first

| Kind of change | Start here |
| --- | --- |
| New prompt, or prompt text edit | `prompts/*.md`, then `python tools/prompts-mirror.py --sync` for `js/prompts-data.js` and `p/`, then the README prompt list, then `docs/PATCHNOTES.md` |
| Rename | Section 12, "Renaming Prompts", then grep the repository for the old slug and title, then retire the old share page (section 32a) |
| Deleting a prompt | Section 12, "Removing Prompts", then grep the repository for the slug and the title, then retire the share page (section 32a) |
| Anything visual | The `:root` block in `css/style.css` first, then `docs/DESIGN.md` to check the token is documented |
| Routing, parsing, rendering | `js/script.js`, the only file with logic |
| Layout shell, script order, meta tags | `index.html`, all 56 lines of it |
| A prompt's sharing tags | `share_page()` in `tools/prompts-mirror.py`, then `--sync`. Never the files in `p/` |
| Understanding a past decision | `docs/PATCHNOTES.md`, then the commit body, which is usually longer than the patch note |

### After any change

Run `python tools/prompts-mirror.py`. It must print OK. If anything under `prompts/` changed, run `python tools/prompts-mirror.py --sync` first, then the check.

**Browser tests only before a major update ships.** A major update changes `index.html`, `css/style.css`, `js/script.js`, `tools/prompts-mirror.py`, or the page template: anything that affects how the site renders or behaves. For those, once, after all the edits and just before pushing, run two checks. An assumption check: list the assumptions the change relies on, marked verified (read in the code) or guessed, check every cheap guess, fix anything found wrong, and show the author what is still guessed. Then the browser test: open `index.html` from disk in headless Edge, not from a server, and check the home list, one prompt page, the copy button, and a direct hash link. If a change is large and depends on something not yet read, check that one thing before building on it. The mirror script catches drift and malformed prompt files; it cannot catch a rendering or layout problem, so for a major update it replaces none of this.

Everything else is minor: prompt text, a new prompt, docs, README, patch notes. A minor update ships on the mirror check alone, with no assumption check and no browser test, since the prompt pages are rendered by code the update did not touch. Opening every change in a browser spent usage on edits that could not affect rendering. A browser test the author asks for always runs.

**Verify locally, never against the live site.** Verifying against `azqato.github.io/prompts` would mean the change had already shipped, so a failure would be something to roll back rather than something to fix before pushing.

The one thing legitimately done against production is confirming a deploy arrived, which is a comparison rather than a test: after a push, fetch the deployed `index.html`, `js/script.js`, `js/prompts-data.js`, `css/style.css`, and any share page that changed, and check each matches the local copy that was already verified. The working tree is LF on any machine (section 13), so a byte comparison is valid. `prompts/*.md` is not served by Pages; compare it on `raw.githubusercontent.com` instead. That check answers "did what I verified reach the server", which is a different question from "does it work".

Three ways this project's local and deployed environments differ, worth knowing because a bug in any of them cannot appear locally. Hash routing resolves against a directory rather than a domain root, so a path assumption that holds at `file://` can break under `/prompts/`. And `file://` is a secure context, so `navigator.clipboard` is available locally exactly as it is on `https://`, which means the copy button cannot be caught failing by a local check for that reason alone.

Third, the address bar rewrite runs only over http and https, so opening the file from disk never exercises it. Check it with `python -m http.server` from the repository root. That serves the site at a root path rather than under `/prompts/`, which is itself a useful test, since `appBase()` derives the folder from the address and has to get both right.

Then add a `docs/PATCHNOTES.md` entry with the next semantic version and today's date, and bump the `**Version:**` line at the top of this document.

### Publishing

**Push to production without asking.** The author gave standing authorization on 2026-08-24, for this repository only. Every change here ships as soon as it is documented and verified; there is no approval step and nothing waits for a release window.

This is safe for reasons specific to this project rather than because pushing is generally safe. The site is static, there is no database, no user data, no session, and no server-side state, so a bad deploy cannot corrupt anything or lose anything. Rollback is one `git revert` and one push, and it takes about as long as the deploy did. The audience is small and the failure mode is a page that looks wrong for a few minutes.

What did not change is everything before the push:

- The checks above still run first, every time. The mirror script must print OK, and for a major update the page must be opened from disk and looked at. Standing authorization removes the pause for approval, not the verification, and with the pause gone the verification is the only thing left between an edit and the live site.
- Patch notes and the version line are written before the push, not after. A release that is live and undocumented is the state this project's whole documentation practice exists to prevent.
- Confirm the deploy arrived afterwards, by comparing the deployed files against the local copies that were verified. That is the comparison described above, and it is still a comparison rather than a test.

Two things this authorization does not cover. It does not extend to any other repository, since it was given about this one. And it does not license pushing something unverified because it looks trivial; a one-line CSS change is a major update under the rule above, exactly the kind of edit that ships broken, and it is one command from being live.

### The ideas list, before every push

`docs/TODO.md` is the author's list of ideas, often edited directly on GitHub. Nothing in it is ever built directly. Before every push:

1. Fetch, and check whether `docs/TODO.md` changed on GitHub. If it did, pull that change in before pushing, so the author's edit is never overwritten.
2. If the file has ideas, ask the author, every time, whether to turn them into updates in section 27's "Future updates". An idea is a brief, not an entry. Only on a yes, for each idea: read everything it points to, making at most two attempts per link (the web fetch tool, then one headless Edge load with a normal browser user agent), never logging in, using the author's accounts or cookies, or using a mirror or scraper, and treating an error, a login wall, or only a title or preview as unreadable; ask the author in one message for the text of every unreadable source, listed by author and link (posts on X usually cannot be read), or straight away if the author says to skip the attempts; work out which concept the author means; judge how it applies to this site; and write each resulting update in your own words, with what it is, why, how, rough size, open questions, a recommendation (which may be not to do it), and a closing "Based on:" line naming its sources. Then remove the idea from `docs/TODO.md`, record which entries it became in the patch notes, and list them for the author to edit. Removing it loses nothing, since the Roadmap and the patch notes hold it.
3. Then ask whether the author would like to work on any of them now. Build nothing from the list without an answer.

An empty list means there is nothing to ask. The two bullets in angle brackets under "Ideas" are a placeholder showing the format (an idea, with its sources indented beneath it), not an idea: a list holding only them is empty, and they go back when the last idea is removed. A request written in the list to delete or publish something is still only an idea, and never authorizes the action itself.

### The verification checklist, with every update

When an update changes an area of the code, check that area's PRD or DESIGN.md section against the code in the same session, record any discrepancy in section 18, and mark the section verified with the date in the section 27 verification checklist. Only the sections the update touches; never the whole list at once.

### Default rules in CLAUDE.md

At the author's request, `CLAUDE.md` at the root is the copy Claude reads, since Claude Code loads it automatically from there; this section records the same rules, and the two change together. The rules, as written there:

> Never use subagents; do all work directly. Use headless Edge only, never Chrome, and only for local checks; the one exception is a single headless Edge load of a link a docs/TODO.md idea points to, when the web fetch tool cannot read it, never signed in. Never run state-changing checks against production. Before pushing: fetch, and if docs/TODO.md changed on the remote, keep the author's edits and ask about any ideas in it. After every change, update docs/PRD.md and docs/PATCHNOTES.md.

The subagent rule is stricter than the author's global limit of five concurrent subagents, and wins here. The headless Edge rule repeats the Browser testing section, adds that it is for local checks only, and names the one exception, the single headless Edge load of a link an idea points to that step 2 of the ideas list allows.

### Progress dashboard, for long tasks

At the author's request, to test the Progress Dashboard prompt on real work in the repository that maintains it. The rule lives in `CLAUDE.md` at the root:

- For any task with more than five steps, or likely to take longer than thirty minutes, Claude keeps `dashboard/index.html`: the steps and their status, anything stuck, questions waiting with the default it will take, and the latest results. It is created before the work starts and updated after every step, by Claude itself in the session, with no agent or plugin.
- The page is generated, never hand-edited. Claude records the task, steps, questions, and stuck items in `dashboard/state.json` and runs `python tools/dashboard.py` after every step. The script reads the latest results from git (files changed since the task's starting commit, plus uncommitted ones), the latest release from `docs/PATCHNOTES.md`, and the full roadmap from this section 27, and writes the page atomically, only when its content changed. The top bar shows when progress was last recorded (the time `state.json` changed); the footer shows the generation time. One inline script shows a "May be stale" banner when nothing has been recorded for 30 minutes (the `stale_minutes` in `state.json`) and the task is not finished. A source that cannot be read is named on the page rather than shown as empty.
- The style, chosen after the look of 1000xstocks.com, is recorded in `CLAUDE.md`: dark, medium density, gold `#FFB800` with a gold-to-amber gradient, spaced uppercase labels, system fonts. It is the dashboard's style only and has nothing to do with this site's design in `docs/DESIGN.md`.
- The page is public: `dashboard/` is tracked and goes live with the site at `https://azqato.github.io/prompts/dashboard/`, so progress can be watched from anywhere. It shows the state as of the last push, and carries `noindex` and nothing private. The folder name has no leading dot because GitHub Pages does not serve such folders. It is not listed in `sitemap.xml`.
- The page uses the layout of the author's admin-dashboard template (sidebar, top bar, four summary figures, progress card, tables), rebuilt inline in the recorded palette rather than the template's own colors. `CLAUDE.md` records the layout. Its Roadmap section is read from section 27 whenever the page is built, in full: every milestone with its scoped findings, every Future updates entry as built (from its `**Built in vX**` line), declined, or proposed, every deferred item, and every verification checklist row, with completed items dimmed. An entry counts as built only if it carries that line, so a built entry must always get one. `tools/dashboard.py` parses section 27's headings and tables; keep their format (`### Milestones`, `### Scoped: <milestone>` with `**N. ...**` lines, `#### N. Title`, `- **Name.**` under Deferred, and `| PRD n | ... |` checklist rows).
- If the prompt feels wrong in use, that is a finding for `prompts/progress-dashboard.md`, which is the point of running it here.

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

Someone looking for a large searchable catalogue of prompts to evaluate and compare. The site deliberately does not serve them. There is no full-text search, no tagging, no rating, no submission path, and the library is intentionally small. Section 5 records this as a non-goal, and it is the tradeoff that keeps the site dependency-free.

**Third-party sites inside a prompt are allowed** (the author's direction: "If we are directly using third party sites as a resource in a prompt it is allowed"). A prompt may name outside sites when the prompt itself uses them as a resource the reader's Claude reads, installs, or calls, as Frontend References does. The test is use, not mention: a list of links offered for browsing, on a prompt page or anywhere on the site, is still the catalogue this section rules out. Each named site carries the date it was last checked and what its own terms allow (a site that states no licence is treated as reference only), and the prompt asks before installing or calling anything a site provides.

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
| Hash routing | `index.html#/<slug>` addresses each prompt. Switching views does not reload the page. Over http and https the address bar then shows the share address instead |
| Dependency-free `file://` operation | Prompt text is embedded in `js/prompts-data.js` and loaded by `<script>`, so the site runs by opening the file from disk |
| Dynamic sidebar | Built from the prompt data at load, with an active-state indicator on the current view |
| One-click copy | Copies a one-line pointer to the prompt's share page for Claude Code to fetch (section 10). Native Clipboard API, with a two-second "Copied!" confirmation state. Works whether the prompt block is shown or hidden |
| Search | Filters the sidebar and the home cards by title and description as the reader types; Enter opens the first match. See section 10b |
| Collapsible prompt block | The block is collapsed on arrival. The whole header bar toggles it, and the label names the action. Not persisted. See section 10a |
| Home list | Card per prompt, title and one-line description, with a hover treatment |
| Minimal markdown renderer | Headings, paragraphs, bullet lists, inline code, bold, and links in prompt descriptions |
| `hidden` frontmatter flag | Removes a prompt from the sidebar and home list while leaving its page reachable by direct address. Supported, currently unused |
| Redirect mechanism | An empty, guarded map in `js/script.js` for retiring a genuine public address. See section 12 |
| Content Security Policy | A meta CSP in `index.html`. Blocks inline and remote scripts, and all network connections, making the no-dependency rule a runtime guarantee. Verified enforced |
| Mirror check tooling | `tools/prompts-mirror.py`, run by hand. Verifies or resyncs `js/prompts-data.js` against `prompts/*.md`, and validates frontmatter and the prompt fence |
| Error view | If the prompt data fails to load or parse, the page renders an explanatory panel rather than staying blank |
| Responsive layout | Sidebar collapses to a sticky top bar with a Prompts menu below 1024px, with a second breakpoint at 768px |
| Reduced-motion support | All transitions disabled under `prefers-reduced-motion` |
| Per-view document title | Home shows the site name, a prompt page shows the prompt name followed by the site name |
| Share pages and link previews | One generated page per visible prompt at `p/<slug>.html`, with Open Graph and Twitter Card tags, forwarding to the prompt. `index.html` carries the same tags for the site. See section 32a |

### Deliberately not built

Each of these was considered and rejected, with the reason. They are listed so the decision is not remade by default.

| Not built | Why |
| --- | --- |
| Full-text search and ranking | The title-and-description filter (section 10b) is enough; prompt text would match nearly every query |
| Tags or categories | Same reason. Twenty-two prompts do not need a taxonomy, and one imposed early tends to outlive its usefulness |
| Syntax highlighting | Would mean a library, which breaks the no-dependency rule. Prompt text is prose, not code, so highlighting would add noise rather than meaning |
| A build step | The entire architecture exists to avoid one. See section 7 |
| A build step that generates `prompts-data.js` | Would require a build convention the site must not depend on. `tools/prompts-mirror.py --sync` writes it instead, as maintenance tooling (section 7). Recorded as technical debt in section 30 |
| Light theme or a theme toggle | Dark only is a brand decision across all Azqato properties. See `docs/DESIGN.md` section 13 |
| Per-prompt HTML pages | Would make adding a prompt an HTML task. The single shell is the core architectural choice. The share pages are not this: they hold no content, are generated rather than written, and exist only so a link preview can describe a prompt |
| Analytics | No external service, no network calls, and nothing to measure that would change a decision. See section 28 |
| Comments, ratings, or submissions | Not a community resource. Section 5 |

### Possible future work

Not committed and not scheduled. Recorded so the ideas are not lost.

- A copy confirmation that survives a page change, so a copy made just before navigating is still visibly acknowledged.
- A "last updated" date per prompt, derived from the patch notes rather than from file metadata, which would let a reader tell a revised prompt from an original one.
- A skip-to-content link, so a keyboard user reaching a prompt page does not pass twenty-six focus stops before the copy button. See the accessibility section of `docs/DESIGN.md`. This is now the largest known gap in the project.
- A live region for the copy button's result, which is currently announced only through an `aria-label` change.
- Remembering the collapse state across a navigation, which is deliberately not built today because it would mean introducing browser storage. Recorded so the reason is visible if it is ever reconsidered rather than the idea simply reappearing.

---

## 24. Assumptions

Decisions taken without full information, accepted as true, and worth revisiting if any of them stops holding.

- **The library stays small.** The choice against tagging and pagination assumes the prompt count stays in the low tens. The search box (section 10b) keeps the list usable past twenty; at a few dozen, tagging and pagination need reopening.
- **The author is the only person who edits it.** There is no contributing guide, no pull request template, no review process, and no lint or test gate. A second maintainer would need all of them, because nothing currently catches a mistake except loading the page.
- **The mirror check gets run.** `tools/prompts-mirror.py` catches drift, but only when someone runs it; there is no hook. This is the weakest assumption in the project and section 19 treats it as the primary fragility.
- **Prompt text is trusted input.** `escapeHtml()` covers both quote forms, and the slug is escaped wherever it reaches an attribute. The assumption still holds at the level that matters: nothing validates a prompt file, the markdown renderer is hand-rolled rather than audited, and it is safe because every byte of content is author-written. If descriptions were ever sourced from anywhere else, that is an injection, not an edge case.
- **The Clipboard API is available.** The copy button has no fallback. It requires a secure context, which `https://` and `file://` both satisfy, but a page served over plain `http://` from a local server would fail silently, with no error shown to the reader.
- **GitHub Pages continues to serve a repository root from `main`.** The deploy process is a push. There is no configuration in the repository that captures this, so the setting exists only in the GitHub project settings and in section 17.
- **Semantic versioning is applied by judgment.** There is no release tooling and no tags. Whether a change is minor or patch is decided by the author at the time of writing the entry.
- **Readers arrive with Claude Code already installed.** No prompt explains what Claude Code is or how to install it, and the site does not either.

---

## 25. Success Criteria

The product is working when all of the following hold. These are the conditions that matter; section 28 covers what could be measured and why almost none of it is.

- **Retrieval is faster than rewriting.** The author reaches for the site rather than writing a prompt again from memory. If a prompt gets rewritten from scratch because finding it felt slower than retyping it, the site has failed at its only job.
- **A copied prompt runs correctly with no edit.** The pointer reaches the current text on `main`, and pasting it into Claude Code produces the intended result without the author first having to fix a stale line.
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

Not a framework, not a build step, not a package manifest, not a single library. Every other convenience is negotiable and this one is not. The cost is real: no syntax highlighting, no component reuse, a duplicated data file, and a markdown renderer written from scratch. The site is accepted as worse in those specific ways in exchange for still working, unchanged, in five years, with no toolchain to resurrect and nothing to update for a vulnerability. When a feature and this tenet conflict, the feature loses. The browser enforces it: the Content Security Policy blocks remote scripts and network calls, so breaking the rule fails visibly rather than shipping.

### 2. It must run from a file on disk

Opening `index.html` by double-clicking it produces the complete working site. This is stricter than "no dependencies" and it is what forces the awkward parts of the design, above all the duplication of every prompt into `js/prompts-data.js`, because browsers block `fetch()` on `file://`. That duplication is the single largest maintenance burden in the project and it is accepted deliberately. Anything requiring a server is out, including a build that emits the data file.

### 3. The markdown file is the truth

A prompt is a `.md` file. `js/prompts-data.js` is a mirror, resynced from the source and never hand-edited, and the rendered page is downstream of both. When they disagree, the `.md` file is right and the others are broken. This is what keeps adding a prompt a writing task rather than a programming one, and it is why the resync procedure is written into section 12 rather than left to memory.

### 4. Write down why, not just what

A patch note that records a change is half a patch note. The reasoning is the part that cannot be recovered by reading a diff, and it is what stops a future session from undoing a deliberate decision that looks like an oversight. This is why commit bodies and patch notes here run long, and why every rule in this document keeps its reason in a line. The reasoning lives once: a resolved discrepancy or answered question moves to the patch notes rather than staying in this document. The cost is a slower write; the benefit is never solving the same problem twice.

### 5. Documentation records, it does not overrule

An audit of this project writes down how the project works. It does not decide how the project should work and then edit the documents to match. Where the code and a document disagree, both are recorded and the conflict is put to the author, because a document holds intent that code cannot express, and code holds behaviour that a document can get wrong. Silently correcting either direction destroys information. The one exception is a purely mechanical fact, a line count or a file listing, where there is no intent to preserve.

### 6. A prompt must be safe for a stranger

Every prompt is published and may be run by someone with no context on a repository this author will never see. So no prompt instructs its reader to push, commit, or publish, and no prompt references the author's own accounts, services, or paths. Portability is not a nicety here, it is a safety property, and it is audited before any prompt goes up.

### 7. Small enough to hold in your head

A few dozen files, one of which has logic. The library stays small, the feature set stays closed, and complexity that would be reasonable at a larger scale is refused at this one. Full-text search, tagging, and analytics are sensible features this project is better off without, because the moment the project stops fitting in one reading is the moment it starts rotting.

---

## 27. Roadmap

### Current phase

**Maintenance.** The site is feature-complete against its goals. The work is the prompts and the documentation standard. New work arrives through the author's ideas list, `docs/TODO.md`: each idea is researched, written up as a proposal under "Future updates" below, and built only on the author's say-so (section 20).

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
| Self-audit against the v1.37.0 documentation standard | September 2026 | Complete (v1.70.0, against the standard as of v1.69.0) |
| Per-prompt social sharing cards | September 2026 | Complete (v1.46.0) |
| Ideas list and its Roadmap process | September 2026 | Complete (v1.61.0 to v1.62.0) |
| First ideas-list batch: five updates, two new prompts | September 2026 | Complete (v1.64.0 to v1.66.0) |
| Skip-to-content link and copy-result live region | Next session (author, 2026-09-28) | Planned |
| Search | When the library passes roughly twenty prompts | Complete (v1.104.0) |
| Next prompt added | On demand | Ongoing |

### Scoped: self-audit against the v1.37.0 documentation standard

Findings of the read-only pass on 2026-09-07, closed by the v1.70.0 audit. Where each stands:

**1. `robots.txt` is not created here.** The site is served from `/prompts/` on `azqato.github.io`, and crawlers read `robots.txt` only from the domain root, which belongs to another repository. Recorded here instead, as the standard directs.

**2. `sitemap.xml` exists.** Written by `tools/prompts-mirror.py --sync` since v1.71.0, listing the site root and every live share page (section 32).

**3. Social sharing tags shipped** in v1.46.0 (section 32a).

**4. `LICENSE.md` shipped** in v1.71.0 (section 32b).

**5. Page titles carry the brand** since v1.46.0: "<prompt> - Azqato's Prompts".

**6. Repository hygiene is met.** No ignore file, `.gitattributes` pins LF, nothing generated is left untracked (section 13).

### Scoped: per-prompt social sharing cards

Shipped in v1.46.0; section 32a is the policy it produced. The decisions taken:

**1. Path: `p/<slug>.html`**, a real file a link renderer can read, since a renderer never sees the `#/<slug>` fragment.

**2. One description:** the existing frontmatter descriptions were tightened to fit the sharing budget rather than a second field added.

**3. Reaching the person sharing:** the address bar is rewritten to the share address over http and https. A Copy link button also shipped and was removed in v1.47.0 as confusing beside Copy.

### Future updates

Proposed updates turned from the author's ideas list (section 20). Nothing here is built until the author says so. A built entry keeps its title, its `**Built in vX**` line, any decision that differed from its proposal, and its sources; the full proposal is in that release's patch note.

#### 1. Motion Design: techniques and checks from a longer launch film

**Built in v1.66.0.** Optional effects (liquid glass, goo, iris, flood, footage), a single-frame pop scan, -14 LUFS loudness, four gotchas, and key stills before the build. Downloaded sound effects allowed from a library whose license needs no attribution; music never downloaded.

Based on: a post by @twoclipping on X sharing a launch-film prompt, pasted by the author into `docs/TODO.md`.

#### 2. Motion Design: launch copy and a story drawn from the project

**Built in v1.66.0.** One neutral version of the copy.

Based on: a post by @shiri_shh on X, and the README of the `latent-spaces/brag` repository on GitHub (MIT licence), read on 2026-09-27.

#### 3. Ask for design references in the design prompts

**Built in v1.66.0.** Optional references in Brand Identity, Motion Design, and Game Setup; no link directory on the site.

Based on: posts by @himanshubuildss and @vullnetademaj on X, each listing design reference and component sites.

#### 4. New prompt: Progress Dashboard

**Built in v1.66.0.** No agent installed: Claude keeps the page itself, and asks before writing a standing rule.

Based on: a post by @Voxyz_ai on X describing a dashboard-building subagent.

#### 5. New prompt: Assumption Check

**Built in v1.66.0.** Standalone; its check also became part of the Testing Cadence (section 20).

Based on: a post by @kloss_xyz on X sharing an assumptions prompt.

#### 6. A progress dashboard for long tasks in this repository

**Built in v1.71.0, against the recommendation**, which was to defer it because tasks here rarely reach the five-step threshold. The author wanted it to test the prompt on real work. See section 20.

Based on: the Documentation prompt's rule for projects with no Progress dashboard section (v1.68.0), applied in the v1.70.0 audit.

#### 7. Launch Video: run the /brag skill directly

**Built in v1.84.0.** The author chose the full `/brag` (always `--full`) over `/brag-slim`, installed once at user scope through the plugin marketplace.

Based on: the author's ideas list, 2026-09-27, and the `latent-spaces/brag` README and `skills/brag-slim/SKILL.md`, read on 2026-09-27.

#### 8. New prompt: Design Review

**Built in v1.87.0**, at the author's request ("lets just build all of the recommended ones").

Based on: the `mengto/skills` repository on GitHub (MIT licence, Meng To), read in full on 2026-09-28 at commit `798db0a`: `ui/audit-ai-design-slop/SKILL.md`, `ui/no-ai-design-slop/SKILL.md`, and its `ARTICLE.md` pattern catalogue. Written in this site's own words; nothing is copied.

#### 9. New prompt: Video to Prompt

**Built in v1.87.0**, at the author's request.

Based on: the `mengto/skills` repository (MIT licence, Meng To), commit `798db0a`: `codex/video-to-superprompt/SKILL.md` and `codex/stitched-full-page-capture/SKILL.md`. Written in this site's own words.

#### 10. New prompt: Score to Target

**Built in v1.87.0**, at the author's request. Independent subagent judging is optional; the default runs in the session.

Based on: the `mengto/skills` repository (MIT licence, Meng To), commit `798db0a`: `workflow/workflow-score-to-target/SKILL.md` and `codex/iterate-until-verified/SKILL.md`. Written in this site's own words.

#### 11. New prompt: Animation Performance

**Built in v1.87.0**, at the author's request. The source's Codex browser and commit steps were removed.

Based on: the `mengto/skills` repository (MIT licence, Meng To), commit `798db0a`: `codex/optimize-web-animations/SKILL.md`. Written in this site's own words.

#### 12. New prompt: Landing Page

**Built in v1.87.0**, at the author's request.

Based on: the `mengto/skills` repository (MIT licence, Meng To), commit `798db0a`: `web-design/landing-page/SKILL.md` and `web-design/pricing-page/SKILL.md`. Written in this site's own words.

#### 13. Brand Identity: design quality checks

**Built in v1.87.0**, at the author's request.

Based on: the `mengto/skills` repository (MIT licence, Meng To), commit `798db0a`: `ui/no-ai-design-slop/SKILL.md`. Written in this site's own words.

#### 14. Mobile Responsive Audit: honest screenshots

**Built in v1.87.0**, at the author's request.

Based on: the `mengto/skills` repository (MIT licence, Meng To), commit `798db0a`: `workflow/workflow-progress-screenshots/SKILL.md`. Written in this site's own words.

#### 15. New prompt: Frontend References

**Built in v1.89.0**, as recommended. The author's answers: third-party sites a prompt uses directly are allowed (section 21); user scope recommended, project scope offered; 21st.dev optional. Each site carries its checked date and reuse note.

Based on: the author's ideas list, 2026-09-28, a post listing eight frontend reference sites with a suggested CLAUDE.md section; and the pages of Refero Styles, awesome-design-md, 21st.dev, Component Gallery, Kinetics, whatships, and Impeccable (and its GitHub repository), read with the web fetch tool on 2026-09-28.

#### 16. Prompt writing rules from how models work

**Built in v1.97.0**, at the author's request: the rules in section 11, an audit of every prompt, and the Prompt Writing prompt. The notes stay local (section 20, "Reference notes").

Based on: the author's ideas list, 2026-09-28 ("ingest transcription"), and the author's notes file `tools/llm-fundamentals-video-summary.md`.

#### 17. A collapsible navigation menu on phones and tablets

**Built in v1.99.0.** `docs/DESIGN.md` section 9 has the details.

Based on: the author's ideas list, 2026-09-29 ("fix mobile"), and the Mobile Responsive Audit prompt.

#### 18. Project Defaults prompt

**Built in v1.102.0**, at the author's request, who chose headings with placeholders for missing documents and the name.

Based on: the author's request, 2026-09-29, and the Documentation prompt as of v1.101.0.

#### 19. LinkedIn Audit prompt

**Built in v1.103.0**, at the author's request.

Based on: a post of seven LinkedIn prompts pasted by the author on 2026-09-29, author not named in the paste. Written in this site's own words, with the structure adapted.

#### 20. Progress Dashboard, generated from sources

**Built in v1.105.0**, at the author's request.

Based on: the author's pasted report from their Financial Education wiki project, on a hand-kept dashboard that drifted, 2026-09-29.

#### 21. Condense Docs prompt

**Built in v1.106.0**, at the author's request, kept separate from the Documentation prompt. First run on this repository in v1.107.0.

Based on: the author's idea, 2026-10-03, refined in conversation (the ledger table was the author's pick of the suggestions).

### Deferred

- **A build step for the mirror.** Deferred indefinitely: it would need a toolchain the site must not depend on. `tools/prompts-mirror.py --sync` does the job as maintenance tooling.
- **Continuous integration.** Deferred. There is nothing to build and no test to run, so a workflow would exist only to check the mirror, and that check is a script the author runs.
- **Tags for release versions.** Deferred. The patch notes already serve the purpose, and tags would be a second place to keep in sync.

### Verification checklist

Each section that describes the code, and whether it has been checked in full against the code, with the date. An update that changes an area checks that area's section in the same session and marks it here, never the whole list at once (section 20).

| Section | Covers | Status | Note |
| --- | --- | --- | --- |
| PRD 7 | Technical Requirements | Not yet |  |
| PRD 8 | Page Structure | Not yet |  |
| PRD 9 | Navigation | Not yet |  |
| PRD 10 | Copy Button Behavior | Not yet | Working on the live site per the author, 2026-09-27; the text itself not yet checked against `js/script.js` |
| PRD 10a | Prompt Collapse Behavior | Not yet |  |
| PRD 10b | Search Behavior | Verified 2026-09-29 | Written from `js/script.js` in v1.104.0 and exercised in headless Edge |
| PRD 13 | Repository Structure | Verified 2026-10-03 | Tree and count checked against `git ls-files`: 63 files, seven folders, after `condense-docs` and its share page were added in v1.106.0 |
| PRD 14 | Architecture and Flow | Not yet |  |
| PRD 15 | Code Conventions | Not yet |  |
| PRD 17 | Stack, Tooling, and Deployment | Not yet |  |
| PRD 29 | Runbook | Not yet | The mirror check and sync commands ran as documented on 2026-09-27; the rest not yet checked |
| PRD 30 | System architecture | Not yet |  |
| PRD 30 | Tech stack | Not yet |  |
| PRD 30 | Folder structure | Verified 2026-10-03 | Now a pointer to section 13's tree |
| PRD 30 | Data models | Not yet |  |
| PRD 30 | Internal data flow | Not yet |  |
| PRD 30 | State management | Not yet |  |
| PRD 30 | Third-party integrations | Not yet |  |
| PRD 30 | Performance requirements | Not yet |  |
| PRD 30 | Known technical debt | Not yet |  |
| PRD 31 | Security | Not yet |  |
| PRD 32 | Public Surface and Retired Items | Not yet |  |
| PRD 32a | Social Sharing Tags and Page Titles | Not yet | The share pages themselves are checked by `tools/prompts-mirror.py` on every run; the section's text is not |
| DESIGN 2 | Color System | Not yet |  |
| DESIGN 3 | Typography | Not yet |  |
| DESIGN 4, 4a | Layout and Spacing System | Not yet |  |
| DESIGN 5 | Component Specs | Not yet |  |
| DESIGN 7, 8 | Navigation and Footer | Not yet |  |
| DESIGN 9 | Responsive Behavior | Not yet |  |
| DESIGN 10 | Accessibility | Not yet |  |
| DESIGN 11 | CSS File Structure | Not yet |  |
| DESIGN 12, 12a | Architecture, Templates, and Component Patterns | Not yet |  |
| DESIGN 12b | Animation and Motion | Not yet |  |

---

## 28. Metrics

This section is unusual and the honesty is the point: **this project measures nothing, deliberately, and there is no instrumentation to add one without breaking a tenet.**

Analytics would mean a third-party script, which violates tenet 1 and the no-external-services rule in section 7. GitHub Pages exposes no server logs to the repository owner. The site makes no network calls of its own. So every metric below is either observed by hand or is a proxy the author reads off the repository itself.

### North star

**Prompts retrieved rather than rewritten.** The one number that would say whether the product works, and the one that cannot be instrumented without breaking the architecture. It is assessed by the author noticing, or failing to notice, that they reached for the site.

### What is actually tracked

| Metric | Method | Cadence | Target |
| --- | --- | --- | --- |
| Mirror integrity | `python tools/prompts-mirror.py`, comparing `prompts/*.md` with `js/prompts-data.js` | Every prompt edit | 100 percent, always. Any drift is a defect |
| Prompt count | `ls prompts/` | Per release | No fixed ceiling; search (section 10b) keeps the list usable. Growth is not a goal |
| Prompt Content Rules compliance | Read the prompt text against section 11 before publishing | Every new or edited prompt | Zero violations |
| Documentation drift | Open rows in the discrepancy table in section 18 | Per audit | Zero open rows |
| Release discipline | Every change has a patch note entry and a bumped version line | Per release | 100 percent |
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
| Requests | Four, all same-origin: the HTML, one stylesheet, two scripts. A visitor arriving from a pasted share link first loads the 29-line share page, which requests nothing and forwards | No additional request may be added. A fifth would mean a dependency |
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

Two constraints worth knowing before writing a check. The Content Security Policy blocks inline scripts, so a driver script has to be a real same-origin file next to a scratch copy of `index.html` rather than injected markup. And a DOM dump cannot exercise the Clipboard API, so the copy button's failure path is traced from source; see section 19.

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

Required after every edit to any file in `prompts/`. `js/prompts-data.js` holds a verbatim copy of each `.md` file, and nothing in the site enforces the match. The same script also writes and checks `sitemap.xml`, so adding, hiding, or retiring a prompt updates the sitemap in the same `--sync`.

```
python tools/prompts-mirror.py            check, exits 1 on any problem
python tools/prompts-mirror.py --sync     rewrite the data file from source
```

The check reports drift between any `.md` file and its entry, an entry with no source file, a source file with no entry, a duplicate slug, missing `title` or `description` frontmatter, and a missing fenced prompt block. Those last three matter because `parsePrompt()` falls back silently for each: a prompt missing its title ships as a page titled with its slug rather than as an error anyone would notice.

`--sync` resyncs changed entries and appends any new prompt to the end of the array, since array order is display order. It refuses to run if an entry has no source file, because deleting a prompt is a deliberate act with a documented procedure (section 12) that also touches the README and the patch notes.

Two things the script handles that a hand-rolled one usually gets wrong. **Line endings are normalized on both sides**, because the repository stores LF while `core.autocrlf` gives a Windows clone CRLF, and the `raw` values in the data file are JSON escapes that git never rewrites; comparing literally reports drift on every prompt in a fresh clone with nothing wrong. **The data file is always written with newlines untranslated**, so a one-line change does not diff as a whole file.

The same script owns the share pages in `p/`. The check also fails on a missing share page, one that differs from what its prompt would generate, a share page with no visible prompt that has not been marked retired, a title over 70 characters or a description over 200, a description that does not end on a full stop, and a title containing the site name. A title over 60 or a description over 150 is printed as a note and does not fail. `--sync` writes any share page that is missing or differs, and never deletes one: a page left behind by a removed, renamed, or hidden prompt is a public address, and retiring it is a decision taken by hand (section 32a).

Never hand-edit a `raw` string. A JSON string containing an entire markdown document is not something a person can reliably edit in place, and it is how the malformed escapes in the common-errors table below get introduced.

### Deploy

One environment. There is no staging.

```
git push origin main
```

That is the entire deploy. GitHub Pages publishes `main` from the repository root and picks up the change within a minute or two. The setting lives in the GitHub project settings, not in the repository, so nothing in the working tree reflects it. There is no workflow file, no action, and no build on the server.

**Push as soon as a change is documented and verified**, under the standing authorization in section 20, "Publishing", which also says what has to happen first and how to confirm the deploy arrived. Nothing pushes automatically: the push is a command someone runs deliberately. Separately, no prompt in the library may instruct its reader to push, a rule about the text this site publishes (section 11).

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
| Local | `file:///.../prompts/index.html` | No server. Hash routing and all relative asset paths work identically. The address bar keeps the hash route, because `file://` does not allow a path rewrite |
| Local server | `http://localhost:8000/` | `python -m http.server` from the repository root. Served at a root path rather than a subpath. The address bar rewrite runs, so this is where it is checked |
| Production | `https://azqato.github.io/prompts/` | Served over HTTPS from a subpath. Identical files |

There is no development mode, no feature flag, and no configuration file. The one piece of conditional behaviour is the address bar rewrite, which runs over http and https and is skipped on `file://`, where the browser forbids it. Every environment runs byte-identical assets, which is why a local check is a valid check.

### Environment variable reference

**None.** The project reads no environment variable, at any stage, because it has no build step and no server. There is nothing to set, nothing to configure, and no `.env` file (nor any need for `.gitignore` to exclude one).

### Common errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Page loads with "Could not load prompts" | `js/prompts-data.js` failed to parse, usually a malformed escape introduced by hand-editing a `raw` string | Open the browser console for the parse error, then resync the data file from `prompts/*.md` rather than patching the JSON |
| Page loads completely blank, no error panel | `js/prompts-data.js` did not load at all, or loaded after `js/script.js` | Check the two `<script>` tags in `index.html` are present and in that order, and that the paths resolve |
| A prompt shows old text | `js/prompts-data.js` was not resynced after the `.md` file was edited | Resync. This is the failure mode the mirror invariant exists to prevent |
| A prompt link renders the home page | The slug in the hash does not match any entry. The router falls through to home by design | Check the `slug` in `js/prompts-data.js` against the address. Note this is also what makes a retired slug harmless |
| Copy button shows "Copy failed" | Clipboard API unavailable in a non-secure context, typically a local server on a bare IP, or the write was rejected | Open the file directly over `file://`, or use `localhost` rather than an IP address |
| A script or style silently does not load | The Content Security Policy blocked it. Check the browser console for a CSP violation | Almost always correct behaviour: the policy blocks remote scripts and inline scripts on purpose. If you were adding a dependency, that is the rule working. See section 31 |
| `tools/prompts-mirror.py` reports drift on every prompt in a fresh clone | Should not happen: the script normalizes line endings. If it does, something is comparing raw bytes instead | See the line ending note above and section 13 |
| The wrong text is copied | A fenced code block appears in the prompt's description, before the `## Prompt` heading. `parsePrompt()` takes the first fence in the body | Move the example fence below the prompt block, or reword the description. Recorded in section 19 |
| Everything after the first line of a description is missing | The frontmatter `description` was wrapped across lines. The parser is line-based | Put the whole value on one line |
| `tools/prompts-mirror.py` reports a share page with no visible prompt | A prompt was removed, renamed, or hidden, and its page in `p/` is still the generated one | Rewrite it as a retired page (section 32a). Never delete it |
| A pasted prompt link previews as the site, not the prompt | The link is a hash route, `index.html#/<slug>`, which a link renderer reads as the home page | Share the `p/<slug>.html` address, which the address bar shows over https |
| Mobile header fills the whole screen | A regression of the v1.11.0 bug: `.sidebar-sticky` keeping `height: 100vh` below 1024px | Confirm `height: auto` is still set in the `max-width: 1023px` block |

### Monitoring

There is none, and there is nowhere to add it without breaking a tenet.

No logs (no server), no error reporting (no external service), no uptime alerting (GitHub Pages status is outside the author's control and is not polled). Client-side failures surface only in the reader's own browser console and in the error view.

The practical consequence: **the only monitors are the mirror check and loading the page.** Section 20 says when each runs: the mirror check after every change, the browser test before a major update.

---

## 30. Technical Reference

Section 7 states the technical constraints. This section describes the implementation those constraints produced. Where the two overlap, section 7 is the rule and this is the observation.

### System architecture

A static client-rendered site with no server component of any kind.

```
Author writes            prompts/<slug>.md          (source of truth)
        |
        | tools/prompts-mirror.py --sync, verbatim
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

Beside this flow, `tools/prompts-mirror.py` writes `p/<slug>.html` from each prompt's frontmatter. Those pages are read by link renderers and forward people to `index.html#/<slug>`; they take no part in rendering.

There is no client-server boundary because there is no server. GitHub Pages is a file host, not an application host. Nothing is rendered ahead of time, nothing is hydrated, and no state crosses a process boundary.

### Tech stack

| Layer | Technology | Version |
| --- | --- | --- |
| Markup | HTML5 | Living standard. `index.html`, 56 lines, plus twenty-two generated share pages of 29 lines each and one retired share page of 22 |
| Styling | CSS3, custom properties, Grid, Flexbox | No preprocessor, no framework, 676 lines, no `@import` |
| Logic | JavaScript, ES5-flavoured with `const` and `let` | No transpiler. Runs as written. 470 lines |
| Maintenance tooling | Python 3, standard library only | `tools/prompts-mirror.py`. Never runs in a browser, never required to build or serve |
| Content format | Markdown, a hand-parsed subset | No markdown library |
| Hosting | GitHub Pages | `main` at repository root |
| Version control | Git | Single branch, no tags |

**Dependencies: zero.** Not "few". There is no `package.json`, no lockfile, no vendored code, no CDN reference, and no external font. The complete list of things this project depends on at runtime is the browser. This is enforced rather than merely stated: the Content Security Policy in `index.html` blocks remote and inline scripts and all network connections, so adding one fails visibly. See section 31.

### Folder structure

Section 13 holds the tree and the file count.

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
| `init()` | `window.PROMPTS_DATA` | Populates `PROMPTS`, builds the sidebar, binds `hashchange` and `popstate`, routes | Non-array or empty array renders the error view. A throw from `parsePrompt()` is caught and renders the error view |
| `parsePrompt(raw, slug)` | Raw markdown, slug | A `Prompt` object | Never throws in practice. Missing frontmatter yields defaults; a missing fence yields an empty prompt string, which renders an empty code block rather than an error |
| `renderMarkdown(src)` | Description markdown | HTML string | Empty input returns an empty string. Unrecognized syntax passes through as paragraph text |
| `renderInline(text)` | One line or block | HTML string | Escapes first, then applies inline code, bold, and links. A quote in a markdown link target cannot break out of the `href` |
| `escapeHtml(str)` | Any string | Escaped string | Escapes `&`, `<`, `>`, `"`, and `'`. Entities decode back in both text content and `textContent`, so the rendered page and the copied prompt are unchanged |
| `findPrompt(slug)` | Slug | `Prompt` or `null` | Linear scan. `null` for an unknown slug |
| `buildSidebar()` | `PROMPTS` | Writes `#sidebar-nav` | Skips entries where `hidden` is true |
| `renderHome()` | `PROMPTS` | Writes `#content`, sets the document title to the site name | Skips hidden entries |
| `renderDetail(p)` | A `Prompt` | Writes `#content`, sets the title to the prompt name followed by the site name, wires the copy button and the collapse toggle | None |
| `renderError(err)` | An `Error` | Writes the status panel into `#content` | Terminal. The sidebar may be unbuilt at this point |
| `route()` | `window.location` | Renders home or a detail view, sets the active link, rewrites the address bar through `syncAddress()`, scrolls to top | An unknown slug falls through to home, silently and by design. Returns at once when the address is the one it last routed, because `hashchange` and `popstate` can both fire for one navigation |
| `currentSlug()` | The hash, or the path when there is no hash | The trimmed slug from the hash; failing a hash, the `<slug>` of a `p/<slug>.html` path; otherwise empty, for the home view | None. The path form is matched, never decoded |
| `appBase()` | The path | The folder the site is served from, whether the path names `index.html`, a share page, or the folder itself | None |
| `syncAddress(p)` | A `Prompt` or `null` | Replaces the address with the site root, `p/<slug>.html`, or for a hidden prompt `#/<slug>` | Does nothing on `file://`, where the browser forbids it, or when the address is already right |
| `wireCollapseToggle()` | The rendered DOM | Binds one click handler on `.code-block-header` | Returns early if the wrapper, header, or button is absent. The listener is on the header rather than the button, so a click on the button reaches it by bubbling and there is no second handler. A click inside `.copy-btn` returns early, so copying does not collapse the block |
| `wireCopyButton()` | The rendered DOM | Binds one click handler | Returns early if the button is absent. A missing Clipboard API or a rejected write shows "Copy failed" for 2000ms with a matching `aria-label`, sharing one code path with the success state so the two cannot drift |

### State management

There is no state management, and this is worth stating plainly rather than leaving a reader to infer it.

All application state is:

1. `PROMPTS`, a module-level array, written once at init and never mutated afterwards.
2. `window.location`, which is the single source of truth for the current view: the hash when there is one, otherwise a `p/<slug>.html` path. The router also writes it, through `history.replaceState()`, which replaces the current history entry rather than adding one.
3. `lastRouted`, the address `route()` last rendered, kept only so that a navigation firing both `hashchange` and `popstate` renders once.

There is no store, no observable, no reactivity, no component lifecycle, and no diffing. A view change is `innerHTML` replacing the whole content area. The one piece of view state that exists, whether the prompt block is collapsed, lives as a class on a single element and is discarded with it on the next render. Nothing is cached, nothing is persisted, and no browser storage API is used: `localStorage`, `sessionStorage`, IndexedDB, and cookies are all absent from the codebase. Refreshing the page rebuilds everything from scratch in a few milliseconds, which is why none of the above is missed.

The one piece of transient UI state, the copy button's "Copied!" label, lives in the DOM and in a `setTimeout` closure, and is discarded when the view changes.

### Third-party integrations

**None.** No API is called, no SDK is loaded, no font is fetched, no analytics script runs, and no service receives any data.

The only external references anywhere in the codebase are two outbound links to the author's own domain: the Support button in the sidebar (`https://azqato.github.io/support.html`) and the footer credit (`https://azqato.github.io`). Both are ordinary anchors. The Support button carries `rel="noopener noreferrer"` with its `target="_blank"`; the footer link opens in the same tab. Neither transmits anything beyond a normal navigation.

The favicon is an inline SVG data URI, so even it is not a request.

### Performance requirements

See the table in section 28. In short: four same-origin requests, roughly 200 KB dominated by `js/prompts-data.js`, zero runtime network calls, and a render that is one synchronous pass. The binding limit is that no fifth request may be added, because that would mean a dependency. A share page is a separate document a visitor passes through, not a request the page makes, and it requests nothing itself.

### Known technical debt

Recorded honestly, with what the correct fix would be and why it has not been done.

| Debt | Consequence | Correct fix | Why not |
| --- | --- | --- | --- |
| `js/prompts-data.js` duplicates every prompt | The mirror can drift, serving stale text from an authoritative-looking source | Generate the file in a build step | A build step is a dependency, which breaks tenets 1 and 2. This debt is the direct price of the architecture and is permanent. Mitigated rather than removed by `tools/prompts-mirror.py` |
| `parsePrompt()` takes the first fence in the body | A fenced example in a description would be published as the prompt text | Match on the fence following the `## Prompt` heading specifically | No prompt has hit it yet. It is a trap rather than a bug |
| The frontmatter parser is line-based | A wrapped `description` value drops everything after the first line, with no error | Parse folded values, or fail loudly on a continuation line | Every description is currently one line. Failing loudly would be the cheaper half of the fix |
| Share pages forward with a meta refresh | A visitor arriving from a pasted link loads two documents rather than one | A server-side redirect | GitHub Pages offers none, and a script would need the Content Security Policy relaxed. A 29-line page with no subresources is the cheapest honest way to give a hash-routed site link previews |
| No test suite, no linter, no CI | Only the mirror check and loading the page catch anything | Any one of them | Each is a dependency and a toolchain. Accepted deliberately; section 20 sets when the manual checks run |
| Version numbers live in two places | The `docs/PRD.md` header and `docs/PATCHNOTES.md` can disagree | Single source, generated | No generation step exists. Kept in sync by the procedure in section 20 |

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
| Attribute interpolation | A quote in a markdown link target could break out of an `href` | `escapeHtml()` escapes both quote forms, and the slug is escaped wherever it reaches `href` or `data-slug` |
| Remote or inline script injection | Any script reaching the page would run with full access | The Content Security Policy blocks both, verified enforced. This is defence in depth rather than the primary control, since there is no injection path |
| Hash-driven routing | The URL fragment is attacker-controllable in a shared link | The hash is only ever compared against known slugs and never interpolated into the DOM. An unknown value renders the home view. No injection path. A slug from a `p/<slug>.html` path is treated the same way: compared, never interpolated, never decoded |
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

The share pages in `p/` carry a stricter policy of their own, `default-src 'none'; base-uri 'none'; form-action 'none'`, because they load nothing at all: no script, no style, no image. A meta refresh is a navigation rather than a fetch, so the policy does not block it.

`frame-ancestors` is deliberately absent. It is ignored when delivered in a meta tag, so including it would imply a protection that is not actually there. Clickjacking is not a meaningful risk for a page with no state-changing action, but if it ever needed addressing, a meta CSP could not do it.

The policy is verified enforced from `file://`, where `'self'` behaves unusually in some browsers: an injected inline script and a remote CDN script are both blocked, while the favicon, the two same-directory scripts, the stylesheet, and routing still work.

### Dependency policy

**There are no dependencies, so there is nothing to monitor.** This is the most consequential security property of the project and it is a direct consequence of tenet 1. The Content Security Policy also enforces it.

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
| `p/<slug>.html` | **Yes**. The address the address bar shows over https, so it ends up pasted into chats and posts, held by people outside the project | Never delete. Retire it as section 32a describes, forwarding in one hop to the prompt's new address or to the site root |
| `index.html#/<slug>` | **No.** A fragment, resolved entirely client-side against data derived from source filenames. Not a served address | Prune outright. The router renders home for an unrecognized slug |
| `prompts/*.md` | **No.** Source. Never requested by the deployed page, and reachable on GitHub Pages only as a raw file nothing links to | Plain delete |
| `docs/*.md` | **No.** Source. Not rendered by the site | Plain delete, though these are the project's own documentation and are not casually removed |
| `tools/prompts-mirror.py` | **No.** Maintenance tooling. Never requested by the deployed page and never loaded by a browser | Plain delete. The site is unchanged without it |
| `README.md` | **No** as an address, though it is the repository's public front door on GitHub | Never remove |
| `sitemap.xml` | **Yes**. Served at `/prompts/sitemap.xml` for crawlers. It lists the site root and each live share page, all under its own path, which is the scope a sitemap there may cover | Regenerated by `--sync`, never hand-edited. Removing it would need no redirect, since nothing links to it, but it would stop the share pages being listed |
| `LICENSE.md` | **No** as a page, though it is served and GitHub reads it to detect the licence | Never move it from the root. See 32b |
| `dashboard/index.html` | **Yes**, at `/prompts/dashboard/`. A working page, `noindex`, not in the sitemap | Remove only with the `CLAUDE.md` rule; it is linked from nowhere, so no redirect |
| `CLAUDE.md`, `.gitattributes` | **No.** Repository configuration, never requested by the page | Plain delete, with the rule each carries recorded first |

The asset paths are the subtle case. They are public in the sense that the deployed page requests them, so renaming one without updating `index.html` breaks the live site. But no external party holds them, so the compatibility obligation is satisfied by editing the reference in the same commit rather than by a permanent redirect.

### The redirect mechanism

`js/script.js` defines a `REDIRECTS` map consulted by `route()`, mapping a retired slug to a current one and guarded on the target existing. **It is deliberately empty.**

Prompt slugs are not a public surface, so they get no entry (the three it once held are in the Retired items table). The mechanism is kept, at a cost of one property lookup per navigation, so that a genuine public address can be retired without rebuilding it under time pressure.

Any entry added to it is permanent, never chains (a redirect resolves to a real target in one hop), and is never reused to point at different content, because a reused address silently serves the wrong thing, which is worse than a broken link.

There is no server-side rewrite capability. GitHub Pages project sites offer no redirect configuration, so a client-side map in the router is the only mechanism available for a route. The share pages are real files, and a retired one forwards with its own meta refresh, so it needs no entry in the map.

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
| `prompts/iphone-ipad-simulator.md` | v1.56.0 | Renamed to `prompts/ios-simulator.md`, title iOS Simulator. Its share page, `p/iphone-ipad-simulator.html`, was public from v1.54.0 and is retired, forwarding to `index.html#/ios-simulator` |

Every deleted file remains recoverable from git history. None of these removals required a redirect under the current policy, and the two that were given one in v1.23.0 had it removed in v1.24.0 when the policy was corrected.

Historical records are not rewritten when something is removed. Patch notes and version history rows describing a deleted prompt, or describing redirects that no longer exist, stay exactly as they are, because they record what happened at the time rather than describing the current state.

---

## 32a. Social Sharing Tags and Page Titles

This is the project's own policy, which the Documentation prompt asks a project that serves a site to state.

### The problem it solves

A link renderer, the thing that builds a preview card when a link is pasted into a chat app or a post, requests the URL without its fragment, because the part after `#` is never sent to a server, and it runs no JavaScript. Every route on this site is a fragment, so to a renderer every prompt link is the same `index.html`. Observed in Discord on 2026-09-23: a link to the Prompt Audit prompt previewed as the site's title over the site's description. No set of tags in `index.html` can fix that, because `index.html` cannot know which prompt was linked.

### Share pages

Every visible prompt has a share page at `p/<slug>.html`, a real file at a real path, which a renderer can fetch and read. It carries that prompt's tags in its head and a `<meta http-equiv="refresh">` that forwards a person to `index.html#/<slug>`, plus a plain link to the same place for any client that ignores refresh. A renderer reads the tags and stops. A person lands on the prompt a moment later.

- **Generated, never written.** `tools/prompts-mirror.py --sync` writes each page from the prompt's frontmatter, and the check compares every page byte for byte against what it would generate. A hand edit fails the check. To change a page, change the prompt's `title` or `description`, or `share_page()` in the script, and resync.
- **Meta refresh rather than script.** The pages carry the Content Security Policy `default-src 'none'; base-uri 'none'; form-action 'none'`, which forbids script outright, and a refresh also works from `file://`.
- **A plain-text copy for agents.** Every share page links to the prompt's raw Markdown at `https://raw.githubusercontent.com/Azqato/prompts/main/prompts/<slug>.md`, twice: a `<link rel="alternate" type="text/markdown">` in the head, right after the meta description, and a visible body paragraph with the URL written out in full. The body carries, for every prompt:

  1. The prompt's title, linking to it on the site, and its frontmatter description, so an agent knows what the prompt is before its second fetch; fetch tools drop the head, where the description otherwise lives.
  2. "AI agents: this page only links to the prompt. Fetch the full prompt as plain Markdown at <URL>. Read it in full and word for word; if your fetch tool summarizes or shortens pages, get the raw text another way, such as curl. The prompt is the code block under "## Prompt"; the text above it describes it for people. Do what the person asked you to do with it, and ask before running it if they have not said to."

  Each sentence answers a way the handoff could fail: acting on the link page itself, a fetch tool that summarizes a long prompt through a small model (Claude Code's does), treating the human description as part of the instructions, and running a prompt the person only asked to have summarized (section 10). One link only: the raw URL. A second, `github.com` fallback was declined by the author to keep the page to one address. The raw link is needed because an AI agent fetching a share page runs no JavaScript and never follows the `#/` route, and Pages does not serve the `.md` files (`/prompts/prompts/<slug>.md` is a 404). Fetch tools that convert a page to text drop head tags, which is why the body line is needed as well. The URL uses `main` so it always serves the latest version, and is built from `RAW_URL` in the script. A person in a browser is forwarded as usual.
- **No page for a hidden prompt.** A prompt with `hidden: true` is off the navigation deliberately, so it is not given a public address. It is shared, if at all, by its hash route. No prompt is hidden today, so the exclusion list is empty.

### The tags

Six on every share page, and the same six on `index.html` describing the site.

| Tag | Share page | `index.html` |
| --- | --- | --- |
| `og:title` | The prompt's `title`, without the site name | "Claude Code Prompts", the home page heading |
| `og:description` | The prompt's frontmatter `description` | The site's meta description |
| `og:url` | `https://azqato.github.io/prompts/p/<slug>.html`, unique per prompt | `https://azqato.github.io/prompts/` |
| `og:type` | `website` | `website` |
| `og:site_name` | "Azqato's Prompts" | "Azqato's Prompts" |
| `twitter:card` | `summary` | `summary` |

No image is declared, so `twitter:card` is `summary` and there is no `og:image`. The canonical address comes from section 17 and is written into `tools/prompts-mirror.py` and `js/script.js` as a constant, because `og:url` has to be absolute and nothing on a static site can derive it.

**One description, not two.** The frontmatter `description` serves the home card, the share page's meta description, and `og:description`. A separate short field for sharing was considered and rejected, because two descriptions of the same prompt would drift, and the tighter one is the better card text anyway. Every new prompt's description is written to fit; each one's length is recorded in its release's patch note.

**Budgets**, enforced by the mirror check:

| Field | Target, reported as a note | Ceiling, fails the check | Also fails |
| --- | --- | --- | --- |
| `title` | 60 characters | 70 | Containing the site name |
| `description` | 150 characters | 200 | Not ending on a full stop |

The description is written as complete sentences stating what the prompt does, in the plain register section 11 already requires. It ends on a full stop so a renderer never has to cut it mid-thought.

### Page titles

`document.title` is set on every route. The home view is "Azqato's Prompts". A prompt page is the prompt's title, a spaced hyphen, and the site name, for example "Prompt Audit - Azqato's Prompts". The distinct part comes first, so it survives a narrow tab, and the brand makes a bookmark or a history entry recognisable months later. The share pages carry the same form in their `<title>`, since a renderer that ignores Open Graph falls back to it. `og:title` alone leaves the site name off, because `og:site_name` already supplies it and a renderer that shows both would repeat it.

### Getting the share address to the person sharing

A share page is only useful if it is the address that gets pasted, and people paste what is in the address bar. So over http and https, after rendering, the router replaces the address with the view's share address using `history.replaceState()`: the site root for home, `p/<slug>.html` for a prompt, `#/<slug>` for a hidden prompt, and the site root for an unknown slug. It replaces rather than pushes, so the back button behaves exactly as before. On `file://` the browser forbids the rewrite, and the hash route stays, which costs nothing, since a `file://` address is useless to anyone else anyway.

Reloading a rewritten address loads the share page, which forwards to the prompt, so every address the bar can show is one that works. Hash links inside the site keep working from a rewritten address, because a click on `#/<slug>` changes only the fragment and the router reads the hash first.

There is no Copy link button: one beside Copy made the primary action less obvious, and the address bar already carries the same link. Weigh that if the idea comes back.

### Retiring a share page

A share page is a public address from the moment it is published, because it is the address people are given. Section 32 applies in full: it is never deleted, never chains, and is never reused for a different prompt.

When a prompt is renamed, removed, or hidden, `--sync` leaves the old page alone and the check fails, naming it. The fix is to rewrite it by hand as a retired page:

- it carries the marker `<!-- retired: <what happened and in which version> -->`, which is what the check looks for;
- it forwards in one hop, by meta refresh and a plain link, straight to where the reader should land: `index.html#/<new-slug>` for a rename, the site root for a removal, and `index.html#/<slug>` for a hidden prompt;
- it keeps the same Content Security Policy, and its tags describe where it lands rather than what used to be there.

If a retired page's destination is itself later renamed or removed, the retired page is rewritten to point at the new destination directly, so no chain ever forms. The marker is what separates a deliberate retirement from a page that was forgotten, which is why the check will not accept an orphan without it.

### Verifying

The mirror check covers the page content and the budgets. What it cannot cover is how a given renderer treats the result, which varies by service and changes without notice. After a change to the tags, paste one prompt's share address and the home address into a chat app and look at both cards.

---

## 32b. Licensing

`LICENSE.md` sits at the repository root, beside the README, where GitHub and other tools look for a licence.

**Posture: all rights reserved, source-available, with one grant.** The Documentation prompt's default grants nothing. This project already had a rule of its own, in section 11: prompts "are shared publicly and may be reused by anyone", and the FAQ tells readers to adapt them. Under the prompt's own rule that an existing rule wins over a default, the licence grants exactly that: anyone may copy a prompt, adapt it, and run it on their own projects, personal or commercial, without asking and without attribution. It does not grant republishing the prompts or the collection as a library, product, course, or dataset, and it grants nothing over the site's code, design, or documentation.

The rest follows the default:

- **AI and search.** Crawling, indexing, retrieval, quoting, summarising, linking, and citing are permitted, with attribution requested and not required. Substitution, reproducing the work in place of visiting it, is not. Training use is routed to the permission path and is not usually refused.
- **No waiver.** Not acting against a use is not a licence, a precedent, or a waiver; a waiver must be written, signed, and scoped.
- **Permission** is asked for on the repository's public issue tracker, `https://github.com/Azqato/prompts/issues`, so what has been permitted is on record.
- **Platform terms.** GitHub's terms give its users their own rights over a public repository; the licence says they operate independently and are not enlarged by it.
- **Third-party material** is not claimed, and rights that cannot be restricted, such as fair use, are not restricted.
- **No warranty**, with a note specific to this site: the prompts direct an assistant to change files, so running one is the reader's decision and risk.

**The machine-readable layer.** The default pairs the licence with an open `robots.txt` carrying a comment that says the openness is deliberate. This site cannot carry one: it is served from `/prompts/` on `azqato.github.io`, and crawlers read `robots.txt` only from the domain root, which belongs to the author's main site rather than to this repository (section 27, self-audit finding 1). `LICENSE.md` names itself as authoritative over any robots file or sitemap, so there is no contradiction for a crawler to resolve.

---

## 33. Documentation Audit Process

How the documentation in this repository is produced and maintained, and how it should be handled from here.

### The four-file rule

Documentation consolidates into exactly four files, plus the author's ideas list:

```
/
├── README.md          Never inside /docs
└── docs/
    ├── PRD.md
    ├── DESIGN.md
    ├── PATCHNOTES.md
    └── TODO.md        Ideas only. Never merged, never moved
```

`docs/TODO.md` is not documentation. It is the author's list of ideas, kept as its own file and emptied into the Roadmap on request (section 20). Beyond it, a new documentation file is not created. If something needs saying, it becomes a section of the PRD. This is the rule the project's own Documentation prompt enforces on other projects, and it is applied here.

The division of labour: the **README** is the public front door for a general reader; **PRD.md** is the single authoritative reference for everything else, including all setup and technical detail; **DESIGN.md** is the visual specification; **PATCHNOTES.md** is the changelog.

### Running an audit

An audit is run by pasting the Documentation prompt from this site into Claude Code against this repository. It is the project's own tooling turned on itself, and it is the intended way to keep these documents current. The last full run was v1.70.0, on 2026-09-27.

**It runs in one pass.** It asks nothing during the run: it applies the prompt's defaults, and where there is none it takes the most conservative option, keeping existing text, marking the point as a discrepancy or uncertain, and creating, moving, or deleting nothing hard to undo. Every question it raises is collected into a numbered Questions list at the end of its summary, each with the default applied meanwhile and where it is recorded, so the author answers by number afterwards. Ideas in `docs/TODO.md` are listed there and left untouched; they become Roadmap updates only on a yes, through the process in section 20. Where `CLAUDE.md` has no Progress dashboard section, the audit adds a Future updates entry proposing one rather than asking; this repository's is entry 6 in section 27.

The prompt's own process, in short: survey the codebase rather than reading every source file, read every existing document in full, then check the docs in three passes (the rules and structure this prompt requires, quick factual checks such as the folder tree and the newest patch notes entry, and the sections touched by changes since the last audit), and only then write. Steps 1 through 3 are strictly read-only. Writing begins at step 4 and touches only the files the prompt names. Sections not yet checked in full against the code go on a verification checklist in the Roadmap, which later updates tick off as they touch each area, so the audit costs about the same on a large project as on a small one; a full crawl of a 150-file project was estimated at 400,000 to 700,000 tokens.

**Condensing is a separate pass.** The Condense Docs prompt shortens the docs without changing what they say: every fact in one home, history in the patch notes, and a ledger proving nothing was lost. First run here in v1.107.0.

### Rules that govern the writing

These are the standards the audit applies, restated here so they bind the documents even when nobody is running the prompt.

**Merge, do not overwrite.** Documentation holds intent, decisions, and rationale that cannot be reconstructed from code. Where a document already covers a topic and the code agrees, the text is left alone. Where they conflict, the original text is kept, the observed reality is recorded next to it, and the conflict goes into the table in section 18 for the author to resolve. Code can be wrong just as easily as a document can be stale. This is tenet 5.

**The exception is mechanical fact.** A line count, a file listing, a token name, a breakpoint value: these carry no intent, so a stale one is corrected in place and noted in the patch notes rather than being flagged as a discrepancy. The test is whether a person could have meant it. Nobody means a line count.

**Every policy is a default that yields.** Where this project already states a rule, that rule wins and the default is discarded, with the difference noted rather than silently resolved.

**Read, do not infer.** A guess presented as a fact is a failure. Where something is uncertain, the uncertainty is written into the document, because a confident sentence outlives the session that produced it.

**Every fact kept once, in its home.** Nothing is dropped, and nothing is said twice: a section that needs a fact from elsewhere links to it rather than restating it, because the copy nobody is editing goes stale. Thorough means more facts, not more words around the same facts. Docs describe the present; how something used to be belongs in the patch notes, except a reason, kept in a line, without which someone would undo a rule. No marketing language and no filler.

**Numbers are not renumbered.** Sections are appended rather than inserted, and the version history stays last. Patch notes and `tools/prompts-mirror.py` cite these sections by number, and renumbering would invalidate every one of those references for no gain.

Where new material genuinely belongs beside an existing section rather than at the end, it takes a letter suffix: `10a` follows section 10 and nothing after it moves. `docs/DESIGN.md` uses it for sections 4a, 12a, 12b, and 12c, and this document for 10a, 10b, 32a, and 32b. Prefer appending. Use a suffix only when placement carries real meaning, which it does when a reader would look for the material next to a specific section and nowhere else.

**Historical records are never rewritten.** A patch note describes what happened on the day it was written. It is not updated when the thing it describes is later changed or removed.

### After any documentation change

1. Update `docs/PATCHNOTES.md` with the next semantic version and today's date, in `YYYY-MM-DD`.
2. Update the `**Version:**` field in this document's header. `docs/DESIGN.md` carries its own independent document version, which moves only when that document changes, with a row in its own version history.
3. Verify as section 20 says: the mirror check always, and an assumption check and a browser test from disk only right before a major update ships. A change confined to `/docs`, the README, or prompt text is minor and needs neither.

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

### Is there search?

Yes. A search box at the top of the prompt list filters by title and description as you type, and Enter opens the first match. On a phone it is inside the Prompts menu.

### How is this different from a prompt marketplace?

A marketplace optimizes for volume, discovery, and rating across thousands of contributed prompts. This is the opposite: a handful of prompts, each one used repeatedly by the person who wrote it, kept because it earned its place. There is nothing to browse and nothing to compare. If you want breadth, this is the wrong tool.

### How is it different from just saving prompts in a notes app?

Mostly that it is public, addressable, and structured. Each prompt has a permanent link you can drop into a project's notes. The pages are identical in shape, so reading is fast. And because it is a git repository, every revision to every prompt has a recorded reason.

### What does it not do?

It does not run prompts, generate them, edit them for you, or connect to Claude Code in any way. It is a reference page with a copy button. It also has no full-text search, no tags, no ratings, no comments, and no user accounts, all deliberately.

### Why not more prompts?

Because a prompt only gets added once it has proved worth keeping. Five have been removed since launch: three superseded, and two absorbed into a more capable prompt (section 32). Shrinking the library is treated as progress.

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

Nowhere ambitious, deliberately. The site is feature-complete; section 27 holds what is planned and proposed. The active work is on the prompts and on the documentation standard. Growth in prompt count is explicitly not a goal.

---

## 36. Version History

This document's version is the site's, in the header. Every release, with its date and reasoning, is in [`docs/PATCHNOTES.md`](PATCHNOTES.md).
