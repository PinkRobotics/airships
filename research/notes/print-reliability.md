# Print reliability — the 0.6 mm / 1.2 mm chain, checked against its sources

Topic note, 2026-08-10. Sources: four Bambu TDS PDFs and two Polymaker Fiberon TDS PDFs (read
in full, catalogue-only — vendor copyright); Gordeev, Galushko & Ananikov 2018 (PLOS ONE,
CC BY, stored at `papers/gordeev-2018-fdm-microdefects.pdf`, read in full); Povilus et al. 2014
(read in full from the arXiv posting; arXiv non-exclusive licence, so catalogue-only); Zwicker
et al. 2015 and Song & Telenko 2017 (paywalled, **citation-verified but not read** — nothing
numeric is taken from either); Slic3r and PrusaSlicer flow documentation (open web docs).

Confidence tags: **MEASURED** (instrumented test in a read source), **DATASHEET** (vendor TDS,
printed specimens, vendor lab, explicitly "for reference and comparison only"), **OOM**
(order-of-magnitude estimate, ours).

## What the sources establish

**1. The PAHT-CF numbers the model uses are exactly what the datasheet says.** [DATASHEET]
E 3860 ± 230 MPa (X-Y) / 2180 ± 130 MPa (Z), σ 92 ± 7 / 47 ± 5 MPa, ρ 1.06 g/cm³, all ISO 527 /
ISO 1183 on printed specimens — verified against the PDF at the URL `sources.json` records
(which is **V3.0**, not the "V2" the catalogue entry says; the numbers are unchanged). Two
riders travel with every one of those values and the model does not currently carry either:

- *Dry state, annealed.* All mechanical values are headed "Dry state" and every specimen was
  annealed and dried at 80 °C for 12 h before testing; the TDS suggests 80–130 °C for 6–12 h
  and warns "some prints may deform and warp after annealing." An as-printed, unconditioned
  strut in shop humidity starts below the datasheet. Annealing is a cheap process step, but it
  is a step the demonstrator plan must contain, with its warp risk accepted.
- *PA12-based, and the wet knockdown is inferred, not measured.* The composition line reads
  "PA 12 and other long-chain PA, carbon fiber"; saturated water absorption 0.88% at 25 °C /
  55% RH. Bambu publishes **no** wet mechanical data for PAHT-CF. The claim that it loses
  little when conditioned comes from a *different vendor's PA12 product* (below) — the audit
  is right to flag every PAHT-CF structural property as **single-sourced**, one datasheet,
  with the wet state unmeasured by anyone. One tensile test or one letter settles it.

**2. Moisture is a 2× design question for PA6 and a rounding error for PA12.** [DATASHEET]
Polymaker's Fiberon TDSes are the only vendor data found with paired dry/conditioned
measurements on printed specimens (conditioning: 48 h immersion at 60 °C, an aggressive
protocol): PA6-CF20 at 5.30% absorbed water keeps E 2508/1056 MPa of a dry 8637/3760 (X-Y/Z —
a **71–72% loss**); PA12-CF10 at 2.92% keeps 3132/1622 of 3311/1807 (**5–10% loss**). A
lifting cell lives outdoors for months, so dry-state PA6 numbers are fiction for this
application, and the PA12-class choice of PAHT-CF is right for a reason the project had never
stated. It is now stated.

**3. Extrusion width ≥ nozzle bore, so the wall is not 1.20 mm.** [open slicer docs]
Slic3r's flow documentation puts the thinnest safe extrusion width at 1.05 × nozzle;
PrusaSlicer's own defaults lay 0.45 mm roads from a 0.4 mm nozzle (112%). A 0.6 mm nozzle
reliably lays 0.63–0.72 mm roads, so the two-perimeter wall lands at **1.26–1.44 mm, not the
1.20 mm** the printer-chain table in `analysis/vacuum-cell.md` implies. Direction of the
error: conservative for strength, optimistic for mass — struts come out roughly 5% heavier
than the 2 × 0.6 arithmetic. Keep wall = 2 × bore as the floor in the strut-length chain;
carry 0.63 mm width in slicer profiles and mass estimates.

