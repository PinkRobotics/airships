# Architecture

The shape of the repository, and why it has that shape. Decisions that a newcomer might
otherwise relitigate have short dated entries in [DECISIONS.md](DECISIONS.md); this
document is the standing description.

The organising constraint is that the model invites attack. Everything else follows from
wanting a reader to be able to check the arithmetic without trusting the website, without
running a build, and without reading the rendering code.

---

## The map

```
index.html            the live fleet monitor — markup and styles only; the app is app/main.js
concept/index.html    how it works: the cycle, the arithmetic, the assumption dials
model-lab/index.html  the 3D development and review surface

sim/                 THE MODEL. No DOM, no network, no clock, no globals.
3d/                  the WebGL vehicle library. Its own README, tests and scripts.
app/                 the application: data, map, cockpit, bridges.
data/                 terrain, water, roads, outline, snapshots; live/ is gitignored
pipeline/             the Python generators for everything in data/
tools/                the boundary linter, golden diff, headless eval, screenshots
tests/golden/         the recorded outputs both dumps compare against
docs/                 this file, PHYSICS.md, DECISIONS.md
```

Four code areas, one direction of dependency:

```
        sim/  ─────┐            3d/
          ▲        │             ▲
          │        └────────┐    │
       concept/            app/──┘
                            │
                        index.html
```

`sim/` imports nothing outside `sim/`. `3d/` imports nothing outside `3d/`. `app/` may
import both. `concept/` may import `sim/` and `3d/`. Nothing imports `app/`.

---

## Why the model is separate and pure

`sim/` computes the simulated fleet behaviour; structural calculations live in `ship/`
and `research/analysis/`. `sim/` touches no DOM node, opens no socket, reads no clock and reads no URL. Every
function is a function of its arguments plus the shared `CFG` object.

This is not tidiness. It buys four specific things.

**It can be read.** The claim the project makes is "here is the arithmetic, check it". That
claim is worthless if checking it means reading a renderer. `physics.js` contains the basic lift and power relations. A reader who disagrees with
the project can find the line they disagree with in a minute.

**It can be run anywhere.** The same modules load in a browser, in node, and in a test
harness. `tests/golden/dump.js` runs the whole model headless. There is no environment in
which the model behaves differently, because there is nothing environment-shaped in it.

**It can be run by a stranger, in place.** `app/main.js` publishes `window.AIRSHIPS.sim`
deliberately, so anyone reading the live page can open devtools and re-run
`AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P10000, AIRSHIPS.sim.MODES.balanced, 15)`
against the same code that produced the figure above it. Arithmetic nobody can re-run is a
claim, not a calculation.

**It can be pinned.** Determinism is a property of `sim/` alone. `rng.js` holds a seed that
the page sets and the model never reads from a URL, so a golden file can compare model
output rather than pixels.

The purity rule has one visible cost, and it is worth naming. `3d/` cannot import `sim/`
either, so `3d/model/config.js` carries its own copy of the assumption set. Their shared assumptions are checked by `tests/cases/spec-parity.cases.js`. A cross-area import would fix the duplication and
would also mean the vehicle renderer could no longer be lifted out and used elsewhere,
which is the trade that was taken.

