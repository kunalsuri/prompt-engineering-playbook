# Progress Tracker

> **How to use:** Fork or download this file. Check off items as you complete them. Items marked 🌟 are highest-priority for your learning path.

---

## Curriculum Modules

### Orientation & Foundations

- [ ] 🌟 [Module 0 — Orientation](00-orientation.md) — Story-first introduction *(15 min)*
- [ ] 🌟 [Module 1 — Introduction](01-introduction.md) — What & Why, prompt anatomy *(30 min)*
- [ ] 🌟 [Module 2 — Core Principles](02-core-principles.md) — Specificity, decomposition, iteration, evaluation *(45 min)*

### Patterns & Production Skills

- [ ] 🌟 [Module 3 — Patterns](03-patterns.md) — Zero-shot, few-shot, CoT, role-playing, ReAct *(60 min)*
- [ ] 🌟 [Module 4 — Best Practices](04-best-practices.md) — Token management, versioning, anti-patterns *(45 min)*

### Advanced & Agentic

- [ ] [Module 5 — Advanced Patterns](05-advanced-patterns.md) — RAG, injection defense, evaluation pipelines *(60 min)*
- [ ] [Module 6 — Agentic Patterns](06-agentic-patterns.md) — Agents, reflection, multi-agent systems *(60 min)*

---

## Exercises

### Module 1
- [ ] Exercise 1.1 — Prompt decomposition (five-component rewrite)
- [ ] Exercise 1.2 — Ambiguity identification
- [ ] Exercise 1.3 — Comparative analysis (naive vs. engineered)

### Module 2
- [ ] Exercise 2.1 — Specificity audit on an existing prompt
- [ ] Exercise 2.2 — Decomposition design (intra vs. inter-prompt)
- [ ] Exercise 2.3 — Iteration log (three revision cycles)

### Module 3
- [ ] Exercise 3.1 — Pattern identification in production prompts
- [ ] Exercise 3.2 — Pattern selection for four tasks
- [ ] Exercise 3.3 — Few-shot vs. zero-shot design comparison

### Module 4
- [ ] Exercise 4.1 — Token budget audit
- [ ] Exercise 4.2 — Prompt refactoring (eliminate duplication across prompt files)
- [ ] Exercise 4.3 — Anti-pattern identification and fix

### Module 5
- [ ] Exercise 5.1 — RAG prompt design for a technical support chatbot
- [ ] Exercise 5.2 — Red-team your own prompt (three attack types)
- [ ] Exercise 5.3 — Evaluation pipeline design (5-case test suite)
- [ ] Exercise 5.4 — Cross-model portability audit

### Module 6
- [ ] Exercise 6.1 — Plan-and-execute agent design
- [ ] Exercise 6.2 — Reflection loop applied to a previous exercise
- [ ] Exercise 6.3 — Multi-agent code review system design
- [ ] Exercise 6.4 — Memory management design for multi-session agent

---

## Hands-On Labs

- [ ] 🌟 [Lab 1 — Zero-Shot vs. Few-Shot](labs/lab_01_zero_vs_few_shot.py) *(10 min)*
- [ ] 🌟 [Lab 2 — Chain-of-Thought Impact](labs/lab_02_chain_of_thought.py) *(10 min)*
- [ ] [Lab 3 — Specificity Experiment](labs/lab_03_specificity.py) *(10 min)*
- [ ] [Lab 4 — Evaluation Pipeline](labs/lab_04_evaluation_pipeline.py) *(15 min)*
- [ ] [Lab 5 — Tool-Calling & Structured Output](labs/lab_05_tool_calling.py) *(20 min)*
- [ ] [Lab 6 — Plan-and-Execute Agent](labs/lab_06_agentic_plan_execute.py) *(25 min)*
- [ ] **Failure Gallery** — Diagnose and fix 5 broken prompts — [labs/failure-gallery/](labs/failure-gallery/README.md) *(30 min)*

---

## Deep-Dive Comparisons

