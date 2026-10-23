# REVIEW-A1 — MAINLINE-056 and MAINLINE-062

**Sixteen of seventeen load-bearing claims reproduce in their stated conditional scope. One differs in its mass-account values: six inherited coating-growth corrections raise payload by 0.095–0.857 kg. All six cases remain negative.** Corrections are **unreviewed**, as required by the one-round process. No pressure-hull, material, fabrication tolerance or cost qualification is released.

Unit `vacuum-review-a-056-062-1020` · order `ord-admiral-rr2-review-a1-dispatch-1020`. **QUESTIONABLE / PROJECTION throughout.** The reviewer wrote 061, not 056 or 062. No owners' code was read or run. The 17 claims and their decision relevance were written first in [LOAD-BEARING.md](50baad56ba89f51b-LOAD-BEARING.md). This half reviews only 056/062; the other half owns 058/061.

## Claim dispositions

“Reproduces” below means the specified source statement, conditional arithmetic or numerical output reproduces. It does not close the physical questions listed in NFI.json. Each claim has exactly one numerical/source disposition.

| Claim / card | Disposition | Independent result and scope |
| --- | --- | --- |
| A1-01 / 056 | reproduces | EUCASS2023-367 §§3.1–3.2.1: experiments validate axial compression; 6.03 MPa is a pressure-postbuckling prediction. |
| A1-02 / 056 | reproduces | Independent force equilibrium at the saved refined state gives 6.159020624266 MPa; original 6.159020624174. Independent raw-path maxima give 6.159020624–6.502271779 MPa. Scope: frozen-state equilibrium and sampled maxima, not a rerun of contact/plastic history or proof of physical instability. |
| A1-03 / 056 | reproduces | Independent ratios: +2.139645510%, mesh −0.115571622%, penalty −0.010452458%. These reproduce the printed rounding; they are observed numerical changes, not certified error bounds. |
| A1-04 / 056 | reproduces | Fresh Q8 elastic/prestress eigenproblems give 30.218153613699 MPa outer-radius and 28.074312431918 MPa midsurface-radius: +9.764451920% and +1.977161031% relative to 27.53 MPa. |
| A1-05 / 056 | reproduces | Withholding P2 gamma is supported: the benchmark is steel/PVC with unresolved calibration; Hexcel supplies distinct directional anchors, not a matched installed CR III crush/unload/mixed-load law. |
| A1-06 / 062 | reproduces | The source record supports withholding physical tolerance release: 345 MPa is a tensile proxy; the in-plane core law, processed compression/bond and manufactured residual state remain unqualified. |
| A1-07 / 062 | reproduces | Materion SR-200 p.1 lists representative scalar E=290 GPa. Its mechanical minimums are tensile; the source does not identify a finished, formed, biaxial compressive allowable. |
| A1-08 / 062 | reproduces | 3M p.1 lists unsupported AF 163-2U at 0.015 lb/ft². Its p.15 200°F table concerns 2K 0.060 lb/ft², so product identity does not qualify the proposed Be/CR III process. |
| A1-09 / 062 | reproduces | Eliminating C between source and target equations gives 0.792569717998 mm at R10, SF1.05, with the declared cure debit. |
| A1-10 / 062 | reproduces | The independent ratio gives 1.628412576678 mm at R20 under the same declared hypothesis. |
| A1-11 / 062 | reproduces | The independent ratio gives 2.485983493740 mm at R30 under the same declared hypothesis. |
| A1-12 / 062 | reproduces | Under homothety, R/tf and tc/tf are constant, so membrane stress, scaled residual debit and C are constant; d and allowed amplitude scale with R. This is a dimensional consequence of the hypothesis, not validation of C transfer. |
| A1-13 / 062 | reproduces | Independent stock/labor/material arithmetic and supplied facility allowances reproduce $66,519,656.56–477,421,594.60. Rates are unquoted assumptions. |
| A1-14 / 062 | reproduces | The same conditional account reproduces $522,773,952.34–3,813,773,030.71. |
| A1-15 / 062 | reproduces | The same conditional account reproduces $1,834,656,370.48–13,448,336,376.35. |
| A1-16 / 062 | differs | All six negative signs reproduce, but inherited coating growth overcharges the stated 20% total allowance. Payload rises 0.095193/0.380771/0.856735 kg at R10/20/30 after removing the embedded-margin denominator error. Six unreviewed field corrections are listed in FIXES.json. |
| A1-17 / 062 | reproduces | Seven records preserve the missing local-defect metrics. Spot checks confirm ALMA's adjusted/masked 16–17 µm RMS and S-II's 0.010 inch core-to-face gap; neither establishes this hull's maximum local defect. |

