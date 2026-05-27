# Repository Instructions

## Language

- Respond to users in Simplified Chinese.
- Keep documentation bilingual when public-facing English documentation exists.

## Package Management

- Use `pnpm` for all frontend and Node.js package workflows.
- Do not use `npm install`, `npm update`, `npm run`, or `npx`.
- Python helper projects must use a project-level virtual environment managed by `uv`.
- Add or remove Python dependencies only with `uv add` and `uv remove`; do not use `pip install` or `pip uninstall`.

## Encoding And Line Endings

- Write generated text files as UTF-8 without BOM.
- Respect `.editorconfig` and `.gitattributes`.
- On Windows, prefer small focused patches and re-read files before follow-up edits.

## Git

- Use Conventional Commits.
- Do not commit generated archives, local virtual environments, dependency folders, credentials, or runtime output.
- Release automation must not publish to npm.

