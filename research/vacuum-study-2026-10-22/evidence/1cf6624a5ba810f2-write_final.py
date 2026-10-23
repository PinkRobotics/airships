#!/usr/bin/env python3
"""Render final three-limit interpretation; retain the earlier campaign as an appendix."""
import json
from data_tools import ROOT,P0,py_estimate
from write_card import main as write_earlier,interval
def main():
    write_earlier()
    earlier=(ROOT/"CARD.md").read_text()
    earlier=earlier.replace(str(ROOT/"TOLERANCE.pdf"),str(ROOT/"FACE-ONLY-TOLERANCE.pdf"))
    (ROOT/"FACE-ONLY-CARD.md").write_text(
        "# Historical face-only campaign — superseded for acceptance\n\n"
        "This appendix preserves the E-in-plane = 0.01 MPa campaign and its sensitivities. "
        "Its amplitude boundaries omit core shear and do not establish admissibility of that core law. "
        "Use CARD.md and CORE-RESULTS.json for the final CHECK-029 fold. "
        "Run totals below include the full combined record.\n\n"+earlier)
    all_data=json.loads((ROOT/"RESULTS.json").read_text());d=all_data["core_fold"]
    checks=json.loads((ROOT/"EVIDENCE-CHECKS.json").read_text())
    resources=json.loads((ROOT/"RUN-RESOURCES.json").read_text())
    nfi=json.loads((ROOT/"NFI.json").read_text())
    assert checks["failed"]==0
    b1,b5=(d["governing_boundaries"][x] for x in ["1.0","1.05"])
    cal=d["calibration"]["global_bracket"]
    cint=f"{cal['passing']['amplitude_mm']:.3f}–{cal['failing']['amplitude_mm']:.3f} mm"
    rows=[
        "# MAINLINE-047 — P2 dimple tolerance including face yield and core shear",
        "",
        "**QUESTIONABLE / PROJECTION. The stated core regularization is not a qualified material law.**",
        "",
        f"At the held 028b geometry, the assumed **255 and 300 MPa face-yield cases fail even with zero dimple**. "
        f"With 345 MPa faces and the explicit regularized core below, the governing tested pass–fail bracket is "
        f"**{interval(b1)} at SF 1** and **{interval(b5)} at SF 1.05**. "
        "Face yield governs these small-dimple boundaries; core shear has now been checked. "
        "The lower amplitude passes the model screen and the upper amplitude fails. "
        "These are numerical brackets for the tested Gaussian family, not physical uncertainty or fabrication allowables.",
        "",
        f"The corresponding one-Gaussian RMS estimates about the prescribed sphere are "
        f"**{1000*b1['rms_estimate_mm']:.2f}/{1000*b5['rms_estimate_mm']:.2f} micrometres**. "
        "A small full-sphere RMS does not limit other defects or a different spatial spectrum.",
        "",
        "## Criterion, geometry and core law",
        "",
        f"`min(P_endpoint, P_first_face_yield, P_first_core_shear) >= SF × {P0:.8f} kPa`. "
        f"The SF 1.05 target is {P0*1.05:.8f} kPa. Endpoint means the last converged static pressure, "
        "not an experimentally validated collapse pressure. The high-yield target controls follow the identical pre-yield branch; "
        "their 10,000 MPa numerical threshold is not a material strength. Actual 345 MPa native runs confirm the governing pass/fail edges.",
        "",
        "R_outer = 10,000 mm; each Be face = 0.794624066985892 mm; core = 23.23721790601544 mm. "
        "The 037b 200 °F cure / 30.3414:1 scarf correction is retained. Faces use E = 290 GPa, nu = 0.0768, "
        "finite-strain isotropic J2 perfect plasticity. The full-sphere CAX8 model uses a stress-free Gaussian inward radial offset "
        "of every layer, shared-node bonds and the minimum axisymmetric restraints.",
        "",
        "**Final conditional core law:** orthotropic StVK, E_normal = 103.4213594 MPa, transverse G_L/G_W = "
        "103.4213594/46.8843496 MPa, **E_in-plane = 1 MPa and G_in-plane = 0.5 MPa**, zero Poisson coupling. "
        "W/L cases interchange meridian and hoop directions. In-plane properties are an explicit regularization sensitivity. "
        "No post-failure core plasticity or damage redistribution is credited.",
        "",
        "**The inherited E_in-plane = 0.01 MPa law is not accepted for the final tolerance.** "
        "CHECK-029 demonstrated loss of ellipticity in that law near 0.088 MPa transverse shear and refined-mesh instability on "
        "its 021/021b dimples. It found its 1 MPa sensitivity stable. The present result explicitly uses that stronger regularization; "
        "changing an unsourced modulus does not establish the real honeycomb response. "
        f"[CHECK-029 evidence]({ROOT/'inputs/rpt-check029-opus-1020/CHECK.md'}) is pinned; no checker code was read or run.",
        "",
        "Core strengths are from [Hexcel CR III Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf), "
        "5056, 3/8-inch cell, 1.0 pcf: W/L **25/45 psi minimum average** and **35/55 psi typical** "
        "(0.172369/0.310264 MPa and 0.241317/0.379212 MPa). Both readings are evaluated. "
        "These are product-type catalog tests at 0.625-inch core thickness, not installed-hull allowables. "
        "The two current transverse shear tractions use a stated quadratic interaction; the native circumferential component is retained.",
        "",
        "The initial campaign stored only face stresses and pole displacements, so its fields could not support a core post-check. "
        "New native runs save core strain and stress. Current material-frame shear is reconstructed from the full Green-strain tensor "
        "and the stated StVK law, then checked by rotation-invariant Cauchy stress quantities.",
        "",
        f"The maximum reconstructed/native stress-invariant difference is {d['maximum_native_invariant_error_MPa']:.3g} MPa. "
        f"At every saved point/increment on the passing boundary paths, a sufficient local acoustic lower bound remains positive "
        f"(minimum {d['minimum_passing_acoustic_bound_MPa']:.6f} MPa). "
        "This checks local strong ellipticity of the chosen law at those states; it does not prove global or nonaxisymmetric stability. "
        f"Maximum core compression on these passing paths is {d['maximum_passing_core_compression_MPa']:.6f} MPa, "
        "below the catalog 35-psi typical crush strength. The derivation and limitations are in METHOD.md.",
        "",
        "The 345 MPa maker value is tensile; 036 found no matched finished-sheet biaxial compressive minimum. "
        "All three yield values are assumptions, and an offset yield is idealized as a sharp plastic onset. "
        "The thicker-sheet nu value in [NASA CR-194164 Table 2](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf) "
        "does not establish thin-gauge isotropy.",
        "",
        "## Perfect sphere with the stated regularized core",
        "",
        "| Face yield (MPa) | W first-yield bracket (kPa) | W endpoint (kPa) | SF 1 |",
        "|---:|---:|---:|---|",
    ]
    for y in [255,300,345]:
        s=d["perfect_cases"][f"{y}-W"];br=s["first_yield_bracket_kPa"]
        rows.append(f"| {y} | {br[0]:.5f}–{br[1]:.5f} | {s['endpoint_kPa']:.5f} | {'Fails even at zero amplitude' if y<345 else 'Passes model screen'} |")
    rows += ["","The L-perfect runs are also retained. Neither lower-strength case receives a tolerance interval containing zero.",
        "","## Tested 345 MPa boundaries","",
        "| Gaussian width (mm) | Meridian | SF 1 pass–fail (mm) | SF 1.05 pass–fail (mm) | SF 1 passing core shear (MPa) | Minimum-average shear index |",
        "|---:|:---:|---:|---:|---:|---:|"]
    for g in d["regularized_boundaries"]:
        p=next(b for b in g["boundaries"] if b["SF"]==1 and b["strength_basis"]=="minimum_average")
        q=next(b for b in g["boundaries"] if b["SF"]==1.05 and b["strength_basis"]=="minimum_average")
        rows.append(f"| {g['width_mm']:.3f} | {g['meridian']} | {interval(p,'')} | {interval(q,'')} | {p['passing_core_shear_MPa']:.6f} | {p['passing_core_index']:.4f} |")
    rows += ["",
        "All eight footprint/orientation cases use exact native target pressures. Minimum-average and typical shear readings "
        "are separately retained in CORE-BOUNDARIES.json. The three narrow widths are 029's two footprints and the current classical "
        "length, approximately inverse buckling wavenumber. A 2181 mm full classical wavelength is an additional broad Gaussian; "
        "it is not substituted for the 332–402 mm defect family.",
        "",
        f"[Tolerance figure]({ROOT/'TOLERANCE.pdf'}); [regularized core sweep]({ROOT/'CORE-PRESSURE-SWEEP.pdf'}); "
        f"[native three-limit sweep table]({ROOT/'CORE-SWEEP.csv'}). The sweep records face-yield brackets, first core-shear "
        "crossings and numerical endpoints separately. A missing core crossing means strength was not reached before the numerical stop.",
        "",
        "## Larger dimples: the endpoint is not capacity",
        "",
        "| Width / meridian | Amplitude (mm) | First face yield estimate (kPa) | First minimum-average core shear (kPa) | Numerical endpoint (kPa) |",
        "|---|---:|---:|---:|---:|"]
    for s in d["sweep"]:
        if s["meridian"]=="W" and s["label"] in ["old021","old021b","fullwave"] and s["amplitude_mm"]>1:
            cs=s["first_core_shear"]["minimum_average"].get("estimate_kPa")
            ctext=f"{cs:.3f}" if cs is not None else "not reached"
            rows.append(f"| {s['width_mm']:.1f} mm / W | {s['amplitude_mm']:.1f} | {s['first_face_yield_estimate_kPa']:.3f} | {ctext} | {s['endpoint_kPa']:.3f} |")
    rows += ["","Crossing estimates interpolate within saved pressure brackets. Numerical paths beyond first material failure remain diagnostics only.",
        "","## Conditional benchmark transfer","",
        f"If endpoint predictions are **10% high**, dividing by **1.10** gives a common SF 1 amplitude bracket "
        f"**{cint}**, limited here by {cal['width_mm']:.3f} mm/{cal['meridian']}. "
        "Every footprint/orientation is explicitly checked at the common passing amplitude; at least one fails at the upper edge. "
        "First face yield and first core shear are included in that minimum. SF 1.05 fails the 1.10 scenario even for the perfect sphere. "
        "Applying the 2.3146–2.4589 imperfect-endpoint factors likewise leaves no admissible amplitude even at SF 1.",
        "",
        "This is not an empirical calibration of the Be hull. CHECK-029 demonstrates that the predecessor nonlinear gap arose "
        "from StVK foam collapse and core discretization; its linear radius/material explanation remains unestablished. "
        "The [EUCASS benchmark](https://www.eucass.eu/doi/EUCASS2023-367.pdf) is a different steel/PVC hemisphere with different "
        "constitutive and imperfection definitions. The original eight-width calibration calculations and exact linear factors remain "
        "in the explicitly historical face-only appendix.",
        "",
        "## Cure debit and manufacturing comparison",
        "",
        "The 037b 3.41022257 MPa residual face-compression magnitude is treated as a separate conservative local strength debit "
        "to 341.58977743 MPa. This does not simulate thermal shape or prestress stiffness, and rechecks the nominal governing footprint rather than optimizing all widths."]
    rows.append("")
    for b in d["thermal_debit"]["boundaries"]:
        if b["strength_basis"]=="minimum_average":
            rows.append(f"- SF {b['SF']:g}: pass–fail {interval(b)}; one-Gaussian RMS estimate {1000*b['rms_estimate_mm']:.2f} micrometres.")
    rows += ["",
        f"042 mapped the present point to about 9.32–16.06 mm near a 0.36 m footprint. The present SF 1 estimate "
        f"({b1['amplitude_estimate_mm']:.3f} mm) is {9.32/b1['amplitude_estimate_mm']:.1f}–{16.06/b1['amplitude_estimate_mm']:.1f} "
        "times smaller. This combines a different numerical model and material restrictions; it is not an isolated correction of the old knockdown formula.",
        "",
        "015b's old 11.8/45.8 mm amplitudes pair with about 0.1393/0.6544 mm single-Gaussian RMS. "
        "The exact spherical integral is used here; the small-patch expression is `a*w/(sqrt(8)*R)`. "
        "Do not interchange full-sphere RMS, reflector RMS, local fit gap or contour peak.",
        "",
        "- Rohr contour errors were about 1.27 mm after trimming and 3.81–5.08 mm after chemical milling, followed by hand forming. "
        "[Primary report, PDF p.25](https://ntrs.nasa.gov/api/citations/19660014454/downloads/19660014454.pdf).",
        "- An all-Be honeycomb panel conformed to a cylindrical die within 0.0762 mm; that does not establish assembled 20 m sphere accuracy. "
        "[Primary report, PDF p.86](https://ntrs.nasa.gov/api/citations/19730016169/downloads/19730016169.pdf).",
        "- S-II's 0.254 mm is a core-to-face fit limit. 042's 0.15 mm reflector-class peak is a three-sigma projection. Neither is a measured hull dimple spectrum.",
        "",
        "## Controls and remaining limits",
        "",
        "The boundary mesh has 512 angular elements, two through each face, six through the core and grading 2. "
        "Own angular/layer controls measure the following changes at the governing passing amplitude:",
        "",
        "| Control | Face-stress change (MPa) | Core-shear change (MPa) |",
        "|---|---:|---:|"]
    for c in d["controls"]:
        if c["kind"].startswith("control_"):
            rows.append(f"| {c['kind']} | {c['face_difference_MPa']:+.6f} | {c['core_shear_difference_MPa']:+.6f} |")
    probe=d["inherited_core_acoustic_probe"]
    if probe and probe["minimum_sampled_acoustic_eigenvalue_MPa"]<0:
        rows += ["",f"An own inherited-law control at the governing passing amplitude finds a negative rank-one acoustic "
                 f"second variation ({probe['minimum_sampled_acoustic_eigenvalue_MPa']:.6g} MPa) at its peak-shear core point. "
                 "That is a local loss-of-ellipticity witness for this native state, independent of the positive-bound check "
                 "on the regularized law. CORE-RESULTS.json retains the strain, wave direction and polarization."]
    rows += ["",
        "Actual 345 MPa native controls confirm the passing/failing edges at both safety factors. "
        "The original nu = 0.03/0.33, hardening, exact 037b geometry, extensive mesh, thread and elastic-eigen sensitivities "
        "remain in FACE-ONLY-CARD.md and RESULTS.json with their inherited 0.01 MPa core scope; "
        "they are not relabeled as a complete requalification of the 1 MPa regularization.",
        "",
        f"{all_data['native_run_count']} native solver records and {checks['passed']} checks are retained, including "
        f"{d['core_run_count']} core-output records. Native elapsed time sums to {resources['summed_native_elapsed_s']:.1f} s; "
        f"measured CPU time is {resources['measured_CPU_seconds']:.1f} s and peak native RSS is "
        f"{resources['peak_solver_RSS_kB']/1024:.1f} MiB. Heavy jobs use simjob and execute serially. "
        "Refused admissions are preserved and retried unchanged at least 60 seconds apart under the standing order.",
        "",
        "The two initial eigen SIGSEGV controls are excluded, with separate successful elastic replacements. "
        "All numerical stop and minimum-step diagnostics remain visible; a native nonconvergence endpoint is not proof of collapse. "
        f"[METHOD.md]({ROOT/'METHOD.md'}), [ALL-NATIVE-RUNS.csv]({ROOT/'ALL-NATIVE-RUNS.csv'}) and the artifact manifest identify the evidence.",
        "",
        f"[NFI.json]({ROOT/'NFI.json'}) records {len(nfi['rows'])} issues. Missing compression allowables, measured in-plane core properties, "
        "a qualified core/bond law, actual defect spectrum, thermal prestress and 3D stability keep installed-hull SF unknown. "
        "The assigned card is complete as a conditional numerical projection; no successor is named. Stop and file.",
    ]
    (ROOT/"CARD.md").write_text("\n".join(rows)+"\n")
    body=f"""MAINLINE-047 filed with CHECK-029 folded in. QUESTIONABLE/PROJECTION.

The criterion is min(endpoint, first face yield, first core shear). The 255/300 MPa cases fail even at zero dimple. With assumed 345 MPa faces, the governing tested pass–fail brackets are {interval(b1)} at SF1 and {interval(b5)} at SF1.05; single-Gaussian RMS estimates {1000*b1['rms_estimate_mm']:.2f}/{1000*b5['rms_estimate_mm']:.2f} micrometres.

These results explicitly use orthotropic StVK core E_in=1 MPa, G_in=.5 MPa, inherited radial/transverse moduli, and catalog minimum-average/typical shear strengths. The inherited .01-MPa core is not accepted after CHECK-029's ellipticity finding. The stronger regularization is unsourced: no actual-hull tolerance is qualified.

New native core stress/strain fields check current-frame shear and local ellipticity on passing paths. Face yield governs the small-dimple limits; larger dimples encounter material limits before numerical endpoints. Both meridians and all four footprints are covered.

Conditional endpoint division by 1.10 gives a common SF1 bracket {cint}; SF1.05 then fails even at zero. Transferring 2.31–2.46x permits none. CHECK-029 identifies a foam-law artifact behind that larger gap, so these are rejection scenarios, not empirical calibration.

Cure debit, controls, 015b/042 comparisons and inherited-law sensitivities are retained. {all_data['native_run_count']} native records, {checks['passed']} checks, {len(nfi['rows'])} NFIs. Retry and keep-turn-open orders observed. No successor; stop and file."""
    assert len(body.split())<=250,len(body.split())
    (ROOT/"REPORT-BODY.txt").write_text(body+"\n")
    print(json.dumps(dict(body_words=len(body.split()),card_bytes=(ROOT/"CARD.md").stat().st_size)))
if __name__=="__main__":main()
