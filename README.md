# Airships: a checkable study

This repository studies whether an evacuated hull could carry water to a fire, using a simulated fleet, published assumptions and code a reader can run. **Nothing here has flown:** the aircraft are imagined, and the replay must never imply that a real fire would have burned differently.

<!-- Float-wording batch: insert the ledger-bound headline finding here after its figures are verified. -->

## Four checks: about 20 minutes with the full gate

From a fresh clone at the repository root, use Python 3 with `requirements.txt`, Node 22, Chromium, and the PDF tools listed at the top of the [Makefile](Makefile) (latexmk, pdfLaTeX, TeX Gyre fonts and poppler). The full check needs Node; the browser fallback skips filesystem-dependent suites. The checks need those installed; the pages themselves need only a local HTTP server. These are measured times on one prepared machine, not a promise for a cold machine. The full check took the stranger 11m32s; the four steps together take about 20 minutes on that prepared machine.

1. **Run the gates (about 12 minutes; browser and PDF tools required).**

   ```sh
   make check
   ```

   This runs the checks in the [Makefile](Makefile). A passing command can still report known failed engineering proofs: read its `NOT PROVEN` and known-failure lines. It can also rewrite tracked telemetry or PDFs, so inspect `git status --short` afterwards. `make check` and CI also run `readmecheck`, `noticecheck`, `mutationcheck` and `buildercheck`; `readmecheck` verifies the generated figures below.

2. **Reproduce and move a number (about one minute; Node only).** This example uses balanced mode and a one-way distance in kilometres. It makes no feed request. What it prints comes from the earlier flight model: read "Model output and limits" below before quoting it.

   ```sh
   node --input-type=module -e "import {planCycle} from './sim/plan.js'; import {CLASSES, MODES} from './sim/config.js'; for (const km of [15, 45]) { const r = planCycle(CLASSES.P10000, MODES.balanced, km); console.log(km, r.tph.toFixed(0), r.cycleMin.toFixed(1), r.eCycleMWh.toFixed(2), r.kwhPerTonne.toFixed(2)); }"
   ```

   The columns are km one way, tonnes/hour, minutes/cycle, MWh/cycle and kWh/delivered tonne. Longer transit lowers throughput and raises drag energy per tonne. Change the distance again, or inspect the assumptions in [`sim/config.js`](sim/config.js). The table below is regenerated from [`research/figures.json`](research/figures.json); `make figfresh` checks that record against the live model.

   <!-- readme:example:start -->
   Expected from the shipped defaults: **13,183 t/h**, **45.5 min/cycle**, **54.33 MWh/cycle**, and **5.43 kWh/t**. These are model outputs, not observed aircraft performance.
   Expected at 45 km from the shipped defaults: **7,683 t/h**, **78.1 min/cycle**, **113.86 MWh/cycle**, and **11.39 kWh/t**. This row is also a model output.
   <!-- readme:example:end -->

