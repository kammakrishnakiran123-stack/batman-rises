---
name: skill-router
description: Central orchestrator skill that inspects the user's request, selects the best matching skill(s) from the Skills library, loads their instructions, and executes or chains them as needed. Use when starting any task that may match an installed skill, when the user asks which skill to use, or when routing/chaining multi-step workflows.
allowed-tools: client
---
# Skill Router

Route any user request to the right specialized skill(s) in your Skills library, load only the needed instructions on demand, and coordinate multi-step handoffs when a task spans multiple skills.

For multi-skill workflows, feasibility checks, and shared safety rules, start from `batman-master/SKILL.md`. This file is the routing table.

## When to Use

- The user asks you to pick, assign, or run the right skill for a task.
- A request matches one or more installed skills across engineering, media, productivity, legal/business, or home automation.
- A complex workflow requires chaining two or more skills together (for example, `last30days` research into `lemo-opuscar` film generation, or `podcast-clipper-search` into `content-production-pipeline`).

## Steps

### 1. Discover Available Skills

Check the local Skills directory (for example, `~/.claude/skills` or `./`) so newly added skills are never missed:

```bash
ls -la ~/.claude/skills . 2>/dev/null || true
```

### 2. Match Requirement to Skill

Use this routing table to assign the primary skill (and any secondary skill for multi-step tasks):

| User Requirement / Use Case | Assigned Skill | File Path |
| --- | --- | --- |
| AST-based structural code search, lint rules & safe multi-file rewrites (`ast-grep/agent-skill`) | `ast-grep-structural-search` | `ast-grep-structural-search/SKILL.md` |
| Generate UI/UX design systems, accessible palettes, font pairings & DTCG/CSS tokens (`nextlevelbuilder/ui-ux-pro-max-skill`) | `ui-ux-design-system` | `ui-ux-design-system/SKILL.md` |
| Pack local/remote repos into AI-friendly XML/Markdown with Tree-sitter compression & token tree (`yamadashy/repomix`) | `repomix-codebase-packer` | `repomix-codebase-packer/SKILL.md` |
| Fetch live, version-specific library & API docs via `ctx7` CLI or Context7 MCP (`upstash/context7`) | `context7-live-docs` | `context7-live-docs/SKILL.md` |
| Token-efficient browser automation, E2E UI testing, screenshots & network inspection (`microsoft/playwright-cli`) | `playwright-browser-automation` | `playwright-browser-automation/SKILL.md` |
| Persistent file-based planning (`task_plan.md`, `findings.md`, `progress.md`) & crash recovery (`OthmanAdi/planning-with-files`) | `planning-with-files` | `planning-with-files/SKILL.md` |
| Static security audit, Semgrep/CodeQL, variant analysis, supply-chain & CI checks (`trailofbits/skills`) | `security-audit-static` | `security-audit-static/SKILL.md` |
| Cut Claude Code token usage with ultra-terse replies, log compression, and `CLAUDE.md` shrinking (`JuliusBrussee/caveman`) | `caveman-token-saver` | `caveman-token-saver/SKILL.md` |
| Spec-first planning, git worktrees, TDD, subagent dev, and systematic debugging (`obra/superpowers`) | `superpowers-dev-workflow` | `superpowers-dev-workflow/SKILL.md` |
| Reverse engineer binaries, Electron/ASAR, APKs, `.NET`, websites, HAR/SAZ (`morluto/rea`) | `rea-reverse-engineer` | `rea-reverse-engineer/SKILL.md` |
| Create code-generated short films or custom visual styles (`lemomo-ai/lemo-opuscar`) | `lemo-opuscar` | `lemo-opuscar/SKILL.md` |
| Build, install, or customize Free My TV on Google TV, LG webOS, or Samsung Tizen | `free-my-tv` | `free-my-tv/SKILL.md` |
| Send/receive WhatsApp messages or voice notes via Claude Code (`rich627/whatsapp-claude-plugin`) | `whatsapp-claude-channel` | `whatsapp-claude-channel/SKILL.md` |
| Review contracts, terms, NDAs, and risks with redlines (`evolsb/claude-legal-skill`) | `contract-risk-review` | `contract-risk-review/SKILL.md` |
| Automate multi-format content production (`alirezarezvani/claude-skills`) | `content-production-pipeline` | `content-production-pipeline/SKILL.md` |
| Draft refund, cancellation, or billing-dispute requests | `refund-request-drafter` | `refund-request-drafter/SKILL.md` |
| Turn meeting notes or call transcripts into a proposal, SOW, or draft contract | `meeting-to-proposal` | `meeting-to-proposal/SKILL.md` |
| Practice a language with SM-2 spaced repetition or build a language app (`m98/fluent`) | `fluent-language-tutor` | `fluent-language-tutor/SKILL.md` |
| Export Claude chats (`agarwalvishal/claude-chat-exporter`) & build an insights dashboard | `chat-insights-dashboard` | `chat-insights-dashboard/SKILL.md` |
| Build an interactive 3D assembly or product manual (`yunongLiu1/IKEA-Manuals-at-Work`) | `interactive-3d-manual` | `interactive-3d-manual/SKILL.md` |
| Catalog owned clothes and generate daily/trip outfits | `wardrobe-outfit-planner` | `wardrobe-outfit-planner/SKILL.md` |
| Sort travel or family photos by EXIF date/location (`ComposioHQ/awesome-claude-skills`) | `photo-library-organizer` | `photo-library-organizer/SKILL.md` |
| Safe read-only triage for corrupted drives or deleted partitions (`ddrescue`/`testdisk`) | `data-recovery-triage` | `data-recovery-triage/SKILL.md` |
| Research last 30 days across Reddit, X, YouTube, HN, Polymarket (`mvanhorn/last30days-skill`) | `last30days` | `last30days/SKILL.md` |
| Build a local web or batch photo-editing app | `photo-editor-builder` | `photo-editor-builder/SKILL.md` |
| Turn Apple Health / wearable exports into meal & fitness insights dashboards | `health-fitness-insights` | `health-fitness-insights/SKILL.md` |
| Transcribe, search, and clip long podcasts/videos with Whisper and `ffmpeg` | `podcast-clipper-search` | `podcast-clipper-search/SKILL.md` |
| Prospect research, personalized outreach, call prep, and sales pipeline workflows | `sales-engine-workflow` | `sales-engine-workflow/SKILL.md` |
| Free macOS disk space (`daymade/claude-code-skills`) or clean Google Drive storage | `disk-and-drive-cleaner` | `disk-and-drive-cleaner/SKILL.md` |
| Turn an old monitor, tablet, or phone into an ambient home kiosk display | `ambient-home-display` | `ambient-home-display/SKILL.md` |
| Scrape JS-rendered webpages/SPAs locally into Markdown/JSON (`crwl`) | `crawl4ai-website-reader` | `crawl4ai-website-reader/SKILL.md` |
| Extract Markdown, metadata, or site link trees via Deepcrawl Worker/API | `deepcrawl-website-reader` | `deepcrawl-website-reader/SKILL.md` |

