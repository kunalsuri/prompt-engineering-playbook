# CONTRIBUTING_AI.md — AI-Agent Contribution Guide

> This guide is specifically for AI agents (Claude Code, GitHub Copilot, GPT, Gemini, or similar automation). For human contributor guidelines, see [CONTRIBUTING.md](../CONTRIBUTING.md).
> Relocated to `.ai/` to save workspace context tokens and keep the repository root clean.

---

## Scope: What AI Agents Can Safely Do Here

### ✅ Safe to do autonomously

- Fix typos and broken links in `learn/`, `prompts/`, and root documentation files
- Add `# Constraints`, `# Examples`, or `# Anti-Patterns` sections to existing `.prompt.md` files
- Update citation keys in `learn/` files when `references.md` has the entry
- Fix YAML frontmatter errors in `.prompt.md` files (missing fields, wrong types)
- Update version numbers in `.prompt.md` frontmatter when behavior changes
- Add new lab exercises to `learn/labs/failure-gallery/` (broken-prompt + solution pairs)
- Improve inline comments in `lab_utils.py` and scripts

### ⚠️ Do with human review

- Add new `.prompt.md` files — requires full validation and README update
- Add new `learn/` modules or major sections — requires citation verification
- Modify `prompts/shared/prompt-registry.schema.json` — affects all prompt file validation
- Modify `scripts/lint-prompt-frontmatter.sh` — changes CI blocking behavior
- Modify `Makefile` targets — affects all developer workflows
- Add entries to `references.md` — must be verified APA format with valid DOI/URL

### ❌ Do not do

- Edit any file inside `docs_src/` — it is a symlink layer, not a content source
- Create symlinks inside `learn/`, `prompts/`, or `assets/` (recursive symlink risk)
- Commit notebook outputs — `nbstripout` removes them, but committing them causes diff noise
- Remove or rename existing citation keys in `references.md` — they are referenced throughout `learn/`
- Add hardcoded API keys, secrets, or internal URLs to any file
- Change `mode:` values without understanding VS Code Copilot mode semantics
- Bump the `version:` field in `.prompt.md` for whitespace/typo changes (only for behavior changes)

---

## Prompt Template Quality Contract

When creating or modifying a `.prompt.md` file, verify every item:

### Required frontmatter
```yaml
---
mode: 'agent'           # 'agent' | 'edit' | 'ask'
description: 'Clear, specific description (10–500 chars)'
version: '1.0.0'        # semver MAJOR.MINOR.PATCH
---
```

### Required cross-link (immediately after closing `---`)
```markdown
> **Learn why this works:** [Pattern Name](../../../learn/03-patterns.md#exact-anchor)
```
- Anchor must match the actual heading in the module file
- Path depth `../../../` is correct for `prompts/<stack>/prompts/*.prompt.md` — verify for each location

### Required body sections (in this order)
```markdown
# Role
<Who the model should act as — imperative, domain-specific>

# Task
<What to do — imperative verbs, explicit success criteria>

# Output Format
<Schema, template, or structured description of expected output>
```

### Strongly recommended sections
```markdown
# Constraints
<"Do not..." instructions — prevent the most common failure modes>

# Examples
<At least one input/output pair if the format is non-obvious>
```

### Validation commands
```bash
make lint       # Must show OK: for the file
make validate   # Must exit 0
```

---

## Citation Rules for `learn/` Content

- All empirical claims (accuracy numbers, latency figures, benchmark results) need a citation key: `[AuthorYear]`
- All technique attributions need a citation key: `[Brown2020]` for few-shot, `[Wei2022]` for CoT, etc.
- Citation keys must exist in `references.md` — check before using
- Format: `[Brown2020]` not `(Brown, 2020)` or `(Brown et al., 2020)`
- Purely instructional examples (exercises, fictional scenarios) do not need citations
- Performance figures must be labeled: either "(from [Source])" for exact figures or "(approximate, for illustration)" for pedagogical examples

---

## Commit Message Format

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

| Type | Use for |
|---|---|
| `feat` | New prompt template, new module section, new comparison doc |
| `fix` | Correcting errors in existing content (factual, code, formatting) |
| `docs` | Documentation-only changes (README, GETTING-STARTED, etc.) |
| `refactor` | Restructuring without content changes |
| `chore` | Dependency updates, CI config, tooling changes |
| `test` | Adding or updating evaluation test cases, lab exercises |

**Scope examples:** `curriculum`, `python`, `react-ts`, `fastapi`, `nodejs-ts`, `shared`, `scripts`, `refs`

---

## File Naming Conventions

### `.prompt.md` files
- Pattern: `<verb>-<noun>.prompt.md`
- Lowercase, hyphen-separated
- Verb describes primary action; noun describes artifact
- ✅ `generate-unit-tests.prompt.md`
- ❌ `tests.prompt.md` (too vague)
- ❌ `generateUnitTests.prompt.md` (camelCase)

### `learn/` files
- Modules: `0N-<topic>.md` (two-digit, zero-padded)
- Comparisons: `<technique>-comparison.md`
- ADRs: `00N-<short-title>.md`
- Labs: `lab_0N_<topic>.py` and `lab_0N_<topic>.ipynb` (matching names)

---

## When Modifying Lab Files

### If editing `lab_utils.py`
- `_mock_text_response()` uses keyword matching against system/user prompts
- If you add a new lab scenario that needs mock support, add a new branch in `_mock_text_response()`
- The mock must return a string that parses correctly for whatever the lab expects
- Run notebook smoke tests: `LABS_SKIP_API=1 LLM_MODEL=mock-labs python scripts/run-notebook-smoke.py`

### If adding a new Jupyter notebook
- Create matching `.py` file with identical content
- Add `LABS_SKIP_API` guard: check `os.getenv("LABS_SKIP_API") == "1"` before API calls, or rely on `lab_utils.complete()` which handles this automatically
- Strip outputs before committing (pre-commit hook handles this, but verify)

### If adding to the failure gallery
- Each case needs: `broken-prompt.md` and `solution.md`
- Case naming: `0N-<failure-category>/` (zero-padded, hyphenated)
- Reference the corresponding module section in `solution.md`
- Add the case to `learn/labs/failure-gallery/README.md`

---

## Checking Your Work

```bash
# After any change to .prompt.md files:
make lint && make validate

# After any change to learn/ or prompts/:
make sync-check

# After any change to scripts/ or lab notebooks:
LABS_SKIP_API=1 LLM_MODEL=mock-labs python scripts/run-notebook-smoke.py

# Full check (matches CI):
make check
```

---

## Red Lines: Things That Break CI

1. `.prompt.md` missing `mode:`, `description:`, or `version:` → `prompt-frontmatter-lint` fails
2. `.prompt.md` missing `> **Learn why this works:**` → `prompt-frontmatter-lint` fails
3. `.prompt.md` missing `# Role`, `# Task`, or `# Output Format` → `prompt-frontmatter-lint` fails
4. Broken internal relative links in `*.md` → `markdown-link-check` fails
5. `docs_src/` symlinks broken (e.g., renamed a source file) → `docs-sync-check` fails
6. Self-referential symlinks in tracked paths → `recursive-symlink-check` fails
7. MkDocs fails to render (broken nav ref, bad Mermaid syntax, etc.) → `docs-build` fails
8. Notebook cell raises exception → `notebook-smoke` fails

> Items 1–3 are the most common. Run `make lint` before every push.
