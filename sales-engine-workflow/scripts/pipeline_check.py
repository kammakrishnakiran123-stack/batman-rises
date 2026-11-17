#!/usr/bin/env python3
"""Check a pipeline CSV against the schema in SKILL.md before it goes into a CRM (standard library).

Usage:
  pipeline_check.py pipeline.csv [--today YYYY-MM-DD]

Exit code 1 if any row has a blocking problem. Warnings do not fail the check.
Required columns: account, contact_name, contact_role, trigger_event, source_url,
stage, next_step, next_step_date, owner, priority
"""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

COLUMNS = ["account", "contact_name", "contact_role", "trigger_event", "source_url",
           "stage", "next_step", "next_step_date", "owner", "priority"]
STAGES = {"prospect", "contacted", "discovery", "proposal", "negotiation", "won", "lost"}
PRIORITIES = {"high", "medium", "low", ""}


def check(path: Path, today: date):
    errors, warnings = [], []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [f"header missing columns: {', '.join(missing)}"], [], 0
        rows = list(reader)
    seen = set()
    for n, row in enumerate(rows, start=2):  # line 1 is the header
        key = (row["account"].strip().lower(), row["contact_name"].strip().lower())
        if key in seen:
            warnings.append(f"line {n}: duplicate account + contact")
        seen.add(key)
        if row["trigger_event"].strip() and not row["source_url"].strip():
            errors.append(f"line {n}: trigger_event has no source_url (cannot be used in outreach)")
        if row["stage"].strip().lower() not in STAGES:
            errors.append(f"line {n}: stage '{row['stage']}' is not one of {sorted(STAGES)}")
        if row["priority"].strip().lower() not in PRIORITIES:
            errors.append(f"line {n}: priority must be high, medium, or low")
        if row["next_step_date"].strip():
            try:
                when = date.fromisoformat(row["next_step_date"].strip())
                if when < today and row["stage"].strip().lower() not in ("won", "lost"):
                    warnings.append(f"line {n}: next_step_date {when} is in the past")
            except ValueError:
                errors.append(f"line {n}: next_step_date must be YYYY-MM-DD")
        elif row["stage"].strip().lower() not in ("won", "lost"):
            warnings.append(f"line {n}: no next_step_date")
    return errors, warnings, len(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", type=Path)
    ap.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = ap.parse_args()
    errors, warnings, count = check(args.csv, args.today)
    for line in errors:
        print("ERROR  " + line)
    for line in warnings:
        print("WARN   " + line)
    print(f"{count} row(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
