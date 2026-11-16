---
name: photo-library-organizer
description: Sort and organize travel or family photos by EXIF date, camera, or location into clean YYYY/YYYY-MM-DD folders safely with dry-run previews (aligned with ComposioHQ/awesome-claude-skills File Organizer). Use when the user asks to sort messy photo folders, rename photos by date, or group travel/family pictures.
allowed-tools: client
---
# Photo Library Organizer

Safely organize messy travel or family photo folders by EXIF timestamp, device, or GPS metadata into clean `YYYY/YYYY-MM-DD` directories, inspired by the File Organizer pattern in [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills).

## When to Use

- The user wants to sort a cluttered folder of travel, event, or family photos into dated directories.
- The user wants to deduplicate exact photo copies (by SHA-256) or standardize filenames (`YYYYMMDD_HHMMSS_<orig>`).
- The user asks about grouping photos by place or activity (requires EXIF GPS or local vision/face-clustering tools).

## Steps

### 1. Inspect the Source Folder (Read-Only First)

Check file types, counts, and available EXIF tools (`exiftool` or Python `Pillow`):

```bash
find "/path/to/photos" -maxdepth 2 -type f | wc -l
which exiftool || python3 -c "import PIL; print('Pillow OK')"
```

### 2. Run a Dry-Run Preview

Write a small Python script (or `exiftool` command) that reads `DateTimeOriginal` (falling back to file `mtime` only when EXIF is absent) and prints the proposed `source -> destination` plan without moving or deleting any file:

- Target layout: `<output_root>/YYYY/YYYY-MM-DD/<filename>` (or `<output_root>/YYYY/YYYY-MM-DD_<Event>/`).
- Detect exact duplicates via SHA-256 hash and list them separately instead of silently deleting.

### 3. Execute Safely After User Confirmation

- Present the dry-run summary (total files, dated vs. undated count, duplicate count).
- Prefer **copy** or **move within the same volume** only after the user confirms the plan.
- For face, place, or activity sorting beyond EXIF dates/GPS, note that local vision/clustering tools (like `immich`, `digikam`, or a local CLIP/face model) are needed.

## Scripts

`scripts/organize_photos.py` does the dry run and the copy. It reads EXIF with Pillow, so RAW and most HEIC files land in `_undated/` unless `exiftool` is used instead.

```bash
python3 scripts/organize_photos.py "/path/to/photos" "/path/to/library" --plan plan.csv   # dry run
python3 scripts/organize_photos.py "/path/to/photos" "/path/to/library" --plan plan.csv --execute
```

## Gotchas

- **Never delete originals silently**: Always run a dry-run first and keep duplicates in a `_duplicates/` review folder rather than deleting them automatically.
- **RAW + sidecar files**: Keep `.CR2`/`.NEF`/`.ARW`/`.DNG` paired with their `.xmp` sidecars when moving.
- **Timezone & WhatsApp strips**: Messaging apps (like WhatsApp) strip EXIF metadata; flag undated files into an `_undated/` folder instead of guessing dates.
