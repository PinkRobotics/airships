# The whole contributor interface. `make` on its own prints it.
#
# Nothing here needs node except `test-node`. This repository is developed on a machine that
# has none, and an interface that only works on the maintainer's box is not an interface.
# Python 3 and a Chromium are the entire toolchain; CI adds node and runs the rest as-is.

PY     ?= python3
CHROME ?= chromium
PORT   ?= 8875

.DEFAULT_GOAL := help
.PHONY: help serve test test-node golden interaction lint check stamp figures pdf pdfcheck clean
.NOTPARALLEL:          # check runs its steps in a fixed order; interleaved output is useless

help:  ## List these targets
	@grep -hE '^[a-z][a-z0-9-]*:.*##' $(MAKEFILE_LIST) \
	  | sed -E 's/^([a-z0-9-]+):.*## +/\1\t/' \
	  | awk -F'\t' '{printf "  make %-12s %s\n", $$1, $$2}'

serve:  ## Serve the repository on 127.0.0.1:8875 with caching off (override with PORT=)
	$(PY) tools/serve.py --port $(PORT)

lint:  ## Check the import boundaries: sim/ and 3d/ depend on nothing outside themselves
	$(PY) tools/check_boundaries.py

# The suite's assertions are shared ES modules under tests/cases/, executed by two runners:
# a page for the browser and a script for node. This target drives the browser one.
BROWSER_RUNNER := $(firstword $(wildcard tests/run.py tests/browser/run.py))

test:  ## Run the browser suites headless: the page's own, then the 3D library's
	@test -n "$(BROWSER_RUNNER)" || { echo "no browser-suite runner: looked for tests/run.py and tests/browser/run.py — see tests/README.md"; exit 1; }
	$(PY) $(BROWSER_RUNNER)
	CHROME=$(CHROME) 3d/scripts/browser-tests.sh

# CI reaches this target with node already installed, so the skip branch is unreachable
# there and a missing node fails the build. Locally, skipping is the honest outcome.
test-node:  ## Run the node unit tests — falls back to a browser shim when node is absent
	@if ! command -v node >/dev/null 2>&1; then \
	   echo 'test-node: no node here — running the same files in a browser instead.'; \
	   echo '           `node --test` in CI stays the authority; see tools/node_tests_in_browser.py.'; \
	   $(PY) tools/node_tests_in_browser.py; \
	 else set -x; \
	   if [ -f tests/node/run.mjs ]; then node tests/node/run.mjs; else node --test tests/node/*.mjs; fi; \
	   node --test 3d/tests/*.test.mjs; \
	 fi

golden:  ## Re-run the model at seed=7 and diff every output against tests/golden/
	@test -f tests/golden/check.py || { echo "tests/golden/check.py is missing — see tests/README.md"; exit 1; }
	$(PY) tests/golden/check.py

# The other suites ask what the model computes and what the page renders. This one asks
# whether the page is still running after someone has used it: a throw inside draw() kills
# the animation frame that would have requested the next one, and the page then sits there
# looking correct and frozen. It drives a browser, so it cannot run at the same time as the
# golden gate — .NOTPARALLEL above is what keeps `make check` from trying.
interaction:  ## Click through the page headless and check it survives every interaction
	@test -f tests/interaction/check.py || { echo "tests/interaction/check.py is missing"; exit 1; }
	CHROME=$(CHROME) $(PY) tests/interaction/check.py

check: lint stampcheck figcheck pdfcheck golden test test-node interaction  ## Everything CI checks

figcheck:  ## Every model figure quoted in a report must be the figure the model produces
	@$(PY) tools/check_figures.py

stampcheck:  ## Fail if any import is stamped at a version other than the current one
	@$(PY) 3d/scripts/stamp-version.py --check
	@$(PY) tools/stamp_site.py --check

pdf:  ## Build the three report PDFs from research/reports/ into research/pdf/out/
	$(PY) research/pdf/build.py

pdfcheck:  ## Fail if the reports no longer convert to LaTeX cleanly
	$(PY) tools/md2tex.py >/dev/null

factsheet:  ## Regenerate research/figures.json from the live model
	@$(PY) tools/serve.py --port 8899 --quiet & sleep 1; \
	 $(PY) tools/js_eval.py "http://127.0.0.1:8899/index.html?seed=7&data=snapshot" \
	   tools/figures_dump.js research/figures.json 16; \
	 kill %1 2>/dev/null || true

stamp:  ## Recompute both version hashes and stamp every import with them
	$(PY) 3d/scripts/stamp-version.py
	$(PY) tools/stamp_site.py

# pipeline/figures.py draws the concept page's diagrams, but it imports `design`, a module
# that stayed behind in the private site repository. It does not run here and is not wired
# up. These are the 3D library's figures, which are self-contained.
figures:  ## Rasterise the 3D figures to PNG, regenerating the SVGs first if node is here
	@if command -v node >/dev/null 2>&1; then cd 3d && node scripts/figures.mjs; \
	 else echo "figures: no node — rasterising the committed SVGs unchanged"; fi
	CHROME=$(CHROME) 3d/scripts/render-figures.sh

clean:  ## Delete generated output: rasterised figures and __pycache__
	rm -f 3d/assets/raster/*.png 3d/assets/raster/*.webp
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	@echo "clean: data/ is untouched — it is input to the pages, not build output"
