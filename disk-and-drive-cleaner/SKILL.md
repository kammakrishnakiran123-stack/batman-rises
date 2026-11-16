---
name: disk-and-drive-cleaner
description: Safely analyze macOS disk usage (referencing daymade/claude-code-skills macos-cleaner) and Google Drive storage hogs, then present user-confirmed cleanup plans. Use when the user asks to free up Mac disk space, find large caches/files, or clean up Google Drive storage.
allowed-tools: client
---
# Disk & Google Drive Cleaner

Diagnose what is consuming storage on macOS (inspired by `macos-cleaner` in [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills)) or in Google Drive, and build a safe, user-confirmed cleanup plan.

## When to Use

- The user is low on Mac disk space and wants to find large files, Xcode/Docker/npm/Homebrew/pip caches, or Time Machine snapshots.
- The user wants to identify large or duplicate files in Google Drive to reclaim quota.
- The user wants to install `macos-cleaner` from `daymade/claude-code-skills`.

## Steps

### 1. Optional: Install `macos-cleaner` in Claude Code

```bash
npx skills add daymade/claude-code-skills/macos-cleaner --agent claude-code
```

### 2. Audit Storage Safely (Read-Only First)

- **macOS local disk**: Check overall free space and top space consumers without deleting anything:

  ```bash
  df -h /
  du -sh ~/Library/Caches/* ~/Downloads/* ~/.Trash 2>/dev/null | sort -hr | head -n 20
  ```

  Also check developer bloat if relevant (`brew cleanup -n`, `docker system df`, `npm cache ls`, `xcrun simctl list` / `~/Library/Developer/Xcode/DerivedData`).
- **Google Drive**: Query largest files (`orderBy="quotaBytesUsed desc"`), Trash contents, and duplicate/old exports.

### 3. Present Categorized Cleanup Plan

Group findings by safety tier before touching anything:

- **Safe to clear** (rebuildable caches, Trash, old installers/DMGs).
- **Review first** (large Downloads, old Xcode DerivedData/simulators, Docker images, large Drive videos/backups).
- **Do not touch** (system files, active app data, SIP-protected paths).

Wait for explicit user confirmation on each item/category before running any delete or cleanup command.

## Scripts

`scripts/size_audit.py` is read-only. It sizes folders two levels deep and tags each one `SAFE_TO_CLEAR`, `REVIEW_FIRST`, `DO_NOT_TOUCH`, or `ASK_USER`. It never deletes anything.

```bash
python3 scripts/size_audit.py ~ --top 25 --md audit.md
```

## Gotchas

- **User runs or confirms every deletion**: Never auto-delete files silently; always show exact paths and sizes first.
- **Never disable SIP**: Do not touch `/System` or SIP-protected directories.
- **Google Drive Trash**: Deleting a Drive file moves it to Trash (still counting toward quota) until Trash is emptied.
