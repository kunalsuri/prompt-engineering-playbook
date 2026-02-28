# PromptSource: Template-Based vs. Freeform Prompting

**Level:** Intermediate

This document compares the template-based prompting approach formalized by PromptSource [Bach2022] with freeform (ad hoc) prompting, and examines how structured prompt templates affect consistency, reusability, and model performance.

---

## Overview

**Freeform prompting** is how most users interact with LLMs: they type a natural-language instruction tailored to the immediate task, with no predefined structure. The prompt is created on the fly and typically used once.

**Template-based prompting** uses predefined prompt structures with placeholders for variable inputs. PromptSource [Bach2022] formalized this approach by creating an integrated development environment (IDE) for writing, sharing, and evaluating prompt templates, resulting in the Public Pool of Prompts (P3) — a crowdsourced collection of templates covering 170+ NLP datasets.

---

## Freeform Prompting

**How it works.** The user writes a prompt from scratch for each task, using natural language and their own judgment about structure, specificity, and format.

**Example:**
```
Tell me if this movie review is positive or negative:
"The cinematography was stunning but the plot made absolutely no sense."
```

**Strengths:**
- Maximum flexibility — can be adapted to any task instantly.
- Requires no infrastructure or template management.
- Natural and intuitive for one-off tasks.

**Weaknesses:**
- **Inconsistent across users.** Two people prompting for the same task will phrase it differently, potentially producing different results.
- **Not reusable.** Ad hoc prompts are rarely saved, versioned, or tested.
- **Difficult to evaluate systematically.** Without a fixed prompt structure, comparing results across runs or models is unreliable.
- **Prone to under-specification.** Users often omit constraints, format requirements, or edge-case handling.

---

## Template-Based Prompting (PromptSource)

**Source:** Bach et al. (2022) [Bach2022]

**How it works.** A prompt template defines a fixed structure with placeholders (variables) that are filled at inference time. The template specifies the exact framing, instruction wording, and output format for a task.

**Example template (from PromptSource):**
```
Given the following review: "{{review_text}}"
Is the sentiment of this review positive or negative?
|||
{{answer_choices[label]}}
```

The `|||` separator divides the input template from the output template. `{{review_text}}` and `{{answer_choices[label]}}` are variables populated from the dataset.

**Key findings from Bach et al. [Bach2022]:**
- PromptSource collected over 2,000 prompt templates for 170+ NLP datasets, contributed by a community of researchers.
- Templates were used to train T0 [Sanh2022], demonstrating that template-diverse training improves zero-shot generalization.
- The same task expressed through different templates produced significantly different model performance, highlighting the importance of prompt design even in controlled settings.
- High-quality templates consistently outperformed hastily written ones.

**Strengths:**
- **Consistency.** Every invocation of the same template produces structurally identical prompts, enabling fair comparison and evaluation.
- **Reusability.** Templates can be shared across teams, projects, and organizations.
- **Testability.** Fixed prompt structures enable systematic evaluation with test suites (see the [evaluation template](../../prompts/shared/evaluation-template.md)).
- **Version control.** Templates are text artifacts that can be stored in Git, reviewed, and iterated on — exactly the practice demonstrated by this repository's `.prompt.md` files.

**Weaknesses:**
- **Upfront design effort.** Creating a high-quality template requires more thought than writing an ad hoc prompt.
- **Rigidity.** Templates may not accommodate unexpected input variations without modification.
- **Over-engineering risk.** For one-off tasks, the overhead of template design is not justified.

---

## Side-by-Side Comparison

| Dimension | Freeform Prompting | Template-Based Prompting |
|-----------|-------------------|-------------------------|
| **Setup effort** | None | Moderate (design + test) |
| **Consistency across runs** | Low | High |
| **Reusability** | Low | High |
| **Testability** | Difficult | Straightforward |
| **Version control** | Rarely practiced | Natural fit |
| **Flexibility** | Maximum | Constrained by template |
| **Best for** | Exploration, one-off tasks | Production workflows, team settings |
| **Skill required** | Low | Moderate (template design) |

---

## How This Repository Applies Template-Based Prompting

The `.prompt.md` files in this repository's [`prompts/`](../../prompts/) directory are template-based prompts designed for VS Code Copilot. They follow the PromptSource philosophy of structured, reusable, versioned prompt artifacts:

- Each prompt file defines a fixed structure with role assignment, constraints, and output format.
- YAML frontmatter (`mode: 'agent'`, `description: '...'`) provides metadata, similar to PromptSource's template annotations.
- Prompts are stored in Git and subject to review (see [CONTRIBUTING.md](../../CONTRIBUTING.md)).
- The [evaluation template](../../prompts/shared/evaluation-template.md) provides a rubric for systematic assessment, closing the quality loop.

The key difference from PromptSource is that these prompts target code-generation and developer-workflow tasks (rather than NLP benchmarks), and they leverage VS Code Copilot's agent mode for tool use.

---

## Decision Framework

**Use freeform prompting when:**
- You are exploring a new task and don't yet know the best prompt structure.
- The task is genuinely one-off and will not be repeated.
- Speed of iteration matters more than consistency.

**Use template-based prompting when:**
- The prompt will be used repeatedly (by you or others).
- Consistent output format is required (e.g., for downstream processing).
- You need to evaluate and compare prompt variants.
- The prompt is part of a team workflow or production system.
- You want to benefit from version control and code review.

A common workflow is to **start freeform** (to explore the task and discover what works), then **crystallize into a template** once the prompt design stabilizes.

---

## Cross-References

- **Module 3** ([03-patterns.md](../03-patterns.md), §3.3) covers few-shot learning, where template design determines example quality.
- **Module 4** ([04-best-practices.md](../04-best-practices.md), §4.3) discusses version control for prompts — the production application of template-based thinking.
- The [Instruction Tuning Comparison](instruction-tuning-comparison.md) explains how T0 used PromptSource templates during training.

---

## References

- [Bach2022] Bach, S. H., et al. (2022). PromptSource: An integrated development environment and repository for natural language prompts. *ACL 2022 System Demonstrations*, 93–104.
- [Sanh2022] Sanh, V., et al. (2022). Multitask prompted training enables zero-shot task generalization. *ICLR*.

See [`references.md`](../../references.md) for full citations with DOIs.
