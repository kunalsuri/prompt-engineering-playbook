#!/usr/bin/env bash
# -------------------------------------------------------
# Setup & serve the MkDocs documentation site locally.
#
# Usage:
#   ./scripts/docs-serve.sh          # build & serve at localhost:8000
#   ./scripts/docs-serve.sh build    # build only (output → _site/)
# -------------------------------------------------------
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# ---------- Create docs_src symlinks ----------
mkdir -p docs_src
for path in learn/learn prompts/prompts assets/assets docs_src/learn/learn docs_src/prompts/prompts docs_src/assets/assets; do
  if [ -L "$path" ]; then rm "$path"; fi
done

link() {
  local src="$1"
  local dst="$2"
  local src_check
  src_check="$(dirname "$dst")/$src"
  if [ ! -e "$src_check" ]; then
    echo "ERROR: Source path not found: $src"
    exit 1
  fi
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    echo "ERROR: Destination exists and is not a symlink: $dst"
    exit 1
  fi
  ln -sfn "$src" "$dst"
}

link ../README.md docs_src/index.md
link ../GETTING-STARTED.md docs_src/GETTING-STARTED.md
link ../CONTRIBUTING.md docs_src/CONTRIBUTING.md
link ../CHANGELOG.md docs_src/CHANGELOG.md
link ../references.md docs_src/references.md
link ../LICENSE docs_src/LICENSE
link ../learn docs_src/learn
link ../prompts docs_src/prompts
link ../assets docs_src/assets

# ---------- Ensure venv + deps ----------
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment…"
  python3 -m venv .venv
fi
source .venv/bin/activate

if ! python -c "import material" 2>/dev/null; then
  echo "Installing MkDocs Material…"
  pip install --quiet -r requirements-docs.txt
fi

# ---------- Build or Serve ----------
if [ "${1:-}" = "build" ]; then
  echo "Building site → _site/"
  mkdocs build --strict --site-dir _site
else
  echo "Serving at http://127.0.0.1:8000  (Ctrl-C to stop)"
  mkdocs serve -a 127.0.0.1:8000
fi
