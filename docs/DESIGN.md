# DESIGN.md - Prompts

**Version:** 1.6
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
| `--color-negative` | `#f85149` | Error states (unused at v1.0) |
| `--color-warning` | `#ffa657` | Caution callouts (unused at v1.0) |
| `--color-purple` | `#bc8cff` | Gradient accent on card hover top border |

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
  border-bottom: 1px solid --color-border
  padding: 10px 16px
  display: flex, justify-content: space-between, align-items: center
  Left label: "Prompt" in --color-text-secondary, 0.8rem
  Right: Copy button (see below)

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
```

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

Transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease
```

JavaScript behavior: on click, use `navigator.clipboard.writeText()` to copy the `<code>` element's text content. Set button to "Copied!" state, then reset after 2000ms.

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

| Breakpoint | Changes |
| --- | --- |
| `< 1024px` | Sidebar becomes top nav bar, backdrop blur, bottom-border active state |
| `< 768px` | h1 reduces to 1.5rem, h2 reduces to 1.2rem, padding reduces to 20px/16px, code block font-size reduces to 0.8rem |

---

## 10. Accessibility

- All color combinations meet WCAG AA contrast minimums (primary text ~15:1, muted text ~4.8:1)
- Copy button includes `aria-label="Copy prompt to clipboard"` and updates `aria-label` to "Copied!" on activation
- Focus styles preserved on all interactive elements (`focus-visible` outline in `--color-accent`)
- `prefers-reduced-motion` disables transition animations
- Code block uses `<pre><code>` semantics; screen readers treat it as preformatted content

---

## 11. CSS File Structure

```
css/style.css structure (in order):
  :root (CSS variables)
  Reset / base
  Layout (site-wrapper flex, site-layout grid)
  Sidebar
  Main content
  Footer
  Typography (h1, h2 with ::before bar, h3, body, lead, caption)
  Prompt page (title block, description block)
  Code block (wrapper, header bar, pre, code)
  Copy button (default, hover, copied states)
  Home page prompt list (items, links, descriptions)
  Hero / intro section
  Media queries (tablet < 1024px, mobile < 768px)
  Reduced motion
```

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
  <link rel="icon" href="data:image/svg+xml,...">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div class="site-wrapper">
    <aside class="sidebar">
      <a class="sidebar-logo" href="#/">Azqato's Prompts<span class="accent-dot">.</span></a>
      <nav class="sidebar-nav" id="sidebar-nav"></nav>
      <div class="sidebar-support">
        <a href="https://azqato.github.io/support.html" target="_blank" rel="noopener noreferrer" class="support-btn">Support</a>
      </div>
    </aside>
    <main class="content" id="content"></main>
  </div>
  <footer>
    <p>Built by <a href="https://azqato.github.io">Azqato</a>.</p>
  </footer>
  <script src="js/prompts-data.js"></script>
  <script src="js/script.js"></script>
</body>
</html>
```

`prompts-data.js` must load before `script.js`. It defines `window.PROMPTS_DATA`, an array of `{ slug, raw }` objects where `raw` is the verbatim text of a `prompts/*.md` file.

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
| 1.6 | 2026-08-23 | Built the card hover treatment that section 2 already documented: the home list items became bordered, rounded cards on `--color-surface` with a 12px gap, hovering to `--color-card-hover` with a teal to purple gradient bar across the top. `--color-card-hover` and `--color-purple` were defined but unused until now. Rewrote the Home Page Prompt List spec to match, and added the card hover to the animation allowance in section 13. Replaced the em dash in this document's title with a hyphen. |
| 1.5 | 2026-06-27 | Documented the optional `hidden: true` frontmatter key in the prompt markdown template. Hidden prompts are excluded from the sidebar and home list but remain reachable by direct link. |
| 1.4 | 2026-06-13 | Static assets reorganized into subfolders: `css/style.css` and `js/script.js`, `js/prompts-data.js`. `index.html` references updated. Shell template and CSS file structure section updated. |
| 1.3 | 2026-06-13 | Sidebar logo updated to "Azqato's Prompts.". Homepage h1 updated to "Claude Code Prompts.". Browser tab title updated to "Azqato's Prompts" on home; prompt pages show only the prompt name. Support button added to bottom of sidebar, pinned via flex column layout on `.sidebar-sticky`. |
| 1.0 | 2026-06-13 | Initial design spec. Inherited Azqato brand system. Sidebar layout, code block with copy button defined. Markdown-driven, single-shell architecture with `prompts-data.js` for dependency-free `file://` loading. Footer set to "Built by Azqato.". |
