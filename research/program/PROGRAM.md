# Programme

Status: standing programme, redirected 2026-10-13. The target is an airship that floats,
confidently. This document sets direction and delivery; it establishes no new scientific
result or qualification. No aircraft has been built or flown.

`not shown · margin UNKNOWN · confidence UNKNOWN · weakest assumption: required structural mass`

## Scope and authority

The 10-13 order changes the target of the 10-09 charter; its authority boundaries stand.
One standing authorisation covers paper analysis, bounded simulation, repository work and
site work within the envelope. Publish existing qualified content within its claim gate.
A FAIL closes a hypothesis, not the programme. Preserve failures, counters and sealed evidence.

Money, physical work, new public scientific claims, the Admiral's settings (including GitHub,
DNS and credentials), and root access remain his alone. Route each through the Captain as a
typed `admiral-decision`, with a DEFAULT and a DATE 48 hours out. A default is not permission
to spend, act physically, publish a new claim or change a reserved setting.

Resolve design questions inside the ship. Record the decision, its assumed default and its
limits, then proceed. Experts will later confirm assumptions and make introductions.

## The unit of progress: a design iteration

Choose a candidate and change the design in pursuit of a credible positive margin.
Geometry, structural concept, materials, scale and pressure ratio may all change within the
envelope. Nothing about the current design is fixed merely because it is already recorded.
Number verification is a tool for a particular iteration, not the programme's work queue.

Each iteration records:

1. The candidate geometry, structure, materials, scale and pressure assumptions, with a source
   revision and a clear distinction between a drawn design, a conceptual candidate and a bound.
2. Its mass budget, stating what is included, omitted or assumed and separating hull mass
   from the equipment, fittings and payload needed for an all-up vehicle.
3. Its lift budget, with the matching configuration, volume, pressure and operating conditions.
4. The margin between those budgets on the same basis, its limits and the confidence warranted
   by the evidence. A positive conditional calculation alone does not establish float confidence.
5. The one assumption most likely to change the answer, and the next design change to try.

Proceed on paper with assumed values explicitly labelled UNKNOWN. Record their basis and
sensitivity; absent measurements do not prevent an assumed-value iteration.
Keep local structural sufficiency separate from global sufficiency. Do not combine budgets
from different configurations or treat a crush-floor bound as a design with a safety reserve.

Start from the best recorded candidate or bound, state why it was selected and what is missing,
then rank the next changes by their likely effect on margin and confidence.
The current carry establishes no complete, buildable floating candidate. Favourable bounds
remain bounds; they are starting points for design work, not qualified all-up vehicles.
Historical stage records remain evidence and constraints. Their old ordering in
[PLAN.md](PLAN.md) and [NEXT-STAGES.md](NEXT-STAGES.md) does not govern the redirected work queue.

## Scoreboard and expert confirmations

Keep the same single scoreboard line at the top of the daily summary and on the repository
front page: does the best current candidate float, by what margin, with what confidence,
and which one assumption would most change the answer? Keep it at or below 180 characters
so the morning report preserves it without truncation. Until the evidence changes, the answer
is `not shown`.
The 06:50 daily summary carries the line and explains how it moved, or why it did not.

Keep one short expert-confirmation ledger alongside the design evidence. For each assumption,
record what an expert must confirm, why it matters, how far the design would move if it were
wrong, and the iteration that depends on it. Use UNKNOWN where that effect is not yet bounded.
Update this list as iterations identify stronger evidence or a different weakest assumption.

## People and resource limits

Until Engineering measures ULTRA delegation, the programme is limited to five seats:
the lead plus four persistent workers. Request workers through the host minter under the lead: two gpt-6-astra at MAX on codex-primary and two glm-5.3 at MAX
on glm-primary. The lead uses gpt-6-astra at ULTRA on codex-primary. Keep internal delegation
small while Engineering measures it; request no additional seats. Claude is outside the
programme except for the XO's signature. Use the codex week, aiming at burn7d 1.0–1.5.
Engineering measures delegation and burn on day one; the Captain may reduce the lead to MAX
if ULTRA misbehaves, without stopping the mission. A lane wall rotates work; it does not stop it.

Use existing enforced slices and lane limits, including task, file, wall-time, affinity,
storage and IPC cleanup controls. The standing parent envelope is 8 CPU and 40 GiB with swap
disabled; this does not allocate the whole envelope to a worker or expand any existing lane.
Handle contention through established isolation and locks, without asking other workers to
pause. `/mnt/scratch` is RAM: create no worktrees there and release completed temporary work.

A guard, validator, IPC, cache or monitor failure before science is a control stop, not a
science attempt. Fix an in-scope control defect and retry once, recording both events.
A completed scientific computation with incomplete monitoring is not automatically eligible
for retry and cannot be qualified by a later fix. Exhausted historical attempts do not gain
new retries from this redirect; define the next distinct hypothesis within applicable limits.

## Evidence and delivery

Use one evidence file per unit and one reviewer for custody. Reuse earlier references rather
than copying and rechecking old inventories. Record the question, frozen assumptions, source,
result and practical limits, with exact candidate commit, tree, base, changed paths, checks,
review referents and landing dependencies. Apply proportionate documentation checks and the
applicable code or scientific review when those surfaces change.

Distinguish PASS within the tested scope, FAIL of a hypothesis, UNKNOWN, NOT RUN and control
stops. Corrections add a disposition; they do not rewrite old evidence or erase coverage gaps.
Every iteration, including FAIL or UNKNOWN, lands as a governed commit under `research/`
the same day. Prepare candidates in isolated worker-owned clones with separate Git directories,
normal governance and a named Builder. The Captain lands the accepted object.

Make at least one actual governed airships or site landing each day. A branch commit or a
message does not count, and a site landing does not replace an iteration's research record.
After acceptance, take the next ranked design change. Report actual landing counts, the first
pending landing and reserved decisions with their defaults and dates alongside the scoreboard.

Existing public model limits remain in the [vacuum-cell analysis](../analysis/vacuum-cell.md),
[mass budget](../analysis/mass-budget.md), [float ledger](../../docs/FLOAT-LEDGER.md) and
[claim gate](../../docs/CLAIM-GATE.md). None establishes a measured aircraft.
