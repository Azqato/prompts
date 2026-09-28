---
title: Animation Performance
description: Measure a page's animations, pause what runs offscreen, fix leaks that slow long sessions, and prove it with before and after numbers.
meta: Claude Code Prompt
---

Fixes pages that make the computer fan spin or grow slower the longer they stay open. Claude measures first: at the top, middle, and bottom of the page and at a phone width, it counts which CSS animations are running while offscreen, including those on `::before` and `::after`, and checks canvas, WebGL, and physics loops separately, since pausing CSS does not stop a JavaScript loop. For leaks, it records element, canvas, and image counts, then samples again after the page sits idle and after navigating away and back.

It then changes the smallest piece of code that owns each problem: an observer that pauses offscreen sections, a render loop that stops when its canvas leaves the screen and resumes when it returns, and cleanup that releases listeners, timers, observers, WebGL resources, animation-library tweens, and media when a component goes away. The aim is not less motion: visible animations must still play.

It proves the result with the same measurements run again, aiming for zero animations running offscreen, and says plainly what it could not measure.

## Prompt

```
Make this page's animations efficient without removing any motion a visitor can see. Measure before editing and after.

Find the work
- Read the project's own instructions first, and follow its browser testing rule if it has one; otherwise use a headless browser against a local copy, never the live site.
- Find the animation sources: CSS keyframes and transitions, requestAnimationFrame loops, setInterval and setTimeout, canvas, WebGL, and physics components, video, animation-library timelines, marquees, and skeleton loaders, and any visibility helpers the project already has.
- In each component's cleanup, check that listeners, observers, loops, timers, loaders, and media are released.

Measure a baseline
- Open the exact page I name (ask if I have not). Sample at the top, middle, and bottom, and at one phone width.
- At each point count the CSS animations running, including pseudo-elements, and note which are offscreen and which element owns them.
- Check canvas and WebGL loops separately: CSS measurements do not show whether a JavaScript loop is still running.
- If I mention slowdowns or memory, also record the counts of elements, canvases, images, and iframes, heap size where the browser exposes it, a sample after 10 to 30 seconds idle, and a sample after navigating away and back a few times. If heap figures are unavailable, say so rather than treating that as proof there is no leak.
- Keep stress tests bounded.

Fix the smallest owner
- Prefer a visibility helper the project already has. Otherwise add an IntersectionObserver (a threshold around 0.01) that marks sections and animated elements as offscreen, and pause their CSS animations with animation-play-state, covering ::before and ::after where needed.
- For canvas, WebGL, and physics loops: start when visible, cancel the animation frame when offscreen, resume on return, and cap the time step after a pause so the simulation does not jump.
- For leaks: clear every timer, cancel frames before unmount, disconnect observers, remove listeners with the same function they were added with, dispose WebGL textures, materials, geometries, and renderers, kill animation-library tweens, stop media, and guard loaders that may finish after the component is gone.
- Respect reduced-motion settings where the code already does, and do not create a render loop in the framework's state to track scrolling.
- Do not pause a visible hero because a selector was too broad, and do not delete animations to make the numbers pass.

Verify
- Re-run the same samples. The target is zero animations running offscreen in the sections tested, with visible ones still playing when scrolled back into view, and loops reporting stopped offscreen.
- For leaks, element and canvas counts should return to the baseline after repeated navigation.
- Try the page's normal interactions (search, filters, navigation) to make sure nothing broke, and check the console.
- Run the project's usual lint and build.

Report the findings first (what ran offscreen, what leaked, what could not be measured), then the before and after numbers per page and position, the checks run, and any limits. Keep what you measured separate from what you found by reading the code. Do not commit anything.
```
