#!/usr/bin/env python3
"""
Lab 4 — Building a Mini Evaluation Pipeline
=============================================
Module reference: Module 5, §5.4 (Evaluation Pipelines)

This lab builds a complete (small-scale) prompt evaluation pipeline:
  1. Define a test suite of (input, expected_output) pairs
  2. Run two prompt variants against the suite
  3. Score outputs using LLM-as-Judge and exact-match
  4. Aggregate metrics and declare a winner

This mirrors the methodology described in the Advanced Patterns module
and the evaluation-template.md shared resource.

Usage:
    python lab_04_evaluation_pipeline.py
"""

from __future__ import annotations

import json
import time

from lab_utils import complete, get_client, print_comparison_table, print_header

# ---------------------------------------------------------------------------
# Test suite: email subject-line generation
# ---------------------------------------------------------------------------
TEST_SUITE = [
    {
        "input": "We're launching a 30% off sale on all running shoes this weekend.",
        "criteria": "mentions discount percentage and product category",
    },
    {
        "input": "Reminder: your annual subscription renews in 3 days. Update payment info if needed.",
        "criteria": "conveys urgency and mentions renewal timeline",
    },
    {
        "input": "Thank you for attending our webinar on cloud security. Here are the slides and recording.",
        "criteria": "references the webinar topic and mentions deliverables",
    },
    {
        "input": "We've updated our privacy policy effective January 1. Please review the changes.",
        "criteria": "mentions policy update and effective date",
    },
    {
        "input": "Congratulations! You've been selected for early access to our new AI assistant.",
        "criteria": "conveys exclusivity and names the product",
    },
]

# ---------------------------------------------------------------------------
# Two prompt variants to compare
# ---------------------------------------------------------------------------
SYSTEM = "You are an email marketing specialist."

VARIANT_A = (
    "Write a subject line for this email:\n\n"
    "{body}\n\n"
    "Subject line:"
)

VARIANT_B = (
    "Write a compelling email subject line that is:\n"
    "- Under 60 characters\n"
    "- Action-oriented (uses a verb)\n"
    "- Specific about the key benefit or information\n"
    "- Free of spam trigger words (FREE, URGENT, !!!)\n\n"
    "Email body:\n{body}\n\n"
    "Subject line:"
)

# ---------------------------------------------------------------------------
# LLM-as-Judge evaluation
# ---------------------------------------------------------------------------
JUDGE_SYSTEM = "You are a strict email marketing evaluator. Return ONLY valid JSON."

JUDGE_TEMPLATE = (
    "Evaluate this email subject line on each criterion (1-5 scale).\n\n"
    "Email body: {body}\n"
    "Subject line: {subject}\n"
    "Quality criteria: {criteria}\n\n"
    "Score these dimensions and return ONLY a JSON object:\n"
    "- relevance: Does it accurately reflect the email content? (1-5)\n"
    "- clarity: Is it clear and easy to understand? (1-5)\n"
    "- engagement: Would it entice the reader to open the email? (1-5)\n"
    "- criteria_met: Does it meet the specific criteria above? (1-5)\n"
    "- conciseness: Is it appropriately brief? (1-5)\n\n"
    "JSON:"
)


def judge_output(body: str, subject: str, criteria: str, client) -> dict:
    """Score a subject line using LLM-as-Judge."""
    prompt = JUDGE_TEMPLATE.format(body=body, subject=subject, criteria=criteria)
    raw = complete(prompt, system=JUDGE_SYSTEM, client=client, temperature=0.0)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return {}


def length_check(subject: str, max_chars: int = 60) -> bool:
    """Heuristic: subject line under max_chars."""
    return len(subject.strip()) <= max_chars


