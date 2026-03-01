#!/usr/bin/env bash
# setup.sh — Unified installer for prompt-engineering-playbook templates.
#
# Copies copilot-instructions and prompt files for a chosen technology stack
# into a target project's .github/ directory, following the VS Code Copilot
# prompt-file convention.
#
# Usage:
#   ./setup.sh --stack <stack> [options] [target-project-directory]
#
# Run ./setup.sh --help for full details.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SHARED_DIR="$REPO_ROOT/prompts/shared"

# ── Available stacks ────────────────────────────────────────────────────────

VALID_STACKS=(python react-typescript react-fastapi nodejs-typescript)

stack_label() {
  case "$1" in
    python)              echo "Python" ;;
    react-typescript)    echo "React + TypeScript" ;;
    react-fastapi)       echo "React + FastAPI" ;;
    nodejs-typescript)   echo "Node.js + TypeScript" ;;
    *)                   echo "$1" ;;
  esac
}

# ── Defaults ────────────────────────────────────────────────────────────────

STACK=""
FORCE=false
DRY_RUN=false
LIST=false

# ── Functions ───────────────────────────────────────────────────────────────

usage() {
  cat <<EOF
Usage: $0 --stack <stack> [options] [target-project-directory]

Copies prompt templates for the chosen stack into your project's .github/
directory. If no target directory is given, defaults to the current directory.

Required:
  --stack <stack>   Technology stack to install. One of:
                      python, react-typescript, react-fastapi, nodejs-typescript

Options:
  --force           Overwrite existing files without prompting.
  --dry-run         Show what would be copied without writing anything.
  --list            List available stacks and exit.
  --help            Show this help message and exit.

Examples:
  $0 --stack python ~/projects/my-python-app
  $0 --stack react-typescript --force .
  $0 --stack nodejs-typescript --dry-run
  $0 --list
EOF
}

list_stacks() {
  echo "Available stacks:"
  for s in "${VALID_STACKS[@]}"; do
    local dir="$REPO_ROOT/prompts/$s"
    local count=0
    if [[ -d "$dir/prompts" ]]; then
      count=$(find "$dir/prompts" -maxdepth 1 -name '*.prompt.md' 2>/dev/null | wc -l | tr -d ' ')
    fi
    printf "  %-22s  %s prompt(s)\n" "$s" "$count"
  done
}

is_valid_stack() {
  local needle="$1"
  for s in "${VALID_STACKS[@]}"; do
    [[ "$s" == "$needle" ]] && return 0
  done
  return 1
}

copy_or_skip() {
  local src="$1" dest="$2" label="$3"
  if [[ "$DRY_RUN" == true ]]; then
    echo "  [DRY-RUN] Would copy: $label"
    return 0
  fi
  if [[ -f "$dest" ]] && [[ "$FORCE" != true ]]; then
    echo "  SKIP: $label already exists (use --force to overwrite)"
    return 1
  fi
  cp "$src" "$dest"
  echo "  Copied: $label"
  return 0
}

# ── Argument parsing ────────────────────────────────────────────────────────

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --stack)
      STACK="$2"; shift 2 ;;
    --stack=*)
      STACK="${1#*=}"; shift ;;
    --force)
      FORCE=true; shift ;;
    --dry-run)
      DRY_RUN=true; shift ;;
    --list)
      LIST=true; shift ;;
    --help|-h)
      usage; exit 0 ;;
    -*)
      echo "Error: Unknown option: $1" >&2
      echo "Run '$0 --help' for usage." >&2
      exit 1 ;;
    *)
      POSITIONAL_ARGS+=("$1"); shift ;;
  esac
done

# Handle --list early
if [[ "$LIST" == true ]]; then
  list_stacks
  exit 0
fi

# Validate --stack
if [[ -z "$STACK" ]]; then
  echo "Error: --stack is required." >&2
  echo "" >&2
  echo "Available stacks: ${VALID_STACKS[*]}" >&2
  echo "Run '$0 --help' for usage." >&2
  exit 1
fi

if ! is_valid_stack "$STACK"; then
  echo "Error: Unknown stack '$STACK'." >&2
  echo "Available stacks: ${VALID_STACKS[*]}" >&2
  exit 1
fi

# Target directory
TARGET_DIR="${POSITIONAL_ARGS[0]:-$PWD}"
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: Target directory does not exist: $TARGET_DIR" >&2
  exit 1
fi

# ── Stack directory ─────────────────────────────────────────────────────────

STACK_DIR="$REPO_ROOT/prompts/$STACK"
STACK_LABEL="$(stack_label "$STACK")"

if [[ ! -d "$STACK_DIR" ]]; then
  echo "Error: Stack directory not found: $STACK_DIR" >&2
  exit 1
fi

# ── Execute ─────────────────────────────────────────────────────────────────

echo "Setting up $STACK_LABEL prompt templates in: $TARGET_DIR"

if [[ "$DRY_RUN" == true ]]; then
  echo "  (dry-run mode — no files will be written)"
fi

# Create directory structure
if [[ "$DRY_RUN" != true ]]; then
  mkdir -p "$TARGET_DIR/.github/prompts"
fi

# Copy base instructions
copy_or_skip \
  "$STACK_DIR/copilot-instructions.md" \
  "$TARGET_DIR/.github/copilot-instructions.md" \
  "copilot-instructions.md" || true

# Copy prompt files
PROMPT_COUNT=0
for prompt_file in "$STACK_DIR/prompts/"*.prompt.md; do
  if [[ -f "$prompt_file" ]]; then
    basename_file="$(basename "$prompt_file")"
    if copy_or_skip "$prompt_file" "$TARGET_DIR/.github/prompts/$basename_file" "$basename_file"; then
      PROMPT_COUNT=$((PROMPT_COUNT + 1))
    fi
  fi
done

if [[ $PROMPT_COUNT -eq 0 ]]; then
  echo "WARNING: No prompt files were copied. Source directory may be empty or all files already exist."
fi

# ── Summary ─────────────────────────────────────────────────────────────────

echo ""
if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run complete. $PROMPT_COUNT prompt file(s) would be copied."
else
  echo "Done! Copied $PROMPT_COUNT prompt file(s)."
  echo ""
  echo "Directory structure created:"
  echo "  $TARGET_DIR/.github/"
  echo "  ├── copilot-instructions.md"
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
fi
