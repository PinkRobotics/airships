# The whole contributor interface. `make` on its own prints it.
#
# Checks need Python dependencies from requirements.txt, Chromium, and the PDF toolchain
# (latexmk, pdfLaTeX, TeX Gyre fonts, poppler). CI also installs Node 22 for test-node.

PY     ?= python3
CHROME ?= chromium
PORT   ?= 8875

.DEFAULT_GOAL := help
.PHONY: help serve test test-node golden interaction lint check stamp figures pdf pdfcheck figfresh \
        analysis analysischeck cellparity explorercheck nodes nodescheck contractcheck \
        assemblycheck contractfreeze skin skincheck fallback fallbackcheck levelscheck shipcheck bandcheck ciparity \
        firstparty firstparty-static labelledcheck clean
.NOTPARALLEL:          # check runs its steps in a fixed order; interleaved output is useless

help:  ## List these targets
	@grep -hE '^[a-z][a-z0-9-]*:.*##' $(MAKEFILE_LIST) \
	  | sed -E 's/^([a-z0-9-]+):.*## +/\1\t/' \
	  | awk -F'\t' '{printf "  make %-15s %s\n", $$1, $$2}'

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
	 else set -ex; \
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

firstparty-static:  ## Refuse external loading URLs in every served source file
	$(PY) tests/firstparty/static.py
	$(PY) -m unittest discover -s tests/firstparty -p 'test_*.py'

firstparty: firstparty-static  ## Record browser requests on every served page in three mirror modes
	node --test tests/firstparty/wind.test.mjs
	CHROME=$(CHROME) $(PY) tests/firstparty/check.py

check: ciparity lint stampcheck figfresh fallbackcheck labelledcheck figcheck analysischeck cellparity skincheck explorercheck levelscheck shipcheck bandcheck nodescheck contractcheck assemblycheck pdfcheck golden test test-node firstparty interaction  ## Everything CI checks

ciparity:  ## CI and make check must run the same ordered gates; verify the stranger runner
	$(PY) tools/check_ci_parity.py
	$(PY) -m unittest discover -s tools/tests -p 'test_*green.py'

# The monitor page's no-script/crawler fallback: the FALLBACK regions in index.html, written
# from the bundled snapshot by replaying it headless (`?seed=7&data=snapshot`, the golden
# suite's own pinned run). `fallback` re-shoots the map poster too; the check does not — a
# canvas capture is not byte-stable — but it DOES re-run the replay and diff every region,
# for the same reason figfresh and skincheck regenerate: this repository has twice shipped a
# gate that lied by comparing a stale file.
fallback:  ## Regenerate index.html's static fallback block (and its map poster) from the snapshot
	$(PY) tools/gen_fallback.py --poster

fallbackcheck:  ## The fallback block must match a fresh regeneration from the snapshot
	$(PY) tools/gen_fallback.py --check

labelledcheck:  ## Recompute six external comparisons and refuse stale reports (a MISS stays published)
	$(PY) research/validation/check.py

analysischeck:  ## Every figure quoted in an analysis note must match its own generated JSON
	$(PY) tools/check_analysis.py

cellparity:  ## ship/model.js must agree with research/analysis/vacuum-cell.py exactly
	$(PY) tools/check_cell_parity.py

explorercheck:  ## The 3D explorer must render every level and display only the model's numbers
	$(PY) tools/check_explorer.py

# THE FAST PATH FOR BLUEPRINT-PAGE EDITS: `make stamp && make levelscheck` is ~10 s against
# the full chain's ~8 min, the same trade explorercheck already gives explorer-only work.
# The full chain still runs once before publish — this is the iteration loop, not the law.
levelscheck:  ## The blueprint page must boot clean, draw every figure, keep text on canvas
	$(PY) tools/check_levels.py

shipcheck:  ## The ship checks page must boot clean and show only the model's numbers
	$(PY) tools/check_ship.py

bandcheck:  ## The band calculator must solve the same physics as the Python mirror
	$(PY) tools/check_band.py

skin:  ## Re-solve the loaded skin (#63): membrane FEM, gore study, generated outputs
	$(PY) tools/gen_skin.py
	@echo 'skin: run `make stamp` — ship/skin.generated.js changed.'

# A full re-solve and byte comparison, not a hash shortcut: the solve is nine seconds,
# and this repository has twice shipped a gate that lied by comparing a stale file.
skincheck:  ## The committed loaded-skin outputs must match a full re-solve, every gate green
	$(PY) tools/gen_skin.py --check

nodes:  ## Regrow every computed joint STL from the SDF rule (research/geometry/nodes)
	$(PY) tools/gen_nodes.py
	@# The explorer's connector tour reads its five families out of the manifest through a
	@# generated ES module. Regrow the joints and it must follow, or explorercheck fails.
	$(PY) tools/gen_node_families.py
	@# The joints the explorer DRAWS: the display field over all 51, plus the five family
	@# representatives at print resolution. Same SDF rule; regrow one, regrow the other.
	$(PY) tools/gen_display_meshes.py
	@echo 'nodes: run `make stamp` — ship/nodes.generated.js and nodemeshes.generated.js changed.'

nodescheck:  ## The computed-node manifest must be closed and match the article graph
	$(PY) tools/check_nodes.py
	@# The display-mesh module is a pure function of gen_nodes.py, its own generator and
	@# the manifest's parameters; --check re-hashes those sources without an SDF run, so a
	@# regenerate-forgotten module goes red here in milliseconds. This repository has twice
	@# shipped a gate that lied by comparing a stale file.
	$(PY) tools/gen_display_meshes.py --check

