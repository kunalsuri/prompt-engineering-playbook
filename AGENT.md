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

## Repository Map (Quick Reference)

```
prompt-engineering-playbook/
├── learn/                     Seven-module curriculum
│   ├── 00-orientation.md      Story-first on-ramp
│   ├── 01-introduction.md     What prompt engineering is
│   ├── 02-core-principles.md  Specificity, decomposition, iteration, evaluation
│   ├── 03-patterns.md         Six patterns (zero-shot, few-shot, CoT, ReAct, role, constrained)
│   ├── 04-best-practices.md   Token management, versioning, team workflows
│   ├── 05-advanced-patterns.md RAG, adversarial, multimodal, evaluation pipelines
│   ├── 06-agentic-patterns.md Plan-and-execute, reflection, multi-agent
│   ├── comparisons/           Deep-dive technique comparisons (cited)
│   ├── decisions/             Prompt design ADRs (001–004)
│   ├── labs/                  Jupyter notebooks + Python scripts + failure gallery
│   ├── prompt-examples/       Worked examples per pattern
│   ├── glossary.md
│   ├── cookbook.md            20 copy-paste everyday recipes
│   ├── cheatsheet.md
│   └── README.md
│
├── prompts/                   Reusable prompt templates
│   ├── shared/                Stack-agnostic (schema, evaluation template)
│   ├── python/                copilot-instructions.md + 7 prompt files
│   ├── react-typescript/      copilot-instructions.md + 8 prompt files
│   ├── react-fastapi/         copilot-instructions.md + 3 prompt files
│   └── nodejs-typescript/     copilot-instructions.md + 4 prompt files
│
├── scripts/                   Developer tooling
│   ├── setup.sh               Unified stack installer (end-user facing)
│   ├── lint-prompt-frontmatter.sh
│   ├── validate-prompt-schema.py
│   ├── run-notebook-smoke.py
│   └── <stack>/setup.sh       Stack-specific installers
│
├── docs_src/                  MkDocs source — SYMLINKS ONLY, do not edit
├── assets/                    Site CSS and favicon
├── Makefile                   Developer task runner
├── mkdocs.yml                 Documentation site config
├── requirements-docs.txt      MkDocs build deps
├── requirements-dev.txt       Validation script deps (jsonschema, pyyaml)
├── .github/
│   ├── copilot-instructions.md  Repo-level Copilot context
│   ├── workflows/               5 CI workflows
│   └── prompts/                 (See .github/prompts/README.md)
├── CONTRIBUTING.md            Human contribution guide
├── CONTRIBUTING_AI.md         AI-agent-specific contribution guide  ← THIS FILE's sibling
├── CLAUDE.md                  Claude Code context (superset of this file for Claude)
├── ARCHITECTURE.md            Deep architecture documentation
├── REPOSITORY_MAP.md          Full navigable file inventory
└── DEVELOPMENT_WORKFLOW.md    Step-by-step developer workflows
```

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

## Known Limitations and Technical Debt

1. **Windows incompatibility** — `make sync` creates POSIX symlinks; Makefile is Linux/macOS only
2. **No unit tests for lab Python code** — only notebook smoke tests with a mock client
3. **Optional schema fields underused** — `tags`, `patterns`, `stack` optional in schema but not consistently populated in prompt files
4. **Token budget advisory only** — the CI check warns but never blocks
5. **`_MockClient` keyword matching** — brittle; matched on specific string fragments from lab prompts

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
