# Contributing

This project publishes arithmetic so that the arithmetic can be attacked. A correction that
removes a number we liked is worth more than a feature. What follows is what makes a change easy
to accept.

## Running it

```sh
python3 -m http.server 8875        # from the repository root
```

Open <http://127.0.0.1:8875/>. No build step, no bundler, no dependency to install. Every page is
static HTML importing ES modules directly, and that is a constraint, not an accident: a reader who
wants to check a figure should be able to read the file that computes it without first
reconstructing a toolchain.

Useful URLs while working:

| URL | What it gives you |
|---|---|
| `/index.html?seed=7&data=snapshot` | the pinned run the golden files were recorded from |
| `/index.html?selftest=1` | runs `sim/selftest.js` on load; result goes to the console and the title |
| `/concept/` | the assumption dials and the worked example |
| `/model-lab/?class=P1000&mode=cutaway-longitudinal&clip=water_fill&t=0.4` | the 3D lab, reproducibly |

## Running the tests

**Structural rules.** Fast, no browser:

```sh
python3 tools/check_boundaries.py
```

**The model's own assertions.** `sim/` has no browser dependency, so it imports under node
unchanged. CI runs:

```sh
node --input-type=module -e "import('./sim/index.js').then(m => console.log(m.selftest()))"
```

Node is required for the full check, but not for viewing the pages. Without it, run the same assertions in the browser by
opening `/index.html?selftest=1`, or call `AIRSHIPS.sim.selftest()` in devtools on any page that
loads the model. It is the same seventeen checks either way.

**Golden outputs.** Two dumps, one for the model and one for what the page renders. Both need the
server running, headless Chromium available, and `TMPDIR` set to a writable scratch folder:

```sh
python3 tools/js_eval.py "http://127.0.0.1:8875/index.html?seed=7&data=snapshot" \
        tests/golden/dump.js "$TMPDIR/airships-dump.json" 16
python3 tools/golden_diff.py tests/golden/seed7-snapshot.json "$TMPDIR/airships-dump.json"

python3 tools/js_eval.py "http://127.0.0.1:8875/index.html?seed=7&data=snapshot" \
        tests/golden/ui-dump.js "$TMPDIR/airships-ui-dump.json" 20
python3 tools/golden_diff.py tests/golden/ui-seed7-snapshot.json "$TMPDIR/airships-ui-dump.json"
```

Both must print `IDENTICAL` unless you meant to change behaviour. `golden_diff.py` reports which
figure moved and by how much, not that bytes differ; it exits non-zero on any difference and takes
`--tol` for a relative tolerance.

Write the dumps somewhere outside the working tree so they cannot be committed by accident. The
model dump is about 300 kB; the UI dump is a couple of kilobytes.

**The 3D library.** `3d/` has its own suite, its own conventions and its own README. Its commands
are written to be run from inside that directory:

```sh
cd 3d
node --test "tests/*.test.mjs"           # unit, model, physics, adapter, geometry
node scripts/audit.mjs                   # containment and interference, all three classes
node scripts/stamp-version.mjs --check   # module URLs are versioned
scripts/browser-tests.sh                 # DOM and WebGL integration, headless
node scripts/figures.mjs --check         # the committed figures still match the model
```

Read [3d/README.md](3d/README.md) before changing anything under `3d/`.

## The four structural rules

`tools/check_boundaries.py` enforces exactly four things. It is short enough to read, and it is the
whole linter.

**Rule 1 — the dependency direction.** `sim/` imports nothing outside `sim/`. `3d/` imports nothing
outside `3d/`. `app/`, `concept/` and `model-lab/` may import `sim/` and `3d/`. `tests/` may import
`sim/`, `3d/` and `app/`. Nothing else imports `app/`. The matrix is the `ALLOWED` dict at the top
of the checker.

The reason is the whole point of the repository. The model is the part that invites argument, so it
has to be readable and runnable on its own. The moment `sim/` imports a canvas or a `fetch`, "read
the physics" becomes "read the whole site", and the invitation to check the numbers stops being a
real one. This is also what lets `sim/` run in node, in a test, and in a console on the live page
with no adaptation.

All three ways of naming another module count: `import … from '…'`, `export … from '…'` and
`import('…')`. The re-export lines in `sim/index.js` and `3d/index.js` are the ones to watch — they
are where a directory's public surface is assembled, and until 2026-08-09 the checker did not look
at them at all.

**Rule 2 — no module assigns to a binding it imported.** ES modules make imported bindings
read-only, so a cross-module write is a runtime `TypeError` in strict mode — a failure you find
when a user hits it, not when you compile. Where one module genuinely needs to change another's
state, the owner exports a function that does it and the change acquires a name. `CFG` is the worked
example: it is one object for the lifetime of the module, never reassigned, and it is changed
through `setConfig` and `resetConfig` so that a typo throws instead of silently creating a tunable
nobody reads.

