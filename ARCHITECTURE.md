# ARCHITECTURE.md — Prompt Engineering Playbook

> Deep architectural documentation. Read this for a complete mental model of how the repo is structured, how the pieces interact, and why key decisions were made.

---

## 1. High-Level Architecture

This repository has **no runtime application**. Its architecture is entirely about content organization, documentation build pipeline, and quality-gate tooling.

```
                    ┌─────────────────────────────────────────────┐
                    │          REPOSITORY ARCHITECTURE              │
                    │                                               │
  Canonical Content │  learn/          prompts/         assets/    │
  (source of truth) │  (curriculum)    (templates)      (CSS/SVG)  │
                    └──────────┬───────────┬────────────────┬──────┘
                               │  make sync (symlinks)      │
                               ▼                            │
                    ┌──────────────────────┐               │
                    │     docs_src/        │◄──────────────┘
                    │  (symlinks only)     │
                    └──────────┬───────────┘
                               │  mkdocs build
                               ▼
                    ┌──────────────────────┐
                    │      _site/          │  ──► GitHub Pages
                    │  (static HTML/CSS)   │      (kunalsuri.github.io/
                    └──────────────────────┘       prompt-engineering-playbook)
```

---

## 2. Content Architecture

### 2.1 Curriculum (`learn/`)

**Module progression** (strictly sequential — each module references the prior):

```
00-orientation  →  01-introduction  →  02-core-principles  →  03-patterns
                                                                     │
                                                              04-best-practices
                                                                     │
                                                           05-advanced-patterns
                                                                     │
                                                           06-agentic-patterns
```

**Supporting content** in `learn/`:

| Directory/File | Purpose | Relation to modules |
|---|---|---|
| `comparisons/` | Deep-dive technique analyses with citations | Referenced from modules 3, 5, 6 |
| `decisions/` | Prompt design ADRs | Cross-referenced from modules 2–6 |
| `labs/` | Jupyter notebooks + Python scripts + failure gallery | Practical application of modules 1–6 |
| `prompt-examples/` | Worked examples per module | Supplements modules 3, 5 |
| `glossary.md` | Term definitions | Repository-wide |
| `cookbook.md` | 20 copy-paste recipes | Standalone; no prerequisites |
| `cheatsheet.md` | Quick reference | Supplements all modules |
| `progress-tracker.md` | Student self-tracking | Standalone |
| `ci-cd-integration.md` | Prompt integration in CI/CD | Advanced supplement |
| `meta-prompting.md` | Prompts that generate prompts | Advanced supplement |

### 2.2 Prompt Templates (`prompts/`)

**Stack structure** (all four stacks are identical in shape):

```
prompts/<stack>/
├── copilot-instructions.md     Always-active system-level instructions
└── prompts/
    └── *.prompt.md             Task-specific prompt files (invoked on demand)
```

**Shared resources** (`prompts/shared/`):
- `prompt-registry.schema.json` — JSON Schema (draft 2020-12) for frontmatter validation
- `evaluation-template.md` — Manual + automated evaluation framework
- `readme-generator-base.md` — Shared README generation base

**Stack inventory:**

| Stack | Instructions | Prompt Count | Key files |
|---|---|---|---|
| `python` | Python 3.12+, PEP 8, ruff, mypy, pytest, Google docstrings | 7 | create-feature, debug-issue, generate-docs, refactor-code, review-code, write-tests, update-generate-readme |
| `react-typescript` | React, TypeScript, strict mode | 8 | auditor-best-practices, auditor-codebase-maturity, auditor-cybersecurity-features, auto-code-implementation, create-chatbot-ollama, create-saas-app-V2, safety-gate-llm, update-generate-readme |
| `react-fastapi` | React + FastAPI full-stack | 3 | create-app-react-fastapi, create-test-suite, update-generate-readme |
| `nodejs-typescript` | Node.js, TypeScript | 4 | create-api-endpoint, generate-openapi-spec, review-code, write-tests |

---

## 3. Documentation Build Pipeline