**4. An as-printed FDM wall is not a vacuum barrier — the print is structure, the film is the
barrier.** Gordeev 2018 [MEASURED] printed vessels and measured air flow through their walls
under ~0.5 bar overpressure: at extrusion multiplier k = 0.85 the walls passed 24 mL/s; the
flow fell to zero only at **k = 0.98**, and thin perimeter-only walls (~0.5 mm) were "often
completely untenable in terms of sealing, for all the possible k-values." Walls of ≥ 1.1 mm
sealed because the space between perimeter arrays is filled by a homogeneous inner layer that
closes the aligned-seam channels. Three caveats we attach before leaning on it: the test
articles are **PLA through a 0.30 mm nozzle**, not CF-nylon through 0.6 mm (the k = 0.98
sealing result is stated to hold for their Nylon-C among other filaments, in supporting
material); the sensitivity is a bubble test — **9–10 orders of magnitude coarser than a
10⁻⁵ mbar·L/s vacuum budget**, so "completely blocked" here says nothing about holding vacuum
for a season; and the k threshold is one lab, one printer, one slicer. What it is good for:
the *mechanism* (inter-road microchannels, concentrated at coinciding seams) and the shape of
the fix (k → 1, walls thick enough to bond an inner layer). It is also the physical
justification for a ±1.5% part-mass QC gate — wall porosity tracks k, and mass tracks k —
though the audit correctly flags that gate as resting on this **single source**.

**5. The polymer itself outgasses more than any plausible leak budget.** Povilus et al. 2014
[MEASURED, with an extrapolation flag] measured **SLS-printed PA12** at 3×10⁻⁸–4×10⁻⁷
mbar·L/cm²·s *after* cleaning and bakeout, residual gases atmospheric (trapped air), and found
the material could only be baked at 65 °C — a 100 °C bake degraded the vacuum to ~10⁻⁶ mbar
and left residue. Scaled to the demonstrator (44 L, ~0.75 m² internal printed surface), that
is 2.3×10⁻⁴–3×10⁻³ mbar·L/s of outgassing against a 90-day, 1%-of-an-atmosphere budget of
~5.7×10⁻⁵ mbar·L/s: **4–50× over, with zero leaks.** [OOM on the scaling] Two honesty labels
on this, both audit-flagged: the measurement is **SLS PA12, extrapolated across process (FDM)
and material (CF-filled PAHT)** — a rate-of-rise test on the first sealed cell is the real
number; and the **budget itself is invented** — the project has no vacuum-degradation
allowance in `figures.json`, this note's 1%/90 days and the barrier note's 10%/10 years were
both made up independently, and no pass/fail means anything until one allowance is adopted.
The design consequence stands at order-of-magnitude strength regardless: the barrier film must
isolate the printed polymer from the evacuated volume (inside face too), or the protocol must
bake, pump long, and expect month-one pressure rise to be outgassing-dominated. Note the
squeeze Povilus adds: bake-out above ~65 °C damaged their polyamide, and PAHT-CF's Tg is 70 °C
— the bake window is narrow and needs its own test.

**6. Hardened 0.6 mm is the vendors' own design point, but the 0.4-mm-bridging story is
ours.** [DATASHEET] All four Bambu CF-nylon TDSes list "Nozzle Size: 0.4, 0.6 (recommended),
0.8 mm"; both Polymaker TDSes state a brass nozzle lasts "approximately 9 h" on CF nylon and
require a wear-resistant nozzle. So 0.6 hardened is manufacturer consensus, not project
eccentricity. But `analysis/vacuum-cell.md`'s stronger claim that chopped fibre "bridges a
0.4 mm orifice" is **community anecdote, not vendor fact** — every vendor lists 0.4 mm as
usable, none publishes a clog-rate comparison, and the audit flags the sentence as unsourced.
The design point survives (a shop running many machines wants the reliability margin); the
stated mechanism should be softened or sourced.

**7. Shrinkage at 251 mm is systematic, therefore removable.** [DATASHEET] Polymaker's 40 mm
shrinkage cubes: PA12-CF10 prints −0.30% (X-Y) / −0.53% (Z), moving to −0.40% / −1.30% after
annealing; PA6-CF20 prints +0.25% (X-Y length) / −0.25% (Z) but its 10 mm *diameter* feature
shrinks −2.7%, −2.9% annealed — the large number is cross-sectional, not height. A 251 mm
strut printed vertically carries PA12-class Z shrink of ~−1.3 mm — enormous against a net
joint fit, trivial against a per-batch scale factor. Anneal *before* final measurement (the
anneal adds up to −0.8% more Z), design node joints with bond-gap compliance, and accept that
batch-to-batch scatter is unpublished by every vendor: measure it across ≥ 3 spools.

