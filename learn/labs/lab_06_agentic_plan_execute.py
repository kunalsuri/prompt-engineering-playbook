#!/usr/bin/env python3
"""
Lab 6 — Plan-and-Execute Agent
================================
Module reference: Module 6, §6.2 (Plan-and-Execute Architecture)

This lab implements a minimal plan-and-execute agent from scratch
using only the LLM API and ~80 lines of logic:

  1. PLAN: given a research goal, generate a numbered plan (3–5 steps)
  2. EXECUTE: run each step individually, accumulating results
  3. SYNTHESIZE: combine all step outputs into a final answer
  4. (Optional) RE-PLAN: after each step, decide whether to adapt the plan

This demonstrates the core separation-of-concerns insight from Module 6:
planning (what to do) and execution (doing it) are separate LLM calls.

Usage:
    python lab_06_agentic_plan_execute.py

Note:
    This lab uses the LLM's parametric knowledge for "execution" steps
    (since labs run without web access). In real agentic systems, you
    would replace the executor LLM call with actual tool invocations
    (web search, code execution, database queries, etc.).
"""

from __future__ import annotations

import re

from lab_utils import complete, get_client, print_header

# ---------------------------------------------------------------------------
# Research goals to plan-and-execute against
# ---------------------------------------------------------------------------
RESEARCH_GOALS = [
    "Summarize the key differences between supervised, unsupervised, and "
    "reinforcement learning for a software engineer who is new to ML.",

    "Explain three practical use cases for RAG (retrieval-augmented generation) "
    "in enterprise software, with a concrete example for each.",
]

# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------
PLANNER_SYSTEM = (
    "You are a planning agent. Given a research goal, produce a numbered plan "
    "of 3–5 concrete, answerable steps. Each step must:\n"
    "  • Start with an action verb (Explain, Compare, Describe, List, Define)\n"
    "  • Be independently answerable in 1–2 paragraphs\n"
    "  • Produce a verifiable piece of information\n"
    "Format: return ONLY the numbered list, one step per line. No preamble."
)

PLANNER_TEMPLATE = "Research goal: {goal}\n\nPlan:"

EXECUTOR_SYSTEM = (
    "You are an execution agent. You will be given one specific step from a "
    "research plan. Answer it thoroughly in 2–4 paragraphs. Be concrete and "
    "specific. Focus exclusively on the step — do not attempt other steps."
)

EXECUTOR_TEMPLATE = (
    "Overall research goal (for context): {goal}\n\n"
    "Your assigned step: {step}\n\n"
    "Execute this step:"
)

SYNTHESIZER_SYSTEM = (
    "You are a synthesis agent. You will receive a research goal and the results "
    "of several execution steps. Combine them into a single, coherent, well-structured "
    "response that directly answers the research goal. Eliminate redundancy. "
    "Use headers if the response benefits from structure. Target 400–600 words."
)

SYNTHESIZER_TEMPLATE = (
    "Research goal: {goal}\n\n"
    "Step results:\n{step_results}\n\n"
    "Synthesized answer:"
)

# ---------------------------------------------------------------------------
# Agent components
# ---------------------------------------------------------------------------
def plan(goal: str, client: object) -> list[str]:
    """Call the planner LLM and return a list of step strings."""
    prompt = PLANNER_TEMPLATE.format(goal=goal)
    raw_plan = complete(prompt, system=PLANNER_SYSTEM, client=client, temperature=0.2)

    steps = []
    for line in raw_plan.strip().splitlines():
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith("-")):
            # Strip leading numbering (e.g., "1.", "1)", "- ")
            cleaned = re.sub(r"^[\d\.\)\-\s]+", "", line).strip()
            if cleaned:
                steps.append(cleaned)
    return steps


def execute_step(goal: str, step: str, client: object) -> str:
    """Execute a single step and return the result text."""
    prompt = EXECUTOR_TEMPLATE.format(goal=goal, step=step)
    return complete(prompt, system=EXECUTOR_SYSTEM, client=client, temperature=0.3, max_tokens=512)


