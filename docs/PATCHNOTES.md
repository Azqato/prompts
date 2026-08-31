# PATCHNOTES.md - Prompts

All notable changes to this project are documented here. Entries are listed in reverse chronological order. Each version entry includes the version number, date, and a summary of what changed.

---

## v1.36.1 - 2026-08-24

A follow-through release. v1.36.0 added `.gitattributes` and documented the decision, but left five other places in `docs/PRD.md` describing the state before it.

### Fixed

- Section 13 said the project is 13 files and that there is no `.gitattributes`, in a paragraph explaining the consequence of not having one. It is now 14 files, and that paragraph describes what the file does and why the mirror needs it. The tree lists it.
- Discrepancy 15 in section 18 ended with "whether to pin LF with a `.gitattributes` is open question 5". Marked resolved, with the note that `tools/prompts-mirror.py` still normalizes line endings and that this is now redundant on purpose rather than load-bearing.
- The deploy comparison in section 20 instructed normalizing line endings before comparing local against deployed, because `core.autocrlf` rewrites the working tree. That is no longer true of a current checkout. It now says the comparison is valid as it stands, and that normalizing anyway costs nothing and keeps the check correct against a clone made before v1.36.0.
- The technical debt table in section 30 still carried the missing `.gitattributes` as open debt. Struck out as fixed, which makes four struck rows.
- Four stale line counts, corrected in place under the mechanical-fact exception in section 33 rather than flagged, since a line count carries no intent: `css/style.css` is 567 lines rather than 540, in three places across sections 13 and 30, and `index.html` is 42 lines rather than 31, in section 20 of this document and section 12c of `docs/DESIGN.md`. Both had been stale since v1.28.0 added the Content Security Policy and the copy button's failed state.

### Notes

Worth recording why this release exists at all. The v1.36.0 change was one new file and a closed open question, which is about as small as a change gets here, and it still left five statements in the PRD false and four numbers wrong. The reason is that this document deliberately repeats facts across sections so each one can be read on its own, which section 33 states as the standard. The cost of that standard is exactly this: a fact that changes has to be chased through every place it appears, and the copy nobody was editing is the one that goes stale. Discrepancy 16, logged in v1.29.0, was the same failure with the same cause. The check that catches it is grepping for the thing that changed rather than trusting that the section it was changed in was the only one mentioning it.

### Verified

- Grepped for `gitattributes`, `autocrlf`, and every stale line count across all tracked files, then read each match rather than assuming the replacement was right.
- Re-rendered in Edge across all six routes. Unchanged, as expected: documentation only.
- `tools/prompts-mirror.py` clean.

---

## v1.36.0 - 2026-08-24

Closes open question 5, which has been open since v1.28.0.

### Added

- `.gitattributes`, pinning `* text=auto eol=lf`. A checkout now produces LF on any machine, whatever its `core.autocrlf` is set to. This repository stores LF, so nothing about the stored content changes; what changes is that the working tree can no longer disagree with it.
- The file carries a comment explaining why, because the reason is not obvious from the rule. The line breaks inside the `raw` strings in `js/prompts-data.js` are JSON escape sequences rather than real newlines, so git never rewrites them. Under `core.autocrlf=true` and with no `.gitattributes`, a checkout therefore produced CRLF source files under `prompts/` while their mirrored copies stayed LF, and the two stopped matching byte for byte with nothing actually wrong.

### Notes

The counter-argument recorded in section 19 was that `tools/prompts-mirror.py` already normalizes line endings on both sides, so the problem was handled. That was true, and it was judged insufficient for two reasons.

The failure mode is silent rather than loud. A literal comparison does not error, it reports a difference that is not there, and the natural response to the mirror check reporting drift on all four prompts is to run `--sync` and rewrite a file that was already correct.

And normalizing inside the tool puts the burden on every tool that touches these files, rather than on the repository. It had already cost two debugging cycles, both in this project: it broke the first version of the mirror script in v1.28.0, discovered only because a file had just been restored with `git checkout`; and in v1.35.0 a `git checkout` mid-session left an edit script unable to match its own target text, which surfaced as an unhelpful "not unique (0)" assertion rather than as anything mentioning line endings.

The deployed site is unaffected either way, since GitHub Pages serves what the repository stores and that was always LF.

### Verified

- Tested against a real checkout rather than by reading the rule. Both `prompts/documentation.md` and `js/prompts-data.js` were deleted and restored with `git checkout`, which is the exact operation that produced CRLF before. Both came back LF, and `tools/prompts-mirror.py` passed clean afterwards: four prompts, no orphans, all frontmatter present. That is the scenario that broke the first mirror script, so it is the one worth testing.
- Re-rendered in Edge across all six routes. Unchanged, as expected: no file the browser loads was modified.

---

## v1.35.0 - 2026-08-24

### Changed

- `prompts/documentation.md`: The enforced folder structure now shows `sitemap.xml` at the repository root and excludes it from the rule that moves stray files into `/docs`, alongside the README, the licence, and `robots.txt`.

### Added

- The reasoning that separates a sitemap from the two files listed beside it, because treating all three as one rule is how an audit either moves a working file or leaves a broken one alone. `robots.txt` is root by requirement: crawlers read it from the origin root and nowhere else. `sitemap.xml` is root by default: a sitemap is scope-limited by its own location, so one at `/docs/sitemap.xml` may only list URLs under `/docs/` and entries outside that path are ignored, while one at the root can list the whole site. That makes the root the position that is always correct without being the only correct one.
- The cross-submission exception, which is the part that changes what an audit should do. A sitemap named on a `Sitemap:` line in `robots.txt` is trusted for the entire host wherever it sits. So a sitemap outside the root is valid exactly when robots.txt points at it, and an audit that finds one there checks for that line rather than assuming the file is broken or relocating it. The same condition as `robots.txt` applies throughout: this is only relevant where the project actually serves a site.

### Verified

- Re-rendered in Edge across all six routes. Every route unchanged, all four prompt pages open collapsed and toggle correctly, no error view. The Documentation prompt matches its source fenced block exactly, confirming the mirror carries the edit.
- `tools/prompts-mirror.py` resynced and passed clean.

---

## v1.34.0 - 2026-08-24

### Changed

- `prompts/documentation.md`: The enforced folder structure now shows `LICENSE.md`. The licensing policy added in v1.33.0 already said the file goes at the repository root, but the structure diagram did not list it, so the two could be read as disagreeing and the diagram is the part a model follows literally.
- `LICENSE.md` is excluded from the rule that moves stray documentation into `/docs`, alongside the README. It is root only for the same reason the README is: it is one of the two files a person or a tool expects to find without looking. Stated explicitly in the prompt because hosting platforms detect a licence by looking in specific locations, the repository root is the most widely recognised of them, and a licence filed under `/docs` may not be detected at all.

- `robots.txt` is listed at the root as well, and excluded from the same move rule. This one is a hard requirement rather than a convention: crawlers fetch it from exactly one address, the origin root, and read it from nowhere else, so a copy under `/docs` is not a robots policy at all, it is an unreferenced text file. The licensing policy added in v1.33.0 already required `robots.txt` to stay open and consistent with the licence, but said nothing about where it lives, which left the one detail that determines whether it does anything.

### Added

- A never-move rule for licences. Where a project already has a licence file, under any name and in any location, it stays exactly where it is and is documented in place. An existing licence is a decision the project already made, and this audit records those rather than overruling them. `LICENSE.md` is created only where no licence exists.
- Two conditions on `robots.txt`, since the structure diagram would otherwise read as an instruction to create one everywhere. It applies only where the project actually serves a site: a library or a CLI has no origin to put one on and should not get one. And where a site is served from a subdirectory of a larger domain, the PRD says so, because the robots.txt governing it belongs to the domain owner and may not be the project's to write. This project is an example: it serves from `/prompts/` under a domain whose root it does not own.

### Notes

This release was written once with the file under `/docs`, then reverted before it was committed and rewritten with it at the root. The `/docs` version had a real problem: the structure rule would have relocated an existing root licence, which can stop a repository being reported as licensed. The reasoning survived the reversal and is now the justification for keeping it at the root rather than for moving it, which is why this note exists at all: the argument is worth more than the position it was first written to support.

### Verified

- Re-rendered in Edge across all six routes, unchanged. The Documentation prompt matches its source fenced block exactly. Mirror check clean.

---

## v1.33.1 - 2026-08-24

### Changed

- `prompts/documentation.md`: The licensing policy now names the licence file as `LICENSE.md` rather than as a plain text file, at all five places it referred to one. The licence is a document people read, it belongs to the same markdown doc set as the four files this audit already writes, and every platform that detects a licence file recognises the `.md` extension, so nothing is lost by it.

### Verified

- Re-rendered in Edge across all six routes, unchanged. The Documentation prompt is 29,137 characters and matches its source fenced block exactly. Mirror check clean.

---

## v1.33.0 - 2026-08-24

A licensing default policy for the Documentation prompt, supplied by the author.

### Added

