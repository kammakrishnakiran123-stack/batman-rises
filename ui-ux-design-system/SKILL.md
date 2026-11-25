---
name: ui-ux-design-system
description: Generate tailored UI/UX design systems, color palettes, font pairings, design tokens (DTCG/CSS), and stack-specific frontend rules across 22 frameworks using nextlevelbuilder/ui-ux-pro-max-skill. Use when building or retheming web/mobile UIs, landing pages, dashboards, or installing ui-ux-pro-max in Claude Code.
allowed-tools: client
---
# UI/UX Design System

Generate tailored, industry-appropriate UI/UX design systems—covering landing patterns, visual styles, accessible color palettes, typography pairings, W3C/CSS tokens, and anti-pattern checklists—using [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).

## When to Use

- The user wants to design or build a landing page, SaaS dashboard, e-commerce store, portfolio, or mobile app UI without generic "AI slop" styling.
- The user wants to retheme an existing app (React, Next.js, Tailwind, shadcn/ui, Vue, Svelte, SwiftUI, Flutter, etc.) using semantic design tokens.
- The user wants to install or run `ui-ux-pro-max` / `uipro` CLI in Claude Code, Cursor, Codex, or Gemini CLI.

## Steps

### 1. Optional: Install `nextlevelbuilder/ui-ux-pro-max-skill`

Requires Python 3.x (standard library only for search scripts) or Node.js for the `uipro` CLI:

```bash
# Claude Code marketplace plugin
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

# Or install via CLI (use ui-ux-pro-max-cli, not legacy uipro-cli)
npm install -g ui-ux-pro-max-cli
uipro init --ai claude --global
```

### 2. Generate a Design System or Query Domains

Run the local search engine from the installed skill directory (or follow the same structured criteria if running standalone):

```bash
# Generate full design system + persist MASTER.md and preview.html
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "fintech dashboard" \
  --design-system --persist --preview --tokens css -p "MyApp"

# Domain-specific lookups (style, typography, chart, ux, icons)
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style --json
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
```

### 3. Apply Tokens & Pre-Delivery Checks

- Persist global rules in `design-system/<project>/MASTER.md` and per-page deviations in `pages/<page>.md`.
- Map colors, typography, spacing, and radii to semantic tokens (`background`, `surface`, `foreground`, `primary`, `border`, `ring`) rather than hard-coded hex values.
- Verify before shipping: no emojis as UI icons (use SVG icons like Lucide/Heroicons/Phosphor), >=4.5:1 text contrast, visible keyboard focus states, `prefers-reduced-motion` support, and clean reflow at `375px`, `768px`, `1024px`, and `1440px`.

## Gotchas

- **Use `ui-ux-pro-max-cli`, not `uipro-cli`**: Older `uipro-cli` releases are stale and lack current v2+ templates.
- **Avoid uploading the full repo ZIP to Claude.ai**: The full repository exceeds Claude.ai's 200-file ZIP limit; use `/plugin install` or `uipro init`.
- **Use `--json` for full records**: Human-readable `search.py` output truncates long fields at 300 characters.
