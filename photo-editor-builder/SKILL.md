---
name: photo-editor-builder
description: Build a local web or desktop photo-editing app with crop, resize, exposure/color adjustments, filters, batch presets, and EXIF stripping. Use when the user asks to create a photo editor app, build an image-editing UI, or batch-process photos with custom filters.
allowed-tools: client
---
# Photo Editor Builder

Design and build a fast, privacy-first local photo-editing web app (HTML5 Canvas / WebGL) or batch-processing tool (Python Pillow / Node Sharp).

## When to Use

- The user wants to build a custom photo-editing web app or desktop tool with Claude.
- The user wants interactive controls for exposure, contrast, saturation, temperature, crop/rotate, presets, or before/after comparison.
- The user wants batch resizing, watermarking, or EXIF stripping.

## Steps

### 1. Clarify Scope and Stack

Confirm the target format (default to a zero-backend local HTML5 Canvas/WebGL app if unspecified):

- **Interactive web editor**: Single-page HTML/CSS/JS using Canvas 2D / WebGL shaders (runs locally in browser, no uploads).
- **Batch CLI/script**: Python (`Pillow`, `pillow-heif`) or Node.js (`sharp`) for automated folder processing.

### 2. Implement Core Editing Pipeline

Build a non-destructive adjustment pipeline (store original image + parameter state, render preview on change):

- **Transform**: Aspect-ratio crop, 90-degree rotate, straighten, flip, and resize.
- **Tone & Color**: Brightness, exposure, contrast, highlights/shadows, saturation, vibrance, and warmth/tint.
- **Presets & UX**: Undo/redo history stack, hold-to-compare before/after toggle, and 3-5 clean starter presets.
- **Export**: Download as PNG/JPEG/WebP with quality slider and optional EXIF metadata strip.

### 3. Verify Rendering and Performance

- Test with high-resolution images (downsample preview to viewport size for 60fps sliders, apply full-res pipeline on export).

## Gotchas

- **Full-res lag**: Running pixel loops on a 24MP image on every slider drag freezes the UI; render a proxy preview (~1600px max edge) during edits and run full-res on export.
- **Color space & EXIF orientation**: Respect EXIF orientation tags when loading JPEG/HEIC files so portrait photos don't load sideways.
- **CORS on local files**: Use `FileReader` / `URL.createObjectURL` for drag-and-drop local files so the app works directly via `file://` or `localhost`.
