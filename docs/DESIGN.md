# DESIGN.md - Prompts

**Version:** 1.9.1
**Status:** Active
**Author:** Azqato

---

## 1. Design Direction

**Aesthetic:** GitHub Dark-inspired. Clean, information-dense, developer-credible. The site should feel at home next to other Azqato properties (portfolio, VIX Strategy, ComposerAtlas, Stocks) with the same visual language, the same color tokens, and the same interaction patterns.

**Tone:** Functional. This is a reference tool, not a portfolio piece. The design should get out of the way and let the content be the focus.

**Audience reading mode:** Quick and task-oriented. People come here to find a prompt and copy it. The design should reward scanning: clear hierarchy, instant recognition of where the prompt lives on the page, no content that requires reading before reaching the goal.

**Design lineage:** Follows the Azqato brand system established at `azqato.github.io`. The accent color (`#00d4a0`), surface colors, border tones, and interaction patterns are consistent with the portfolio site, ComposerAtlas, and the Stocks methodology site.

---

## 2. Color System

All colors are defined as CSS custom properties in `:root`.

| Token | Hex | Usage |
| --- | --- | --- |
| `--color-bg` | `#0d1117` | Page background |
| `--color-surface` | `#161b22` | Card and sidebar backgrounds |
| `--color-border` | `#30363d` | All borders and dividers |
| `--color-accent` | `#00d4a0` | Primary interactive color: links, active nav, hover borders, copy button |
| `--color-accent-hover` | `#00e6b0` | Hover state for accent elements |
| `--color-accent-light` | `rgba(0,212,160,0.08)` | Subtle tinted backgrounds (code block header, copy button hover) |
| `--color-tag-bg` | `#21262d` | Code block background |
| `--color-card-hover` | `#1c2128` | Card hover background |
| `--color-text-primary` | `#eef3f7` | Body copy, headings |
| `--color-text-secondary` | `#cbdae6` | Subtitles, captions, sidebar inactive links |
| `--color-positive` | `#3fb950` | Success state (copy button "Copied!" feedback) |
| `--color-negative` | `#f85149` | Error states. In use since v1.28.0 by the copy button's failed state |
| `--color-warning` | `#ffa657` | Caution callouts. Reserved, referenced nowhere in the stylesheet as of v1.28.0 |
| `--color-purple` | `#bc8cff` | Gradient accent on card hover top border |

`--color-warning` is held deliberately rather than deleted: it is part of the shared Azqato palette, and a caution state added later should use the brand value rather than inventing one.

Note that the error view described in section 5 does **not** use `--color-negative`, even though it is the error view. It is styled as a neutral information panel, because a failure to load prompt data is a diagnostic for the author in a broken working copy rather than an alarm for a reader. The one place the negative colour appears is the copy button's failed state, where it is reporting that an action the reader just took did not work, which is the case that genuinely warrants it.

**Rationale:** The `#00d4a0` teal is the Azqato brand signature across all projects. The dark background palette is drawn from the azqato.github.io design system. Primary text on background passes approximately 15:1 contrast; muted text on background is approximately 4.8:1, meeting WCAG AA.

---

## 3. Typography

**Font stack:** System fonts only. No external font loading.

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

**Monospace (code blocks, prompt text):**

```css
font-family: 'SF Mono', 'Consolas', 'Liberation Mono', 'Courier New', monospace;
```

| Role | Size | Weight | Color | Notes |
| --- | --- | --- | --- | --- |
| H1 (page title) | 1.875rem | 700 | `--color-text-primary` | Letter-spacing -0.3px |
| H2 (section title) | 1.375rem | 700 | `--color-text-primary` | Has `::before` vertical accent bar |
| H3 (subsection) | 1.0625rem | 600 | `--color-text-primary` | |
| Body | 1rem | 400 | `--color-text-primary` | Line height 1.6 |
| Lead / description | 1rem | 400 | `--color-text-secondary` | Line height 1.65 |
| Caption / meta | 0.78rem | 400 | `--color-text-secondary` | |
| Code / prompt text | 0.875rem | 400 | `--color-text-primary` | Monospace stack, line height 1.6 |

---

## 4. Layout

### Grid

```
Desktop (>= 1024px): 2-column grid
[ Sidebar (220px) | Content (1fr) ]

Tablet / Mobile (< 1024px): Single column
Sidebar collapses to a sticky top nav bar
```

### Sidebar (Left Navigation)

Persistent on desktop. Contains:

- Site logo (`Azqato's Prompts.` with teal dot accent)
- A Home link plus one nav link per prompt, built dynamically from the prompt data
- A Support button pinned to the bottom of the sidebar, linking to `https://azqato.github.io/support.html` in a new tab
- No in-page anchor links at v1.0

**Sidebar width:** 220px
**Sidebar background:** `--color-surface` (`#161b22`)
**Sidebar border:** 1px solid `--color-border` on the right
**Active nav link:** `--color-accent` text, 3px left border in accent, weight 600
**Inactive link color:** `--color-text-secondary`
**Hover link color:** `--color-text-primary`

### Content Area

**Max width:** `max(820px, calc(75vw - 56px))` on the text column, set by `--content-max`
**Padding:** 32px top/bottom, 28px left/right on desktop; 20px on mobile

The content block is capped at `--content-max` plus its 56px of horizontal padding, so the block itself measures 75vw once the viewport is wide enough. Below roughly 1170px the `max()` floor holds the text column at 820px, which keeps line length readable on laptops and leaves the mobile layout completely unchanged. Above that, the column grows with the viewport so wide screens are not left with a narrow strip of content and a large empty margin. The floor is what makes this safe at the 1023px breakpoint, where the sidebar collapses to a full-width top nav and a bare `75vw` would otherwise shrink the content instead of widening it.

