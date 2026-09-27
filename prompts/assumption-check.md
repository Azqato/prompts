---
title: Assumption Check
description: Have Claude list what it assumes about your code, marked verified or guessed, check the cheap guesses, and propose fixes without changing anything.
meta: Claude Code Prompt
---

Makes Claude show its working before it changes code. It lists every assumption it is making about the codebase that affects the task at hand, such as which framework version is in use, how the tests run, or where a feature lives, and marks each one as verified, meaning it read the code that shows it and names the file and line, or guessed, meaning it inferred it and says from what. Guesses are where most bugs start, so any guess that is cheap to check by reading a file is checked straight away and moved to verified or wrong.

For everything still guessed or found wrong, it proposes the smallest fix or check that would settle it and says what would break if the assumption is wrong. The list is sorted so the wrong and guessed items come first. It is read-only: nothing is edited, installed, or run that changes anything, and it stops for your review. Use it before a large change, or mid-session when Claude seems to be working from a picture of the code that does not match yours.

## Prompt

```
Before changing anything, list every assumption you are making about this codebase that affects the task we are working on. If there is no task yet, cover the parts of the code you have read.

For each assumption:
- State it in one sentence.
- Mark it verified (you read the code that shows it: give the file and line) or guessed (you inferred it: say from what).
- If a guessed one is cheap to check by reading a file or running a read-only command, check it now and mark it verified or wrong.

Then, for every assumption still guessed or found wrong, propose the smallest fix or check that would settle it, and say what breaks if it is wrong.

Sort the list: wrong first, then guessed, then verified. Keep each verified item to one line.

This is read-only. Do not edit any file, install anything, or run anything that changes state. Stop and wait for my review.
```
