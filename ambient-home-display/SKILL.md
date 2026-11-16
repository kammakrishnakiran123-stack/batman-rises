---
name: ambient-home-display
description: Turn an old monitor, tablet, or spare phone into a full-screen ambient home dashboard displaying clock, weather, calendar, transit, or home status. Use when the user asks to repurpose an old monitor/tablet/phone as a wall display, smart home dashboard, or kiosk screen.
allowed-tools: client
---
# Ambient Home Display

Build a clean, distraction-free, full-screen web dashboard designed to run 24/7 on an old monitor, iPad/Android tablet, or spare smartphone.

## When to Use

- The user wants to repurpose an old phone, tablet, or monitor into a wall/desk home display.
- The user wants a kiosk dashboard showing time, weather, calendar agenda, transit, stocks/crypto, or Home Assistant status.

## Steps

### 1. Confirm Hardware & Widgets

Check only what's needed:

- Target screen orientation/resolution (portrait phone, tablet, 1080p/4K monitor) and how it will be hosted (local `index.html` or lightweight local server).
- Desired widgets (clock/date, local weather, today's calendar/tasks, transit arrivals, photo frame, or Home Assistant entities).

### 2. Build the Kiosk Dashboard

Create a responsive, zero-clutter web app (`index.html` + CSS/JS) with:

- **High-contrast, glanceable typography** readable from across the room.
- **Auto-refresh & resilience**: Periodic data refresh with graceful offline/error fallback so stale data is clearly marked instead of crashing.
- **Day/Night auto-dimming**: Automatic dark/low-brightness mode at night (for example, 22:00-07:00) and subtle pixel shift if running on an OLED screen.
- **Zero-scroll layout**: Grid sized to `100vw x 100vh` with kiosk/fullscreen support.

### 3. Provide Device Kiosk Setup Tips

- **Old monitor + Pi/Mac/PC**: Launch Chrome/Chromium with `--kiosk http://localhost:<port>` and disable screen sleep.
- **Old tablet/phone**: Add to Home Screen (PWA/fullscreen) and enable Guided Access (iOS) or Screen Pinning / Fully Kiosk Browser (Android).

## Gotchas

- **API keys in client JS**: Keep any private API tokens (like Home Assistant or calendar tokens) in a local backend proxy rather than hardcoding them in public HTML.
- **OLED burn-in**: On old OLED phones/tablets, use dark backgrounds, low brightness, and slight periodic layout shifts.
- **CORS on `file://`**: Serve the dashboard via a tiny local server (`python3 -m http.server`) rather than `file://` if fetching live APIs.
