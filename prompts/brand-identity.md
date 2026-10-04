---
title: Brand Identity
description: Build a complete logo system for a project: a brand brief, three SVG concepts, every lockup and icon size, a presentation, and a client deck.
meta: Claude Code Prompt
---

Runs a full brand identity project in eight phases, the way a branding agency would. It starts with a read-only pass, reading every markdown documentation file in the project (the README, `CLAUDE.md`, `PRD.md`, `DESIGN.md`, the patch notes, and any others) for anything that bears on the brand, and summarizes what it found with the source of each point. It then reads `package.json`, landing page copy, and any existing brand or style files, and fills in a brand brief, asking once for anything it cannot work out, including, optionally, a few brands, sites, or images you like as references. Next it studies five to eight competitors in the project's industry and lists the visual clichés the logo must avoid, draws three concept directions as hand-written SVG (luxury minimalism, typography first, and a symbolic mark), and stops for you to pick one or combine them. If the project already has a brand, a fourth concept evolves it, while the other three treat it only as a starting suggestion.

The chosen concept becomes a full logo system in `brand/logo/`: horizontal and stacked lockups, the symbol and the wordmark on their own, black, white, and full-color versions, a favicon, app icons, and a single-color version for print, embroidery, and stickers. Every concept and every file is rendered in headless Microsoft Edge and checked by eye for legibility at 16px, in grayscale, and on light and dark backgrounds, rather than judged from the SVG code. A brand kit follows in `brand/kit/`: social media images (a link preview, a profile picture, and X and LinkedIn banners), the colors and type as CSS and JSON files with a contrast table, an email signature logo, and a web app manifest. The favicon also switches to a lighter version in dark mode so it stays visible on dark tab bars. It finishes with `brand/presentation.html`, a single page that reveals the logo and shows it on business cards, packaging, a website, a billboard, an app icon, and merchandise, with the color palette, a type specimen, and the design rationale. The logo files themselves are always SVG, the master every other format is made from. For the mockups, put your own photos in `brand/mockups/` and it places the logo on them; without photos it builds the mockups in CSS and SVG, with perspective, shadows, and textures so they read as physical objects. The presentation is also saved as `brand/brand-guidelines.pdf`, the file to send to a printer, a freelancer, or a client.

Nothing in the project itself is changed: no favicon is linked and no header logo is swapped. Everything stays in `brand/` for you to use however you decide. The one exception is a Brand Design page where your team can preview, open, and download every brand file without opening the repository. If your site has a sign-in area for internal pages, the page goes there, with the files served through one handler that accepts only paths inside the brand folders and tests for path tricks. If the site is public with no way to restrict a page, or there is no site, it becomes an offline page, `brand/brand-design.html`, that opens by double-click and is listed in `.gitignore`, so it is never committed or published. Written documentation goes into a `## Brand Identity` section of `docs/PRD.md` (the brief, competitive analysis, and deliverables checklist) and of `docs/DESIGN.md` (the concepts, logo system specs, rationale, and usage guidelines), and anything already in either file is left alone.

It ends with `brand/index.html`, the front page of the brand folder: the whole project presented as a strategy consultancy would present it to a board, as a 16:9 slide deck with a switch to a scrolling report. Each slide states its conclusion as a full-sentence title, and every figure, color, and file on it comes from the docs and `brand/`, with a source line. It runs from an executive summary through the brief, the competitors, the concepts, the chosen logo system, color, type, the mockups, and the deliverables, to next steps, and links to the presentation and the PDF. It is committed with the rest of `brand/`, so it holds nothing private, and it prints one slide per page.

## Prompt

