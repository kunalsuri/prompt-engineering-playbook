# Module 4 — Best Practices for Production Prompts

## Learning Objectives

By the end of this module, you will be able to manage token budgets and context windows effectively, apply version-control principles to prompt development, implement prompt workflows suitable for team environments, and avoid common anti-patterns that degrade prompt reliability.

!!! note "For Software Engineers"
    This module applies engineering discipline to prompts as first-class artefacts:

    - **Token management** → Think of the context window as a fixed-size buffer; overflowing it silently degrades output quality.
    - **Prompt versioning** → `git blame` for prompts: every change tagged with the model version and eval result that motivated it.
    - **Anti-patterns** → The PE equivalents of code smells: vague specs, missing output contracts, no regression tests.
    - **CI/CD integration** → Prompts with failing evals block the build, exactly like failing unit tests.

    If your team already uses GitOps or Infrastructure-as-Code, prompt versioning will feel natural — the workflow is identical.

---

## 4.1 Token Budget Management

Every LLM operates within a fixed context window — the total number of tokens (prompt + response) that the model can process in a single interaction. As of 2025, context windows range from 8K tokens for lightweight models to 200K+ for frontier models, but effective utilization is not simply a matter of fitting within the limit. Research consistently shows that model attention degrades over very long contexts [Liu2024], with information in the middle of a long prompt receiving less weight than information at the beginning or end.

**Practical strategies for token management:**

**Front-load critical instructions.** Place the most important constraints, role assignments, and output specifications at the beginning of the prompt. Secondary context and reference material should follow. This aligns with the primacy effect observed in LLM attention patterns.

**Use structured references instead of inline content.** Rather than pasting an entire file into the prompt, provide a summary and reference the file by path: "The authentication module at `src/auth/session.py` implements JWT-based session management. Key functions: `create_token()`, `verify_token()`, `refresh_token()`. Review these for..." This is how the production prompts in this repository work with VS Code Copilot — the agent resolves file references dynamically, keeping the prompt itself compact.

**Set explicit length constraints on outputs.** Without a length constraint, models tend toward verbose responses that consume reply tokens unnecessarily. Specify expectations: "Provide a summary in 3–5 sentences," or "List no more than 5 findings, prioritized by severity."

**Estimate before executing.** A rough heuristic for English text is 1 token ≈ 4 characters or ≈ 0.75 words. For code, token density is higher due to syntax tokens. Before submitting a complex prompt, estimate the total token count (prompt + expected response) and verify it fits within the model's effective window with margin.

## 4.2 Context-Window Optimization

Beyond raw token counting, the *structure* of information within the context window affects output quality. The following strategies are drawn from both empirical research and the production patterns observed in this repository's template files.

**The Sandwich Principle.** For long prompts, place instructions at both the beginning and the end. The opening sets the frame ("You are a senior security engineer reviewing..."), and the closing reinforces the key requirements ("Remember: every finding must include a severity rating and a remediation timeline"). This counteracts the "lost in the middle" effect documented by Liu et al. [Liu2024].

**Chunked processing for large inputs.** When the input exceeds a comfortable fraction of the context window (a conservative threshold is 60%), split it into chunks and process each chunk separately, then synthesize results in a final prompt. This is the basis of map-reduce prompting strategies and is essential for tasks like reviewing an entire codebase.

**Progressive disclosure.** In agent-mode workflows (such as VS Code Copilot with `mode: 'agent'`), the model can request additional context as needed rather than receiving everything upfront. The prompt files in this repository's `prompts/*/prompts/` directories are designed for this pattern — they provide behavioral instructions and constraints, while the agent retrieves file contents on demand.

## 4.3 Version Control for Prompts

Prompts are code. They should be versioned, reviewed, tested, and deployed with the same discipline applied to application source code. This repository models this principle by maintaining prompt files in version-controlled directories, though the practice can be formalized further.

**Prompt files as first-class artifacts.** Store prompts in your repository alongside the code they operate on. The `.github/` directory convention used by VS Code Copilot is one approach; a `prompts/` directory at the project root is another. What matters is that prompts are tracked in Git, subject to code review, and included in your CI/CD pipeline where appropriate.

**Semantic versioning for prompts.** When a prompt change alters its behavior (as opposed to fixing a typo or improving readability), treat it as a version bump. The v0-to-v1 evolution of this repository's prompts (documented in `CHANGELOG.md`) represents this concept — the restructuring from monolithic to modular prompts warranted a major version change. See the `CHANGELOG.md` at the repository root for the recommended format.

**Diff-friendly formatting.** Write prompts with one instruction per line or one concept per paragraph to produce meaningful Git diffs. Avoid long, unbroken paragraphs where a single-word change produces an uninformative diff.

**Prompt review checklist.** Before merging a prompt change, verify: (a) the role assignment is appropriate, (b) all constraints are internally consistent, (c) output format is explicitly specified, (d) the prompt has been tested against at least three representative inputs, (e) token budget is within the target model's effective window.

