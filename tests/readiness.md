# Browser readiness waits

Navigation time does not prove that asynchronous data and route planning have
finished. The page publishes `app.ready`; accepted fleet planning publishes
`app.planning.state === 'settled'`. Wind data and its note can arrive before the
last missions finish planning. Waiting on an old `planningDone` promise also
cannot certify the current generation after a concurrent replan supersedes it.

A Chromium CPU-throttling reproduction loaded fresh wind successfully, failed
with the former ten-second predicate while planning remained pending, and then
settled after 97.225 seconds. The normal fleet budget is 300 seconds, checked
against a wall clock, with an explicit failure instead of partial
output. The corrected probe applied CPU32 after fresh wind loaded and measured 116.817
seconds for the actual wind wait. The hosted checks job slowed from 171 to 286
minutes (about 1.67 times), so the 300-second budget provides more headroom than
the initially tested 180 seconds without delaying an early successful return.
Native evidence at 180 seconds is carried for this constant-only increase;
focused virtual-clock checks validate the final 300-second predicates. It is a cooperative
page deadline: a synchronous model calculation can hold the browser event loop.

| Consumer | Wait changed and completion signal |
| --- | --- |
| `firstparty/check.py` boot | 80 to 300 s; page ready, settled planning and known wind status |
| `firstparty/check.py` wind | 10 to 300 s; ready and settled plus the mode-specific wind state/note, including stale/missing still-air replanning |
| `firstparty/check.py` held request | 10 to 300 s; drain the retained fetch promise even when a test assertion fails |
| `firstparty/check.py` note | 10 to 300 s; expected resource-observer text |
| `firstparty/check.py` transport/load | response 100 to 360 s; load event 90 to 300 s; allows the page deadline to report its own failure |
| `interaction/check.py` | 90 to 300 s; ready, nonempty exercise fleet and settled planning; reject incomplete fleet; load event 60 to 300 s and bounded 360 s responses |
| `guard/check.py` probe and heat | replace 40/30 s loops with one 300 s wait; ready and settled, or a legitimate record-only view |
| `guard/check.py` outer probe | 300 to 420 s; preserve room outside the 300 s page deadline for navigation and observations |
| `guard/check.py` layout | 20 to 300 s; actual visible first-visit overlay; begin evaluation at navigation instead of after nine seconds, before its twelve-second dismissal |
| `guard/assurance.js` | 180 to 300 s budget, use wall clock and reject pending planning even when page readiness is already true |
| `energy/fleet-envelope.py` | 50 to 300 s; ready and settled planning |
| `served-energy/page.js` | replace 30/50 s loops with a shared 300 s budget for the handle and accepted app/concept planning |
| `golden/dump.js` | replace three-second sample with 300 s readiness; current app ready and settled, or allocated classic-script plans |
| `golden/ui-dump.js` | replace four-second sample with readiness; layout 6 to 300 s, require a nonzero stable map and refuse at expiry |
| `browser/run.py` | 30 to 600 s; the completed `window.__tests` record; measured hosted interval about 246 s includes synchronous model tests |
| `exercise/capture.py` | replace five-second sample with up to 300 s; target document complete and, with scripts on, app ready and settled; static/script-disabled pages need document completion |
| `tools/check_model_lab.py` | 120 to 300 s; correct target URL, complete document, lab handle and rendered scale table; bounded 360 s transport |
| `tools/gen_operations_records.py` | 50 to 300 s; ready and settled; retain accepted-plan audit |
| `tools/gen_fallback.py` poster | replace fourteen-second sample with 300 s target-page/planning readiness; bounded 360 s transport |

Retained waits and reasons:

- `tools/fallback_dump.js`: the existing sixty-second ready/settled wait already
  fixed the exercise producer race. It stays inside the region regeneration's
  120-second outer cap; all four hosted plant shards passed with it. Its five
  delayed/absent/invalid-plan regressions remain in the fast gate.
- `interaction/check.py`: the heartbeat observation interval and 400 ms after
  overlay dismissal measure animation/rendering; they do not claim boot ready.
- `guard/check.py`: 1200 ms samples rendered text after readiness. Overlay auto
  dismissal remains application behavior, observed before it can dismiss.
- `golden/ui-dump.js`: two animation frames and 1600 ms sample the pinned clock's
  rendered panels; the explicit narration checks still reject incorrect text.
- `firstparty/check.py`: the two-second fixture hold and 250 ms observation test
  clearing wind before a reply; 200 ms network/screenshot observation and
  30/1000 ms scrolling intervals observe requests and rendering. The late-note
  injection's 50 ms loop is a deliberately asynchronous fixture, supervised by
  the bounded note wait; it is not a second readiness assertion.
- `tools/check_model_lab.py`: three seconds measures whether motion advances;
  paused and reduced-motion controls must remain still over the same interval.
- `tools/gen_fallback.py`: 2.5 s after poster setup observes rendering. No poster
  is regenerated by `--check`; deterministic simulation-time capture is separate.
- `tools/js_eval.py` and the golden driver's 16/18 s navigation samples are
  warmup intervals; the consumer now certifies actual readiness independently.
- Numeric loops in `tests/cases`, `tests/node`, `tests/energy`, geometry and
  season checks sample model/data domains, not a wall-clock readiness condition.
  Capture-tool sleeps are injected rate-limit observations, not browser waits.

The checks job limit is 360 minutes, up from 300. The measured hosted job took
286 minutes, leaving only 14 minutes at the former limit. Log command-to-next-
recipe intervals attribute about 130 minutes to the float-runner unittest
wrapper and 61 minutes to analysis freshness; these include their subcommands,
not individual-test CPU measurements. Increasing the limit gives that run
74 minutes of headroom. Splitting would change the ordered CI parity contract
and duplicate setup across jobs; the current change preserves every gate and
its ordering. The four existing plant shards keep their own 300-minute limits.
