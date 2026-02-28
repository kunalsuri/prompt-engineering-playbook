# Research Extension Track

This directory provides a curated reading list and study guides for learners who want to go beyond the curriculum and engage with the primary research literature on prompt engineering, LLM reasoning, and agent systems.

---

## How to Use This Track

1. **Prerequisites:** Complete Modules 1–5 of the curriculum first. Module 6 (Agentic Patterns) is recommended but not required.
2. **New to research papers?** Read the "How to Read an ML Paper" primer below before starting.
3. **Reading order:** Papers are grouped by topic. Within each group, read in the order listed — earlier papers provide context for later ones.
4. **Study guide format:** Each paper entry includes a summary, key contributions, discussion questions, and connections to the curriculum.
5. **Time estimate:** ~2 hours per paper (reading + reflection). Budget 20–25 hours for the full track.

---

## How to Read an ML Paper

If you are a developer, researcher, or student without extensive experience reading machine learning papers, this primer will help you extract maximum value without getting lost in mathematical notation or unfamiliar conventions.

### Paper Structure (What to Expect)

Most ML papers follow a standard structure:

| Section | What It Contains | How to Read It |
|---------|-----------------|----------------|
| **Abstract** | One-paragraph summary of the problem, method, and key result | Read first — decide if the paper is relevant to your goals |
| **Introduction** | Motivation, problem statement, and high-level approach | Read fully — this is where the authors explain *why* their work matters |
| **Related Work** | How this paper differs from prior work | Skim — return to it after you understand the method |
| **Method** | Technical details of the approach | Read at the level of detail you need (see below) |
| **Experiments** | Evaluation setup, datasets, baselines, and results | Focus on the tables and figures first, then read the analysis |
| **Discussion/Conclusion** | Limitations, implications, and future directions | Read fully — the limitations section is often the most honest part of the paper |

### Reading Strategy: Three Passes

**Pass 1 — Survey (10 minutes).** Read the abstract, introduction, section headings, and conclusion. Look at all figures and tables. After this pass, you should be able to answer: *What problem does this paper solve? What is the key idea? What are the main results?*

**Pass 2 — Comprehension (30–60 minutes).** Read the full paper, skipping dense mathematical proofs on first encounter. Mark passages you do not understand but keep moving. Focus on understanding the experimental setup and results. After this pass, you should be able to explain the paper's contribution to a colleague.

**Pass 3 — Critical analysis (30–60 minutes, optional).** Re-read the method section carefully. Evaluate whether the experimental design supports the claims. Consider: *Are the baselines fair? Would this work on different data? What are the unstated assumptions?* This pass is where you form your own opinion rather than accepting the authors' framing.

### Practical Tips

- **Do not expect to understand every equation.** Many ML papers include mathematical formulations that are primarily for rigor and reproducibility. Understanding the intuition behind the method is more important for prompt engineering than following every derivation.
- **Read the tables first.** Tables typically contain the core empirical results. Understanding what was measured, what was compared, and which method won tells you most of what you need to know.
- **Pay attention to ablations.** Ablation studies systematically remove components of the method to show which parts matter. These are the most informative experiments for practitioners because they tell you what to prioritize.
- **Check the scale.** Note model sizes, dataset sizes, and compute budgets. A technique that works on GPT-4 with 100K examples may not transfer to your use case with a smaller model and 50 examples.
- **Follow citations backward.** If a paper references a concept you don't understand, find and read the cited foundational paper. The first 2–3 papers in any topic area establish the vocabulary everything else builds on.
- **Use LLMs to help.** Paste a confusing paragraph into an LLM and ask it to explain in plain language. This is a meta-application of the skills you are learning in this curriculum.

---

## Track 1: Foundations of In-Context Learning

### Paper 1: Language Models are Few-Shot Learners [Brown2020]

**Citation:** Brown, T. B., et al. (2020). Language models are few-shot learners. *NeurIPS 33*, 1877–1901.

**Summary:** Demonstrates that GPT-3 (175B parameters) can perform tasks with zero, one, or a few examples provided in-context — without gradient updates. Establishes the paradigm of "prompting" as an alternative to fine-tuning.