- `prompts/documentation.md`: A **Licensing** section, placed after Security since both concern what a project asserts rather than how it is built. Like every policy in this prompt it yields to what the project already has: where a project has a well defined licence, the audit names it, points at the file, and states what it permits, and the default applies only where there is no licence or where a bare licence name sits in a README with no licence text behind it.
- The default posture is all rights reserved, source-available rather than open source. Publish a LICENSE that grants nothing, because the repository is published so it can be read and publishing is not a grant. The reasoning is the part that makes the rule usable: a permission given to everyone cannot easily be withdrawn from one person, and the goal is usually not to stop copying but to retain the ability to act against a specific bad actor. Those two goals conflict the moment the licence hands out broad permissions.
- The NO WAIVER clause is called out as load-bearing, since a long history of tolerating copies is the first thing an infringer points at. Also stated: the asymmetry rule, that widening a grant is one sentence and narrowing a granted right is not, so when in doubt grant less and offer the request route; and that a licence is never asserted without licence text, because a bare name with no file is an ambiguity rather than a grant.
- One standing carve-out, for AI and search referencing. Search engines, AI assistants, answer engines, and other automated systems may crawl, index, store for retrieval, quote, summarise, link to, and cite the work, with attribution requested rather than required and no permission to ask for. Being cited in an AI answer is the modern equivalent of ranking: it costs nothing and gains distribution, and enforcing against a citation works against the project's own purpose. The line is drawn at three distinct things: referencing is granted, substitution is not, and training data is not granted by default but is routed to the request path with a note that it is not usually refused. Retrieval-and-cite is what actually produces the citations, so this keeps the benefit without handing over a training licence.
- Three things the licence must not claim: it does not purport to override a hosting platform's terms, since a public repository already grants that platform's users whatever its terms say and the licence should state that those operate independently rather than pretend to withhold them; it does not claim third-party data derived from an external API or public source; and it does not restrict rights that cannot be restricted, such as fair use or fair dealing.
- The required LICENSE sections are listed, and the machine-readable layer is required to stay consistent with the licence: `robots.txt` stays fully open with a comment marking that as deliberate, and the LICENSE is named authoritative if the two ever disagree. A grants-nothing licence beside an open `robots.txt` is a contradiction a cautious crawler operator may resolve the wrong way.

### Changed

- The permission-request route was generalized. The policy as supplied named a specific repository's issue tracker as the example. Section 11 of `docs/PRD.md` prohibits a prompt from referencing services or accounts belonging to the author, and discrepancy 8 in section 18 records two prompts being deleted in v1.19.0 partly for exactly that. The prompt now says to route to a public tracker rather than private email and to name that tracker's address for the repository being audited, which preserves the reasoning, that a visible record suits a posture whose enforcement depends on permissions being specific and traceable, without embedding one project's address in a prompt meant to run anywhere.

### Notes

**This repository has no LICENSE file**, so by the policy just written it falls to the default. That was not acted on in this release, for two reasons. A licence is a legal assertion published under the author's name rather than a documentation change, so it is the author's call rather than a default to inherit silently. And the posture deserves a deliberate answer here in particular: this site exists to hand people prompts to copy and use, which is not obviously the same posture as all rights reserved. Recorded as open question 7 in section 19. Declining the default and saying why is a valid answer; leaving no licence and no note is the only outcome that carries a real cost, because it leaves a reader guessing.

### Verified

- Re-rendered in Edge across all six routes. Every route unchanged, all four prompt pages open collapsed and toggle correctly, no error view.
- The Documentation prompt grew to 28,907 characters and the rendered page carries the new section, matching the fenced block in `prompts/documentation.md` exactly, which confirms the mirror carries the edit rather than a stale copy.
- `tools/prompts-mirror.py` resynced and passed clean: four prompts, no orphans, all frontmatter present.

---

## v1.32.0 - 2026-08-24

A working practice change rather than a product change. Nothing about the site itself is different.

### Removed

- `docs/PRD.md` section 20: "Never push or publish without being asked. Publishing is the author's decision." The author gave standing authorization on 2026-08-24 for this repository, so every change here now ships as soon as it is documented and verified. There is no approval step and nothing waits for a release window.

### Changed

- `docs/PRD.md` section 20 gains a Publishing subsection recording the authorization, its date, and its scope, along with the reasoning. The reasoning is worth keeping because it is specific to this project rather than a general claim that pushing is safe: the site is static, with no database, no user data, no session, and no server-side state, so a bad deploy cannot corrupt or lose anything. Rollback is one revert and one push and takes about as long as the deploy did.
- The Never list keeps an entry in the same position, rewritten: never push a change that has not passed the checks. Removing the approval step does not remove the verification, and with the pause gone the verification is the only thing left between an edit and the live site. That is a stronger reason to run it than existed before, not a weaker one.
- `docs/PRD.md` section 29, Deploy: the same change, stated where the deploy procedure actually lives so a reader following the runbook does not have to have read section 20 first.

### Notes

Three boundaries were written into the change rather than left implied.

**It covers this repository only.** The authorization was given about this project, so it does not travel to any other repository.

**It does not shorten the procedure before a push.** The mirror check must still print OK, the page must still be opened from disk and looked at, and the patch notes and version history row are still written before the push rather than after. A release that is live and undocumented is precisely the state this project's documentation practice exists to prevent.

**It is unrelated to the rule in section 11** that no prompt's text may instruct its reader to push. That rule is about the content this site publishes to other people, not about how this site is maintained, and the two were easy to conflate because both used the word "push". Section 29 now says so explicitly.

### Verified

- Re-rendered in Edge across all six routes. No change, which is the expected result: this release touches only documentation, and no file the browser loads was modified.
- `tools/prompts-mirror.py` passed clean without needing a resync, since no prompt source changed: four prompts, no orphans, all frontmatter present.

---

## v1.31.0 - 2026-08-24

A second default policy for the Documentation prompt, on where a change is verified.

### Added

- `prompts/documentation.md`: A **Verification Environment** section, placed after Browser Testing since the two answer adjacent questions about how a project checks its own work. The default is to verify locally and never against production, unless the request explicitly asks for a production check. Local means whatever the project's own setup produces: the file opened from disk, a local server, a development build.
- The section gives the reason rather than only the rule, because a rule without one gets dropped the first time it is inconvenient. Testing against production means the change has already shipped, so the test can only report what users are already seeing. It also puts load, writes, or test data onto a live system, and it turns a failure into something the author has to roll back rather than something they fix before pushing.
- **It separates two things that are easy to conflate.** Verifying functionality is local. Confirming a deploy arrived is a separate step, run against production after the push, and it is a comparison rather than a test: fetch the deployed artifact and check it matches what was already verified locally. That is legitimate and is explicitly not an exception to the rule, because it answers a different question. Without saying this the policy would appear to forbid the post-push check this project has done for two releases.
- Two further clauses. Where local and production genuinely differ in a way that can hide a bug, the Runbook must name what differs and what class of bug can therefore only appear once deployed, since a reader who does not know a gap exists cannot compensate for it. And a destructive or state-changing check is never pointed at production, covering writes, deletes, migrations, seeded records, and anything that sends mail or a webhook; where a live system is the only way to exercise something, stop and ask.
- `docs/PRD.md` section 20: The rule stated explicitly for this repository, along with the deploy-confirmation procedure and the two ways local and deployed differ here.

### Changed

- Nothing about how this project works. It has described its check as opening `index.html` from disk since v1.0, which is the rule already. The prompt now requires that to be written down rather than implied, so section 20 says it outright. This is the merge rule working as intended: the project already had a rule, so the default did not overrule it, it documented it.

### Notes

The two environment differences recorded for this project are worth stating here too, because both are the kind of thing a local check silently cannot catch. Hash routing resolves against a directory rather than a domain root, so a path assumption that holds at `file://` can break under `/prompts/`. And `file://` is a secure context, so `navigator.clipboard` is available locally exactly as it is over `https://`, which means a local check cannot catch the copy button failing for a secure-context reason. That second one is a genuine limit on the verification gap already recorded as open question 6, not a reassurance.

### Verified

- Re-rendered in Edge across all six routes, per the policy added in v1.30.0. Every route unchanged: the home view and an unknown slug both render four cards, all four prompt pages open collapsed and toggle correctly, no route renders the error view.
- The Documentation prompt grew to 24,682 characters and the rendered page carries the new section, matching the fenced block in `prompts/documentation.md` exactly, which confirms the mirror carries the edit.
- `tools/prompts-mirror.py` resynced and passed clean: four prompts, no orphans, all frontmatter present.

---

## v1.30.0 - 2026-08-24

A browser testing policy, added to the Documentation prompt as a default and then applied to this repository and to the one other prompt that drives a browser.

### Added

- `prompts/documentation.md`: A **Browser Testing** section, placed beside Writing Style because it has the same shape: document the project's rule if it states one, and only adopt the default where it does not. The default is to drive Microsoft Edge and never Chrome. Where there is no JavaScript runtime on the maintenance machine, end-to-end testing means driving a headless browser directly, and Chrome is typically the owner's day-to-day browser, so driving it disturbs a live session. Edge runs the same engine, so nothing about the results changes.
- Three clauses were added around the rule itself, because the bare instruction leaves the obvious gaps unanswered. It applies to every browser a test drives rather than only the one named in a config file, since an ad hoc headless invocation from a shell command is testing too, and that is the form this project actually uses. The resolved binary path belongs in the Runbook, because it differs by platform and is the first thing that breaks on a new machine. And a project that genuinely needs a second engine should say which browsers it targets and why, rather than dropping the default silently.
- `docs/PRD.md` section 29: This repository's own browser testing rule, adopted from that default since it stated none. Records the Edge path on this machine, the exact headless invocation used, and two constraints that are not obvious: the Content Security Policy blocks inline scripts, so a driver has to be a real same-origin file rather than injected markup, and a DOM dump cannot exercise the Clipboard API, which is why the copy button's paths remain unverified.

