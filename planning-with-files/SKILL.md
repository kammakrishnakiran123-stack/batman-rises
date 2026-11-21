---
name: planning-with-files
description: Maintain crash-proof, Manus-style persistent file-based planning on disk (task_plan.md, findings.md, progress.md) for long-running tasks and multi-session recovery using OthmanAdi/planning-with-files. Use when starting complex multi-phase tasks, preventing context rot across /clear or compaction, or installing planning-with-files in Claude Code.
allowed-tools: client
---
# Planning With Files

Keep long-running agent tasks on track across `/clear`, context compaction, and multi-session handoffs by storing execution state in three Markdown files on disk (`task_plan.md`, `findings.md`, `progress.md`), adapted from [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files).

## When to Use

- A task spans 3+ phases, >5 tool calls, or multiple files/APIs where context rot or mid-run resets are likely.
- The user wants crash-proof progress tracking, session recovery after `/clear`, or isolated parallel task plans (`.planning/YYYY-MM-DD-<slug>/`).
- The user wants to install or configure `OthmanAdi/planning-with-files` in Claude Code, Codex, Cursor, OpenCode, or Gemini CLI.

## Steps

### 1. Optional: Install `OthmanAdi/planning-with-files`

Install the Claude Code plugin (includes lifecycle hooks and `/plan`, `/pwf`, `/status`, `/plan-doctor`, `/plan-attest`) or the standalone skill:

```bash
# Claude Code plugin (recommended, includes hooks and slash commands)
/plugin marketplace add OthmanAdi/planning-with-files
/plugin install planning-with-files@planning-with-files

# Or cross-agent standalone skill (60+ agents)
npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g
```

### 2. Initialize the 3-File Pattern

Before starting execution on a complex task, create (and gitignore for working scratchpads if not a deliverable):

- **`task_plan.md`**: Goal, numbered phases with checkboxes (`[ ]`, `[x]`), current phase, and completion criteria.
- **`findings.md`**: Research notes, verified URLs, key decisions, and constraints discovered along the way.
- **`progress.md`**: Chronological session log, commands run, and test/verification results.

For parallel tasks in the same repo, isolate each plan under `.planning/YYYY-MM-DD-<slug>/` and pin threads via `PLAN_ID=<slug>`.

### 3. Follow the Core Execution Rules

- **Create Plan First**: Never start multi-phase work without `task_plan.md` on disk.
- **2-Action Rule**: Flush key discoveries to `findings.md` after every 2 read/browse/search operations so visual or web context is never lost.
- **Re-read Before Acting**: Read `task_plan.md` after compaction or `/clear` before making the next edit.
- **Log All Errors & Never Repeat Failures**: Record failed attempts in `progress.md` and mutate the approach rather than retrying the exact same failing step.

## Gotchas

- **Keep working plans out of git**: Add `task_plan.md`, `findings.md`, `progress.md`, and `.planning/` to `.gitignore` unless the user explicitly wants them committed.
- **Hooks require the plugin route**: `npx skills add` installs `SKILL.md` without Claude Code lifecycle hooks; use `/plugin install` and verify with `/plan-doctor` if automatic turn-start injection and Stop-gate checks are needed.
- **One-shot opt-out**: Set `PLANNING_DISABLED=1` for quick unrelated tasks in a directory that already has an active plan.
