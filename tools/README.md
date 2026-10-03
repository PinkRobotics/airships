# tools/

Development tooling. None of it is served to the web (see `dist.manifest`) and none of it
runs in a browser. The tools use Python and JavaScript; `make help`
lists the targets that wrap the ones you will use most.

The headless drivers need Chromium and `websockets`. Python dependencies are listed in
`requirements.txt`; the Makefile documents Node and PDF toolchain requirements.

`make linkcheck` checks tracked Markdown and HTML links, including anchors. It lists
external addresses without fetching them. `make noticecheck` separately checks links
in a temporary publication package. Both use `linkparse.py`.

---

## `serve.py` — the development server

    python3 tools/serve.py            # http://127.0.0.1:8875
    make serve

**Run it whenever you are working on the pages.** `python3 -m http.server` mostly works and
then wastes an hour of your life, because it sends no `Cache-Control` and answers
conditional requests with a 304. A browser holds a module graph in memory once it has
fetched it, so you edit `sim/physics.js`, reload, and re-run the old copy — the symptom is
that your change appears to do nothing. This server sends `no-store`, pins the JavaScript
and JSON MIME types instead of trusting the host's mime database, and binds loopback only.

It prints the three page URLs and the deterministic replay URL on startup.

## `check_boundaries.py` — the structural linter

    python3 tools/check_boundaries.py
    python3 tools/check_boundaries.py --selftest
    make lint

**Run it before opening a pull request; CI runs it on every push.** It enforces four rules.

1. **The dependency direction.** `sim/` imports nothing outside `sim/`, `3d/` nothing outside
   `3d/`, and nothing imports `app/`. The model is the part of this project that invites
   argument, so it has to be readable and runnable on its own. All three ways one module can
   name another are resolved: `import … from`, `export … from` and `import(…)`.
2. **No module assigns to a binding it imported** — that is a runtime `TypeError` in a
   strict-mode ES module, not a compile error, so it is the kind of thing that ships.
3. **Live data is passed, not defaulted away.** `planTargets()` must be called with its `heat`
   argument inside `app/`; the `[]` default exists for `sim/` running with no feed, and as an
   application call site it is a silent wrong answer.
4. **`sim/` reaches for no environment** — no DOM, network, storage, wall clock or `location`,
   which is what `sim/README.md` promises and what Rule 1 cannot see. The one allowance,
   `Math.random` in `sim/rng.js` for the default seed, is listed in the checker with its reason.

Every failure prints the file and the line.

`--selftest` runs the checker against twenty-nine constructed trees and asserts the exact set of
violations each produces. A plain run does the same before it reads the working tree, so `make
lint` cannot pass with a checker that has stopped checking — which it silently had: until
2026-08-09 Rule 1 resolved only the first of the three import forms, and the forty re-exports in
`sim/index.js` and `3d/index.js` went unexamined.

## `golden_diff.py` — semantic diff of two model dumps

    python3 tools/golden_diff.py tests/golden/seed7-snapshot.json candidate.json [--tol 1e-9]

**Run it when you have changed `sim/` and want to know exactly what moved.** It walks two
dumps in parallel and reports which named outputs differ and by how much, rather than that
the bytes differ. That report is what the pull request template asks you to paste and
explain, line by line.

`make golden` is the wrapper that produces the candidate dump and runs this against the
committed baseline. Reach for `golden_diff.py` directly when you are comparing two dumps of
your own — before and after a change, or two seeds.

## `js_eval.py` — evaluate JavaScript against a loaded page

    python3 tools/js_eval.py URL SCRIPT.js OUT.json [WAIT_SECONDS]

**The workhorse.** It starts headless Chromium, navigates to `URL`, waits (14 seconds by
default — the page loads data and animates before it settles), evaluates `SCRIPT.js` in the
page, and writes the returned value to `OUT.json`. It exits non-zero and prints the
exception if the script throws.

This is how the golden dumps are taken:

    python3 tools/js_eval.py \
      'http://127.0.0.1:8875/index.html?seed=7&data=snapshot' \
      tests/golden/dump.js candidate.json

`?seed=N` pins the model's random choices and `?data=snapshot` pins its inputs. Both are
required for a comparable dump; without them you are diffing two different runs.

The Chromium binary name is hard-coded as `chromium`, unlike the shell scripts in
`3d/scripts/`, which honour `$CHROME`. On a machine that only has Google Chrome, put a
symlink named `chromium` on your `PATH` — CI does exactly that.

