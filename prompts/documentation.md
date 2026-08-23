---
title: Documentation
description: Scan the entire codebase, then consolidate all documentation into four core files, packing every supporting doc, the house conventions, and the writing style into a deeply sectioned PRD.
meta: Claude Code Prompt
---

Crawls the full codebase first, then audits and consolidates all documentation into four core files: README.md at the root, and PRD.md, DESIGN.md, and PATCHNOTES.md inside `/docs`. Missing files are created and the correct folder structure is enforced. The PRD absorbs everything else, with required sections for Tenets, Roadmap, Metrics, Runbook, Technical Requirements, Conventions, Writing Style, Security, Deprecation and Removal, Documentation Versus Reality, Risks and Open Questions, Working Practice, a Press Release, and an FAQ, so the entire project can be understood from `/docs` alone without reading any code.

Use it when a project needs one authoritative, exhaustive doc set in a single pass. Rather than spreading detail across a suite of ten or more separate documents, it folds that full depth into a single comprehensive PRD, so there are only ever four files to keep current. It also derives the house conventions from the code, cross-checks the docs against reality, records risks and open questions, and enforces the writing style, so a project does not need a separate onboarding or style pass. Every policy it writes is a default, applied only where the project does not already state a rule of its own.

## Prompt

```
Perform a full documentation audit of the /docs folder. Your goal is to ensure every document accurately reflects the current state of the codebase with no gaps, outdated information, or missing coverage.
Steps to follow:

Steps 1 through 3 are strictly read-only. Do not write, edit, refactor, rename, delete, or move any file. Do not run installers, migrations, formatters, builds that write output, or any version control command that changes state. Read-only commands and searches are encouraged. Writing begins at step 4, and is limited to the documentation files named in this prompt. Do not skip a step because it looks obvious or because you think you already know the answer, and if a step turns up nothing, say so explicitly rather than staying silent.

1. Crawl the entire codebase and build a complete picture of what exists: all files, features, components, routes, configs, and logic.
2. Open every document in /docs one by one, and read each in full.
3. For each document, compare its content against the actual codebase and identify anything that is outdated, missing, inaccurate, or incomplete.
4. Rewrite or update each document so it is fully accurate and comprehensive based on the current version of the site.
5. Do not skip any document. Every single file in /docs must be reviewed and updated.
6. After all documents are updated, provide a summary of what changed in each file and why.

Standards to uphold:

Every document should be thorough enough that a new contributor or AI model can understand the project entirely from the /docs folder alone.
If a document is missing a section that the codebase clearly warrants, add it.
Merge, do not overwrite. Documentation holds intent, decisions, and rationale that cannot be reconstructed by reading code. Where a document already covers a topic and the code agrees, leave the text alone. Where the code contradicts it, do not silently correct the document: keep the original text, add the observed reality next to it, and mark it as a discrepancy for the author to resolve. Code can be wrong just as easily as a document can be stale.
Every policy in the specifications below is a default. Where the project already states a rule of its own on that topic, in its docs, a contributing guide, or a consistent pattern in the code and changelog, document that rule and leave it alone. Adopt the default only where no rule exists, and where an existing rule and a default differ, keep the existing rule and flag the difference rather than silently replacing one with the other.
Read files rather than inferring from their names. A guess presented as a fact is a failure of this task. Where you are uncertain, mark it as uncertain in the document rather than smoothing it over: a confident sentence outlives the session that produced it.
Be thorough. In /docs, and in PRD.md above all, completeness beats brevity. A section that restates context to stand on its own is doing its job, not padding, because the reader may arrive at it directly and should not have to assemble the answer from three other sections. When in doubt, include it. The cost of a document that says too much is a longer read; the cost of one that says too little is someone guessing, and guessing is what this whole exercise exists to prevent.
This is not licence for filler. Do not write marketing language, do not restate the obvious to fill space, and do not add a sentence that carries no information the reader did not already have. Thorough means more facts, not more words around the same facts. The README is the exception to all of this and stays tight, since everything it omits is one link away.

Make sure to perform a full codebase scan before touching any documentation.

1) Consolidate all of the files in docs into 4 main documents: README.md, /docs/PRD.md, /docs/DESIGN.md, /docs/PATCHNOTES.md

2) Create any missing documentation files and populate them accordingly.

3) Enforce the following folder structure:

   /project-root
   ├── README.md          ← Important: README.MD is always root only, never inside /docs
   └── /docs
       ├── PRD.md
       ├── DESIGN.md
       └── PATCHNOTES.md

   If any of these files exist outside of /docs (except README.md), move them into
   /docs. If /docs does not exist, create it.

---
README.md - The front door. First thing anyone sees. Explains what the project is and how to use it.
PATCHNOTES.md - A running log of every change made, with dates and reasons why.
DESIGN.md - How it looks. Colors, fonts, spacing, and UI rules to stay consistent.
PRD.md - What you're building and who it's for. You should be so detailed that it is easy to understand everything about the entire project without having to review any code. This file should also contain additional sections consolidating all of the documentation files you are removing from this audit in order to keep track of the overall direction of the project accurately from all perspectives. 

---

### README.md (root)
The README is the public front door for the project. Write it for a
general reader, not a developer. This holds for every project regardless
of type: developers are served by /docs/PRD.md, which carries the stack,
the setup, and the deploy process in full. The README never has to
compromise for them.

Required sections:
- Project name and a one or two sentence description of what the site is
- Link to the live site, or a plain statement that there is no hosted
  instance, so a reader is never left looking for a link that does not exist
- What the site offers: main sections or features, described in plain
  language and what a visitor gets from each
- Who it is for
- Current status (live, in progress, archived)
- Where to learn more: link to /docs for setup, architecture, and all
  technical documentation

Rules:
- No install steps, commands, ports, env vars, or build instructions.
  Those belong in /docs.
- No version numbers or dependency lists.
- Plain descriptive language. Clear and factual, not salesy.
- Be as thorough as possible while ensuring readability. The README is the
  one document where brevity wins a tie: it is read by people deciding
  whether to care, and everything it leaves out is in /docs.

---

### /docs/DESIGN.md
Required sections:
- Design philosophy: 1-3 sentences on the visual and UX direction
- Color palette: every color token with hex value and intended use
- Typography: font families, sizes, weights, and line heights for each text role
  (heading 1-3, body, caption, label, code)
- Spacing system: the spacing scale used (e.g. 4px base unit)
- Breakpoints: every responsive breakpoint and what changes at each
- Component patterns: rules for how recurring UI elements (buttons, cards, forms,
  modals) should be built and styled
- Accessibility standards: WCAG level targeted, contrast requirements, keyboard
  navigation expectations
- Animation and motion: timing, easing, and rules for when motion is appropriate
- Any additional information an AI model would find relevant when it comes to understanding the design philosophy behind the website.

---

### /docs/PATCHNOTES.md
Required format per entry:
- Version number using semantic versioning (MAJOR.MINOR.PATCH)
- Date in YYYY-MM-DD format
- Sections: Added, Changed, Fixed, Removed
- Each line item is one change, written in past tense

If no prior changelog exists, create an initial entry for the current state of
the project labeled as v0.1.0 or the nearest appropriate version.

---

### /docs/PRD.md
Required sections:
- Problem statement: what problem does this product solve and for whom
- Target users: specific personas with context on their needs
- Goals: what success looks like for this product
- Non-goals: explicit list of what this product will not do
- User stories: written as "As a [user], I want to [action] so that [outcome]"
- Feature list: split into MVP (must ship) and Future (post-launch)
- Constraints: technical, time, budget, or platform limitations
- Assumptions: decisions made without full information that the team accepts as true
- Success criteria: measurable outcomes that confirm the product is working
Additional sections:
Tenets
- 3-7 tenets maximum. More than 7 dilutes the value.
- Each tenet has a short title (3-5 words) and a 2-4 sentence explanation.
- Tenets must be opinionated enough to resolve a real product tradeoff.
  A tenet that everyone agrees with without hesitation is not useful.
- Order them by priority. When two tenets conflict, the higher one wins.
Roadmap
- Current phase: name and brief description of where the product is now
- Milestone table: each milestone has a name, target date or relative
  timeframe, and a status (Planned, In Progress, Complete, Blocked)
- Feature breakdown per milestone: bullet list of what ships in each phase
- Explicitly deferred items: features considered but intentionally pushed
  out with a short reason why
Metrics
- North star metric: the single number that best represents if the product
  is delivering value
- Acquisition metrics: how users find and start using the product
- Engagement metrics: how users interact with the product over time
- Retention metrics: whether users come back
- Performance metrics: technical health indicators (load time, error rate,
  uptime)
- Targets: a specific goal value for each metric and a timeframe
- Measurement method: what tool or method captures each metric
- Reporting cadence: how often each metric is reviewed
Runbook
This section carries everything a developer needs to run the project, since
the README deliberately does not. Assume the reader has just cloned the
repository and has nothing else.
- Prerequisites: runtime and version, package manager, and any system
  requirement, each with the version the project actually needs rather than
  the newest available
- Local setup: complete steps to get the project running from a fresh
  machine. Installation commands in the exact order they must be run, the
  command that starts it, and the default port it serves on
- Build: exact command to produce a production build and where the
  output goes
- Deploy: step-by-step deploy process for each environment (staging,
  production). Include any manual steps that are not automated.
- Rollback: how to revert to the previous working version
- Environment configs: list of environments and what differs between them
- Environment variable reference: every key name, what each one does, and
  whether it is required or optional. Never the values themselves
- Common errors: a table of known errors, their likely cause, and the
  fix
- Monitoring: where to check logs, errors, and uptime alerts
Technical Requirements
- System architecture: describe how the system is structured at a high level
  (client/server, serverless, static, etc.)
- Tech stack: every language, framework, library, and tool used with versions
- Folder structure: annotated tree of the project directory
- Data models: every major data type, its fields, types, and relationships
- API design: all endpoints or functions, their inputs, outputs, and error states.
  If browser-only, document the internal data flow instead.
- State management: how application state is managed and where it lives
- Third-party integrations: every external API or service used, what it does,
  and how it is authenticated
- Performance requirements: target load times, bundle size limits, rendering targets
- Known technical debt: any shortcuts taken with a note on what the correct
  solution would be
Conventions
Derive the house style from the code itself, not from any style guide the project
happens to contain. Where the two differ, record both and say which is dominant.
- Naming: files, folders, functions, variables, classes, and constants.
- Formatting: indentation, quote style, semicolons, line length, import ordering.
- Organization: file size norms, when logic is split out, how modules export.
- Comment density and format, and what earns a comment in this codebase.
- Error handling, logging, and validation patterns.
- Commit message style and branching pattern, read from the version control
  history rather than from any contributing guide.
- Where a convention is inconsistent, say which form is dominant and which files
  deviate, so the next contributor matches the majority rather than the last file
  they happened to open.
Writing Style
Record the project's rule for prose in its docs, UI copy, and code comments. If
the project already states one, document it. If it does not, adopt this default
and write it in:
- Em dashes are prohibited in all three forms: the literal Unicode character, the
  &mdash; HTML entity, and the double dash used as punctuation. The Unicode
  character and the entity must be searched independently, because a search for
  one will not catch the other. CSS custom properties (--color-bg and the like)
  are valid syntax, not punctuation, and are never touched.
- Replace each instance with whichever alternative fits the context: a comma (the
  most natural in most cases), a colon (introducing a list or elaboration after a
  complete clause), a semicolon (joining two closely related independent clauses),
  parentheses (asides and supplementary detail), a period (splitting one sentence
  into two), or a single hyphen.
- The single hyphen is permitted and encouraged where context justifies it. The
  prohibition does not cover it, and it is the closest visual match to the em dash
  it replaces, so prefer it in document titles, section headings, and version
  lines (for example "## v1.2.0 - 2026-01-01") where a comma or colon reads
  awkwardly. In running prose the other replacements are usually better.
- Leave any instance the text needs in order to mean anything, such as a rule, a
  table, or an example naming the character it prohibits. Replacing those destroys
  the line.
- Tone: direct and functional, plain declarative sentences, no marketing language,
  no filler openings.
Apply the writing style to every document you write in this audit. Then sweep the
rest of the project's text for violations and fix those too, and record in the
patch notes how many were found and where.
Security
- Authentication model: how users are identified and sessions are managed
- Authorization model: what different user roles can and cannot do
- Data storage: what user data is stored, where, and how it is protected
- Environment variables: confirm no secrets are hardcoded; list all
  variables that must be set in the environment and never committed
- Third-party trust: list every third-party service that receives user
  data and what data it receives
- Known attack surface: any areas of the app with elevated risk and
  what mitigations are in place
- Dependency policy: how dependencies are monitored for vulnerabilities
Deprecation and Removal
- Removal policy: first check whether the project already has a removal rule of its
  own, stated in its docs, in a contributing guide, or established by a consistent
  pattern in the changelog and the code. If it does, document that rule and leave it
  alone. This audit records how the project works, it does not overrule how the
  project has decided to work. Where an existing rule and the default below differ,
  keep the existing rule and note the difference so the author can decide, rather
  than silently replacing one with the other.
  Only where the project states no rule, adopt this default and write it into the
  PRD as the policy. Whether a removal needs a redirect is decided by whether the
  thing being removed is public facing, not by the fact that it is being removed.
    - Public facing: the deployed artifact and the addresses it serves. A live
      URL or route, a published package, an exported name other code imports.
      Removing one retires the address behind a redirect, alias, or equivalent
      compatibility shim pointing at whatever replaces it, so the old address
      keeps resolving.
    - Internal: the source that builds the artifact, and anything else not
      reachable from outside. Source files are not public facing even when their
      names appear in a built URL, because the name is derived from the source
      rather than being the contract. Removing one is a plain delete. No
      redirect, no alias, no stub file, no tombstone. Nothing external is
      pointing at it, so there is no address to preserve, and a permanent
      compatibility entry would be maintenance in exchange for nothing.
  Draw the line at the deploy boundary, and say in the PRD where the project puts
  it, because a reader cannot apply the rule without knowing which side a given
  file is on.
  Adapt the mechanism to whatever the project actually has (a router redirect
  map, a server rewrite rule, a deprecated re-export), and record the reasoning
  alongside the rule so it is not relitigated later. If the project has no
  redirect mechanism at all, say so, and state what it does instead.
- Public surface: list what is publicly addressable, item by item. This list is
  whichever policy applies is applied against, so it has to be specific enough to
  answer the question for any given file rather than gesturing at categories.
- Compatibility entries: where the project has them, state that they are
  permanent, are never chained (a redirect always resolves to a real target in
  one hop), and are never reused to point at different content later, since a
  reused address silently serves the wrong thing, which is worse than a broken
  link.
- Retired items: what has been removed, when, and what replaced it. A reader
  who finds a reference to something that no longer exists should be able to
  resolve it here.
- Historical records are not rewritten when something is removed. Changelog
  entries and version history rows that describe a deleted item stay as they
  are, because they record what happened at the time rather than describing the
  current state.
Documentation Versus Reality
Compare every document against the actual code and record each discrepancy rather
than quietly fixing it. Treat the code as the truth about what is, and the
documentation as the truth about what was intended.
- Documented features that do not exist in the code.
- Implemented features that appear in no documentation.
- Instructions, commands, paths, or file names in the docs that are wrong or stale.
- Version numbers, dependency lists, or structure diagrams that no longer match.
- Contradictions between two documents.
For each, state which source you would trust and why. Keep resolved entries in the
table with a note on how they were resolved, so the record shows what was found and
what was decided, not just the current state.
Risks and Open Questions
Be honest about the edges of the analysis. This section is worth more than the
confident parts of the document.
- Parts of the codebase you did not fully understand, and why.
- Fragile areas: files with no tests, complex logic, heavy coupling, obvious
  workarounds, and anything marked TODO, FIXME, or HACK.
- Anything dangerous to change without more context, and what would break.
- Work already in progress: uncommitted changes, unmerged branches, half-finished
  features, stubbed functions.
- Open questions for the author, numbered so they can be answered by reference.
  When one is answered, fold the answer into the relevant section and record it
  here as answered rather than deleting it.
Working Practice
The approach anyone, human or model, should take on future work in this project.
Written as concrete instructions, not principles.
- What to always check before editing, and which document to read first for which
  kind of change.
- What never to do here, with the reason attached, so the rule survives contact
  with someone who thinks they have a good exception.
- Where to look first for each kind of change, as a table mapping the kind of work
  to the file to open.
- How to verify a change, including the exact command or manual check, and what to
  update afterwards (patch notes, version history).
Press Release
- Written as if the product has just launched publicly. Include
  product name, what it does, who it is for, the key benefit, and a mock quote
  from a fictional user. Written for a general audience, no jargon.
- Headline - one sentence naming the product and its core benefit, written as a live published announcement
- Subheadline - expands on the headline with one added detail or hook
- Dateline - city and release date
- Opening paragraph - covers who, what, when, where, and why in 3 to 5 sentences
- Problem statement - the specific pain point being solved, written from the customer perspective
- Solution description - how the product solves it, in plain non-technical language
- Customer quote - fictional but realistic quote from a named target persona
- Call to action - what the reader should do next (sign up, visit, download)
- Company boilerplate - one short paragraph describing the organization
Frequently Asked Questions
- External FAQ: 10-25 questions a real user would ask. Cover how it works,
  what it costs, what data it uses, and what it does not do.
- Core definition and target audience
- Step by step usage summary
- Pricing and availability - cost, tiers, launch date, and regions
- Technical requirements - integrations, compatibility, and dependencies
- Competitive differentiation - how it differs from existing alternatives
- Known limitations - what the product does not do in v1
- Support and onboarding - how users get help and ramp up
- Internal stakeholder questions - ROI rationale, success metrics, and roadmap direction

---

After everything is updated, add these recent changes to PATCHNOTES.md and describe this process and how everything should be handled moving forward in PRD.md.
```
