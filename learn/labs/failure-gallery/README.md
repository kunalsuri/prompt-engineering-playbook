# Failure Gallery — Diagnose and Fix Broken Prompts

> **Purpose:** Each subdirectory in this gallery contains a deliberately broken `.prompt.md` file, a description of its symptoms, and a blank `diagnosis.md` for you to fill in before reading the solution.

This gallery is meant to be used **alongside** the [Prompt Debugging Guide](../../prompt-debugging.md) and Module 4 §4.5 (Anti-Patterns). Each case corresponds to one named anti-pattern or failure category.

---

## How to Use This Gallery

1. Open a case's `broken-prompt.md` and read the prompt.
2. Without looking at `solution.md`, write down:
   - What failure category this belongs to (from the debugging guide)
   - What specific element(s) are missing or broken
   - How you would fix it
3. Save your answer in `diagnosis.md` (fill in the template).
4. Open `solution.md` and compare.

---

## Case Index

| Case | Anti-Pattern | Module Reference |
|------|-------------|-----------------|
| [01 — Kitchen Sink](01-kitchen-sink/) | Overloaded, multi-goal prompt | Module 4 §4.5 |
| [02 — Stale Context](02-stale-context/) | Hallucination bait; missing grounding | Module 5 §5.1 |
| [03 — Injection Vulnerable](03-injection-vulnerable/) | Unguarded system prompt | Module 5 §5.2 |
| [04 — Ambiguous Format](04-ambiguous-format/) | No output schema specified | Module 3 §3.6 |
| [05 — Missing Constraints](05-missing-constraints/) | Absent role + constraints; vague task | Module 1 §1.3 + Module 2 §2.1 |

---

## Scoring Rubric

When reviewing your diagnosis against the solution, score yourself on:

| Dimension | Points |
|-----------|--------|
| Correctly named the anti-pattern or failure category | 2 |
| Identified the specific broken element | 2 |
| Proposed a fix that addresses the root cause (not just symptoms) | 3 |
| Fix preserves what was good about the original prompt | 1 |
| **Total** | **8** |

A score of 6+ means you have a solid grasp of this failure mode. Below 4 means reviewing the referenced module section will help.

---

[← Back to Labs](../README.md) · [Prompt Debugging Guide](../../prompt-debugging.md)
