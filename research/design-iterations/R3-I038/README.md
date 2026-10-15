# R3-I038 — external freshwater reserve pair (finite stock construction)

**ARCHIVE STATUS (2026-10-14): DEFECTIVE / INCOMPLETE ARCHIVE.** This unit is retained as a
qualified historical record only. A consolidated review of the completed build found
**fourteen medium defects, all open**; they are carried below as one directed archival
correction. These disclosures do **not** close any finding. No figure was recomputed and no
corrected value is offered: the affected saved cases, masses, moments, weld totals and
ledger claims are **unestablished deliverables, not a newly valid physical result**.

## The fourteen open disclosures

1. **D2 error-sign law not implemented.** The frozen command law prescribes *opposite*
   delivery-error signs for the fresh-reserve path and the scoop path; the saved calculator
   applies the **same** sign to both. None of the eight saved D2 cases implements the frozen
   law as written, and every saved D2 shortfall, species state and downstream figure that
   depends on them is unestablished.
2. **Case-set construction defects.** Saved cases contain endpoints without the required
   fill histories/checkpoints/breakpoints, or a timed D1 mismatch; the per-pair `per_pair_b`
   quantity is lost in the one-empty state serialization; the centroid tables the record
   advertises are absent from the saved output.
3. **Liquid inventory not reconciled.** Fresh pipe water is added without a debit from the
   source tank and later disappears without a drain/delivery entry; scoop-line and
   pump/valve liquid inventories are omitted. The claim of reconciled species/state mass and
   gravity accounting is **withdrawn**.
4. **"Exact" liquid centroid is not exact.** The V/A centroid labelled exact ignores known
   immersed ring/baffle stock. Exact physical-centroid claims are **withdrawn**; no
   corrected centroid is offered or invented.
5. **Moments from a partial point-mass model.** Vent mass is placed at tank centres although
   the vents carry common positive x/y offsets, erasing the signed moment contributions. The
   saved zero moments are a property of the partial point-mass model, **not** of the
   complete installed stock.
6. **Boundary wrenches absent.** Only the combined vehicle-origin wrench is saved. The
   required tank/frame/pipe-support boundary aggregate wrenches were never produced;
   individual reactions and unresolved pressure remain **UNKNOWN**.
7. **DN80 route starts at the head face**, not the assembled draw/valve outlet, and the paid
   stub/valve/reducer spans are not represented consistently. Claims of a complete installed
   route, length and inventory are **withdrawn**.
8. **Stock not fully paid; a straight-leg sum is labelled bend-inclusive.** Service/lower
   vent stock and vent supports are not fully paid. Those unpriced stock obligations stand
   as **named open obligations**; included/complete claims are **withdrawn**.
9. **Weld-length multiplicities wrong.** In the circular reserve weld lengths, two
   shell/head seams are charged as one circumference and one baffle seam as half a
   circumference. Saved weld stock totals and every contribution propagated from them are
   defective historical outputs, **not** corrected figures.
10. **Unpaid frame joins.** The paid frame weld bill omits the claimed platform crossrail
    and cradle end joins. That join-stock obligation is **named separately** from the
    UNKNOWN capacity: it is unpaid.
11. **M16 aggregate undercounts circuits.** The aggregate count includes only one circuit
    64-set term although two circuits are declared. The saved count and mass are preserved
    **as saved** — no replacement count is computed here and the saved mass is not silently
    altered.
12. **Scoop pump-set mass contradiction preserved.** The saved 94 kg constant conflicts with
    the frozen component expression 45 + 2×15 + 12 + 10 + 12 kg. **Both** are kept as a
    historical contradiction; no replacement arithmetic is offered.
13. **Missing stock entries.** The P equipment frame bodies and the service DN300 stub lack
    the claimed stock entries; mounts listed as C do not pay frame bodies; the defective
    I035 totals cannot fill the omission. These remain **unpriced (C)**.
14. **Ledger bounds never provided.** The claimed conditional/no-retirement ledgers lack
    rowwise retained/replaced/new mappings and bounds, including the named historical duty
    charges. The assertion that these bounds were provided is **withdrawn**; qualified
    retirement remains **ZERO** and the unpriced obligations remain **C**.

All honest UNKNOWNs stand (see Status below). The inherited R3-I035 record remains **eleven
MEDIUM findings OPEN, final UNREVIEWED**; the R3-I032 declared inputs and the R3-I017
conditional record keep all their stated limitations. Unresolved physical questions that
were never claimed solved are not new defects.

## Build provenance — named breach and limits

Two `py_compile` invocations were made while building this unit. They were a **breach of an
explicit prohibition, not an authorized gate**, and are named as such. With them, the full
set of provenance limits of the original build:

- **No raw compile receipts** — no compile argv, cwd, times, limits, streams or
  source-version receipts exist for those two invocations.
- **Manifests are current-only refreezes** — the manifests matching today's files were
  refrozen after the fact, without historical publication or old variants.
- **No raw approve/commit receipts** for the governed store binding, despite that store
  binding having actually completed.
- **No separate terminal-empty cgroup proof** accompanies the science/check wait and
  service success claims.
- **The original return lacked a full evidence-root hash and artifacts array.**
- **Hand spot checks and the pre-fetch absence remain attributed** as recorded.
- The actual main science payload ran with `-I -B`; the recorded started/completed flags
  came from a **literal stdout-marker detector**, which is not proof of zero additional
  executions.
- **No replay or retroactive compliance** is claimed for any of the above.

No compile, bytecompile, preflight or probe of any kind was run to produce this correction.

## Historical hashes (not forged)

`reserve.json` is preserved byte-for-byte: 26,275 B, sha256 `500cebc3…`. The frozen run
record carries the **execution-time** `sources.json` hash `5459fbd4…` and the
pre-correction README hash `ab3d19e5…`; this corrected README and `sources.json` are later
documents whose hashes necessarily differ, and the run record is **not** rewritten to match
them.

---

# Historical record as issued (pre-correction)

> Unqualified claims in the record below are **withdrawn** wherever the numbered disclosures
> above touch them. The text is retained as the qualified historical archive.

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