**Key Contributions:**
- Defined zero-shot, one-shot, and few-shot evaluation protocols for LLMs.
- Showed scaling laws: larger models benefit more from in-context examples.
- Identified tasks where prompting succeeds (translation, QA) and where it struggles (complex reasoning).

**Discussion Questions:**
1. Why does providing examples in the context improve performance, given that no weights are updated?
2. What are the practical implications of the finding that example quality matters more than quantity? How does this align with Module 3 §3.3?
3. The paper pre-dates instruction tuning (RLHF). How has instruction tuning changed the few-shot vs. zero-shot trade-off?

**Curriculum Connection:** Module 3 §3.2–§3.3; [Few-Shot Comparison](../comparisons/few-shot-comparison.md).

---

### Paper 2: Training Language Models to Follow Instructions with Human Feedback [Ouyang2022]

**Citation:** Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 35*, 27730–27744.

**Summary:** Introduces InstructGPT — fine-tuning GPT-3 with human feedback (RLHF) to follow instructions more reliably. The resulting model is preferred by humans over the 100× larger base GPT-3 on instruction-following tasks.

**Key Contributions:**
- Formalized the three-step RLHF pipeline: supervised fine-tuning → reward model → PPO optimization.
- Showed that alignment training makes models more responsive to prompt instructions, reducing the need for elaborate few-shot setups.
- Identified the "alignment tax" — aligned models sometimes sacrifice raw capability for safety/helpfulness.

**Discussion Questions:**
1. How does RLHF change what prompt engineers need to worry about? (Consider: do you need fewer examples? More explicit safety instructions?)
2. The paper shows that InstructGPT sometimes "over-refuses" safe requests. How does this relate to the Safety Refusal failure category in the [Prompt Debugging Guide](../prompt-debugging.md)?
3. What assumptions do the production prompts in this repository make about instruction-tuned models?

**Curriculum Connection:** Module 1 §1.2; [Instruction Tuning Comparison](../comparisons/instruction-tuning-comparison.md).

---

## Track 2: Reasoning and Chain-of-Thought

### Paper 3: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models [Wei2022]

**Citation:** Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 35*, 24824–24837.

**Summary:** Demonstrates that providing step-by-step reasoning traces in few-shot examples enables LLMs to solve multi-step reasoning problems (arithmetic, commonsense, symbolic) significantly better than standard prompting.

**Key Contributions:**
- Introduced "chain-of-thought" (CoT) as a prompting technique.
- Showed CoT is an emergent ability — it helps large models (>100B params) but not small ones.
- Achieved state-of-the-art on GSM8K (math) and StrategyQA (commonsense reasoning).

**Discussion Questions:**
1. Why might CoT be an emergent ability of scale? What does this imply for prompt design on smaller models?
2. Compare the CoT examples in the paper to the prompts in Module 3 §3.4. What structural elements make a reasoning trace effective?
3. Design an experiment (using the lab framework in `learn/labs/`) to test whether CoT helps on a task of your choosing.

**Curriculum Connection:** Module 3 §3.4; [Chain-of-Thought Comparison](../comparisons/chain-of-thought-comparison.md); [Lab 2](../labs/lab_02_chain_of_thought.py).

---

### Paper 4: Large Language Models are Zero-Shot Reasoners [Kojima2022]

**Citation:** Kojima, T., et al. (2022). Large language models are zero-shot reasoners. *NeurIPS 35*.

**Summary:** Shows that simply adding "Let's think step by step" to a prompt (with no examples) activates reasoning capabilities in LLMs, achieving strong performance on reasoning benchmarks without curated CoT demonstrations.

**Key Contributions:**
- Introduced "Zero-Shot CoT" — CoT with no examples, triggered by a simple phrase.
- Demonstrated that the trigger phrase matters: "Let's think step by step" outperforms alternatives like "Think carefully."
- Provided evidence that models have latent reasoning abilities that prompts can unlock.

**Discussion Questions:**
1. What does the success of Zero-Shot CoT tell us about the knowledge already embedded in large language models?
2. When would you choose Zero-Shot CoT over Few-Shot CoT? Consider the token budget implications (Module 4).
3. Try different trigger phrases on a fixed reasoning task and measure the difference. What makes certain phrases more effective?

