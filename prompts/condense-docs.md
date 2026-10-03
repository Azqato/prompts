---
title: Condense Docs
description: Shrink your project's docs to what is true now: one home for every fact, history moved to the patch notes, and a table proving nothing was lost.
meta: Claude Code Prompt
---

Makes a project's documentation shorter without making it poorer. Docs grow by addition: every change adds a "since version 1.4" sentence, a fact gets restated in three files, finished roadmap items keep their full write-up, and the copies drift apart. This prompt reads every document, finds the repeats and the history, and rewrites each document to describe the project as it is now, with each fact kept in one place and linked from the others. What happened in the past moves to the patch notes, or is confirmed to be there already. The reasons behind decisions stay, in a line, because a rule without its reason gets undone. Before anything is removed, it builds a table that maps every cut passage to where its information now lives, and checks that table with a script, so you can see that nothing was lost. It shows you the plan first and changes nothing until you say yes, and it records the commit it started from so the whole pass can be undone. It reorganizes and shortens only; it does not check the docs against the code, which is what the Documentation prompt is for.

## Prompt

```
Condense this project's documentation: make every document shorter and simpler while keeping all of its information. This is not an audit against the code. Do not read source code except to find scripts that read the docs, or, if I agree in step 2, to settle a number two copies disagree on (a line count, a file list). Do not change what any rule or fact says, only where it lives and how many words it takes.

Rules for the result
- Docs describe the present. A sentence about how something used to be, or when it changed ("since v1.4", "previously", "was moved from"), becomes a plain statement of how it is now. The history belongs in the changelog (patch notes, CHANGELOG.md, or similar).
- One home for every fact. When the same fact appears in more than one place, keep it in the document it belongs to and replace the other copies with a short link to it. Where copies disagree, do not pick one: list the conflict under Questions and leave both.
- Keep the reasons. "We do X because Y broke" stays, cut to one line, even though it describes the past: without it, someone will undo X.
- Keep what looks like history but is still a rule: retired addresses and their redirects, names that must never be reused, deprecations still in force, and dated decisions other text depends on.
- Finished roadmap items move to a short Done list (title, version, and a link to the changelog entry) and lose their full write-up, once the changelog holds what they said. Open items stay as they are.
- The changelog itself is not condensed: it is the record. Only fix entries that are broken or duplicated outright.
- Leave alone, word for word: CLAUDE.md and any other file of instructions for an AI agent, licence text, rules quoted exactly from elsewhere, and anything marked as not to be edited.
- Plain, short sentences. Cut filler and repeated explanation, never facts, numbers, names, paths, or conditions.

0. Make it undoable
- If the project uses git, run git status and note the current commit. If any documentation file has uncommitted changes, stop and ask me to commit or stash them first, so this pass is one clean diff. Never commit, stash, or reset yourself.
- If it does not use git, copy every documentation file to a folder outside the project before step 3, and say where.

1. Read (nothing changes yet)
- List every documentation file: README, everything in docs/, CHANGELOG or patch notes, contributing guides, and any other prose file meant for people. Read each in full.
- Find any script, build step, or tool that reads these docs (for example one that parses a roadmap table or a version line). Note the exact formats it depends on; those must survive unchanged. Where it is safe to run, run it now and save what it reports (counts of rows, entries, or items), to compare afterwards.
- Find the docs' own rules about history: any rule that says to keep resolved items, mark rather than delete answered questions, prefer completeness, or never remove old text. Each one conflicts with this prompt; list it as a question, and do not override it without my answer.
- Measure each file: lines, words, and characters.

2. Plan, then wait
- Build the ledger: a table with one row for every passage you would remove or move. Columns: file and section, a short quote of the passage, what kind it is (duplicate, history, dated audit result, finished roadmap item, filler), and where its information lives afterwards (file and section, or "changelog vX.Y.Z", or "nothing: filler, no information"). A history passage whose changelog entry is missing gets one written, and the ledger says so. A pattern that repeats (for example forty "since vX" phrases) may be one row, with its count and the sections it appears in.
- A version history table that repeats the changelog row for row is a duplicate: propose replacing it with the current version and a link to the changelog.
- Where removing a structure (a table, a list, a section) would leave an instruction that writes to it, such as "add a row to the version history", list that instruction too, and how it changes.
- Also list the conflicts between copies, the passages you kept as rules or reasons and why, and the formats that scripts depend on.
- Ask, as a standing question, whether to fix each conflict to what the code shows, or to leave both copies as they are.
- Show me the ledger, the expected size of each file afterwards, and the questions. Then stop and wait for my yes. Change nothing before it.

3. Rewrite
- Apply the plan, one file at a time. Move each piece of information to its home before removing it from anywhere else.
- Update every instruction that wrote to a removed structure. If it is in a file you must leave alone, such as CLAUDE.md, do not edit it: list it under Questions.
- Keep each document's existing headings where a script or a link depends on them. Where you rename or merge a heading that other files link to, update those links.
- Bump each document's version line, if it has one, and add one changelog entry for this pass, dated from the system clock, saying the docs were condensed and nothing was removed.

4. Prove nothing was lost
- With a script, not by eye, check every ledger row: the destination exists, and the key terms of the passage (names, numbers, paths, versions) appear there. Match case-insensitively and on short distinctive terms, so a changed word ending does not fail a row. Fix any row that fails and rerun until every row passes.
- Check with a script that every version or date mentioned in removed history has an entry in the changelog.
- Check with a script that every internal link, anchor, and section reference still resolves, looking up a reference to another document's section in that document. Run each script that reads the docs and compare its counts with the ones saved in step 1; a difference is a failure unless the ledger explains it.
- Search the result for history phrasing left outside the changelog ("since v", "previously", "used to", "was changed"), and either rewrite each hit or say why it stays.

Limits
- Write only documentation files. Do not edit source code, install anything, or run any version control command that changes state.
- Do the work yourself in this session, with no subagents.

Report
1. Each file's size before and after, in lines and words, the total saved, and how far each differs from the estimate in step 2.
2. How to undo it: the starting commit, with git diff <commit> -- <file> to review and git checkout <commit> -- <file> to restore one file (or the folder of copies, without git).
3. The ledger, with each row marked as checked.
4. The facts that had more than one copy, and where each now lives.
5. Anything kept that looks like history, and why.
6. Questions, numbered so I can answer by number: each conflict between copies, and anything you were unsure how to classify, with what you did meanwhile.
```