### Changed

- `prompts/mobile-responsive-audit.md`: The verification methodology section opened with "Headless Chrome enforces an effective minimum viewport", which is an instruction to drive Chrome and directly contradicted the new default. It now names Edge, defers to any rule the project states, and describes the viewport floor as a property of any headless Chromium browser, which is what it always was. The measurements are unchanged because the engine is the same.

### Notes

Worth stating plainly: every browser check in this project up to and including v1.29.0 used Chrome, this session included. The policy is new, not newly enforced, and the patch notes for v1.28.0 and v1.29.0 accurately record Chrome as what was used at the time. They are left alone, because they describe what happened rather than what the rule is now.

### Verified

- The full render check was re-run in Edge across all six routes, which is both the verification for this release and the first exercise of the policy. Every route matches what Chrome produced: the home view and an unknown slug both render four cards, all four prompt pages open collapsed with the label reading "Expand" and toggle to "Hide", and no route renders the error view.
- The Documentation prompt now renders at 22,785 characters and the new section reaches the page: the rendered text contains both "Browser Testing" and the Edge rule. That count matches the fenced block in `prompts/documentation.md` exactly, which confirms the mirror in `js/prompts-data.js` carries the edit rather than a stale copy.
- `tools/prompts-mirror.py` resynced the data file and then passed a clean check: four prompts, no orphans in either direction, all frontmatter present.

---

## v1.29.0 - 2026-08-24

The prompt block is now collapsible, and collapsed when a page opens. The first new component on the site since v1.0.

### Added

- `js/script.js`: A collapse toggle in the code block header bar, sitting immediately left of the copy button. It is a real `<button>` carrying `aria-expanded` and `aria-controls="prompt-body"`, both kept in step with its visible label. Its label names the action it performs rather than the state it is in, "Expand" when the block is hidden and "Hide" when it is shown, which is the convention the copy button already sets.
- **The entire header bar is the click target, not only the button.** The listener sits on `.code-block-header`, which carries `cursor: pointer`. A click on the toggle reaches the same handler by bubbling, so there is no second listener on the button and no way for the two to fire against each other. Clicks originating inside `.copy-btn` return early, so copying never collapses the block that was just copied.
- The button exists alongside the clickable bar rather than instead of it, because the bar is a `div`: it cannot be focused, cannot be reached by keyboard, and carries no accessible name or state. The bar is deliberately given no ARIA role, since the button inside it is already the accessible control and labelling the container would announce the same action twice.
- `css/style.css`: `.code-block-actions`, a flex row with an 8px gap holding the toggle and the copy button, so the header is a label on the left and an action group on the right.
- `docs/DESIGN.md` section 5: A full Collapse Toggle spec, and the code block spec now documents the action group, the pointer cursor on the bar, and the collapsed default.
- `docs/PRD.md` section 10a: Prompt Collapse Behavior. This is the first lettered section in the PRD. It is numbered `10a` rather than inserted as a new section 11 because nine releases of these notes cite that document by section number, and renumbering would silently invalidate every one of those references. The convention is now stated in section 33, which previously said only that sections are appended.

### Changed

- **The prompt block is collapsed when a prompt page opens**, on every load and every navigation. The prompts run to several hundred lines; the Documentation prompt alone rendered as roughly 350 lines of unbroken text directly beneath the title. That buried the description, which is the part explaining what the reader is about to copy, off the top of the screen on arrival.
- This appears to contradict the tenet that the code block is the product, and does not. Copy works whether the block is shown or hidden, because the text stays in the DOM and only its display is suppressed, so the primary action is still one click from arrival. The rule that actually mattered, that the header bar with the copy button is visible without scrolling on desktop, now holds on every prompt at every length rather than only on short ones. `docs/DESIGN.md` section 12c records the reconciliation instead of leaving a future reader to spot the tension and resolve it the wrong way.
- `css/style.css`: The toggle shares the copy button's rule outright, as `.copy-btn, .code-toggle`, rather than getting a second button treatment. The two are pixel-identical at rest because they are literally the same declarations, which is a property that cannot drift. `docs/DESIGN.md` section 12a now states this as the rule for adding any peer control.
- `docs/PRD.md` section 24: The assumption bullet on trusted input still described `escapeHtml()` as not escaping quotes, which stopped being true in v1.28.0. The v1.28.0 pass updated sections 30 and 31 for that change and missed this one, so the document contradicted itself for a release. Corrected, and logged as discrepancy 16 in section 18. The underlying assumption still holds and is restated at the level where it is still true: nothing validates a prompt file and the markdown renderer is hand-rolled, so the content being author-written is what makes it safe.

### Notes

Three things were considered and deliberately not done.

**No animation.** The collapse is `display: none`, not a height transition, and the toggle has no rotating chevron. `docs/DESIGN.md` section 12b permits transitioning only `color`, `border-color`, `background`, and `opacity`; an animated open needs `height` and a chevron needs `transform`. An earlier draft used a swapped glyph pair to stay inside that rule, which was dropped once the label became a word, since a word button beside a word button does not need one. The rule this implies is now written down: show and hide, do not animate open and closed.

**No persistence.** The block collapses again on every navigation. Remembering the reader's choice would mean `localStorage`, and section 31 of the PRD states as a privacy property that no browser storage API appears anywhere in the codebase. That is worth more than the convenience. Recorded under possible future work in section 23 so the reason is visible if it is ever reconsidered, rather than the idea simply reappearing.

**No hover treatment on the bar.** A build in progress lit the toggle up whenever the header was hovered, on the reasoning that the bar is the real click target and ought to say so. In use it reads as a glitch rather than as feedback, because the pointer can be several hundred pixels from the element that changed. It was removed before release. The pointer cursor carries the affordance on its own, and the design notes now say not to add it back.

### Verified

- Checked in headless Chrome from `file://`, driven by a real script rather than inspected statically, since every behaviour here is a click result. Fifteen assertions: the toggle is a `<button>`, its `aria-controls` resolves to an element that exists, it precedes the copy button in the DOM and to its left on screen, the label is leftmost, the bar reports `cursor: pointer`, and the two buttons render at identical heights. The block starts hidden with the label reading "Expand" and `aria-expanded` false. Clicking the button, the bar, and the label each toggle it correctly, with the label and the ARIA state moving together every time. Clicking copy changes neither. The prompt text is intact while hidden, the header keeps the copy button visible, and its bottom border is removed while collapsed.
- After the hover treatment was removed, confirmed that no `.code-block-header:hover` rule remains in the stylesheet, that the toggle does not match that selector in the rendered page, and that the toggle and copy button compute to identical colour and background at rest.
- Both states were also captured as screenshots at 1280x900 and looked at, because a passing assertion about a computed style is not the same as the layout being right.

---

## v1.28.0 - 2026-08-23

Acted on all four open questions raised by the v1.27.0 audit, after the author answered each one. This is the first release since v1.18.0 in which the site was actually rendered and checked.

### Added

- `tools/prompts-mirror.py`: A check and resync tool for the mirror between `prompts/*.md` and `js/prompts-data.js`, which section 19 has named the project's highest-value invariant and its weakest assumption since v1.18.0. `python tools/prompts-mirror.py` reports drift, an entry with no source file, a source file with no entry, a duplicate slug, missing `title` or `description` frontmatter, and a missing fenced prompt block, exiting non-zero on any of them. Those last three matter because `parsePrompt()` falls back silently for each: a prompt missing its title ships as a page titled with its slug rather than as an error anyone would notice. `--sync` rewrites the data file from source and appends any new prompt to the end of the array, since array order is display order. It refuses to sync when an entry has no source file, because deleting a prompt is a deliberate act with a documented procedure that also touches the README and these notes.
- The script uses only the Python standard library, is never loaded by the page, and is not a build step. Deleting it leaves the site byte-identical, which is the test the PRD now states for whether something is tooling or a dependency. It also ends the pattern of rewriting the resync procedure from scratch in every session.
- `index.html`: A Content Security Policy, delivered as a `<meta http-equiv>` because GitHub Pages does not allow custom response headers on a project site. `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'`. The reason is not XSS hardening, which is marginal on a page with no external resources, no inline handlers, and no untrusted input. The reason is that it makes the no-dependency rule enforceable by the browser rather than by discipline: a future session that reaches for a CDN script or adds a `fetch()` now gets a hard, visible failure instead of a working page that has quietly broken the guarantee the whole architecture exists to protect. Tenet 1 becomes a runtime property instead of a written one.
- `frame-ancestors` was deliberately left out, because it is ignored in a meta tag and including it would imply a protection that is not there.
- `js/script.js`: A failure path on the copy button. A missing Clipboard API, which is how an insecure context presents itself rather than as a rejection, or a rejected write now shows "Copy failed" for two seconds with a matching `aria-label` telling the reader to select the text manually. Success and failure share one code path and differ only in label, class, and `aria-label`, so their timing and reset behaviour cannot drift apart.
- `css/style.css`: A `.copy-btn.copy-failed` state in `--color-negative`. This is the first use of that token, which had been defined and unreferenced since v1.0.

