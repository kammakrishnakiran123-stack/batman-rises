#!/usr/bin/env bash
# Links every skill folder (a directory containing SKILL.md) into ~/.claude/skills/.
# Skill discovery looks one level down, so each skill is linked on its own.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.claude/skills"
mkdir -p "${SKILLS_DIR}"

linked=0
skipped=0
for dir in "${REPO_DIR}"/*/; do
  name="$(basename "${dir}")"
  [ -f "${dir}SKILL.md" ] || continue
  target="${SKILLS_DIR}/${name}"
  if [ -e "${target}" ] || [ -L "${target}" ]; then
    echo "exists, skipped: ${name}"
    skipped=$((skipped + 1))
    continue
  fi
  ln -s "${REPO_DIR}/${name}" "${target}"
  linked=$((linked + 1))
done

echo "Linked ${linked} skill(s) into ${SKILLS_DIR} (${skipped} already present)."
echo "Use skill-router or invoke any skill by name in Claude Code."
