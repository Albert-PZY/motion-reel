#!/usr/bin/env python3
"""Generate scene audio with Edge TTS.

Run from a Remotion project root:
    uv add edge-tts
    uv run python scripts/generate_audio_edge.py
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path
from typing import TypedDict

try:
    import edge_tts
except ImportError as exc:
    raise SystemExit("Missing dependency. Run: uv add edge-tts") from exc


FPS = 30
VOICE = "zh-CN-YunyangNeural"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "public" / "audio"
CONFIG_FILE = PROJECT_ROOT / "src" / "audioConfig.ts"


class Scene(TypedDict):
    id: str
    title: str
    text: str


SCENES: list[Scene] = [
    {
        "id": "01-intro",
        "title": "Opening",
        "text": "欢迎观看本期视频。",
    },
    {
        "id": "02-main",
        "title": "Main idea",
        "text": "今天我们用一个清晰的例子说明核心概念。",
    },
]


def get_audio_duration(file_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    output = result.stdout.strip()
    return float(output) if output else 0.0


async def generate_scene_audio(scene: Scene) -> dict[str, str | int | float]:
    output_file = OUTPUT_DIR / f"{scene['id']}.mp3"

    if output_file.exists() and output_file.stat().st_size > 0:
        duration = get_audio_duration(output_file)
        return {
            "id": scene["id"],
            "title": scene["title"],
            "file": output_file.name,
            "duration": duration,
            "frames": round(duration * FPS),
            "status": "skipped",
        }

    communicate = edge_tts.Communicate(scene["text"], VOICE)
    await communicate.save(str(output_file))
    duration = get_audio_duration(output_file)

    return {
        "id": scene["id"],
        "title": scene["title"],
        "file": output_file.name,
        "duration": duration,
        "frames": round(duration * FPS),
        "status": "generated",
    }


def write_audio_config(results: list[dict[str, str | int | float]]) -> None:
    scene_blocks: list[str] = []
    for result in results:
        scene_blocks.append(
            "\n".join(
                [
                    "  {",
                    f'    id: "{result["id"]}",',
                    f'    title: "{result["title"]}",',
                    f'    durationInFrames: {result["frames"]},',
                    f'    audioFile: "{result["file"]}",',
                    "  }",
                ],
            ),
        )

    scenes_content = ",\n".join(scene_blocks)
    content = f"""export interface SceneConfig {{
  id: string;
  title: string;
  durationInFrames: number;
  audioFile: string;
}}

export const SCENES: SceneConfig[] = [
{scenes_content},
];

export function getSceneStart(sceneIndex: number): number {{
  return SCENES.slice(0, sceneIndex).reduce(
    (sum, scene) => sum + scene.durationInFrames,
    0,
  );
}}

export const FPS = {FPS};

export const TOTAL_FRAMES =
  SCENES.reduce((sum, scene) => sum + scene.durationInFrames, 0) + 60;
"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(content, encoding="utf-8", newline="\n")


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Edge TTS voice: {VOICE}")
    print(f"Output directory: {OUTPUT_DIR}")

    results: list[dict[str, str | int | float]] = []
    for index, scene in enumerate(SCENES, start=1):
        print(f"[{index}/{len(SCENES)}] {scene['id']}...", flush=True)
        result = await generate_scene_audio(scene)
        results.append(result)
        print(
            f"  {result['status']}: {result['duration']:.2f}s "
            f"({result['frames']} frames)",
        )

    write_audio_config(results)
    manifest = OUTPUT_DIR / "manifest.json"
    manifest.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {CONFIG_FILE}")


if __name__ == "__main__":
    asyncio.run(main())

