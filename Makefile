# Makefile — Prompt Engineering Playbook
# Common development tasks.  Run `make help` to see all targets.
#
# Prerequisites: Python venv at .venv/ (created by scripts/python/setup.sh)
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
install:        ## Install / refresh docs + dev dependencies
	$(VENV)/pip install -q -r $(REQS_DOCS)
	$(VENV)/pip install -q -r requirements-dev.txt

# ─── Sync ────────────────────────────────────────────────────────────────────

.PHONY: sync
sync:           ## Create docs_src/ symlinks to learn/, prompts/, and top-level docs
	@mkdir -p docs_src
	@ln -sf ../README.md          docs_src/index.md
	@ln -sf ../GETTING-STARTED.md docs_src/GETTING-STARTED.md
	@ln -sf ../CONTRIBUTING.md    docs_src/CONTRIBUTING.md
	@ln -sf ../CHANGELOG.md       docs_src/CHANGELOG.md
	@ln -sf ../references.md      docs_src/references.md
	@ln -sf ../LICENSE            docs_src/LICENSE
	@ln -sf ../learn              docs_src/learn
	@ln -sf ../prompts            docs_src/prompts
	@ln -sf ../docs/assets        docs_src/assets
	@echo "Sync complete (symlinks created)."

.PHONY: sync-check
sync-check:     ## Verify docs_src/ symlinks resolve correctly
	@errors=0; \
	for target in docs_src/index.md docs_src/GETTING-STARTED.md docs_src/CONTRIBUTING.md \
	              docs_src/CHANGELOG.md docs_src/references.md docs_src/LICENSE docs_src/learn docs_src/prompts; do \
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
	for path in learn/learn prompts/prompts docs/assets/assets; do \
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
build: sync     ## Sync docs_src/, then build the MkDocs static site into _site/
	$(MKDOCS) build

.PHONY: serve
serve: sync     ## Sync docs_src/, then start the MkDocs dev server (live-reload)
	$(MKDOCS) serve

# ─── Lint ────────────────────────────────────────────────────────────────────

.PHONY: lint
lint:           ## Run all prompt-file linters (frontmatter + cross-link + required sections)
	./scripts/lint-prompt-frontmatter.sh

.PHONY: validate
validate:       ## Run the full YAML schema validator for prompt files
	$(VENV)/python scripts/validate-prompt-schema.py

# ─── Composite ───────────────────────────────────────────────────────────────

.PHONY: check
check: lint validate sync-check recursive-symlink-check build  ## Run full checks including docs build
	@echo "All checks passed."