- [ ] [Chain-of-Thought Comparison](comparisons/chain-of-thought-comparison.md)
- [ ] [ReAct Comparison](comparisons/react-comparison.md)
- [ ] [Few-Shot Comparison](comparisons/few-shot-comparison.md)
- [ ] [Instruction Tuning Comparison](comparisons/instruction-tuning-comparison.md)
- [ ] [PromptSource Comparison](comparisons/promptsource-comparison.md)
- [ ] [Adversarial Robustness Comparison](comparisons/adversarial-robustness-comparison.md)
- [ ] [Automatic Prompt Optimization](comparisons/automatic-prompt-optimization.md)
- [ ] [Cross-Model Portability](comparisons/cross-model-portability.md)

---

## Reference Guides

- [ ] [Glossary](glossary.md)
- [ ] [Cheat Sheet](cheatsheet.md)
- [ ] [Prompt Debugging Guide](prompt-debugging.md)
- [ ] [Meta-Prompting Guide](meta-prompting.md)
- [ ] [CI/CD Integration Guide](ci-cd-integration.md)
- [ ] [Cookbook — 20 Everyday Recipes](cookbook.md)
- [ ] [Before & After Gallery](before-and-after-gallery.md)
- [ ] [Prompt Engineering for Your Existing Codebase](prompt-engineering-existing-codebase.md)
- [ ] [Exercise Solutions](solutions/exercise-solutions.md)

## Architecture Decision Records

- [ ] [ADR-001: Few-Shot over Fine-Tuning](decisions/001-few-shot-over-fine-tuning.md)
- [ ] [ADR-002: Split Planner-Executor](decisions/002-split-planner-executor.md)
- [ ] [ADR-003: Add Safety Gate](decisions/003-add-safety-gate.md)
- [ ] [ADR-004: Structured Output Schema](decisions/004-structured-output-schema.md)

---

## Research Extension Track (~25 hours total)

### Track 1: Foundations of In-Context Learning
- [ ] Paper 1 — Language Models are Few-Shot Learners [Brown2020]
- [ ] Paper 2 — Training LMs with Human Feedback [Ouyang2022]

### Track 2: Reasoning and Chain-of-Thought
- [ ] Paper 3 — Chain-of-Thought Prompting [Wei2022]
- [ ] Paper 4 — Large LMs are Zero-Shot Reasoners [Kojima2022]
- [ ] Paper 5 — Self-Consistency CoT [Wang2023]

### Track 3: Agents and Tool Use
- [ ] Paper 6 — ReAct [Yao2023]
- [ ] Paper 7 — Reflexion [Shinn2023]
- [ ] Paper 8 — Generative Agents [Park2023]

### Track 4: Safety and Robustness
- [ ] Paper 9 — Red Teaming LMs with LMs [Perez2022]
- [ ] Paper 10 — Indirect Prompt Injection [Greshake2023]

### Track 5: Retrieval Augmentation and Evaluation
- [ ] Paper 11 — RAG for Knowledge-Intensive NLP [Lewis2020]
- [ ] Paper 12 — MT-Bench and Chatbot Arena [Zheng2023]

### Track 6: Reasoning Models and Test-Time Compute
- [ ] Paper 13 — Test-Time Compute Scaling [Snell2024]
- [ ] Paper 14 — Process Supervision / Let's Verify Step by Step [Lightman2023]
- [ ] Paper 15 — System-2 Attention [Saha2024]

See [Research Extension Track](research/README.md) for full study guides.

---

## Prompt Templates Used

### Python Stack
- [ ] `create-feature.prompt.md`
- [ ] `review-code.prompt.md`
- [ ] `debug-issue.prompt.md`
- [ ] `write-tests.prompt.md`
- [ ] `refactor-code.prompt.md`
- [ ] `generate-docs.prompt.md`
- [ ] `update-generate-readme.prompt.md`

### React + TypeScript Stack
- [ ] `auditor-best-practices.prompt.md`
- [ ] `auditor-codebase-maturity.prompt.md`
- [ ] `auditor-cybersecurity-features.prompt.md`
- [ ] `auto-code-implementation.prompt.md`
- [ ] `create-chatbot-ollama.prompt.md`
- [ ] `safety-gate-llm.prompt.md`

### Node.js + TypeScript Stack
- [ ] `create-api-endpoint.prompt.md`
- [ ] `review-code.prompt.md`
- [ ] `write-tests.prompt.md`
- [ ] `generate-openapi-spec.prompt.md`

---

*Last updated: February 2026. Check [CHANGELOG.md](../CHANGELOG.md) for new additions.*

[← Back to curriculum](README.md)
