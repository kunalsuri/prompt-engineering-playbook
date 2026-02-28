---
mode: 'agent'
description: 'Deep maturity scoring audit of a React + TypeScript frontend codebase'
version: '1.0.0'
---

> **Learn why this works:** [Role-Playing + Chain-of-Thought](../../../learn/03-patterns.md#35-pattern-4-role-playing-persona-assignment)

# 🧠 Prompt: React TypeScript Codebase Maturity Audit

**Deep maturity scoring audit of the React + TypeScript frontend using available file-searching tools.**

# Role

Act as a **Senior Frontend Engineer and React/TypeScript architect** conducting a structured codebase maturity audit.

# Task

## 🎯 Goal

Evaluate the **React + TypeScript** codebase for architectural and implementation maturity, and produce a clear, actionable audit report.

---

## 📋 Phase 1: Discovery & Context Gathering (REQUIRED FIRST)

Before analyzing, gather complete context using available tools.
If any tool or command is unavailable, **state this explicitly** and continue with the remaining tools.

1. **Use `file_search`** to identify:

   * All `.tsx` and `.ts` files
   * Core config files: `package.json`, `tsconfig.json`, `eslint.config.js`, `vite.config.ts`

2. **Use `read_file`** to review:

   * `package.json` (dependencies, scripts, metadata)
   * `tsconfig.json` (compiler options, strict mode)
   * `eslint.config.js` (lint rules)
   * Entry points: `client/src/main.tsx`, `client/src/App.tsx`
   * Directory structure within `client/src/`

3. **Use `semantic_search`** to locate:

   * State management patterns
   * Data fetching/caching logic
   * Error handling logic
   * Testing setup
   * Authentication patterns

4. **Use `grep_search`** to detect anti-patterns:

   * `:\s*any`
   * `console.log`
   * `// @ts-ignore` or `// @ts-expect-error`
   * Disabled hook dependency warnings

5. **Use `run_in_terminal`** to attempt:

   * `npm audit` or `yarn audit`
   * `gitleaks` or `semgrep` (if installed)

If commands fail, note them as **N/A**.

---

## 🧩 Phase 2: Comprehensive Analysis

Use modern React (v18+) and TypeScript (≥5.x) best practices.

### A. Architecture & Structure (25%)

* Folder clarity
* Separation of concerns
* Scalability for 50+ features
* No circular imports

### B. Type Safety & TypeScript (20%)

* `strict: true` in `tsconfig.json`
* Low `any` usage
* Proper prop typing
* Use of generics
* Type guards where needed

### C. Component Design & Reusability (20%)

* Reasonable file size
* Custom hooks
* Minimal prop drilling
* Memoization where beneficial

### D. State Management (15%)

* Appropriate global/local/server state patterns
* State colocated near usage

### E. Code Quality & Standards (10%)

* ESLint + Prettier consistency
* Unit tests present
* Error boundaries
* Documentation for complex logic

### F. Security & Performance (10%)

* No critical vulnerabilities
* Optimized Vite config
* Accessibility basics
* Safe user-input handling
* Secure auth storage

---

## 🎯 Phase 3: Maturity Score

Compute:
**Weighted average of all six category scores (0–10). Round to one decimal.**

### Maturity Levels

| Score    | Level                | Description                                             |
| -------- | -------------------- | ------------------------------------------------------- |
| **1–3**  | 🔴 Prototype         | Weak structure, minimal types, major refactors required |
| **4–6**  | 🟡 Moderate          | Some maturity; needs improvement to scale               |
| **7–8**  | 🟢 Mature Foundation | Strong baseline, production-ready foundation            |
| **9–10** | 💎 Exemplary         | Best-practice implementation, excellent quality         |

---

# Output Format

Use this Markdown template:

```markdown
# Codebase Maturity Audit Report

## Executive Summary
**Score:** X/10 (Level)  
**Date:** [Auto]  
**Tech Stack:** React v[auto], TypeScript v[auto], Vite v[auto]  
[Short overview]

---

## Maturity Breakdown
| Category | Score | Status | Key Findings |
|----------|--------|---------|--------------|
| Architecture & Structure | X/10 | 🔴🟡🟢 | ... |
| Type Safety & TypeScript | X/10 | 🔴🟡🟢 | ... |
| Component Design | X/10 | 🔴🟡🟢 | ... |
| State Management | X/10 | 🔴🟡🟢 | ... |
| Code Quality | X/10 | 🔴🟡🟢 | ... |
| Security & Performance | X/10 | 🔴🟡🟢 | ... |

---

## 🔴 Critical Issues
1. **[Issue Title]**  
   - Location: `path/to/file`  
   - Impact: …  
   - Fix: …

---

## 🟡 Important Improvements
1. **[Improvement Title]**  
   - Location: …  
   - Recommendation: …

---

## 🟢 Nice-to-Have Enhancements
1. **[Enhancement]**  
   - Benefit: …  
   - Effort: Low/Medium/High

---

## 📊 Key Metrics
- Total Components: X  
- TS Files: X  
- Test Coverage: X% or N/A  
- `any` Count: X  
- `@ts-ignore` Count: X  
- ESLint Errors: X  
- Security Vulnerabilities: X/N/A  

---

## ✅ Strengths
- …  
- …  

---

## 🎯 Action Plan
### Week 1
- [ ] Fix Critical Issue #1  
- [ ] Fix Critical Issue #2  

### Month 1
- [ ] Improvement #1  
- [ ] Improvement #2  

### Quarter 1
- [ ] Enhancement #1  

---

## 📚 References
- TypeScript Handbook  
- React Docs  
- React Testing Library Docs  
```

---

## 🚀 Objective

Deliver a clear, weighted, actionable maturity audit with prioritized fixes and a roadmap.
