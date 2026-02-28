# Before & After Gallery

> **15 side-by-side prompt comparisons organized by task.** Each entry shows a vague prompt, the improved version, and a one-line explanation of what changed. No pattern jargon required — just see the difference.

---

## How to Use This Page

1. Find a task that matches something you actually do.
2. Read the "Before" prompt — notice what's missing.
3. Read the "After" prompt — notice what was added.
4. Try both in any LLM and compare the outputs yourself.

---

## Writing & Communication

### 1. Summarizing a Document

**Before:**
```
Summarize this article.
```

**After:**
```
Summarize the following article in exactly 3 bullet points. Each bullet
should be one sentence. Focus on the author's main argument, the strongest
piece of evidence, and the practical implication. Write for a reader who
has not read the article.

[paste article here]
```

**What changed:** Added audience, format, length, and focus criteria. The model now knows *how many* bullets, *what* to cover, and *who* will read the summary.

---

### 2. Drafting an Email

**Before:**
```
Write an email to my boss about the project delay.
```

**After:**
```
You are a professional communicator who writes concise, respectful emails.

Write an email to my engineering manager, Sarah Chen, informing her that
the authentication feature will be delivered 5 business days late due to
an unexpected API dependency issue discovered during integration testing.

Tone: professional but not overly formal.
Length: 4–6 sentences in the body.
Include: a brief explanation of the cause, the revised delivery date
(March 14), and one concrete step you are taking to prevent recurrence.
Do not apologize more than once.
```

**What changed:** Added recipient identity, specific cause, tone calibration, length bounds, required content, and a negative constraint. The model produces a sendable email, not a generic template.

---

### 3. Writing a Cover Letter

**Before:**
```
Help me write a cover letter for a software engineering job.
```

**After:**
```
Write a cover letter for a Senior Backend Engineer position at Stripe.
I have 6 years of experience building payment systems in Python and Go,
led a team of 4 at my current company (FinCore), and reduced API latency
by 40% through database query optimization.

Requirements from the job posting:
- Distributed systems experience
- Strong Python skills
- Payment domain knowledge

Tone: confident but not arrogant. Length: 3 paragraphs, each 3–4 sentences.
Do not use phrases like "I am writing to express my interest" or
"I believe I would be a great fit."
```

**What changed:** Added specific experience, company name, job requirements, tone guidance, and banned clichés. The model writes a letter that sounds like a real person, not a template.

---

## Research & Analysis

### 4. Explaining a Concept

**Before:**
```
Explain machine learning.
```

**After:**
```
Explain supervised machine learning to a high-school student who has
taken algebra but no statistics. Use a concrete analogy (not
"teaching a dog tricks"). Keep your explanation under 150 words.
Do not use the words "algorithm," "optimization," or "neural network."
```

**What changed:** Added audience (high-school, algebra-level), a banned analogy, word limit, and vocabulary constraints. The model calibrates depth and language to the actual reader.

---

### 5. Comparing Options

**Before:**
```
Compare React and Vue.
```

**After:**
```
Compare React and Vue.js for a team of 3 mid-level developers building
an internal dashboard application with ~20 pages, no SSR requirement,
and a 6-month timeline.

Evaluate on these dimensions only:
1. Learning curve for developers who know vanilla JS but no framework
2. Component library ecosystem for data tables and charts
3. TypeScript support quality
4. Bundle size for a dashboard-scale app

Format: a Markdown table with one row per dimension, columns for React
and Vue, and a "Winner" column with a one-word verdict.
Do not include a general introduction or conclusion paragraph.
```

**What changed:** Added team context, project constraints, specific evaluation dimensions, output format, and scope boundaries. The comparison addresses *this decision* rather than the abstract question.

---

### 6. Summarizing Research

**Before:**
```
What does this paper say?
```

**After:**
```
Summarize the following research paper abstract. Provide:

1. **Research question** — What problem does this paper address? (1 sentence)
2. **Method** — How did they study it? (1 sentence)
3. **Key finding** — What is the main result? (1 sentence)
4. **Limitation** — What did the authors NOT test or account for? (1 sentence)
5. **So what?** — Why should a practitioner care? (1 sentence)

Abstract:
---
[paste abstract here]
---
```

