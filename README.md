# Memory Palace Setup Skill

Aligned with `Memory Palace v3.6.3`.

This repository is not the `Memory-Palace` project itself.

It is the **onboarding layer** for AI clients. Its job is to teach an AI how to
route the user onto the correct installation path, instead of making the user
jump between `README`, `GETTING_STARTED`, `IDE_HOSTS`, `install_skill.py`, and
manual MCP configuration.

Important warning:

> For `Cursor / Windsurf / VSCode-host / Antigravity`, seeing the
> `memory-palace` skill does **not** mean MCP is already installed.
> IDE hosts still require the repo-local MCP snippet path.
>
> Current automation boundary:
> `Cursor`, `Antigravity`, `VSCode-host`, and `Windsurf` can usually be
> auto-configured for MCP when their local host CLI/config surface is available.
> The runtime `memory-palace` layer can also be installed or projected globally
> through user-level skill, rule, instruction, or workflow surfaces, while MCP
> keeps pointing at the current checkout.

## Two Different Things

This is the easiest place to get confused:

- `memory-palace-setup`
  - the onboarding skill in this repository
  - its job is to guide installation and first-run troubleshooting
- `memory-palace`
  - the canonical skill shipped by the main `Memory-Palace` repository
  - target repo: `https://github.com/AGI-is-going-to-arrive/Memory-Palace`
  - its job is to drive normal day-to-day durable-memory workflows after setup

One more distinction matters just as much:

- **service startup**
  - `Dashboard / API / SSE` are running
- **client integration**
  - `Claude / Codex / Gemini / OpenCode / IDE host` can actually trigger and use
    Memory Palace

Those are different layers. A running service does not mean the client is
already connected.

For IDE hosts, one more trap matters:

- seeing a skill or workflow entry is **not** proof that `memory-palace` MCP is
  installed
- the IDE host still needs `AGENTS.md + MCP snippet`

## Supported Hosts

CLI clients:

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`
- `OpenCode`

IDE hosts:

- `Cursor`
- `Windsurf`
- `VSCode-host`
- `Antigravity`

## Default Recommendation

- Prefer **skills + MCP** for normal day-to-day use.
- Separate **onboarding access**, **runtime skill visibility**, and **MCP binding**.
- The onboarding repo `memory-palace-setup` itself does **not** need persistent
  global installation by default.
- The normal public path is:
  - give the AI this GitHub repository URL
  - or tell the AI to read this repository's `README.md` and `SKILL.md`
- When recommending something to install persistently, prioritize the main
  repo's runtime `memory-palace` skill instead of the temporary onboarding
  `memory-palace-setup` skill.
- For a one-command persistent runtime install or projection, use:
  - `python scripts/apply_runtime_global_setup.py --host ... --repo /path/to/local/Memory-Palace-checkout`
- Keep the current MCP logic unchanged:
  - CLI clients still follow the existing stable user-scope-first MCP path where documented
  - IDE hosts still point MCP at the current `Memory-Palace` checkout
- Treat **MCP-only** as a fallback for explicit remote `/sse`, Docker-only, or
  no-skill environments.
- Start with **Profile B** when the user wants the fewest extra dependencies.
- Recommend **Profile C** when local embedding / reranker services are ready.
- Recommend **Profile D** when the user already plans to use remote APIs or a
  hosted environment.

One-line policy:

> Start with `B` to get it running.  
> Move to `C` when local retrieval services are available.  
> Move to `D` when remote APIs or hosted deployment are already part of the
> plan.

## Default Scope Answer

If the user is not asking about one specific host yet and is instead asking for
the default policy, answer directly instead of asking a follow-up question
first.

Use this exact stance:

- onboarding access
  - default: give the AI this setup repo URL or ask it to read this repo
    directly
  - do not present persistent installation of `memory-palace-setup` itself as
    mandatory
- runtime skill visibility
  - if the user wants something installed persistently, prioritize the main
    repo's `memory-palace` skill
  - for a cross-host installer, use `scripts/apply_runtime_global_setup.py`
- MCP binding
  - keep the current host-specific logic unchanged
  - CLI still follows the existing stable MCP recommendation per client
  - IDE hosts still point MCP at the current `Memory-Palace` checkout

Only move to a host-specific follow-up question after stating that default.

## Platform Boundary

The main `Memory-Palace` repository now has two repo-local stdio launcher paths:

- native Windows
  - default repo-local wrapper: `backend/mcp_wrapper.py`
- macOS / Linux / `WSL` / `Git Bash`
  - default repo-local wrapper: `scripts/run_memory_palace_mcp_stdio.sh`

Both wrappers expect:

- the current checkout
- the repo's local `.env`
- the repo's local `backend/.venv`

Important boundary:

- do **not** copy Docker container paths like `/app/...` or `/data/...` into a
  host-side `.env`
- repo-local stdio wrappers will reject that configuration
- if the user wants the containerized service instead, route them to Docker
  `/sse`

## Optional Onboarding Skill Install

Repository URL:

```text
https://github.com/AGI-is-going-to-arrive/memory-palace-setup.git
```

Most users do **not** need to install `memory-palace-setup` persistently.

The normal public path is simply:

- send the AI this repository URL
- or tell it to read this repository's `README.md` and `SKILL.md`

Only use the following clone path when you explicitly want this onboarding layer
available as a local skill for a specific client.

### Optional CLI Local Skill Directories

#### Claude Code

```bash
git clone https://github.com/AGI-is-going-to-arrive/memory-palace-setup.git \
  ~/.claude/skills/memory-palace-setup
