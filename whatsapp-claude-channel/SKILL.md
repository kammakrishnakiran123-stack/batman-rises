---
name: whatsapp-claude-channel
description: Connect WhatsApp to Claude Code using rich627/whatsapp-claude-plugin to send and receive messages, transcribe voice notes, and approve tools remotely. Use when the user asks to message on WhatsApp via Claude, set up the WhatsApp channel plugin, or control Claude Code from WhatsApp.
allowed-tools: client
---
# WhatsApp Claude Channel

Connect WhatsApp directly to a Claude Code session as a native channel using [Rich627/whatsapp-claude-plugin](https://github.com/rich627/whatsapp-claude-plugin) with no API keys or Docker required.

## When to Use

- The user wants to send, read, or reply to WhatsApp messages through Claude Code.
- The user wants to install or troubleshoot `Rich627/whatsapp-claude-plugin`.
- The user wants voice-note transcription, remote tool approval, or access control over WhatsApp.

## Steps

### 1. Install the Plugin in Claude Code

Inside a Claude Code session, add the marketplace and install the plugin:

```bash
/plugin marketplace add Rich627/whatsapp-claude-plugin
/plugin install whatsapp@whatsapp-claude-plugin
```

### 2. Launch Claude Code with the WhatsApp Channel

Start Claude Code with the WhatsApp channel enabled and link your device when prompted:

```bash
claude --channels plugin:whatsapp@whatsapp-claude-plugin
```

### 3. Configure Access Control and Messaging

- Review `ACCESS.md` and `USAGE.md` in the plugin repo before allowing external contacts or group chats.
- Restrict allowed numbers/groups so unauthorized senders cannot trigger tool calls on your machine.
- Use voice notes or text prompts in the linked chat; confirm any sensitive tool approvals before executing.

## Gotchas

- **Access control first**: Never leave channel access open to unknown numbers or public groups, since incoming messages can invoke Claude Code tools.
- **Linked-device session**: Because it uses Baileys (WhatsApp Web protocol), keep your phone's WhatsApp linked-devices session active and avoid violating WhatsApp's spam/automation policies.
- **Confirm before sending**: Always confirm the recipient and message text before sending outbound WhatsApp messages to real contacts.
