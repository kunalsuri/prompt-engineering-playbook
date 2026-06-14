"""Tests for scripts/run-notebook-smoke.py's notebook sanitizer.

The smoke runner swaps interactive provider-setup cells for a deterministic
mock cell before executing notebooks in CI. If that substitution silently
stopped matching, CI would try to make real API calls (or hang on input()).
These tests pin the detection + replacement behaviour.
"""

from __future__ import annotations

import nbformat

from conftest import load_script_module

rns = load_script_module("run-notebook-smoke.py")


def _nb(*sources: str) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(src) for src in sources]
    return nb


def test_sanitize_replaces_interactive_setup():
    nb = _nb("from openai import OpenAI\nclient = OpenAI()", "print('keep me')")
    rns.sanitize_notebook(nb)
    assert nb.cells[0].source == rns.MOCK_SETUP_CELL
    assert nb.cells[1].source == "print('keep me')"  # untouched


def test_sanitize_matches_getpass_and_prompt():
    nb = _nb("key = getpass.getpass('API key')")
    rns.sanitize_notebook(nb)
    assert nb.cells[0].source == rns.MOCK_SETUP_CELL


def test_sanitize_leaves_plain_cells_alone():
    nb = _nb("x = 1 + 1\nprint(x)")
    rns.sanitize_notebook(nb)
    assert nb.cells[0].source == "x = 1 + 1\nprint(x)"


def test_mock_setup_cell_forces_skip_api():
    # The injected cell must keep the labs in deterministic/offline mode.
    assert 'LABS_SKIP_API' in rns.MOCK_SETUP_CELL
    assert 'mock-labs' in rns.MOCK_SETUP_CELL
