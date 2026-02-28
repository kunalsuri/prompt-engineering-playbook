# ReAct: Reasoning + Acting vs. Standard Prompting

**Level:** Intermediate–Advanced

This document compares the ReAct prompting paradigm [Yao2023] with standard prompting approaches, analyzing when interleaved reasoning and action traces outperform direct question-answering or reasoning-only methods.

---

## Overview

Standard prompting asks a model to produce an answer directly from its parametric knowledge. Chain-of-thought prompting adds explicit reasoning but still operates entirely within the model's internal knowledge. ReAct extends this by interleaving **reasoning traces** (Thought) with **external actions** (Act) and their results (Observation), creating a loop that grounds the model's reasoning in real-world information.

---

## Standard Prompting

**Mechanism.** The model receives a question and produces an answer in a single generation step, drawing entirely on knowledge encoded during pretraining.

```
Q: What is the elevation of the birthplace of the inventor of the telephone?
A: [model generates answer directly]
```

**Strengths:**
- Minimal latency (single inference call).
- No external dependencies or tool integration required.

**Weaknesses:**
- Prone to hallucination on knowledge-intensive questions, especially for facts not well-represented in training data.
- No ability to access current or private information.
- No self-correction mechanism — errors in early tokens propagate.

---

## Reasoning-Only (Chain-of-Thought)

**Mechanism.** The model generates intermediate reasoning steps before the final answer but still relies entirely on internal knowledge.

```
Q: What is the elevation of the birthplace of the inventor of the telephone?
Thought: The telephone was invented by Alexander Graham Bell. He was born in
         Edinburgh, Scotland. Edinburgh's elevation is approximately 47 meters.
A: Approximately 47 meters.
```

**Strengths:**
- Explicit reasoning traces are interpretable and auditable.
- Improves accuracy on multi-step reasoning tasks [Wei2022].

**Weaknesses:**
- Reasoning traces can contain confidently stated but incorrect facts (hallucination persists).
- No mechanism to verify factual claims against external sources.

---

## ReAct (Reasoning + Acting)

**Source:** Yao et al. (2023) [Yao2023]

**Mechanism.** The model alternates between generating reasoning traces (Thought), issuing tool-use commands (Action), and processing the results (Observation). This creates an iterative loop where reasoning is grounded in external evidence.

```
Q: What is the elevation of the birthplace of the inventor of the telephone?

Thought 1: I need to find who invented the telephone.
Action 1: Search("inventor of the telephone")
Observation 1: Alexander Graham Bell is credited with inventing the telephone.

Thought 2: I need to find where Alexander Graham Bell was born.
Action 2: Search("Alexander Graham Bell birthplace")
Observation 2: Bell was born in Edinburgh, Scotland, on March 3, 1847.

Thought 3: I need to find the elevation of Edinburgh.
Action 3: Search("Edinburgh Scotland elevation")
Observation 3: Edinburgh has an elevation of approximately 47 metres (154 ft).

Thought 4: I now have all the information needed to answer the question.
A: The elevation of Edinburgh, the birthplace of Alexander Graham Bell
   (inventor of the telephone), is approximately 47 metres (154 ft).
```

**Key findings from Yao et al. [Yao2023]:**
- On knowledge-intensive tasks (HotpotQA, FEVER), ReAct outperformed both standard prompting and reasoning-only (CoT) approaches by grounding answers in retrieved evidence.
- On interactive decision-making tasks (ALFWorld, WebShop), ReAct outperformed imitation learning and reinforcement learning baselines.
- ReAct substantially reduced hallucination compared to CoT-only prompting, because factual claims could be verified through search actions.
- ReAct traces are more **interpretable** than CoT traces: the action–observation pairs allow a human reviewer to verify exactly what information the model used.

---

## Side-by-Side Comparison

| Dimension | Standard Prompting | Chain-of-Thought | ReAct |
|-----------|--------------------|-------------------|-------|
| **Knowledge source** | Parametric only | Parametric only | Parametric + external tools |
| **Hallucination risk** | High | Moderate (reasoning may catch some errors) | Low (grounded in observations) |
| **Latency** | Low (1 call) | Low (1 call) | Higher (multiple reasoning–action cycles) |
| **Interpretability** | Low (direct answer) | Moderate (reasoning visible) | High (reasoning + evidence visible) |
| **Requires tool integration** | No | No | Yes |
| **Best for** | Simple factual retrieval, well-known facts | Multi-step reasoning within model knowledge | Knowledge-intensive QA, interactive tasks, fact verification |
| **Infrastructure complexity** | None | None | Requires action runtime (search API, code executor, etc.) |

---

## When to Use ReAct

**Use ReAct when:**
- The task requires information the model may not have (or may have inaccurately) — current events, private data, rapidly changing facts.
- Factual accuracy is more important than response latency.
- The task involves interacting with external systems (databases, APIs, file systems, code execution environments).
- You need an auditable trace showing where each fact came from.

**Use standard or CoT prompting when:**
- The task is reasoning-intensive but requires only common knowledge.
- Latency is critical and tool calls would add unacceptable delay.
- No external tools are available in the deployment environment.
- The task is primarily about format transformation, code generation, or creative writing rather than factual question-answering.

---

## ReAct in VS Code Copilot

The production prompts in this repository use VS Code Copilot's agent mode (`mode: 'agent'` in YAML frontmatter), which implements a ReAct-style architecture. When agent mode is active, Copilot can:

- **Think** about what files or information it needs.
- **Act** by reading files, running terminal commands, searching the codebase.
- **Observe** the results of those actions.
- **Reason** about the observations and decide the next action.

This is why prompts like the codebase maturity auditor ([`auditor-codebase-maturity.prompt.md`](../../prompts/react-typescript/prompts/auditor-codebase-maturity.prompt.md)) include explicit phases: discovery (action), analysis (reasoning), and reporting (output). The prompt structure mirrors the ReAct loop.

---

## Limitations of ReAct

- **Action quality depends on tool quality.** If the search API returns irrelevant results, the model's reasoning over those results will be compromised.
- **Loop termination.** The model may enter unproductive action loops (repeatedly searching for the same information). Setting a maximum number of reasoning–action cycles is a practical safeguard.
- **Cost.** Each action–observation cycle consumes tokens. Complex queries may require many cycles, significantly increasing total token usage.

---

## Cross-References

- **Module 2** ([02-core-principles.md](../02-core-principles.md), §2.2) introduces decomposition, the principle underlying ReAct's multi-step structure.
- **Module 3** ([03-patterns.md](../03-patterns.md), §3.7) defines the ReAct pattern with a worked example.
- **Module 5** ([05-advanced-patterns.md](../05-advanced-patterns.md)) covers RAG, which shares ReAct's principle of grounding LLM output in external evidence.

---

## References

- [Yao2023] Yao, S., et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*.
- [Wei2022] Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 35*, 24824–24837.

See [`references.md`](../../references.md) for full citations with DOIs.
