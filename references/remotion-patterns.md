# Remotion Patterns

## Timeline Primitives

Use these Remotion primitives first:

| Primitive | Use |
|---|---|
| `Composition` | Register a renderable video with id, size, fps, duration, and props |
| `useCurrentFrame()` | Read the current frame and derive animation state |
| `useVideoConfig()` | Read fps, dimensions, and total frames |
| `interpolate()` | Map frame ranges to opacity, position, scale, or color stops |
| `spring()` | Create natural entrance and emphasis animations |
| `Sequence` | Place scenes, audio, overlays, or chapters on the timeline |
| `staticFile()` | Load files from `public/` |
| `Audio`, `Video`, `OffthreadVideo`, `Img` | Mount media assets |

## Interpolation

Clamp values unless overshoot is intentional:

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

const translateY = interpolate(frame, [0, 30], [50, 0], {
  extrapolateRight: "clamp",
});
```

## Spring

Use spring for entry motion and emphasis:

```tsx
const scale = spring({
  frame,
  fps,
  config: { damping: 12, stiffness: 100 },
});
```

Offset spring timing by subtracting a delay:

```tsx
const titleProgress = spring({
  frame: frame - 20,
  fps,
  config: { damping: 14 },
});
```

## Sequence Layout

Use sequences to keep scenes independent:

```tsx
<>
  <Sequence from={0} durationInFrames={60}>
    <Intro />
  </Sequence>
  <Sequence from={60} durationInFrames={120}>
    <Main />
  </Sequence>
  <Sequence from={180}>
    <Outro />
  </Sequence>
</>
```

Inside each scene component, pass a local frame when the animation should start
from zero:

```tsx
const Scene = ({ startFrame }: { startFrame: number }) => {
  const globalFrame = useCurrentFrame();
  const frame = globalFrame - startFrame;
  return <Title frame={frame} />;
};
```

## Static Assets

Place assets in `public/`:

```tsx
import { Audio, Img, OffthreadVideo, staticFile } from "remotion";

<Img src={staticFile("images/logo.png")} />;
<Audio src={staticFile("audio/intro.mp3")} volume={0.8} />;
<OffthreadVideo src={staticFile("clips/background.mp4")} />;
```

Prefer `OffthreadVideo` over `Video` when render determinism matters.

## Parameterized Videos

Use zod schemas when the video needs dynamic input props:

```tsx
import { z } from "zod";

const schema = z.object({
  title: z.string(),
  accentColor: z.string(),
});

type MainProps = z.infer<typeof schema>;

export const MainVideo: React.FC<MainProps> = ({ title, accentColor }) => {
  return <h1 style={{ color: accentColor }}>{title}</h1>;
};
```

Register defaults:

```tsx
<Composition
  id="Main"
  component={MainVideo}
  schema={schema}
  defaultProps={{ title: "Launch", accentColor: "#58c4dd" }}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
/>
```

Render with props:

```bash
pnpm exec remotion render Main out/video.mp4 --props='{"title":"Launch"}'
```

## Rendering

Useful commands:

```bash
pnpm exec remotion studio
pnpm exec remotion render Main out/video.mp4
pnpm exec remotion render Main out/video.mp4 --codec=h264
pnpm exec remotion render Main out/video.webm --codec=vp8
pnpm exec remotion render Main out/animated.gif --codec=gif
pnpm exec remotion render Main out/audio.mp3 --codec=mp3
pnpm exec remotion still Main --frame=30 out/thumbnail.png
pnpm exec remotion render Main out/check.mp4 --frames=0-90
```

Common parameters:

| Parameter | Use |
|---|---|
| `--codec` | Choose h264, h265, vp8, vp9, gif, mp3, wav |
| `--crf` | Set quality, lower is better |
| `--props` | Pass JSON props |
| `--scale` | Render at a scale factor for quick checks |
| `--concurrency` | Increase parallel rendering when the machine can handle it |

## Captions

Install caption tooling only when captions are needed:

```bash
pnpm add @remotion/captions @remotion/install-whisper-cpp
pnpm exec remotion-install-whisper-cpp
```

Transcribe in a Node script:

```ts
import { transcribe } from "@remotion/install-whisper-cpp";

const { transcription } = await transcribe({
  inputPath: "public/audio/narration.mp3",
  whisperPath,
  model: "medium",
});
```

Keep captions frame-aligned and render them as text overlays with stable
dimensions so line wrapping cannot shift the whole layout.

## Player Embedding

Install only for web app embedding:

```bash
pnpm add @remotion/player
```

```tsx
import { Player } from "@remotion/player";
import { MainVideo } from "./MainVideo";

<Player
  component={MainVideo}
  durationInFrames={150}
  fps={30}
  compositionWidth={1920}
  compositionHeight={1080}
  controls
  inputProps={{ title: "Dynamic Title" }}
/>;
```

## Performance

- Memoize expensive calculations and generated arrays.
- Avoid reading files, parsing data, or allocating large objects inside render
  without memoization.
- Use lower scale or frame ranges while iterating.
- Keep each scene's mounted media and 3D canvases minimal.
- Use `delayRender()` and `continueRender()` for async asset preparation when
  necessary.

