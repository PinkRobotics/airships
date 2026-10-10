# Programme

Status: standing programme charter, 2026-10-09. This document sets out scope, delivery and next work; it adds no scientific result or qualification. No aircraft has been built or flown.

## Scope and authority

One standing authorization covers paper analysis, bounded simulation, repository work and publication of existing qualified content. Work proceeds through ranked hypotheses rather than a new permission request for each stage. A failed hypothesis closes that hypothesis; it does not end the programme. Historical failures, counters and sealed evidence remain part of the record.

Money, physical action, new public scientific claims, settings and root access remain reserved for the programme owner. Route such a decision through the Captain with a proposed default and a decision date, normally within 48 hours. A proposed default does not authorize spending or physical action.

## Next work

The table is a work plan, not a scientific disposition register. Any result publication requires its own research record and the applicable claim gate.

| Stage | Planned work and limits |
|---|---|
| P1, port | P1.6 assumed-value paper with explicit assumptions and a measurement list |
| P2, cylinder | Repair monitor wiring as a separate unit, then assess a distinct supported hypothesis using applicable enforcement |
| P3, NASA/CFD | Next ranked experiment with applicable enforcement and scope; no implied cap expansion |
| P4/P5, float and joints | P4.5 assumed cord, end and shared-anchor paper, keeping local and global sufficiency separate |
| Stage A, toolchain | Continue toolchain and interface work within its applicable qualification scope |
| P6, cost | Quote-backed dated costs or explicit UNKNOWN; no spending authorized |

For the existing public model and limits, see [vacuum-cell analysis](../analysis/vacuum-cell.md), [mass budget](../analysis/mass-budget.md), [float ledger](../../docs/FLOAT-LEDGER.md) and [claim gate](../../docs/CLAIM-GATE.md). These documents do not establish a measured aircraft.

## Execution and delivery

Use existing enforced resource slices and lane limits, including task, file, wall-time, affinity, storage and IPC cleanup controls. The standing parent envelope is 8 CPU and 40 GiB with swap disabled; it does not grant a worker those whole limits or expand an existing lane. Contention is handled by the established isolation and lock mechanisms, without asking other workers to pause.

A guard, validator, IPC, cache or monitor failure before science is a control stop, not a science attempt. Fix an in-scope control defect and retry once, recording both events. A completed scientific computation with incomplete monitoring is not automatically eligible for a retry or qualified by a later fix.

Workers persist across bounded units. Use one evidence file per unit and one custody review; reuse earlier references rather than copy and recheck old inventories. Documentation receives proportionate checks; code receives the applicable review. Correct a demonstrated defect and preserve asserted concerns in the record.

Every accepted unit, including FAIL or UNKNOWN, receives a governed `research/` record the same day. The daily delivery goal is at least one actual airships or site landing; a branch commit or message is not a landing. Candidate commits are prepared in isolated clones with normal governance and a named Builder. Captain lands the accepted object. See [next stages](NEXT-STAGES.md) and [plan](PLAN.md).
