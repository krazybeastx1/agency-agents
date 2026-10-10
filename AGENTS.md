# AGENTS.md

## What this repo is

A corpus of **markdown agent definitions** (one `.md` per agent) plus pure-bash
tooling that converts them into 17 tool-specific formats and installs them.
No package.json, no build system, no test framework — the "test suite" is
`scripts/test-*.sh`. Content rules live in `CONTRIBUTING.md`; trust the
scripts/CI over prose when they disagree.

## Layout

- `<division>/<division>-<slug>.md` — source agents (18 divisions).
  `divisions.json` at the root is the single source of truth for the division set.
- `strategy/` — NEXUS playbooks/runbooks + `runbooks.json`. **Not a division**;
  files have no agent frontmatter.
- `integrations/<tool>/` — **generated** output of `scripts/convert.sh`.
  Only `integrations/<tool>/README.md` is committed; everything else is gitignored.
- `examples/`, `scripts/` — also not divisions.
- `.opencode/agents/` in a working copy is local `install.sh` output: untracked
  and *not* gitignored — never commit it.

## Commands (verified)

```bash
./scripts/lint-agents.sh [file ...]        # frontmatter + section lint; no args = whole roster
./scripts/check-agent-originality.sh [file ...]  # near-duplicate detection (needs python3)
./scripts/check-divisions.sh               # divisions.json vs dirs vs scripts vs CI
./scripts/check-tools.sh                   # tools.json vs install.sh vs convert.sh
./scripts/check-runbooks.sh                # runbook roster slugs → real agent filenames
./scripts/test-convert-outputs.sh          # regenerate all tool output, check the product
./scripts/test-install.sh [-v]             # installer tests, sandboxed $HOME
./scripts/convert.sh [--tool <name>]       # regenerate integrations/<tool>/
```

- `bash -n scripts/*.sh` is the only syntax check CI does on every script.
- CI's ordered checklist for converter/installer changes is
  `.github/workflows/check-tools.yml` — read it and run those steps in that
  order; `.github/workflows/test-install.yml` adds macOS + Linux (bash 3.2/5).
- Converter changed on purpose? `./scripts/test-convert-outputs.sh --update`
  and commit `scripts/convert-outputs.sha256` in the same PR.

## Rules that are easy to break

- **Never commit generated `integrations/<tool>/*` files.** A new tool needs a
  matching `.gitignore` rule — the easiest step to miss (CONTRIBUTING.md's
  integration checklist).
- **Adding a division** touches 5 places: the directory, `divisions.json`,
  `AGENT_DIRS` in both `scripts/convert.sh` and `scripts/lint-agents.sh`, and the
  path filters in `.github/workflows/lint-agents.yml`. `check-divisions.sh`
  fails until all agree.
- **Adding a tool**: `tools.json` + `convert_<tool>()` + `install_<tool>()` +
  `.gitignore` + `integrations/<tool>/README.md`, then `check-tools.sh`.
  New integrations are "discuss first" per CONTRIBUTING.md.
- **Frontmatter**: `name`, `description`, `color` are required (error);
  recommended sections only warn. A `color` *name* must be one of the keys in
  `resolve_opencode_color()` in `scripts/convert.sh` — anything else silently
  becomes grey in the OpenCode output. Hex `#RRGGBB` always works.
  `lint-agents.sh` reads the allowed names out of the converter, so it can't drift.
- **Section headers matter**: `convert.sh` splits agent bodies into persona vs
  operations by those headings — keep Identity/Communication/Rules grouped apart
  from Mission/Deliverables/Workflow/Metrics.
- **Slugs**: the agent filename stem is the id used by `strategy/runbooks.json`
  and the desktop app. Renaming/removing a file breaks `check-runbooks.sh`.
- **Bash 3.2 + BSD userland only**: no jq, no GNU-only flags; scripts run on
  macOS CI. Shared helpers live in `scripts/lib.sh`.
- **The installer/README warn that OpenCode only registers ~119 agents**
  (anomalyco/opencode#27988). On opencode v2.0.24 that cap no longer
  reproduces: `opencode debug agents` returns every installed agent (273 +
  7 built-ins = 280 here). Trust that command over the warning, and check
  which agents actually loaded after an install.

## PR scope (from CONTRIBUTING.md)

A single new/edited agent `.md` is the ideal PR. Bulk edits to existing agents,
committed build output, and find-replace "re-skins" are closed without merge —
run `check-agent-originality.sh` first. Manifest drift on agent PRs is
advisory; maintainers regenerate `convert-outputs.sha256` at landing.