```
Act as a world-class brand identity designer. Build a complete logo system for this project, working like a top branding agency.

First: a read-only pass
Before anything else, open and read in full every markdown documentation file in the project, such as README.md, CLAUDE.md, docs/PRD.md, docs/DESIGN.md, docs/PATCHNOTES.md (or a CHANGELOG), and any other .md file that describes the project, so you understand the current state of the site. Skip dependency folders and build output. This pass changes nothing: do not create, edit, or move any file, and ask me nothing yet.
While reading, note everything relevant to brand design: the product and what it does, who it is for, its tone of voice, any existing logo, colors, fonts, design tokens, or style rules, what the site looks like today and which pages it has, past design or brand decisions and why they were made (the patch notes often record these), anything the docs say must not change, and any rules about where files go or how work is done here. Where two documents disagree, note both rather than choosing.
Then give me a short summary of what you found that bears on the brand, with the file each point came from, and carry it into Phase 1.

Documentation rule

All written documentation goes in two files only (create docs/ if missing):

docs/PRD.md: the "why" (brand brief, audience, competitive analysis, requirements, deliverables checklist)
docs/DESIGN.md: the "how" (concepts, chosen direction, rationale, logo system specs, usage guidelines)

If either file already exists, add or update a ## Brand Identity section instead of overwriting other content. Image and code assets still go in brand/.

Scope rule

Do not change the project's site or app. Do not link the favicon, replace a header logo, or edit anything outside brand/ and the two ## Brand Identity sections. The new identity lives only in brand/ and the presentation until I decide how to use it. The only exception is the Brand Design page in Phase 7, placed as that phase describes.

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
Gather context before asking anything: build on the read-only pass, then read package.json, the landing page copy, and any existing brand or style files it pointed you to.
Fill in this brief:
[brand name]
[core value] the logo must communicate
[audience] it targets
[idea/mission] the symbolic mark should represent
[industry] to analyze
Color or font constraints, if any
[existing brand]: if the project already has an established brand (a logo, palette, typefaces, or style guide), summarize it
[references]: optional, 2 to 5 brands, sites, or images I like. Read what you can, ask me for screenshots of anything you cannot open, and tell me which qualities you are taking from each (such as spacing, type, color, or motion) rather than copying any one. Suggest "none" as the default.
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

All concepts must communicate [core value], target [audience], and avoid the Phase 2 clichés. Save SVGs to brand/concepts/ and run the render check on each. Document each concept (intent, shapes, palette, type) in docs/DESIGN.md under ## Brand Identity > Concepts. Before presenting them, check each concept, and later the brand kit, against these: it has one focal point; every gradient, glow, texture, or effect in it has a job (it carries meaning, hierarchy, or recognition), and anything that has none is removed rather than restyled; and it could not be pasted onto an unrelated brand unchanged. Fix what fails, and note what you removed. Summarize the concepts and ask me to pick one (or combine) before continuing.

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
A contrast table in docs/DESIGN.md under ## Brand Identity > Color Contrast, listing each text and background pair with its WCAG contrast ratio, computed with a script from the hex values rather than estimated, and whether it passes AA
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

Phase 7: Brand Design showcase page

Once Phases 1 to 6 are done, build a Brand Design page so the team can browse, open, and download every brand file without opening the repository. Do not ask whether to build it. Brand working files are not for the public, so choose its form from the project:

- Gated page: if the site or app has a founders-only, admin-only, or other signed-in area for internal pages, put the page there, behind the same access check, and add a nav link or tab named "Brand Design" next to the related internal pages. Follow every section below.
- Offline page: if the site is public with no way to restrict a page (for example a static site), or the project has no site or app with pages, build brand/brand-design.html instead: one self-contained file that opens by double-clicking, with no server, no handler, and nothing loaded from the network. It shows the same sections and tiles as below, linking to each file by a relative path inside brand/. A file opened from disk cannot read its folder, so list the files as they are when you write the page, and say at the top of the page that running this phase again refreshes the list. Add brand/brand-design.html to the project's .gitignore (create the file if there is none, adding only this line), so the page is never committed or published; tell me you did. Skip "Serving the files safely" and the handler tests, and do not link the page from the site.
- Tell me which form you chose and why.

What it shows
- A short intro line: "The files the brand identity work created, from brand/ in the repository. Click a file to open it, or download it."
- One section per brand folder, in this order, each with a heading and a one-sentence blurb:
  1. Logo system (brand/logo): the symbol, wordmark, and lockups, with favicons and app icons.
  2. Brand kit (brand/kit): social images, the email signature, and the color and type tokens.
  3. Render checks (brand/checks, PNGs only): each logo file rendered to confirm it draws correctly.
  4. Other brand images: any other brand design files in the project, so nothing made over time is missed, including files from an earlier run of this prompt or from other work. Look in the rest of brand/ (such as brand/concepts, brand/mockups, brand/brand-guidelines.pdf, and brand/presentation.html) and in the site's own asset folders for logos, symbols, wordmarks, favicons, app and touch icons, share and link-preview images, social banners, and web manifests. Skip dependency folders, build output, and caches, and list only files that exist now: do not restore deleted files from git history. Group them by where they live, and show each file's path under its name so the team can find it.
  Match the names to the folders this work actually created, and skip empty folders (or show "No files found.").
- A responsive grid of tiles in each section (grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)), with a 1rem gap). Each tile has:
  - A 150px-high preview area. SVG, PNG, ICO, JPG, and WebP files show as an img with object-fit: contain and loading="lazy". Other files (CSS, JSON, webmanifest) show their extension as a large label in the accent color.
  - Files meant for dark backgrounds (names containing "white" or "reversed") get the brand's dark background in the preview, so white logos stay visible. The rest get white.
  - The whole preview links to the file, opening in a new tab.
  - A caption row with the file name (long names wrap) and a Download link with the download attribute.
- Files listed alphabetically within each section. On the gated page, read them from disk when the page is requested, so new brand files appear without code changes.

Serving the files safely (gated page only)
- Copy the brand folders into the build output (for example a Content/brand folder) so the deployed site has them, since the repository is not on the server. Use the project's own build or deploy step for this. Copy the files found for Other brand images into that folder too, under brand/other/ with their original paths kept below it, so the handler never needs to reach outside the brand folders.
- Serve them through one handler protected by the page's access check, in whatever form the framework uses (for example ?handler=File&path=brand/logo/x.svg, or a route like /brand-design/file?path=...). Do not put them in the public static folder.
- The handler accepts only paths under the brand folders. It rejects "..", absolute paths, and anything that resolves outside those folders after normalizing, and returns 404 for anything else or any missing file.
- Set the content type from the extension: image/svg+xml, image/png, image/x-icon, image/jpeg, image/webp, text/css, application/json, and application/manifest+json.
- Add tests in the project's test framework: a real brand file is served; an empty path, a path outside the brand folders, a ../ traversal, a lookalike folder such as brandx/, and a missing file all return 404. If the project has no tests yet, tell me and ask before adding a test setup.

Styling
- Use the site's existing tokens (surface, line, radius, accent) so the page matches the rest of the site, not the new brand's palette unless the site already uses it. The offline page, which has no site around it, uses the new brand's own palette and typeface from brand/kit/tokens.css, inlined. Tiles: a 1px border in the line color, the site's radius, the surface background, and overflow: hidden.
- It must work at phone width with no horizontal scroll.

Finish
- Update the project's PRD and patch notes (or changelog) with the new page. Mention a gated page in the README's feature list; for an offline page, record in the PRD that it exists, where, and that it is ignored.
- Check it locally in a headless browser, never against the live site: every section renders, dark tiles show white logos, and a download works. For a gated page, also check that a signed-out visitor is refused, and run the new tests. For an offline page, also check it works opened straight from disk and that git status does not list it.

Phase 8: Brand overview deck (brand/index.html)

Last, build brand/index.html: the front page of brand/, presenting the whole project the way a top strategy consultancy presents to a client's board. It summarizes everything this work created and links to presentation.html for the full reveal; it does not replace it. It is committed with the rest of brand/, so it holds nothing private: no internal addresses, no link to a gated page, and no names of people the docs do not already publish.

Read before writing: the ## Brand Identity sections of docs/PRD.md and docs/DESIGN.md, and a listing of brand/ made with a command. Every number, hex value, file name, and claim on the page comes from those. Leave out anything you cannot find rather than filling it in.

Format: a 16:9 slide deck by default, with a "Read as report" switch that shows the same content as one scrolling page.
- Deck view: one slide at a time, scaled to fit the window at 16:9, letterboxed, never cropped or scrolled. Left and Right arrows, Page Up and Page Down, Space, Home, and End move between slides, and on-screen Previous and Next buttons do the same. Show "n / total" and a thin progress bar. The address hash records the slide (#slide-4), so a link opens on it and the Back button works.
- Report view: the same slides stacked as full-width sections, readable at 375px wide with no horizontal scroll. The switch is a button with aria-pressed, the choice is remembered in localStorage (inside try/catch), and screens under 700px wide open in report view.
- Print: one slide per landscape page, with the controls hidden.

Slide style, as in consulting decks:
- Every slide has an action title: one full sentence stating the slide's conclusion, such as "The mark stays legible from a 16px tab to a billboard", never a topic label such as "Scalability".
- A small tracker in the top corner names the section. A footer carries the brand name, "Brand identity", and the slide number. A source line under each exhibit names the doc or file it came from.
- One idea per slide, generous white space, and the brand's own palette and typeface from brand/kit/tokens.css (inlined, with the same Google Fonts link presentation.html uses). No decoration without a job.
- Exhibits are real: logos are the SVG files from brand/, swatches show hex values and the contrast table's ratios, and comparisons are tables rather than prose.

Slides, in this order. Skip one only when its source does not exist, and say which:
1. Title: the logo, the brand name, "Brand identity", and today's date from the system clock.
2. Executive summary: three to five full-sentence conclusions covering the challenge, the chosen direction, why it wins, and what was delivered.
3. The brief: core value, audience, mission, and industry in a 2x2 grid.
4. Competitive landscape: a table of the Phase 2 competitors with their shapes, colors, and type, the clichés to avoid, and the one-sentence positioning.
5. Concepts explored: the concepts side by side, each with its intent in one line and the chosen one marked.
6. The chosen direction: the logo large, with the rationale as three numbered points.
7. Logo system: the lockups, symbol, and wordmark on light and dark.
8. Scalability: the mark at 16, 32, and 512px and in grayscale, from the render checks.
9. Color: the palette with hex values and the AA results from the contrast table.
10. Typography: a specimen with the typeface, its license, and its fallbacks.
11. In use: two or three mockups from presentation.html, with a link to it.
12. Deliverables: the checklist from docs/PRD.md as a table of item, file, and status, including anything that could not be produced and why.
13. Next steps: three to five recommendations for rolling out the identity (for example linking the favicon or swapping the header logo), each with its effort, and each marked as my decision under the scope rule.
14. Appendix: links to presentation.html, brand-guidelines.pdf, tokens.css, tokens.json, and site.webmanifest. Never link brand/brand-design.html, which is not committed.

Check it before reporting: open brand/index.html from disk in headless Edge at 1920x1080 and 1280x720 in deck view and at 375px wide in report view, screenshot every slide, and look at each one. Nothing overflows its slide, every action title fits on two lines, every logo and swatch renders, and all text meets WCAG AA against its background, with the ratios computed by a script. Then check that the keys move the slides, a #slide-n link opens that slide, the switch changes the view and is remembered after a reload, and printing to PDF gives one slide per page. Fix and re-check anything that fails. Record the page in docs/DESIGN.md under ## Brand Identity > Brand Overview and in the deliverables checklist in docs/PRD.md, then report what you checked and anything you could not check.
```
