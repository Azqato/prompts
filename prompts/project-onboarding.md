---
title: Project Onboarding
description: Force a full read of the codebase, structure, and documentation before any work begins, then fold everything learned into PRD.md so the understanding outlives the session.
meta: Claude Code Prompt
---

Puts the model through a complete, read-only intake of a project before it is allowed to touch anything. It maps the folder structure, reads every documentation file, traces the real entry points and data flow, catalogues conventions, and cross-checks the docs against the actual code. Everything it establishes is then merged into PRD.md, the one file it is permitted to write: additive only, matching the existing structure, preserving intent it cannot reconstruct from code, and flagging contradictions for a human to resolve rather than silently correcting them.

Use it at the start of a session on an unfamiliar codebase, when handing a project to a new model or contributor, or any time work has gone sideways because the assistant guessed at conventions instead of reading them. Because the output lands in the PRD rather than the chat, running it once pays forward into every session after it.

## Prompt

```
Before doing any work on this project, perform a complete onboarding analysis. Your only goal in this pass is to understand the project and record that understanding in the PRD.

Phases 1 through 8 are strictly read-only. Do not write, edit, refactor, rename, delete, or move any file. Do not run installers, migrations, formatters, builds that write output, or any version control command that changes state. Read-only commands and searches are encouraged. The single exception is the deliverable at the end of this prompt, which updates one file and one file only: PRD.md.

Work through every phase below in order. Do not skip a phase because it looks obvious or because you think you already know the answer. If a phase turns up nothing, say so explicitly rather than staying silent.

PHASE 1 - STRUCTURE
Map the entire repository from the root down.
- List every top-level file and folder and state what each one is for.
- Recurse into every source folder and describe what lives there. Note the depth and shape of the tree.
- Identify which folders are source, which are generated or build output, which are vendored or third-party, and which are ignored by version control.
- Read the ignore files and any editor or tooling config that shapes the workspace.
- Note the approximate file count and the largest files, and flag anything unusually large or unusually placed.

PHASE 2 - IDENTITY AND PURPOSE
Determine what this project actually is.
- What problem does it solve, and who is it for?
- What kind of artifact is it: application, site, library, service, CLI, extension, script collection, or something else?
- How does an end user reach it: a URL, an install command, an import, a binary, a double-clicked file?
- Is it in active development, maintenance, or archived? Justify the answer from evidence in the repository.

PHASE 3 - DOCUMENTATION
Read every documentation file in the project, not a sample.
- Read the README and any root-level docs in full.
- Read every file in the documentation folder or folders, whatever they are named, one by one.
- Read any instruction files intended for AI assistants, contributor guides, changelogs, patch notes, roadmaps, design docs, requirement docs, architecture notes, and inline docs in config files.
- For each document, summarize what it claims, when it appears to have last been accurate, and what it tells you about intended direction.
- Extract every explicit rule, constraint, standard, or prohibition stated anywhere in the documentation and collect them into a single list. Treat these as binding.

PHASE 4 - TECHNICAL FOUNDATION
Establish how the project is actually built and run.
- Identify the language or languages, runtime, and version requirements.
- Read the dependency manifests and lockfiles. List the significant dependencies and what each is used for. Note anything unused, duplicated, deprecated, or pinned unusually.
- Identify the build system, bundler, task runner, and every available script or command, and state exactly what each one does.
- Identify how the project is tested, linted, typechecked, and formatted, and whether those tools are actually configured or merely installed.
- Identify how and where it is deployed or published, including any continuous integration or automation configuration.
- Note the environment variables, secrets, and external services it depends on, without reading or printing any secret values.

PHASE 5 - ARCHITECTURE AND FLOW
Trace how the project actually works, from real code and not from the documentation.
- Find the true entry point or points and read them fully.
- Follow the flow from entry point through to output: what loads first, what it calls, where the main logic lives, and where the result is rendered, returned, or written.
- Identify the core modules and how they depend on one another. Call out the files that everything else depends on.
- Describe how state, data, and configuration move through the system, and where they are stored or persisted.
- Identify integration points with anything external: APIs, databases, file systems, third-party services.
- Note the architectural patterns in use and whether they are applied consistently.

PHASE 6 - CONVENTIONS
Derive the house style from the code itself, not from any style guide.
- Naming conventions for files, folders, functions, variables, classes, and constants.
- Formatting: indentation, quote style, semicolons, line length, import ordering and grouping.
- Code organization: file size norms, when logic is split out, how modules export.
- Comment and documentation density, and the format of comments in code.
- Error handling, logging, and validation patterns.
- Commit message style and branching pattern, read from the version control history.
- Where a convention is inconsistent across the codebase, say which form is dominant and which files deviate.

PHASE 7 - CROSS-CHECK
Compare the documentation against the code and report every discrepancy.
- Documented features that do not exist in the code.
- Implemented features that appear in no documentation.
- Instructions, commands, paths, or file names in the docs that are wrong or stale.
- Version numbers, dependency lists, or structure diagrams that no longer match reality.
- Contradictions between two documents.
State clearly which source you would trust for each conflict, and why. As a default, treat the code as the truth about what is, and the documentation as the truth about what is intended.

PHASE 8 - RISK AND UNKNOWNS
Be honest about the edges of your understanding.
- List the parts of the codebase you did not fully understand and say why.
- Identify fragile areas: files with no tests, complex logic, heavy coupling, obvious workarounds, or code marked with TODO, FIXME, HACK, or similar.
- Identify anything that would be dangerous to change without more context, and what would break.
- List the questions you would need answered before making significant changes.
- Note any evidence of work already in progress: uncommitted changes, unmerged branches, half-finished features, stubbed functions.

DELIVERABLE
When all phases are complete, write what you learned into PRD.md so the understanding survives this session and is available to anyone, human or model, who works on this project next. Locate the existing PRD.md first. It is usually at /docs/PRD.md, but check the root and any other documentation folder before concluding it is missing. If there is genuinely no PRD.md anywhere, create it at /docs/PRD.md.

Rules for the update, in priority order:
- Merge, do not overwrite. The PRD holds intent, decisions, rationale, and direction that cannot be reconstructed by reading code. Never delete or rewrite that content on the strength of what you found in this pass.
- Where the PRD already covers a topic and your findings agree, leave the text alone.
- Where the PRD already covers a topic and your findings contradict it, do not silently correct it. Keep the original text, add the observed reality next to it, and mark it clearly as a discrepancy for me to resolve. Code can be wrong just as easily as a document can be stale.
- Where the PRD is silent on something you established, add it.
- Match the PRD's existing heading structure, depth, tone, and formatting. If it has a house style, follow it rather than imposing this prompt's layout.
- Preserve everything that is still accurate, including sections this pass has nothing to say about.
- Do not touch any file other than PRD.md. Do not update the README, the changelog, the patch notes, or the design docs in this pass, even if you found errors in them. Report those instead.

Cover the following, using or adapting the PRD's own sections where equivalents already exist, and adding new sections only where nothing suitable is there:

1. What this project is - purpose, audience, current state, in plain language.
2. Structure - the folder map with the role of each part.
3. Stack and tooling - languages, dependencies, commands, build, test, deploy.
4. How it works - entry points and the flow through the system.
5. Conventions - the rules you will follow when writing code here, stated concretely.
6. Rules and constraints - every binding instruction found in the documentation, listed.
7. Documentation vs reality - the discrepancy list.
8. Risks and open questions - fragile areas, unknowns, and what you need from me.
9. How I will work here - the specific approach you will take on future tasks in this project, including what you will always check before editing, what you will never do, and where you will look first for any given kind of change.

When the PRD is updated, report back in the chat with a short summary only: which sections you added, which you extended, which you left untouched, every discrepancy you flagged for me to resolve, and every question you still need answered. Do not paste the full PRD back to me.

Then stop. Do not begin any implementation work. Wait for me to confirm or correct the PRD update before you change anything else.

Constraints for this pass:
- Read files rather than inferring from their names. A guess presented as a fact is a failure of this task.
- Where you are uncertain, mark it as uncertain in the PRD itself rather than smoothing it over. A confident sentence in a document outlives the session that produced it.
- Prefer evidence over assumption, and cite the file path that supports each significant claim.
- Do not pad the PRD. Every line you add should be something I could act on, or something the next person would be wrong without.
```
