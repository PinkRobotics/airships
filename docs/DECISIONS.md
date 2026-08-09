# Decisions

Short entries for decisions a newcomer would otherwise relitigate. Each says what was
decided, why, and what it costs. Dates are when the decision was **recorded**, not
necessarily when it was first made — much of this predates the extraction of the code into
this repository on 2026-08-08 and is written down here for the first time.

A decision recorded here is not permanent. It is a statement that the trade-off was
considered, so that reopening it starts from the reasoning rather than from scratch.

---

## 2026-08-08 — No bundler, no build step

The browser loads the same bytes GitHub shows. Every `<script type="module">` points at a
file that exists at that path in the repository.

The project's proposition is that the arithmetic can be checked. A build step puts a
translation between what is published and what is reviewed, and then checking the
arithmetic means trusting the build. Open the network tab, see `sim/plan.js`, open
`sim/plan.js` on GitHub, and it is the same file.

Costs, accepted: no TypeScript, no JSX, no minification, more requests than a bundle, and
the module graph is the deployment unit — which is what forced the version stamp on `3d/`.

Not to be reopened for developer convenience. Reopen it if the page becomes too slow to
load on a phone over a bad connection, which is a measurable condition.

## 2026-08-08 — No framework

Plain DOM, plain canvas, plain WebGL. No React, no Vue, no Svelte, no signals library.

The application is a map, a set of instruments and a table, all redrawn from one state
object at 60 Hz by an explicit `requestAnimationFrame` loop. A reactive framework's value
is in reconciling many small independent updates; this page has one update per frame,
computed by one function. There is nothing for a framework to reconcile.

Cost: the rendering code is imperative and longer than a declarative version would be.
`app/map/render.js` is 363 lines that a framework would not need.

## 2026-08-08 — No dependencies

Zero runtime dependencies, zero build dependencies, no `package.json`, no lockfile, no
`node_modules`. The Python in `pipeline/` and `tools/` uses the standard library and,
where a fetch is unavoidable, `urllib`.

Three reasons. There is no supply chain to audit, which matters for a project whose whole
argument is "check this yourself". There is nothing to rot: a clone in five years still
runs. And the 3D library in particular would have cost about 600 kB of vendored Three.js
to draw flat-shaded solids and technical linework, when the thing it actually needs —
hidden-line removal for readable engineering drawings — is a depth prepass, not a scene
graph.

Cost: `3d/render/gl.js` is a hand-written WebGL2 renderer. That is a real maintenance
burden and it was taken deliberately.

## 2026-08-08 — One simulation, shared by both pages

The monitor and the concept page import the same `sim/index.js`.

The concept page used to carry its own copy of the model. By the time anybody checked, the
two copies had already drifted, and the site was publishing two different answers to the
same question in two places. A reader who noticed would have been right to stop reading.

Now if a figure is wrong on one page it is wrong in the same way on the other, which is the
only defensible arrangement for a project that asks to be checked.

Cost: the concept page cannot import `app/` (the boundary rule forbids it), so it carries a
small rendering shim of its own for the class cards, the dials and the worked example. Some
markup-building code is duplicated. Only the model is shared, and only the model needs to
be.

## 2026-08-08 — The model is pure, and a linter enforces it

`sim/` touches no DOM, opens no socket, reads no clock, reads no `location`, declares no
globals. `tools/check_boundaries.py` fails CI if it starts to.

The rule protects the reason the model is separate. The moment `sim/` imports a canvas or a
`fetch`, "read the physics" becomes "read the whole site", and the headless golden dumps
stop working. It is checked mechanically because it is exactly the kind of rule that erodes
under one convenient exception.

The linter's second rule — no module assigns to a binding it imported — exists because that
mistake is a runtime `TypeError` in strict mode rather than anything a reader notices.
State changes across module boundaries go through named functions: `setSeed`, `setConfig`,
`resetConfig`, `setAssumptions`.

Recorded as written on 2026-08-08 and left standing, because the correction is worth more
than the tidy version: the first sentence of this entry was not true when it was written.
The linter checked imports, not purity, so nothing would have failed if `sim/` had started
reading a clock. See the 2026-08-09 entry below.

