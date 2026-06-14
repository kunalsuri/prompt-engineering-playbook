"""Integration tests: run every validator against the *real* repository content
and assert it passes. These guard against content drift (a broken citation, a
desynced lab, a dangling cross-link) and confirm the happy path on real files,
complementing the fixture-based unit tests.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(cmd), cwd=REPO_ROOT, capture_output=True, text=True
    )


@pytest.mark.parametrize(
    "script",
    [
        "scripts/check-citations.py",
        "scripts/check-lab-sync.py",
        "scripts/check-prompt-crosslinks.py",
    ],
)
def test_stdlib_python_checkers_pass(script):
    result = _run(sys.executable, script)
    assert result.returncode == 0, result.stdout + result.stderr


def test_schema_validation_passes():
    result = _run(sys.executable, "scripts/validate-prompt-schema.py")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "script",
    [
        "scripts/lint-prompt-frontmatter.sh",
        "scripts/lint-copilot-instructions.sh",
    ],
)
def test_shell_linters_pass(script):
    result = _run("bash", script)
    assert result.returncode == 0, result.stdout + result.stderr
