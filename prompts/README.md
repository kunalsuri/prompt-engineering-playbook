# ⚡ Prompt Templates

Production-ready prompt files for VS Code & GitHub Copilot. Pick your stack, copy the files into your project's `.github/` directory, and start using them immediately.

---

## Choose Your Stack

### 🐍 [Python](python/)

For Python applications — CLI tools, APIs, data pipelines, ML services.

**Base instructions:** [`python/copilot-instructions.md`](python/copilot-instructions.md)
Enforces Python 3.12+, modern type hints (`str | int`, `list[str]`), Google-style docstrings, `ruff` + `mypy` + `pytest` toolchain.

**Available prompts:**

| Prompt File | What It Does |
|------------|-------------|
| `create-feature.prompt.md` | Generate a new feature with types, docs, and tests |
| `review-code.prompt.md` | Review code for style, correctness, and edge cases |
| `write-tests.prompt.md` | Generate pytest test suite for existing code |
| `debug-issue.prompt.md` | Diagnose and fix a bug with step-by-step reasoning |
| ... | See [`python/prompts/`](python/prompts/) for the full list |

---

### ⚛️ [React + TypeScript](react-typescript/)

For frontend applications built with React and TypeScript.

**Base instructions:** [`react-typescript/copilot-instructions.md`](react-typescript/copilot-instructions.md)
Enforces strict TypeScript, functional components, Tailwind CSS, React Router v6 patterns.

**Available prompts:**

| Prompt File | What It Does |
|------------|-------------|
| `create-saas-app-V2.prompt.md` | Scaffold a complete SaaS application |
| `auditor-cybersecurity-features.prompt.md` | Multi-perspective security audit (OWASP/MITRE/NIST) |
| `auditor-best-practices.prompt.md` | Audit codebase for best practices |
| `auditor-codebase-maturity.prompt.md` | Assess codebase maturity |
| `safety-gate-llm.prompt.md` | LLM output validation with confidence scoring |
| `auto-code-implementation.prompt.md` | Autonomous code implementation agent |
| `create-chatbot-ollama.prompt.md` | Build an Ollama-powered chatbot |
| ... | See [`react-typescript/prompts/`](react-typescript/prompts/) for the full list |

---

### 🔗 [React + FastAPI Full-Stack](react-fastapi/)

For full-stack applications combining React/TypeScript frontend with Python FastAPI backend.

**Base instructions:** [`react-fastapi/copilot-instructions.md`](react-fastapi/copilot-instructions.md)
Covers both frontend and backend conventions, API contract design, Pydantic v2 schemas, CORS configuration, and deployment.

**Available prompts:**

| Prompt File | What It Does |
|------------|-------------|
| `create-app-react-fastapi.prompt.md` | Scaffold a complete full-stack application |
| ... | See [`react-fastapi/prompts/`](react-fastapi/prompts/) for the full list |

---

### 🟢 [Node.js + TypeScript](nodejs-typescript/)

For Node.js backend or full-stack applications using TypeScript.

**Base instructions:** [`nodejs-typescript/copilot-instructions.md`](nodejs-typescript/copilot-instructions.md)
Enforces Node.js 20 LTS+, TypeScript 5.x strict mode, `vitest`/`jest`, `zod` validation, ESLint with `@typescript-eslint`.

**Available prompts:**

| Prompt File | What It Does |
|------------|-------------|
| `create-api-endpoint.prompt.md` | Generate a new REST API endpoint with validation and tests |
| `review-code.prompt.md` | Review TypeScript/Node.js code for type safety and correctness |
| `write-tests.prompt.md` | Generate vitest/jest test suite for existing code |
| `generate-openapi-spec.prompt.md` | Generate OpenAPI 3.1 specification from route handlers |

---

## Shared Instructions

Files in [`shared/`](shared/) apply across all stacks. These should be copied once into your project's `.github/instructions/` directory.

| File | Purpose |
|------|---------|
| [`codacy.instructions.md`](shared/codacy.instructions.md) | Code quality standards, complexity thresholds, security gates || [`evaluation-template.md`](shared/evaluation-template.md) | Four-part prompt evaluation framework (manual rubric, automated pipeline, LLM-as-Judge, A/B testing) |
| [`readme-generator-base.md`](shared/readme-generator-base.md) | Shared base for all README-generator prompts (referenced via `#file:` directive) |
| [`prompt-registry.schema.json`](shared/prompt-registry.schema.json) | JSON Schema for validating `.prompt.md` YAML frontmatter |
---

## How to Install

**Step 1:** Copy the base instructions for your stack into `.github/copilot-instructions.md` in your project root. Copilot reads this file automatically on every interaction.

**Step 2:** Copy the prompt files you want into `.github/prompts/` in your project. Each `.prompt.md` file becomes available as a command in Copilot Chat.

**Step 3:** Copy shared instructions into `.github/instructions/`.

```bash
# Example: install React + TypeScript stack
mkdir -p .github/prompts .github/instructions

cp prompts/react-typescript/copilot-instructions.md  .github/copilot-instructions.md
cp prompts/react-typescript/prompts/*.prompt.md       .github/prompts/
cp prompts/shared/codacy.instructions.md              .github/instructions/
```

For the full walkthrough including customization and troubleshooting, see [GETTING-STARTED.md](../GETTING-STARTED.md).

---

[← Back to main README](../index.md)