### Changed

- `js/script.js`: `escapeHtml()` now escapes both quote forms as well as `&`, `<`, and `>`. `renderInline()` writes a markdown link target straight into `href="..."`, so a quote in a description's link target could previously break out of the attribute. It was never exploitable, because every byte of content is author-written, but it was the sharpest edge in the codebase and the fix is five characters. Entities decode back in both text content and `textContent`, so the rendered page and the copied prompt are unchanged.
- `js/script.js`: The slug is now escaped wherever it is interpolated into an attribute, in `buildSidebar()` (`href` and `data-slug`) and `renderHome()` (`href`). Slugs are filename-derived and safe today; this is the same fix applied consistently rather than left half-done in the one place it was noticed.
- `docs/DESIGN.md`: Both discrepancies flagged in v1.27.0 are corrected rather than left standing, after the author confirmed neither preserved an intended design. The section 11 CSS file structure list is now read from the stylesheet: the `.site-layout` class that never existed is gone, `.site-wrapper` is correctly described as the grid rather than as flex, the order matches the file, and the four omitted blocks are listed. The section 12 shell template now includes the `.sidebar-sticky` wrapper the sidebar layout depends on, plus the meta description, the nav `aria-label`, the `aria-live` region, and the new policy, with its three load-bearing elements called out. Rebuilding the shell from the old template would have broken the layout.
- `docs/PRD.md`: Sections 7, 13, 16, 18, 19, 20, 23, 26, 27, 29, 30, 31, and 32 updated for the four changes. The technical debt table in section 30 now shows three items struck out as fixed. Section 31 gained a Content Security Policy subsection recording the policy, the reasoning, and how it was verified. Section 20 adds running the mirror check to the mandatory post-change procedure, and adds never weakening the policy to the "Never" list, on the grounds that a change needing `script-src` relaxed is a change adding a dependency.
- `docs/PRD.md`: Section 7 now permits maintenance tooling explicitly, with the boundary stated: not part of the deployed artifact, never runs in a browser, no third-party package, and the site unchanged if it is deleted.

### Fixed

- A latent line ending mismatch, found while testing the new script rather than by reading anything. `core.autocrlf` is true system-wide, this repository has no `.gitattributes`, and it stores LF. So git hands a Windows clone CRLF source files, while the `raw` values inside `js/prompts-data.js` stay LF forever, because they are JSON escapes rather than real line breaks and git never rewrites them. A literal comparison would have reported drift on all four prompts in a fresh clone with nothing actually wrong, and the first version of the mirror script did exactly that the moment a file was restored with `git checkout`. The script now normalizes line endings on both sides, since they are a property of the checkout rather than of the content, and always writes the data file with LF. Whether to pin this repository-wide with a `.gitattributes` is recorded as open question 5.

### Verified

- **The site was rendered for the first time since v1.18.0**, in headless Chrome from `file://`, closing the verification gap that release opened and that v1.27.0 recorded. Three routes checked: the home view (four cards, five nav links, the hero heading), a prompt page (`#/documentation`, correct `h1`, copy button present), and an unknown slug (`#/does-not-exist`, falls through to the home view as designed). No error view on any of them. The card hover treatment built in v1.18.0 had been specified, styled, and documented for ten releases without anyone loading the page.
- **The Content Security Policy was verified enforced, not merely accepted.** A policy that is silently ignored also renders a working page, so passing was not evidence of anything on its own. The page was loaded from `file://` with an inline script and a real remote CDN script injected. Without the policy both executed, which confirms the test itself was valid. With the policy both were blocked, while the favicon data URI, the two same-directory scripts, the stylesheet, and all three routing cases continued to work. `'self'` behaves unusually on `file://` in some browsers and breaking local loading would have violated tenet 2, so this was tested before being committed to rather than after.
- **The mirror script was verified against real drift**, not just against a passing repository. A check that never fails is worthless: a byte was appended to a prompt file, the check failed with the correct message and a non-zero exit, `--sync` repaired it, and the check passed again. It was also confirmed to pass with a CRLF file in the working tree, which is the case that broke the first version.

### Notes

`tools/` is the fifth folder and the thirteenth file in the project, and the first addition to the repository that is not part of the deployed site. The line drawn in section 7 is deliberate and worth restating: it is tooling rather than a dependency because it never runs in a browser, is never required to build, serve, or deploy, and can be deleted without changing the site. Nothing automates it. There is still no hook and no continuous integration, so it depends on the procedure in section 20 being followed, exactly as the manual page check does.

---

## v1.27.0 - 2026-08-23

Full documentation audit, run by pointing this project's own Documentation prompt at this repository. The whole codebase was read first, then every document in `/docs` in full, then each was compared against the code before anything was written.

### Added

- `docs/PRD.md`: Sections 21 through 35, the fifteen sections the Documentation prompt requires that this PRD had never carried. Target Users (the two real personas behind the one-line scope note in section 6, plus the non-user the site deliberately does not serve), User Stories, Feature List (shipped, deliberately not built with the reason for each, and possible future work), Assumptions, Success Criteria, Tenets, Roadmap, Metrics, Runbook, Technical Reference, Security, Public Surface and Retired Items, Documentation Audit Process, Press Release, and Frequently Asked Questions.
- `docs/PRD.md`: Section 26, seven tenets ordered by priority, each stating the tradeoff it resolves rather than a principle everyone would agree with. No dependencies ever, it must run from a file on disk, the markdown file is the truth, write down why not just what, documentation records rather than overrules, a prompt must be safe for a stranger, and small enough to hold in your head.
- `docs/PRD.md`: Section 28, Metrics, which records that this project measures nothing and cannot without breaking a tenet. Analytics would mean a third-party script, GitHub Pages exposes no logs to the repository owner, and the site makes no network calls. The north star, prompts retrieved rather than rewritten, is explicitly not instrumentable. What is actually tracked is six manual checks, and a performance budget is stated structurally: four same-origin requests, roughly 200 KB, zero runtime network calls, and no fifth request permitted because it would mean a dependency.
- `docs/PRD.md`: Section 29, the Runbook, written for someone who has just cloned the repository. Prerequisites are a browser and nothing else, with the five browser features actually required. Records that there is no port because there is no server, that there is no build at all, and that the environment variable reference is empty. Includes the resync procedure for `js/prompts-data.js`, the one-line deploy, rollback, and an eight-row common-errors table covering every failure mode identified during the audit.
- `docs/PRD.md`: Section 30, Technical Reference, carrying what section 7 states as constraints. Both data models with every field, type, source, and fallback; a function-by-function contract table for `js/script.js` standing in for the API surface the project does not have; an explicit statement that there is no state management and no storage API is used anywhere; and nine items of known technical debt, each with the correct fix and the reason it has not been done.
- `docs/PRD.md`: Section 31, Security. Confirms by reading every file that no secret, credential, token, or environment variable exists anywhere, that no cookie or browser storage is used, and that no third party receives any data. Records the attack surface honestly rather than claiming there is none: `innerHTML` used for all rendering, `escapeHtml()` not escaping quotes while a markdown link target is written into an `href`, and repository compromise as the realistic worst case. States the dependency policy as a rule: no dependency may be added, for any reason.
- `docs/PRD.md`: Section 32, the item-by-item public surface list the removal policy in section 12 is applied against, which that policy previously required without providing. Nine addressable items each marked public or internal with the consequence of removing it, the state of the empty `REDIRECTS` map, and a complete retired-items table covering all eleven removals since v1.0 so a reader who finds a reference to something deleted can resolve it.
- `docs/PRD.md`: Section 33, Documentation Audit Process, recording how these documents are produced and how they should be handled going forward: the four-file rule, how an audit is run, and the seven writing rules that bind the documents even when nobody is running the prompt.
- `docs/DESIGN.md`: Section 4a, the spacing system. Base unit 2px with a preferred 4px rhythm, derived from the values actually in the stylesheet rather than invented, with a fifteen-step scale mapping each value to what uses it. Records that spacing is deliberately not tokenized and why, and that horizontal padding is the only spacing that changes responsively.
- `docs/DESIGN.md`: Section 12a, Component Patterns. The shared container pattern (surface, border, 10px radius), the interactive state progression, rules for buttons and cards, and an explicit statement that forms and modals do not exist and should not, because a form implies submission which implies a server.
- `docs/DESIGN.md`: Section 12b, Animation and Motion. One duration and one easing curve, `0.15s ease`, used everywhere, with the reasoning for allowing no second value. A complete five-row inventory of everything that moves, and the rules: transition only colour, border, background, and opacity, never `all`, never a layout-affecting property, reveal rather than shift, no entrance animation, and no loading state.
- `docs/DESIGN.md`: Section 12c, notes for a model working on the design. The context that is invisible when editing a single rule: the design is inherited from four sibling sites rather than invented, restraint is the design, the code block is the product, and the specific declarations that are load-bearing.
- `docs/DESIGN.md`: A component spec for the error and status panel, which had shipped since v1.0 in both `js/script.js` and `css/style.css` and appeared in no document. Includes the reasoning for styling it as a neutral information panel rather than an alert.
- `README.md`: Sections the new standard requires and the old README did not have: who the site is for, current status, and a "Learn More" section pointing at `/docs` and naming what each document carries.

