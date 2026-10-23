#!/usr/bin/env python3
"""Render the filed interpretation from completed, checked numerical artifacts."""
import json, pathlib
from data_tools import ROOT,P0,py_estimate,summary

def interval(b,unit="mm"):
    return f"{b['passing_amplitude_mm']:.3f}–{b['failing_amplitude_mm']:.3f} {unit}"
def main():
    d=json.loads((ROOT/"RESULTS.json").read_text())
    checks=json.loads((ROOT/"EVIDENCE-CHECKS.json").read_text())
    resources=json.loads((ROOT/"RUN-RESOURCES.json").read_text())
    nfi=json.loads((ROOT/"NFI.json").read_text())
    assert checks["failed"]==0
    g1=d["governing_boundaries"]["1.0"];g5=d["governing_boundaries"]["1.05"]
    cal=min(d["calibration"],key=lambda g:g["refined_10percent_SF1"]["amplitude_estimate_mm"])
    c=cal["refined_10percent_SF1"]
    lines=[
        "# MAINLINE-047 — P2 dimple tolerance with plastic faces",
        "",
        "**QUESTIONABLE / PROJECTION. No installed-hull qualification.**",
        "",
        f"At the held 028b point, the 255 and 300 MPa face-yield cases have **no admissible amplitude, including a perfect sphere**, under the requested pressure/first-yield screen. With the assumed 345 MPa law, the governing tested amplitude boundary is **{interval(g1)} at SF 1** and **{interval(g5)} at SF 1.05**. The passing value is the lower end of each interval; the upper end fails the first-yield screen. These are numerical brackets on the tested Gaussian branch, not physical uncertainty bounds.",
        "",
        f"The corresponding single-dimple RMS estimates about the prescribed sphere are **{1000*g1['rms_estimate_mm']:.2f} µm** and **{1000*g5['rms_estimate_mm']:.2f} µm**. This small global RMS is a consequence of one localized defect occupying little sphere area. It is not a generic RMS fabrication specification.",
        "",
        "## Criterion and point held",
        "",
        f"The calculation requires `min(P_endpoint, P_first_yield) ≥ SF × {P0:.8f} kPa`; SF 1.05 therefore requires {P0*1.05:.8f} kPa. Endpoint means the last converged monotonic static pressure. No arc-length collapse load or measured failure pressure was obtained.",
        "",
        "The main point has R_outer = 10 m, two 0.794624066985892 mm faces and a 23.23721790601544 mm core. Faces use E = 290 GPa and nu = 0.0768, with ideal finite-strain J2 plasticity at 255/300/345 MPa. Core radial modulus is 103.421 MPa; L/W transverse shear moduli are 103.421/46.884 MPa. Both face integration-point fields are checked. The 037b cure/scarf fix is carried as a 200 °F cure and 30.3414:1 scarf; seams and residual-stress stiffness are not resolved.",
        "",
        "The 255/300/345 MPa values are assumed compression sensitivities. The 036 source audit found no matched finished-sheet compressive minimum; the 345 MPa SR-200 maker value is tensile. The scalar isotropic law and using an offset yield as a sharp onset are projections. The thicker-sheet nu basis is [NASA CR-194164, Table 2](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf).",
        "",
        "## Perfect-sphere limit",
        "",
        "| Assumed yield (MPa) | First-yield native bracket, W (kPa) | Estimate (kPa) | Numerical endpoint, W (kPa) | SF 1 result |",
        "|---:|---:|---:|---:|---|",
    ]
    for y in [255,300,345]:
        r=next(r for r in d["perfect_cases"][str(y)] if r["meridian"]=="W")
        b=r["first_yield_bracket_kPa"]
        lines.append(f"| {y} | {b[0]:.5f}–{b[1]:.5f} | {py_estimate(r):.5f} | {r['endpoint_kPa']:.5f} | {'Fails even at a=0' if y<345 else 'Passes this model screen'} |")
    lines += [
        "",
        "The 300 MPa case is a small but explicit failure at the held geometry. Its entire first-yield bracket and numerical endpoint are below service pressure. No positive tolerance is assigned to either lower-strength case.",
        "",
        "## Amplitude boundaries for the 345 MPa case",
        "",
        "| Gaussian width (mm) | Meridian | SF 1 pass–fail (mm) | One-dimple RMS estimate (µm) | SF 1.05 pass–fail (mm) | RMS estimate (µm) |",
        "|---:|:---:|---:|---:|---:|---:|",
    ]
    for group in d["refined_boundaries"]:
        b1=next(b for b in group["boundaries"] if b["SF"]==1)
        b5=next(b for b in group["boundaries"] if b["SF"]==1.05)
        lines.append(f"| {group['width_mm']:.3f} | {group['meridian']} | {interval(b1,'')} | {1000*b1['rms_estimate_mm']:.2f} | {interval(b5,'')} | {1000*b5['rms_estimate_mm']:.2f} |")
    lines += [
        "",
        "The 332 and 402 mm widths retain 029's two footprints. The current classical length is 347 mm, approximately the inverse buckling wavenumber; the full classical wavelength is 2181 mm and is checked separately as a broad Gaussian. The latter is not silently substituted for the narrow defect width. The result is limited to these tested footprints and meridian surrogates.",
        "",
        "First yield generally precedes the numerical endpoint. The no-yield boundary uses a high-yield numerical control to evaluate the identical pre-yield constitutive branch at the exact target pressures. The control's 10,000 MPa threshold is not a proposed material strength. Actual 345 MPa runs confirm yield-free passing edges and plastic failing edges at the governing boundaries.",
        "",
        f"A geometric check helps explain the scale: the governing SF 1 dimple changes the initial pole curvature by about {100*(1-d['geometric_sanity']['curvature_ratio_to_sphere']):.1f}%. At that width the pole becomes locally concave above {d['geometric_sanity']['amplitude_at_zero_pole_curvature_mm']:.2f} mm. A small amplitude relative to the 10 m radius can therefore be a substantial local curvature error. This check explains the geometry; it is not an independent strength prediction.",
        "",
        f"The main amplitude sweeps' endpoints and first-yield brackets are in [SWEEP.csv]({ROOT/'SWEEP.csv'}). [ALL-NATIVE-RUNS.csv]({ROOT/'ALL-NATIVE-RUNS.csv'}) additionally lists every auxiliary calculation, identifying load caps, yield not reached, and excluded controls. [Pressure sweep figure]({ROOT/'PRESSURE-SWEEP.pdf'}) and [tolerance figure]({ROOT/'TOLERANCE.pdf'}) show the distinction. Extrapolations outside native PEEQ brackets are rejected and listed in RESULTS.json.",
        "",
        "## What the inherited benchmark gap does",
        "",
        f"If the new model's endpoint is divided by **1.10**, while first-yield pressure is left unchanged, the smallest SF 1 boundary estimate is **{interval(c)}** at width {cal['width_mm']:.3f} mm/{cal['meridian']} ({1000*c['rms_estimate_mm']:.2f} µm one-dimple RMS). At SF 1.05 the perfect sphere already fails that scenario. Transferring the larger **2.3146–2.4589×** imperfect-endpoint bias leaves no admissible amplitude even at SF 1.",
        "",
        "CALIBRATION.json retains the unadjusted reading, the exact 029 linear factors 1.095667 and 1.097609, the rounded 1.10 scenario, and both imperfect factors. These reductions are conditional endpoint-transfer calculations, not calibrated predictions. Applying an elastic predecessor's error to a model that now includes plasticity may double-count part of the omitted-material effect.",
        "",
        "The source benchmark is a small clamped steel/PVC hemisphere with nonlinear foam, a contact-generated defect and an arc-length solution. Its geometry and mechanisms differ substantially from this low-Vc Be/CR-III sphere. See the [EUCASS paper](https://www.eucass.eu/doi/EUCASS2023-367.pdf), the pinned 029 record, and NFI row 047-05.",
    ]
    if "thermal_strength_debit" in d:
        lines += ["","## 037b cure correction","",
            "A separate local strength-debit sensitivity subtracts 3.41022257 MPa from the 345 MPa screen. It accounts conservatively for the stated residual stress magnitude through the von Mises norm inequality, but does not solve thermal deformation or geometric stiffness. It is evaluated at the nominal governing width/meridian, not presented as a new global optimization."]
        for group in d["thermal_strength_debit"]["groups"]:
            for b in group["boundaries"]:
                lines.append(f"- At SF {b['SF']:g}, width {group['width_mm']:.3f} mm/{group['meridian']}: pass–fail {interval(b)}; single-dimple RMS estimate {1000*b['rms_estimate_mm']:.2f} µm.")
        lines += ["",
            "037b's small re-optimization has tf = 0.7946220286 mm and tc = 23.2319086293 mm. The exact-geometry control is retained beside the held-point control in RESULTS.json; the main campaign does not silently switch geometries."]
    lines += [
        "",
        "## Comparison with 015b and 042",
        "",
        f"042 mapped the present P2 point to roughly 9.32–16.06 mm at a footprint near 0.36 m. The new governing SF 1 estimate is {g1['amplitude_estimate_mm']:.3f} mm, about {9.32/g1['amplitude_estimate_mm']:.1f}–{16.06/g1['amplitude_estimate_mm']:.1f} times smaller. This comparison adds a first-yield restriction and changes the numerical model; it is not an isolated calibration of the old knockdown formula.",
        "",
        "The older 021/021b map amplitudes were about 11.8 and 45.8 mm. 015b corrected their paired single-Gaussian RMS values to about 0.1393 and 0.6544 mm. Pairing the amplitude from one footprint with the width from another is not repeated here.",
        "",
        "Relevant 042 precedents remain different measurements:",
        "",
        "- Rohr's gores departed contour about 1.27 mm after trimming and 3.81–5.08 mm after chemical milling; hand forming followed. Those deviations are comparable to or larger than the narrow-defect limits, but they are not measured Gaussian defects on this hull. [Primary report, PDF p.25](https://ntrs.nasa.gov/api/citations/19660014454/downloads/19660014454.pdf).",
        "- The all-Be honeycomb panel report gives 0.0762 mm conformity to a cylindrical die after forming. That is encouraging at panel scale; it does not establish the shape of an assembled 20 m sphere. [Primary report, PDF p.86](https://ntrs.nasa.gov/api/citations/19730016169/downloads/19730016169.pdf).",
        "- S-II's 0.254 mm figure is a core-to-face fit limit, not whole-shell peak/RMS accuracy. 042's 0.15 mm reflector-class peak is a three-sigma projection from RMS data. Treating either as the present hull's measured dimple spectrum would be unjustified.",
        "",
        "For one Gaussian, RMS is approximately `a w / (sqrt(8) R)`; the filed results use the exact spherical-area integral. Multiple defects, a fitted sphere, reflector panel RMS, local waviness and core-to-face gaps need separate spatial definitions. A global RMS number alone cannot enforce this local amplitude bound.",
        "",
        "## Numerical controls and unresolved work",
        "",
        f"{d['native_run_count']} native solver records are retained, including {len(d['excluded_runs'])} excluded initial eigen controls. The failed controls returned SIGSEGV and supplied no factor; their pure-elastic replacements are separate records. Static one/four-core runs agree; eigen runs use one core. All heavy runs use simjob and own jobs execute serially.",
        "",
        "Mesh controls vary angular resolution, pole grading, face layers and core layers. The constitutive controls compare the native plastic law's pre-yield response against StVK, a core in-plane regularization change, and a small hardening slope. Nu = 0.03 and 0.33 are tested at 0, 1 and 11.8 mm in both meridians with the 345 MPa law. Full tables and actual differences are in RESULTS.json; mesh brackets are not substituted for physical uncertainty.",
        "",
        "At the target-load control (a = 1 mm, w = 347.153 mm), doubling the angular resolution from 512 to 1024 with two face layers changes the service-pressure maximum stress by 0.031 MPa; increasing to four face layers changes it by 0.139 MPa. The exact 037b re-optimized geometry changes it by 0.019 MPa. The adopted boundary mesh uses 512 angular elements, two elements through each face, six through the core, and pole grading 2.",
        "",
        f"The five-increment target ramp agrees with the 21-increment reference within {max(abs(p['difference_MPa']) for p in d['target_ramp_control']['points']):.5f} MPa. Completed longer ramps are preserved, and each model records its own time-to-pressure mapping. Actual-yield confirmations use separate linear ramps.",
        "",
        "Conditional endpoint-bias boundaries use 256 angular elements and one layer per face. At the governing passing point, the following controls measure sensitivity; their pressure differences are not an amplitude error bound:",
        "",
        "| Endpoint control | Reference (kPa) | Checked (kPa) | Change |",
        "|---|---:|---:|---:|",
    ]
    for ccheck in d["boundary_checks"]:
        if ccheck["kind"].startswith("endpoint_"):
            lines.append(f"| {ccheck['kind']} | {ccheck['reference_endpoint_kPa']:.5f} | {ccheck['endpoint_kPa']:.5f} | {100*ccheck['relative_difference']:+.4f}% |")
    lines += [
        "",
        "At a = 1 mm and w = 347.153 mm, the comparable 128-element angular meshes give:",
        "",
        "| nu | Meridian | First-yield native bracket (kPa) | Numerical endpoint (kPa) |",
        "|---:|:---:|---:|---:|",
    ]
    nu_rows=[summary("p128-a1-W-y345"),summary("p128-a1-L-y345")]
    nu_rows += [r for r in d["sensitivities"] if r["amplitude_mm"]==1]
    for r in sorted(nu_rows,key=lambda r:(r["nu"],r["meridian"])):
        b=r["first_yield_bracket_kPa"]
        lines.append(f"| {r['nu']:.4f} | {r['meridian']} | {b[0]:.3f}–{b[1]:.3f} | {r['endpoint_kPa']:.3f} |")
    lines += [
        "",
        "The inherited minimum step request of 1e-7 is raised by CalculiX to 1e-6 of the ramp, as recorded in NATIVE-WARNINGS.json. Load-control endpoints and coarse first-yield estimates are qualified accordingly. The plastic-law setup and output convention are documented in [METHOD.md]("+str(ROOT/"METHOD.md")+") and the [CalculiX manual](https://www.dhondt.de/ccx_2.21.pdf).",
        "",
        f"{sum('too many cutbacks' in s['reason'] for s in d['numerical_endpoint_stops'])} paths stop at the consecutive-cutback limit after observed first yield. All numerical stop diagnostics, including minimum-increment stops, remain in NUMERICAL-ENDPOINT-STOPS.json. Retaining their converged histories does not make them successful collapse solutions.",
        "",
        f"{checks['passed']} custody, numerical and arithmetic checks pass; this does not validate the physical hull. Native solver elapsed time sums to {resources['summed_native_elapsed_s']:.1f} s, with measured CPU time {resources['measured_CPU_seconds']:.1f} s and peak native RSS {resources['peak_solver_RSS_kB']/1024:.1f} MiB. Wall-clock start/end measurements are in RUN.json.",
        "",
        f"[NFI.json]({ROOT/'NFI.json'}) records {len(nfi['rows'])} issues, including finished-sheet compression, orthotropy, core/bond behavior, continuation versus nonconvergence, thermal prestress, three-dimensional geometry, shape metrics and benchmark transfer. Installed-hull SF remains unknown.",
        "",
        "The assigned work is complete. The brief names no successor; stop and file.",
    ]
    (ROOT/"CARD.md").write_text("\n".join(lines)+"\n")
    body=f"""MAINLINE-047 filed, QUESTIONABLE/PROJECTION.

The held 028b point has no admissible dimple amplitude under the 255 or 300 MPa first-yield cases: even the perfect sphere fails 95.46084 kPa.

With assumed 345 MPa faces and nu=.0768, the governing tested pass–fail brackets are {interval(g1)} at SF1 and {interval(g5)} at SF1.05. Single-Gaussian RMS estimates are {1000*g1['rms_estimate_mm']:.2f}/{1000*g5['rms_estimate_mm']:.2f} micrometres. Both meridians, three narrow footprints and the full classical-wavelength footprint are covered. Native histories separate first yield from the numerical endpoint.

If endpoints are 10% high, division by 1.10 gives {interval(c)} at SF1; SF1.05 then fails even at zero amplitude. Transferring the 2.31–2.46x imperfect benchmark gap permits none. These transfers are not calibrations of the new plastic model.

Cure strength-debit, Poisson-ratio, mesh, constitutive and exact-037b-geometry sensitivities are filed. 015b/042 comparisons keep peak, RMS and fit-gap metrics separate. {len(d['excluded_runs'])} crashed initial eigen controls are preserved and excluded; separate elastic replacements are checked. {d['native_run_count']} native records, {checks['passed']} checks and {len(nfi['rows'])} NFI rows are retained.

No installed-hull qualification. No successor named; stop and file."""
    assert len(body.split())<=250,len(body.split())
    (ROOT/"REPORT-BODY.txt").write_text(body+"\n")
    print(json.dumps(dict(body_words=len(body.split()),card_bytes=(ROOT/"CARD.md").stat().st_size)))
if __name__=="__main__":main()
