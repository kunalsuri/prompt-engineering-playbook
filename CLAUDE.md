# CLAUDE.md — Prompt Engineering Playbook

> AI-agent context file for Claude Code. Optimized for minimal token usage and maximal accuracy.

## What This Repository Is

An **educational repository** with two self-contained halves:

1. **`learn/`** — Seven-module prompt-engineering curriculum (Modules 0–6) + comparison docs, ADRs, labs, and a failure gallery.
2. **`prompts/`** — Reusable `.prompt.md` templates for four tech stacks, tested with VS Code + GitHub Copilot.

**Not** a software application. No server, no package to publish, no database. The primary artifacts are Markdown files and shell/Python tooling scripts.

---

## Essential Commands

```bash
# Setup (Linux/macOS only — Makefile uses ln -sfn)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt -r requirements-dev.txt

# Full check suite (runs lint → validate → sync-check → symlink-check → build)
make check

# Individual steps
make lint           # Validate .prompt.md frontmatter, cross-links, required sections
make validate       # JSON schema validation of .prompt.md YAML (requires .venv)
make sync           # Regenerate docs_src/ symlinks
make sync-check     # Verify symlinks resolve
make build          # Build MkDocs static site → _site/
make serve          # Local dev server (live-reload)

# Notebook smoke tests (CI pattern — no API calls)
LABS_SKIP_API=1 LLM_MODEL=mock-labs python scripts/run-notebook-smoke.py
```

> **Windows**: `make sync` and `make lint` use POSIX shell (`ln`, `bash`). Run these steps in WSL or Git Bash, or use the GitHub Actions CI as the authoritative check.

---

## Critical Constraints

### `.prompt.md` Files — Three Mandatory Checks

Every file matching `prompts/**/*.prompt.md` MUST satisfy all three:

1. **YAML frontmatter** (first block, between `---` delimiters):
   ```yaml
   ---
   mode: 'agent'          # or 'edit' | 'ask'
   description: 'One-sentence description (10–500 chars)'
   version: '1.0.0'       # semver — bump on behavior change
   ---
   ```

2. **Cross-link** (immediately after closing `---`):
   ```markdown
   > **Learn why this works:** [Pattern Name](../../../learn/03-patterns.md#anchor)
   ```

3. **Required body sections** (in this order):
   ```markdown
   # Role
   # Task
   # Output Format
   ```

CI blocks merge if any of these are missing. Run `make lint` locally before pushing.

### `docs_src/` Is Symlinks Only

**Never edit files inside `docs_src/`** — it is a generated layer of symlinks produced by `make sync`. Edit canonical files at their source locations:

| Content area | Canonical location |
|---|---|
| Top-level docs | `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, etc. (repo root) |
| Curriculum | `learn/` |
| Prompt templates | `prompts/` |
| Assets | `assets/` |

### Citations in `learn/`

All factual claims and performance figures in curriculum files must use citation keys from `references.md` (format: `[Brown2020]`, `[Wei2022]`). If you add a new citation, add it to `references.md` first in APA 7th edition format.

### Python Environment Isolation

Scripts that import third-party packages (`validate-prompt-schema.py`) require a virtual environment. The script itself will fail fast with a clear error if run outside one.

---
## Key Files & Locations

Refer to [.ai/REPOSITORY_MAP.md](.ai/REPOSITORY_MAP.md) for the complete, navigable directory map and file inventory of this repository.

---

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `chore`, `test`
**Scopes:** `curriculum`, `comparisons`, `python`, `react-ts`, `fastapi`, `nodejs-ts`, `shared`, `scripts`, `refs`

---

## Adding a New Prompt Template

1. Place file at `prompts/<stack>/prompts/<verb>-<noun>.prompt.md` (lowercase, hyphen-separated)
2. Add YAML frontmatter (`mode`, `description`, `version`)
3. Add cross-link: `> **Learn why this works:** ...`
4. Add `# Role`, `# Task`, `# Output Format` sections
5. Run `make lint` — all lines must show `OK:`
6. Run `make validate` — must exit 0
7. Update `prompts/<stack>/prompts/README.md` with the new entry