### Changed

- `README.md`: Rewritten to the general-reader standard adopted in v1.26.0. The previous README was written for a developer and carried a Files table of internal paths, a file structure tree, the prompt markdown format, "Running Locally", and the full add, rename, and remove procedures, all of which the standard now bars from the README and routes to `/docs`. It now describes what the site is, what each prompt does in plain language, who it is for, and where the technical detail lives. Nothing was lost: every relocated item landed in sections 29, 30, or 33 of `docs/PRD.md`. Length went from 141 lines to 55.
- `docs/DESIGN.md`: Section 10, Accessibility, rewritten from five bullets. Now states the target as WCAG 2.1 Level AA, carries a contrast table with the warning that muted text on surface is the tightest pair on the site, lists what is implemented including the `aria-live` region and the global `focus-visible` rule, and sets out keyboard navigation expectations. Two gaps are recorded rather than omitted: there is no skip-to-content link, so a keyboard user passes seven stops before reaching the copy button on a prompt page, and that count grows with every prompt added; and the copy confirmation is announced only through an `aria-label` change.
- `docs/DESIGN.md`: Section 9 expanded from a two-row table to the full rule set below 1024px. `height: auto` on `.sidebar-sticky` and `flex-basis: 100%` on `.sidebar-nav` are marked load-bearing, because both are the v1.11.0 bug fixes and each looks like an ordinary declaration that could be tidied away, which would silently reintroduce a shipped bug.
- `docs/DESIGN.md`: Section 2 no longer describes `--color-negative` and `--color-warning` as "unused at v1.0". Both are still unused at v1.27.0. Added why they are reserved rather than deleted, and noted that the error view deliberately does not use `--color-negative`.
- `docs/PRD.md`: Section 13 said `css/style.css` was 509 lines. It is 536, and has been since v1.18.0. Corrected in place rather than flagged, under the mechanical-fact exception now stated in section 33: a line count carries no intent, so nobody could have meant it.
- `docs/PRD.md`: The closing paragraph of section 19 said the Em Dash Audit and Project Onboarding prompts "were retired behind redirects". Those redirects were deleted in v1.24.0. The sentence described the v1.23.0 state and v1.24.0 did not catch it. Corrected. The v1.23.0 patch note still describes the redirects and is deliberately left alone, because a patch note records what happened at the time while that paragraph describes the current state.
- `docs/PRD.md`: Section 19 claimed there were no TODO, FIXME, or HACK markers anywhere in the repository. A literal search now matches in three files. Every match is prose naming the markers, including the sentence making the claim. Reworded to carry the same "naming the thing" exemption that section 11 gives the em dash rule.
- `docs/PRD.md`: Section 19 rewritten. Added a limits-of-the-analysis subsection recording that nothing was executed, no page was rendered, the contrast ratios were not recomputed, the browser support claim is a judgment rather than a checked matrix, and the Pages configuration is unreadable from the repository. The open questions list was replaced with four new numbered questions.
- `docs/PRD.md`: Sections 6 and 7 gained cross-references to the new sections that carry their detail.

### Fixed

- Nothing. No defect was found in the code. The audit was read-only through step 3 and every write landed in the four documentation files.

### Discrepancies recorded rather than corrected

Six new rows were added to the section 18 table in `docs/PRD.md`, numbered 9 through 14. Two blocks in `docs/DESIGN.md` were annotated in place rather than fixed, under the merge rule: **the CSS file structure list in section 11**, which names a `.site-layout` class that does not exist, describes `.site-wrapper` as flex when it is the grid, lists the blocks out of the file's actual order, and omits four blocks entirely; and **the shell template in section 12**, which omits the `.sidebar-sticky` wrapper that the sidebar layout depends on, along with the meta description and two ARIA attributes. Rebuilding the shell from that template would break the layout, so each now carries an inline note recording the observed reality and directing the reader to `index.html` and `css/style.css` as authoritative. Both remain open question 1 for the author.

### Audit findings, no change required

- **Mirror integrity: clean.** All four `prompts/*.md` files are byte-identical to their `js/prompts-data.js` entries, with no orphan in either direction.
- **Em dash sweep: zero violations.** All three forms were searched independently across all twelve files. Eight matches, every one an instance that names the character it prohibits: three in section 11 of `docs/PRD.md`, one in the Documentation prompt's Writing Style section, its mirror in `js/prompts-data.js`, and two historical patch notes describing the rule. All are exempt under section 11. No double dash is used as punctuation anywhere. Every document written in this audit was checked the same way before being saved.
- **Security sweep: clean.** No secret, credential, token, API key, or environment variable anywhere in the repository. No `fetch`, `XMLHttpRequest`, `localStorage`, `sessionStorage`, or `indexedDB` in any file. The only outbound URLs are the W3C SVG namespace inside the favicon data URI and two links to the author's own domain.
- **No orphan CSS.** Every class used in `index.html` and `js/script.js` is defined in `css/style.css`.
- **Prompt Content Rules: clean.** No prompt instructs its reader to push, commit, or publish, and none references the author's accounts, services, or paths.
- **No TODO, FIXME, or HACK markers.** See the note above on why a literal search matches anyway.

---

## v1.26.0 - 2026-08-23

### Changed

- `prompts/documentation.md`: Repurposed the README specification. The README is now the public front door, written for a general reader rather than a developer, and asks for what the site offers in plain language, who it is for, current status, and where to learn more. Install steps, commands, ports, environment variables, build instructions, version numbers, and dependency lists are explicitly barred from it and belong in `/docs`. This holds for every project regardless of type: developers are served by `PRD.md`, so the README never has to compromise for them.
- `prompts/documentation.md`: Relocated the evicted technical content rather than duplicating it. The Runbook section now opens by stating that it carries everything a developer needs to run the project, since the README deliberately does not, and assumes a reader who has just cloned the repository. It gained a Prerequisites bullet (runtime, package manager, and system requirements, each at the version the project actually needs rather than the newest available), absorbed installation order, start command, and default port into its local setup bullet, and gained an environment variable reference covering key names, what each does, and whether it is required, never the values.
- `prompts/documentation.md`: Replaced the "Do not pad" standard. In `/docs`, and in `PRD.md` above all, completeness now beats brevity: a section that restates context to stand on its own is doing its job, because a reader may arrive at it directly and should not have to assemble an answer from three other sections. The standard still bars filler, marketing language, and sentences carrying no new information, on the principle that thorough means more facts rather than more words around the same facts. The README is named as the exception and stays tight.
- `prompts/documentation.md`: The live site link is now satisfiable by a plain statement that there is no hosted instance, so a required section can no longer invite invention on a project that has never been deployed.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Recorded this release in the version history.

### Removed

- `prompts/documentation.md`: The `ReadMe` PRD section added alongside the README repurpose. Every bullet in it was already required elsewhere: the tech stack by Technical Requirements, installation and build and deploy by Runbook, and environment variables by both Runbook and Security. Three sections claiming the same facts is the duplication the README change set out to remove, relocated rather than fixed, so the section was dropped and the two bullets it uniquely contributed (prerequisites, default port) were folded into Runbook. This also removed a duplicated artifact line and the `ReadMe` casing inconsistency.

---

## v1.25.0 - 2026-08-23

### Added

- `prompts/documentation.md`: The read-only constraint from the retired Project Onboarding prompt, at the top of "Steps to follow". Steps 1 through 3, the codebase crawl and the read of every existing document, now forbid writing, editing, renaming, deleting, and moving any file, along with installers, migrations, formatters, builds that write output, and any state-changing version control command. Writing begins at step 4 and is limited to the documentation files the prompt names. This was the one part of Project Onboarding not carried over in v1.22.0, on the reasoning that the Documentation prompt exists to write files. Scoping it to the analysis steps rather than the whole run resolves that: the prompt already required a full scan before touching any documentation, and this makes the requirement enforceable instead of advisory.
- `prompts/documentation.md`: Also carried over the instruction not to skip a step because it looks obvious, and to say so explicitly when a step turns up nothing rather than staying silent.

### Changed

- `prompts/documentation.md`: The steps in "Steps to follow" are now numbered, so the read-only constraint can name the range it applies to. Step 1 gained "read files rather than inferring from their names" and step 2 gained "read each in full", both from the retired prompt.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.24.0 - 2026-08-23

### Removed

- `js/script.js`: All three `REDIRECTS` entries. The map is now empty. `github-wiki-setup` to `github-wiki` (added v1.17.0) and the two added in v1.23.0 all pointed at prompt slugs, and prompt slugs are not a public surface.

### Changed

