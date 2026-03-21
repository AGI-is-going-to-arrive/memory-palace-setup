---
name: memory-palace-setup
description: >-
  Use this skill when the user wants to install, configure, connect, or
  troubleshoot first-run setup for the Memory Palace project itself. Route
  correctly for Claude Code, Codex CLI, Gemini CLI, OpenCode, Cursor,
  Windsurf, VSCode-host, and Antigravity; distinguish the onboarding
  `memory-palace-setup` skill from the main repo's canonical `memory-palace`
  skill; prefer skills plus MCP over MCP-only; choose CLI user-scope installs
  versus IDE-host AGENTS.md plus MCP snippet paths; handle native Windows via
  `backend/mcp_wrapper.py` and POSIX hosts via
  `scripts/run_memory_palace_mcp_stdio.sh`; inspect local facts before
  suggesting commands; and guide the user step by step through validation and
  common failures such as Docker `/app/...` paths, wrong scope, service-vs-
  client confusion, or Dashboard setup-assistant ambiguity. Chinese trigger
  hints: 安装配置这个项目, 首次接通, skills+mcp, mcp-only 太麻烦, 一步步引导,
  Claude/Codex/Gemini/OpenCode/Cursor/Windsurf/VSCode/Antigravity.
---

# Memory Palace Setup

Use this skill for first-time onboarding of the **Memory Palace project itself**.

This is a setup-and-routing skill, not the durable-memory operation skill.

## Separate The Two Layers First

Explain this immediately when the user is confused:

- `memory-palace-setup`
  - the onboarding skill in this repository
- `memory-palace`
  - the canonical runtime skill shipped by the main `Memory-Palace` repository

Also explain:

- service startup is not the same as client integration
- a running Dashboard / API / SSE service does not mean the user's client is
  already connected
- for `Cursor / Windsurf / VSCode-host / Antigravity`, seeing the
  `memory-palace` skill does **not** prove MCP is installed yet

## Default Stance

- Prefer **skills + MCP** for supported clients.
- Treat **MCP-only** as a fallback for explicit Docker `/sse`, remote-only, or
  no-skill environments.
- Default to **Profile B** to get the system running with the fewest extra
  services.
- Recommend **Profile C** once local embedding / reranker services are ready.
- Recommend **Profile D** once remote APIs or a hosted environment are already
  part of the plan.

## First-Pass Routing

Before giving commands, determine these facts:

1. Which host is the user trying to use?
   - `Claude Code`
   - `Codex CLI`
   - `Gemini CLI`
   - `OpenCode`
   - `Cursor`
   - `Windsurf`
   - `VSCode-host`
   - `Antigravity`
   - service-only (`Dashboard / API / SSE`)
2. What is the user trying to do?
   - run the service only
   - connect a CLI client to the current repo
   - connect an IDE host to the current repo
   - connect to Docker `/sse` only
3. What platform boundary matters?
   - native Windows
   - macOS / Linux
   - `WSL` / `Git Bash`
4. What is already present?
   - repo checkout
   - `.env` or `.env.docker`
   - `backend/.venv`
   - `scripts/sync_memory_palace_skill.py`
   - `scripts/install_skill.py`
   - `scripts/render_ide_host_config.py`

If one concise question can disambiguate the path, ask it. Otherwise inspect
the repo first.

## Platform Rules

- native Windows repo-local stdio default:
  - `backend/mcp_wrapper.py`
- macOS / Linux / `WSL` / `Git Bash` repo-local stdio default:
  - `scripts/run_memory_palace_mcp_stdio.sh`
- On Windows, do not lead with “you must use Git Bash / WSL.”
- On Windows, `Git Bash / WSL` are only relevant when the user explicitly wants
  the POSIX wrapper path.
- Do not tell the user to copy Docker `/app/...` or `/data/...` paths into a
  host `.env`.
- For `Cursor`, `Antigravity`, and `VSCode-host`, prefer an automatic local config write when
  the host CLI or config surface is known; otherwise fall back to rendered
  snippet + manual paste.
