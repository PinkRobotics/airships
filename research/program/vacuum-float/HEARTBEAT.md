# Vacuum Float heartbeat and stall-cap mechanism — U3 definition

Status: unit-specific six-hour mechanism DEFINED, implemented and bound
(U3-BOUND-BINDINGS-DISPOSITION-1017): ledger, source, owner, routes and the
six-hour allocation are resolved. **ACTIVATION BLOCKED** (see the end of this
file and [OPERATIONS.md](OPERATIONS.md)). Nothing here is a deployment
receipt.

## Mechanism

`tools/float_progress.py --ledger <owned-dir> heartbeat` is the entry point.
One run:

1. Regenerates the scoreboard from the ledger's events and writes
   `scoreboard.json` atomically — the full board object carrying the exact
   scoreboard `line` and `generated_at`, one file, no partial reads.
2. Evaluates the delivery queue in `<ledger>/delivery-pending.json` and
   delivers through the posting adapter (`--post-command` argv, one JSON
   object per item on stdin): the scoreboard line when it differs from the
   LAST ADMITTED line, plus any due stall notices. Delivery contract:
   - **stable ids, allocated at creation**: `vf-line-<seq>-<sha8(line)>` for
     lines (the seq comes from `delivery-pending.json` and never reuses a
     number), `vf-stall-<sha8(episode_key)>-48h` and
     `vf-stall-<sha8(episode_key)>-5d` for notices;
   - **frozen envelopes**: the adapter (`tools/float_post.py`) resolves the
     addressee from the runtime binding ONCE, freezes the full envelope in
     its owned delivery state BEFORE the first submission, and reuses it
     verbatim on every retry — addressee and deadline are never re-resolved;
   - **admission is proven, not printed**: a delivery counts only when the
     stored submission carries the same AUTHORED fields (queue timestamps
     and ingest metadata are not authored). An earlier identical admission
     of the same id is success; a conflicting payload under the same id is
     an error (fail closed);
   - **bounded attempts**: at most three adapter calls per run
     (`HEARTBEAT_MAX_POST_ATTEMPTS`), each held to 150 s
     (`HEARTBEAT_POST_TIMEOUT_S`); the adapter itself holds submit.py to
     120 s. Priority order: the 5-day admiral-decision card first, the 48 h
     diagnosis second, then the oldest pending line. Items that do not fit
     the budget stay PENDING — nothing is ever dropped or abandoned;
   - **failure is loud**: any due item left undelivered (including
     budget-deferred ones) exits nonzero, so the service unit's OnFailure
     pages the host instead of passing silently. Retries happen only on the
     next scheduled run — never in an in-run polling loop;
   - an unchanged, already-admitted line causes no seat work: no post, no
     wake, no action request, no Admiral message.
3. Evaluates the stall clocks (below) and emits threshold notices,
   idempotently per stall episode. The 5-day card's DATE is frozen at first
   creation (creation + 48 h) and retained verbatim on every late retry — a
   late delivery never recomputes the decision deadline.
4. Never awards anything. A heartbeat cannot mint points, verify science or
   reset a scientific stall.

Without `--post-command` the run is a probe: it regenerates, records pending
delivery items and exits 0 — useful for inspecting what WOULD be delivered.
The service unit always passes the adapter.

## Adapter exit codes (`tools/float_post.py`)

| rc | meaning | heartbeat treatment |
|---|---|---|
| 0 | admitted now, or an earlier identical admission verified | item admitted |
| 2 | CONFLICT: the same id carries a different authored payload | operator; item stays pending, admission revoked |
| 3 | submit.py refused (its documented rc 1) — a definite no | kept pending, reported |
| 4 | no admission evidence: crash, odd exit, timeout, or filed nothing | kept pending, retried next run |
| 5 | addressee binding unresolved — nothing filed | kept pending until the binding exists |

## Timer

The cadence is six hours at :13 past the hour (`00/6:13`), driven by a
`systemd --user` timer on the host — NOT a new ship queue or lifecycle
daemon. The unit definitions in `ops/systemd/user/` are the deliverable
(`vacuum-float-heartbeat.service` and `.timer`, sha-verified against the
Operations artifacts); installing and enabling them is the activation step,
which stays blocked until the handoff names land. Installation steps and
rollback live in the service file's comments and in
[OPERATIONS.md](OPERATIONS.md).

## Stall caps (events, not clocks)

The anchor is the accepted Sciences execution brief to a READY builder —
the programme-start anchor — and after the first verified map point, the
LAST admitted Una-verified map point (its accepted event id is the next
episode key). Nomination, landing, cost update, heartbeat or retry never
resets a scientific stall.

- At **48 h** without a verified map point: ONE diagnosis report to the Desk,
  through the CO's existing reporting route (`asks: reply`, next: carry to
  the Desk).
- At **5 days**: an admiral-decision card with DEFAULT pause, routed through
  the CO as a typed admiral-decision with DEFAULT and the frozen DATE.

Each threshold notification is idempotent for its stall episode: a duplicate
heartbeat cannot re-emit it or repeatedly wake recipients. Notices are
mechanism artifacts under `<ledger>/notices/` carrying the frozen DATE; the
delivery route files them through the queue. Historical episodes are
retained in `heartbeat-state.json` after a subsequent verified point re-arms
the clocks. The default is not permission to act: the mechanism stops no
seats, kills no jobs, retires no workers and changes no custody. A due-by is
a stall cap, not a reason for a worker to sleep.

## Activation

**ACTIVATION BLOCKED**, recorded verbatim in every `status`/`heartbeat`
output. The bindings resolved ledger, source, owner (Sciences), routes and
the timer allocation; the remaining gates and their owners:

| missing item | owner |
|---|---|
| Una verification/sign-off of the U3 candidate | Una |
| landing on the CO's order | the CO |
| measured install of service + timer | Operations (on the CO's order) |

Until they land, the delivered mechanism runs only by explicit invocation,
files nothing and substitutes no direct runtime writes. Sciences decides
disposition and any further issue.
