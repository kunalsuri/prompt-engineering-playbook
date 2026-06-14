#!/usr/bin/env python3
"""
scripts/check-prompt-crosslinks.py
==================================
Verify that the "Learn why this works" cross-link in every ``*.prompt.md`` file
points at a target that actually exists.

The frontmatter linter (``lint-prompt-frontmatter.sh``) only checks that the
cross-link *line* is present.  This script goes one step further and resolves
the link, catching the much more common rot:

  1. The target Markdown file does not exist (path typo, moved file).
  2. The ``#anchor`` fragment does not match any heading in the target file.

Anchor slugs are computed with the GitHub-Flavored-Markdown algorithm
(lowercase, drop punctuation, spaces -> hyphens) so they match the anchors
MkDocs / GitHub generate for headings.

Exit codes
----------
  0  every cross-link resolves (file + anchor)
  1  one or more cross-links are broken (details printed to stdout)

Usage
-----
  # From repository root (stdlib only -- no pip install required):
  python scripts/check-prompt-crosslinks.py

  # Check specific files:
  python scripts/check-prompt-crosslinks.py prompts/python/prompts/write-tests.prompt.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"

# Matches:  > **Learn why this works:** [Label](path/to/file.md#anchor)
CROSSLINK_PATTERN = re.compile(
    r"\*\*Learn why this works:\*\*\s*\[[^\]]*\]\(([^)]+)\)"
)

# Matches ATX headings (# .. ######), capturing the heading text.
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def slugify(heading_text: str) -> str:
    """Replicate the GitHub-Flavored-Markdown heading-anchor algorithm."""
    text = heading_text.strip().lower()
    # Drop everything that is not a word char, space, or hyphen.
    text = re.sub(r"[^\w\s-]", "", text)
    # Collapse whitespace runs into single hyphens.
    text = re.sub(r"\s+", "-", text)
    return text


def heading_anchors(md_path: Path) -> set[str]:
    """Return the set of anchor slugs for all headings in a Markdown file."""
    anchors: set[str] = set()
    for line in md_path.read_text(encoding="utf-8").splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            anchors.add(slugify(match.group(2)))
    return anchors


def extract_crosslink(prompt_path: Path) -> str | None:
    """Return the raw link target (``path#anchor``) of the cross-link, if any."""
    text = prompt_path.read_text(encoding="utf-8")
    match = CROSSLINK_PATTERN.search(text)
    return match.group(1) if match else None


def check_file(prompt_path: Path) -> list[str]:
    """Validate a single prompt file's cross-link. Returns error strings."""
    target = extract_crosslink(prompt_path)
    if target is None:
        # Presence is enforced by lint-prompt-frontmatter.sh; don't double-report.
        return []

    errors: list[str] = []
    path_part, _, anchor = target.partition("#")

    # External links (http/https/mailto) are out of scope for this checker.
    if re.match(r"^[a-z][a-z0-9+.-]*://", path_part) or path_part.startswith("mailto:"):
        return []

    resolved = (prompt_path.parent / path_part).resolve()
    if not resolved.is_file():
        errors.append(
            f"cross-link target file not found: '{path_part}' "
            f"(resolved to {resolved})"
        )
        return errors  # Can't check the anchor if the file is missing.

    if anchor:
        anchors = heading_anchors(resolved)
        if anchor not in anchors:
            errors.append(
                f"cross-link anchor '#{anchor}' not found in {path_part}. "
                f"(file has {len(anchors)} headings)"
            )

    return errors


def main() -> int:
    if len(sys.argv) > 1:
        files = [Path(arg).resolve() for arg in sys.argv[1:]]
    else:
        files = sorted(PROMPTS_DIR.rglob("*.prompt.md"))

    if not files:
        print("No .prompt.md files found.")
        return 0

    total = 0
    failed = 0
    for prompt_path in files:
        if not prompt_path.is_file():
            print(f"SKIP: {prompt_path} (not found)")
            continue
        total += 1
        rel = (
            prompt_path.relative_to(REPO_ROOT)
            if prompt_path.is_relative_to(REPO_ROOT)
            else prompt_path
        )
        errors = check_file(prompt_path)
        if errors:
            failed += 1
            print(f"FAIL: {rel}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK:   {rel}")

    print()
    if failed:
        print(f"crosslink-check FAILED -- {failed}/{total} file(s) have broken cross-links.")
        return 1
    print(f"crosslink-check PASSED -- all {total} cross-link(s) resolve (file + anchor).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
