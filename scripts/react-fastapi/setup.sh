#!/usr/bin/env bash
# setup.sh — Set up the React + FastAPI prompt templates in a target project.
#
# Usage:
#   ./setup.sh /path/to/your-project
#
# This script copies the React + FastAPI copilot-instructions and prompt
# files into the target project's .github/ directory, following the
# VS Code Copilot prompt-file convention.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FASTAPI_DIR="$REPO_ROOT/prompts/react-fastapi"
SHARED_DIR="$REPO_ROOT/prompts/shared"

# --- Argument parsing ---
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-project-directory>"
  echo ""
  echo "Copies React + FastAPI prompt templates into your project's .github/ directory."
  echo ""
  echo "Example:"
  echo "  $0 ~/projects/my-fullstack-app"
  exit 1
fi

TARGET_DIR="$1"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: Target directory does not exist: $TARGET_DIR"
  exit 1
fi

# --- Create directory structure ---
echo "Setting up React + FastAPI prompt templates in: $TARGET_DIR"

mkdir -p "$TARGET_DIR/.github/prompts"
mkdir -p "$TARGET_DIR/.github/instructions"

# --- Copy base instructions ---
echo "  Copying copilot-instructions.md ..."
cp "$FASTAPI_DIR/copilot-instructions.md" "$TARGET_DIR/.github/copilot-instructions.md"

# --- Copy prompt files ---
echo "  Copying prompt files ..."
PROMPT_COUNT=0
for prompt_file in "$FASTAPI_DIR/prompts/"*.prompt.md; do
  if [[ -f "$prompt_file" ]]; then
    cp "$prompt_file" "$TARGET_DIR/.github/prompts/"
    PROMPT_COUNT=$((PROMPT_COUNT + 1))
  fi
done

# --- Copy shared instructions ---
if [[ -f "$SHARED_DIR/codacy.instructions.md" ]]; then
  echo "  Copying shared instructions ..."
  cp "$SHARED_DIR/codacy.instructions.md" "$TARGET_DIR/.github/instructions/"
fi

# --- Summary ---
echo ""
echo "Done! Copied $PROMPT_COUNT prompt files."
echo ""
echo "Directory structure created:"
echo "  $TARGET_DIR/.github/"
echo "  ├── copilot-instructions.md"
echo "  ├── instructions/"
echo "  │   └── codacy.instructions.md"
echo "  └── prompts/"
for prompt_file in "$TARGET_DIR/.github/prompts/"*.prompt.md; do
  if [[ -f "$prompt_file" ]]; then
    echo "      ├── $(basename "$prompt_file")"
  fi
done
echo ""
echo "Next steps:"
echo "  1. Open your project in VS Code."
echo "  2. Customize .github/copilot-instructions.md for your project."
echo "  3. Use /prompt-name in Copilot Chat to invoke prompts."
