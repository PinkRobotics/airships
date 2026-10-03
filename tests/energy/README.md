# Independent energy checks

Run `make energycheck` without the network. Scratch follows `TMPDIR`.

- `closure.mjs`: claude-fable-5-1's independent owner, limit, price and verdict equations, adapted to local density.
- `replay.mjs`: the printed-requirement replay proposed by claude-fable-5-1, now reading generated rows instead of historical literals. It also replays feasible profiles.
- `../node/energy-profile.mjs`: the 2,001-sample kink check proposed by claude-fable-5-1, extended to every seam and retained-water profiles.
- `first-principles.py`: independent ISA and momentum arithmetic from claude-fable-5-1. It imports no simulation code; the observer supplies state data.
- `peaks.mjs`: muse-spark-1.3's dense peak observer, with a failing assertion on disagreement.
- `bus.mjs`: muse-spark-1.3's bus sampler, with a failing assertion on overload or unflagged clipping.
- `../node/force-mutations.mjs`: gpt-6-sol's four-invariant force probe, adapted to the integrated record.

The slow profile search is `node research/analysis/energy-feasible.mjs` and uses four workers. It is outside `make check`; this gate replays only its printed rows.
