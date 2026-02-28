---
mode: 'agent'
description: 'Analyze the provided project files and generate an updated root README.md'
version: '1.1.0'
---

> **Learn why this works:** [Constrained Output + Specificity](../../../learn/03-patterns.md#36-pattern-5-constrained-output)

> **Shared base instructions:** #file:../../shared/readme-generator-base.md
> Apply all shared Role, Scope, Goal, Formatting Rules, and Output Format from that file.
> The stack-specific overrides below take precedence where they differ.

# Role

Technical Writer LLM specializing in documentation for React + TypeScript projects (see shared base for full role definition).

# Task

Generate an updated root `README.md` for this React + TypeScript project, incorporating the stack-specific conventions below.

# Stack-Specific Overrides — React + TypeScript

## Requirements (additions to shared base)
- **Tech stack**: React + TypeScript + listed libraries only

## Output Format
- Output the full updated `README.md` inside one fenced Markdown block.
- After the block, provide a **concise checklist** of changes made compared to the previous README (if provided).