---

## 4a. Spacing System

**Base unit: 2px. Preferred rhythm: 4px.**

There is no spacing token in `:root`. Every value is written literally in the rule that uses it, which is a deliberate consequence of the project's size: a token indirection for spacing would cost more in lookup than it saves in consistency across a single 536-line stylesheet. The scale below is therefore descriptive, derived from the values actually in use, not a set of variables to reference.

| Step | Value | Used for |
| --- | --- | --- |
| Hairline | 1px | Borders and dividers |
| 1 | 2px | The card hover gradient bar height |
| 1.5 | 3px | The `h2::before` accent bar width, the active sidebar link left border |
| 2 | 4px | Tightest gap: description offset under a card title, sidebar nav link gap, copy button vertical padding |
| 3 | 6px | Title-to-meta gap on a prompt header, list item spacing, mobile nav link vertical padding |
| 4 | 8px | Sidebar nav link vertical padding, support button vertical padding |
| 5 | 10px | Code block header vertical padding, mobile nav link horizontal padding |
| 6 | 12px | Card gap in the home list, support button horizontal padding, copy button horizontal padding, mobile logo bottom margin |
| 7 | 14px | Paragraph bottom margin, h2 bottom margin, hero h1 bottom margin, mobile sidebar vertical padding |
| 8 | 16px | Card padding, code block header horizontal padding, mobile content horizontal padding, mobile nav horizontal padding |
| 9 | 20px | Code block and status panel padding, mobile content vertical padding, h3 top margin, sidebar support top padding |
| 10 | 24px | Sidebar horizontal padding, sidebar logo bottom margin, description top margin, tablet content vertical padding |
| 11 | 28px | Content horizontal padding, footer vertical padding, sidebar vertical padding, h2 top margin, description bottom margin |
| 12 | 32px | Content vertical padding, footer horizontal padding |
| 14 | 40px | Hero bottom margin, the largest gap on the page |

**Rules:**

- Prefer a multiple of 4. The three values that are not (6px, 10px, 14px) are optical adjustments on small elements, not the norm to follow.
- Never introduce a value above 40px. If a section needs more separation than the hero gets, the layout is wrong rather than the spacing.
- Vertical rhythm inside the content column is driven by margins on the typographic elements themselves (`p`, `h2`, `h3`), not by wrapper padding. Match that when adding a block.
- Horizontal padding differs by breakpoint and is the only spacing that changes responsively: 28px on desktop, 20px on tablet, 16px on mobile.
- The one named spatial token is `--sidebar-width: 220px`, because it appears in the grid definition and would be meaningless as a literal there. `--content-max` is a computed width rather than a spacing step; see section 4.

---

## 5. Component Specs

### Section Heading (h2)

All `h2` elements include a `::before` pseudo-element: a 3px wide, 1.1em tall vertical bar in `--color-accent`, rendered inline via `display: flex; align-items: center; gap: 0.5rem`. This is the signature section delineation from the Azqato portfolio site.

---

### Prompt Page Structure

Each prompt page renders three sections in a single-column flow within the content area:

1. **Title block:** `h1` with the prompt name. Below the title, a small meta label (e.g. "Claude Code Prompt") in `--color-text-secondary`, 0.8rem.
2. **Description block:** One or more paragraphs in body text. Color `--color-text-primary`. Separated from the title by 24px margin.
3. **Code block:** Full prompt text. See Code Block spec below.

---

### Code Block

The code block is the primary UI element on every prompt page.

```
Outer wrapper:
  bg: --color-surface
  border: 1px solid --color-border
  border-radius: 10px
  overflow: hidden

Header bar (inside wrapper, above pre):
  bg: --color-tag-bg
  border-bottom: 1px solid --color-border  (removed while collapsed)
  padding: 10px 16px
  display: flex, justify-content: space-between, align-items: center
  cursor: pointer  (the whole bar is the collapse target)
  Left label: "Prompt" in --color-text-secondary, 0.8rem. Plain text, not a control
  Right: .code-block-actions, a flex row with 8px gap holding the
         collapse toggle then the Copy button, in that order

pre element:
  bg: --color-tag-bg
  padding: 20px
  overflow-x: auto
  margin: 0
  font-family: monospace stack
  font-size: 0.875rem
  line-height: 1.6
  color: --color-text-primary
  white-space: pre-wrap
  word-break: break-word
  display: none while the wrapper carries .collapsed
```

**The block is collapsed on arrival.** `renderDetail()` writes the wrapper with
`.collapsed` already on it, so a prompt page opens showing the title, the
description, and the header bar alone. The prompts run to several hundred lines
and an expanded default buried the description under a wall of text before the
reader had decided they wanted it. See the collapse toggle spec below.

---

### Collapse Toggle

Positioned in the code block header bar, immediately left of the Copy button.

```
Appearance: identical to the Copy button in every resting property.
  The two share one rule (.copy-btn, .code-toggle) rather than
  defining a second button treatment. Same border, radius, padding,
  size, colour, and hover.

Collapsed state (the default):
  text: "Expand"
  aria-expanded: false
  wrapper carries .collapsed
  pre: display: none
  header bar: border-bottom removed

Expanded state:
  text: "Hide"
  aria-expanded: true
```

Three things about this are deliberate.

**The label names the action, not the state.** "Expand" when collapsed, "Hide"
when expanded, matching the convention "Copy" already sets.

