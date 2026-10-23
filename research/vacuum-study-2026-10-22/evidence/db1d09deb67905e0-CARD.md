# CHECK-045 — independent damage-tolerance audit

**Complete with corrections.** The main conditional danger screens reproduce.
Neither P2 nor P3 has demonstrated installed damage tolerance. The owner's
categorical statements about every puncture or member loss are stronger than
the unvalidated models support. All results remain QUESTIONABLE; transferred
properties and operating scenarios are PROJECTION. No installed allowable,
safe operating procedure, procurement or contact with another seat is claimed.

Order: `ord-admiral-rr2-check045-codex-d1c0-1020`.
Owner report: `rpt-ref-57c98dcce7960aca042a`.
Nine owner/predecessor programs remained unread and unexecuted.
The frozen report and its non-code inputs are under inputs [source link unavailable in this public projection].

The check contains 1358 comparisons: 895 arithmetic/search,
311 trajectory, 56 selected frame and
96 independent witness/evidence/invariant checks.
1287 pass their declared tolerances; 71 differ.
These include search improvements and approximation differences, not only errors.
[MISMATCHES.json](ab67a5776e8e19ef-MISMATCHES.json) lists every differing field with both values,
then adds six primary-source mass/energy corrections, seven prose/integer
corrections and four condition-number fields whose matrix constraints were not
stated in the permitted non-code inputs. Those diagnostics are explicitly
distinguished from arithmetic errors.
The owner's priced geometry witnesses forward-score successfully; the 96
audit/invariant checks and all 56 selected frame comparisons pass.

Independent critical checks [source link unavailable in this public projection]

## P2: the important numbers reproduce

| Quantity | Independent value | Interpretation |
| --- | ---: | --- |
| Membrane force per face | 238.652095 kN/m | pR/4 |
| Face bending rigidity | 12.194523 N·m | nu=.0752 |
| Typical core crush used | 0.241 MPa | rounded; not an installed minimum |
| Clamped / simply supported patch cutoff | 54.779991 / 27.127598 mm | proposed growth model |
| 80 mm patch growth depth | 0.609913 / 0.366023 mm | clamped / simply supported |
| 50.8 mm hail crushed diameter | 80.865106 mm | **width, not depth** |
| Fluid / Shi / all-energy dent | 0.390712 / 1.675384 / 5.430417 mm | three conditional impact readings |
| Design-hail growth threshold | 0.611682 / 0.372950 mm | clamped / simply supported |
| Pressure fraction eliminating modeled growth | 0.458903732 | clamped, same fixed footprint |
| Air admitted at 500 m convention | 2645.660029 kg | full-volume, isothermal reference |
| Time through 200 mm stationary valve | 614.067073 s | includes short subsonic end interval |
| Available mass to usage=1 | 14.580616 kg | 11.602885 g/m² |

Thus the design hail exceeds the clamped threshold on the Shi and all-energy
readings; it exceeds the simply supported threshold on all three. The 0.914 m/s,
0.5 m contact expends more than the core-crush capacity. The analogous
lambda-1/Lee-depth contact speed is 0.494866 m/s.

The global-map threshold lambda=0.630970, widths and 16.057336/9.318286 mm
depth inversions also reproduce. They remain transferred dimple-map screens,
not a validated result for interacting impact damage in a sandwich.

The mass rejection is robust in the stated model. Bridging the 80.865 mm
patch requires a 1.030199 mm face; **faces alone weigh 4789.970 kg**, versus a
4169.660 kg structural upper bound even before the necessary core. Required
crush 0.577091/1.763546 MPa corresponds to density multipliers 1.688638/3.300820
under the assumed k^(5/3) law. The priced denser cores and shields reproduce.
Their `feasible=true` fields must not imply allowed optimism usage: six such
rows exceed one. [Detailed arithmetic](e8cf84f14908806d-ARITHMETIC-CHECKS.json).