**8. PPA-CF is the material lever, with a brittleness tax.** [DATASHEET] Bambu PPA-CF: E
11800 ± 670 (X-Y) / 4300 ± 340 MPa (Z), σ 168 ± 4 / 57 ± 5 MPa, ρ 1.25 g/cm³, specimens
tested *un-annealed* with the TDS noting higher chamber temperature raises Z properties
further. Its Euler-relevant index (E_Z^⅔/ρ) beats PAHT-CF by ~33%. The tax: CAD ~191/kg, and
**Z elongation at break 0.9 ± 0.2%** against PAHT-CF's 4.1% — a brittle interlayer at exactly
the nodes and breach cases where toughness matters. One A/B strut-and-joint test decides it.
PET-CF (E_Z 2160 MPa, σ_Z 35 MPa, but 0.37% saturated moisture) is a fixture material here,
not a strut material.

## Where the sources do not support what we would like

- **No published failure-rate dataset for consumer print farms exists.** Song & Telenko 2017
  is the only peer-reviewed FDM waste measurement found and it is paywalled and **was not
  read**; no number from it is carried here. The planning figure of **5–10% scrap is
  invented** [OOM, audit-flagged], as is the 60% duty-cycle behind the throughput sketch. The
  demonstrator's own print-yield log would be a real contribution; until then every
  cost/throughput number below is decoration.
- **Throughput and cost are OOM only.** ~33 g/strut from model geometry, ~46 machine-hours and
  ~CAD 200 in material per standalone cell [OOM]. This sits on the audit-flagged bookkeeping
  discrepancy: the model's `demonstrator()` reports 0.948 kg using the array-shared strut
  convention while a standalone cell physically prints 36 struts + 14 nodes ≈ **1.32 kg** —
  ~40% heavier. Pick one convention; the printed-parts count and the mass must agree.
- **Vacuum-tightness of the printed wall was never the claim, and nothing found rescues it.**
  Gordeev's bubble-tight is mL/s-tight; Povilus says the bulk polymer outgasses over budget
  even with perfect walls; Zwicker 2015 (unread, catalogue-only) is the standard reference
  that laboratory-vacuum FDM parts get epoxy-sealed. All three point the same way: the
  "4–7 orders" gap the project already states between printed wall and barrier film is
  supported, and the outgassing number tightens it.
- **The wet-state modulus of the actual strut material is unmeasured by anyone.** Everything
  rests on the PA12-class analogy. Expected knockdown −7–10%; it currently hides inside the
  ×1.31 safety factor and should be verified before it silently eats margin.
- **Every structural number in this note is a vendor datasheet number.** Printed specimens,
  vendor labs, and each TDS's own disclaimer that values are for reference and comparison
  only. Nothing here is an independent measurement of the material the demonstrator will
  print; the strut buckling test in the verification plan is what converts DATASHEET to
  MEASURED.

## What this project takes

The 0.6 mm hardened / two-perimeter design point, now vendor-sourced; a 1.26–1.44 mm as-built
wall and the ~5% mass correction; the anneal-and-dry process step with its Tg-70 °C bake-window
conflict recorded; PAHT-CF confirmed as the right nylon *class* for outdoor exposure, with its
wet knockdown flagged unmeasured; k → 1 extrusion calibration and a ±1.5% mass gate as the QC
core (single-sourced, cheap, mechanistically justified); per-batch Z scale-factor calibration
at 251 mm; and the demonstrator protocol change that outgassing forces — bake, film the inside
face or budget for a getter, and design the first pump-down to distinguish outgassing from
leaks (rate-of-rise vs temperature separates them).

## Corrections made while checking the draft against sources

The scratch draft of this note said Gordeev measured at "0.5–4 bar" (the paper's flow tests
are ~0.5 bar overpressure), attributed PA6-CF20's −2.7% shrink to the Z axis (it is the
diameter feature; Z is −0.25%), and described Polymaker's conditioned PA12 specimens as at
"equilibrium" (they are at 2.92% moisture after 60 °C immersion). It also carried a Song &
Telenko waste headline from secondary reporting; dropped here because the paper was not read.
