---
title: Project Defaults
description: Give any project clear house rules and a ready docs folder in one quick pass, while keeping every rule and document it already has.
meta: Claude Code Prompt
---

Sets up the ground rules and the documentation skeleton a project needs, without the full review the Documentation prompt does. It puts the four documents and the ideas list in place with their headings, writes the standing rules (patch notes on every change, when to test, how to handle secrets, licensing, and the rest) into the PRD, and adds the root files a site needs. Anything the project has already decided wins: its own rules and documents are kept exactly as they are, the defaults only fill the gaps, and any clash is listed for you rather than changed. It reads no source code and checks nothing against it, so it is quick on any project; the sections it cannot write without that review get a placeholder heading, ready for a Documentation run later.

## Prompt

```
Set up this project's standing rules and documentation structure, using sensible defaults. This is not an audit: do not review the codebase, and do not check existing documents against the code. The project's own rules and documents are the source of truth. The defaults only fill the gaps.

The defaults are defined in the Documentation prompt. Before writing anything, fetch it and read it in full, word for word: https://raw.githubusercontent.com/Azqato/prompts/main/prompts/documentation.md. If your fetch tool summarizes or shortens pages, get the raw text another way, such as curl. If you cannot read it in full, stop and tell me. Use its folder structure, required sections, templates, and policy wording exactly. Do not run its audit steps.

Run the whole setup in one pass without stopping to ask me anything. Where a decision is needed, take the default. Where there is none, take the most conservative option: keep existing text, and create, move, or delete nothing that cannot easily be undone. Do all the work yourself in this session, with no subagents.

1. Find what already exists (read-only)
- List the files at the project root and in /docs. Read in full: README.md, CLAUDE.md, every file in /docs, any contributing guide, the licence file, .gitignore, .gitattributes, robots.txt, and sitemap.xml, where each exists. Read the main manifest only for the project's name and type.
- Decide whether the project serves a site (it has pages a browser loads, or a deploy config for one). If you cannot tell, treat it as not serving one and say so.
- For each policy listed in step 3, note whether the project already has a rule on that topic, in its docs, CLAUDE.md, or a contributing guide. Read no source code beyond this step.

2. Put the structure in place
- Create /docs if it is missing. Leave existing files where they are: do not move, merge, rename, or delete any document, including one that the Documentation prompt would move into /docs. List those under Questions instead.
- For each of README.md, docs/PRD.md, docs/DESIGN.md, and docs/PATCHNOTES.md: if it does not exist, create it with every required section from the Documentation prompt as a heading, each followed by one line: "Not yet written. A Documentation run fills this in." If it exists, add only the required headings it lacks, with the same line, and change none of its existing text.
- Fill in what needs no review: the project name, and in the README, the live site link or a plain statement that there is no hosted instance, where the files you read give it. Mark anything you are unsure of as uncertain.
- docs/TODO.md: if missing, create it with the exact template the Documentation prompt gives. If an ideas list exists elsewhere, leave it and list it under Questions.
- docs/PATCHNOTES.md: if it has no entries, add a first one, v0.1.0 unless the project already states a version, dated from the system clock, recording this setup.
- CLAUDE.md: do not create one if it is missing. If it exists, leave it unchanged.

3. Write the standing rules into docs/PRD.md
For each policy below, if the project has its own rule, record that rule under the heading and leave it as it is. If it has none, write in the Documentation prompt's default for it.
- Writing Style (record the rule only; do not sweep the project's text for violations)
- Browser Testing
- Verification Environment
- Testing Cadence
- Repository Hygiene (a policy record only; do not create or edit an ignore file)
- Licensing. Create LICENSE.md at the root only where the project has no licence of any kind, under the default posture. An existing licence file stays exactly where it is.
- Social Sharing Tags and Page Titles, only where the project serves a site. Record the rule; do not edit any page.
- Deprecation and Removal
- Working Practice, including the docs/TODO.md rule, the verification checklist rule, and each rule in CLAUDE.md, with a line saying CLAUDE.md is the copy Claude reads and the two change together
- Under the Roadmap, a verification checklist listing every PRD and DESIGN.md section that describes the code, each marked not yet verified
Where a project's rule and a default differ, keep the project's rule and list the difference under Questions. Never replace one with the other.

4. Root files for a site
Only where the project serves a site:
- robots.txt, if missing: fully open (User-agent: * and Allow: /) with a comment marking that as deliberate, as the Licensing policy describes.
- sitemap.xml, if missing: create it only if the pages a visitor can reach without signing in can be listed from the file listing alone, using the site address the files you read name. Otherwise create none, and list it under Questions.

Limits
- Write only the files this prompt names. Do not edit source code, install anything, or run any version control command that changes state.
- Never put a secret, key, or password into any file.

Check, then report
- Check with a script, not by eye, that every required file exists and every required heading is present in each document. Fix anything missing and rerun until the check passes.
- Then report, in this order:
  1. Files created, and headings added to existing files, one line per file.
  2. Policies: which kept the project's own rule and which took the default.
  3. Anything you marked uncertain, and why.
  4. The script check's result.
  5. Questions, numbered so I can answer by number: each difference between a project rule and a default, each document left outside /docs, and anything else you decided without me, each with the default you took meanwhile.
- End by saying that the placeholder sections are filled by a Documentation run, which also checks the documents against the code.
```