```

#### Codex CLI

```bash
git clone https://github.com/AGI-is-going-to-arrive/memory-palace-setup.git \
  ~/.codex/skills/memory-palace-setup
```

#### Gemini CLI

```bash
git clone https://github.com/AGI-is-going-to-arrive/memory-palace-setup.git \
  ~/.gemini/skills/memory-palace-setup
```

#### OpenCode

```bash
git clone https://github.com/AGI-is-going-to-arrive/memory-palace-setup.git \
  ~/.opencode/skills/memory-palace-setup
```

### IDE Hosts

Do **not** lead with hidden skill mirrors for:

- `Cursor`
- `Windsurf`
- `VSCode-host`
- `Antigravity`

For IDE hosts, the main project now uses:

1. repo-local `AGENTS.md`
2. `python scripts/render_ide_host_config.py --host ...`
3. optional host-specific compatibility layers only when needed

Current automation split:

- `Cursor`
  - if the host CLI/config surface is available, prefer automatic MCP config
  - for persistent runtime visibility, prefer a user-level visible skill
    projection under `~/.cursor/skills-cursor/memory-palace/`
- `Antigravity`
  - if the host CLI/config surface is available, prefer automatic MCP config
  - also keep the workflow projection in sync
  - user-level workflow projection is a stable runtime surface
- `VSCode-host`
  - if the local VS Code MCP config surface is available, prefer automatic MCP config
  - for persistent runtime visibility, prefer a visible user-level custom agent
- `Windsurf`
  - if the local Windsurf MCP config surface is available, prefer automatic MCP config
  - for persistent runtime visibility, prefer a visible global skill under the
    Windsurf user skill directory

For the onboarding layer itself, the practical default is:

- let the current AI read this repository's `README.md` and `SKILL.md`
- or give the AI this repository URL directly
- only install `memory-palace-setup` as a persistent client skill when the user
  explicitly wants that extra convenience layer

`Antigravity` still has an optional workflow projection path, but it is an
extra layer, not the primary route:

```bash
mkdir -p ~/.gemini/antigravity/global_workflows
cp /path/to/memory-palace-setup/variants/antigravity/global_workflows/memory-palace-setup.md \
  ~/.gemini/antigravity/global_workflows/
```

If the user has already cloned
`https://github.com/AGI-is-going-to-arrive/Memory-Palace` locally, the
preferred automation path for `Cursor / Antigravity / VSCode-host / Windsurf`
is:

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host windsurf --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host windsurf --repo /path/to/local/Memory-Palace-checkout --check
```

This script:

- renders the canonical repo-local MCP snippet from the main repo
- writes the actual local host config file
- copies the canonical antigravity workflow when needed
- supports `--dry-run`, `--check`, and `--home` for testing

If the user wants the runtime `memory-palace` layer visible globally across
folders, use:

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host claude --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host codex --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host gemini --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host opencode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host cursor --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host vscode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host windsurf --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host antigravity --repo /path/to/local/Memory-Palace-checkout
```

This script:

- installs the runtime `memory-palace` layer globally at user scope for CLI
  hosts
- projects the runtime layer globally for IDE hosts through host-native
  skills, agents, workflows, or compatibility skill surfaces
- for `Cursor`, also writes a visible global skill projection under
  `~/.cursor/skills-cursor/memory-palace/`
- for `VSCode-host`, writes a visible global skill under
  `~/.copilot/skills/memory-palace/` and a custom agent under
  `~/.copilot/agents/memory-palace.agent.md`
- for `Windsurf`, writes a visible global skill under
  `~/.codeium/windsurf/skills/memory-palace/`
- for `OpenCode`, also writes a visible global skill under
  `~/.config/opencode/skills/memory-palace/`
- writes IDE MCP into the host's user-level config surface, but still points it
  at one selected local `Memory-Palace` checkout
- does **not** install `memory-palace-setup` persistently

## IDE Global Runtime Caveat

If the user chooses the global runtime path for IDE hosts, say this plainly:

- the runtime rule or skill layer is global
- the MCP config is also written at user scope
- but that MCP entry still targets one selected local `Memory-Palace` checkout
- if that checkout is moved, deleted, or its `.env` / `.venv` breaks, the IDE
  can still see the runtime rule layer while tool calls fail