**The whole header bar is the click target, not just the button.** The listener
sits on `.code-block-header`, which carries `cursor: pointer`. A click on the
toggle bubbles up to that same handler, so there is no second listener on the
button and no chance of a double fire. Clicks originating inside `.copy-btn` are
ignored, so copying never collapses the block. The button still exists because
the bar is a `div`: it cannot be focused, cannot be reached by keyboard, and has
no accessible name or state.

**Only the buttons themselves show hover.** An earlier build lit the toggle up
whenever the bar was hovered, on the reasoning that the bar is the real target
and should say so. It reads as a glitch rather than as feedback, because the
pointer can be several hundred pixels away from the element that changed. The
pointer cursor carries the affordance on its own. Do not add it back.

There is no persistence. The block is collapsed again on every page load and on
every navigation, because no browser storage API is used anywhere in the project
and adding one for this would contradict a stated security property. See
`docs/PRD.md` section 31.

---

### Copy Button

Positioned in the code block header bar, flush right.

```
Default state:
  text: "Copy"
  bg: transparent
  border: 1px solid --color-border
  border-radius: 6px
  padding: 4px 12px
  font-size: 0.78rem
  color: --color-text-secondary
  cursor: pointer

Hover state:
  border-color: rgba(0,212,160,0.5)
  color: --color-accent
  bg: --color-accent-light

Copied state (2 seconds):
  text: "Copied!"
  color: --color-positive
  border-color: rgba(63,185,80,0.4)

Failed state (2 seconds):
  text: "Copy failed"
  color: --color-negative
  border-color: rgba(248,81,73,0.4)

Transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease
```

The default and hover blocks above are shared with the collapse toggle. Only the
copied and failed states are the copy button's own.

JavaScript behavior: on click, use `navigator.clipboard.writeText()` to copy the `<code>` element's text content. Set the button to "Copied!", then reset after 2000ms.

Both outcomes are reported. If the Clipboard API is unavailable, or the write rejects, the button shows "Copy failed" for the same 2000ms and its `aria-label` becomes "Copy failed. Select the prompt text and copy it manually". Added in v1.28.0: before that a failed copy left the button reading "Copy" and said nothing, so the reader would paste whatever was on the clipboard already, believing it had worked. A silent failure on the site's only action was the worst failure mode it had.

The two states share one code path and differ only in label, class, and `aria-label`, so they cannot drift apart in timing or reset behaviour.

---

### Home Page Prompt List

On `index.html`, each prompt is a card. The list is a vertical flex column with a 12px gap, one card per prompt.

```
Card (.prompt-list-item, an <a> wrapping the whole card):
  position: relative
  display: flex, flex-direction: column, align-items: flex-start
  padding: 16px
  background: --color-surface
  border: 1px solid --color-border
  border-radius: 10px
  overflow: hidden
  transition: background 0.15s ease, border-color 0.15s ease

  Prompt title in --color-accent, weight 600, 1rem
  Below title: one-line description in --color-text-secondary, 0.875rem,
    margin-top 4px

Hover:
  background: --color-card-hover
  border-color: rgba(0,212,160,0.5)
  title underlines
  ::before gradient bar fades in (opacity 0 to 1, 0.15s ease)

::before (the gradient top border):
  absolutely positioned, top/left/right 0, height 2px
  background: linear-gradient(90deg, --color-accent, --color-purple)
  opacity 0 by default
```

The bar is an absolutely positioned pseudo-element rather than a real `border-top`, so the card does not shift by 2px when it appears. `overflow: hidden` on the card clips the bar to the 10px corner radius.

---

### Error / Status Panel

Rendered into the content area by `renderError()` when `js/prompts-data.js` fails to load or parse. It replaces the whole view: there is no partial state, because without the prompt data there is nothing to render.

```
Heading: h1 "Could not load prompts"
Below it: the error message as a normal description paragraph
Then the panel (.status-message):
  background: --color-surface
  border: 1px solid --color-border
  border-radius: 10px
  padding: 20px
  color: --color-text-secondary
  line-height: 1.65
  Inline code inside it: 0.85rem
```

Styled as a neutral information panel, not an alert. It uses no `--color-negative`, no icon, and no red border. The reasoning: this failure is only ever reachable by the author, in a broken working copy, and the panel's job is to say which file to check rather than to signal alarm. A visitor to the deployed site will never see it unless the site is genuinely broken, in which case the calm version is still the right one.

The sidebar may be unbuilt when this renders, since `renderError()` can be called before `buildSidebar()`. That is accepted: navigation to a prompt would fail anyway.

---

### Hero / Intro Section (index.html)

```
h1: "Claude Code Prompts." (with teal dot in --color-accent)
Lead paragraph: --color-text-secondary, 1rem, line height 1.65
Max width: 640px
Margin bottom: 40px before the prompt list
```

---

### Favicon

All pages use an emoji SVG data URI favicon:

```html
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>">
```

---

## 6. Signature Element

The signature design element is the code block with its integrated copy button. Every prompt page exists to deliver one thing and the code block is that thing. The header bar with the "Copy" button must always be immediately visible without scrolling on desktop.

The `h2::before` vertical teal bar is the secondary signature element, consistent with the Stocks site and the rest of the Azqato brand.

---

## 7. Navigation

### Sidebar Links

- **Inactive:** `--color-text-secondary`, weight 500
- **Hover:** `--color-text-primary`
- **Active / current page:** `--color-accent`, weight 600, 3px left border in accent color

### Support Button

