# Azqato's Prompts

A personal library of reusable Claude Code prompts. Each one is a complete, tested instruction you can copy in a single click and paste straight into Claude Code.

Live site: [azqato.github.io/prompts](https://azqato.github.io/prompts/)

---

## What This Is

Good prompts get written once and then lost, buried in an old chat thread or a notes app nobody opens again. This site is the fix: a small, permanent shelf for the prompts that turned out to be worth keeping.

Every prompt gets its own page with a plain-language description of what it does, when to reach for it, and what it will change. Below that sits the full prompt text, tucked behind an Expand button so the description is not buried under it. Read the description, press Copy, paste it into Claude Code, and go. You do not need to expand anything first. To send a prompt to someone else, copy the address from your browser: pasted into a chat or a post, it shows that prompt's own title and description.

---

## What You Will Find Here

The library covers recurring maintenance work, the kind of task that is tedious to describe from scratch every time:

- **Documentation** rebuilds a project's entire documentation set in one pass. It reads the whole codebase first, then consolidates everything into four files and folds the full depth of a larger doc suite into a single detailed product document.
- **Mobile Audit** checks every page of a site at seven screen widths for layout bugs and overflow, fixes the underlying cause rather than the symptom, and confirms the fix by measuring the real page instead of trusting a screenshot.
- **GitHub Wiki** builds a project's GitHub wiki from its existing documentation, or diffs an existing wiki against the current docs and tells you what has gone stale before changing anything.
- **Prompt Audit** is a single command rather than a block of text. It runs the built-in `claude-api` skill across a project's skills, instruction files, and prompts, and fixes the prompting patterns that were written for an older model and now hold a current one back.
- **Brand Identity** designs a complete logo system for a project, the way a branding agency would. It studies the competition, draws three concepts for you to choose from, then builds every version of the chosen logo, from a 16px favicon to a print-ready file, plus a kit of social images, color and type files, and an email signature, and presents it all on mockups in a single page and a PDF.
- **iOS Simulator** gets an iPhone or iPad app running in Apple's iOS Simulator and reviews how it looks. It installs Xcode if needed, builds and launches the app on the smallest and largest iPhones, checks every screen in dark mode and with large text, and can include iPad and the foldable iPhone Duo. It reports each problem with a screenshot and a proposed fix.
- **Game Setup** starts a three.js browser game on solid foundations: a clean project structure, a game loop that runs the same on any screen, controls for keyboard, gamepad, and touch, and sound, then builds a small playable version of the game and tests it in a real browser.
- **Motion Design** makes a short, looping product animation entirely in code: one shape morphing through interface states, from a button to a music player to a command palette, driven by an on-screen cursor in time with a song, and rendered to a video ready for social media.
- **Add Prompt** is the one that maintains this site. Hand it a raw prompt and it writes the title and description and files everything in the right places.

Each page is deliberately the same shape, so once you have read one you know exactly where to look on all the others.

---

## Who It Is For

Anyone who uses Claude Code and would rather start from a known-good prompt than rewrite one from memory. It is built and maintained as a personal reference, so it is opinionated and small rather than exhaustive, but nothing here is private and every prompt is written to work on any project, not just this author's.

---

## Status

Live and actively maintained. New prompts are added when a task proves worth saving, and existing ones are revised as they are used in anger.

---

## Learn More

Everything technical lives in [`/docs`](docs/): how the site is built, how to run it, the full design specification, and the complete change history.

- [`docs/PRD.md`](docs/PRD.md) is the single authoritative reference. It covers the architecture, setup, conventions, and the reasoning behind every rule the project follows.
- [`docs/DESIGN.md`](docs/DESIGN.md) is the visual specification.
- [`docs/PATCHNOTES.md`](docs/PATCHNOTES.md) is the running changelog.

---

## Author

**Azqato**, [azqato.github.io](https://azqato.github.io)
