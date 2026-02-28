# Module 3 — Prompting Patterns

## Learning Objectives

By the end of this module, you will be able to identify, select, and apply the six major prompting patterns, understand the empirical basis for each pattern's effectiveness, and navigate to the detailed comparison documents for deeper study.
!!! note "For Software Engineers"
    Prompting patterns are the design patterns of LLM interaction. You’ll recognise the analogues:

    | Prompting Pattern | SE Analogue |
    |---|---|
    | **Zero-shot** | Direct function call with no examples |
    | **Few-shot** | Doctests / examples-as-documentation |
    | **Chain-of-Thought** | Structured comments explaining logic step-by-step |
    | **ReAct** | State machine with external I/O |
    | **Role-Playing** | Interface / type declaration (“tell the model what it is”) |
    | **Constrained Output** | Strong typing / JSON schema validation |

    Combining patterns is like composing design patterns — powerful, but watch for token-budget trade-offs (covered in Module 4).
---

## 3.1 Overview: What Is a Prompting Pattern?

A prompting pattern is a reusable structural template for organizing the content of a prompt to achieve a specific class of outcomes. Patterns are to prompt engineering what design patterns are to software engineering — they encode proven solutions to recurring problems. The patterns described in this module are not mutually exclusive; production prompts frequently combine multiple patterns (e.g., role-playing with chain-of-thought, or few-shot with constrained output).

The six patterns covered here represent the current consensus of the prompt engineering community, grounded in empirical research from 2020–2025. Each section includes a definition, a worked example, guidance on when to use (and when not to use) the pattern, and cross-references to the repository's comparison documents and production templates.

---

## 3.2 Pattern 1: Zero-Shot Instruction

**Definition.** A zero-shot prompt provides a task description with no examples. The model relies entirely on its pretrained knowledge to interpret the instruction and generate an appropriate response.

**When to use.** Zero-shot is appropriate when the task is well-defined, the expected output format is standard (e.g., a Python function, a JSON object, a paragraph of prose), and the model is known to perform well on the task class. Most of the production prompts in this repository (e.g., `prompts/python/copilot-instructions.md`) are effectively zero-shot: they specify behavior through detailed instructions rather than through examples.

**When to avoid.** Zero-shot prompts are unreliable when the task involves unusual formatting, domain-specific conventions the model may not have encountered frequently in training, or subtle distinctions that are difficult to describe but easy to demonstrate.

**Worked example:**
```
You are a Python code reviewer. Review the following function for:
1. Type annotation correctness (PEP 484 / PEP 604 syntax)
2. Docstring completeness (Google style)
3. Edge-case handling

Provide your review as a numbered list of findings, each with a severity
(critical / warning / suggestion) and a concrete fix.

```python
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
```​
```

This prompt succeeds as zero-shot because code review is a well-represented task in LLM training data, the evaluation criteria are explicit, and the output format is clearly specified.

---

## 3.3 Pattern 2: Few-Shot Learning

**Definition.** A few-shot prompt includes one or more input–output example pairs before the actual task. The examples demonstrate the expected behavior, format, and reasoning style, allowing the model to generalize by analogy.

**Empirical basis.** Brown et al. [Brown2020] demonstrated that few-shot prompting enables GPT-3 to perform competitively with fine-tuned models on many benchmarks. The key finding is that example quality matters more than example quantity — two well-chosen examples often outperform ten mediocre ones.

**When to use.** Few-shot is particularly effective for tasks involving non-standard output formats, domain-specific terminology, classification with a fixed label set, or any situation where "show, don't tell" is more efficient than verbose description.

**When to avoid.** Few-shot prompts consume context-window tokens. If the task is straightforward and zero-shot performance is satisfactory, the additional tokens are wasted. Additionally, poorly chosen examples can *harm* performance by anchoring the model on irrelevant features.

**Worked example:**
```
Convert the following error messages into structured JSON with fields:
"level", "code", "message", and "suggestion".

Example 1:
Input: "TypeError: Cannot read property 'map' of undefined"
Output: {"level": "error", "code": "TS2532", "message": "Object is possibly undefined", "suggestion": "Add a null check or use optional chaining (?.)"}

Example 2:
Input: "Warning: Each child in a list should have a unique 'key' prop"
Output: {"level": "warning", "code": "REACT_KEY", "message": "Missing key prop in list rendering", "suggestion": "Add a unique `key` prop using item ID, not array index"}

Now convert:
Input: "ESLint: Unexpected console statement (no-console)"
```

