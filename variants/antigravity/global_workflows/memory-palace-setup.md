---
description: 'Memory Palace setup workflow: separate onboarding skill from runtime skill, choose the correct CLI or IDE-host path, prefer skills plus MCP, and validate with a real smoke step.'
---

# /memory-palace-setup

## Preconditions

- The request is about installing, configuring, connecting, or troubleshooting
  first-run setup for the Memory Palace project itself.
- Prefer the full `skills + MCP` path when the user wants normal client usage.
- Do not use this workflow for normal durable-memory operations after setup is
  already working.

## Inputs

- User request: `$ARGUMENTS`
- Prefer repository-local rule files: `AGENTS.md`, and accept legacy
  `GEMINI.md` only when needed.
- Prefer repo-visible setup docs from the Memory Palace repo when they exist:
  - `docs/skills/SKILLS_QUICKSTART.md`
  - `docs/skills/GETTING_STARTED.md`
  - `docs/skills/CLI_COMPATIBILITY_GUIDE.md`
  - `docs/skills/IDE_HOSTS.md`
  - `docs/GHCR_QUICKSTART.md`

## Execution

1. Clarify whether the current object is:
   - the onboarding `memory-palace-setup` skill
   - or the main repo's canonical `memory-palace` skill
2. Determine whether the user wants:
   - service-only setup
   - full CLI integration
   - IDE-host integration
   - or `MCP-only` / Docker `/sse`
3. For supported clients, recommend `skills + MCP` before `MCP-only`.
4. Explain that skill discovery and MCP binding are different layers.
5. For `Antigravity`, use repo-local `AGENTS.md + render_ide_host_config.py`.
6. On native Windows, prefer the generated `python-wrapper` path instead of
   leading with `Git Bash` / `WSL`.
7. If the user copied Docker `/app/...` or `/data/...` paths into a local
   `.env`, stop and correct that before continuing.
8. Give one step at a time, with exact commands and a short success signal
   after each step.
9. End with one real smoke step, not just `mcp list`.

## Verification

- The answer prefers `skills + MCP` for normal usage.
- `MCP-only` is framed as a fallback, not the default.
- The explanation separates onboarding skill from runtime skill.
- The explanation separates service startup from client integration.
- The steps are incremental and checkable.
- The final step includes a real Memory Palace smoke call.

## Output

- A concise, step-by-step setup plan
- Clear stop conditions when prerequisites are missing
- One smoke-step instruction before calling setup complete
