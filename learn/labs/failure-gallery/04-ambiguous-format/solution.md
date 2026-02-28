# Case 04 — Solution

## Analysis

**Missing component:** Constraints — specifically, the output schema. The prompt defines the role (data analyst) and task (classify sentiment) but provides no output format specification. LLMs will choose their own format, which varies across runs, models, and temperature settings.

## Fixed Prompt

```
You are a data analyst. Classify the sentiment of each customer feedback item below.

Output ONLY a valid JSON array. Each element must have exactly these fields:
{
  "id": <integer, the item number>,
  "text": <string, the original feedback text, verbatim>,
  "sentiment": <string, exactly one of: "Positive", "Negative", "Neutral", "Mixed">,
  "confidence": <string, exactly one of: "High", "Medium", "Low">
}

Do not include any prose, explanation, or markdown before or after the JSON array.

Feedback items:
1. "The checkout process was fast and painless."
2. "I waited 45 minutes and nobody helped me."
3. "The product is okay but the packaging was damaged."
4. "Best experience I've had with any online store!"
5. "Returned it on day one. Terrible quality."

JSON output:
```

## Expected Output

```json
[
  {"id": 1, "text": "The checkout process was fast and painless.", "sentiment": "Positive", "confidence": "High"},
  {"id": 2, "text": "I waited 45 minutes and nobody helped me.", "sentiment": "Negative", "confidence": "High"},
  {"id": 3, "text": "The product is okay but the packaging was damaged.", "sentiment": "Mixed", "confidence": "High"},
  {"id": 4, "text": "Best experience I've had with any online store!", "sentiment": "Positive", "confidence": "High"},
  {"id": 5, "text": "Returned it on day one. Terrible quality.", "sentiment": "Negative", "confidence": "High"}
]
```

## What Changed

1. **Exact schema defined** — Every field, its type, and its allowed values are specified
2. **Enumerated values** — `sentiment` is constrained to 4 exact values; no invented categories possible
3. **Explicit JSON-only instruction** — Prevents prose wrappers and markdown code fences
4. **Output prefix anchor** — `JSON output:` at the end gives the model a completion cue that it is about to produce JSON (not prose)

## Key Lesson

For any task with a structured output (classification, extraction, analysis), define the exact output schema in the prompt. Enumerate allowed values. Specify the format (JSON, Markdown table, CSV). Use output anchors. This transforms a non-deterministic output distribution into a narrow, parseable one. See Module 3 §3.6.
