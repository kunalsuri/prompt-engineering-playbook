# Case 04 — Ambiguous Format

**Anti-pattern:** Missing Output Schema  
**Module reference:** Module 3 §3.6 (Constrained Output)

---

## Broken Prompt

```
You are a data analyst. I have a list of customer feedback. Analyze the sentiment
of each item and classify it. Here is the data:

1. "The checkout process was fast and painless."
2. "I waited 45 minutes and nobody helped me."
3. "The product is okay but the packaging was damaged."
4. "Best experience I've had with any online store!"
5. "Returned it on day one. Terrible quality."

Classify each item.
```

---

## Symptoms

When you run this prompt 5 times, you get 5 different output formats:
- Response 1: A numbered list with prose explanations
- Response 2: A Markdown table with Sentiment and Confidence columns
- Response 3: A JSON array
- Response 4: Bullet points grouped by sentiment category
- Response 5: One word per line, no structure

None of them are wrong, but none of them are predictable or directly parseable by downstream code.

---

## Diagnosis Template

Fill this in before reading the solution:

1. **Which prompt component is entirely missing?** _______________________
2. **What does "parseable by downstream code" require from the output?** _______________________
3. **Write the output format specification section for this prompt:**
   _______________________
4. **What module section covers this pattern?** _______________________

---

## Solution

See [solution.md](solution.md).
