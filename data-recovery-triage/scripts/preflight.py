#!/usr/bin/env python3
"""Read-only preflight checks before any imaging or recovery. It never writes to the source.

Usage:
  preflight.py --source /dev/sdX-or-file --dest /path/on/healthy/drive [--image-size-bytes N]

Checks:
  1. The source exists and is readable.
  2. The destination is on a different device from the source (never recover onto the source).
  3. The destination has room for a full image (size from --image-size-bytes, or the source size).
  4. On Linux, the source is not mounted read-write.
Exit code 1 if any check fails. Run this before ddrescue, testdisk, or photorec.
"""
import argparse
import os
import shutil
import stat
import sys
from pathlib import Path


def source_size(path: Path):
    st = os.stat(path)
    if stat.S_ISBLK(st.st_mode):
        try:
            with open(path, "rb") as fh:
                return fh.seek(0, os.SEEK_END)
        except OSError:
            return None
    return st.st_size


def mounted_rw(source: Path):
    """Return True/False if /proc/mounts says the source is mounted rw, None if unknown."""
    mounts = Path("/proc/mounts")
    if not mounts.exists():
        return None
    real = str(source.resolve())
    for line in mounts.read_text().splitlines():
        fields = line.split()
        if len(fields) >= 4 and fields[0] == real:
            return "rw" in fields[3].split(",")
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--dest", type=Path, required=True)
    ap.add_argument("--image-size-bytes", type=int, default=None)
    args = ap.parse_args()

    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))

    src_ok = args.source.exists() and os.access(args.source, os.R_OK)
    check("source exists and is readable", src_ok, str(args.source))
    if not src_ok:
        sys.exit(1)

    dest_ok = args.dest.is_dir()
    check("destination folder exists on the healthy drive", dest_ok,
          "" if dest_ok else "create it yourself on the healthy drive; this check never writes")
    if dest_ok:
        same_dev = (not stat.S_ISBLK(os.stat(args.source).st_mode)
                    and os.stat(args.source).st_dev == os.stat(args.dest).st_dev)
        check("destination is a different device from the source", not same_dev,
              "same device: pick a different drive" if same_dev else "")

    need = args.image_size_bytes or source_size(args.source)
    if not dest_ok:
        need = None
    if dest_ok and need is None:
        check("image size known", False, "pass --image-size-bytes for this device")
    elif dest_ok:
        free = shutil.disk_usage(args.dest).free
        check("destination has room for the full image", free >= need,
              f"need {need:,} bytes, free {free:,} bytes")

    rw = mounted_rw(args.source)
    if rw is None:
        print("[INFO] mount status not checked on this system")
    else:
        check("source is not mounted read-write", not rw,
              "unmount it first (umount or diskutil unmountDisk)" if rw else "")

    print("\nAll checks passed. Image the source with ddrescue, then work only on the image." if all(results)
          else "\nFix the failures above before running any recovery tool.")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
