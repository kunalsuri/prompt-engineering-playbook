# Case 01 — Solution

## Analysis

**Primary anti-pattern:** Kitchen-Sink Prompt  
**Tasks counted:** 12 distinct tasks (code review, type hints, bug fixes, refactoring, tests, docstrings, README, security audit, performance optimization, variable renaming, PEP 8, logging, error handling, function decomposition — actually 13+).

**Why this fails:**
- Each task requires different expertise, different output format, and different parts of the codebase
- The model cannot do all tasks deeply in a single context; it performs each task shallowly
- The reviewer of the output cannot tell which task produced which change
- Token budget: a thorough response to each of these 12 tasks might require 500–1000 tokens each; the combined task easily exceeds any practical context window
- Some tasks conflict: "optimize for performance" and "refactor for readability" sometimes push in opposite directions

## Fixed Version — Decomposed Prompts

Break into focused, independently-reviewable prompts:

**Prompt 1 — Bug Fix (run first; fixes must not be undone by later steps):**
```
You are a Senior Python Debugger. Review the following code for runtime errors,
logic errors, and unhandled exceptions only. Do not refactor, add types, or
change the logic beyond the minimum fix. List each bug as:
  - Location (function name + line estimate)
  - Description
  - Minimal fix (code snippet)

Code:
[code]
```

**Prompt 2 — Type Hints (run after bugs are fixed):**
```
You are a Python type annotation specialist. Add PEP 484/604-compliant type hints
to all function signatures and return types in the following code. Do not change
logic, variable names, or structure. Output: the modified code only.

Code:
[fixed code from Prompt 1]
```

**Prompt 3 — Refactor + PEP 8 (run after type hints):**
```
You are a Python code quality engineer. Refactor the following code to:
1. Split any function longer than 20 lines into smaller, single-responsibility functions
2. Rename vague variable names (use PEP 8 snake_case, descriptive)
3. Fix any remaining PEP 8 violations

Do not change function signatures, types, or logic. Output the refactored code.

Code:
[typed code from Prompt 2]
```

Continue this pattern for: docstrings, tests, security audit, performance, README.

## Key Lesson

One task per prompt. If a task requires multiple concerns, use decomposition sequences (Module 2 §2.2) where the output of each prompt feeds the next.
