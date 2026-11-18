---
name: caveman-token-saver
description: Cut Claude Code and AI coding-agent token costs by compressing agent replies, shrinking large log/JSON/CSV tool outputs, and compressing CLAUDE.md memory files using JuliusBrussee/caveman. Use when the user wants shorter/terser replies, lower token usage, /caveman modes, or compressed CLAUDE.md files while keeping code and errors exact.
allowed-tools: client
---
# Caveman Token Saver

Reduce AI coding-agent input and output token usage using [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) while keeping code, commands, file paths, numbers, and error messages byte-exact.

## When to Use

- The user wants terser, zero-filler responses (`/caveman`, `/ultracave`, `/megacave`) to save tokens and read faster.
- The user wants to shrink `CLAUDE.md` / `AGENTS.md` memory files (`/caveman-compress`) or audit where session tokens go (`caveman learn`, `caveman stats`).
- The user wants to install or configure `JuliusBrussee/caveman` for Claude Code, Codex, Gemini CLI, or OpenCode.

## Steps

### 1. Install `JuliusBrussee/caveman` (Optional)

Install the skill only, the Claude Code plugin, or the full CLI (requires Node.js `22.13+`):

```bash
# Full CLI + output/input compression (macOS, Linux, Windows)
npx @caveman-ai/cli@latest

# Or skill-only install (no proxy)
npx skills add JuliusBrussee/caveman -g

# Or Claude Code marketplace plugin
/plugin marketplace add JuliusBrussee/caveman
/plugin install caveman@caveman
```

### 2. Apply Caveman Compression Rules

When operating in caveman mode (or running `/caveman` / `/ultracave`):

- **Answer first**: Lead with `[thing] [action] [reason]. [next step].` with no greeting, throat-clearing, or recap.
- **One idea per sentence**: Active voice, max ~20 words, drop filler articles (`a`, `an`, `the`) where meaning stays unambiguous.
- **Never drop negation or units**: Keep `not`, `never`, `no`, `only`, numbers, and units intact.
- **Payload verbatim**: Leave code blocks, shell commands, file paths, symbols, and error messages 100% untouched.
- **Auto-Clarity pause**: Automatically switch back to full, clear sentences for security warnings, irreversible/destructive action confirmations, or when the user is confused, then resume.

### 3. Compress Memory & Inspect Token Waste

- Run `/caveman-compress <file>` (or `caveman shrink -- <cmd>`) to shrink `CLAUDE.md` or noisy test/log outputs while keeping a backup of the original.
- Run `caveman status` to check active switches and `caveman stats` to inspect session savings.

## Gotchas

- **Never compress user prompts**: Rewriting the user's own prompt into caveman-speak degrades model accuracy; only compress agent output and bloated tool/memory files.
- **Security & destructive ops**: Always drop caveman phrasing for security warnings and destructive confirmations so nothing is misread.
- **Telemetry opt-out**: The CLI collects anonymous usage stats by default; disable permanently with `caveman telemetry off` or `DO_NOT_TRACK=1`.
