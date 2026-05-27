[中文](README_zh-CN.md)

# Motion Reel

> A Codex skill for creating programmatic videos with Remotion, React, scene-timed audio, captions, and 3D motion.

Motion Reel turns the original Remotion video skill into a Codex-native skill.
It gives Codex a focused workflow for planning, building, debugging, and
rendering Remotion videos with scene data, TTS narration, visual timing, and
repeatable release artifacts.

The repository itself is a valid Codex skill folder: `SKILL.md` is the runtime
entry point, `references/` holds optional deep guidance, `templates/` contains
copyable project files, and `scripts/` contains helper code for TTS and release
validation.

## Attribution

This project is based on the original
[wshuyi/remotion-video-skill][original-skill] project. That repository provided
the initial Remotion and TTS knowledge base. Motion Reel keeps the useful video
production patterns while reshaping the
skill for Codex conventions, pnpm-first Node workflows, uv-managed Python
helpers, bilingual documentation, and GitHub release automation without npm
publishing.

## Links

- [Codex skill entry](SKILL.md)
- [Chinese README](README_zh-CN.md)
- [Commit convention](docs/git-commit-guidelines.md)
- [Release process](docs/release-process.md)
- [Remotion docs][remotion-docs]
- [Original upstream skill][original-skill]

## Release Status

Motion Reel uses Semantic Versioning and GitHub Releases such as `v0.1.0`.
Release automation is driven by Conventional Commits through Release Please.
Merging a release PR creates the GitHub Release, exact version tag, moving
`vX` and `vX.Y` tags, and a downloadable `motion-reel.zip` skill archive.

The workflow intentionally does not publish to npm. This repository is consumed
as a Codex skill folder or release archive, not as a package registry artifact.

## Highlights

| Area | Support |
|---|---|
| Codex compatibility | Native `SKILL.md` frontmatter, concise triggering, and `agents/openai.yaml` metadata |
| Remotion workflow | Project inspection, composition setup, timeline patterns, render commands, and verification steps |
| Package management | pnpm-only Node guidance and CI scripts |
| Python helpers | uv-first TTS scripts for Edge TTS and MiniMax TTS |
| Scene timing | `scenes.json` and `audioConfig.ts` templates for audio-driven scene durations |
| Narration | Data-driven per-scene audio generation, duration probing, manifest output, and resumable generation |
| 3D video | Remotion Three guidance for cameras, GLTF models, video textures, and coordinate pitfalls |
| Tutorial design | Process-animation patterns for explanatory and educational videos |
| Documentation | English and Simplified Chinese READMEs |
| Release automation | CI verification, Release Please, moving tags, and release asset upload without npm publishing |

## Install

Clone the repository into your Codex skills directory or download a release
archive and place it there:

```sh
git clone https://github.com/Albert-PZY/motion-reel.git ~/.codex/skills/motion-reel
```

On Windows PowerShell:

```powershell
git clone https://github.com/Albert-PZY/motion-reel.git "$env:USERPROFILE\.codex\skills\motion-reel"
```

Start a new Codex session after installing the skill so the metadata can be
discovered.

## Usage

Invoke the skill explicitly:

```text
Use $motion-reel to create a 90-second Remotion explainer video about gradient descent with narration.
```

It also triggers naturally for requests involving Remotion, programmatic video,
React video, TTS-narrated tutorials, captions, music visualizers, data-driven
videos, and 3D video scenes.

Example prompts:

```text
Use $motion-reel to build a Remotion video that explains Python decorators in Chinese with scene-timed narration.
```

```text
Use $motion-reel to debug why my @remotion/three camera keeps shaking during render.
```

```text
Use $motion-reel to create a data-driven yearly review video from this JSON file.
```

## Skill Layout

| Path | Purpose |
|---|---|
| `SKILL.md` | Main Codex skill instructions and trigger metadata |
| `agents/openai.yaml` | Codex UI metadata |
| `references/remotion-patterns.md` | Remotion animation, media, rendering, player, and caption patterns |
| `references/tts.md` | Edge TTS and MiniMax TTS setup, audio timing, and sync guidance |
| `references/three.md` | `@remotion/three` camera, model, texture, and coordinate guidance |
| `references/tutorial-video.md` | Explainer-video pacing, script structure, and process animation patterns |
| `templates/scenes.json` | Copyable narration scene data template |
| `templates/audioConfig.ts` | Copyable scene timing template |
| `scripts/generate_audio_edge.py` | Edge TTS helper for Remotion projects |
| `scripts/generate_audio_minimax.py` | MiniMax TTS helper for Remotion projects |

## TTS Helpers

The Python scripts are intended to be copied into a Remotion project. Scene
narration lives in `scripts/scenes.json`, so most projects should edit data
rather than Python source. The scripts assume `ffprobe` is available for
duration detection.

Use uv:

```sh
uv venv
cp templates/scenes.json scripts/scenes.json
uv add edge-tts
uv run python scripts/generate_audio_edge.py
```

For MiniMax:

```sh
cp templates/scenes.json scripts/scenes.json
uv add requests
export MINIMAX_API_KEY="your-api-key"
export MINIMAX_VOICE_ID="your-voice-id"
uv run python scripts/generate_audio_minimax.py
```

The scripts generate audio under `public/audio/`, write `src/audioConfig.ts`,
and keep a JSON manifest next to the audio files.

## Development

Use pnpm only:

```sh
pnpm install
pnpm lint
pnpm test
pnpm build
```

The local checks validate:

- required skill files and metadata;
- absence of UTF-8 BOM and CRLF line endings in text files;
- README structure in both languages;
- Python helper syntax;
- release archive creation at `dist/motion-reel.zip`.

## Release

Normal changes should be committed with Conventional Commits:

```sh
git commit -m "feat: add codex remotion skill"
```

Pushes to `main` run CI and Release Please. When Release Please opens a release
PR, merge it to publish the next GitHub Release and upload the skill archive.
See [docs/release-process.md](docs/release-process.md) for the full workflow.

## Contributing

Before opening a pull request, read [CONTRIBUTING.md](CONTRIBUTING.md). Commits
must follow [Conventional Commits 1.0.0][conventional-commits] and should be
split by logical change category.

Keep generated video output, local virtual environments, credentials, and
dependency folders out of commits.

## License

[MIT](LICENSE)

[conventional-commits]: https://www.conventionalcommits.org/en/v1.0.0/ "Conventional Commits 1.0.0"
[original-skill]: https://github.com/wshuyi/remotion-video-skill "Original remotion-video skill"
[remotion-docs]: https://www.remotion.dev/docs "Remotion documentation"
