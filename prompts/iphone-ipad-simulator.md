---
title: iPhone and iPad Simulator
description: Set up Xcode and the simulator, build and launch your iPhone or iPad app, then check it at every screen size, in dark mode, and with large text.
meta: Claude Code Prompt
---

Gets an iPhone or iPad app running in the iOS Simulator so you can see how it looks, then reviews it the way a tester would. It checks the Mac and the installed Xcode, installs whatever is missing, builds the app for the simulator, and launches it on three iPhone sizes: the smallest screen available, a standard one, and the largest. Each screen is screenshotted in light and dark mode and with the largest text size, and the screenshots are looked at rather than assumed to be fine. It works with native Xcode projects, Swift packages, and cross-platform apps built with Expo, React Native, Flutter, or Capacitor.

Before it starts, it asks once whether to include two more kinds of device. **iPad** is suggested when the app supports it: the smallest and largest iPads, in all four orientations, sharing the screen with another app in Split View, Slide Over, and Stage Manager, and with a keyboard and pointer. **iPhone Duo**, Apple's foldable, adds the Xcode 27.1 beta, installed alongside your current Xcode rather than replacing it, and checks both displays and each fold pose. It needs a Mac with Apple silicon on macOS 26.6 or later.

It never handles your Apple ID password: when a step needs you to sign in, accept a license, or approve a system prompt, it stops and tells you exactly what to do. It builds for the simulator only and signs, uploads, or submits nothing. The only code it changes on its own is the minimum a new SDK needs to build, each change explained. It ends with a report of every layout problem it found, with the screenshot, the likely cause in the code, and a proposed fix, and waits for you to choose which to make.

## Prompt

