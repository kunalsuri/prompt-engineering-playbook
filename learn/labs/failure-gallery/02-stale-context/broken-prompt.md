# Case 02 — Stale Context

**Anti-pattern:** Hallucination Bait / Missing Grounding  
**Module reference:** Module 5 §5.1 (RAG), Module 2 §2.1

---

## Broken Prompt

```
You are a helpful assistant. What are the latest features in React 19? List every
new hook added in 2025, describe how the new concurrent rendering improvements work,
and give me the exact changelog entries for versions 19.2 through 19.5.
```

---

## Symptoms

When you run this prompt, the model will:
- Confidently describe React features that may not be accurate (the model's training has a cutoff)
- Fabricate specific version numbers and changelog entries
- Mix confirmed features with invented details
- Provide no indication of uncertainty

---

## Diagnosis Template

Fill this in before reading the solution:

1. **What critical information is the model missing?** _______________________
2. **What will the model do to fill that gap?** _______________________
3. **How does RAG (Module 5 §5.1) address this problem?** _______________________
4. **What explicit instruction could reduce hallucination without RAG?** _______________________

---

## Solution

See [solution.md](solution.md).