# THE CAP, and it is deliberately two targets. `contractcheck` asks whether the cap on disk
# FITS THIS ARTICLE — that contract.json exists at all, is the schema this prover writes, names
# the same 432 member-ends and 51 nodes, and was frozen at the parameters the STLs beside it
# were cut for. That is the one failure a property diff cannot report, because a diff against a
# contract that was never frozen has nothing to say and would pass in silence. It evaluates no
# field, so it costs about a second and belongs here, immediately after the manifest it reads.
# `assemblycheck` below then asks the opposite question — whether the article still MATCHES the
# cap — because that answer needs the full measurement and is free once the measurement is
# running. Splitting them this way is what keeps `make check` from paying for the same two
# minutes twice.
contractcheck:  ## The frozen connection contract must exist and cover this article
	$(PY) tools/check_assembly.py --contract-only

# `nodescheck` asks whether 51 meshes are closed and whether the manifest counts match the
# analysis. Both can be true of an article that cannot be built, and were: a socket drawn for
# the wrong tube, a shoulder the pipe never reaches, 166 members with 0.00 mm of insertion
# travel where 20 mm is needed. This measures each of the 432 member-ends out of the SDF and
# holds it to a frozen contract. It regenerates nothing and drives no browser, so it costs a
# minute rather than the minutes `make nodes` costs. CI runs it plain; the nightly runs
# --exhaustive, which adds the void-topology fill, the STL cross-check and the full insertion
# sweep for about three minutes.
#
# It also DIFFS every proven property of every member-end against research/geometry/nodes/
# contract.json and fails naming the member-end, the property and both values. That is what
# makes the coming weight optimisation safe: shrink a node, lose 3 mm of engagement on nine
# arms, and this goes red with those nine arms named rather than passing on an unchanged
# triangle count. Nothing in this file re-freezes it — see `contractfreeze`.
assemblycheck:  ## Measure all 432 member-ends from the joint SDF against the frozen contract
	$(PY) tools/check_assembly.py

# NOT IN `check`, AND IT NEVER WILL BE. Re-freezing is a decision, not a build step: it says
# "these connections are different now and I have read how". The script prints every property
# it is about to cap before it writes one byte, and it leaves the run's own exit code alone, so
# freezing a red article records a red article rather than greening it. A target exists only so
# that the command is written down in the same place as the gate it answers to.
contractfreeze:  ## Cap today's measured connection state as the new contract — read the diff first
	$(PY) tools/check_assembly.py --freeze

figcheck:  ## Every model figure quoted in a report must be the figure the model produces
	@$(PY) tools/check_figures.py

stampcheck:  ## Fail if any import is stamped at a version other than the current one
	@$(PY) 3d/scripts/stamp-version.py --check
	@$(PY) tools/stamp_site.py --check

pdf:  ## Build the three report PDFs from research/reports/ into research/pdf/out/
	$(PY) research/pdf/build.py

pdfcheck:  ## Fail if the reports no longer convert, or the PDFs no longer set cleanly
	$(PY) tools/md2tex.py >/dev/null
	$(PY) research/pdf/build.py --fast --strict

# THE MOST IMPORTANT CHECK HERE. `figcheck` compares the reports against
# research/figures.json and prints "N cited figures match the model" — but figures.json is a
# committed cache that only `factsheet` refreshes, and `factsheet` was in neither `check` nor
# CI. Change a constant in sim/, update the goldens the way the docs say to, and the whole gate
# goes green while six published figures are wrong. See the script's header.
figfresh:  ## Fail if research/figures.json has drifted from the live model
	$(PY) tools/check_figures_fresh.py

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

# NOT IN `check`, like `analysis`: these need a browser plus minutes, and the review needs
# the LOCAL vision fleet (dual-GPU gemma at :8010), which CI does not have. The joints are
# expected to keep changing; this pair is the per-change visual verification — every joint
# rendered six ways with seat markers, then reviewed by the vision model against its own
# facts. Verdicts land in research/geometry/nodes/vision/verdicts.json and ARE committed;
# the shot PNGs are regenerated evidence and are gitignored.
jointshots:  ## Capture six marked views of every printed joint (browser, ~15 min)
	$(PY) tools/joint_shots.py

jointreview: jointshots  ## Vision-review every joint against its seats (needs the fleet)
	$(PY) tools/review_joints.py

# The concept analyses in research/analysis/. These answer questions about the VEHICLE rather
# than about the code, so they are not in `check`: two of them take minutes and one needs a
# fire-history extract that is fetched, not generated. But they must stay reproducible, and
# the browser-run ones must read the live model rather than a cached figure, for the same
# reason `figfresh` exists.
analysis:  ## Regenerate the concept analyses in research/analysis/
	$(PY) research/analysis/mass-budget.py --json research/analysis/mass-budget.json
	$(PY) research/analysis/delivery.py --json research/analysis/delivery.json
	$(PY) research/analysis/vacuum-cell.py --json research/analysis/vacuum-cell.json
	$(PY) research/analysis/helium.py --json research/analysis/helium.json
	@test -f data/fire-history-bc.json || { \
	   echo 'analysis: data/fire-history-bc.json is missing.'; \
	   echo '          Fetch it with: $(PY) pipeline/firehistory.py data/fire-history-bc.json'; \
	   exit 1; }
	@$(PY) tools/serve.py --port 8899 --quiet & sleep 1; \
	 for a in water-availability descent; do \
	   $(PY) tools/js_eval.py "http://127.0.0.1:8899/index.html?seed=7&data=snapshot" \
	     research/analysis/$$a.js research/analysis/$$a.json 20 || exit 1; \
	 done; \
	 kill %1 2>/dev/null || true

clean:  ## Delete generated output: rasterised figures and __pycache__
	rm -f 3d/assets/raster/*.png 3d/assets/raster/*.webp
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	@echo "clean: data/ is untouched — it is input to the pages, not build output"