Sits at the bottom of the sidebar, pushed down by `margin-top: auto` on the `.sidebar-support` container. The `.sidebar-sticky` element is `height: 100vh` with `display: flex; flex-direction: column` so the button always pins to the viewport bottom.

```
Default state:
  display: block, text-align: center
  border: 1px solid --color-border
  border-radius: 6px
  padding: 8px 12px
  font-size: 0.8125rem, weight 500
  color: --color-text-secondary

Hover state:
  color: --color-accent
  border-color: rgba(0,212,160,0.5)
  background: --color-accent-light

Opens: https://azqato.github.io/support.html in a new tab (target="_blank" rel="noopener noreferrer")
```

On mobile (below 1024px), the support button flows inline with the nav links in the top bar.

### Tablet / Mobile (below 1024px)

Sidebar collapses to a sticky top bar with light blur backdrop (`backdrop-filter: blur(12px)`). Active state uses a bottom border instead of a left border.

---

## 8. Footer

```
border-top: 1px solid --color-border
background: --color-bg (#0d1117)
text: --color-text-secondary, 0.8rem, center-aligned
links: --color-accent
padding: 28px 32px
content: "Built by Azqato." where "Azqato" is a link to azqato.github.io
         in --color-accent. The trailing period sits outside the link and
         inherits --color-text-secondary (same color as "Built by"), so it
         is not colored and not clickable
```

---

## 9. Responsive Behavior

There are exactly two breakpoints, both `max-width`, both at the bottom of the stylesheet. The design is desktop-first: the base rules describe the desktop layout and each query overrides downward.

| Breakpoint | Changes |
| --- | --- |
| `< 1024px` | Sidebar becomes top nav bar, backdrop blur, bottom-border active state |
| `< 768px` | h1 reduces to 1.5rem, h2 reduces to 1.2rem, padding reduces to 20px/16px, code block font-size reduces to 0.8rem |

### Below 1024px, in full

The collapse is more than a grid change, and two of these declarations are load-bearing bug fixes rather than styling. **Removing either one silently reintroduces a shipped bug.** Both were added in v1.11.0 after the Mobile Audit prompt was run against the live site.

| Rule | Declaration | Why |
| --- | --- | --- |
| `.site-wrapper` | `grid-template-columns: 1fr` | Single column |
| `.sidebar` | `position: sticky; top: 0; z-index: 10; height: auto; width: 100%` | Becomes a top bar |
| `.sidebar` | `border-right: none; border-bottom: 1px solid` | Divider moves to the bottom edge |
| `.sidebar` | `background: rgba(22, 27, 34, 0.85)` plus `backdrop-filter: blur(12px)` | Translucent header. Degrades to a near-opaque bar without `backdrop-filter` support |
| `.sidebar-sticky` | **`height: auto`** | **Load-bearing.** The desktop rule sets `height: 100vh` for the vertical sidebar. Without this override the collapsed header stays full-viewport-tall with its contents vertically centred, pushing all page content roughly 1200px below the fold |
| `.sidebar-sticky` | `position: static; max-height: none; overflow: visible` | Undoes the desktop sticky column |
| `.sidebar-sticky` | `flex-direction: row; flex-wrap: wrap; align-items: center` | Horizontal bar |
| `.sidebar-nav` | **`flex-basis: 100%`** | **Load-bearing.** Without it the nav shares its flex row with the logo and squeezes into a roughly 150px column, stacking one link per row. This forces it onto its own line beneath the logo, which the logo's `margin-bottom` already implied was the intent |
| `.sidebar-nav` | `flex-direction: row; flex-wrap: wrap; gap: 4px` | Links flow horizontally and wrap |
| `.sidebar-nav a` | `border-left: none; border-bottom: 2px solid transparent; padding: 6px 10px` | Active indicator moves to the bottom edge |
| `.sidebar-support` | `margin-top: 0; padding: 0 16px 0 4px` | Releases the `margin-top: auto` that pinned it to the bottom on desktop, so it flows inline |
| `.content` | `padding: 24px 20px; max-width: 100%` | Full width. Note this overrides `--content-max`, so the `max()` formula does not apply below 1024px |

### Below 768px

Type and padding only. No layout change: the structure established at 1024px carries down unchanged. The site is verified at seven widths from 375px to 1920px; see `docs/PATCHNOTES.md` v1.11.0.

---

## 10. Accessibility

**Target: WCAG 2.1 Level AA.** Not formally audited, and the known gaps are listed below rather than omitted.

### Contrast

| Pair | Approximate ratio | AA requirement |
| --- | --- | --- |
| `--color-text-primary` on `--color-bg` | 15:1 | 4.5:1 for body text. Passes comfortably |
| `--color-text-secondary` on `--color-bg` | 4.8:1 | 4.5:1. Passes, with little margin |
| `--color-text-secondary` on `--color-surface` | Slightly lower than the above, since the surface is lighter than the background | 4.5:1. The tightest pair on the site |
| `--color-accent` on `--color-bg` | Well above 4.5:1 | Passes |

These figures are carried forward from earlier versions of this document and are stated as approximate. They have not been recomputed with a contrast tool. **Any new muted-text-on-surface combination should be checked rather than assumed**, because that pair already sits close to the floor.

Rule: never place `--color-text-secondary` on anything lighter than `--color-surface`, and never introduce a third surface tone without checking the muted pair against it.

### Implemented

