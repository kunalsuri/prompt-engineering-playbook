# AGENT.md — Prompt Engineering Playbook

> General AI-agent context file. Start here if you are an AI assistant or automation (GitHub Copilot, Claude, GPT, Gemini, or similar) reading this repository.

---

## Repository Purpose

**Prompt Engineering Playbook** is an open-source educational repository by Kunal Suri (DOI: 10.5281/zenodo.18827631).

It contains:
- A **seven-module prompt-engineering curriculum** (`learn/`) with labs, exercises, comparison documents, and architecture decision records
- **Reusable `.prompt.md` templates** (`prompts/`) for Python, React+TypeScript, React+FastAPI, and Node.js+TypeScript stacks — designed for VS Code + GitHub Copilot
- **Tooling** (`scripts/`, `Makefile`) for validating, building, and publishing the documentation

**Audience:** developers, educators, researchers. **Not** a deployable application.

---

## AI Agent Metadata & Maps

To prevent repository clutter for human developers and significantly reduce session token consumption, all heavy agent-specific inventories and guides are stored in the hidden `.ai/` folder. **Do not read these in full unless specifically requested by your task:**

1. **Detailed Inventory Map:** See [.ai/REPOSITORY_MAP.md](.ai/REPOSITORY_MAP.md) for a complete list of files and their edit permissions.
2. **AI Contributor Guidelines:** See [.ai/CONTRIBUTING_AI.md](.ai/CONTRIBUTING_AI.md) for safety policies, prompt design contracts, and validation instructions.

---

## Primary Rules for AI Agents

### Rule 1: Content Lives in Canonical Locations

`docs_src/` is entirely symlinks — **do not create or edit files there**. All content is in:
- `learn/` — curriculum
- `prompts/` — templates
- Repo root — README, CONTRIBUTING, CHANGELOG, GETTING-STARTED, references.md

### Rule 2: `.prompt.md` Files Have a Strict Contract

Every file at `prompts/**/*.prompt.md` must have:

```yaml
---
mode: 'agent'   # required; also: 'edit' | 'ask'
description: 'One sentence (10–500 chars)'
version: '1.0.0'  # semver; bump on behavior change
---
```

Followed immediately by:
```markdown
> **Learn why this works:** [Pattern](../../../learn/03-patterns.md#anchor)
```

Followed by body with these required sections:
```markdown
# Role
# Task
# Output Format
```

### Rule 3: All Citations Use Keys from `references.md`

Format: `[Brown2020]`, `[Wei2022]`, etc. Never inline a URL where a citation key applies. If you need a new citation, add it to `references.md` first.

### Rule 4: Commit Messages Follow Conventional Commits

`<type>(<scope>): <description>`

Types: `feat` | `fix` | `docs` | `refactor` | `chore` | `test`

### Rule 5: Python Tooling Requires a Virtual Environment

Scripts checking `VIRTUAL_ENV` will abort if run without one. Always use `.venv/bin/python`.

---

## Validation Checklist Before Committing

- [ ] `.prompt.md` files: `make lint` shows all `OK:` (no `FAIL:`)
- [ ] `.prompt.md` files: `make validate` exits 0
- [ ] New/changed `learn/` content: citations checked against `references.md`
- [ ] Any file under `learn/` or `prompts/`: run `make sync-check`
- [ ] Notebooks: outputs stripped (pre-commit hook `nbstripout`)
- [ ] No files added to `docs_src/`
- [ ] Commit message follows Conventional Commits

---

## Domain Vocabulary

| Term | Meaning in this repo |
|---|---|
| `.prompt.md` | A Markdown file with YAML frontmatter that VS Code Copilot can invoke as a slash command |
| `copilot-instructions.md` | Always-active system prompt for Copilot in a given project |
| `mode: 'agent'` | Enables Copilot autonomous operation: file reads, terminal commands, multi-step loops |
| `make sync` | Creates `docs_src/` symlinks pointing to canonical source files |
| `_MockClient` | CI-only stub in `learn/labs/lab_utils.py` that intercepts API calls deterministically |
| `LABS_SKIP_API=1` | Env var that makes `get_client()` return `_MockClient` instead of real OpenAI client |
| ADR | Architecture Decision Record — captures *why* a prompt design decision was made |
| Failure Gallery | `learn/labs/failure-gallery/` — deliberately broken prompts for diagnostic exercises |
| Cross-link | `> **Learn why this works:**` block in every `.prompt.md` linking back to the module |
