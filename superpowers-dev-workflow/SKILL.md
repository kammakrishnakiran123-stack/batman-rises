---
name: superpowers-dev-workflow
description: Run structured, spec-first, test-driven software engineering workflows using obra/superpowers (brainstorming, git worktrees, bite-sized implementation plans, subagent-driven development, RED-GREEN-REFACTOR TDD, systematic debugging, and pre-merge code review). Use when building non-trivial software features, refactoring codebases, or installing obra/superpowers in Claude Code.
allowed-tools: client
---
# Superpowers Dev Workflow

Apply the [obra/superpowers](https://github.com/obra/superpowers) agentic software development methodology: design before coding, isolate work in git worktrees, plan in bite-sized tasks, enforce RED-GREEN-REFACTOR TDD, and verify before merging.

## When to Use

- The user wants to build a non-trivial feature, service, or application with disciplined engineering guardrails.
- The user wants spec-first planning, subagent-driven task execution, systematic 4-phase debugging, or TDD enforcement.
- The user wants to install or update `obra/superpowers` in Claude Code, Codex, Cursor, Gemini CLI, or OpenCode.

## Steps

### 1. Optional: Install `obra/superpowers` in Claude Code

Install from Anthropic's official marketplace or the Superpowers marketplace:

```bash
# Official Claude plugin marketplace
/plugin install superpowers@claude-plugins-official

# Or Superpowers marketplace
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### 2. Follow the 6-Stage Engineering Loop

1. **Brainstorm & Spec**: Clarify requirements and edge cases before touching code; present the design in short, reviewable sections and get user sign-off.
2. **Isolate Workspace (`using-git-worktrees`)**: Create a dedicated feature branch or git worktree and verify a clean baseline test run before editing.
3. **Write Bite-Sized Plan (`writing-plans`)**: Break the approved spec into 2-5 minute tasks with exact file paths, concrete verification commands, and YAGNI/DRY discipline.
4. **RED-GREEN-REFACTOR (`test-driven-development`)**: Write a failing test first, watch it fail, write the minimal code to pass, then refactor cleanly.
5. **Execute & Review (`subagent-driven-development` / `requesting-code-review`)**: Dispatch isolated tasks (or execute inline sequentially) and review against the spec before advancing.
6. **Verify & Finish (`verification-before-completion` / `finishing-a-development-branch`)**: Run the full test suite and linter with real command output before claiming completion or proposing a merge/PR.

### 3. Systematic Debugging (When Fixing Bugs)

- Reproduce the failure reliably and trace root cause across 4 phases (observe, isolate, hypothesize, test) before changing code.
- Add a regression test that fails before the fix and passes after.

## Gotchas

- **Never skip the failing test**: Writing implementation code before a failing test violates RED-GREEN-REFACTOR and hides untestable coupling.
- **No claims without fresh verification**: Never state "tests pass" or "bug fixed" without running the verification command after the final edit.
- **Keep plans lean (YAGNI)**: Do not over-engineer abstractions or speculative features outside the signed-off spec.
