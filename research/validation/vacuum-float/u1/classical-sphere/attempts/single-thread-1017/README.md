# Classical sphere: single-thread attempt

This separately frozen attempt tests whether one solver thread reproduces the original ideal elastic comparator. The original eight-thread FAIL and its raw evidence remain unchanged. This is another attempt of the same benchmark and creates no additional award.

The copied [case](case.json) preserves the physical inputs, three mesh divisions, eight requested modes, lowest-positive-mode rule, 5% comparison tolerance and both 1% successive-mesh tolerances. Its parent case and original runner are hash-pinned. Only the solver thread controls change to one.

[Deck preparation](prepare_decks.py) invokes the original runner's mesh and deck functions without solving. It checks the regenerated middle-mesh deck against the original hash before any solver invocation. Each frozen deck then goes through the original runner's fixed-deck path once, with all supported thread controls set to one. The preparation and each solve require the same measured resource bounds. Any required physical change or failed solve stops this attempt; no retry or tuning is allowed.

The source freeze precedes all three solves. Results, all eight factors, convergence and absolute raw evidence pointers will be added after execution. No result or verification is claimed by this freeze.
