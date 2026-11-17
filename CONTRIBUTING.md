# Contributing to Batman Rises

Contributions are welcome! Each skill lives in its own kebab-case directory with a self-contained `SKILL.md` file.

## Adding a New Skill

1. Create a folder named `<kebab-case-skill-name>/` with a `SKILL.md` file.
2. Include valid YAML frontmatter (`name`, `description`, `allowed-tools`).
3. Keep instructions concise, imperative, and under 500 lines, with clear **When to Use**, **Steps**, and **Gotchas** sections.
4. Add your skill to the routing table in `skill-router/SKILL.md` and the catalog in `README.md`.
5. Never commit API keys, tokens, personal emails, or local machine paths.
6. If you add a script, put it in `<skill>/scripts/`, make it standard-library only where possible, and add a test to `tests/test_skills.py`.
7. Run `python3 tests/test_skills.py` before opening a pull request. It must pass.
