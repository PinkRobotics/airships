# The overnight reviews, digested — what the loop found, what held up, what changes

Written 2026-08-12, after reading everything in `~/data/airships-reviews/` (orders 864, 865,
868, the supply primer, the briefs) and the three `devworker/*` branches, and verifying the
load-bearing claims against this repository. The loop continues tonight (869 metal joint,
870 end fixity, 871 the commercial floor); the "when they land" section says what to do
with each.

## The bottom line, for getting to floating

The reviews moved the mission's ground truth in three ways, all verified here:

1. **R1 — subdivide the lattice — is dead as priced.** The blocking check (865) sized the
   even-n face members for the film's transverse bending, which the study had explicitly
   deferred: every axial-only optimum fails at margin 0.35–0.40 against SF 1.5, and the
   re-priced rows are **10.76–12.51 kg/m³ against the 9.31 baseline — worse than not
   subdividing.** The cube law the study hoped would save it is real (M ∝ 1/n³, proved in
   its new self-checks) but section modulus falls with the smaller tubes just as fast.
   *Landed on main tonight: the reworked `tools/subdivision_study.py` (film bending as a
   selection constraint, corrected 0.715 kg joint basis, finite cut-list pricing) and the
   honest FLOAT.md §3 rewrite. The tool reproduces its published table on this machine.*

2. **The joints are the second-biggest lever and the current design is not the standard
   mechanism.** The joint study (868): no buyable fitting in the 10–16 mm band publishes
   both a complete-node mass and a 3–7 kN rating; the standard engineering answer is a
   **bonded tapered socket/end-fitting spreading load into the tube wall** — not a solid
   many-arm printed hub. Corrected numbers: our 0.715 kg of joints is **29.9% of tube
   mass** (target 15%); at n=2 the printed-solid law projects joints at **116.7% of tube**
   — at fine subdivision the joint architecture, not the tube, is the wall. The material
   sensitivity for a bonded no-hub node prices at 0.299 kg/m³ (vs the 0.407 target) but
   deliberately omits the central redistribution material; it is a hypothesis to test, not
   a design. Orders 869 (which metal regime — prediction on record: bond-limited) and 870
   (end fixity: K = 0.7 would double Euler capacity — is the joint dead weight or a lever)
   are in flight on exactly this question.

3. **Article A is not structurally proved, and that is now precisely catalogued.** The
   physics audit (864, 17 findings): the member demands are honest *envelopes* that
   reproduce family by family, but they are not a closing equilibrium (9/51 nodes balance;
   the 8.08 kN "residual" is the bookkeeping of deliberately double-assigned indeterminate
   pulls, not a physics error). The genuinely unproved things: **U1** tube-to-joint
   interface adequacy (bearing/pull-out/bond all screens, no licensed capacity — and the
   rim rows are contaminated by the probe-SKU defect this repo had already found
   independently); **U3** end restraint (K = 0.65 unlicensed); **U4** combined
   axial + bending + beam-column: the spoke's combined margin is **1.02** — essentially no
   reserve beyond the SF. Two loud favourable corrections: the real cut schedule is
   **−0.367 kg of tube** (audit O7 = our P14, independently confirmed to the millimetre),
   and R1's allocation was pessimistic for a bulk array (3.65×, not 4.06× — moot now that
   R1 died, but the control-volume lesson stands).

The supply primer adds the constraint that reshapes all of it: **local wall buckling is a
hoop failure, and the cheap high-modulus tube (pultruded, ~134 GPa) is the wrong
construction for it.** Roll-wrapped tube that actually carries hoop bottoms out near
0.889 mm wall at the big stock house (0.254 mm at the widest custom range) — so the study
rows that requested 0.15–0.30 mm walls were never buyable. The orchestrator's rough floor
arithmetic (~3× the wall after every route succeeds) is why 871 exists: a rigorous
commercial floor with the 0.605 fix first, ending in an unhedged floats/doesn't sentence.

## What this repo knows that the reviews don't (cross-corrections)

