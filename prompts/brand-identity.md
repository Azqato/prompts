---
title: Brand Identity
description: Build a complete logo system for a project: a brand brief, three SVG concepts to choose from, every lockup and icon size, and a presentation page.
meta: Claude Code Prompt
---

Runs a full brand identity project in six phases, the way a branding agency would. It reads the project first (the README, `CLAUDE.md`, `PRD.md`, `DESIGN.md`, `package.json`, landing page copy, and any existing brand or style files) and fills in a brand brief, asking once for anything it cannot work out. It then studies five to eight competitors in the project's industry and lists the visual clichés the logo must avoid, draws three concept directions as hand-written SVG (luxury minimalism, typography first, and a symbolic mark), and stops for you to pick one or combine them. If the project already has a brand, a fourth concept evolves it, while the other three treat it only as a starting suggestion.

The chosen concept becomes a full logo system in `brand/logo/`: horizontal and stacked lockups, the symbol and the wordmark on their own, black, white, and full-color versions, a favicon, app icons, and a single-color version for print, embroidery, and stickers. Every concept and every file is rendered in headless Microsoft Edge and checked by eye for legibility at 16px, in grayscale, and on light and dark backgrounds, rather than judged from the SVG code. A brand kit follows in `brand/kit/`: social media images (a link preview, a profile picture, and X and LinkedIn banners), the colors and type as CSS and JSON files with a contrast table, an email signature logo, and a web app manifest. The favicon also switches to a lighter version in dark mode so it stays visible on dark tab bars. It finishes with `brand/presentation.html`, a single page that reveals the logo and shows it on business cards, packaging, a website, a billboard, an app icon, and merchandise, with the color palette, a type specimen, and the design rationale. The logo files themselves are always SVG, the master every other format is made from. For the mockups, put your own photos in `brand/mockups/` and it places the logo on them; without photos it builds the mockups in CSS and SVG, with perspective, shadows, and textures so they read as physical objects. The presentation is also saved as `brand/brand-guidelines.pdf`, the file to send to a printer, a freelancer, or a client.

Nothing in the project itself is changed: no favicon is linked and no header logo is swapped. Everything stays in `brand/` for you to use however you decide. Written documentation goes into a `## Brand Identity` section of `docs/PRD.md` (the brief, competitive analysis, and deliverables checklist) and of `docs/DESIGN.md` (the concepts, logo system specs, rationale, and usage guidelines), and anything already in either file is left alone.

## Prompt

