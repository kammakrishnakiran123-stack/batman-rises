---
name: lemo-opuscar
description: Create code-generated short films and custom visual styles using lemomo-ai/lemo-opuscar (99 ready-to-use film styles across 15 categories). Use when the user asks to make a code-generated film, render an animated explainer with Canvas/WebGL and ffmpeg, use a Lemo-Opuscar style, or create a custom film style in Claude Code.
allowed-tools: client
---
# Lemo-Opuscar

Direct, draw, score, and mix short films entirely in code (Canvas/WebGL frame-by-frame capture + TTS narration + original score + ffmpeg muxing, with no video-generation model) using [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar).

## When to Use

- The user asks to create a short film, explainer, launch video, or music video in code using Lemo-Opuscar or one of its 99 styles.
- The user wants to customize a library style or build a new reusable film style under `~/lemo-my-styles/`.
- The user wants to install, update, or troubleshoot the `lemo-opuscar` Claude Code plugin.

## Steps

### 1. Check Installation and Prerequisites

Verify Node.js (`20+`), `ffmpeg` (`7+`), and Python (`3.11+` or `uv`):

```bash
node -v && ffmpeg -version | head -n 1 && python3 --version
```

If `lemo-opuscar` is not installed yet, install the Claude Code plugin (downloads guides, tools, and style prompts to `~/lemo-opuscar` on first run):

```bash
claude plugin marketplace add lemomo-ai/lemo-opuscar
claude plugin install lemo-opuscar@lemolab
```

To update later:

```bash
claude plugin marketplace update lemolab && claude plugin update lemo-opuscar@lemolab
```

Or clone the repo directly (films are created inside `films/<name>/`):

```bash
git clone https://github.com/lemomo-ai/lemo-opuscar.git
```

### 2. Gather Film Inputs Once Up Front

Before writing code, clarify only what cannot be inferred:

- **Topic and style**: Pick one of the 99 library styles across 15 categories (for example, `Swiss Motion Graphics`, `Watercolor Brush`, `Blueprint`, `Ukiyo-e`, `80s Cel Anime`, `Neon Tubes`) or a saved custom style in `~/lemo-my-styles/`.
- **Duration and format**: Default is `1920x1080` at `24 fps` (some styles use `30 fps`); switch to `1080x1920` or `1080x1440` for vertical feeds.
- **Assets**: Ask if the user has their own voiceover, music, photos, or data to include, and whether they want to review a storyboard first.

### 3. Follow the Studio Guides

Read the core guides from `~/lemo-opuscar/` (or the cloned repo) before building scenes:

- `DIRECTOR.md` for story, rhythm, camera, sound, and self-checks.
- `TECHNIQUE.md` for frame-by-frame headless browser rendering, TTS (local Kokoro for English; Edge TTS for Chinese), music, and `ffmpeg` mixing.
- `styles/<style>/STYLE.md` for the chosen visual and audio grammar.

### 4. Customize or Create a Style (`MY-STYLES.md`)

When the user wants to adapt a library style or start from a blank page:

- Follow `MY-STYLES.md` to plan changes one question at a time (platform/aspect ratio, palette, typography, pace, signature moves, and name).
- Render one style frame side-by-side (original left, custom right) before rendering a 15-30s demo film.
- Save approved custom styles to `~/lemo-my-styles/<name>/` so updates never overwrite them.

## Gotchas

- **Ubuntu ffmpeg version**: Ubuntu 24.04 ships `ffmpeg 6.1`, which is too old. Install a static `ffmpeg 7+` build.
- **Image-generator styles**: Three styles (`Manga Panels`, `Text Flash Cuts`, `Comic History Cartoon`) require an external image generator; all other 96 styles render purely in code.
- **Model effort**: Lemo-Opuscar styles are tuned for Claude with `/effort high`; other models or lower effort settings may degrade visual fidelity.
- **Time and token budget**: A full film takes roughly 30-60 minutes of agent execution. Check visual frames and audio mix before final delivery.