```
                  make sync
learn/ ──────────────────────────────┐
prompts/ ────────────────────────────┤──► docs_src/ (symlinks)
assets/ ─────────────────────────────┤
README.md, CONTRIBUTING.md, etc. ────┘

                  mkdocs build --strict
docs_src/ ──────────────────────────────► _site/ ──► GitHub Pages
mkdocs.yml (nav + theme config)
```

**Symlink map** (created by `make sync`):

| `docs_src/` symlink | → Points to |
|---|---|
| `docs_src/index.md` | `../README.md` |
| `docs_src/GETTING-STARTED.md` | `../GETTING-STARTED.md` |
| `docs_src/CONTRIBUTING.md` | `../CONTRIBUTING.md` |
| `docs_src/CHANGELOG.md` | `../CHANGELOG.md` |
| `docs_src/BETA-RELEASE-NOTES.md` | `../BETA-RELEASE-NOTES.md` |
| `docs_src/references.md` | `../references.md` |
| `docs_src/LICENSE` | `../LICENSE` |
| `docs_src/learn` | `../learn` |
| `docs_src/prompts` | `../prompts` |
| `docs_src/assets` | `../assets` |

**Key invariant**: `make sync` must be idempotent and must clean up known self-referential symlink locations first (see `make recursive-symlink-check`).

---

## 4. CI/CD Architecture

Five GitHub Actions workflows, each with independent trigger scoping:

### 4.1 `lint-markdown.yml`
Triggers: push/PR on `**/*.md`

| Job | Tool | What it checks | Blocking? |
|---|---|---|---|
| `markdown-link-check` | `gaurav-nelson/github-action-markdown-link-check` | Internal relative links only (external excluded by `mlc-config.json`) | Yes |
| `prompt-frontmatter-lint` | `scripts/lint-prompt-frontmatter.sh` | mode/description/version fields, cross-link, # Role/# Task/# Output Format | Yes |
| `prompt-token-budget` | inline bash | ≈4000 token limit (chars/4) | No (advisory) |
| `docs-sync-check` | inline bash + `make sync` | `docs_src/` symlinks resolve | Yes |
| `recursive-symlink-check` | inline bash | No self-referential symlinks | Yes |
| `docs-build` | `mkdocs build --strict` | MkDocs renders without errors | Yes |

### 4.2 `quality-nonmarkdown.yml`
Triggers: push/PR on Makefile, mkdocs.yml, requirements, scripts, notebooks, workflows

| Job | What it does |
|---|---|
| `check` | `make check` — full suite in a Python 3.12 venv |
| `notebook-smoke` | Executes `lab_*.ipynb` with `LABS_SKIP_API=1` via `nbclient` |

### 4.3 `deploy-docs.yml`
Triggers: push to `main` on docs-related paths; `workflow_dispatch`

Builds MkDocs site and deploys to GitHub Pages via `actions/deploy-pages`. Uses `concurrency: group: pages` to prevent overlapping deploys.

### 4.4 `link-check-external.yml`
Triggers: weekly Monday 08:00 UTC

Uses `lycheeverse/lychee-action` to check external URLs. Accepts 200, 206, 403, 429 status codes (403/429 tolerated to handle rate-limiting). Excludes `.github/**`.

### 4.5 `security-dependencies.yml`
Triggers: PR to `main`, weekly Monday 07:00 UTC, `workflow_dispatch`

| Job | What it does |
|---|---|
| `dependency-review` | GitHub Dependency Review Action on PRs (detects newly introduced CVEs) |
| `pip-audit` | Runs `pip-audit` against `requirements-dev.txt`, `requirements-docs.txt`, and `learn/labs/requirements.txt` |

---

## 5. Validation Architecture

Three distinct validation layers for `.prompt.md` files:

```
Layer 1: STRUCTURE (shell)
  scripts/lint-prompt-frontmatter.sh
  - Checks frontmatter delimiter exists
  - Checks required YAML keys: mode, description, version
  - Checks cross-link pattern: "> **Learn why this works:**"
  - Checks required sections: "# Role", "# Task", "# Output Format"
  Invoked via: make lint / CI: prompt-frontmatter-lint job

Layer 2: SCHEMA (Python)
  scripts/validate-prompt-schema.py + prompts/shared/prompt-registry.schema.json
  - Validates frontmatter YAML against JSON Schema draft 2020-12
  - Checks type/length constraints on mode, description, version
  - Validates enum values for mode ('agent'|'edit'|'ask')
  - Checks semver pattern on version
  - Enforces: if deprecated=true, then superseded_by is required
  Invoked via: make validate / CI: indirectly via make check

Layer 3: TOKEN BUDGET (bash, advisory)
  Inline in lint-markdown.yml
  - Estimates tokens as chars/4
  - Warns if > 4000 tokens (never blocks CI)
```

