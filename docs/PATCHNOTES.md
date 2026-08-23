# PATCHNOTES.md — Prompts

All notable changes to this project are documented here. Entries are listed in reverse chronological order. Each version entry includes the version number, date, and a summary of what changed.

---

## v1.15.0 — 2026-08-23

### Added

- `prompts/project-onboarding.md`: Ninth prompt, "Project Onboarding". Puts a model through an eight-phase, read-only intake of an unfamiliar project before it is allowed to change anything: structure map, identity and purpose, a full read of every documentation file, technical foundation (dependencies, scripts, build, test, deploy), architecture traced from real entry points rather than from the docs, conventions derived from the code itself, a documentation-versus-reality cross-check, and an explicit risks-and-unknowns pass. Phases 1 through 8 forbid all writes, installs, and state-changing version control commands.
- The deliverable is not a chat briefing. Everything established is merged into `PRD.md`, the single file the prompt is permitted to write, so the understanding survives the session. The merge is additive: it preserves intent and rationale that cannot be reconstructed from code, matches the PRD's existing heading structure and tone, and where findings contradict the PRD it keeps both and marks the conflict for a human to resolve rather than silently correcting the document from code. No other file is touched, including the README and these patch notes; errors found elsewhere are reported instead.
- `js/prompts-data.js`: Regenerated to include `project-onboarding`.

### Changed

- `README.md`: Added `prompts/project-onboarding.md` to the Files table and the file structure tree.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.14.0 — 2026-07-06

### Changed

- `prompts/github-wiki-setup.md`: Renamed the "Changelog" wiki page to "Patch Notes" (`Patch-Notes.md`) throughout the prompt's frontmatter description, on-page description, and prompt text, to match this site's own terminology (`docs/PATCHNOTES.md`) rather than the more generic "Changelog" label.
- `js/prompts-data.js`: Regenerated to mirror the renamed page.

---

## v1.13.0 — 2026-07-06

### Changed

- `prompts/github-wiki-setup.md`: Reworked into "GitHub Wiki Sync" (title and description regenerated to match). Added an update mode: if the wiki repo already exists, the prompt pulls the current pages, diffs them against the README, PRD, PATCHNOTES, DESIGN, and any other project docs, and summarizes outdated sections, missing features, stale links, and content drift before editing anything. Page creation is no longer a fixed set beyond Home, Product Overview, and Changelog; the prompt now uses judgment on wiki information architecture, creating pages like FAQ, Roadmap, Architecture, Getting Started, Troubleshooting, or API Reference wherever a topic is distinct and cohesive. Added a step to create or keep a `_Sidebar.md` page in sync with the full current page structure.
- `js/prompts-data.js`: Regenerated to mirror the reworked `github-wiki-setup.md`.
- Also caught and fixed two more em dashes in the prompt's body text, in the Product Overview and Changelog descriptions, that were missed in the previous pass, replacing both with parentheses per the site's em dash prohibition.
- `README.md`: Updated the `github-wiki-setup.md` Files table description to match the reworked prompt.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.12.0 — 2026-07-06

### Added

- `prompts/github-wiki-setup.md`: Eighth prompt, "GitHub Wiki Setup". Reviews every documentation markdown file in a project, then sets up a GitHub wiki sourced from them. Checks first whether the wiki repo is initialized (GitHub only creates it after one manual page is added via the web UI) and stops to ask if it isn't. Curates, rather than dumps verbatim, content into a Home page (overview plus table of contents), a Product Overview page (stable current-state PRD sections), a Changelog page (condensed patch notes), and any other page mapping to a distinct PRD section. Rewrites internal/planning language for a public audience and drops internal-only notes.
- `js/prompts-data.js`: Regenerated to include `github-wiki-setup`.

### Changed

- `README.md`: Added `prompts/github-wiki-setup.md` to the Files table and file structure tree.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.11.0 — 2026-07-05

### Fixed