- **The analysis' square film panel is the wrong shape.** `PANEL["squareSpoked"] =
  1/(2+√2)` of the edge (73.42 mm) is the inradius of a *half*-square (one diagonal), but
  the article's four in-plane ties quarter each square through the face centre
  (`gen_nodes.article_graph`, tie #1: rim vertex → face centre — both diagonals). The real
  square panel inradius is `S(2−√2)/2 = 51.92 mm`. The audit *reproduced* the code's
  numbers (U2, U5, the film-mass ledger) without catching the geometry mismatch, so its
  square-panel tension (7,903 N/m), film areal mass, smeared volume debit, and the
  square-tie's "radial pull" contribution to the 5,037.67 N governing short-member demand
  all inherit the too-large panel. Correcting it moves several margins in the favourable
  direction (the tie's film pull scales with the panel inradius). Queued as its own
  analysis-layer commit — it ripples through parity, the contract demands, and gated
  prose, so it gets the full freeze-and-read-the-bill treatment.
- **The displacement debit is worse than the audit's smeared 8.57%.** #63 (closed today)
  solved the true membrane over every real panel: the pumped-down article displaces
  **159.76 L, a 10.35% debit** — the smeared flat-area×h/2 rule is reproduced as a check
  inside `tools/gen_skin.py` and then superseded. The audit's loaded-density multiplier
  (×1.0937) should be ×1.115 on the solved shape. Its U5 "pre-form the membrane" demand
  is now met: the net keeps its proven outline and is **formed** (the gore study measured
  flat cutting to death — even twelve gores per panel misses the film's elastic budget).
- **U1's "checker defect" is confirmed and already on the books here** as the probe-SKU
  gap (probe_node samples the global 10×8 annulus on 14×12 rim arms). The audit's
  corrected-area arithmetic (rim seat 12.419 mm², spigot 18.533 mm²) is the right
  direction; the fix remains a per-arm field-probe rerun plus a measured re-freeze, not a
  report-side rewrite. That work joins the #65 pass.

## Disposition of every finding

**Landed tonight (this commit set):**
- Order 865's branch: `subdivision_study.py` film-bending constraint + 0.715 kg basis +
  finite cut pricing; FLOAT.md §1 headline (measured 17.6, 18.4×) and §3 rewrite; the
  HANDOFF one-liner (the ~4.2 claim). Verified: both study self-checks green here, table
  reproduces, `make check` green.
- The audit and joint reports themselves: their branches add `docs/audit/*.md` verbatim
  copies of the drop files; adopting the drop as the canonical location, the branches can
  be deleted after 871 lands (they contain nothing else).

**Queued next, in order (each its own gated commit):**
1. **P14 — bill the nine cuts** — DONE tonight (audit O7 concurred; its −0.367 kg was
   the pre-sunken-frame schedule, the live nine-row table is −0.442 kg): stock_build
   2.390 → 1.948 kg tube, article 3.13 → 2.69 kg, 15.13 kg/m³ = 15.8× the wall. Billed
   from a measured, mirrored CUT_SCHEDULE_MEASURED that the prover holds row-by-row to
   the live manifest; P14 passes and the contract is re-frozen on exactly that flip.
2. **The square-panel correction** (above) — analysis + model parity + contract re-freeze.
3. **Probe-SKU field rerun** (with #65) — then the corrected P16 census the audit asks for.
4. **0.605 — NOT mine to do:** 871's brief explicitly fixes it first and restates R4's
   headlines. Review its branch when it lands rather than racing it. (If 871 comes back
   without it, adopt audit O1 directly: `tubeStrut`, `ladder`, and the P16 spigot screen
   omit the classical coefficient; `subdivision_study` already has it.)

**Standing corrections to how results are read (no code change):**
- §3's route table is directional hypotheses, not article configurations (audit verdict —
  the landed FLOAT rewrite already says this for R1).
- Nothing in §1/§3 is a complete-BOM density; the audit's not-yet-counted ledger
  (21.6/95.3/202.9 g low/base/high, plus unbounded joint-reinforcement unknowns) rides
  along until the interface is licensed.
- K = 0.65 socket fixity may not be credited anywhere until 870 lands evidence.

**When tonight's orders land:**
- **869 (metal joint):** expect a regime verdict (strength → Ti, stiffness → Al,
  bond-limited → thinnest sound socket). Check its socket-wall assumptions against the
  primer's printed-metal minimums (~0.4–0.8 mm) and the powder-vent point (SLM parts are
  vented by construction — the "sparse infill is a virtual leak" doctrine is FFF-specific
  and does not transfer).
- **870 (fixity):** if it licenses K < 1 with an M-θ story, Euler-sized members re-price by
  1/K²; if not, U3 stands and pinned stays the law.
- **871 (floor):** the big one. Review the 0.605 fix first (it changes published analysis
  figures — parity + prose gates), then the floor build-up, then the which-assumption-
  must-break list. Its verdict sentence is the project's new headline either way.

## What did NOT survive scrutiny

- The joint study's 0.299 kg/m³ bonded-node line is **not** a design (its own words) — the
  central redistribution mass must fit in 0.43 kg across 201 nodes at n=2 for the 15%
  target to survive, and no allocation exists. Treat every "joints could be X% lighter"
  claim as unpriced until 869/870 supply mechanism numbers.
- The audit's 16.03 kg/m³ "base scenario" for article A is a *scenario* stack (cut tube +
  0.465-era nodes + allowances) — it mixes the pre-sunken-frame joint geometry and is
  explicitly not a BOM. Do not quote it as the article's density; the article's gated
  numbers are now 2.69 kg / 15.13 kg/m³ (P14 landed tonight) on the same gates.
- Reviews before 2026-08-11 23:20 ran Codex-only (the clone had no Claude lane); the helm
  side now hard-fails a missing lane. Nothing above relies on a claimed-but-absent review.
