---
name: Memory Palace
description: Use Memory Palace durable memory tools and workflow across sessions.
tools: ['memory-palace/*']
target: vscode
---

# Memory Palace Runtime

Use this custom agent for the runtime `memory-palace` layer from the main
`Memory-Palace` repository.

Core runtime rules:

- Before the first real Memory Palace operation in a session, start with
  `read_memory("system://boot")`.
- If the target URI is unknown, use `search_memory(..., include_session=true)`
  before guessing a path.
- Read before every mutation: `create_memory`, `update_memory`,
  `delete_memory`, `add_alias`.
- If `guard_action` is `NOOP`, `UPDATE`, or `DELETE`, stop and inspect
  `guard_target_uri` / `guard_target_id` before deciding what to do next.
- Prefer repo-visible references under `docs/skills/memory-palace/`.
- If the user is asking how to install or connect Memory Palace itself, switch
  to the setup guidance repo instead of staying in the runtime workflow.