```
Set up Xcode and the iOS Simulator, then build and launch my app so I can see how it looks, and review it across devices, screen sizes, appearance, and text size.

Ground rules
- Never ask for, type, or store my Apple ID password or any other credential. If a step needs me to sign in, accept a license with sudo, or approve a system prompt, stop, tell me exactly what to do, and wait.
- Keep any Xcode already installed. If another version is needed, install it alongside (for example /Applications/Xcode-beta.app) and point commands at it with DEVELOPER_DIR instead of switching the whole system with xcode-select.
- Build for the simulator only. Do not change the bundle identifier, signing team, provisioning profiles, or version numbers, and do not archive, upload, or submit anything.
- Apart from the minimum needed to build (Step 4), do not change my app's code until I have seen the report and chosen which fixes to make.
- Do not upgrade the project's dependencies. Install them as locked.

Step 1: Check the Mac and the project
- Report the chip (uname -m), the macOS version (sw_vers), and the free disk space. Xcode, its download, and a simulator runtime together need tens of gigabytes, so warn me if less than 30 GB is free.
- List the installed Xcode versions and which one is selected (xcode-select -p, xcodebuild -version).
- Identify the project type: an .xcworkspace or .xcodeproj, a Swift package, or a cross-platform app (Expo or React Native, Flutter, Capacitor). For a native project, list its schemes with xcodebuild -list.
- Find which devices the app targets: TARGETED_DEVICE_FAMILY in the build settings (1 is iPhone, 2 is iPad), or the framework's equivalent, such as supportsTablet in an Expo config.
- If there is no iPhone or iPad app in this project, stop and tell me.

Step 2: Ask me once
Ask in ONE message, with your suggested default for each, then wait:
- Should the review include iPad? Default: yes if the app targets iPad. If it is iPhone-only, say so: it still runs on iPad in a compatibility window, which is worth one look, but the default is no.
- Should the review include iPhone Duo, Apple's foldable? It needs the Xcode 27.1 beta or later, a Mac with Apple silicon, and macOS 26.6 or later. Say whether this Mac qualifies. Default: no.
- Which scheme to build, only if there is more than one plausible app scheme.
- Anything else Step 1 could not settle.

Step 3: Install what is missing
- Xcode: if no Xcode is installed, or the installed one cannot build this project, install the current release. Use the xcodes command-line tool if it is available (it asks me to sign in, so let me complete that myself); otherwise send me to the Mac App Store or developer.apple.com/download and wait until I confirm it is installed.
- If I chose iPhone Duo and no Xcode 27.1 beta or later is installed, install it alongside the current Xcode the same way. If a non-beta Xcode with iPhone Duo support has been released by now, use that instead.
- Run first-launch setup for each Xcode you will use (xcodebuild -runFirstLaunch). If the license needs accepting, give me the sudo command to run.
- Make sure the matching iOS simulator runtime is installed (xcrun simctl runtime list); it covers iPad as well as iPhone. If it is missing, download it with xcodebuild -downloadPlatform iOS and report progress.

Step 4: Build and launch
- Choose simulators from xcrun simctl list devicetypes, using the newest runtime: three iPhones (the smallest screen available, a standard size, and the largest), plus, if I chose iPad, the smallest and the largest iPad. Create any that do not exist yet, and boot them. If I chose iPhone Duo, add an iPhone Duo simulator on the beta's runtime; its first boot can take several minutes, so wait rather than retry.
- Cross-platform apps: install dependencies as locked (for example npm ci, pod install, flutter pub get), then use the framework's own iOS run command, pointed at each simulator.
- Native apps: build once with xcodebuild -scheme <scheme> -destination 'platform=iOS Simulator,name=<device>' -derivedDataPath build/sim build, then install the .app with xcrun simctl install <device> <path> and launch it with xcrun simctl launch <device> <bundle id>.
- If the build fails, read the errors and fix only what the SDK requires to build (a deprecation that became an error, a deployment target the SDK no longer supports), explaining each change. If the fix is larger than that, stop and ask me.
- Open the Simulator app so I can use the running app myself.

Step 5: Review how it looks
- For clean screenshots, set the status bar with xcrun simctl status_bar <device> override --time 9:41 --batteryLevel 100.
- On each simulator, visit the app's main screens and take a screenshot of each (xcrun simctl io <device> screenshot) into build/sim/screenshots/, named by device, screen, and variant. Capture:
  - portrait, and landscape if the app supports it
  - light and dark appearance (xcrun simctl ui <device> appearance light or dark)
  - default text and the largest accessibility text size (xcrun simctl ui <device> content_size accessibility-extra-extra-extra-large)
- If a screen cannot be reached from the command line, tell me which screens to open in the Simulator and wait for me before capturing.
- Open every screenshot and look at it. Judge from the images, not from the code. Check for: text that is truncated, clipped, or overlapping; layouts that assume one screen size and leave gaps or overflow on the smallest or largest device; content under the notch, the Dynamic Island, or the home indicator; tap targets smaller than 44 by 44 points; low contrast or invisible elements in dark mode; hard-coded colors that ignore the appearance; and screens that break or stop scrolling at large text sizes.
- If I chose iPad, also capture all four orientations, and the app sharing the screen with another app in Split View at one third, one half, and two thirds width, in Slide Over, and in a resized Stage Manager window. Tell me which to set up in the Simulator and wait for me before each capture. Check for: a phone layout stretched across a wide screen where a sidebar, split view, or multi-column layout belongs; layouts that break when the window narrows to phone width; popovers, sheets, and menus positioned for iPhone; and missing keyboard and pointer support (hover states, keyboard shortcuts, focus movement with Tab). For an iPhone-only app, check only that it runs cleanly in the compatibility window.
- If I chose iPhone Duo, also capture each pose the simulator offers (closed, partly folded, fully open) and both displays. Check for layouts that stretch or leave gaps on the open display, content hidden in the fold, and state lost when folding or unfolding (a form cleared, a scroll position reset, a screen popping back). If a pose cannot be set from the command line, tell me which to choose in the Simulator menu and wait. StandBy is unavailable in the iPhone Duo simulator and most app extensions cannot run there, so do not report those as app bugs.

Step 6: Report
- What was installed and where, each simulator's name and UDID, and the exact commands to rebuild and relaunch next time.
- The screenshots, grouped by device and variant.
- Every issue found, ordered by how badly it affects the app, each with the screenshot that shows it, the likely cause in the code (file and line), and a proposed fix.
Then wait for me to choose which fixes to make.
```
