#!/usr/bin/env python3
"""SM-2 spaced-repetition deck stored in a local JSON file (standard library only).

Usage:
  sm2.py DECK.json add "FRONT" "BACK"
  sm2.py DECK.json due [--today YYYY-MM-DD]
  sm2.py DECK.json review ID Q [--today YYYY-MM-DD]     # Q = 0..5 (see grading)
  sm2.py DECK.json list

Grading Q:
  5 perfect, 4 correct after hesitation, 3 correct with real effort,
  2 wrong but the answer felt familiar, 1 wrong, 0 blackout.
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

MIN_EASE = 1.3


def load(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"next_id": 1, "items": []}


def save(path: Path, deck):
    path.write_text(json.dumps(deck, indent=2, ensure_ascii=False), encoding="utf-8")


def sm2_update(item: dict, q: int, today: date) -> dict:
    """Apply one SM-2 review. Pure function: returns a new item, easy to test."""
    if not 0 <= q <= 5:
        raise ValueError("q must be between 0 and 5")
    ef, reps, interval = item["ease_factor"], item["repetitions"], item["interval_days"]
    if q < 3:
        reps, interval = 0, 1
    else:
        reps += 1
        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 6
        else:
            interval = max(1, round(interval * ef))
    ef = max(MIN_EASE, ef + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    return {**item, "ease_factor": round(ef, 4), "repetitions": reps, "interval_days": interval,
            "next_review": (today + timedelta(days=interval)).isoformat(),
            "last_review": today.isoformat()}


def due_items(deck, today: date):
    return [i for i in deck["items"] if date.fromisoformat(i["next_review"]) <= today]


def parse_today(value):
    return date.fromisoformat(value) if value else date.today()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", type=Path)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("front")
    a.add_argument("back")
    d = sub.add_parser("due")
    d.add_argument("--today")
    r = sub.add_parser("review")
    r.add_argument("id", type=int)
    r.add_argument("q", type=int)
    r.add_argument("--today")
    sub.add_parser("list")
    args = ap.parse_args()

    deck = load(args.deck)
    today = parse_today(getattr(args, "today", None))

    if args.cmd == "add":
        item = {"id": deck["next_id"], "front": args.front, "back": args.back,
                "ease_factor": 2.5, "repetitions": 0, "interval_days": 0,
                "next_review": today.isoformat(), "last_review": None}
        deck["items"].append(item)
        deck["next_id"] += 1
        save(args.deck, deck)
        print(f"Added card {item['id']}")
    elif args.cmd == "due":
        items = due_items(deck, today)
        for i in items:
            print(f"[{i['id']}] {i['front']}")
        print(f"{len(items)} due on {today.isoformat()}")
    elif args.cmd == "review":
        for idx, item in enumerate(deck["items"]):
            if item["id"] == args.id:
                deck["items"][idx] = sm2_update(item, args.q, today)
                save(args.deck, deck)
                nxt = deck["items"][idx]
                print(f"Card {args.id}: next review {nxt['next_review']} (interval {nxt['interval_days']} d)")
                return
        sys.exit(f"No card with id {args.id}")
    elif args.cmd == "list":
        for i in deck["items"]:
            print(f"[{i['id']}] {i['front']} -> {i['back']}  (next {i['next_review']}, reps {i['repetitions']})")


if __name__ == "__main__":
    main()
