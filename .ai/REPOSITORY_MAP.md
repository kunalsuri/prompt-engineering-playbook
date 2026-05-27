# REPOSITORY_MAP.md — Prompt Engineering Playbook

> Complete navigable inventory of the repository. Last audited: 2026-05-27. Relocated to `.ai/` to optimize initial agent loading token budget and keep the repository root clean.

---

## Root Files

| File | Purpose | Edit? |
|---|---|---|
| `README.md` | Main entry point; quick nav, stack table, how-to | Yes (canonical) |
| `GETTING-STARTED.md` | End-user installation and usage walkthrough | Yes (canonical) |
| `CONTRIBUTING.md` | Human contributor guide | Yes (canonical) |
| `.ai/CONTRIBUTING_AI.md` | AI-agent contributor guide (relocated) | Yes |
| `CHANGELOG.md` | Version history (Keep a Changelog format) | Yes (append only) |
| `BETA-RELEASE-NOTES.md` | Beta-specific notes | Yes |
| `ROADMAP.md` | Planned features and future work | Yes |
| `TECHNICAL-REPORT.md` | Technical report on the playbook | Yes |
| `CLAUDE.md` | Claude Code context (root router) | Yes |
| `AGENT.md` | General AI agent context (root router) | Yes |
| `ARCHITECTURE.md` | Deep architecture documentation | Yes |
| `.ai/REPOSITORY_MAP.md` | This file | Yes |
| `DEVELOPMENT_WORKFLOW.md` | Step-by-step developer workflows | Yes |
| `LICENSE` | MIT License | No |
| `CODEOWNERS` | Code ownership rules | Yes (rare) |
| `CODE_OF_CONDUCT.md` | Contributor Covenant | No |
| `SECURITY.md` | Security reporting policy | Yes (rare) |
| `CITATION.cff` | Machine-readable citation metadata | Yes (on version) |
| `.zenodo.json` | Zenodo archival metadata | Yes (on release) |
| `Makefile` | Developer task runner | Yes (with care) |
| `mkdocs.yml` | MkDocs configuration | Yes (with care) |
| `requirements-docs.txt` | MkDocs build deps | Yes (with care) |
| `requirements-dev.txt` | Validation script deps | Yes (with care) |
| `.pre-commit-config.yaml` | Pre-commit hooks (nbstripout) | Yes |
| `.gitignore` | Git ignore rules | Yes |
| `index.md` | Root-level index (MkDocs entry?) | Verify |
| `references.md` | Centralized bibliography (APA) | Yes (append only) |

---

## `learn/` — Curriculum

### Core Modules

| File | Module | Key Topics |
|---|---|---|
| `learn/00-orientation.md` | 0 | Story-first on-ramp; no jargon |
| `learn/01-introduction.md` | 1 | What PE is; anatomy of a prompt; role/context/task/constraints/examples |
| `learn/02-core-principles.md` | 2 | Specificity, decomposition, iteration, evaluation |
| `learn/03-patterns.md` | 3 | Six patterns: zero-shot, few-shot, CoT, ReAct, role-playing, constrained output |
| `learn/04-best-practices.md` | 4 | Token budget, version control, team workflows, anti-patterns |
| `learn/05-advanced-patterns.md` | 5 | RAG, adversarial robustness, multimodal, evaluation pipelines |
| `learn/06-agentic-patterns.md` | 6 | Plan-and-execute, reflection loops, multi-agent, agent safety |

### Supporting Documents

| File | Purpose |
|---|---|
| `learn/README.md` | Module index and progression guide |
| `learn/glossary.md` | Definitions of all PE terminology used in the repo |
| `learn/cookbook.md` | 20 copy-paste recipes for everyday tasks |
| `learn/cheatsheet.md` | Quick reference card |
| `learn/progress-tracker.md` | Student self-tracking sheet |
| `learn/meta-prompting.md` | Prompts that generate prompts |
| `learn/prompt-debugging.md` | Debugging guide for broken prompts |
| `learn/ci-cd-integration.md` | Integrating prompts into CI/CD pipelines |
| `learn/prompt-engineering-existing-codebase.md` | PE for legacy/existing codebases |
| `learn/before-and-after-gallery.md` | Side-by-side prompt improvement examples |
| `learn/beginners-guide.md` | Simplified on-ramp |
| `learn/solutions/exercise-solutions.md` | Solutions for module exercises |

### Comparisons (`learn/comparisons/`)

