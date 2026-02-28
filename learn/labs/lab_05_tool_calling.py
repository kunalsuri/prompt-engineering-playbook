#!/usr/bin/env python3
"""
Lab 5 — Tool-Calling & Structured Output
==========================================
Module reference: Module 3, §3.6 (Constrained Output) and Module 5, §5.4

This lab compares two strategies for getting reliably structured JSON output:

  1. JSON-Mode Prompting: instruct the model in natural language to emit JSON,
     then validate the result with json.loads().

  2. Function-Calling (Tool-Calling): define a typed function schema and let
     the model fill its arguments — the API enforces structural validity.

It runs both strategies on five product description extraction tasks and
reports: valid-JSON rate, field-completeness rate, and consistency across runs.

Usage:
    python lab_05_tool_calling.py

Requirements:
    OpenAI-compatible API (Google Gemini, Groq, OpenAI — see labs/README.md)
    For function-calling, OpenAI or Gemini with function declarations recommended.
    Groq supports tool-calling on mixtral/llama3 models.
"""

from __future__ import annotations

import json
from typing import Any

from lab_utils import complete, get_client, print_comparison_table, print_header

# ---------------------------------------------------------------------------
# Test data: unstructured product descriptions to extract from
# ---------------------------------------------------------------------------
PRODUCT_DESCRIPTIONS = [
    "Apple iPhone 16 Pro - 256GB - Black Titanium. Price: $999. "
    "Display: 6.3-inch Super Retina XDR. Camera: 48MP main + 12MP ultra-wide. Battery: up to 27h video playback.",

    "Sony WH-1000XM6 Wireless Headphones. $349.99. "
    "Industry-leading noise cancellation. 30-hour battery life. Bluetooth 5.3. Colors: Black, Silver, Midnight Blue.",

    "LEGO Technic Bugatti Chiron #42083 - $449.99. "
    "3599 pieces. Ages 16+. Dimensions when built: 56cm x 25cm x 14cm. "
    "Features working 8-speed gearbox and aerodynamic rear spoiler.",

    "Kindle Paperwhite Signature Edition - 32GB. $189.99. "
    "6.8-inch glare-free display, 300 ppi. Adjustable warm light. USB-C charging. "
    "Waterproof (IPX8). Up to 12 weeks battery life.",

    "Dyson V15 Detect Absolute Cordless Vacuum. Price: $749.99. "
    "Suction: 240 AW. Run time: up to 60 minutes. Weight: 3.1 kg. "
    "Includes laser dust detect, HEPA filtration, and 7 attachments.",
]

# Expected fields in extracted output
REQUIRED_FIELDS = ["name", "price_usd", "category", "key_specs"]

# ---------------------------------------------------------------------------
# Strategy 1: JSON-Mode Prompting
# ---------------------------------------------------------------------------
JSON_MODE_SYSTEM = (
    "You are a product data extraction assistant. "
    "You respond ONLY with valid JSON objects. No prose, no markdown, no code fences."
)

JSON_MODE_TEMPLATE = (
    "Extract product information from the following description and return a JSON object "
    "with exactly these fields:\n"
    '  "name": string — full product name including model/variant\n'
    '  "price_usd": number — price as a float (no currency symbols)\n'
    '  "category": string — one of: Electronics, Toys, Books, Appliances, Other\n'
    '  "key_specs": array of strings — 2-4 bullet-point specifications\n\n'
    "Return ONLY the JSON object. No explanation.\n\n"
    "Product description:\n{description}"
)

RUNS_PER_VARIANT = 3


def run_json_mode(description: str, client: Any) -> list[dict]:
    """Run JSON-mode prompting and return list of parsed results."""
    results = []
    prompt = JSON_MODE_TEMPLATE.format(description=description)
    for _ in range(RUNS_PER_VARIANT):
        raw = complete(prompt, system=JSON_MODE_SYSTEM, client=client, temperature=0.1)
        try:
            # Strip markdown fences if model wraps output despite instructions
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1])
            parsed = json.loads(cleaned)
            results.append({"success": True, "data": parsed, "raw": raw[:80]})
        except json.JSONDecodeError as e:
            results.append({"success": False, "error": str(e), "raw": raw[:80]})
    return results


# ---------------------------------------------------------------------------
# Strategy 2: Function-Calling / Tool-Calling
# ---------------------------------------------------------------------------
PRODUCT_TOOL = {
    "type": "function",
    "function": {
        "name": "extract_product",
        "description": "Extract structured product information from a description.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full product name including model/variant",
                },
                "price_usd": {
                    "type": "number",
                    "description": "Price in USD as a float",
                },
                "category": {
                    "type": "string",
                    "enum": ["Electronics", "Toys", "Books", "Appliances", "Other"],
                    "description": "Product category",
                },
                "key_specs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "2-4 key specifications",
                },
            },
            "required": ["name", "price_usd", "category", "key_specs"],
        },
    },
}


