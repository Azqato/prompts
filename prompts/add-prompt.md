---
title: Add Prompt
description: Add a new prompt to the site by providing the raw prompt text: Claude Code generates the title, description, and updates all required files.
meta: Claude Code Prompt
---

Takes a raw prompt text and handles the full addition workflow: generates the title and one-line description, creates the markdown file in `prompts/`, mirrors it into `prompts-data.js`, adds it to the prompt list in `README.md`, and adds a version entry to `docs/PATCHNOTES.md`.

Use it when adding any new prompt to the site. Paste the prompt text below the `Prompt:` label before running.

## Prompt

```
Add this new prompt to the website. Make sure to follow the process listed in @README.md @docs/PRD.md @docs/DESIGN.md @docs/PATCHNOTES.md . Update documentation accordingly and patch notes:

Title: Generate a title based on the prompt that I have provided.

Description: Generate a description based on the prompt that I have provided.

Prompt:
```
