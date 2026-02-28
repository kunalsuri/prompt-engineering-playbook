# Getting Started

This guide walks you through the process of selecting, customizing, and using the prompt templates in this repository with VS Code and GitHub Copilot. By the end, you will have a working prompt configuration integrated into your own project.

---

## Prerequisites

Before you begin, ensure you have the following:

- **VS Code** (version 1.96 or later) with the **GitHub Copilot** extension installed and activated with a Copilot Pro, Business, or Enterprise subscription.
- **Git** installed and configured on your system.
- A target project where you want to use the prompt templates. This can be an existing repository or a new one.

---

## Step 1: Understand the Prompt-File Mechanism

VS Code's GitHub Copilot recognizes special Markdown files in your repository that provide custom instructions and prompt templates. There are two mechanisms:

**Custom instructions** are Markdown files (typically named `copilot-instructions.md`) placed in your project's `.github/` directory. Copilot reads these files automatically and applies their content as persistent behavioral guidelines in every interaction. Think of them as a system prompt for your project — they define code style, tooling preferences, documentation standards, and architectural conventions.

**Prompt files** are Markdown files with the `.prompt.md` extension, typically stored in `.github/prompts/`. Each prompt file defines a reusable task — such as "generate a React component," "perform a security audit," or "create a FastAPI endpoint." Prompt files support YAML frontmatter with metadata fields:

```yaml
---
mode: 'agent'           # Enables agent mode: Copilot can read files,
                         # run commands, and take multi-step actions.
description: 'Create a new React component with tests and Storybook story'
---
```

When `mode` is set to `'agent'`, Copilot operates as an autonomous agent that can read your project files, execute terminal commands, and iterate on its output — enabling complex, multi-step workflows defined by the prompt.

---

## Step 2: Choose Your Technology Stack

This repository provides templates for four technology stacks. Select the one that matches your project:

**Python** — If your project is a Python application (CLI tool, data pipeline, ML service, API server using Django/Flask). Use templates from `prompts/python/`.

**React + TypeScript** — If your project is a frontend application built with React and TypeScript. Use templates from `prompts/react-typescript/`.

**React + Python FastAPI (Full-Stack)** — If your project combines a React/TypeScript frontend with a FastAPI backend. Use templates from `prompts/react-fastapi/`.

**Node.js + TypeScript** — If your project is a Node.js backend or full-stack application using TypeScript. Use templates from `prompts/nodejs-typescript/`.

Each stack directory contains a `copilot-instructions.md` (base instructions) and a `prompts/` subdirectory (task-specific prompts).

---

## Step 3: Copy Templates into Your Project

### Option A: Use as a GitHub Template Repository

Click the **"Use this template"** button on the GitHub repository page. This creates a new repository with all template files included. You can then remove the files for stacks you don't need.

### Option B: Cherry-Pick Files for Your Stack

If you have an existing project, copy only the files you need. The following example demonstrates the process for a Python project. Adapt the paths for other stacks.

```bash
# Navigate to your project root
cd /path/to/your-project

# Create the .github directory structure
mkdir -p .github/prompts

# Download the base instructions
curl -o .github/copilot-instructions.md \
  https://raw.githubusercontent.com/kunalsuri/prompt-engineering-playbook/main/prompts/python/copilot-instructions.md

# Download all prompt files for the Python stack
for prompt in $(curl -s https://api.github.com/repos/kunalsuri/prompt-engineering-playbook/contents/prompts/python/prompts | grep '"name"' | cut -d'"' -f4); do
  curl -o ".github/prompts/${prompt}" \
    "https://raw.githubusercontent.com/kunalsuri/prompt-engineering-playbook/main/prompts/python/prompts/${prompt}"
done

# Download the shared Codacy instructions
mkdir -p .github/instructions
curl -o .github/instructions/codacy.instructions.md \
  https://raw.githubusercontent.com/kunalsuri/prompt-engineering-playbook/main/prompts/shared/codacy.instructions.md
```

After downloading, verify that the directory structure matches:

```
your-project/
├── .github/
│   ├── copilot-instructions.md          # Base instructions for your stack
│   ├── instructions/
│   │   └── codacy.instructions.md       # Shared code-quality instructions
│   └── prompts/
│       ├── create-feature.prompt.md     # Task: generate a new feature
│       ├── review-code.prompt.md        # Task: review code for issues
│       ├── write-tests.prompt.md        # Task: generate unit tests
│       └── ...                          # Additional task prompts
├── src/
├── tests/
└── ...
```

---

## Step 4: Customize the Base Instructions

