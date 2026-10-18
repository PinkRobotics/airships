# Vacuum Float progress ledger — event schema and authority contract

Status: U3 delivery, schema version 1. Machine-readable companion:
[schema.json](schema.json). Initial configuration template:
[state-initial.json](state-initial.json). Operations and activation:
[OPERATIONS.md](OPERATIONS.md); six-hour mechanism: [HEARTBEAT.md](HEARTBEAT.md).

This is plumbing, not science. The ledger records nominations, verified
results, scorer decisions and derived views as SEPARATE things; a software
PASS, ledger entry, signature or landing is never a validated map point. Una
(the XO seat) alone verifies and awards under
[POINTS.md](../POINTS.md); Sciences and builders cannot move the scoreboard on
their own assertions.

## Ledger layout

The ledger lives in an OWNED directory passed explicitly on every invocation
of `tools/vacuum_progress.py --ledger <dir>` — never inside this repository and
never a hard-coded runtime path:

```
<dir>/events.jsonl          append-only event log, one canonical-JSON object per line
<dir>/ledger-state.json     map/rubric version, verifier seats seen, activation record
<dir>/ledger.lock           flock serializing every read-modify-write
<dir>/scoreboard.json       derived, regenerated: the full board carrying the exact line + generated_at, written atomically
<dir>/scoreboard.line       derived single line, rewritten only when it changes
<dir>/heartbeat-state.json  mechanism state: last regenerated line, last admitted line, pending delivery ids, run count, stall episodes
<dir>/delivery-pending.json delivery queue: next line seq + pending items (stable ids, frozen bodies and deadlines, attempt receipts)
<dir>/notices/              stall artifacts (48 h diagnosis, 5-day decision card with its frozen DATE)
```

The initial production state is EMPTY: no events, UNVERIFIED margin, UNKNOWN
material gap, zero points. No fabricated points, awards, material cards,
carry-in margins or convergence claims. Test fixtures are unmistakably
synthetic and never seed the production ledger.

## Events

Every event carries: stable `event_id` (`q-<accepted submission id>` for
queue-derived events); `event_type`; `from_seat` (the accepted record's
admitted filer); `lane` and `model` attribution; `map_version` and
`rubric_version` context at ingest; `event_at` (the accepted record's own
timestamp) and `ingested_at` (excluded from the replay digest); source
commit/tree when available; the canonical `authority` reference; typed
`result`/value/units/uncertainty fields where present; and evidence references
with hashes. Missing evidence stays explicitly unavailable — never zero, never
inferred.

Event types:

- **nomination** — any accepted filing that is not verifier authority. Never
  carries points, never verified, always reported with its precise reason.
- **verification-award** — Una-verified award of a POINTS.md kind. `points`
  must equal the rubric row (`tokens-100m` scales by `units`); a mismatch is
  refused and stays a nomination. `benchmark` requires a `benchmark_key`.
- **audit-zero** — verifier-filed; names `lane` and `map_version`. Zeroes the
  named lane's CURRENT map version only, as a new scoped event. Prior awards,
  evidence and earlier map versions are preserved. A stale or mismatched map
  reference is recorded and NOT applied to a newer map.
- **map-version** — verifier-filed; advances the current map version,
  forward-only.
- **rubric-change** — verifier-filed; advances `rubric_version` forward-only,
  at most one change per map version, and must reference accepted approval
  records from BOTH Una and an Admiral seat. Existing awards keep their
  original rubric version; there is no retrospective rescoring.
- **cost-update** — any seat; session-keyed token accounting (`result.session`
  names the native record, `tokens` its CUMULATIVE total; `coverage`
  `measured` | `unmeasured`; optional `bucket: overhead` with `role`
  `sciences-head` | `scorer` | `scorer-rerun` | `co` | `review`). Never an
  award and never points. The view keeps the latest snapshot per session — a
  redelivered or stale record never double-counts — and sums sessions per
  lane; a late-found record adds in when found.

A validated scientific point (kind `map-point`) must refer to the closed-form
candidate, mesh-converged FEA eigenvalue/nonlinear seeded-imperfection
evidence and the stated agreement tolerance the redirect requires, as accepted
by Una. The mechanism does not substitute an algorithmic plausibility check
for her verification. A verified FAIL may be a map point and is never
relabelled a successful floating design.

## Append-only invariants

- Identical replay of an already-accepted event is a no-op.
- The same `event_id` with a different payload is refused — no second award,
  no silent overwrite.
- Corrections and revocations append their disposition and explicitly
  reference earlier events; originals and historical views are preserved.
- A torn final line is an interrupted append: excluded from every view and
  reported until `repair-tail` removes the uncommitted bytes. An interrupted
  append can never leave a fabricated committed award.
- All mutations hold an exclusive `flock` for the whole read-modify-write, so
  heartbeat and manual runs cannot interleave or double-ingest.

## Authority contract

The initial authority adapter reads ACCEPTED queue submissions read-only, by
exact id, from the ship's submissions directory (see state-initial.json;
default `/home/tyler/data/helm/ship/queue/submissions`). It uses the queue
writer's admitted `from_seat` and never writes runtime records or trusts a
caller's substitute JSON.

A filing becomes a verification event only when BOTH hold:

1. The filer is Una: a seat in the configured `verifier_seats`, or the CURRENT
   binding principal for the verifier billet (`binding/xo.json`
   `principal.seat`), or a seat the ledger has already accepted verifier
   authority from — a later succession never invalidates a historical
   authority record.