- For `Windsurf`, stay conservative unless the local machine proves a stable
  host CLI path.

## Repo-Visible Sources To Prefer

When the main `Memory-Palace` repo is present, prefer these paths:

- `README.md`
- `docs/README.md`
- `docs/skills/SKILLS_QUICKSTART.md`
- `docs/skills/GETTING_STARTED.md`
- `docs/skills/CLI_COMPATIBILITY_GUIDE.md`
- `docs/skills/IDE_HOSTS.md`
- `docs/GHCR_QUICKSTART.md`
- `scripts/sync_memory_palace_skill.py`
- `scripts/install_skill.py`
- `scripts/render_ide_host_config.py`
- `scripts/run_memory_palace_mcp_stdio.sh`
- `backend/mcp_wrapper.py`

## Routing Rules

- For CLI clients, read `references/cli-routing.md`.
- For all host-specific differences, read `references/host-matrix.md`.
- For service-only, Docker, GHCR, or `/sse` paths, read
  `references/service-modes.md`.
- For step-by-step validation, read `references/validation-matrix.md`.
- For common setup failures or boundary conditions, read
  `references/common-failures.md`.
- For automatic IDE-host MCP config, read `references/host-matrix.md` first and
  prefer `scripts/apply_ide_mcp.py` when the host is `Cursor`,
  `Antigravity`, or `VSCode-host`.
- If the user is looking at Dashboard first-run setup UI or screenshots, read
  `references/ui-setup-assistant.md`.

## Mandatory Workflow

1. State which object is being installed right now:
   - onboarding skill
   - canonical runtime skill
2. Diagnose the user's host, goal, platform, and scope.
3. Recommend the smallest correct path.
4. Prefer one copyable command block per step.
5. After each step, tell the user what success should look like.
6. Validate with the smallest relevant check before moving on.
7. Do not stop at `mcp list`; require at least one real smoke call.
8. If a prerequisite is missing, stop and say exactly what must be fixed first.

## Hard Rules

- Do not recommend `MCP-only` as the primary path when the user wants normal
  daily use on a supported host.
- Do not assume “the service is running” means “the client is connected.”
- Do not present hidden skill mirrors as the default entry path for IDE hosts.
- For IDE hosts, route to repo-local `AGENTS.md + render_ide_host_config.py`.
- For `Cursor`, `Antigravity`, and `VSCode-host`, prefer automatic MCP config
  before asking the user to paste JSON manually.
- If the host CLI claims success, still verify the actual config file changed.
- For CLI clients, prefer **user-scope first**.
- Only add workspace/project-level entries when they are actually needed,
  especially for `Claude` and `Gemini`.
- Treat `Codex` and `OpenCode` as **user-scope MCP first**.
- Treat the Dashboard setup assistant as a convenience layer, not proof that
  the client integration is complete.

## Output Contract

Your answer should usually contain:

- one short diagnosis
  - current host
  - current platform
  - current mode
  - current scope
- one step at a time
- exact commands
- one verification signal after each step
- one real smoke step before calling setup “done”
- one explicit next step

Do not dump every path at once unless the user asks for a comparison.

## Example Prompts That Should Trigger This Skill

- “使用这个 skill 帮我安装配置 Memory Palace 项目。”
- “Help me install and configure Memory Palace step by step.”
- “我想让 Claude Code / Codex / Gemini / OpenCode 接这个项目，优先走 skills + MCP。”
- “我想让 Cursor / Windsurf / VSCode-host / Antigravity 接这个项目。”
- “帮我判断我是该走 repo-local，还是 Docker `/sse`。”
- “我只配了 MCP，但现在想补完整的 skill 安装。”

## Example Prompts That Should Not Trigger This Skill

- “帮我写一条长期记忆。”
- “为什么 `guard_action=NOOP`？”
- “修一下前端页面布局。”
- “解释一下 SQLite 检索实现。”
