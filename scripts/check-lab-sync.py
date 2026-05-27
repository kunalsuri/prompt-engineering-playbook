#!/usr/bin/env python3
"""
scripts/check-lab-sync.py
=========================
Verify that lab .ipynb and .py files maintain consistent prompt templates and
module exports.  Two complementary checks:

  1. IMPORT RESOLUTION (all labs)
     Notebook cells that contain ``from lab_XX import NAMES`` are parsed and
     every imported name is verified to exist as a top-level definition in the
     corresponding .py file.  This catches the pattern where a notebook cell
     references a function or variable that has been renamed or removed in the
     .py (e.g. TASKS vs RESEARCH_GOALS in lab 6, which is what triggered this
     script's creation).

  2. PROMPT-CONSTANT PARITY (labs 1-4, self-contained style)
     Labs 1-4 duplicate the experiment logic in both file formats.  This check
     extracts every UPPERCASE string constant (>= MIN_CONSTANT_LEN chars) from
     the .py file and asserts that its value appears with the same content
     somewhere in the notebook's code cells.  Comparison is done by evaluating
     both sides through ast.parse so that escape sequences and implicit string
     concatenation are normalised before comparison.  This catches prompt drift:
     if someone updates a template string in the .py but forgets the notebook
     (or vice-versa), CI fails.

     Labs 5-6 use a thin-wrapper pattern (notebook imports from .py) so the
     parity check is skipped; only import resolution applies.

Exit codes
----------
  0  all checks passed
  1  one or more issues found (details printed to stdout)

Usage
-----
  # From repository root (requires only stdlib -- no pip install):
  python scripts/check-lab-sync.py

  # Also invoked by the lab-sync job in quality-nonmarkdown.yml.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LABS_DIR = Path(__file__).resolve().parent.parent / "learn" / "labs"

ALL_LABS = [
    "lab_01_zero_vs_few_shot",
    "lab_02_chain_of_thought",
    "lab_03_specificity",
    "lab_04_evaluation_pipeline",
    "lab_05_tool_calling",
    "lab_06_agentic_plan_execute",
]

# These labs use a thin-wrapper pattern (notebook imports from .py).
# Prompt-constant parity is not applicable; only import resolution runs.
THIN_WRAPPER_LABS: frozenset[str] = frozenset({
    "lab_05_tool_calling",
    "lab_06_agentic_plan_execute",
})

# Only check string constants whose value is at least this many characters.
# Filters out trivial markers like "JSON:", "Positive", etc.
MIN_CONSTANT_LEN = 30

# ---------------------------------------------------------------------------
# Notebook helpers
# ---------------------------------------------------------------------------


def nb_code_cells(nb_path: Path) -> list[str]:
    """Return the source of every *code* cell in an nbformat-4 notebook."""
    with nb_path.open(encoding="utf-8") as fh:
        nb = json.load(fh)
    cells: list[str] = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        # nbformat stores source as either a list-of-lines or a plain string.
        if isinstance(src, list):
            src = "".join(src)
        cells.append(src)
    return cells


def find_notebook_imports(code_cells: list[str], lab_name: str) -> list[str]:
    """
    Collect every name imported from *lab_name* across all code cells.

    Handles lines of the form::

        from lab_XX_name import FOO, BAR, baz
    """
    pattern = re.compile(
        rf"from\s+{re.escape(lab_name)}\s+import\s+(.+)",
        re.IGNORECASE,
    )
    imported: list[str] = []
    for cell in code_cells:
        for line in cell.splitlines():
            m = pattern.match(line.strip())
            if m:
                for name in m.group(1).split(","):
                    name = name.strip()
                    if name:
                        imported.append(name)
    return imported


# ---------------------------------------------------------------------------
# Python source helpers
# ---------------------------------------------------------------------------


def py_top_level_names(py_path: Path) -> set[str]:
    """
    Return every top-level name defined in the .py file -- functions, classes,
    and simple variable assignments (including annotated assigns).
    """
    with py_path.open(encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                names.add(node.target.id)
    return names


def _string_constants_from_source(src: str) -> dict[str, str]:
    """
    Extract {NAME: value} for UPPERCASE string constants from Python source.

    Python's parser folds implicit string concatenation::

        TEMPLATE = (
            "Part 1\\n"
            "Part 2"
        )

    into a single ast.Constant node before we ever see the AST, so this
    function handles all such patterns without extra logic.
    """
    tree = ast.parse(src)
    constants: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not (isinstance(target, ast.Name) and target.id.isupper()):
                continue
            val_node = node.value
            if (
                isinstance(val_node, ast.Constant)
                and isinstance(val_node.value, str)
                and len(val_node.value) >= MIN_CONSTANT_LEN
            ):
                constants[target.id] = val_node.value
    return constants


def py_string_constants(py_path: Path) -> dict[str, str]:
    """Extract UPPERCASE string constants from a .py file."""
    with py_path.open(encoding="utf-8") as fh:
        return _string_constants_from_source(fh.read())


def nb_string_constants(nb_path: Path) -> dict[str, str]:
    """
    Extract UPPERCASE string constants from all code cells of a notebook.

    Notebook code cells often contain interactive constructs (%pip install,
    input(), display()) that ast.parse cannot handle as a module.  We parse
    each cell independently, ignoring cells that raise SyntaxError, and strip
    IPython magic lines (starting with % or !) before parsing.
    """
    constants: dict[str, str] = {}
    for cell_src in nb_code_cells(nb_path):
        cleaned = "\n".join(
            line
            for line in cell_src.splitlines()
            if not line.lstrip().startswith(("%", "!"))
        )
        try:
            constants.update(_string_constants_from_source(cleaned))
        except SyntaxError:
            pass  # Skip cells whose syntax ast cannot parse
    return constants


# ---------------------------------------------------------------------------
# Per-lab check
# ---------------------------------------------------------------------------


def check_lab(lab: str) -> list[str]:
    """Run all sync checks for one lab; return a list of error strings."""
    py_path = LABS_DIR / f"{lab}.py"
    nb_path = LABS_DIR / f"{lab}.ipynb"
    errors: list[str] = []

    if not py_path.exists():
        return [f"[{lab}] .py file not found at {py_path}"]
    if not nb_path.exists():
        return [f"[{lab}] .ipynb file not found at {nb_path}"]

    cells = nb_code_cells(nb_path)

    # ------------------------------------------------------------------
    # Check 1: import resolution (all labs)
    # ------------------------------------------------------------------
    imported_names = find_notebook_imports(cells, lab)
    if imported_names:
        defined = py_top_level_names(py_path)
        for name in imported_names:
            if name not in defined:
                errors.append(
                    f"[{lab}] notebook imports '{name}' from {py_path.name}, "
                    f"but '{name}' is not defined there. "
                    f"(Defined names: {sorted(defined)[:8]} ...)"
                )

    # ------------------------------------------------------------------
    # Check 2: prompt-constant parity (self-contained labs 1-4 only)
    # ------------------------------------------------------------------
    # We compare evaluated constant *values* (not raw source text) by parsing
    # both files with ast.  This correctly handles implicit string concatenation
    # and escape sequences that differ between source representations:
    # e.g. "Review: \"{review}\"\n" in source == 'Review: "{review}"\n' as value.
    # ------------------------------------------------------------------
    if lab not in THIN_WRAPPER_LABS:
        py_consts = py_string_constants(py_path)
        nb_consts = nb_string_constants(nb_path)

        for name, py_value in py_consts.items():
            if name not in nb_consts:
                excerpt = repr(py_value[:60]) + ("..." if len(py_value) > 60 else "")
                errors.append(
                    f"[{lab}] constant {name!r} ({len(py_value)} chars) is defined "
                    f"in .py but missing from notebook code cells. "
                    f"Value starts: {excerpt}"
                )
            elif nb_consts[name] != py_value:
                py_ex = repr(py_value[:60])
                nb_ex = repr(nb_consts[name][:60])
                errors.append(
                    f"[{lab}] constant {name!r} differs between .py and notebook.\n"
                    f"       .py value:      {py_ex}\n"
                    f"       notebook value: {nb_ex}"
                )

    return errors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    all_errors: list[str] = []

    for lab in ALL_LABS:
        errors = check_lab(lab)
        all_errors.extend(errors)

    if all_errors:
        print(f"lab-sync check FAILED -- {len(all_errors)} issue(s) found:\n")
        for err in all_errors:
            print(f"  FAIL: {err}")
        print()
        return 1

    print(f"lab-sync check PASSED -- all {len(ALL_LABS)} labs verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
