---
title: Game Setup
description: Set up a three.js game with Vite and TypeScript, a fixed-step game loop, input, audio, and asset systems, then build a small playable slice.
meta: Claude Code Prompt
---

Sets up a browser game on three.js the way it should start, then builds a small, complete, playable slice on top so you can judge how the game feels. It reads the project first, then asks once about the game itself: genre, camera, core loop, desktop or mobile, which renderer, whether to use React Three Fiber, whether it needs physics, and the art direction. Each question comes with a recommended default. It also names anything missing or out of date in the project's docs. If your docs set rules this kind of game cannot follow, such as no build step, no dependencies, running without a server, or a strict Content Security Policy, it quotes each one, explains what the game needs instead, and asks whether to update the docs, work within the rule at a stated cost, or stop. If your answers leave the core loop, the controls, or how to win and lose unclear, it asks a short follow-up instead of inventing them, and it asks again before writing anything to the docs that only you can supply.

The setup is Vite and strict TypeScript, with the renderer, game loop, input, audio, assets, and game logic in separate modules. Game logic runs at a fixed step, so the game plays the same on a 60Hz and a 144Hz screen. The game pauses when its tab is hidden, cleans up GPU memory when a level unloads, and recovers if the graphics context is lost. Controls are named actions that can be remapped across keyboard, mouse, gamepad, and touch. Models are compressed glTF, and a debug mode behind `?debug` shows the frame rate, draw calls, and live tuning controls. Because three.js changes its API often, it checks the installed version's documentation instead of relying on memory, and it never uses removed APIs.

It stops once to confirm the architecture and the planned slice, then builds the smallest complete version of the game's core loop: menu, play, win or lose, restart. It is verified by type checks, unit tests, and a headless browser test that fails on any console error and saves screenshots, which it looks at before calling anything done. It measures frame time and draw calls against a stated budget, records the decisions in the project's docs, and deploys nothing.

## Prompt

