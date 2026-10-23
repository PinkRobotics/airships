# MAINLINE062 conditional manufacturing route

**QUESTIONABLE / PROJECTION. No cheapest qualified route has been established.**
The proposed candidate uses supplier-formed face panels, matched cores,
panel-level cure, a removable ground jig with adjusters, measured seam closure,
and a passive completed sphere. It minimizes the additional *assumed airborne*
support mass among the compared approaches. Neither its tolerance attainment nor
its cost ranking is demonstrated by a supplier or physical article.

Large single-piece spinning/stretching has no matched 20/40/60 m Be production
and tolerance record here. A reflector or segmented-mirror back structure is
effective for shape control but would require a new flight mass bill. Optical
polishing alone cannot remove the bonded sphere's residual stress, seam offsets
or instability. These comparisons motivate the candidate; they do not prove an
economic optimum.

## Proposed process and the evidence it needs

1. Release the material/process evidence in `ADMISSIBILITY.md` and `FE-NEXT.md`.
   Procure actual minimum-gauge sheet and usable blank dimensions. The inherited
   R10 24 × 72 inch layout is not confirmed for its thin stock class. Recompute
   seams and mass if smaller blanks or forming losses are required.
2. Have a qualified supplier form the two face sheets of each curved panel.
   Map thickness and shape after release from forming tools. Machine/profile
   the core to the measured faces, preserving known ribbon orientation and
   cell venting. Reject or separately qualify localized thinning and dents.
3. Bond and cure individual panels with the exact released Be surface
   preparation, primer and AF 163-2U process. The proposed 200 °F cure is a
   starting proposal, not a qualified Be/CR III recipe. Measure shape and strain
   after cooldown and tool removal, and check the bond nondestructively.
4. Assemble panels on an adjustable full-sphere ground jig inside a controlled
   hall. Use the approved scarf geometry and seal process, close sectors in a
   measured sequence, and inspect both face seams. Hold shape while the seam
   reaches its qualified state. Record material added for every adjustment,
   seal, shim and repair.
5. Remove the jig in a controlled sequence and remeasure the unsupported
   sphere. Repeat over the intended thermal range and incremental evacuation
   with pressure response and leakage measurements. A sphere that needs
   retained adjusters or a frame fails this particular bill; add those items
   and re-evaluate instead of treating them as free.

A curved panel, joined panel pair and released closed sector/shell are necessary
process articles before the whole-hull acceptance claim. Their measurements must
show that the process retains shape; the analysis must predict their pressure
response using independently measured properties. The final qualification
article count and destructive-test program remain unpriced.

## Conditional shape targets

These proposed shop caps leave some headroom below the conditional SF 1.05
face-yield screen. They are **not released acceptance limits** and have no
demonstrated process capability.

| Radius / diameter (m) | Model limit after cure debit (mm) | Proposed peak inward shop cap (mm) | Gaussian e-fold span w (m) | Initial broad-field scan pitch ≤ w/8 (mm) |
| --- | ---: | ---: | ---: | ---: |
| 10 / 20 | 0.793 | 0.60 | 0.325 | 40.7 |
| 20 / 40 | 1.628 | 1.20 | 0.645 | 80.7 |
| 30 / 60 | 2.486 | 1.80 | 0.967 | 120.9 |

| Peak-error allocation (mm) | R10 | R20 | R30 |
| --- | ---: | ---: | ---: |
| Forming | 0.18 | 0.36 | 0.54 |
| Panel cure/release | 0.12 | 0.24 | 0.36 |
| Seam closure | 0.12 | 0.24 | 0.36 |
| Final support release and thermal change | 0.12 | 0.24 | 0.36 |
| Measurement uncertainty | 0.06 | 0.12 | 0.18 |
| Total, added worst-case | 0.60 | 1.20 | 1.80 |

These allocations add arithmetically; they are not independent Gaussian errors
combined by RSS. The thermal allocation needs a specified temperature field,
which is still an open process requirement.

Measure signed deviations from a common nominal geometry after a declared
rigid-body/radius fit. Do not fit away local dents or mask faulty panels.
Archive inward peak, radial span, local curvature and spatial spectrum,
including seam steps, wrinkles and interactions. The w/8 pitch only resolves
the broad Gaussian used by this scaling hypothesis. Finer seam/wrinkle scans,
gauge maps and bond inspections remain necessary. Surface finish alone is not
the pressure-hull acceptance observable.

