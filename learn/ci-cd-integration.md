# CI/CD Integration Guide for Prompt Engineering

## Overview

Prompts are code. Like application code, they benefit from automated testing, version control, and continuous integration. This guide shows how to integrate prompt evaluation into your CI/CD pipeline using GitHub Actions, building on the evaluation methodology from Module 5, §5.4 and the prompt registry schema from `prompts/shared/`.

---

## 1. What to Automate

| Check | Purpose | Blocking? | Complexity |
| --- | --- | --- | --- |
| **Frontmatter lint** | Ensure `.prompt.md` files have required YAML fields (`mode`, `description`, `version`) | ✅ Yes | Low |
| **Markdown link check** | Catch broken links across the curriculum and prompt files | ✅ Yes | Low |
| **Token budget estimate** | Warn if a prompt exceeds a configurable token threshold | ⚠️ Advisory | Low |
| **Prompt regression tests** | Run prompts against a test suite and check output quality | ✅ Yes (for production prompts) | Medium |
| **Schema validation** | Validate prompt metadata against a JSON schema | ✅ Yes | Low |
| **Security scan** | Check prompts for accidental secret leaks or injection-vulnerable patterns | ✅ Yes | Low |

This repository already implements the first three in `.github/workflows/lint-markdown.yml`. This guide covers the remaining three.

---

## 2. Prompt Regression Testing

### Concept

A prompt regression test is analogous to a unit test for code. You maintain a set of (input, expected behavior) pairs and run them against your prompt after every change. If outputs degrade, the CI pipeline fails.

### Test Suite Structure

Create a `tests/` directory alongside your prompts:

```
prompts/
  python/
    prompts/
      review-code.prompt.md
    tests/
      review-code/
        test_suite.json
        evaluate.py
```

**test_suite.json:**
```json
{
  "prompt_file": "review-code.prompt.md",
  "model": "gpt-4o",
  "temperature": 0.0,
  "test_cases": [
    {
      "id": "tc-001",
      "description": "Missing type hints",
      "input": "def add(a, b):\n    return a + b",
      "assertions": [
        {"type": "contains", "value": "type hint"},
        {"type": "format", "value": "numbered list"}
      ]
    },
    {
      "id": "tc-002",
      "description": "Empty function",
      "input": "def process():\n    pass",
      "assertions": [
        {"type": "contains", "value": "implementation"},
        {"type": "min_length", "value": 50}
      ]
    }
  ]
}
```

### Evaluation Script

**evaluate.py:**
```python
#!/usr/bin/env python3
"""
Prompt regression test runner.

Usage:
    python evaluate.py test_suite.json

Exit codes:
    0 — all tests passed
    1 — one or more tests failed
"""

import json
import os
import re
import sys

from openai import OpenAI


def load_test_suite(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def load_prompt(prompt_path: str) -> str:
    with open(prompt_path) as f:
        content = f.read()
    # Strip YAML frontmatter
    if content.startswith("---"):
        end = content.index("---", 3) + 3
        content = content[end:].strip()
    return content


def run_prompt(client: OpenAI, prompt: str, user_input: str,
               model: str, temperature: float) -> str:
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ],
    )
    return response.choices[0].message.content or ""


def check_assertion(output: str, assertion: dict) -> tuple[bool, str]:
    atype = assertion["type"]
    value = assertion["value"]

    if atype == "contains":
        passed = value.lower() in output.lower()
        return passed, f"contains '{value}': {'PASS' if passed else 'FAIL'}"

    if atype == "not_contains":
        passed = value.lower() not in output.lower()
        return passed, f"not_contains '{value}': {'PASS' if passed else 'FAIL'}"

    if atype == "min_length":
        passed = len(output) >= int(value)
        return passed, f"min_length {value}: {'PASS' if passed else 'FAIL'} (actual: {len(output)})"

    if atype == "max_length":
        passed = len(output) <= int(value)
        return passed, f"max_length {value}: {'PASS' if passed else 'FAIL'} (actual: {len(output)})"

    if atype == "format":
        if value == "numbered list":
            passed = bool(re.search(r"^\d+\.", output, re.MULTILINE))
        elif value == "json":
            try:
                json.loads(output)
                passed = True
            except json.JSONDecodeError:
                passed = False
        elif value == "markdown":
            passed = bool(re.search(r"^#{1,6}\s", output, re.MULTILINE))
        else:
            passed = True  # unknown format, skip
        return passed, f"format '{value}': {'PASS' if passed else 'FAIL'}"

    if atype == "regex":
        passed = bool(re.search(value, output, re.IGNORECASE | re.MULTILINE))
        return passed, f"regex '{value}': {'PASS' if passed else 'FAIL'}"

    return True, f"unknown assertion type '{atype}': SKIPPED"


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py test_suite.json")
        sys.exit(1)

    suite_path = sys.argv[1]
    suite = load_test_suite(suite_path)

    # Resolve prompt path relative to test suite
    suite_dir = os.path.dirname(os.path.abspath(suite_path))
    prompt_path = os.path.join(suite_dir, "..", suite["prompt_file"])
    prompt = load_prompt(prompt_path)

    client = OpenAI()
    model = suite.get("model", "gpt-4o")
    temperature = suite.get("temperature", 0.0)

    total = 0
    passed = 0
    failed = 0

    for case in suite["test_cases"]:
        total += 1
        print(f"\n--- Test {case['id']}: {case['description']} ---")
        output = run_prompt(client, prompt, case["input"], model, temperature)
        print(f"Output preview: {output[:200]}...")

        case_passed = True
        for assertion in case["assertions"]:
            ok, msg = check_assertion(output, assertion)
            print(f"  {msg}")
            if not ok:
                case_passed = False

        if case_passed:
            passed += 1
            print(f"  → PASSED")
        else:
            failed += 1
            print(f"  → FAILED")

    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
```

