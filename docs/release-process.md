# 发布流程

Motion Reel 使用 GitHub Actions 和 Release Please 自动发布 GitHub Release。
发布产物是 Codex Skill 压缩包，不发布 npm 包。

## 自动化内容

推送到 `main` 后会触发：

1. `CI` workflow：
   - 安装 pnpm；
   - 运行 `pnpm install --frozen-lockfile`；
   - 运行 `pnpm lint`；
   - 运行 `pnpm test`；
   - 运行 `pnpm build`。
2. `Release Please` workflow：
   - 根据 Conventional Commits 创建或更新发布 PR；
   - 合并发布 PR 后创建 GitHub Release；
   - 创建精确 tag，例如 `v0.2.0`；
   - 同步移动 tag，例如 `v0` 和 `v0.2`；
   - 构建并上传 `motion-reel.zip`。

## 发版步骤

1. 按 Conventional Commits 提交变更。
2. 推送到 `main` 或合并普通 PR。
3. 等待 Release Please 创建发布 PR。
4. 检查发布 PR 中的版本号和 `CHANGELOG.md`。
5. 合并发布 PR。
6. 到 GitHub Release 页面确认 `motion-reel.zip` 已上传。

## 触发版本的提交

会触发版本发布：

```text
feat: add new skill workflow
fix: correct tts setup guidance
perf: reduce validation overhead
feat!: change public skill layout
```

通常不会触发版本发布：

```text
docs: fix typo
test: add readme validation
chore: update repository metadata
```

## 手动本地验证

```bash
pnpm install
pnpm lint
pnpm test
pnpm build
```

构建成功后应生成：

```text
dist/motion-reel.zip
```

## 故障处理

### 没看到发布 PR

确认最近合入 `main` 的提交是否包含 `feat`、`fix`、`perf` 或 breaking change。
纯 `docs`、`test`、`chore` 通常不会触发发布 PR。

### Release 创建了但没有附件

重新运行失败的 `Release Please` workflow。若仍失败，检查 `pnpm build` 是否能在本地
生成 `dist/motion-reel.zip`。

### 版本 tag 指向不正确

Release workflow 会强制同步 `vX` 和 `vX.Y` 移动 tag。精确 tag `vX.Y.Z` 由
Release Please 创建，不应手动改写。

### 误加入 npm 发布

移除相关步骤。该仓库的发布目标只有 GitHub Release 与 Skill 归档附件。

