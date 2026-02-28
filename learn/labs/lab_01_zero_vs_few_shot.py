#!/usr/bin/env python3
"""
Lab 1 — Zero-Shot vs. Few-Shot Classification
===============================================
Module reference: Module 3, §3.2 (Zero-Shot) and §3.3 (Few-Shot)

This lab sends the same classification task to an LLM twice:
  1. Zero-shot: instruction only, no examples
  2. Few-shot:  instruction + 3 demonstration examples

It runs each variant multiple times and compares accuracy and consistency.

Usage:
    python lab_01_zero_vs_few_shot.py
"""

from __future__ import annotations

from lab_utils import complete, get_client, print_comparison_table, print_header

# ---------------------------------------------------------------------------
# Test data: (input_text, expected_label)
# ---------------------------------------------------------------------------
TEST_CASES = [
    ("The battery lasts all day and the camera is incredible!", "Positive"),
    ("Delivery was fast but the product broke after two days.", "Negative"),
    ("It's okay for the price. Nothing special, nothing terrible.", "Neutral"),
    ("Absolutely love it — best purchase I've made this year.", "Positive"),
    ("Waste of money. Returned it immediately.", "Negative"),
]

# ---------------------------------------------------------------------------
# Prompt variants
# ---------------------------------------------------------------------------
SYSTEM = "You are a sentiment classifier. Respond with exactly one word: Positive, Negative, or Neutral."

ZERO_SHOT_TEMPLATE = (
    "Classify the sentiment of the following product review.\n"
    "Respond with exactly one word: Positive, Negative, or Neutral.\n\n"
    "Review: \"{review}\"\n"
    "Sentiment:"
)

FEW_SHOT_TEMPLATE = (
    "Classify the sentiment of product reviews.\n"
    "Respond with exactly one word: Positive, Negative, or Neutral.\n\n"
    "Review: \"Superb quality and fast shipping!\" → Positive\n"
    "Review: \"Stopped working after a week. Very disappointed.\" → Negative\n"
    "Review: \"It does what it says. Average product.\" → Neutral\n\n"
    "Review: \"{review}\"\n"
    "Sentiment:"
)

RUNS_PER_VARIANT = 3


def normalize_label(raw: str) -> str:
    """Extract a clean label from model output."""
    cleaned = raw.strip().strip(".").strip()
    for label in ("Positive", "Negative", "Neutral"):
        if label.lower() in cleaned.lower():
            return label
    return cleaned[:20]  # fallback: truncated raw output


def run_experiment() -> None:
    print_header("Lab 1 — Zero-Shot vs. Few-Shot Classification")

    client = get_client()
    results: dict[str, list[dict]] = {"zero_shot": [], "few_shot": []}

    for variant_name, template in [("zero_shot", ZERO_SHOT_TEMPLATE), ("few_shot", FEW_SHOT_TEMPLATE)]:
        print(f"Running {variant_name.replace('_', '-')} variant ({RUNS_PER_VARIANT} runs × {len(TEST_CASES)} cases)...")
        for review, expected in TEST_CASES:
            prompt = template.format(review=review)
            run_results = []
            for _ in range(RUNS_PER_VARIANT):
                raw = complete(prompt, system=SYSTEM, client=client, temperature=0.3)
                predicted = normalize_label(raw)
                run_results.append(predicted)

            majority = max(set(run_results), key=run_results.count)
            correct = majority == expected
            consistent = len(set(run_results)) == 1

            results[variant_name].append({
                "review": review[:40] + "...",
                "expected": expected,
                "predictions": run_results,
                "majority": majority,
                "correct": correct,
                "consistent": consistent,
            })

    # --- Print results ---
    for variant_name in ("zero_shot", "few_shot"):
        label = variant_name.replace("_", "-").title()
        print(f"\n--- {label} Results ---")
        headers = ["Review (truncated)", "Expected", "Predictions", "Correct", "Consistent"]
        rows = []
        for r in results[variant_name]:
            rows.append([
                r["review"],
                r["expected"],
                ", ".join(r["predictions"]),
                "✓" if r["correct"] else "✗",
                "✓" if r["consistent"] else "✗",
            ])
        print_comparison_table(headers, rows)

    # --- Summary ---
    print_header("Summary")
    headers = ["Metric", "Zero-Shot", "Few-Shot"]
    zs = results["zero_shot"]
    fs = results["few_shot"]
    zs_acc = sum(1 for r in zs if r["correct"]) / len(zs) * 100
    fs_acc = sum(1 for r in fs if r["correct"]) / len(fs) * 100
    zs_con = sum(1 for r in zs if r["consistent"]) / len(zs) * 100
    fs_con = sum(1 for r in fs if r["consistent"]) / len(fs) * 100
    rows = [
        ["Accuracy (majority vote)", f"{zs_acc:.0f}%", f"{fs_acc:.0f}%"],
        ["Consistency (all runs agree)", f"{zs_con:.0f}%", f"{fs_con:.0f}%"],
    ]
    print_comparison_table(headers, rows)

    print("Takeaway: Few-shot examples typically improve both accuracy and consistency")
    print("on classification tasks, especially for ambiguous or edge-case inputs.")
    print("See Module 3, §3.3 and the Few-Shot Comparison document for deeper analysis.\n")


if __name__ == "__main__":
    run_experiment()
