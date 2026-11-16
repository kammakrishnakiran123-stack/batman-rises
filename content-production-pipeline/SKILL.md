---
name: content-production-pipeline
description: Automate end-to-end content production from research and outlining to multi-format drafting, repurposing, and editorial QA (compatible with alirezarezvani/claude-skills). Use when the user asks to build a content pipeline, repurpose one piece into blogs/social/newsletters, or automate content creation.
allowed-tools: client
---
# Content Production Pipeline

Turn a topic, source document, or transcript into a complete multi-channel content package (outline, long-form article, social threads, newsletter, and QA checklist), optionally paired with [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).

## When to Use

- The user wants to automate recurring content production (blog posts, LinkedIn/X threads, newsletters, video scripts).
- The user wants to repurpose one source asset (podcast, article, product release) into multiple formats.
- The user wants to install or use marketing/content skills from `alirezarezvani/claude-skills`.

## Steps

### 1. Optional: Install `alirezarezvani/claude-skills`

If the user wants the broader Claude Code skills collection:

```bash
# In Claude Code:
/plugin marketplace add alirezarezvani/claude-skills
```

### 2. Lock Brief Parameters Up Front

Confirm or infer from context:

- **Audience & Goal**: Who is reading and what action should they take?
- **Voice & Constraints**: Tone (technical, conversational, executive), word count, and words/claims to avoid.
- **Target Formats**: Article/blog, X/LinkedIn posts, newsletter, or script.

### 3. Execute the 4-Stage Pipeline

1. **Angle & Outline**: Propose 2-3 sharp angles with a hook, key proof points, and structure.
2. **Core Draft**: Write the primary long-form piece with concrete examples, zero filler, and source links for every external claim.
3. **Repurpose Pack**: Derive platform-native variants (short-form hooks, thread/carousel bullets, newsletter blurb) without copy-pasting the same sentences. Apply these channel limits:
   - **X post**: 280 characters or fewer. A thread is 3-8 posts, each able to stand alone.
   - **LinkedIn post**: put the hook in the first ~200 characters, since that is what shows before "see more".
   - **Newsletter**: subject line of about 60 characters or fewer, one call to action.
   - **Blog/article**: one H1, scannable H2s, and a summary paragraph at the top.
4. **Editorial QA**: Check for factual accuracy, active voice, scannable headings, and CTA clarity.

## Scripts

`scripts/channel_lint.py` checks a draft against the channel limits above. X posts are separated by a line containing only `---`. LinkedIn goes under a `## LinkedIn` heading. The newsletter subject is a line starting `Subject:`.

```bash
python3 scripts/channel_lint.py draft.md
```

## Gotchas

- **Avoid generic AI prose**: Strip buzzwords and vague openings; lead with concrete specifics or a real problem.
- **Verify facts and links**: Never invent statistics, quotes, or URLs during content generation.
- **Platform fit**: Adapt length and formatting per channel rather than truncating one long post.
