#!/usr/bin/env bash
# scripts/lint-copilot-instructions.sh
# =====================================
# Validate every prompts/*/copilot-instructions.md file against a minimum
# structural standard.  Four checks per file:
#
#   1. H1 title present              — first non-blank line begins with "# "
#   2. At least 3 H2 sections        — lines that begin with "## "
#   3. Negative-constraint keyword   — at least one of: never / avoid / do not /
#                                      must not / prohibited / do_not (case-insensitive)
#   4. Minimum 300 characters        — guards against near-empty stub files
#
# Exit codes
# ----------
#   0  all files pass
#   1  one or more files fail (details printed to stdout)
#
# Usage
# -----
#   # From repository root:
#   ./scripts/lint-copilot-instructions.sh
#
#   # Or via Make:
#   make lint

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXIT_CODE=0
PASS=0
FAIL=0

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

check_file() {
    local file="$1"
    local errors=0

    # ------------------------------------------------------------------
    # Check 1: H1 title present
    # ------------------------------------------------------------------
    local first_nonblank_line
    first_nonblank_line="$(grep -m1 -E '[^[:space:]]' "$file" || true)"
    if [[ ! "$first_nonblank_line" =~ ^#\  ]]; then
        echo "  FAIL [$file] Missing H1 title (first non-blank line must start with '# ')"
        errors=$((errors + 1))
    fi

    # ------------------------------------------------------------------
    # Check 2: At least 3 H2 sections
    # ------------------------------------------------------------------
    local h2_count
    h2_count=$(grep -cE '^## ' "$file" || true)
    if [ "$h2_count" -lt 3 ]; then
        echo "  FAIL [$file] Too few H2 sections: $h2_count (minimum: 3)"
        errors=$((errors + 1))
    fi

    # ------------------------------------------------------------------
    # Check 3: Negative-constraint keyword
    # ------------------------------------------------------------------
    if ! grep -qiE '\b(never|avoid|do[ _]not|must not|prohibited)\b' "$file"; then
        echo "  FAIL [$file] No negative constraint keyword found (never/avoid/do not/do_not/must not/prohibited)"
        errors=$((errors + 1))
    fi

    # ------------------------------------------------------------------
    # Check 4: Minimum 300 characters
    # ------------------------------------------------------------------
    local char_count
    char_count=$(wc -c < "$file")
    if [ "$char_count" -lt 300 ]; then
        echo "  FAIL [$file] File too short: $char_count chars (minimum: 300)"
        errors=$((errors + 1))
    fi

    if [ "$errors" -eq 0 ]; then
        echo "  PASS [$file]"
        PASS=$((PASS + 1))
    else
        FAIL=$((FAIL + 1))
        EXIT_CODE=1
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "copilot-instructions lint"
echo "========================="

shopt -s nullglob
files=("$REPO_ROOT"/prompts/*/copilot-instructions.md)
shopt -u nullglob

if [ "${#files[@]}" -eq 0 ]; then
    echo "WARNING: No prompts/*/copilot-instructions.md files found."
    exit 0
fi

for file in "${files[@]}"; do
    check_file "$file"
done

echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "PASSED — all ${PASS} copilot-instructions.md file(s) meet the structural standard."
else
    echo "FAILED — $FAIL file(s) have issues, $PASS passed."
fi

exit "$EXIT_CODE"