### GitHub Actions Workflow

Add this job to your workflow to run prompt regression tests on every PR that modifies prompt files:

```yaml
# .github/workflows/prompt-regression.yml
name: Prompt Regression Tests

on:
  pull_request:
    paths:
      - 'prompts/**/*.prompt.md'
      - 'prompts/**/tests/**'

jobs:
  prompt-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install openai

      - name: Run prompt regression tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          failed=0
          for suite in prompts/**/tests/*/test_suite.json; do
            echo "Running: $suite"
            python "$(dirname "$suite")/evaluate.py" "$suite" || failed=1
          done
          exit $failed
```

---

## 3. Schema Validation

If you adopt the prompt registry schema (see [prompt-registry.schema.json](../prompts/shared/prompt-registry.schema.json) if available), add a validation step:

```yaml
  schema-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install jsonschema
        run: pip install jsonschema pyyaml

      - name: Validate prompt frontmatter
        run: |
          python scripts/validate-prompt-schema.py prompts/**/*.prompt.md
```

---

## 4. Security Scanning for Prompts

Prompts can accidentally leak patterns that indicate sensitive content:

```yaml
  prompt-security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan for sensitive patterns
        run: |
          echo "Scanning prompt files for potential secrets..."
          patterns=(
            'sk-[a-zA-Z0-9]{20,}'        # OpenAI API keys
            'ghp_[a-zA-Z0-9]{36}'         # GitHub PATs
            'AKIA[0-9A-Z]{16}'            # AWS access keys
            'password\s*[:=]\s*\S+'       # Hardcoded passwords
          )
          failed=0
          for pattern in "${patterns[@]}"; do
            if grep -rPn "$pattern" prompts/ learn/; then
              echo "FAIL: Found sensitive pattern: $pattern"
              failed=1
            fi
          done
          if [ $failed -eq 0 ]; then
            echo "PASS: No sensitive patterns found."
          fi
          exit $failed
```

---

## 5. Complete Workflow Example

Here is a complete `.github/workflows/prompt-ci.yml` that combines all checks:

```yaml
name: Prompt CI

on:
  pull_request:
    paths:
      - 'prompts/**'
      - 'learn/**'
      - 'scripts/**'

  push:
    branches: [main]
    paths:
      - 'prompts/**'
      - 'learn/**'

jobs:
  # --- Lint checks (fast, no API needed) ---
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint prompt frontmatter
        run: bash scripts/lint-prompt-frontmatter.sh

      - name: Check markdown links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'

  # --- Token budget (fast, no API needed) ---
  token-budget:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Estimate token budgets
        run: |
          for f in $(find prompts -name '*.prompt.md'); do
            chars=$(wc -c < "$f")
            tokens=$((chars / 4))
            if [ "$tokens" -gt 4000 ]; then
              echo "WARNING: $f ≈ $tokens tokens (exceeds 4000)"
            else
              echo "OK: $f ≈ $tokens tokens"
            fi
          done

  # --- Security scan (fast, no API needed) ---
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan for secrets in prompts
        run: |
          patterns='(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16})'
          if grep -rPn "$patterns" prompts/ learn/; then
            echo "::error::Potential secrets found in prompt files"
            exit 1
          fi
          echo "No secrets found."

  # --- Regression tests (requires API key, runs only on prompt changes) ---
  regression:
    if: github.event_name == 'pull_request'
    needs: [lint, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - run: pip install openai

      - name: Run prompt regression tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          found=0
          for suite in $(find prompts -name 'test_suite.json' 2>/dev/null); do
            dir=$(dirname "$suite")
            if [ -f "$dir/evaluate.py" ]; then
              echo "Running: $suite"
              python "$dir/evaluate.py" "$suite" || found=1
            fi
          done
          if [ $found -eq 0 ] && [ "$(find prompts -name 'test_suite.json' | wc -l)" -eq 0 ]; then
            echo "No test suites found — skipping regression tests."
          fi
          exit $found
```

---

## 6. Best Practices

1. **Separate fast checks from slow checks.** Lint, link-check, and security scans run in seconds. Regression tests call the LLM API and take minutes. Run them in parallel, and gate regression tests behind the fast checks.

2. **Use temperature 0 for regression tests.** Non-determinism is the enemy of CI. Set `temperature: 0` so outputs are as reproducible as possible (though not perfectly — model updates can still change outputs).

3. **Test behavior, not exact text.** Assert on structural properties (contains keyword, correct format, within length range) rather than exact string matches. This makes tests robust to minor model output variations.

4. **Budget API costs.** Limit the number of test cases to what you can afford per PR. 5–10 cases per prompt is typically sufficient for catching regressions.

5. **Version your test suites with your prompts.** When you change a prompt, update the corresponding test suite in the same commit.

6. **Cache evaluation results.** For long-running test suites, consider caching outputs for unchanged (prompt + input) pairs to avoid redundant API calls.

---

## Connection to This Repository

- The existing workflow at `.github/workflows/lint-markdown.yml` implements the frontmatter lint and markdown link checks.
- The evaluation methodology is described in Module 5, §5.4 and `prompts/shared/evaluation-template.md`.
- The lab at `learn/labs/lab_04_evaluation_pipeline.py` demonstrates the evaluation approach interactively.
- The prompt registry schema (Item 18) provides the validation target for schema checks.

---

[← Back to curriculum](README.md)