Corrections: the 55 mm clamped threshold is **19.176311 mm**, inside the
23.237218 mm core, contradicting its table cell. Pach's test-depth field must
be **0.0011 m**, not 1.1 m, and the modeled 1.489–1.541 mm is outside the stated
1.1–1.2 mm residual-test range. The primary thesis supports the measured range,
not the claimed calibration agreement. [Pach thesis](https://espace.rmc.ca/jspui/bitstream/11264/2883/1/AlekPach_Thesis_Submitted.pdf).

IEC's table prints the 35/55/65 mm ball masses: **20.7/80.2/132.0 g**.
Their corresponding energies are **7.657344/46.083321/88.894740 J**, rather
than 7.643405/46.071507/89.128614 J. The primary page was visually checked.
This does not alter the NBS 50.8 mm design case or the resulting growth
classifications. Table image [source link unavailable in this public projection],
[exact corrections](86a037c6487bae16-IEC-MASS-CORRECTIONS.json).

## P3: nominal point, contact and lost-member screens

The nominal 022d point reproduces: SF 1.258252477, spacing 3.170758569 m,
OD 275.082856 mm, wall 1.137364845 mm, force 873.771337 kN,
film 214.541558 kg and tubes 4183.590023 kg. Total-gauge film stress
1.382870316 GPa corresponds to **2.765740632 GPa in each directional ply**,
or 47.6852% of the assumed 5.8 GPa fibre strength.

The non-governing Perry value is wrong: **3.454499160**, not 4.095817936.
The direct magnified-bending equation, separate quadratic root and pinned
022d table agree. Correcting it leaves the nominal controlling factor unchanged.

The tube-contact transfer reproduces 55.549976 MPa per MPa pressure and
the design-hail conditional tube-hit probabilities **0.011321398–0.052772758**.
The 299/192 MPa characteristic strengths and 4.6/5.5 Weibull moduli are
supported; effective size, flaw population, impact dynamics and prestress
transfer are not qualified. [ORNL/INL primary report](https://lwrs.inl.gov/content/uploads/11/2024/03/M3LW-13IN0504053-Silicon_Carbide_Ceramic_Matrix_Composite_Failure_Mode_Analysis.pdf).

For independent repeated trials, exact real-valued 50%-failure counts are
**60.877292/12.784859**, versus the stored rare-event approximations
61.224523/13.134564. Integer ceilings remain 61/13. Identical repeated loading
of one specimen does not by itself justify independent strength redraws.
Neither per-tube-hit probability nor tube coverage supplies a storm frequency.

The four filed rigid-joint removals reproduce: stress ratios
**2.427468–3.270739**, moments up to 129.311660 kN·m and tension up to
947.133864 MPa. The independent model also checks all six f4 and nine f5 edge
classes. Their combined range is **1.959485–3.270739** in stress ratio and
**0–1019.372 MPa** in maximum tension. Consequently the four cases are
examples, not a bound on every lost member. A pin-jointed compatibility
calculation gains one non-rigid mechanism after a member is removed.
The static screen does not prove a dynamic cascade for every case.
[Mesh and all cases](367d897e98a75dbc-FRAME-RESULTS.json), [condition/rank diagnostics](3af94e9e28b636fd-TRUSS-RANK-CHECKS.json).

The merged-bay geometric factor 1.5 and film SF **0.838834984** reproduce.
So do the projected slit half-lengths 0.006741–1.908531 mm.
These use substitute-polymer toughness and assumed moduli; an installed
PBO laminate's notch tolerance and arrest behavior remain unknown.

The owner's priced witnesses are numerically consistent, but the new search
finds stronger alternatives within the same scalar model:

| Case | Filed SF | New witness SF |
| --- | ---: | ---: |
| 1.0 GPa film allowable | 1.196893 | 1.200403 |
| 1.5 mm minimum tube wall | 0.800189 | 0.805476 |
| 2.0 mm minimum tube wall | 0.469060 | 0.483053 |
| 3.0 mm minimum tube wall | no point reported | 0.223304 |
| 303.532 MPa tear-screen allowable | 0.975205 | 0.975445 |

At the last point film mass is **848.604 kg**, versus 880.534 kg in the
filed local solution. None of the wall/tear fixes reaches SF1; these are
improved witnesses, not a proof of a global optimum or installed strength.
[Forward checks](6c1cd1eb6cc1de19-FILED-WITNESS-CHECKS.json),
[independent mass/section/stress invariants](53dec7f6747b6ef6-NEW-WITNESS-INVARIANTS.json).

## Leak and operating-model audit

All headline flow, pressure, touchdown and valve numbers reproduce under
the declared gross-mass, fixed-volume, isothermal assumptions:

| Quantity | Independent value |
| --- | ---: |
| 1 mm hole initial inflow | 0.107710854 g/s |
| Hole for 0.914 m/s touchdown | 63.100934–65.606770 mm |
| Hole for 4.2 m/s touchdown | 130.226408–146.972238 mm |
| 0.3 m hole touchdown speed | 8.551214–11.354483 m/s |
| Torn bay touchdown time | 23.468391–28.766999 s |
| Torn bay touchdown speed | 23.090363–34.587475 m/s |
| Valve for 0.914 / 2 / 7.5 m/s | 69.937748 / 103.455491 / 200.340697 mm |
| 1 Pa / 0.1 Pa one-hour equivalent leak | 0.363443 / 0.114931 mm |

The neutral full-sphere pressure ratio is **1.011407511**; the smaller P2
gas volume gives the approximately 1.0110 pressure result. This is a
temperature/volume convention, not increased differential pressure equal
to the entire outside pressure rise. The valve table uses the hydrostatic
pressure gradient; the neutral ISA density-gradient diameters are
62.933750/93.094819/180.277342 mm. Both require a specified control objective.

Twenty-four `t_first_half_kg_s` fields are late relative to rooted events:
for a 100 mm hole **0.464206 s**, not 0.770164 s; for a torn bay
**0.000837478 s**, not 0.001535376 s. These errors do not drive the published
touchdown values. [Exact event differences](11eb13a53720b436-LEAK-DIFFERENCES.json).

The trajectory's initial non-air mass is **4889.444 kg** for both hulls:
it is a full gross neutral reference, not the demonstrated carried inventory
of the built 028b/022d points. It also terminates with the sphere centre at
zero altitude. First contact over level terrain is at **10 m centre height**.
On that correction, the same reference torn bay reaches ground in
23.179081–28.334006 s at **23.099647–34.541863 m/s**.
The admitted 5130–5131 kg of gas is not net heaviness; the latter is about
**4889 kg** after subtracting local displacement. [Ground sensitivity](2ccd6a9f6262bde3-GROUND-CONTACT-SENSITIVITY.json).

The 46% venting result is a conditional reduction of the modeled load,
not a completed handling plan. At sea-level ISA the same absolute
differential needs **2912.791 kg** air on the full-volume convention.
An airborne neutral hull becomes heavy when vented; support, descent and
landing must be specified. A regulatory test velocity is not a demonstrated
safe speed for this shell. The atmosphere's 500 m reference is not by itself
an AGL operating altitude.

## Evidence and disposition

All 388 source-library rows have source URLs and QUESTIONABLE tags, and all
87 selected value mappings agree with their underlying records. Independent
retrieval yielded 41 substantive files; five eCFR access pages are quarantined.
The named CFR quantities were checked in the official 2025 annual edition;
this is historical source verification, not a claim of a current regulatory
route. [Evidence ledger](fe1ec202647ebc8d-EVIDENCE.json).

All 36 frozen inputs remain intact. The final recheck found a later COMMON
amendment about simulation-job retry; 35 of 36 live originals still match.
No scientific input changed. [Recorded amendment](731651c66897eaa0-INPUT-DRIFT.json).

The tap-test 41.8/29 mm figures are disbond a90/95 values on aluminium.
The 0.2 mm laser statement is a contour interval and measurement threshold,
not established Be damage-detection performance. [Primary tap study](https://icaf.aero/icaf2023/proceedings/documents/55.pdf).

All **15 new and 16 inherited NFIs remain open and nonblocking**.
The proposed corrections are filed here for downstream adoption; the owner's
artifacts remain unchanged. No installed SF, damage-tolerance qualification
or universally safe puncture/dent limit is established.
[Method](fb002a1ddc0eb6f4-METHOD.md), [full findings](ab67a5776e8e19ef-MISMATCHES.json),
[NFI register](41b8aa9cd7a7898c-NFI.json), [machine results](255297b7f73fea31-RESULTS.json).

The brief names no successor. Stop and file; return to SLEEPING.
