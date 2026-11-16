#!/usr/bin/env python3
"""Build an offline insights dashboard from exported chat Markdown files.

Expected turn format (as written by the chat exporter):
    ## Human
    message text
    ## Claude
    reply text
Optional YAML-style frontmatter lines `title:` and `date:` (YYYY-MM-DD) are used when present.

Usage:
  chat_insights.py EXPORT_DIR OUT_DIR

Writes OUT_DIR/stats.json and OUT_DIR/dashboard.html (self-contained, no network calls).
Only aggregated numbers and the conversation titles go into the HTML.
"""
import argparse
import html
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

TURN = re.compile(r"^## (Human|Claude)\s*$", re.MULTILINE)
STOPWORDS = set("""a an and are as at be but by can do for from has have how i if in is it its
just me my not of on or our so that the their them then there these they this to up us was we
what when which who will with would you your about into more also get make like need want
use using one new out all any some than been were had here where why does did im dont
""".split())


def parse_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    title, when = path.stem, None
    front = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if front:
        for line in front.group(1).splitlines():
            key, _, value = line.partition(":")
            if key.strip() == "title" and value.strip():
                title = value.strip().strip('"')
            elif key.strip() == "date":
                try:
                    when = date.fromisoformat(value.strip()[:10])
                except ValueError:
                    pass
        text = text[front.end():]
    turns = []
    matches = list(TURN.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        turns.append((m.group(1), text[m.end():end].strip()))
    return {"title": title, "date": when, "turns": turns}


def words(text):
    return [w for w in re.findall(r"[a-zA-Z][a-zA-Z'-]{2,}", text.lower()) if w not in STOPWORDS]


def summarize(convs):
    human_words = claude_words = 0
    topics = Counter()
    by_month = Counter()
    per_conv = []
    for c in convs:
        h = [t for role, t in c["turns"] if role == "Human"]
        k = [t for role, t in c["turns"] if role == "Claude"]
        hw = sum(len(t.split()) for t in h)
        kw = sum(len(t.split()) for t in k)
        human_words += hw
        claude_words += kw
        for t in h:
            topics.update(words(t))
        if c["date"]:
            by_month[c["date"].strftime("%Y-%m")] += 1
        per_conv.append({"title": c["title"], "date": c["date"].isoformat() if c["date"] else None,
                         "turns": len(c["turns"]), "human_words": hw, "claude_words": kw})
    n = len(convs)
    total_turns = sum(len(c["turns"]) for c in convs)
    return {
        "conversations": n,
        "turns": total_turns,
        "human_words": human_words,
        "claude_words": claude_words,
        "avg_turns_per_conversation": round(total_turns / n, 1) if n else 0,
        "top_topics": topics.most_common(15),
        "conversations_by_month": dict(sorted(by_month.items())),
        "per_conversation": sorted(per_conv, key=lambda r: r["turns"], reverse=True),
    }


def bar_chart(data: dict) -> str:
    if not data:
        return "<p>No dated conversations found.</p>"
    width, height, pad = 640, 220, 30
    peak = max(data.values())
    step = (width - 2 * pad) / len(data)
    bars = []
    for i, (label, value) in enumerate(data.items()):
        h = (value / peak) * (height - 2 * pad)
        x = pad + i * step + step * 0.15
        y = height - pad - h
        bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{step * 0.7:.1f}" height="{h:.1f}" fill="#4f7cff"/>'
                    f'<text x="{x + step * 0.35:.1f}" y="{height - 10}" font-size="10" text-anchor="middle">{html.escape(label[-2:])}</text>')
    return f'<svg viewBox="0 0 {width} {height}" width="100%">{"".join(bars)}</svg>'


def render(stats: dict) -> str:
    rows = "".join(
        f"<tr><td>{html.escape(r['title'])}</td><td>{r['date'] or '-'}</td>"
        f"<td>{r['turns']}</td><td>{r['human_words']}</td><td>{r['claude_words']}</td></tr>"
        for r in stats["per_conversation"]
    )
    topics = ", ".join(f"{html.escape(w)} ({n})" for w, n in stats["top_topics"]) or "none"
    kpis = [("Conversations", stats["conversations"]), ("Turns", stats["turns"]),
            ("Your words", stats["human_words"]), ("Claude words", stats["claude_words"]),
            ("Avg turns / chat", stats["avg_turns_per_conversation"])]
    cards = "".join(f'<div class="card"><div class="v">{v}</div><div class="k">{k}</div></div>' for k, v in kpis)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Chat insights</title>
<style>
body{{font-family:system-ui,sans-serif;margin:24px;color:#1b1f2a;background:#f7f8fb}}
.cards{{display:flex;gap:12px;flex-wrap:wrap}}
.card{{background:#fff;border-radius:10px;padding:14px 18px;min-width:130px;box-shadow:0 1px 3px #0001}}
.v{{font-size:26px;font-weight:600}} .k{{color:#667;font-size:13px}}
table{{border-collapse:collapse;width:100%;background:#fff;margin-top:16px}}
td,th{{padding:6px 10px;border-bottom:1px solid #eee;text-align:left;font-size:14px}}
input{{padding:6px;width:260px;margin:12px 0}}
</style></head><body>
<h1>Chat insights</h1>
<div class="cards">{cards}</div>
<h3>Conversations by month</h3>{bar_chart(stats["conversations_by_month"])}
<h3>Top topics in your messages</h3><p>{topics}</p>
<h3>Conversations</h3>
<input id="q" placeholder="Filter by title" oninput="filter(this.value)">
<table id="t"><tr><th>Title</th><th>Date</th><th>Turns</th><th>Your words</th><th>Claude words</th></tr>{rows}</table>
<script>
function filter(v){{v=v.toLowerCase();document.querySelectorAll('#t tr').forEach((r,i)=>{{if(i)r.style.display=r.textContent.toLowerCase().includes(v)?'':'none'}})}}
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    files = sorted(args.export_dir.glob("*.md"))
    if not files:
        sys.exit(f"No .md exports found in {args.export_dir}")
    convs = [parse_file(f) for f in files]
    empty = [c["title"] for c in convs if not c["turns"]]
    stats = summarize(convs)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "stats.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")
    (args.out_dir / "dashboard.html").write_text(render(stats), encoding="utf-8")
    print(f"Wrote {args.out_dir}/dashboard.html and stats.json ({stats['conversations']} conversations, {stats['turns']} turns)")
    if empty:
        print(f"Warning: {len(empty)} file(s) had no '## Human' / '## Claude' turns and were counted as empty.")


if __name__ == "__main__":
    main()
