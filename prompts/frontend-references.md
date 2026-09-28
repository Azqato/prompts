---
title: Frontend References
description: Give Claude a standing rule for when to use proven design references for style, components, motion, and demo videos, with nothing installed unasked.
meta: Claude Code Prompt
---

Claude is already good at frontend work; what it usually lacks is something concrete to aim at. This prompt writes a short standing rule into your CLAUDE.md that points it at proven outside references, each matched to the moment you get stuck: a written design system when there is no style yet, a component registry and a gallery of how mature design systems build each component when components look rough, a spring-animation library when motion feels flat, a library of real launch videos when you need a demo, and a design plugin for a final pass when something still feels off.

The rule applies only when building a new page, when you say something looks bad, or when you name one of the sites. For small changes Claude just does the work. Your project's own design system always comes first, and the references only fill what has not been decided. Nothing is installed or called without asking you, nothing is filled in from memory when a page cannot be read, and each time a reference is used Claude says which one and what it changed.

It asks whether the rule should apply to every project on your machine or only this one, shows you the exact text, and writes nothing until you confirm. Each site was checked on the date shown, with what its terms allow.

## Prompt

```
Set up a standing "Frontend references" rule in CLAUDE.md, so that you use the outside references below at the right moments in future sessions. Show me the exact text first and write nothing until I confirm.

Where it goes
- Ask me once: for every project on this machine (my user CLAUDE.md, ~/.claude/CLAUDE.md), recommended so any project can use it, or only this project (CLAUDE.md at the project root).
- If that file already has a Frontend references section, show me the difference and ask before replacing it. Leave everything else in the file untouched.

The rule to write (adapt the wording only to fit the file):

## Frontend references

Use these only when building a new page, when I say something looks bad, or when I name one of these sites. For small changes, just do the work.

The project's own design system and components come first. Outside references only fill in what has not been decided yet.

- No style yet: pick a DESIGN.md that fits the product from Refero Styles (styles.refero.design) or VoltAgent's awesome-design-md on GitHub. Save it in the project and add an @ import for it to the project's CLAUDE.md, so later work follows its colors, typography, and spacing. It sets the style only: never copy the brand it came from, its name, logo, or identity.
- Rough components: first see how mature design systems handle the same component on Component Gallery (component.gallery). Optional: 21st.dev has React and Tailwind components and an MCP for Claude Code (set up with `npx @21st-dev/cli@latest init --client claude`), but its free tier allows only a few copies a day, so ask me before installing it, and tell me what you are looking for before each call.
- Flat motion: take a ready-made prompt, CSS, or React version of a spring animation from Kinetics (kinetics.colorion.co), tuned to this project's timing.
- Demo videos: I pick reference videos on whatships (whatships.com) and send them to you. Tile their frames into one contact sheet to read the pacing and transitions, then build our own video with HyperFrames (hyperframes.dev). They are references to study, not footage to reuse: whatships links to the original posts and is not a download service.
- Still feels off when it is done: run Impeccable's polish and distill commands (impeccable.style, a Claude Code plugin: `/plugin marketplace add pbakaus/impeccable`). Ask me before installing it.

Rules:
- If an MCP, plugin, skill, or command-line tool you need is not installed, ask me whether to install it. Never imitate it yourself.
- If you cannot read a page's actual content, stop and ask me to paste it in. Do not fill anything in from memory.
- Treat a site that states no licence as reference only: learn from it, do not copy its code or assets into the project without my say-so.
- Every time you use an outside reference, tell me which one and what you changed.

Sites checked 2026-09-28: Refero Styles (2,000+ design systems, no licence stated), awesome-design-md (73 brand files, MIT, brand identities stay their owners'), Component Gallery (60 components across 95 design systems, free), 21st.dev (12,000+ components, a few free copies a day, no licence stated), Kinetics (153 spring animations, no licence stated), whatships (2,000+ launch videos, cite the original post), HyperFrames, and Impeccable (Apache 2.0). If a site has changed or gone, tell me rather than working around it.

After I confirm
- Write the section, then read the file back and show me that it is there.
- Do not install anything or call any of these sites now. The rule is for later work.
```