For illustration, a single shallow Gaussian dent has whole-sphere RMS
approximately `a*w/(sqrt(8)*R)`. At the proposed peak caps its RMS would be only
0.0069, 0.0137 and 0.0205 mm. Thus an excellent-looking global RMS can coexist
with a design-significant local dent. No acceptance threshold is inferred from
this illustration.

## Complete inherited mass bill plus the proposed addition

`MASS-TABLE.md` shows every ISA line. `MASS-BILL.csv` and `RESULTS.json` retain
all six weather accounts and the 057 concept mass-growth calculation. The
selected endpoints use **mask 15 and actual joining**, not the separate 5%
joint-floor cases. Existing face, core, joining, finish, pad, gas, system,
water, primer and contamination items are preserved once. Weather headroom
is a lift debit, not physical mass.

The only new retained allowance is **0.020 kg/m²**: 0.004 for targets and 0.016
for local shims/filler. This adds 25.13, 100.53 and 226.19 kg, with 30% concept
growth on the addition. Those masses are assumptions, not measured adequacy.
The ground jig is explicitly removed; its projected 25–75 kg/m² is costed.

| R (m) | ISA payload before growth (kg) | ISA with concept growth (kg) | Other inherited weather case with concept growth (kg) | ISA with hypothetical flat 5% hardware growth (kg) |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 102.12 | **−611.48** | **−773.47** | −123.27 |
| 20 | 2,893.77 | **−2,553.52** | **−3,854.68** | 1,133.37 |
| 30 | 11,410.95 | **−6,703.78** | **−11,101.63** | 5,510.56 |

The hypothetical flat-5% column is a maturity sensitivity, not a released
substitute for concept growth. In the other inherited weather case, flat-5%
payload is −275.96, −92.95 and 1,365.99 kg respectively. Consequently even the
R20 favorable maturity case can lose float with modest unproved process mass.
None of the six concept-growth accounts supports a positive payload claim.

## Cost and purchasing quantities

All prices are **unquoted 2026 USD planning assumptions**, not a supplier offer,
market estimate with measured confidence, or a demonstrated cheapest price.
The range varies rates, yield and cost contingency together.

| R (m) | Finished Be face mass (t) | Purchased Be (t) | Total face blanks, ideal layout | Two-face scarf length (km) | Temporary jig (t) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 3.764 | 4.418–5.681 | 2,382 | 5.689 | 31.4–94.2 |
| 20 | 30.226 | 37.556–48.287 | 10,084 | 23.592 | 125.7–377.0 |
| 30 | 102.212 | 134.752–173.252 | 24,074 | 55.132 | 282.7–848.2 |

These ideal tiling counts omit detailed polar/closure nesting; actual panel
development may change them. Purchased stock starts from the **full rectangular
blank count before scarf trimming**, then applies a separate 90%/70%
process/procurement yield. The resulting total finished-face/purchased-stock
yield is lower. This yield and cost contingency of 30%/50% are explicit
assumptions, not proofs that the layout or quantities suffice.
No scrap-value credit is taken.

| R (m) | First-shell and listed facilities/process total | Per m² of **spherical shell** |
| ---: | ---: | ---: |
| 10 | **$66.5–477.4 million** | $52,935–379,920 |
| 20 | **$522.8 million–3.814 billion** | $104,003–758,726 |
| 30 | **$1.835–13.448 billion** | $162,219–1,189,094 |

`COST-TABLE.md` and `COST-BILL.csv` itemize stock, forming, core,
joining, cure/seam labor, retained shape hardware, jig, metrology/NDE,
finish/primer, pads, systems/service, hall, handling and an initial qualification
allowance. Every rate is in `ASSUMPTIONS.json`.

The inherited Be price assumption is $10,000–50,000/kg of purchased stock.
It dominates the arithmetic and has **no vendor quote**. Non-stock subtotals
before contingency are about $7.0–34.2 million, $26.6–128.2 million and
$63.8–302.9 million; these include facilities and the stated qualification
allowance, not just shape-setting labor. Neither stock capacity nor the forming
hours are established production facts.

This account includes a $1–5 million coupon/process/subscale allowance before
contingency. **Full-scale destructive qualification or replacement hull, land,
financing, taxes and operations are unknown additional costs, not zero.**
The result is a first-completed-shell planning account, not a qualified-flight
procurement total. Competitive quotations, article count and process yield are
needed before identifying a cheapest credible route.
