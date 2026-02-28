# Chain-of-Thought Prompting: A Three-Way Comparison

**Level:** Intermediate

This document compares three variants of chain-of-thought (CoT) prompting — Few-Shot CoT, Zero-Shot CoT, and Self-Consistency CoT — along dimensions relevant to practitioners selecting a prompting strategy for reasoning-intensive tasks.

---

## Overview

Chain-of-thought prompting is a family of techniques that improve LLM performance on tasks requiring multi-step reasoning by eliciting explicit intermediate reasoning steps. The core insight, established by Wei et al. [Wei2022], is that LLMs produce more accurate final answers when they generate reasoning traces rather than jumping directly to conclusions.

Three major variants have emerged, each offering different trade-offs between setup effort, token cost, and reliability.

---

## Variant 1: Few-Shot Chain-of-Thought

**Source:** Wei et al. (2022) [Wei2022]

**Mechanism.** The prompt includes hand-crafted examples that demonstrate the desired reasoning process. Each example shows an input, a step-by-step reasoning trace, and a final answer. The model generalizes from these demonstrations to produce similar reasoning for new inputs.

**Example structure:**
```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
   Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is
   2 × 3 = 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: [new question]
A:
```

**Key findings from Wei et al. [Wei2022]:**
- CoT prompting substantially improved performance on arithmetic reasoning (GSM8K), commonsense reasoning (StrategyQA), and symbolic reasoning benchmarks.
- The effect is **emergent with model scale** — in the original 2022 experiments, models below approximately 100 billion parameters showed minimal or no improvement with CoT, while large models (PaLM 540B, GPT-3 175B) benefited significantly. *Note:* more recent models (2024–2026) can exhibit strong CoT gains at much smaller sizes due to improved training techniques, data quality, and instruction tuning. The 100B threshold should be understood as a historical observation from the original study, not a universal rule.
- The quality of the reasoning demonstrations in the examples matters: examples with incorrect reasoning traces degrade performance.

**Strengths:**
- Highest degree of control over reasoning style and output format.
- The practitioner can steer the model toward domain-specific reasoning patterns.

**Weaknesses:**
- Requires manual effort to craft high-quality reasoning demonstrations.
- Consumes significant context-window tokens (each example includes both the input and the full reasoning trace).
- Examples may inadvertently anchor the model on irrelevant reasoning patterns if poorly chosen.

---

## Variant 2: Zero-Shot Chain-of-Thought

**Source:** Kojima et al. (2022) [Kojima2022]

**Mechanism.** Instead of providing examples, the prompt appends a trigger phrase — most commonly "Let's think step by step" — to the task description. This single phrase is sufficient to elicit step-by-step reasoning from the model without any demonstrations.

**Example structure:**
```
Q: A juggler can juggle 16 balls. Half of the balls are golf balls, and
   half of the golf balls are blue. How many blue golf balls are there?

A: Let's think step by step.
```

**Key findings from Kojima et al. [Kojima2022]:**
- The phrase "Let's think step by step" elicited reasoning chains across diverse benchmarks, including arithmetic, symbolic, commonsense, and logical reasoning tasks.
- Zero-Shot CoT achieved strong performance improvements over standard zero-shot prompting without requiring any hand-crafted examples.
- Performance was competitive with Few-Shot CoT on many tasks, despite requiring zero additional tokens for examples.

**Strengths:**
- Extremely low setup effort — a single phrase added to any prompt.
- No context-window overhead from examples.
- Generalizes across task types without task-specific example design.

**Weaknesses:**
- Less control over the reasoning format and style compared to Few-Shot CoT.
- The model may produce verbose or meandering reasoning traces.
- Sensitive to the exact trigger phrase; minor variations can affect performance.

---

## Variant 3: Self-Consistency Chain-of-Thought

**Source:** Wang et al. (2023) [Wang2023]

**Mechanism.** Self-Consistency extends either Few-Shot or Zero-Shot CoT by sampling multiple reasoning paths (using temperature > 0) and selecting the final answer by majority vote. The intuition is that while any single reasoning path may contain errors, the correct answer is more likely to emerge consistently across multiple independent reasoning attempts.