- `css/style.css`: Ran the Mobile Audit prompt against the live site (headless Chrome via CDP, `scrollWidth`/`clientWidth`/`getBoundingClientRect()` measurements at 375–1920px, not screenshots) and found the mobile/tablet header (< 1024px) was badly broken. Root cause: `.sidebar-sticky` sets `height: 100vh` for the desktop vertical sidebar, and the `@media (max-width: 1023px)` block that converts it into a horizontal header never reset that height, so the header stayed full-viewport-tall with its logo/nav/support button vertically centered inside — pushing all page content roughly 1200px below the fold on a typical mobile screen. Added `height: auto` to `.sidebar-sticky` in that media query.
- `css/style.css`: Secondary bug in the same header: `.sidebar-nav` shared its row with `.sidebar-logo` instead of dropping to its own line, squeezing the 5 nav links into a ~150px-wide column that stacked one link per row instead of wrapping across the full width (the existing `margin-bottom` on `.sidebar-logo` already implied the intended layout was logo-then-nav-below). Added `flex-basis: 100%` to `.sidebar-nav` in the same media query so it wraps full-width beneath the logo.
- No page-level horizontal overflow, `overflow` shorthand conflicts, bare `1fr` grid overflow, flex `min-width: auto` overflow, or margin/gap double-spacing were found anywhere else at any of the seven audited breakpoints across the home page and all seven prompt detail pages.

---

## v1.10.0 — 2026-07-05

### Added

- `prompts/mobile-responsive-audit.md`: Seventh prompt, "Mobile Audit". Audits every page of a site at seven fixed breakpoints (375px to 1920px) for horizontal overflow, container overflow, unwrapped toolbars, modal sizing, and clipped text. Targets four specific CSS bug patterns: the `overflow` shorthand canceling `overflow-x`, bare `1fr` grid tracks forcing page overflow from wide content, flexbox children ignoring their parent's width due to default `min-width: auto`, and doubled spacing from `margin` stacking with a flex/grid `gap`. Verifies fixes by injecting a debug script to read `scrollWidth`/`clientWidth` and bounding rectangles rather than relying on screenshots, since headless browsers enforce a minimum viewport width. Flags any fix that changes content presentation for a design decision before implementation, and ends by updating the project's existing changelog and planning docs.
- `js/prompts-data.js`: Regenerated to include `mobile-responsive-audit`.

### Changed

- `README.md`: Added `prompts/mobile-responsive-audit.md` to the Files table and file structure tree.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.9.0 — 2026-06-27

### Added

- `js/script.js`: Support for an optional `hidden` frontmatter flag on prompts. `parsePrompt` reads `hidden` (true/yes/1), and `buildSidebar` and `renderHome` skip any prompt where it is set. `findPrompt` and routing are unchanged, so hidden prompts stay reachable by direct link (`index.html#/<slug>`).

### Changed

- `prompts/consolidate-documents.md`, `prompts/docs-folder-audit.md`, `prompts/documentation-audit.md`: Added `hidden: true` to the frontmatter. These three prompts are retired from the sidebar and home list but kept on the backend; existing direct links still resolve. The newer Documentation prompt supersedes them in the navigation.
- `js/prompts-data.js`: Regenerated to mirror the three `hidden: true` frontmatter additions.
- `README.md`: Noted which prompts are hidden from navigation and still reachable by direct link.
- `docs/PRD.md`: Documented the `hidden` frontmatter flag in the navigation and prompt markdown sections, and recorded the release in the version history.
- `docs/DESIGN.md`: Documented the optional `hidden: true` key in the prompt markdown template and version history.

---

## v1.8.0 — 2026-06-27

### Added

- `prompts/documentation.md`: Sixth prompt. The most comprehensive of the documentation prompts. Crawls the entire codebase first, then consolidates all documentation into four core files (README.md at the root; PRD.md, DESIGN.md, and PATCHNOTES.md in `/docs`), creates any missing files, and enforces the correct folder structure. Folds the full depth of a larger doc suite into a single PRD with required sections for Tenets, Roadmap, Metrics, Runbook, Technical Requirements, Security, a Press Release, and an FAQ, so the project can be understood from `/docs` alone without reading code.
- `js/prompts-data.js`: Regenerated to include `documentation`.

### Changed

- `README.md`: Added `prompts/documentation.md` to the Files table and file structure tree.
- `docs/PRD.md`: Added an "Adding Prompts" process note documenting the standing workflow for adding a new prompt and keeping documentation in sync, and recorded this release in the version history.

---

## v1.7.0 — 2026-06-14

### Added

- `prompts/docs-folder-audit.md`: Fifth prompt. Audits every document in `/docs` against the current codebase. Crawls all files first to build a complete picture of the project, then reviews each doc in `/docs` for outdated, missing, or inaccurate content and rewrites it. Ends with a per-file summary of what changed and why.
- `js/prompts-data.js`: Regenerated to include `docs-folder-audit`.

