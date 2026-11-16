---
name: fluent-language-tutor
description: Run AI language-learning sessions with spaced repetition (SM-2) or build a language-learning app using m98/fluent. Use when the user asks to practice a foreign language, drill vocabulary, set up m98/fluent in Claude Code, or build a language-learning tool.
allowed-tools: client
---
# Fluent Language Tutor

Practice vocabulary, writing, speaking, and reading with SM-2 spaced repetition—or build a custom language-learning app—using [m98/fluent](https://github.com/m98/fluent).

## When to Use

- The user wants to install or use `m98/fluent` in Claude Code for structured language learning.
- The user asks to practice a target language (vocab drills, writing correction, graded reading, conversation).
- The user wants to build a language-learning app or spaced-repetition flashcard/tutor workflow.

## Steps

### 1. Install `m98/fluent` (Optional for Claude Code)

Requires Python `3.8+` (standard library only, no pip packages needed):

```bash
# Global plugin install in Claude Code
claude plugin marketplace add m98/fluent && claude plugin install fluent@m98

# Or clone for per-project state
git clone https://github.com/m98/fluent.git && cd fluent && claude
```

### 2. Run Fluent Commands (When Installed)

Restart Claude Code after installing, then use:

- `/fluent-setup` to configure name, target language, current level, and goals.
- `/fluent-learn` to start a guided session.
- Focused skills: `/fluent-vocab`, `/fluent-writing`, `/fluent-speaking`, `/fluent-reading`, `/fluent-review`, `/fluent-progress`.

### 3. Build or Run a Custom Language Session (Standalone)

If building an app or running a session without the plugin:

- Track items with SM-2 spaced repetition (`ease_factor`, `interval_days`, `repetitions`, `next_review`).
- Grade learner responses with clear severity (`critical`, `moderate`, `minor`), natural native phrasing, and one targeted rule explanation.
- Log session results to a local JSON/SQLite store so weak patterns inform the next session.

## Gotchas

- **Adapt to CEFR level**: Keep explanations and target-language prompts calibrated to the learner's stated level (A1-C2).
- **Correct gently and concretely**: Show the natural native correction right beside the learner's sentence rather than lecturing.
- **No external pip deps needed**: `m98/fluent` uses Python's standard library only; verify `python3 --version` is `3.8+`.