```
Act as a world-class brand identity designer. Build a complete logo system for this project, working like a top branding agency.

Documentation rule

All written documentation goes in two files only (create docs/ if missing):

docs/PRD.md: the "why" (brand brief, audience, competitive analysis, requirements, deliverables checklist)
docs/DESIGN.md: the "how" (concepts, chosen direction, rationale, logo system specs, usage guidelines)

If either file already exists, add or update a ## Brand Identity section instead of overwriting other content. Image and code assets still go in brand/.

Scope rule

Do not change the project's site or app. Do not link the favicon, replace a header logo, or edit anything outside brand/ and the two ## Brand Identity sections. The new identity lives only in brand/ and the presentation until I decide how to use it.

Guiding principles (apply to every phase)
Style should feel premium, timeless, and globally recognizable.
Avoid trends; focus on longevity.
Think Apple x Nike level simplicity.
Keep it simple enough to be recognized at a glance, but meaningful enough to tell a story.
Must look equally strong at small and large sizes.
Stand out while still feeling credible in the industry. Avoid clichés used by competitors.

Render check (used in Phases 3 to 6)
Judge every logo from a rendered image, never from the SVG code. Build a contact sheet page in brand/checks/ that shows the logo at 16, 32, and 512px, in full color and in grayscale (CSS filter: grayscale(1)), on a light and a dark background. Screenshot it with headless Microsoft Edge (use Chrome if Edge is not installed), for example:
msedge --headless --disable-gpu --hide-scrollbars --window-size=1200,900 --screenshot=brand/checks/<name>.png brand/checks/<name>.html
Then open the screenshot and look at it. Fix anything that blurs, fills in, disappears, or loses balance, and check again.

Phase 1: Brand foundation
Gather context before asking anything: read README, CLAUDE.md, PRD.md, DESIGN.md, package.json, landing page copy, and any existing brand or style files.
Fill in this brief:
[brand name]
[core value] the logo must communicate
[audience] it targets
[idea/mission] the symbolic mark should represent
[industry] to analyze
Color or font constraints, if any
[existing brand]: if the project already has an established brand (a logo, palette, typefaces, or style guide), summarize it
If any field is still unknown, ask me in ONE message with suggested defaults, then wait.
Save the brief to docs/PRD.md under ## Brand Identity > Brand Brief.

Phase 2: Competitive edge
Analyze top brands in [industry] (5 to 8; use web search if available, otherwise your knowledge, and say which).
Note their shared shapes, colors, and type styles, then list the clichés used by competitors that this logo must avoid.
State in one sentence how [brand name] will stand out while still feeling credible in that space.
Save to docs/PRD.md under ## Brand Identity > Competitive Analysis.

Phase 3: Three concept directions

Hand-write clean, optimized SVG for each (no raster images, no embedded fonts):

A. Luxury minimalism: a minimalist, high-end logo. Use clean geometry, balanced spacing, and a restrained color palette: one or two colors plus black and white, taken from the brief's color constraints if there are any. Think Apple x Nike level simplicity.
B. Typography first: a typography-driven logo. Set [brand name] in an open-license typeface that suits the brief (such as one from Google Fonts), then make it its own with one or two custom details, such as a cut, a ligature, or a shape in the negative space. Focus on kerning and negative space. Convert the lettering to paths if a tool for that is installed (such as fonttools or opentype.js); otherwise reference the typeface by name. Record the typeface and its license in docs/DESIGN.md. The logo should feel iconic even without a symbol.
C. Symbol plus meaning: a symbolic mark that represents [idea/mission]. Simple enough to be recognized at a glance, but meaningful enough to tell a story.

If the brief found an [existing brand], add a fourth concept:
D. Evolved: the existing brand refined, keeping its current guidelines and format while expanding them wherever that helps.
In that case A, B, and C take the existing brand only as a suggestion and go in whatever direction serves the brand best.

All concepts must communicate [core value], target [audience], and avoid the Phase 2 clichés. Save SVGs to brand/concepts/ and run the render check on each. Document each concept (intent, shapes, palette, type) in docs/DESIGN.md under ## Brand Identity > Concepts. Summarize the concepts and ask me to pick one (or combine) before continuing.

Phase 4: Scalability (logo system for the chosen concept)

Create a logo system that works across all formats: favicon, app icon, website header, merchandise. Must look equally strong at small and large sizes. Produce in brand/logo/:

Primary horizontal lockup (website header), stacked lockup, symbol only, wordmark only
Monochrome black, monochrome white (reversed), full color
favicon.svg (switching to a lighter variant under prefers-color-scheme: dark, so it stays visible on dark tab bars), favicon.ico (16, 32, and 48 in one file), and favicon 16, 32, 48 PNG
App icon 180, 192, 512, 1024 PNG, plus maskable 192 and 512 versions for Android. Keep the mark inside the central 80% so rounded and masked crops never cut it, and give the 1024 icon a solid background with no transparency, since the App Store rejects transparent icons.
Merchandise-ready single-color version (for print, embroidery, stickers), with no line or gap thinner than about 1mm at the smallest size it will be stitched or cut
Clear space and minimum size rules

For the PNG and ICO files, use sharp, rsvg-convert, ImageMagick, or similar if installed. If none is, render each PNG in headless Edge from a page sized exactly to the icon, adding --default-background-color=00000000 for a transparent background. List any file that still cannot be produced in the deliverables checklist, with the command that would generate it.

Verify: run the render check on every file and confirm each is legible at 16px, works in grayscale, and is balanced on light and dark backgrounds. Fix and re-check any failure. Record the chosen direction, file inventory, sizes, clear space, and minimum size rules in docs/DESIGN.md under ## Brand Identity > Logo System, and add a deliverables checklist to docs/PRD.md.

Phase 5: Brand kit

Produce in brand/kit/, rendering each image from SVG with the same tools as Phase 4 and running the render check on it:

Social images: a 1200x630 link preview (og-image.png), a 400x400 profile picture that still works cropped to a circle, an X header at 1500x500, and a LinkedIn banner at 1584x396. Keep the logo clear of the areas each site covers with the profile picture.
tokens.css with the palette as CSS custom properties and the typeface with its fallbacks, and tokens.json with the same values
A contrast table in docs/DESIGN.md under ## Brand Identity > Color Contrast, listing each text and background pair with its WCAG contrast ratio and whether it passes AA
Email signature logo: a PNG at twice its display size (for example 400x100 to show at 200x50) that reads well in both light and dark mail clients, since most email clients do not display SVG
site.webmanifest with the brand name, theme color, background color, and the 192 and 512 icons from brand/logo/ (created but not linked from the project, per the scope rule)

Record the kit's file inventory in docs/DESIGN.md under ## Brand Identity > Brand Kit, and add it to the deliverables checklist in docs/PRD.md.

Phase 6: Presentation (the secret)

Present the logo like a $500,000 brand project. Create brand/presentation.html (a single file of CSS and SVG; its only external link is the brand typeface loaded from Google Fonts, and its only images are my photos in brand/mockups/, referenced by relative path):

Hero reveal of the logo
Show it on mockups: business cards, packaging, website, billboard (plus app icon and merchandise). If I have placed mockup photos in brand/mockups/, set the logo onto them, matching each photo's perspective and lighting. Otherwise build the mockups in SVG/CSS and make them feel physical, not flat: 3D perspective tilts, soft layered shadows, paper, card, and fabric textures, and lighting gradients. Do not download images from anywhere else.
Color palette with hex values and a type specimen
A short rationale explaining design choices and brand positioning, including how it communicates [core value] and stands apart from competitors

Give the page print styles (@media print) so each section starts on a new page. Screenshot the finished page in headless Edge and review it, then save it as brand/brand-guidelines.pdf with headless Edge (--print-to-pdf) and check that the pages break cleanly. Also copy the rationale into docs/DESIGN.md under ## Brand Identity > Rationale, and add ## Brand Identity > Usage Guidelines covering usage, misuse, spacing, colors (hex values), and fonts.
```
