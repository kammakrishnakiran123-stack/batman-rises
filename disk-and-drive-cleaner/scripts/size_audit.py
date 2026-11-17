#!/usr/bin/env python3
"""Read-only disk usage audit with safety tiers. It never deletes or modifies anything.

Usage:
  size_audit.py PATH [--top 20] [--md report.md]

Each top-level child of PATH is sized and tagged:
  SAFE_TO_CLEAR   rebuildable caches and Trash
  REVIEW_FIRST    large user data a person should look at (Downloads, DerivedData, Docker, node_modules)
  DO_NOT_TOUCH    system and app-state locations
  ASK_USER        anything unrecognized: the user decides
Tags come from path names only. Always confirm with the user before any deletion.
"""
import argparse
import os
import sys
from pathlib import Path

# Each key is a sequence of whole path components, matched in order (not substrings).
TIERS = [
    ("SAFE_TO_CLEAR", [("library", "caches"), ("caches",), (".trash",), ("trash",), (".npm",),
                       (".cache", "pip"), ("library", "caches", "homebrew")]),
    ("REVIEW_FIRST", [("downloads",), ("library", "developer", "xcode", "deriveddata"),
                      ("docker",), ("node_modules",), ("backups",)]),
    ("DO_NOT_TOUCH", [("library", "keychains"), ("library", "application support"),
                      ("system",), ("applications",)]),
]


def _contains_sequence(parts, seq):
    n = len(seq)
    return any(tuple(parts[i:i + n]) == seq for i in range(len(parts) - n + 1))


def tier_for(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    for tier, keys in TIERS:
        if any(_contains_sequence(parts, k) for k in keys):
            return tier
    return "ASK_USER"  # unknown: needs the user to decide


def dir_size(root: Path) -> int:
    total = 0
    for dirpath, _dirs, files in os.walk(root, onerror=lambda e: None, followlinks=False):
        for name in files:
            try:
                total += os.lstat(os.path.join(dirpath, name)).st_size
            except OSError:
                pass
    return total


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--md", type=Path, default=None)
    args = ap.parse_args()
    if not args.path.is_dir():
        sys.exit(f"Not a folder: {args.path}")

    # Size two levels deep so Library/Caches shows up on its own, not hidden inside Library.
    rows = []
    for child in args.path.iterdir():
        if child.is_symlink():
            continue
        if child.is_dir():
            rows.append((dir_size(child), child, tier_for(child)))
            for grand in child.iterdir():
                if grand.is_dir() and not grand.is_symlink():
                    rows.append((dir_size(grand), grand, tier_for(grand)))
        elif child.is_file():
            rows.append((child.lstat().st_size, child, tier_for(child)))
    rows.sort(reverse=True)

    lines = [f"# Disk audit: {args.path}", "", "| Size | Tier | Path |", "|---|---|---|"]
    for size, path, tier in rows[: args.top]:
        lines.append(f"| {human(size)} | {tier} | {path} |")
    totals = {}
    top_level = [r for r in rows if r[1].parent == args.path or r[1].parent.parent == args.path]
    for size, p_, tier in top_level:
        if p_.parent == args.path:
            totals[tier] = totals.get(tier, 0) + size
    lines += ["", "Totals by tier:"] + [f"- {t}: {human(s)}" for t, s in sorted(totals.items())]
    lines += ["", "Nothing was deleted. Confirm each category with the user before any cleanup."]
    report = "\n".join(lines)
    print(report)
    if args.md:
        args.md.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
