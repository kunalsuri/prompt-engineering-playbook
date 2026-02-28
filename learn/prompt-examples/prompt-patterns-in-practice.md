# Prompt Patterns in Practice

This document provides worked examples of the six prompting patterns defined in [Module 3](../03-patterns.md), applied to practical coding tasks. Each section shows a naive prompt, the pattern-improved prompt, and a brief analysis of why the structured approach produces better results.

---

## Example 1: Zero-Shot Instruction

**Task:** Generate a Python utility function.

**Naive prompt:**
```
Write a function to check if a string is a palindrome.
```

**Pattern-applied prompt (zero-shot with explicit constraints):**
```
Write a Python 3.12+ function called `is_palindrome` that:
- Accepts a single `str` argument and returns `bool`
- Ignores case and non-alphanumeric characters (e.g., "A man, a plan, a canal: Panama" → True)
- Includes a Google-style docstring with Args, Returns, and Examples sections
- Includes three positive and two negative inline doctests
- Raises TypeError if the input is not a string
```

**Why it works:** The zero-shot constraints eliminate ambiguity about language version, handling of whitespace/punctuation, documentation style, and error behavior. Both LLMs will produce structurally similar outputs because the design space is tightly constrained.

**Pattern reference:** Module 3, §3.2

---

## Example 2: Few-Shot Learning

**Task:** Convert unstructured error messages into structured JSON.

**Naive prompt:**
```
Convert this error to JSON: "TypeError: Cannot read property 'map' of undefined"
```

**Pattern-applied prompt (few-shot with 2 examples):**
```
Convert error messages into structured JSON with fields: "level", "code", "message", "suggestion".

Example 1:
Input: "ReferenceError: x is not defined"
Output: {"level": "error", "code": "REF_UNDEF", "message": "Variable x is not defined in current scope", "suggestion": "Check variable spelling and ensure it is declared before use"}

Example 2:
Input: "Warning: Each child in a list should have a unique 'key' prop"
Output: {"level": "warning", "code": "REACT_KEY", "message": "Missing key prop in list rendering", "suggestion": "Add a unique key prop using item ID, not array index"}

Now convert:
Input: "TypeError: Cannot read property 'map' of undefined"
```

**Why it works:** The two examples demonstrate the output schema, severity classification, code naming convention, and the level of detail expected in suggestions. The model generalizes these patterns to the new input.

**Pattern reference:** Module 3, §3.3

---

## Example 3: Chain-of-Thought

**Task:** Debug a logic error.

**Naive prompt:**
```
Why doesn't this function work?
def get_max(numbers):
    max_val = 0
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
```

**Pattern-applied prompt (zero-shot CoT):**
```
Analyze the following Python function for bugs. Think step by step:
1. Trace the execution with the input [-3, -1, -7]
2. Trace the execution with the input [5, 3, 8]
3. Trace the execution with the input []
4. For each trace, state whether the output is correct and why.
5. List all bugs found with fixes.

def get_max(numbers):
    max_val = 0
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
```

**Why it works:** The step-by-step tracing forces the model to execute the function mentally with specific inputs, including edge cases (all negatives, empty list). This surfaces the bug (initializing `max_val = 0` fails for negative-only inputs and empty lists) more reliably than a vague "doesn't work" prompt.

**Pattern reference:** Module 3, §3.4

---

## Example 4: Role-Playing (Persona Assignment)

**Task:** Review code for security issues.

**Naive prompt:**
```
Review this code for problems.
```

**Pattern-applied prompt (role assignment):**
```
You are a senior application security engineer conducting a pre-deployment
security review. Your expertise covers OWASP Top 10, input validation,
authentication, and data exposure.

Review the following Express.js route handler for security vulnerabilities.
For each finding, provide:
- Severity (Critical / High / Medium / Low)
- CWE identifier
- Description of the vulnerability
- Concrete fix with code

app.post('/api/users', (req, res) => {
  const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;
  db.query(query, (err, result) => {
    res.json(result);
  });
});
```

**Why it works:** The security engineer role activates domain-specific knowledge about SQL injection, CWE classifications, and remediation patterns. The model responds with appropriate technical depth rather than generic advice.

**Pattern reference:** Module 3, §3.5

---

## Example 5: Constrained Output

**Task:** Classify the sentiment of customer feedback.

**Naive prompt:**
```
What's the sentiment of this review? "The product arrived late but works great."
```

**Pattern-applied prompt (constrained output with schema):**
```
Classify the sentiment of the following customer review. Respond with
ONLY a JSON object matching this exact schema — no additional text:

{
  "sentiment": "positive" | "negative" | "mixed",
  "confidence": <float 0.0–1.0>,
  "key_phrases": [<string>, ...],
  "summary": "<one sentence>"
}

Review: "The product arrived late but works great."
```

**Why it works:** The explicit JSON schema with typed fields, enumerated values, and value ranges ensures the output is parseable by downstream systems. The "no additional text" constraint prevents the model from adding conversational wrapper text.

**Pattern reference:** Module 3, §3.6

---

## Example 6: ReAct (Reasoning + Acting)

**Task:** Determine the test coverage of a specific module.

This example demonstrates the ReAct pattern conceptually. In practice, ReAct is implemented through VS Code Copilot's agent mode (`mode: 'agent'`), where the model can execute actions autonomously.

**Standard prompt (no tool use):**
```
What is the test coverage of the auth module?
```
*Result: The model guesses or states it cannot determine coverage without running tests.*

**ReAct pattern (agent mode):**
```
Determine the current test coverage of the auth module in this project.

Process:
1. Find the test files for the auth module.
2. Run the test suite with coverage measurement.
3. Report the overall and per-file coverage percentages.
4. Identify the least-covered file and suggest which functions need tests.
```

*Result: The agent reads the project structure, executes `pytest --cov`, observes the output, and produces a grounded report based on actual coverage data.*

**Why it works:** The ReAct pattern grounds the model's response in real observations rather than parametric guesses. The explicit process steps guide the reasoning–action loop.

**Pattern reference:** Module 3, §3.7

---

## Cross-References

- All patterns are defined in [Module 3 — Patterns](../03-patterns.md).
- The principles behind why these patterns work are covered in [Module 2 — Core Principles](../02-core-principles.md).
- Production-grade examples of these patterns in use can be found in the [`prompts/`](../../prompts/) directory.

---

[← Back to prompt examples](README.md) · [← Back to curriculum](../README.md)