3. **Inspect the latest recorded change (about two minutes with a browser).** The [public log](https://pinkrobotics.ca/log/) displays its builder, checker and token and wall-time cost. It needs JavaScript to load `data/activity.json`; plain `curl` only sees the fallback. Compare its commit identifier with your clone's `git log -1 --oneline`: this branch and the published log can be at different commits. The log's provenance and cost are reported by the crew's own records, not independently audited here.

4. **Read the float case (about four minutes).** Start with [the ship float brief](docs/FLOAT.md) for the present design, then [the cell calculation](research/analysis/vacuum-cell.md) and [the mass budget](research/analysis/mass-budget.md) for their separate assumptions. Those documents state the basis and [verification plan](docs/VERIFICATION-PLAN.md) names the experiments that could change it. You can inspect the records without a browser:

   ```sh
   python3 -c "import json; x=json.load(open('research/analysis/vacuum-cell.json')); print('ship0.worlds.s1050_sf12 ratioSL:', x['ship0']['worlds']['s1050_sf12']['ratioSL'], 'ship0.worldsFramePractice.s1450_sf12 ratioSL:', x['ship0']['worldsFramePractice']['s1450_sf12']['ratioSL'])"
   python3 research/analysis/mass-budget.py
   ```

   The first command prints `ship0.worlds.s1050_sf12 ratioSL: 0.558` and `ship0.worldsFramePractice.s1450_sf12 ratioSL: 0.981` from the committed record.

Known model defects, deliberate failing tests and the decisions still open are recorded in [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md). The committed mass-budget JSON and prose currently lag a fresh run of its Python source; use the command above for its current calculation. The [objection loop](GOALS.md) says how a disputed number should be reproduced and corrected. The assembly gate can exit successfully with frozen failed proofs; a green suite is not evidence that the craft is buildable.

## Model output and limits

This table describes the simulated cycle under the model defaults. It is a calculation, not a performance claim. Its energy and delivery figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected energy figures will be higher and delivery lower, and some cycles may not be flyable as drawn. That model also has a documented disagreement between planned and integrated draw in [the open questions](docs/OPEN-QUESTIONS.md). The P-100 is the reference class. Nobody is proposing to build a P-10000.

<!-- readme:headline:start -->
| Model output, balanced mode, 15 km one way | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Payload | 100 t | 1,000 t | 10,000 t |
| Hull length | 110 m | 238 m | 512 m |
| Cycle | 34.2 min | 35.4 min | 45.5 min |
| Water delivered | 175 t/h | 1,697 t/h | 13,183 t/h |
| Descent anchor | 125 t | 1,250 t | 12,400 t |
| Retained ballast | 0 t | 0 t | 0 t |
| Energy per cycle | 1.39 MWh | 8.45 MWh | 54.33 MWh |
| Energy per delivered tonne | 13.91 kWh/t | 8.45 kWh/t | 5.43 kWh/t |
| Binding constraint | transit distance | transit distance | transit distance |
<!-- readme:headline:end -->

It is the descent: a large enough hull cannot push itself back down into the dense air over a lake. The descent anchor in the model is a proposed water bag, not demonstrated hardware.

## Where to inspect the calculation

[`sim/config.js`](sim/config.js) names the classes, modes and defaults. [`sim/plan.js`](sim/plan.js) computes cycle duration, water delivered, energy and binding constraint; [`sim/physics.js`](sim/physics.js) contains the lift and power equations. Run `make figfresh` to compare the generated figure record with the model, and `make readmecheck` to compare this page with that record. Regenerate this page after model records change with `python3 tools/gen_readme.py`.

For a pinned browser run, serve the repository root and open the snapshot URL. The snapshot is committed data; it does not fetch a live emergency feed.

```sh
python3 -m http.server 8875
```

Open <http://127.0.0.1:8875/index.html?seed=7&data=snapshot>. The repository's browser-feed code is held to first-party requests by `make firstparty`. The deployed site has its own publish cycle; verify its served code before making the same claim about it.

## Evidence and scope

Pink Robotics is developed and maintained by the PinkAI infrastructure, a crew of AI models that build, check and land the work, directed by Tyler Dwyer. See the [work log](https://pinkrobotics.ca/log/). The work log names the model behind each change it records, from 1 October 2026; earlier work predates that record.

<!-- readme:sources:start -->
The [source catalogue](research/sources.json) contains **108 entries**.
<!-- readme:sources:end -->

[DATA-SOURCES.md](DATA-SOURCES.md) records the datasets, licences and query methods. The captured snapshot under [`data/`](data/) supports offline replay. Do not query emergency agency feeds to run this test.

The study's purpose and acceptance target are in [GOALS.md](GOALS.md). [CONTRIBUTING.md](CONTRIBUTING.md) explains how to bring a reproducible objection. The code licence is in [LICENSE](LICENSE).
