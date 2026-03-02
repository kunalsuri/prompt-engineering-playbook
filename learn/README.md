# 🎓 Learn Prompt Engineering

A structured, seven-module curriculum for mastering prompt engineering — from foundational concepts through advanced techniques and autonomous agent architectures. No prior prompt engineering experience is assumed.

---

## Choose Your Path

| Path | Who It's For | Start Here |
| --- | --- | --- |
| **Beginner / Non-Programmer** | High-school students, writers, researchers, or anyone new to AI | **[Beginner's Reading Guide](beginners-guide.md)** — a curated path through the curriculum with plain-language signposts and code-free exercise alternatives |
| **Developer / CS Practitioner** | Graduate students, professional developers, and prompt engineers | Continue below with the full Learning Roadmap |

---

## Learning Roadmap

Start at Module 1 and work through in order. Each module builds on the previous one and includes 2–3 hands-on exercises.

| Module | Topic | You'll Learn | Level | Time |
|--------|-------|-------------|-------|------|
| **[00 — Orientation](00-orientation.md)** | Narrative On-Ramp | A story-first guide that shows prompt improvement in action — no jargon, no code | Beginner | 15 min |
| **[01 — Introduction](01-introduction.md)** | What & Why | What prompt engineering is, the anatomy of a prompt, naive vs. engineered prompts | Beginner | 30 min |
| **[02 — Core Principles](02-core-principles.md)** | How to Think | Specificity, decomposition, iteration, evaluation — the four pillars | Beginner–Intermediate | 45 min |
| **[03 — Patterns](03-patterns.md)** | What to Use | Zero-shot, few-shot, chain-of-thought, role-playing, constrained output, ReAct | Intermediate | 60 min |
| **[04 — Best Practices](04-best-practices.md)** | Production Skills | Token management, version control for prompts, team workflows, anti-patterns | Intermediate–Advanced | 45 min |
| **[05 — Advanced Patterns](05-advanced-patterns.md)** | Cutting Edge | RAG, prompt injection defense, multimodal prompting, evaluation pipelines | Advanced | 60 min |
| **[06 — Agentic Patterns](06-agentic-patterns.md)** | Autonomous Agents | Plan-and-execute, reflection loops, multi-agent collaboration, memory, tool-use design, agent safety | Advanced | 60 min |

**Total estimated time: ~6 hours** (reading + exercises). Add ~20 hours for the full Research Extension Track, or ~2 day for the optional lab experiments.

---

## Deep-Dive Comparisons

After completing the modules (or when referenced from within them), these standalone analyses provide detailed, research-backed comparisons of specific techniques.

| Document | Compares |
|----------|----------|
| [Chain-of-Thought Comparison](comparisons/chain-of-thought-comparison.md) | Few-Shot CoT vs. Zero-Shot CoT vs. Self-Consistency CoT |
| [ReAct Comparison](comparisons/react-comparison.md) | ReAct (reasoning + acting) vs. standard prompting |
| [Instruction Tuning Comparison](comparisons/instruction-tuning-comparison.md) | FLAN, T0, InstructGPT approaches |
| [PromptSource Comparison](comparisons/promptsource-comparison.md) | Template-based vs. freeform prompting |
| [Few-Shot Comparison](comparisons/few-shot-comparison.md) | Zero-shot, one-shot, and few-shot strategies |
| [Adversarial Robustness Comparison](comparisons/adversarial-robustness-comparison.md) | Attack types, defenses, and safety-aware prompting |
| [Automatic Prompt Optimization](comparisons/automatic-prompt-optimization.md) | DSPy, OPRO, APE, and PromptBreeder — when to automate vs. hand-craft |
| [Cross-Model Portability](comparisons/cross-model-portability.md) | GPT-4o, Claude 3.5, Gemini 1.5, Llama 3 — behavioral differences and portable prompt strategies |

---

## Worked Examples

| Document | What It Covers |
|----------|---------------|
| [Prompt Patterns in Practice](prompt-examples/prompt-patterns-in-practice.md) | One worked example for each of the six patterns from Module 3, showing naive vs. pattern-applied prompts |
| [Advanced Patterns in Practice](prompt-examples/advanced-patterns-in-practice.md) | Worked examples for Module 5: RAG grounding, injection-resistant system prompts, evaluation pipelines, and multimodal UI review |

---

## Glossary

Unfamiliar with a term? The **[Glossary](glossary.md)** provides concise definitions for all key terms used across the curriculum — from "token" and "context window" to "RAG" and "prompt injection."

---

## Quick Reference

Want to track your progress? Fork or download the **[Progress Tracker](progress-tracker.md)** — a one-page checklist for every module, lab, comparison doc, and research paper in the curriculum.

Need a refresher without re-reading an entire module? The **[Cheat Sheet](cheatsheet.md)** provides a one-page reference card covering all five prompt components, six patterns, four principles, five anti-patterns, and a copy-paste prompt template.

Prompt not working? The **[Prompt Debugging Guide](prompt-debugging.md)** provides a systematic decision tree for diagnosing failures — fifteen failure categories, a diagnostic flowchart, and targeted fix strategies for each.

Want to use LLMs to write better prompts? The **[Meta-Prompting Guide](meta-prompting.md)** covers prompt generation, evaluation, and refinement — with copy-paste templates and a four-step workflow.

Ready to add prompts to your CI pipeline? The **[CI/CD Integration Guide](ci-cd-integration.md)** covers regression testing, schema validation, security scanning, and complete GitHub Actions workflows.

Looking for ready-to-use prompts? The **[Prompt Cookbook](cookbook.md)** provides 20 copy-paste prompts for everyday non-programming tasks — writing, analysis, research, communication, and decision-making — each tagged with the patterns it uses.

New to prompt engineering but already have LLM calls in your code? The **[Prompt Engineering for Your Existing Codebase](prompt-engineering-existing-codebase.md)** guide walks you through auditing, scoring, and incrementally improving prompts without a full rewrite.

Want to see good vs. bad prompts side-by-side? The **[Before & After Gallery](before-and-after-gallery.md)** shows 15 prompt comparisons organized by task — no pattern jargon required.

Want to understand *why* prompt design decisions were made? The **[Architecture Decision Records](decisions/README.md)** document the reasoning behind four real-world prompt design choices, with alternatives considered and trade-offs accepted.

Want to read the primary research? The **[Research Extension Track](research/README.md)** provides curated study guides for 15 foundational papers — with summaries, discussion questions, and connections back to the curriculum.

---

## Hands-On Labs

Ready to experiment with a real API? The **[Labs](labs/README.md)** directory contains six runnable Python experiments that let you observe prompt-engineering concepts first-hand:

| Lab | Concept | Module Link |
|-----|---------|-------------|
| [Lab 1 — Zero-Shot vs. Few-Shot](labs/lab_01_zero_vs_few_shot.py) | Classification with/without examples | Module 3 §3.2–§3.3 |
| [Lab 2 — Chain-of-Thought](labs/lab_02_chain_of_thought.py) | Step-by-step reasoning | Module 3 §3.4 |
| [Lab 3 — Specificity Spectrum](labs/lab_03_specificity.py) | Vague → moderate → specific prompts | Module 2 §2.1 |
| [Lab 4 — Evaluation Pipeline](labs/lab_04_evaluation_pipeline.py) | LLM-as-Judge scoring | Module 5 §5.4 |
| [Lab 5 — Tool-Calling & Structured Output](labs/lab_05_tool_calling.py) | JSON-mode vs. function-calling reliability | Module 5 §5.4 + Module 3 §3.6 |
| [Lab 6 — Plan-and-Execute Agent](labs/lab_06_agentic_plan_execute.py) | Planner + Executor agent in pure Python | Module 6 §6.2 |

See the [Lab README](labs/README.md) for setup instructions.

---

## Exercise Solutions

Finished the exercises? Compare your work against the **[Reference Solutions](solutions/exercise-solutions.md)** for all 20 exercises across Modules 1–6. (Module 0 is a narrative on-ramp with no exercises.) Exercises marked **(Exemplar)** show one valid approach — your answers may differ and still be correct.

---

## Prerequisites

**For the developer path (full roadmap):** You should be comfortable with at least one programming language (Python or TypeScript preferred) and have basic familiarity with what large language models are.

**For the beginner path:** No programming experience is required — just curiosity and access to any LLM (ChatGPT free tier, Claude free tier, Google Gemini, or similar). See the [Beginner's Reading Guide](beginners-guide.md) for the recommended route.

If you have access to an LLM, you'll get the most out of the exercises. No prior prompt engineering experience is required for either path.

---

## How This Connects to the Prompt Templates

Throughout these modules, you'll encounter cross-references to real production prompts in the [`prompts/`](../prompts/README.md) directory. These are not decorative — they show you how the concepts you're learning are applied in practice. For example, Module 3 references the cybersecurity audit prompt to demonstrate multi-pattern composition, and Module 5 references the safety-gate prompt to illustrate constrained output and LLM-as-judge patterns.

---

## Citation

All empirical claims are cited using entries in [`references.md`](../references.md). Performance figures are explicitly flagged as either exact (from a cited source) or approximate (for pedagogical purposes). See the bibliography for DOIs and stable URLs.

---

[← Back to main README](../index.md) · [Start Module 1 →](01-introduction.md)