**Curriculum Connection:** Module 3 §3.4; [Chain-of-Thought Comparison](../comparisons/chain-of-thought-comparison.md).

---

### Paper 5: Self-Consistency Improves Chain of Thought Reasoning [Wang2023]

**Citation:** Wang, X., et al. (2023). Self-consistency improves chain of thought reasoning in language models. *ICLR*.

**Summary:** Proposes sampling multiple reasoning paths from an LLM and selecting the most consistent answer via majority voting. This simple technique consistently improves accuracy over single-sample CoT.

**Key Contributions:**
- Introduced self-consistency decoding as a prompting-time technique (no training required).
- Showed 5–15% accuracy gains on arithmetic, commonsense, and symbolic reasoning tasks.
- Demonstrated that diverse reasoning paths catch different errors.

**Discussion Questions:**
1. Self-consistency requires multiple API calls. Calculate the cost multiplier for 5× sampling on a prompt that costs $0.01 per call. When is this worthwhile?
2. How does self-consistency relate to the evaluation pipeline concept in Module 5 §5.4?
3. Design a self-consistency wrapper for one of the lab experiments in `learn/labs/`.

**Curriculum Connection:** Module 5 §5.4; [Chain-of-Thought Comparison](../comparisons/chain-of-thought-comparison.md).

---

## Track 3: Agents and Tool Use

### Paper 6: ReAct: Synergizing Reasoning and Acting in Language Models [Yao2023]

**Citation:** Yao, S., et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*.

**Summary:** Combines chain-of-thought reasoning with external tool actions in an interleaved Thought-Action-Observation loop. This enables LLMs to solve tasks that require both reasoning and information retrieval.

**Key Contributions:**
- Formalized the Thought → Action → Observation loop for LLM agents.
- Showed benefits on knowledge-intensive tasks (HotpotQA, FEVER) and interactive environments (AlfWorld, WebShop).
- Demonstrated that reasoning traces improve action selection, and action results improve reasoning.

**Discussion Questions:**
1. How does ReAct differ from "just using tools"? What role does the explicit Thought step play?
2. Compare the ReAct pattern in Module 3 §3.7 to the paper's original formulation. What did the module simplify?
3. Design a ReAct prompt for a new task (e.g., planning a meal with dietary restrictions using a recipe search tool).

**Curriculum Connection:** Module 3 §3.7; Module 6 §6.1–§6.2; [ReAct Comparison](../comparisons/react-comparison.md).

---

### Paper 7: Reflexion: Language Agents with Verbal Reinforcement Learning [Shinn2023]

**Citation:** Shinn, N., et al. (2023). Reflexion: Language agents with verbal reinforcement learning. *NeurIPS 36*.

**Summary:** Introduces a framework where language agents reflect on failures in natural language, storing those reflections as episodic memory for future attempts. Significantly improves success rates on coding and decision-making tasks without model weight updates.

**Key Contributions:**
- Verbal self-reflection as a substitute for gradient-based learning.
- Episodic memory that persists across attempts.
- 80% → 91% on HumanEval coding tasks; 75% → 97% on AlfWorld decision tasks.

**Discussion Questions:**
1. How does verbal reflection compare to traditional reinforcement learning? What are the advantages and limitations?
2. Module 6 §6.3 presents reflection as a prompt pattern. How faithful is the module's treatment to the paper's original formulation?
3. Design a reflection prompt for a writing task (e.g., essay improvement) using the template from Module 6 §6.3.2.

**Curriculum Connection:** Module 6 §6.3; Module 5 §5.4 (external evaluation as complementary mechanism).

---

### Paper 8: Generative Agents: Interactive Simulacra of Human Behavior [Park2023]

**Citation:** Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. *UIST*.

**Summary:** Creates a simulated town of 25 AI-powered agents that plan daily activities, form relationships, spread information, and coordinate — all driven by LLM prompts combined with memory retrieval and reflection.