- Copy button carries `aria-label="Copy prompt to clipboard"`, updated to `"Copied!"` on activation so the state change is announced rather than only shown in the visible label.
- The collapse toggle is a real `<button>` carrying `aria-expanded` and `aria-controls="prompt-body"`, which resolves to the `<pre>`. Both are kept in step with the visible label on every toggle. The header bar it sits in is also clickable, but the bar is a `div` and is deliberately not given a role: the button inside it is the accessible control, and duplicating that on the container would announce the same action twice.
- The collapsed prompt uses `display: none`, so it is removed from the accessibility tree as well as from the page. A screen reader is not offered several hundred lines of text the reader has not asked for.
- `#content` carries `aria-live="polite"`, so a view change on hash navigation is announced. This matters because routing never reloads the page and there is no other signal that the content changed.
- `#sidebar-nav` carries `aria-label="Prompt navigation"`.
- `:focus-visible` renders a 2px `--color-accent` outline with a 2px offset and a 3px radius, applied globally rather than per-component, so no interactive element can be added without one.
- `prefers-reduced-motion: reduce` sets `transition: none !important` and `animation: none !important` on every element and pseudo-element, and disables `scroll-behavior: smooth`.
- The code block uses `<pre><code>` semantics, so screen readers treat the prompt as preformatted text.
- The Support link uses `rel="noopener noreferrer"` with `target="_blank"`.
- Every card in the home list is a single `<a>` wrapping its whole content, so the entire card is one focusable target with one accessible name rather than a div with a nested link.
- `<html lang="en">` is set.
- Colour is never the sole carrier of meaning. The active nav link is marked by a border and a weight change as well as by colour; the copied state changes the button's text.

### Keyboard navigation

Expected behaviour, and what is actually there.

- All interactive elements are native `<a>` and `<button>` elements, so they are in the tab order by default. There is no `tabindex` anywhere, positive or negative, and no custom key handler. Tab, Shift-Tab, Enter, and Space all behave natively.
- Tab order follows the DOM: logo, then each nav link in order, then the Support button, then into the content area, reaching the collapse toggle and then the copy button after the description. The toggle is before Copy in the DOM as well as visually, so tab order matches reading order.
- **Known gap: there is no skip-to-content link.** On a prompt page a keyboard user must tab past the logo, every nav link, and the Support button before reaching the copy button, which is the primary action. With four prompts that is seven stops. This is the most significant accessibility shortfall on the site and it grows with every prompt added. Adding one would mean a visually-hidden anchor as the first focusable element in `<body>`, targeting `#content`, which needs a `tabindex="-1"` to be focusable as a heading target.
- **Known gap: the copy button's result is announced only via the `aria-label` change.** That is a reasonable signal but not a guaranteed one across screen readers; a live region would be more reliable. This applies to the failure state added in v1.28.0 as well as to success, and it matters more there, since a reader who does not notice the failure will paste the wrong thing.

### Deliberately not addressed

- No high-contrast theme and no light theme. Dark only is a brand decision (section 13), and the base palette meets AA on its own.
- No font-size control. The page uses `rem` throughout, so browser and OS text scaling applies without any custom widget.

---

## 11. CSS File Structure

Read from the file, in the order the blocks actually appear.

```
css/style.css structure (in order):
  :root (CSS variables, including --sidebar-width and --content-max)
  Reset / base (box-sizing, margin, padding, html, body, a)
  Layout (.site-wrapper, the two-column grid)
  Sidebar (.sidebar, .sidebar-sticky, .sidebar-logo, .accent-dot, .sidebar-nav)
  Sidebar support button (.sidebar-support, .support-btn)
  Main content (.content)
  Footer
  Typography (h1, h2 with ::before bar, h3, p, .lead, code)
  Hero / intro section (.hero)
  Home page prompt list (.prompt-list, .prompt-list-item and its ::before,
    hover states, .prompt-list-title, .prompt-list-desc)
  Prompt detail page (.prompt-header, .prompt-meta, .prompt-description)
  Code block (.code-block-wrapper, header bar, .code-block-actions,
    collapsed states, pre, code)
  Copy button and collapse toggle (shared default and hover,
    plus copied and copy-failed on the copy button alone)
  Status / error message (.status-message)
  Focus styles (:focus-visible)
  Media queries (tablet < 1024px, mobile < 768px)
  Reduced motion (prefers-reduced-motion)
```

Corrected in v1.28.0. This list previously named a `.site-layout` class that has never existed, described `.site-wrapper` as flex when it is the grid, listed the blocks in an order the file does not use, and omitted four blocks entirely. It was flagged as a discrepancy in v1.27.0 and corrected once the author confirmed there was no intended design being preserved in it.

Two notes for anyone adding a block. There is no spacing section, because spacing is written literally at each use rather than tokenized; see section 4a. And `body` is the flex column that pins the footer, while `.site-wrapper` is the grid inside it, which is the distinction the old list got backwards.

---

## 12. Architecture and Templates

### Single Shell

There is one HTML file, `index.html`. It is a static shell: sidebar, empty content area, footer. All views (home and each prompt) are rendered into the content area by `script.js` based on the URL hash. There are no per-prompt HTML files.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Azqato's Prompts</title>
  <meta name="description" content="A personal library of reusable Claude Code prompts.">
  <link rel="icon" href="data:image/svg+xml,...">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div class="site-wrapper">
    <aside class="sidebar">
      <div class="sidebar-sticky">
        <a class="sidebar-logo" href="#/">Azqato's Prompts<span class="accent-dot">.</span></a>
        <nav class="sidebar-nav" id="sidebar-nav" aria-label="Prompt navigation"></nav>
        <div class="sidebar-support">
          <a href="https://azqato.github.io/support.html" target="_blank" rel="noopener noreferrer" class="support-btn">Support</a>
        </div>
      </div>
    </aside>
    <main class="content" id="content" aria-live="polite"></main>
  </div>
  <footer>
    <p>Built by <a href="https://azqato.github.io">Azqato</a>.</p>
  </footer>
  <script src="js/prompts-data.js"></script>
  <script src="js/script.js"></script>
