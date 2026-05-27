#!/usr/bin/env python3
"""
scripts/check-citations.py
==========================
Verify that every citation key used in ``learn/`` Markdown files is defined
in ``references.md``.

Citation key format: ``[AuthorYear]`` or ``[AuthorYeara]``
  - Starts with one uppercase letter
  - Followed by one or more alphanumeric characters
  - Ends with 4 digits and an optional lowercase suffix
  - Examples: ``[Brown2020]``, ``[Wei2022]``, ``[OWASP2025]``, ``[Wang2023a]``

Keys defined in ``references.md`` are expected in the form ``**[KeyName]**``
(bold, as used throughout the playbook bibliography).

Exit codes
----------
  0  all cited keys are defined in references.md
  1  one or more keys are missing (details printed to stdout)

Usage
-----
  # From repository root (requires only stdlib -- no pip install):
  python scripts/check-citations.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
LEARN_DIR = REPO_ROOT / "learn"
REFERENCES_FILE = REPO_ROOT / "references.md"

# Pattern that matches citation keys used in prose: [Brown2020], [OWASP2025], etc.
# Deliberately excludes plain numbers ([1]), old web-index refs ([web:2]),
# and generic labels ([TODO]).
CITE_PATTERN = re.compile(r"\[([A-Z][A-Za-z0-9]+\d{4}[a-z]?)\]")

# Pattern that matches citation key *definitions* in references.md: **[Brown2020]**
DEFN_PATTERN = re.compile(r"\*\*\[([A-Z][A-Za-z0-9]+\d{4}[a-z]?)\]\*\*")

# Markdown files to skip inside learn/ (e.g., generated artefacts, examples
# that intentionally use fictitious keys for illustration).
SKIP_FILES: frozenset[str] = frozenset()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def collect_defined_keys(references_path: Path) -> frozenset[str]:
    """Extract all citation keys defined in references.md."""
    if not references_path.exists():
        print(f"ERROR: {references_path} not found.")
        sys.exit(1)
    text = references_path.read_text(encoding="utf-8")
    return frozenset(DEFN_PATTERN.findall(text))


def collect_used_keys(learn_dir: Path) -> dict[str, set[str]]:
    """
    Walk learn/ and collect every citation key used across all .md files.

    Returns a mapping of {key: set_of_file_paths_that_use_it}.
    """
    used: dict[str, set[str]] = {}
    for md_file in sorted(learn_dir.rglob("*.md")):
        if md_file.name in SKIP_FILES:
            continue
        text = md_file.read_text(encoding="utf-8")
        for key in CITE_PATTERN.findall(text):
            used.setdefault(key, set()).add(str(md_file.relative_to(REPO_ROOT)))
    return used


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    defined_keys = collect_defined_keys(REFERENCES_FILE)
    used_keys = collect_used_keys(LEARN_DIR)

    missing: dict[str, set[str]] = {
        key: files
        for key, files in used_keys.items()
        if key not in defined_keys
    }

    if missing:
        print(f"citation-check FAILED -- {len(missing)} undefined key(s) found:\n")
        for key in sorted(missing):
            files = sorted(missing[key])
            print(f"  FAIL: [{key}] is used but not defined in references.md")
            for f in files:
                print(f"        used in: {f}")
        print()
        print("Fix: add the missing entry to references.md using APA 7th edition format")
        print("and the key pattern  **[AuthorYear]**  (bold brackets).")
        return 1

    print(
        f"citation-check PASSED -- {len(used_keys)} key(s) in learn/ all defined "
        f"in references.md ({len(defined_keys)} keys available)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