**Key Contributions:**
- Demonstrated a complete memory architecture: observation → retrieval → reflection → planning.
- Showed that LLM agents can exhibit emergent social behaviors (organizing a party, spreading rumors) not explicitly programmed.
- Introduced importance scoring for memory retrieval prioritization.

**Discussion Questions:**
1. How does the memory architecture in this paper compare to Module 6 §6.5? What would you adopt for a production agent?
2. The paper uses "importance scoring" to decide which memories to retrieve. Design a prompt that assigns importance scores to new observations.
3. What ethical considerations arise when creating convincing simulations of human behavior?

**Curriculum Connection:** Module 6 §6.4 (multi-agent), §6.5 (memory systems).

---

## Track 4: Safety and Robustness

### Paper 9: Red Teaming Language Models with Language Models [Perez2022]

**Citation:** Perez, E., et al. (2022). Red teaming language models with language models. *EMNLP*, 3419–3448.

**Summary:** Uses one LLM to automatically generate adversarial test cases that reveal harmful behaviors in a target LLM. Discovers failure modes that human red-teamers miss.

**Key Contributions:**
- Automated red teaming at scale (generated thousands of test cases).
- Discovered that models can produce harmful outputs even with safety training.
- Showed that LLM-generated attacks transfer across model families.

**Discussion Questions:**
1. How could you adapt LLM-based red teaming to test the safety of your own prompts? Design a red-teaming meta-prompt.
2. Exercise 5.2 asks you to manually red-team a prompt. How would automated red-teaming complement manual testing?
3. What are the ethical implications of publishing automated attack generation techniques?

**Curriculum Connection:** Module 5 §5.2; Module 6 §6.7; [Adversarial Robustness Comparison](../comparisons/adversarial-robustness-comparison.md).

---

### Paper 10: Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection [Greshake2023]

**Citation:** Greshake, K., et al. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. *ACM Workshop on AI Security*.

**Summary:** Demonstrates that LLM-integrated applications (email assistants, code copilots, search-augmented chatbots) are vulnerable to indirect prompt injection — malicious instructions hidden in data the model processes (web pages, emails, documents).

**Key Contributions:**
- Taxonomy of indirect injection attacks: data exfiltration, plugin/tool manipulation, social engineering through the AI.
- Real-world demonstrations against production systems.
- Defense analysis: no single technique fully mitigates indirect injection.

**Discussion Questions:**
1. How do the defensive techniques in Module 5 §5.2.3 hold up against the attacks described in this paper?
2. The RAG pattern (Module 5 §5.1) retrieves external documents into the prompt. How does this create attack surface for indirect injection?
3. Design a defense-in-depth strategy combining prompt-level defenses (Module 5 §5.2) with application-level defenses (Module 6 §6.7) for a RAG-based customer support bot.

**Curriculum Connection:** Module 5 §5.2; Module 6 §6.7.2; [Adversarial Robustness Comparison](../comparisons/adversarial-robustness-comparison.md).

---

## Track 5: Retrieval Augmentation and Evaluation

### Paper 11: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks [Lewis2020]

**Citation:** Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 33*, 9459–9474.

**Summary:** Introduces RAG — combining a non-parametric retrieval component (dense passage index) with a parametric generative model (BART). On knowledge-intensive NLP tasks, RAG outperforms models that rely solely on parametric memory, and can be updated without retraining.

**Key Contributions:**
- First end-to-end trainable RAG architecture (retriever + generator jointly optimized).
- Showed that hybrid parametric + non-parametric memory outperforms either alone.
- Demonstrated that updating the retrieval index at inference time updates the model's "knowledge."

**Discussion Questions:**
1. The paper trains the retriever and generator jointly. In a prompt-only RAG system (no training), what assumptions does your prompt need to make instead? See Module 5 §5.1.2.
2. How does the chunk size of retrieved documents affect your prompt design? (Consider context window limits from Module 4.)
3. Design a RAG prompt that specifically instructs the model to cite the retrieved passage and refuse to answer if the evidence is insufficient.

**Curriculum Connection:** Module 5 §5.1; [failure-gallery/02-stale-context](../labs/failure-gallery/02-stale-context/).

