---
description: Browse, list by division, and dispatch the 282 agency subagents (Claude Code)
argument-hint: "[lists [division] | <agent name> <task>]"
allowed-tools: Agent, Read, Glob, Bash(python3:*)
disable-model-invocation: true
---

The "agency" roster is installed as Claude Code subagents in `~/.claude/agents/`
— 282 agents across 18 divisions. Every entry below is shown as
`fileName=>Agent Name`; **dispatch using the Agent Name** (Claude identifies a
subagent only by its frontmatter `name`).

!`python3 "${CLAUDE_PROJECT_DIR}/.claude/commands/roster.py"`

Requested: $ARGUMENTS

Handle exactly one case, then stop:

1. **Empty, or `lists`** — Present the whole roster grouped by division: division
   label, agent count, and each agent's **Agent Name** with a one-line summary
   (read `~/.claude/agents/<fileName>.md` to source the `description:`).
   Recommend 2-3 agents for what the user seems to be doing, then ask what they
   want to delegate. Launch nothing.

2. **`lists <division>` or a bare `<division>`** — A valid division is one of the
   keys in `DIVISIONS:` above; display labels such as "Game Development" also
   work. List **only that division's** agents with one-line summaries, recommend
   1-2, and ask what to delegate. Launch nothing.

   In cases 1 and 2, output a clean markdown table or bullet list of Agent Name +
   summary. **Do not paste raw file contents** (no frontmatter, no prompt bodies)
   — summarize the `description:` in your own words.

3. **`<agent name> <task>`** — If the first argument matches an Agent Name from
   the roster (case-insensitive; the file stem also works, e.g.
   `security-penetration-tester`), dispatch it with the **Agent tool**, setting
   `subagent_type` to the exact **Agent Name** (e.g. `Penetration Tester`), and
   pass the remainder of the arguments as the task prompt. If only a name is
   given with no task, pick a sensible default from that agent's specialty — or
   ask for one. The subagent does the work; do not do it in this session.

4. **Anything else** — Say there is no such agent or division, show the nearest
   matches, and print the syntax:
   `/subagents` · `/subagents lists <division>` · `/subagents <agent name> <task>`
