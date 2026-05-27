#!/usr/bin/env python3
"""Generate scene audio with MiniMax TTS.

Run from a Remotion project root:
    uv add requests
    uv run python scripts/generate_audio_minimax.py
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import TypedDict

try:
    import requests
except ImportError as exc:
    raise SystemExit("Missing dependency. Run: uv add requests") from exc


FPS = 30
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "public" / "audio"
CONFIG_FILE = PROJECT_ROOT / "src" / "audioConfig.ts"
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
MINIMAX_VOICE_ID = os.environ.get("MINIMAX_VOICE_ID")
MINIMAX_API_BASE = os.environ.get("MINIMAX_API_BASE", "https://api.minimax.io")


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
        "id": "02-concept",
        "title": "Core concept",
        "text": "今天我们用一个清晰的例子说明核心概念。",
    },
    {
        "id": "03-summary",
        "title": "Summary",
        "text": "最后快速回顾一下整个流程。",
    },
]


def require_env() -> None:
    if not MINIMAX_API_KEY or not MINIMAX_VOICE_ID:
        raise SystemExit(
            "Set MINIMAX_API_KEY and MINIMAX_VOICE_ID before running this script.",
        )


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


def generate_scene_audio(scene: Scene) -> dict[str, str | int | float]:
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

    response = requests.post(
        f"{MINIMAX_API_BASE.rstrip('/')}/v1/t2a_v2",
        headers={
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "speech-02-hd",
            "text": scene["text"],
            "stream": False,
            "voice_setting": {
                "voice_id": MINIMAX_VOICE_ID,
                "speed": 1.0,
                "vol": 1.0,
                "pitch": 0,
            },
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1,
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    audio_hex = payload.get("data", {}).get("audio")
    if not audio_hex:
        error = payload.get("base_resp", {}).get("status_msg", payload)
        raise RuntimeError(f"MiniMax API error: {error}")

    output_file.write_bytes(bytes.fromhex(audio_hex))
    duration = payload.get("extra_info", {}).get("audio_length", 0) / 1000
    if not duration:
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


def main() -> None:
    require_env()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"MiniMax TTS host: {MINIMAX_API_BASE}")
    print(f"Output directory: {OUTPUT_DIR}")

    results: list[dict[str, str | int | float]] = []
    for index, scene in enumerate(SCENES, start=1):
        print(f"[{index}/{len(SCENES)}] {scene['id']}...", flush=True)
        try:
            result = generate_scene_audio(scene)
        except Exception:
            print("Generation stopped. Completed audio files were kept.")
            raise
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
    main()