Known consequence: `3d/` cannot import `sim/` either, so `3d/model/config.js` carries its
own copy of the assumption set. Every field both files carry is pinned by
`tests/cases/spec-parity.cases.js`, because keeping them in step by hand did not work:
a P-10000 respec reached `sim/` and only half-reached the 3D copy, and the model lab
spent a day computing that hull's descent authority from a 650 MW bus while the page
used 1,550 MW. That
duplication was preferred over making the vehicle renderer depend on the wildfire model,
because the renderer is meant to be liftable.

## 2026-08-08 — A first-party mirror of the wildfire feeds, not per-visitor fetches

`pipeline/live.py` fetches the BC Wildfire Service, CWFIS and Open-Meteo feeds on a timer,
server-side, and publishes them under `data/live/`. Visitors read the mirror.

These are emergency-services feeds under real load during a fire season. A page that
fetched them from every browser would multiply that load by its own traffic, and a page
about wildfire response has no business degrading wildfire response. One fetch per interval
total, not one per viewer.

The direct feed is kept as a fallback, and the committed snapshot as a fallback below that,
so the page still works when the mirror job dies — and it says which tier it is on, with a
true fetch age rather than the reload time. Every remote source is additionally cached in
`localStorage` with a TTL matched to how often the source actually updates, so reloads and
extra tabs cost the origin nothing.

## 2026-08-08 — Golden JSON files, not screenshot comparison

`tests/golden/seed7-snapshot.json` records every model output at `?seed=7&data=snapshot`;
`ui-seed7-snapshot.json` records what the page renders from them.

Screenshot tests fail on a font substitution, an antialiasing change or a driver update,
and pass on wrong arithmetic. For this project that is exactly backwards: the pixels are
illustration and the numbers are the argument. A golden JSON diff points at
`plans[47].eCycleMWh` and says what it was and what it is now.

This is what let the extraction of `sim/` out of the original single-file page be called
behaviour-preserving rather than hoped to be. Both dumps came back byte-identical.

Cost: nothing catches a purely visual regression. That is accepted; the 3D library has its
own browser test page for the things that are genuinely visual.

## 2026-08-08 — Determinism through two URL parameters

`?seed=N` pins the model's choices. `?data=snapshot` pins its inputs.

Both are parsed in the application, never in `sim/`, so the model stays runnable outside a
browser. `rng.js` exposes `setSeed` and reads no URL itself.

Replay mode declines to replay the wind. A wind forecast cannot be honestly reconstructed
from a file, so replay is still air and the page says so, rather than presenting a stale
forecast as a current one.

## 2026-08-08 — The version stamp applies to `3d/` only

The 3D library's entry URL carries an eight-character content hash of every module in the
tree, and each module's own specifiers carry the same one, so importing the stamped entry
pins the whole graph.

It exists because the module graph is the deployment unit and an edge cache will happily
serve a new entry point alongside a stale dependency. That was observed in production: old
fins, old rotors, no solar skin, on a page whose `index.js` was current.

`sim/` and `app/` are not stamped. They are shallower, smaller, and no stale-mix fault has
been seen. If one is, they get the same treatment.

Two stampers exist — `.mjs` for CI, which has node, and `.py` for the development machine,
which does not — and running either after the other must be a no-op. Divergence between
them is a bug in the stampers, not a thing to work around.

## 2026-08-08 — British-ish spelling throughout

behaviour, metre, minimise, modelled, litre. `en-CA` number formatting.

The project is Canadian, about a Canadian province, using Canadian public data.
Consistency matters more than the particular choice; the rule is written down so it stops
being re-decided per file. Identifiers in code keep whatever spelling their upstream API
uses.

## 2026-08-08 — The vehicle naming scheme

Classes are `P-<payload in tonnes>`: P-100, P-1000, P-10000. The number is the only
specification anyone needs to remember, and it scales by decades so the three are never
confused.

Individual hulls are named for water birds, grouped so the name alone gives the class. The
P-100s are divers that take fish one at a time — Kingfisher, Tern, Merganser, Dipper,
Grebe, Loon, Swift, Petrel, Kestrel, Auklet. The P-1000s are the big scoopers — Osprey,
Pelican, Heron, Albatross, Skimmer. The single P-10000 is named for the largest wingspan
alive: Condor.

The order in `HULL_NAMES` is fixed and load-bearing. A hull keeps its name across the
fifteen-minute live-data rebuild, and the name is what keys its energy ledger in
`S.battByHull`. Reordering the list would silently transfer one ship's remaining storage to
another.

