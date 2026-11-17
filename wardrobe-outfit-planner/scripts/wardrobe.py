#!/usr/bin/env python3
"""Validate a wardrobe inventory and generate outfits from owned items only (standard library).

Usage:
  wardrobe.py validate wardrobe.json
  wardrobe.py outfits wardrobe.json --season warm|mild|cold --formality casual|smart-casual|formal|active [--limit 10]
  wardrobe.py capsule wardrobe.json --days N --season ... --formality ...

Inventory format: a JSON list of objects with these keys:
  id, name, category (top|bottom|outerwear|footwear|accessory),
  color, pattern, fabric, formality (casual|smart-casual|formal|active),
  season (warm|mild|cold|all)
Outfits use only items in the file. Nothing is added from outside the inventory.
"""
import argparse
import itertools
import json
import math
import sys
from pathlib import Path

CATEGORIES = {"top", "bottom", "outerwear", "footwear", "accessory"}
FORMALITY = {"casual": 1, "smart-casual": 2, "formal": 3}
SEASONS = {"warm", "mild", "cold", "all"}
REQUIRED = ["id", "name", "category", "color", "pattern", "fabric", "formality", "season"]


def load(path: Path):
    try:
        items = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit(f"Invalid JSON in {path}: {exc}")
    if not isinstance(items, list):
        sys.exit("Inventory must be a JSON list of items.")
    return items


def validate(items):
    problems, seen = [], set()
    for n, item in enumerate(items, 1):
        label = item.get("id", f"item #{n}")
        for key in REQUIRED:
            if key not in item or item[key] in ("", None):
                problems.append(f"{label}: missing '{key}'")
        if item.get("id") in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(item.get("id"))
        if item.get("category") not in CATEGORIES:
            problems.append(f"{label}: category must be one of {sorted(CATEGORIES)}")
        if item.get("formality") not in FORMALITY and item.get("formality") != "active":
            problems.append(f"{label}: formality must be casual, smart-casual, formal, or active")
        if item.get("season") not in SEASONS:
            problems.append(f"{label}: season must be warm, mild, cold, or all")
    return problems


def eligible(items, season, formality):
    """Keep items that suit the season and formality (within one level for non-active)."""
    out = []
    for it in items:
        if it.get("season") not in (season, "all"):
            continue
        f = it.get("formality")
        if formality == "active":
            if f == "active":
                out.append(it)
        elif f in FORMALITY and abs(FORMALITY[f] - FORMALITY[formality]) <= 1:
            out.append(it)
    return out


def outfits(items, season, formality):
    pool = eligible(items, season, formality)
    tops = [i for i in pool if i["category"] == "top"]
    bottoms = [i for i in pool if i["category"] == "bottom"]
    shoes = [i for i in pool if i["category"] == "footwear"]
    layers = [i for i in pool if i["category"] == "outerwear"] if season in ("cold", "mild") else []
    if not (tops and bottoms and shoes):
        return []
    combos = []
    for t, b, s in itertools.product(tops, bottoms, shoes):
        combo = {"top": t["name"], "bottom": b["name"], "footwear": s["name"]}
        if layers:
            combo["layer"] = layers[0]["name"]
        combos.append(combo)
    return combos


def capsule(items, season, formality, days):
    """Smallest top x bottom grid, from the owned pool, that covers the trip without repeats."""
    pool = eligible(items, season, formality)
    tops = [i for i in pool if i["category"] == "top"]
    bottoms = [i for i in pool if i["category"] == "bottom"]
    shoes = [i for i in pool if i["category"] == "footwear"]
    if not (tops and bottoms and shoes):
        return None
    best = None
    for t in range(1, len(tops) + 1):
        for b in range(1, len(bottoms) + 1):
            if t * b >= days:
                cost = t + b + min(2, len(shoes))
                if best is None or cost < best[0]:
                    best = (cost, t, b)
                break
    if best is None:
        return {"enough": False, "available_combinations": len(tops) * len(bottoms)}
    _, t, b = best
    return {"enough": True, "tops": [x["name"] for x in tops[:t]],
            "bottoms": [x["name"] for x in bottoms[:b]], "footwear": [x["name"] for x in shoes[:2]],
            "outfit_slots": t * b}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("file", type=Path)
    o = sub.add_parser("outfits")
    o.add_argument("file", type=Path)
    o.add_argument("--season", choices=["warm", "mild", "cold"], required=True)
    o.add_argument("--formality", choices=["casual", "smart-casual", "formal", "active"], required=True)
    o.add_argument("--limit", type=int, default=10)
    c = sub.add_parser("capsule")
    c.add_argument("file", type=Path)
    c.add_argument("--days", type=int, required=True)
    c.add_argument("--season", choices=["warm", "mild", "cold"], required=True)
    c.add_argument("--formality", choices=["casual", "smart-casual", "formal", "active"], required=True)
    args = ap.parse_args()

    items = load(args.file)
    if args.cmd == "validate":
        problems = validate(items)
        if problems:
            print("\n".join(problems))
            sys.exit(1)
        print(f"Inventory OK: {len(items)} items")
    elif args.cmd == "outfits":
        problems = validate(items)
        if problems:
            sys.exit("Fix the inventory first (run validate).")
        combos = outfits(items, args.season, args.formality)
        if not combos:
            print("No complete outfit (top + bottom + footwear) fits these settings. Add items or relax the filter.")
        for n, combo in enumerate(combos[: args.limit], 1):
            print(f"{n}. " + ", ".join(f"{k}: {v}" for k, v in combo.items()))
        if len(combos) > args.limit:
            print(f"... {len(combos) - args.limit} more")
    else:
        result = capsule(items, args.season, args.formality, args.days)
        if result is None:
            print("Need at least one top, bottom, and footwear item for this season and formality.")
        elif not result["enough"]:
            print(f"Only {result['available_combinations']} combinations available; "
                  f"{args.days} days needs more owned items or a laundry plan.")
        else:
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
