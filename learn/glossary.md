# Glossary

Key terms used throughout the curriculum, listed alphabetically. Each definition is written for readers who may be encountering the term for the first time. Where a term is introduced in a specific module, the cross-reference is noted.

---

**Agent mode** — A VS Code Copilot operating mode (enabled via `mode: 'agent'` in YAML frontmatter) in which the model can autonomously read files, run terminal commands, and iterate on its output rather than producing a single response. See [Module 3, §3.7](03-patterns.md#37-pattern-6-react-reasoning-acting).

**Chain-of-thought (CoT)** — A prompting technique that instructs the model to produce explicit intermediate reasoning steps before arriving at a final answer, improving accuracy on multi-step tasks. Introduced by Wei et al. [Wei2022]. See [Module 3, §3.4](03-patterns.md#34-pattern-3-chain-of-thought-cot) and [CoT Comparison](comparisons/chain-of-thought-comparison.md).

**Constrained output** — A prompting pattern that specifies the exact structure, format, or schema of the expected response (e.g., JSON with named fields and typed values). See [Module 3, §3.6](03-patterns.md#36-pattern-5-constrained-output).

**Context window** — The maximum number of tokens (prompt + response combined) that a model can process in a single interaction. As of 2025, context windows range from 8K tokens for lightweight models to 200K+ for frontier models. See [Module 4, §4.1](04-best-practices.md#41-token-budget-management).

**Decomposition** — The principle of breaking complex tasks into smaller, focused subtasks, each addressed by a separate prompt or prompt segment. See [Module 2, §2.2](02-core-principles.md#22-principle-2-decomposition).

**Delimiter** — A marker (such as XML tags `<user_input>...</user_input>` or triple backticks) used in prompts to clearly separate trusted instructions from untrusted input data. Used as a defense against prompt injection. See [Module 5, §5.2.3](05-advanced-patterns.md#523-defensive-prompt-engineering).

**Embedding** — A numerical vector representation of text produced by a specialized model. Used in RAG systems to convert queries and documents into vectors for semantic similarity search. See [Module 5, §5.1.1](05-advanced-patterns.md#511-concept-and-motivation).

**Evaluation pipeline** — An automated system that programmatically assesses prompt outputs against a test suite using defined metrics, enabling systematic comparison of prompt variants. See [Module 5, §5.4](05-advanced-patterns.md#54-systematic-evaluation-methodology) and [Evaluation Template](../prompts/shared/evaluation-template.md).

**Few-shot prompting** — A prompting strategy that includes one or more input–output example pairs in the prompt to demonstrate the expected behavior. The model generalizes by analogy from these examples. Established by Brown et al. [Brown2020]. See [Module 3, §3.3](03-patterns.md#33-pattern-2-few-shot-learning) and [Few-Shot Comparison](comparisons/few-shot-comparison.md).

**Frontier model** — An LLM at the current leading edge of capability (e.g., GPT-4, Claude 3+, Gemini). These models typically have the largest parameter counts and the most advanced training techniques.

**YAML frontmatter** — A metadata block at the top of a Markdown file, delimited by `---` lines, containing key–value pairs. In this repository, prompt files use YAML frontmatter with `mode` and `description` fields. See [GETTING-STARTED.md](../GETTING-STARTED.md).

**Grounding** — The property of an LLM response being based on verifiable evidence (retrieved documents, tool outputs, or provided context) rather than solely on the model's parametric knowledge. RAG and ReAct both aim to improve grounding.

**Hallucination** — When an LLM generates content that is factually incorrect, fabricated, or unsupported by the provided context — while presenting it with the same confidence as accurate information.

**In-context learning** — The ability of LLMs to perform tasks by conditioning on examples or instructions provided in the prompt, without updating model parameters. Few-shot prompting is the most common form. See [Brown2020].

**Instruction tuning** — A fine-tuning process in which a pretrained LLM is further trained on a dataset of (instruction, response) pairs to improve instruction-following capability. See [Instruction Tuning Comparison](comparisons/instruction-tuning-comparison.md).

**LLM (Large Language Model)** — A neural network trained on large amounts of text data that can generate, summarize, translate, and reason about natural language. Examples include GPT-4, Claude, Gemini, and Llama.

**LLM-as-judge** — An evaluation technique where a secondary LLM assesses the output quality of a primary LLM against a rubric. See [Module 5, §5.4.3](05-advanced-patterns.md#543-llm-as-judge) and [Zheng2023].

**Parametric knowledge** — Information encoded in a model's weights during pretraining. This knowledge is frozen at training time and cannot be updated without retraining or fine-tuning the model.

**Prompt engineering** — The disciplined practice of designing, structuring, and iterating on natural-language inputs to LLMs to elicit accurate, useful, and reproducible outputs. See [Module 1, §1.1](01-introduction.md#11-what-is-prompt-engineering).

**Prompt injection** — An adversarial attack in which malicious instructions are embedded in user input or retrieved data to override a model's system instructions. OWASP lists this as the #1 risk for LLM applications [OWASP2025]. See [Module 5, §5.2](05-advanced-patterns.md#52-adversarial-robustness-and-prompt-injection) and [Adversarial Robustness Comparison](comparisons/adversarial-robustness-comparison.md).

**Prompt template** — A predefined prompt structure with placeholders for variable inputs, enabling consistent and reusable prompt design. The `.prompt.md` files in this repository are prompt templates. See [PromptSource Comparison](comparisons/promptsource-comparison.md).

**RAG (Retrieval-Augmented Generation)** — An architecture that augments an LLM's context with documents retrieved from an external knowledge base at inference time, enabling responses grounded in current or domain-specific information. Introduced by Lewis et al. [Lewis2020]. See [Module 5, §5.1](05-advanced-patterns.md#51-retrieval-augmented-generation-rag).

**ReAct (Reasoning + Acting)** — A prompting paradigm that interleaves reasoning traces with tool-use actions, creating an observe–think–act loop. Introduced by Yao et al. [Yao2023]. See [Module 3, §3.7](03-patterns.md#37-pattern-6-react-reasoning-acting) and [ReAct Comparison](comparisons/react-comparison.md).

**RLHF (Reinforcement Learning from Human Feedback)** — A training technique in which a model is optimized to produce outputs preferred by human raters, using a learned reward model. Used in InstructGPT [Ouyang2022]. See [Instruction Tuning Comparison](comparisons/instruction-tuning-comparison.md).

**Role assignment (persona)** — A prompting pattern that assigns the model a specific identity or expertise level (e.g., "You are a senior security engineer") to steer its output toward domain-appropriate vocabulary and reasoning. See [Module 3, §3.5](03-patterns.md#35-pattern-4-role-playing-persona-assignment).

**Self-consistency** — A CoT variant that generates multiple reasoning paths at non-zero temperature and selects the most frequent answer via majority vote, improving reliability. Introduced by Wang et al. [Wang2023]. See [CoT Comparison](comparisons/chain-of-thought-comparison.md).

**Specificity** — The principle that increasing the precision and detail of a prompt reduces the space of plausible model outputs, thereby increasing the probability of a desired result. See [Module 2, §2.1](02-core-principles.md#21-principle-1-specificity).

**Stochastic** — Involving randomness. LLMs are stochastic systems: given the same input, they may produce different outputs across runs due to sampling during token generation.

**System prompt** — The initial instruction set provided to a model that establishes persistent behavioral constraints, role assignment, and rules for the entire conversation. In VS Code Copilot, the `copilot-instructions.md` file functions as the system prompt.

**Token** — The basic unit of text that an LLM processes. Tokens are typically subword units (a common word may be one token; an uncommon word may be split into multiple tokens). A rough heuristic for English text: 1 token ≈ 4 characters or ≈ 0.75 words. See [Module 4, §4.1](04-best-practices.md#41-token-budget-management).

**Zero-shot prompting** — A prompting strategy that provides a task description with no examples, relying entirely on the model's pretrained knowledge to interpret the instruction. See [Module 3, §3.2](03-patterns.md#32-pattern-1-zero-shot-instruction).

---

[← Back to curriculum](README.md)
