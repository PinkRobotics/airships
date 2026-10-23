# MAINLINE-018b — independent pressure, shear and face-bending check

72 of 75 numeric comparisons reproduce. One already identified unequal-face omission changes three dimple fields by −0.0297486%. The pressure/crimp ratios, H80/H35 sensitivity arithmetic, and own-face-bending fractions reproduce. The carried lead least factor remains 0.650411843680531.

QUESTIONABLE properties and model transfer; PROJECTION curve/design extrapolation. Certification: none. Started 2026-10-20T00:43:38-07:00; calculation completed 2026-10-20T00:49:15-07:00. No owner script was inspected as code, imported or executed. INPUTS.json records the independent source readings and pins; RESULTS.json records every comparison.

## Source pressures

The checker independently extracted the pinned EUCASS 2023-367 PDF and visually inspected Figures 9, 10, 12 and 13. Its sections 3.2.1–3.3 give the following numerical predictions. The [Sim journal article](https://onlinelibrary.wiley.com/doi/10.1155/2024/8765733), Table 1, section 3.2.3 and conclusions, corroborates the material inputs and linear/imperfect pressure pairs. The paper's preceding validation is an axial-compression experiment; these external-pressure collapses are numerical.

| Pressure, MPa | Flat, inner face .42 mm | Dimple, inner face .40 mm |
|---|---:|---:|
| Linear perfect | 27.53 | 27.56 |
| Nonlinear perfect | 12.45 | 12.44 |
| Imperfect, converged | 6.03 | 5.63 |
| Imperfect / linear perfect | 0.219033781329 | 0.204281567489 |

The last row rounds to the published KDFs 0.22 and 0.20. Their denominator differs from the handbook crimp pressure. The journal's flat-model section repeats 27.56, but its conclusion and EUCASS explicitly give 27.53; this check uses the latter, consistent with its reported −0.11% comparison. The nonlinear-perfect values are independently verified in EUCASS; they are not quoted numerically in the journal HTML read here.

## Independent equations and correction

Source geometry: outer radius .0428 m, core .0031 m, outer face .00042 m; inner face .00042/.00040 m. The face material has E=210 GPa, nu=.33; paper foam E=40 MPa, nu=0, density=80 kg/m³. Derived isotropic Gc=20 MPa is conditional on those elastic inputs. h=tc+(t1+t2)/2, Rmiddle=Router−(tc+t1+t2)/2.

The [NASA CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf) unequal-face factor is q=2√(t1t2)/(t1+t2). Use sigma0=qEh/[Rmiddle√(1−nu²)], sigmacrimp=h²Gc/[(t1+t2)tc], Vc=sigma0/sigmacrimp, pcrimp=2h²Gc/(Rmiddle tc), and pclassical=2sigma0(t1+t2)/Rmiddle. For the flat case q=1. For the dimple q=0.999702513752156; the owner omitted it in sigma0.

| Dimple field | Filed | Corrected |
|---|---:|---:|
| sigma_0_Pa | 19119540732.739 | 19113852932.306 |
| Vc | 197.24625832023 | 197.18758027094 |
| p_classical_Pa | 767777835.49685 | 767549432.14939 |

Both remain on the crimp branch. Flat Vc=201.532463528414; corrected dimple Vc=197.187580270942. Crimp pressure and every collapse/crimp ratio are unchanged by q. Flat classical pressure 789.131279531168 MPa reproduces; corrected dimple classical pressure is 767.549432149391 MPa.

## H80/H35 rows

The pinned DIAB Divinycell H sheet H.ds-u/10_2012.rev7 was visually checked. Its ASTM C273 shear moduli are H80=27 MPa and H35=12 MPa. ASTM D1621 perpendicular compression moduli are H80=90 MPa and H35=40 MPa. These are average data at 23°C. H35 density is 38 kg/m³, versus 80 for H80 and the paper's PVC80. Matching compression modulus alone does not identify the paper foam as H35.

| Denominator case | Gc, MPa | Flat pcrimp, MPa | Dimple pcrimp, MPa | Flat collapse/crimp | Dimple collapse/crimp |
|---|---:|---:|---:|---:|---:|
| paper_E_over_2 | 20 | 3.915653417395 | 3.892483649806 | 1.539972862054 | 1.446377302132 |
| H80 | 27 | 5.286132113484 | 5.254852927238 | 1.140720638559 | 1.071390594172 |
| H35 | 12 | 2.349392050437 | 2.335490189883 | 2.566621436757 | 2.410628836887 |

These are denominator-only sensitivities: the published collapse pressures stay fixed. Changing the material in a structural simulation would also affect its collapse pressure. No new H80/H35 simulation or pressure measurement is supplied.

## Own-face bending and design interpretation

With core longitudinal rigidity neglected, let Down=E(t1³+t2³)/[12(1−nu²)] and Dseparation=Et1t2h²/[(t1+t2)(1−nu²)]. Down/(Down+Dseparation) is 0.004723195064743 flat and 0.004538262400473 dimple. Both filed fractions reproduce. This is a fraction of conventional facings-only flexural rigidity, not a measured share of collapse pressure.

NASA section 2.3.2, printed p 2-41, explicitly says neglected own-face bending can materially affect crimping; section 4.7.3.1, p 4-72, lists its neglect as an assumption. The linear/crimp ratios 7.030755040192 and 7.080312335127 mix effects and do not isolate that contribution.

The owner's lead-least-times-gamma values reproduce as scalar products. They are not all-mode least factors: even if crimp credit were increased beyond 1, unchanged wrinkling limits the lead to 0.650414127458800; face compression is also below 1. The declared gamma cap of 1 leaves the carried least at 0.650411843680531. Thus no all-mode feasibility follows from the scalar product just above 1.

These two high-Vc numerical cases exceed the conditional unity-crimp prediction. They do not calibrate the continuous optimistic curve, test its moderate-Vc segment used in 009e, or validate transfer to the 10 m honeycomb sphere. NFI.json retains that inference limit, source inconsistency, material substitutions, face-bending uncertainty and P3 exclusion. These issues do not block filing the check.
