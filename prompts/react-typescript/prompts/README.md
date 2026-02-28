# React + TypeScript Prompt Files

Task-specific prompt files for React + TypeScript development with VS Code & GitHub Copilot.

| Prompt File | What It Does |
|------------|-------------|
| `create-saas-app-V2.prompt.md` | Scaffold a complete feature-based SaaS application |
| `auditor-best-practices.prompt.md` | Audit codebase against industry best practices |
| `auditor-codebase-maturity.prompt.md` | Assess codebase maturity across multiple dimensions |
| `auditor-cybersecurity-features.prompt.md` | Multi-perspective security audit (OWASP/MITRE/NIST/SLSA) |
| `safety-gate-llm.prompt.md` | LLM output validation with JSON-schema confidence scoring |
| `auto-code-implementation.prompt.md` | Autonomous code implementation agent |
| `create-chatbot-ollama.prompt.md` | Build an Ollama-powered chatbot feature |
| `update-generate-readme.prompt.md` | Analyze a project and generate or update its README |

## Usage

Copy the `.prompt.md` files you need into your project's `.github/prompts/` directory. Each file becomes available as a slash command in Copilot Chat (e.g., `/create-saas-app-V2`).

All prompts expect `mode: 'agent'` — Copilot will read your project files, generate code, and run commands autonomously. See [`copilot-instructions.md`](../copilot-instructions.md) for the base React + TypeScript standards that Copilot applies alongside these prompts.
