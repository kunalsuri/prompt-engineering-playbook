# Module 6 — Agentic Prompt Patterns

## Learning Objectives

By the end of this module, you will be able to design prompts for autonomous LLM agents, implement plan-and-execute architectures, build reflection loops that improve output through self-critique, orchestrate multi-agent collaboration, and apply memory and tool-use patterns to solve complex, multi-step tasks.

---

## 6.1 From Prompts to Agents

### 6.1.1 What Makes a Prompt "Agentic"?

Modules 1–5 treated prompts as single-turn or few-turn interactions: you send a prompt, the model responds, and you evaluate the output. **Agentic prompting** extends this into a loop where the LLM drives its own multi-step workflow — choosing tools, interpreting results, adjusting strategy, and iterating until a goal is met.

Module 3 §3.7 introduced ReAct [Yao2023] as a single pattern combining reasoning and action. This module generalizes ReAct into a family of agentic architectures, each suited to different problem structures. The key insight is that **the prompt is no longer just an instruction — it is a cognitive architecture specification** that defines how the agent perceives, reasons, acts, and learns within an episode.

### 6.1.2 The Agent Loop

All agentic systems share a common loop:

```
┌─────────────────────────────────────────────────────┐
│                   AGENT LOOP                         │
│                                                      │
│  1. PERCEIVE  — observe task state + tool outputs    │
│  2. REASON    — plan next step (chain-of-thought)    │
│  3. ACT       — call a tool or produce output        │
│  4. EVALUATE  — check if goal is met                 │
│  5. REPEAT    — return to step 1 if not done         │
│                                                      │
│  Exit: goal achieved OR max iterations reached       │
└─────────────────────────────────────────────────────┘
```

The differences between agentic architectures lie in *how* each step is implemented and *who* performs it (one model, multiple models, or a mix of models and code).

---

## 6.2 Plan-and-Execute

### 6.2.1 Concept

The plan-and-execute pattern separates **planning** (deciding what steps to take) from **execution** (performing each step). This separation addresses a core weakness of unconstrained ReAct: the model may wander aimlessly, repeating failed strategies or losing track of the overall goal.

The architecture uses two prompts:

1. **Planner prompt** — given the user's goal, produce a numbered plan of concrete steps.
2. **Executor prompt** — given one step from the plan, execute it using available tools and return the result.

An optional **re-planner** reviews progress after each step and revises the remaining plan if the intermediate results change the optimal path.

### 6.2.2 Planner Prompt Design

```
You are a planning agent. Given the user's goal, create a numbered plan
of 3–8 concrete, actionable steps. Each step should be independently
executable and produce a verifiable output.

Rules:
- Each step must start with an action verb (Search, Compute, Write, Verify).
- Each step must specify its expected output (e.g., "→ produces a list of 5 URLs").
- Include a final step that synthesizes all intermediate results into the
  deliverable the user requested.
- If the goal is ambiguous, state your assumptions before the plan.

User goal: {goal}

Plan:
```

**Key design choices:**
- The 3–8 step constraint prevents both under-planning (1 vague step) and over-planning (20 micro-steps that exceed context length).
- Requiring expected outputs makes progress verifiable — the executor can check whether each step succeeded.
- The action-verb rule reduces the chance of producing thought-steps ("Consider the implications...") instead of action-steps.

### 6.2.3 Executor Prompt Design

```
You are an executor agent. You have access to the following tools:
{tool_catalog}

Execute the following step from a larger plan:
Step {n}: {step_description}

Previous results from earlier steps:
{accumulated_context}

Instructions:
- Use the most appropriate tool for this step.
- If the step cannot be completed with available tools, explain why and
  suggest an alternative approach.
- Return your result in this format:
  RESULT: [your output]
  STATUS: [COMPLETE | PARTIAL | FAILED]
  NOTES: [any observations relevant to subsequent steps]
```

### 6.2.4 When to Use Plan-and-Execute

| Scenario | Recommended? | Reason |
| --- | --- | --- |
| Multi-step research tasks (literature review, competitive analysis) | ✅ Yes | Benefits from structured decomposition |
| Simple Q&A or single-tool tasks | ❌ No | Overhead of planning adds latency for no benefit |
| Tasks where optimal steps depend on intermediate results | ⚠️ With re-planner | Static plans fail when step 3's result changes what step 4 should be |
| Long-running tasks (>10 steps) | ⚠️ Carefully | Context window fills up; consider summarizing intermediate results |

