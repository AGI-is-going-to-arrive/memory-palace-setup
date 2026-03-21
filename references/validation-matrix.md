# Validation Matrix

Use this file when you need the smallest acceptable proof that setup is really
working.

## CLI Clients

### Minimal Pass

1. sync the runtime skill

```bash
python scripts/sync_memory_palace_skill.py
```

2. install the CLI binding

```bash
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --force
python scripts/install_skill.py --targets claude,codex,gemini,opencode --scope user --with-mcp --check
```

3. confirm the client sees `memory-palace`

```bash
claude mcp list
codex mcp list
gemini mcp list
opencode mcp list
```

4. run one smoke call

```text
Use Memory Palace to read system://boot and tell me whether the call succeeded.
```

### Preferred Pass

After the first read succeeds, add one temporary write + search smoke:

```text
Use Memory Palace to create one temporary memory under notes://setup-smoke/<today>/<client>, then search for "setup smoke".
```

## IDE Hosts

### Minimal Pass

1. for `Cursor / Antigravity / VSCode-host`, prefer automatic config first

```bash
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/Memory-Palace
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/Memory-Palace
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/Memory-Palace
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host cursor --repo /path/to/Memory-Palace --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host antigravity --repo /path/to/Memory-Palace --check
python /path/to/memory-palace-setup/scripts/apply_ide_mcp.py --host vscode --repo /path/to/Memory-Palace --check
```

2. for `Windsurf`, or when host automation is unavailable, render the repo-local
   snippet

```bash
python scripts/render_ide_host_config.py --host cursor
python scripts/render_ide_host_config.py --host windsurf
python scripts/render_ide_host_config.py --host vscode
python scripts/render_ide_host_config.py --host antigravity
```

3. confirm the host sees `memory-palace`
4. run:

```text
Use Memory Palace to read system://boot.
```

### Extra Windows / CRLF-Safe Preview

```bash
python scripts/render_ide_host_config.py --host antigravity --launcher python-wrapper
```

## Service-Only Mode

### Minimal Pass

```bash
curl http://127.0.0.1:8000/health
```

Confirm:

- the backend health payload is reachable
- the frontend page opens if the frontend is part of the route

## Docker `/sse` Or MCP-Only Fallback

### Minimal Pass

1. confirm the service is actually reachable
2. confirm the client points to the intended `/sse` URL
3. say explicitly that this is a fallback path, not full `skills + MCP`

## Cross-Platform Acceptance Notes

- native Windows:
  - validate that the generated binding points to `backend/mcp_wrapper.py`
- macOS / Linux / `WSL` / `Git Bash`:
  - validate that the generated binding points to
    `scripts/run_memory_palace_mcp_stdio.sh`
- any repo-local stdio path:
  - validate that `.env` is host-correct and not using `/app/...` or
    `/data/...`
