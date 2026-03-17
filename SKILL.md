---
name: memory-palace-setup
description: >-
  Use this skill when the user wants to install, configure, connect, or
  troubleshoot first-run setup for the Memory Palace project itself. Prefer the
  full skills plus MCP path over MCP-only; route correctly for Claude Code,
  Codex CLI, Gemini CLI, Cursor, and Antigravity; distinguish repo-local setup
  from Docker or SSE-only service mode; inspect local facts before suggesting
  commands; and guide the user step by step through sync, install, validation,
  and common failures such as missing .env, Docker /app paths, wrong scope, or
  Windows shell mismatches. Chinese trigger hints: 安装配置这个项目, 首次接通,
  skills+mcp, mcp-only 太麻烦, 一步步引导, Claude/Codex/Gemini/Cursor/Antigravity.
---

# Memory Palace Setup

Use this skill for first-time onboarding of the **Memory Palace project itself**.

This is a setup and routing skill, not the durable-memory operation skill.

## Use this skill when

- The user wants to install or configure Memory Palace.
- The user wants step-by-step guidance instead of reading multiple docs.
- The user is wiring up a client such as Claude Code, Codex CLI, Gemini CLI, Cursor, or Antigravity.
- The user is unsure whether to use `skills + MCP` or `MCP-only`.
- The user is stuck on first-run setup, skill discovery, MCP binding, or repo-local path issues.

## Do not use this skill when

- The user is already set up and wants normal Memory Palace operations such as `read_memory`, `search_memory`, or write-guard handling.
- The task is generic coding, docs editing, UI work, or test debugging outside the setup flow.
- The task is about another project.

When setup is complete and the user wants actual memory workflows, switch to the main `memory-palace` skill.

## Default stance

- Prefer **skills + MCP** for supported clients.
- Treat **MCP-only** as a fallback for explicit Docker or SSE-only goals, remote-only setups, or environments that cannot install skills.
- Do not present `MCP-only` as the default daily-use path for this project.

## First-pass routing

Before giving commands, determine these facts:

1. Which client or host is the user trying to use?
   - `Claude Code`
   - `Codex CLI`
   - `Gemini CLI`
   - `Cursor`
   - `Antigravity`
   - Service-only (`Dashboard / API / SSE`) with no client integration
2. Is the user trying to:
   - run the service only
   - connect a client to the current repo
   - connect to Docker `/sse` only
3. What platform boundary matters?
   - macOS or Linux
   - native Windows
4. What is already present?
   - repo checkout
   - `.env` or `.env.docker`
   - `backend/.venv`
   - `scripts/sync_memory_palace_skill.py`
   - `scripts/install_skill.py`
   - `scripts/render_ide_host_config.py`

If one concise question can disambiguate the entire path, ask it. Otherwise inspect the repo first.

## Deployment profile rule

When the user asks which deployment profile to start with:

- Default to **Profile B** as the starting point because it requires the fewest extra services.
- Strongly recommend **Profile C or D** as soon as the user wants real retrieval quality, long-term use, or already has model services ready.
- Do not present Profile B as the best final state unless the user explicitly wants the lowest-dependency local boot only.

## Repo-visible sources to prefer

When the Memory Palace repo is present, prefer these repo-visible paths over paraphrasing from memory:

- `docs/skills/SKILLS_QUICKSTART.md`
- `docs/skills/GETTING_STARTED.md`
- `docs/skills/IDE_HOSTS.md`
- `docs/GHCR_QUICKSTART.md`
- `scripts/sync_memory_palace_skill.py`
- `scripts/install_skill.py`
- `scripts/render_ide_host_config.py`
- `scripts/run_memory_palace_mcp_stdio.sh`

## Mandatory workflow

1. Explain the two layers clearly:
   - skill discovery
   - MCP binding to the current repo
2. Recommend the smallest correct path.
3. Prefer one copyable command block per step.
4. After each step, tell the user what success should look like.
5. Validate with the smallest relevant check before moving on.
6. If a prerequisite is missing, stop and say exactly what must be fixed first.

## Routing rules

- For CLI clients, read `references/cli-routing.md`.
- For service-only, Docker, GHCR, or `/sse` paths, read `references/service-modes.md`.
- For common setup failures, boundary conditions, or platform traps, read `references/common-failures.md`.

## Hard rules

- Do not recommend `MCP-only` as the primary path when the user wants normal client usage on a supported host.
- Do not assume “the service is running” means “the client is connected”.
- Do not tell users to copy Docker `/app/...` database paths into local `.env`.
- On native Windows, warn that repo-local wrapper examples use `bash` or `/bin/zsh`, so `Git Bash` or `WSL` is required.
- For `Codex CLI`, prefer user-scope MCP install when the user needs a stable binding.
- For `Cursor` and `Antigravity`, treat them as IDE hosts for the project integration path.
- When the user wants the project itself in IDE hosts, point them to repo-local `AGENTS.md + render_ide_host_config.py`; this setup skill only supplies the AI guidance layer.

## Output contract

Your answer should usually contain:

- one short diagnosis of the user’s current path
- one step at a time
- exact commands
- one verification signal after each step
- one explicit next step

Do not dump every option at once unless the user asks for a comparison.

## Example prompts that should trigger this skill

- “使用这个 skill 帮我安装配置 Memory Palace 项目。”
- “Help me install and configure Memory Palace step by step.”
- “我想让 Claude Code 接这个项目，优先走 skills + MCP。”
- “帮我判断我是该走 repo-local 还是 Docker `/sse`。”
- “我只配了 MCP，但现在想补完整的 skill 安装。”

## Example prompts that should not trigger this skill

- “帮我写一条长期记忆。”
- “为什么 `guard_action=NOOP`？”
- “修一下前端页面布局。”
- “解释一下 SQLite 检索实现。”
