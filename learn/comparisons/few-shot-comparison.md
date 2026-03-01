# Few-Shot Prompting Strategies Compared

**Level:** Beginner–Intermediate

This document compares zero-shot, one-shot, and few-shot prompting strategies as demonstrated in the foundational work on in-context learning [Brown2020], and provides practical guidance for selecting the right number and quality of examples.

---

## Overview

In-context learning is the ability of large language models to perform tasks by conditioning on examples provided in the prompt, without any parameter updates. Brown et al. [Brown2020] systematically studied this capability in GPT-3 across zero-shot, one-shot, and few-shot settings, establishing the empirical basis for modern prompt engineering.

---

## Zero-Shot Prompting

**Definition.** The prompt contains only a task description — no examples.

```
Translate English to French:
"The weather is beautiful today."
```

**Characteristics:**
- Relies entirely on the model's pretrained knowledge and instruction-following capability.
- Lowest token cost per prompt.
- Performance depends heavily on how well the model's training data covers the task.
- Works well for tasks that are clearly specified and common in training data (translation, summarization, simple classification).

---

## One-Shot Prompting

**Definition.** The prompt includes exactly one input–output example before the actual task.

```
Translate English to French:
"Hello, how are you?" → "Bonjour, comment allez-vous ?"

"The weather is beautiful today." →
```

**Characteristics:**
- A single example clarifies the expected format, register, and scope.
- Minimal token overhead compared to zero-shot.
- Particularly useful when the output format is non-obvious (e.g., a specific JSON structure, a particular coding style).
- One poorly chosen example can mislead the model more than zero examples.

---

## Few-Shot Prompting (2+ examples)

**Definition.** The prompt includes multiple input–output examples (typically 2–8) that demonstrate the task pattern.

```
Translate English to French:
"Hello, how are you?" → "Bonjour, comment allez-vous ?"
"I would like a coffee, please." → "Je voudrais un café, s'il vous plaît."
"Where is the train station?" → "Où est la gare ?"

"The weather is beautiful today." →
```

**Characteristics:**
- Multiple examples allow the model to identify patterns that a single example might not make clear.
- Especially effective for classification tasks with multiple categories, where each example can demonstrate a different category.
- Token cost scales linearly with the number of examples.

---

## Key Findings from Brown et al. [Brown2020]

Brown et al. (2020) [Brown2020] evaluated GPT-3 (175B parameters) across dozens of NLP benchmarks in all three settings:

- **Performance generally improved** from zero-shot to one-shot to few-shot, with diminishing returns as more examples were added.
- **The benefit of examples was most pronounced** for tasks the model found difficult in zero-shot mode — for tasks where zero-shot performance was already high, additional examples provided smaller gains.
- **Model scale interacted with example count** — larger models made better use of in-context examples. Smaller models showed less improvement from additional examples.
- **Example quality mattered more than quantity** — a small number of well-chosen, diverse examples outperformed a larger number of similar or low-quality examples.

---

## Side-by-Side Comparison

| Dimension | Zero-Shot | One-Shot | Few-Shot (2–8) |
|-----------|-----------|----------|----------------|
| **Token cost** | Lowest | Low | Moderate–High |
| **Format clarity** | Relies on instructions | One demonstration | Strong format signal |
| **Task coverage** | Common tasks only | Most tasks | Complex or unusual tasks |
| **Risk of bad examples** | None | Moderate | Lower (diversity buffers) |
| **Best number of examples** | 0 | 1 | 3–5 (practical sweet spot) |
| **Setup effort** | Minimal | Low | Moderate (example curation) |

---

## Practical Guidelines for Example Selection

**1. Choose diverse examples.** If classifying sentiment, include positive, negative, and neutral examples — not three positive ones. Diversity helps the model understand the full output space.

**2. Match the difficulty distribution.** If the target task includes edge cases, include at least one edge case in the examples. Models anchor on the difficulty level demonstrated by examples.

**3. Order matters (slightly).** Place the most representative example last (closest to the actual task input). Some research suggests models attend more to recent examples, though this effect is model-dependent.

**4. Keep examples concise.** Long examples consume tokens without proportional benefit. If the task can be demonstrated with short inputs and outputs, use short examples.

**5. Prefer real examples over synthetic ones.** Examples drawn from actual data are more natural and less likely to introduce artifacts that mislead the model.

**6. Test with and without examples.** Zero-shot performance may be sufficient for your task. Always verify that adding examples actually improves output quality before committing the token budget.

---

## Decision Framework

1. **Start with zero-shot.** Write a clear instruction. If the output meets your requirements, stop.
2. **If format is ambiguous, add one example.** This is often sufficient to resolve format questions.
3. **If the task is complex or has multiple output categories, add 2–5 examples.** Ensure diversity across categories.
4. **If accuracy is still insufficient, improve example quality** before adding more examples. Re-read existing examples for clarity and representativeness.
5. **If token budget is constrained, consider zero-shot with detailed instructions** as an alternative to few-shot. Module 3 discusses when detailed instructions can substitute for examples.

---

## Cross-References

- **Module 1** ([01-introduction.md](../01-introduction.md), §1.3) introduces examples as one of the five structural components of a prompt.
- **Module 3** ([03-patterns.md](../03-patterns.md), §3.2–§3.3) covers zero-shot and few-shot patterns with worked examples.
- **Module 4** ([04-best-practices.md](../04-best-practices.md), §4.1) discusses token budget management, which directly affects how many examples you can afford.
- The [Chain-of-Thought Comparison](chain-of-thought-comparison.md) extends the few-shot concept to include reasoning traces in examples.

---

## References

- [Brown2020] Brown, T. B., et al. (2020). Language models are few-shot learners. *NeurIPS 33*, 1877–1901.

See [`references.md`](../../references.md) for full citations with DOIs.
