# Case 05 — Solution

## Analysis

**Component audit:**
- Role: ❌ Absent — no persona assigned for the explainer
- Context: ❌ Absent — no audience, purpose, or background
- Task: ⚠️ Technically present ("explain") but underspecified — "explain" could mean define, overview, tutorial, comparison, history...
- Constraints: ❌ Absent — no length, no depth, no scope boundaries
- Examples: ❌ Absent

Four of five components are missing. This prompt maximizes ambiguity.

## Fixed Prompts — Three Valid Rewrites

Each rewrite serves a different audience. All three start from the same broken prompt but are entirely different prompts.

### Rewrite A — For a High-School Student

```
You are a patient science teacher explaining AI concepts to a 16-year-old with
no prior programming experience.

Explain machine learning in 3–4 short paragraphs. Use an everyday analogy as
your opening sentence. Avoid jargon; if you must use a technical term, define
it in plain language. Do not include any code.
```

### Rewrite B — For a Software Engineer New to ML

```
You are a senior ML engineer giving a 5-minute orientation to a software
engineer who knows Python but has never used machine learning.

Explain machine learning. Cover:
1. The core paradigm (how ML differs from traditional programming)
2. The three main learning types (supervised, unsupervised, reinforcement)
3. One concrete code-level example using scikit-learn that illustrates fitting a model

Length: 400–500 words. Use a code snippet for the scikit-learn example.
```

### Rewrite C — Executive Summary

```
You are a technology strategist briefing a non-technical executive.

Explain machine learning in exactly 3 sentences:
1. What it is (plain language, no jargon)
2. What business problem it solves
3. One example from retail or finance that a CFO would recognize

Do not use the words "algorithm," "data," or "model" — replace them with
business-level vocabulary.
```

## Key Lesson

"Explain [concept]" is the canonical example of a prompt that is maximally ambiguous. Every word in the "Explain machine learning" prompt is vague:
- "Explain" — at what depth, in what format, with or without code?
- "machine learning" — which aspects? supervised only? history? math?

Before sending any explanation-request prompt, ask: *Who is the reader? For what purpose? At what length? In what format?* These four questions map directly to Role, Context, Constraints, and Format in the five-component framework. See Module 1 §1.3 and Module 2 §2.1.