### Changed

- `README.md`: Added `prompts/docs-folder-audit.md` to the Files table and file structure tree.

---

## v1.6.0 — 2026-06-13

### Changed

- `style.css` → `css/style.css`: Moved stylesheet into a dedicated `css/` subfolder.
- `prompts-data.js` → `js/prompts-data.js`: Moved prompt data file into a dedicated `js/` subfolder.
- `script.js` → `js/script.js`: Moved main script into the `js/` subfolder.
- `index.html`: Updated `<link>` and `<script>` references to reflect new asset paths (`css/style.css`, `js/prompts-data.js`, `js/script.js`).
- `README.md`: Updated Files table and file structure tree to reflect new `css/` and `js/` folder layout.
- `docs/DESIGN.md`: Updated shell template, CSS file structure heading, and version history.

---

## v1.5.0 — 2026-06-13

### Added

- `prompts/add-prompt.md`: Fourth prompt. A meta-prompt for adding new prompts to the site. Accepts a raw prompt text and instructs Claude Code to generate the title and one-line description, create the markdown file in `prompts/`, mirror it into `prompts-data.js`, update the Files table in `README.md`, and add a version entry to `docs/PATCHNOTES.md`.
- `prompts-data.js`: Regenerated to include `add-prompt`.

### Changed

- `README.md`: Added `prompts/add-prompt.md` to the Files table and file structure tree.

---

## v1.4.0 — 2026-06-13

### Added

- `prompts/consolidate-documents.md`: Third prompt. Consolidates all project documentation into four core files: README.md at the root, and PRD.md, DESIGN.md, and PATCHNOTES.md inside `/docs`. Creates any missing files with required sections. Enforces the correct folder structure and moves misplaced files. A leaner alternative to the Documentation Audit prompt, targeting four documents instead of eleven.
- `prompts-data.js`: Regenerated to include `consolidate-documents`.

### Changed

- `README.md`: Added `prompts/consolidate-documents.md` to the Files table and file structure tree.

---

## v1.3.0 — 2026-06-13

### Changed

- `index.html`: Sidebar logo updated from "Prompts." to "Azqato's Prompts." Added Support button to the bottom of the sidebar, linking to `https://azqato.github.io/support.html` in a new tab.
- `script.js`: Homepage h1 updated from "Prompts." to "Claude Code Prompts." (teal dot preserved). Browser tab title updated to "Azqato's Prompts" on home view. Prompt pages now set the tab title to just the prompt name, with no site suffix.
- `style.css`: `.sidebar-sticky` changed from `max-height: 100vh` to `height: 100vh` with `display: flex; flex-direction: column` so the Support button pins to the bottom via `margin-top: auto`. `.sidebar-nav` gains `flex: 1` to fill available space. Added `.sidebar-support` and `.support-btn` styles with hover state matching the site's teal accent. Mobile breakpoint updated to flow the support button inline with nav links.
- `docs/DESIGN.md`: Updated sidebar spec, navigation spec (support button added), hero section spec, shell template, and version history.
- `docs/PRD.md`: Updated navigation section to document the support button.
- `README.md`: Project title updated to "Azqato's Prompts".

---

## v1.2.0 — 2026-06-13

### Changed

- `prompts/em-dash-audit.md`: Removed "Finally, push everything to GitHub." from the prompt text. Prompts are shared publicly and must not instruct users to push to any remote repository. Rewrote the closing instruction to: "After making these changes, ensure the patch notes and documentation files are all up to date describing the changes you just made." Updated the frontmatter description and on-page description paragraph to remove all mention of pushing to GitHub.
- `prompts-data.js`: Regenerated to mirror the updated `em-dash-audit.md`.
- `docs/PRD.md`: Added a Prompt Content Rules section to the Writing Style rules. Documents that prompts must not include GitHub push instructions or any account-specific actions, and requires this to be audited before any new prompt is published.

---

## v1.1.0 — 2026-06-13

### Added

- `prompts/documentation-audit.md`: Second prompt. Runs a full documentation audit on any project: reads all source files and existing docs, then creates or updates the complete suite of eleven documents (README, PRD, TRD, DESIGN, PATCHNOTES, PRFAQ, TENETS, METRICS, ROADMAP, SECURITY, RUNBOOK) to their required specifications. Also enforces the correct folder structure, moving any misplaced files into `/docs`.

