---
name: security-audit-static
description: Run structured static security audits, Semgrep/CodeQL scanning, variant analysis, fail-open insecure-defaults checks, dependency supply-chain audits, and GitHub Actions security reviews using trailofbits/skills. Use when the user asks to audit code for vulnerabilities, write Semgrep rules, check supply-chain risk, or install trailofbits/skills in Claude Code.
allowed-tools: client
---
# Security Audit (Static)

Perform repeatable static security audits, variant analysis, supply-chain risk checks, and GitHub Actions workflow reviews informed by [trailofbits/skills](https://github.com/trailofbits/skills).

## When to Use

- The user asks for a security review or vulnerability audit of a codebase, PR diff, or GitHub Actions workflow.
- The user wants to run Semgrep/CodeQL static analysis, find variant bugs across files, or check for fail-open insecure defaults.
- The user wants to audit npm/PyPI/Go dependencies for supply-chain risk or install `trailofbits/skills` in Claude Code.

## Steps

### 1. Optional: Install `trailofbits/skills` in Claude Code

Add the Trail of Bits marketplace and pick specific security plugins via `/plugin menu`:

```bash
/plugin marketplace add trailofbits/skills
/plugin menu
```

### 2. Build Context Before Hunting Bugs

- Map entry points, trust boundaries, authentication/authorization checks, and sensitive data sinks before flagging issues.
- For PRs or commits, run a differential review (`git diff`) to focus on newly introduced attack surfaces and regressions.

### 3. Run Layered Static Checks

- **Pattern & SAST scanning (`static-analysis` / `semgrep-rule-creator`)**: Run Semgrep or CodeQL if installed, or write targeted Semgrep rules for the discovered bug class to catch every variant across the repo.
- **Insecure defaults (`insecure-defaults`)**: Check for fail-open auth, hardcoded secrets, permissive CORS, disabled TLS verification, or weak crypto defaults.
- **Supply chain (`supply-chain-risk-auditor`)**: Inspect `package.json`, `requirements.txt`/`pyproject.toml`, and `go.mod` for known advisories, suspicious install scripts, or unpinned dependencies.
- **CI/CD & Agentic Actions (`agentic-actions-auditor`)**: Audit `.github/workflows/` for untrusted `pull_request_target` triggers, prompt injection into AI actions, and over-privileged `GITHUB_TOKEN` permissions.

### 4. Verify Findings & Report Severity

- Run false-positive verification (`fp-check`) on every candidate bug: confirm reachability from an untrusted input and lack of upstream sanitization.
- Report only verified or clearly marked unverified findings with exact file paths, line numbers, impact, CVSS-style severity, and concrete remediation diffs.

## Gotchas

- **Never claim a clean bill of health**: Static analysis proves presence of bugs, not absence of vulnerabilities; state exact scope and unexamined paths.
- **Verify reachability**: Do not report theoretical sinks without tracing whether untrusted input can actually reach them.
- **Do not run exploits against external targets**: Keep all analysis local and authorized to the target repository.
