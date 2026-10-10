---
description: Browse, list by division, and dispatch the 282 agency subagents
---

The agency roster is installed as OpenCode subagents in `.opencode/agents/` —
282 agents, all `mode: subagent`, so they never appear in `/agents` and are
dispatched from here instead. They are grouped into the divisions below
(computed live from `divisions.json` + the installed files).

!`cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" && python3 .opencode/commands/roster.py`

Requested: $ARGUMENTS

Handle exactly one of these cases, then stop:

1. **Empty, or `lists`** — Present the whole roster grouped by division: division
   name, agent count, and each agent's id with a short description (read
   `.opencode/agents/<id>.md` to source it). Recommend 2-3 agents for what the
   user seems to be doing, and ask what they want to delegate. Launch nothing yet.

2. **`lists <division>` or a bare `<division>`** — A valid division is one of the
   keys in `DIVISIONS:` above (display labels like "Game Development" also work).
   List **only that division's** agents with short descriptions, then recommend
   1-2 and ask what to delegate. Launch nothing yet.

In cases 1 and 2, output a clean markdown table or bullet list of id + one-line
summary. **Do not paste raw agent file contents** (no frontmatter, no system
prompt bodies) — summarize the `description:` in your own words.

3. **`<id> [task]`** — If the first argument matches an installed subagent id or
   display name, dispatch the remainder as the task to that subagent **using the
   subagent tool, in a foreground child session**. Do not do the work yourself in
   this session. With no task after the id, pick a sensible default from the
   agent's specialty, or ask for one.

4. **Anything else** — Say there is no such subagent or division, show the
   closest matches, and print the syntax:
   `/sub-agents` · `/sub-agents lists <division>` · `/sub-agents <id> [task]`