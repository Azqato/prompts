---
title: Video to Prompt
description: Turn a screen recording of a site or animation into one detailed prompt that can rebuild it: layout, motion, scroll, assets, and mobile behavior.
meta: Claude Code Prompt
---

Turns a video of a design you admire, a landing page scrolled top to bottom or an animation you want to learn from, into one prompt detailed enough that a model can rebuild it without seeing the video. Claude reads the video's facts with ffprobe, pulls frames at each beat with ffmpeg rather than at even intervals, and studies it in layers: the story and section order, the layout, the motion and its timing, the visual design, and how each part would actually be built.

The prompt it writes names exact mechanisms rather than adjectives, a pinned section, a scrubbed timeline, a mask, a parallax layer, instead of "nice transitions", and always includes mobile behavior, a reduced-motion fallback, and what to avoid. It asks first whether you want an exact recreation or a new design inspired by the video, and when it is inspiration it keeps the ideas and leaves the other site's brand, copy, and images behind.

It needs ffmpeg, which it checks for and asks before installing. It writes the prompt and stops; it builds nothing unless you ask.

## Prompt

```
Turn a reference video into one paste-ready prompt that can rebuild what it shows.

Source
- Ask me for the video (a local file or a link) if I have not given one. If you cannot open it, say so and wait; never describe a video you have not seen.
- Ask once: exact recreation, or a new design inspired by it? For inspiration, keep the structure, pacing, and techniques, and leave out the other site's name, logo, copy, images, and numbers.
- If the video is of a page you can open, you may also open the page itself to confirm details. For a full-page still of it, scroll the page once top to bottom so lazy content loads, return to the top, then capture it one viewport at a time with a short wait after each scroll, and stitch those captures. Do not trust a single one-shot full-page screenshot: on animated pages it often comes out blank or partial.

Tools
- This needs ffprobe and ffmpeg. Check for them, and ask before installing anything. Put extracted frames in a temporary folder outside the project, and delete it at the end unless I ask to keep it.

Inspect
- Run ffprobe for duration, size, and frame rate.
- Extract frames at each visible beat: the start, each section or scene change, each transition's middle, and the end, rather than one frame every second. Look at each one.

Analyze in layers
- Story: what it is for, the order of sections, how each hands over to the next.
- Layout: framing, grid, sticky areas, cards, media, overlays, navigation, footer.
- Motion: what triggers each movement, its timing and easing, reveals, masks, parallax, pinned sections, scroll scrubbing, hover and tap states, looping ambient motion.
- Visual design: type, color, surfaces, borders, shadows, texture, icons, image treatment.
- How to build it: name the likely mechanism for each effect (CSS, IntersectionObserver, a scroll-linked timeline, video scrubbing, canvas, WebGL, a physics library) and say when you are inferring rather than seeing it.
- Mobile and access: what changes on a phone, the reduced-motion version, loading and performance limits.

Write the prompt
- One fenced text block. Start with what to build and whether it is a recreation or an inspired design.
- Include an asset list (exact files or links where known, clearly marked placeholders otherwise), the design language, then each section in order with its purpose, layout, visuals, motion, interaction, and reduced-motion fallback.
- Use numbers and named mechanisms, not taste words. Avoid "make it beautiful", "similar animation", "smooth transitions".
- End with what to avoid: stock landing-page sections the video does not have, decorative filler, text overlapping media, and autoplay where the video shows scroll control.

Before you finish, check that every asset in the prompt exists or is marked as a placeholder, and that the prompt keeps the video's order and pacing. Give me the prompt and a short list of anything you inferred rather than saw, then stop.
```
