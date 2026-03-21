# Common Failures

Use this file when the user is already following setup steps but the result
still does not work.

Target project repo:

```text
https://github.com/AGI-is-going-to-arrive/Memory-Palace
```

## 1. The User Installed `memory-palace-setup`, But Not `memory-palace`

Symptom:

- the onboarding skill is available
- but the runtime workflow still does not trigger correctly

Cause:

- the user installed the router skill in this repo
- but never synced or installed the main repo's canonical `memory-palace` skill

Fix:

- explain the two-skill distinction plainly
- move the user to the main repo's `sync_memory_palace_skill.py` and
  `install_skill.py` path

## 2. “Docker Is Up, Why Can't The Client Use Memory Palace?”

Cause:

- the user started `Dashboard / API / SSE`
- but never installed the runtime skill layer or bound MCP for the client

Fix:

- service startup and client integration are different layers
- if the user wants normal AI conversations to use Memory Palace, move them to
  the `skills + MCP` path

## 3. Docker `/app/...` Or `/data/...` Path Copied Into Local `.env`

Cause:

- the user copied a container-internal SQLite path into the host-side `.env`

Why it breaks:

- repo-local stdio MCP runs on the host, not inside the container

Fix:

- use a host absolute path in local `.env`
- or keep using Docker `/sse`
- do not mix the two

## 4. Skill Installed, But MCP Not Bound

Symptom:

- the client can see or mention the skill
- but actual tool calls do not work

Cause:

- only the discovery layer is present

Fix:

- run the main repo's `install_skill.py --with-mcp`
- validate with the client's `mcp list`
- then run one real smoke call

## 5. MCP Bound, But Runtime Skill Not Synced

Symptom:

- `mcp list` shows `memory-palace`
- but the model does not reliably enter the Memory Palace workflow

Cause:

- only MCP was added
- the runtime skill mirrors were never synced or installed

Fix:

- sync or install the repo's canonical `memory-palace` skill first

## 6. `mcp list` Passes, But The First Tool Call Fails

Symptom:

- config looks present
- but `read_memory("system://boot")` fails or never executes

Likely causes:

- wrong launcher path
- wrong scope
- stale user config
- backend `.venv` missing
- `.env` points to a Docker-only database path

Fix:

- re-run `install_skill.py --check`
- verify the launcher path points to the current checkout
- verify `backend/.venv` exists
- then retry one smoke call

## 7. Native Windows Confusion

Symptom:

- the user assumes repo-local stdio requires `Git Bash` or `WSL`

Correct explanation:

- native Windows now has a real repo-local wrapper path:
  - `backend/mcp_wrapper.py`
- `Git Bash` / `WSL` are only needed when the user explicitly wants the POSIX
  shell wrapper path

Fix:

- tell the user to trust the installer-generated binding on native Windows
- do not ask them to manually copy bash launcher examples unless they chose
  `WSL` or `Git Bash`

## 8. Wrong Scope Expectation For Codex Or OpenCode

Symptom:

- the user expects workspace-local MCP to behave like the stable default

Fix:

- reset the explanation:
  - repo-local skill discovery is fine
  - stable MCP binding should usually be **user-scope first**

## 9. IDE Host Confusion

Symptom:

- the user applies CLI hidden-mirror logic to `Cursor`, `Windsurf`,
  `VSCode-host`, or `Antigravity`

Fix:

- say plainly that the project path is:
  - repo-local `AGENTS.md`
  - plus `python scripts/render_ide_host_config.py --host ...`
- do not lead with hidden skill mirrors

## 10. IDE Host Snippet Was Rendered, But The Host Still Does Not See It

Symptom:

- `render_ide_host_config.py` produced a valid snippet
- but the IDE host still cannot see `memory-palace`

Likely causes:

- snippet pasted into the wrong settings surface
- host does not support local stdio MCP
- host does not support workspace/project rules
- `Antigravity` is reading legacy rules only

Fix:

- confirm the snippet was pasted into the host's local stdio MCP surface
- confirm the repo-local rule file is in scope
- for `Antigravity`, mention `AGENTS.md` first and `GEMINI.md` as legacy
  fallback

## 11. Global IDE Runtime Layer Exists, But Tool Calls Still Fail

Symptom:

- the IDE still shows `memory-palace` rules, instructions, or workflows
- but actual tool calls fail after the user changed folders or after some time

Likely cause:

- the global runtime layer is still present at user scope
- but the global MCP config still points at one selected local
  `Memory-Palace` checkout
- that checkout moved, was deleted, lost `.venv`, or has a broken `.env`

Fix:

- explain that “global runtime visibility” and “working tool calls” are not the
  same thing
- verify which local checkout the IDE MCP config currently points to
- verify that the visible runtime surface still exists for the chosen host
  - for `VSCode-host`, check `~/.copilot/skills/memory-palace/`
  - for `VSCode-host`, check `~/.copilot/agents/memory-palace.agent.md`
  - for `Windsurf`, check `~/.codeium/windsurf/skills/memory-palace/`
- verify that checkout still has:
  - `backend/mcp_wrapper.py`
  - `backend/.venv`
  - a host-correct `.env`
- if the user wants another checkout to become the global target, rerun the
  global runtime installer against that checkout

## 12. Dashboard Setup Assistant Looks Unclear

Symptom:

- the UI shows masked or faint values
- the user cannot tell whether secrets or backend fields were really saved

Correct explanation:

- the setup assistant shows a safe summary and does not echo raw secret values
- backend-side changes still require a restart
- UI convenience does not prove skill discovery or client MCP binding

Fix:

- inspect the actual `.env` target and restart requirement
- return to the script path for client integration
- validate with `/health`, `install_skill.py --check`, and a real smoke call

## 13. Missing Local Prerequisites

Stop and say so when any of these are missing:

- repo checkout
- `.env` for repo-local stdio path
- `backend/.venv`
- the relevant install scripts in the main repo

Do not continue with speculative commands after a prerequisite is missing.
