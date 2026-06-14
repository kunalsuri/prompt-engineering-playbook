"""Tests for scripts/check-prompt-crosslinks.py.

Proves the cross-link resolver (a) slugifies headings the GitHub way,
(b) accepts a prompt whose link points at a real file + real anchor, and
(c) FAILS when the target file is missing or the anchor doesn't exist.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import load_script_module

cl = load_script_module("check-prompt-crosslinks.py")


@pytest.mark.parametrize(
    "heading,slug",
    [
        ("3.6 Pattern 5: Constrained Output", "36-pattern-5-constrained-output"),
        ("Chain-of-Thought (CoT)", "chain-of-thought-cot"),
        ("  Trailing space  ", "trailing-space"),
        ("Already-hyphenated", "already-hyphenated"),
    ],
)
def test_slugify_matches_github(heading, slug):
    assert cl.slugify(heading) == slug


def test_heading_anchors(tmp_path: Path):
    md = tmp_path / "doc.md"
    md.write_text("# Title\n\n## 3.6 Pattern 5: Constrained Output\n\ntext\n", encoding="utf-8")
    anchors = cl.heading_anchors(md)
    assert "title" in anchors
    assert "36-pattern-5-constrained-output" in anchors


def _make_prompt(tmp_path: Path, link: str) -> Path:
    p = tmp_path / "x.prompt.md"
    p.write_text(f"> **Learn why this works:** [Why]({link})\n", encoding="utf-8")
    return p


def test_check_file_ok(tmp_path: Path):
    target = tmp_path / "learn" / "03-patterns.md"
    target.parent.mkdir()
    target.write_text("## 3.6 Pattern 5: Constrained Output\n", encoding="utf-8")
    prompt = _make_prompt(tmp_path, "learn/03-patterns.md#36-pattern-5-constrained-output")
    assert cl.check_file(prompt) == []


def test_check_file_missing_target_file(tmp_path: Path):
    prompt = _make_prompt(tmp_path, "learn/nope.md#anchor")
    errors = cl.check_file(prompt)
    assert errors and "not found" in errors[0]


def test_check_file_missing_anchor(tmp_path: Path):
    target = tmp_path / "learn" / "doc.md"
    target.parent.mkdir()
    target.write_text("## Real Heading\n", encoding="utf-8")
    prompt = _make_prompt(tmp_path, "learn/doc.md#ghost-anchor")
    errors = cl.check_file(prompt)
    assert errors and "anchor" in errors[0]


def test_check_file_ignores_external_link(tmp_path: Path):
    prompt = _make_prompt(tmp_path, "https://example.com/page#frag")
    assert cl.check_file(prompt) == []


def test_check_file_no_crosslink_is_ignored(tmp_path: Path):
    # Presence is enforced elsewhere; this checker stays silent.
    p = tmp_path / "x.prompt.md"
    p.write_text("# Role\nno crosslink here\n", encoding="utf-8")
    assert cl.check_file(p) == []
