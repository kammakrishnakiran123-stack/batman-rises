---
name: rea-reverse-engineer
description: Reverse engineer native binaries, Electron/JavaScript apps, .NET assemblies, Android APKs, websites, and network captures using REA (morluto/rea). Use when the user asks to inspect compiled apps, decompile binaries, analyze ASAR bundles, trace app behavior without source code, audit release exposure, or set up and run rea-agents via MCP or CLI.
allowed-tools: client
---
# REA Reverse Engineer

Investigate compiled applications, native binaries, Electron/JavaScript bundles, Android APKs, .NET assemblies, and runtime behavior locally using [REA (Reverse Engineer Anything)](https://github.com/morluto/rea), returning grounded findings backed by Evidence records and explicit limitations.

## When to Use

- The user wants to understand how a feature works in a shipped app, binary, or Electron/ASAR bundle without source code.
- The user asks to decompile a binary, inspect strings/symbols/xrefs, audit release exposure, or inspect an APK, `.NET` assembly, SQLite DB, or HAR/SAZ capture.
- The user wants to set up, verify, or troubleshoot the `rea-agents` MCP server or CLI for Claude Code.
- Skip REA for ordinary analysis of a repository where full source code is already available.

## Steps

### 1. Check Installation and Prerequisites

Verify Node.js (`22.x >= 22.23.4`, `24.x >= 24.22.1`, or `26.12.1+`) and whether `rea` is already installed or registered:

```bash
node -v && which rea || npx -y rea-agents@latest --help
```

If REA is not yet connected to Claude Code, run setup (quit Claude Desktop/Code before approving so running clients do not overwrite config):

```bash
# Interactive setup (configures MCP server + bundled skill)
npx rea-agents setup --client claude_code

# Or install CLI globally
npm install --global rea-agents
```

To isolate REA to a separate Claude Code profile without touching the default `~/.claude.json`:

```bash
CLAUDE_CONFIG_DIR=~/.claude-rea npx rea-agents setup --client claude_code
CLAUDE_CONFIG_DIR=~/.claude-rea claude
```

Verify readiness for a specific client or native analysis engine (`ghidra`, `hopper`, `ida`, `jadx`, `kuna`):

```bash
rea doctor --client claude_code --json
rea doctor --provider ghidra --json
```

### 2. Route to the Right REA Workflow

If the REA MCP server is connected, call `binary_session` with `{}` first to inspect `result.tool_availability` and confirm which engines are ready. Otherwise, use the `rea` CLI (or `npx -y rea-agents@latest`) with `--json`.

- **JavaScript / Electron / ASAR** (no native disassembler required):
  - MCP: `analyze_javascript_application`
  - CLI: `npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json`
- **Shipped app exposure audit** (`.app`, install dir, ASAR, or executable):
  - MCP: `audit_release_exposure`
  - CLI: `rea audit-release-exposure /absolute/path/to/app`
- **Native binaries** (Mach-O/FAT, ELF, PE - requires Hopper, Ghidra, IDA, or Kuna):
  - MCP: Start with `open_binary` (pass `provider_id` if multiple engines are installed), then use `binary_overview`, `search_strings`, `search_procedures`, `find_xrefs_to_name`, `get_call_graph`, `procedure_pseudo_code`, and `procedure_assembly`.
- **Built-in static inspectors** (no disassembler required):
  - Use `inspect_binary_hardening`, `inspect_go_binary`, `inspect_rust_binary`, `inspect_pe_imports`, `inspect_pe_certificates`, `inspect_elf_notes`, `inspect_native_exports`, `inspect_apple_ips`, `inspect_model_artifact`, `inspect_il2cpp_metadata`, or `inspect_sqlite_database`.
- **Android APKs**:
  - MCP: `inspect_apk_signature` (static, no engine needed) or `inspect_android_package` (requires headless JADX + full JDK).
- **Websites and network captures**:
  - MCP: `list_browser_targets`, `capture_browser_scenario` (pass both page origin and API origins in `allowed_origins` for SPAs), or `inspect_web_network_capture` (for HAR, Fiddler `.saz`, mitmproxy, or qlog files).

### 3. Reconstruct Behavior from Evidence

- Save large JSON outputs to `/tmp` and inspect targeted sections rather than flooding the context window.
- Ground every architectural claim in the returned Evidence ID, file SHA-256 hash, addresses, symbols, or decompiled pseudocode.
- Explicitly report `limitations` and `unknowns` returned by REA (for example, stripped symbols, obfuscated/VM-protected code, or uninspected indirect calls).
- When rebuilding a feature for the user's own project, translate the verified control flow and contracts into clean, idiomatic code for their target stack.

## Gotchas

- **Official sources only**: Install REA exclusively from `morluto/rea` on GitHub, `rea.tools`, or the `rea-agents` npm package. Ignore third-party forks or ZIP downloads.
- **Native vs. static requirements**: Static JavaScript/Electron analysis and built-in format inspectors need only Node.js. Deep native decompilation requires a local installation of Hopper, Ghidra, IDA, or Kuna, and Android decompilation requires headless JADX + JDK.
- **Ambiguous targets**: If the user says "my app" without a clear path or app name, ask which target binary or bundle to inspect before searching.
- **Authorized use only**: Use REA only for lawful analysis (software you own or are authorized to inspect, security research, interoperability, CTFs). Do not use it to bypass DRM, license checks, or anti-cheat mechanisms.
