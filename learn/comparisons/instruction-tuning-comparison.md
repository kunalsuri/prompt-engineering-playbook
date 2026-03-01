# Instruction Tuning: FLAN, T0, and InstructGPT Compared

**Level:** Intermediate–Advanced

This document compares three landmark instruction-tuning approaches — T0 [Sanh2022], Flan [Chung2022], and InstructGPT [Ouyang2022] — and explains how they shape the models that prompt engineers work with today.

---

## Why This Matters for Prompt Engineering

Instruction tuning is the process of fine-tuning a pretrained LLM on a dataset of (instruction, response) pairs so that the model learns to follow natural-language instructions. Understanding how models were instruction-tuned helps prompt engineers write better prompts, because it reveals what kinds of instructions the model was trained to follow and where its instruction-following capabilities may break down.

---

## Approach 1: T0 — Multitask Prompted Training

**Source:** Sanh et al. (2022) [Sanh2022]

**Base model:** T5 (11 billion parameters, encoder-decoder architecture).

**Training method:** T0 was trained on a diverse set of NLP tasks (sentiment analysis, question answering, summarization, etc.) reformatted as natural-language prompts using templates from PromptSource [Bach2022]. The key innovation was using a large variety of prompt templates per task, exposing the model to many different ways of expressing the same instruction.

**Key findings:**
- T0 achieved zero-shot performance competitive with GPT-3's few-shot performance on several benchmarks, despite being approximately 16× smaller.
- Exposure to diverse prompt phrasings during training improved robustness — T0 was less sensitive to the exact wording of prompts than models trained on a single template per task.
- Performance improved with both the number of training tasks and the diversity of prompt templates.

**Implications for prompt engineering:**
- Models trained with T0-style methods are relatively robust to prompt phrasing variation.
- These models respond well to direct task descriptions without examples.
- The training methodology favors classification and short-answer tasks; long-form generation was less emphasized.

---

## Approach 2: Flan — Scaling Instruction-Finetuned Models

**Source:** Chung et al. (2022) [Chung2022]

**Base models:** T5, PaLM (including PaLM 540B).

**Training method:** Flan extended the T0 approach by significantly scaling the number of tasks (1,800+ tasks), adding chain-of-thought training data, and applying instruction tuning to much larger models. Flan-PaLM was trained on both standard instruction-following tasks and tasks requiring explicit reasoning steps.

**Key findings:**
- Scaling the number and diversity of instruction-tuning tasks continued to improve performance.
- Including chain-of-thought (CoT) reasoning data during fine-tuning improved the model's ability to produce reasoning traces at inference time, even on tasks not seen during training.
- Flan-PaLM achieved strong results across a wide range of benchmarks, outperforming the base PaLM model on both standard and reasoning-intensive tasks.

**Implications for prompt engineering:**
- Flan-style models respond well to both direct instructions and "think step by step" reasoning requests.
- The inclusion of CoT data during training means that chain-of-thought prompting (Module 3, §3.4) is particularly effective with these models.
- Larger, more diversely tuned models are generally more responsive to complex, multi-requirement prompts.

---

## Approach 3: InstructGPT — RLHF Alignment

**Source:** Ouyang et al. (2022) [Ouyang2022]

**Base model:** GPT-3 (various sizes, up to 175B parameters, decoder-only architecture).

**Training method:** InstructGPT used a three-stage process:
1. **Supervised fine-tuning (SFT):** GPT-3 was fine-tuned on a dataset of (prompt, ideal response) pairs written by human annotators.
2. **Reward model training:** Human raters ranked multiple model outputs for the same prompt. A reward model was trained to predict these rankings.
3. **Reinforcement learning from human feedback (RLHF):** The SFT model was further optimized using PPO (Proximal Policy Optimization) to maximize the reward model's score.

**Key findings:**
- InstructGPT 1.3B (a much smaller model) was preferred by human raters over the base GPT-3 175B, demonstrating that alignment training can be more impactful than raw model scale.
- InstructGPT produced fewer harmful, untruthful, and unhelpful outputs compared to the base GPT-3.
- The model showed improved instruction following, especially for nuanced requests involving tone, format, and constraint adherence.

**Implications for prompt engineering:**
- RLHF-aligned models respond well to natural, conversational instructions — they were trained to interpret human intent even when instructions are imprecise.
- These models are generally better at following negative constraints ("do not ...") and format specifications.
- The alignment process may introduce a tendency toward verbose, cautious responses ("hedging"), which can be counteracted with explicit brevity instructions.

---

## Side-by-Side Comparison

| Dimension | T0 [Sanh2022] | Flan [Chung2022] | InstructGPT [Ouyang2022] |
|-----------|---------------|-------------------|--------------------------|
| **Architecture** | Encoder-decoder (T5) | Encoder-decoder (T5) + decoder-only (PaLM) | Decoder-only (GPT-3) |
| **Key training signal** | Diverse prompted tasks | Scaled prompted tasks + CoT data | Human preferences via RLHF |
| **Scale demonstrated** | 11B parameters | Up to 540B parameters | Up to 175B parameters |
| **Zero-shot strength** | Classification, short QA | Reasoning, diverse tasks | Instruction following, safety |
| **Prompt sensitivity** | Lower (diverse templates) | Lower (diverse tasks) | Lower (human-preference tuning) |
| **Reasoning capability** | Moderate | Strong (CoT training) | Moderate (not CoT-trained) |
| **Alignment / safety** | Not specifically targeted | Not specifically targeted | Core objective |
| **Open-source availability** | Yes (T0 weights available) | Partially (Flan-T5 available) | No (proprietary) |

---

## How These Approaches Relate to Modern Models

Most modern instruction-following LLMs combine elements from all three approaches:

- **GPT-4, Claude, Gemini** use RLHF (InstructGPT lineage) for alignment and safety, combined with diverse instruction-tuning data (T0/Flan lineage) for broad task competence.
- **Open-source models** (Llama, Mistral fine-tunes) often use supervised instruction tuning with community-generated datasets, following the T0/Flan methodology, sometimes augmented with RLHF or DPO (Direct Preference Optimization).

For prompt engineers, the practical takeaway is that modern models are responsive to both explicit instructions (T0/Flan heritage) and natural conversational guidance (InstructGPT heritage). The most effective prompts leverage both: explicit structural instructions for format and task specification, combined with natural-language guidance for tone, role, and reasoning style.

---

## Cross-References

- **Module 1** ([01-introduction.md](../01-introduction.md), §1.1) introduces why prompt engineering matters in the context of instruction-following models.
- **Module 3** ([03-patterns.md](../03-patterns.md)) catalog patterns that work because of instruction tuning — especially zero-shot (§3.2) and chain-of-thought (§3.4).
- The [PromptSource Comparison](promptsource-comparison.md) examines the template system used to train T0.
- The [Chain-of-Thought Comparison](chain-of-thought-comparison.md) explores CoT in detail, including its connection to Flan's CoT training data.

---

## References

- [Sanh2022] Sanh, V., et al. (2022). Multitask prompted training enables zero-shot task generalization. *ICLR*.
- [Chung2022] Chung, H. W., et al. (2022). Scaling instruction-finetuned language models. *arXiv preprint*.
- [Ouyang2022] Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 35*, 27730–27744.
- [Bach2022] Bach, S. H., et al. (2022). PromptSource: An integrated development environment and repository for natural language prompts. *ACL 2022 System Demonstrations*, 93–104.

See [`references.md`](../../references.md) for full citations with DOIs.
