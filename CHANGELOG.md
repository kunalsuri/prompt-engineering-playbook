# Changelog

All notable changes to this repository are documented in this file. This project follows [Semantic Versioning](https://semver.org/) adapted for prompt files: a **major** version indicates a behavioral change in prompt output, a **minor** version adds new capabilities without altering existing behavior, and a **patch** version covers typos, clarifications, and formatting fixes.

---

## [Unreleased]

### Added — Curriculum (`learn/`)

- **Module 0 — Orientation** (`learn/00-orientation.md`): Story-first narrative on-ramp for non-technical learners; no jargon, no code.
- **Module 6 — Agentic Patterns** (`learn/06-agentic-patterns.md`): Plan-and-execute, reflection loops, multi-agent collaboration, memory systems, tool-use design, and agent safety. Includes exercises.
- **Eight comparison documents** (up from six): added Automatic Prompt Optimization and Cross-Model Portability.
- **Advanced worked examples** (`learn/prompt-examples/advanced-patterns-in-practice.md`): RAG grounding, injection-resistant system prompts, evaluation pipelines, multimodal UI review.
- **Nine supplementary guides**: cheatsheet, prompt debugging, meta-prompting, CI/CD integration, cookbook (20 recipes), before-and-after gallery, existing-codebase guide, progress tracker, glossary expansion.
- **Six runnable labs** (`learn/labs/`): Jupyter notebooks and Python scripts for zero-vs-few-shot, chain-of-thought, specificity, evaluation pipeline, tool-calling, and plan-and-execute agent.
- **Failure gallery** (`learn/labs/failure-gallery/`): Five broken-prompt diagnostic cases with solutions.
- **Four architecture decision records** (`learn/decisions/`): Few-shot over fine-tuning, split planner-executor, add safety gate, structured output schema.
- **Research extension track** (`learn/research/`): Curated study guides for 15 foundational papers.

### Added — Prompt Templates (`prompts/`)

- **Node.js + TypeScript stack** (4 prompts): `create-api-endpoint`, `review-code`, `write-tests`, `generate-openapi-spec`. All at version `1.0.0` with `mode: 'agent'`.
- **Node.js + TypeScript base instructions** (`prompts/nodejs-typescript/copilot-instructions.md`): Node.js 20 LTS+, TypeScript 5.x strict mode, vitest, zod validation.

### Added — Infrastructure

- **Node.js + TypeScript setup script** (`scripts/nodejs-typescript/setup.sh`).
- **Prompt registry JSON schema** (`prompts/shared/prompt-registry.schema.json`): Validates `.prompt.md` YAML frontmatter with conditional rules.
- **Schema validation script** (`scripts/validate-prompt-schema.py`): Validates all prompt files against the registry schema.
- **MkDocs documentation site** with Material theme, GitHub Pages deployment workflow, and live-reload development server.

### Changed

- Updated module count from "five-module" / "six-module" to "seven-module" across all documentation.
- Updated README directory tree to include `nodejs-typescript` stack.
- Added CODEOWNERS entry for `/prompts/nodejs-typescript/`.
- Removed recursive/self-referential symlinks (`learn/learn`, `prompts/prompts`, `docs/assets/assets`) that caused MkDocs path recursion and unstable builds.
- Hardened local and CI validation with explicit recursive-symlink checks plus a full MkDocs build gate in `.github/workflows/lint-markdown.yml`.
- Fixed contradictory constraints in `prompts/nodejs-typescript/prompts/generate-openapi-spec.prompt.md` and bumped to `1.1.0`.
- Updated `prompts/react-typescript/prompts/safety-gate-llm.prompt.md` to remove explicit chain-of-thought output requirements and bumped to `1.1.0`.
- Corrected markdown formatting in `prompts/nodejs-typescript/copilot-instructions.md` by removing erroneous wrapper code fences.
- Clarified `CONTRIBUTING.md` guidance for symlink-based docs sync and citation scope for empirical vs narrative content.

---

## [1.1.0] — 2026-02-21

### Changed — Prompt Templates

- **Deduplicated README-generator prompts.** The three stack-specific `update-generate-readme.prompt.md` prompts (Python, React + TypeScript, React + FastAPI) now reference a shared base file at `prompts/shared/readme-generator-base.md` via `#file:` directives, reducing total maintained lines from ~106 to ~50. Each prompt retains only its stack-specific overrides (role suffix, tech stack, setup sections).
- **Version bumped** all three README-generator prompts from `1.0.0` → `1.1.0` to reflect the structural change.

### Added — Shared Resources

- **`prompts/shared/readme-generator-base.md`** — New shared base document containing the common Role, Scope Rules, Goal, Requirements, Formatting Rules, and Output Format used by all README-generator prompts.

---

## [1.0.0] — 2026-02-21

### Added — Curriculum (`learn/`)

- **Five-module curriculum** covering prompt engineering from first principles through advanced techniques:
  - Module 1: Introduction (prompt anatomy, motivating examples)
  - Module 2: Core Principles (specificity, decomposition, iteration, evaluation)
  - Module 3: Patterns (zero-shot, few-shot, chain-of-thought, role-playing, constrained output, ReAct)
  - Module 4: Best Practices (token management, version control, team workflows, anti-patterns, CI/CD)
  - Module 5: Advanced Patterns (RAG, adversarial robustness, multimodal prompting, evaluation pipelines, cross-model portability)
- **Six comparison documents** (`learn/comparisons/`) providing deep-dive analyses of specific techniques: Chain-of-Thought variants, ReAct vs. standard prompting, Few-Shot strategies, Instruction Tuning approaches, PromptSource template-based prompting, and Adversarial Robustness.
- **Worked examples** (`learn/prompt-examples/prompt-patterns-in-practice.md`) demonstrating all six Module 3 patterns with naive vs. pattern-applied comparisons.
- **Exercise solutions** (`learn/solutions/exercise-solutions.md`) for all 16 exercises across the five modules.
- **Beginner's reading guide** (`learn/beginners-guide.md`) with phased reading order and code-free exercise alternatives for Modules 4–5.
- **Glossary** (`learn/glossary.md`) with 30+ terms cross-referenced to curriculum sections.

### Added — Prompt Templates (`prompts/`)

- **Python stack** (7 prompts): `create-feature`, `debug-issue`, `generate-docs`, `refactor-code`, `review-code`, `write-tests`, `update-generate-readme`. All at version `1.0.0` with `mode: 'agent'`.
- **React + TypeScript stack** (8 prompts): `auditor-best-practices`, `auditor-codebase-maturity`, `auditor-cybersecurity-features`, `auto-code-implementation`, `create-chatbot-ollama`, `create-saas-app-V2`, `safety-gate-llm`, `update-generate-readme`. All at version `1.0.0` with `mode: 'agent'`.
- **React + FastAPI stack** (3 prompts): `create-app-react-fastapi`, `create-test-suite`, `update-generate-readme`. All at version `1.0.0` with `mode: 'agent'`.
- **Stack-specific base instructions** (`copilot-instructions.md`) for each stack.

### Added — Shared Resources (`prompts/shared/`)

- **`codacy.instructions.md`** — Single source of truth for Codacy code-quality configuration.
- **`evaluation-template.md`** — Four-part evaluation framework with manual rubric, automated pipeline schema, LLM-as-Judge integration, and A/B testing protocol.

### Added — Infrastructure

- **Setup scripts** (`scripts/`) for Python, React + TypeScript, and React + FastAPI stacks.
- **Frontmatter linting** (`scripts/lint-prompt-frontmatter.sh`) validating `mode`, `description`, and `version` fields in all `.prompt.md` files.
- **GitHub Actions workflow** (`.github/workflows/lint-markdown.yml`) with Markdown link checking and prompt frontmatter validation.
- **CODEOWNERS**, **CONTRIBUTING.md**, **GETTING-STARTED.md**, **LICENSE** (MIT), and centralized **references.md** bibliography.

### Design Decisions

- **Modular architecture.** Prompts are organized into stack-specific directories with a shared layer, following the layered architecture described in Module 4 §4.4.
- **Curriculum–template integration.** Modules cross-reference production prompt files to demonstrate concepts in practice (e.g., Module 3 references `auditor-cybersecurity-features.prompt.md` for multi-pattern composition).
- **Dual-audience design.** The `learn/` directory serves both beginners (via `beginners-guide.md`) and developers (via the full learning roadmap).
