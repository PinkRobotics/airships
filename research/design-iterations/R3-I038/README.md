# R3-I038 — external freshwater reserve pair (finite stock construction)

Issued successor on landing81 (base `dc31909d`, tree `1e2837ba`). One fixed external
freshwater reserve per upper barrel, complete paid support frame and segregated plumbing,
built from the I038 design freeze. This is a **finite stock/geometry record, not a
qualification**: no capacity, structural, energy or margin claim is made anywhere in this
unit; physical float is **NOT SHOWN**.

## The one frozen design change vs I035

The internal reserve divider system is **absent**. Each upper barrel is one unpartitioned
service interior (25 t D1 fresh, then 25.45 t scoop). Each barrel gets an **independent
external reserve tank** (OD 1.8 m, 2.4 m straight, 4 mm 5083 shell, 12 mm flat heads) that
starts with 5 t and supplies only its paired lower delivery circuit during D2 — reserve
fresh never passes through a scoop chamber. The 0.45 t-per-lower relocation stays upstairs
(location, not mass). No numeric old-bill saving is claimed for the removed divider
sump/through-reserve drain: their complete old mass was never established.

## Files

- `baseline.json` — saved-input assembly, three labelled categories: (1) accepted I017
  conditional mission/stock records with all their limitations (duty rows, authority
  datums, recorded FAILs/UNKNOWNs), (2) I032 declared geometric/material inputs —
  declared assumptions, never successful calculations (lower baffle planes and oblate-head
  volumes stay UNKNOWN), (3) the frozen external-reserve construction from the issued
  design freeze. Every source is bound by git blob OID at the named base.
- `reserve.py` — stdlib-only calculator. Contract:
  `python3 -I -B research/design-iterations/R3-I038/reserve.py --write`.
- `reserve.json` — generated record: per-item stock bill (shells, heads, rings, T
  stiffeners, baffle, fillets, full frame, bands/straps, enumerated bolt sets, circuits,
  flanges, seals, vents), non-negative route lengths with full clamp/bracket counts,
  reserve enclosed geometry with displacements subtracted once, event/species/centroid
  tables with signed six-component aggregate wrenches, the eight D2 command cases with
  honest shortfalls, the C list, and the scoreboard. Produced by guarded science start 1
  of at most 3 (launcher `07abcaf2…`, guard verbatim `7e0e628f…`, pre-execution controls
  PASS incl. private IPC/CPU-28/Threads-1/fd0-devnull; exit 0, wall 0.081 s, memory peak
  7.5 MiB; 26,275 B, sha256 `500cebc3…`).
- `sources.json` — roles and provenance of every input.

## What is computed, what is carried, what is refused

**Computed:** every specified stock item from fixed dimensions at declared densities
(5083 2660, steel 7850, polymer 1200 assumed); route centreline lengths (elbows as arcs,
corners replaced, convention declared); clamp+bracket counts per run at ≤2 m spacing and
at every elbow/valve/pump; fill-dependent liquid centroids (reserves exact vertical
cylinder; inherited barrels straight-segment model with head contribution UNKNOWN);
aggregate wrenches per state at the common origin (no equal support split, no rigid
receiver); the eight D2 cases by the frozen command law.

**Carried:** I017 conditional duty rows shown separately (qualified retirement ZERO,
conditional common-duty comparison only where rowwise established, no-retirement bound
retains all previously charged duties); declared device masses (valves, pumps, P/V,
instruments); the inherited econ 35.1× FAIL and fuel shorts 0.245112/0.350732 t.

**Refused:** no subtraction from the I035 8.991 t figure (its outputs are withdrawn
archival); no formula adopted from its executable; no usable-volume or margin claim while
the vent/overflow inlet, head volumes and deadwater are unestablished; no qualified total
while required hardware or receiver stock is unpriced; no equal W/4 or W/2 pickup
reaction; no tuned dimensions; unfinished D2 delivery at T is FAIL, never extension.

## Status

Usable capacity UNKNOWN (all six tanks); structure UNKNOWN; fresh delivery FAIL class in
the eight cases (lagging pair short by construction, ~1.25–1.27 t fresh at +5% error/2 s
lag); economics and fuel inherited FAILs. The weakest assumption: the external reserves
and their receiving structure are installable without consuming unreserved bag/equipment
space. One later hypothesis, unissued: a paid shared same-frame collection beam.

Ancestors: R3-I017 (conditional flat-tank record), R3-I032 (declared geometry baseline),
R3-I035 (withdrawn outputs, archival only — see its README and sources at the same base).
