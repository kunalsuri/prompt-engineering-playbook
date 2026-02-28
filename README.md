# Prompt Engineering Playbook

> Production-ready prompts for AI-assisted development with VS Code & GitHub Copilot, plus a hands-on curriculum to learn prompt engineering from scratch.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<br> 

---

## Pick Your Path

### 🎓 [I want to **learn** prompt engineering →](learn/)

A seven-module curriculum that takes you from first principles through advanced techniques like RAG, adversarial robustness, systematic evaluation, and agentic architectures. Each module includes worked examples and hands-on exercises. No prior prompt engineering experience required.

### ⚡ [I want to **use** prompt templates →](prompts/)

Copy-paste-ready prompt files for Python, React/TypeScript, React + FastAPI, and Node.js/TypeScript projects. Designed for VS Code Copilot's agent mode. Pick your stack, grab the files, and start building.

### 📚 [I want **20 copy-paste recipes** for everyday tasks →](learn/cookbook.md)

Ready-to-use prompts for writing, research, analysis, communication, and decision-making — no programming required. Each recipe is tagged with the prompting patterns it uses.

### 🔧 [I want to **set up** my project →](GETTING-STARTED.md)

Step-by-step guide to installing these templates in your own project, understanding the VS Code Copilot prompt-file mechanism, and customizing templates for your team.

<br> 

---

## Quick Start (60 seconds)

**Option A — Use as a GitHub template:**
Click **"Use this template"** at the top of this page to create your own copy with all files included.

**Option B — Grab files for one stack:**

```bash
# Example: set up Python prompts in your project
mkdir -p .github/prompts

# Base instructions (Copilot reads this automatically)
curl -o .github/copilot-instructions.md \
  https://raw.githubusercontent.com/kunalsuri/prompt-engineering-playbook/main/prompts/python/copilot-instructions.md

# All Python prompt files
curl -o .github/prompts/create-feature.prompt.md \
  https://raw.githubusercontent.com/kunalsuri/prompt-engineering-playbook/main/prompts/python/prompts/create-feature.prompt.md

# Repeat for each prompt file you need, or clone and copy:
git clone https://github.com/kunalsuri/prompt-engineering-playbook.git
cp -r prompt-engineering-playbook/prompts/python/prompts/*.prompt.md .github/prompts/
```

<br> 

---

## What's Inside

```
├── learn/                     🎓 Seven-module curriculum + deep-dive comparisons
│   ├── 00-orientation.md               Story-first on-ramp (no technical background needed)
│   ├── 01-introduction.md
│   ├── 02-core-principles.md
│   ├── 03-patterns.md
│   ├── 04-best-practices.md
│   ├── 05-advanced-patterns.md
│   ├── 06-agentic-patterns.md          Plan-and-execute, reflection loops, multi-agent systems
│   ├── comparisons/                    Chain-of-Thought, ReAct, Few-Shot, cross-model portability
│   └── prompt-examples/                Worked examples for each pattern
│
├── prompts/                   ⚡ Production prompt templates
│   ├── shared/                Instructions that apply to ALL stacks
│   ├── python/                Python-specific prompts & instructions
│   ├── react-typescript/      React + TypeScript prompts & instructions
│   ├── react-fastapi/         Full-stack React + FastAPI prompts
│   └── nodejs-typescript/     Node.js + TypeScript prompts & instructions
│
├── scripts/                   🔧 Setup helper scripts
│   ├── python/setup.sh
│   ├── react-typescript/setup.sh
│   ├── react-fastapi/setup.sh
│   └── nodejs-typescript/setup.sh
│
├── GETTING-STARTED.md         How to install and use these templates
├── CONTRIBUTING.md            Guidelines for contributors
├── CHANGELOG.md               Version history and migration guide
└── references.md              Bibliography (APA, with DOIs)
```

---

<br> 


## Available Stacks

| Stack | Instructions | Prompts | Setup Script |
|-------|-------------|---------|-------------|
| **Python** | [copilot-instructions.md](prompts/python/copilot-instructions.md) | [7 prompts](prompts/python/prompts/) | [setup.sh](https://github.com/kunalsuri/prompt-engineering-playbook/blob/main/scripts/python/setup.sh) |
| **React + TypeScript** | [copilot-instructions.md](prompts/react-typescript/copilot-instructions.md) | [8 prompts](prompts/react-typescript/prompts/) | [setup.sh](https://github.com/kunalsuri/prompt-engineering-playbook/blob/main/scripts/react-typescript/setup.sh) |
| **React + FastAPI** | [copilot-instructions.md](prompts/react-fastapi/copilot-instructions.md) | [3 prompts](prompts/react-fastapi/prompts/) | [setup.sh](https://github.com/kunalsuri/prompt-engineering-playbook/blob/main/scripts/react-fastapi/setup.sh) |
| **Node.js + TypeScript** | [copilot-instructions.md](prompts/nodejs-typescript/copilot-instructions.md) | [4 prompts](prompts/nodejs-typescript/prompts/) | [setup.sh](https://github.com/kunalsuri/prompt-engineering-playbook/blob/main/scripts/nodejs-typescript/setup.sh) |

Each stack includes a `copilot-instructions.md` (base rules Copilot follows automatically) and task-specific `.prompt.md` files (invoked on demand via Copilot Chat).

---

<br> 

## How Copilot Prompt Files Work

When you place files in your project's `.github/` directory, VS Code Copilot picks them up automatically:

```
your-project/
├── .github/
│   ├── copilot-instructions.md    ← Always active (style, conventions, tooling)
│   └── prompts/
│       ├── create-feature.prompt.md   ← Invoke with /create-feature in Copilot Chat
│       ├── review-code.prompt.md      ← Invoke with /review-code
│       └── ...
```

The YAML frontmatter `mode: 'agent'` enables Copilot to read files, run commands, and iterate autonomously. See [GETTING-STARTED.md](GETTING-STARTED.md) for the full walkthrough.

---

<br> 

## Contributing

Contributions are welcome — whether it's fixing a typo, adding an exercise, or creating prompts for a new stack. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, commit conventions, and review checklists.

<br> 

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

<br> 

## ✍️ How to Cite

If you use this framework to structure your research, paper framing, or methodology curriculum, please cite it using the following format:

<br> 

**APA Format:**
> Suri, K. (2026). *Prompt Engineering Playbook*. GitHub. https://github.com/kunalsuri/prompt-engineering-playbook

<br> 

**BibTeX:**
```bibtex
@misc{ks_pe_playbook_2026,
  author       = {Kunal Suri},
  title        = {Prompt Engineering Playbook},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/kunalsuri/prompt-engineering-playbook}
}
```

<br> 

## 💡 Declaration of AI Usage

* **Coding:** GitHub Copilot / Microsoft GitHub Pro and related LLM-assisted features within Visual Studio Code were used to support the coding of this project, primarily for code generation, completion, and debugging. All AI-generated code was independently reviewed, tested, and refined by the author(s). The author(s) takes full responsibility for the correctness and integrity of all code in this work.

* **Writing & Ideation:**  Large language model (LLM) tools — specifically (Anthropic Claude and Google Gemini Pro) — were used to assist with brainstorming, structural organization, and language refinement during the writing process. All underlying arguments, intellectual contributions, and conclusions originate with the author(s). All AI-assisted material was critically reviewed and substantially revised by the author(s), who takes full responsibility for the accuracy, originality, and integrity of the published content.

<br/>

<br/>

<div align="center">

**⭐ If you find this work interesting, please consider starring the repository.**

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>