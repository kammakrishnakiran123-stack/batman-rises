---
name: repomix-codebase-packer
description: Pack local or remote GitHub repositories into AI-friendly XML, Markdown, or JSON snapshots with Tree-sitter compression, token counting, git diffs/logs, and Secretlint checks using yamadashy/repomix. Use when analyzing a codebase, feeding a repo to an LLM, auditing token usage, or configuring Repomix MCP/plugins in Claude Code.
allowed-tools: client
---
# Repomix Codebase Packer

Package entire local codebases or remote GitHub repositories into a single AI-friendly snapshot (XML, Markdown, JSON, or plain text) with token-count breakdowns, Tree-sitter structural compression (`--compress`), and built-in Secretlint credential checks using [yamadashy/repomix](https://github.com/yamadashy/repomix).

## When to Use

- The user wants to feed a local project or remote GitHub repo into an LLM for architecture review, refactoring, test generation, or documentation.
- The user wants to inspect token distribution (`--token-count-tree`) or stay within a strict context budget (`--token-budget`).
- The user wants to install or configure Repomix as a Claude Code plugin or sandboxed MCP server.

## Steps

### 1. Optional: Install `yamadashy/repomix` in Claude Code

Run directly with `npx repomix@latest` (no install needed), or install the official Claude Code plugins / MCP server:

```bash
# Claude Code plugins
/plugin marketplace add yamadashy/repomix
/plugin install repomix-mcp@repomix
/plugin install repomix-explorer@repomix

# Or register MCP server directly (add --sandbox for untrusted workspaces)
claude mcp add repomix -- npx -y repomix --mcp --sandbox
```

### 2. Pack Local or Remote Repositories

- **Inspect token distribution first** (prevents context overflow):
  ```bash
  npx repomix@latest --token-count-tree 1000
  ```
- **Pack local codebase** (XML default is best for Claude; add `--compress` for ~70% token reduction on large repos):
  ```bash
  npx repomix@latest --style xml --compress -o /tmp/repomix-output.xml
  ```
- **Pack filtered files or recent git changes**:
  ```bash
  npx repomix@latest --include "src/**/*.ts,**/*.md" --ignore "**/*.test.ts" --include-diffs --include-logs --include-logs-count 10
  ```
- **Pack a remote GitHub repository** without manually cloning:
  ```bash
  npx repomix@latest --remote yamadashy/repomix --compress -o /tmp/remote-pack.xml
  ```

### 3. Analyze Packed Output Incrementally

- For large packed files, use `grep` / targeted line reads instead of loading the entire output into context at once.
- Split oversized packs with `--split-output 1mb` when targeting tools with strict file-size caps.

## Gotchas

- **Untrusted repository configs**: Remote `repomix.config.*` files are ignored by default because `input.processors` can execute shell commands. Never pass `--remote-trust-config` unless you have audited the remote config first, and always pass `--sandbox` when exposing Repomix MCP to untrusted directories.
- **Keep Secretlint active**: Do not pass `--no-security-check` unless working solely with sanitized mock fixtures, so credentials are never leaked into packed outputs.
- **Clean up temporary packs**: Write outputs to `/tmp/` or add `repomix-output.*` to `.gitignore` so large snapshots are not accidentally committed.