## 2026-08-09 — Known defects are documented before they are fixed

Five defects found by audit are written up with numbers in `docs/PHYSICS.md` and summarised
in `sim/README.md`, and they are being fixed in separate commits afterwards.

The alternative was to fix them quietly and publish the corrected model. That was rejected.
The project asks to be attacked; publishing a list of the places it is already known to be
wrong is the cheapest possible demonstration that the invitation is genuine, and a reader
who finds a sixth defect learns more from a project that found five than from one that
claims none.

Separate commits, because a physics correction and a documentation change should never
arrive in the same diff. Each fix changes the golden files, and the diff of the golden files
is the evidence that the fix did what it said.

## 2026-08-09 — The linter is tested, and says only what it checks

`tools/check_boundaries.py` is the mechanism behind every structural claim this project
makes about itself, and until now nothing tested it. An audit found three ways that mattered.

Its dependency rule resolved `import … from '…'` only, so `export … from '…'` re-exports and
`import('…')` were invisible — and all forty re-exports in this repository are in
`sim/index.js` and `3d/index.js`, the two files where "depends on nothing outside itself" is
the claim being made. Its success message read "sim/ and 3d/ depend on nothing outside
themselves", which is a broader statement than an import graph can support: a module that
calls `fetch` imports nothing. And its argument rule matched calls with a regex that stopped
at the first `)`, so `wrap(planTargets(m))` slipped past the check written specifically to
stop that call losing its data.

The fix was to widen the checks rather than narrow the message, on the grounds that the
message is what the project asks to be believed. The purity promise in `sim/README.md` is now
a fourth rule: a scan of `sim/` for `document`, `fetch`, `Date`, `Math.random` and the rest,
with one allowance — the default seed in `sim/rng.js` — named in the source with its reason.

The linter now carries twenty-nine self-tests, each a small tree and the exact violations it
must produce. They run on every ordinary invocation, not only under `--selftest`, so `make
lint` cannot report a clean tree using a checker that has stopped checking. That is the
general lesson and the reason this is written down: a guard with no test does not fail
loudly when it breaks, it starts passing everything, and the passing is indistinguishable
from success.

Cost: about 150 lines of test data inside the tool, and four rules to explain where the
documentation had been describing two — it had never caught up with the third, added the same
week. Both were cheaper than a reviewer discovering the gap.

## 2026-08-09 — Buoyancy is evaluated where the ship is, and the hulls are sized for the worst of it

`ledger()` used to compute displacement lift at sea-level density and hand the answer to
every altitude. It now takes an altitude in metres above mean sea level and has no default,
so a caller that has not decided where the ship is gets an exception rather than a wrong
number. Density comes from `sim/atmosphere.js`, the ISA troposphere, with its constants
sourced to ISO 2533:1975 and tested against the published table rather than against itself.

Two constants carry the decision and both are in `sim/config.js` where a reader meets the
class table: `TERRAIN_MSL` = 1,000 m, one reference elevation for the interior plateau, and
`WORK_ALT_MSL` = 2,500 m, the cruise ceiling above it. `planCycle` sizes at the second;
`stateAt` uses the ship's own altitude at every instant.

The hulls were then resized to a requirement rather than to the defect: FAIL-SAFE FLOAT-UP,
positively buoyant at the working altitude while fully loaded with water it cannot drop, with
a stated 5% margin. Nitrogen is excluded from that mass because it vents in seconds; water is
the load a ship can be stuck with. Displacement is 2,200 m³ per tonne of payload, +22.2%, and
the margin comes out at +5.25% identically on all three classes because dry mass is set equal
to payload on all three. The `ln2CapT` tanks were resized on the same principle — enough
nitrogen to LAND an empty hull with no rotor authority, checked at the ground where the air is
densest rather than at the ceiling where the descent starts.

Flying lower was available as relief and was not taken. The terrain envelope is stated in
`sim/config.js`: the interior fire belt burns between valley floors at 300–500 m and treeline
near 2,100 m, with local summits to about 2,320 m, and a 2,500 m ceiling clears all of it.

Costs, accepted: every published size moved, the vacuum shell has 14% more area to cover
within an unchanged mass allowance, and cruise drag rose 14% on every class. The first is the
hardest number in the project and this made it harder. That is the price of a safety property
and it is charged rather than netted off.
