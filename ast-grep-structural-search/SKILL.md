---
name: ast-grep-structural-search
description: Perform AST-based structural code search, linting, and multi-file refactoring across JS/TS, Python, Rust, Go, Java, and C/C++ using ast-grep/agent-skill and ast-grep-mcp. Use when searching code by syntax structure rather than plain text, finding missing error handling, auditing patterns, or running safe structural rewrites.
allowed-tools: client
---
# ast-grep Structural Search

Search, lint, and rewrite codebases by Abstract Syntax Tree (AST) structure rather than brittle regex or plain-text grep using [ast-grep/agent-skill](https://github.com/ast-grep/agent-skill) and `ast-grep`.

## When to Use

- The user wants to find code by syntax or structural context (for example, async functions missing `try/catch`, React hooks inside conditionals, or functions with >3 parameters).
- The user wants safe, syntax-aware multi-file refactoring or custom lint rules across TypeScript, JavaScript, Python, Rust, Go, Java, or C/C++.
- The user wants to install `ast-grep/agent-skill` or `ast-grep-mcp` in Claude Code.

## Steps

### 1. Check Prerequisites and Optional Plugin Install

Verify `ast-grep` is installed (install via Homebrew, npm, or Cargo if missing):

```bash
ast-grep --version || brew install ast-grep
```

To install the official Claude Code skill or MCP server:

```bash
# Via skills.sh or Claude Code plugin marketplace
npx skills add ast-grep/agent-skill
# Or inside Claude Code:
/plugin marketplace add ast-grep/agent-skill
/plugin install ast-grep
```

### 2. Run Structural Pattern or Rule Searches

- **Simple pattern search** (use `$VAR` metavariables for any single AST node and `$$$` for zero or more nodes):
  ```bash
  ast-grep run --pattern 'console.log($ARG)' --lang javascript .
  ```
- **Relational / composite rule search** (for structural context like "inside" or "missing child"):
  ```bash
  ast-grep scan --inline-rules "id: async-no-try
  language: javascript
  rule:
    kind: function_declaration
    has:
      pattern: await \$EXPR
      stopBy: end
    not:
      has:
        kind: try_statement
        stopBy: end" .
  ```
- **Safe structural rewrite** (preview diffs before applying `--update-all`):
  ```bash
  ast-grep run --pattern 'oldApi($A, $B)' --rewrite 'newApi({ a: $A, b: $B })' --lang typescript .
  ```

### 3. Debug Zero-Match Patterns

- A zero-match `ast-grep` run exits with code `0`, so "no results" and "wrong AST pattern" look identical.
- Test the pattern against a minimal 3-line snippet first, or dump the AST with `ast-grep-mcp` / `--debug-query` before scanning the whole repo.

## Gotchas

- **Quote `$` metavariables in bash**: Always wrap patterns in single quotes (`'$VAR'`) or escape `\$EXPR` in double-quoted inline YAML so the shell does not expand them as empty variables.
- **Specify `--lang` explicitly**: Multi-language repos (`.ts` vs `.tsx` vs `.js`) need explicit `--lang` (for example, `--lang tsx` for JSX) so parser rules match cleanly.
- **Preview before `--update-all`**: Always inspect matched locations or `git diff` after a structural rewrite before committing.
