# 18-Second Product Launch / Brag Card Recipe

Deterministic, high-impact 18-second video card for new product releases, feature highlights, and milestone announcements.

## Boundary
- Intent: `video_html` (short deterministic launch card, <90s).
- Full application walkthroughs and Indonesian spoken narration remain strictly `id-demo-video`.
- Photoreal 3D/cinematic promo ads remain `visual-studio`.
- Always load `composition.md` and `render.md` alongside this recipe.
- If Chromium or FFmpeg is absent: report `NOT_CONFIGURED` or `DEGRADED`, generate self-contained HTML/CSS/JS artifacts, and provide the exact render command. Never call remote HeyGen APIs or request hosted keys.

## Composition Specification
- **Duration:** Exactly 18.0 seconds (`totalSeconds = 18`, `fps = 60`, `totalFrames = 1080`).
- **Canvas / Viewport:** 1920x1080 (16:9 landscape) or 1080x1920 (9:16 vertical/shorts).
- **Target Output Path:** `brag-output/brag.mp4`.
- **Assets:** Fully local only (inline SVGs, CSS typography, base64 or relative images). No external CDN links.

## Beat Sheet (18 Seconds)

| Beat | Window | Scene | Visual Action |
|---|---|---|---|
| **1. Hook & Problem** | `0.0s - 3.5s` | Hook Card | Dark minimal backdrop, glitching problem statement or bold metric text fading in with spring scale. |
| **2. Solution Reveal** | `3.5s - 8.0s` | Hero Reveal | Product brand logo + high-fidelity UI mockup card translates into center with smooth deceleration curve (`cubic-bezier(0.16, 1, 0.3, 1)`). |
| **3. Capability Highlight** | `8.0s - 13.5s` | Feature Carousel | 3 kinetic badge callouts or terminal command executions popping in sequence with numerical counters. |
| **4. Call to Action** | `13.5s - 18.0s` | Outro Lockup | Clean repository / install command (`opencode-he ...` or `git clone ...`), release tag badge, and link fade-out. |

## Seekable Timeline Contract

```javascript
// Master timeline contract driven strictly by frame or elapsed seconds
function renderFrame(t) {
  // t is in seconds (0.000 to 18.000)
  const progress = Math.min(Math.max(t / 18.0, 0), 1);

  if (t < 3.5) {
    // Scene 1: Hook
    const s1Progress = t / 3.5;
    renderHookScene(s1Progress);
  } else if (t < 8.0) {
    // Scene 2: Hero Reveal
    const s2Progress = (t - 3.5) / 4.5;
    renderHeroScene(s2Progress);
  } else if (t < 13.5) {
    // Scene 3: Highlight
    const s3Progress = (t - 8.0) / 5.5;
    renderHighlightScene(s3Progress);
  } else {
    // Scene 4: CTA
    const s4Progress = (t - 13.5) / 4.5;
    renderOutroScene(s4Progress);
  }
}
```

## Local Execution & Output

```bash
# 1. Output directory preparation
mkdir -p brag-output

# 2. Local deterministic render via hyperframes CLI or local script
npx -y hyperframes render \
  --input index.html \
  --output brag-output/brag.mp4 \
  --width 1920 \
  --height 1080 \
  --fps 60 \
  --duration 18
```
