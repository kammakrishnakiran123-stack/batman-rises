#!/usr/bin/env python3
"""Lint a content draft against channel limits (standard library).

Draft conventions (Markdown):
  - X posts: separate posts with a line containing only '---'.
  - LinkedIn: a section headed '## LinkedIn'. The hook is its first ~200 characters.
  - Newsletter: a line starting 'Subject:'.

Usage:
  channel_lint.py draft.md

Exit code 1 if a hard limit is broken (X over 280 characters). Warnings do not fail.
"""
import re
import sys
from pathlib import Path

X_LIMIT = 280
LINKEDIN_HOOK = 200
SUBJECT_LIMIT = 60


def lint(text: str):
    errors, warnings = [], []

    x_section = re.split(r"^## LinkedIn\s*$", text, maxsplit=1, flags=re.MULTILINE)[0]
    posts = [p.strip() for p in re.split(r"^---\s*$", x_section, flags=re.MULTILINE) if p.strip()]
    posts = [p for p in posts if not p.startswith("#") and not p.lower().startswith("subject:")]
    for n, post in enumerate(posts, 1):
        if len(post) > X_LIMIT:
            errors.append(f"X post {n}: {len(post)} characters (limit {X_LIMIT})")
    if len(posts) > 8:
        warnings.append(f"X thread has {len(posts)} posts; 3-8 is the usual range")

    li = re.search(r"^## LinkedIn\s*$\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if li:
        body = li.group(1).strip()
        if not body:
            warnings.append("LinkedIn section is empty")
        elif len(body.split("\n", 1)[0]) > LINKEDIN_HOOK:
            warnings.append(f"LinkedIn first line is {len(body.split(chr(10), 1)[0])} characters; "
                            f"hook should fit in about {LINKEDIN_HOOK} before 'see more'")

    subj = re.search(r"^Subject:\s*(.+)$", text, flags=re.MULTILINE)
    if subj and len(subj.group(1).strip()) > SUBJECT_LIMIT:
        warnings.append(f"Newsletter subject is {len(subj.group(1).strip())} characters; aim for {SUBJECT_LIMIT} or fewer")

    if re.search(r"\bhttps?://\S*(example\.com|\[insert|\bTODO\b)", text, flags=re.IGNORECASE):
        errors.append("Draft still contains a placeholder URL or TODO; verify every link before publishing")
    return errors, warnings, len(posts)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    errors, warnings, n_posts = lint(path.read_text(encoding="utf-8"))
    for e in errors:
        print("ERROR  " + e)
    for w in warnings:
        print("WARN   " + w)
    print(f"{n_posts} X post(s) checked: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
