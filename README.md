# Airships: a checkable study

This repository studies whether an evacuated hull could carry water to a fire, using a simulated fleet, published assumptions and code a reader can run. **The fires are real; the fleet is simulated and never flew.** The labelled exercise uses invented fires. Nothing here says or implies that a real fire would have burned differently.

## Run and inspect the study

From a fresh clone at the repository root, use Python 3 with `requirements.txt`, Node 22, Chromium, and the PDF tools listed at the top of the [Makefile](Makefile) (latexmk, pdfLaTeX, TeX Gyre fonts and poppler). The full check needs Node; the browser fallback skips filesystem-dependent suites. The pages themselves need only a local HTTP server. Check runtimes depend on the machine.

1. **Run the gates (browser and PDF tools required).**

   ```sh
   export TMPDIR="$PWD/.browser-scratch"
   mkdir -p "$TMPDIR"
   make check
   ```

   This runs the checks in the [Makefile](Makefile). A passing command can still report known failed engineering proofs: read its `NOT PROVEN` and known-failure lines. It can also rewrite tracked telemetry or PDFs, so inspect `git status --short` afterwards. `readmecheck` verifies the generated figures below. `noticecheck` checks the publication package; `linkcheck` checks repository documentation links and anchors without fetching external URLs.

<!-- readme:energy-input:start -->
2. **Reproduce and move a number (about one minute; Node only).**
   This example uses balanced mode and a one-way distance in kilometres.
   It prints both energy bases and the force verdict, without a feed request.

   ```sh
   node --input-type=module -e "import {planCycle,CLASSES,MODES} from './sim/index.js'; for(const km of [15, 45]) for(const basis of ['record','favourable']) { const p=planCycle(CLASSES.P10000,MODES.balanced,km,null,{basis}); console.log(km,basis,p.feasible,p.cycleMin,p.eCycleMWh,p.kwhPerTonne,p.worst); }"
   ```

   The columns are distance, basis, force verdict, minutes, supplied MWh, kWh per planned tonne, and the worst unheld force.
   An infeasible row establishes no delivery or endurance.
   The example and table use `energy-documents.json`; `make energydoccheck` compares that record with the model.
<!-- readme:energy-input:end -->

   <!-- readme:example:start -->
   At 15 km, the prescribed P-10000 cycle takes **45.5 minutes** and does not close on the drawn hardware.
   Its supplied effort is **694.38 MWh/cycle** on record and **757.61 MWh/cycle** on favourable.
   The corresponding **69.44 / 75.76 kWh per planned tonne** do not establish delivered water.
   At 45 km, the prescribed P-10000 cycle takes **78.1 minutes** and does not close on the drawn hardware.
   Its supplied effort is **976.51 MWh/cycle** on record and **1168.58 MWh/cycle** on favourable.
   The corresponding **97.65 / 116.86 kWh per planned tonne** do not establish delivered water.
   <!-- readme:example:end -->