**Cross-reference.** The comparison document `comparisons/few-shot-comparison.md` and the examples in `prompt-examples/prompt-patterns-in-practice.md` provide additional worked demonstrations of few-shot prompting across different tasks.

---

## 3.4 Pattern 3: Chain-of-Thought (CoT)

**Definition.** Chain-of-thought prompting instructs the model to produce explicit intermediate reasoning steps before arriving at a final answer. This can be triggered by a simple instruction ("Think step by step") or by providing examples that include reasoning traces.

**Empirical basis.** Wei et al. [Wei2022] showed that CoT prompting improves accuracy on arithmetic, commonsense, and symbolic reasoning tasks by 10–40 percentage points on benchmarks such as GSM8K and StrategyQA. The improvement is most pronounced on tasks requiring multi-step logic and is negligible on single-step retrieval tasks.

**Variants.** Three major CoT variants exist, each with distinct trade-offs:

**Few-Shot CoT** provides examples with full reasoning traces. This offers the most control over reasoning style but is token-expensive and requires carefully crafted demonstrations.

**Zero-Shot CoT** simply appends "Let's think step by step" (or similar) to the prompt. Kojima et al. [Kojima2022] demonstrated that this single phrase improves reasoning performance substantially, making it the lowest-effort CoT technique.

**Self-Consistency CoT** [Wang2023] generates multiple reasoning paths and selects the answer that appears most frequently. This improves robustness at the cost of increased compute (typically 5–20 sampled paths).

**When to use.** CoT is most valuable for tasks involving arithmetic, logical deduction, multi-step planning, or causal reasoning. It is also useful for code debugging, where forcing the model to trace execution step-by-step often surfaces errors that a direct "find the bug" prompt misses.

**When to avoid.** CoT adds latency and token cost. For classification, formatting, and retrieval tasks, CoT is unnecessary overhead.

**Cross-reference.** The `comparisons/chain-of-thought-comparison.md` document provides a detailed three-way comparison of these variants with empirical performance tables and selection criteria. It is strongly recommended reading after this section.

---

## 3.5 Pattern 4: Role-Playing (Persona Assignment)

**Definition.** A role-playing prompt assigns the model a specific identity, expertise level, or professional role. This steers the model toward domain-appropriate vocabulary, reasoning patterns, and output conventions.

**Mechanism.** Role assignment works because LLMs are trained on text written by people in specific roles. Prompting "You are a senior database administrator" activates distributional patterns associated with DBA-authored content — including appropriate concern for query performance, index design, and data integrity — that a generic prompt would not prioritize.

**Worked example from this repository.** The `prompts/react-fastapi/prompts/create-app-react-fastapi.prompt.md` implicitly assigns a full-stack senior engineer role through its detailed technology stack specification, architectural constraints, and quality expectations. The `prompts/react-typescript/prompts/auditor-cybersecurity-features.prompt.md` explicitly assigns multiple roles (Red-Team analyst, Blue-Team defender, AI Security specialist) to ensure multi-perspective coverage.

**When to use.** Role assignment is valuable whenever the task requires domain expertise, a specific level of technical depth, or a particular communication register. It composes well with all other patterns.

**When to avoid.** Avoid assigning roles that conflict with the task. An "expert beginner" role, for example, produces confused output. Also be aware that role assignment does not grant the model knowledge it does not have — it only adjusts how existing knowledge is expressed and prioritized.

---

## 3.6 Pattern 5: Constrained Output

**Definition.** A constrained-output prompt specifies the exact structure, format, or schema of the expected response. This ranges from simple format instructions ("respond in JSON") to full schema definitions with field types, enumerations, and validation rules.

**Why it matters.** Constrained output is essential for prompts that feed into downstream systems. A code-generation prompt whose output must be parseable by a CI pipeline cannot afford format variation. A security-audit prompt whose output must populate a JIRA ticket needs predictable field structure.

**Worked example from this repository.** The safety-gate prompt at `prompts/react-typescript/prompts/safety-gate-llm.prompt.md` exemplifies best-in-class constrained output: it defines a JSON schema with required fields (`safety_score`, `confidence`, `flags`, `explanation`), specifies value ranges and enumerations, and provides worked examples showing the expected output for different input scenarios. This is the gold standard for constrained-output prompt design.

**Techniques for enforcement.** Beyond verbal instructions, several techniques improve format compliance. Providing a JSON schema (as in the safety-gate prompt) is highly effective. Starting the model's response with the opening brace `{` or bracket `[` via a system-prompt prefix can force JSON output. For structured text, providing a template with placeholders (e.g., `## Findings\n\n### Finding 1\n- Severity: ___\n- Description: ___`) is more reliable than describing the format verbally.

