# Meta-Prompting: Prompts That Write Prompts

## Overview

Meta-prompting is the practice of using LLMs to **generate, evaluate, and refine other prompts**. While Modules 1–5 teach you to write prompts by hand and the [Automatic Prompt Optimization](comparisons/automatic-prompt-optimization.md) comparison covers algorithmic approaches, meta-prompting occupies the practical middle ground: using carefully designed "meta-prompts" to accelerate your manual workflow.

This guide covers three meta-prompting techniques — prompt generation, prompt evaluation, and prompt refinement — each with worked examples and copy-paste templates.

---

## 1. Prompt Generation: Bootstrapping a First Draft

### When to Use

You know *what* you want a prompt to do, but staring at a blank page is inefficient. A prompt-generation meta-prompt can produce a solid first draft in seconds.

### Template

```
You are an expert prompt engineer. Given a task description, generate a
high-quality prompt that follows these best practices:
- Clear role assignment (Module 2, §2.1)
- Explicit constraints and output format (Module 3, §3.6)
- Appropriate use of examples if the task benefits from few-shot (Module 3, §3.3)
- Defensive instructions against common failure modes (Module 5, §5.2)

Task description: {task_description}
Target model: {model_name_or_family}
Desired output format: {format_description}

Generate the prompt. Include comments (lines starting with #) explaining
your design choices for each section.
```

### Worked Example

**Input:**
```
Task description: Classify customer support emails into categories
  (billing, technical, account, general) and extract the key issue
  in one sentence.
Target model: GPT-4o
Desired output format: JSON with "category" and "key_issue" fields
```

**Model output (meta-prompt generates this):**
```
# Role: establishes domain expertise and output expectations
You are a customer support triage specialist. You classify incoming
emails and extract the core issue.

# Task: explicit instruction with constrained categories
Classify the following email into exactly one category:
- billing: payment, invoice, refund, subscription charges
- technical: bugs, errors, performance, integration issues
- account: login, password, permissions, profile changes
- general: feedback, feature requests, other inquiries

# Output format: enforces structure
Respond with ONLY a JSON object:
{"category": "<category>", "key_issue": "<one-sentence summary>"}

# Defensive instruction: prevents common failures
Do not include markdown formatting, code fences, or explanatory text
outside the JSON object.

# Input
Email:
---
{email_text}
---
```

### Tips

- Always tell the meta-prompt which model family the generated prompt targets — prompts for Claude differ from prompts for GPT.
- Review and edit the generated prompt; meta-prompting produces a draft, not a finished product.
- The `# comment` pattern helps you understand the meta-prompt's reasoning and makes the output self-documenting.

---

## 2. Prompt Evaluation: Scoring an Existing Prompt

### When to Use

You have a working prompt but want a structured critique before investing time in testing. A prompt-evaluation meta-prompt acts as a "prompt code review."

### Template

```
You are a prompt engineering reviewer. Evaluate the following prompt
against these criteria, scoring each 1–5:

1. **Clarity** — Is the instruction unambiguous? (1=vague, 5=crystal clear)
2. **Specificity** — Are constraints, format, and scope explicit? (1=absent, 5=comprehensive)
3. **Robustness** — Does it handle edge cases and adversarial input? (1=fragile, 5=hardened)
4. **Efficiency** — Is it concise without sacrificing quality? (1=bloated, 5=optimal)
5. **Portability** — Would it work across model families? (1=model-specific, 5=portable)

For each criterion:
- Assign a score (1–5)
- Provide a one-sentence justification
- If the score is ≤3, suggest a specific improvement

Then provide an overall recommendation: SHIP, REVISE, or REDESIGN.

Prompt to evaluate:
---
{prompt_text}
---
```

### Worked Example

**Running the evaluation meta-prompt on a naive prompt:**

```
Prompt to evaluate:
---
Summarize this article.
---
```

**Model output:**
```
1. Clarity:      2/5 — "Summarize" is ambiguous (length, style, audience unspecified).
   → Fix: "Write a 3-sentence summary for a technical audience."
2. Specificity:  1/5 — No constraints on format, length, or focus.
   → Fix: Add word count, output format, and topic focus.
3. Robustness:   1/5 — No handling for empty input, non-article text, or very long content.
   → Fix: Add "If the input is not an article, respond with 'NOT_AN_ARTICLE'."
4. Efficiency:   3/5 — Concise, but only because it's incomplete.
5. Portability:  4/5 — Simple enough to work across models, though results will vary.

Overall: REDESIGN — this prompt lacks the specificity to produce consistent results.
```

---

## 3. Prompt Refinement: Iterating on a Draft

### When to Use

