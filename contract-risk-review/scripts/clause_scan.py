#!/usr/bin/env python3
"""First-pass risk scan of contract text. A triage aid, not legal advice (standard library).

Usage:
  clause_scan.py contract.txt

Finds candidate clauses with line numbers so a reviewer can read them in context.
Pattern matching misses things and flags harmless wording too. Every hit needs a human read,
and any decision needs a qualified lawyer in the relevant jurisdiction.
"""
import re
import sys
from pathlib import Path

RULES = [
    ("High", "Uncapped or unlimited liability",
     r"unlimited liability|uncapped|without (any )?limit(ation)? (of )?liabilit"),
    ("High", "Unilateral right to change terms",
     r"(may|reserves? the right to) (modify|amend|change|update)[^.\n]{0,80}(at any time|without (notice|consent))"),
    ("High", "Assignment of IP to the other party",
     r"hereby assigns?|shall assign to|assigns? to (the )?(company|provider|licensor)"),
    ("High", "Automatic renewal",
     r"automatic(ally)? renew|renews? automatically|auto-?renew|renew(s|al)? (for|automatically)"),
    ("Medium", "Perpetual or irrevocable grant",
     r"perpetual|irrevocable"),
    ("Medium", "Use of your data to train models",
     r"(train|improve)[^.\n]{0,40}(models?|machine learning|AI)"),
    ("Medium", "Non-compete or non-solicit",
     r"non-?compet|non-?solicit"),
    ("Medium", "Indemnity obligation",
     r"indemnif"),
    ("Medium", "Termination restricted or requires long notice",
     r"(terminat\w*)[^.\n]{0,60}(only|solely) (for|upon|in the event)"),
    ("Low", "Late fees or interest",
     r"late (fee|payment charge)|interest at (the )?rate|per annum"),
]


def scan(text: str):
    hits = []
    lines = text.splitlines()
    for severity, label, pattern in RULES:
        rx = re.compile(pattern, re.IGNORECASE)
        for n, line in enumerate(lines, 1):
            if rx.search(line):
                hits.append((severity, label, n, line.strip()[:160]))
    if not re.search(r"governing law|governed by|laws of", text, re.IGNORECASE):
        hits.append(("Medium", "No governing-law clause found", 0, "Search the whole document to confirm"))
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(hits, key=lambda h: (order[h[0]], h[2]))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    hits = scan(text)
    if not hits:
        print("No candidate clauses matched. Still read the full document.")
        return
    print("| Risk | Issue | Line | Text |")
    print("|---|---|---|---|")
    for severity, label, n, snippet in hits:
        where = str(n) if n else "-"
        print(f"| {severity} | {label} | {where} | {snippet} |")
    print("\nAnalytical aid only. Not legal advice; have a qualified lawyer review before signing.")


if __name__ == "__main__":
    main()