## 4.3.1 Prompt Versioning with Git — Worked Example

Abstract advice about "version-controlling prompts" is more useful with a concrete example. Below is a realistic `git diff` showing a prompt change and the review reasoning it produces.

**Scenario:** The `review-code.prompt.md` prompt originally asked for findings in a prose list. The team decides to switch to a Markdown table for easier parsing.

```diff
--- a/prompts/python/prompts/review-code.prompt.md
+++ b/prompts/python/prompts/review-code.prompt.md
@@ -3,6 +3,7 @@
 mode: 'agent'
 description: 'Review Python code for style, correctness, type safety, and edge cases'
-version: '1.0.0'
+version: '1.1.0'
 ---

 # Role
@@ -18,8 +19,10 @@

 ## Output Format
-Present each finding as a bullet point with the file path, line number,
-severity (Critical / High / Medium / Low), and a one-sentence description.
+Present findings as a Markdown table with these columns:
+
+| File:Line | Severity | Category | Finding | Suggested Fix |
+| --- | --- | --- | --- | --- |
```

**Why this diff is reviewable:**

- **One instruction per line** — the old text wraps a single concept across two lines, but the new version uses a table header that is self-documenting. The diff clearly shows *what changed* (output format) without touching unrelated sections.
- **Version bump** — `version: '1.0.0'` → `'1.1.0'` signals a behavior change (minor, not patch, because the output format is structurally different).
- **Checklist applied:** (a) role unchanged ✓, (b) table columns are internally consistent with the severity levels defined earlier in the prompt ✓, (c) output format now explicitly specified as a table ✓, (d) team should re-run the prompt against 3 test inputs to verify the model produces valid Markdown tables ✓, (e) the added lines are ~40 tokens — negligible impact on budget ✓.

**Tip for diff-friendly formatting.** When writing prompts, use one of these structures:

- **One constraint per line** (bulleted list) — easiest to diff, easiest to reorder
- **One paragraph per concept** with a blank line between — produces clean block-level diffs
- **Avoid** long single-paragraph instructions — a one-word change produces an unreadable diff of the entire paragraph

## 4.4 Team Workflows

When multiple team members use and maintain prompts, coordination becomes essential. The following practices help prevent the drift, duplication, and inconsistency that can emerge across prompt directories.

**Single source of truth.** Shared instructions (e.g., code style rules, documentation standards, common linting configurations) should exist in exactly one file, referenced by other prompts rather than duplicated. If your Python style guide appears in three places, it will inevitably diverge. The v0 version of this repository had three independent copies of `codacy.instructions.md`. The current version consolidates them into `prompts/shared/codacy.instructions.md` — an example of this principle applied.

**Layered architecture.** Organize prompts into layers: (a) a base layer of universal instructions (language standards, security practices, documentation conventions), (b) a stack-specific layer (Python, TypeScript, FastAPI conventions), and (c) a task-specific layer (code review, feature generation, security audit). Each prompt composes the relevant layers rather than restating shared content.

**Prompt ownership.** Assign ownership of prompt files using the same CODEOWNERS mechanism you use for source code. Prompt changes should require approval from the designated owner, ensuring that modifications are intentional and tested.

## 4.5 Common Anti-Patterns

**The Kitchen-Sink Prompt.** Attempting to address every possible concern in a single prompt. Symptoms: prompts exceeding 2000 words, contradictory instructions, outputs that are mediocre across all dimensions rather than strong on any one. Solution: decompose into focused prompts (see Module 2, §2.2).

**The Implicit Assumption.** Relying on the model to infer requirements that are obvious to the prompt author but nowhere stated. Symptoms: outputs that are technically correct but miss the point, inconsistent behavior across runs. Solution: apply the Substitution Test (Module 2, §2.1) and have a colleague who is unfamiliar with the task read the prompt for ambiguities.

**The Copy-Paste Drift.** Duplicating prompt content across files instead of referencing a shared source. Symptoms: inconsistent instructions across related prompts, increasing maintenance burden. Solution: adopt the layered architecture described in §4.4.

**The Untested Prompt.** Deploying a prompt to a team without running it against representative inputs. Symptoms: surprising failures in production, prompts that work for the author but not for colleagues using different inputs. Solution: maintain a small test suite of inputs with expected outputs for each production prompt.

**The Stale Prompt.** A prompt that references tools, libraries, or practices that have changed since the prompt was written. Symptoms: the model generates code using deprecated APIs, recommends outdated tools. Solution: include prompts in your dependency-update review process and flag version-pinned references for periodic review.

## 4.6 Prompts in Your CI/CD Pipeline

Prompts are code, and like code they benefit from automated checks. Integrating prompt validation into your CI/CD pipeline catches errors before they reach production.

### 4.6.1 What to Validate Automatically

