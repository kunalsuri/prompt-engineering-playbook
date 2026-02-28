---
mode: 'agent'
description: 'Analyze the provided project files and generate an updated root README.md for Python projects.'
version: '1.1.0'
changelog:
  - version: '1.1.0'
    date: '2025-06-01'
    changes: 'Expanded file-analysis scope and improved section-generation logic'
  - version: '1.0.0'
    date: '2025-01-15'
    changes: 'Initial release'
---

> **Learn why this works:** [Constrained Output + Specificity](../../../learn/03-patterns.md#36-pattern-5-constrained-output)

> **Shared base instructions:** #file:../../shared/readme-generator-base.md
> Apply all shared Role, Scope, Goal, Formatting Rules, and Output Format from that file.
> The stack-specific overrides below take precedence where they differ.

# Task

Generate an updated root `README.md` for this Python project, incorporating the stack-specific conventions below.

# Stack-Specific Overrides — Python

## Role
Act as a **Technical Writer LLM** specializing in clear and accurate software documentation **for Python projects**.

## Requirements (additions to shared base)
- **Tech stack**: Python and related packages

## Output Format
- Output the full updated `README.md` inside one fenced Markdown block.
- After the block, provide a **concise checklist** of changes made compared to the previous README (if provided).