**Gap**: Layers 1 and 2 both check that `mode`, `description`, `version` exist, but only Layer 2 checks their values. Optional fields (`tags`, `patterns`, `stack`) are validated by Layer 2 only when present.

---

## 6. Lab Architecture (`learn/labs/`)

```
labs/
├── lab_utils.py              Shared client abstraction + mock
├── requirements.txt          openai>=1.12.0, python-dotenv>=1.0.0
├── .env.example              API key examples
├── lab_0N_<topic>.py         Standalone Python scripts
├── lab_0N_<topic>.ipynb      Jupyter notebooks (same content, dual format)
└── failure-gallery/          Deliberately broken prompts for exercises
```

**Provider detection** in `lab_utils.py` (priority order):
1. `GOOGLE_API_KEY` → Gemini 2.0 Flash (via OpenAI-compatible endpoint)
2. `GROQ_API_KEY` → Llama 3.1 8B Instant
3. `OPENAI_API_KEY` → GPT-4o Mini
4. `OPENAI_API_BASE` + `OPENAI_API_KEY` → Any compatible endpoint

**CI mode** (`LABS_SKIP_API=1`): `get_client()` returns `_MockClient`, which has deterministic keyword-matching responses for each lab scenario.

**Notebook smoke tests**: `scripts/run-notebook-smoke.py` uses `nbclient` to execute each `lab_*.ipynb` in-process. Interactive setup cells are replaced with `MOCK_SETUP_CELL` at runtime. Timeout: 180s per notebook.

---

## 7. Key Architectural Decisions

### Decision: Symlink-based `docs_src/` instead of file copying
**Why**: Avoids content duplication. Edits to `learn/` or `prompts/` are immediately reflected in the docs build without a sync step.
**Trade-off**: Linux/macOS only. CI must always run `make sync` before `mkdocs build`.
**ADR**: Not formally captured — see `Makefile` comments.

### Decision: Two-script validation (shell + Python)
**Why**: Shell script runs in CI without Python env setup; Python script provides richer JSON Schema validation.
**Trade-off**: Some redundancy in checking `mode`/`description`/`version` existence.

### Decision: Dual format labs (`.py` + `.ipynb`)
**Why**: `.py` files are version-control friendly (no JSON diff noise); `.ipynb` files provide interactive experience with Jupyter.
**Trade-off**: Must maintain both files in sync (currently manual).

### Decision: OpenAI-compatible client wrapper
**Why**: Supports Google Gemini, Groq, and OpenAI through one interface; free-tier-first approach lowers barrier to entry.
**Trade-off**: Mock client uses string matching — adding new lab prompts requires updating `_mock_text_response()`.

---

## 8. File Modification Impact Analysis

| File | Impact of change | Required follow-up |
|---|---|---|
| Any `.prompt.md` | Affects end-user usage; version bump required if behavior changes | `make lint`, `make validate` |
| `prompts/shared/prompt-registry.schema.json` | Changes validation rules for ALL prompt files | `make validate` on all files |
| `learn/0N-*.md` | Curriculum content change | Check cross-references from `.prompt.md` files |
| `references.md` | Citation key changes break `[BibKey]` refs in `learn/` | Search all `.md` files in `learn/` |
| `scripts/lint-prompt-frontmatter.sh` | Changes CI blocking behavior | Test locally; audit existing prompt files |
| `Makefile` | Build/CI workflow changes | Test all `make` targets |
| `mkdocs.yml` | Nav/theme changes | `make build` |
| `docs_src/**` | **Should not be edited** — symlinks | Use `make sync` |
| `learn/labs/lab_utils.py` | Affects all labs; mock changes affect CI | Run notebook smoke tests |
