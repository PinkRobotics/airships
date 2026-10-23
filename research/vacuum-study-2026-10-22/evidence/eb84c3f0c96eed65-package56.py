"""Build reviewable input metadata and the result card from completed raw runs."""
import datetime
import hashlib
import json
from pathlib import Path

from material56 import baseline_tables

ROOT=Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def pin(path):
    blob=path.read_bytes()
    return {"path":str(path),"sha256":hashlib.sha256(blob).hexdigest(),"bytes":len(blob)}


def build():
    results=read(ROOT/"RESULTS.json")
    assert results["work_complete"], "Only package after the simulations finish."
    cases={r["name"]:r for r in results["pressure_cases"]}
    foam,steel,foam_total,steel_total=baseline_tables()
    inputs={
        "unit":results["unit"],"tag":"QUESTIONABLE / PROJECTION","certification":"none",
        "custody":read(ROOT/"INPUT-CUSTODY.json"),
        "honeycomb_access":read(ROOT/"sources/HONEYCOMB-ACCESS.json"),
        "source_custody_audit":pin(ROOT/"CUSTODY-AUDIT.json"),
        "material_curve_scope":"Rounded visual digitization and explicit constitutive assumptions; no pressure fitting.",
        "foam_elastic":{"E_MPa":40.,"nu":0.,"tag":"QUESTIONABLE","source":"EUCASS2023-367 Table 1"},
        "steel_elastic":{"E_MPa":210000.,"nu":.33,"tag":"QUESTIONABLE","source":"EUCASS2023-367 Table 1"},
        "foam_yield":{
            "form":"sqrt((q^2+alpha^2*p^2)/(1+alpha^2/9))-Y(kappa)",
            "flow":"associated; dkappa=dlambda","base_alpha":3/2**.5,
            "tag":"PROJECTION for hydrostatic ratio and associated flow",
            "source":"https://abaqus.uclouvain.be/English/SIMACAEMATRefMap/simamat-c-crushfoam.htm"},
        "foam_total_log_strain_Cauchy_MPa":foam_total.tolist(),
        "foam_plastic_strain_strength_MPa":foam.tolist(),
        "steel_total_log_strain_Cauchy_MPa":steel_total.tolist(),
        "steel_plastic_strain_strength_MPa":steel.tolist(),
        "curve_conversion":"plastic_log_strain=total_log_strain-Cauchy_stress/E",
        "foam_extrapolation":"Beyond last plastic knot, continue the last dY/dkappa; flagged at every step.",
        "steel_curve_tag":"PROJECTION: Figure 5 stress labels divided by ten; literal-axis x10 scenario separate.",
        "geometry":{"faces_mm":[.42,.42],"core_mm":3.1,
                    "radius_readings":{"outer_mm":42.8,"midsurface_mm":42.8},
                    "Gaussian_amplitude_mm":2.955,"Gaussian_width":"0.1*outer_radius",
                    "indentation_radius_mm":4.28,"indentation_target_depth_mm":2.955,
                    "indentation_state_import":"Reset stress, plastic strain and hardening; conditional."},
        "per_case_parameters":{n:{"model":r["parameters"],"plastic_step_cap":r.get("plastic_step_cap"),
                                  "elastic_step_cap_mm":r.get("elastic_step_cap_mm"),
                                  "maximum_step_mm":r["maximum_step_mm"],
                                  "tolerance":r["tolerance"]}
                               for n,r in cases.items()},
        "code":[pin(p) for p in sorted(ROOT.glob("*.py"))]+[pin(ROOT/"reuse/axi029.py")],
        "executed_source_snapshots":[pin(p) for p in sorted((ROOT/"logs").glob("*/SOURCE-PINS.json"))],
        "sources":[pin(p) for p in sorted((ROOT/"sources").iterdir()) if p.is_file()],
        "reproduction":"Use each logs/<job>/RECEIPTS.json argv and its logs/<job>/source snapshot. Heavy runs require simjob; use fresh output names.",
        "unused_source":"lsdyna-theory-r16.pdf was acquired but is not relied on for a constitutive equation.",
    }
    (ROOT/"INPUTS.json").write_text(json.dumps(inputs,indent=2)+"\n")

    def pressure(name):
        return cases[name]["peak"]["pressure_MPa"]

    def local(name):
        return cases[name]["first_sampled_limit_point"]["sample"]["pressure_MPa"]

    def bracket(name,key):
        a,b=cases[name]["first_screen_brackets_MPa"][key]
        return f"{a:.4f}–{b:.4f}"

    mid="indent-mid192p30k-pressure"
    outer="indent-outer96p30k-pressure"
    tight="guarded192c8-tight"
    p_mid=pressure(mid)
    primary=[mid,"indent-mid96p30k-pressure","indent-mid96p60k-pressure",outer]
    pmin=min(pressure(n) for n in primary)
    pmax=max(pressure(n) for n in primary)
    comparison_rows="\n".join(
        f"| {r['comparison']} | {r['first_peak_MPa']:.6f} → {r['second_peak_MPa']:.6f} | {r['relative_change_percent']:+.4f}% |"
        for r in results["mesh_step_contact_comparisons"])
    event_rows="\n".join(
        f"| {label} | {bracket(tight,key)} | {bracket(mid,key)} |"
        for label,key in [
            ("Combined-stress foam yield","core_yield"),
            ("First face yield","face_yield"),
            ("First use of extrapolated foam hardening","foam_extrapolation"),
            ("Implied initial pure-shear-strength screen","core_shear_screen")])
    peak_rows="\n".join(
        f"| {name} | {cases[name]['parameters']['ntheta']} / {cases[name]['parameters']['ncore']} / {cases[name]['parameters']['nface']} | {local(name):.6f} | {pressure(name):.6f} | {cases[name]['gap_to_paper_percent']:+.3f}% |"
        for name in ["base96c4","base192c4","base192c8","base192c12","base384c8",
                     "guarded96c4",tight,"mid96c4-guarded",outer,
                     "indent-mid96p30k-pressure",mid,"indent-mid96p60k-pressure"])
    sensitivity_rows="\n".join(
        f"| {name} | {pressure(name):.6f} | {cases[name]['gap_to_paper_percent']:+.3f}% |"
        for name in ["alpha1p5-96c4-guarded","alpha3-96c4-guarded","foam090-96c4-guarded",
                     "foam110-96c4-guarded","steel-literal-96c4-guarded"])
    nfis=read(ROOT/"NFI.json")
    refs={r["radius_reading"]:r for r in results["linear_results"] if r["ntheta"]==384}
    mesh=next(r for r in results["mesh_step_contact_comparisons"] if r["comparison"]=="contact mesh refinement")
    penalty=next(r for r in results["mesh_step_contact_comparisons"] if r["comparison"]=="contact penalty refinement")
    peak=cases[mid]["peak"]
    kdf=cases[mid]["benchmark_normalized_pressure"]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    text=f"""# MAINLINE056 — conditional crushable-core benchmark

**QUESTIONABLE / PROJECTION throughout. No certification. No P2 gamma released.**

The constitutive extension reduces the inherited 13.9569 MPa elastic result toward the paper's pressure prediction. With reconstructed indentation, the midsurface-radius case gives **{p_mid:.6f} MPa ({100*(p_mid/6.03-1):+.3f}%)** against 6.03 MPa. The four indentation/radius cases with at least 96 meridional elements and contact penalty at least 30000 MPa/mm span **{pmin:.4f}–{pmax:.4f} MPa**, or **{100*(pmin/6.03-1):+.2f}% to {100*(pmax/6.03-1):+.2f}%**. The preliminary 48-element, softer-contact pilot is excluded from that range and retained in the full results. This is a conditional scenario range, not a confidence interval or a calibrated error bound.

**The 6.03 MPa target is numerical, not measured.** EUCASS2023-367 predicts pressure collapse and validates separately against axial-compression tests. The source does not establish an experimentally validated pressure-shell capacity here. The answer to “does it reproduce the measured shell?” is therefore **not established**. The simulation comparison is much closer, but unresolved material and geometric inputs prevent a unique calibration. [Primary paper](https://www.eucass.eu/doi/EUCASS2023-367.pdf).

**Implementation.** Reused CHECK029's Q8 axisymmetric mesh, kinematics, follower pressure, boundary conditions and eigenproblem, pinned as `reuse/axi029.py` (SHA-256 `4d39299f2e88bc0690d857839c13a02ecdf5367a96733a4e57f09cafc315eeda`). MAINLINE029's exact selected decks and code are also pinned. New owned code supplies associated Deshpande–Fleck foam plasticity, J2 steel plasticity, corotational logarithmic strain, committed state, and displacement-controlled equilibrium. `METHOD.md` states the equations and assumptions; `INPUTS.json` supplies curves and pins. The 28 custody checks all match.

**Convergence and geometry.** Mesh counts below are meridional elements / core layers / layers per face. All listed runs trace a descending branch; the first sampled local maximum and the largest path pressure are separate. The Gaussian shape moves every layer equally. The reconstructed rigid-sphere indentation compresses the core and imports the resulting geometry with stress, plastic strain and hardening reset. This import convention is conditional. The indenter radius and depth were fixed from the paper; no parameter was adjusted to match 6.03 MPa.

| Case | Mesh | First sampled local maximum, MPa | Largest traced pressure, MPa | Largest-pressure gap to 6.03 |
|---|---:|---:|---:|---:|
{peak_rows}

The `base` and `pilot` Gaussian runs did not constrain local plastic increments and can jump across local crushing states. The guarded runs supply the reference admissibility brackets; close global maxima do not make every unrestricted local state accurate.

| Numerical comparison | Largest pressure, MPa | Change |
|---|---:|---:|
{comparison_rows}

The reconstructed midsurface case changes {mesh['relative_change_percent']:+.4f}% when the angular and core mesh are doubled, and {penalty['relative_change_percent']:+.4f}% when the coarse-mesh contact penalty is doubled. These are observed refinements, not rigorous error bounds. The Gaussian path's early negative-slope branch means its larger later maximum cannot be called its first pressure-control instability. No full nonaxisymmetric stability or dynamic jump is computed.

**Linear gap.** At 384 meridional elements, eight core layers and two layers per face, the dead-pressure eigenvalues are {refs['outer']['dead_pressure_MPa'][0]:.9f} MPa for outer radius 42.8 mm ({refs['outer']['dead_gap_percent']:+.5f}%) and {refs['mid']['dead_pressure_MPa'][0]:.9f} MPa for midsurface radius 42.8 mm ({refs['mid']['dead_gap_percent']:+.5f}%) against the paper's 27.53 MPa. Including follower-load stiffness gives {refs['outer']['follower_pressure_MPa'][0]:.9f} and {refs['mid']['follower_pressure_MPa'][0]:.9f} MPa respectively. `LINEAR.json` retains all three meshes and four eigenvalues per case. The radius reading explains much of the linear gap.

**Benchmark normalization.** The paper's pressure ratio is 6.03/27.53 = {6.03/27.53:.9f}. The refined midsurface indentation pressure divided by the converged same-radius dead-pressure eigenvalue gives {kdf['largest_over_dead_linear']:.9f} ({kdf['dead_ratio_gap_percent']:+.3f}% relative to that ratio); using the follower-load eigenvalue gives {kdf['largest_over_follower_linear']:.9f}. `RESULTS.json` keeps the denominator definition and first-turn ratio for every case. This numerical normalization is not a P2 lead gamma or a material validation.

**Admissibility at every increment.** All raw paths retain plastic strains, Cauchy stresses, source-extrapolation counts, Jacobians and equilibrium residuals. The following pressure intervals bracket each first crossing. Events are grouped by type; the pressure turning points are listed separately.

| Event | Tight Gaussian outer-radius case, MPa | Refined indentation midsurface case, MPa |
|---|---:|---:|
{event_rows}
| First sampled pressure turning point | {local(tight):.6f} | {local(mid):.6f} |
| Largest traced pressure | {pressure(tight):.6f} | {p_mid:.6f} |

The Gaussian path's first turning point precedes its shear-screen crossing on the later ascending branch. For the reconstructed indentation, the shear screen is crossed before the first pressure maximum.

Foam plastic yielding occurs first. For these two guarded reference cases, **face yield precedes the implied initial shear-strength crossing and the pressure turning point**. Plastic yielding is permitted by this constitutive model; it is not itself rupture. The foam shear screen is the assumed yield ellipse's virgin pure-shear strength, 0.989949 MPa, not a recovered PVC80 fracture allowable. Consequently, a physical shear-failure-versus-instability governing capacity cannot be assigned from these sources. At the refined indentation peak, maximum foam equivalent plastic strain is {peak['core_equivalent_plastic_strain']:.6f}, {peak['core_extrapolated_points']} core integration points use extrapolation, resolved core shear is {peak['core_shear_MPa']:.6f} MPa, and minimum J is {peak['minimum_J']:.6f}.

**Material uncertainty.** The paper omits the foam hydrostatic strength and flow calibration. The declared zero-plastic-Poisson-ratio assumption and two alternative ellipses are separate scenarios. The printed foam densification slope exceeds its stated E=40 MPa; the constant-E monotone hardening fit cannot represent that entire curve. Later strains explicitly extrapolate the last retained slope. The steel plot's apparent factor-of-ten axis problem is unresolved: 750 MPa initial yield is a declared interpretation, not an established erratum.

| Material sensitivity, 96 / 4 / 2 Gaussian outer-radius mesh | Largest pressure, MPa | Gap to 6.03 |
|---|---:|---:|
{sensitivity_rows}

The literal steel-axis reading produces {pressure('steel-literal-96c4-guarded'):.4f} MPa, outside the indentation scenario range. Thus proximity of one pressure result does not remove source uncertainty.

**Honeycomb transfer.** `HONEYCOMB-TRANSFER.md` specifies a sourced orthotropic directional crush/shear candidate and maximum-stress onset screen. For CR III 5056, 3/8-inch cell, 1.0 pcf, the datasheet distinguishes stabilized compression peak 60 psi typical / 35 psi minimum-average from the separate 35 psi crush stress; L shear is 55 / 45 psi and W shear 35 / 25 psi. Those scalars do not identify postpeak strain, densification, unloading or shear-fracture energy. [Hexcel Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).

**P2 disposition.** No trusted P2 gamma follows. It still needs identified directional honeycomb curves and mixed-mode failure, thin beryllium compression/fracture and bonding data, admissible finite-strain in-plane behavior, a realizable ribbon layout, imperfections/joints, and three-dimensional stability, followed by relevant experimental validation. The CHECK029 lead strength violations remain unresolved. A steel/PVC hemisphere cannot establish a honeycomb/beryllium knockdown by transfer alone.

**Evidence and closure.** `RESULTS.json` contains all {len(cases)} pressure cases, {len(results['indentation_cases'])} indentation cases, first-event brackets, turning-point samples, mesh/step/contact comparisons and resource receipts. `VERIFICATION.json` has 28 passing material/assembled-force/linear-anchor checks; the contact tangent check passes at relative error 3.58e-7. Two earlier verification-harness failures are retained with their corrected reruns. Every heavy run used simjob with one core and 4 GiB; logs preserve admission/release, with exact source snapshots for every pressure/indentation job and the final successful verification. `NFI.json` has {len(nfis['issues'])} explicit unresolved issues. PNG/PDF figures and raw NPZ states are included. Start: {results['started_at']}; end: {now}, measured only.

The assigned card is complete with the stated scientific limitations. No successor is named by this brief.
"""
    (ROOT/"CARD.md").write_text(text)
    results["ended_at"]=now
    results["disposition"]={
        "measured_pressure_validation":"not established; target is numerical",
        "conditional_indent_band_MPa":[pmin,pmax],
        "conditional_indent_gap_percent":[100*(pmin/6.03-1),100*(pmax/6.03-1)],
        "band_scope":"Four indentation/radius cases with at least96 meridional elements and penalty at least30000 MPa/mm; interpreted steel curve; excludes48-element pilot; not a confidence interval.",
        "band_case_names":primary,
        "first_material_yield":"foam",
        "first_requested_strength_screen":"face yield",
        "screen_order_scope":[tight,mid],
        "physical_core_shear_failure":"unidentified; no recovered rupture criterion",
        "P2_gamma":"not released"}
    (ROOT/"RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({"card":str(ROOT/"CARD.md"),"pressure_cases":len(cases),"ended_at":now}))


if __name__=="__main__":
    build()