- if the user has multiple `Memory-Palace` checkouts, they must pick which one
  is the current global target

## How To Use It After Installation

Once the onboarding skill is installed, say one of these:

```text
Use $memory-palace-setup to install and configure Memory Palace step by step.
Target repo: https://github.com/AGI-is-going-to-arrive/Memory-Palace
Prefer skills + MCP over MCP-only. Start with Profile B, but recommend C/D if the environment is ready.
```

```text
使用 $memory-palace-setup 帮我一步步安装配置 Memory Palace。
目标仓库是 https://github.com/AGI-is-going-to-arrive/Memory-Palace
优先走 skills + MCP，不要默认 MCP-only。先按 Profile B 起步，但如果环境允许，请主动推荐我升级到 C/D。
```

If the onboarding skill is not installed yet, the fallback prompt is:

```text
Please read this repository's README.md and SKILL.md first, then guide me step by step to install and configure Memory Palace from https://github.com/AGI-is-going-to-arrive/Memory-Palace. Prefer skills + MCP over MCP-only.
```

Or even shorter:

```text
Use this repo URL as the setup guide for installing Memory Palace:
https://github.com/AGI-is-going-to-arrive/memory-palace-setup
```

## What The AI Should Do

The AI should:

1. separate the two objects first
   - onboarding skill: `memory-palace-setup`
   - canonical runtime skill: `memory-palace`
2. identify the host
   - CLI client
   - IDE host
   - service-only goal
3. identify the platform boundary
   - native Windows
   - macOS / Linux
   - `WSL` / `Git Bash`
4. separate the scope decisions
   - onboarding access
     - default: repo URL or direct read of this repo's docs
     - persistent install of `memory-palace-setup` is optional
   - runtime skill visibility
     - if something should be installed persistently, prioritize the main
      repo's runtime `memory-palace` skill
     - for a unified installer, prefer `scripts/apply_runtime_global_setup.py`
   - MCP binding
     - keep the current host-specific recommendation unchanged
5. choose the smallest correct path
   - full `skills + MCP`
   - IDE-host `AGENTS.md + MCP snippet`
   - service-only
   - explicit `MCP-only` fallback
6. do not treat `memory-palace-setup` itself as the thing that must be installed
   globally
7. keep the current MCP logic unchanged
   - CLI: follow the existing stable MCP recommendation per client
   - IDE: keep MCP pointed at the current repo
8. when recommending persistent installation, prioritize the runtime
   `memory-palace` skill from the main repo
9. mention repo-local/workspace add-ons only when they are actually needed
   - especially for `Claude` and `Gemini`
10. validate with a real smoke chain, not just `mcp list`

If the user is explicitly asking for the default cross-host scope policy:

- answer the default scope split first
- do not stop and ask “which host?” before giving that default

## Minimal Verification Chain

The setup is not complete until the AI can show all of these:

1. the correct skill layer is installed
2. the client sees the `memory-palace` MCP entry
3. the binding points to the current checkout
4. the backend health check is reachable when service startup is involved
5. the first real Memory Palace call succeeds
   - minimum: `read_memory("system://boot")`
6. optional but preferred:
   - create one temporary smoke memory
   - search for it once

For the exact per-host checks, see:

- `references/host-matrix.md`
- `references/validation-matrix.md`

## Dashboard Setup Assistant Boundary

If the user is looking at the Dashboard first-run setup assistant:

- the UI shows a **safe summary**, not the raw secret value
- some fields may appear masked or visually faint
- if the app is running in Docker, writing `.env` there can still be a
  temporary convenience result
- backend-side config changes still require a restart
- this assistant helps local runtime configuration
- it does **not** replace `skill discovery + MCP binding`

So if the user wants real client integration, route back to the repo scripts and
validation chain instead of treating the UI as proof that setup is finished.

See `references/ui-setup-assistant.md`.

## Repo-Visible Sources To Prefer

When the main `Memory-Palace` repository is available locally, prefer these
paths over paraphrasing:

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

## Repository Layout

```text
memory-palace-setup/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── apply_runtime_global_setup.py
│   └── apply_ide_mcp.py
├── references/
│   ├── cli-routing.md
│   ├── common-failures.md
│   ├── host-matrix.md
│   ├── service-modes.md
│   ├── ui-setup-assistant.md
│   └── validation-matrix.md
└── variants/
    └── antigravity/
        └── global_workflows/
            └── memory-palace-setup.md
    ├── vscode/
    │   └── agents/
    │       └── memory-palace.agent.md
    └── windsurf/
        └── skills/
            └── memory-palace/
```

## Scope Boundary

This repository is only responsible for:

- installation routing
- first-time connection
- first-time configuration
- first-time troubleshooting

It is not responsible for:

- normal durable-memory operations
- replacing the main `memory-palace` skill
- editing code inside the main `Memory-Palace` repository

Once setup is complete, normal use should switch to the canonical
`memory-palace` skill from the main project.
