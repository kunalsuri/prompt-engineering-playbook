#!/usr/bin/env python3
"""
Lab 2 — Chain-of-Thought Prompting
====================================
Module reference: Module 3, §3.4 (Chain-of-Thought)

This lab compares direct-answer prompting with Chain-of-Thought (CoT) on
multi-step arithmetic / reasoning problems. The hypothesis is that CoT
reduces errors on problems requiring intermediate steps.

Usage:
    python lab_02_chain_of_thought.py
"""

from __future__ import annotations

from lab_utils import complete, get_client, print_comparison_table, print_header

# ---------------------------------------------------------------------------
# Test problems: (question, expected_answer)
# ---------------------------------------------------------------------------
PROBLEMS = [
    (
        "A store has 23 apples. They sell 8, then receive a shipment of 15. "
        "A customer returns 3 apples. How many apples does the store have?",
        "33",
    ),
    (
        "A train travels at 60 km/h for 2.5 hours, then at 80 km/h for "
        "1.5 hours. What is the total distance traveled?",
        "270",
    ),
    (
        "Maria has $50. She buys 3 books at $8 each and 2 pens at $3 each. "
        "How much money does she have left?",
        "20",
    ),
    (
        "A rectangular garden is 12 meters long and 8 meters wide. A path "
        "1 meter wide surrounds the garden. What is the area of the path?",
        "44",
    ),
    (
        "In a class of 30 students, 40% prefer math, 30% prefer science, "
        "and the rest prefer art. How many students prefer art?",
        "9",
    ),
]

# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------
SYSTEM = "You are a helpful math tutor."

DIRECT_TEMPLATE = (
    "Answer the following question. Provide ONLY the final numerical answer, "
    "with no units or explanation.\n\n"
    "Question: {question}\n"
    "Answer:"
)

COT_TEMPLATE = (
    "Answer the following question. Think step by step, showing your work. "
    "After your reasoning, provide the final numerical answer on a new line "
    "prefixed with 'ANSWER: '.\n\n"
    "Question: {question}\n"
    "Solution:"
)


def extract_number(raw: str) -> str:
    """Pull the numeric answer from model output."""
    # For CoT, look for "ANSWER:" line
    for line in reversed(raw.strip().splitlines()):
        if "ANSWER:" in line.upper():
            parts = line.upper().split("ANSWER:")
            num_str = parts[-1].strip().rstrip(".")
            # Remove units / extra text
            tokens = num_str.split()
            if tokens:
                return tokens[0].replace(",", "").replace("$", "")
    # Fallback: take last number-like token in entire output
    import re

    numbers = re.findall(r"-?\d+\.?\d*", raw)
    return numbers[-1] if numbers else raw.strip()[:20]


def answers_match(predicted: str, expected: str) -> bool:
    """Compare numeric answers with tolerance for float rounding."""
    try:
        return abs(float(predicted) - float(expected)) < 0.5
    except ValueError:
        return predicted.strip() == expected.strip()


def run_experiment() -> None:
    print_header("Lab 2 — Chain-of-Thought Prompting")

    client = get_client()
    results: dict[str, list[dict]] = {"direct": [], "cot": []}

    for variant_name, template in [("direct", DIRECT_TEMPLATE), ("cot", COT_TEMPLATE)]:
        label = "Direct" if variant_name == "direct" else "CoT"
        print(f"\nRunning {label} variant on {len(PROBLEMS)} problems...")
        for question, expected in PROBLEMS:
            prompt = template.format(question=question)
            raw = complete(prompt, system=SYSTEM, client=client, temperature=0.0)
            predicted = extract_number(raw)
            correct = answers_match(predicted, expected)

            results[variant_name].append({
                "question": question[:50] + "...",
                "expected": expected,
                "predicted": predicted,
                "correct": correct,
                "raw_snippet": raw.strip()[:80].replace("\n", " "),
            })

    # --- Print results ---
    for variant_name in ("direct", "cot"):
        label = "Direct Answer" if variant_name == "direct" else "Chain-of-Thought"
        print(f"\n--- {label} Results ---")
        headers = ["Problem (truncated)", "Expected", "Predicted", "Correct"]
        rows = []
        for r in results[variant_name]:
            rows.append([
                r["question"],
                r["expected"],
                r["predicted"],
                "✓" if r["correct"] else "✗",
            ])
        print_comparison_table(headers, rows)

    # --- Summary ---
    print_header("Summary")
    d_acc = sum(1 for r in results["direct"] if r["correct"]) / len(PROBLEMS) * 100
    c_acc = sum(1 for r in results["cot"] if r["correct"]) / len(PROBLEMS) * 100
    headers = ["Metric", "Direct", "CoT"]
    rows = [["Accuracy", f"{d_acc:.0f}%", f"{c_acc:.0f}%"]]
    print_comparison_table(headers, rows)

    print("Takeaway: Chain-of-Thought prompting helps the model 'show its work',")
    print("reducing arithmetic errors on multi-step problems.  See Module 3, §3.4")
    print("and the Chain-of-Thought Comparison document for empirical analysis.\n")

    # --- Show a CoT trace example ---
    if results["cot"]:
        print_header("Example CoT Trace (Problem 1)")
        prompt = COT_TEMPLATE.format(question=PROBLEMS[0][0])
        trace = complete(prompt, system=SYSTEM, client=client, temperature=0.0)
        print(trace.strip())
        print()


if __name__ == "__main__":
    run_experiment()
