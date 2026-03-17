---
description: 'Memory Palace setup workflow: route users to the correct install path, prefer skills plus MCP, and guide first-run setup step by step.'
---

# /memory-palace-setup

## Preconditions

- The request is about installing, configuring, connecting, or troubleshooting first-run setup for the Memory Palace project itself.
- Prefer the full `skills + MCP` path when the user wants normal client usage.
- Do not use this workflow for normal durable-memory operations after setup is already working.

## Inputs

- User request: `$ARGUMENTS`
- Prefer repository-local rule files: `AGENTS.md`, and accept legacy `GEMINI.md` only when needed.
- Prefer repo-visible setup docs from the Memory Palace repo when they exist:
  - `docs/skills/SKILLS_QUICKSTART.md`
  - `docs/skills/GETTING_STARTED.md`
  - `docs/skills/IDE_HOSTS.md`
  - `docs/GHCR_QUICKSTART.md`

## Execution

1. Determine whether the user wants service-only setup or full client integration.
2. For supported clients, recommend `skills + MCP` before `MCP-only`.
3. Explain that skill discovery and MCP binding are two different layers.
4. Give one step at a time, with exact commands and a short success signal after each step.
5. For `Cursor` and `Antigravity`, treat the project integration path as repo-local `AGENTS.md + render_ide_host_config.py`.
6. If the user copied Docker `/app/...` paths into a local `.env`, stop and correct that before continuing.
7. On native Windows, warn that repo-local wrapper commands require `Git Bash` or `WSL`.

## Verification

- The answer prefers `skills + MCP` for normal usage.
- `MCP-only` is framed as a fallback, not the default.
- The explanation separates service startup from client integration.
- The steps are incremental and checkable.

## Output

- A concise, step-by-step setup plan
- Clear stop conditions when prerequisites are missing
