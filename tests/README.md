# tests/ — Tooling test-suite

This repository is educational content (Markdown + a small set of validation
scripts), so it has no application code to unit-test. What it *does* have is a
"test suite" made of validators — and **these tests test the validators**.

A linter that silently always passes is worse than no linter: it gives false
confidence while bad content merges. The suite below proves each validator
rejects the failure it claims to catch, not just that it accepts good input.

## What is covered

| Test file | Subject under test |
|---|---|
| `test_check_citations.py` | `scripts/check-citations.py` — citation-key grammar + undefined-key detection |
| `test_validate_prompt_schema.py` | `scripts/validate-prompt-schema.py` + the JSON schema — every rejection path (bad version, short description, bad mode/stack, unknown/missing keys) |
| `test_check_lab_sync.py` | `scripts/check-lab-sync.py` — AST helpers + the two drift conditions (missing import, constant mismatch) |
| `test_check_crosslinks.py` | `scripts/check-prompt-crosslinks.py` — GFM slugging + file/anchor resolution |
| `test_lab_utils.py` | `learn/labs/lab_utils.py` — the deterministic mock, provider detection, sandbox enforcement, `complete()` |
| `test_notebook_smoke.py` | `scripts/run-notebook-smoke.py` — interactive-cell → mock-cell sanitiser |
| `test_shell_linters.py` | `lint-prompt-frontmatter.sh` + `lint-copilot-instructions.sh` — exit codes on good vs. bad fixtures |
| `test_repo_integration.py` | All checkers run against the **real** repo content (drift guard) |

## Running

```bash
# From repo root, inside the project .venv:
make test          # pytest + coverage (term-missing report)
make check         # full suite: linters, validators, tests, docs build
make check-all     # check + notebook smoke tests (full local/CI parity)

# Directly:
.venv/bin/python -m pytest                 # quick
.venv/bin/python -m pytest --cov           # with coverage
```

## How the hyphen-named scripts are imported

Several scripts (`check-citations.py`, `validate-prompt-schema.py`,
`check-lab-sync.py`, `check-prompt-crosslinks.py`, `run-notebook-smoke.py`) have
hyphens in their names and cannot be imported with a normal `import` statement.
`conftest.py` provides `load_script_module("name.py")`, which loads them by path
via `importlib`. `lab_utils` and the `scripts/` directory are placed on
`pythonpath` by `pyproject.toml`.