You have a prompt that *mostly* works but fails on certain inputs. Instead of manually guessing fixes, use a refinement meta-prompt that analyzes failure cases and proposes targeted improvements.

### Template

```
You are a prompt optimization specialist. I have a prompt that works
for most inputs but fails on specific cases. Analyze the failures and
propose targeted revisions.

Current prompt:
---
{current_prompt}
---

Failure cases (input → actual output → expected output):
{failure_cases}

For each failure:
1. Diagnose the root cause (refer to the Prompt Debugging Guide categories
   if applicable: hallucination, format violation, instruction non-compliance,
   over-generation, under-generation, safety refusal, inconsistency).
2. Propose a specific prompt revision that addresses the failure.
3. Explain why the revision should fix the issue without breaking
   currently-passing cases.

Then produce the complete revised prompt incorporating all fixes.
```

### Worked Example

**Input:**
```
Current prompt: "Translate the following English text to French. Return
only the translation, no explanations."

Failure cases:
1. Input: "I'm feeling blue today."
   Actual: "Je suis bleu aujourd'hui."
   Expected: "Je me sens triste aujourd'hui." (idiomatic, not literal)

2. Input: "" (empty string)
   Actual: "Voici la traduction:" followed by hallucinated text.
   Expected: "EMPTY_INPUT"
```

**Model output:**
```
Failure 1 diagnosis: Instruction non-compliance — the prompt doesn't
specify idiomatic vs. literal translation. The model defaults to literal.
→ Fix: Add "Translate idiomatically, preserving the intended meaning
  rather than translating word-by-word."

Failure 2 diagnosis: Hallucination on empty input — no guard clause.
→ Fix: Add "If the input is empty or contains no translatable text,
  respond with exactly 'EMPTY_INPUT'."

Revised prompt:
---
Translate the following English text into natural, idiomatic French.
Preserve the intended meaning rather than translating word-by-word.
Return ONLY the French translation with no explanations or commentary.

If the input is empty or contains no translatable text, respond with
exactly: EMPTY_INPUT

English text:
{text}

French translation:
---
```

---

## 4. Meta-Prompting Workflow

Combine the three techniques into a systematic workflow:

```
┌───────────────────┐
│ 1. GENERATE       │  Use the generation meta-prompt to bootstrap
│    (first draft)  │  a prompt from your task description.
└────────┬──────────┘
         ▼
┌───────────────────┐
│ 2. EVALUATE       │  Run the evaluation meta-prompt to identify
│    (critique)     │  weaknesses before testing.
└────────┬──────────┘
         ▼
┌───────────────────┐
│ 3. TEST           │  Run the prompt against real inputs
│    (real inputs)  │  (see Module 5, §5.4 for evaluation pipelines).
└────────┬──────────┘
         ▼
┌───────────────────┐
│ 4. REFINE         │  Feed failures into the refinement meta-prompt
│    (fix failures) │  for targeted improvements.
└────────┬──────────┘
         ▼
┌───────────────────┐
│ 5. REPEAT         │  Iterate steps 2–4 until the prompt meets
│    (until stable) │  your quality threshold.
└───────────────────┘
```

---

## 5. Anti-Patterns in Meta-Prompting

| Anti-Pattern | Problem | Fix |
| --- | --- | --- |
| **Blind trust** | Shipping the meta-prompt's output without review | Always manually review and test generated prompts |
| **Over-delegation** | Using meta-prompts for simple tasks you could write in 30 seconds | Reserve meta-prompting for complex multi-constraint prompts |
| **Infinite recursion** | Using meta-prompts to generate meta-prompts to generate meta-prompts... | Two levels of meta is the practical limit |
| **Ignoring context** | Not telling the meta-prompt about the target model, audience, or use case | Always provide task context in the meta-prompt input |
| **Skipping testing** | Assuming a refined prompt works because the meta-prompt said it would | Evaluation meta-prompts are heuristic — always validate on real inputs |

---

## Connection to Other Resources

- **Cheat Sheet** ([cheatsheet.md](cheatsheet.md)) — the copy-paste prompt template is an excellent starting point *before* engaging meta-prompting.
- **Prompt Debugging Guide** ([prompt-debugging.md](prompt-debugging.md)) — the seven failure categories map directly to the refinement meta-prompt's diagnostic step.
- **Evaluation Template** ([../prompts/shared/evaluation-template.md](../prompts/shared/evaluation-template.md)) — provides the scoring framework for step 3 of the workflow.
- **Automatic Prompt Optimization** ([comparisons/automatic-prompt-optimization.md](comparisons/automatic-prompt-optimization.md)) — when meta-prompting isn't enough, algorithmic approaches (DSPy, OPRO, APE) automate the loop.

---

[← Back to curriculum](README.md)