The storage ledger — the integration of per-system draw into remaining
megawatt-hours — still lives in `app/loop.js`, so model arithmetic remains in
the application layer. The cycle budget and `stateAt` now use the same force
and power calculation; the independent integral checks their agreement. See
[PHYSICS.md §Force and energy rules](PHYSICS.md#force-and-energy-rules).

---

## Why there is no build step

The browser loads the same bytes GitHub shows. No bundler, no transpiler, no minifier, no
`node_modules`, no lockfile, no generated `dist/`. Every `<script type="module">` points at
a file that exists in the repository at that path.

Anyone auditing the numbers should be able to open the network tab, see `sim/plan.js`,
open `sim/plan.js` on GitHub, and know they are looking at the same thing. A build step
puts a translation between what is published and what is reviewed, and this project's
entire proposition is that there is no such translation.

The costs are real and accepted: no TypeScript, no JSX, no npm libraries, more HTTP
requests than a bundle, and the module graph is the deployment unit. In exchange the
browser application has no package installation or bundling step; its development tools
and data sources still have dependencies.

The one place this bites is caching, which is what the version stamp is for.

---

## The simulation pages

| Page | What it is | What it imports |
|---|---|---|
| `index.html` | the live fleet monitor: map, cockpit, roster, 3D panel | `app/main.js`, which pulls `sim/` and lazily `3d/` |
| `concept/index.html` | how it works: the cycle explained, the worked example, the assumption dials | `sim/index.js` directly; no `app/` |
| `model-lab/index.html` | the 3D library's development surface: every class, mode, camera, clip, failure state | `3d/index.js` only |

The monitor and the concept page run **the same simulation**. The concept page used to
carry its own copy of the model, kept in step by hand; the two had already drifted when
that was found. Both now import `sim/index.js`, so if a figure on one is wrong the same
figure on the other is wrong in the same way, which is the only honest arrangement. When a
dial on the concept page moves it writes to `CFG` and the same `planCycle` produces the new
tiles.

The concept page cannot import `app/` — the boundary rule forbids it — so it carries a
small rendering shim of its own for the class cards, the dials and the worked example.
Only the model is shared, and only the model needs to be.

`model-lab` is `noindex` and is not part of the public argument. It exists so a change to
the vehicle model can be reviewed at a reproducible URL:
`?class=P1000&mode=cutaway-longitudinal&clip=water_fill&t=0.4&camera=cutaway-long&paused=1`.

---

## How state flows

One fetch cycle, one frame, one selected ship:

```
  BC Wildfire Service ──┐
  CWFIS satellite heat ─┼─► app/net.js ──► data/live/ mirror ──► app/feeds.js
  Open-Meteo 850 hPa ───┘                    (or direct, or data/snapshot.json)
                                                     │
                                          normalize(): fires with rings
                                                     │
                                    app/fleet.js  rebuildMissions()
                                       sixteen hulls, largest class first
                                                     │
                                   sim/mission.js  buildMission(fire, water, mode, …)
                                     ├─ assign.js   which class, and why
                                     ├─ water.js    which lake, and where over it
                                     ├─ targets.js  drop lines, scored and sequenced
                                     └─ plan.js     planCycle → durations, energy, t/h
                                                     │
                                          m.plan, m.phaseEnds, m.cycleSec
                                                     │
                             app/loop.js  frame(ts): simTime += dt × speed
                                                     │
                                    sim/state.js  stateAt(m, simTime)
                                                     │
          ┌──────────────┬─────────────────┬─────────┴────────┬───────────────────┐
          ▼              ▼                 ▼                  ▼                   ▼
   app/map/render  app/cockpit/gauges  app/cockpit/shipviz  app/bridge/viz3d   app/loop.js
   position, track   needles, dials     2D wire avatar      → 3d/ adapter      battE ledger
```

The rule that matters: **`stateAt` is the only source of "what is the ship doing right
now"**. The map, the six gauges, the phase dial, the power bars, the 2D schematic avatar,
the 3D model and the narration all call the same function with the same `simTime`. No two
surfaces can disagree about phase, altitude, heading, mass or power draw, because there is
only one place any of those come from.

`stateAt` returns a single object carrying position (`ll`, `bearing`, `alt`), motion
(`gs`, `vf`, `acc`), mass (`water`, `ln2`, `massT`), forces (`buoyN`, `weightN`, `netN`,
`vert`), power (`draw`, `gen`) and phase (`idx`, `phase`, `label`, `prog`, `sub`). Adding a
surface means reading more of that object, never computing a parallel version of it.

`vert` is the clearest example of why. It is one signed number — how hard the rotors are
holding the hull down, as a fraction of the most they ever could — and the 3D model tilts
its rotors from it, the 2D avatar draws its force arrow from it, and the power ledger
prices it. Three renderings that cannot contradict each other.

### The 3D bridge

`app/bridge/viz3d.js` is the only file that knows both the monitor and the vehicle library
exist. The library knows nothing about wildfires: `3d/adapter/fable.js` takes a mission and
a `stateAt` callback and does the unit translation. Everything page-specific — which view
suits which phase, how the camera follows a heading, how a highlight button maps to the
model's own component categories — lives in the bridge.

The library is loaded by dynamic `import()` on first use, and the monitor degrades to
hiding the panel if it fails. That is deliberate: the 3D model is illustration, and the
numbers must survive WebGL being unavailable.

### The 2D avatar

`app/cockpit/shipviz.js` draws a wireframe prolate hull with labelled force vectors on a
2D canvas. It is not a fallback for the 3D model and it is not decoration. A wireframe with
arrows can say *which way the rotors are pushing and how hard*, which a shaded render
cannot. Both are driven from the same `stateAt` output, so the schematic is an assertion
about the render, not an alternative to it.

---

## The cache-busting stamp

The 3D library's entry URL carries a content hash: `import('3d/index.js?v=a1f05b86')`. The
hash is sha256 over the stripped contents of every module in `3d/`, truncated to eight hex
characters, and it is written into `3d/version.json` and into every relative specifier
inside the library.

It exists because the module graph is the deployment unit. Without a stamp, an edge cache
can serve a new `index.js` alongside a stale `model/build.js` for hours — observed in
production as old fins, old rotors and a missing solar skin on a page whose entry point was
current. Stamping the entry pins the whole import tree, because each module's specifiers
carry the same version.

`app/bridge/viz3d.js` fetches `3d/version.json` with `cache: 'reload'` and a timestamp
query before importing, so the version lookup cannot itself be the stale link. If that
fetch fails the import falls back to `?v=unpinned`, which is no worse than having no stamp.

Two stampers exist and must agree: `3d/scripts/stamp-version.mjs` for CI, which has node,
and `3d/scripts/stamp-version.py` for this machine, which does not. Running either after
the other must be a no-op. If it is not, one of them has drifted and that is the bug.
`--check` fails when the stamp is stale.

One gap, left by the extraction and open. Both stampers look for the lab page at
`<site>/airships/model-lab/index.html`, the path it had inside the private website
repository. In this repository it is at `model-lab/index.html`, so it is neither stamped
nor checked: it still imports `../../3d/index.js?v=41bc1f51` while the library is at
`a1f05b86`, and `--check` reports clean. The path needs to become repository-relative.

`sim/` and `app/` are not stamped. They are served with the site's own cache policy and are
small enough that a stale-mix window has not caused a visible fault; the 3D library needed
the stamp because it is thirty modules deep and visually obvious when it tears.

---

## The four rules the boundary linter enforces

`tools/check_boundaries.py`, run by CI. It exits non-zero with the file and line.

**Rule 1 — the dependency direction.** The table at the top of this document, expressed as
an allow-list. `sim/` may import only `sim/`; `3d/` only `3d/`; `app/` may import `app/`,
`sim/` and `3d/`; `concept/` may import `concept/`, `sim/` and `3d/`; `model-lab/` may
import `model-lab/`, `3d/` and `sim/`; `tests/` may import `tests/`, `sim/`, `3d/` and
`app/`. Nothing else may import `app/`.

The rule protects the reason the model is separate. The moment `sim/` imports a canvas or a
`fetch`, "read the physics" becomes "read the whole site", and the golden dumps stop being
runnable headless. It is checked mechanically because it is exactly the kind of rule that
erodes under one convenient exception.

All three ways one module can name another are checked, because a rule that only sees one
of them is a rule with two doors left open:

| Form | Where it occurs here |
|---|---|
| `import … from '…'` | 240 references |
| `export … from '…'` | 40 references, every one of them in `sim/index.js` (14) or `3d/index.js` (26) |
| `import('…')` | 1, in `app/bridge/viz3d.js`, written as `import(new URL('../../3d/index.js?v=…', import.meta.url))` |

The re-export form is the one that matters most: the index files are where a directory's
public surface is assembled, so they are where a single added line would widen it. Until
2026-08-09 the linter resolved only the first form, which meant the guarantee was
unenforced in exactly the forty places it was most load-bearing. A dynamic import whose
specifier is computed rather than written — no string literal in the call — is reported
inside `sim/` and `3d/`, because a dependency that cannot be read off the source cannot be
checked by anything.

**Rule 2 — no module assigns to a binding it imported.** ES modules make imported bindings
read-only, so `SEED = 7` in a module that imported `SEED` is a runtime `TypeError` in strict
mode, not a compile error anybody notices. Where one module genuinely needs to change
another's state, the owning module exports a function that does it and the change gets a
name: `setSeed`, `setConfig`, `resetConfig`, `setAssumptions`. The linter strips comments,
strings and regex literals — keeping `${…}` interpolations, which are real code and
routinely the only call site of a helper — and then flags any assignment to an imported
name. Default and namespace imports (`import CFG from …`, `import * as sim from …`) bind
just as read-only as named ones and are covered too; an aliased import `{ CSS as STYLES }`
binds `STYLES` and not `CSS`, and only `STYLES` is flagged.

**Rule 3 — live data must be passed, not defaulted away.** `planTargets(mission, heat)`
takes the satellite hotspots as an argument so the model can run with no feed, and the
argument defaults to `[]` so that `sim/` stays runnable alone. That default is a trap for
the application: all three call sites lost the argument during the extraction, no test
noticed — the golden files are recorded in replay mode, where the sampled fleet carries no
heat-derived targets — and the page silently scored drop lines on geometry only. Inside
`app/`, the argument is required. The rule reads calls by matching brackets rather than by
regex, so `wrap(planTargets(m))` and a call split over three lines are both caught.

**Rule 4 — `sim/` reaches for no environment.** `sim/README.md` and the header of
`sim/index.js` promise "no DOM, no network, no wall clock, no `location`, no globals".
Rule 1 cannot see that promise: a module that calls `fetch` or reads `Date.now()` imports
nothing at all. So the linter also scans `sim/` for the bare identifiers `document`,
`window`, `navigator`, `location`, `globalThis`, `self`, `process`, `require`, `fetch`,
`XMLHttpRequest`, `WebSocket`, `EventSource`, `localStorage`, `sessionStorage`,
`indexedDB`, `caches`, `Date`, `performance`, `setTimeout`, `setInterval`,
`requestAnimationFrame`, `crypto`, `console`, `alert` and `Math.random`, after the same
comment and string stripping. Names reached through a dot (`state.window`) are not matched.

One allowance, listed in `ALLOWED_ENVIRONMENT` in the checker with its reason:
`Math.random` in `sim/rng.js`, which produces the default seed when the page does not pass
`?seed=`. `setSeed()` replaces it, and every published number is produced with a seed set.
Anything else has to be argued for in that dict, in public, next to the reason.

**The linter has its own tests.** Twenty-nine constructed trees, each with the exact set of
violations it must produce — exact, so a rule that starts over-reporting fails as loudly as
one that stops reporting. `python3 tools/check_boundaries.py --selftest` runs them alone;
an ordinary run does them first, so `make lint` cannot pass with a broken checker. The
reason is plain: this file is the mechanism behind the structural claims made above, and
until 2026-08-09 nothing checked it. When tests were finally written, all three of the
rules then in place turned out to have gaps between what they checked and what this
document said they checked.

---

## Determinism, and the golden files

Two URL parameters, both parsed in the application so that nothing in `sim/` needs to know
a browser exists:

- `?seed=N` → `app/main.js` calls `setSeed(N)`, pinning target order, drop-line jitter and
  phase offsets.
- `?data=snapshot` → `app/feeds.js` reads `data/snapshot.json` and `data/snapshot-heat.json`
  instead of the network, and declines to fake a wind. Replay mode is still air, and says
  so.

Together they fully determine a run. That buys a link that shows another person exactly
what you were looking at, a page that works with no network, and tests that compare
numbers rather than screenshots.

`tests/golden/` holds two recorded runs of the invented exercise (`?view=exercise`), a
committed scene that carries its own seed and its own fires. The file names keep the
earlier scene's words:

| File | Produced by | What it pins |
|---|---|---|
| `seed7-snapshot.json` | `dump.js` | every model output: the class table, the ledgers, `planCycle` over a grid of class × mode × distance × wind, the fleet allocation, `stateAt` samples, the narration, the selftest result |
| `ui-seed7-snapshot.json` | `ui-dump.js` | what the page actually renders from them |

`tools/golden_diff.py` compares a fresh dump against the recorded one.
`tools/js_eval.py URL SCRIPT.js OUT.json [WAIT]` drives a headless chromium to produce one.
The extraction of `sim/` from the original single-file page was verified this way: the
dumps are identical, which is the only reason the refactor could be called
behaviour-preserving.

Golden JSON rather than screenshot comparison is a deliberate choice — see
[DECISIONS.md](DECISIONS.md). Screenshots fail on font rendering and pass on wrong
arithmetic, which is precisely backwards for this project.

---

## Data and the pipeline

`data/` holds generated artefacts, committed: `terrain-bc.jpg`, `water-bc.json` (lake and
reservoir outlines from the BC Freshwater Atlas), `roads-bc.json`, `bc-outline.json`, and
the dated `snapshot.json` / `snapshot-heat.json` that replay mode and the golden tests use.
`data/live/` is the first-party mirror and is gitignored.

### First-party boundary

The repository's `make firstparty` gate checks loading URLs in the served files and records
browser requests against a local fixture server. It establishes what this code asks the browser
to load. The network serving the public site can alter the response after this code leaves the
repository. The monitor's first-party note therefore scans load-bearing elements and the browser's
resource log for the page, and is handed each later log entry as the browser records it, so a log
that fills up cannot hide a later request. It always states the code's own claim, names any other
host it sees, and says when the log is unavailable or was already full when the note started. It
does not say who asked for a host it names: changed code, the network in front of the site and the
browser itself look the same from inside the page. The note does not make a request. It claims only
what it checks. Outside the log are a WebSocket, a connection that has not finished, a request that
failed, a form post, a service worker's own requests, what a frame loads inside itself, and a
request to this site that the server redirects to another. A page that shrinks the log hides
entries too. This is a visible audit, not a complete network trace.

After each deploy, run `python3 tools/check_first_party.py <address>` for each published page.
It sends one browser-like HTML request per address, reports foreign loads in the returned HTML
and the `report-to` and `nel` headers, and exits nonzero for foreign loads. A plain HTTP request
may receive different HTML. This check inspects returned HTML, not requests made later by scripts;
the page's live note and the browser network panel provide that later view. The live result is
measured at the time of the request and is not asserted by this repository.

`pipeline/` holds the Python that produced them: `water.py`, `terrain.py`, `figures.py`, and
`live.py`, which is the server-side job that refreshes `data/live/`. They are not run by the
page; they are run by hand or on a timer, and their outputs are committed so that cloning
the repository gives a working page.

Feeds are read in two tiers, in order: the first-party mirror and then the committed snapshot.
The mirror exists so that traffic to this page does not become traffic to an emergency service.
The page reports the age of the data it actually shows rather than treating a reload as a new
source reading.

---

## What is published on `window`

The page is an ES module, so nothing it declares leaks. Two globals are published
deliberately, in `app/main.js`:

- `window.APP` — because the markup binds to it: row selection and phase stepping for
  reduced-motion users.
- `window.AIRSHIPS` — `{ sim, app, stateAt }`, so a reader can re-run the model and inspect
  the live application state in their own devtools.

The second one is the point of the whole architecture, reduced to one line.
