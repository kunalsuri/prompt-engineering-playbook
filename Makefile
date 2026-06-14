# Makefile — Prompt Engineering Playbook
# Common development tasks.  Run `make help` to see all targets.
#
# Prerequisites: Python venv at .venv/ (created via standard venv setup)
#   or run: python -m venv .venv && .venv/bin/pip install -r requirements-docs.txt

.DEFAULT_GOAL := help
VENV          := .venv/bin
MKDOCS        := $(VENV)/mkdocs
REQS_DOCS     := requirements-docs.txt

# ─── Help ────────────────────────────────────────────────────────────────────

.PHONY: help
help:           ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

# ─── Install ─────────────────────────────────────────────────────────────────

.PHONY: install
install: venv-check ## Install / refresh docs + dev dependencies
	$(VENV)/pip install -q -r $(REQS_DOCS)
	$(VENV)/pip install -q -r requirements-dev.txt

.PHONY: venv-check
venv-check:     ## Ensure .venv exists before running Python-based repo tasks
	@if [ ! -x "$(VENV)/python" ]; then \
	  echo "ERROR: Missing .venv Python environment."; \
	  echo "Run:"; \
	  echo "  python3 -m venv .venv"; \
	  echo "  source .venv/bin/activate"; \
	  echo "  python -m pip install -r requirements-docs.txt -r requirements-dev.txt"; \
	  exit 1; \
	fi

# ─── Sync ────────────────────────────────────────────────────────────────────

.PHONY: sync
sync:           ## Create docs_src/ symlinks to learn/, prompts/, and top-level docs
	@mkdir -p docs_src
	@for path in learn/learn prompts/prompts assets/assets docs_src/learn/learn docs_src/prompts/prompts docs_src/assets/assets; do \
	  if [ -L "$$path" ]; then rm "$$path"; fi; \
	done
	@set -eu; \
	link() { \
	  src="$$1"; dst="$$2"; \
	  src_check="$$(dirname "$$dst")/$$src"; \
	  if [ ! -e "$$src_check" ]; then \
	    echo "ERROR: Source path not found: $$src"; \
	    exit 1; \
	  fi; \
	  if [ -e "$$dst" ] && [ ! -L "$$dst" ]; then \
	    echo "ERROR: Destination exists and is not a symlink: $$dst"; \
	    exit 1; \
	  fi; \
	  ln -sfn "$$src" "$$dst"; \
	}; \
	link ../README.md docs_src/index.md; \
	link ../GETTING-STARTED.md docs_src/GETTING-STARTED.md; \
	link ../CONTRIBUTING.md docs_src/CONTRIBUTING.md; \
	link ../CHANGELOG.md docs_src/CHANGELOG.md; \
	link ../BETA-RELEASE-NOTES.md docs_src/BETA-RELEASE-NOTES.md; \
	link ../references.md docs_src/references.md; \
	link ../LICENSE docs_src/LICENSE; \
	link ../learn docs_src/learn; \
	link ../prompts docs_src/prompts; \
	link ../assets docs_src/assets
	@echo "Sync complete (symlinks created)."

.PHONY: sync-check
sync-check: sync ## Verify docs_src/ symlinks resolve correctly
	@errors=0; \
	for target in docs_src/index.md docs_src/GETTING-STARTED.md docs_src/CONTRIBUTING.md \
	              docs_src/CHANGELOG.md docs_src/BETA-RELEASE-NOTES.md docs_src/references.md docs_src/LICENSE docs_src/learn docs_src/prompts docs_src/assets; do \
	  if [ ! -e "$$target" ]; then \
	    echo "ERROR: Symlink target does not resolve: $$target"; \
	    errors=$$((errors + 1)); \
	  fi; \
	done; \
	if [ "$$errors" -gt 0 ]; then \
	  echo "FAILED — $$errors broken symlink(s) detected."; \
	  exit 1; \
	fi; \
	echo "PASSED — all docs_src/ symlinks resolve correctly."

.PHONY: recursive-symlink-check
recursive-symlink-check: ## Ensure no recursive/self-referential symlinks exist in tracked content paths
	@errors=0; \
	for path in learn/learn prompts/prompts assets/assets docs_src/learn/learn docs_src/prompts/prompts docs_src/assets/assets; do \
	  if [ -L "$$path" ]; then \
	    echo "ERROR: Recursive symlink detected: $$path -> $$(readlink "$$path")"; \
	    errors=$$((errors + 1)); \
	  fi; \
	done; \
	if [ "$$errors" -gt 0 ]; then \
	  echo "FAILED — $$errors recursive symlink(s) detected."; \
	  exit 1; \
	fi; \
	echo "PASSED — no recursive symlinks detected."

# ─── Build & Serve ───────────────────────────────────────────────────────────

.PHONY: build
build: venv-check sync ## Sync docs_src/, then build the MkDocs static site into _site/
	$(MKDOCS) build --strict

.PHONY: serve
serve: venv-check sync ## Sync docs_src/, then start the MkDocs dev server (live-reload)
	$(MKDOCS) serve

# ─── Lint ────────────────────────────────────────────────────────────────────

.PHONY: lint
lint:           ## Run structural linters (prompt frontmatter + copilot-instructions)
	./scripts/lint-prompt-frontmatter.sh
	./scripts/lint-copilot-instructions.sh

.PHONY: validate
validate: venv-check ## Validate .prompt.md YAML frontmatter against the JSON schema
	$(VENV)/python scripts/validate-prompt-schema.py

.PHONY: citations
citations:      ## Verify every [CitationKey] in learn/ is defined in references.md
	python3 scripts/check-citations.py

.PHONY: crosslinks
crosslinks:     ## Verify every prompt cross-link resolves (target file + heading anchor)
	python3 scripts/check-prompt-crosslinks.py

.PHONY: lab-sync
lab-sync:       ## Verify lab .py/.ipynb pairs stay in sync (imports + prompt constants)
	python3 scripts/check-lab-sync.py

.PHONY: shellcheck
shellcheck:     ## Static-analyse shell scripts (skips with a warning if shellcheck absent)
	@if command -v shellcheck >/dev/null 2>&1; then \
	  shellcheck scripts/*.sh scripts/*/*.sh && echo "shellcheck PASSED."; \
	else \
	  echo "WARNING: shellcheck not installed; skipping. Install it for full coverage."; \
	fi

# ─── Test ────────────────────────────────────────────────────────────────────

.PHONY: test
test: venv-check ## Run the pytest tooling test-suite with coverage
	$(VENV)/python -m pytest --cov --cov-report=term-missing

.PHONY: smoke
smoke: venv-check ## Execute lab notebooks as deterministic smoke tests (no API calls)
	LABS_SKIP_API=1 LLM_MODEL=mock-labs $(VENV)/python scripts/run-notebook-smoke.py

# ─── Composite ───────────────────────────────────────────────────────────────

.PHONY: check
check: venv-check lint validate citations crosslinks lab-sync test sync-check recursive-symlink-check build  ## Run the full check suite (everything except notebook smoke)
	@echo "All checks passed."

.PHONY: check-all
check-all: check smoke ## check + notebook smoke tests (full local/CI parity)
	@echo "All checks (including notebook smoke) passed."
