"""Tests for scripts/check-citations.py.

Proves the citation checker (a) recognises the citation-key grammar, (b) maps
used keys to the files that use them, and (c) FAILS when a key is cited in
learn/ but never defined in references.md.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import load_script_module

cc = load_script_module("check-citations.py")


# --------------------------------------------------------------------------- #
# Key-grammar regexes
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "text,expected",
    [
        ("see [Brown2020] for detail", ["Brown2020"]),
        ("multi [Wei2022] and [OWASP2025]", ["Wei2022", "OWASP2025"]),
        ("disambiguated [Wang2023a]", ["Wang2023a"]),
        ("numeric refs [1] and [web:2] are ignored", []),
        ("generic [TODO] label ignored", []),
    ],
)
def test_cite_pattern_matches_only_real_keys(text, expected):
    assert cc.CITE_PATTERN.findall(text) == expected


def test_defn_pattern_requires_bold_brackets():
    assert cc.DEFN_PATTERN.findall("**[Brown2020]**") == ["Brown2020"]
    # Non-bold occurrences are usages, not definitions.
    assert cc.DEFN_PATTERN.findall("[Brown2020]") == []


# --------------------------------------------------------------------------- #
# Collection helpers
# --------------------------------------------------------------------------- #
def test_collect_defined_keys(tmp_path: Path):
    refs = tmp_path / "references.md"
    refs.write_text("**[Brown2020]** Brown, T. ...\n**[Wei2022]** Wei, J. ...\n", encoding="utf-8")
    assert cc.collect_defined_keys(refs) == frozenset({"Brown2020", "Wei2022"})


def test_collect_used_keys_maps_to_files(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(cc, "REPO_ROOT", tmp_path)  # relative_to() base
    learn = tmp_path / "learn"
    (learn / "sub").mkdir(parents=True)
    (learn / "a.md").write_text("uses [Brown2020]", encoding="utf-8")
    (learn / "sub" / "b.md").write_text("uses [Brown2020] and [Wei2022]", encoding="utf-8")

    used = cc.collect_used_keys(learn)
    assert set(used) == {"Brown2020", "Wei2022"}
    assert len(used["Brown2020"]) == 2  # referenced from two files
    assert len(used["Wei2022"]) == 1


def test_collect_defined_keys_missing_file_exits(tmp_path: Path):
    with pytest.raises(SystemExit) as exc:
        cc.collect_defined_keys(tmp_path / "nope.md")
    assert exc.value.code == 1


# --------------------------------------------------------------------------- #
# End-to-end behaviour via main()
# --------------------------------------------------------------------------- #
def _run_main(monkeypatch, tmp_path: Path, refs_text: str, learn_files: dict[str, str]):
    learn = tmp_path / "learn"
    learn.mkdir()
    for name, body in learn_files.items():
        (learn / name).write_text(body, encoding="utf-8")
    refs = tmp_path / "references.md"
    refs.write_text(refs_text, encoding="utf-8")
    monkeypatch.setattr(cc, "LEARN_DIR", learn)
    monkeypatch.setattr(cc, "REFERENCES_FILE", refs)
    monkeypatch.setattr(cc, "REPO_ROOT", tmp_path)
    return cc.main()


def test_main_passes_when_all_keys_defined(monkeypatch, tmp_path, capsys):
    rc = _run_main(
        monkeypatch, tmp_path,
        refs_text="**[Brown2020]** ...\n",
        learn_files={"m.md": "cites [Brown2020]"},
    )
    assert rc == 0
    assert "PASSED" in capsys.readouterr().out


def test_main_fails_on_undefined_key(monkeypatch, tmp_path, capsys):
    rc = _run_main(
        monkeypatch, tmp_path,
        refs_text="**[Brown2020]** ...\n",
        learn_files={"m.md": "cites [Brown2020] and undefined [Ghost2099]"},
    )
    assert rc == 1
    out = capsys.readouterr().out
    assert "FAILED" in out
    assert "Ghost2099" in out
