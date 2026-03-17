# CLI Routing

Use this file when the user wants to connect **Claude Code**, **Codex CLI**, or **Gemini CLI** to the **Memory Palace** project.

## Core rule

For supported CLI clients, prefer:

1. install or sync the repo-local `memory-palace` skill
2. bind MCP to the current repo
3. validate

Do **not** start with `MCP-only` unless the user explicitly wants Docker `/sse` only.

## Explain the two layers first

- **skill discovery**
  - decides when the client should enter the Memory Palace workflow
- **MCP binding**
  - points the client to the real backend in the current repo

If either layer is missing, the setup is incomplete.

## Fresh-machine default for CLI daily use

Inside the Memory Palace repo:

```bash
python scripts/sync_memory_palace_skill.py
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --force
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --check
```

Why this default:

- it installs the repo’s own `memory-palace` skill mirrors
- it prefers the more stable user-scope MCP path on fresh machines
- it is easier to explain than mixing workspace and user scopes too early

## Claude Code

Recommended first move:

```bash
python scripts/install_skill.py --targets claude --scope user --with-mcp --force
```

Useful checks:

```bash
claude mcp list
python scripts/install_skill.py --targets claude --scope user --with-mcp --check
```

Optional:

- If the user also wants a project-level entry in the current repo, add a workspace install afterward.

## Codex CLI

Recommended first move:

```bash
python scripts/install_skill.py --targets codex --scope user --with-mcp --force
```

Useful checks:

```bash
codex mcp list
python scripts/install_skill.py --targets codex --scope user --with-mcp --check
```

Important boundary:

- Do not oversell workspace-local MCP as the stable default for Codex in this project.
- The stable message is: repo-local skill discovery plus **user-scope MCP binding**.

## Gemini CLI

Recommended first move:

```bash
python scripts/install_skill.py --targets gemini --scope user --with-mcp --force
```

Useful checks:

```bash
gemini skills list --all
gemini mcp list
python scripts/install_skill.py --targets gemini --scope user --with-mcp --check
```

Important boundary:

- Workspace-level Gemini entry can exist, but user-scope install is the more stable default on fresh machines.

## When to mention workspace install

Only mention workspace install when the user specifically wants:

- the current repo to contain a visible project-level entry
- or an additional local mirror for Claude or Gemini

Then use:

```bash
python scripts/install_skill.py --targets claude,gemini --scope workspace --with-mcp --force
```

## What success looks like

The user should end up with:

- the repo’s canonical `memory-palace` skill under `docs/skills/memory-palace/`
- client-local skill mirrors or user-scope skill installs
- a client MCP entry pointing to the current repo’s `scripts/run_memory_palace_mcp_stdio.sh`

Never describe the setup as complete before both skill discovery and MCP binding are checked.