### Removed

- `first prompt example.txt.txt`: Source text for the first prompt. Content is now canonical in `prompts/em-dash-audit.md`. No longer needed.
- `message.txt`: Source text for the documentation audit prompt. Content is now canonical in `prompts/documentation-audit.md`. No longer needed.

### Changed

- `prompts-data.js`: Regenerated to include both `em-dash-audit` and `documentation-audit`.
- `docs/PATCHNOTES.md`: Corrected v1.0.0 design decisions note about footer (period is not teal; it inherits the muted text color).

---

## v1.0.0 — 2026-06-13

**Initial release.**

### Added

- `index.html`: Single-page shell (sidebar, content area, footer). Renders the home view and every prompt view via hash-based routing. No per-prompt HTML files.
- `prompts/em-dash-audit.md`: First prompt, authored in markdown. Documents the full em dash audit workflow for Claude Code projects, covering both the literal Unicode character and the `&mdash;` HTML entity form, double dash punctuation handling, CSS custom property exceptions, and context-sensitive replacement rules (comma, colon, semicolon, parentheses, period). Includes instructions to update `docs/PRD.md` with a Writing Style section and push all changes to GitHub after the audit is complete.
- `prompts-data.js`: Embedded copy of every prompt markdown file as `window.PROMPTS_DATA`, loaded via a `<script>` tag. This lets the site read prompt content with no server, so it runs by opening `index.html` directly (`file://`) while keeping the `.md` files as the readable source.
- `style.css`: Full design system stylesheet. Implements the Azqato brand system: `#0d1117` background, `#161b22` surface, `#00d4a0` teal accent, system font stack, CSS Grid sidebar layout, code block component, copy button with state transitions, home page prompt list, hero section, responsive breakpoints at 1024px and 768px, reduced motion support.
- `script.js`: Parses the embedded prompt markdown (frontmatter, description, fenced prompt block), builds the sidebar dynamically, handles hash routing, and provides copy-to-clipboard behavior using the native Clipboard API. On click, reads the rendered `<code>` element's text content, writes it to clipboard, updates the button label to "Copied!" for 2 seconds, then resets to "Copy".
- `README.md`: Project overview, how-it-works, files table, docs table, file structure, prompt markdown format, design summary, running locally instructions, and instructions for adding new prompts.
- `docs/PRD.md`: Product requirements. Covers problem statement, solution, goals, non-goals, audience, technical requirements, page structure, navigation, copy button behavior, writing style rules (em dash prohibition in all forms, replacement guidelines, general tone), and prompt addition workflow.
- `docs/DESIGN.md`: Full design specification. Covers design direction, color system with all CSS custom property tokens, typography scale, layout grid, sidebar spec, content area spec, code block component spec, copy button spec, home page prompt list spec, hero section spec, favicon, signature elements, navigation states, footer, responsive behavior, accessibility requirements, CSS file structure, architecture and templates, and what-not-to-do rules.
- `docs/PATCHNOTES.md`: This file.

### Design Decisions

- Prompts are authored as markdown files in `prompts/`, not as hand-written HTML. Adding a prompt is a content task, not an HTML task.
- The site runs with zero dependencies and no server. Because browsers block `fetch()` on `file://`, prompt markdown is embedded in `prompts-data.js` and loaded with a `<script>` tag, which the browser permits from local disk. The `.md` files remain the canonical, readable source and `prompts-data.js` mirrors them.
- Inherited the Azqato brand system directly from the Stocks methodology site and ComposerAtlas. Consistent accent color (`#00d4a0`), surface colors, sidebar layout, and `h2::before` vertical bar are intentional cross-site design continuity.
- Footer reads "Built by Azqato." with only the wordmark "Azqato" as a teal link. The trailing period sits outside the link and inherits the muted text color, so it is neither colored nor clickable.
- No syntax highlighting at v1.0. Prompt text is plain monospace. The goal is readability and copy speed, not code presentation.
- Code block header bar pattern (label left, copy button right) mirrors common documentation site conventions (Stripe, Tailwind, GitHub) and provides instant affordance for the primary user action.
- Emoji favicon (`💬`) chosen to distinguish the Prompts site from other Azqato properties visually in browser tabs while remaining zero-dependency.