</body>
</html>
```

Corrected in v1.28.0. The previous template omitted the `.sidebar-sticky` wrapper, and **rebuilding the shell from it would have broken the sidebar layout**: that div is what carries `position: sticky`, `height: 100vh`, and the `display: flex; flex-direction: column` that lets `margin-top: auto` pin the Support button to the bottom. It also omitted the meta description, the nav `aria-label`, and the `aria-live` region. Flagged as a discrepancy in v1.27.0 and fixed once the author confirmed it was a stale transcription rather than an intended design.

Three things in this template are load-bearing and are not stylistic:

- **`.sidebar-sticky` must wrap all three sidebar children.** See above.
- **`prompts-data.js` must load before `script.js`.** It defines `window.PROMPTS_DATA`, an array of `{ slug, raw }` objects where `raw` is the verbatim text of a `prompts/*.md` file. Reverse the order and the page renders the error view.
- **The Content Security Policy must keep `script-src 'self'`.** It is what makes the project's no-dependency rule a runtime guarantee rather than a written one: a CDN script or a `fetch()` added later fails in the browser instead of silently shipping. Verified enforced on `file://`. See `docs/PRD.md` section 31. It defines `window.PROMPTS_DATA`, an array of `{ slug, raw }` objects where `raw` is the verbatim text of a `prompts/*.md` file.

### Prompt Markdown Template

Each prompt is a file in `prompts/`:

```markdown
---
title: [Prompt Name]
description: [One-line summary for the home list]
meta: Claude Code Prompt
hidden: true   # optional; omit for normal prompts
---

[Description of what the prompt does and when to use it.]

## Prompt

[fenced code block containing the full prompt text]
```

`script.js` parses the frontmatter, renders the description (a minimal markdown subset: paragraphs, lists, inline code, bold, links), and renders the first fenced code block as the copyable prompt. The optional `hidden: true` key removes the prompt from the sidebar and home list while leaving its page reachable by direct link; omit the key for a normal, visible prompt.

### Rendered Prompt View

The DOM produced for a prompt view matches the original component specs:

```html
<div class="prompt-header">
  <h1>[Prompt Title]</h1>
  <span class="prompt-meta">[meta]</span>
</div>
<div class="prompt-description"> ... </div>
<div class="code-block-wrapper">
  <div class="code-block-header">
    <span class="code-label">Prompt</span>
    <button class="copy-btn" aria-label="Copy prompt to clipboard">Copy</button>
  </div>
  <pre><code>[Full prompt text]</code></pre>
</div>
```

### Why No Fetch

Loading `prompts/*.md` with `fetch()` would require an HTTP server, because browsers block `fetch()` of local files on the `file://` protocol. Embedding the markdown in `prompts-data.js` and loading it with a `<script>` tag is what allows the site to run by double-clicking `index.html`, with no server and no dependencies, while keeping the `.md` files as the readable source.

---

## 12a. Component Patterns

Rules for building any recurring element, so a new one matches without having to reverse-engineer the existing ones.

### The shared container pattern

Every raised surface on the site (the code block wrapper, a prompt card, the status panel) is the same three declarations:

```css
background: var(--color-surface);
border: 1px solid var(--color-border);
border-radius: 10px;
```

10px is the container radius and it does not vary. Smaller controls use 6px (buttons), and the focus outline uses 3px. There is no other radius on the site. Do not introduce a fourth.

### Interactive states

Every interactive element follows the same progression, and the accent hover is the site's single interaction idiom:

| State | Treatment |
| --- | --- |
| Default | `--color-text-secondary` text, `--color-border` border, transparent or surface background |
| Hover | Text to `--color-accent` (or `--color-text-primary` for nav links), border to `rgba(0, 212, 160, 0.5)`, background to `--color-accent-light` |
| Active / current | `--color-accent` text, weight 600, a 3px accent bar (left border on desktop, bottom border on mobile), `--color-accent-light` background |
| Success | `--color-positive` text, `rgba(63, 185, 80, 0.4)` border. Used only by the copy button |
| Focus | Global `:focus-visible` outline. Never overridden per component |
| Disabled | No pattern exists. Nothing on the site can be disabled |

Note the two hardcoded `rgba()` values. They are the only colour literals outside `:root`, and they exist because they are alpha variants of tokens that CSS cannot derive without `color-mix()`. If a third is ever needed, define it as a token instead.

### Buttons

Three exist, and they are the template for any fourth.

- **Copy button** (`.copy-btn`): a real `<button>`, 4px/12px padding, 6px radius, 0.78rem, transparent background. Carries an `aria-label` that updates with its state.
- **Collapse toggle** (`.code-toggle`): a real `<button>` sharing the copy button's rule outright rather than restating it. Its label names the action it performs. Carries `aria-expanded` and `aria-controls`.
- **Support button** (`.support-btn`): an `<a>` styled as a button. `display: block`, centred text, 8px/12px padding, 6px radius, 0.8125rem, weight 500.

When a new control is a peer of an existing one, sitting beside it and doing the same kind of job, add it to that selector rather than writing a second rule. The toggle and Copy are pixel-identical at rest because they are literally the same declarations, which is a property that cannot drift.

Rules: use a real `<button>` for an action and an `<a>` for a navigation, never the reverse. Always set `font-family: var(--font-sans)` on a `<button>`, since it does not inherit. Always transition `color`, `border-color`, and `background` together at 0.15s ease. Never use a filled accent background: the accent is for text and borders, and a solid teal button would be louder than anything else on the page.

### Cards

One exists, the home list item. The pattern: an `<a>` wrapping the entire card so the whole surface is one focusable target with one accessible name, `position: relative` with `overflow: hidden` so a pseudo-element bar clips to the radius, a flex column with `align-items: flex-start`, and 16px padding.

Never put a second link inside a card. It would nest interactive elements and split the accessible name.

### Forms and modals

**Neither exists, and neither should.** There is no `<input>`, `<textarea>`, `<select>`, `<form>`, or `<dialog>` anywhere in the project, and no overlay, drawer, tooltip, or toast.

This is not an omission to be filled in. A form implies submission, which implies a server, which the architecture forbids. A modal implies a state layer the site does not have. If a future feature seems to need either, that is a signal to reconsider the feature. Should a genuine need ever arise, the container pattern above supplies the surface treatment, and the focus management would have to be written from scratch, since there is no library.

---

## 12b. Animation and Motion

Motion here is confirmation, never decoration. Every animation on the site tells the reader that something responded to them. Nothing moves on its own, nothing animates on load, and nothing draws attention to itself.

### Timing and easing

**One duration and one easing curve, used everywhere: `0.15s ease`.**

There is no second value. 150ms is fast enough to feel instantaneous rather than animated, which is the intent: the reader should register that the element responded, not watch it transition. Do not introduce a slower duration for a "smoother" feel, and do not add a custom cubic-bezier. A single timing across every element is what makes the interface feel like one thing.

The only other timed behaviour is the copy button's success state, which holds for **2000ms** before reverting. That is a state duration set in JavaScript, not an animation.

`scroll-behavior: smooth` is set on `html`, which applies the browser's own scroll timing. `route()` also calls `window.scrollTo(0, 0)` on every navigation, so a new view always starts at the top.

### The complete inventory

Everything that moves. If it is not on this list, it should not move.

| Element | Property | Trigger |
| --- | --- | --- |
| Sidebar nav link | `color`, `border-color`, `background` | Hover, active |
| Support button | `color`, `border-color`, `background` | Hover |
| Copy button | `color`, `border-color`, `background` | Hover, copied, copy failed |
| Collapse toggle | `color`, `border-color`, `background` | Hover |
| Prompt card | `background`, `border-color` | Hover |
| Prompt card `::before` gradient bar | `opacity` 0 to 1 | Hover |

### Rules

- **Transition only `color`, `border-color`, `background`, and `opacity`.** Never `transform`, `width`, `height`, `margin`, or `padding`. Nothing on this site should move position or change size, and layout-affecting transitions cause reflow.
- **Never transition `all`.** Name each property.
- **Reveal, do not shift.** The card's gradient bar is an absolutely positioned pseudo-element faded in with `opacity` rather than a real `border-top`, precisely so the card does not jump by 2px when it appears. Any similar treatment must follow the same approach.
- **No entrance animation.** Nothing fades or slides in on page load or on a view change. The content is already what the reader came for.
- **Show and hide, do not animate open and closed.** The collapse is `display: none`, with no height transition and no rotating chevron. Both would break the rule above: height is a layout property and a chevron needs `transform`. The state change is carried by the button's label instead, which is also the only form a screen reader can use.
- **No loading state.** There is nothing to load, so there is no spinner, skeleton, or progress indicator anywhere in the project.
- **No hover animation on non-interactive elements.** If it moves, it must be clickable.
- **`prefers-reduced-motion: reduce` disables everything** via a global `transition: none !important; animation: none !important` on all elements and pseudo-elements, plus `scroll-behavior: auto`. Because motion here is only ever confirmation and never information, nothing is lost when it is off: every animated state also changes colour or text.

---

## 12c. Notes for a Model Working on This Design

Context that is obvious to someone who has read the whole stylesheet and invisible to someone editing one rule.

**The design is inherited, not invented.** `#00d4a0`, the surface tones, the `h2::before` bar, and the interaction states all come from the Azqato brand system used across `azqato.github.io`, ComposerAtlas, and the Stocks methodology site. Changing one of them here does not make this site inconsistent with itself, it makes it inconsistent with four other sites. This is why section 13 states the accent as non-negotiable.

**Restraint is the design, not the absence of one.** There is one accent colour, one radius scale, one transition duration, one interaction idiom, and no imagery. A change that adds a second of any of those is a larger change than it appears, even when it looks locally reasonable. The correct instinct when something seems to need a new value is to check whether an existing one can carry it.

**The code block is the product, and since v1.29.0 it starts hidden.** That reads like a contradiction and is not. The page's job is to deliver one copyable block, and Copy works whether the block is shown or not, so the primary action is still one click from arrival. What collapsing removes is the several hundred lines of prompt text that used to sit between the reader and the description explaining what they were about to copy. The rule that still holds without qualification is the one that matters: **the header bar must be visible without scrolling on desktop**, and it now always is, on every prompt, at every length. Anything that pushes it down (a longer description treatment, an added metadata row, a callout) is working against the page's only job.

**Two rules are bug fixes wearing styling clothes.** `height: auto` on `.sidebar-sticky` and `flex-basis: 100%` on `.sidebar-nav`, both in the `max-width: 1023px` block, look like ordinary declarations and are not. Section 9 records what each one prevents. Do not tidy either away.

**`--content-max` is load-bearing at the breakpoint.** The `max(820px, calc(75vw - 56px))` formula is not a stylistic flourish. Simplifying it to a bare `75vw` shrinks the content on tablets rather than widening it. Section 4 explains the floor.

**`overflow: hidden` on the prompt card is structural.** It clips the gradient pseudo-element to the 10px radius. Removing it leaves a square bar overhanging two rounded corners.

**The CSS structure list in section 11 and the shell template in section 12 were both wrong until v1.28.0** and are now read from the files. They are the two blocks most likely to go stale again, because nothing checks them, so verify against `index.html` and `css/style.css` before relying on either.

**Where to change what.** A colour, font, or width: the `:root` block in `css/style.css`, and check the token is documented in section 2 of this file. A component: find its `/* Section */` banner in the stylesheet; the file is ordered by component and has no imports. Responsive behaviour: the two media queries at the bottom, and read section 9 first. Anything structural: `index.html`, all 42 lines of it.

**Verification.** There is no test, no linter, and no visual regression check. The only way to confirm a change is to open `index.html` from disk and look at it: the home list, one prompt page, the copy button, and both breakpoints. `docs/PRD.md` section 20 makes this mandatory rather than advisory.

---

## 13. What Not To Do

- No light/white backgrounds (dark theme only, consistent with Azqato brand)
- No gradient backgrounds (only gradient is the 2px top border on card hover)
- No external font loading (system fonts only)
- No external JavaScript libraries
- No syntax highlighting libraries (plain monospace text only at v1.0)
- No animations beyond: copy button state transition, sidebar link hover, prompt card hover (background, border, and gradient bar fade)
- No em dashes in any copy (see PRD.md Writing Style section)
- No decorative images or illustrations
- Do not deviate from the `#00d4a0` teal accent. It is the cross-site brand color

