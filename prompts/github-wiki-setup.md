---
title: GitHub Wiki Sync
description: Review every documentation file, then set up a new GitHub wiki or diff and update an existing one, curating content into a Home, Product Overview, Patch Notes, and other pages with a maintained sidebar.
meta: Claude Code Prompt
---

Sets up or updates a GitHub wiki for a repo, sourced from its existing documentation markdown files. Every markdown file in the project is reviewed first. If the wiki repo does not exist yet, it stops and asks you to create the first page through GitHub's web UI (GitHub only creates the wiki's git repo after that first manual page). If the wiki already exists, it treats the run as an update: it pulls the current pages, diffs them against the README, PRD, PATCHNOTES, DESIGN, and any other project docs, and summarizes what has gone stale (outdated sections, missing new features, stale links, drift between the wiki and the source docs) before touching anything.

Content is curated, not dumped verbatim, into a Home page with an overview and table of contents, a Product Overview page built from the stable current-state PRD sections, and a Patch Notes page condensed from the project's changelog. Beyond that fixed set, it uses judgment on wiki information architecture rather than a strict one-to-one doc mapping, creating pages like FAQ, Roadmap, Architecture, Getting Started, Troubleshooting, or API Reference wherever a topic is distinct and cohesive enough to deserve its own page. A `_Sidebar.md` page is created or kept in sync with the full current page structure. Internal planning language and engineering rationale that only make sense as internal notes are rewritten for a public audience or dropped.

## Prompt

```
Set up or update the GitHub wiki for this repo, sourced from the existing documentation markdown files. Be sure to review every single markdown file in the project before taking any action.

Step 1: Check Wiki State

Attempt git clone https://github.com/<owner>/<repo>.wiki.git
If "Repository not found": tell me to enable Wiki in repo Settings and create one placeholder page via GitHub's web UI, then stop and wait.
If it clones successfully: treat this as an update task, not a fresh build. Proceed to Step 2.

Step 2: Diff Against Current State (Update Mode Only)

Pull the existing wiki pages and compare each against current README, PRD, PATCHNOTES, DESIGN, and any other docs/site content.
Flag: outdated sections, missing new features, stale screenshots/links, and content drift between wiki and source docs.
Summarize the diff for me before editing, unless I've told you to just proceed.

Step 3: Build/Update Pages

Curate, don't dump verbatim.
Home.md: overview plus table of contents.
Product-Overview.md: stable current-state PRD sections only.
Patch-Notes.md: condensed reverse-chronological PATCHNOTES summary.
Create additional pages wherever there's a distinct, cohesive topic that doesn't belong crammed into an existing page (e.g. FAQ, Roadmap, Architecture, Getting-Started, Troubleshooting, API-Reference). Use your judgment on wiki information architecture, not just 1:1 doc mapping.
Rewrite internal/planning language into visitor-facing explanations; drop internal-only notes (dated decisions, "why X over Y" rationale).

Step 4: Sidebar

Maintain a _Sidebar.md reflecting the full current page structure.
```