| File | Topic |
|---|---|
| `adversarial-robustness-comparison.md` | Prompt injection and adversarial defense techniques |
| `automatic-prompt-optimization.md` | APO methods vs. manual engineering |
| `chain-of-thought-comparison.md` | CoT variants (standard, zero-shot CoT, self-consistency) |
| `cross-model-portability.md` | Prompt transferability across model families |
| `few-shot-comparison.md` | Few-shot vs. fine-tuning vs. RAG |
| `instruction-tuning-comparison.md` | RLHF / instruction-tuning context |
| `promptsource-comparison.md` | PromptSource and other template frameworks |
| `react-comparison.md` | ReAct vs. CoT vs. Tool-use patterns |

### Architecture Decision Records (`learn/decisions/`)

| File | Decision |
|---|---|
| `README.md` | ADR format and usage guide |
| `001-few-shot-over-fine-tuning.md` | Few-shot prompting vs fine-tuning for classification |
| `002-split-planner-executor.md` | Splitting monolithic prompt into planner + executor |
| `003-add-safety-gate.md` | Separate safety-gate validation prompt |
| `004-structured-output-schema.md` | JSON schema constraints vs. natural language format instructions |

### Research Track (`learn/research/`)

| File | Content |
|---|---|
| `README.md` | **15-paper reading track** covering foundations, reasoning, agents, safety, RAG, and reasoning models (o1/o3). Includes paper summaries, discussion questions, curriculum connections, and reading checklist. Mapped to [Brown2020], [Wei2022], [Yao2023], [Shinn2023], and 11 more. |

### Prompt Examples (`learn/prompt-examples/`)

| File | Content |
|---|---|
| `README.md` | Index |
| `prompt-patterns-in-practice.md` | Worked examples for Module 3 patterns |
| `advanced-patterns-in-practice.md` | Worked examples for Module 5 patterns |

### Labs (`learn/labs/`)

| File | Content |
|---|---|
| `README.md` | Lab index and setup instructions |
| `.env.example` | Template for API keys |
| `requirements.txt` | `openai>=1.12.0`, `python-dotenv>=1.0.0` |
| `lab_utils.py` | Shared client, `_MockClient`, `complete()`, helpers |
| `lab_01_zero_vs_few_shot.py` / `.ipynb` | Zero-shot vs. few-shot comparison |
| `lab_02_chain_of_thought.py` / `.ipynb` | Chain-of-thought prompting |
| `lab_03_specificity.py` / `.ipynb` | Specificity and constraint effects |
| `lab_04_evaluation_pipeline.py` / `.ipynb` | Building evaluation pipelines |
| `lab_05_tool_calling.py` / `.ipynb` | Tool/function calling patterns |
| `lab_06_agentic_plan_execute.py` / `.ipynb` | Plan-and-execute agent |

### Failure Gallery (`learn/labs/failure-gallery/`)

| Case | Anti-Pattern | Module Ref |
|---|---|---|
| `01-kitchen-sink/` | Overloaded multi-goal prompt | Module 4 §4.5 |
| `02-stale-context/` | Hallucination bait; missing grounding | Module 5 §5.1 |
| `03-injection-vulnerable/` | Unguarded system prompt | Module 5 §5.2 |
| `04-ambiguous-format/` | No output schema specified | Module 3 §3.6 |
| `05-missing-constraints/` | Absent role + constraints; vague task | Module 1 §1.3 + Module 2 §2.1 |

Each case: `broken-prompt.md` + `solution.md`

---

## `prompts/` — Reusable Templates

### `prompts/shared/`

| File | Purpose |
|---|---|
| `prompt-registry.schema.json` | JSON Schema (draft 2020-12) for `.prompt.md` frontmatter |
| `evaluation-template.md` | Evaluation rubric (manual + automated) |
| `readme-generator-base.md` | Base instructions for README generation |

### `prompts/python/`

| File | Purpose |
|---|---|
| `copilot-instructions.md` | Always-active Python standards (3.12+, ruff, mypy, pytest, Google docstrings) |
| `prompts/create-feature.prompt.md` | Generate a new Python feature/module |
| `prompts/debug-issue.prompt.md` | Debug and fix Python issues |
| `prompts/generate-docs.prompt.md` | Generate/improve documentation |
| `prompts/refactor-code.prompt.md` | Refactor Python code |
| `prompts/review-code.prompt.md` | Code review across 5 dimensions |
| `prompts/write-tests.prompt.md` | Generate pytest test suites |
| `prompts/update-generate-readme.prompt.md` | Update/generate README |
| `prompts/README.md` | Prompt index for this stack |

### `prompts/react-typescript/`