**Rule 3 — live data must be passed, not defaulted away.** `planTargets(mission, heat)` defaults
`heat` to `[]` so `sim/` runs with no feed. Inside `app/` the argument is required, because a call
site that forgets it does not fail — it quietly scores drop lines on geometry alone, which is
exactly what happened during the extraction and what no test caught.

**Rule 4 — `sim/` reaches for no environment.** No `document`, `window`, `fetch`, `localStorage`,
`Date`, `setTimeout`, `console`, `Math.random` or the rest of the list in `ENVIRONMENT` at the top
of the checker. This is the promise `sim/README.md` makes, and Rule 1 cannot see it: calling `fetch`
imports nothing. The single allowance is `Math.random` in `sim/rng.js`, which makes the default
seed; it is listed in `ALLOWED_ENVIRONMENT` with the reason. If you need a clock or a random number
in the model, take it as an argument.

All four rules are mechanical. If the checker says you broke one, you broke one.

The checker is also the only thing standing behind those claims, so it has its own tests:
`python3 tools/check_boundaries.py --selftest` runs twenty-nine constructed trees and asserts the
exact set of violations each one produces. A plain run does the same before it looks at your work.
If you change a rule, add the case that would have caught the old behaviour.

## Comment and prose style

Plain, exact, unhedged. Say what a thing is and why it is that way. Never narrate what the next
line does — the line already does that.

- A comment earns its place by carrying information the code cannot: the reason a constant is that
  value, the bug that made the clamp necessary, the assumption a formula rests on.
- Write sentences that survive being quoted by a hostile reader. If a claim needs a qualifier, put
  the qualifier in; if a number is uncertain, say so and say by how much.
- British-ish spelling throughout: behaviour, metre, minimise, modelled.
- No emoji. No exclamation marks. No marketing voice. "Demonstration assumption" is the honest
  label for most of `config.js`, and it is used.
- Units in the comment when the name cannot carry them. The model is SI internally — kg, m, s, N, W
  — and surfaces tonnes, km, minutes, MW and MWh.

Existing comments in `sim/plan.js` and `sim/state.js` are the reference. They explain overlap
doctrine, why a leg is a trapezoid rather than a step, and why heading accumulates through a 180°
reversal. None of them says what the next line does.

## What a good pull request looks like here

**A physics objection is the most welcome kind, and it comes with a number.** Not "the drag model
is wrong" but: here is the coefficient I think is right, here is the reference or the calculation
behind it, here is what `planCycle(CLASSES.P10000, MODES.balanced, 15)` returns before and after,
and here is which published figure on the site changes as a result. An objection with a number
attached can be checked in an afternoon. One without cannot be checked at all.

You do not need to clone anything to produce that. Open the live page, open devtools, and call
`AIRSHIPS.sim.planCycle(...)` or `AIRSHIPS.sim.setConfig({Cd: 0.09})` and re-run. Paste what you
got.

**Any change under `sim/` must show the golden diff and explain every changed figure.** The
extraction of the model into `sim/` is proven behaviour-preserving against `tests/golden/`; that
proof is the repository's only defence against silent drift. So:

1. Run both golden dumps and paste the `golden_diff.py` output into the pull request.
2. For each figure that moved, say why it moved and why the new value is the right one. "Cycle
   energy fell 12% because the letdown window no longer double-counts the return leg" is an
   explanation. "Numbers changed" is not.
3. Update the baselines in the same commit, so that the recorded diff and the new baseline land
   together and a reviewer can see both.
4. If a change is meant to preserve behaviour, the diff must be empty. Say so explicitly.

**Other things that make a change easy to accept:**

- One concern per pull request. A physics correction and a rendering change in the same diff is two
  reviews wearing one hat.
- If you fix one of the defects listed in the README, say what it does to the published figures.
  Several of them will make the concept look worse. That is fine and expected; the numbers going
  the wrong way is not a reason to reject a correction.
- Documentation-only and comment-only changes are welcome and need no golden diff, but they must
  still be true. A comment asserting something the code does not do is a defect.
- New assumptions go in `sim/config.js` with their units and the word "assumption" where that is
  what they are. A magic number inline in a formula will be asked about.
- Keep `sim/` pure. No DOM, no network, no wall clock, no `location`, no globals, no
  `Math.random` outside the one seeded initialiser in `sim/rng.js`. Determinism is a feature that
  several other features depend on.

## Reporting something that is not a pull request

Open an issue. A defect in the model, a data source we have mis-attributed, or a claim on the page
that the code does not support are all worth an issue on their own. Security reports go the way
[SECURITY.md](SECURITY.md) describes. Conduct is covered by
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
