---
title: Launch Video
description: Turn your project into a short launch video with music, motion, and share copy, using the /brag plugin installed once for every project.
meta: Claude Code Prompt
---

Makes a short, shareable launch video about the project you built, with its own soundtrack, sound effects, and the copy for the post that carries it. It does not build a video tool of its own: it runs `/brag`, an open-source Claude Code plugin (MIT licence, github.com/latent-spaces/brag) that reads your project's code, plans a story specific to it, storyboards it, and renders it with the Hyperframes video framework. It uses the full `/brag` workflow rather than its lighter `/brag-slim` mode.

The first time, it checks whether `/brag` is installed and, after asking you, installs it once for your user account rather than inside the project, so every project on your machine and any other prompt can use it without installing it again. It checks the tools the full workflow needs (Node.js 22 or newer, ffmpeg, and the Hyperframes command line) and asks before installing anything missing. For rendering it installs Hyperframes' own headless Chrome into the Hyperframes cache rather than using the browser already on your machine: the pinned build keeps the output the same everywhere, and Edge does not work as a substitute. Then it asks you once for the tone, format, and length, with a suggestion for each drawn from your project, and runs it. You get a `brag-output/` folder with the plan, the composition brief, the share copy, and the rendered video.

Use it when you want a launch video that tells the story of a whole project. For a looping animation of one interface morphing through its states in time with a song, use the Motion Design prompt instead.

## Prompt

```
Make a launch video for this project with the /brag plugin (github.com/latent-spaces/brag), using its full workflow. Do not build your own video pipeline or copy the plugin's files into this project: run the plugin itself.

Install, once
- Check whether /brag is already installed: run `claude plugin list` if the claude command is available to you, or look for brag in the command list. If it is, skip to Requirements.
- If it is not, tell me in two or three lines what it is (a third-party open-source plugin, MIT licence) and what it adds, and ask before installing.
- Install it at user scope, so it is available in every project on this machine and to any other prompt: run `claude plugin marketplace add latent-spaces/brag`, then `claude plugin install brag@brag`. User scope is that command's default; do not pass `--scope project` or `--scope local` unless I ask for it. If the claude command is not available to you, give me the two commands to type in the session instead, `/plugin marketplace add latent-spaces/brag` and `/plugin install brag@brag`, and tell me to choose "Install for you (user scope)".
- Plugins from this marketplace do not update themselves. Tell me once that `claude plugin update brag@brag` updates it, or that auto-update can be turned on for the brag marketplace in the Marketplaces tab of /plugin.

Requirements
- The full workflow needs Node.js 22 or newer, ffmpeg on the PATH, and the Hyperframes command line (`npx hyperframes doctor` checks it). Check each one and list what is present, with versions, and what is missing.
- Ask before installing anything that is missing, and install nothing into this project to satisfy it.
- Render with Hyperframes' own Chrome headless shell, never the Chrome or Edge already installed on this machine. After asking, run `npx hyperframes browser ensure` to install the pinned build into the Hyperframes cache, then run `npx hyperframes browser path` and check that the path it prints is inside that cache. If it points at a system browser instead, stop and tell me rather than rendering with it. Do not try Edge as a substitute: it does not work with Hyperframes' renderer.

Brief
Read the project first: its README, its main page or entry point, and its styles. Then ask me once, with your suggested default for each drawn from what you read, and wait:
- Tone: a preset (default, polished, yc-parody, chaotic, deadpan, cinematic, app-store) or a direction in my own words.
- Format: landscape, vertical, or square. Default landscape.
- Length in seconds. Default: let /brag choose, usually 15 to 25.
- Music and sound effects: on or off. Default on.
- Voiceover: on or off. Default off.
- Title. Default: inferred from the project.

Run
- Invoke /brag with --full and the options I chose, for example `/brag --full --tone polished --format vertical`. Always pass --full: on some models /brag otherwise switches to its lighter /brag-slim mode, and I want the full Hyperframes workflow. Add --voice only if I turned voiceover on, and --no-music or --no-sfx if I turned those off. When installed as a plugin the command may be listed as /brag:brag; use whichever form the command list shows.
- Let /brag do the planning, storyboarding, rendering, and share copy. Answer its questions from my brief, and ask me only what the brief does not cover.
- If /brag stops on an error, show me the error and what you think caused it, and wait rather than working around the plugin.

Afterwards
- Tell me where the video and the share copy are, show me the share copy, and say anything /brag flagged.
- brag-output/ is generated output, not part of the project's source. Tell me it exists and ask whether it should be kept out of version control.
```
