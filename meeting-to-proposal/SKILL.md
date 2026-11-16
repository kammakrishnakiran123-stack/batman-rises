---
name: meeting-to-proposal
description: Turn raw meeting notes, call transcripts, or discovery bullets into structured client proposals, statements of work (SOW), or draft contracts. Use when the user asks to convert meeting notes into a proposal, scope document, SOW, or project agreement.
allowed-tools: client
---
# Meeting Notes to Proposal

Transform messy call notes or transcripts into a clear, client-ready proposal, statement of work (SOW), or draft service agreement.

## When to Use

- The user pastes meeting notes, a transcript, or voice-memo summary and asks for a proposal, quote, or SOW.
- The user wants to extract scope, deliverables, timeline, assumptions, and pricing from a discovery call.
- Optionally pair with skills from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) if installed.

## Steps

### 1. Extract Structured Inputs from Notes

Parse the meeting notes for:

- Client name, stakeholders, and project goal / pain points.
- In-scope deliverables and explicit out-of-scope items.
- Timeline, milestones, dependencies (client-provided assets/approvals), and budget/pricing terms.

### 2. Flag Gaps Before Finalizing

- If critical commercial terms (pricing, payment schedule, or key dates) are missing from the notes, list them cleanly so the user can fill or confirm them rather than inventing numbers.

### 3. Draft the Proposal / SOW

Structure the document cleanly:

1. **Executive Summary**: Problem statement and proposed outcome in 2-3 sentences.
2. **Scope & Deliverables**: Concrete, verifiable deliverables (and an explicit **Out of Scope** list).
3. **Timeline & Milestones**: Phased schedule with client review checkpoints.
4. **Investment & Payment Terms**: Itemized pricing table and payment schedule.
5. **Assumptions & Next Steps**: Approval/signature block and kickoff date.

## Gotchas

- **Never invent pricing or commitments**: Only use numbers, dates, and deliverables stated in the notes or confirmed by the user.
- **Explicit exclusions save projects**: Always include an Out of Scope section to prevent scope creep.
- **Legal review**: If turning the proposal into a binding contract, note that legal counsel should review liability and IP clauses.