2. The record carries an explicit typed block: record `scope` with
   `programme: vacuum-float` and an `award` object, or an artifact named with
   path and sha256 whose JSON `type` is `vacuum-float-award`. A digest
   mismatch is never trusted.

Anything else — a builder's report, a mismatched digest, an award whose
points contradict the rubric, a control block missing its required fields —
stays an unverified nomination with the precise reason recorded in
`status`/`scoreboard`.

## Derivation and caps

Scoreboard, balances and current-map views are derived from events on every
run. Caps are derivation properties, so no new id, replay or map-version
rollover can widen them:

- `benchmark`: credited once ever per `benchmark_key`; duplicates are listed
  uncredited.
- `falsification`: at most 3 per ROLLING 168 hours per lane; excess listed
  uncredited.
- `material-card`: at most 5 per ROLLING 168 hours per lane; excess listed
  uncredited.

The cap window is fixed by the Scorer conventions (v0) — Una's disposition of
2026-10-17, carried in [POINTS.md](../POINTS.md): a rolling 168 hours of exact
instants keyed on the verification instant (UTC, closed interval; no
timezone, no calendar week, no boundary to stack across). An over-cap event
is still verified and still occupies its window, so stacking can never outrun
the cap and a cleared window reopens it; it scores 0, is never banked, never
rolled into a later window and never rescored. Caps count PER LANE (the
builder plus its workers and successor relief); the per-model leaderboard
attributes awards to the producing model while the caps stay per-lane.

Margin and material gap move ONLY on verified `map-point` /
`scoreboard-improve` events; until one exists the scoreboard reads UNVERIFIED
and UNKNOWN. A six-hour regeneration does not manufacture a verified result.

## Cost honesty and the token penalty

Measured zero cost is distinct from unavailable cost. Provider, lane/model,
interval, units and coverage are preserved; cumulative snapshots are not
added; pooled spend is not automatically this lane's spend; unknown cost is
not zero. The count of admitted map points is tracked SEPARATELY from the
rubric score: one +10 map point is one point identity, lifetime totals are
correction-adjusted, an audit-zero withdraws the current map's count
explicitly (the number withdrawn is recorded), and benchmarks, penalties and
other kinds never create or destroy point identities. Cost per validated map
point appears only with an agreed accounting basis AND a non-zero admitted
map-point denominator — a zero denominator yields an unavailable ratio, never
infinity, zero cost-per-point or invented efficiency.

The token penalty follows Scorer conventions (v0) section 2 (see
[POINTS.md](../POINTS.md)): the lane basis is every token its sessions
processed per their native records (all input, cached and uncached, plus all
output; counted once per assistant message id; no provider weighting),
cumulative for the life of the programme and never reset by week or map
version. Usage of the Sciences head seat, the scorer and her re-run
sub-workers, the CO and the external review round is NOT charged to any lane:
it is reported as programme overhead beside cost per point. A session with no
readable native record is UNMEASURED, named in the coverage line, never
zero-filled or estimated.

Each crossing of a 100M-token multiple is observed by the ledger and dated at
the regeneration that first sees it, attributed to the map version current
then; observation dates are recorded once, never rewritten, and a record
found late adds its crossing when found. The penalty POINTS come only from
Una-verified `tokens-100m` awards — the mechanism never mints them — so
observed-but-unawarded crossings are displayed as pending discrepancies for
her disposition. Symmetrically, an award above the observed crossings is
never refused or rescored: the excess is surfaced as a displayed over-award
discrepancy for her disposition.

## Delivery contract (heartbeat publications)

Heartbeat output is filed through the delivery adapter, never written to the
runtime directly. Every deliverable — a changed scoreboard line, a 48 h
diagnosis, a 5-day decision card — becomes a pending item with a STABLE id
(`vf-line-<seq>-<sha8(line)>` with a seq allocated at creation and never
reused; `vf-stall-<sha8(episode_key)>-48h` / `-5d`). The adapter resolves the
addressee from the runtime binding once, freezes the full envelope before the
first submission and reuses it verbatim on retry; the 5-day card's DATE
(creation + 48 h) is frozen at first creation and kept on late retries.
Admission is proven by the stored submission's COMPLETE authored projection
— a printed SUBMITTED proves nothing. Every expected key must be PRESENT
(the door writes authority/re/supersedes as explicit nulls, so absence is a
conflict); values compare by recursive TYPE-SENSITIVE JSON equality, where
bool/int and float/int are distinct types and drift nested inside containers
still rejects; only the door's documented stamps (at, ingested, from_seat,
_vouched, links_schema, _intake_deferred, admiral_seat) are excluded;
conditional keys the envelope never authored must be ABSENT; and any stored
key outside the envelope plus door contract is an unexpected authored field
that rejects. The receipt names the actual compared fields. An earlier
identical admission of the same id is success, and a conflicting payload
under the same id fails closed. The delivery state itself is validated at
load before any adapter call, cursor recovery or write: id/type nonempty
strings, body a nonempty string, a notice's episode key nonempty, attempts
(when present) a nonnegative integer never a boolean — absent keeps the
documented zero default — created_at (when present) a string, the 5-day
card's deadline a MANDATORY timezone-aware ISO string, and any optional
deadline on a line or diagnosis equally aware ISO when present. At most
three adapter calls per run in priority order (5-day card, 48 h diagnosis,
oldest pending line), each time-bounded; anything left undelivered stays
pending and exits nonzero for the timer. Exit codes, service units and
activation gates:
[HEARTBEAT.md](HEARTBEAT.md), [OPERATIONS.md](OPERATIONS.md).
