```instructions
# Node.js & TypeScript Development Standards

**Target Runtime: Node.js 20 LTS+  |  TypeScript 5.x**

## 1. Language and Type Safety

- **Strict mode**: `"strict": true` in `tsconfig.json`. No exceptions.
- **Type annotations**: Required on all function parameters and return types. Avoid `any`; use `unknown` + type guards where the type is genuinely unknown.
- **Modern TypeScript**: Use `satisfies`, `const` type parameters (TS 5.0+), and template literal types where they add precision.
- **Imports**: Use ES module syntax (`import`/`export`). Enable `"module": "NodeNext"` and `"moduleResolution": "NodeNext"`.
- **No enum**: Prefer `const` objects with `as const` or union types over TypeScript `enum`.

## 2. Code Style & Quality

- **Formatter**: `Prettier` with default settings (or project `.prettierrc`).
- **Linter**: `ESLint` with `@typescript-eslint` plugin. Enable `@typescript-eslint/recommended-type-checked`.
- **Naming**: `camelCase` for variables/functions, `PascalCase` for types/interfaces/classes, `SCREAMING_SNAKE_CASE` for module-level constants.
- **Functions**: Prefer named functions for top-level exports (easier stack traces). Arrow functions for callbacks and short lambdas.
- **Error handling**: Custom error classes extending `Error`. Always include `cause` when re-throwing. Never swallow errors silently.

## 3. Async Patterns

- Use `async`/`await` exclusively. No raw `.then()` chains in new code.
- Use `Promise.all` / `Promise.allSettled` for concurrent independent async calls.
- Validate all external inputs (HTTP requests, env vars) with `zod` before use.

## 4. API Development (Express / Fastify / Hono)

- Route handlers must be typed: input via `zod` schema, output via declared response type.
- Separate concerns: router → controller (thin) → service (business logic) → repository (data access).
- HTTP status codes: use named constants from `http-status-codes`.
- Always return consistent error envelopes: `{ error: { code, message, details? } }`.

## 5. Testing

- **Framework**: `vitest` (preferred for ESM compatibility) or `jest` with `ts-jest`.
- **Structure**: Co-locate tests (`*.test.ts`) or use a `__tests__/` sibling directory.
- **Mocking**: Use `vi.mock` / `jest.mock`. Avoid testing implementation details; test behaviour.
- **Coverage**: Aim for ≥80% branch coverage on service and utility layers.

## 6. Project Standards

- **Config**: Use environment variables validated via `zod` at startup (`src/config.ts`). No hardcoded secrets.
- **Package manager**: `npm` with lockfile committed (`package-lock.json`). Pin exact versions in `dependencies`; allow patch ranges in `devDependencies`.
- **Scripts**: `package.json` scripts are the entry points: `build`, `dev`, `test`, `lint`, `typecheck`.

## 7. Anti-Patterns to Avoid

- `require()` in TypeScript (use `import`).
- `@ts-ignore` without an explanatory comment.
- Nested callbacks / callback hell.
- Storing secrets in source code or `.env` files committed to git.
- Unhandled promise rejections (use `process.on('unhandledRejection', ...)` as a last resort, but prefer proper `try/catch`).

## 8. Enforcement

Configure tooling via root-level config files:

- **`tsconfig.json`**: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`
- **`eslint.config.js`**: `@typescript-eslint/recommended-type-checked` ruleset
- **`vitest.config.ts`**: coverage provider `v8`, threshold 80%
- **`.pre-commit-config.yaml`** (optional): run `eslint`, `prettier --check`, `tsc --noEmit` on staged files
```
