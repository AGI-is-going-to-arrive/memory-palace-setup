# Memory Palace Setup Skill

This repository is not the `Memory-Palace` project itself.

It is a dedicated **onboarding skill** for AI clients. Its job is simple:

> When a user says "use this skill to help me install and configure Memory Palace," the AI should enter the correct step-by-step setup flow immediately, instead of sending the user back and forth between `README`, `GETTING_STARTED`, skill docs, and MCP configuration.

The default position of this skill is:

- **Install the skill first, then bind MCP**
- **Prefer `skills + MCP`**
- **Only fall back to `MCP-only` when the user explicitly wants remote `/sse`, Docker-only usage, or cannot install skills**

## What Problem This Solves

This repository does not replace the real scripts and docs in the main `Memory-Palace` repo.

Instead, it teaches the AI to:

1. classify the user's setup goal first
2. choose the correct client path
3. give one step at a time
4. explain what success should look like after each step
5. stop early on common setup traps instead of continuing with bad assumptions

Typical trigger prompts:

- `Use $memory-palace-setup to install and configure Memory Palace step by step`
- `Use this skill to help me install and configure the Memory Palace project`
- `Help me connect Memory Palace to Claude Code / Codex / Gemini / Cursor / Antigravity`
- `I do not want an MCP-only setup. Guide me through the full skills + MCP path`

## Profile Policy

When this skill helps users choose deployment profiles for the main `Memory-Palace` repo, it should always follow this policy:

- **Profile B** is the default starting point
  - it requires the fewest extra services
  - it is the best path for getting the project running quickly
- **Profile C / D** are the strongly recommended targets
  - as soon as the user wants better retrieval quality, long-term usage, or real deployment, the AI should recommend upgrading to `C / D`

One-line policy:

> Start with **B** to get it running.  
> As soon as model services are available, **strongly recommend** moving to **C / D**.

## Install This Skill

Replace `<this-skill-repo-url>` with the actual GitHub URL of this repository.

### Claude Code

```bash
git clone <this-skill-repo-url> ~/.claude/skills/memory-palace-setup
```

### Codex CLI

```bash
git clone <this-skill-repo-url> ~/.codex/skills/memory-palace-setup
```

### Gemini CLI

```bash
git clone <this-skill-repo-url> ~/.gemini/skills/memory-palace-setup
```

### Cursor

```bash
git clone <this-skill-repo-url> ~/.cursor/skills/memory-palace-setup
```

### Antigravity

Preferred path: clone the full skill repo into Antigravity's skills directory:

```bash
git clone <this-skill-repo-url> ~/.gemini/antigravity/skills/memory-palace-setup
```

If your Antigravity setup prefers workflow projection, also copy the optional workflow file:

```bash
mkdir -p ~/.gemini/antigravity/global_workflows
cp ~/.gemini/antigravity/skills/memory-palace-setup/variants/antigravity/global_workflows/memory-palace-setup.md \
  ~/.gemini/antigravity/global_workflows/
```

## How To Use It After Installation

Once the skill is installed, say this in your AI client:

```text
Use $memory-palace-setup to install and configure the Memory Palace project step by step.
```

Or:

```text
Use $memory-palace-setup to connect this project with the correct setup path. Prefer skills + MCP, not MCP-only.
```

The AI should then follow this flow:

1. determine which path you actually need
   - `Dashboard / API / SSE` only
   - or full client integration for `Claude Code / Codex / Gemini / Cursor / Antigravity`
2. default to `skills + MCP`
3. choose the correct client-specific commands
4. give one validation signal after each step
5. stop and explain boundary conditions when prerequisites are missing

## How The AI Should Guide Users

The default guidance policy is:

- **For supported clients, prefer `skills + MCP`**
- **Do not confuse "the service is running" with "the client is connected"**
- **Do not present `MCP-only` as the default path**

The AI should route users back to the real entry points in the main `Memory-Palace` repository:

- `docs/skills/SKILLS_QUICKSTART.md`
- `docs/skills/GETTING_STARTED.md`
- `docs/skills/IDE_HOSTS.md`
- `docs/GHCR_QUICKSTART.md`
- `scripts/sync_memory_palace_skill.py`
- `scripts/install_skill.py`
- `scripts/render_ide_host_config.py`

That means this onboarding skill is a **router + guide**, not a replacement for the main repo scripts.

When a user asks which deployment profile to use, the AI should say:

- `B`: default starting profile, lowest external setup cost
- `C`: strongly recommended whenever local model services are available
- `D`: also a strongly recommended target for remote API or hosted environments

## Why `MCP-only` Is Not The Default Recommendation

For this project, a standalone MCP-only setup is usually weaker because:

- the model may not know when to enter the Memory Palace workflow
- users often miss the `skill discovery` layer
- MCP configuration surfaces differ across clients
- IDE hosts and CLI clients do not use the same primary path

So the safer default answer is:

> For normal day-to-day use of Memory Palace, install **both the skill and the MCP binding**.  
> `MCP-only` should be treated as a fallback for explicit remote `/sse`, Docker-only, or no-skill environments.

## Common Traps This Skill Should Catch

- copying Docker `/app/...` paths into a local `.env`
- installing the skill but forgetting MCP
- configuring MCP but never enabling skill discovery
- assuming successful `docker compose` means the client is already connected
- copying `/bin/zsh` or `bash` examples directly into native Windows without `Git Bash` or `WSL`
- forcing unstable workspace-local MCP expectations onto `Codex` or `OpenCode`
- applying CLI hidden-mirror logic to `Cursor` or `Antigravity`

## Repository Layout

```text
memory-palace-setup/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── cli-routing.md
│   ├── service-modes.md
│   └── common-failures.md
└── variants/
    └── antigravity/
        └── global_workflows/
            └── memory-palace-setup.md
```

## Scope Boundary

This repository is only responsible for:

- installation
- first-time connection
- first-time configuration
- first-time troubleshooting

It is not responsible for:

- normal durable-memory operations
- replacing the main `memory-palace` skill
- editing code inside the main `Memory-Palace` repo

Once setup is complete, questions about `read_memory`, `search_memory`, `update_memory`, write guard behavior, or `rebuild_index` should switch back to the main `memory-palace` skill.