def run_tool_calling(description: str, client: Any) -> list[dict]:
    """Run function-calling and return list of parsed results."""
    results = []
    for _ in range(RUNS_PER_VARIANT):
        try:
            response = client.chat.completions.create(
                model=client._default_model if hasattr(client, "_default_model") else "gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a product data extraction assistant.",
                    },
                    {
                        "role": "user",
                        "content": f"Extract product information:\n\n{description}",
                    },
                ],
                tools=[PRODUCT_TOOL],
                tool_choice={"type": "function", "function": {"name": "extract_product"}},
                temperature=0.1,
            )
            tool_call = response.choices[0].message.tool_calls
            if tool_call:
                args_str = tool_call[0].function.arguments
                parsed = json.loads(args_str)
                results.append({"success": True, "data": parsed, "raw": args_str[:80]})
            else:
                results.append({"success": False, "error": "No tool call returned", "raw": ""})
        except Exception as exc:
            # Fallback: provider may not support tool-calling (e.g., some Groq models)
            results.append({"success": False, "error": f"API error: {exc}", "raw": ""})
    return results


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------
def check_completeness(data: dict) -> tuple[int, list[str]]:
    """Return (present_field_count, missing_fields) for REQUIRED_FIELDS."""
    present = [f for f in REQUIRED_FIELDS if f in data and data[f] is not None]
    missing = [f for f in REQUIRED_FIELDS if f not in present]
    return len(present), missing


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
def run_experiment() -> None:
    print_header("Lab 5 — Tool-Calling & Structured Output")
    client = get_client()

    # Attach default model name so tool-calling can use it
    from lab_utils import DEFAULT_MODEL
    client._default_model = DEFAULT_MODEL  # type: ignore[attr-defined]

    summary_rows: list[list[str]] = []

    for i, description in enumerate(PRODUCT_DESCRIPTIONS, start=1):
        short_name = description[:40] + "..."
        print(f"\n[Product {i}] {short_name}")

        json_results = run_json_mode(description, client)
        tool_results = run_tool_calling(description, client)

        def summarize(results: list[dict]) -> tuple[int, float, float]:
            valid_count = sum(1 for r in results if r["success"])
            valid_rate = valid_count / len(results)
            completeness_scores = []
            for r in results:
                if r["success"]:
                    score, _ = check_completeness(r["data"])
                    completeness_scores.append(score / len(REQUIRED_FIELDS))
            avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.0
            return valid_count, valid_rate, avg_completeness

        jm_valid, jm_rate, jm_comp = summarize(json_results)
        tc_valid, tc_rate, tc_comp = summarize(tool_results)

        summary_rows.append([
            f"Product {i}",
            f"{jm_valid}/{len(json_results)} ({jm_rate:.0%})",
            f"{jm_comp:.0%}",
            f"{tc_valid}/{len(tool_results)} ({tc_rate:.0%})",
            f"{tc_comp:.0%}",
        ])

        # Show detail for first product only
        if i == 1:
            print("\n  JSON-Mode sample output:")
            for r in json_results:
                status = "✓ valid" if r["success"] else "✗ invalid"
                print(f"    Run: {status} — {r['raw']}")
            print("\n  Tool-Calling sample output:")
            for r in tool_results:
                status = "✓ valid" if r["success"] else f"✗ {r.get('error', 'failed')}"
                print(f"    Run: {status} — {r.get('raw', '')}")

    # Print overall comparison table
    print_header("Summary Comparison")
    headers = ["Product", "JSON-Mode\nValid", "JSON-Mode\nFields", "Tool-Call\nValid", "Tool-Call\nFields"]
    print_comparison_table(headers, summary_rows, col_widths=[12, 16, 14, 16, 14])

    print("Key Observations:")
    print("  • Tool-calling enforces schema at the API level — valid-JSON rate should be 100%")
    print("    when the provider supports it (vs. JSON-mode which relies on model compliance).")
    print("  • JSON-mode is more portable (works with any OpenAI-compatible API).")
    print("  • For production use: prefer tool-calling when available; fall back to JSON-mode")
    print("    with strict output instructions and postprocessing validation.")
    print("  • See Module 3 §3.6 (Constrained Output) and Module 5 §5.4 for deeper analysis.\n")


if __name__ == "__main__":
    run_experiment()