---

## Adding Curriculum Content

1. Edit the canonical `.md` file under `learn/`
2. Cite all facts with keys from `references.md`; add new references if needed
3. Include learning objectives, worked examples, and at least two exercises
4. Run `make sync-check` to ensure docs_src/ stays consistent
5. Run `make build` to catch any MkDocs rendering errors

---

## Dangerous Areas / Invariants

- **`docs_src/`** — symlinks only; adding real files here will break `make check`
- **Recursive symlinks** — CI explicitly checks for `learn/learn`, `prompts/prompts`, etc. Do not create self-referential symlinks inside `learn/` or `prompts/`
- **Notebook outputs** — pre-commit hook strips them with `nbstripout`; do not commit notebooks with outputs
- **`scripts/validate-prompt-schema.py`** — must be run from `.venv`; reads schema from `prompts/shared/prompt-registry.schema.json`
- **Version field in `.prompt.md`** — must be bumped on any behavior change (enforced by schema: `pattern: "^\d+\.\d+\.\d+$"`)
- **Token budget** — prompt files exceeding ~4000 estimated tokens trigger a CI warning (not blocking), but large prompts harm usability

---

## CI Overview

| Workflow | Trigger | What it checks |
|---|---|---|
| `lint-markdown.yml` | push/PR on `*.md` | Links, frontmatter lint, token budget, citations, prompt cross-links, copilot-instructions lint, docs sync, recursive symlinks, docs build |
| `quality-nonmarkdown.yml` | push/PR on scripts/tests/notebooks/config | `make check` (validators + `pytest` suite), lab-sync, notebook smoke tests, `shellcheck` |
| `deploy-docs.yml` | push to `main` (docs paths) | Builds & deploys MkDocs to GitHub Pages |
| `link-check-external.yml` | Weekly Monday 08:00 UTC | External URL liveness check |
| `security-dependencies.yml` | scheduled | Dependency CVE scan |

---

## Testing Strategy

This repo has no application code, so "tests" are content validators plus a
`pytest` suite (`tests/`) that tests those validators. Quality is enforced through:

1. **Frontmatter linting** — `scripts/lint-prompt-frontmatter.sh` (bash, structural check)
2. **Copilot-instructions linting** — `scripts/lint-copilot-instructions.sh` (bash, structural check)
3. **Schema validation** — `scripts/validate-prompt-schema.py` (Python, JSON Schema draft 2020-12)
4. **Citation check** — `scripts/check-citations.py` (every `[Key]` in `learn/` is defined in `references.md`)
5. **Cross-link check** — `scripts/check-prompt-crosslinks.py` (each prompt's "Learn why this works" link resolves to a real file + heading anchor)
6. **Lab sync check** — `scripts/check-lab-sync.py` (`.py`/`.ipynb` parity)
7. **Notebook smoke tests** — `scripts/run-notebook-smoke.py` with `_MockClient` (no API calls)
8. **`pytest` tooling suite** — `tests/` exercises every validator above (incl. failure paths) and `lab_utils.py`; run with `make test` (coverage via `pytest-cov`)
9. **`shellcheck`** — static analysis of shell scripts (config in `.shellcheckrc`)
10. **Link checking** — internal (MLC) and external (Lychee) broken link detection
11. **Docs build** — `mkdocs build --strict` catches rendering/navigation errors

`make check` runs 1–6 + 8–11; `make check-all` additionally runs the notebook
smoke tests (7). See `tests/README.md` for details.

---

## Assumptions / Unclear Areas

> ⚠️ Items that need human clarification:

- `mkdocs.yml` was not shown in this audit — confirm `nav:` structure matches current module count
- `BETA-RELEASE-NOTES.md` references `v0.1.0-beta`; whether `[Unreleased]` in CHANGELOG will become `v0.2.0` is unclear
- The `scripts/<stack>/setup.sh` files (e.g., `scripts/python/setup.sh`) were not read — they may be legacy or stack-specific variants of `scripts/setup.sh`
- Windows support: `make sync` creates POSIX symlinks; the Makefile is functionally Linux/macOS-only