## 056: what the independent computation establishes

The original paper describes axial-compression validation separately from its pressure calculations; 6.03 MPa belongs to the latter. It therefore supplies no measured pressure-collapse target for this comparison. [EUCASS2023-367, §§3.1–3.2.1](https://www.eucass.eu/doi/EUCASS2023-367.pdf).

The review derived Q8 interpolation from an eight-term nodal polynomial basis, reconstructed deformation gradients and logarithmic elastic strains from the pinned mesh/displacement/plastic-state arrays, and integrated internal and current-surface pressure forces. The pressure obtained from free-node equilibrium was **6.159020624266 MPa**, only **9.16×10⁻¹¹ MPa** above the saved value. Relative free-force residual was **1.17×10⁻⁸**. No saved pressure entered that reconstruction. The standard [rr, zz, hoop, engineering-rz] plastic-strain layout with xi-outer Gauss ordering uniquely satisfies the checked equilibrium conventions; alternatives have residual ratios above 21.

This independently checks the decisive **frozen equilibrium state**. The pressure-path samples separately confirm its maximum and following lower samples. It does not independently recreate the full indentation/plastic history or establish the first three-dimensional pressure-control instability. The check also recovers minimum J=0.398052588 and 1543 core points beyond the retained hardening knots. The documented source extrapolation and flow/history questions remain open.

A second, fresh calculation built the perfect hemisphere and assembled elastic and unit-prestress geometric stiffness at 384 meridional elements, eight core layers and two layers per face. It reproduced both dead-pressure eigenvalues to within 10⁻⁹ MPa; eigen residuals are below 9×10⁻¹¹. The radius-reading gaps and the pressure/refinement percentages are therefore reproduced numerical quantities. Their closeness to the paper does not turn the unqualified steel/PVC model into Be/honeycomb capacity.

## 062: source and scaling checks

The source checks support the card's admissibility distinctions: SR-200 has a representative scalar modulus of 290 GPa, while its listed minimum mechanical strengths are tensile. Thin-stock availability also limits the assumed blank layout. [Materion SR-200, pp.1–3](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6). Light AF 163-2U exists; its identity does not transfer the guide's 2K 200°F aluminum-joint results to this proposed process. [3M guide, pp.1 and 15](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf). Directional coupon anchors remain distinct from a complete installed nonlinear core law. [Hexcel Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).

The shape calculation eliminates the fitted coefficient between the reference and target equations. With `d=tf+tc`, `σm=SF pR/(4tf)`, it gives `aR=a0(dR/d0)[(Fy−σres,R)/σm,R−1]/[Fy/σm,0−1]`. Using the explicitly rounded CHECK047 reference and the 057 bill-derived gauges gives the three printed SF1.05 values. Under homothety, the dimensionless stress ratios stay fixed and d scales with R, so amplitude scales with R. Holding that coefficient across nonhomothetic gauges, defects and weather remains a PROJECTION.

| R (m) | Independent cure-debited SF1.05 amplitude (mm) | Printed (mm) |
| --- | --- | --- |
| 10 | 0.792569717998 | 0.793 |
| 20 | 1.628412576678 | 1.628 |
| 30 | 2.485983493740 | 2.486 |

The precedent check supports the metric distinction, not manufacturing acceptance. ALMA's 16–17 µm figures are adjusted reflector RMS, with faulty areas masked in the prototype maps. [ALMA prototype paper, Table 2 and Figs.4/6](https://arxiv.org/pdf/astro-ph/0609329). S-II's 0.010 inch figure is a permitted core-to-face bond gap, equivalent to 0.254 mm. It is not a maximum external dent. [S-II manufacturing record, printed p.4-45](https://ntrs.nasa.gov/api/citations/19720008130/downloads/19720008130.pdf). No RMS-to-maximum-defect conversion is supported.

## Costs and the demonstrated mass correction

Rebuilding the full rectangular stock takeoff, panel count, seams, material and labor charges reproduces the six cost totals exactly at stored precision. The hall and handling lines are retained as supplied allowances: their larger-radius values imply R^2.5 and R^2 scaling, which ASSUMPTIONS.json does not spell out. That documentation/price-evidence gap is NFI-A1-FACILITY-SCALING, not a demonstrated wrong total.

| R (m) | Low first-shell account (USD) | High first-shell account (USD) |
| --- | --- | --- |
| 10 | 66,519,656.56 | 477,421,594.60 |
| 20 | 522,773,952.34 | 3,813,773,030.71 |
| 30 | 1,834,656,370.48 | 13,448,336,376.35 |

The price intervals remain unquoted planning cases with incomplete qualified-flight program scope. This review establishes arithmetic, not affordability, availability, a cheapest feasible route or supplier performance.

The inherited coating mass `m` already equals 1.10 times its unmarginated mass. To reach a 20% total allowance, the increment is `m(1.20/1.10−1)=m×0.10/1.10`. The carried 057 formula instead adds `m×0.10`, resulting in 21% total. The table below gives the six field corrections; owner files remain unchanged. These are one demonstrated inherited cause, six unreviewed correction rows.

| R (m) | Weather | Card payload (kg) | Corrected payload (kg) | Increase (kg) |
| --- | --- | --- | --- | --- |
| 10 | ISA | -611.484348 | -611.389155 | 0.095193 |
| 10 | optimistic | -773.465088 | -773.369895 | 0.095193 |
| 20 | ISA | -2553.524790 | -2553.144018 | 0.380771 |
| 20 | optimistic | -3854.681843 | -3854.301072 | 0.380771 |
| 30 | ISA | -6703.783776 | -6702.927041 | 0.856735 |
| 30 | optimistic | -11101.632034 | -11100.775299 | 0.856735 |

No float/no-float decision changes. 062's deliberate retention of the original 057 account explains the inheritance; it does not remove the denominator correction required by the stated 20% total coating allowance. The hypothetical flat-5% maturity sensitivity is not substituted for the concept-growth rows.

## Handoff

The review is complete in one round. Numerical status and physical qualification are separate in [RESULTS.json](8edf42ff4ed7d253-RESULTS.json). [FIXES.json](0063cb5be8f2809e-FIXES.json) supplies six **unreviewed** field corrections; [NFI.json](038b8c48cc2481f2-NFI.json) supplies eleven source/qualification questions. Nothing here authorizes another run, review dispatch or physical release.

Reproducible evidence: [INPUTS.json](9dca16514a02bee9-INPUTS.json), [METHOD.md](ee6e747e19fe94b7-METHOD.md), [FIELD-CHECK.json](ebd5b7692388b968-FIELD-CHECK.json), [LINEAR-CHECK.json](7c15280c1687253b-LINEAR-CHECK.json), [ACCOUNT-CHECK.json](3145170d4c6a8ead-ACCOUNT-CHECK.json), [VALIDATION.json](bb6c7c74d5e7c4f0-VALIDATION.json), and MANIFEST.json [source link unavailable in this public projection]. Simjob receipts record one-core jobs and released reservations; elapsed times are measurements, not budgets.
