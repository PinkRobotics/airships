#!/usr/bin/env python3
"""Assemble the check's evidence, closure matrix, and nonblocking findings."""
import hashlib
import json
from collections import Counter
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def load(path):
    return json.loads(path.read_text())


def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path.resolve()), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    table="| Prior finding | Disposition | What 015b addresses | What remains |\n|---|---|---|---|\n"
    for c in coverage:
        table+=f"| {c['index']}. {c['prior_id'].removeprefix('NFI-015-CHECK-')} | {c['status'].replace('_',' ')} | {c['addressed']} | {c['remaining']} |\n"
    (ROOT/"COVERAGE.md").write_text(
        "# MAINLINE-015b response to all fourteen earlier findings\n\n"
        "The replacement map resolves three findings, partly addresses five, leaves five outside its focused scope unrevisited, and acknowledges one still-open validation finding. Omission is not closure. These are nonblocking dispositions; they do not turn the focused map assignment into a demand to redo every earlier section.\n\n"+table)
    sh=results["independently_derived"]["shells"]
    geometry="| Shell | tf mm | core mm | teq mm | exact finite-face teq mm | R/teq | lambda-1 width m | classical wavelength m |\n|---|---:|---:|---:|---:|---:|---:|---:|\n"
    for name,s in sh.items():
        geometry+=f"| {name} | {s['tf_m']*1000:.9f} | {s['core_m']*1000:.9f} | {s['t_eq_m']*1000:.9f} | {s['t_eq_exact_ad_m']*1000:.9f} | {s['R_over_t_eq']:.9f} | {s['width_lambda_1_m']:.9f} | {s['classical_wavelength_m']:.9f} |\n"
    tolerances="| Shell | kd | Eq. 3 amplitude mm | Eq. 3 RMS mm | Lee amplitude mm | Lee RMS k1 mm | Lee RMS k5 mm |\n|---|---:|---:|---:|---:|---:|---:|\n"
    for name,s in sh.items():
        for key in ("0.9","0.7","0.595","0.5","0.468","0.3","0.2"):
            e,l=s["levels"][key]["eq3"],s["levels"][key]["lee"]
            amp="not invertible" if e["amplitude_mm"] is None else f"{e['amplitude_mm']:.9f}"
            rms="—" if e["single_dimple_rms_mm"] is None else f"{e['single_dimple_rms_mm']:.9f}"
            tolerances+=f"| {name} | {key} | {amp} | {rms} | {l['amplitude_mm']:.9f} | {l['single_dimple_rms_mm_at_k_1']:.9f} | {l['single_dimple_rms_mm_at_k_5']:.9f} |\n"
    finite_table="| Shell | k1 RMS approximation overstatement % | k5 overstatement % | Exact k5/k1 ratio | Eeq/Ef |\n|---|---:|---:|---:|---:|\n"
    for name,s in results["supplemental"].items():
        finite_table+=f"| {name} | {s['finite_spherical_area']['1']['approx_overstatement_percent']:.9f} | {s['finite_spherical_area']['5']['approx_overstatement_percent']:.9f} | {s['exact_RMS_k5_over_k1']:.9f} | {s['effective_modulus_over_face_E']:.12f} |\n"
    lee_url=next(p["url"] for p in load(OLD/"sources/manifest.json") if p["id"]=="lee2016")
    baiz_url=next(p["url"] for p in load(OLD/"sources/manifest.json") if p["id"]=="baizhikova2026")
    check=f"""# Independent check of MAINLINE-015b — ESTIMATE / QUESTIONABLE

Order `{ORDER}`. Unit `{UNIT}`. Nothing here is a certification.

The focused correction passes its arithmetic check. The live lambda-1 amplitude/width pair and nu 0.33 repair the principal error found in 015. All 1,331 scalar/display/flag comparisons match at the stated precision. There is one false blanket prose claim about rounding and two qualifications concerning RMS area measure and Lee's envelope width. These do not invalidate the reproduced arithmetic. All fourteen prior findings are dispositioned individually below; this revision does not close all fourteen.

## Independence, identity and coverage

Own `check.py` derives the equations and performs the comparisons. The owner's `map015b.py` and earlier owner scripts were not read as code or run. Pinned 015, 021 and 021b RESULTS provide geometry and gamma inputs only; this check does not redo the 021/021b optimisations. P2-E's filed input rounding is preserved. The former 015 check and its primary PDFs are immutable inputs.

All original owner/authority pins, seven owner-declared upstream pins, and the prior primary-source manifest match their hashes and lengths; `SOURCE-PINS.json` records each verification. Snapshot and prior-check pins are in `INPUTS.json`.

Every one of the 1,201 numeric, Boolean, null or decimal-string leaves of owner RESULTS is covered, with no missing or extra scalar path. Categories: 647 numeric, 223 Boolean, 24 null, 216 display fields and 91 leaves in the owner's 47 self-check records. A further 40 directly parsed CARD table entries and 90 CARD/report quantities match. `NUMERIC-CHECK.csv` gives reported value, independently computed value, exact floating-point difference and disposition for each comparison; `PROSE-CHECK.json` identifies checked excerpts. Booleans and displays are compared exactly. Raw tolerances are relative 5e-12 or absolute 2e-12; the published ten-decimal threshold is allowed 5e-11.

The published threshold 0.5183040769 differs from the independently recovered 0.5183040769297532 by -2.97532e-11, consistent with rounding. Apart from this intentional printed precision and floating-point operation-order differences, there are no numerical mismatches under the specified approximate map. Coefficients and range limits are separately checked against primary sources. Identifiers, dates and equation numbers are metadata.

## Derivation

Write face thickness f, core depth d, face-center separation h=d+f, radius R=10 m, and alpha=delta/teq. Matching the face-dominated extensional and bending stiffnesses gives

`teq_thin = sqrt(3) h`, `teq_finite = sqrt(3h²+f²)`, and `Eeq/Ef = 2f/teq`.

The latter modulus relation is still missing from the owner's description. It is required if the equivalent monocoque is used to calculate absolute pressure. This card only maps dimensionless defects and does not claim a new pressure score. For P2-E, Eeq/Ef=0.00341122758754; keeping Ef with the equivalent thickness would not preserve extensional stiffness.

At a chosen width parameter lambda,

`beta0 = lambda sqrt(teq/R) / [12(1-nu²)]^(1/4)`, `width = R beta0`, `classical wavelength = 2pi R beta0(lambda=1)`.

The map's RMS is `delta beta0/sqrt(8)`, a small-angle area approximation for a single Gaussian dimple on a whole sphere. It is not an arbitrary manufactured-field maximum or a hemispherical RMS. The classical wavelength is distinct from `sqrt(R teq)`.

For [Baizhikova et al., Eq. 3]({baiz_url}), lambda=1 gives

`alpha = -ln[(kd-0.45)/0.51]/3.88`.

There is no finite real inverse at or below kd=0.45. The reported 0.2 and 0.3 rows correctly return null. The old-to-live RMS ratio at fixed amplitude is

`2.625 [(1-0.33²)/(1-0.30²)]^(1/4) = 2.611262732308197`.

For [Lee et al., Eq. 23]({lee_url}),

`alpha = 0.25/(kd-0.068) - 0.28`.

This uses the original coefficient 0.068. Alpha at kd 0.9/0.7/0.5/0.3/0.2 is 0.0204807692308 / 0.115569620253 / 0.298703703704 / 0.797586206897 / 1.61393939394. Its forward equation round-trips every level checked.

{geometry}
## Recomputed tolerance rows

These are the owner's conditional small-angle RMS quantities, not validated manufacturing tolerances. Lee k1 and k5 columns bound geometry at the envelope-derived amplitude; they are not a statement that every width has the requested kd.

{tolerances}
All nine levels for every shell, including both unrounded gammas, are retained in `RESULTS.json`; above are the seven requested rounded/low-kd levels.

For the actual 021 geometry at gamma 0.5953179642995181, Eq. 3 amplitude is 11.8014082501152 mm, matched RMS 0.139344127347082 mm, and retired RMS 0.363864126707443 mm. Lee amplitude is 7.07901609093948 mm and the approximate geometric RMS interval is 0.0835848823091335–0.417924411545668 mm.

For actual 021b at gamma 0.46822856667720764, Eq. 3 amplitude is 45.8194414540033 mm, matched RMS 0.654415969675917 mm, and retired RMS 1.70885203304205 mm. Lee amplitude is 18.3916873867886 mm and the approximate geometric interval is 0.262679193662454–1.31339596831227 mm.

## Source limits and interpretation

Baizhikova's source computations use nu 0.5 and R/t from 100 to 1550. Its discussion explicitly excludes the near-perfect asymptote around alpha below 0.07 from what Eq. 3 captures. The kd 0.9 inverse is 0.0322585419984552, so every such row needs the limitation. P2-E has R/teq=50.7479713774, outside the source range. The three Be geometries lie inside that radius interval; this does not validate material or sandwich transfer.

Lee section 7 supplies no FEM values below alpha 0.15 and no ODE values below 0.2. The computed radii are R/t=100 and 200. Kd 0.9 and 0.7 inverses are below both amplitude limits. Kd 0.595 and the actual 021 gamma lie between the two limits. Kd 0.5, 0.468, actual 021b gamma, 0.3 and 0.2 satisfy both amplitude cutoffs. The numerical range flags all reproduce. Be-015 and Be-021b lie between the computed radii; P2-E and Be-021 lie outside the interval. None is exactly a computed radius.

Lee Fig. 6(c) provides a minimizing width as a function of amplitude. The scalar Eq. 23 does not encode that width, but the paper does provide information beyond the scalar envelope. The owner's k1–k5 RMS span is a defensible broad geometric bound, conditional on the source sweep and mapping. It is not an iso-knockdown curve; equality at both endpoints is not established. This is NFI-015B-CHECK-LEE-CRITICAL-WIDTH.

## Exact corrections and additional qualifications

The CARD says rounding gamma changes the fourth digit of amplitude. For 021, using 0.595 instead of its actual gamma gives 11.8219982525557 rather than 11.8014082501152 mm: +0.0205900024405 mm, or +0.174470724206% relative to the actual-gamma value. For 021b, using 0.468 gives 45.9929887386092 rather than 45.8194414540033 mm: +0.173547284606 mm, or +0.378763422466%; the third significant digit changes. On P2-E the latter delta is +0.640836306447 mm. The two numerical columns are correct; the blanket prose is not. NFI-015B-CHECK-ROUNDING-PROSE records this correction.

For a Gaussian displacement referenced to the original spherical surface, retaining the spherical area element gives

`RMS/delta = sqrt[ (1/2) integral_0^pi exp(-2(theta/beta0)²) sin(theta) dtheta ]`.

Replacing sin(theta) by theta and extending the negligible Gaussian tail gives the owner's beta0/sqrt(8). Direct quadrature and the equivalent infinite-tail Dawson-function expression agree to better than 1e-13 in RMS/amplitude for these widths. The widest P2-E k5 calculation overstates this spherical-area RMS by 0.628886203836%; its exact k5/k1 ratio is 4.96999986296 rather than 5. At lambda 1, the largest overstatement is only 0.025110128610%. This is a model-precision qualification, not an error in implementing the stated formula.

{finite_table}
NFI-015B-CHECK-RMS-AREA asks that the approximation be named. No fit coefficient is changed and no physical validation is inferred from this integration.

## Continuous threshold and manufacturing comparison

The original 015 threshold is independently reconstructed from its mass law `1.05 Mstructure + 100 = 4889.442150186961 kg`, pressure 95460.83791390515 Pa and original Be/CR-III properties. Yield sets f=pR/(4 sigma_y). At the yield-feasible core-fraction boundary x=0.140403238862653, global buckling with the existing NASA Kc gives kd=0.5183040769297532. Global capacity is increasing across the yield-feasible split interval, as confirmed by the analytic derivative; all other original modes exceed one at the crossing. The 0.518 grid optimum is 0.999887434269507 and the 0.519 grid optimum is 1.00017826831089. Thus 0.519 remains the first passing level on the original 0.001 grid. This recheck does not conflate the original 015 optimum with either 021 floating-point geometry.

Against 0.25 mm, the matched Eq. 3 RMS ratios are 0.697838266371 for P2-E kd 0.9, 0.157890102811 for frozen Be kd 0.9, 0.557376509388 for actual 021 and 2.61766387870 for actual 021b. The directions in the corrected CARD are right. The last is looser; the first three are tighter. The GBT figure refers to an active assembled surface under benign nighttime conditions, not proof of a loaded pressure-shell defect spectrum. The corrected CARD appropriately disclaims a manufacturing proof, but does not restore all old benchmark provenance.

## Response to every earlier finding

Three resolved in this map; five partly addressed; five not revisited because they are outside the focused map; one validation finding acknowledged and still open. The unchanged original sections are not silently approved. `COVERAGE.json` retains the original text and requested action for each finding.

{table}
## Filing

`NFI.json` carries the eleven earlier findings that remain open in some respect and the three new qualifications, all nonblocking. `COVERAGE.json` separately records the three resolved findings. No additional job is named. The one report closes the assigned check work; it does not certify a vacuum shell or close the remaining scientific questions.

Start measured {results['started_at']}; arithmetic completed {results['calculated_at']}. Final assembly/end time is recorded in WORK.json. These are measurements, not work limits.
"""
    (ROOT/"CHECK.md").write_text(check)
    card=f"""# MAINLINE-015b independent check — ESTIMATE / QUESTIONABLE

Unit {UNIT}; order {ORDER}. No certification.

The corrected lambda-1 amplitude/width pair and nu 0.33 pass. All 1,331 arithmetic/display/flag comparisons match; all 1,201 owner RESULTS scalar leaves are covered. Original and upstream pins match. Only own arithmetic ran.

Continuous kd threshold: 0.5183040769297532; first passing original grid level: 0.519. Old mixed RMS / corrected RMS: 2.611262732308197.

Actual 021 matched amplitude/RMS: 11.8014082501152 / 0.139344127347082 mm.
Actual 021b: 45.8194414540033 / 0.654415969675917 mm.

The fourteen earlier findings are all answered in COVERAGE.md: three resolved in the new map, five partly addressed, five outside-scope topics not revisited, and one validation issue acknowledged but open.

Three new qualifications: the rounding sentence understates the 021b change (+0.3787634225%, affecting the third significant digit); whole-sphere RMS uses a small-angle area approximation (largest k5 overstatement 0.6288862038%); Lee's width span is a conditional geometric bound, with the actual minimizing width described by its Fig. 6(c).

Remaining source and sandwich-transfer limits stay QUESTIONABLE. Eleven carried findings and three new findings are nonblocking in NFI.json. CHECK.md supplies formulas, exact comparisons, full tables and source links. Stop; no successor job.
"""
    (ROOT/"CARD.md").write_text(card)
    print(json.dumps(dict(coverage_counts=counts,open_carried=11,new_findings=3,
                          artifacts=["CHECK.md","CARD.md","COVERAGE.md","COVERAGE.json","NFI.json","INPUTS.json"])))


if __name__=="__main__":
    main()
