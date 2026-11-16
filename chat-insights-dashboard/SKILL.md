---
name: chat-insights-dashboard
description: Export Claude.ai chats with agarwalvishal/claude-chat-exporter and turn chat logs (Markdown/JSON) into an interactive local insights dashboard. Use when the user asks to export Claude chats, analyze conversation history, or build a dashboard from chat data.
allowed-tools: client
---
# Chat Insights Dashboard

Export conversations cleanly with [agarwalvishal/claude-chat-exporter](https://github.com/agarwalvishal/claude-chat-exporter) and transform exported Markdown or JSON chat logs into an interactive local analytics dashboard.

## When to Use

- The user wants to export Claude.ai conversations (including artifacts, tables, math, and attachments) to Markdown.
- The user wants to analyze chat logs (topics, message counts, time patterns, response lengths, recurring themes).
- The user asks to build an HTML/JS insights dashboard from exported chat data.

## Steps

### 1. Export Claude.ai Chats (If Needed)

To export a conversation locally in the browser with `agarwalvishal/claude-chat-exporter` (runs client-side, no server):

1. Open the conversation on `claude.ai`.
2. Open the browser Developer Console (`Cmd+Option+J` on Mac Chrome/Edge, `Ctrl+Shift+J` on Windows/Linux).
3. Paste `claude-chat-exporter.js` from the repo (type `allow pasting` first if prompted) and press Enter to download `{conversation-title}.md`.

### 2. Parse the Exported Chat Files

Write a local Python script to parse exported Markdown (`## Human` / `## Claude` turns and YAML frontmatter) or JSON exports into a clean summary dataset:

- Total conversations, turns per conversation, word/character counts, and timestamps.
- Top recurring topics, tools/languages mentioned, and time-of-day / day-of-week activity.

### 3. Generate a Local Interactive Dashboard

Build a self-contained HTML dashboard (for example, `chat_dashboard.html` using Chart.js or SVG) with:

- KPI summary cards (total chats, turns, words, average length).
- Activity timeline and topic/category breakdown charts.
- Searchable/filterable table of conversations with key takeaways.

## Gotchas

- **Active branch only**: `claude-chat-exporter` exports the currently visible branch of a regenerated message; switch branches in the UI first if you want a different version.
- **Privacy**: Chat exports can contain sensitive personal or work data; process everything locally and never upload user chat logs to external servers.
- **Large exports**: Aggregate metrics in Python before embedding JSON into the HTML dashboard so the browser stays fast.
