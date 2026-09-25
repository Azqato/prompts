---
title: Motion Design
description: Create a looping UI motion video entirely in code: one shape morphing through interface states in time with a song, driven by a cursor.
meta: Claude Code Prompt
---

Makes a short, looping product animation of the kind usually built in After Effects, entirely in code. One shape never cuts away: it morphs from a button into a loader, a music player, a slider, tabs, a chart, a command palette, and back, with an on-screen cursor clicking and dragging to drive every change, all in time with a song. It is useful for showing off a product's interface on social media or on a landing page, and it can use your project's own components, colors, and font.

It asks first for the eight to twelve interface states, a color scheme, a royalty-free song you supply, the format (square, 16:9, or 9:16), and the length. It then analyzes the song's beat grid and shows you every state placed on a beat before writing any code. Everything on screen is computed from the time alone, using spring physics rather than keyframes, so any frame can be rendered exactly and the last frame matches the first for a seamless loop. A preview page lets you scrub through it in a browser with the music playing.

Before the full render it produces a contact sheet with one frame per beat and fixes anything off the beat, cramped, or hard to read. The final video is rendered frame by frame in a headless browser with motion blur, mixed with the song and synthesized interface sounds, and saved as a 60fps MP4 that plays on X, Instagram, and LinkedIn. It needs Node, Python, and ffmpeg, asks before installing anything, and works in its own folder if the project's docs forbid build tools or dependencies.

## Prompt

```
Create a looping UI motion design video, rendered entirely from code: one shape that morphs through a sequence of interface states in time with a song, driven by an on-screen cursor.

Start
Read the README, CLAUDE.md, and docs/ if they exist. If this project has its own UI, note its components, colors, and font: they can become the states and the style. Check the docs for rules this work would break (such as no npm dependencies or no build tools), quote each with its file and line, and ask whether to update the docs, work in a separate folder (motion/ by default), or stop.
Then ask me in ONE message, with your suggested default for each, and wait:
- 8 to 12 UI states for the shape to become. Suggest states from this project's own UI if it has one; otherwise suggest from: button, loader, check, dynamic island, music player, progress scrubber, volume slider, toggle, tabs, chart with tooltip, command palette, toast.
- Color: pure black and white, or one accent color (this project's accent, if it has one).
- The song: a royalty-free track around 120 BPM that I supply as a file, with a license that allows how I will use the video. Do not download music yourself.
- Format: square 1440x1440 (default), 16:9 at 1920x1080, or 9:16 at 1080x1920. Length: the number of bars, 7 by default.
- Font: Geist by default (open font license, installed locally from the @fontsource/geist package), or this project's UI font.
If my answers leave the states, their order, or the interaction in each unclear, ask a short follow-up rather than inventing them.
Once you have the song, analyze its beat grid (see Audio), then show me the state list placed on the beat grid, one line per beat, before you write any code. Wait for my approval.

Direction
Polished product UI motion. One shape, never cut: every state is the same element morphing its size, corner radius, and color while its content swaps with a short blur. A cursor drives every change with real clicks and drags. Light warm-gray canvas, black and white components (plus the accent, if chosen), one clean UI font. Springs everywhere, with a tiny overshoot at most. The camera zooms so each state fills the frame. The last frame is the first frame, so it loops.
Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon stroke widths, dead time, and anything that looks like a template.

Structure
Something happens on every beat. Each state gets the beats it needs to read clearly: a morph in, one interaction (a click, a drag, typing), and a morph out. Transitions land on beats, and big changes land on downbeats. Example path at 120 BPM over 7 bars: button → loader → check → dynamic island → music player with a play/pause morph → scrub the progress bar → it becomes a volume slider that stretches when dragged past its maximum → a toggle flips on the beat → the knob becomes a liquid tab indicator → the tabs open into a chart that draws itself, with a tooltip on hover → it collapses into a ⌘K command palette → type to filter → enter → toast → back to the button.

Build
1. One HTML file at the chosen size. Every style is computed from time inside seek(t): no CSS transitions, no CSS animations, no timers, no state carried between frames. Calling seek(t) for any t, in any order, must produce the same frame.
2. Springs are closed-form step responses. A value that changes target many times is the sum of one spring per change, so it stays a pure function of time. Tune stiffness and damping for at most a tiny overshoot.
3. The tab indicator's two edges ride different springs, so the leading edge stretches ahead of the trailing one. Use the same trick for the toggle knob.
4. Drags are direct manipulation: while the cursor is held, the value is computed from its position. On release it springs back from wherever it was. The cursor is an element drawn inside the page, and its path and press states are also functions of time.
5. Text that swaps inside a morphing container gets its own enter and exit timing (fade and blur out, then in), so old and new text never overlap.
6. Load the font from a local file, and render nothing until document.fonts.ready has resolved.
7. Add a preview mode at ?preview: a scrub bar, play and pause, and the song playing in sync, so I can review the motion in a browser before rendering.

Audio
- Find the beats with librosa (librosa.beat.beat_track, which also estimates the tempo) if it is available, otherwise with numpy from the song's stated tempo and its first strong onset. Neither detects downbeats, so take the strongest beat in the opening bars as beat 1 of a bar, tell me the time you chose, and ask me to confirm it by ear. Start the timeline on that downbeat, and report the measured tempo and any drift.
- UI sounds (clicks, ticks, a soft whoosh on big morphs) are synthesized locally or come from files I supply. Place each one so its measured peak lands exactly on its event, not its file start.
- Mix the song and the UI sounds with ffmpeg, keeping the UI sounds quiet under the music.

Render
1. Before the full render, render one frame per beat into a contact sheet and look at it. Fix anything off the grid, cramped, clipped, or hard to read, and show me the sheet.
2. Render with Playwright: call seek(t) and take a screenshot at 4 subframes per video frame (240 per second for 60fps).
3. Blend with ffmpeg for motion blur: tmix=frames=4 to average each group of four subframes, then framestep=4 to keep one frame per group, giving 60fps. Encode H.264, yuv420p, high quality (CRF 16 or lower), with the mixed audio, as an .mp4 that plays on X, Instagram, and LinkedIn.
4. Check the loop: the last frame must match the first, cursor position and speed included. Play the join and confirm it does not stutter.
Before starting, confirm that Node with Playwright, Python with numpy (and librosa), and ffmpeg are installed. Ask before installing anything, and install locally to the working folder.

Gotchas
- Never put will-change on anything the camera scales, or the text renders blurry.
- Text that swaps inside a morphing container needs its own enter and exit timing, or it overlaps.
- Make the last frame identical to the first, cursor position and speed included, or the loop stutters.
- Screenshots taken before fonts load render in a fallback font. Wait for them.

Report
The video file, the preview page, the state list on the beat grid as built, the contact sheet, how to re-render after a change, and anything that could not be matched to the beat.
```
