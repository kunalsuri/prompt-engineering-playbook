# Contributing to Prompt Engineering Playbook

Thank you for your interest in contributing to this repository. This document describes the standards, workflows, and review criteria for contributions. Whether you are fixing a typo, expanding the curriculum, or adding a new prompt template, please read this guide before submitting a pull request.

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold a respectful and inclusive environment for all contributors.

---

## What You Can Contribute

**Curriculum improvements** — expanding or correcting content in the `learn/` modules, adding exercises, improving explanations, or fixing inaccuracies. This is the highest-value contribution area.

**New prompt templates** — adding task-specific prompt files (`.prompt.md`) for existing or new technology stacks. New prompts must meet the quality criteria described in the Prompt Review Checklist below.

**Comparison documents** — adding or improving deep-dive analyses in `learn/comparisons/`. These must include proper APA citations referencing entries in `references.md`.

**Bug fixes and maintenance** — correcting broken links, outdated tool versions, formatting issues, or inconsistencies across files.

**Script improvements** — enhancing the setup and utility scripts in `scripts/`.

---

## Development Workflow

### 1. Fork and Clone

Fork this repository to your GitHub account, then clone your fork locally:

```bash
git clone https://github.com/<your-username>/prompt-engineering-playbook.git
cd prompt-engineering-playbook
```

### 2. Create a Feature Branch

Create a branch from `main` with a descriptive name following the pattern `<type>/<short-description>`:

```bash
git checkout -b feat/add-rag-comparison
git checkout -b fix/update-python-tool-versions
git checkout -b docs/expand-module-3-exercises
```

### 3. Make Your Changes

Follow the formatting and quality guidelines described in the sections below. For curriculum content, ensure your additions integrate smoothly with the existing module structure and cross-references.

### 4. Commit with Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This enables automated changelog generation and provides a clear project history.

**Format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**

| Type | Usage |
|------|-------|
| `feat` | A new prompt template, curriculum module, or comparison document |
| `fix` | Correcting an error in existing content (factual, code, or formatting) |
| `docs` | Documentation-only changes (README, GETTING-STARTED, CONTRIBUTING) |
| `refactor` | Restructuring files without changing content (e.g., consolidating duplicates) |
| `chore` | Maintenance tasks (updating tool versions, CI config, dependencies) |
| `test` | Adding or updating evaluation test cases |

**Scopes** (optional but encouraged):

| Scope | Files Affected |
|-------|---------------|
| `curriculum` | `learn/` modules and exercises |
| `comparisons` | `learn/comparisons/` |
| `python` | `prompts/python/` templates |
| `react-ts` | `prompts/react-typescript/` templates |
| `fastapi` | `prompts/react-fastapi/` templates |
| `shared` | `prompts/shared/` |
| `nodejs-ts` | `prompts/nodejs-typescript/` templates |
| `scripts` | `scripts/` |
| `refs` | `references.md` |

**Examples:**
```
feat(curriculum): add exercises to Module 3 patterns

Add three hands-on exercises covering pattern identification,
pattern selection, and few-shot prompt design. Each exercise
includes clear success criteria and estimated completion time.

Closes #42
```

```
fix(python): update ruff version from 0.4.x to 0.8.x

The copilot-instructions.md file referenced ruff 0.4.x which
is now outdated. Updated to 0.8.x and verified all rule
references remain valid.
```

```
docs: add GETTING-STARTED.md tutorial

New guided tutorial explaining the VS Code Copilot prompt-file
mechanism, template selection workflow, and end-to-end usage
example. Addresses #35.
```

### 5. Submit a Pull Request

Push your branch to your fork and open a pull request against `main`. In the PR description, include the following:

- **What** — a concise summary of the change.
- **Why** — the motivation (e.g., addresses an audit finding, fills a gap, fixes an error).
- **Testing** — how you verified the change (e.g., ran prompts against a model, checked links, verified formatting).
- **Checklist** — confirm that all items in the relevant review checklist (below) are satisfied.

---

## Formatting Standards

### Markdown Files

All Markdown files must render correctly on GitHub and in VS Code's built-in preview. Follow these conventions:

