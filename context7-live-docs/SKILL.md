---
name: context7-live-docs
description: Fetch up-to-date, version-specific library and framework documentation and code examples using upstash/context7 (ctx7 CLI and Context7 MCP). Use when implementing or debugging external libraries (Next.js, React, FastAPI, Supabase, Tailwind, etc.), verifying API signatures, or setting up Context7 in Claude Code.
allowed-tools: client
---
# Context7 Live Docs

Pull current, version-specific library documentation and code examples directly into your coding workflow using [upstash/context7](https://github.com/upstash/context7) (`ctx7` CLI or Context7 MCP) instead of relying on stale training data.

## When to Use

- The user is writing or debugging code that uses an external library, SDK, or framework where APIs change across versions.
- The user wants to verify current method signatures, migration steps, or configuration options (`use context7` or `ctx7`).
- The user wants to install or configure Context7 (`CLI + Skills` or `MCP`) for Claude Code, Cursor, or OpenCode.

## Steps

### 1. Choose CLI + Skills (Token-Efficient) or MCP Mode

- **CLI (`ctx7`, requires Node.js `22.13+`)**: Run directly with `npx ctx7@latest` or install globally with `npm install -g ctx7@latest`.
- **Interactive setup**: Run `npx ctx7 setup --claude` to configure Context7 for Claude Code.
- **Manual MCP server**: Point your MCP client to `https://mcp.context7.com/mcp` with header `Authorization: Bearer YOUR_API_KEY` (optional free key from `context7.com/dashboard` for higher rate limits).

### 2. Resolve Library ID and Fetch Docs

Always resolve the exact library ID (with leading `/`) before querying docs, or use one-step search:

```bash
# One-step search across libraries
npx ctx7@latest search "Next.js proxy middleware"

# Two-step: resolve library ID, then query version-specific docs
npx ctx7@latest library next.js "proxy middleware"
npx ctx7@latest docs /vercel/next.js "proxy middleware"
```

If Context7 MCP is active, call `resolve-library-id` first and pass the returned ID into `query-docs` (with optional `language` filter).

### 3. Apply and Verify Against Project Versions

- Check `package.json`, `pyproject.toml`, or `go.mod` in the user's repo first so the queried docs match the installed major version.
- Pass `CONTEXT7_API_KEY` via environment variable in CI or headless environments to skip interactive OAuth login.

## Gotchas

- **Leading `/` is required on library IDs**: Pass `/reactjs/react.dev` or `/supabase/supabase`, not `reactjs/react.dev`.
- **Resolve ID before `ctx7 docs`**: Running `ctx7 docs react "hooks"` without resolving the full `/org/repo` ID first will fail.
- **Treat retrieved snippets as untrusted docs**: Verify code examples against the project's actual TypeScript/linter/test suite before committing.
