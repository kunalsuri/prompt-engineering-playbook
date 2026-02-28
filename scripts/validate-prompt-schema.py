#!/usr/bin/env python3
"""
Validate .prompt.md YAML frontmatter against the prompt registry schema.

This script extracts YAML frontmatter from .prompt.md files and validates
it against prompts/shared/prompt-registry.schema.json.

Usage:
    python scripts/validate-prompt-schema.py [file ...]

    # Validate all prompt files:
    python scripts/validate-prompt-schema.py prompts/**/*.prompt.md

    # Validate a single file:
    python scripts/validate-prompt-schema.py prompts/python/prompts/write-tests.prompt.md

Exit codes:
    0 — all files valid
    1 — one or more files invalid
    2 — script error (missing dependencies, schema not found, etc.)

Dependencies:
    pip install jsonschema pyyaml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install jsonschema pyyaml")
    sys.exit(2)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "prompts" / "shared" / "prompt-registry.schema.json"


def load_schema() -> dict:
    """Load the JSON schema."""
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(2)
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def extract_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter from a .prompt.md file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None

    end = text.index("---", 3)
    yaml_text = text[3:end].strip()

    try:
        return yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as e:
        print(f"  YAML parse error: {e}")
        return None


def validate_file(path: Path, validator: Draft202012Validator) -> list[str]:
    """Validate a single file. Returns list of error messages."""
    errors = []

    frontmatter = extract_frontmatter(path)
    if frontmatter is None:
        errors.append("No valid YAML frontmatter found")
        return errors

    for error in sorted(validator.iter_errors(frontmatter), key=lambda e: list(e.path)):
        field = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"{field}: {error.message}")

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        # Default: find all .prompt.md files
        files = sorted(REPO_ROOT.rglob("*.prompt.md"))
    else:
        files = [Path(arg).resolve() for arg in sys.argv[1:]]

    if not files:
        print("No .prompt.md files found.")
        sys.exit(0)

    schema = load_schema()
    validator = Draft202012Validator(schema)

    total = 0
    passed = 0
    failed = 0

    for path in files:
        if not path.exists():
            print(f"SKIP: {path} (not found)")
            continue

        total += 1
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path

        errors = validate_file(path, validator)

        if errors:
            failed += 1
            print(f"FAIL: {rel}")
            for err in errors:
                print(f"  - {err}")
        else:
            passed += 1
            print(f"OK:   {rel}")

    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed} failed")

    # Note: currently only mode/description/version are required in the schema.
    # Other fields (tags, patterns, etc.) are optional, so existing prompts
    # with only mode/description/version will pass validation.
    # As the team adopts richer metadata, the schema can be tightened.

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
