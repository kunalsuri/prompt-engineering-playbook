#!/usr/bin/env bash
# lint-prompt-frontmatter.sh
# Validates every .prompt.md file in prompts/ against the mandatory structure:
#   1. YAML frontmatter with fields: mode, description, version
#   2. Learn↔prompts cross-link  ("> **Learn why this works:**")
#   3. Required body sections:    # Role, # Task, # Output Format
#
# Usage:  ./scripts/lint-prompt-frontmatter.sh
# Exit:   0 if all files pass, 1 if any file fails.

set -euo pipefail

REQUIRED_FIELDS=("mode" "description" "version")
REQUIRED_SECTIONS=("# Role" "# Task" "# Output Format")
ERRORS=0
CHECKED=0

while IFS= read -r -d '' file; do
  CHECKED=$((CHECKED + 1))
  FILE_ERRORS=0

  # --- Check that the file starts with "---" (YAML frontmatter delimiter) ---
  first_line=$(head -1 "$file")
  if [[ "$first_line" != "---" ]]; then
    echo "FAIL: $file — missing YAML frontmatter (first line is not '---')"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  # --- Extract frontmatter (lines between the first two "---" lines) ---
  frontmatter=$(awk 'BEGIN{found=0} /^---$/{found++; next} found==1{print} found>=2{exit}' "$file")

  if [[ -z "$frontmatter" ]]; then
    echo "FAIL: $file — empty YAML frontmatter"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  # --- Check each required YAML field exists ---
  for field in "${REQUIRED_FIELDS[@]}"; do
    if ! echo "$frontmatter" | grep -qE "^${field}:"; then
      echo "FAIL: $file — missing required frontmatter field '${field}'"
      ERRORS=$((ERRORS + 1))
      FILE_ERRORS=$((FILE_ERRORS + 1))
    fi
  done

  # --- Check learn↔prompts cross-link ---
  if ! grep -q '> \*\*Learn why this works:\*\*' "$file"; then
    echo "FAIL: $file — missing cross-link (add '> **Learn why this works:** [pattern](../../../learn/...)')"
    ERRORS=$((ERRORS + 1))
    FILE_ERRORS=$((FILE_ERRORS + 1))
  fi

  # --- Check required body sections ---
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -qF "$section" "$file"; then
      echo "FAIL: $file — missing required section '${section}'"
      ERRORS=$((ERRORS + 1))
      FILE_ERRORS=$((FILE_ERRORS + 1))
    fi
  done

  if [[ "$FILE_ERRORS" -eq 0 ]]; then
    echo "OK:   $file"
  fi

done < <(find prompts -name '*.prompt.md' -print0)

echo ""
echo "Checked $CHECKED prompt file(s)."

if [[ $ERRORS -gt 0 ]]; then
  echo "FAILED — $ERRORS error(s) found."
  exit 1
else
  echo "PASSED — all files have required frontmatter, cross-link, and sections."
  exit 0
fi
