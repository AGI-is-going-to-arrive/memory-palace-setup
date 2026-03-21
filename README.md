# Memory Palace Setup Skill

Aligned with `Memory Palace v3.6.2`.

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
> `Cursor`, `Antigravity`, and `VSCode-host` can usually be auto-configured for MCP.
> `Windsurf` should still default to the rendered snippet +
> manual paste path unless the local machine proves a stable host CLI path.

## Two Different Things

This is the easiest place to get confused:

- `memory-palace-setup`
  - the onboarding skill in this repository
  - its job is to guide installation and first-run troubleshooting
- `memory-palace`
  - the canonical skill shipped by the main `Memory-Palace` repository
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

## Install This Onboarding Skill

Repository URL:

```text
https://github.com/AGI-is-going-to-arrive/memory-palace-setup.git
```

### CLI Clients With Local Skill Directories

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
- `Antigravity`
  - if the host CLI/config surface is available, prefer automatic MCP config
  - also keep the workflow projection in sync
- `VSCode-host`
  - if the local VS Code MCP config surface is available, prefer automatic MCP config
- `Windsurf`
  - default to rendered snippet + manual paste unless a stable local host CLI is
    confirmed on that machine

For the onboarding skill itself, the practical default is:

- let the current AI read this repository's `README.md` and `SKILL.md`
- or open this repository locally in the host

`Antigravity` still has an optional workflow projection path, but it is an
extra layer, not the primary route:

```bash
mkdir -p ~/.gemini/antigravity/global_workflows
cp /path/to/memory-palace-setup/variants/antigravity/global_workflows/memory-palace-setup.md \
  ~/.gemini/antigravity/global_workflows/
```

If the main `Memory-Palace` repo is already cloned locally, the preferred
automation path for `Cursor / Antigravity / VSCode-host` is:

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/Memory-Palace
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/Memory-Palace
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/Memory-Palace
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/Memory-Palace --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/Memory-Palace --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/Memory-Palace --check
```

This script:

- renders the canonical repo-local MCP snippet from the main repo
- writes the actual local host config file
- copies the canonical antigravity workflow when needed
- supports `--dry-run`, `--check`, and `--home` for testing

## How To Use It After Installation

Once the onboarding skill is installed, say one of these:

```text
Use $memory-palace-setup to install and configure Memory Palace step by step.
Prefer skills + MCP over MCP-only. Start with Profile B, but recommend C/D if the environment is ready.
```

```text
使用 $memory-palace-setup 帮我一步步安装配置 Memory Palace。
优先走 skills + MCP，不要默认 MCP-only。先按 Profile B 起步，但如果环境允许，请主动推荐我升级到 C/D。
```

If the onboarding skill is not installed yet, the fallback prompt is:

```text
Please read this repository's README.md and SKILL.md first, then guide me step by step to install and configure Memory Palace. Prefer skills + MCP over MCP-only.
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
4. choose the smallest correct path
   - full `skills + MCP`
   - IDE-host `AGENTS.md + MCP snippet`
   - service-only
   - explicit `MCP-only` fallback
5. prefer **user-scope first** for CLI clients
   - `Claude / Codex / Gemini / OpenCode`
6. mention workspace/project-level installs only when they are actually needed
   - especially for `Claude` and `Gemini`
7. validate with a real smoke chain, not just `mcp list`

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
