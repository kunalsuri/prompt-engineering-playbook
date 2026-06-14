"""Tests for the bash linters (now arg-aware so they can be tested in isolation):
  * scripts/lint-prompt-frontmatter.sh
  * scripts/lint-copilot-instructions.sh

Each test feeds a known-good and a known-bad fixture file and asserts the
exit code, proving the linter actually rejects malformed input rather than
silently passing.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FM_LINTER = REPO_ROOT / "scripts" / "lint-prompt-frontmatter.sh"
COPILOT_LINTER = REPO_ROOT / "scripts" / "lint-copilot-instructions.sh"

GOOD_PROMPT = """\
---
mode: 'agent'
description: 'A good description for testing'
version: '1.0.0'
---

> **Learn why this works:** [Pattern](../../../learn/03-patterns.md#anchor)

# Role
You are a tester.

# Task
Do the thing.

# Output Format
Markdown.
"""

GOOD_COPILOT = """\
# Project Instructions

## Overview
Some overview text that is sufficiently long to clear the 300-character minimum
required by the linter so that this fixture is accepted as a valid file.

## Conventions
Follow the house style. You must never commit secrets.

## Testing
Run the suite before pushing.
"""


def _run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(script), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


# --------------------------------------------------------------------------- #
# Frontmatter linter
# --------------------------------------------------------------------------- #
def test_frontmatter_linter_accepts_good(tmp_path: Path):
    f = tmp_path / "good.prompt.md"
    f.write_text(GOOD_PROMPT, encoding="utf-8")
    result = _run(FM_LINTER, str(f))
    assert result.returncode == 0, result.stdout + result.stderr


def test_frontmatter_linter_rejects_missing_section(tmp_path: Path):
    f = tmp_path / "bad.prompt.md"
    f.write_text(GOOD_PROMPT.replace("# Output Format\nMarkdown.\n", ""), encoding="utf-8")
    result = _run(FM_LINTER, str(f))
    assert result.returncode == 1
    assert "# Output Format" in result.stdout


def test_frontmatter_linter_rejects_missing_crosslink(tmp_path: Path):
    f = tmp_path / "bad.prompt.md"
    body = GOOD_PROMPT.replace(
        "> **Learn why this works:** [Pattern](../../../learn/03-patterns.md#anchor)\n", ""
    )
    f.write_text(body, encoding="utf-8")
    result = _run(FM_LINTER, str(f))
    assert result.returncode == 1
    assert "cross-link" in result.stdout


def test_frontmatter_linter_rejects_missing_field(tmp_path: Path):
    f = tmp_path / "bad.prompt.md"
    f.write_text(GOOD_PROMPT.replace("version: '1.0.0'\n", ""), encoding="utf-8")
    result = _run(FM_LINTER, str(f))
    assert result.returncode == 1
    assert "version" in result.stdout


# --------------------------------------------------------------------------- #
# Copilot-instructions linter
# --------------------------------------------------------------------------- #
def test_copilot_linter_accepts_good(tmp_path: Path):
    f = tmp_path / "copilot-instructions.md"
    f.write_text(GOOD_COPILOT, encoding="utf-8")
    result = _run(COPILOT_LINTER, str(f))
    assert result.returncode == 0, result.stdout + result.stderr


def test_copilot_linter_rejects_too_short(tmp_path: Path):
    f = tmp_path / "copilot-instructions.md"
    f.write_text("# Title\n\n## A\n## B\n## C\nnever\n", encoding="utf-8")
    result = _run(COPILOT_LINTER, str(f))
    assert result.returncode == 1
    assert "too short" in result.stdout.lower()


def test_copilot_linter_rejects_missing_negative_keyword(tmp_path: Path):
    body = GOOD_COPILOT.replace("You must never commit secrets.", "Keep it tidy.")
    f = tmp_path / "copilot-instructions.md"
    f.write_text(body, encoding="utf-8")
    result = _run(COPILOT_LINTER, str(f))
    assert result.returncode == 1
    assert "negative constraint" in result.stdout.lower()


def test_copilot_linter_rejects_too_few_h2(tmp_path: Path):
    body = "# Title\n\n## Only One\n" + ("padding never do not " * 30)
    f = tmp_path / "copilot-instructions.md"
    f.write_text(body, encoding="utf-8")
    result = _run(COPILOT_LINTER, str(f))
    assert result.returncode == 1
    assert "h2 sections" in result.stdout.lower()
