---
name: sales-engine-workflow
description: Run a structured sales workflow for prospect research, personalized outreach sequences, objection-handling playbooks, call follow-ups, and pipeline tracking. Use when the user asks to research leads, draft cold emails or LinkedIn outreach, prep for a sales call, or organize a sales pipeline.
allowed-tools: client
---
# Sales Engine Workflow

Turn prospect lists, company websites, and call notes into personalized outreach sequences, call prep briefs, objection responses, and CRM-ready pipeline summaries.

## When to Use

- The user wants to research target accounts/leads and draft personalized cold outreach or follow-up sequences.
- The user wants a call prep brief, discovery questions, or an objection-handling playbook.
- The user wants to organize lead data (CSV/JSON/notes) into a prioritized outreach plan.

## Steps

### 1. Define ICP and Value Proposition

Confirm from context (ask only if missing):

- Product/service being sold and core measurable outcome.
- Ideal Customer Profile (role, company size, industry, trigger event).
- Desired CTA (15-min intro call, async demo, audit, reply).

### 2. Research & Personalize per Account

- Ground every outreach hook in real, verified company signals (recent launch, job postings, public news, tech stack) rather than generic flattery.
- Keep cold emails under 100-125 words: 1-line specific trigger, 1-line problem/outcome, 1 low-friction CTA.

### 3. Build Multi-Touch & Follow-Up Assets

- **Outreach sequence**: Initial email + 2 short value-add follow-ups + LinkedIn note.
- **Call prep / follow-up**: Recap buyer pain points, agreed next steps, and mutual action plan after calls.
- **Pipeline export**: Output clean CSV/Markdown tables ready for CRM import.

### 4. Objection-Handling Playbook

When the user is preparing for objections, or pastes one from a live thread:

1. Name the objection as it was really said (price, timing, "we already use X", no budget owner).
2. Give one response that addresses the underlying concern, not a script that argues with it.
3. Give one proof point taken from the user's material or verified sources. Do not invent a customer result.
4. End with a question that moves the deal forward.

Keep the playbook in a Markdown file so the user can reuse it across calls.

### 5. Pipeline CSV Schema

When the user has no CRM export, use this column order so the output imports cleanly:

`account, contact_name, contact_role, trigger_event, source_url, stage, next_step, next_step_date, owner, priority`

Leave a cell empty rather than guessing. `source_url` is required for any `trigger_event` to be used in outreach.

## Scripts

`scripts/pipeline_check.py` validates a pipeline CSV against the schema above. It exits 1 on errors, so it can gate an import.

```bash
python3 scripts/pipeline_check.py pipeline.csv --today 2026-11-16
```

## Gotchas

- **Never fabricate company facts**: Only cite triggers, metrics, or news verified from user input or search results.
- **No spammy templates**: Avoid hype words, fake urgency, or walls of text; respect opt-out and compliance norms.
- **Confirm before sending**: Always review outbound emails/messages with the user before sending.
