# Service Modes

Use this file when the user is unsure whether they need:

- just the service
- a full client integration
- or a Docker `/sse` fallback

## Three different goals

### 1. Service only

Use this when the user only wants:

- `Dashboard`
- `API`
- `SSE`

In that case, they can stop after local backend or Docker setup. Skill installation is not mandatory yet.

Profile guidance for service startup:

- Start with **Profile B** when the goal is to boot with the fewest extra requirements.
- Strongly recommend **Profile C / D** once the user wants better retrieval quality or a more serious deployment target.

### 2. Full daily-use client integration

Use this when the user wants:

- Claude Code, Codex CLI, Gemini CLI, Cursor, or Antigravity to actually use Memory Palace in normal conversations

This is the default recommended path for the project.

The answer should say clearly:

> For normal use, prefer the repo’s **skills + MCP** path.  
> Do not start with bare MCP unless you have a specific reason.

If the user also asks about deployment profiles, say:

> **Profile B** is the default starting point because it needs the least extra setup.  
> **Profile C / D** are the strongly recommended target profiles once model services are available.

### 3. MCP-only or Docker `/sse`

Use this only when:

- the user explicitly wants a remote client connected to Docker `/sse`
- or the environment cannot install the repo’s skill layer
- or the user refuses local skill installation

In that case, be explicit that the user is taking the fallback path.

## Service-only quick path

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

## Docker or GHCR boundary

Explain this clearly:

- Docker or GHCR gets the service running
- it does **not** automatically configure the user’s local skill or MCP client

So if the user later says “now connect Claude/Codex/Gemini to it”, switch back to the `skills + MCP` route.

## IDE host rule

For `Cursor` and `Antigravity`, the integration path for the project itself is:

- repo-local `AGENTS.md`
- plus `python scripts/render_ide_host_config.py --host ...`

This setup skill repo only teaches the AI how to guide that process.

## Exact recommendation language

When a user asks “which mode should I use?”, default to:

- `skills + MCP` for real day-to-day usage
- `MCP-only` only for explicit remote `/sse`, Docker-only, or constrained environments
