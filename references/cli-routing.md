# CLI Routing

Use this file when the user wants to connect a CLI client to the
`Memory-Palace` project.

Target project repo:

```text
https://github.com/AGI-is-going-to-arrive/Memory-Palace
```

When talking to the user, name the GitHub repository first. Only switch to a
local checkout path when the next command actually needs the local clone.

Supported CLI clients:

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`
- `OpenCode`

## Core Rule

For supported CLI clients, prefer:

1. sync the repo-local canonical `memory-palace` skill
2. install the client binding with the repo script
3. validate the MCP binding
4. run one real smoke call

Do **not** start with `MCP-only` unless the user explicitly wants Docker
`/sse` only.

## Explain The Two Skill Layers First

- `memory-palace-setup`
  - onboarding router
- `memory-palace`
  - canonical runtime skill from the main repo

If the user only installs the onboarding skill and never installs or syncs the
main repo's canonical `memory-palace` skill, the final setup is still
incomplete.

## Cross-Platform Baseline

The install commands below are cross-platform because they call Python scripts
from the main repo.

Wrapper selection happens inside the main repo:

- native Windows
  - writes repo-local bindings that point to `backend/mcp_wrapper.py`
- macOS / Linux / `WSL` / `Git Bash`
  - writes repo-local bindings that point to
    `scripts/run_memory_palace_mcp_stdio.sh`

So on Windows:

- prefer the installer-generated binding
- do **not** manually transpose bash launcher examples unless the user is
  explicitly using `WSL` or `Git Bash`

## Fresh-Machine Default

Inside the `Memory-Palace` repo:

```bash
python scripts/sync_memory_palace_skill.py
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --force
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --check
```

Why this default:

- it installs the repo's canonical `memory-palace` skill mirrors
- it uses the more stable **user-scope** MCP path on fresh machines
- it keeps `Codex` and `OpenCode` on their recommended binding path
- it lets `Claude` and `Gemini` work first, then add workspace entries only if
  needed

## Optional Workspace Add-On

Only mention workspace/project-level entries when the user explicitly wants:

- a visible repo-local project entry in the current checkout
- or an extra project-level entry for `Claude Code` / `Gemini CLI`

Then use:

```bash
python scripts/install_skill.py --targets claude,gemini --scope workspace --with-mcp --force
python scripts/install_skill.py --targets claude,gemini --scope workspace --with-mcp --check
```

Do not oversell workspace scope as the stable default for:

- `Codex`
- `OpenCode`

## Per-Client Guidance

### Claude Code

Recommended first move:

```bash
python scripts/install_skill.py --targets claude --scope user --with-mcp --force
```

Useful checks:

```bash
claude mcp list
python scripts/install_skill.py --targets claude --scope user --with-mcp --check
```

Optional add-on:

- add a workspace install afterward if the user also wants a project-level
  entry in the repo

### Codex CLI

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

- stable message: repo-local skill discovery plus **user-scope MCP binding**
- do not present workspace-local MCP as the primary stable path

### Gemini CLI

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

- user-scope is the more stable default on fresh machines
- workspace install is optional, not the primary path
- the installer also manages `memory-palace-overrides.toml`

### OpenCode

Recommended first move:

```bash
python scripts/install_skill.py --targets opencode --scope user --with-mcp --force
```

Useful checks:

```bash
opencode mcp list
python scripts/install_skill.py --targets opencode --scope user --with-mcp --check
```

Important boundary:

- do not describe OpenCode as “natively out-of-the-box”
- accurate wording:
  - the repo-local skill can be synced and installed
  - the stable MCP path is still **user-scope**
  - a real run can still depend on the user's provider credentials

## Minimal CLI Validation Chain

Do not call the setup complete before the user can verify:

1. canonical skill synced
2. selected client shows `memory-palace` in `mcp list`
3. `install_skill.py --check` passes for the chosen scope
4. the user asks the AI for one real Memory Palace call

Suggested smoke prompt:

```text
Use Memory Palace to read system://boot. If that works, create one temporary memory under notes://setup-smoke/<today>/<client>, then search for "setup smoke".
```

If the user only wants the minimum check, stop after:

```text
Use Memory Palace to read system://boot and tell me whether the call succeeded.
```

## What Success Looks Like

The user should end up with:

- the canonical `memory-palace` skill under `docs/skills/memory-palace/`
- local skill mirrors or installed copies for the chosen CLI client
- an MCP entry pointing to the current repo's launcher
- one successful smoke call, not just a visible config item
