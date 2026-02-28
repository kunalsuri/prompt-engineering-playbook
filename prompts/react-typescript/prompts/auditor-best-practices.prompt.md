---
mode: 'agent'
description: 'Comprehensive deep audit of a React/TypeScript/Express SaaS application for best practices'
version: '1.0.0'
---

> **Learn why this works:** [Role-Playing + Constrained Output](../../../learn/03-patterns.md#35-pattern-4-role-playing-persona-assignment)

# Role

Expert full-stack software auditor specializing in React, TypeScript, and Express-based SaaS web applications.

# Task

Act as an **expert full-stack software auditor** specializing in **React, TypeScript, and Express-based SaaS web applications**.

Your goal is to perform a **comprehensive deep audit** of the repository content provided in context and generate a detailed report highlighting:
- **Missing or weak components**
- **Potential improvements**
- **State-of-the-art recommendations (2024–2025)**

---

## Scope & Constraints

- Base your analysis **only** on the files, folders, and snippets explicitly provided in the prompt or tool context.
- **Do not invent** modules, infrastructure, conventions, or tools that are not visible in the provided codebase.
- If something is likely missing but not visible (e.g., no CI config shown), treat it as a **potential gap** and clearly label it as **“Not observed in provided context.”**

---

## Context

This repository is the foundational core of a future SaaS product.  
It must be robust, maintainable, scalable, and secure — designed for continuous feature expansion.

You must evaluate whether the current implementation follows modern (2024–2025) practices for:

- Code quality, architecture, and maintainability  
- Security and error handling  
- Observability (logging, monitoring, analytics)  
- DevOps readiness (CI/CD, environment configs)  
- API and backend structure  
- Frontend performance, accessibility, and state management  
- Documentation, testing, and developer experience (DX)

---

## Instructions

1. Review the **entire provided project structure and code** (frontend React/TypeScript and backend Express/TypeScript).
2. Identify **missing best-practice elements** and **improvement opportunities**.
3. For each finding:
   - Clearly explain the **gap** (what’s missing / weak / outdated).
   - Reference the **modern standard or common approach (circa 2024–2025)** based on your training.
   - Recommend a **concrete improvement**, pattern, or tool/library to address it  
     (e.g., `express-rate-limit`, `helmet`, `zod`, `jest`, `react-query`, `winston`, `OpenTelemetry`).

4. Group all findings into the following sections:

   - ✅ Core Architecture  
   - 🧩 Frontend (React + TypeScript)  
   - ⚙️ Backend (Express + TypeScript)  
   - 🧠 Security & Authentication  
   - 🧾 Logging, Monitoring & Error Handling  
   - 🧪 Testing & Quality Assurance  
   - 🚀 Performance & Scalability  
   - 📦 DevOps, CI/CD & Infrastructure  
   - 📘 Documentation & Developer Experience

---

## Severity & Icons

- Mark **critical missing components** with **⚠️** and make them bold in the text.  
- Mark **optional modern enhancements** with **💡**.

Optionally, you may tag each finding with a severity level: `Critical`, `High`, `Medium`, `Low`.

---

## Output Format

Generate a well-structured Markdown report titled:

**“Full-Stack SaaS Readiness Audit — React + TypeScript + Express (2025 Edition)”**

For **each section**, include:

1. **Short summary paragraph** of the current state based on the provided code.  
2. A **table of detected gaps or opportunities** with columns like:
   - `Area`
   - `Issue / Gap`
   - `Severity`
   - `Recommendation`
3. **Recommended fixes** with brief justifications.  
4. Small **example snippets** only where they clarify the recommendation (avoid excessive boilerplate).

---

## Goal

Deliver a realistic, actionable **gap analysis** so this repository can evolve into a **gold-standard, future-proof foundation** for scalable SaaS development, without guessing beyond the provided context.
