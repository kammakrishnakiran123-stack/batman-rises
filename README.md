# Batman Rises

A modular collection of Claude skills and a central orchestrator (`skill-router`) covering reverse engineering, code-generated films, smart TV customization, 30-day multi-source research, contract review, productivity, media pipelines, and local utilities.

## Central Orchestrator

- [`skill-router`](./skill-router/SKILL.md) - Inspects incoming requests, selects the matching skill(s), and loads only the required instructions on demand.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `ambient-home-display` | Turn an old monitor, tablet, or spare phone into a full-screen ambient home dashboard |
| `chat-insights-dashboard` | Export Claude.ai chats and build an interactive local insights dashboard |
| `content-production-pipeline` | Multi-format content research, drafting, repurposing, and editorial QA |
| `contract-risk-review` | Clause-by-clause contract, NDA, and terms risk review with suggested redlines |
| `crawl4ai-website-reader` | Local JS/SPA webpage scraping to clean Markdown or JSON via Crawl4AI |
| `data-recovery-triage` | Safe, read-only drive imaging and recovery triage (`ddrescue`, `testdisk`, `photorec`) |
| `deepcrawl-website-reader` | Edge Markdown, metadata, and link-tree extraction via Deepcrawl |
| `disk-and-drive-cleaner` | Safe macOS disk and Google Drive storage audit with user-confirmed cleanup |
| `fluent-language-tutor` | SM-2 spaced-repetition language tutoring and practice workflows |
| `free-my-tv` | Ad-free home screen setup and customization for Google TV, LG webOS, and Samsung Tizen |
| `health-fitness-insights` | Local Apple Health / wearable export analysis and trend dashboards |
| `interactive-3d-manual` | Browser-based Three.js/WebGL 3D step-by-step assembly manuals |
| `last30days` | Multi-platform 30-day community research across Reddit, X, YouTube, HN, Polymarket, and the web |
| `lemo-opuscar` | Code-generated short films (Canvas/WebGL + TTS + ffmpeg) across 99 visual styles |
| `meeting-to-proposal` | Convert raw meeting notes or transcripts into structured proposals or SOWs |
| `photo-editor-builder` | Local Canvas/WebGL or batch photo-editing app builder |
| `photo-library-organizer` | Safe EXIF-based photo sorting with dry-run previews and duplicate detection |
| `podcast-clipper-search` | Local Whisper transcription, full-text search, and `ffmpeg` highlight clipping |
| `rea-reverse-engineer` | Local reverse engineering for native binaries, Electron/ASAR, APKs, and network captures |
| `refund-request-drafter` | Policy-grounded refund, cancellation, and billing-dispute message drafting |
| `sales-engine-workflow` | Prospect research, personalized outreach sequences, call prep, and pipeline tracking |
| `wardrobe-outfit-planner` | Owned-wardrobe inventory and weather/occasion outfit planning |
| `whatsapp-claude-channel` | Native WhatsApp channel integration for Claude Code |

## Quick Start

Copy or symlink this folder to `~/.claude/skills` (or point Claude Code to this directory):

```bash
ln -s "$(pwd)" ~/.claude/skills/batman-rises
```
