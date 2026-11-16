#!/usr/bin/env python3
"""Organize a photo folder into YYYY/YYYY-MM-DD, safely.

Default mode is a dry run: it writes only a CSV plan and never touches photos.
--execute copies files into the destination. It never moves or deletes originals.

Usage:
  organize_photos.py SRC DST [--plan photo_plan.csv]     # dry run
  organize_photos.py SRC DST --execute                   # copy after reviewing the plan

Layout:
  DST/YYYY/YYYY-MM-DD/<file>   files with an EXIF capture date
  DST/_undated/<file>          no readable EXIF date (not guessed from mtime)
  DST/_duplicates/<file>       byte-identical copies (SHA-256); first copy is kept
"""
import argparse
import csv
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

MEDIA_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".tif", ".tiff",
              ".cr2", ".nef", ".arw", ".dng"}
SIDECAR_EXTS = {".xmp"}
EXIF_IFD = 0x8769          # Exif sub-IFD holds DateTimeOriginal
TAG_ORIGINAL = 36867
TAG_DIGITIZED = 36868
TAG_DATETIME = 306
EXIF_FORMAT = "%Y:%m:%d %H:%M:%S"


def capture_date(path: Path):
    """Return the EXIF capture date as a date, or None. Pillow cannot read RAW or
    most HEIC files; those come back as None and land in _undated."""
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            sub = exif.get_ifd(EXIF_IFD) if exif else {}
            for tag, source in ((TAG_ORIGINAL, sub), (TAG_DIGITIZED, sub), (TAG_DATETIME, exif)):
                raw = source.get(tag)
                if raw:
                    try:
                        return datetime.strptime(str(raw).strip()[:19], EXIF_FORMAT).date()
                    except ValueError:
                        continue
    except (OSError, ValueError):
        return None
    return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect(src: Path):
    """Return visible media files (sorted) and a map of sidecar path -> media path.
    Both common sidecar names are matched: photo.xmp and photo.jpg.xmp."""
    media, sidecar_paths = [], []
    for p in sorted(src.rglob("*")):
        if not p.is_file() or any(part.startswith(".") for part in p.relative_to(src).parts):
            continue
        ext = p.suffix.lower()
        if ext in MEDIA_EXTS:
            media.append(p)
        elif ext in SIDECAR_EXTS:
            sidecar_paths.append(p)
    sidecars = {}
    for m in media:
        for candidate in (m.with_suffix(".xmp"), Path(str(m) + ".xmp")):
            if candidate in sidecar_paths:
                sidecars.setdefault(m, []).append(candidate)
    return media, sidecars


def unique_dest(dest: Path, taken: set) -> Path:
    candidate, n = dest, 2
    while candidate in taken or candidate.exists():
        candidate = dest.with_name(f"{dest.stem}_{n}{dest.suffix}")
        n += 1
    taken.add(candidate)
    return candidate


def build_plan(src: Path, dst: Path):
    media, sidecars = collect(src)
    seen_hashes = {}
    taken = set()
    rows = []
    for path in media:
        digest = sha256(path)
        when = capture_date(path)
        if digest in seen_hashes:
            folder = dst / "_duplicates"
            status = "duplicate"
        elif when:
            folder = dst / f"{when:%Y}" / f"{when:%Y-%m-%d}"
            status = "dated"
        else:
            folder = dst / "_undated"
            status = "undated"
        seen_hashes.setdefault(digest, path)
        targets = [(path, folder)]
        targets += [(sc, folder) for sc in sidecars.get(path, [])]
        for source, target_dir in targets:
            dest = unique_dest(target_dir / source.name, taken)
            rows.append({
                "status": status,
                "source": str(source),
                "destination": str(dest),
                "sha256": digest if source == path else "",
                "duplicate_of": str(seen_hashes[digest]) if status == "duplicate" and source == path else "",
            })
    return rows


def guard_paths(src: Path, dst: Path):
    src_r, dst_r = src.resolve(), dst.resolve()
    if dst_r == src_r or src_r in dst_r.parents:
        sys.exit("Destination must not be the source folder or inside it.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--plan", type=Path, default=Path("photo_plan.csv"))
    ap.add_argument("--execute", action="store_true", help="copy files after reviewing the plan")
    args = ap.parse_args()

    if not args.src.is_dir():
        sys.exit(f"Source is not a folder: {args.src}")
    guard_paths(args.src, args.dst)

    rows = build_plan(args.src, args.dst)
    with args.plan.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["status", "source", "destination", "sha256", "duplicate_of"])
        writer.writeheader()
        writer.writerows(rows)

    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(f"Plan written to {args.plan} ({len(rows)} files)")
    for status in ("dated", "undated", "duplicate"):
        print(f"  {status:10s} {counts.get(status, 0)}")

    if not args.execute:
        print("Dry run only. Review the plan, then re-run with --execute to copy.")
        return

    for row in rows:
        dest = Path(row["destination"])
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(row["source"], dest)
    print(f"Copied {len(rows)} files into {args.dst}. Originals were not changed.")


if __name__ == "__main__":
    main()
