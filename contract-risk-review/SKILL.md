---
name: contract-risk-review
description: Review terms of service, contracts, NDAs, and agreements for legal risks, missing protections, market benchmarks, and redlines using evolsb/claude-legal-skill patterns. Use when the user asks to review a contract, flag risky clauses, compare terms, or draft redlines.
allowed-tools: client
---
# Contract Risk Review

Analyze contracts, NDAs, SaaS terms, and vendor agreements for risk exposure, missing standard protections, and suggested redlines, informed by [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill).

## When to Use

- The user shares a contract, NDA, MSA, SLA, or terms of service to review.
- The user asks to identify unfavorable clauses, liability caps, IP ownership traps, auto-renewals, or termination risks.
- The user wants suggested redline wording or a negotiation summary.

## Steps

### 1. Optional: Install `evolsb/claude-legal-skill`

If the user wants the full upstream CUAD benchmark skill installed in Claude Code:

```bash
git clone https://github.com/evolsb/claude-legal-skill ~/.claude/skills/contract-review
```

### 2. Gather Context and Party Role

Identify before reviewing:

- Which party the user represents (vendor, customer, employer, contractor, licensor, licensee).
- Jurisdiction / governing law if stated.
- Deal sensitivity (standard low-value NDA vs. high-value commercial agreement).

### 3. Run Structured Clause-by-Clause Risk Review

Inspect and classify issues by severity (`High`, `Medium`, `Low`):

- **Liability & Indemnification**: Uncapped liability, one-sided indemnities, consequential damages carve-outs.
- **IP & Confidentiality**: Broad IP assignment of pre-existing IP, weak NDA survival/exclusions, data-training rights.
- **Term, Renewal & Termination**: Silent auto-renewal windows, lack of termination for convenience or cure periods.
- **Payment, SLA & Scope**: Unclear acceptance criteria, unlimited scope creep, punitive late fees.

### 4. Produce Actionable Redlines

- Present a concise risk summary table (Clause | Risk Level | Issue | Proposed Redline).
- Quote exact section numbers/headings from the provided document.
- Include a clear note that this review is an analytical aid and not formal legal advice.

## Scripts

`scripts/clause_scan.py` is a first-pass triage over plain text. It prints each candidate clause with its line number. Convert PDF or DOCX to text first. Pattern matching misses clauses and flags harmless wording, so read every hit in context.

```bash
python3 scripts/clause_scan.py contract.txt
```

## Gotchas

- **Not legal advice**: Always state clearly that AI contract review does not replace review by a qualified attorney in the relevant jurisdiction.
- **Never invent clauses**: Only cite sections, numbers, and obligations that appear in the supplied contract text.
- **Watch definitions**: Defined terms (like "Confidential Information" or "Deliverables") often hide the real risk outside the main clause.
