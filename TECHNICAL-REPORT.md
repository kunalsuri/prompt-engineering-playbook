# A Practical Playbook for Prompt Engineering 

**Draft Status:** v0.1.0-beta release
**Author:** Kunal Suri
**Date:** March 1, 2026
**Repository:** [https://github.com/kunalsuri/prompt-engineering-playbook](https://github.com/kunalsuri/prompt-engineering-playbook)
**DOI:** [https://doi.org/10.5281/zenodo.18827631](https://doi.org/10.5281/zenodo.18827631)

---

## Abstract

This report introduces the *Prompt Engineering Playbook*, an open-source educational repository that provides a structured, seven-module curriculum and a library of reusable prompt templates for large language model (LLM)-powered software development. Designed for developers, educators, students, researchers, and AI enthusiasts, the playbook covers the full spectrum of prompt engineering — from foundational concepts such as zero-shot and few-shot learning through advanced techniques including chain-of-thought reasoning, retrieval-augmented generation, adversarial robustness, and autonomous agentic architectures. By combining research-grounded curriculum materials with production-ready prompt files for multiple technology stacks (Python, React/TypeScript, React + FastAPI, Node.js/TypeScript), the repository serves as a centralized, hands-on resource that bridges the gap between academic theory and practical application in LLM-assisted development workflows. By providing stack-specific, version-controlled prompts, this playbook reduces trial-and-error overhead and standardizes AI interactions for development teams.

**Keywords:** prompt engineering, large language models, developer tools, GitHub Copilot, open-source education, few-shot learning, chain-of-thought, agentic AI, retrieval-augmented generation, VS Code

---

## 1. Introduction

### 1.1 Context

Large language models have rapidly become integral to modern software development, research, and knowledge work. Systems such as OpenAI's GPT-4, Anthropic's Claude, Google's Gemini, and open-weight models like Meta's Llama are now embedded into developer toolchains, writing assistants, and autonomous agents used by millions of practitioners worldwide. The ability to interact effectively with these models — commonly referred to as *prompt engineering* — has emerged as a critical skill. Well-crafted prompts can dramatically improve the quality, reliability, and safety of LLM outputs, while poorly constructed prompts lead to hallucinations, inconsistent behavior, and wasted compute resources.

The academic foundations are well established. Brown et al. (2020) demonstrated that GPT-3 could perform tasks from only a handful of examples (few-shot learning), Wei et al. (2022) showed that chain-of-thought prompting unlocks multi-step reasoning capabilities, and Yao et al. (2023) introduced ReAct to synergize reasoning with tool-use in agentic workflows. These landmark works, among others, have produced a rich but fragmented body of knowledge.

### 1.2 The Problem

Despite the growing importance of prompt engineering, practitioners face several barriers to effective skill acquisition:

1. **Fragmentation.** Research papers, blog posts, and documentation are scattered across dozens of sources with no unified curriculum or progression path.
2. **Theory–practice gap.** Academic publications establish empirical foundations but rarely provide copy-paste-ready templates that developers can immediately apply to production codebases.
3. **Accessibility.** Many high-quality resources are hidden behind paywalls, gated platforms, or require specialized ML backgrounds that exclude a large portion of the potential audience.
4. **Stack specificity.** Generic prompt engineering guides do not address the practical requirements of specific technology stacks (type systems, testing frameworks, style conventions), which are essential for tool-integrated workflows such as VS Code with GitHub Copilot.

### 1.3 The Solution

The *Prompt Engineering Playbook* addresses these challenges as a centralized, hands-on, open-source resource. It combines two complementary components:

- **A seven-module curriculum** (`learn/`) that takes learners from zero prior experience through advanced topics — including retrieval-augmented generation, prompt injection defense, multimodal prompting, evaluation pipelines, and agentic architectures — in approximately six hours of guided study.
- **A library of production-ready prompt templates** (`prompts/`) organized by technology stack, optimized for VS Code GitHub Copilot's agent mode but portable to any LLM interface.

The repository is licensed under MIT, follows Conventional Commits, provides a centralized APA-formatted bibliography with DOIs, and is accompanied by setup scripts, CI validation workflows, and a documentation site built with MkDocs.

---

## 2. Core Concepts Covered

The playbook teaches six major prompting patterns, four governing principles, and several advanced and agentic techniques. The following subsections provide a brief overview of each core concept.

### 2.1 Prompting Patterns

#### 2.1.1 Zero-Shot Instruction

A zero-shot prompt provides a task description with no examples, relying entirely on the model's pretrained knowledge to interpret the instruction. This pattern is appropriate when the task is well-defined and the expected output format is standard.

> *Example:* "You are a Python code reviewer. Review the following function for type annotation correctness, docstring completeness, and edge-case handling. Provide your review as a numbered list of findings."

#### 2.1.2 Few-Shot Learning

A few-shot prompt includes one or more input–output example pairs before the actual task, allowing the model to generalize by analogy through a process formally known as In-Context Learning (ICL). Few-shot prompting is particularly effective when the desired format or reasoning style is difficult to describe but easy to demonstrate (Brown et al., 2020).

> *Example:* Providing three examples of converting natural-language descriptions to SQL queries, followed by a new description for the model to convert.

#### 2.1.3 Chain-of-Thought (CoT) Reasoning

Chain-of-thought prompting instructs the model to produce explicit intermediate reasoning steps before arriving at a final answer. Wei et al. (2022) demonstrated that this technique significantly improves accuracy on arithmetic, commonsense, and symbolic reasoning tasks.

> *Example:* Appending "Let's solve this step by step" to a math problem prompt, causing the model to show its working before producing the final numerical answer.

#### 2.1.4 Role-Playing

A role-playing prompt assigns the model a specific persona, domain expertise, or behavioral profile. This pattern constrains the model's response distribution toward outputs consistent with the assigned role, improving domain relevance, stylistic consistency, and response quality.

> *Example:* "You are a senior security engineer specializing in OWASP Top 10 vulnerabilities. Conduct a threat model review of the following API endpoint."

#### 2.1.5 Constrained Output

A constrained output prompt explicitly specifies the structure, schema, or format of the expected response — such as JSON with named keys, Markdown with specific header levels, or a typed data structure. This pattern reduces ambiguity and makes LLM outputs machine-parseable. In production systems, constrained output prompting is increasingly complemented by provider-level structured output APIs — such as OpenAI's JSON mode and response format schemas, or Anthropic's tool-use definitions — which enforce output structure at the decoding layer rather than relying solely on prompt instructions.

> *Example:* "Return your analysis as a JSON object with keys: `severity` (string), `description` (string), `suggested_fix` (string), `confidence` (float between 0 and 1)."

#### 2.1.6 ReAct (Reasoning + Acting)

ReAct (Yao et al., 2023) interleaves reasoning traces with tool-use actions in a loop, enabling agents to observe environmental feedback (e.g., search results, API responses) and adjust their approach dynamically. It forms the foundation for agentic workflows.

> *Example:* A prompt that instructs the model to follow a Thought → Action → Observation cycle: "Thought: I need to find the current exchange rate. Action: Search('USD to EUR exchange rate'). Observation: 1 USD = 0.92 EUR. Thought: Now I can compute the conversion."

### 2.2 Governing Principles

The curriculum is organized around four governing principles that apply across all prompting patterns:

1. **Specificity** — increase precision to narrow the output distribution toward intended results. Analogous to typed function signatures and API contracts in software engineering.
2. **Decomposition** — break complex tasks into focused subtasks, each addressed by a scoped prompt or prompt segment. Mirrors the Single Responsibility Principle.
3. **Iteration** — treat prompt engineering as a red–green–refactor cycle: write, observe, diagnose gaps, revise.
4. **Evaluation** — define explicit success criteria and measure prompt performance systematically, akin to automated testing in CI/CD pipelines.

### 2.3 System Prompts versus User Prompts

Modern LLM APIs draw a clear architectural distinction between *system prompts* (persistent instructions that define the model's behavior, persona, and constraints) and *user prompts* (per-turn task inputs). The playbook's prompt templates reflect this separation: `copilot-instructions.md` files function as system-level instructions that persist across interactions, while `.prompt.md` files serve as user-level task prompts invoked on demand. Understanding this boundary is critical for prompt template design — system prompts should encode invariants (style guides, safety rules, output schemas), while user prompts should encode task-specific parameters.

### 2.4 Advanced and Agentic Techniques

Beyond the foundational patterns, the playbook covers:

- **Retrieval-Augmented Generation (RAG):** Designing prompts that ground responses in dynamically retrieved context while preventing hallucination beyond the evidence (Lewis et al., 2020).
- **Adversarial Robustness:** Identifying and mitigating prompt injection attacks, aligned with OWASP Top 10 for LLM Applications (OWASP, 2025; Perez et al., 2022).
- **Multimodal Prompting:** Constructing prompts that combine text and images for tasks such as UI review and visual reasoning.
- **Evaluation Pipelines:** Implementing systematic assessment frameworks for prompt quality, including LLM-as-a-Judge approaches (Zheng et al., 2023) to measure specific metrics such as response relevance, factual groundedness, and precision/recall for constrained outputs.
- **Reasoning Models and Test-Time Compute:** Prompting strategies for reasoning-optimized models (e.g., OpenAI o1/o3, DeepSeek-R1) that perform extended chain-of-thought at inference time. These models shift the optimization target from prompt complexity to compute allocation, often performing best with concise, minimally scaffolded prompts — the opposite of traditional CoT elicitation (Snell et al., 2024). The curriculum covers when to use reasoning models versus standard instruction-following models and how prompting strategies differ between them.
- **Plan-and-Execute Agents:** Separating planning from execution to create structured, goal-directed agent workflows.
- **Reflection Loops:** Self-critique mechanisms where the model evaluates and iteratively improves its own outputs (Shinn et al., 2023).
- **Multi-Agent Collaboration:** Orchestrating multiple specialized agents on complex tasks, with memory management and tool-use design.

---

## 3. Playbook Architecture & Usage

### 3.1 Repository Structure

The repository is organized into four primary top-level directories:

```
prompt-engineering-playbook/
├── learn/                     # Seven-module curriculum + supplementary materials
│   ├── 00-orientation.md      # Narrative on-ramp (no technical background needed)
│   ├── 01-introduction.md     # Foundations: what prompt engineering is
│   ├── 02-core-principles.md  # Specificity, decomposition, iteration, evaluation
│   ├── 03-patterns.md         # Zero-shot, few-shot, CoT, ReAct, role-playing, constrained output
│   ├── 04-best-practices.md   # Token management, versioning, team workflows, anti-patterns
│   ├── 05-advanced-patterns.md # RAG, adversarial robustness, multimodal, evaluation
│   ├── 06-agentic-patterns.md # Plan-and-execute, reflection, multi-agent, memory, tool use
│   ├── comparisons/           # 8 deep-dive research-backed technique comparisons
│   ├── labs/                  # Lab framework (exercises planned for future release)
│   ├── prompt-examples/       # Worked examples for each pattern
│   ├── cookbook.md             # 20 copy-paste recipes for non-programming tasks
│   ├── cheatsheet.md          # One-page reference card
│   ├── glossary.md            # Term definitions
│   ├── beginners-guide.md     # Curated path for non-programmers
│   └── ...                    # Additional guides (debugging, meta-prompting, CI/CD)
│
├── prompts/                   # Reusable prompt templates by technology stack
│   ├── shared/                # Cross-stack instructions
│   ├── python/                # Python-specific prompts (7 templates)
│   ├── react-typescript/      # React + TypeScript prompts (8 templates)
│   ├── react-fastapi/         # Full-stack React + FastAPI prompts (3 templates)
│   └── nodejs-typescript/     # Node.js + TypeScript prompts (4 templates)
│
├── scripts/                   # Setup helper scripts per stack
│   ├── setup.sh               # Unified setup entry-point
│   ├── validate-prompt-schema.py
│   └── <stack>/setup.sh       # Stack-specific setup scripts
│
├── references.md              # Centralized APA bibliography with DOIs
├── GETTING-STARTED.md         # Installation and usage walkthrough
├── CONTRIBUTING.md            # Contributor guidelines and conventions
├── CHANGELOG.md               # Version history and migration guide
├── mkdocs.yml                 # Documentation site configuration
└── Makefile                   # Automation targets (lint, check, docs)
```

#### File Types

- **Markdown (`.md`):** All curriculum modules, comparison documents, guides, and documentation are written in Markdown with ATX-style headers, fenced code blocks with language identifiers, and Mermaid diagrams for visual representations.
- **Prompt files (`.prompt.md`):** Production prompt templates use Markdown with YAML frontmatter specifying `mode`, `description`, and `version` fields. These files integrate natively with VS Code GitHub Copilot's agent mode.
- **Python scripts (`.py`):** Validation scripts (e.g., `validate-prompt-schema.py`) enforce structural and formatting requirements on prompt files.
- **Shell scripts (`.sh`):** Setup helpers automate the installation of prompt templates into target projects.

### 3.2 How to Use the Playbook

#### For Learners

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kunalsuri/prompt-engineering-playbook.git
   cd prompt-engineering-playbook
   ```
2. **Navigate to the curriculum:** Open `learn/README.md` and follow the Learning Roadmap from Module 0 (Orientation) through Module 6 (Agentic Patterns). Each module builds on the previous one and includes 2–3 hands-on exercises. Estimated total study time is approximately six hours.
3. **Explore deep-dive comparisons:** After completing the core modules, consult the `learn/comparisons/` directory for detailed, research-backed analyses of techniques such as Chain-of-Thought variants, ReAct versus standard prompting, and cross-model portability.
4. **Use quick references:** The Cheat Sheet, Glossary, and Progress Tracker provide fast lookup and self-assessment support.

#### For Developers Using Prompt Templates

1. **Choose a stack:** Select from Python, React/TypeScript, React + FastAPI, or Node.js/TypeScript from the `prompts/` directory.
2. **Install templates via setup script (recommended):**
   ```bash
   bash setup.sh --stack python "$PWD"
   ```
   This copies the appropriate `copilot-instructions.md` and `.prompt.md` files into your project's `.github/` directory. Note that the script does not modify your package dependencies; ensure your testing frameworks (e.g., `pytest`, `jest`) match the instructions in the templates.
3. **Alternatively, install manually:**
   ```bash
   mkdir -p .github/prompts
   cp prompts/python/copilot-instructions.md .github/copilot-instructions.md
   cp prompts/python/prompts/*.prompt.md .github/prompts/
   ```
4. **Use in VS Code:** Open Copilot Chat and invoke prompt commands (e.g., `/create-feature`, `/review-code`, `/write-tests`) which correspond to the installed prompt files.

---

## 4. Target Audience and Educational Value

### 4.1 Educators

The playbook's modular, progressively sequenced curriculum makes it suitable for integration into university courses, boot camps, and corporate training programs. Educators can:

- **Adopt the full seven-module curriculum** as a self-contained prompt engineering unit (~6 hours of instruction plus ~20 hours for the research extension track).
- **Select individual modules** (e.g., Module 3 on patterns or Module 6 on agentic architectures) for topic-specific lectures or workshops.
- **Use the comparison documents** as assigned readings that expose students to primary research literature through an accessible, applied lens.
- **Leverage the worked examples** in `prompt-examples/` for live-coding demonstrations and in-class exercises.
- **Design assessment exercises** using the worked examples and cookbook recipes as starting points. A dedicated lab framework (`learn/labs/`) is scaffolded and planned for a future release.

The explicit citation apparatus — with all claims linked to a centralized APA bibliography — supports academic rigor and teaches students to evaluate empirical evidence critically.

### 4.2 Self-Learners

Individual learners — whether career-changers, hobbyists, or AI enthusiasts — benefit from:

- **A clear progression path:** Module 0 provides a story-first, jargon-free on-ramp; the Beginner's Reading Guide offers a curated path with plain-language signposts and code-free exercise alternatives.
- **Self-assessment tools:** The Progress Tracker provides a one-page checklist for every module, lab, comparison document, and research paper.
- **Practical output:** Learners complete the curriculum with not only conceptual understanding but also a library of reusable prompt templates they can immediately apply to their own projects.
- **The Prompt Cookbook:** 20 copy-paste recipes for everyday non-programming tasks (writing, analysis, research, communication, decision-making) allow non-developers to derive immediate practical value.

### 4.3 Developers and Engineering Teams

Professional developers and teams using AI-assisted development workflows gain:

- **Stack-specific prompt templates** tested with VS Code Copilot and adaptable to any LLM. Templates enforce best practices for specific ecosystems (e.g., Python 3.12+ type hints with `ruff`/`mypy`/`pytest`; strict TypeScript with Tailwind CSS and React Router v6).
- **Prompt versioning and CI integration:** The CI/CD Integration Guide covers regression testing, schema validation, and security scanning for prompt files within GitHub Actions workflows.
- **Promptops practices:** Module 4 covers token management, version control for prompts, team workflows, and common anti-patterns — the operational discipline needed to maintain prompts at team scale.
- **Security awareness:** Module 5 and the adversarial robustness comparison document provide practical defenses against prompt injection, aligned with OWASP's LLM Top 10.

---

## 5. Related Work

The *Prompt Engineering Playbook* builds upon and differentiates itself from several existing resources in the prompt engineering ecosystem:

- **Provider documentation.** OpenAI's *Prompt Engineering Guide* (2024) and Anthropic's *Prompt Engineering Documentation* (2024) offer authoritative, model-specific guidance but are inherently vendor-scoped, do not provide cross-model comparisons, and lack a progressive curriculum structure. The playbook synthesizes insights from multiple providers into a vendor-neutral curriculum.
- **Community collections.** Repositories such as `awesome-chatgpt-prompts` (Akinyele, 2023) and similar crowd-sourced catalogs prioritize breadth of example prompts but lack pedagogical sequencing, citation rigor, or stack-specific template integration. The playbook's prompts are structured with YAML frontmatter, semantically versioned, and CI-validated.
- **Framework hubs.** LangChain Hub and LangSmith provide prompt management within the LangChain ecosystem but are tightly coupled to that framework's abstractions. The playbook's templates are framework-agnostic and optimized for IDE-native workflows (VS Code + GitHub Copilot).
- **Academic surveys.** Liu et al. (2023) and others have produced comprehensive prompt engineering taxonomies, but these remain in paper format without accompanying executable templates or self-paced learning paths.
- **Prompt pattern catalogs.** White et al. (2023) established a systematic catalog of prompt patterns. The playbook extends this foundational work by mapping patterns to specific technology stacks and providing production-ready implementations.

To our knowledge, the *Prompt Engineering Playbook* is the first open-source resource that combines a research-cited, progressively structured curriculum with stack-specific, CI-validated prompt templates designed for IDE-native developer workflows.

---

## 6. Conclusion and Future Work

### 6.1 Summary

The *Prompt Engineering Playbook* fills a significant gap in the current landscape of AI education and tooling. By combining a research-grounded curriculum with production-ready prompt templates, it provides a unified resource that serves learners across the experience spectrum — from beginners encountering LLMs for the first time to senior engineers building agentic systems. The modular architecture, explicit citation practices, and open MIT license ensure the playbook can be adopted, adapted, and extended by a wide community.

The repository contributes to the field in three concrete ways: (1) it synthesizes fragmented research into a coherent, progressively structured curriculum; (2) it bridges the theory–practice gap by providing stack-specific, copy-paste-ready prompt templates tested with real developer toolchains; and (3) it establishes a model for open-source prompt engineering education — complete with versioned prompt files, CI validation, and a centralized bibliography — that others can replicate and improve.

### 6.2 Limitations

This work has several limitations that should be considered when evaluating its contributions:

1. **Cross-provider portability.** Standardizing prompts across different LLM providers (e.g., OpenAI vs. Anthropic vs. Meta) is inherently lossy due to varying architectures, RLHF training processes, and system prompt interpretations. Prompt templates that perform well with one model may yield degraded results with another without adaptation.
2. **No formal user study.** The playbook's educational effectiveness has not been validated through controlled user studies, classroom trials, or learner outcome measurements. Claims about study time estimates (~6 hours) and pedagogical value are based on the author's assessment rather than empirical data.
3. **Tooling scope.** Prompt templates have been primarily tested with VS Code GitHub Copilot. While designed to be portable, systematic testing with other AI coding assistants (Cursor, Cline, Windsurf, JetBrains AI) has not been conducted.
4. **Language limitation.** All curriculum materials and prompt templates are available only in English, limiting accessibility for non-English-speaking learners and development teams.
5. **Temporal sensitivity.** The rapid pace of model updates, new prompting techniques (e.g., evolving reasoning model paradigms), and shifting provider APIs may quickly deprecate specific prompt tactics. Users are encouraged to continuously assess prompt effectiveness within their specific environments.
6. **Lab content.** The `learn/labs/` directory currently contains a framework README but no fully developed lab exercises. Hands-on assessment materials are planned for a future release.

### 6.3 Future Work

Several directions for future development are planned or under consideration:

1. **Multimodal and Vision-Language Guides:** Expanding Module 5's multimodal section into a dedicated module covering vision-language models (GPT-4o vision, Gemini multimodal), including techniques for image-grounded prompting, video understanding, and audio transcription workflows.
2. **Agent Framework Integration:** Providing worked examples and prompt templates for popular agent orchestration frameworks such as LangChain, LangGraph, CrewAI, and AutoGen — demonstrating how the playbook's patterns map to framework-specific abstractions.
3. **Additional Stack Support:** Extending the prompt template library to Go and Rust ecosystems (currently on the roadmap for Q2–Q3 2026).
4. **Automated Prompt Optimization:** Full integration examples for DSPy (Khattab et al., 2023) and other automatic prompt optimization frameworks, enabling learners to experiment with programmatic prompt tuning.
5. **Interactive Extension:** Development of a VS Code extension for template scaffolding, providing an in-editor experience for browsing, customizing, and installing prompt templates.
6. **RAG-Enhanced Context Fetching:** Built-in Copilot rules for automatic context retrieval in large monorepos, reducing the manual effort required to ground prompts in codebase-specific knowledge.
7. **Expanded Evaluation Frameworks:** Extending evaluation templates to support deep multi-agent workflow testing, including metrics for agent coordination efficiency, tool-use accuracy, and goal completion rates.

---

## 7. References

Bach, S. H., Sanh, V., Yong, Z. X., et al. (2022). PromptSource: An integrated development environment and repository for natural language prompts. *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics: System Demonstrations*, 93–104. https://doi.org/10.18653/v1/2022.acl-demo.9

Brown, T. B., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems, 33*, 1877–1901. https://doi.org/10.48550/arXiv.2005.14165

Chung, H. W., Hou, L., Longpre, S., et al. (2022). Scaling instruction-finetuned language models. *arXiv preprint*. https://doi.org/10.48550/arXiv.2210.11416

Gao, Y., Xiong, Y., Gao, X., et al. (2024). Retrieval-augmented generation for large language models: A survey. *arXiv preprint*. https://doi.org/10.48550/arXiv.2312.10997

Greshake, K., Abdelnabi, S., Mishra, S., et al. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security*, 79–90. https://doi.org/10.1145/3605764.3623985

Khattab, O., Singhvi, A., Maheshwari, P., et al. (2023). DSPy: Compiling declarative language model calls into self-improving pipelines. *arXiv preprint*. https://doi.org/10.48550/arXiv.2310.03714

Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. *Advances in Neural Information Processing Systems, 35*. https://doi.org/10.48550/arXiv.2205.11916

Lewis, P., Perez, E., Piktus, A., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*, 9459–9474. https://doi.org/10.48550/arXiv.2005.11401

Liu, N. F., Lin, K., Hewitt, J., et al. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics, 12*, 157–173. https://doi.org/10.1162/tacl_a_00638

Ouyang, L., Wu, J., Jiang, X., et al. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems, 35*, 27730–27744. https://doi.org/10.48550/arXiv.2203.02155

OWASP. (2025). *OWASP Top 10 for Large Language Model Applications*. https://owasp.org/www-project-top-10-for-large-language-model-applications/

Park, J. S., O'Brien, J. C., Cai, C. J., et al. (2023). Generative agents: Interactive simulacra of human behavior. *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST)*. https://doi.org/10.1145/3586183.3606763

Perez, E., Huang, S., Song, F., et al. (2022). Red teaming language models with language models. *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 3419–3448. https://doi.org/10.18653/v1/2022.emnlp-main.225

Shinn, N., Cassano, F., Gopinath, A., et al. (2023). Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems, 36*. https://doi.org/10.48550/arXiv.2303.11366

Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2024). Cognitive architectures for language agents. *Transactions on Machine Learning Research (TMLR)*. https://doi.org/10.48550/arXiv.2309.02427

Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is all you need. *Advances in Neural Information Processing Systems, 30*, 5998–6008. https://doi.org/10.48550/arXiv.1706.03762

Wang, X., Wei, J., Schuurmans, D., et al. (2023). Self-consistency improves chain of thought reasoning in language models. *International Conference on Learning Representations (ICLR)*. https://doi.org/10.48550/arXiv.2203.11171

Wei, J., Wang, X., Schuurmans, D., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems, 35*, 24824–24837. https://doi.org/10.48550/arXiv.2201.11903

White, J., Fu, Q., Hays, S., et al. (2023). A prompt pattern catalog to enhance prompt engineering with ChatGPT. *arXiv preprint*. https://doi.org/10.48550/arXiv.2302.11382

Yao, S., Zhao, J., Yu, D., et al. (2023). ReAct: Synergizing reasoning and acting in language models. *International Conference on Learning Representations (ICLR)*. https://doi.org/10.48550/arXiv.2210.03629

Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems, 36*. https://doi.org/10.48550/arXiv.2306.05685

Zhou, Y., Muresanu, A. I., Han, Z., et al. (2023). Large language models are human-level prompt engineers. *International Conference on Learning Representations (ICLR)*. https://doi.org/10.48550/arXiv.2211.01910

Snell, C., Lee, J., Xu, K., & Kumar, A. (2024). Scaling LLM test-time compute optimally can be more effective than scaling model parameters. *arXiv preprint*. https://doi.org/10.48550/arXiv.2408.03314

---

## 8. Declaration on Usage of AI

**Coding:** GitHub Copilot (Pro/Enterprise), Google Antigravity, and open-weight models run via Ollama were used in Visual Studio Code to support development, primarily for code generation, completion, and debugging. All AI-assisted code was independently reviewed, tested, and refined by the author. The author takes full responsibility for the correctness and integrity of the codebase.

**Writing & Ideation:** Large language model (LLM) tools — specifically Anthropic Claude and Google Gemini models — were used to support brainstorming, structural organization, and language refinement during the writing process. All underlying arguments, intellectual contributions, and conclusions originate with the author. All AI-assisted material was critically reviewed and substantially revised by the author, who takes full responsibility for the accuracy, originality, and integrity of the published content.

---

*Cite this work:*

> Suri, K. (2026). *Prompt Engineering Playbook: Curriculum and Reusable Prompt Templates for LLM-powered Development*. Zenodo. https://doi.org/10.5281/zenodo.18827631
