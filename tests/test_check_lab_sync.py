"""Tests for scripts/check-lab-sync.py.

Proves the .py/.ipynb parity checker (a) extracts top-level names and string
constants via AST, (b) resolves notebook imports, and (c) FAILS on the two
drift conditions it exists to catch: a notebook importing a missing name, and a
prompt constant that differs between the .py and the notebook.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import load_script_module

cls = load_script_module("check-lab-sync.py")

LONG = "x" * cls.MIN_CONSTANT_LEN  # long enough to be considered a real constant


# --------------------------------------------------------------------------- #
# Pure AST helpers
# --------------------------------------------------------------------------- #
def test_py_top_level_names(tmp_path: Path):
    py = tmp_path / "m.py"
    py.write_text(
        "import os\n"
        "FOO = 1\n"
        "BAR: int = 2\n"
        "def fn():\n    inner = 3\n"
        "class C:\n    pass\n",
        encoding="utf-8",
    )
    names = cls.py_top_level_names(py)
    assert {"FOO", "BAR", "fn", "C"} <= names
    assert "inner" not in names  # nested names are not top-level


def test_string_constants_filters_by_length():
    src = f"BIG = '{LONG}'\nSMALL = 'short'\nnotupper = '{LONG}'\n"
    consts = cls._string_constants_from_source(src)
    assert "BIG" in consts
    assert "SMALL" not in consts       # under MIN_CONSTANT_LEN
    assert "notupper" not in consts    # not UPPERCASE


def test_string_constants_normalises_implicit_concat():
    a = f"T = ('{LONG}'\n     'tail')\n"
    b = f"T = '{LONG}tail'\n"
    assert cls._string_constants_from_source(a) == cls._string_constants_from_source(b)


def _nb(*code_cells: str) -> dict:
    cells = [{"cell_type": "code", "source": c} for c in code_cells]
    cells.append({"cell_type": "markdown", "source": "ignored"})
    return {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}


def test_find_notebook_imports(tmp_path: Path):
    cells = ["from lab_99_demo import FOO, bar, BAZ\n", "x = 1\n"]
    assert cls.find_notebook_imports(cells, "lab_99_demo") == ["FOO", "bar", "BAZ"]


def test_nb_string_constants_skips_magic_lines(tmp_path: Path):
    nb = tmp_path / "n.ipynb"
    nb.write_text(json.dumps(_nb(f"%pip install x\nTPL = '{LONG}'\n")), encoding="utf-8")
    consts = cls.nb_string_constants(nb)
    assert consts.get("TPL") == LONG


# --------------------------------------------------------------------------- #
# check_lab() end-to-end against synthetic fixtures
# --------------------------------------------------------------------------- #
def _make_lab(labs_dir: Path, name: str, py_src: str, nb_cells: list[str]) -> None:
    (labs_dir / f"{name}.py").write_text(py_src, encoding="utf-8")
    (labs_dir / f"{name}.ipynb").write_text(json.dumps(_nb(*nb_cells)), encoding="utf-8")


def test_check_lab_passes_when_in_sync(tmp_path, monkeypatch):
    monkeypatch.setattr(cls, "LABS_DIR", tmp_path)
    _make_lab(
        tmp_path, "lab_01_demo",
        py_src=f"PROMPT = '{LONG}'\n",
        nb_cells=[f"PROMPT = '{LONG}'\n"],
    )
    assert cls.check_lab("lab_01_demo") == []


def test_check_lab_flags_missing_import(tmp_path, monkeypatch):
    monkeypatch.setattr(cls, "LABS_DIR", tmp_path)
    _make_lab(
        tmp_path, "lab_05_tool_calling",  # thin-wrapper: import check only
        py_src="def run():\n    return 1\n",
        nb_cells=["from lab_05_tool_calling import run, GONE\n"],
    )
    errors = cls.check_lab("lab_05_tool_calling")
    assert any("GONE" in e for e in errors)


def test_check_lab_flags_constant_drift(tmp_path, monkeypatch):
    monkeypatch.setattr(cls, "LABS_DIR", tmp_path)
    _make_lab(
        tmp_path, "lab_02_demo",
        py_src=f"PROMPT = '{LONG}_PYVERSION'\n",
        nb_cells=[f"PROMPT = '{LONG}_NBVERSION'\n"],
    )
    errors = cls.check_lab("lab_02_demo")
    assert any("differs" in e for e in errors)


def test_check_lab_missing_files(tmp_path, monkeypatch):
    monkeypatch.setattr(cls, "LABS_DIR", tmp_path)
    errors = cls.check_lab("lab_01_absent")
    assert errors and "not found" in errors[0]
