# Delivery plan

Status: 2026-10-09. Follow the [programme](PROGRAM.md) and [ranked next stages](NEXT-STAGES.md).

## First documentation slice

The first candidate adds the newcomer introduction, a badge linked to the actual CI workflow, an existing CC BY illustration, citation metadata, the documentation index, Builder guidance and these programme documents. It preserves generated README regions and numerical records. Open-question reconciliation and issue filing follow in a bounded update, using existing anchors and actual open states.

For this documentation slice, run `make readmecheck linkcheck buildercheck` with project scratch configured. The checks verify generated README regions, local tracked links and anchors, and recorded Builder trailers. External URLs are listed without fetching. Check Builder history again after committing. No physics computation or hardware qualification follows from these checks.

## Unit record and review

Record the question, frozen assumptions, source revision, observed result and practical limits under `research/`. Distinguish PASS within its tested scope, FAIL of a hypothesis, UNKNOWN where evidence is absent, NOT RUN and control stops. Preserve previous chronology; corrections add a new disposition rather than rewriting old evidence.

Keep one evidence file for a unit, with exact candidate commit, tree and base, changed paths, check commands and results, review referents and any required landing dependencies. A reviewer checks custody once. A documentation change is checked as documentation; source or physics changes need their applicable code review and scientific evidence.

Prepare commits in an isolated worker-owned clone with a separate Git directory and normal project governance. Include the Builder trailer described in [CONTRIBUTING.md](../../CONTRIBUTING.md). Submit the exact candidate and its checks for Captain landing; no worker edits the primary or lands directly. Record acceptance and the actual landing in the unit's research record that day. Do not count an unlanded branch commit toward daily delivery.

## Daily progress

Report actual per-repository landing counts, stage states, the first pending landing and reserved decisions with their proposed defaults and dates. Continue to the next assigned ranked item in the same hour after acceptance. Reuse preserved evidence references instead of making historical custody a new gate.

The documentation slice establishes no scientific result. Result publication needs its own research record and applicable claim gate. No numerical acceptance threshold or physical measurement changes in this slice.