---

## 6.3 Reflection and Self-Critique

### 6.3.1 Concept

Reflection [Shinn2023] adds a self-evaluation step to the agent loop. After producing an output, the model (or a separate critic model) reviews the output, identifies errors or gaps, and generates an improved version. This pattern is to agentic systems what code review is to software engineering: a quality gate that catches errors before they propagate.

### 6.3.2 The Reflection Prompt

A minimal reflection loop requires two prompts:

**Generator prompt** — produces the initial output (any task-specific prompt).

**Reflector prompt:**
```
You are a critical reviewer. Evaluate the following output against the
original requirements.

Original task: {task}
Output to review:
---
{output}
---

Evaluate on these dimensions:
1. Correctness — Are all facts and computations accurate?
2. Completeness — Does it fully address the task requirements?
3. Format compliance — Does it follow the specified output format?
4. Conciseness — Is there unnecessary content that should be removed?

For each dimension, assign PASS or FAIL with a one-sentence explanation.
If any dimension is FAIL, provide specific revision instructions.

Then produce the revised output incorporating all fixes.
```

### 6.3.3 Multi-Turn Reflection

For complex tasks, a single reflection pass may not suffice. Multi-turn reflection iterates until the reflector assigns PASS on all dimensions or a maximum iteration count is reached:

```python
# Pseudocode for multi-turn reflection
max_iterations = 3
output = generate(task)

for i in range(max_iterations):
    reflection = reflect(task, output)
    if all_pass(reflection):
        break
    output = revise(task, output, reflection)
```

**Important guard rail:** Always set a maximum iteration count. Without it, the reflection loop can cycle endlessly on subjective criteria ("Could be more concise" → "Now too terse" → "Could be more concise" → ...).

### 6.3.4 Empirical Evidence

Shinn et al. [Shinn2023] demonstrated that Reflexion — a verbal reinforcement learning approach where agents reflect on failures in natural language — improved success rates on coding tasks (HumanEval) from 80% to 91% and on decision-making tasks (AlfWorld) from 75% to 97%, using the same base model with no weight updates. The improvement comes purely from prompt-driven self-critique and retry, demonstrating the power of the reflection pattern.

### 6.3.5 Cross-Reference

The evaluation pipeline from Module 5, §5.4 can serve as an *external* reflection mechanism: instead of the model judging its own output, a separate evaluation prompt scores it against a test suite. Combining self-reflection (fast, per-output) with pipeline evaluation (thorough, per-variant) provides defense in depth.

---

## 6.4 Multi-Agent Collaboration

### 6.4.1 Why Multiple Agents?

A single prompt — no matter how well-crafted — forces the model into one perspective. Multi-agent architectures assign different **roles** to different LLM instances (or different prompts to the same model), enabling debate, specialization, and division of labor.

This is the advanced evolution of the role-playing pattern from Module 3 §3.5: instead of asking one model to *pretend* to be an expert, you create multiple agents that each *function* as a specialist, then orchestrate their collaboration.

### 6.4.2 Architecture: Supervisor–Worker

The most common multi-agent pattern uses a **supervisor agent** that:
1. Receives the user's request.
2. Decomposes it into sub-tasks.
3. Delegates each sub-task to a **worker agent** with a specialized prompt.
4. Aggregates worker outputs into a final response.

**Supervisor prompt:**
```
You are a project coordinator. You manage a team of specialist agents:
- RESEARCHER: Finds and summarizes relevant information.
- CODER: Writes and debugs code.
- REVIEWER: Evaluates code and text for quality and correctness.
- WRITER: Produces user-facing documentation and explanations.

Given the user's request, create a work plan that assigns tasks to agents.
For each assignment, specify:
1. Agent name
2. Task description (be specific enough for the agent to act independently)
3. Required inputs (from user or from another agent's output)
4. Expected output format

User request: {request}

Work plan:
```