**Process:**
1. Present the prompt (with CoT, either few-shot or zero-shot).
2. Sample N responses from the model (typically N = 5–40) at non-zero temperature.
3. Extract the final answer from each response.
4. Return the answer that appears most frequently (majority vote).

**Key findings from Wang et al. [Wang2023]:**
- Self-Consistency improved over standard (greedy) CoT decoding across arithmetic, commonsense, and symbolic reasoning benchmarks.
- The improvement was consistent across different model families and sizes.
- Increasing the number of sampled paths yields diminishing returns — most of the benefit is captured within the first 10–20 paths.

**Strengths:**
- Improves reliability without requiring better prompts or examples.
- Reduces the impact of individual reasoning errors.
- Composable with both Few-Shot and Zero-Shot CoT.

**Weaknesses:**
- Multiplies inference cost by the number of sampled paths (N).
- Requires the ability to extract and compare final answers programmatically.
- Not applicable to open-ended generation tasks where there is no single "correct" answer to vote on.

---

## Side-by-Side Comparison

| Dimension | Few-Shot CoT | Zero-Shot CoT | Self-Consistency CoT |
|-----------|-------------|---------------|---------------------|
| **Setup effort** | High (craft examples) | Minimal (add trigger phrase) | Moderate (configure sampling) |
| **Token cost per call** | High (examples + reasoning) | Low (trigger phrase + reasoning) | N × base CoT cost |
| **Control over reasoning style** | High | Low | Inherited from base CoT |
| **Best for** | Domain-specific reasoning, custom formats | General reasoning, rapid prototyping | High-stakes decisions, reliability-critical tasks |
| **Model size requirement** | Large (100B+) in original study* | Large (100B+) in original study* | Large (100B+) in original study* |
| **Failure mode** | Bad examples anchor bad reasoning | Verbose or unfocused reasoning | Majority can still be wrong on hard problems |

> *\*Model size requirement:* The 100B+ threshold reflects the original 2022–2023 findings. Modern smaller models (e.g., 7B–70B parameter instruction-tuned models) can also benefit substantially from CoT prompting.

> **Note on performance figures.** The original papers report specific accuracy numbers on benchmarks such as GSM8K and StrategyQA. These numbers vary by model, prompt variant, and evaluation protocol. Consult Wei et al. [Wei2022], Kojima et al. [Kojima2022], and Wang et al. [Wang2023] directly for precise empirical results. See [`references.md`](../../references.md) for full citations.

---

## Decision Framework

Use this flowchart to select a CoT variant:

1. **Is the task a reasoning task?** (arithmetic, logic, planning, multi-step inference)
   - No → CoT is unlikely to help. Use zero-shot instruction or few-shot without reasoning traces.
   - Yes → Continue.

2. **Do you have high-quality reasoning demonstrations for this task?**
   - Yes → Use **Few-Shot CoT** for maximum control.
   - No → Use **Zero-Shot CoT** as a strong baseline.

3. **Is reliability critical?** (e.g., the output feeds into an automated pipeline, or errors are costly)
   - Yes → Add **Self-Consistency** on top of whichever CoT variant you chose.
   - No → Single-path CoT is sufficient.

4. **Is latency or cost a constraint?**
   - Yes → Prefer Zero-Shot CoT (fewest tokens) with greedy decoding (single path).
   - No → Self-Consistency with Few-Shot CoT provides the highest reliability.

---

## Cross-References

- **Module 3** ([03-patterns.md](../03-patterns.md), §3.4) introduces CoT as one of six major prompting patterns.
- **Module 5** ([05-advanced-patterns.md](../05-advanced-patterns.md), §5.4) covers evaluation pipelines that can be used to compare CoT variants empirically.
- The production prompts in [`prompts/react-typescript/prompts/`](../../prompts/react-typescript/prompts/) demonstrate implicit CoT through step-by-step audit instructions.

---

## References

- [Wei2022] Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 35*, 24824–24837.
- [Kojima2022] Kojima, T., et al. (2022). Large language models are zero-shot reasoners. *NeurIPS 35*.
- [Wang2023] Wang, X., et al. (2023). Self-consistency improves chain of thought reasoning in language models. *ICLR*.

See [`references.md`](../../references.md) for full citations with DOIs.