**Frontmatter schema.** Every `.prompt.md` file should have required YAML fields (`mode`, `description`, `version`). A lightweight shell or Python script can parse the frontmatter and fail the build if fields are missing. This repository enforces this with `scripts/lint-prompt-frontmatter.sh`, which runs as a GitHub Actions job alongside the Markdown link checker.

**Internal link integrity.** Prompts that reference other files by path (e.g., "Follow the standards in `prompts/shared/codacy.instructions.md`") will break silently if those files are renamed or deleted. The link-checker already running in this repository's CI (see `.github/workflows/lint-markdown.yml`) catches these regressions.

**Token budget guards.** For prompts that must fit within a specific context window, a CI step can measure file size and estimate token count. A simple check:

```bash
MAX_TOKENS=4000
for file in prompts/*/prompts/*.prompt.md; do
  chars=$(wc -c < "$file")
  est_tokens=$((chars / 4))
  if [ "$est_tokens" -gt "$MAX_TOKENS" ]; then
    echo "WARN: $file ≈ $est_tokens tokens (limit: $MAX_TOKENS)"
  fi
done
```

This is a rough heuristic — for precise enforcement, use a tokenizer library like `tiktoken` (Python) or `@anthropic-ai/tokenizer` (Node.js).

### 4.6.2 What to Validate Manually (via Code Review)

Some checks cannot be automated reliably and belong in the human review step:

- **Behavioral regression.** Did the prompt change produce different outputs for the same inputs? Run the prompt against 3–5 representative inputs before and after the change.
- **Constraint consistency.** Are all constraints in the prompt mutually achievable? A CI script cannot determine if "be concise" conflicts with "include all 12 OWASP categories."
- **Audience calibration.** Does the role assignment still match the intended user? A prompt written for senior engineers may need adjustment if the team onboards juniors.

### 4.6.3 Example GitHub Actions Workflow

The following workflow runs two parallel jobs — one for Markdown link checking and one for prompt frontmatter validation — on every push or pull request:

```yaml
name: Lint Markdown

on:
  push:
    branches: [main]
    paths: ['**/*.md']
  pull_request:
    branches: [main]
    paths: ['**/*.md']

jobs:
  markdown-link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check internal Markdown links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          use-verbose-mode: 'yes'
          config-file: '.github/workflows/mlc-config.json'
          folder-path: '.'
          file-extension: '.md'

  prompt-frontmatter-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate prompt file frontmatter
        run: ./scripts/lint-prompt-frontmatter.sh
```

This is the exact workflow used by this repository (`.github/workflows/lint-markdown.yml`). Extending it with a token-budget job requires only adding a third job block that runs the estimation script above.

---

## Check Your Understanding

<details>
<summary><strong>Q1: What two things must be recorded together when versioning a prompt to make results reproducible?</strong></summary>

**Answer:** The **prompt text** itself and the **model configuration** under which it was evaluated (model name/version, temperature, max tokens, top-p). Without capturing both, a known-good version cannot be reliably reproduced because model updates may change behaviour independently of the prompt.

</details>

<details>
<summary><strong>Q2: Name three prompt anti-patterns described in §4.5.</strong></summary>

**Answer:** Any three of: **vague or underspecified instructions**, **missing output format constraints**, **overly long system prompts that dilute focus**, **no negative examples or exclusion criteria**, **testing on only one model**, **no iteration log or baseline to compare against**.

</details>

<details>
<summary><strong>Q3: Why is including prompt evaluation in a CI/CD pipeline valuable?</strong></summary>

**Answer:** It catches **regressions automatically** — when a prompt or a model is updated, the pipeline runs the test suite and fails the build before degraded outputs reach production. This treats prompts as first-class code artefacts with the same quality guarantees as application code.

</details>

---

## Exercises

**Exercise 4.1 — Token Budget Estimation.** Select the largest prompt file in the repository (likely `prompts/react-fastapi/prompts/create-app-react-fastapi.prompt.md`). Estimate its token count using the 4-characters-per-token heuristic. Then verify your estimate using a tokenizer tool (such as OpenAI's `tiktoken` library or Anthropic's token counter). Calculate what fraction of a 128K context window this prompt consumes, and how much room remains for the model's response and any file content it needs to reference.

**Exercise 4.2 — Prompt Refactoring.** Identify a case of content duplication across two or more prompt files in the repository's `prompts/` directories. Propose a refactored structure that eliminates the duplication while preserving the functionality of each prompt. Write out the refactored files.

**Exercise 4.3 — Anti-Pattern Diagnosis.** Write a deliberately bad prompt that exhibits at least three of the anti-patterns described in §4.5. Then write a corrected version. In a brief (150–200 word) reflection, explain which anti-pattern was hardest to eliminate and why.

---

> **Validated against:** GPT-4o (2025-11), Claude 3.5 Sonnet, Gemini 1.5 Pro — February 2026.  
> Behavioral claims may drift as models are updated. Performance figures marked *(approx.)* are illustrative.

---

## References

- [Liu2024] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics, 12*, 157–173.