- Use ATX-style headers (`#`, `##`, `###`). Do not skip header levels.
- Use fenced code blocks with language identifiers (` ```python `, ` ```bash `, ` ```json `).
- Wrap prose at a reasonable line length (80–120 characters) for readable diffs. Do not use hard wraps within paragraphs if your editor supports soft wrapping.
- Use `---` (horizontal rule) to separate major sections.
- Internal links should use relative paths: `[Module 3](learn/03-patterns.md)`, not absolute URLs.

### Prompt Files (`.prompt.md`)

Prompt files must include YAML frontmatter with `mode`, `description`, and `version` fields:

```yaml
---
mode: 'agent'
description: 'Brief description of what this prompt does'
version: '1.0.0'
---
```

The body of the prompt file should follow the structural patterns established by the existing templates: clear role assignment, explicit constraints, defined output format, and anti-pattern guidance where applicable. See Module 3 (`learn/03-patterns.md`) for the pattern vocabulary.

### Citations and References

All factual claims, empirical figures, and technique attributions in curriculum and comparison documents must be cited. Use the citation key format defined in `references.md` (e.g., `[Wei2022]`, `[Brown2020]`). If your contribution references a work not yet in `references.md`, add it in APA 7th edition format with a DOI or stable URL.

Performance numbers must be explicitly flagged as either (a) exact figures from a cited source, or (b) approximate/illustrative figures for pedagogical purposes.

---

## How to Add a Prompt Template

This section walks you through creating a new production-ready prompt template from scratch.

### 1. Choose a Stack Directory

Prompt files typically live under `prompts/<stack>/prompts/`. Current stacks:

| Stack | Directory |
|-------|-----------|
| Python | `prompts/python/prompts/` |
| React + TypeScript | `prompts/react-typescript/prompts/` |
| React + FastAPI | `prompts/react-fastapi/prompts/` |
| Node.js + TypeScript | `prompts/nodejs-typescript/prompts/` |
| Shared (stack-agnostic resources) | `prompts/shared/` |

To add a new stack, create the directory tree, a `copilot-instructions.md`, and a `README.md` following the pattern in an existing stack folder.

### 2. Name the File

Use the pattern `<verb>-<noun>.prompt.md`, where the verb describes the primary action and the noun describes the target artifact. Keep names lowercase and hyphen-separated.

**Good names:** `generate-unit-tests.prompt.md`, `review-pull-request.prompt.md`, `refactor-api-handler.prompt.md`
**Avoid:** `tests.prompt.md` (too vague), `generateUnitTestsForPythonFunctions.prompt.md` (camelCase, too long)

### 3. Add Required YAML Frontmatter

Every `.prompt.md` file **must** begin with these three fields:

```yaml
---
mode: 'agent'          # or 'edit' or 'ask' — see VS Code Copilot docs
                       # Valid values: 'agent', 'edit', 'ask'
description: 'One-sentence description of what this prompt does.'
version: '1.0.0'       # semantic version; bump when behavior changes
---
```

Use semantic versioning:
- **Patch** (`1.0.x`) — typos, wording clarifications that do not change model behaviour.
- **Minor** (`1.x.0`) — new sections, new constraints, new output requirements.
- **Major** (`x.0.0`) — complete rewrites or breaking changes to expected output structure.

### 4. Write the Required Sections

Every prompt body must contain the following headings (in this order):

```markdown
# Role

# Task

# Output Format
```

Additional sections (`# Constraints`, `# Examples`, `# Anti-Patterns`) are strongly encouraged but not enforced by CI.

### 5. Add the Learn↔Prompts Cross-Link

Directly below the YAML frontmatter closing `---`, add a blockquote that links to the curriculum module explaining the pattern used in the prompt:

```markdown
> **Learn why this works:** Pattern name → ../../../learn/03-patterns.md#<real-anchor>
```

To find the correct anchor: open `learn/03-patterns.md` (or whichever module is most relevant), locate the heading, convert it to a GitHub-slug anchor:
- lowercase everything
- replace spaces and punctuation other than hyphens with hyphens
- collapse consecutive hyphens to one
- strip leading/trailing hyphens

Example: `## 3.2 Pattern 2 — Role Assignment` → `#32-pattern-2-role-assignment`

### 6. Validate Locally

```bash
# Lint frontmatter, cross-link, and required sections for all prompt files:
./scripts/lint-prompt-frontmatter.sh

# Or use the Makefile shortcut:
make lint
```

Fix any `FAIL:` lines before pushing. CI will reject the PR if this check fails.

### 7. Sync to docs_src/

If you also edit any file under `learn/` or `prompts/`, run:

```bash
make sync
```

This mirrors `learn/` → `docs_src/learn/` and `prompts/` → `docs_src/prompts/` so that the MkDocs build stays consistent. CI will fail the `docs-sync-check` job if these trees differ.

---

## Prompt Review Checklist

Before submitting a new or modified prompt template, verify the following:

- [ ] **Role assignment** — the prompt assigns a clear, appropriate role (or deliberately omits one with justification).
- [ ] **Task specification** — the task is described with imperative verbs and unambiguous success criteria.
- [ ] **Output format** — the expected output structure is explicitly defined (schema, template, or verbal description).
- [ ] **Constraints** — all constraints are internally consistent (no contradictions between different sections of the prompt).
- [ ] **Negative instructions** — the prompt includes relevant "do not" instructions to prevent common failure modes.
- [ ] **Token budget** — the prompt fits comfortably within the target model's context window, leaving room for file content and response.
- [ ] **YAML frontmatter** — the `.prompt.md` file includes valid YAML frontmatter with `mode`, `description`, and `version` fields. Use semantic versioning (e.g., `version: '1.0.0'`). Bump the version when the prompt's behavior changes.
- [ ] **Testing** — the prompt has been tested against at least three representative inputs, and the outputs meet the evaluation rubric (see `prompts/shared/evaluation-template.md`).
- [ ] **No secrets** — the prompt contains no API keys, passwords, internal URLs, or other sensitive information.
- [ ] **No duplication** — the prompt does not duplicate content that exists in the shared instructions (`copilot-instructions.md` or `prompts/shared/`). Shared content should be referenced, not copied.

---

## Curriculum Content Checklist

Before submitting new or modified curriculum content (`learn/` modules or comparisons):

- [ ] **Learning objectives** — the module opens with clear, measurable learning objectives.
- [ ] **Progressive structure** — content builds from simpler to more complex concepts, with explicit bridges to prerequisite and follow-up modules.
- [ ] **Worked examples** — at least one concrete, worked example demonstrates each key concept.
- [ ] **Cross-references** — connections to comparison documents, production templates, and other modules are explicitly noted.
- [ ] **Exercises** — at least two exercises are included, each with clear instructions and implicit or explicit success criteria.
- [ ] **Citations** — all claims are properly cited using `references.md` entries.
- [ ] **Audience calibration** — content is appropriate for the target audience (graduate students, postdocs, researchers, and professional developers; no prior prompt engineering experience assumed). Neither too elementary nor assumes niche domain expertise without explanation.

---

## Review Process

All pull requests require at least one approving review before merge. Reviewers will evaluate contributions against the relevant checklist above and may request revisions. The repository maintainer has final approval authority.

For prompt template contributions, reviewers are encouraged to independently test the prompt against at least one input not in the contributor's test set.

---

## Questions?

If you are unsure whether a contribution is in scope or how to structure it, open a GitHub Issue with the `question` label. We are happy to provide guidance before you invest time in a pull request.

---

## Repository Tooling

### Codacy Configuration (`.codacy/`)

The `.codacy/` directory contains configuration files for [Codacy](https://www.codacy.com/) — a code-quality platform that runs automated analysis on pull requests. The directory includes:

- `codacy.yaml` — top-level Codacy project configuration
- `cli-config.yaml` — Codacy CLI settings
- `cli.sh` — helper script for running the Codacy CLI locally
- Tool-specific configs for ESLint, Markdownlint, Pylint, Shellcheck, Stylelint, etc.

These files are maintained by the repository owner and generally do not require changes from contributors. If you modify linting rules or add new file types, you may need to update the corresponding tool config in `.codacy/`.
