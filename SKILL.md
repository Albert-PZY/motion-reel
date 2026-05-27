---
name: motion-reel
description: Create programmatic videos with Remotion in Codex. Use when the user asks Codex to build, plan, debug, render, or automate React/Remotion videos, tutorial videos, explainer animations, TTS narrated videos, captions, music visualizers, data-driven videos, 3D scenes with @remotion/three, or batch video generation. Trigger phrases include "Remotion", "用代码做视频", "编程视频", "React 视频", "视频自动化", "教程视频", "配音视频", "字幕视频", and "$motion-reel".
---

# Motion Reel

Use Remotion to create deterministic videos from React components, scene data,
audio, and assets. Prefer project-specific code over generic demos: every video
should have a clear composition, timeline, visual system, and render command.

## Operating Rules

- Use `pnpm` for Node and Remotion commands. Do not use `npm`, `npx`, or `npm run`.
- Use project-level Python virtual environments with `uv` for TTS helpers. Add and
  remove Python dependencies only with `uv add` and `uv remove`.
- Keep generated text files UTF-8 without BOM.
- Re-read files before editing in Windows workspaces and apply small patches.
- Put static media under `public/` and load it through `staticFile()`.
- Keep render output outside committed source, usually in `out/` or `dist/`.

## First Pass

1. Inspect the existing project before changing files:
   - `package.json`
   - `src/Root.tsx` or `src/Root.jsx`
   - Remotion config files
   - `public/` assets
   - existing scripts and tests
2. If no Remotion project exists, create one with pnpm:
   ```bash
   pnpm create video@latest
   ```
3. Install only the packages the project needs:
   ```bash
   pnpm add remotion @remotion/renderer
   pnpm add react react-dom
   ```
   Add optional packages such as `@remotion/three`, `three`,
   `@react-three/fiber`, `@react-three/drei`, `@remotion/captions`, or
   `@remotion/player` only when the task needs them.
4. Standardize useful scripts in `package.json`:
   ```json
   {
     "scripts": {
       "dev": "remotion studio",
       "render": "remotion render Main out/video.mp4",
       "still": "remotion still Main out/thumbnail.png",
       "lint": "tsc --noEmit"
     }
   }
   ```

## Core Remotion Pattern

Register compositions in `src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Main"
      component={MainVideo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

Drive animation with frames:

```tsx
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrance = spring({ frame, fps, config: { damping: 14 } });
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        backgroundColor: "#0b1020",
        color: "white",
        justifyContent: "center",
      }}
    >
      <h1 style={{ opacity, transform: `scale(${entrance})` }}>Motion Reel</h1>
    </AbsoluteFill>
  );
};
```

## Scene-Driven Narration

For narrated tutorial or explainer videos, make audio the timing authority:

1. Write the narration as scene records: `id`, `title`, `text`.
2. Generate one audio file per scene.
3. Write `src/audioConfig.ts` with `durationInFrames` for each scene.
4. Set `Composition.durationInFrames` from `TOTAL_FRAMES`.
5. Render one `Sequence` per scene and mount scene audio inside that sequence.

Copy `templates/scenes.json` to `scripts/scenes.json`, write the narration
there, then copy `templates/audioConfig.ts` as the initial timing file. Use
`scripts/generate_audio_edge.py` for a free local TTS path and
`scripts/generate_audio_minimax.py` when the user has MiniMax credentials. Set
`MOTION_REEL_SCENES_FILE` only when the scene JSON lives elsewhere.

Read [references/tts.md](references/tts.md) before implementing TTS or audio
sync.

## Visual Architecture

- One concept per scene. Avoid stuffing an entire tutorial into one component.
- Treat color as semantic data, not decoration. Define a small color map early.
- Use staged reveals, progress indicators, labels, and focus highlights to guide
  attention.
- Prefer 2D or orthographic 2.5D for explanations where clarity matters more
  than spectacle.
- Use 3D only when spatial reasoning, product form, or depth actually helps.
- Clamp progress values with `Math.min()` or Remotion extrapolation options.

Read [references/remotion-patterns.md](references/remotion-patterns.md) for
animation, rendering, subtitles, player embedding, and workflow patterns.

Read [references/three.md](references/three.md) before building 3D scenes.

Read [references/tutorial-video.md](references/tutorial-video.md) before writing
long-form educational scripts or process animations.

## Verification

For every implementation, run the smallest meaningful checks:

```bash
pnpm lint
pnpm exec remotion render Main out/video.mp4
```

For expensive renders, first verify a still frame or a short frame range:

```bash
pnpm exec remotion still Main --frame=30 out/check.png
pnpm exec remotion render Main out/check.mp4 --frames=0-90
```

If a browser preview is needed, run Remotion Studio and inspect it with browser
tools:

```bash
pnpm dev
```

Report the exact commands run and any render artifacts created.
