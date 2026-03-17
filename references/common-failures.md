# Common Failures

Use this file when the user is already following setup steps but the result still does not work.

## 1. “Docker is up, why can’t the client use Memory Palace?”

Cause:

- The user started `Dashboard / API / SSE`
- but never installed the repo’s skill layer or bound MCP for the client

What to say:

- Service startup and client integration are different layers.
- If the user wants the client to use Memory Palace in normal conversations, move them to the `skills + MCP` path.

## 2. Docker `/app/...` path copied into local `.env`

Cause:

- The user copied a container-internal path such as `/app/data/...` into the host-side `.env`

Why it breaks:

- repo-local stdio MCP runs on the host, not inside the container

What to say:

- Use a host absolute path in local `.env`
- or keep using Docker `/sse`
- do not mix the two

## 3. Skill installed, but MCP not bound

Symptom:

- the client can see or mention the skill
- but actual tool calls do not work

Cause:

- only the discovery layer is present

Fix:

- run the repo’s `install_skill.py --with-mcp`
- validate with the client’s `mcp list`

## 4. MCP bound, but skill not discovered

Symptom:

- tools exist
- but the model does not reliably enter the Memory Palace workflow

Cause:

- only MCP was added
- the repo skill was never synced or installed

Fix:

- sync or install the repo’s `memory-palace` skill first

## 5. Native Windows shell mismatch

Symptom:

- commands copied from docs fail around `bash` or `/bin/zsh`

Cause:

- the repo-local wrapper examples assume `Git Bash` or `WSL`

Fix:

- tell the user this is a real runtime boundary, not a docs typo
- ask them to use `Git Bash` or `WSL`
- or switch to a path that does not require the local wrapper

## 6. Wrong scope expectation for Codex or similar clients

Symptom:

- the user expects a workspace-local MCP entry to behave like the default stable path

Fix:

- reset the explanation:
  - repo-local skill discovery is fine
  - stable MCP binding should usually be user-scope first

## 7. IDE host confusion

Symptom:

- the user applies CLI hidden-mirror logic to `Cursor` or `Antigravity`

Fix:

- say plainly that the project’s own integration path is:
  - repo-local `AGENTS.md`
  - rendered MCP snippet
- do not lead with CLI-only mirror assumptions

## 8. Missing local prerequisites

Stop and say so when any of these are missing:

- repo checkout
- `.env` for repo-local stdio path
- `backend/.venv`
- the relevant install scripts in the main repo

Do not continue with speculative commands after a prerequisite is missing.
