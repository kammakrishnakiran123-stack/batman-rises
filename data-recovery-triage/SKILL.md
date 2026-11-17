---
name: data-recovery-triage
description: Guide safe, read-only data recovery triage for corrupted drives, SD cards, or deleted files using ddrescue, testdisk, and photorec. Use when the user asks to recover files from a failing or corrupted drive, partition, or USB/SD card.
allowed-tools: client
---
# Data Recovery Triage

Perform safe, read-only triage and recovery planning for corrupted drives, SD cards, or accidentally deleted partitions without causing further data loss.

## When to Use

- The user has a corrupted USB drive, SD card, external HDD/SSD, or accidentally formatted/deleted partition.
- The user asks how to image a failing drive or run `ddrescue`, `testdisk`, or `photorec`.

## Steps

### 1. Enforce the Golden Rule: Stop Writing Immediately

Before running any command:

- **Do not write, format, `chkdsk /f`, or `fsck -y` on the failing drive.**
- Unmount the affected volume read-only if mounted (`diskutil unmountDisk /dev/diskN` on macOS, `umount` on Linux).
- Confirm a separate healthy destination drive exists with enough free space to hold a full byte-for-byte image of the damaged drive.

### 2. Image First, Recover from the Image

Always clone the failing media to an image file with `ddrescue` (handles bad sectors cleanly with a mapfile) and work exclusively on the image:

```bash
# Identify the disk carefully first (macOS: diskutil list | Linux: lsblk)
ddrescue -d -r3 /dev/rdiskN /path/to/healthy/drive/recovery.img /path/to/healthy/drive/recovery.map
```

If the run stops early or is interrupted, run the same command again with the same mapfile. `ddrescue` resumes from the mapfile instead of starting over. Keep the mapfile on the healthy drive; losing it means restarting the copy.

### 3. Run Read-Only Partition & File Recovery on the Image

- **Missing/corrupted partition table**: Run `testdisk /path/to/recovery.img` to inspect and restore partition structures non-destructively.
- **Deleted files / raw carving**: Run `photorec /d /path/to/healthy/recovered/ /path/to/recovery.img` (confirm the options with `photorec /h` on the installed version). `/d` sends output to the healthy directory. Create that directory before starting.
- **Filesystem check**: Run `fsck -n` (read-only dry run) on a copy of the image before attempting any repair.

Report what was recovered and where it was written, and tell the user that the original media was only read, never written to.

## Scripts

`scripts/preflight.py` runs read-only checks before any recovery tool: the source is readable, the destination folder exists and is on a different drive, the destination has room for a full image, and the source is not mounted read-write. It exits 1 on any failure and never creates folders or writes to the source.

```bash
python3 scripts/preflight.py --source /dev/diskN --dest /Volumes/Healthy --image-size-bytes 500000000000
```

## Gotchas

- **Hardware failure signs**: If a mechanical drive is clicking, grinding, or disconnecting repeatedly, **stop immediately**—software tools will accelerate platter damage; recommend a professional clean-room lab.
- **Never recover to the same drive**: Writing recovered files back onto the source partition overwrites unrecovered sectors permanently.
- **Verify disk identifiers**: Double-check `/dev/diskN` or `/dev/sdX` before running `ddrescue` so you never overwrite a healthy system drive.
