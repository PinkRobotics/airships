# The vacuum night, 10-19 22:20 to 10-20 08:20: the robotics seat's efficiency evaluation

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## Sources
- **Pool readings:** `[internal source path omitted]`, one frontier reading per minute.
- **Claude tokens per session per day:** `[internal source path omitted]`. Codex seats are not in it, and neither are the vacuum Opus leads.
- **The queue:** one single-level scan of `ship/queue/submissions`. 779 items since 10-19 17:00 touch the vacuum units or this seat.
- **Other:** jobs.csv (one row per job, below), this seat's notes, and Pike's 07:00 report.

## What it cost
- **Codex:**
  - 99% of the old week at 22:20.
  - The reset was banked at 23:32-23:33.
  - 93% of the new week was used by 08:21, at 10.6 points an hour. That is about 18x an even weekly pace (burn 18.95; his stated target is 2-4).
- **Grok, GLM and muse:** run to their weekly walls, as his policy intends.
- **Claude:**
  - primary from 42% to 64% of its week;
  - provider-pool from 63% to 89%.
- **The host:** MemAvailable never fell below 33.7 GB (at 01:16). Load peaked at 41.2 (at 05:56).

## What it bought
- **146 jobs:** 75 cards and 71 checks.
  - The median time from dispatch to first report was 31 min for cards and 28 min for checks.
  - At the peak, 24 jobs filed in an hour.
- **By provider:**

  | Provider | Cards | Checks | Window |
  |---|---|---|---|
  | codex | 31 | 41 | 00:24-07:46 |
  | Opus | 15 | 6 | |
  | grok | 21 | 15 | to 02:30 |
  | glm | 3 | 6 | |
  | muse | 5 | 3 | |

- **Codex cost per job:** about 1.3 points of its week.
- **The picture:** about 20 cards carry the morning picture, among them 040, 042-060, 029 and 020/049.

## Where it was wasteful (largest first; the ranking is judgment)
1. **Checks, one per card (71 for 75).**
   - 41 of codex's 72 jobs were checks.
   - About 15 checks changed a number or claim that mattered. That count is this seat's reading of the night's notes. Examples:
     - CHECK-057: the first floating row moves from TRL 8 to TRL 7;
     - CHECK-059: the drying times; P3's ponding is not reproduced;
     - CHECK-043: the proof claim;
     - CHECK-042: the S-II gap is fit, not shape;
     - CHECK-040: the 1 mm water row;
     - CHECK-045: the damage thresholds;
     - CHECK-055: the rig reach.
   - 45 checks ran before 03:00, on early cards whose numbers 040, 048 and 052 later replaced.
   - Many checks re-derived whole tables (25k-653k comparisons) instead of the load-bearing numbers.
2. **This seat.**
   - 1,339 monitor event lines woke it. They covered seat flickers, acks, mints and ingests, not only filings and stalls.
   - 10-20 from 00:00 to 08:10: 5,556 calls, 1.28 B cache-read tokens (an average of 231k), 7.5 M output. That is about 2x the next-largest session the console tracks.
3. **Re-runs and re-routing.**
   - 18 lettered variants, and 009's unit filed nine times.
   - 57 orders re-routed, re-sequenced or re-scoped cards already out. Many of them came from dispatching a card before the result it needed had filed.
4. **The register built four times** (030, 030b, 030c, 030d). Each build re-folded everything.
5. **Long contexts.** About eight cards were chained on each Opus lead: six compactions (Pike's count). At 08:3x, 6ea737f read 81% context and 1693a54 77%.
6. **Queue churn.**
   - 216 orders from this seat, and 217 acknowledgements in the same traffic.
   - At 07:00 the Board read this seat's standing lines plus deadlines as holds: 26 false stall notices, 8 re-filed orders and their acks.

## A leaner shape (estimate)
- Review only the load-bearing results, once, at the end of a piece.
- Build one register per piece.
- Dispatch only on finished inputs.
- Use a fresh or light-context seat per card.
- This seat wakes on filings, stalls and questions only.

Together that is about 40% fewer jobs and less than half this seat's cost, for nearly the same picture.

## Not measured
- Per-seat tokens for codex and the Opus leads (the console does not track their sessions).
- The quality of each result. Spock's review is asked to judge which results are solid.
