# Git 提交与版本发布规范

本项目采用 [约定式提交 1.0.0](https://www.conventionalcommits.org/zh-hans/v1.0.0/)
管理提交信息，并通过 Release Please 自动生成版本、CHANGELOG、GitHub Release
和 Skill 归档附件。

本项目不发布 npm 包。

## 提交格式

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

常用写法：

```text
feat: add codex remotion skill
fix(tts): preserve generated audio config newlines
docs: add release process
ci: upload skill archive from release workflow
feat!: change skill resource layout
```

## type 取值

- `feat`: 新功能或新增用户可感知能力。
- `fix`: 修复 bug、错误示例或异常行为。
- `docs`: 只修改文档。
- `test`: 只新增或修改验证脚本。
- `refactor`: 不改变外部行为的代码整理。
- `perf`: 性能优化。
- `ci`: GitHub Actions、发布流水线等 CI/CD 变更。
- `build`: 构建系统、打包配置、依赖范围变更。
- `chore`: 仓库维护、脚手架、非业务性调整。
- `style`: 只改格式，不改语义。
- `revert`: 回滚历史提交。

## 提交粒度

- 不同功能分开提交，例如 Skill 内容、发布 workflow、README 修改不要混在一个
  提交里，除非它们是同一个初始化变更的一部分。
- 每个提交只表达一个清晰意图，英文描述使用小写开头，末尾不加句号。
- 不提交本地密钥、虚拟环境、依赖目录、生成视频、Release 压缩包和临时验证文件。
- 涉及行为变化时，提交前至少运行对应验证；发布相关变更运行完整验证。

## 破坏性变更

破坏性变更必须显式标记，二选一即可：

```text
feat!: change skill resource layout
```

或：

```text
feat(skill): change resource layout

BREAKING CHANGE: references are now loaded from a new directory structure.
```

只要出现 `!` 或 `BREAKING CHANGE:`，Release Please 会按主版本发布处理。

## 版本号规范

本项目使用 SemVer：`MAJOR.MINOR.PATCH`。

- `fix` 对应 `PATCH`，例如 `0.1.0` -> `0.1.1`。
- `feat` 对应 `MINOR`，例如 `0.1.0` -> `0.2.0`。
- `!` 或 `BREAKING CHANGE:` 对应 `MAJOR`，例如 `0.1.0` -> `1.0.0`。
- `docs`、`test`、`refactor`、`ci`、`build`、`chore` 默认不触发版本号提升，
  除非带有破坏性变更标记。

## 发布规则

- 不手动修改 `package.json` 版本号，除非自动化发布链路故障且已经明确需要人工修复。
- 合并 Release Please 创建的发布 PR 后，GitHub Actions 会创建精确 tag：`vX.Y.Z`。
- 每次发布会同步维护主版本 tag `vX` 和次版本 tag `vX.Y`。
- Release workflow 会运行校验并上传 `dist/motion-reel.zip` 到 GitHub Release。
- 不配置 npm token，不执行 package registry 发布。

## 推荐命令

提交前运行：

```bash
pnpm lint
pnpm test
pnpm build
git diff --check
```

提交示例：

```bash
git add SKILL.md references/ README.md README_zh-CN.md
git commit -m "feat: add codex remotion skill"
git push origin main
```

