# MAINLINE-061 — method and limits

All inherited physical/material inputs are **QUESTIONABLE**. Every changed material, growth allowance, service extrapolation and closure target is a **PROJECTION**. A computed constraint ratio of one is not a qualified hull safety factor. Independent REVIEW-A remains pending under PROCESS-v2.

## Question and common account

Reprice and resize the P2 Be sandwich and P3 SiC/PBO frame at radii 12, 20 and 30 m, for the inherited ISA and “optimistic” weather accounts. Start from CHECK-057's corrected itemized bills; show their frozen values separately from the 061 reoptimized scenario. Include 054's seven-day SIOX/3A dry-cavity account in P3. Examine the actual 058 relief/finish hulls before crediting operational savings.

The lift reference is 4,889.442150186961 kg at R10, scaling as R³. P2 design pressure is `p0 max(1.01, weather_pressure_factor) + qwind`; optimistic weather also reserves 1.1318450493548677% of lift. These labels describe the inherited load model, not a comprehensive flight envelope. P3 uses the corresponding pinned 052 pressure and lift rows, including its sag debit.

For each candidate, payload equals reference lift minus all nominal mass/debit entries minus their incremental growth allowances. Change the property, resize the geometry, recompute joining/service masses, then apply growth to the resulting entries. Do not apply a blanket multiplier to the old payload deficit.

The inherited concept scenario assigns 15% to calculated structure, 30% to estimated hardware and 20% to thermal hardware. The cavity monitoring battery uses the separate 25% estimated-battery column. Existing systems, gas, external water, weather/sag and other allocations retain CHECK-057's exempt classification; the additional system-level margin discussed in the NASA paper is not imposed here. This is the requested inherited accounting scenario, not a claim that every component has achieved its declared maturity.

**Source correction:** NASA GSFC's Table VI-1 gives 5% for TRL-7 brackets/clips/hardware and 6% for batteries. 057/CHECK-057 used 6% for hardware. 061 applies 5% and keeps the earlier numbers in the pre-correction archive. The coating's embedded 10% is removed from its denominator before adding any excess allowance: `coating_mass / 1.1 × max(target − 0.1, 0)`. P3 adds growth to actual sleeves only to the extent it exceeds the already charged joint allowance. Battery separation slightly reduces the concept P3 charge.

## P2 equations and geometry search

`tf` is the thickness of each of two faces, `tc` the core thickness, `h = tf + tc`, and `A = 4πR²`.

* Pressure compression: `σp = pR/(4tf)`.
* Classical sandwich scale: `σ0 = Eh/(R sqrt(1−ν²))`.
* Core shear/crimp scale: `σcr = G h²/(2 tf tc)`; `Vc = σ0/σcr`.
* `Kc = 1−Vc/4` for `Vc ≤ 2`, otherwise `1/Vc`.
* Global screen: `γ Kc σ0/(σp + σcure) ≥ 1`.
* Local demand includes pressure, thermal gradient, thermal bending and cure mismatch. Face compression, crimping, wrinkling, intracell dimpling, core crush, scarf shear, core-wall yield and thermal interface shear all remain active.
* Wrinkling resistance is `β Q sqrt(E Ec tf/tc)`, where `β³ + β − 1 = 0`.
* The scarf screen is average shear ≤10 MPa at the inherited scarf ratio 30.3413973. It caps the relevant face demand near 304 MPa even when face strength increases.

The primary, already favorable endpoint uses E=293.6 GPa, strength=379.2 MPa, Q=0.82, γ=`0.2+0.4 min(Vc,2)` and bond film 0.0732364 kg/m²/interface. The handbook sensitivity uses E=290 GPa, strength=345 MPa, Q=0.33, γ=0.2 below Vc=2 (1 above), and twice the film mass. Neither basis is a qualified full hull.

The core is the inherited CRIII 5056 3/8-1.0 row: density 16.018463 kg/m³, through-thickness modulus 103.421 MPa, weak-direction shear modulus 46.884 MPa, cell size 9.525 mm and crush 241.317 kPa. Thermal interface shear uses the 25 psi minimum-average weak-direction value. P2 retains the mooring pad, actual film/scarf/splice/seal mass, primer, absorbed water, 24-hour gas/pressure screen, systems, exterior water and contamination.

R12 uses the 048 MLCCAg thermal table. R20/R30 retain the 040 temperature table with the 048 coating mass transfer; this is an unresolved optical/temperature transfer. Unlike the old large-R witness, 061 includes cure compression in the global denominator as in the later direct 048 calculation, and resizes absorbed water. The frozen CHECK-057 account is displayed separately so this scenario change is visible.

For each property factor, search core thickness over `[0.0012 R/10, 1.4 R/10]` m on a logarithmic grid, solve the minimum feasible face thickness, and refine local maxima and feasibility boundaries. Face thickness is bounded between 1 µm and `min(0.0195, 0.008 R/10)` m. Main searches use 180–320 core points; closure witnesses are checked again with 1,000. Factors are bracketed and refined. Modulus receives an additional 25-point scan over factors 1–5 with peak refinement because its thermal penalty makes feasibility nonmonotonic.

The improvement conventions are:

| Variable | Factor ≥1 means |
|---|---|
| Face strength / modulus | Multiply the named property, retaining other properties |
| Face density | Divide density by the factor; retain the endpoint's mechanics and thermal constants |
| γ | Multiply the geometry-dependent knockdown, capped at 1 |
| Q | Multiply Q, capped at 0.82 |
| Core specific shear | Multiply shear modulus at fixed density, strength and thermal constants |
| Bond film / finish | Divide its areal mass, retaining its structural/barrier/optical function |