### 3. Load Only the Selected Skill(s)

- Read the matched `SKILL.md` (or `.md`) file in full before running commands.
- Never preload every `SKILL.md` in the folder at once; load only the skill(s) needed for the active request.
- If a newly added skill is not in the table above, read its YAML frontmatter (`name` and `description`) to decide if it fits.

### 4. Execute or Chain Workflows

- **Single-skill task**: Follow the assigned skill's Steps and Gotchas directly.
- **Multi-skill chain**: Execute the upstream skill first, pass its verified output to the downstream skill, and preserve source citations and safety constraints across steps.
- **No match**: If no installed skill fits, handle the request with standard tools or offer to create a new skill.

### 5. Resolve Overlapping Requests

Several skills look similar. Use these rules before loading one:

- **Website reading**: `crawl4ai-website-reader` for JS-rendered pages and local runs; `deepcrawl-website-reader` only when the user runs a Deepcrawl Worker or API; `last30days` when the user wants what people said recently, not the page itself.
- **Contracts**: `contract-risk-review` for risk analysis and redlines; `meeting-to-proposal` when the user wants a new proposal or SOW written from notes; `refund-request-drafter` for money owed back on a purchase.
- **Sales**: `sales-engine-workflow` for prospects, outreach, and pipeline; `meeting-to-proposal` once a deal has reached proposal stage.
- **Audio/video**: `podcast-clipper-search` for transcribing and cutting recordings; `content-production-pipeline` for writing articles or posts from a transcript that already exists.
- **Photos**: `photo-library-organizer` for sorting and deduplicating files; `photo-editor-builder` for building an editing app.
- **Storage**: `disk-and-drive-cleaner` for freeing space you can delete safely; `data-recovery-triage` when a drive is failing or files are lost.

If the request still fits two skills after these rules, ask one brief question.

## Gotchas

- **Avoid context bloat**: Inspect directory names/frontmatter first, then load only the matched skill.
- **Respect safety gates**: Never bypass confirmation gates inside downstream skills (such as `disk-and-drive-cleaner`, `data-recovery-triage`, `whatsapp-claude-channel`, or `refund-request-drafter`).
- **Clarify ambiguous intent**: If a request could plausibly map to two different skills, ask one brief question before executing heavy steps.
- **Deepcrawl path**: The Deepcrawl skill lives at `deepcrawl-website-reader/SKILL.md`. Read it from that folder.
