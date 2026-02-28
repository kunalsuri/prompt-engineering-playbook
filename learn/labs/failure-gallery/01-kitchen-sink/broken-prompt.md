# Case 01 — Kitchen Sink

**Anti-pattern:** Kitchen-Sink Prompt  
**Module reference:** Module 4 §4.5

---

## Broken Prompt

```
You are an AI assistant. Help me with my Python project.

Please review the code, add type hints, fix any bugs, refactor the functions for
better readability, write unit tests, add docstrings, update the README, check for
security vulnerabilities, optimize for performance, make the variable names more
descriptive, and also make sure it follows PEP 8. Oh, and if you see any logging
opportunities, add those too. Also could you add error handling and maybe split the
large functions into smaller ones?

Here is my code:
[code]
```

---

## Symptoms

When you run this prompt, the model will:
- Attempt everything superficially rather than doing any one thing well
- Miss several of the twelve requested changes entirely
- Produce output that is hard to review because it mixes concerns
- Run out of token budget before completing the task

---

## Diagnosis Template

Fill this in before reading the solution:

1. **Primary anti-pattern name:** _______________________
2. **Count of distinct tasks requested:** _______
3. **What a well-decomposed version would look like:** 
   _______________________
4. **Which tasks should be done first vs. last and why:**
   _______________________

---

## Solution

See [solution.md](solution.md).
