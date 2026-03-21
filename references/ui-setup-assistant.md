# Dashboard Setup Assistant

Use this file when the user is looking at the Dashboard first-run setup
assistant, or sends screenshots from that UI.

## What The Setup Assistant Is

It is a convenience layer for local runtime setup.

It can help with:

- browser-session dashboard auth
- writing common local runtime fields into `.env`
- summarizing current local setup status

It is **not** the same thing as:

- syncing the runtime `memory-palace` skill
- binding MCP for `Claude / Codex / Gemini / OpenCode`
- rendering IDE-host MCP snippets

## Important UI Boundaries

- the assistant shows a **safe summary**
  - it does not echo raw secret values back into the UI
- some fields can appear masked or visually faint
  - that does not prove the value is wrong
- if the app is running inside Docker, writing `.env` there can still be a
  temporary local-runtime convenience result
- backend-side config changes still require a restart

## What To Tell The User

If the user is unsure whether the setup assistant actually finished the job,
say this plainly:

- the Dashboard assistant helps local runtime setup
- it does not prove that the AI client can already use Memory Palace
- client integration still needs:
  - runtime skill discovery
  - MCP binding
  - a real smoke call

## When To Route Back To Scripts

Route back to the repo scripts when:

- the user wants `Claude / Codex / Gemini / OpenCode` to work
- the user wants `Cursor / Windsurf / VSCode-host / Antigravity` to work
- the user is confused by masked or faint UI fields
- the user is not sure whether the backend restart happened

Preferred checks:

```bash
curl http://127.0.0.1:8000/health
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --check
```

For IDE hosts:

```bash
python scripts/render_ide_host_config.py --host cursor
python scripts/render_ide_host_config.py --host antigravity
```

## What Counts As Real Completion

Do not call setup complete until:

1. the service health check is fine when service startup is involved
2. the client or IDE host has the correct binding
3. `read_memory("system://boot")` succeeds once