| File | Purpose |
|---|---|
| `copilot-instructions.md` | Always-active React+TypeScript standards |
| `prompts/auditor-best-practices.prompt.md` | Audit codebase against best practices |
| `prompts/auditor-codebase-maturity.prompt.md` | Assess codebase maturity |
| `prompts/auditor-cybersecurity-features.prompt.md` | Security audit |
| `prompts/auto-code-implementation.prompt.md` | Auto-implement features |
| `prompts/create-chatbot-ollama.prompt.md` | Create Ollama-backed chatbot |
| `prompts/create-saas-app-V2.prompt.md` | Scaffold SaaS app |
| `prompts/safety-gate-llm.prompt.md` | Safety gate for LLM outputs |
| `prompts/update-generate-readme.prompt.md` | Update/generate README |
| `prompts/README.md` | Prompt index for this stack |

### `prompts/react-fastapi/`

| File | Purpose |
|---|---|
| `copilot-instructions.md` | Always-active React+FastAPI standards |
| `prompts/create-app-react-fastapi.prompt.md` | Scaffold full-stack app |
| `prompts/create-test-suite.prompt.md` | Generate test suite |
| `prompts/update-generate-readme.prompt.md` | Update/generate README |
| `prompts/README.md` | Prompt index for this stack |

### `prompts/nodejs-typescript/`

| File | Purpose |
|---|---|
| `copilot-instructions.md` | Always-active Node.js+TypeScript standards |
| `prompts/create-api-endpoint.prompt.md` | Create API endpoint |
| `prompts/generate-openapi-spec.prompt.md` | Generate OpenAPI specification |
| `prompts/review-code.prompt.md` | Code review |
| `prompts/write-tests.prompt.md` | Generate test suite |
| `prompts/README.md` | Prompt index for this stack |

---

## `scripts/`

| File | Purpose | Run via |
|---|---|---|
| `setup.sh` | Unified stack installer for end users | `bash setup.sh --stack <stack>` |
| `lint-prompt-frontmatter.sh` | Validate `.prompt.md` structure | `make lint` |
| `validate-prompt-schema.py` | JSON schema validation | `make validate` |
| `run-notebook-smoke.py` | Execute notebooks in CI | `python scripts/run-notebook-smoke.py` |
| `docs-serve.sh` | Local docs server helper | `make serve` |
| `python/setup.sh` | Python stack installer | Called by `setup.sh` |
| `react-typescript/setup.sh` | React+TS stack installer | Called by `setup.sh` |
| `react-fastapi/setup.sh` | React+FastAPI stack installer | Called by `setup.sh` |
| `nodejs-typescript/setup.sh` | Node.js+TS stack installer | Called by `setup.sh` |

---

## `.github/`

| File/Directory | Purpose |
|---|---|
| `copilot-instructions.md` | Repo-level always-active Copilot instructions |
| `prompts/README.md` | Index for `.github/prompts/` |
| `workflows/deploy-docs.yml` | Deploy MkDocs to GitHub Pages |
| `workflows/lint-markdown.yml` | Lint Markdown, frontmatter, docs sync |
| `workflows/quality-nonmarkdown.yml` | Check scripts, notebooks, config |
| `workflows/link-check-external.yml` | Weekly external URL check |
| `workflows/security-dependencies.yml` | Dependency CVE scan |
| `workflows/mlc-config.json` | Markdown Link Check config (excludes external URLs) |
| `ISSUE_TEMPLATE/bug_report.md` | Bug report template |
| `ISSUE_TEMPLATE/curriculum_suggestion.md` | Curriculum improvement suggestion |
| `ISSUE_TEMPLATE/feature_request.md` | Feature request template |
| `PULL_REQUEST_TEMPLATE.md` | PR description template |
| `FUNDING.yml` | GitHub Sponsors config |
| `dependabot.yml` | Dependabot configuration |

---

## `docs_src/` — Generated Symlinks (Do Not Edit)

| Symlink | → Points to |
|---|---|
| `docs_src/index.md` | `README.md` |
| `docs_src/learn` | `learn/` |
| `docs_src/prompts` | `prompts/` |
| `docs_src/assets` | `assets/` |
| `docs_src/GETTING-STARTED.md` | `GETTING-STARTED.md` |
| `docs_src/CONTRIBUTING.md` | `CONTRIBUTING.md` |
| `docs_src/CHANGELOG.md` | `CHANGELOG.md` |
| `docs_src/BETA-RELEASE-NOTES.md` | `BETA-RELEASE-NOTES.md` |
| `docs_src/references.md` | `references.md` |
| `docs_src/LICENSE` | `LICENSE` |

---

## `assets/`

| File | Purpose |
|---|---|
| `assets/extra.css` | Custom CSS overrides for MkDocs Material theme |
| `assets/favicon.svg` | Site favicon |
