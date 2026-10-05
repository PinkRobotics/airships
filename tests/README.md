# tests

The test groups answer different questions. This table introduces five groups;
`make help` lists the full gate set, and `make ciparity` checks its CI order.

| tier | question | where | needs |
|---|---|---|---|
| unit | does the model still make sense? | `cases/*.cases.js` | a browser, or node 18+ |
| golden / goldenui | do the model outputs and captured page elements still match? | `golden/check.py` | python3 + chromium |
| shipped selftest | can a reader check the numbers from the page itself? | `../sim/selftest.js` | the live page |
| season | do the season files match a regeneration, and do their pinned totals hold? | `season/check.py` (`make seasoncheck`) | python3 |
| capture | does the daily capture tool behave against recorded responses? | `capture/check.py` (`make capturecheck`) | python3; a fixture server on 127.0.0.1 |

The unit tier is written once and run twice. The assertions live in `cases/`, import nothing
but the code under test and `harness.js`, and are executed by `browser/index.html` and
`node/run.mjs`. `make check` and CI run both runners.

```
harness.js              describe/it, five assertions, and knownFail; collects, does not print
cases/*.cases.js        the assertions — the only files most changes should touch
browser/index.html      runner 1: loads the cases in a page and renders the result
browser/run.py          drives that page headless and reports it in a terminal
node/run.mjs            runner 2: re-emits the same cases into node:test
golden/check.py         the regression gate: replay the page, diff against the baselines
golden/*.json           the baselines; golden/*dump.js the scripts that produce them
```

## Running

```sh
make test        # the browser suites, headless
make test-node   # Node suites; browser-compatible 3D fallback if Node is absent
make golden      # replay the seeded model and diff its captured outputs
make goldenui    # diff the rendered-page snapshot
make check       # all local gates; CI omits CI_REFERENCE_CHECK; Node is required
```

**In a browser**, to read it rather than script it — no toolchain, no install:

```sh
make serve       # or: python3 -m http.server 8875 --directory .
# then open http://127.0.0.1:8875/tests/browser/
```

**Headless**, which is what `make test` does:

```sh
$ tests/browser/run.py            # add -v to list the passing tests too

```

That driver loads the same page and reads the record it leaves on `window.__tests` — per
suite, per test, with the failure message. For something even smaller to parse, the page
puts a summary in `document.title`, and `tools/screenshot.py` prints titles:

```sh
$ python3 tools/screenshot.py http://127.0.0.1:8875/tests/browser/

```

**Under node** (this is what CI runs):

```sh
node --test tests/node/run.mjs
```

No dependencies and no install step: `node:test` is in the standard library, and the model is
plain ES modules.

**The golden gate:**

```sh
tests/golden/check.py            # exits non-zero on any difference
tests/golden/check.py --only ui  # just the rendered-page half
tests/golden/check.py --update   # rewrite the baselines, deliberately
```

`tests/browser/run.py` and `tests/golden/check.py` each serve their own repository on a
system-chosen port and close the server on exit. CI uses the same arrangement; neither
runner needs a server started beforehand.

## What belongs where

**`cases/*.cases.js` — invariants and hand-computed values.** A test here should still be
right after someone rewrites the internals. Prefer a relation that must hold (`delivered +
retained = payload`, throughput falls with distance, the phases tile the cycle) over a number
that happens to come out. Where a literal number is the point — pump power, disc power, a
great-circle distance — work it out in the comment, in SI, so a reader can check the
arithmetic without running anything. Anything that would need updating on every unrelated
change belongs in `golden/`, not here.

- `sim-atmosphere` — ISA density against altitude, checked against the ISO 2533 table rather
  than against itself. The buoyancy ledger reads from it, so an error here is an error in
  every published tonne.
- `sim-physics` — `pumpMW`, `dragMW`, `diskMW`, `ledger`, and the `diskMW` ↔ `rotorMaxT`
  round trip that the whole descent argument rests on. Also the two sizing requirements the
  class table exists to satisfy: fail-safe float-up and unpowered recovery.
- `sim-plan` — `planCycle`: the mass book, the durations, wind symmetry, the modes, the
  tunables, and the three mechanisms the site's copy describes.
- `sim-state` — the phase machine: coverage, monotonic water, continuity across every seam,
  vertical duty, ground speed, a dead hull.
- `sim-energy` — the planned cycle budget against the integrated instantaneous draw.
- `sim-determinism` — what `?seed=` pins, and when it is read.
- `sim-config` — `setConfig` / `resetConfig`, the only mutable state in the model.
- `sim-geo` — distance, béziers, easing, and short-way heading interpolation.
- `sim-heat` — that the satellite heat layer actually reaches the drop planner, rather than
  being fetched and dropped.
- `spec-parity` — every field `sim/config.js` and `3d/model/config.js` both claim to know,
  compared. Written after the two copies drifted and the drift was found by review.

**`golden/` — characterisation.** `seed7-snapshot.json` holds model outputs at the captured inputs, and
`ui-seed7-snapshot.json` holds selected rendered elements, both captured from
`/?view=exercise`: the bundled exercise supplies its own seed, invented fires and
pinned inputs. Any difference is a failure, including an improvement. When a change is
meant to move the numbers, regenerate with `--update`, **read the diff**, and commit the new
baseline in the same change as the code that moved it.

**`../sim/selftest.js` — the shipped checks.** Model assertions that run in devtools on
the live page, for a reader who does not trust the numbers and does not want to clone
anything. It is duplicated in spirit by `cases/`, on purpose: one is for CI, one is for a
stranger.

## Known failures

`harness.js` has a fourth outcome besides pass and fail. `knownFail(name, reason, body)`
marks a test that is *expected* to fail against a defect that is open and tracked. It still
runs. Failing is reported as `known` and does not fail the suite; **passing is reported as a
hard failure**, because a defect that has quietly been fixed must not keep a permanent excuse
in the suite — the marker has to come off and the test has to start asserting the corrected
behaviour.

<!-- test-status:markers:start -->
The registered suites contain **0 known-failing markers**.
The corrected wind flag runs as an ordinary assertion in `cases/sim-plan.cases.js`.
The force ledger and phase-integral checks run in `cases/sim-energy.cases.js`.
These counts describe registered tests, not an execution result.
<!-- test-status:markers:end -->

### Keeping the test inventory current

`make test` and `make test-node` compare the files and test names that actually
run with `research/test-inventory.json`. The browser fallback checks the same
inventory, with its named Node-only exclusions. Missing or renamed tests fail
with their identities even after `make stamp`.

After deliberately adding, renaming or retiring a test, run
`python3 tools/gen_test_status.py --inventory` once. Review the inventory diff:
every removed file and test name must have a reason. Use
`python3 tools/gen_test_status.py --inventory --check` to verify it without writing.
The generator's existing count/document mode remains separate; `make stamp`
changes cache versions and never writes the test inventory.
