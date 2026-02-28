#!/usr/bin/env python3
"""
Lab 3 — The Specificity Spectrum
=================================
Module reference: Module 2, §2.1 (Clarity and Specificity)

This lab demonstrates how increasing prompt specificity improves output
quality. It sends three versions of the same request — vague, moderate,
and highly specific — then scores the outputs on structure and detail.

Usage:
    python lab_03_specificity.py
"""

from __future__ import annotations

import json

from lab_utils import complete, get_client, print_comparison_table, print_header

# ---------------------------------------------------------------------------
# Three prompts at different specificity levels
# ---------------------------------------------------------------------------
SYSTEM = "You are a helpful writing assistant."

PROMPTS = {
    "vague": (
        "Write something about Python testing."
    ),
    "moderate": (
        "Write a guide about testing in Python. Cover unit tests and "
        "integration tests. Include code examples."
    ),
    "specific": (
        "Write a concise guide (300-400 words) on Python testing best "
        "practices for a mid-level developer. Structure the guide with "
        "these sections:\n"
        "1. **Unit Tests** — explain the AAA pattern (Arrange, Act, Assert) "
        "with a pytest example testing a `calculate_discount(price, percent)` "
        "function.\n"
        "2. **Integration Tests** — show a pytest example that tests a "
        "FastAPI endpoint using `TestClient`.\n"
        "3. **Key Principles** — list 3 bullet-point testing principles "
        "(e.g., test isolation, determinism, meaningful names).\n\n"
        "Use fenced Python code blocks. End with a one-sentence summary."
    ),
}

# ---------------------------------------------------------------------------
# LLM-as-Judge evaluation prompt
# ---------------------------------------------------------------------------
EVAL_SYSTEM = "You are a strict technical writing evaluator. Return ONLY valid JSON."

EVAL_TEMPLATE = (
    "Evaluate the following technical guide on a 1-5 scale for each criterion.\n"
    "Return ONLY a JSON object with these keys:\n"
    "- structure: Does it have clear sections/headers? (1=none, 5=excellent)\n"
    "- detail: Are explanations specific and actionable? (1=vague, 5=very specific)\n"
    "- code_quality: Are code examples present, correct, and useful? (1=none/poor, 5=excellent)\n"
    "- completeness: Does it cover the topic adequately? (1=minimal, 5=comprehensive)\n"
    "- overall: Overall quality (1=poor, 5=excellent)\n\n"
    "Guide to evaluate:\n"
    "---\n"
    "{guide}\n"
    "---\n\n"
    "JSON:"
)


def evaluate_output(text: str, client) -> dict:
    """Use LLM-as-Judge to score a guide."""
    prompt = EVAL_TEMPLATE.format(guide=text[:2000])
    raw = complete(prompt, system=EVAL_SYSTEM, client=client, temperature=0.0)

    # Try to parse JSON from the response
    try:
        # Find the JSON object in the response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass

    return {"structure": 0, "detail": 0, "code_quality": 0, "completeness": 0, "overall": 0}


def run_experiment() -> None:
    print_header("Lab 3 — The Specificity Spectrum")

    client = get_client()
    outputs = {}
    scores = {}

    # --- Generate outputs ---
    for level, prompt in PROMPTS.items():
        print(f"\nGenerating {level} output...")
        print(f"  Prompt: {prompt[:80]}...")
        output = complete(prompt, system=SYSTEM, client=client, temperature=0.3)
        outputs[level] = output
        print(f"  Output length: {len(output)} chars, {len(output.split())} words")

    # --- Evaluate outputs ---
    print_header("LLM-as-Judge Evaluation")
    for level, output in outputs.items():
        print(f"Evaluating {level} output...")
        scores[level] = evaluate_output(output, client)

    # --- Print scores ---
    criteria = ["structure", "detail", "code_quality", "completeness", "overall"]
    headers = ["Criterion", "Vague", "Moderate", "Specific"]
    rows = []
    for c in criteria:
        rows.append([
            c.replace("_", " ").title(),
            str(scores.get("vague", {}).get(c, "?")),
            str(scores.get("moderate", {}).get(c, "?")),
            str(scores.get("specific", {}).get(c, "?")),
        ])
    print_comparison_table(headers, rows)

    # --- Print output previews ---
    for level in ("vague", "moderate", "specific"):
        print_header(f"Output Preview — {level.title()}")
        preview = outputs[level][:500]
        if len(outputs[level]) > 500:
            preview += "\n... [truncated]"
        print(preview)
        print()

    # --- Takeaway ---
    print_header("Takeaway")
    print("More specific prompts consistently produce higher-quality, more")
    print("structured output. The 'specific' prompt constrains word count,")
    print("defines exact sections, names functions, and specifies the audience —")
    print("giving the model clear success criteria to optimize for.")
    print("See Module 2, §2.1 for the Clarity and Specificity principle.\n")


if __name__ == "__main__":
    run_experiment()