## `screenshot.py` — load a page, collect console errors, optionally screenshot

    python3 tools/screenshot.py URL [OUT.png] [WIDTH] [WAIT_SECONDS]

**Run it to find out why a page is blank.** It reports the `<title>`, every console message
and every page error, which is usually enough: a module that 404s leaves a console error
and an empty page, and that is otherwise indistinguishable from a rendering bug. The
screenshot is optional and off unless you name an output file.

## `publish.py` — copy the served subset into the deploying website

    python3 tools/publish.py --dest DIR            # copy, reporting what changed
    python3 tools/publish.py --dest DIR --check    # change nothing; fail if the deployed copy drifted
    export AIRSHIPS_SITE_DEST=DIR                  # or name DIR once, and drop --dest

**Maintainers only; you do not need this to contribute.** There is no build step, so
publishing is a file copy plus the cache-busting stamp. What gets copied is decided by
`dist.manifest`, which must classify every top-level entry — an unclassified entry is an
error, because both defaults are wrong: serving something by accident puts a test harness
on a public host, and omitting something by accident ships a page whose imports 404.

**The destination is always yours to name.** `DIR` is the published copy, the `airships/`
directory of the website tree that deploys these pages. Pass it as `--dest`, or set
`AIRSHIPS_SITE_DEST`; `--dest` wins when both are given. With neither, the tool exits 2 and
says so: the repository carries no default, because a default would name one maintainer's
machine. `AIRSHIPS_SITE_DEST` is not `AIRSHIPS_PUBLISH_DEST`, which belongs to
`pipeline/live.py` and names where the live-data mirror is pushed.

Publishing also removes every file in `DIR` that the manifest does not list, so a page
deleted here stops being served. A wrong `DIR` would therefore lose files, and the tool
refuses a `DIR` that is this repository, lies inside it or contains it, and a `DIR` that
already holds files without being a published copy (no `index.html` beside a
`sim/version.json`). `data/live/` is never touched: the server owns it.

`--check` is the useful half day to day. It writes nothing, and it catches an edit made
directly in the deployed tree, where it would otherwise quietly become the truth. When it
reports drift, read both sides before copying either way. A drift found in 2026 held newer
wording on the deployed side and honesty labels on this side; a copy in either direction
would have lost one of them.

## `migrate/` — the one-time extraction scripts

    slice.py  extract_sim.py  extract_app.py  patch_sim.py  patch_app.py
    rewire_page.py  rewire_concept.py

**You will almost certainly never run these.** They performed one job, once: cutting the
model and then the application out of a single 8000-line `index.html` into `sim/` and
`app/`. They work by moving exact source lines rather than by retyping, so every byte of a
function body arrived in its new file exactly as it left the old one, and the seams — the
`export` keywords, the import headers — are the only new text. `patch_sim.py` and
`patch_app.py` hold the handful of edits that could not be a pure move, each one asserted
so a partial application fails loudly.

They are kept because they are the evidence for the claim that the extraction changed no
behaviour: the whole reorganisation can be re-run from the original file and audited as one
mechanism, and `tests/golden/` proves the output was identical. Treat them as a record, not
as maintained tooling — they refer to line markers in a file that no longer exists in that
shape.

---

## Related tooling that lives elsewhere

`3d/scripts/` belongs to the WebGL library and is documented in `3d/README.md`:

| | |
| --- | --- |
| `stamp-version.py` | Recomputes the library's content hash and stamps every import with `?v=`. A faithful port of `stamp-version.mjs` for machines without node; running either after the other must be a no-op, and if it is not, that is the bug. `make stamp`. |
| `browser-tests.sh` | Runs the 3D browser suite headless with software WebGL. Part of `make test`. |
| `render-figures.sh` | Rasterises the generated SVG figures with Chromium. Part of `make figures`. |
| `figures.mjs` | Generates those SVGs from the model. Needs node, so `make figures` skips it and rasterises the committed vectors when node is absent. |

`pipeline/` holds the Python that builds `data/`: `live.py` mirrors the wildfire feeds on a
timer, `water.py` and `terrain.py` build the water extract and the hillshade. `figures.py`
draws the concept page's diagrams; it imports nothing but `argparse` and `pathlib` and runs
here. `python3 pipeline/figures.py --print` reports the four figure sizes without touching
anything. See `pipeline/README.md`.
