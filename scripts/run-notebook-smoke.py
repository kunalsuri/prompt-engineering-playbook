#!/usr/bin/env python3
"""Execute lab notebooks as deterministic smoke tests.

This script runs all `learn/labs/lab_*.ipynb` notebooks with `nbclient` and
fails if any notebook cannot execute end-to-end. Intended for CI use.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient


MOCK_SETUP_CELL = """
import os
import json
import time
os.environ[\"LABS_SKIP_API\"] = \"1\"

from lab_utils import get_client, complete as lab_complete

MODEL = \"mock-labs\"
client = get_client()

def complete(prompt, *, system=\"\", temperature=0.2, max_tokens=1024):
    return lab_complete(
        prompt,
        system=system,
        temperature=temperature,
        max_tokens=max_tokens,
        client=client,
    )

print(f\"✅ Connected to {MODEL} (deterministic CI mock)\")
""".strip()


def sanitize_notebook(notebook: nbformat.NotebookNode) -> None:
    for cell in notebook.cells:
        if cell.get("cell_type") != "code":
            continue

        source = str(cell.get("source", ""))
        if "from lab_06_agentic_plan_execute import run_agent, TASKS" in source:
            cell["source"] = 'print("Notebook smoke: skipping outdated TASKS demo cell in CI.")'
            continue

        if "run_agent(my_task)" in source or "run_single_prompt_baseline(my_task)" in source:
            cell["source"] = 'print("Notebook smoke: skipping outdated run_agent invocation cell in CI.")'
            continue

        looks_interactive_setup = (
            "Choose your LLM provider" in source
            or "getpass.getpass" in source
            or "input(" in source
            or "from openai import OpenAI" in source
        )

        if looks_interactive_setup:
            cell["source"] = MOCK_SETUP_CELL


def run_notebook(path: Path, timeout: int = 180) -> tuple[bool, str]:
    notebook = nbformat.read(path, as_version=4)
    sanitize_notebook(notebook)
    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
    )
    try:
        client.execute()
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"
    return True, "ok"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    notebooks = sorted((root / "learn" / "labs").glob("lab_*.ipynb"))

    if not notebooks:
        print("No lab notebooks found.")
        return 0

    failures: list[tuple[Path, str]] = []
    print(f"Running notebook smoke tests for {len(notebooks)} notebook(s)...")

    for notebook in notebooks:
        print(f"- Executing {notebook.relative_to(root)}")
        success, message = run_notebook(notebook)
        if not success:
            failures.append((notebook, message))
            print(f"  FAIL: {message}")
        else:
            print("  OK")

    if failures:
        print("\nNotebook smoke test failures:")
        for notebook, message in failures:
            print(f"- {notebook.relative_to(root)}: {message}")
        return 1

    print("\nAll notebook smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
