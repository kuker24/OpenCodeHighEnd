# Product-Film Mode Reference (Real App UI)

Distilled motion doctrine adapted from `kaventro/motion-designer@0cf0ba9` (MIT).
Used when the user requests a launch film, teaser, or product promo of a real application interface (iOS, macOS/Windows/Linux desktop, Electron/Tauri, web app) rather than an abstract business commercial.

## 1. Real App Interface & Device Boundaries

- **Real Code or Screenshots Only**: Rebuild screens directly from repository components, styling tokens, icons, and layout, or use verified repository screenshots. Generic mockups, stock UI, and ungrounded templates are rejected.
- **Mobile in Device Chrome**: Mobile interfaces remain inside an iPhone frame with dynamic island or status bar for the entire film. Never show mobile app UI full-bleed without device context. Close-ups may crop vertically but must retain horizontal device bounds.
- **Desktop in Window Chrome**: Desktop apps remain inside their application window (with title bar, traffic lights/caption controls, dock/menu bar context). The cursor moves only when demonstrating a specific user interaction. Never let the pointer drift randomly.
- **No Style Kits**: Do not adopt foreign upstream style kits (Meadow, Midnight, Warm Ink, Field Guide, Paper and Ink, Color Block). Derive visual tokens directly from the app itself or from `emil-design-eng` motion principles.

## 2. Deterministic Frame Contract: `seek(t)`

- **Pure Function of Time**: Every scene property, layout transform, spinner, caret, and kinetic element must be a pure deterministic function of elapsed time `seek(t)`.
- **Prohibited Primitives**: Zero timers (`setTimeout`, `setInterval`), zero `Date.now()`, zero `Math.random()`, and zero asynchronous state carryover between frames. Zero CSS transitions or CSS `@keyframes` animations.
- **Seam & Path Consistency**: The timeline loop must close cleanly (the frame immediately following the end must match the initial frame). Seeking to time `t` from any order or direction must yield bit-identical pixels.

## 3. Beat-Map & Sound Direction

- **Beat-Driven Choreography**: Map the story across tempo (BPM), bars, and musical drops.
- **Drop Synchronization**: Core product actions, key reveals, and major value transitions must land squarely on musical drops.
- **Soundtrack Priority**: Prioritize the user-provided audio track.
- **Optional Heavy Models**: Heavy audio generation models (ACE-Step ~11 GB) and speech synthesizers (Chatterbox, Kokoro) are `OPTIONAL_POINTER`. Never execute upstream `install.sh` and never auto-download models. When absent, report `NOT_CONFIGURED`.

## 4. The Four-Still Approval Gate

Before writing implementation code or starting a build, you must define the story beats and present four distinct still frames for explicit user review:
1. **Opening Still**: Hook and initial device entrance.
2. **Key Product Moment Still**: The primary feature or workflow shown in action.
3. **The Drop Still**: The pivotal climax or key result landing on the musical drop.
4. **Final Frame Still**: The concluding lock-up, product mark, and call to action.

*Halt Gate:* Without explicit approval of the four stills from the user, stop and do not proceed to build.

## 5. QA Loop & Mechanical Ledger

- **Contact Sheets**: Generate visual contact sheets of the film (timeline overview every 0.5 s, transitions every 0.05 s) to review cadence, cropping, and legibility.
- **Failure Catalogue**: Audit against common flaws:
  - Text cut off or truncated (`"Savi"`, `"Uncategori…"`).
  - UI displayed full-bleed without device framing.
  - Arbitrary crossfades between unrelated scenes instead of physical UI transitions.
  - Cursor moving without purpose or clicking empty space.
  - Invented features or claims not present in the codebase.
- **Evidence Ledger (`FACT:`)**:
  - `FACT:` Verified local MP4 output file path and byte size.
  - `FACT:` Presence or absence of `ffmpeg` and `ffprobe`.
  - `FACT:` Presence or absence of headless Chrome / Chromium.
  - `FACT:` Integrated audio loudness (LUFS) and true peak (dBFS) if audio is rendered.
- **Tooling Gate**: If `ffmpeg` or `chromium` is missing from the local environment, report `NOT_CONFIGURED`. Never emit a false `PASS`.

## 6. Rendering Engine Hierarchy

- **Default Engine**: Rendering is executed through `hyperframes` (deterministic HTML/CSS/canvas to seekable frames). 18-second brag cards remain strictly in `skills/hyperframes/references/brag.md`.
- **Alternative Upstream Pipeline**: Direct DevTools-driven Chrome frame capture into ffmpeg is used only when explicitly requested by the user and Chrome is verified available on the machine.

## 7. Neighbor Boundaries

- Spoken Indonesian app walkthroughs and demo contests: strictly `id-demo-video`.
- 2D timeline scrollytelling websites: `scroll-craft`.
- Continuous camera fly-through 3D worlds: `scroll-world`.
- UI motion physics and micro-interactions: `emil-design-eng`.
- Product UI atom design and implementation: `impeccable` and `found-this-design`.
- Gateway multi-model routing: `ninerouter`.