Density is a synthetic replacement-face target, not a means to make elemental Be less dense. Raising core shear at fixed density is one isolated route to higher specific shear; it is not a full alternate-core optimization. Gamma is a mathematical surrogate, not a measured fabrication tolerance.

Single-variable searches extend to 10,000 except physical γ/Q caps. “Not alone” means no closure in this declared model/domain, and reports the remaining binding screen; it is not a theorem about all possible materials. Product minimization jointly varies the eight factors and both thicknesses using constrained multistart SLSQP, with starts from every successful single-factor point and a mixed point. A fresh geometry search verifies the best result. This establishes the best feasible numerical product found, not a global-optimality proof. Product caps are 1,000 for strength/modulus/density/core shear, 10,000 for film/finish and the stated γ/Q caps.

The primary bill charges actual joining. A separate sensitivity retains the old 5%-of-face-plus-core floor. These are different bookkeeping assumptions; the comparison is not allowed to erase joining twice.

## P3 equations, resizing and limiting certificate

Use the pinned 052 f5-019 family: 252 nodes, 750 members and 500 membrane bays, with `g/R = 0.00868494175` and member section area proportional to R². The current whole-member compression requirement is about 1.055 GPa, below the assumed 3.9 GPa SiC endpoint. Local tube-shell compression fixes the minimum section in this family. Increasing compressive strength alone therefore cannot reduce the tube section. A different g/R, topology, tube material modulus/density or validated local-shell law requires a new structural solution and is explicitly outside this certificate.

For each factor, resize the membrane gauge:

`t = p rc / (Fply × retention × 0.964012200518 − 90.501688129 MPa)`,

with `rc = 2.61598097465 R/10`. The endpoint Fply is 5.8 GPa and ten-year retention is `0.995^10 = 0.9511101304657719`; retention is capped at one. PBO mass is `A t × 1560 kg/m³`. The film-mass factor is deliberately generous: it reduces PBO and barrier/protection mass together while preserving all functions. Node mass is a separate factor. The tube strength factor changes the strength requirement comparison but not the binding local-shell section.

054's seven-day SIOX/3A route adds 2 g/m² barrier mass and uses WVTR 0.08 g/m²/day plus the pinned seam leakage. Recompute initial release when membrane mass changes. Solve dry-bed mass from

`0.06 Mbed = 1.1 [external water + seven-day release + 0.001 Mhardware (1−exp(−7))]`,

where `Mhardware = 5 + max(1, 0.25 Mbed)` kg. Monitoring battery mass is `0.5 W × 24 h × 7 / 108 Wh/kg = 0.77778 kg`. Retained incoming gas/water is charged only above the existing gas reserve, avoiding double charging redistribution of initial material water. R20/R30 extend a source calculation conducted through R15.

The combined-lever limit gives free film and nodes, infinite ply/member strength and perfect retention. A stronger certificate also deletes every film, node, sleeve/joint and cavity gram, retaining only the minimum tubes plus systems, vacuum service, gas, exterior water, contamination, load introduction, sag and weather debits. Negative payload even in this lighter-than-possible account excludes closure by the named levers within the inherited family. A further sensitivity gives that account the entire 058 full-to-relieved tube mass fraction for free. This overcredits relief relative to 057 and omits its lost lift, deliberately favoring closure.

## Relief, finish, history and supply

058's full-range starting pressure is higher than the 057 ISA design pressure. Therefore its full-to-relieved saving cannot be subtracted directly from the already lighter 057 bill. Reprice 058's actual full, trim−30, AlAOC and low-emissivity-night hull bills, including their retained joining floor, under the common growth account. Add a 5 kg relief valve with 30% growth; omit bladder and admitted-air debits to form an optimistic upper bound. Different operational envelopes are explicitly labeled. Thermal finish can extend cold-edge operation without closing the material budget.

Compare 017b's historical factors as a different model, not as interchangeable starting points. Its older P2 model omitted the later thermal/service account and its old P3 film trend concerned a different Ti/Kapton route. Also show growth/no-growth factors within 061's own handbook model to isolate the accounting effect. Use 017b's pinned historical trend data; do not invent a positive trend or a forecast date where the closure property has no such trend.

Be demand is the reoptimized nominal pure-Be face mass for the no-growth geometry, plus a separately labeled 15% face budget. Divide by USGS's estimated 2025 world mine production, rounded 430 tonnes Be content. This denominator is not refined sheet capacity, and the numerator excludes manufacturing losses, scrap and spares. The lighter replacement-face closure target is not counted as literal Be production.

## Reproduction and handoff

`source61.py` copies only specifically named, hash-checked upstream files. Owner code is retained as evidence where read but is not imported or executed. `check61.py` checks direct P2 bills and all six R10/R12/R15 seven-day P3 reference rows. `run61.py` computes factors; `audit61.py` preserves the pre-correction result, checks dense closure witnesses, applies the NASA column correction, and calculates operational/supply sensitivities. `build61.py` prepares the handoff, and `validate61.py` checks its arithmetic and pins.

All substantive numerical runs use `admit61.py` through simjob with one core, 1 GiB memory and numerical-library thread counts set to one. It retries only admission-refusal exit 75 with the identical request. Logged durations are measurements, not work budgets. To reproduce from this checkout, use:

```sh
env TMPDIR=unpublished-local-ref:1ffe4110219d37c0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 .ship/work/outputs/vacuum-mainline061-improvement-targets-growth-1020/admit61.py check61.py
```

The same wrapper runs `run61.py`, then `audit61.py`. `audit61.py` intentionally audits its immutable first pre-correction archive; use a new output directory for a new scientific revision rather than silently mixing revisions. Input pins, numerical fixes and open physical questions travel with the result.
