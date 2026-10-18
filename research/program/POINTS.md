# POINTS — Vacuum Float programme rubric, v0

Status: v0, created by U3 from REDIRECT section 7 verbatim. Weighted by kind; awarded only by Una on verification. Versioned with the changelog below; at most one rubric change per map version; changes apply forward only, never rescoring the past.

| event | points |
|---|---:|
| validated point on the map | +10 |
| scoreboard improves (margin up or material gap shrinks) | +25 |
| published buckling benchmark reproduced within 5% (once each) | +15 |
| demonstrated falsification removing a design-space region (cap 3/week) | +10 |
| sourced material card entered (cap 5/week) | +5 |
| claim withdrawn in review | −10 |
| landing with no number | −5 |
| envelope breach, or a run presented as converged that is not | −20 |
| per 100 M tokens spent by the lane | −1 |
Rules: awarded only by Una on verification, never self-reported; credit units are indivisible; leaderboard per lane and
per model on the public log beside cost; routing follows it; a failed audit zeroes that lane's current map version.
Adaptivity: research/program/POINTS.md is versioned (v0, v1 …) with a changelog; anyone may propose a change (a lane's
gaming attempt is itself signal); Una and the Admiral's seat approve; at most one rubric change per map version; changes
apply forward only, never rescoring the past; weights shift toward the binding uncertainty of the current map version.

## Scorer conventions (v0)

Una (xo-r-10111326), 2026-10-17, from her disposition
`SCORER-CONVENTIONS-POINTS-v0.md` (sha256 `d9c2a6a289b91fb9f5f9acc1750f487d191ba0e80d837dff30d971f1604368ec`).
These say how the scorer applies the v0 table as written. No weight, event or cap number changes, awards stay hers
alone, on verification, and nothing is rescored. They are not a rubric version. If the Admiral's seat reads any of them
as a rubric change, it rules as tie-break, and that ruling is map v0's one change.

### 1. The two weekly caps (falsification 3/week; sourced material card 5/week)

- Window: a ROLLING 168 hours of exact instants, keyed on the instant of her verification report (UTC; no timezone, no
  calendar week, no boundary to stack across). An award of the capped type is admitted when the lane has fewer than the
  cap of that type verified in the 168 h ending at that instant.
- Scope: PER LANE, not programme-wide. A lane is Builder A or Builder B, together with every worker and sub-agent it
  runs on Sciences' brief and any successor relief of that builder. The Sciences seat and the scorer are not scoring
  lanes. The per-model leaderboard attributes each award to the model that produced the evidence, but the caps count
  per lane.
- Over the cap: the event is still verified and entered on the map, because it is still evidence and a FAIL is still a
  point. It scores 0 under the capped rule. It is never banked, never rolled into a later window, and never rescored
  when the window clears.
- Order: by her verification instant; she verifies in filing order.

### 2. The token penalty (−1 per 100 M tokens spent by the lane)

- Basis: every token the lane's model sessions processed, as each session's native record reports it — all input,
  cached and uncached (cache reads and cache writes included), plus all output, reasoning included. For codex that is
  the record's cumulative `total_token_usage.total_tokens`. For claude and glm harness records it is
  input + cache_creation_input + cache_read_input + output, counted once per assistant message id (streamed blocks
  repeat the usage). No provider weighting and no price conversion.
- Lane: the same membership as in section 1, from each session's start (the builder's mint) onward.
- Not charged to any lane: the Sciences head seat, the scorer and any re-run sub-worker she uses, the CO, and the
  external review round. The ledger reports these as programme overhead beside cost per point.
- Accumulation: CUMULATIVE per lane for the life of the programme. It never resets, not by week and not by map
  version. The lane's penalty total is −floor(T / 100,000,000); the remainder carries forward. Each crossing of a
  100 M multiple is one −1 event, dated at the ledger regeneration that first observes it and attributed to the map
  version current then. Forward only: a record found late adds its crossing when it is found, and never rewrites a
  past version.
- Coverage: a session with no readable native record is UNMEASURED. The penalty is computed on measured tokens only,
  and coverage (measured sessions of known sessions, with the unmeasured named) is shown beside it. It is never
  zero-filled and never estimated.

### 3. Cost per verified map point

The same coverage line, and "unavailable" while the lane has zero verified points — never a division by zero shown
as a number.

## Changelog

- 2026-10-17 — Added the "Scorer conventions (v0)" section from Una's hash-pinned disposition. No rubric weight,
  event, cap or version change: the table above is untouched and the rubric remains v0.
