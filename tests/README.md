# tests

Three tiers, answering three different questions.

| tier | question | where | needs |
|---|---|---|---|
| unit | does the model still make sense? | `cases/*.cases.js` | a browser, or node 18+ |
| golden | does the model still produce the same numbers? | `golden/check.py` | python3 + chromium |
| shipped selftest | can a reader check the numbers from the page itself? | `../sim/selftest.js` | the live page |

The unit tier is written once and run twice. The assertions live in `cases/`, import nothing
but the code under test and `harness.js`, and are executed by two runners: `browser/index.html`
locally, `node/run.mjs` in CI. That split exists because the machine this was written on has no
node and CI has no browser, and because a test that only runs in one of them is a test that
rots in the other.

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
make test-node   # the same assertions under node --test, or a plain "no node here"
make golden      # replay at seed=7 and diff every output against the baselines
make check       # everything that runs without node
```

**In a browser**, to read it rather than script it — no toolchain, no install:

```sh
make serve       # or: python3 -m http.server 8875 --directory .
# then open http://127.0.0.1:8875/tests/browser/
```

**Headless**, which is what `make test` does:

```sh
$ tests/browser/run.py            # add -v to list the passing tests too
150 passed, 0 failed, 4 known-failing — 154 tests in 35 suites, 81 ms
```

That driver loads the same page and reads the record it leaves on `window.__tests` — per
suite, per test, with the failure message. For something even smaller to parse, the page
puts a summary in `document.title`, and `tools/screenshot.py` prints titles:

```sh
$ python3 tools/screenshot.py http://127.0.0.1:8875/tests/browser/
TITLE: AIRSHIPS TESTS pass=150 fail=0 known=4 total=154
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

`tests/browser/run.py` and `tests/golden/check.py` both serve the repository themselves on a
free port, unless `AIRSHIPS_PORT` (or `PORT`) names a development server that is already
listening, in which case they reuse it. CI starts one server for the whole job; locally you
do not have to start anything.

## What belongs where

**`cases/*.cases.js` — invariants and hand-computed values.** A test here should still be
right after someone rewrites the internals. Prefer a relation that must hold (`delivered +
retained = payload`, throughput falls with distance, the phases tile the cycle) over a number
that happens to come out. Where a literal number is the point — pump power, disc power, a
great-circle distance — work it out in the comment, in SI, so a reader can check the
arithmetic without running anything. Anything that would need updating on every unrelated
change belongs in `golden/`, not here.

- `sim-physics` — `pumpMW`, `dragMW`, `diskMW`, `ledger`, and the `diskMW` ↔ `rotorMaxT`
  round trip that the whole descent argument rests on.
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

**`golden/` — characterisation.** `seed7-snapshot.json` is every model output, and
`ui-seed7-snapshot.json` is what the page renders, both captured from
`/?seed=7&data=snapshot`: the seed pins every choice the model makes, the snapshot pins
every external input. Any difference is a failure, including an improvement. When a change is
meant to move the numbers, regenerate with `--update`, **read the diff**, and commit the new
baseline in the same change as the code that moved it.

**`../sim/selftest.js` — the shipped checks.** Seventeen assertions that run in devtools on
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

Four are currently marked:

1. **`physics · lift at the working-band density covers dry mass plus payload`** — the
   buoyancy ledger buys lift at sea-level density (1.225 kg/m³) while the ships cruise
   1,500 m up. At the working-band density the model already uses for drag (1.10 kg/m³) all
   three classes are net heavy: 198 t of lift against 200 t for the P-100, 19,800 against
   20,000 for the P-10000. This contradicts the page's claim that the rotors only ever push
   down.
2. **`plan · windUsed is false when the wind was not applied`** — `windUsed` tests only
   `wind.spd`, while the legs also require `wind.bearing`. The flag can report a wind the plan
   ignored. Harmless today, because `mission.js` always sets the bearing before planning.
3. **`plan · the letdown term is a minor share of cycle energy`** — `min(6, RETURN_TRANSIT ×
   0.2)` sets 53% of the P-10000's published 82.5 MWh cycle. Neither the 6 nor the 0.2 is
   justified anywhere in the model.
4. **`energy · the planned budget and the integrated draw agree within 25%`** — two power
   models. On a 19 km leg `planCycle` budgets 99.3 MWh for the P-10000 while integrating
   `stateAt`'s per-system draw over the same cycle gives 227.7 MWh, a factor of 2.29. The gap
   widens with the size of the ship: 1.14× on the P-100, 1.58× on the P-1000.

Everything else about those defects — including the numbers above — is asserted by ordinary
passing tests alongside the markers, so the arithmetic is on the record either way.

**Four markers, six open questions.** `docs/OPEN-QUESTIONS.md` tracks six items and only
three of them appear above; the fourth marker, `windUsed`, has no entry there because it is
too small. The three that cannot have a marker are dead descent ballast (`selftest.js`
*requires* `retainedT` to be zero, so a failing test would assert the opposite of the
specification), the Esri basemap (not a model behaviour), and the uncredited generators (no
assertion can fail because a term is missing from a sum). Those three are held to ordinary
passing tests that record what the code does. A count of markers is not a count of defects.

## Adding a test

1. Put the assertion in the right `cases/*.cases.js` file, or a new one.
2. **If you add a file, add it to both runners** — the `CASES` array in
   `browser/index.html` and the import list in `node/run.mjs`. They are deliberately
   explicit rather than globbed, because a browser cannot glob; the cost is that a file
   listed in one and not the other runs in one and not the other.
3. Run it both ways before committing, and run `golden/check.py` if you touched anything
   under `sim/`.

A test that cannot fail is worse than no test. If you are not sure a new assertion has any
teeth, break the code on purpose and watch it go red.

## Notes on the harness

`harness.js` is 140 lines and has no dependencies. It collects test definitions at
import time and runs them on demand, returning a record rather than printing, so both runners
can format the same outcomes their own way. Assertions: `ok`, `eq` (`Object.is`), `close(a, b,
tol)` (absolute tolerance, no default — state the one you mean), `throws`, `deepEq`.
Everything is synchronous; nothing in `sim/` is async, and a test framework that can await is
a test framework that can hang.

## Gotchas

- **The golden dumps need time.** `check.py` waits 16 s for the model dump and 18 s for the UI
  dump before evaluating. Twelve is not enough — the page has not finished building the fleet
  and the evaluation fails outright rather than returning something wrong.
- **Two golden runs at once are fine now.** `tools/js_eval.py` used to bind a fixed debug port
  (9281) and share the default browser profile, so a second run found the port taken, got no
  debuggable page, and died pointing at the websocket library rather than at the collision. It
  now takes a free port from the kernel and a profile of its own, as `tests/interaction/check.py`
  always did.
- **`CFG` is global.** It is the only mutable state in `sim/`, so any test that patches it
  must `resetConfig()` in a `finally`. `sim-config.cases.js` is both the test of that and the
  worked example of the pattern.
- **Cycle 1 is not a typical cycle.** `SOURCE_APPROACH` has no previous return leg to
  continue on the first cycle, so it sits at the intake on a default heading. Continuity
  tests sample cycle 2.
