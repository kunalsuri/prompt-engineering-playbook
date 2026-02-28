# Python Prompt Files

Task-specific prompt files for Python development with VS Code & GitHub Copilot.

| Prompt File | What It Does |
|------------|-------------|
| `create-feature.prompt.md` | Generate a new feature module with types, docs, and tests |
| `review-code.prompt.md` | Five-dimension code review (correctness, types, style, edge cases, docs) |
| `write-tests.prompt.md` | Generate a pytest test suite with coverage targets |
| `debug-issue.prompt.md` | Six-step diagnostic process to find and fix bugs |
| `refactor-code.prompt.md` | Refactor code for readability, complexity, and idiomatic style |
| `generate-docs.prompt.md` | Generate Google-style docstrings and API reference docs |
| `update-generate-readme.prompt.md` | Analyze a project and generate or update its README |

## Usage

Copy the `.prompt.md` files you need into your project's `.github/prompts/` directory. Each file becomes available as a slash command in Copilot Chat (e.g., `/create-feature`).

All prompts expect `mode: 'agent'` — Copilot will read your project files, generate code, and run commands autonomously. See [`copilot-instructions.md`](../copilot-instructions.md) for the base Python standards that Copilot applies alongside these prompts.