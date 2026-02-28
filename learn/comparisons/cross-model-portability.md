# Cross-Model Portability — Behavioral Comparison

> **Validation note:** Characterizations below are based on published model evaluation results, community benchmarks (LMSYS Chatbot Arena, OpenLLM Leaderboard), and widely reported behavioral patterns as of February 2026. Model behavior changes with every update. Treat specifics as directional guidance, not guarantees. Re-verify against your target model version before deploying critical prompts. All performance delta figures are *(approx.)*.

---

## Why Portability Matters

A prompt crafted for GPT-4o may behave differently when run against Claude 3.5 Sonnet, Gemini 1.5 Pro, or an open-weights model like Llama 3.1 70B. The differences are not random — they are systematic and stem from:

- **Training data composition** — models that saw more instruction-following examples are more responsive to explicit directives
- **RLHF reward model calibration** — safety and helpfulness trade-offs differ across providers
- **Context window architecture** — how attention distributes across long contexts varies
- **Native API capabilities** — structured-output APIs (JSON mode, tool-calling) are provider-specific

Understanding these differences lets you write prompts that work reliably across models, or at minimum, know where to add model-specific adjustment layers.

---

## Capability Grid

The following grid shows how five key capabilities are supported across four major model families. Ratings: ✅ Strong native support · ⚠️ Partial or inconsistent · ❌ Absent or unreliable.

| Capability | GPT-4o | Claude 3.5 Sonnet | Gemini 1.5 Pro | Llama 3.1 70B |
|---|---|---|---|---|
| **System prompt adherence** | ✅ Very strong | ✅ Very strong | ✅ Strong | ⚠️ Moderate — longer system prompts lose effect |
| **Zero-shot instruction following** | ✅ | ✅ | ✅ | ⚠️ Benefits more from few-shot [Brown2020] than others |
| **Chain-of-thought (explicit)** | ✅ | ✅ | ✅ | ✅ Requires explicit "think step by step" trigger |
| **Native JSON mode / structured output** | ✅ `response_format: json_object` | ⚠️ Via tool-use or prompt engineering | ✅ Constrained decoding (Gemini API) | ❌ Prompt-based only; wrapping in markdown common |
| **Tool-calling / function-calling** | ✅ Native parallel tool-calling | ✅ Tool-use API | ✅ Function declarations API | ⚠️ Supported on select fine-tuned variants only |
| **Refusal sensitivity** | ⚠️ Occasionally over-refuses edge-case legitimate requests | ⚠️ More conservative; explicit context needed | ✅ Generally permissive for commercial use | ✅ Minimal RLHF refusals — requires your own safety layer |
| **Long-context attention** | ✅ Up to 128K tokens, good recall | ✅ Up to 200K tokens, strong recall | ✅ Up to 1M tokens, variable recall at extremes | ⚠️ 128K window; attention degrades beyond ~32K in practice [Liu2024] |
| **Code generation accuracy** | ✅ | ✅ | ✅ | ✅ Strong on common languages; weaker on niche |
| **Following negative constraints** ("do NOT...") | ✅ | ✅ | ⚠️ Occasionally ignores peripheral negatives | ⚠️ Needs repetition for strict compliance |
| **Markdown / format compliance** | ✅ | ✅ | ✅ | ⚠️ Extra prose around structured output is common |

---

## Behavioral Differences by Dimension

### Output Length

Models calibrate default output length differently.

| Model | Tendency | Portable Mitigation |
|---|---|---|
| GPT-4o | Moderately verbose; matches instruction-specified length well | Specify word/token count explicitly |
| Claude 3.5 | Verbose by default; thorough answers with justifications | Add: `Be concise. Limit your response to [N] sentences.` |
| Gemini 1.5 | Terse to moderate; sometimes truncates before completing structured output | Add explicit completion instruction: `Complete all fields.` |
| Llama 3.1 70B | Variable; depends heavily on system prompt | Repeat length constraints in both system and user turns |

### JSON Compliance

Getting raw, parseable JSON is one of the most common prompt engineering challenges.

| Model | Behavior without JSON mode | Best Practice |
|---|---|---|
| GPT-4o | Wraps JSON in markdown fences unless `response_format: json_object` is set | Use API-level JSON mode |
| Claude 3.5 | Returns prose with embedded JSON unless tool-use API is used | Define a tool with the required schema; or instruct: `Reply ONLY with valid JSON. No prose. No markdown.` |
| Gemini 1.5 | Native constrained decoding when used via the Gemini API response schema | Pass `response_schema` in API call; or use strong prompt: `Output only a valid JSON object matching this schema: {...}` |
| Llama 3.1 70B | Frequently wraps output in markdown fences; plain JSON unreliable without instruction | Start prompt with example of the exact JSON format; use `json` tag in prompt if using llama.cpp or Ollama |

**Universal portable pattern:** Instruction-level guarantee without structured-output APIs:

