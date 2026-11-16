---
name: interactive-3d-manual
description: Build interactive 3D step-by-step assembly or product manuals in the browser using Three.js/WebGL with part highlighting, exploded views, and step controls (informed by yunongLiu1/IKEA-Manuals-at-Work). Use when the user asks to create a 3D manual, interactive assembly guide, or exploded-view product walkthrough.
allowed-tools: client
---
# Interactive 3D Manual

Build a browser-based interactive 3D assembly or product manual using Three.js/WebGL with step-by-step animations, part highlighting, orbit controls, and exploded views, informed by 3D grounding patterns from [yunongLiu1/IKEA-Manuals-at-Work](https://github.com/yunongLiu1/IKEA-Manuals-at-Work).

## When to Use

- The user wants an interactive 3D assembly manual, repair guide, or exploded-view diagram.
- The user provides a 3D model (`.glb`/`.gltf`/`.obj`) or product specs and wants step-synchronized instructions.
- The user wants a standalone HTML/JS 3D viewer with next/previous step controls and part callouts.

## Steps

### 1. Define Parts and Assembly Sequence

- List every component (ID, name, quantity, fastener type) and group them into ordered assembly steps.
- If a `.glb`/`.gltf` model is provided, inspect mesh names so each step maps cleanly to exact 3D parts.
- If no 3D model is provided, compose clean parametric Three.js geometry (or procedural parts) with distinct materials.

### 2. Build the Three.js Interactive Viewer

Create a self-contained web app (`index.html` + JS/CSS) featuring:

- **3D Viewport**: `OrbitControls`, soft studio lighting, and smooth camera transitions focusing on the active step's parts.
- **Step Synchronization**: Next/Prev buttons, step slider, part highlight/glow, and animated part-insertion paths.
- **Exploded View & X-Ray**: Toggle to separate parts along assembly axes or dim already-assembled components.
- **Parts List Sidebar**: Clickable BOM (Bill of Materials) that highlights the corresponding part in 3D.

### 3. Verify Usability

- Test in a local browser (`python3 -m http.server`) and verify every step transitions smoothly without overlapping geometry or missing labels.

## Gotchas

- **Self-contained assets**: Load Three.js from a pinned CDN or local bundle and avoid external textures that fail offline or hit CORS blocks.
- **Mobile/touch support**: Enable touch orbit/pinch zoom so the manual works on tablets and phones at the workbench.
- **Clear orientation**: Keep a subtle ground grid or orientation gizmo so users don't lose track of front/back while rotating.