---

### Paper 12: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena [Zheng2023]

**Citation:** Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS 36*.

**Summary:** Introduces MT-Bench (multi-turn benchmark) and Chatbot Arena (Elo-based live evaluation) and studies LLM-as-judge reliability. Shows strong correlation between GPT-4 judgements and human preferences, validating LLM-as-judge as a scalable evaluation method.

**Key Contributions:**
- MT-Bench: 80 challenging multi-turn questions covering writing, reasoning, math, coding — with model-graded scoring.
- Chatbot Arena: public battle-format human preference platform with 30K+ evaluations.
- Identified three failure modes of LLM judges: position bias, verbosity bias, self-enhancement bias.

**Discussion Questions:**
1. The paper identifies position bias — judges prefer the answer in the first position. How would you design an evaluation prompt (Module 5 §5.4.3) to counteract this?
2. Verbosity bias means judges favor longer answers. Does the Lab 4 evaluation pipeline have this issue? How would you detect and correct it?
3. Design a judge prompt for evaluating the outputs of the debug-issue prompt template. What rubric dimensions would capture quality for that specific task?

**Curriculum Connection:** Module 5 §5.4; Module 2 §2.4 (evaluation); [Lab 4](../labs/lab_04_evaluation_pipeline.py).

---

## Track 6: Reasoning Models and Test-Time Compute

> This track covers the post-2024 shift toward models that allocate additional computation at inference time to improve reasoning quality. These developments fundamentally change the prompting calculus — techniques like explicit chain-of-thought may become unnecessary or even counterproductive with reasoning-native models.

### Paper 13: Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling Model Parameters

**Citation:** Snell, C., Lee, J., Xu, K., & Kumar, A. (2024). Scaling LLM test-time compute optimally can be more effective than scaling model parameters. *arXiv preprint*. https://doi.org/10.48550/arXiv.2408.03314

**Summary:** Demonstrates that allocating additional compute at inference time (via repeated sampling, verification, and search) can match or exceed the performance of much larger models. Establishes that test-time compute scaling follows predictable laws analogous to training-time scaling laws.

**Key Contributions:**
- Formalized the relationship between test-time compute budget and task performance.
- Showed that a smaller model with optimal test-time compute can outperform a 14× larger model on reasoning tasks.
- Identified two effective strategies: process-based reward models (verifying each step) and revision-based approaches (iterative self-correction).

**Discussion Questions:**
1. If test-time compute can substitute for model size, how does this change prompt design? Should prompts encourage more "thinking" even if it increases latency?
2. Compare this paper's "revision-based" approach to the Reflexion pattern in Module 6 §6.3. What are the structural similarities?
3. What are the cost implications for production systems? When is test-time compute scaling more economical than using a larger model?

**Curriculum Connection:** Module 3 §3.4 (CoT); Module 6 §6.3 (Reflection).

---

### Paper 14: Let's Verify Step by Step

**Citation:** Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever, I., & Cobbe, K. (2023). Let's verify step by step. *International Conference on Learning Representations (ICLR)*. https://doi.org/10.48550/arXiv.2305.20050

**Summary:** Compares outcome-based reward models (evaluating only the final answer) against process-based reward models (evaluating each reasoning step). Process supervision significantly outperforms outcome supervision on mathematical reasoning, achieving state-of-the-art on GSM8K and MATH benchmarks.

**Key Contributions:**
- Demonstrated that per-step verification catches errors earlier in the reasoning chain.
- Released the PRM800K dataset of step-level human labels.
- Showed that process supervision produces more interpretable reasoning traces.

**Discussion Questions:**
1. The paper validates individual reasoning steps. How could you apply this principle to prompt evaluation — verifying intermediate outputs in a multi-step prompt pipeline?
2. Compare step-level verification to the self-consistency technique from Paper 5 [Wang2023]. Which is more practical for a prompt engineer without access to a reward model?
3. Design a prompt that mimics process supervision: instruct the model to generate steps, then self-verify each step before proceeding.

**Curriculum Connection:** Module 3 §3.4 (CoT reasoning traces); Module 5 §5.4 (evaluation methodology).

