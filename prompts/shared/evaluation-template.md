# Prompt Evaluation Template

> **Version:** 1.0.0 | **Last updated:** 2026-02-21

This template provides a structured framework for evaluating prompt effectiveness. It serves two purposes: (1) a manual rubric for assessing individual prompt outputs during development, and (2) a reference architecture for building automated evaluation pipelines in production.

---

## Part 1: Manual Evaluation Rubric

Use this rubric to score individual prompt outputs on a 1–5 Likert scale. Each dimension includes anchor descriptions for scores 1 (unacceptable), 3 (adequate), and 5 (excellent).

### Dimension 1: Relevance

Does the output address the task specified in the prompt?

| Score | Anchor |
|-------|--------|
| 1 | Output is off-topic or addresses a different task entirely. |
| 3 | Output addresses the core task but includes tangential or unnecessary content. |
| 5 | Output is precisely scoped to the task with no irrelevant material. |

### Dimension 2: Accuracy

Is the output factually and technically correct?

| Score | Anchor |
|-------|--------|
| 1 | Contains multiple factual errors, incorrect code, or hallucinated information. |
| 3 | Mostly correct with minor errors that do not compromise the overall result. |
| 5 | Fully correct; code compiles/runs, facts are verifiable, logic is sound. |

### Dimension 3: Completeness

Does the output cover all requirements specified in the prompt?

| Score | Anchor |
|-------|--------|
| 1 | Addresses fewer than half of the stated requirements. |
| 3 | Addresses most requirements but omits one or more non-trivial items. |
| 5 | Addresses every stated requirement with no omissions. |

### Dimension 4: Format Compliance

Does the output conform to the structural and formatting requirements?

| Score | Anchor |
|-------|--------|
| 1 | Output format bears no resemblance to the specification (e.g., prose when JSON was required). |
| 3 | Output follows the general format but deviates in specific details (e.g., missing fields, wrong nesting). |
| 5 | Output matches the specified format exactly; parseable by downstream systems without modification. |

### Dimension 5: Safety and Constraint Adherence

Does the output respect all negative constraints, safety requirements, and boundaries?

| Score | Anchor |
|-------|--------|
| 1 | Violates explicit constraints (e.g., uses a banned library, exposes secrets, ignores safety instructions). |
| 3 | Respects critical constraints but bends minor guidelines (e.g., slightly exceeds a length limit). |
| 5 | Fully respects all constraints, including edge cases and implicit safety requirements. |

### Scoring

Compute the overall score as the unweighted mean of all five dimensions. For domain-specific applications, you may assign weights to reflect the relative importance of each dimension (e.g., safety-critical applications should weight Dimension 5 at 2× or 3×).

---

## Part 2: Sample Evaluation Walkthrough

To illustrate how the rubric is applied, here is a scored example.

**Prompt under evaluation:**
```
You are a Python code reviewer. Review the following function for type
annotation correctness, docstring completeness, and edge-case handling.
Output your findings as a numbered list with severity ratings.

def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
```

**Model output (abbreviated):**
```
1. [Critical] Missing type annotations. The function signature should be:
   def calculate_average(numbers: Sequence[float]) -> float

2. [Critical] No docstring. Add a Google-style docstring with Args,
   Returns, and Raises sections.

3. [Critical] ZeroDivisionError on empty input. Add a guard:
   if not numbers: raise ValueError("Cannot calculate average of empty sequence")

4. [Suggestion] Consider using statistics.mean() for numerical stability
   on large datasets.
```

**Rubric scores:**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Relevance | 5 | All findings directly address the three requested dimensions. |
| Accuracy | 4 | Findings 1–3 are correct. Finding 4 is reasonable but `statistics.mean()` does not improve numerical stability for standard use cases — this is a minor inaccuracy. |
| Completeness | 5 | All three requested review dimensions are covered. The bonus suggestion adds value. |
| Format Compliance | 5 | Output follows the requested numbered-list format with severity ratings. |
| Safety/Constraints | 5 | No constraint violations. |
| **Overall** | **4.8** | |

This output would be considered excellent. An output scoring below 3.0 overall should trigger a prompt revision.

---

## Part 3: Automated Evaluation Pipeline

For production prompts, manual evaluation does not scale. This section describes a reference architecture for automated evaluation.

### 3.1 Test Suite Structure

Organize test cases as JSON files with the following schema:

```json
{
  "test_suite": "python-code-review",
  "version": "1.0.0",
  "cases": [
    {
      "id": "tcr-001",
      "description": "Function with missing type annotations and no error handling",
      "input": "def calculate_average(numbers):\n    return sum(numbers) / len(numbers)",
      "context": {},
      "expected_findings": [
        {"dimension": "type_annotations", "severity": "critical"},
        {"dimension": "edge_cases", "severity": "critical", "specific": "ZeroDivisionError"},
        {"dimension": "docstring", "severity": "critical"}
      ],
      "expected_format": "numbered_list_with_severity"
    },
    {
      "id": "tcr-002",
      "description": "Well-typed function with comprehensive docstring",
      "input": "def calculate_average(numbers: Sequence[float]) -> float:\n    \"\"\"Calculate the arithmetic mean.\n\n    Args:\n        numbers: Non-empty sequence of numbers.\n\n    Returns:\n        The arithmetic mean.\n\n    Raises:\n        ValueError: If the sequence is empty.\n    \"\"\"\n    if not numbers:\n        raise ValueError('Empty sequence')\n    return sum(numbers) / len(numbers)",
      "context": {},
      "expected_findings": [],
      "expected_format": "numbered_list_with_severity",
      "notes": "Output should confirm no issues found or suggest only minor improvements"
    }
  ]
}
```

### 3.2 Automated Metrics

For each test case, compute the following metrics programmatically:

**Finding Recall** — What fraction of expected findings did the model identify? This is computed as: `|expected ∩ actual| / |expected|`. A finding is considered "matched" if it addresses the same dimension and severity level, regardless of exact wording.

**Finding Precision** — What fraction of the model's findings are legitimate (i.e., not false positives)? This is computed as: `|expected ∩ actual| / |actual|`. False positives indicate the model is hallucinating issues.

**Format Compliance Rate** — Does the output parse correctly into the expected structure? For JSON outputs, this is a binary check. For structured text (like numbered lists with severity), use a regex or lightweight parser.

**Consistency Score** — Run the same prompt and input N times (typically N = 5) and measure output variance. For deterministic tasks (code review, classification), the outputs should be highly consistent. Report the pairwise similarity (e.g., Jaccard index on the set of finding types) across runs.

### 3.3 LLM-as-Judge Integration

For dimensions that are difficult to assess programmatically (e.g., the quality of a suggestion, the clarity of an explanation), use a secondary LLM as a judge. See Module 5, §5.4.3 for the judge prompt template.

The judge's output should be structured (JSON with numeric scores and textual rationale) and should be calibrated against human evaluations on a held-out set of at least 20 examples. Report the correlation (Pearson or Spearman) between judge scores and human scores as a measure of judge reliability.

### 3.4 A/B Testing Protocol

When comparing two prompt variants for deployment, follow this protocol:

**Step 1: Hypothesis.** State what you expect Variant B to improve over Variant A, and by how much. Example: "Variant B (with explicit severity definitions) will improve Finding Precision by at least 10 percentage points over Variant A (without severity definitions)."

**Step 2: Sample size determination.** Use a power analysis to determine the required number of test cases. For detecting a 10-percentage-point difference in a proportion with 80% power and α = 0.05, you need approximately 200 test cases per variant. For smaller effect sizes, you need more.

**Step 3: Randomization.** Randomly assign each test case to Variant A or Variant B. If test cases are reusable, use a within-subjects design (both variants see every test case) and apply a paired test (McNemar's test for binary outcomes, Wilcoxon signed-rank for ordinal/continuous).

**Step 4: Execution.** Run both variants under identical conditions (same model, same temperature, same max tokens). Log all inputs, outputs, and metadata.

**Step 5: Analysis.** Compute the primary metric for each variant. Report the difference, 95% confidence interval, and p-value. If using multiple metrics, apply a Bonferroni correction to the significance threshold.

**Step 6: Decision.** If the primary metric shows a statistically significant improvement and no secondary metric shows a significant regression, deploy Variant B. Otherwise, retain Variant A or investigate further.

---

## Part 4: Continuous Monitoring

After deployment, track prompt performance over time by logging a random sample of production inputs and outputs (with appropriate privacy controls) and running them through the automated evaluation pipeline on a weekly cadence. Plot metric trends and set alerts for significant degradation (e.g., a 2-standard-deviation drop in any primary metric over a rolling 4-week window).

Common causes of prompt degradation include model updates (the underlying LLM is updated by the provider), input distribution shift (users start submitting inputs the prompt was not designed for), and context drift (the codebase evolves but the prompt references outdated patterns or deprecated APIs). Each cause has a distinct remediation: model updates require re-evaluation and possible prompt revision; input shift requires test-suite expansion; context drift requires prompt maintenance as part of regular dependency updates.

---

## Cross-References

This template is referenced from the `learn/` curriculum at Module 2, §2.4 (Principle: Evaluation), Module 4, §4.3 (Version Control for Prompts), and Module 5, §5.4 (Systematic Evaluation Methodology). The centralized bibliography is at `references.md`.