```
[CRITICAL] Respond with ONLY a valid JSON object. No prose before or after. No markdown code fences.
The JSON must match this exact schema:
{
  "field_name": "string",
  "count": 0
}
```

### Role Assignment (System Prompt)

| Model | How system prompts are processed | Notes |
|---|---|---|
| GPT-4o | `system` message is strongly respected; persists throughout conversation | Place all behavioral instructions in `system`; use `user` for task only |
| Claude 3.5 | `system` message is respected but Claude may contextually override it in multi-turn if user requests conflict | Restate key constraints in long conversations |
| Gemini 1.5 | `systemInstruction` field respected; in multi-turn, behaves like a persistent context | Some nuance: Gemini may partially override safety-adjacent instructions even in system context |
| Llama 3.1 70B | System prompt weight decreases in long conversations; last user message often dominates | For strict compliance, repeat role assignment in each user turn for critical instructions |

### Safety Refusals

| Model | Refusal Profile | Mitigation for Legitimate Edge-Case Requests |
|---|---|---|
| GPT-4o | Balanced; sometimes over-refuses dual-use content (e.g., security audit prompts) | Provide explicit professional context: `This is for a security audit. The codebase is yours.` |
| Claude 3.5 | More conservative on potentially harmful content; refuses more broadly on ambiguous requests | Specify intent explicitly and unambiguously; frame in professional context |
| Gemini 1.5 | Similar to GPT-4o; generally permissive for developer/enterprise use cases | Rare issues; addressing `SafetySettings` in API call is the escalation path |
| Llama 3.1 70B | Depends on fine-tune; base Llama 3.1 has minimal RLHF refusals | If deploying Llama-based systems: implement your own safety filtering layer |

---

## Prompting Strategies for Maximum Portability

These five strategies reduce model-specific behavioral variation without sacrificing output quality.

### Strategy 1: Make Format Explicit at Both Ends

Place format instructions at the beginning AND end of the assistant instruction (the Sandwich Principle from Module 4 §4.2):

```
[OPENING]
You are a ... Respond with a JSON object following this schema: {...}

[CONTENT]
Here is the input: ...

[CLOSING]
Remember: output ONLY the JSON object. No prose, no markdown fences.
```

### Strategy 2: Use Exact Output Anchors When Possible

Start expected output with a literal prefix the model must complete. This works on all major models:

```
Classify the review below. Respond starting with "Classification:" followed by exactly one word.

Review: "..."

Classification:
```

### Strategy 3: Explicit Negative Constraints (With Repetition)

For models that partially ignore negative constraints, repeat them:

```
Do NOT include:
- Explanatory prose
- Markdown formatting
- Anything other than the JSON object

[task]

Do NOT add prose or markdown. Output only: {...}
```

### Strategy 4: Context-Independent Role Assignment

For Llama and other models where system prompt weight degrades, encode role in user turn:

```
[As a [ROLE]: You are a senior security engineer. Only report confirmed vulnerabilities.]

Audit the following:
```

### Strategy 5: Calibrate CoT Usage Per Model

| Scenario | Recommendation |
|---|---|
| GPT-4o / Claude 3.5 on complex reasoning | CoT helps *(approx. +10–20% on multi-step tasks)* |
| GPT-4o / Claude 3.5 on simple extraction | Direct instruction without CoT — CoT adds latency and verbose output |
| Gemini 1.5 on reasoning | CoT helps similarly to GPT-4o class models |
| Llama 3.1 70B on reasoning | CoT is often required even for tasks where GPT-4o succeeds zero-shot |
| Any model on format-strict tasks | Disable CoT — reasoning tokens contaminate structured output |

---

## Migration Checklist: Switching Your Prompt to a New Model

When porting a prompt from one model to another, work through this checklist:

- [ ] **System prompt:** Does the new model have a separate system prompt channel, or do I need to embed it in the user turn?
- [ ] **JSON output:** Does the new model have a native JSON/structured output API? If not, add explicit format instructions.
- [ ] **Length calibration:** Run 5 test cases and check if the new model's default output length matches the expected range.
- [ ] **Refusal check:** Does any instruction trigger an unexpected refusal? Add professional framing if so.
- [ ] **Negative constraints:** Verify that "Do NOT..." instructions are being honored. If not, repeat them.
- [ ] **CoT applicability:** Does this task benefit from CoT on the new model? Test both with and without.
- [ ] **Tool-calling:** If the prompt uses tool-calling, verify the new model's function schema syntax matches (OpenAI vs. Anthropic tool-use vs. Gemini function declarations differ slightly).

---

## Further Reading

- Module 5 §5.5 — Cross-model portability strategies
- Module 4 §4.1 — Token budget management (context window differences)
- [Adversarial Robustness Comparison](adversarial-robustness-comparison.md) — how safety behavior differs across models

---

[← Back to comparisons](../README.md#deep-dive-comparisons) · [Module 5 →](../05-advanced-patterns.md)