**What changed:** Added structured dimensions, sentence limits, and a "so what?" requirement that forces practical relevance. The model produces an analysis, not a restatement.

---

## Coding & Technical Tasks

### 7. Writing a Function

**Before:**
```
Write a function to validate emails.
```

**After:**
```
Write a Python 3.12+ function called `validate_email` that:
- Accepts a single `str` argument and returns `bool`
- Uses `re` (no third-party libraries)
- Validates against RFC 5322 simplified rules: local part allows
  alphanumeric, dots, hyphens, and underscores; domain requires at
  least one dot with alphanumeric labels of 1–63 characters
- Includes a Google-style docstring with Args, Returns, and Raises
- Includes 3 positive and 3 negative inline doctests
- Raises `TypeError` if input is not a string
```

**What changed:** Added language version, function signature, validation specification, documentation style, test expectations, and error handling. Two different LLMs will produce structurally similar outputs.

**Source:** [Module 1, §1.2](01-introduction.md#12-a-motivating-example)

---

### 8. Debugging Code

**Before:**
```
Why doesn't this function work?

def get_max(numbers):
    max_val = 0
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
```

**After:**
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

**What changed:** Added specific test inputs (including edge cases), step-by-step tracing, and a structured output format. The model walks through execution rather than guessing at the bug.

**Source:** [Prompt Patterns in Practice, Example 3](prompt-examples/prompt-patterns-in-practice.md#example-3-chain-of-thought)

---

### 9. Code Review

**Before:**
```
Review this code for problems.
```

**After:**
```
You are a senior application security engineer conducting a
pre-deployment security review. Your expertise covers OWASP Top 10,
input validation, authentication, and data exposure.

Review the following Express.js route handler for security
vulnerabilities. For each finding, provide:
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

**What changed:** Added an expert persona, specific standards (OWASP, CWE), a structured output format, and a requirement for concrete fixes. The model responds with technical depth rather than surface observations.

**Source:** [Prompt Patterns in Practice, Example 4](prompt-examples/prompt-patterns-in-practice.md#example-4-role-playing-persona-assignment)

---

### 10. Generating Tests

**Before:**
```
Write tests for this function.
```

**After:**
```
Write a pytest test suite for the following Python function. Include:
- 3 positive test cases (valid inputs that should return expected outputs)
- 2 negative test cases (invalid inputs that should raise specific exceptions)
- 1 edge case (empty input, boundary value, or type boundary)

Use `pytest.raises` for exception tests. Include descriptive test names
that state the expected behavior (e.g., `test_returns_zero_for_empty_list`).
Do not use `unittest` or mocking — only `pytest` with built-in assertions.

```python
def calculate_average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate average of empty sequence")
    return sum(numbers) / len(numbers)
```​
```

**What changed:** Added framework, test categories with counts, naming convention, constraint on mocking, and specific assertion patterns. The output is drop-in usable.

---

## Planning & Decision-Making

### 11. Making a Decision

**Before:**
```
Should I use PostgreSQL or MongoDB?
```

**After:**
```
I am choosing a database for a new project with these characteristics:
- E-commerce platform with ~50K products and ~10K daily orders
- Complex queries: product search with filters, order aggregation reports
- Team of 3 developers, all experienced with SQL, none with MongoDB
- Hosted on AWS, budget-conscious (< $500/month for database)
- Must support ACID transactions for payment processing

Compare PostgreSQL and MongoDB for this specific use case. For each,
state: (1) fit for the query patterns, (2) team learning curve,
(3) estimated AWS hosting cost, (4) transaction support quality.

End with a one-sentence recommendation and the single strongest reason.
```

**What changed:** Added project constraints, team experience, budget, and specific evaluation criteria. The recommendation addresses *this* decision rather than the abstract debate.

---

### 12. Planning a Project

**Before:**
```
Help me plan my app.
```

**After:**
```
I am building a habit-tracking mobile app as a solo developer using
React Native and Firebase. I have 3 hours per day for 8 weeks.

Create a phased development plan with these constraints:
- Phase 1 must produce a working MVP I can demo
- Each phase lists 3–5 concrete deliverables (not "design the app")
- Every deliverable starts with an action verb (Build, Implement, Deploy)
- Mark each deliverable as Must-Have or Nice-to-Have

Output as a Markdown table with columns: Phase, Deliverable, Priority,
Dependencies (which earlier deliverables must be complete first).
```

**What changed:** Added tech stack, available time, phasing requirements, deliverable format, prioritization, and dependency tracking. The plan is actionable rather than aspirational.

---

## Learning & Study

### 13. Studying a Topic

**Before:**
```
Help me study for my biology exam.
```

**After:**
```
I have a biology exam on cellular respiration (glycolysis, Krebs cycle,
electron transport chain) in 3 days. I understand glycolysis well but
struggle with the Krebs cycle intermediate steps.

Create a study guide with:
1. A 5-question self-test on the Krebs cycle (multiple choice, answers
   at the bottom)
2. A simplified diagram description of the Krebs cycle showing inputs
   and outputs at each step
3. Three mnemonics for remembering the intermediate molecules
4. Two common exam trick questions on this topic with explanations

Write for a college freshman biology student.
```

**What changed:** Added specific topics, self-assessed weak areas, concrete deliverable types, and audience level. The model focuses effort where it's needed.

---

### 14. Getting Feedback on Writing

**Before:**
```
Is my essay good?
```

**After:**
```
You are a college writing tutor who gives honest, specific feedback.

Evaluate the following essay on three dimensions only:
1. **Thesis clarity** — Is the main argument stated clearly in the
   first paragraph? Can you restate it in one sentence?
2. **Evidence quality** — Does each body paragraph contain a specific
   example, statistic, or quote? Identify any paragraph that makes a
   claim without evidence.
3. **Transitions** — Rate the logical flow between paragraphs as
   smooth, adequate, or abrupt. Quote the weakest transition.

For each dimension, give a score (Strong / Adequate / Needs Work) and
one specific revision suggestion with a concrete example of how to
rewrite the weakest sentence.

Essay:
---
[paste essay here]
---
```

**What changed:** Added an expert persona, three specific evaluation dimensions, scoring criteria, and a requirement for concrete rewrite examples. The feedback is actionable rather than vague encouragement.

---

### 15. Explaining for Different Audiences

**Before:**
```
Explain how APIs work.
```

**After:**
```
Explain what a REST API is, written three ways:

1. **For a 10-year-old:** Use an analogy involving ordering food at a
   restaurant. No technical terms. 3 sentences maximum.
2. **For a business manager:** Focus on what APIs enable for the business
   (integrations, automation, data sharing). No code. 4 sentences.
3. **For a junior developer:** Include one concrete example using a
   GET request to a weather API, showing the URL, request, and response.
   5–6 sentences with a code snippet.

Label each version clearly. Do not repeat content between versions.
```

**What changed:** Added three distinct audiences with tailored constraints (analogy type, code inclusion, sentence limits) and a non-repetition rule. The model produces genuinely different explanations, not the same explanation at three verbosity levels.

---

## The Pattern

Every improvement above follows the same structure:

| What the "Before" is missing | What the "After" adds |
|-----|----|
| Who is the audience? | Specific reader/recipient identity |
| What exactly should be included? | Enumerated requirements or dimensions |
| How long should the output be? | Word/sentence/bullet count |
| What format should it use? | Table, JSON, bullet list, or template |
| What should be excluded? | Negative constraints ("do not...") |
| What does a good output look like? | Concrete examples or worked demonstrations |

This pattern maps directly to the five prompt components taught in [Module 1](01-introduction.md): **Role**, **Context**, **Task**, **Constraints**, and **Examples**.

---

## Next Steps

- **Want to understand the theory?** Start with [Module 1 — Introduction](01-introduction.md).
- **Want more before/after examples organized by pattern?** See [Prompt Patterns in Practice](prompt-examples/prompt-patterns-in-practice.md).
- **Want 20 copy-paste recipes?** See the [Prompt Cookbook](cookbook.md).
- **Want to debug a prompt that isn't working?** See the [Prompt Debugging Guide](prompt-debugging.md).

---

[← Back to curriculum](README.md)
