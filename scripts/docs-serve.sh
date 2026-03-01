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
ln -sf ../README.md          docs_src/index.md
ln -sf ../GETTING-STARTED.md docs_src/GETTING-STARTED.md
ln -sf ../CONTRIBUTING.md    docs_src/CONTRIBUTING.md
ln -sf ../CHANGELOG.md       docs_src/CHANGELOG.md
ln -sf ../references.md      docs_src/references.md
ln -sf ../LICENSE            docs_src/LICENSE
ln -sf ../learn              docs_src/learn
ln -sf ../prompts            docs_src/prompts
ln -sf ../docs/assets        docs_src/assets

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
  mkdocs build --site-dir _site
else
  echo "Serving at http://127.0.0.1:8000  (Ctrl-C to stop)"
  mkdocs serve -a 127.0.0.1:8000
fi
