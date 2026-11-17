#!/usr/bin/env python3
"""List the commercial and scope details missing from meeting notes before a proposal is drafted.

Usage:
  proposal_gaps.py notes.md

Checks for the terms the SKILL.md template needs. It reports what is missing and never
invents a value. Each check is a keyword test, so confirm the result by reading the notes.
"""
import re
import sys
from pathlib import Path

CHECKS = [
    ("Pricing or budget", r"(\$|₹|€|£|usd|inr|eur|gbp)\s?\d|\b\d[\d,]*\s?(rs|usd|inr|per month|/month|per hour|/hr)\b|\b(price|fee|cost|budget|rate|quote)\b[^.\n]{0,30}\d"),
    ("Payment schedule", r"\bnet\s?\d+\b|upfront|milestone|advance payment|invoice|retainer|50%|deposit"),
    ("Start or end dates", r"\b(20\d\d-\d\d-\d\d|(january|february|march|april|june|july|august|september|october|november|december)\b|\bmay \d{1,2}\b)|\bdeadline\b|\bby (mon|tue|wed|thu|fri)"),
    ("Timeline or phases", r"\bweeks?\b|\bmonths?\b|\bsprint\b|\bphase\b|\bmilestone\b"),
    ("Deliverables", r"\bdeliver\w*|\bwill (provide|build|create|produce)\b"),
    ("Out of scope", r"out of scope|not included|excluded|won'?t (do|include)"),
    ("Client decision maker", r"\b(approve|sign(off| off)?|decision maker|final say)\b"),
    ("Client-provided assets", r"\b(client|customer) (will )?(provide|share|supply)\b|dependenc"),
]


def gaps(text: str):
    return [label for label, pattern in CHECKS if not re.search(pattern, text, re.IGNORECASE)]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    missing = gaps(text)
    if not missing:
        print("All checked terms appear in the notes. Still confirm them before drafting.")
        return
    print("Missing or unclear, ask the user before drafting:")
    for label in missing:
        print(f"- {label}")
    print("\nDo not invent these values. Leave a clearly marked gap in the draft.")


if __name__ == "__main__":
    main()