**Worker prompt (example — REVIEWER):**
```
You are a code reviewer specializing in {language}. You receive code
from the CODER agent and evaluate it against these criteria:
1. Correctness — Does it implement the specification?
2. Security — Are there injection, overflow, or data-leak risks?
3. Performance — Are there obvious O(n²) or memory-waste issues?
4. Style — Does it follow {style_guide} conventions?

For each issue found, provide:
- Severity: CRITICAL | WARNING | SUGGESTION
- Location: function/line reference
- Fix: concrete code change

Code to review:
---
{code}
---
```

### 6.4.3 Architecture: Debate

In the **debate** pattern, two or more agents argue opposing positions, and a judge agent selects or synthesizes the best answer. This is effective for tasks where the correct answer is uncertain and benefits from adversarial scrutiny.

```
[Agent A — Advocate]
Argue that {position_a} is the best approach. Provide evidence,
examples, and address potential counter-arguments.

[Agent B — Challenger]
Argue that {position_b} is a better approach. Challenge Agent A's
reasoning and provide counter-evidence.

[Agent C — Judge]
You have read arguments from two expert agents. Evaluate both positions
on logical soundness, evidence quality, and practical feasibility.
Select the stronger position or synthesize a combined recommendation.
Explain your reasoning.
```

### 6.4.4 When to Use Multi-Agent vs. Single-Agent

| Factor | Single Agent | Multi-Agent |
| --- | --- | --- |
| Task complexity | Low to moderate | High (multiple domains or perspectives) |
| Latency tolerance | Low (one LLM call preferred) | Higher (multiple sequential/parallel calls acceptable) |
| Error criticality | Moderate | High (debate/review catches errors) |
| Token budget | Constrained | Sufficient for multiple prompts |
| Development overhead | Low | Higher (must design orchestration and routing) |

---

## 6.5 Memory Systems

### 6.5.1 The Memory Problem

LLMs are stateless — each API call starts with no memory of previous calls. Agentic systems that span many turns must synthesize their own memory from the conversation history, but naive approaches (concatenating all previous messages) quickly exhaust the context window.

### 6.5.2 Memory Architectures

**Short-term memory (working memory).** The most recent messages and tool outputs, kept in the context window. For most agents, the last 3–5 turns of interaction are sufficient for immediate task context.

**Long-term memory (episodic memory).** A persistent store of facts, decisions, and summaries from past interactions. Implemented as a retrieval system (vector database, key-value store) that the agent can query.

**Semantic memory (knowledge base).** Domain knowledge that remains constant across episodes — documentation, API references, company policies. This is the RAG pattern from Module 5 §5.1 applied to agent memory.

### 6.5.3 Memory Prompt Patterns

**Summarization-based memory:**
```
You are a memory manager. After each agent interaction, summarize the
key information into a structured note:

TASK_STATE: [current status of the overall goal]
DECISIONS_MADE: [bullet list of decisions and their rationale]
KEY_FACTS: [facts discovered that may be needed later]
OPEN_QUESTIONS: [unresolved issues]
NEXT_STEP: [what the agent should do next]

This summary replaces the full conversation history to save context space.
```

**Retrieval-based memory:**
```
Before answering the user's question, search your memory store for
relevant past interactions using these queries:
1. [Semantic query derived from the user's question]
2. [Query for any previous decisions on this topic]

Retrieved memories:
{retrieved_memories}

Use these memories as additional context. If a retrieved memory
contradicts current information, prefer the more recent source.
```

### 6.5.4 Practical Token Management for Agents

