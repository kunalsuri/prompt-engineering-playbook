"""Shared pytest fixtures and helpers for the tooling test-suite.

The repository's "test suite" is its set of validation scripts (under
``scripts/``) plus the lab support module (``learn/labs/lab_utils.py``).
These tests exist to prove that machinery actually catches the failures it
claims to — i.e. they test the testers.

Several scripts have hyphenated filenames (``check-citations.py``) that are not
importable with a normal ``import`` statement, so :func:`load_script_module`
loads them by path via importlib.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_script_module(filename: str) -> ModuleType:
    """Import a (possibly hyphen-named) script from scripts/ by file path."""
    path = SCRIPTS_DIR / filename
    module_name = "scriptmod_" + path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def scripts_dir() -> Path:
    return SCRIPTS_DIR
