---
title: Mobile Audit
description: Audit every page at multiple breakpoints for overflow and layout bugs, fix root causes, verify with real DOM measurements instead of screenshots, then document the fixes.
meta: Claude Code Prompt
---

Runs a full mobile-friendliness and responsive-design pass across an entire site. Checks every page at a fixed set of widths (375px through 1920px) for horizontal overflow, container overflow, unwrapped toolbars, modal sizing, and clipped text. It also targets four specific CSS bug patterns that are common and easy to miss: the `overflow` shorthand silently canceling an `overflow-x` setting, bare `1fr` grid tracks forcing page-level overflow from wide content, flexbox children ignoring their flex parent's width because of the default `min-width: auto`, and doubled spacing when `margin` stacks with a flex/grid `gap`.

Verification is done by injecting a debug script that reads `scrollWidth`/`clientWidth` and element bounding rectangles, not by eyeballing screenshots, since headless browsers enforce a minimum viewport width that makes narrow screenshots unreliable. Any fix that changes how content is presented (not a pure CSS correctness fix) is flagged for a design decision before implementation. The prompt ends with updating the project's existing changelog and planning docs with the root cause and fix, following whatever documentation conventions the project already has.

## Prompt

```
Do a mobile-friendliness / responsive audit-and-fix pass across this entire site, following this process:

## 1. Audit scope
Check every page/view at these widths: 375px, 700px, 900px, 1023px (or your main sidebar/desktop breakpoint), 1150px, 1440px, 1920px. For each width, check for:
- Horizontal page overflow (the page itself becomes wider than the viewport)
- Elements that overflow their own container without an intended scroll affordance
- Any table, wide toolbar, or button row that doesn't wrap or reflow cleanly
- Modal/dialog sizing at narrow widths
- Text/labels getting clipped or overlapping

## 2. Specific bug patterns to check for (these are common, easy to introduce, and easy to miss)
- **CSS `overflow` shorthand resetting both axes**: if any element sets `overflow-x: auto` and elsewhere in the same rule (or a later rule) sets the bare `overflow: hidden`/`overflow: <value>` shorthand, it silently cancels the x-axis setting. Grep for elements with both an explicit `overflow-x`/`overflow-y` AND a bare `overflow` declaration.
- **CSS Grid implicit min-width on `1fr` tracks**: any `grid-template-columns` using a bare `1fr` has an implicit `min-width: auto`, which resolves to the intrinsic content width, not zero. If a grid cell contains something wide (a table, a long button row), it can force the whole grid, and the page, wider than the viewport. Fix is `minmax(0, 1fr)` instead of `1fr`. **Check this in EVERY media query that touches the same grid**, not just the desktop rule, since it's common to fix it in one breakpoint and have a separate mobile override silently reset it back to a bare `1fr`.
- **Flexbox children with default `min-width`/`min-height: auto`**: a flex item's default min-size is `auto`, which for a large-content child (e.g. a scrollable table wrapper inside a `flex: 1` column) resolves to "big enough to fit everything," not "shrink to the space given." This causes the child to overflow its flex parent instead of scrolling internally. Fix is `min-width: 0` / `min-height: 0` on the flex item.
- **Redundant spacing when adjacent elements are in a flex/grid container with `gap`**: if a container already has `gap`, don't also add `margin` on a child for spacing, since they stack and double that one gap. Check any element that was moved into a `gap`-based container after being styled for a different original position.

## 3. Verification methodology, do NOT rely on screenshots alone
Drive Microsoft Edge rather than Chrome, unless the project states its own
browser testing rule. Chrome is typically the owner's day-to-day browser and
driving it disturbs a live session; Edge runs the same engine, so every
measurement below is identical.

Any headless Chromium browser enforces an effective minimum viewport (~485-500px) even when you request a smaller `--window-size`, and screenshot pixel dimensions don't always match the actual layout viewport. Screenshots below that width will look broken even when there's zero actual overflow, and can also miss real bugs that only show up in specific coordinate ranges. Instead:
- Inject a small debug `<script>` into a scratch copy of the page that prints `window.innerWidth`, `document.documentElement.scrollWidth`, `document.documentElement.clientWidth`, and `getBoundingClientRect()` for suspect elements.
- The reliable check for "is there page-level overflow" is `scrollWidth === clientWidth`, not a visual read of a screenshot.
- For subtler layout bugs (like uneven spacing between sibling buttons), measure `getBoundingClientRect().left`/`.right` for every sibling and diff the gaps programmatically rather than eyeballing a zoomed screenshot.
- Test against a local copy served via `python -m http.server`, not the live site, so fixes can be verified before shipping.

## 4. Design decisions, ask, don't guess
If fixing overflow requires a real design choice (e.g., should a wide table hide columns responsively, switch to a card layout, or just gain a visible horizontal scrollbar; should hidden content be recoverable via a menu), stop and ask which approach to use before implementing. Don't silently pick an approach for anything that changes how content is presented, only for pure bug fixes (CSS correctness issues with one obviously correct fix).

## 5. Regression safety
Before and after each fix, verify no functional/data regression, whatever this site's zero-regression check is (a known-good rendering of key data, a specific test page's expected content, etc.), reconfirm it matches after the CSS/layout changes, since these are render-only changes that shouldn't touch logic.

## 6. Documentation
After the fixes are verified, update this project's changelog/patch-notes file with a dated entry describing what was found and fixed (root cause, not just "fixed mobile bugs"), and update any roadmap/PRD-style planning doc if this project has one. Follow whatever documentation conventions already exist in this repo (check for existing docs before creating new ones).

Work through this systematically: audit first and report what you find across all breakpoints, then ask about any open design questions, then implement and verify, then document.
```
