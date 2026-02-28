# Repository-Level Copilot Instructions

These instructions apply to all Copilot interactions within this repository.

## Project Context

This is the **Prompt Engineering Playbook** — an educational repository containing a seven-module curriculum on prompt engineering (`learn/`) and production-ready prompt templates for VS Code & GitHub Copilot (`prompts/`).

## Content Standards

- All curriculum content (`learn/`) must cite sources using citation keys from `references.md` (e.g., `[Wei2022]`, `[Brown2020]`).
- Performance figures must be explicitly flagged as either exact (from a cited source) or approximate (for pedagogical purposes).
- Prompt files (`.prompt.md`) must include YAML frontmatter with `mode`, `description`, and `version` fields. Use semantic versioning (e.g., `version: '1.0.0'`). Bump the version when the prompt's behavior changes.

## Formatting

- Use ATX-style Markdown headers (`#`, `##`, `###`). Do not skip header levels.
- Use fenced code blocks with language identifiers.
- Internal links use relative paths (e.g., `[Module 3](learn/03-patterns.md)`).
- Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Repository Structure

- `learn/` — Seven-module curriculum (Modules 0–6) and comparison documents
- `prompts/` — Production prompt templates organized by stack (python, react-typescript, react-fastapi, nodejs-typescript, shared)
- `scripts/` — Setup helper scripts
- `references.md` — Centralized bibliography