# Codacy Integration — Shared Instructions

> **Location:** `prompts/shared/codacy.instructions.md`
> **Version:** 1.0.0
> **Last updated:** 2026-02-21
>
> This is the single source of truth for Codacy configuration across all technology stacks.
> Stack-specific directories should reference this file rather than maintaining independent copies.

---

## Overview

Codacy is used for automated code quality analysis across all projects in this repository. The following instructions define the shared Codacy configuration and conventions that apply regardless of technology stack.

## Code Quality Standards

All code must pass Codacy analysis with zero critical or major issues before merging. Minor issues should be addressed in the same PR when feasible, or tracked as follow-up tasks with explicit ticket references.

## Configuration

Codacy analysis is configured via the repository-level `.codacy.yml` file. Stack-specific overrides (e.g., disabling Python-specific rules for TypeScript-only directories) should be added to the `exclude_paths` section rather than disabling rules globally.

## Conventions

- **Complexity threshold**: Cyclomatic complexity must not exceed 10 per function. Functions exceeding this threshold should be decomposed.
- **Duplication threshold**: Code duplication above 3% triggers a warning. Duplicated logic should be extracted into shared utilities.
- **Coverage gate**: New code must maintain or improve the existing coverage percentage. PRs that reduce coverage require explicit justification in the PR description.
- **Security analysis**: Codacy's security patterns are enabled for all stacks. Findings classified as "Security" must be resolved before merge — no exceptions.

## Stack-Specific Notes

For Python projects, Codacy integrates with `ruff` and `mypy` output. Ensure your local linting passes before pushing to avoid redundant Codacy findings.

For TypeScript projects, Codacy integrates with ESLint output. The repository's `.eslintrc` configuration should be consistent with Codacy's rule set to prevent conflicting feedback.

## Troubleshooting

If Codacy reports false positives, suppress them using inline annotations appropriate to the language (`# codacy:ignore` for Python, `// codacy:ignore` for TypeScript) and document the rationale in a comment on the same line.
