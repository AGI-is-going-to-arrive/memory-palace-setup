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

## Separate Skill Scope From MCP Scope

Do not answer these as one combined “scope” choice.

- onboarding setup access
  - default recommendation: this setup repo URL or direct reads of this repo's
    `README.md` and `SKILL.md`
  - do not default `memory-palace-setup` itself to persistent installation
- runtime skill visibility
  - if the user wants something installed persistently, make that the main
    repo's `memory-palace` skill
  - repo-local or workspace skill entries are optional add-ons when the user
    explicitly wants the current checkout to expose a local entry too
- MCP binding
  - keep the current stable per-client recommendation unchanged
  - do not move MCP to workspace scope just because the user asked for a
    repo-local runtime skill entry

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

- it gives the user/global skill install most people actually want on a fresh
  machine
- it still installs the repo's canonical `memory-palace` skill mirrors where
  the main repo expects them
- it uses the more stable **user-scope** MCP path on fresh machines
- it keeps `Codex` and `OpenCode` on their recommended binding path
- it lets `Claude` and `Gemini` work first, then add workspace entries only if
  needed

If the user wants the setup repo to drive the persistent runtime install
directly, use:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host claude --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host codex --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host gemini --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host opencode --repo /path/to/local/Memory-Palace-checkout
```

This wrapper keeps the same user-scope-first MCP behavior; it just gives the
setup repo one stable entry point for persistent runtime install.

## Optional Repo-Local Skill Add-On

Only mention repo-local or workspace add-ons when the user explicitly wants the
current checkout to expose a local skill entry too.

If the user wants a repo-local projection without changing the existing MCP
logic, use:

```bash
python scripts/sync_memory_palace_skill.py
python scripts/install_skill.py --targets claude,gemini --scope workspace --force
```

What this means:

- `sync_memory_palace_skill.py`
  - refreshes repo-local mirrors in the current checkout
- `install_skill.py --scope workspace --force`
  - adds repo-local skill entries for targets that support a stable workspace
    skill surface
- because `--with-mcp` is omitted here, this add-on does **not** change the
  user's current MCP binding logic

## Optional Workspace MCP Add-On

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
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host claude --repo /path/to/local/Memory-Palace-checkout
```

Equivalent main-repo command:

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
  repo-local skill entry
- only add `--with-mcp` on that workspace step when the user explicitly also
  wants workspace MCP

### Codex CLI

Recommended first move:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host codex --repo /path/to/local/Memory-Palace-checkout
```

Equivalent main-repo command:

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
- if the user wants an extra repo-local skill projection in the current
  checkout, use `sync_memory_palace_skill.py` as the add-on and leave MCP on
  the user-scope route

### Gemini CLI

Recommended first move:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host gemini --repo /path/to/local/Memory-Palace-checkout
```

Equivalent main-repo command:

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
- if the user only wants repo-local skill visibility as an add-on, a workspace
  install without `--with-mcp` is enough; keep MCP on the existing stable route

### OpenCode

Recommended first move:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host opencode --repo /path/to/local/Memory-Palace-checkout
```

Equivalent main-repo command:

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
- if the user wants an extra repo-local skill projection in the current
  checkout, use `sync_memory_palace_skill.py` as the add-on and leave MCP on
  the user-scope route

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
- a user/global skill install by default for the chosen CLI client
- for `OpenCode`, a visible global skill under
  `~/.config/opencode/skills/memory-palace/`
- optional repo-local mirrors or workspace entries only when the user asked for
  current-checkout visibility too
- an MCP entry pointing to the current repo's launcher
- one successful smoke call, not just a visible config item
