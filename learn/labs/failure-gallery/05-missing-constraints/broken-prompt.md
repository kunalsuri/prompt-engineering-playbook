# Case 05 — Missing Constraints

**Anti-pattern:** Absent Role, Missing Constraints, Vague Task  
**Module reference:** Module 1 §1.3, Module 2 §2.1

---

## Broken Prompt

```
Explain machine learning.
```

---

## Symptoms

This prompt will produce:
- A 2000-word textbook overview when you wanted a 2-sentence summary
- A PhD-level technical paper when you needed a high-school explanation
- A Python tutorial when you needed conceptual understanding
- A Python tutorial focused on scikit-learn when you actually use PyTorch
- A different structure, depth, and focus every single run

The output is never "wrong" in an absolute sense — machine learning explanations are all valid. But none of them are right *for the person asking* because the person never said who they are, what they need it for, or what constraints apply.

---

## Diagnosis Template

Fill this in before reading the solution:

1. **List all five prompt components and mark which ones are present in this prompt:**
   - Role: present / absent
   - Context: present / absent
   - Task: present / absent
   - Constraints: present / absent
   - Examples: present / absent

2. **What is the minimum additional information needed to make this prompt reliable?**
   _______________________

3. **Rewrite the prompt for a specific use case of your choice:**
   _______________________

---

## Solution

See [solution.md](solution.md).