- Corrected the definition of public facing, which the redirect policy depends on. The public surface of this project is the deployed page, `index.html` and the asset paths it loads. Everything under `prompts/` is source. A prompt's slug is derived from its source filename rather than being a contract of its own, so renaming or removing a prompt is an internal change and needs no redirect. The router already renders the home view for an unrecognized slug, so an old hash resolves to a working page.
- `js/script.js`: The `REDIRECTS` map is kept, empty, with its comment rewritten to explain when an entry would be warranted. The mechanism costs one property lookup per navigation and would otherwise have to be rebuilt if a genuine public address is ever retired.
- `docs/PRD.md`: Rewrote both procedures in section 12. "Renaming Prompts" no longer pairs a slug change with a redirect and drops the four rules for the map, keeping the permanence, no-chaining, and no-reuse rules scoped to genuine public addresses in "Removing Prompts". "Removing Prompts" now draws the line at the deploy boundary rather than at whether a prompt is visible in the navigation. Updated the section 14 flow description, the section 16 binding rules, the section 18 redirect bullet, and the section 20 working practice.
- `prompts/documentation.md`: The Deprecation and Removal section defined public facing as anything with an address someone could be holding, which swept in source files. It now draws the line at the deploy boundary, states that a source file is not public facing even when its name appears in a built URL, and requires the PRD to say where the project puts that boundary, since the rule cannot be applied without knowing which side a file is on.
- `README.md`: Rewrote the "Renaming a Prompt" and "Removing a Prompt" sections to match, and corrected the note added in v1.23.0 that described the two retirements as redirected.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Recorded this release in the version history.

Patch notes for v1.17.0 and v1.23.0 still describe redirects that no longer exist. They are left as they are, since they record what happened at the time.

---

## v1.23.0 - 2026-08-23

### Removed

- `prompts/em-dash-audit.md`, `prompts/project-onboarding.md`: Retired. The Documentation prompt absorbed both in v1.22.0, the em dash rule as its Writing Style section and the onboarding analysis as its Conventions, Documentation Versus Reality, Risks and Open Questions, and Working Practice sections.
- `js/prompts-data.js`: Removed the two corresponding entries. Four prompts remain: Add Prompt, Documentation, Mobile Audit, and GitHub Wiki.
- `README.md`: Removed the two rows from the Files table and the two lines from the file structure tree.

### Added

- `js/script.js`: Two `REDIRECTS` entries, `em-dash-audit` to `documentation` and `project-onboarding` to `documentation`. Unlike the three prompts deleted in v1.19.0, these two were live in the sidebar and home list, so their slugs are public addresses that people may hold. Section 12 of `docs/PRD.md` requires a redirect in that case, not a plain delete. The map now holds three entries.

### Changed

- `prompts/documentation.md`: The description named the Em Dash Audit and Project Onboarding prompts, which no longer exist. Rewritten to describe the same capability without referring to them.
- `README.md`: The hash routing example used `index.html#/em-dash-audit`, and the prompt markdown format example used the Em Dash Audit frontmatter. Both now use live prompts. Added a note to the hidden prompts paragraph explaining why these two retirements got redirects when the v1.19.0 deletions did not.
- `docs/PRD.md`: Section 11 referred to the Em Dash Audit prompt as the place the prohibited characters are quoted; it now points at the Writing Style section of the Documentation prompt. Updated the section 13 file counts (12 files, four prompts), the section 18 mirror and redirect map bullets, and closed the open question from v1.22.0.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.

---

## v1.22.0 - 2026-08-23

### Added

- `prompts/documentation.md`: Absorbed the Project Onboarding and Em Dash Audit prompts as required PRD sections. The prompt now produces a document that covers what those two prompts produced separately, in one pass.
- `prompts/documentation.md`: New "Conventions" section, deriving the house style from the code rather than from any style guide the project contains. Covers naming, formatting, organization, comment density, error handling, and commit and branching style read from version control history. Where a convention is inconsistent it records which form is dominant and which files deviate, so the next contributor matches the majority rather than the last file they opened.
- `prompts/documentation.md`: New "Writing Style" section carrying the em dash rule as a default: prohibited in all three forms, searched independently because a search for one will not catch the other, CSS custom properties untouched, the six replacements including the permitted single hyphen, and the exemption for instances that name the character they prohibit. The prompt applies the style to every document it writes, then sweeps the rest of the project and records what it found.
- `prompts/documentation.md`: New "Documentation Versus Reality" section, recording each discrepancy rather than quietly fixing it, with the code treated as the truth about what is and the documentation as the truth about what was intended. Resolved entries stay in the table with a note on how they were resolved.
- `prompts/documentation.md`: New "Risks and Open Questions" section, covering what the analysis did not understand, fragile areas, what is dangerous to change, work already in progress, and numbered open questions that are folded back in as answered rather than deleted.
- `prompts/documentation.md`: New "Working Practice" section, written as concrete instructions rather than principles: what to check before editing, what never to do with the reason attached, a table mapping each kind of change to the file to open first, and how to verify a change.
- `prompts/documentation.md`: Four new standards in the audit preamble, carried over from Project Onboarding. Merge rather than overwrite, since documentation holds intent that cannot be reconstructed from code. Every policy in the specifications is a default that applies only where the project states no rule of its own, with conflicts flagged rather than silently resolved. Read files rather than inferring from their names, and mark uncertainty as uncertainty. Do not pad.

### Changed

- `prompts/documentation.md`: Frontmatter description and on-page description updated for the wider scope.
- `README.md`: Updated the Files table row for the Documentation prompt.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Recorded this release in the version history.

`prompts/em-dash-audit.md` and `prompts/project-onboarding.md` were left in place. Both are live on the site, so their slugs are public addresses, and removing either would need a redirect under the policy in `docs/PRD.md` section 12. Whether they stay as standalone prompts now that the Documentation prompt covers their ground is an open question for the author.

---

## v1.21.0 - 2026-08-23

### Changed

- `prompts/documentation.md`: The removal policy is now a default rather than an override. The prompt checks first whether the project already states a removal rule of its own, in its docs, a contributing guide, or a consistent pattern in the changelog and code. If it does, that rule is documented and left alone, on the grounds that the audit records how a project works rather than overruling how it has decided to work. Where an existing rule and the default differ, both are kept and the difference is flagged for the author instead of one silently replacing the other. The public-facing versus internal rule from v1.20.0 applies only where the project states no rule at all.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.20.0 - 2026-08-23

### Changed

- `prompts/documentation.md`: The Deprecation and Removal section added in v1.19.0 asked the model to state whatever removal rule a project already had. It now prescribes this site's rule instead: a redirect is decided by whether the thing being removed is public facing, not by the fact that it is being removed. Anything with an address someone outside the project could be holding (URL, route, slug, permalink, published artifact, exported name) is retired behind a redirect or equivalent shim. Anything internal is pruned entirely, with no redirect, alias, stub, or tombstone. The prompt tells the model to adapt the mechanism to whatever the project has, to record the reasoning, and to say so explicitly if the project has no redirect mechanism at all.
- `prompts/documentation.md`: The section also now requires the public surface list to be specific enough to answer the question for any given file, states that compatibility entries are permanent, never chained, and never reused for different content, and records that historical changelog entries are not rewritten when something is deleted.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.19.0 - 2026-08-23

### Removed

- `prompts/consolidate-documents.md`, `prompts/docs-folder-audit.md`, `prompts/documentation-audit.md`: Deleted. All three were documentation prompts superseded by the Documentation prompt, and had been hidden from the sidebar and home list since v1.9.0. No redirects were added. A redirect exists to keep a public URL working, and a prompt that has been off the navigation since v1.9.0 is not one anyone is being handed. Adding three permanent redirect entries would have been maintenance in exchange for nothing.
- `js/prompts-data.js`: Removed the three corresponding entries. Six prompts remain.
- `README.md`: Removed the three rows from the Files table and the three lines from the file structure tree.

### Added

- `docs/PRD.md`: New "Removing Prompts" subsection in section 12. The rule is that a redirect is decided by whether the thing being removed is public facing, not by whether it is being removed. A live prompt's slug is a public address and gets retired behind a redirect. Anything already off the navigation is deleted outright. The same test applies to any file in the repository. Includes the five-step delete procedure and the note that historical patch notes are left alone.
- `README.md`: New "Removing a Prompt" section summarizing the policy and pointing at the PRD for the procedure.
- `prompts/documentation.md`: New "Deprecation and Removal" section in the required PRD sections, covering the project's removal policy, an explicit list of what is publicly addressable, and a record of retired items. Any project documented with this prompt now has to state its own version of the rule rather than deciding it case by case.

### Changed

- `prompts/documentation.md`: The description compared this prompt to Consolidate Documents and Documentation Audit by name, both now deleted. Rewritten to describe the depth it folds into the PRD without referring to prompts that no longer exist. Also corrected "Tenents" to "Tenets" in the required sections list.
- `js/prompts-data.js`: Resynced the `documentation` entry from its source `.md` file.
- `docs/PRD.md`: Updated the section 13 file counts (14 files, six prompts), added the removal rule to section 16, marked item 8 of the section 18 discrepancy table resolved by deletion, rewrote the two bullets in section 18 that described the hidden prompts in the present tense, closed two open questions in section 19, and added the delete case to section 20.

---

## v1.18.0 - 2026-08-23

### Added