def run_experiment() -> None:
    print_header("Lab 4 — Mini Evaluation Pipeline")

    client = get_client()

    # --- Step 1: Generate outputs ---
    print_header("Step 1: Generate Subject Lines")
    variant_outputs: dict[str, list[str]] = {"A": [], "B": []}

    for case in TEST_SUITE:
        body = case["input"]
        for variant_name, template in [("A", VARIANT_A), ("B", VARIANT_B)]:
            prompt = template.format(body=body)
            raw = complete(prompt, system=SYSTEM, client=client, temperature=0.3)
            subject = raw.strip().strip('"').strip("'").splitlines()[0]
            variant_outputs[variant_name].append(subject)

    # Print generated subjects
    headers = ["Email (truncated)", "Variant A", "Variant B"]
    rows = []
    for i, case in enumerate(TEST_SUITE):
        rows.append([
            case["input"][:45] + "...",
            variant_outputs["A"][i][:50],
            variant_outputs["B"][i][:50],
        ])
    print_comparison_table(headers, rows)

    # --- Step 2: Heuristic checks ---
    print_header("Step 2: Heuristic Checks (length ≤ 60 chars)")
    headers = ["Email #", "Variant A (len)", "A Pass", "Variant B (len)", "B Pass"]
    rows = []
    for i in range(len(TEST_SUITE)):
        a_len = len(variant_outputs["A"][i])
        b_len = len(variant_outputs["B"][i])
        rows.append([
            str(i + 1),
            str(a_len),
            "✓" if length_check(variant_outputs["A"][i]) else "✗",
            str(b_len),
            "✓" if length_check(variant_outputs["B"][i]) else "✗",
        ])
    print_comparison_table(headers, rows)

    # --- Step 3: LLM-as-Judge scoring ---
    print_header("Step 3: LLM-as-Judge Scoring")
    all_scores: dict[str, list[dict]] = {"A": [], "B": []}
    dimensions = ["relevance", "clarity", "engagement", "criteria_met", "conciseness"]

    for i, case in enumerate(TEST_SUITE):
        for variant_name in ("A", "B"):
            subject = variant_outputs[variant_name][i]
            scores = judge_output(case["input"], subject, case["criteria"], client)
            all_scores[variant_name].append(scores)
            time.sleep(0.2)  # gentle rate limiting

    # Per-case scores
    for i, case in enumerate(TEST_SUITE):
        print(f"\n  Email {i+1}: {case['input'][:50]}...")
        for variant_name in ("A", "B"):
            s = all_scores[variant_name][i]
            score_str = ", ".join(f"{d}={s.get(d, '?')}" for d in dimensions)
            print(f"    Variant {variant_name}: {score_str}")

    # --- Step 4: Aggregate metrics ---
    print_header("Step 4: Aggregate Results")

    def avg_score(variant: str, dim: str) -> float:
        vals = [s.get(dim, 0) for s in all_scores[variant] if isinstance(s.get(dim), (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    headers = ["Dimension", "Variant A (avg)", "Variant B (avg)", "Winner"]
    rows = []
    a_wins = 0
    b_wins = 0
    for dim in dimensions:
        a_avg = avg_score("A", dim)
        b_avg = avg_score("B", dim)
        if a_avg > b_avg:
            winner = "A"
            a_wins += 1
        elif b_avg > a_avg:
            winner = "B"
            b_wins += 1
        else:
            winner = "Tie"
        rows.append([dim.replace("_", " ").title(), f"{a_avg:.1f}", f"{b_avg:.1f}", winner])

    # Add length compliance row
    a_pass = sum(1 for s in variant_outputs["A"] if length_check(s))
    b_pass = sum(1 for s in variant_outputs["B"] if length_check(s))
    rows.append(["Length ≤60 (count)", f"{a_pass}/{len(TEST_SUITE)}", f"{b_pass}/{len(TEST_SUITE)}",
                 "A" if a_pass > b_pass else ("B" if b_pass > a_pass else "Tie")])
    print_comparison_table(headers, rows)

    # --- Declare winner ---
    print_header("Conclusion")
    overall = "Variant B" if b_wins > a_wins else ("Variant A" if a_wins > b_wins else "Tie")
    print(f"  Variant A won {a_wins} dimensions, Variant B won {b_wins} dimensions.")
    print(f"  Overall winner: {overall}")
    print()
    print("Takeaway: Variant B's explicit constraints (length, verb usage, no spam words)")
    print("give the model concrete success criteria, which typically produces more")
    print("consistent, higher-quality output. This demonstrates the value of building")
    print("evaluation pipelines to objectively compare prompt variants.")
    print("See Module 5, §5.4 and prompts/shared/evaluation-template.md for methodology.\n")


if __name__ == "__main__":
    run_experiment()