Open `.github/copilot-instructions.md` in your editor. This file contains general-purpose standards for the technology stack. You should customize it to reflect your project's specific conventions:

**Project-specific tooling.** If you use `poetry` instead of `pip`, or `pnpm` instead of `npm`, update the package-management instructions accordingly.

**Internal conventions.** Add your team's naming conventions, import ordering rules, directory structure standards, or any project-specific patterns that all generated code should follow.

**Excluded patterns.** If there are patterns or libraries the model should never suggest (e.g., deprecated internal APIs, banned dependencies), add explicit negative instructions: "Never use library X; use library Y instead."

Save your changes. Copilot will automatically pick up the updated instructions in your next interaction.

---

## Step 5: Use a Prompt File

Open VS Code's Copilot Chat panel (Ctrl+Shift+I / Cmd+Shift+I). You can invoke a prompt file in two ways:

**From the chat input**, type `/` followed by the prompt file name (without the `.prompt.md` extension). VS Code will autocomplete available prompts from your `.github/prompts/` directory.

**From the Command Palette**, open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P), type "Copilot: Run Prompt," and select the desired prompt file from the list.

When a prompt file has `mode: 'agent'`, Copilot will operate autonomously — reading files, generating code, creating new files, and running terminal commands as specified by the prompt. You will see each action in the chat panel and can approve, modify, or reject individual steps.

---

## Step 6: End-to-End Example

Let's walk through a concrete example: using the Python stack templates to generate a new API endpoint.

1. **Ensure base instructions are in place** at `.github/copilot-instructions.md`. These tell Copilot to use Python 3.12+, type annotations, Google-style docstrings, `ruff` for linting, and `pytest` for testing.

2. **Open Copilot Chat** and invoke the code-generation prompt: type `/create-feature` (or the equivalent prompt name in your setup).

3. **Describe your requirement** in the chat: "Create a `GET /users/{user_id}/activity` endpoint that returns the last 30 days of user activity, paginated with cursor-based pagination. Use the existing `UserActivity` Pydantic model from `src/models/activity.py`."

4. **Review Copilot's plan.** In agent mode, Copilot will first read the relevant files (`src/models/activity.py`, existing route files), then propose a plan. Review the plan before approving execution.

5. **Approve file creation.** Copilot will generate the route handler, update route registration, create corresponding tests in `tests/`, and run `ruff` and `mypy` to verify compliance. Each step appears in the chat for your review.

6. **Iterate.** If the generated code needs adjustments, describe the changes in the chat. Copilot retains the full context of the prompt and its previous output.

---

## Step 7: Learning Prompt Engineering

If you are new to prompt engineering or want to deepen your understanding of the principles behind these templates, the `learn/` directory provides a seven-module curriculum:

| Module | File | Topic |
|--------|------|-------|
| 0 | `00-orientation.md` | Story-first on-ramp — no jargon, no code |
| 1 | `01-introduction.md` | What prompt engineering is and why it matters |
| 2 | `02-core-principles.md` | Specificity, decomposition, iteration, evaluation |
| 3 | `03-patterns.md` | Six major prompting patterns with worked examples |
| 4 | `04-best-practices.md` | Token management, version control, team workflows |
| 5 | `05-advanced-patterns.md` | RAG, adversarial robustness, multimodal, evaluation pipelines |
| 6 | `06-agentic-patterns.md` | Plan-and-execute, reflection loops, multi-agent systems, agent safety |

Each module includes exercises. The `comparisons/` subdirectory provides deep-dive analyses of specific techniques referenced from the modules.

---

## Troubleshooting

**Copilot does not seem to follow the instructions in `copilot-instructions.md`.** Ensure the file is located at exactly `.github/copilot-instructions.md` (not a subdirectory or another location). VS Code only recognizes the `.github/` directory in the workspace root.

**Prompt files do not appear in the `/` autocomplete.** Verify that prompt files have the `.prompt.md` extension and are located in `.github/prompts/`. Restart VS Code if you added files while the editor was open.

**Agent mode is not available.** Agent mode requires GitHub Copilot version 0.24+ and an eligible subscription tier. Check for extension updates and verify your subscription in GitHub Settings → Copilot.

**Generated code does not match the style guide.** The base instructions and the prompt interact: if the prompt specifies conventions that conflict with the base instructions, the prompt typically takes precedence. Review both files for contradictions.

---

## Next Steps

Once you are comfortable with the templates, consider contributing improvements. See `CONTRIBUTING.md` for guidelines on submitting changes, including the Conventional Commits format and the prompt review checklist.