---

## 14. Version History

| Version | Date | Summary |
| --- | --- | --- |
| 1.9.1 | 2026-08-24 | Corrected the `index.html` line count in section 12c, which had said 31 since before the Content Security Policy was added in v1.28.0. A line count carries no intent, so it is fixed in place under the mechanical-fact exception rather than flagged. |
| 1.9 | 2026-08-24 | Specced the collapse toggle, which is the first new component since v1.0 and the third button on the site. Section 5 gains a Collapse Toggle spec and the code block header now documents the action group, the pointer cursor on the bar, and the collapsed default. Section 12a records the rule the toggle follows: a peer control joins the existing selector rather than getting a second treatment. Section 12b adds the show-and-hide rule, which is what the no-transform and no-height rules imply for a collapse. Section 12c reconciles the collapsed default with the tenet that the code block is the product. Sections 10 and 11 updated for the new control. |
| 1.8 | 2026-08-23 | Resolved both discrepancies flagged in 1.7, after the author confirmed neither preserved an intended design. The section 11 CSS structure list is now read from the stylesheet: the `.site-layout` class that never existed is gone, `.site-wrapper` is correctly described as the grid, the order matches the file, and the four omitted blocks are listed. The section 12 shell template now includes the `.sidebar-sticky` wrapper the layout depends on, plus the meta description, the nav `aria-label`, the `aria-live` region, and the new Content Security Policy, with the three load-bearing elements called out. Documented the copy button's new failed state, which is the first use of `--color-negative`. |
| 1.7 | 2026-08-23 | Documentation audit against the codebase. Added the spacing system (section 4a), component patterns (12a), animation and motion (12b), and a notes-for-a-model section (12c). Added the error and status panel component spec, which had shipped since v1.0 undocumented. Rewrote accessibility (section 10) with the WCAG target stated, a contrast table, keyboard navigation expectations, and two recorded gaps: no skip-to-content link, and a copy confirmation announced only through `aria-label`. Expanded section 9 with the full sub-1024px rule set, marking `height: auto` on `.sidebar-sticky` and `flex-basis: 100%` on `.sidebar-nav` as load-bearing v1.11.0 bug fixes. Annotated two blocks as unresolved discrepancies rather than correcting them: the CSS structure list in section 11 and the shell template in section 12. Noted that `--color-negative` and `--color-warning` remain reserved and unused. |
| 1.6 | 2026-08-23 | Built the card hover treatment that section 2 already documented: the home list items became bordered, rounded cards on `--color-surface` with a 12px gap, hovering to `--color-card-hover` with a teal to purple gradient bar across the top. `--color-card-hover` and `--color-purple` were defined but unused until now. Rewrote the Home Page Prompt List spec to match, and added the card hover to the animation allowance in section 13. Replaced the em dash in this document's title with a hyphen. |
| 1.5 | 2026-06-27 | Documented the optional `hidden: true` frontmatter key in the prompt markdown template. Hidden prompts are excluded from the sidebar and home list but remain reachable by direct link. |
| 1.4 | 2026-06-13 | Static assets reorganized into subfolders: `css/style.css` and `js/script.js`, `js/prompts-data.js`. `index.html` references updated. Shell template and CSS file structure section updated. |
| 1.3 | 2026-06-13 | Sidebar logo updated to "Azqato's Prompts.". Homepage h1 updated to "Claude Code Prompts.". Browser tab title updated to "Azqato's Prompts" on home; prompt pages show only the prompt name. Support button added to bottom of sidebar, pinned via flex column layout on `.sidebar-sticky`. |
| 1.0 | 2026-06-13 | Initial design spec. Inherited Azqato brand system. Sidebar layout, code block with copy button defined. Markdown-driven, single-shell architecture with `prompts-data.js` for dependency-free `file://` loading. Footer set to "Built by Azqato.". |