Long-running agents accumulate context across many turns. Apply these strategies (building on Module 4's token management principles):

1. **Sliding window** — keep only the last *k* turns in the context; summarize older turns.
2. **Hierarchical summarization** — every 5 turns, compress the oldest turns into a one-paragraph summary.
3. **Selective injection** — only include tool outputs that are relevant to the current step (the plan-and-execute pattern's accumulated context serves this purpose).
4. **Output truncation** — instruct tools to return concise results (e.g., "return the top 5 results, not all 200").

---

## 6.6 Tool-Use Design

### 6.6.1 The Tool Catalog

Module 3 §3.7 introduced tool use via the ReAct pattern. For production agents, a well-designed **tool catalog** is critical — it shapes how effectively the model selects and uses tools.

**Effective tool catalog entry:**
```
Tool: search_documentation
Description: Searches the product documentation index for passages
             relevant to a query. Use when you need factual information
             about product features, API endpoints, or configuration.
Parameters:
  - query (string, required): Natural language search query.
  - max_results (integer, optional, default=5): Number of passages to return.
Returns: A JSON array of {passage, source_url, relevance_score} objects.
Example:
  search_documentation(query="authentication token expiry", max_results=3)
```

**Design principles for tool catalogs:**
- **Describe *when* to use the tool**, not just what it does. "Use when you need factual information" is more helpful than just "Searches documentation."
- **Include a concrete example call.** Models choose tools more accurately when they've seen an example invocation.
- **Specify what the tool does NOT do.** "Does not execute code — use `run_code` for that." This prevents the model from misusing tools.
- **Keep the catalog concise.** If you have 20+ tools, group them into categories and provide selection heuristics (see Module 3 §3.7.1).

### 6.6.2 Error Handling in Tool Use

Agents frequently encounter tool errors — network timeouts, invalid parameters, empty results. Without explicit error-handling instructions, models tend to either silently ignore errors or retry infinitely.

```
Tool-use error handling rules:
1. If a tool returns an error, read the error message carefully.
2. Diagnose the cause:
   - PARAMETER_ERROR: You passed invalid arguments. Fix and retry once.
   - NOT_FOUND: The resource doesn't exist. Try an alternative approach.
   - RATE_LIMIT: Wait briefly and retry once.
   - UNKNOWN: Report the error to the user with the full error message.
3. Never retry the exact same call more than once.
4. If two different approaches both fail, stop and ask the user for guidance.
```

### 6.6.3 Tool Composition

Complex agent tasks often require chaining tool calls: search → read → compute → write. The prompt should provide **composition patterns** that demonstrate how tools work together:

```
Common tool sequences:
- Research: search_documentation → read_page → summarize
- Code fix: read_file → diagnose_error → edit_file → run_tests
- Data analysis: query_database → compute_statistics → create_chart
```

---

## 6.7 Designing Safe Agents

### 6.7.1 Scope Constraints

Agents with tool access can take real-world actions (writing files, sending emails, making API calls). Defining **scope constraints** in the system prompt is critical:

```
Scope constraints — you MUST follow these rules:
1. READ operations are always allowed (search, read, query).
2. WRITE operations require user confirmation:
   - Before writing/editing a file, show the proposed change and wait
     for approval.
   - Before sending any external request (API call, email), describe
     the request and wait for approval.
3. NEVER execute destructive operations (delete, drop, format) even
   if the user requests them — ask the user to perform these manually.
4. NEVER access resources outside the current project directory.
```

### 6.7.2 Preventing Agent Injection

The prompt-injection defenses from Module 5 §5.2 become even more critical in agentic systems because a successful injection could trigger tool actions, not just generate misleading text. Layer these additional defenses:

1. **Input sanitization** — treat all user input and tool output as untrusted data. Delimit them clearly (Module 5 §5.2.3).
2. **Action confirmation** — require the agent to state its intent before executing any write operation.
3. **Output filtering** — post-process the agent's tool calls programmatically to verify parameters before execution.
4. **Privilege separation** — run the agent's code execution tool in a sandboxed environment with no network access and limited file-system scope.

### 6.7.3 Graceful Degradation

Design agents to fail gracefully:

```
If you cannot complete the user's request:
1. Clearly state what you were able to accomplish.
2. Explain which step failed and why.
3. Suggest what the user can do to unblock the task.
4. Do NOT hallucinate a completed result. An honest partial result is
   always preferable to a fabricated complete one.
```

---

## 6.8 Putting It All Together: An Agent Blueprint

The following blueprint combines the patterns from this module into a complete agent system prompt. This is a structural template — adapt the specifics (tools, domain, constraints) to your use case.

```
# SYSTEM PROMPT — Agent Blueprint

## Identity
You are {agent_name}, a {domain} assistant powered by {model_name}.

## Capabilities
You have access to these tools:
{tool_catalog}

## Architecture
Follow the plan-and-execute workflow:
1. PLAN: Given the user's goal, create a numbered plan (3–8 steps).
2. EXECUTE: Work through each step using available tools.
3. REFLECT: After completing all steps, review your work:
   - Did you fully address the user's goal?
   - Are there errors or omissions?
   - If yes, revise the relevant steps.
4. DELIVER: Present the final result to the user.

## Memory
- Maintain a running summary of key decisions and findings.
- When context grows long, summarize older results before continuing.
- Reference your memory summary when planning subsequent steps.

## Tool Use
- Select the most appropriate tool for each step.
- Always check tool outputs for errors before proceeding.
- Never retry the exact same tool call more than once.
- Chain tools when needed (search → read → analyze → write).

## Safety and Scope
- READ operations: always allowed.
- WRITE operations: describe your intent and wait for user approval.
- NEVER execute destructive operations.
- NEVER fabricate results — honest uncertainty is always preferred.
- If you encounter content that violates safety guidelines, decline
  that specific sub-task and continue with the rest.

## Output Format
- Use markdown for structured output.
- Include section headers for long responses.
- For code, use fenced code blocks with language identifiers.
- End with a brief summary of what was accomplished and any open items.
```

---

## Check Your Understanding

<details>
<summary><strong>Q1: In a plan-and-execute architecture, what are the distinct responsibilities of the Planner, Executor, and Synthesizer?</strong></summary>

**Answer:** The **Planner** decomposes the user task into an ordered list of sub-tasks (N steps). The **Executor** receives one step at a time, has no knowledge of other steps, and returns a focused result. The **Synthesizer** receives all N results and composes the final user-facing answer. This separation enables targeted debugging: each role can be prompted and tested independently.

</details>

<details>
<summary><strong>Q2: What prompt injection risk is specific to tool-using agents that does not apply to single-shot LLM calls?</strong></summary>

**Answer:** **Indirect prompt injection via tool output.** Malicious content returned by a web search, database query, or file read can contain instructions (e.g., “Ignore all previous instructions and…”) that hijack the agent’s subsequent reasoning. Because the agent is designed to act on retrieved content, it may comply with injected instructions unless the system prompt explicitly disallows overrides from tool results.

</details>

<details>
<summary><strong>Q3: Why would adding a reflection step between the Executor and Synthesizer improve agent reliability?</strong></summary>

**Answer:** A reflection step asks the model to evaluate each executor output before passing it to the Synthesizer: “Is this result sufficient for Step N? If not, what is missing?” This catches low-quality intermediate results before they propagate and corrupt the final synthesis. Without reflection, a single bad executor step silently degrades the entire output.

</details>

---

## Exercises

**Exercise 6.1 — Plan-and-Execute.** Choose a complex research question (e.g., "Compare the three most popular Python web frameworks for building REST APIs in 2025"). Write (a) a planner prompt that decomposes this into steps, (b) an executor prompt for each step type, and (c) a re-planner prompt that adjusts the plan based on intermediate findings. Test your prompts by simulating the workflow manually.

**Exercise 6.2 — Reflection Loop.** Take your solution from any previous exercise and apply a two-pass reflection loop: (a) generate the initial output, (b) write a reflector prompt that critiques it, (c) apply the reflector and revise. Compare the initial and revised outputs. Did reflection improve quality? What types of errors did it catch?

**Exercise 6.3 — Multi-Agent Design.** Design a multi-agent system for code review. Define at least three specialist agents (e.g., Security Reviewer, Performance Reviewer, Style Reviewer) plus a Coordinator agent. Write the system prompt for each agent and the orchestration logic for the Coordinator. What are the advantages of this approach over a single comprehensive code-review prompt?

**Exercise 6.4 — Memory Management.** Design a memory management system for an agent that handles a multi-session customer support workflow. The agent must remember the customer's issue across sessions, track resolution progress, and avoid re-asking for information already provided. Write (a) the summarization prompt that runs after each session, (b) the retrieval prompt that loads relevant history at the start of a new session, and (c) an estimate of the token budget required for each component.

---

## Key Takeaways

1. **Agentic prompts define cognitive architectures**, not just instructions. The prompt specifies how the agent perceives, reasons, acts, and learns.
2. **Plan-and-execute separates thinking from doing**, making complex tasks more reliable and debuggable.
3. **Reflection loops catch errors cheaply** — verbal self-critique can approach the benefit of fine-tuning without weight updates [Shinn2023].
4. **Multi-agent systems enable specialization and adversarial quality checks**, at the cost of higher latency and token usage.
5. **Memory is an engineering problem**, not just a prompt problem. Combine summarization, retrieval, and sliding windows to manage token budgets.
6. **Safety is non-negotiable for tool-using agents.** Scope constraints, action confirmation, and sandboxing prevent prompt injections from causing real-world harm.

---

## 6.8 Reasoning Models and the Future of Prompt Engineering

A significant development in the LLM landscape is the emergence of **reasoning models** — models that allocate additional computation at inference time to "think" before responding (sometimes called "test-time compute scaling" [Snell2024]). Examples include OpenAI's o1/o3 series and other models that use chain-of-thought internally without explicit prompting.

### 6.8.1 What Changes with Reasoning Models

**Less prompting, more delegation.** With reasoning models, many traditional prompt-engineering techniques become less necessary:

- **Chain-of-thought prompting** is often redundant — the model reasons step-by-step internally. Adding "think step by step" to a reasoning model may actually degrade performance by conflicting with the model's built-in reasoning process.
- **Few-shot examples for reasoning tasks** may be unnecessary — the model can handle complex multi-step reasoning without demonstrations.
- **Decomposition prompts** that break tasks into substeps may compete with the model's own decomposition strategy.

**What still matters.** Even with reasoning models, the fundamentals of prompt engineering remain essential:

- **Specificity** (Module 2, §2.1) — clearly defining the task, constraints, and output format is always necessary.
- **Role assignment** — setting the model's perspective and expertise domain still shapes output quality.
- **Constrained output** — formatting requirements, schema compliance, and anti-pattern guidance remain important.
- **Safety and guardrails** — defensive prompting, tool-use constraints, and scope limitations are even more critical when models operate autonomously.
- **Evaluation** — structured testing and monitoring become more important, not less, as models handle more complex tasks.

### 6.8.2 Practical Guidance

**Know your model.** Before applying traditional techniques, check whether your model uses internal reasoning. If it does:
- Start with a simple, direct prompt and evaluate the output quality.
- Only add chain-of-thought scaffolding if the simple prompt produces reasoning errors.
- Avoid over-constraining the reasoning process — give the model room to think.

**Process supervision vs. outcome supervision.** Lightman et al. [Lightman2023] showed that verifying each reasoning step (process supervision) can outperform only checking the final answer (outcome supervision). For critical applications using reasoning models, consider adding a verification step that checks the model's reasoning chain, not just its conclusion.

**Adaptive complexity.** Not every task needs a reasoning model. Use lightweight models for simple classification, formatting, and extraction tasks. Reserve reasoning models for tasks that genuinely require multi-step thinking: mathematical problem-solving, code generation with complex constraints, strategic planning, and nuanced analysis.

---

> **Validated against:** GPT-4o (2025-11), Claude 3.5 Sonnet, Gemini 1.5 Pro — February 2026.
> Behavioral claims may drift as models are updated. Performance figures marked *(approx.)* are illustrative.

---

## References

- [Yao2023] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*. https://doi.org/10.48550/arXiv.2210.03629
- [Shinn2023] Shinn, N., Cassano, F., Gopinath, A., Shakkottai, K., Labash, A., & Kambhampati, S. (2023). Reflexion: Language agents with verbal reinforcement learning. *NeurIPS 36*. https://doi.org/10.48550/arXiv.2303.11366
- [Schick2023] Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. *NeurIPS 36*. https://doi.org/10.48550/arXiv.2302.04761
- [Park2023] Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST)*. https://doi.org/10.1145/3586183.3606763
- [Sumers2024] Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2024). Cognitive architectures for language agents. *Transactions on Machine Learning Research (TMLR)*. https://doi.org/10.48550/arXiv.2309.02427
- [Snell2024] Snell, C., Lee, J., Xu, K., & Kumar, A. (2024). Scaling LLM test-time compute optimally can be more effective than scaling model parameters. *arXiv preprint*. https://doi.org/10.48550/arXiv.2408.03314
- [Lightman2023] Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever, I., & Cobbe, K. (2023). Let's verify step by step. *ICLR*. https://doi.org/10.48550/arXiv.2305.20050

---

[← Module 5](05-advanced-patterns.md) · [Back to curriculum](README.md)