3. **Inspect a recorded change.** The [public log](https://pinkrobotics.ca/log/) displays its builder, checker and token and wall-time cost. It needs JavaScript to load `data/activity.json`; plain `curl` only sees the fallback. Compare its commit identifier with your clone's `git log -1 --oneline`: this branch and the published log can be at different commits. The log's provenance and cost are reported by the crew's own records, not independently audited here.

4. **Read the float case (about four minutes).** Start with [the ship float brief](docs/FLOAT.md) for the present design, then [the cell calculation](research/analysis/vacuum-cell.md) and [the mass budget](research/analysis/mass-budget.md) for their separate assumptions. Those documents state the basis and [verification plan](docs/VERIFICATION-PLAN.md) names the experiments that could change it. You can inspect the records without a browser:

   <!-- readme:float:start -->
   **Nothing floats today as drawn.**
   Both bases use structural safety factor 1.2 against full sea-level pressure.
   The record basis assumes knockdown 0.30 and 1,050 MPa chords.
   Its 52 m hull’s lift is 0.558 of its mass at sea level and 0.436 at 2,500 m.
   The favourable basis assumes knockdown 0.65 and a 1,450 MPa carbon-laminate ceiling, both unverified.
   Its lift-to-mass ratio is 0.981 at sea level and 0.766 at 2,500 m.
   The bill and the drawing disagree in 20 places.
   Across 5 readings of the end caps, the favourable ratio runs from 0.751 to 0.998 at sea level and from 0.586 to 0.780 at 2,500 m.
   No reading reaches 1.
   The [float ledger](docs/FLOAT-LEDGER.md) gives every case and what would have to be true to close it.
   <!-- readme:float:end -->

   ```sh
   python3 - <<'PYCODE'
   import json
   x = json.load(open('research/analysis/cap-readings.json'))
   for basis, row in x['readings']['R']['byBasis'].items():
       for altitude, result in row['at'].items():
           print(basis, altitude, result['altitudeM'], result['liftToMass'], result['marginT'])
   for basis, altitudes in x['ranges'].items():
       for altitude, result in altitudes.items():
           print('range', basis, altitude, result['min'], result['max'])
   PYCODE
   make analysischeck analysisfresh censuscheck
   ```

   The columns are basis, altitude name, altitude in metres, lift/mass and margin in tonnes; range rows give the minimum and maximum over all readings.
   These are computations with unresolved structural questions.

Known model defects, deliberate failing tests and the decisions still open are recorded in [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md). The mass-budget record now uses the configured capsule areas; `make analysisfresh` checks it against fresh generation. <!-- readme:energy-budget-context:start -->
The mass budget's cycle-energy context follows the figure cache. Its battery sizing does not establish feasible endurance.
<!-- readme:energy-budget-context:end --> The [objection loop](GOALS.md) says how a disputed number should be reproduced and corrected. The assembly gate can exit successfully with frozen failed proofs; a green suite is not evidence that the craft is buildable.

## Model output and limits

<!-- readme:energy-intro:start -->
This table describes prescribed cycles under the model defaults. The force ledger and energy integrals now share one calculation.
All rows below are unsupported prescribed profiles; their requested mass and supplied effort are not achieved delivery.
The P-100 is the reference class. Nobody is proposing to build a P-10000.
<!-- readme:energy-intro:end -->

<!-- readme:headline:start -->
| Prescribed balanced profile at 15 km | P100 | P1000 | P10000 |
|---|---:|---:|---:|
| Force verdict | does not close / does not close | does not close / does not close | does not close / does not close |
| Hull length, m | 110 | 238 | 512 |
| Minutes | 34.2 | 35.4 | 45.5 |
| Requested payload, t | 100 | 1000 | 10000 |
| Water kept, t | 0 | 0 | 0 |
| Supplied MWh: record / favourable | 8.192 / 6.402 | 62.314 / 61.155 | 694.378 / 757.615 |
| kWh per planned tonne: record / favourable | 81.923 / 64.017 | 62.314 / 61.155 | 69.438 / 75.761 |
| Worst unheld t: record / favourable | 34.556 / -5.714 | 818.465 / 818.465 | 7073.819 / 7073.819 |
<!-- readme:headline:end -->

<!-- readme:energy-reading:start -->
The prescribed profiles leave force unheld in several phases, including stationary fill on the larger classes.
The [generated tables](docs/ENERGY-CLOSURE-2026-10.md) show the cheapest feasible profiles found in the stated space, their retained water and their minutes.
The independent [payload-exchange study](research/analysis/payload-exchange.md) is analysis, not design.
<!-- readme:energy-reading:end -->

## Where to inspect the calculation

<!-- readme:energy-method:start -->
`sim/config.js` names the assumptions. `sim/plan.js` times the cycle; `sim/power.js` owns force limits and integrated power.
`sim/requirements.js` searches the stated profiles. Run `make energycheck energydoccheck figfresh` to check the energy records and documents.
Run `make readmecheck` to compare this page with those records; regenerate it with `python3 tools/gen_readme.py`.
<!-- readme:energy-method:end -->

For a pinned browser run, serve the repository root and open the snapshot URL. The snapshot is committed data; it does not fetch a live emergency feed.

```sh
python3 -m http.server 8875
```

Open <http://127.0.0.1:8875/index.html?seed=7&data=snapshot>. The repository's browser-feed code is held to first-party requests by `make firstparty`. The deployed site has its own publish cycle; verify its served code before making the same claim about it.

## Pages and documents

| Start here | What to inspect |
|---|---|
| [Fleet monitor](index.html) | Dated fire records and the labelled simulated fleet or invented exercise |
| [Concept](concept/index.html) | Proposed mission, assumptions and limitations |
| [Engineering](engineering/index.html) | Structural questions across the design scales |
| [Ship viewer](ship/index.html) | The drawn structure and its model readings |
| [Cell](cell/index.html), [blueprint](cell/levels.html), [checks](cell/ship.html), [band calculator](cell/band.html) | Cell and hull calculations |
| [Model lab](model-lab/index.html) | Vehicle visualisation and development controls |
| [Float case](docs/FLOAT.md), [ledger](docs/FLOAT-LEDGER.md), [member census](docs/MEMBER-CENSUS.md) | Verdict, basis and drawing/bill disagreements; also [readable as pages](float/index.html) |
| [Physics](docs/PHYSICS.md), [open questions](docs/OPEN-QUESTIONS.md), [verification plan](docs/VERIFICATION-PLAN.md) | Equations, unresolved defects and proposed experiments |
| [Research guide](research/README.md), [reports](research/reports/README.md) | Source notes and analysis |
| [Architecture](docs/ARCHITECTURE.md), [tests](tests/README.md), [tools](tools/README.md) | Code boundaries and contributor commands |
| [Data and sources](DATA-SOURCES.md), [notices](notices.html) | Captures, provenance and redistribution terms |

## Evidence and scope

Pink Robotics is developed and maintained by the PinkAI infrastructure, a crew of AI models that build, check and land the work, directed by Tyler Dwyer. See the [work log](https://pinkrobotics.ca/log/). The work log names the model behind each change it records, from 1 October 2026; earlier work predates that record.

<!-- readme:sources:start -->
The [source catalogue](research/sources.json) contains **108 entries**.
<!-- readme:sources:end -->

[DATA-SOURCES.md](DATA-SOURCES.md) records the datasets, licences and query methods. The captured snapshot under [`data/`](data/) supports offline replay. Do not query emergency agency feeds to run this test.

The study's purpose and acceptance target are in [GOALS.md](GOALS.md). [CONTRIBUTING.md](CONTRIBUTING.md) explains how to bring a reproducible objection. The code licence is in [LICENSE](LICENSE).