### Structured Outputs via API

Many LLM providers now offer native structured-output modes that guarantee schema-valid responses — no prompt-level enforcement needed. When available, prefer these over prompt-only techniques:

- **OpenAI's `response_format`** — pass `{ "type": "json_schema", "json_schema": { ... } }` in the API call. The model is constrained at the decoding level to produce valid JSON matching the schema.
- **Anthropic's tool-use responses** — define a tool with an `input_schema`; the model returns arguments conforming to the schema.
- **Open-source constrained decoding** — libraries such as `outlines` and `guidance` apply grammar-based constraints during token generation, guaranteeing well-formed output for any model.

When structured-output modes are not available (e.g., in VS Code Copilot's prompt-file workflow), the prompt-level techniques above remain your primary tool.

---

## 3.7 Pattern 6: ReAct (Reasoning + Acting)

**Definition.** ReAct [Yao2023] interleaves reasoning traces with tool-use actions. The model thinks about what to do, executes an action (search, code execution, API call), observes the result, reasons about it, and decides the next action. This creates an observe–think–act loop that enables the model to interact with external systems.

```mermaid
flowchart LR
    Q["Question"] --> T1["Thought"]
    T1 --> A1["Action\n(tool call)"]
    A1 --> O1["Observation\n(tool result)"]
    O1 --> T2["Thought"]
    T2 -->|"need more info"| A2["Action"]
    A2 --> O2["Observation"]
    O2 --> T3["Thought"]
    T3 -->|"ready"| Ans["Answer"]
```

**Why it matters.** Pure LLM prompting is limited to the model's training data and the content of the context window. ReAct extends the model's capabilities to include real-time information retrieval, code execution, database queries, and any other tool accessible through an API. This is the foundation of modern AI agent architectures.

**Worked example (conceptual):**
```
Question: What is the current test coverage of the `auth` module?

Thought: I need to run the test suite with coverage measurement to answer this.
Action: execute_bash("pytest tests/auth/ --cov=auth --cov-report=term-missing")
Observation: Name          Stmts   Miss  Cover
                           auth/login.py     45      3    93%
                           auth/session.py   32      8    75%
                           TOTAL             77     11    86%
Thought: The overall coverage is 86%. The session module has the lowest
         coverage at 75%. I should report both the aggregate and the
         per-module breakdown.
Answer: The `auth` module has 86% test coverage overall. The `login.py`
        submodule is well-covered at 93%, while `session.py` is at 75%
        and would benefit from additional tests.
```

The YAML frontmatter field `mode: 'agent'` in this repository's prompt files indicates that those prompts are designed for VS Code Copilot's agent mode, which supports ReAct-style tool use.

**Cross-reference.** The `comparisons/react-comparison.md` document provides a detailed analysis of ReAct versus standard prompting, including performance comparisons on knowledge-intensive tasks.

### 3.7.1 Advanced Agent Patterns

Basic ReAct is a single reasoning-action loop. Production agent systems extend this into more sophisticated architectures. Understanding these patterns prepares you for building multi-step AI workflows.

**Plan-and-Execute.** Rather than deciding one action at a time, the model first generates a complete plan (a numbered list of steps), then executes each step sequentially, revising the plan if an intermediate result changes the approach. This reduces the problem of "greedy" action selection in basic ReAct, where the model picks locally optimal actions that lead to globally suboptimal paths.

```text
Question: Refactor the auth module to use JWT instead of session tokens.

Plan:
1. Read the current auth module to understand the session-based implementation.
2. Identify all files that import or reference session tokens.
3. Design the JWT token structure (claims, expiry, signing algorithm).
4. Implement the JWT generation and validation functions.
5. Update all dependent files to use the new JWT functions.
6. Update tests to cover JWT-specific cases.
7. Run the full test suite to verify no regressions.

Executing Step 1...
[Observation: auth/session.py contains login(), logout(), validate_session()]

Plan revision: No changes needed. Proceeding to Step 2.
```

**Reflection.** After completing a task (or failing at it), the model critiques its own output and iterates. Shinn et al. [Shinn2023] demonstrated that adding a reflection step — "What went wrong? How can I fix it?" — followed by a retry significantly improves success rates on coding and reasoning tasks. In prompt design, this means structuring a two-phase prompt:

1. **Act:** Generate the output (code, answer, analysis).
2. **Reflect:** Review the output against the requirements and identify errors, omissions, or improvements.
3. **Revise:** Produce a corrected version incorporating the reflection.

**Multi-tool orchestration.** Real-world agents need to choose among many tools — file search, code execution, web search, database queries, API calls. Effective multi-tool prompts:

- Provide a **tool catalog** listing each tool's name, description, required parameters, and return type.
- Include **tool selection heuristics**: "Use `search` when you need factual information. Use `execute_code` when you need to compute a result or verify code. Use `read_file` when you need the contents of a specific file."
- Specify **error recovery**: "If a tool call returns an error, diagnose the cause before retrying. Do not retry the same call with the same parameters more than once."

**When basic ReAct is sufficient.** Not every task needs advanced agent patterns. Use the simplest architecture that works:

- **Single-step retrieval or computation** → basic ReAct (1–2 tool calls).
- **Multi-step tasks with known steps** → plan-and-execute.
- **Tasks where first attempts often have errors** → reflection loop.
- **Tasks requiring diverse tools** → multi-tool orchestration with a tool catalog.

---

## 3.8 Combining Patterns

Production prompts rarely use a single pattern in isolation. The most effective prompts in this repository combine multiple patterns deliberately. For example, the cybersecurity audit prompt combines role-playing (multiple expert personas), constrained output (severity taxonomy, compliance mapping), chain-of-thought (requiring the model to explain its reasoning for each finding), and zero-shot instruction (no examples needed because the output structure is fully specified).

When combining patterns, be aware of **token budget trade-offs**. Few-shot examples are expensive; adding CoT reasoning traces on top further increases length. Module 4 covers token management strategies for complex prompts.

---

## Check Your Understanding

<details>
<summary><strong>Q1: Chain-of-Thought prompting delivers the largest gains on which type of task?</strong></summary>

**Answer:** **Multi-step reasoning tasks** — arithmetic, symbolic logic, planning problems, and science questions requiring intermediate deductions. CoT has little or no benefit on tasks with direct lookup answers (e.g., simple factual retrieval).

</details>

<details>
<summary><strong>Q2: What is the key difference between ReAct and standard Chain-of-Thought?</strong></summary>

**Answer:** Standard CoT produces a reasoning trace in a single forward pass without external calls. **ReAct** interleaves reasoning steps with **actions** (tool calls, searches, code execution), allowing the model to incorporate fresh external information before completing its reasoning. This makes ReAct suitable for tasks requiring real-time retrieval or computation.

</details>

<details>
<summary><strong>Q3: Why might two well-crafted few-shot examples outperform detailed zero-shot instructions on a text classification task?</strong></summary>

**Answer:** Examples demonstrate the **output distribution** concretely — they show label format, edge-case handling, and the assumed decision boundary. Instructions describe rules verbally, but models may interpret boundaries differently if the rules are ambiguous. Examples resolve that ambiguity with ground truth.

</details>

---

## Exercises

**Exercise 3.1 — Pattern Identification.** Select three prompt files from any `prompts/*/prompts/` directory in this repository. For each prompt, identify which patterns it uses (it may use multiple). Justify your classification by pointing to specific sections of the prompt text.

**Exercise 3.2 — Pattern Selection.** For each of the following tasks, determine which pattern or pattern combination would be most effective and explain your reasoning: (a) generating unit tests for an existing function, (b) debugging a race condition in concurrent code, (c) converting a REST API response into a typed TypeScript interface, (d) performing a literature review on a specific ML technique.

**Exercise 3.3 — Few-Shot Design.** Write a few-shot prompt (2–3 examples) for a task from your own work. Then write a zero-shot version of the same prompt that achieves comparable output quality through detailed instructions instead of examples. Compare the token counts and output quality. Which approach is more maintainable for your use case?

---

> **Validated against:** GPT-4o (2025-11), Claude 3.5 Sonnet, Gemini 1.5 Pro — February 2026.  
> Behavioral claims may drift as models are updated. Performance figures marked *(approx.)* are illustrative.

---

## References

- [Brown2020] Brown, T. B., et al. (2020). Language models are few-shot learners. *NeurIPS 33*, 1877–1901.
- [Kojima2022] Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. *NeurIPS 35*.
- [Shinn2023] Shinn, N., Cassano, F., Gopinath, A., Shakkottai, K., Labash, A., & Kambhampati, S. (2023). Reflexion: Language agents with verbal reinforcement learning. *NeurIPS 36*.
- [Wang2023] Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., … & Zhou, D. (2023). Self-consistency improves chain of thought reasoning in language models. *ICLR*.
- [Wei2022] Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 35*, 24824–24837.
- [Yao2023] Yao, S., et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*.
