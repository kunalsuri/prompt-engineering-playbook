# DEVELOPMENT_WORKFLOW.md — Prompt Engineering Playbook

> Step-by-step workflows for common development tasks. Optimized for both humans and AI agents.

---

## Prerequisites

```bash
# Required: Python 3.12+, git, make
# Recommended: Node.js (for some stacks), VS Code with GitHub Copilot

# First-time setup
git clone https://github.com/kunalsuri/prompt-engineering-playbook.git
cd prompt-engineering-playbook

python3 -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\activate           # Windows (limited support — see note below)
pip install -r requirements-docs.txt -r requirements-dev.txt

# Install pre-commit hooks (strips notebook outputs automatically)
pip install pre-commit
pre-commit install
```

> **Windows note**: `make sync`, `make lint`, and `make validate` require POSIX tools (`bash`, `ln`). Use WSL, Git Bash, or GitHub Actions CI as the authoritative check. Core content editing (Markdown, YAML) works natively.

---

## Workflow 1: Edit Curriculum Content

**When to use**: Fixing errors, adding sections, adding exercises to `learn/` modules.

```bash
# 1. Create a branch
git checkout -b docs/expand-module-3-exercises

# 2. Edit the canonical file
# Example: learn/03-patterns.md

# 3. Verify any new citations exist in references.md
grep -n "\[NewKey\]" learn/03-patterns.md
# If key is new, add it to references.md first

# 4. Rebuild docs to check rendering
make sync && make build
# Fix any MkDocs errors before proceeding

# 5. Commit
git add learn/03-patterns.md
git commit -m "docs(curriculum): add exercises to Module 3 patterns"

# 6. Push and open PR
git push origin docs/expand-module-3-exercises
```

**CI checks triggered**: `lint-markdown.yml` (links, docs-sync, docs-build)

---

## Workflow 2: Add a New Prompt Template

**When to use**: Creating a new `.prompt.md` for an existing stack.

```bash
# 1. Create a branch
git checkout -b feat/python-add-security-audit-prompt

# 2. Create the file (correct location and naming)
# Location: prompts/<stack>/prompts/<verb>-<noun>.prompt.md
# Example: prompts/python/prompts/audit-security.prompt.md

# 3. Write the file with required structure:
cat > prompts/python/prompts/audit-security.prompt.md << 'EOF'
---
mode: 'agent'
description: 'Audit Python code for security vulnerabilities (OWASP Top 10)'
version: '1.0.0'
tags: [security, audit, python]
stack: python
patterns: [role-playing, constrained-output]
---

> **Learn why this works:** [Role-Playing + Constrained Output](../../../learn/03-patterns.md#35-pattern-4-role-playing-persona-assignment)

# Role

...

# Task

...

# Output Format

...

# Constraints

...
EOF

# 4. Lint — must show OK: for the new file
make lint

# 5. Schema validation — must exit 0
make validate

# 6. Update the stack README
# Add entry to prompts/python/prompts/README.md

# 7. Test the prompt against at least 3 representative inputs
# (Manual step — document results in PR description)

# 8. Commit
git add prompts/python/prompts/audit-security.prompt.md prompts/python/prompts/README.md
git commit -m "feat(python): add security audit prompt"

# 9. Push and open PR
git push origin feat/python-add-security-audit-prompt
```

**CI checks triggered**: `lint-markdown.yml` (frontmatter lint, schema, token budget, links)

---

## Workflow 3: Add a New Technology Stack

**When to use**: Adding Go, Rust, Java, etc. as a new stack.

```bash
# 1. Create directory structure
mkdir -p prompts/<stack>/prompts

# 2. Create copilot-instructions.md
# Model it after prompts/python/copilot-instructions.md

# 3. Create at least one .prompt.md (follow Workflow 2)

# 4. Create prompts/<stack>/prompts/README.md
# List all prompt files with descriptions

# 5. Create prompts/<stack>/README.md (optional but recommended)
# Link to copilot-instructions and prompts/README.md

# 6. Update root README.md
# Add row to the "Available Stacks" table

# 7. Update CONTRIBUTING.md
# Add to the "Choose a Stack Directory" table

# 8. Update scripts/setup.sh
# Add the new stack to VALID_STACKS array and stack_label()

# 9. Create scripts/<stack>/setup.sh (optional — for stack-specific steps)

# 10. Add schema entry for the new stack (if using stack: field)
# Update prompts/shared/prompt-registry.schema.json
# Add new stack value to the "stack" enum

# 11. Full validation
make lint && make validate && make check
```

---

## Workflow 4: Run Labs Locally

**When to use**: Testing or developing lab exercises.

```bash
# Setup lab environment
cd learn/labs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy and configure API keys
cp .env.example .env
# Edit .env and add one of:
#   GOOGLE_API_KEY=...   (free — recommended)
#   GROQ_API_KEY=...     (free)
#   OPENAI_API_KEY=...   (paid)

# Run a Python lab directly
python lab_01_zero_vs_few_shot.py

# Run with Jupyter
pip install jupyter
jupyter notebook lab_01_zero_vs_few_shot.ipynb

# Run in CI mode (no API calls, deterministic mock)
LABS_SKIP_API=1 LLM_MODEL=mock-labs python lab_01_zero_vs_few_shot.py
```

**Important**: Never commit notebooks with outputs. The pre-commit hook strips them, but verify:
```bash
# Strip notebook outputs manually if needed
pip install nbstripout
nbstripout learn/labs/lab_01_zero_vs_few_shot.ipynb
```

---

## Workflow 5: Fix Broken Documentation Links

