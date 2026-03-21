# Host Matrix

Use this file when the user needs a quick host-by-host routing decision.

Target project repo:

```text
https://github.com/AGI-is-going-to-arrive/Memory-Palace
```

## Object Distinction

Always keep these separate:

- onboarding router:
  - `memory-palace-setup`
- runtime skill from the main repo:
  - `memory-palace`

## CLI Clients

### Claude Code

- route: CLI `skills + MCP`
- stable default:
  - `python scripts/install_skill.py --targets claude --scope user --with-mcp --force`
- optional add-on:
  - workspace/project-level entry
- checks:
  - `claude mcp list`
  - installer `--check`

### Codex CLI

- route: CLI `skills + MCP`
- stable default:
  - `python scripts/install_skill.py --targets codex --scope user --with-mcp --force`
- important boundary:
  - user-scope MCP first
- checks:
  - `codex mcp list`
  - installer `--check`

### Gemini CLI

- route: CLI `skills + MCP`
- stable default:
  - `python scripts/install_skill.py --targets gemini --scope user --with-mcp --force`
- important boundary:
  - user-scope first
  - workspace optional
  - installer also manages `memory-palace-overrides.toml`
- checks:
  - `gemini skills list --all`
  - `gemini mcp list`
  - installer `--check`

### OpenCode

- route: CLI `skills + MCP`
- stable default:
  - `python scripts/install_skill.py --targets opencode --scope user --with-mcp --force`
- important boundary:
  - user-scope MCP first
  - do not describe it as “natively out-of-the-box”
- checks:
  - `opencode mcp list`
  - installer `--check`

## IDE Hosts

### Cursor

- route: repo-local `AGENTS.md + MCP`
- preferred automation:

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/local/Memory-Palace-checkout --check
```

- fallback command:

```bash
python scripts/render_ide_host_config.py --host cursor
```

- actual config surface on current macOS path:
  - `~/.cursor/mcp.json`
- important boundary:
  - if a host CLI reports success, still verify the config file really contains
    `mcpServers.memory-palace`

### Windsurf

- route: repo-local `AGENTS.md + MCP`
- preferred automation:

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host windsurf --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host windsurf --repo /path/to/local/Memory-Palace-checkout --check
```

- fallback render command:

```bash
python scripts/render_ide_host_config.py --host windsurf
```

- actual config surface on current macOS path:
  - `~/Library/Application Support/Windsurf/User/mcp.json`
- important boundary:
  - verify the local Windsurf CLI really supports `--add-mcp`
  - after automation, verify the actual host config file contains
    `mcpServers.memory-palace`

### VSCode-host

- route: repo-local `AGENTS.md + MCP`
- preferred automation:

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/local/Memory-Palace-checkout --check
```

- fallback render command:

```bash
python scripts/render_ide_host_config.py --host vscode
```

- actual config surface on current macOS path:
  - `~/Library/Application Support/Code/User/mcp.json`
- important boundary:
  - confirm the local `code` binary really belongs to VS Code, not Cursor or another editor fork

### Antigravity

- route: repo-local `AGENTS.md + MCP`
- preferred automation:

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/local/Memory-Palace-checkout --check
```

- fallback render command:

```bash
python scripts/render_ide_host_config.py --host antigravity
```

- compatibility command:

```bash
python scripts/render_ide_host_config.py --host antigravity --launcher python-wrapper
```

- extra boundary:
  - prefer `AGENTS.md`
  - accept legacy `GEMINI.md` only when needed
  - optional workflow projection remains an extra layer
  - actual config surface on current macOS path is commonly
    `~/.gemini/antigravity/mcp_config.json`
  - keep `~/.gemini/antigravity/global_workflows/memory-palace.md` aligned with
    the main repo when automation is available

## Platform Matrix

### Native Windows

- repo-local default launcher:
  - `backend/mcp_wrapper.py`
- message:
  - do not lead with `Git Bash` / `WSL`
- `Git Bash` / `WSL` only matter if the user explicitly wants the POSIX wrapper

### macOS / Linux

- repo-local default launcher:
  - `scripts/run_memory_palace_mcp_stdio.sh`

### WSL / Git Bash

- treat as POSIX shell environments
- use the shell wrapper path when the user intentionally chose that route

## Default End State

CLI users should end up with:

- synced or installed runtime skill
- a client MCP entry that points to the current checkout
- one successful smoke call

IDE-host users should end up with:

- repo-local `AGENTS.md` in scope
- an actual host config file containing `mcpServers.memory-palace`
- the host visibly seeing `memory-palace`
- one successful smoke call
