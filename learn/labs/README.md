# Prompt Engineering Labs

> **Runnable experiments** that demonstrate curriculum concepts with real LLM API calls. Each lab is a self-contained Python script — or run them **free in Google Colab** with zero local setup.

---

## 🚀 Run Free in Google Colab (Recommended)

Click any badge below to open the lab directly in your browser — no installation required:

| Lab | Colab Link |
| --- | --- |
| Lab 1 — Zero-Shot vs. Few-Shot | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kunalsuri/prompt-engineering-playbook/blob/main/learn/labs/lab_01_zero_vs_few_shot.ipynb) |
| Lab 2 — Chain-of-Thought Impact | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kunalsuri/prompt-engineering-playbook/blob/main/learn/labs/lab_02_chain_of_thought.ipynb) |
| Lab 3 — Specificity Experiment | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kunalsuri/prompt-engineering-playbook/blob/main/learn/labs/lab_03_specificity.ipynb) |
| Lab 4 — Evaluation Pipeline | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kunalsuri/prompt-engineering-playbook/blob/main/learn/labs/lab_04_evaluation_pipeline.ipynb) |
| Lab 5 — Tool-Calling & Structured Output | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kunalsuri/prompt-engineering-playbook/blob/main/learn/labs/lab_05_tool_calling.ipynb) |
| Lab 6 — Agentic Plan-and-Execute | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kunalsuri/prompt-engineering-playbook/blob/main/learn/labs/lab_06_agentic_plan_execute.ipynb) |

### Free LLM Providers

The Colab notebooks let you choose a provider at runtime. **No credit card required** for the free options:

| Provider | Free Tier | How to Get a Key |
| --- | --- | --- |
| **Google Gemini** ⭐ | 15 RPM, 1 M tokens/day | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| **Groq** | 30 RPM, 14.4 K tokens/min | [console.groq.com](https://console.groq.com) |
| **OpenAI** (paid) | Pay-per-token | [platform.openai.com](https://platform.openai.com/api-keys) |

---

## Run Locally

### Prerequisites

- Python 3.10+
- An API key for at least one provider (see table above)

### Setup

```bash
cd learn/labs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key(s)
```

---

## Available Labs

| Lab | Module Link | What You'll Learn | Time |
| --- | --- | --- | --- |
| [Lab 1 — Zero-Shot vs. Few-Shot](lab_01_zero_vs_few_shot.py) | [Module 3, §3.2–§3.3](../03-patterns.md) | Quantify the difference between zero-shot and few-shot on a classification task | 10 min |
| [Lab 2 — Chain-of-Thought Impact](lab_02_chain_of_thought.py) | [Module 3, §3.4](../03-patterns.md#34-pattern-3-chain-of-thought-cot) | Measure CoT's improvement on arithmetic reasoning (direct vs. step-by-step) | 10 min |
| [Lab 3 — Specificity Experiment](lab_03_specificity.py) | [Module 2, §2.1](../02-core-principles.md#21-principle-1-specificity) | Compare outputs from vague vs. specific prompts across multiple runs | 10 min |
| [Lab 4 — Evaluation Pipeline](lab_04_evaluation_pipeline.py) | [Module 5, §5.4](../05-advanced-patterns.md#54-systematic-evaluation-methodology) | Build a mini evaluation pipeline with test suite, metrics, and LLM-as-Judge | 15 min |
| [Lab 5 — Tool-Calling & Structured Output](lab_05_tool_calling.py) | [Module 3, §3.6](../03-patterns.md) · [Module 5, §5.4](../05-advanced-patterns.md) | Compare JSON-mode prompting vs. function-calling API — measure valid-JSON rate and field completeness | 15 min |
| [Lab 6 — Agentic Plan-and-Execute](lab_06_agentic_plan_execute.py) | [Module 6, §6.2](../06-agentic-patterns.md) | Build a plan-and-execute agent in pure Python; compare to single-prompt baseline | 20 min |

---

## How Labs Work

Each lab script:
1. Defines two or more prompt variants (naive vs. pattern-applied)
2. Sends each variant to the configured LLM API multiple times
3. Collects and scores the outputs
4. Prints a comparison table showing the difference

The labs auto-detect your provider: Google Gemini → Groq → OpenAI (first available key wins). Override with `LLM_MODEL` and `OPENAI_API_BASE` in your `.env`.

---

## Failure Gallery

Interactive exercises where you **diagnose broken prompts** before reading the solution.

| Case | Anti-Pattern | Core Lesson |
| --- | --- | --- |
| [01 — Kitchen Sink](failure-gallery/01-kitchen-sink/) | Doing too much in one prompt | Task decomposition |
| [02 — Stale Context](failure-gallery/02-stale-context/) | Relying on out-of-date model knowledge | Grounding / RAG |
| [03 — Injection Vulnerable](failure-gallery/03-injection-vulnerable/) | Secrets in system prompt, no override defense | Security & input sanitisation |
| [04 — Ambiguous Format](failure-gallery/04-ambiguous-format/) | No output schema for structured data | Constrained output (Lab 5) |
| [05 — Missing Constraints](failure-gallery/05-missing-constraints/) | All 4 of 5 prompt components absent | Prompt anatomy (Module 1) |

See [failure-gallery/README.md](failure-gallery/README.md) for the scoring rubric.

---

## Output Disclaimer

LLM outputs are non-deterministic. Your results will differ from run to run and from model to model. The purpose of these labs is to observe *relative* differences between prompt strategies, not to reproduce exact numbers.

---

[← Back to curriculum](../README.md)
