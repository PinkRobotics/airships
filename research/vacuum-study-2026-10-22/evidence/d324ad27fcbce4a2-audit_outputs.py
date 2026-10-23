"""Scalar audit and packaging of already-completed data; no simulation launch.

Uses only the Python standard library. Rise-force checks here are conditional
arithmetic on owner output, never a substitute for the refused independent solve.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_text())


def save(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")


owner=read("intake/owner/RESULTS.json")
own={p.parent.name:json.loads(p.read_text()) for p in sorted((ROOT/"runs").glob("*/RESULTS.json"))}
endpoints={r["frequency"]:r for r in read("ENDPOINT-AUDIT.json")["rows"]}
comparisons=[]
conditional=[]
sampling_differences=[]


def compare(row,field,claimed,calculated,kind="independent",rel=2e-8,abs_tol=1e-4):
    if isinstance(claimed,(int,float)) and isinstance(calculated,(int,float)):
        item=dict(row=row,field=field,card_value=claimed,checker_value=calculated,
                  difference=calculated-claimed,relative_tolerance=rel,absolute_tolerance=abs_tol,
                  passed=math.isclose(claimed,calculated,rel_tol=rel,abs_tol=abs_tol),basis=kind)
        (comparisons if kind=="independent" else conditional).append(item)


def tree(row,a,b,prefix="",kind="independent"):
    if isinstance(b,dict) and isinstance(a,dict):
        for key,value in b.items():
            if key in a:
                tree(row,a[key],value,prefix+"/"+key,kind)
    elif isinstance(a,(float,int)) and isinstance(b,(float,int)):
        compare(row,prefix,a,b,kind)


source_cases=read("intake/owner/CASES.json")
source022=read("intake/upstream/intake/rpt-mainline022-grok-p3-optimistic-floating-point-1020/RESULTS.json")["carried_011b_k02"]["equilateral"]
source022b=read("intake/upstream/intake/rpt-mainline022b-grok-equilibrium-1020/GAMMA.json")["cases"]["percent_crush_5"]["equilateral"]
source_input_rows=[]
for f,source,mapping in [
    (4,source022,dict(nominal_s_m="s_m",r_o_m="r_o_m",wall_m="t_w_m",film_mass_kg="m_film_kg",systems_kg="m_systems_kg",source_payload_kg="m_payload_kg")),
    (2,source022b,dict(nominal_s_m="s_m",r_o_m="r_o_m",wall_m="t_w_m",film_mass_kg="m_film",source_sag_debit_kg="sag_kg"))]:
    for copied,original in mapping.items():
        a,b=source_cases[str(f)][copied],source[original]
        source_input_rows.append(dict(frequency=f,field=copied,source_field=original,
                                     card_value=a,source_value=b,passed=math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)))
save("SOURCE-INPUT-CHECK.json",dict(rows=source_input_rows,all_pass=all(x["passed"] for x in source_input_rows),
     note="Section and mass inputs trace to the selected source rows. Physical material, film and joint validity is not inferred."))

linear_summary=[]
mass_summary=[]
static_summary=[]
for row in owner["comparison"]:
    f=row["frequency"]
    label={2:"f2-m48",4:"f4-m24",6:"f6-m12"}[f]
    calc=own[label]
    tree(f"f{f} model",row["model"],calc["model"])
    # The owner samples one endpoint according to stored member orientation.
    # Our original outputs averaged both ends. Align the declared statistic
    # without changing either frozen scientific output.
    static_comparable=dict(calc["static"])
    static_comparable["member_endpoint_chord_thrust_N"]=endpoints[f]["independent_first_endpoint_in_owner_orientation_stats"]
    tree(f"f{f} static",row["static"],static_comparable)
    for name in ["member_mean_compression_all_N","member_endpoint_chord_thrust_all_N"]:
        checked=(endpoints[f]["own_first_endpoint_in_owner_order_N"]
                 if name=="member_endpoint_chord_thrust_all_N" else calc["static"][name])
        a,b=sorted(row["static"][name]),sorted(checked)
        assert len(a)==len(b)
        for i,(x,y) in enumerate(zip(a,b)):
            compare(f"f{f} static",f"{name}/sorted/{i}",x,y)
    for field in ["mean","max"]:
        a=row["static"]["member_endpoint_chord_thrust_N"][field]
        b=endpoints[f]["independent_both_endpoint_mean_stats"][field]
        sampling_differences.append(dict(row=f"f{f} baseline",field="member_endpoint_chord_thrust_N/"+field,
            card_value=a,checker_value=b,difference=b-a,status="different endpoint sampling convention",
            owner_convention="first endpoint in stored member orientation",
            checker_alternative="per-member average of both endpoint chord thrusts",
            same_convention_value=endpoints[f]["independent_first_endpoint_in_owner_orientation_stats"][field],
            nfi="NFI-C026B-ENDPOINTS"))
    # Match five-valent nodes by actual location, not implementation-specific IDs.
    for node in row["static"]["five_valent_nodes"]:
        matched=min(calc["static"]["five_valent_nodes"],
                    key=lambda q:sum((a-b)**2 for a,b in zip(q["position"],node["position_m"])))
        distance=math.sqrt(sum((a-b)**2 for a,b in zip(matched["position"],node["position_m"])))
        assert distance<1e-9
        compare(f"f{f} node at {node['position_m']}","incident_member_mean_compression_N/mean",
                node["incident_member_mean_compression_N"]["mean"],matched["mean_member_compression_N"])
        compare(f"f{f} node at {node['position_m']}","incident_endpoint_compression_N/mean",
                node["incident_endpoint_compression_N"]["mean"],matched["mean_endpoint_axial_compression_N"])
    linear=own["f6-m24"] if f==6 else calc
    compare(f"f{f}","linear",row["linear"],linear["linear"],rel=2e-9,abs_tol=1e-10)
    continuum=calc["model"]["continuum_perfect_lambda_nominal_s"]
    diff=100*(linear["linear"]/continuum-1)
    compare(f"f{f}","linear_difference_from_nominal_continuum_pct",
            row["linear_difference_from_nominal_continuum_pct"],diff)
    compare(f"f{f}","linear_over_nominal_continuum",row["linear_over_nominal_continuum"],linear["linear"]/continuum)
    compare(f"f{f}","linear_over_mean_arc_continuum",row["linear_over_mean_arc_continuum"],
            linear["linear"]/calc["model"]["continuum_perfect_lambda_actual_mean_arc"])
    refinement=[]
    for old in row["linear_convergence"]:
        name=f"f{f}-m{old['segments']}"
        if f==2 and old["segments"]==12:name="validation-f2-m12"
        result=own[name]
        compare(f"f{f} convergence",f"m{old['segments']}/lambda",old["lambda"],result["linear"],rel=2e-9,abs_tol=1e-10)
        refinement.append(dict(segments=old["segments"],owner_lambda=old["lambda"],checker_lambda=result["linear"]))
    change=None
    if len(refinement)>1:
        change=100*(refinement[-1]["checker_lambda"]/refinement[-2]["checker_lambda"]-1)
        compare(f"f{f}","linear_last_refinement_pct",row["linear_last_refinement_pct"],change,abs_tol=1e-8)
    linear_summary.append(dict(frequency=f,owner_lambda=row["linear"],checker_lambda=linear["linear"],
        difference=linear["linear"]-row["linear"],continuum_nominal=continuum,
        difference_from_continuum_percent=diff,refinement=refinement,last_mesh_change_percent=change,
        max_checker_eigen_residual=max(p["relative_residual"] for p in linear["linear_modes"])))
    m=calc["model"]
    mass_summary.append(dict(frequency=f,**{k:m[k] for k in [
        "tube_mass_kg","joints_5pct_kg","node_mass_kg","film_mass_inherited_kg",
        "systems_inherited_kg","total_mass_with_inherited_allowances_kg",
        "payload_before_sag_kg","payload_after_source_sag_kg",
        "headroom_after_source_sag_and_source_payload_kg"]},
        carried_sag_kg=source_cases[str(f)]["source_sag_debit_kg"],
        joint_rule=source_cases[str(f)]["joint_rule"]))
    static_summary.append(dict(frequency=f,segments=calc["model"]["segments_per_arc"],
        mean_compression_N=calc["static"]["member_mean_compression_N"]["mean"],
        max_member_mean_compression_N=calc["static"]["member_mean_compression_N"]["max"],
        five_valent_member_means_N=[n["mean_member_compression_N"] for n in calc["static"]["five_valent_nodes"]],
        five_valent_endpoint_means_N=[n["mean_endpoint_axial_compression_N"] for n in calc["static"]["five_valent_nodes"]],
        max_bending_stress_Pa=calc["static"]["max_end_bending_stress_Pa"],
        equilibrium_relative_residual=calc["equilibrium_relative_residual"]))

pin_checks=read("runs/validation-f2-m12/VALIDATION.json")["pin_counts"]
for p in pin_checks:
    row=next(r for r in owner["comparison"] if r["frequency"]==p["frequency"])
    compare(f"f{p['frequency']}","pinned_internal_mechanisms_excluding_six_rigid_motions",
            row["pinned_internal_mechanisms_excluding_six_rigid_motions"],p["internal_mechanisms"])

# This is bookkeeping on owner-supplied raised-shape and force outputs.
# It does not solve, interpolate, or substitute a model for the refused job.
rise=owner["rise_supplement"]
area=own["f6-m12"]["model"]["A_m2"]
inertia=own["f6-m12"]["model"]["I_m4"]
ro=source_cases["6"]["r_o_m"]
rise_audit=[]
for key in ["rise8_m12","rise8_m24"]:
    r=rise[key];model=r["model"];s=r["static"]
    tubes=3100*area*model["arc_total_length_m"]
    mass=1.05*tubes+model["node_mass_kg"]+97.515+50.
    bending=s["max_end_bending_moment_Nm"]*ro/inertia
    for field,a,b in [
        ("tube_mass_kg",model["tube_mass_kg"],tubes),
        ("total_mass_with_inherited_allowances_kg",model["total_mass_with_inherited_allowances_kg"],mass),
        ("max_end_bending_stress_Pa",s["max_end_bending_stress_Pa"],bending)]:
        compare(key,field,a,b,"owner_inputs_only")
    rise_audit.append(dict(row=key,owner_mean_compression_N=s["member_mean_compression_N"]["mean"],
        independently_solved_mean_compression_N=None,owner_chord_thrust_N=s["member_endpoint_chord_thrust_N"]["mean"],
        owner_peak_moment_Nm=s["max_end_bending_moment_Nm"],
        bending_from_owner_moment_and_independent_section_Pa=bending,
        mass_from_owner_arc_length_and_independent_section_kg=mass,
        geometry_and_forces_independently_reproduced=False))
baseline=own["f6-m12"]["static"]
a=rise["rise8_m12"]["static"];b=rise["rise8_m24"]["static"]
for field,value in [
    ("mean_axial_ratio_rise8_to_baseline_m12",a["member_mean_compression_N"]["mean"]/baseline["member_mean_compression_N"]["mean"]),
    ("mean_chord_thrust_ratio_rise8_to_baseline_m12",a["member_endpoint_chord_thrust_N"]["mean"]/endpoints[6]["independent_first_endpoint_in_owner_orientation_stats"]["mean"]),
    ("refinement_mean_axial_pct",100*(b["member_mean_compression_N"]["mean"]/a["member_mean_compression_N"]["mean"]-1)),
    ("refinement_peak_bending_pct",100*(b["max_end_bending_stress_Pa"]/a["max_end_bending_stress_Pa"]-1))]:
    compare("rise supplement",field,rise[field],value,"owner_inputs_only")

nonlinear_audit=[]
for f,ms in [(4,[6,12]),(2,[12,24])]:
    owner_row=next(r for r in owner["comparison"] if r["frequency"]==f)
    for m in ms:
        r=read(f"intake/owner-data/nonlinear/perfect-f{f}-m{m}/RESULTS.json")
        lo,hi=r["stability_bracket"]
        midpoint=(lo["lambda"]+hi["lambda"])/2
        compare(f"nonlinear f{f} m{m}","critical_lambda_estimate",r["critical_lambda_estimate"],midpoint,"owner_inputs_only")
        nonlinear_audit.append(dict(frequency=f,segments=m,raw_reported_crossing=r["critical_lambda_estimate"],
            bracket_midpoint=midpoint,bracket_control_width_m=hi["control_m"]-lo["control_m"],
            pressure_slope_on_final_bracket_Pa_per_m=95460.8379139*(hi["lambda"]-lo["lambda"])/(hi["control_m"]-lo["control_m"]),
            independent_equilibrium_or_eigen_solve=False,verified_first_instability=None,
            maximum_raw_relative_Newton_residual=max(p["final_relative_residual"] for p in r["path"]),
            raw_interpretation=r["interpretation"],raw_stability_solver=r["stability_solver"]))
    values=[r for r in nonlinear_audit if r["frequency"]==f]
    change=100*(values[-1]["bracket_midpoint"]/values[0]["bracket_midpoint"]-1)
    compare(f"nonlinear f{f}","nonlinear_last_refinement_pct",owner_row["nonlinear_last_refinement_pct"],change,"owner_inputs_only")
    compare(f"nonlinear f{f}","reported_tangent_zero_over_discrete_linear",
        owner_row["reported_tangent_zero_over_discrete_linear"],
        values[-1]["bracket_midpoint"]/next(r["checker_lambda"] for r in linear_summary if r["frequency"]==f),
        "owner_inputs_only")

f4path=read("intake/owner-data/nonlinear/perfect-f4-m12/RESULTS.json")["path"]
ambiguity=[r for r in f4path if abs(r["lambda"]-5.059944979206884)<1e-10 or abs(r["lambda"]-5.080744423604787)<1e-10]
assert len(ambiguity)==2
save("NONLINEAR-AUDIT.json",dict(rows=nonlinear_audit,f4_ambiguous_nearest_zero_points=ambiguity,
    conclusion="Bracket midpoints and arithmetic reproduce only from the owner data. Nearest-zero selection does not certify the first loss; new top-level null fields are appropriate.",
    reference="https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html"))
save("RISE-AUDIT.json",dict(rows=rise_audit,independent_static_solve=False,
    reason="Independent rise8 m12 admission refused; no retry or alternative solver execution. m24 rise8 was not submitted.",
    arithmetic=conditional[:10],
    unverified_owner_frozen_spherical_load=rise["rise8_m24"]["frozen_spherical_load_sensitivity"]))

receipts=[json.loads(p.read_text()) for p in sorted((ROOT/"execution").glob("*/END.json"))]
refused=[p for p in receipts if p["refused"]]
assert len(refused)==1 and refused[0]["label"]=="f6-m12-rise8"
assert all(p["returncode"]==0 and p["released"] for p in receipts if p["admitted"])
latest_failure=datetime.fromisoformat(refused[0]["ended_utc"])
assert all(datetime.fromisoformat(p["started_utc"])<=latest_failure for p in receipts)
owner_receipts=[json.loads(p.read_text()) for p in sorted((ROOT/"intake/owner-data/execution").glob("*/END.json"))]
owner_exit_counts=Counter(p["returncode"] for p in owner_receipts)
assert owner_exit_counts=={0:16,75:1},owner_exit_counts
save("EXECUTION.json",dict(jobs=receipts,admitted=sum(p["admitted"] for p in receipts),
    refused=len(refused),released=sum(p["released"] for p in receipts),
    post_refusal_solver_launches=0,all_admitted_jobs_succeeded_and_released=True,
    owner_pinned_exit_receipts=dict(owner_exit_counts),time_budget=None,
    remaining_activity="Read-only data inspection, scalar arithmetic, and report packaging; no numerical-library or simulation launch."))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]