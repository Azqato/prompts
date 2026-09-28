---
title: Score to Target
description: Name a bar like 8 out of 10. Claude writes the rubric, scores each item from real evidence, and improves the weakest round by round until all pass.
meta: Claude Code Prompt
---

Turns "make it better" into a number that has to be earned. You name the bar, such as "get everything to 8 out of 10" or "bring anything under 6 up to 6". Claude writes the scoring rubric down before scoring anything, so an 8 means the same in the last round as in the first, breaks each item into three to five criteria worth up to two points each, and measures whatever can be measured instead of judging it.

It scores every item on its own, from the real thing (a render, a recording, a test run, a measurement), never from the code or from memory, and it scores the starting point first so the improvement can be shown. Then it works in rounds: the lowest items first, the criterion costing the most points in each, re-scored with the same rubric. It never rounds a 7.5 up to an 8, never raises one score by lowering another or by breaking a test, and stops honestly, reporting any item that cannot reach the bar and why.

It works on anything that can be judged: pages, components, animations, game assets, copy, or a set of prompts.

## Prompt

```
Score the work I point you to out of 10 and improve it until it reaches the bar I set. If I have not named the items, the bar, or what I compare against, ask me once, then continue.

1. Pin down the bar and the items
- Restate the bar and whether it applies to every item or to the average. "Get them to 8" means every item reaches 8.
- List every item to be scored, one by one, never as a single blob.
- Name the benchmark I judge against (sites, games, or products I mention). If I name none, say what you are comparing against.

2. Write the rubric before scoring
- Use these anchors: 10 best in class; 9 excellent, almost nothing to fault; 8 polished and intentional, minor nits only; 7 good with one noticeable flaw; 6 acceptable, works and reads clearly with rough edges; 5 the idea is there but the execution distracts; 3 to 4 clearly broken in places; 1 to 2 barely works.
- Break each kind of item into three to five criteria worth 0 to 2 points each, so every point has a reason.
- Wherever a criterion can be measured, measure it (a size, a time, a count, a contrast ratio, a pass rate) rather than judging it.
- Show me the rubric before the first round.

3. Score from evidence
- Score from the real thing: rendered pages, recordings, test results, or measurements. Never from reading the code or from memory. Capture each item's state before scoring it.
- Score the starting point before changing anything.
- Be your own harshest judge: look for failures first, and never round up. A 7.5 on an 8 bar is below the bar. If I ask for independent judging and your tools allow it, have a fresh reviewer who did not do the work score from the captures and the rubric alone, and take the lower score where you disagree.

4. Improve in rounds
- Fix the lowest items first, and within each, the criterion losing the most points.
- After each round, capture again and re-score with the same rubric. Show me the scores moving, for example "Header 5 to 7 to 8".
- Do not trade away tests, performance, or other items' scores to lift one number. Note any trade-off you made.
- Stop when every item meets the bar, or when an item stops improving because of something outside this task (a missing asset, a hard limit). Report that item as short, with the reason and what it would take.

5. Report
- Lead with the result, for example "All 12 now score 8 or better; 7 started below 8."
- A table: item, score before and after, and the main fault fixed or the reason it is still short.
- How it was scored: the rubric, the benchmark, who judged, and from what evidence. Say which criteria were measured and which were judged.
- Offer to save the scorecard in the project so later rounds start from it, and, where a bar can be checked by a test, offer to add that test. Do neither unless I say yes.
```
