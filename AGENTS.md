# Repository Guidelines
This guide helps agents align with the repository’s structure, automation scripts, and documentation standards.

## Project Structure & Module Organization
- `docs/` hosts planning artifacts, product briefs, and the PRD; keep new narrative content alongside the closest existing topic.
- `docs/stories/` contains story markdown that feeds automation; preserve numbering and headings so parsing stays stable.
- `tools/` holds Python utilities such as `create_issues_from_stories.py`; place new scripts here with matching module docstrings.
- `CLAUDE.md` and `README.md` define voice and strategy—review them before proposing brand or workflow changes.
- Store drafts or research collateral under `docs/work/` unless a more specific subfolder exists.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` creates an isolated environment for tooling.
- `python -m pip install requests` installs the only required dependency for the GitHub automation script.
- `python tools/create_issues_from_stories.py --root . --dry-run` validates story parsing without creating remote artifacts.
- `python tools/create_issues_from_stories.py --root .` publishes milestones and issues once the dry run is clean.
- `python tools/create_issues_from_stories.py --help` lists optional filters and rate-limit controls.

## Coding Style & Naming Conventions
- Follow PEP 8 for Python: 4-space indentation, `snake_case` functions, and descriptive verb-based names (e.g., `ensure_milestone`).
- Keep constants uppercase and colocate helper functions near their consumers for readability.
- Use Title Case headings in markdown and keep bullet lists action-oriented.
- Name new markdown files with kebab-case prefixes that reflect their epic or story lineage.

## Testing Guidelines
- Always run the automation script with `--dry-run` after edits and review console output for skipped tasks or rate-limit warnings.
- When logic changes, test against at least one file in `docs/stories/` and confirm the expected milestone/title mapping.
- For documentation updates, reconcile facts with the latest PRD (`docs/prd.md`) and architecture notes before submitting.

## Commit & Pull Request Guidelines
- Craft concise, action-oriented commit subjects, mirroring history such as `Stories completed and channel strategy done`.
- Group related documentation edits together; commit automation changes separately so reviews stay focused.
- Pull requests should outline scope, link relevant stories, and include terminal snippets when script behavior changes.
- Request reviewer sign-off before running live GitHub automation or distributing new tokens.

## Security & Configuration Tips
- Export `GITHUB_TOKEN` and `REPO` as environment variables; never commit credentials or screenshots containing tokens.
- Rotate tokens after external testing and document required scopes in the pull request description.
