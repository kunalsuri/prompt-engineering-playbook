---
mode: 'agent'
description: 'Analyze the provided project files and generate an updated root README.md for Full-Stack (React + Python) projects.'
version: '1.1.0'
---

> **Learn why this works:** [Constrained Output + Specificity](../../../learn/03-patterns.md#36-pattern-5-constrained-output)

> **Shared base instructions:** #file:../../shared/readme-generator-base.md
> Apply all shared Role, Scope, Goal, Formatting Rules, and Output Format from that file.
> The stack-specific overrides below take precedence where they differ.

# Task

Generate an updated root `README.md` for this React + FastAPI project, incorporating the stack-specific conventions below.

# Stack-Specific Overrides — React + FastAPI (Full-Stack)

## Role
Act as a **Technical Writer LLM** specializing in documentation **for full-stack web applications** (React/TypeScript Frontend + Python/FastAPI Backend).

## Goal
Generate a clean, accurate, and developer-friendly `README.md` that reflects the **current** state of the **monorepo**.

## Requirements (replaces shared base Requirements)
The README must include:

- **Project Title & Description**: One-line summary of the SaaS/App.
- **Key Features**: Derived strictly from visible React features and Python endpoints.
- **Tech Stack**:
  - **Frontend**: React, TypeScript, Vite, Tailwind, State Management (Zustand/Query).
  - **Backend**: Python, FastAPI, Pydantic, Storage (JSON/SQL).
- **Monorepo Structure**: A text-based tree highlighting `frontend/` and `backend/` directories.
- **Getting Started** (Split into two clear sections):
  1.  **Backend Setup**: Python version, venv creation, requirements installation.
  2.  **Frontend Setup**: Node version, `npm/yarn` install.
- **Running the App**: Exact commands to start both servers (e.g., `uvicorn` and `npm run dev`) and port numbers.
- **Environment Config**: Mention `.env` requirements for both sides.

## Formatting Rules (additions to shared base)
- Use **Tabs** or **Accordions** if instructions are lengthy.

## Output Format
- Output the full updated `README.md` inside one fenced Markdown block.
- After the block, provide a **concise checklist** of changes made.
