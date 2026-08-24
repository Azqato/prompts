# Azqato's Prompts

A personal library of reusable Claude Code prompts. Each one is a complete, tested instruction you can copy in a single click and paste straight into Claude Code.

Live site: [azqato.github.io/prompts](https://azqato.github.io/prompts/)

---

## What This Is

Good prompts get written once and then lost, buried in an old chat thread or a notes app nobody opens again. This site is the fix: a small, permanent shelf for the prompts that turned out to be worth keeping.

Every prompt gets its own page with a plain-language description of what it does, when to reach for it, and what it will change. Below that sits the full prompt text, tucked behind an Expand button so the description is not buried under it. Read the description, press Copy, paste it into Claude Code, and go. You do not need to expand anything first.

---

## What You Will Find Here

The library covers recurring maintenance work, the kind of task that is tedious to describe from scratch every time:

- **Documentation** rebuilds a project's entire documentation set in one pass. It reads the whole codebase first, then consolidates everything into four files and folds the full depth of a larger doc suite into a single detailed product document.
- **Mobile Audit** checks every page of a site at seven screen widths for layout bugs and overflow, fixes the underlying cause rather than the symptom, and confirms the fix by measuring the real page instead of trusting a screenshot.
- **GitHub Wiki** builds a project's GitHub wiki from its existing documentation, or diffs an existing wiki against the current docs and tells you what has gone stale before changing anything.
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