```
Set up a three.js game project using current best practices, then build a small playable vertical slice on top of it: one complete loop of play, start to finish, polished enough to judge the game's feel. Structure first, content second.

Ground rules
- three.js changes its API often. Check the installed version (npm ls three) and read its docs and migration notes for anything you are unsure of, rather than relying on memory. Never use removed APIs such as Geometry or the old examples/jsm import paths; add-ons come from three/addons/.
- Install everything from npm and bundle it. No CDN script tags.
- Keep the game loop, rendering, input, audio, assets, and game logic in separate modules. No single file over roughly 300 lines.
- Judge the game from what it actually renders, never from the code alone (see Verification).
- Do not deploy or publish anything.

Phase 1: Understand the project
Read the README, CLAUDE.md, docs/, and package.json if they exist. If this is an existing project, map its structure and keep its conventions; if it already uses three.js, note the version and anything outdated.
Check those docs for rules this prompt would break, such as: no build step, no npm dependencies, running from file:// with no server (browsers block JavaScript modules and asset loading there, so a three.js game needs at least a local server), or a strict Content Security Policy (a three.js game needs connect-src 'self' to load assets, 'wasm-unsafe-eval' for WebAssembly such as Rapier and the model decoders, and worker-src blob: for decoder workers). For each conflict, quote the rule with its file and line, and explain what this prompt needs instead and why. Put these at the top of the Phase 1 message, and ask whether to:
- update the docs so the project allows what this game needs (I confirm the wording first),
- adapt the setup to stay within the rule where that is possible, saying what it costs (for example, no build step means no TypeScript, no model compression, and no test tooling), or
- stop.
Do not change the docs or start building until I answer.
Then ask me in ONE message, with your recommended default for each, and wait:
- The game: genre, camera (first person, third person, top-down, side view, fixed), and the one-sentence core loop (what the player does over and over).
- Targets: desktop only, or mobile too (this decides touch controls and the performance budget).
- Renderer: WebGPURenderer (import from three/webgpu; falls back to WebGL2 automatically; custom shaders are written in TSL, and ShaderMaterial and onBeforeCompile do not work with it) or WebGLRenderer (widest compatibility with existing add-ons, examples, and GLSL shaders). Recommend one for this game and say why.
- Structure: plain three.js (recommended for games, for frame-level control) or React Three Fiber (if the game is mostly UI or the project already uses React).
- Physics: none, simple custom collision, or a physics engine (Rapier, @dimforge/rapier3d-compat, by default).
- Art direction: low-poly, stylized, realistic, or placeholder shapes for now.
- Documentation: anything the existing docs are missing, out of date on, or contradict about this game, and the details only I can supply (such as the game's name, audience, or story) that the docs will need.
If my answers still leave the core loop, the controls, or the win and lose conditions unclear, ask a short follow-up rather than inventing them. Do not start Phase 2 until the game is clear enough to build.

Phase 2: Scaffold
- Vite plus TypeScript in strict mode. Scripts for dev, build, preview, typecheck, and test.
- Folder layout, adjusted to the game:
  src/engine/ (renderer, loop, resize, debug tools)
  src/input/ (actions and devices)
  src/audio/
  src/assets/ (loading and disposal)
  src/game/ (state machine, entities, systems, levels)
  src/ui/ (HTML overlay: menus, HUD)
  public/assets/ (models, textures, sounds)
- ESLint and Prettier with default configs. A .gitignore for node_modules and dist.

Phase 3: Engine core
- Renderer: created once, antialiasing on, pixel ratio capped at Math.min(devicePixelRatio, 2), sized with a ResizeObserver on the canvas container (update the camera aspect and projection). Choose tone mapping deliberately (ACES Filmic, AgX, or Neutral) and set the colorSpace of color textures to SRGBColorSpace. If neither WebGPU nor WebGL is available, show a clear message instead of a blank page.
- Loop: renderer.setAnimationLoop. Run game logic and physics at a fixed step (1/60 s) with an accumulator, render every frame, and interpolate positions between steps so motion is smooth at any refresh rate. Clamp the frame delta (for example to 0.1 s) so returning to a background tab does not teleport objects. Pause on visibilitychange and on window blur.
- State machine: boot, loading, menu, playing, paused, game over. Each state has enter, exit, update, and render, and the UI follows the state.
- Entities: a light component-and-system structure, or plain classes with update methods for a small game. Do not build a full ECS unless the game has hundreds of interacting entity types.
- Debug mode behind ?debug in the URL: an FPS and frame-time overlay (stats-gl or similar), renderer.info (draw calls, triangles, geometries, textures), lil-gui for live tuning, and physics collider outlines if physics is used.
- Handle a lost graphics context (webglcontextlost and webglcontextrestored on WebGL, device loss on WebGPU): pause, then rebuild GPU resources.

Phase 4: Systems
- Input: map physical controls to named actions (move, look, jump, interact, pause), so the game reads actions, never raw keys. Support keyboard, mouse (pointer lock for first person), gamepad, and touch if mobile is a target (on-screen stick and buttons). Controls can be remapped, and the mapping is saved.
- Assets: one loader using LoadingManager for a progress screen. Models in glTF/GLB. Provide a script that compresses models with gltf-transform (Meshopt or Draco geometry, KTX2 textures) and wire in the matching decoders. Cache shared assets. When a level unloads, dispose of its geometries, materials, and textures, and confirm with renderer.info that the counts go back down.
- Audio: one AudioListener on the camera, unlocked on the first user gesture, because browsers block audio before one. Separate music and effects volumes, positional audio for in-world sounds, saved settings.
- Physics (if chosen): step it inside the fixed-step update, never per frame. Keep physics bodies and meshes linked in one place, with colliders as simple shapes rather than render meshes.
- Saves and settings: localStorage with a version number, a migration path, and a safe fallback if the data is missing or corrupt.
- Performance defaults: InstancedMesh or BatchedMesh for repeated objects, shared materials, one shadow-casting light with a tightly fitted shadow camera and a modest shadow map, LOD for large scenes, and no new objects per frame in hot paths (reuse vectors and matrices). Set a budget for this game (target frame rate, maximum draw calls and triangles) and state it.
- Accessibility: pause from anywhere, remappable controls, camera shake and flashes reduced when prefers-reduced-motion is set, information never shown by color alone, and HUD text readable on the smallest target screen.

Checkpoint
Summarize the architecture, the chosen defaults, and the vertical slice you plan to build, in a few lines each, and wait for my go-ahead.

Phase 5: Vertical slice
Build the smallest version of the core loop that is complete: start from the menu, play, reach a win or lose condition, see the result, restart. Use placeholder shapes unless I supplied art. Make it feel good before making it big: responsive controls, a camera that follows smoothly, and clear feedback when something happens (a sound, a small particle burst or flash, a HUD change).

Verification
- npm run typecheck, npm run build, and npm test must pass. Unit test the game logic that does not need a renderer (state transitions, scoring, collision rules, save migration) with Vitest.
- Add a Playwright smoke test that starts the preview build, loads the game, fails on any console error or unhandled rejection, reaches the playing state, and saves screenshots of the menu and of gameplay. Headless browsers often have no GPU: if WebGL is unavailable, launch Chromium with --use-angle=swiftshader --enable-unsafe-swiftshader. SwiftShader offers no WebGPU adapter, so a WebGPURenderer game will run on its WebGL2 fallback in this test.
- Open the screenshots and look at them: is anything black, missing, stretched, or unlit? Fix and repeat.
- Record frame time, draw calls, and triangles in debug mode on the gameplay scene, and compare them with the budget. Note that numbers from a software renderer are not representative; measure in a real browser where possible.

Report
- How to run it (dev, build, debug mode), the folder structure, and where to add a new entity, level, or input action.
- The decisions made and why, the budget and the measured numbers, and the screenshots.
- A short, prioritized list of what to build next, and anything you skipped or could not verify.
Record the architecture and decisions in the project's docs (docs/PRD.md and docs/DESIGN.md if the project uses them, otherwise the README). If an update needs information you do not have, ask me for it before writing, and never fill a gap with invented details.
```
