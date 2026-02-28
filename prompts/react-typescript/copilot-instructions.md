# **General + React + TypeScript Ruleset (Final Version)**

## **Meta Rule**

* All rules below override model defaults and apply to **every code generation task**.
* Follow **Feature-Driven Modular Architecture** with the structure:

  ```
  src/
    features/
    components/
    hooks/
    lib/
    types/
  ```
  
* Before adding new code, **audit, refactor, and correct** existing issues.
* No speculative or non-functional code. Output must be **compilable**.
* Code must be modular, readable, maintainable, and minimal.

---

## **Code Style**

* Use **functional components** with hooks only.
* No classes, no side effects inside render.
* Extract reusable logic into custom hooks or utilities.
* Keep components **small and single-responsibility**.

---

## **Naming**

* Directories: `lowercase-dash` (e.g., `auth-wizard`).
* Hooks: `use*` naming.
* Variables: descriptive (`isLoading`, `hasError`).
* Prefer **named exports** everywhere except top-level pages.

---

## **TypeScript**

* Must run in **strict mode**.
* Prefer `interface` for objects.
* Avoid `any`; allowed only with a justification comment.
* Prefer union types or string enums; avoid numeric enums.

---

## **Syntax**

* Use `function` keyword for pure functions.
* Arrow functions for callbacks and inline handlers.
* Always use braces `{}` for conditionals.
* JSX must remain declarative and clean.

---

## **Formatting & Linting**

* Enforce **Prettier** for formatting.
* Use **ESLint** with React + TypeScript recommended rules.
* All output must pass linting (imports included).

---

## **Styling**

* Default styling: **Tailwind CSS**.
* Use responsive layouts: Flexbox, Grid, container queries.
* Dark mode via CSS variables or `next-themes`.
* Avoid inline styles except for dynamic values.

---

## **Accessibility**

* Use semantic HTML.
* Add ARIA attributes only when necessary.
* Ensure keyboard navigation and focus management.
* Follow Lighthouse or axe accessibility standards.

---

## **Animations**

* Use **Framer Motion** (default).
* Keep animations minimal and performance-safe.

---

## **Error Handling**

* Wrap async logic in `try/catch`.
* Provide user-friendly error states.
* Use an Error Boundary placed in:

  ```
  src/components/common/ErrorBoundary.tsx
  ```

---

## **Testing**

* Use **Jest + React Testing Library**.
* Write tests only when requested or when generating core logic.

---

## **Output Expectations (for AI Agent)**

* Output complete files with filename headers, e.g.:

  ```ts
  // src/components/Button.tsx
  ```
* Include imports, types, and comments for complex logic.
* Ensure final code compiles without errors.
* After code, include a short **integration checklist**.

---
