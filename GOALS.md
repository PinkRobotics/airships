# Goals

This file says what Pink Robotics is working toward and in what proportion. Pink Robotics is developed and maintained by the PinkAI infrastructure, a crew of AI models that build, check and land the work, directed by Tyler Dwyer. See the [work log](https://pinkrobotics.ca/log/). The work log names the model behind each change it records, from 1 October 2026; earlier work predates that record. A daily planner, not built yet, will read the table below and
propose work in proportion to the weights. It will not be able to add an objective or change a
weight: those change only on the director's word, and every change is a commit in this repository's
history.

Where this file describes something that is not true yet, it says so.

Last change of direction: 2026-10-01, the opening weights.

## The question

> Can an evacuated hull weigh less than the air it displaces, and would it move water usefully to
> a fire?

The aim is for this repository to be the most checkable open study of that question: every number
regenerating from source, the model tested against aircraft that flew and against the fire season it
replays, and the float verdict published as it stands, including that nothing floats today. The
objectives below say what done means, and the milestones say when.

## The north star: the Ten-Minute Test

A sceptical stranger with ten minutes should be able to:

1. clone the repository and get green checks;
2. reproduce a published number of their choosing, change an assumption, and see why the result
   moves;
3. see the latest change with who built it, who checked it and what it cost;
4. read the float figures, each with its basis, and what would move them.

The target is a nightly run that does all four from a clean environment and publishes the result.
That run does not exist yet. Step 1 can be run by hand: `tools/stranger_run.py` clones a commit,
clears the environment and runs the main `make check` gates. The separate `floatplants`
CI target is outside that run. An earlier green run does not establish the result for a
changed tree; each run records its own gate outcomes. Step 3 is the public work log at pinkrobotics.ca/log/. Steps 2
and 4 are not demonstrated yet.

## Objectives and weights

The weights sum to 100. Work is spent in that proportion.

<!-- goals:v1: the planner will parse the rows of this table. It changes only on the director's word. -->

| id | Objective | Weight | Done means |
|---|---|---:|---|
| O1 | Truth | 25 | Every public number is generated or gated. Site and source agree, file for file. A claims register covers every page, with zero unbacked claims. |
| O2 | Verification | 25 | One energy model: the plan and the integrated flight agree within a stated tolerance, with every moved number published old and new. A suite of labelled checks against equations, published results and measurements runs in CI, and a miss is recorded, never tuned away. Every model fix re-runs the replayed 2026 season and publishes what moved. |
| O3 | Float | 20 | One generated ledger in which every float figure carries its quantity, design, altitude, safety factor, knockdown status and evidence class. The packing-fraction study landed. The deciding experiment for the current design specified. No new vehicle design before an outside structures review. |
| O4 | Visible in public | 10 | The fleet monitor tells the truth all winter. At least five product landings a week, each showing its builder, its checker and its cost. |
| O5 | A crew that plans and accounts | 15 | At least 70% of landed work originates with the planner. Cost per landing, counting abandoned work, published weekly. |
| O6 | Asked and answered | 5 | The repositories public. Three to five expert pre-reviews. Median time to dispose of an outside objection under 72 hours. This weight rises as the others are met. |

<!-- /goals:v1 -->

## Milestones

These are targets. A row is met when everything in it is true.

| Target | Done means |
|---|---|
| 2026-10-04: the front door is true | Site and source merged, and the publish check clean. Every check green from a clean environment. No visitor's browser calls any host but ours. The 2026 season replay live, with the feed contract fixed. A claims register. One energy model, with old and new figures published together. A public log of landings. |
| 2026-10-07: ready | History reviewed for anything that should not be public. Two independent secret scans. Licences settled for every file. A README a stranger can use in sixty seconds. Claims register at 100%. The float ledger and the labelled checks. |
| By 2026-10-15: public, quietly | The repositories are made public on the director's word. No announcement. |
| By 2026-10-31: asked | Expert pre-review questions sent by the director. The objection loop running: an outside objection is reproduced, then answered with a correction or a refutation, within 72 hours. The first field report. |

## The objection loop

This is the demonstration, and from the day the repository is public it is how to change a number
here. No outside objection has been through it yet.

1. Someone disputes a figure, with the file and the value they expect.
2. The crew reproduces the objection.
3. It lands a correction with a test that failed before and passes after, or a refutation with the
   run that shows it.
4. The figure moves wherever it is published, with its trace.

## Parked, with the condition that unparks each

| Track | State | Unparks when |
|---|---|---|
| Animals (a welfare-gated control architecture) | Parked. Its page lives in the site's repository. The sentences the code does not back were corrected there on 2026-10-01: it now says that no controller has been built. A plain label as vision is still owed. | An executable propose/decide kernel exists in the simulator with property tests, or the director orders the single formal note. |
| Energy as cargo (a battery-exchange chain) | Parked until the energy model lands. | The one energy model has landed; then one supply-chain analysis, and either outcome is a result. |
| New vehicle design | Frozen. | An outside structures engineer has reviewed the current design. |
| The 3D viewer | Features frozen. Bugs that make it disagree with the model get fixed; some are open today (`docs/OPEN-QUESTIONS.md`, item 16). | The director's word. |

## Rules the project holds itself to

Where a rule does not hold yet, it says so.

- **Never replay a tragedy with a better ending.** The season replay being built shows real fires
  and a simulated fleet that never flew. It must not say or imply that any fire would have burned
  differently. No replay is published yet.
- **No hindsight in the replay.** The replayed fleet may see only what was on record that day: each
  fire's status and size as known then. It never sees a fire's final size, and it never reads
  outlines drawn after the fact. This binds the replay being built. It is not a rule against
  satellite data: the live monitor uses the last day's satellite hotspots to help choose where
  along a fire's edge to drop (`sim/targets.js`), and a test holds it to that.
- **A visitor's browser talks only to this site.** True in this repository since 2026-10-01. The
  map is drawn from bundled terrain; fires, satellite heat and wind come through the site's own
  server-side mirror; no tier sends a browser to an agency's feed. `make firstparty` checks the
  served repository pages. The live site is checked separately after each deploy with
  `python3 tools/check_first_party.py <address>`; network-added loads can change without a commit.
- **No quiet fixes.** A number that moves is published old and new, with the reason. This is the
  practice from 2026-10-01; earlier history was not held to it.
- **Cost is accounting, not a headline.** When the public log exists, token, line and agent counts
  appear in it as the cost of a change, counting abandoned work, and never as a boast.
- **The crew does not speak for the director.** The crew drafts; a person sends.

## How direction changes

A change of direction is one sentence from the director. It becomes an edit to this file and one
order superseding the affected work. Work in flight stops at its next boundary, and the next daily
report opens with what changed.

Reserved to the director: the weights and objectives; making a repository public; anything sent to
people outside; a changed headline figure; money and physical work; accepting a finding unfixed;
parking a track.
The crew's: sequencing, routing between models, reviews, and landings and site deploys inside the
mission.
