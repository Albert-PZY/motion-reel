#!/usr/bin/env python3
"""Generate scene audio with Edge TTS.

Run from a Remotion project root:
    uv add edge-tts
    uv run python scripts/generate_audio_edge.py
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import TypedDict

try:
    import edge_tts
except ImportError as exc:
    raise SystemExit("Missing dependency. Run: uv add edge-tts") from exc


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FPS = int(os.environ.get("MOTION_REEL_FPS", "30"))
VOICE = os.environ.get("EDGE_TTS_VOICE", "zh-CN-YunyangNeural")
OUTPUT_DIR = Path(os.environ.get("MOTION_REEL_AUDIO_DIR", str(PROJECT_ROOT / "public" / "audio")))
CONFIG_FILE = Path(os.environ.get("MOTION_REEL_CONFIG_FILE", str(PROJECT_ROOT / "src" / "audioConfig.ts")))
SCENES_FILE = Path(os.environ.get("MOTION_REEL_SCENES_FILE", str(PROJECT_ROOT / "scripts" / "scenes.json")))


class Scene(TypedDict):
    id: str
    title: str
    text: str


def load_scenes() -> list[Scene]:
    if not SCENES_FILE.exists():
        raise SystemExit(
            f"Scene file not found: {SCENES_FILE}\n"
            "Copy templates/scenes.json to scripts/scenes.json and edit it first.",
        )

    payload = json.loads(SCENES_FILE.read_text(encoding="utf-8"))
    raw_scenes = payload.get("scenes") if isinstance(payload, dict) else payload
    if not isinstance(raw_scenes, list):
        raise SystemExit("Scene file must be a JSON array or an object with a scenes array.")

    scenes: list[Scene] = []
    for index, raw_scene in enumerate(raw_scenes, start=1):
        if not isinstance(raw_scene, dict):
            raise SystemExit(f"Scene #{index} must be an object.")
        missing = {"id", "title", "text"} - set(raw_scene)
        if missing:
            raise SystemExit(f"Scene #{index} is missing fields: {', '.join(sorted(missing))}")
        scenes.append(
            {
                "id": str(raw_scene["id"]),
                "title": str(raw_scene["title"]),
                "text": str(raw_scene["text"]),
            },
        )
    return scenes


def get_audio_duration(file_path: Path) -> float:
    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe was not found. Install FFmpeg before generating audio.")

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
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {file_path}: {result.stderr.strip()}")
    output = result.stdout.strip()
    if not output:
        raise RuntimeError(f"ffprobe returned no duration for {file_path}")
    return float(output)


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
    scenes = load_scenes()

    print(f"Edge TTS voice: {VOICE}")
    print(f"Scene file: {SCENES_FILE}")
    print(f"Output directory: {OUTPUT_DIR}")

    results: list[dict[str, str | int | float]] = []
    for index, scene in enumerate(scenes, start=1):
        print(f"[{index}/{len(scenes)}] {scene['id']}...", flush=True)
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