---

### Paper 15: Thinking, Fast and Slow in Large Language Models

**Citation:** Saha, S., Hase, P., & Bansal, M. (2024). System-2 attention (is something you might need too). *arXiv preprint*. https://doi.org/10.48550/arXiv.2311.11829

**Summary:** Applies the Kahneman dual-process framework (System 1 fast/intuitive vs. System 2 slow/deliberate) to LLMs. Proposes "System 2 Attention" — a technique where the model first regenerates the input to remove irrelevant or misleading content, then reasons over the cleaned version. This reduces sycophancy and improves factual accuracy.

**Key Contributions:**
- Demonstrated that standard attention is susceptible to irrelevant context (distractor text, leading questions).
- Proposed a two-pass approach: first pass extracts relevant context, second pass reasons over it.
- Showed reduced sycophancy and improved factual accuracy without fine-tuning.

**Discussion Questions:**
1. How does the two-pass "System 2 Attention" approach relate to the decomposition principle (Module 2 §2.2)? Could you implement a similar technique purely through prompt design?
2. The paper addresses sycophancy specifically. Compare its approach to the fix strategies for Category 14 (Sycophancy) in the [Prompt Debugging Guide](../prompt-debugging.md).
3. Design a two-phase prompt where the first phase summarizes and filters the input, and the second phase reasons over the filtered version. Test it on a task where you know the model is prone to distraction.

**Curriculum Connection:** Module 2 §2.2 (Decomposition); [Prompt Debugging Guide](../prompt-debugging.md), Category 14 (Sycophancy).

---

### Implications for Prompt Engineers

The emergence of reasoning models (OpenAI o1/o3, extended thinking in Claude, Gemini's reasoning mode) has several practical implications:

1. **CoT may become redundant.** Models with built-in reasoning allocate inference-time compute internally. Adding "think step by step" to a reasoning model may produce redundant traces or interfere with the model's own reasoning process. Test both with and without CoT instructions.

2. **Prompt simplicity may outperform complexity.** When the model handles decomposition internally, a clear task description with strong constraints may outperform an elaborate multi-step prompt. The overhead of manual CoT competes with the model's native reasoning.

3. **Evaluation becomes more important, not less.** Reasoning models produce longer outputs with more intermediate steps. Verifying the reasoning chain (not just the final answer) becomes essential — aligning with the process supervision approach from Paper 14.

4. **Cost/latency trade-offs shift.** Reasoning models are slower and more expensive per query. Prompt engineers must decide when to pay for deeper reasoning vs. when a fast, standard model with manual CoT suffices.

These implications do not invalidate the curriculum — the principles of specificity, decomposition, evaluation, and iteration (Module 2) remain foundational. What changes is *how* these principles are applied when the model handles some decomposition and reasoning autonomously.

---

## Reading Checklist

Use this checklist to track your progress through the research track:

- [ ] Paper 1: Brown2020 — Few-Shot Learners
- [ ] Paper 2: Ouyang2022 — InstructGPT / RLHF
- [ ] Paper 3: Wei2022 — Chain-of-Thought
- [ ] Paper 4: Kojima2022 — Zero-Shot Reasoners
- [ ] Paper 5: Wang2023 — Self-Consistency
- [ ] Paper 6: Yao2023 — ReAct
- [ ] Paper 7: Shinn2023 — Reflexion
- [ ] Paper 8: Park2023 — Generative Agents
- [ ] Paper 9: Perez2022 — Red Teaming with LLMs
- [ ] Paper 10: Greshake2023 — Indirect Prompt Injection
- [ ] Paper 11: Lewis2020 — Retrieval-Augmented Generation
- [ ] Paper 12: Zheng2023 — MT-Bench and Chatbot Arena
- [ ] Paper 13: Snell2024 — Test-Time Compute Scaling
- [ ] Paper 14: Lightman2023 — Process Supervision (Let's Verify Step by Step)
- [ ] Paper 15: Saha2024 — System-2 Attention

---

## Additional Resources

For full bibliographic details and DOIs, see [references.md](../../references.md).

---

[← Back to curriculum](../README.md)
