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

Before the host-specific route, keep these two scope decisions separate:

- onboarding setup access
  - default: this setup repo URL or direct reads of this repo's docs
  - do not default `memory-palace-setup` itself to persistent global
    installation
- runtime skill or rule visibility
  - if the user wants something installed persistently, prioritize the main
    repo's runtime `memory-palace` layer
  - repo-local `AGENTS.md` remains the concrete runtime anchor and compatibility
    path for IDE hosts
- MCP binding
  - for the setup-repo-managed global path, the host MCP config is user-level
    but still points at one selected local `Memory-Palace` checkout
  - do not change the existing MCP routing logic just because the user asked
    about onboarding access or runtime skill visibility

### Cursor

- route: repo-local `AGENTS.md + MCP`
- preferred persistent runtime projection:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host cursor --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host cursor --repo /path/to/local/Memory-Palace-checkout --check
```

- user-level runtime surface:
  - visible global skill: `~/.cursor/skills-cursor/memory-palace/`
  - compatibility projection: `~/.cursor/skills/memory-palace/`
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
  - the global runtime layer can remain visible even if the selected checkout
    later breaks; tool calls still depend on that checkout

### Windsurf

- route: repo-local `AGENTS.md + MCP`
- preferred persistent runtime projection:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host windsurf --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host windsurf --repo /path/to/local/Memory-Palace-checkout --check
```

- user-level runtime surface:
  - visible global skill: `~/.codeium/windsurf/skills/memory-palace/`
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
  - the global runtime layer can remain visible even if the selected checkout
    later breaks; tool calls still depend on that checkout

### VSCode-host

- route: repo-local `AGENTS.md + MCP`
- preferred persistent runtime projection:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host vscode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host vscode --repo /path/to/local/Memory-Palace-checkout --check
```

- user-level runtime surface:
  - visible global skill: `~/.copilot/skills/memory-palace/`
  - visible custom agent: `~/.copilot/agents/memory-palace.agent.md`
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
  - the global runtime layer can remain visible even if the selected checkout
    later breaks; tool calls still depend on that checkout

### Antigravity

- route: repo-local `AGENTS.md + MCP`
- preferred persistent runtime projection:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host antigravity --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host antigravity --repo /path/to/local/Memory-Palace-checkout --check
```

- user-level runtime surface:
  - `~/.gemini/antigravity/global_workflows/memory-palace.md`
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
  - the global runtime workflow can remain visible even if the selected
    checkout later breaks; tool calls still depend on that checkout

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

- a user/global runtime skill install by default
- optional repo-local mirrors only when they explicitly want current-checkout
  visibility too
- a client MCP entry that points to the current checkout
- one successful smoke call

IDE-host users should end up with:

- access to the setup repo URL or this repo's docs when they need onboarding
- a user/global runtime `memory-palace` projection when they want that layer
  visible across folders
- repo-local `AGENTS.md` in scope
- an actual host config file containing `mcpServers.memory-palace`
- the host visibly seeing `memory-palace`
- one successful smoke call
