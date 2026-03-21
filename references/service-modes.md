# Service Modes

Use this file when the user is unsure whether they need:

- just the service
- full `skills + MCP`
- an IDE-host connection
- or an `MCP-only` / Docker `/sse` fallback

Target project repo:

```text
https://github.com/AGI-is-going-to-arrive/Memory-Palace
```

## Mode Selector

Choose one of these modes explicitly:

### 1. Service Only

Use this when the user only wants:

- `Dashboard`
- `API`
- `SSE`

In this mode, the user can stop after backend or Docker setup. Skill
installation is not mandatory yet.

### 2. Full CLI Daily-Use Integration

Use this when the user wants:

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`
- `OpenCode`

to actually use Memory Palace in normal conversations.

This is the default recommendation for CLI users.

### 3. IDE Host Integration

Use this when the user wants:

- `Cursor`
- `Windsurf`
- `VSCode-host`
- `Antigravity`

to use the current repo.

The project path here is:

- repo-local `AGENTS.md`
- `python scripts/render_ide_host_config.py --host ...`

### 4. MCP-Only Or Docker `/sse`

Use this only when:

- the user explicitly wants a remote client connected to Docker `/sse`
- or the environment cannot install the repo's skill layer
- or the user refuses local skill installation

Be explicit that this is the fallback path.

## Profile Selector

When the user asks which deployment profile to start with:

- **Profile B**
  - use when the goal is to boot the project with the fewest extra
    dependencies
- **Profile C**
  - use when local embedding / reranker services are already available or the
    user wants stronger retrieval quality
- **Profile D**
  - use when remote APIs, hosted model services, or a hosted deployment target
    are already part of the plan

Do not present `B` as the best final state unless the user explicitly wants the
lightest local boot only.

## Local Service Quick Path

If the user only wants the service, route them to the project docs for:

- `docs/GETTING_STARTED.md`
- `docs/GHCR_QUICKSTART.md`

Typical local path:

```bash
cp .env.example .env
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Typical frontend path:

```bash
cd frontend
npm install
npm run dev
```

Minimal service health checks:

```bash
curl http://127.0.0.1:8000/health
```

Then verify:

- backend health returns a payload
- frontend opens on its dev URL

## CLI Full-Integration Quick Path

Inside the main repo:

```bash
python scripts/sync_memory_palace_skill.py
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --force
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --check
```

Optional workspace add-on for `Claude` / `Gemini` only:

```bash
python scripts/install_skill.py --targets claude,gemini --scope workspace --with-mcp --force
```

## IDE Host Quick Path

Inside the main repo:

```bash
python scripts/render_ide_host_config.py --host cursor
python scripts/render_ide_host_config.py --host windsurf
python scripts/render_ide_host_config.py --host vscode
python scripts/render_ide_host_config.py --host antigravity
```

If the host has `stdin/stdout` or `CRLF` quirks, switch to the wrapper form:

```bash
python scripts/render_ide_host_config.py --host antigravity --launcher python-wrapper
```

Important boundary:

- IDE hosts do not use hidden skill mirrors as the default public route
- the route is `AGENTS.md + MCP snippet`

## Docker Or GHCR Boundary

Explain this clearly:

- Docker or GHCR gets the service running
- it does **not** automatically configure the user's local skill or MCP client

So if the user later says:

- “now connect Claude / Codex / Gemini / OpenCode”
- or “now connect Cursor / Antigravity”

switch back to the CLI or IDE-host route immediately.

## Exact Recommendation Language

When the user asks “which mode should I use?”, default to:

- `skills + MCP` for real day-to-day usage
- `AGENTS.md + MCP snippet` for IDE hosts
- `MCP-only` only for explicit remote `/sse`, Docker-only, or constrained
  environments
