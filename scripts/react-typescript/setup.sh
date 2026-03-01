#!/usr/bin/env bash
# setup.sh — React + TypeScript stack setup (backward-compatible wrapper).
# Delegates to the unified scripts/setup.sh.
# Usage: ./setup.sh [--force] [target-project-directory]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/../setup.sh" --stack react-typescript "$@"
