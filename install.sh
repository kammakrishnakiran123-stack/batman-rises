#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.claude/skills/batman-rises"

mkdir -p "${HOME}/.claude/skills"

if [ -L "${TARGET_DIR}" ] || [ -e "${TARGET_DIR}" ]; then
  echo "Existing installation found at ${TARGET_DIR}"
  echo "Remove it first if you want to relink: rm -rf \"${TARGET_DIR}\""
  exit 0
fi

ln -s "${REPO_DIR}" "${TARGET_DIR}"
echo "Linked Batman Rises skills to ${TARGET_DIR}"
echo "Use skill-router or invoke any of the 23 skills in Claude Code."
