# Node.js & TypeScript Prompt Templates

Production-ready prompts for Node.js + TypeScript development. Use with GitHub Copilot's agent mode in VS Code.

## Prerequisites

1. Copy `copilot-instructions.md` to your project as `.github/copilot-instructions.md`.
2. Open the target `.ts` or `.js` file you want Copilot to work on.
3. Run any prompt using **Copilot Chat → Agent mode** (`@workspace`).

## Available Prompts

| Prompt | Purpose | Key Patterns |
|---|---|---|
| [create-api-endpoint](create-api-endpoint.prompt.md) | Scaffold a typed REST endpoint with validation | Decomposition + Role-Playing |
| [review-code](review-code.prompt.md) | Review TypeScript code for safety, style, and correctness | Role-Playing + Constrained Output |
| [write-tests](write-tests.prompt.md) | Generate `vitest`/`jest` tests for a module | Few-Shot + Constrained Output |
| [generate-openapi-spec](generate-openapi-spec.prompt.md) | Generate OpenAPI 3.1 YAML from TypeScript types | Constrained Output + Specificity |

## Usage Example

```
# In Copilot Chat (Agent mode):
@workspace #file:src/routes/users.ts
Use the create-api-endpoint prompt to add a PATCH /users/:id endpoint.
```

## Stack Assumptions

- **Runtime:** Node.js 20 LTS+
- **Language:** TypeScript 5.x with `strict: true`
- **Validation:** `zod`
- **Testing:** `vitest`
- **API framework:** Express, Fastify, or Hono (prompts are framework-agnostic where possible)

---

[← Back to Prompts index](../../README.md) · [Learn the patterns →](../../../learn/03-patterns.md)
