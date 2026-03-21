# Validation Matrix

Use this file when you need the smallest acceptable proof that setup is really
working.

Target project repo:

```text
https://github.com/AGI-is-going-to-arrive/Memory-Palace
```

## CLI Clients

### Minimal Pass

1. install the runtime skill globally at user scope

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host claude --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host codex --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host gemini --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host opencode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host claude --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host codex --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host gemini --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host opencode --repo /path/to/local/Memory-Palace-checkout --check
```

2. sync the runtime skill in the current repo only when the user also wants repo-local mirrors

```bash
python scripts/sync_memory_palace_skill.py
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

1. install or project the runtime layer globally first

```bash
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host cursor --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host antigravity --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host vscode --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host windsurf --repo /path/to/local/Memory-Palace-checkout
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host cursor --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host antigravity --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host vscode --repo /path/to/local/Memory-Palace-checkout --check
python /path/to/memory-palace-setup/scripts/apply_runtime_global_setup.py --host windsurf --repo /path/to/local/Memory-Palace-checkout --check
```

2. for `Cursor / Antigravity / VSCode-host / Windsurf`, keep automatic MCP config on the current checkout

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
- persistent runtime projection:
  - validate that the expected user/global runtime surface exists for the
    chosen host
  - for `Cursor`, validate both the visible global skill path
    `~/.cursor/skills-cursor/memory-palace/` and the compatibility projection
    `~/.cursor/skills/memory-palace/`
  - for `VSCode-host`, validate the visible global skill path
    `~/.copilot/skills/memory-palace/`
  - for `VSCode-host`, validate the visible custom agent path
    `~/.copilot/agents/memory-palace.agent.md`
  - for `Windsurf`, validate the visible global skill path
    `~/.codeium/windsurf/skills/memory-palace/`
  - for `OpenCode`, validate the visible global skill path
    `~/.config/opencode/skills/memory-palace/`
- macOS / Linux / `WSL` / `Git Bash`:
  - validate that the generated binding points to
    `scripts/run_memory_palace_mcp_stdio.sh`
- any repo-local stdio path:
  - validate that `.env` is host-correct and not using `/app/...` or
    `/data/...`
