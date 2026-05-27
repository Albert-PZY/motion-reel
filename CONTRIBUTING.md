# Contributing to Motion Reel

## Workflow

- Use `pnpm` for all Node scripts.
- Do not use `npm` or `npx` in this repository.
- Use `uv` for Python helper dependencies.
- Keep changes small and split by logical area.
- Run `pnpm lint`, `pnpm test`, and `pnpm build` before opening a PR.

## Commit Format

This repository follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

```text
<type>[optional scope]: <short summary>
```

Recommended types:

- `feat`: new user-facing skill behavior or resources
- `fix`: bug fixes or corrected guidance
- `docs`: documentation-only changes
- `test`: validation-only changes
- `refactor`: internal restructuring without behavior change
- `ci`: GitHub Actions or release pipeline changes
- `build`: build tooling or packaging changes
- `chore`: repository maintenance

Examples:

```text
feat: add codex remotion skill
fix(tts): preserve generated audio config newlines
docs: add release process
ci: upload skill archive from release workflow
```

## Pull Request Expectations

- Describe the behavior or documentation change clearly.
- List the commands used to verify the change.
- Keep credentials, local virtual environments, generated videos, dependency
  directories, and release archives out of commits.
- Do not add npm publishing steps to the release workflow.

## Release Discipline

- Group unrelated changes into separate commits.
- Prefer one commit per feature or repair.
- Use `feat`, `fix`, `perf`, or breaking-change markers when a release should be
  created.
- Release Please creates GitHub Releases and archives; npm publication is out of
  scope for this repository.

