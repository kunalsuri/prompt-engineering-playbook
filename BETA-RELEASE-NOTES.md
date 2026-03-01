# Beta Release Notes (March 2026)

## Release Status

This repository is now publicly available as a **beta release**.

This beta is intended for:

- Developers using prompt files with VS Code + GitHub Copilot
- Educators teaching practical prompt engineering workflows
- Teams evaluating reusable prompt templates and learning materials

This beta is **not** intended to be a final benchmark authority for model-to-model performance comparisons.

---

## What’s Included in This Beta

- Seven-module curriculum in `learn/`
- Reusable stack-specific prompt templates in `prompts/`
- Setup and validation scripts in `scripts/`
- MkDocs documentation site and CI quality gates
- Centralized bibliography in `references.md`

---

## Known Limitations

- Some cross-model comparison guidance is a research synthesis and includes approximate figures for pedagogical use.
- Model behavior can drift over time as providers update model versions.
- Not all empirical claims are currently enforced by automated citation linting.
- Reproducibility artifacts for all “validated against” statements are still being expanded.

---

## Usage Guidance for Beta Readers

- Treat benchmark-style comparisons as directional guidance, not guarantees.
- Re-run evaluations on your own model versions, prompts, and datasets before production rollout.
- Use the provided evaluation patterns to validate task-specific reliability in your environment.

---

## Short-Term Hardening Plan

The next release cycle will prioritize:

1. Stronger citation and empirical-claim validation in CI
2. Expanded reproducibility artifacts for model validation claims
3. Tightened dependency/reproducibility controls for local and CI runs
4. Additional script/runtime tests for non-Markdown surfaces

---

## Feedback and Issue Reporting

- General improvements: open a GitHub issue or pull request
- Security-related concerns: use the private security advisory path in `SECURITY.md`

---

## Release Positioning (Suggested Copy)

> The Prompt Engineering Playbook is released as a beta educational framework and template library. It is stable for learning and practical team adoption, while selected comparison and validation surfaces continue to be hardened for high-scrutiny research-style review.