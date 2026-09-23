---
title: Brand Identity
description: Build a complete logo system for a project: a brand brief, three SVG concepts to choose from, every lockup and icon size, and a presentation page.
meta: Claude Code Prompt
---

Runs a full brand identity project in five phases, the way a branding agency would. It reads the project first (the README, `CLAUDE.md`, `PRD.md`, `DESIGN.md`, `package.json`, landing page copy, and any existing brand or style files) and fills in a brand brief, asking once for anything it cannot work out. It then studies five to eight competitors in the project's industry and lists the visual clichés the logo must avoid, draws three concept directions as hand-written SVG (luxury minimalism, typography first, and a symbolic mark), and stops for you to pick one or combine them.

The chosen concept becomes a full logo system in `brand/logo/`: horizontal and stacked lockups, the symbol and the wordmark on their own, black, white, and full-color versions, a favicon, app icons, and a single-color version for print, embroidery, and stickers. Each is checked for legibility at 16px, in grayscale, and on light and dark backgrounds. It finishes with `brand/presentation.html`, a self-contained page that reveals the logo and shows it on business cards, packaging, a website, a billboard, an app icon, and merchandise, with the color palette, a type specimen, and the design rationale.

Written documentation goes into two files only. The brief, competitive analysis, and deliverables checklist go into a `## Brand Identity` section of `docs/PRD.md`, and the concepts, logo system specs, rationale, and usage guidelines into the same section of `docs/DESIGN.md`. Anything already in either file is left alone. The PNG favicon and app icon sizes are only produced if an image converter such as `sharp` or `rsvg-convert` is already installed.

Before running, replace `$ARGUMENTS` on the Input line with the brand name and anything you already know about the brand, or leave it and the prompt will ask. It pauses twice: once if the brief has gaps, and once for you to choose a concept.

## Prompt

```
Act as a world-class brand identity designer. Build a complete logo system for this project, working like a top branding agency.

Documentation rule

All written documentation goes in two files only (create docs/ if missing):

docs/PRD.md: the "why" (brand brief, audience, competitive analysis, requirements, deliverables checklist)
docs/DESIGN.md: the "how" (concepts, chosen direction, rationale, logo system specs, usage guidelines)

If either file already exists, add or update a ## Brand Identity section instead of overwriting other content. Image and code assets still go in brand/.

Input from the user: $ARGUMENTS

Guiding principles (apply to every phase)
Style should feel premium, timeless, and globally recognizable.
Avoid trends; focus on longevity.
Think Apple x Nike level simplicity.
Keep it simple enough to be recognized at a glance, but meaningful enough to tell a story.
Must look equally strong at small and large sizes.
Stand out while still feeling credible in the industry. Avoid clichés used by competitors.

Phase 1: Brand foundation
Gather context before asking anything: read README, CLAUDE.md, PRD.md, DESIGN.md, package.json, landing page copy, and any existing brand or style files.
Fill in this brief:
[brand name]
[core value] the logo must communicate
[audience] it targets
[idea/mission] the symbolic mark should represent
[industry] to analyze
Color or font constraints, if any
If any field is still unknown, ask me in ONE message with suggested defaults, then wait.
Save the brief to docs/PRD.md under ## Brand Identity > Brand Brief.

Phase 2: Competitive edge
Analyze top brands in [industry] (5 to 8; use web search if available, otherwise your knowledge, and say which).
Note their shared shapes, colors, and type styles, then list the clichés used by competitors that this logo must avoid.
State in one sentence how [brand name] will stand out while still feeling credible in that space.
Save to docs/PRD.md under ## Brand Identity > Competitive Analysis.

Phase 3: Three concept directions

Hand-write clean, optimized SVG for each (no raster images, no embedded fonts; convert letterforms to paths where possible):

A. Luxury minimalism: a minimalist, high-end logo. Use clean geometry, balanced spacing, and a restrained color palette (black, white, gold accents). Think Apple x Nike level simplicity.
B. Typography first: a typography-driven logo. Focus on custom letterforms, kerning, and negative space. The logo should feel iconic even without a symbol.
C. Symbol plus meaning: a symbolic mark that represents [idea/mission]. Simple enough to be recognized at a glance, but meaningful enough to tell a story.

All concepts must communicate [core value], target [audience], and avoid the Phase 2 clichés. Save SVGs to brand/concepts/. Document each concept (intent, shapes, palette, type) in docs/DESIGN.md under ## Brand Identity > Concepts. Summarize the three and ask me to pick one (or combine) before continuing.

Phase 4: Scalability (logo system for the chosen concept)

Create a logo system that works across all formats: favicon, app icon, website header, merchandise. Must look equally strong at small and large sizes. Produce in brand/logo/:

Primary horizontal lockup (website header), stacked lockup, symbol only, wordmark only
Monochrome black, monochrome white (reversed), full color
favicon.svg plus favicon 16, 32, 48 PNG; app icon 180, 512, 1024 PNG (use sharp, rsvg-convert, or similar if installed)
Merchandise-ready single-color version (for print, embroidery, stickers)
Clear space and minimum size rules

Verify: legible at 16px, works in grayscale, balanced on light and dark backgrounds. Fix and re-check any failure. Record the chosen direction, file inventory, sizes, clear space, and minimum size rules in docs/DESIGN.md under ## Brand Identity > Logo System, and add a deliverables checklist to docs/PRD.md.

Phase 5: Presentation (the secret)

Present the logo like a $500,000 brand project. Create brand/presentation.html (self-contained, CSS and SVG only):

Hero reveal of the logo
Show it on mockups built in SVG/CSS: business cards, packaging, website, billboard (plus app icon and merchandise)
Color palette with hex values and a type specimen
A short rationale explaining design choices and brand positioning, including how it communicates [core value] and stands apart from competitors

Also copy the rationale into docs/DESIGN.md under ## Brand Identity > Rationale, and add ## Brand Identity > Usage Guidelines covering usage, misuse, spacing, colors (hex values), and fonts.
```
