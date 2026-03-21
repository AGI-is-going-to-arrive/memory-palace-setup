---
name: memory-palace-setup
description: >-
  Use this skill when the user wants to install, configure, connect, or
  troubleshoot first-run setup for the Memory Palace project itself. Distinguish
  the onboarding `memory-palace-setup` skill from the main repo's canonical
  `memory-palace` skill; prefer skills plus MCP over MCP-only; treat this setup
  repo as temporary guidance that can be used by URL or direct doc reads
  without persistent installation; prioritize the main repo's runtime
  `memory-palace` skill when recommending something to install persistently;
  keep the existing MCP logic unchanged; route Windows to
  `backend/mcp_wrapper.py` and POSIX hosts to
  `scripts/run_memory_palace_mcp_stdio.sh`; and guide setup for Claude Code,
  Codex CLI, Gemini CLI, OpenCode, Cursor, Windsurf, VSCode-host, and
  Antigravity. Chinese trigger hints: 安装配置这个项目, 首次接通, skills+mcp,
  github地址, 仓库地址, 不安装也能看, 临时安装引导.
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
  - target repo: `https://github.com/AGI-is-going-to-arrive/Memory-Palace`

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
5. What scope decision is actually being made?
   - onboarding access
     - default: repo URL or direct read of this repo's `README.md` and
       `SKILL.md`
     - persistent installation of `memory-palace-setup` is optional
   - runtime skill visibility
     - if something should be installed persistently, prioritize the main
       repo's `memory-palace` skill
   - MCP binding
     - keep the current host-specific recommendation from the main repo
     - do not silently change MCP scope just because the user asked about
       onboarding access or runtime skill visibility

If one concise question can disambiguate the path, ask it. Otherwise inspect
the repo first.

If the user is explicitly asking for the default cross-host scope policy, do
not ask a host-selection follow-up first. Answer the default split directly:

- onboarding access
  - default to repo URL or direct doc reads
- runtime skill visibility
  - if something should be installed persistently, make that the main repo's
    `memory-palace` skill
  - if the user wants one stable cross-host installer, prefer
    `scripts/apply_runtime_global_setup.py`
- MCP binding
  - keep the current host-specific logic unchanged

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
- For `Cursor`, `Antigravity`, `VSCode-host`, and `Windsurf`, prefer an automatic local config write when
  the host CLI or config surface is known; otherwise fall back to rendered
  snippet + manual paste.
- When the user chooses the global runtime path for IDE hosts, say explicitly:
  - the runtime rule or skill layer is global
  - the IDE MCP config is also user-level
  - but that MCP entry still points to one selected local `Memory-Palace`
    checkout
  - if that checkout is moved, deleted, or broken, tool calls fail even though
    the runtime rule layer still appears available

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
  `Antigravity`, `VSCode-host`, or `Windsurf`.
- For persistent runtime `memory-palace` install or projection across hosts,
  prefer `scripts/apply_runtime_global_setup.py`.
- If the user is looking at Dashboard first-run setup UI or screenshots, read
  `references/ui-setup-assistant.md`.

## Mandatory Workflow

1. State which object is being installed right now:
   - onboarding skill
   - canonical runtime skill
   - when naming the target project, prefer the GitHub repo URL
     `https://github.com/AGI-is-going-to-arrive/Memory-Palace`
   - only switch to a local checkout path when the next command truly needs one
2. Diagnose the user's host, goal, platform, and scope.
3. Separate onboarding access from runtime skill visibility and MCP binding.
4. Default the onboarding layer to repo URL or direct doc reads unless the user
   explicitly wants to install `memory-palace-setup` as a persistent skill.
   - if the user wants the runtime `memory-palace` layer available across
     folders, prefer `scripts/apply_runtime_global_setup.py`
5. Recommend the smallest correct path.
6. Prefer one copyable command block per step.
7. After each step, tell the user what success should look like.
8. Validate with the smallest relevant check before moving on.
9. Do not stop at `mcp list`; require at least one real smoke call.
10. If a prerequisite is missing, stop and say exactly what must be fixed
    first.

When the user asks “global or repo-local by default?” across multiple hosts:

- answer the cross-host default policy first
- only ask a follow-up question afterward if the next command block depends on
  the specific host

## Hard Rules

- Do not recommend `MCP-only` as the primary path when the user wants normal
  daily use on a supported host.
- Do not assume “the service is running” means “the client is connected.”
- Do not collapse onboarding access, runtime skill visibility, and MCP binding
  into one generic scope answer.
- Do not dodge a direct cross-host default-scope question by immediately asking
  “which host?” when the user is clearly asking for the default policy itself.
- Do not default `memory-palace-setup` itself to persistent global installation.
- If the user wants something installed persistently, prioritize the main repo's
  runtime `memory-palace` skill instead.
- If the user wants a stable setup-repo-managed command path for persistent
  runtime install, prefer `scripts/apply_runtime_global_setup.py` before
  spelling out lower-level host-specific script combinations.
- If the user is using an IDE host with global runtime projection, do not hide
  the selected-checkout caveat.
- Do not present hidden skill mirrors as the default entry path for IDE hosts.
- For IDE hosts, route to repo-local `AGENTS.md + render_ide_host_config.py`.
- For `Cursor`, `Antigravity`, `VSCode-host`, and `Windsurf`, prefer automatic MCP config
  before asking the user to paste JSON manually.
- If the host CLI claims success, still verify the actual config file changed.
- For CLI clients, keep the current MCP guidance unchanged:
  - stable default remains **user-scope first**
  - only add workspace/project-level entries when they are actually needed,
    especially for `Claude` and `Gemini`
- Treat `Codex` and `OpenCode` as **user-scope MCP first**.
- Treat the Dashboard setup assistant as a convenience layer, not proof that
  the client integration is complete.

## Output Contract

Your answer should usually contain:

- one short diagnosis
  - current host
  - current platform
  - current mode
  - current onboarding access mode
  - current runtime skill visibility scope
  - current MCP scope
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
- “默认到底该把什么全局安装？MCP 逻辑先别改。”

## Example Prompts That Should Not Trigger This Skill

- “帮我写一条长期记忆。”
- “为什么 `guard_action=NOOP`？”
- “修一下前端页面布局。”
- “解释一下 SQLite 检索实现。”