- `css/style.css`: Built the card hover treatment on the home prompt list. `docs/DESIGN.md` had specified `--color-card-hover` as a card hover background and `--color-purple` as a gradient accent since v1.0, but neither token was ever referenced and `.prompt-list-item:hover` explicitly set `background: none`. Each list item is now a bordered, rounded card on `--color-surface` with a 12px gap between cards, hovering to `--color-card-hover` with an accent border and a 2px teal to purple gradient bar across the top. The bar is an absolutely positioned `::before` rather than a real `border-top`, so the card does not shift by 2px when it appears, and `overflow: hidden` clips it to the corner radius.
- `docs/PRD.md`: Sections 13 through 20, written by a full read-only onboarding pass over the repository. Structure map, architecture and flow traced from the code, code conventions derived from the files, the complete list of binding rules with their sources, stack and deployment, a documentation versus reality table, risks and open questions, and a working practice section covering what to check before editing and where to look for each kind of change.
- `docs/PRD.md`: The single hyphen is now a documented replacement in the section 11 Writing Style table, with a note that the prohibition covers only the em dash character, the `&mdash;` entity, and the double dash, and that instances naming the prohibited character are left in place.

### Changed

- Ran the Em Dash Audit across the project. Replaced 25 literal em dashes with single hyphens: the titles of `docs/PRD.md`, `docs/DESIGN.md`, and `docs/PATCHNOTES.md`, and all 20 version headings in this file. Replaced one prose em dash in the v1.11.0 entry with a comma, three in the section 8 `/docs/` bullets of `docs/PRD.md` with colons, and one double dash used as punctuation in `prompts/documentation-audit.md` with a colon. The em dashes inside the section 11 prohibition list and inside the Em Dash Audit prompt were left alone, since those lines exist to name the character.
- `prompts/em-dash-audit.md`: The prompt now instructs that a single hyphen is permitted and encouraged where context justifies it, and is preferred in document titles, section headings, and version lines, since it is the closest visual match to the em dash it replaces. Also added an instruction to leave instances that the text needs in order to mean anything.
- `js/prompts-data.js`: Resynced the `em-dash-audit` and `documentation-audit` entries from their source `.md` files.
- `docs/DESIGN.md`: Rewrote the Home Page Prompt List component spec for the card layout, added the card hover to the animation allowance in section 13, and bumped the document to 1.6.
- `docs/PRD.md`: The `**Version:**` header field now tracks the current release rather than sitting at 1.0 forever. Recorded that GitHub Pages publishes `main` at the repository root by manual push, which the onboarding pass could not determine from the repository alone. Marked items 2, 5, and 6 of the section 18 discrepancy table as resolved and rewrote the open questions list.

---

## v1.17.0 - 2026-08-23

### Added

- `js/script.js`: A `REDIRECTS` map and a redirect step in `route()`. A retired slug now rewrites the hash to the current one, which re-enters the router and renders the right prompt with a canonical address bar. Every redirect is guarded on its target existing, so a stale entry falls through to the home view instead of trapping the reader in a dead end. First entry: `github-wiki-setup` to `github-wiki`.
- `docs/PRD.md`: New "Renaming Prompts" subsection in section 12, making the redirect practice canonical. A slug is a public URL, so a slug change is always paired with a redirect rather than done bare. Documents the five-step rename procedure and four rules for the map: entries are permanent, redirects never chain, retired slugs are never reused for a different prompt, and every redirect is guarded on its target. Also records that historical patch notes and version history rows are not rewritten during a rename.
- `README.md`: New "Renaming a Prompt" section summarizing the practice and pointing at the PRD for the full procedure.

### Changed

- `prompts/github-wiki-setup.md` renamed to `prompts/github-wiki.md`, with the slug changed from `github-wiki-setup` to `github-wiki` so it matches the title set in v1.16.0. Renamed with `git mv` to preserve file history. The old URL (`index.html#/github-wiki-setup`) keeps working through the new redirect map. This is the rename that v1.16.0 deliberately deferred for lack of a redirect mechanism.
- `js/prompts-data.js`: Updated the slug for that entry. The `raw` value was resynced from the renamed `.md` file rather than hand-edited.
- `README.md`: Updated the Files table and file structure tree to the new filename.
- `css/style.css`: Widened the content area. `--content-max` changed from a flat `820px` to `max(820px, calc(75vw - 56px))`, so the content block measures 75vw on wide screens while the 820px floor holds line length steady on laptops. The floor also protects the layout below the 1023px breakpoint, where the sidebar collapses to a full-width top nav and a bare `75vw` would have shrunk the content instead of widening it. Mobile rendering is unchanged.
- `docs/DESIGN.md`: Updated the Content Area max width spec and documented why the `max()` floor is load-bearing.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.16.0 - 2026-08-23

### Changed

- `prompts/github-wiki-setup.md`: Renamed the prompt from "GitHub Wiki Sync" to "GitHub Wiki". The frontmatter `description` and body were left as they are, since both still describe the prompt accurately. The slug stays `github-wiki-setup` so existing direct links (`index.html#/github-wiki-setup`) keep working, and the filename is unchanged.
- `js/prompts-data.js`: Resynced the `github-wiki-setup` entry from its source `.md` file.
- `README.md`: Updated the Files table description to the new title.
- `docs/PRD.md`: Recorded this release in the version history.

Earlier patch notes and version history rows that mention "GitHub Wiki Sync" were deliberately left alone. They are a record of what the prompt was called at the time.

---

## v1.15.0 - 2026-08-23

### Added

- `prompts/project-onboarding.md`: Ninth prompt, "Project Onboarding". Puts a model through an eight-phase, read-only intake of an unfamiliar project before it is allowed to change anything: structure map, identity and purpose, a full read of every documentation file, technical foundation (dependencies, scripts, build, test, deploy), architecture traced from real entry points rather than from the docs, conventions derived from the code itself, a documentation-versus-reality cross-check, and an explicit risks-and-unknowns pass. Phases 1 through 8 forbid all writes, installs, and state-changing version control commands.
- The deliverable is not a chat briefing. Everything established is merged into `PRD.md`, the single file the prompt is permitted to write, so the understanding survives the session. The merge is additive: it preserves intent and rationale that cannot be reconstructed from code, matches the PRD's existing heading structure and tone, and where findings contradict the PRD it keeps both and marks the conflict for a human to resolve rather than silently correcting the document from code. No other file is touched, including the README and these patch notes; errors found elsewhere are reported instead.
- `js/prompts-data.js`: Regenerated to include `project-onboarding`.

### Changed

- `README.md`: Added `prompts/project-onboarding.md` to the Files table and the file structure tree.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.14.0 - 2026-07-06

### Changed

- `prompts/github-wiki-setup.md`: Renamed the "Changelog" wiki page to "Patch Notes" (`Patch-Notes.md`) throughout the prompt's frontmatter description, on-page description, and prompt text, to match this site's own terminology (`docs/PATCHNOTES.md`) rather than the more generic "Changelog" label.
- `js/prompts-data.js`: Regenerated to mirror the renamed page.

---

## v1.13.0 - 2026-07-06

### Changed

- `prompts/github-wiki-setup.md`: Reworked into "GitHub Wiki Sync" (title and description regenerated to match). Added an update mode: if the wiki repo already exists, the prompt pulls the current pages, diffs them against the README, PRD, PATCHNOTES, DESIGN, and any other project docs, and summarizes outdated sections, missing features, stale links, and content drift before editing anything. Page creation is no longer a fixed set beyond Home, Product Overview, and Changelog; the prompt now uses judgment on wiki information architecture, creating pages like FAQ, Roadmap, Architecture, Getting Started, Troubleshooting, or API Reference wherever a topic is distinct and cohesive. Added a step to create or keep a `_Sidebar.md` page in sync with the full current page structure.
- `js/prompts-data.js`: Regenerated to mirror the reworked `github-wiki-setup.md`.
- Also caught and fixed two more em dashes in the prompt's body text, in the Product Overview and Changelog descriptions, that were missed in the previous pass, replacing both with parentheses per the site's em dash prohibition.
- `README.md`: Updated the `github-wiki-setup.md` Files table description to match the reworked prompt.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.12.0 - 2026-07-06

### Added

- `prompts/github-wiki-setup.md`: Eighth prompt, "GitHub Wiki Setup". Reviews every documentation markdown file in a project, then sets up a GitHub wiki sourced from them. Checks first whether the wiki repo is initialized (GitHub only creates it after one manual page is added via the web UI) and stops to ask if it isn't. Curates, rather than dumps verbatim, content into a Home page (overview plus table of contents), a Product Overview page (stable current-state PRD sections), a Changelog page (condensed patch notes), and any other page mapping to a distinct PRD section. Rewrites internal/planning language for a public audience and drops internal-only notes.
- `js/prompts-data.js`: Regenerated to include `github-wiki-setup`.

### Changed

- `README.md`: Added `prompts/github-wiki-setup.md` to the Files table and file structure tree.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.11.0 - 2026-07-05

### Fixed

