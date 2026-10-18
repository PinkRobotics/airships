# Vacuum Float progress machinery — operations

Status: U3 delivery. Schema and authority contract: [SCHEMA.md](SCHEMA.md).
Six-hour mechanism and activation state: [HEARTBEAT.md](HEARTBEAT.md).

## Tool

`tools/float_progress.py` — the progress script. Stdlib-only Python 3. Every
invocation names its OWNED ledger directory explicitly; the repository and
the ship runtime are never written. `tools/float_post.py` is the delivery
adapter the heartbeat calls through `--post-command`: it resolves the
addressee from the runtime binding once, freezes the envelope in its owned
delivery state, files through the ship submit door and proves admission by
comparing the stored submission's authored fields (exit codes 0/2/3/4/5 —
see HEARTBEAT.md).

```
python3 tools/float_progress.py --ledger <owned-dir> ingest --id <accepted-submission-id> [...]
python3 tools/float_progress.py --ledger <owned-dir> scoreboard [--out LINE] [--json-out JSON]
python3 tools/float_progress.py --ledger <owned-dir> heartbeat [--post-command <argv...>]
python3 tools/float_progress.py --ledger <owned-dir> status
python3 tools/float_progress.py --ledger <owned-dir> selfcheck
python3 tools/float_progress.py --ledger <owned-dir> repair-tail
python3 tools/float_progress.py schema
python3 tools/float_post.py --runtime <ship-runtime> --submit <submit.py> --delivery-state <owned-dir>
```

`--config <json>` overrides the defaults in
[state-initial.json](state-initial.json); `--binding-dir` overrides the ship
binding directory used for canonical verifier resolution.

- **ingest** reads accepted queue submissions read-only by exact id and
  appends the event each maps to (verification event, control event or
  nomination). Identical replay is a no-op; a conflicting payload under the
  same event id is refused. A torn final line is reported and excluded.
- **scoreboard** derives and prints the single scoreboard line; optionally
  writes the line and the full JSON to paths you own. A regeneration also
  records, once and never rewritten, the instant it first observes each new
  100M-token crossing per lane (with the map version current then); observed
  crossings pend as displayed discrepancies until Una's verified
  `tokens-100m` award — the mechanism never mints them.
- **heartbeat** is the six-hour mechanism run (see HEARTBEAT.md).
- **status** prints the ledger summary, activation record, verifier seats,
  unverified nominations with precise reasons, and the scoreboard.
- **selfcheck** re-verifies ledger invariants (unique ids, rubric-conformant
  points, control-event shapes, no torn tail); nonzero exit on violation.
- **repair-tail** truncates one torn final append — uncommitted bytes only.

## Event route (unchanged by this machinery)

A point or benchmark is filed to Una; her canonical verification/award drives
the ledger; a finding is scored only through its admitted authority. A first
validated point or benchmark PASS reaches the Desk through the CO's existing
reporting route. This mechanism never bypasses that route with a
self-authored award.

## Execution envelope

Every execution job runs inside the CO's enforced slice — at most 8 CPU,
40 GiB, 2 h wall — via a named `systemd-run --user --scope` with
`CPUQuota=800%`, `MemoryMax=40G` and a two-hour timeout (smaller bounds
where sufficient, never larger). Example for the focused checks:

```
systemd-run --user --scope -p CPUQuota=800% -p MemoryMax=40G \
  --setenv=TMPDIR=/home/<you>/run/tmp \
  timeout 7200 python3 -m unittest discover -s tools/tests -p 'test_float_progress.py' -v
```

Working trees, scratch, temporary output and results live on `/home`
filesystem run directories — never `/tmp`, `/mnt/scratch` (tmpfs) or the
full `/mnt/24TB-A`/`B` archives. Record actual limits, argv, owned
cwd/interpreter, source identity, start/end, rc and cleanup for each job; do
not silently fall back to an unenforced process or retry an exhausted
allowance. One heavy job at a time per builder, never beside a full suite.
No GPU. No physical work.

## Focused checks

```
python3 -m unittest discover -s tools/tests -p 'test_float_progress.py' -v
python3 -m unittest discover -s tools/tests -p 'test_float_post.py' -v
```

Tests use temporary owned directories and injected time/posting adapters;
they send no real queue messages, alter no live ledger and wait for no real
clock. The adapter tests run the real `float_post.py` as a subprocess against
a fake submit door and admission store inside the owned temp dir — no real
queue filing ever happens. Fixtures are unmistakably synthetic.

## Installation and activation state

**ACTIVATION BLOCKED.** The mechanism is delivered reviewable and inert. The
U3 bindings resolved what the earlier handoff left open: the ledger and
source (this repository), the permanent owner (Sciences), the delivery
routes (line → sciences billet information-only; 48 h diagnosis → CO, asks
reply; 5-day card → CO, typed admiral-decision) and the timer allocation
(six hours at :13 past the hour, `Persistent=true`). The tracked units in
`ops/systemd/user/` carry the install and rollback steps in their comments.
Still missing before activation:

1. **Una verification/sign-off** of the U3 candidate;
2. **landing** of the source on the CO's order;
3. **measured install** of the service and timer by Operations.

Every `status` and `heartbeat` output carries this blocker verbatim until the
items are supplied; the delivered default posts nothing and writes no runtime
record. A tracked schema or timer definition is not a deployment receipt.
Live publication or installation uses the sanctioned adapter/installer only.
Sciences decides disposition; there is no indefinite polling and no waiting
on another seat to resolve it.

## Custody record

One unit custody record is kept with source pins and concise execution
evidence — candidate commit/tree/base, owned diff and file list, focused test
commands and results, authority-adapter details, the empty production
starting state, and the labelled activation blocker. Repeated inventories and
provenance stacks are explicitly out of scope.
