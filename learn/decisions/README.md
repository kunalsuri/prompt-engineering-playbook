# Prompt Design Architecture Decision Records (ADRs)

Architecture Decision Records are a lightweight method for capturing important
design decisions along with their context and consequences. In software
engineering, ADRs document choices about system architecture. Here we adapt
the format for **prompt engineering decisions** -- the choices we make when
designing, structuring, and orchestrating prompts in LLM-powered systems.

## Why prompt design ADRs?

Prompt engineering involves more trade-offs than most teams realise. Should you
use few-shot examples or fine-tune? One monolithic prompt or a multi-step
pipeline? Inline safety checks or a separate validation pass? The answers
depend on constraints that shift over time -- model capabilities, latency
budgets, data sensitivity, and team expertise.

ADRs capture **the reasoning behind a decision, not just the decision itself**.
Six months from now, when someone asks "why do we run two prompts instead of
one?", the ADR explains the context that led to that choice and the
alternatives that were weighed.

## Template structure

Every ADR in this directory follows a consistent template:

| Section                  | Purpose                                                |
|--------------------------|--------------------------------------------------------|
| **Status**               | Accepted, Superseded, or Deprecated                    |
| **Date**                 | When the decision was made                             |
| **Context module**       | Which curriculum module the decision relates to        |
| **Context**              | The situation, problem, and constraints                |
| **Decision**             | The specific approach chosen                           |
| **Rationale**            | Why this option over the alternatives                  |
| **Alternatives Considered** | Other options, their pros/cons, why they were rejected |
| **Consequences**         | Positive outcomes, negative trade-offs, and risks      |
| **Related Decisions**    | Links to other ADRs, modules, or prompt files          |

## How to use these records

- **Learning:** Read through the ADRs below to see how experienced prompt
  engineers reason about design trade-offs. Each record maps back to one or
  more curriculum modules so you can study the underlying principles.
- **Writing:** When you face a non-trivial prompt design choice on a real
  project, copy the template and fill it in. The discipline of writing down
  alternatives and consequences often clarifies your thinking before you commit
  to an approach.
- **Reviewing:** During prompt code review, reference relevant ADRs to explain
  why a particular pattern was chosen.

## Table of contents

| ADR | Title | Context Module |
|-----|-------|----------------|
| [001](001-few-shot-over-fine-tuning.md) | Few-shot prompting over fine-tuning for classification | Core Principles / Patterns |
| [002](002-split-planner-executor.md) | Split monolithic prompt into planner + executor pipeline | Advanced Patterns / Agentic Patterns |
| [003](003-add-safety-gate.md) | Add a separate safety-gate validation prompt | Best Practices |
| [004](004-structured-output-schema.md) | JSON schema constraints over natural language format instructions | Core Principles / Best Practices |

---

[Back to curriculum](../README.md)
