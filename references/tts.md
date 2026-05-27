# TTS And Audio Sync

Use TTS when the video needs narration, automatic timing, or batch generation.
For tutorial videos, let generated audio define scene durations.

## Recommended Decision Flow

1. If the user has `MINIMAX_API_KEY` and `MINIMAX_VOICE_ID`, use MiniMax TTS.
2. If MiniMax is not configured or should not be billed, use Edge TTS.
3. If the user supplies existing audio, skip TTS and measure those files.

## Python Environment

Use `uv` from the project root:

```bash
uv venv
uv add edge-tts
uv run python scripts/generate_audio_edge.py
```

Do not use `pip install`.

## ffprobe

Both helper scripts use `ffprobe` to measure audio duration. Install FFmpeg when
duration detection fails:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows with winget
winget install Gyan.FFmpeg
```

## Edge TTS

Edge TTS is free and needs no API key:

```bash
cp templates/scenes.json scripts/scenes.json
uv add edge-tts
uv run python scripts/generate_audio_edge.py
```

Useful Mandarin voices:

| Voice ID | Style |
|---|---|
| `zh-CN-YunyangNeural` | Professional broadcaster |
| `zh-CN-XiaoxiaoNeural` | Warm and natural |
| `zh-CN-YunxiNeural` | Bright young male |

## MiniMax TTS

MiniMax is a paid cloud TTS option and supports voice cloning. Configure:

```bash
$env:MINIMAX_API_KEY = "your-api-key"
$env:MINIMAX_VOICE_ID = "your-voice-id"
cp templates/scenes.json scripts/scenes.json
uv add requests
uv run python scripts/generate_audio_minimax.py
```

Use the correct API host:

| Account | Host |
|---|---|
| International | `https://api.minimax.io` |
| Mainland China | `https://api.minimaxi.com` |

Do not use `api.minimax.chat` for TTS.

## Audio Config Contract

The TTS helpers read `scripts/scenes.json` by default. Override paths and frame
rate through environment variables:

| Variable | Default |
|---|---|
| `MOTION_REEL_SCENES_FILE` | `scripts/scenes.json` |
| `MOTION_REEL_AUDIO_DIR` | `public/audio` |
| `MOTION_REEL_CONFIG_FILE` | `src/audioConfig.ts` |
| `MOTION_REEL_FPS` | `30` |
| `EDGE_TTS_VOICE` | `zh-CN-YunyangNeural` |
| `MINIMAX_API_BASE` | `https://api.minimax.io` |

Scene JSON format:

```json
{
  "scenes": [
    {
      "id": "01-intro",
      "title": "Opening",
      "text": "欢迎观看本期视频。"
    }
  ]
}
```

Use this structure in `src/audioConfig.ts`:

```ts
export interface SceneConfig {
  id: string;
  title: string;
  durationInFrames: number;
  audioFile: string;
}

export const SCENES: SceneConfig[] = [
  {
    id: "01-intro",
    title: "Opening",
    durationInFrames: 300,
    audioFile: "01-intro.mp3",
  },
];

export const FPS = 30;
export const TOTAL_FRAMES =
  SCENES.reduce((sum, scene) => sum + scene.durationInFrames, 0) + 60;
```

Use `getSceneStart(index)` for `Sequence.from`.

## Remotion Audio Sync

```tsx
import { Audio, Sequence, staticFile } from "remotion";
import { SCENES, getSceneStart } from "./audioConfig";

{SCENES.map((scene, index) => (
  <Sequence
    key={scene.id}
    from={getSceneStart(index)}
    durationInFrames={scene.durationInFrames}
  >
    <Audio src={staticFile(`audio/${scene.audioFile}`)} />
  </Sequence>
))}
```

## Script Requirements

TTS scripts should:

- skip existing non-empty audio files;
- read scene narration from JSON instead of hardcoded Python lists;
- print foreground progress;
- keep already generated files when a later scene fails;
- write TypeScript with real newline characters, never literal `\n` sequences;
- create parent directories before writing output;
- leave credentials in environment variables only.

## Common Issues

| Issue | Cause | Fix |
|---|---|---|
| `invalid api key` | Wrong MiniMax host or credential | Use `api.minimax.io` or `api.minimaxi.com` and check env vars |
| No duration | `ffprobe` missing | Install FFmpeg and rerun |
| TypeScript contains literal `\n` | Bad Python string join in f-string | Join lines before putting them into the template |
| Audio and video drift | Hardcoded frame counts | Regenerate `audioConfig.ts` from measured durations |
| Long task feels stuck | Script runs in background | Run in foreground and print per-scene progress |