def synthesize(goal: str, step_results: list[tuple[str, str]], client: object) -> str:
    """Synthesize all step results into a final answer."""
    formatted_results = "\n\n".join(
        f"Step {i + 1}: {step}\nResult: {result}"
        for i, (step, result) in enumerate(step_results)
    )
    prompt = SYNTHESIZER_TEMPLATE.format(goal=goal, step_results=formatted_results)
    return complete(
        prompt, system=SYNTHESIZER_SYSTEM, client=client, temperature=0.2, max_tokens=1024
    )


# ---------------------------------------------------------------------------
# Full agent loop
# ---------------------------------------------------------------------------
def run_agent(goal: str, client: object) -> None:
    """Run the full plan-and-execute loop for a single goal."""
    separator = "─" * 60

    print(f"\n{separator}")
    print(f"GOAL: {goal}")
    print(separator)

    # Step 1: Plan
    print("\n[1/3] Planning...")
    steps = plan(goal, client)
    print(f"Generated {len(steps)}-step plan:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

    # Step 2: Execute each step
    print(f"\n[2/3] Executing {len(steps)} steps...")
    step_results: list[tuple[str, str]] = []
    for i, step in enumerate(steps, 1):
        print(f"  Executing step {i}/{len(steps)}: {step[:60]}...")
        result = execute_step(goal, step, client)
        step_results.append((step, result))
        # Show first 100 chars of each result for visibility
        preview = result.replace("\n", " ")[:100]
        print(f"    → {preview}...")

    # Step 3: Synthesize
    print("\n[3/3] Synthesizing final answer...")
    final_answer = synthesize(goal, step_results, client)

    print(f"\n{'=' * 60}")
    print("FINAL ANSWER:")
    print("=" * 60)
    print(final_answer)
    print("=" * 60)

    # Report LLM call count
    total_calls = 1 + len(steps) + 1  # planner + executors + synthesizer
    print(f"\nAgent used {total_calls} LLM calls: 1 planner + {len(steps)} executors + 1 synthesizer")
    print(
        "Compare to a single-prompt approach: the plan-and-execute agent produces\n"
        "more consistent, reviewable intermediate results at the cost of latency.\n"
    )


# ---------------------------------------------------------------------------
# Main experiment: compare single-prompt vs. plan-and-execute
# ---------------------------------------------------------------------------
def run_single_prompt_baseline(goal: str, client: object) -> str:
    """Baseline: attempt the same goal in a single LLM call."""
    return complete(
        goal,
        system="You are a knowledgeable research assistant. Answer the following question thoroughly.",
        client=client,
        temperature=0.3,
        max_tokens=1024,
    )


def run_experiment() -> None:
    print_header("Lab 6 — Plan-and-Execute Agent")
    client = get_client()

    for goal in RESEARCH_GOALS:
        # Baseline: single-prompt
        print(f"\n{'─' * 60}")
        print(f"BASELINE (single prompt): {goal[:60]}...")
        baseline = run_single_prompt_baseline(goal, client)
        baseline_lines = baseline.count("\n") + 1
        baseline_words = len(baseline.split())
        print(f"  → {baseline_words} words, {baseline_lines} lines (1 LLM call)")

        # Agent: plan-and-execute
        run_agent(goal, client)

    print("\nTakeaway:")
    print("  • Plan-and-execute produces modular, debuggable intermediate outputs")
    print("  • Each step can be inspected and improved independently")
    print("  • The synthesizer step allows the final answer to be restructured")
    print("    without re-running the expensive execution steps")
    print("  • Cost: N+2 LLM calls instead of 1; useful when task requires depth")
    print("\nSee Module 6 §6.2 for the full plan-and-execute design pattern.\n")


if __name__ == "__main__":
    run_experiment()
