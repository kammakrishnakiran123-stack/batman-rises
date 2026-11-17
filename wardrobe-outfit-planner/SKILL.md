---
name: wardrobe-outfit-planner
description: Catalog owned clothing items into a structured wardrobe inventory and generate outfit combinations, weather-aware daily looks, and trip packing lists. Use when the user asks to organize their closet, generate outfits from clothes they own, or build a capsule wardrobe or packing plan.
allowed-tools: client
---
# Wardrobe Outfit Planner

Catalog the clothes you already own and generate practical, weather- and occasion-appropriate outfits or minimal trip packing lists.

## When to Use

- The user wants to generate outfits from clothes they already own (text list, CSV/JSON, or photos).
- The user wants to build a digital wardrobe inventory or capsule wardrobe.
- The user needs a mix-and-match packing list for a trip based on destination weather and activities.

## Steps

### 1. Build or Load the Wardrobe Inventory

Create or read a local `wardrobe.json` (or Markdown table) with each item's:

- `id`, `name`, `category` (top, bottom, outerwear, footwear, accessory)
- `color`, `pattern`, `fabric`, `formality` (casual, smart-casual, formal, active)
- `season` (warm, mild, cold, all)

If the user provides photos of clothing items, describe and tag each piece consistently before saving.

### 2. Gather Context for Recommendations

Confirm only what's missing:

- Occasion/dress code (office, casual, wedding, gym, travel).
- Weather/temperature range or trip duration.
- Color or comfort preferences/exclusions.

### 3. Generate Mix-and-Match Outfits

- Propose complete outfits (Top + Bottom + Footwear + optional Layer/Accessory) using **only** items in the inventory.
- Balance color harmony (neutrals + max 1-2 accent pieces), formality consistency, and weather suitability.
- For travel, maximize outfit combinations from the fewest pieces (capsule packing list).

## Scripts

`scripts/wardrobe.py` validates `wardrobe.json`, lists outfits built only from owned items, and suggests a trip capsule.

```bash
python3 scripts/wardrobe.py validate wardrobe.json
python3 scripts/wardrobe.py outfits wardrobe.json --season warm --formality smart-casual
python3 scripts/wardrobe.py capsule wardrobe.json --days 5 --season warm --formality casual
```

## Gotchas

- **Use owned items only**: Never sneak in unowned items unless the user explicitly asks for shopping/gap-filling suggestions.
- **Match formality**: Avoid pairing formal blazers with athletic shorts or gym sneakers with tailored trousers unless intentional streetwear is requested.
- **Update after feedback**: Record disliked pairings or retired items in `wardrobe.json` so future suggestions improve.
