[English](README.md)

# Motion Reel

> 面向 Codex 的 Remotion 编程式视频 Skill，支持 React 视频、场景化配音、字幕、数据驱动动画和 3D 动效。

Motion Reel 将原本面向 Claude 的 Remotion 视频 Skill 改造成 Codex 原生
Skill。它为 Codex 提供一套清晰的工作流，用于规划、实现、调试和渲染
Remotion 视频，并覆盖场景数据、TTS 配音、音画同步、视觉节奏和可重复发布产物。

这个仓库本身就是一个可用的 Codex Skill 目录：`SKILL.md` 是运行时入口，
`references/` 放按需读取的深入指南，`templates/` 放可复制的项目模板，
`scripts/` 放 TTS 与发布校验辅助脚本。

## 来源与致谢

本项目基于 [wshuyi/remotion-video-skill][original-skill] 改造。原仓库提供了
面向 Claude 工作流的 Remotion 与 TTS 知识基础。Motion Reel 保留其中有价值的
视频制作模式，同时按 Codex 规范重构触发描述、pnpm 优先的 Node 工作流、
uv 管理的 Python 辅助脚本、双语文档，以及不发布 npm 包的 GitHub Release
自动化。

## 快速入口

- [Codex Skill 入口](SKILL.md)
- [英文 README](README.md)
- [提交规范](docs/git-commit-guidelines.md)
- [发布流程](docs/release-process.md)
- [Remotion 官方文档][remotion-docs]
- [原始上游 Skill][original-skill]

## 发布状态

Motion Reel 使用 Semantic Versioning 和稳定 GitHub Release，例如 `v0.1.0`。
发布自动化基于 Conventional Commits 和 Release Please。合并发布 PR 后，
工作流会创建 GitHub Release、精确版本 tag、移动 tag `vX` 与 `vX.Y`，
并上传可下载的 `motion-reel.zip` Skill 归档。

发布流程刻意不发布到 npm。本仓库作为 Codex Skill 目录或 Release 归档使用，
不是 npm registry 包。

## 主要能力

| 领域 | 支持情况 |
|---|---|
| Codex 兼容 | 原生 `SKILL.md` frontmatter、精简触发描述和 `agents/openai.yaml` 元数据 |
| Remotion 工作流 | 项目检查、Composition 配置、时间线模式、渲染命令和验证步骤 |
| 包管理 | 只使用 pnpm 的 Node 指南和 CI 脚本 |
| Python 辅助 | 使用 uv 的 Edge TTS 与 MiniMax TTS 脚本 |
| 场景时长 | `audioConfig.ts` 模板和音频驱动的场景时长计算 |
| 配音 | 单场景音频生成、时长检测、manifest 输出和断点续作 |
| 3D 视频 | Remotion Three 的相机、GLTF、视频纹理和坐标陷阱指南 |
| 教程视频 | 面向讲解视频的过程动画、脚本节奏和视觉引导模式 |
| 文档 | 英文与简体中文 README |
| 发布自动化 | CI 校验、Release Please、移动 tag 和 Release 附件上传，不发布 npm |

## 安装

把仓库克隆到 Codex skills 目录，或下载 Release 归档后放到该目录：

```sh
git clone https://github.com/Albert-PZY/motion-reel.git ~/.codex/skills/motion-reel
```

Windows PowerShell：

```powershell
git clone https://github.com/Albert-PZY/motion-reel.git "$env:USERPROFILE\.codex\skills\motion-reel"
```

安装后开启新的 Codex 会话，让 Skill 元数据被重新发现。

## 使用方式

可以显式调用：

```text
Use $motion-reel to create a 90-second Remotion explainer video about gradient descent with narration.
```

当任务涉及 Remotion、编程式视频、React 视频、TTS 配音教程、字幕、音乐可视化、
数据驱动视频或 3D 视频场景时，也适合自然触发。

示例提示词：

```text
Use $motion-reel to build a Remotion video that explains Python decorators in Chinese with scene-timed narration.
```

```text
Use $motion-reel to debug why my @remotion/three camera keeps shaking during render.
```

```text
Use $motion-reel to create a data-driven yearly review video from this JSON file.
```

## Skill 结构

| 路径 | 用途 |
|---|---|
| `SKILL.md` | Codex Skill 主说明与触发元数据 |
| `agents/openai.yaml` | Codex UI 元数据 |
| `references/remotion-patterns.md` | Remotion 动画、媒体、渲染、播放器和字幕模式 |
| `references/tts.md` | Edge TTS 与 MiniMax TTS 配置、音频时长和同步指南 |
| `references/three.md` | `@remotion/three` 相机、模型、纹理和坐标指南 |
| `references/tutorial-video.md` | 教程视频节奏、脚本结构和过程动画模式 |
| `templates/audioConfig.ts` | 可复制的场景时长模板 |
| `scripts/generate_audio_edge.py` | 面向 Remotion 项目的 Edge TTS 辅助脚本 |
| `scripts/generate_audio_minimax.py` | 面向 Remotion 项目的 MiniMax TTS 辅助脚本 |

## TTS 辅助脚本

Python 脚本预期复制到具体 Remotion 项目中，并按该项目的场景脚本修改。
它们依赖 `ffprobe` 检测音频时长。

使用 uv：

```sh
uv venv
uv add edge-tts
uv run python scripts/generate_audio_edge.py
```

MiniMax：

```sh
uv add requests
export MINIMAX_API_KEY="your-api-key"
export MINIMAX_VOICE_ID="your-voice-id"
uv run python scripts/generate_audio_minimax.py
```

脚本会在 `public/audio/` 下生成音频，写入 `src/audioConfig.ts`，并在音频目录旁
输出 JSON manifest。

## 开发

只使用 pnpm：

```sh
pnpm install
pnpm lint
pnpm test
pnpm build
```

本地检查会验证：

- 必需的 Skill 文件与元数据；
- 文本文件没有 UTF-8 BOM 和 CRLF 行尾；
- 中英文 README 结构；
- Release 归档能生成到 `dist/motion-reel.zip`。

## 发布

日常变更使用 Conventional Commits：

```sh
git commit -m "feat: add codex remotion skill"
```

推送到 `main` 后会运行 CI 和 Release Please。Release Please 创建发布 PR 后，
合并该 PR 即可发布下一个 GitHub Release 并上传 Skill 归档。完整流程见
[docs/release-process.md](docs/release-process.md)。

## 贡献

提交 PR 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。所有提交必须遵守
[Conventional Commits 1.0.0][conventional-commits]，并按逻辑类别拆分。

不要提交生成的视频输出、本地虚拟环境、凭据和依赖目录。

## 许可证

[MIT](LICENSE)

[conventional-commits]: https://www.conventionalcommits.org/zh-hans/v1.0.0/ "Conventional Commits 1.0.0"
[original-skill]: https://github.com/wshuyi/remotion-video-skill "Original remotion-video skill"
[remotion-docs]: https://www.remotion.dev/docs "Remotion documentation"

