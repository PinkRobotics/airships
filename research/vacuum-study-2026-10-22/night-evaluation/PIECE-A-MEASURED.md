# Piece A, measured (robotics seat, 10-20, 10:5x)

Process v2.1 (PROCESS-v2.md) asked for this measurement before any savings target is set. The sources are the queue store's file times, pinkai-history system-20261020.ndjson, and telemetry-state.json.

## Jobs
Accepted completion runs from ingestion to the report's arrival in the store.

| Job | Seat | Ingested | Report | Completion | Queue delay |
|---|---|---|---|---|---|
| 061, improvement targets | 795b17f1 (fresh codex) | 08:50:36 | 09:34:28 | 43.9 min | 1.4 min |
| 062, buildable shape | 1228320 (warm codex) | 08:59:43 | 09:38:13 | 38.5 min | 1.0 min |
| REVIEW-A1, on 056 and 062 | 795b17f1 | 09:54:20 | 10:18:21 | 24.0 min | 0.9 min |
| REVIEW-A2, on 058 and 061 | 1228320 | 09:54:20 | 10:22:53 | 28.6 min | 0.9 min |
| 030e, the claim record | 795b17f1 | 10:24:19 | 10:50:13 | 25.9 min | 0.4 min |

- **Wall time:** 2 h 01 min, from the first dispatch (08:49:10) to the last report (10:50:13).
- **The one loss:** the order for a fresh REVIEW-A lead got no reply from Ops for 15 minutes, while Ops was busy with Pike's pool moves. I then split the review across the piece's own two seats, each reviewing what it did not write, which needed no mint. Without that wait the piece would have taken about 1 h 46 min.

## Cost
- **Codex 7d:** 93% at 08:49 and 98% at 10:50, so 5 points (±1, integer readings). That covers five jobs plus the tail of Spock's codex process review, at about 1 point per job or less. The night ran at about 1.3.
- **This seat:** 640 messages and about 145 M cache reads from 08:10 to 10:50. That window includes the night's evaluation and the process work. The rate was about 240 messages an hour, against about 680 an hour overnight.
- **Wakes:** 10 watch exits from 09:04 to 10:50, against 1,339 monitor lines overnight.
- **Filings by this seat:**
  - 9 orders, including one withdrawn mint and three retirements;
  - 1 withdrawal ack;
  - 0 acks of reports that asked nothing.

  That is about 2 filings a job, against about 3 overnight (216 orders and 217 acks for 147 jobs).
- **Not tracked:** the codex seats' tokens.

## What the piece decided (all QUESTIONABLE/PROJECTION)
- **Neither lead floats under concept mass growth.** Some cases float only at the TRL 7 allowance, which is a hypothetical maturity.
- **P2 comes closest at R 30.** It needs a face density divided by 1.0593 (ISA) on the favorable endpoint, or by 2.1435 on the handbook basis. That spread is the biggest open question.
- **P3 does not close in its family:** local tube-shell compression binds.
- **The tolerance:**
  - 047's limit is not yet a physical tolerance, because the core, sheet and bond are unsourced;
  - SR-200's 290 GPa is sourced;
  - closed-form limits are 0.793/1.628/2.486 mm at R 10/20/30;
  - unquoted first-shell costs run from $67-477M at R 10 to $1.8-13.4B at R 30.
- **Beryllium:** the R 30 faces need 23.8-24.4% of the estimated 2025 world mined Be.
- **Weather:** the valve and bladder mass lower the day fractions by up to 3.8 points.
- **The review:** 34 load-bearing claims. 29 reproduce, 3 differ and 2 need evidence. The 8 fix rows are carried UNREVIEWED.
- **The record:** it is one incremental claim record (version 5: 118 rows, 2,351 claims). Later pieces append deltas.

## Lessons for Piece B
- **A pinned brief is frozen.** I amended PROCESS-v2.md in place after 061 was dispatched with it pinned. The seat recovered the dispatched bytes by hash. Amendments go in a new versioned file.
- **An order to Ops needs the silence test.** Watch v32 added NO REPLY and NO COMPLETION checks, and NO REPLY fired once, correctly.
- **The piece's own seats can review each other's work.** Each half reviews only what it did not write, which keeps the review independent and avoids a mint.
