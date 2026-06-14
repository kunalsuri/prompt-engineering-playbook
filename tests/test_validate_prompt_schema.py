"""Tests for scripts/validate-prompt-schema.py and the JSON schema itself.

Proves the validator rejects frontmatter that violates the registry schema
(bad version string, too-short description, missing required keys, unknown
keys) and accepts well-formed frontmatter.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from conftest import load_script_module

vps = load_script_module("validate-prompt-schema.py")
vps.load_runtime_dependencies()  # populate yaml + Draft202012Validator


@pytest.fixture(scope="module")
def validator():
    schema = vps.load_schema()
    return vps.Draft202012Validator(schema)


VALID_FRONTMATTER = textwrap.dedent(
    """\
    ---
    mode: 'agent'
    description: 'Generate a comprehensive pytest test suite for existing code'
    version: '1.2.3'
    tags: [testing, pytest]
    stack: python
    ---
    # Role
    body
    """
)


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "x.prompt.md"
    p.write_text(body, encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
# Frontmatter extraction
# --------------------------------------------------------------------------- #
def test_extract_frontmatter_ok(tmp_path):
    fm = vps.extract_frontmatter(_write(tmp_path, VALID_FRONTMATTER))
    assert fm["mode"] == "agent"
    assert fm["stack"] == "python"
    assert fm["version"] == "1.2.3"


def test_extract_frontmatter_missing_delimiter(tmp_path, capsys):
    assert vps.extract_frontmatter(_write(tmp_path, "no frontmatter here")) is None


def test_extract_frontmatter_unterminated(tmp_path, capsys):
    body = "---\nmode: 'agent'\n# never closes\n"
    assert vps.extract_frontmatter(_write(tmp_path, body)) is None
    assert "closing delimiter" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# Schema validation: happy path
# --------------------------------------------------------------------------- #
def test_valid_file_has_no_errors(tmp_path, validator):
    assert vps.validate_file(_write(tmp_path, VALID_FRONTMATTER), validator) == []


# --------------------------------------------------------------------------- #
# Schema validation: each rejection path
# --------------------------------------------------------------------------- #
def _frontmatter(**overrides) -> str:
    base = {
        "mode": "'agent'",
        "description": "'A perfectly adequate ten-plus char description'",
        "version": "'1.0.0'",
        "tags": "[testing]",
        "stack": "python",
    }
    base.update(overrides)
    lines = "\n".join(f"{k}: {v}" for k, v in base.items())
    return f"---\n{lines}\n---\n# Role\n"


def test_rejects_bad_version(tmp_path, validator):
    errs = vps.validate_file(_write(tmp_path, _frontmatter(version="'v1.0'")), validator)
    assert any("version" in e for e in errs)


def test_rejects_short_description(tmp_path, validator):
    errs = vps.validate_file(_write(tmp_path, _frontmatter(description="'short'")), validator)
    assert any("description" in e for e in errs)


def test_rejects_invalid_mode(tmp_path, validator):
    errs = vps.validate_file(_write(tmp_path, _frontmatter(mode="'wizard'")), validator)
    assert any("mode" in e for e in errs)


def test_rejects_invalid_stack(tmp_path, validator):
    errs = vps.validate_file(_write(tmp_path, _frontmatter(stack="cobol")), validator)
    assert any("stack" in e for e in errs)


def test_rejects_unknown_key(tmp_path, validator):
    body = _frontmatter(surprise="true")
    errs = vps.validate_file(_write(tmp_path, body), validator)
    assert errs, "additionalProperties:false should reject unknown keys"


def test_reports_missing_required_keys(tmp_path, validator):
    body = "---\nmode: 'agent'\n---\n# Role\n"  # missing description/version/tags/stack
    errs = vps.validate_file(_write(tmp_path, body), validator)
    assert errs