**When to use**: After renaming files or reorganizing directories.

```bash
# Find all internal links in Markdown
grep -r "\[.*\](\..*\.md" learn/ prompts/ *.md

# Or run the link checker locally (requires npm)
npx markdown-link-check --config .github/workflows/mlc-config.json learn/01-introduction.md

# Fix broken links by updating relative paths
# Then verify:
make sync-check
make build
```

**CI check**: `lint-markdown.yml` → `markdown-link-check` job

---

## Workflow 6: Update Documentation Site

**When to use**: Verifying doc rendering, adding new pages to navigation.

```bash
# Start live-reload dev server
make serve
# Open http://127.0.0.1:8000 in browser
# Edit files — changes render automatically

# Build static site
make build
# Output: _site/ directory

# Check that docs_src/ symlinks are correct
make sync-check

# Check for recursive symlinks (safety check)
make recursive-symlink-check
```

**Note**: `mkdocs.yml` must be updated if you add new top-level pages to the navigation.

---

## Workflow 7: Run Full Validation Suite

**When to use**: Before opening a PR; before merging.

```bash
# Ensure you're in .venv
source .venv/bin/activate

# Run everything
make check
# This runs: lint → validate → sync-check → recursive-symlink-check → build

# Notebook smoke tests (separate — not in make check)
LABS_SKIP_API=1 LLM_MODEL=mock-labs python scripts/run-notebook-smoke.py

# Expected output
# All checks passed.
# All notebook smoke tests passed.
```

---

## Workflow 8: Add a Lab Exercise

**When to use**: Adding a new lab to `learn/labs/`.

```bash
# 1. Choose a lab number (next sequential)
# Example: lab_07_<topic>

# 2. Create both files (they must be kept in sync)
touch learn/labs/lab_07_<topic>.py
touch learn/labs/lab_07_<topic>.ipynb

# 3. Follow the pattern in existing labs:
#    - Import lab_utils
#    - Use lab_utils.complete() for LLM calls
#    - Use lab_utils.print_header() for output sections
#    - Guard API-dependent code with LABS_SKIP_API check (automatic via lab_utils)

# 4. If your lab needs new mock responses:
#    - Add the scenario to lab_utils._mock_text_response()
#    - Or add a new mock function and wire it in

# 5. Test in CI mode
LABS_SKIP_API=1 LLM_MODEL=mock-labs python learn/labs/lab_07_<topic>.py

# 6. Run notebook smoke tests
LABS_SKIP_API=1 LLM_MODEL=mock-labs python scripts/run-notebook-smoke.py

# 7. Strip notebook outputs before committing
nbstripout learn/labs/lab_07_<topic>.ipynb

# 8. Update learn/labs/README.md with the new lab entry
```

---

## Workflow 9: Add a Failure Gallery Case

**When to use**: Adding a new deliberately broken prompt for the diagnostic exercise gallery.

```bash
# 1. Create the case directory (next sequential number)
mkdir -p learn/labs/failure-gallery/06-<failure-category>

# 2. Create the broken prompt
cat > learn/labs/failure-gallery/06-<failure-category>/broken-prompt.md << 'EOF'
# Broken Prompt: <Title>

> **Symptoms:** <What goes wrong when this prompt is used>
> **Anti-Pattern:** <Name from Module 4 or elsewhere>
> **Module Reference:** <e.g., Module 4 §4.5>

---

[The deliberately broken prompt content here]
EOF

# 3. Create the solution
cat > learn/labs/failure-gallery/06-<failure-category>/solution.md << 'EOF'
# Solution: <Title>

## Diagnosis

**Anti-pattern:** ...
**Broken element:** ...
**Root cause:** ...

## Fixed Prompt

[Corrected prompt here]

## Why the Fix Works

[Explanation citing module sections]
EOF

# 4. Update the gallery README
# Add a row to the Case Index table in:
# learn/labs/failure-gallery/README.md
```

---

## Workflow 10: Release a New Version

**When to use**: Tagging a new release (vX.Y.Z).

```bash
# 1. Update CHANGELOG.md
# Move [Unreleased] items to a new versioned section
# Format: ## [X.Y.Z] - YYYY-MM-DD

# 2. Update CITATION.cff
# Bump version: field and date-released: field

# 3. Update .zenodo.json
# Bump version field

# 4. Commit
git add CHANGELOG.md CITATION.cff .zenodo.json
git commit -m "chore: release vX.Y.Z"

# 5. Tag
git tag vX.Y.Z
git push origin main --tags

# 6. GitHub Actions will deploy docs automatically
# Zenodo will archive automatically on the GitHub release
```

---

## Command Reference

| Command | Description |
|---|---|
| `make help` | Show all available targets |
| `make install` | Install/refresh all Python dependencies |
| `make sync` | Create `docs_src/` symlinks |
| `make sync-check` | Verify symlinks resolve correctly |
| `make recursive-symlink-check` | Ensure no self-referential symlinks |
| `make lint` | Validate `.prompt.md` structure (shell) |
| `make validate` | Validate `.prompt.md` schema (Python) |
| `make build` | Build MkDocs site → `_site/` |
| `make serve` | Start MkDocs dev server (live-reload) |
| `make check` | Run full suite: lint + validate + sync-check + recursive-check + build |
| `LABS_SKIP_API=1 python scripts/run-notebook-smoke.py` | Run notebook smoke tests (CI mode) |
| `bash scripts/setup.sh --stack python <target-dir>` | Install Python stack templates |
| `bash scripts/setup.sh --list` | List available stacks |
| `bash scripts/setup.sh --dry-run --stack python` | Preview without writing |