- `css/style.css`: Ran the Mobile Audit prompt against the live site (headless Chrome via CDP, `scrollWidth`/`clientWidth`/`getBoundingClientRect()` measurements at 375–1920px, not screenshots) and found the mobile/tablet header (< 1024px) was badly broken. Root cause: `.sidebar-sticky` sets `height: 100vh` for the desktop vertical sidebar, and the `@media (max-width: 1023px)` block that converts it into a horizontal header never reset that height, so the header stayed full-viewport-tall with its logo/nav/support button vertically centered inside, pushing all page content roughly 1200px below the fold on a typical mobile screen. Added `height: auto` to `.sidebar-sticky` in that media query.
- `css/style.css`: Secondary bug in the same header: `.sidebar-nav` shared its row with `.sidebar-logo` instead of dropping to its own line, squeezing the 5 nav links into a ~150px-wide column that stacked one link per row instead of wrapping across the full width (the existing `margin-bottom` on `.sidebar-logo` already implied the intended layout was logo-then-nav-below). Added `flex-basis: 100%` to `.sidebar-nav` in the same media query so it wraps full-width beneath the logo.
- No page-level horizontal overflow, `overflow` shorthand conflicts, bare `1fr` grid overflow, flex `min-width: auto` overflow, or margin/gap double-spacing were found anywhere else at any of the seven audited breakpoints across the home page and all seven prompt detail pages.

---

## v1.10.0 - 2026-07-05

### Added

- `prompts/mobile-responsive-audit.md`: Seventh prompt, "Mobile Audit". Audits every page of a site at seven fixed breakpoints (375px to 1920px) for horizontal overflow, container overflow, unwrapped toolbars, modal sizing, and clipped text. Targets four specific CSS bug patterns: the `overflow` shorthand canceling `overflow-x`, bare `1fr` grid tracks forcing page overflow from wide content, flexbox children ignoring their parent's width due to default `min-width: auto`, and doubled spacing from `margin` stacking with a flex/grid `gap`. Verifies fixes by injecting a debug script to read `scrollWidth`/`clientWidth` and bounding rectangles rather than relying on screenshots, since headless browsers enforce a minimum viewport width. Flags any fix that changes content presentation for a design decision before implementation, and ends by updating the project's existing changelog and planning docs.
- `js/prompts-data.js`: Regenerated to include `mobile-responsive-audit`.

### Changed

- `README.md`: Added `prompts/mobile-responsive-audit.md` to the Files table and file structure tree.
- `docs/PRD.md`: Recorded this release in the version history.

---

## v1.9.0 - 2026-06-27

### Added

- `js/script.js`: Support for an optional `hidden` frontmatter flag on prompts. `parsePrompt` reads `hidden` (true/yes/1), and `buildSidebar` and `renderHome` skip any prompt where it is set. `findPrompt` and routing are unchanged, so hidden prompts stay reachable by direct link (`index.html#/<slug>`).

### Changed

- `prompts/consolidate-documents.md`, `prompts/docs-folder-audit.md`, `prompts/documentation-audit.md`: Added `hidden: true` to the frontmatter. These three prompts are retired from the sidebar and home list but kept on the backend; existing direct links still resolve. The newer Documentation prompt supersedes them in the navigation.
- `js/prompts-data.js`: Regenerated to mirror the three `hidden: true` frontmatter additions.
- `README.md`: Noted which prompts are hidden from navigation and still reachable by direct link.
- `docs/PRD.md`: Documented the `hidden` frontmatter flag in the navigation and prompt markdown sections, and recorded the release in the version history.
- `docs/DESIGN.md`: Documented the optional `hidden: true` key in the prompt markdown template and version history.

---

## v1.8.0 - 2026-06-27

### Added

- `prompts/documentation.md`: Sixth prompt. The most comprehensive of the documentation prompts. Crawls the entire codebase first, then consolidates all documentation into four core files (README.md at the root; PRD.md, DESIGN.md, and PATCHNOTES.md in `/docs`), creates any missing files, and enforces the correct folder structure. Folds the full depth of a larger doc suite into a single PRD with required sections for Tenets, Roadmap, Metrics, Runbook, Technical Requirements, Security, a Press Release, and an FAQ, so the project can be understood from `/docs` alone without reading code.
- `js/prompts-data.js`: Regenerated to include `documentation`.

### Changed

- `README.md`: Added `prompts/documentation.md` to the Files table and file structure tree.
- `docs/PRD.md`: Added an "Adding Prompts" process note documenting the standing workflow for adding a new prompt and keeping documentation in sync, and recorded this release in the version history.

---

## v1.7.0 - 2026-06-14

### Added

- `prompts/docs-folder-audit.md`: Fifth prompt. Audits every document in `/docs` against the current codebase. Crawls all files first to build a complete picture of the project, then reviews each doc in `/docs` for outdated, missing, or inaccurate content and rewrites it. Ends with a per-file summary of what changed and why.
- `js/prompts-data.js`: Regenerated to include `docs-folder-audit`.

### Changed

- `README.md`: Added `prompts/docs-folder-audit.md` to the Files table and file structure tree.

---

## v1.6.0 - 2026-06-13

### Changed

- `style.css` → `css/style.css`: Moved stylesheet into a dedicated `css/` subfolder.
- `prompts-data.js` → `js/prompts-data.js`: Moved prompt data file into a dedicated `js/` subfolder.
- `script.js` → `js/script.js`: Moved main script into the `js/` subfolder.
- `index.html`: Updated `<link>` and `<script>` references to reflect new asset paths (`css/style.css`, `js/prompts-data.js`, `js/script.js`).
- `README.md`: Updated Files table and file structure tree to reflect new `css/` and `js/` folder layout.
- `docs/DESIGN.md`: Updated shell template, CSS file structure heading, and version history.

---

## v1.5.0 - 2026-06-13

### Added

- `prompts/add-prompt.md`: Fourth prompt. A meta-prompt for adding new prompts to the site. Accepts a raw prompt text and instructs Claude Code to generate the title and one-line description, create the markdown file in `prompts/`, mirror it into `prompts-data.js`, update the Files table in `README.md`, and add a version entry to `docs/PATCHNOTES.md`.
- `prompts-data.js`: Regenerated to include `add-prompt`.

### Changed

- `README.md`: Added `prompts/add-prompt.md` to the Files table and file structure tree.

---

## v1.4.0 - 2026-06-13

### Added

- `prompts/consolidate-documents.md`: Third prompt. Consolidates all project documentation into four core files: README.md at the root, and PRD.md, DESIGN.md, and PATCHNOTES.md inside `/docs`. Creates any missing files with required sections. Enforces the correct folder structure and moves misplaced files. A leaner alternative to the Documentation Audit prompt, targeting four documents instead of eleven.
- `prompts-data.js`: Regenerated to include `consolidate-documents`.

### Changed

- `README.md`: Added `prompts/consolidate-documents.md` to the Files table and file structure tree.

---

## v1.3.0 - 2026-06-13

### Changed

- `index.html`: Sidebar logo updated from "Prompts." to "Azqato's Prompts." Added Support button to the bottom of the sidebar, linking to `https://azqato.github.io/support.html` in a new tab.
- `script.js`: Homepage h1 updated from "Prompts." to "Claude Code Prompts." (teal dot preserved). Browser tab title updated to "Azqato's Prompts" on home view. Prompt pages now set the tab title to just the prompt name, with no site suffix.
- `style.css`: `.sidebar-sticky` changed from `max-height: 100vh` to `height: 100vh` with `display: flex; flex-direction: column` so the Support button pins to the bottom via `margin-top: auto`. `.sidebar-nav` gains `flex: 1` to fill available space. Added `.sidebar-support` and `.support-btn` styles with hover state matching the site's teal accent. Mobile breakpoint updated to flow the support button inline with nav links.
- `docs/DESIGN.md`: Updated sidebar spec, navigation spec (support button added), hero section spec, shell template, and version history.
- `docs/PRD.md`: Updated navigation section to document the support button.
- `README.md`: Project title updated to "Azqato's Prompts".

---

## v1.2.0 - 2026-06-13

### Changed

- `prompts/em-dash-audit.md`: Removed "Finally, push everything to GitHub." from the prompt text. Prompts are shared publicly and must not instruct users to push to any remote repository. Rewrote the closing instruction to: "After making these changes, ensure the patch notes and documentation files are all up to date describing the changes you just made." Updated the frontmatter description and on-page description paragraph to remove all mention of pushing to GitHub.
- `prompts-data.js`: Regenerated to mirror the updated `em-dash-audit.md`.
- `docs/PRD.md`: Added a Prompt Content Rules section to the Writing Style rules. Documents that prompts must not include GitHub push instructions or any account-specific actions, and requires this to be audited before any new prompt is published.

---

## v1.1.0 - 2026-06-13

### Added

- `prompts/documentation-audit.md`: Second prompt. Runs a full documentation audit on any project: reads all source files and existing docs, then creates or updates the complete suite of eleven documents (README, PRD, TRD, DESIGN, PATCHNOTES, PRFAQ, TENETS, METRICS, ROADMAP, SECURITY, RUNBOOK) to their required specifications. Also enforces the correct folder structure, moving any misplaced files into `/docs`.

### Removed

- `first prompt example.txt.txt`: Source text for the first prompt. Content is now canonical in `prompts/em-dash-audit.md`. No longer needed.
- `message.txt`: Source text for the documentation audit prompt. Content is now canonical in `prompts/documentation-audit.md`. No longer needed.

### Changed

- `prompts-data.js`: Regenerated to include both `em-dash-audit` and `documentation-audit`.
- `docs/PATCHNOTES.md`: Corrected v1.0.0 design decisions note about footer (period is not teal; it inherits the muted text color).

---

## v1.0.0 - 2026-06-13

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
