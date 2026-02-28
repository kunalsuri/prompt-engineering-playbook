# React + FastAPI Prompt Files

Task-specific prompt files for full-stack React + FastAPI development with VS Code & GitHub Copilot.

| Prompt File | What It Does |
|------------|-------------|
| `create-app-react-fastapi.prompt.md` | Scaffold a complete full-stack application (React frontend + FastAPI backend) |
| `create-test-suite.prompt.md` | Generate a comprehensive test suite spanning frontend and backend |
| `update-generate-readme.prompt.md` | Analyze a project and generate or update its README |

## Usage

Copy the `.prompt.md` files you need into your project's `.github/prompts/` directory. Each file becomes available as a slash command in Copilot Chat (e.g., `/create-app-react-fastapi`).

All prompts expect `mode: 'agent'` — Copilot will read your project files, generate code, and run commands autonomously. See [`copilot-instructions.md`](../copilot-instructions.md) for the base React + FastAPI standards that Copilot applies alongside these prompts.
