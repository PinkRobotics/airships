import json
import math
import statistics
from datetime import datetime
from rederive import OUT, OWNER, AREA, R, P, E, NU, RC, RHO, LIFT, RESERVE, SCARF, skin_join, model, score


def psi_single_skin(a,b,d,t,nu):
    skin=t/(1-nu*nu)
    lattice=.75*math.sqrt(3)*b*d/a
    bare=t**3/(12*(1-nu*nu))
    composite=bare+lattice*d*d/12+skin*lattice/(skin+lattice)*((t+d)/2)**2
    return composite/bare


def run():
    full=json.loads((OWNER/"RUNS.json").read_text())
    # Reconstruct the nominal seam-limited floating baseline by two equalities.
    f=P*R/(4*SCARF)
    jp=skin_join(f,0.)
    fixed=sum(v for k,v in jp.items() if k!="seam_m")
    c=(LIFT-RESERVE-100-2*AREA*f*RHO-fixed)/(AREA*RC+jp["seam_m"]*.25)
    baseline=model("baseline",None,f,c)
    b=baseline["base"]
    nominal=dict(Vc=baseline["Vc"],gamma_needed=1/b["global"],Q_needed=1/b["wrinkle_per_Q"],
                 crimp=b["crimp"],dimple=b["dimple"],crush=b["crush_uniform"],scarf=b["scarf_screen"],
                 face_SF_345=b["face_per_Pa"]*345e6,teq_mm=baseline["teq"]*1000,
                 global_wavelength_m=baseline["lam_g"],
                 joining=dict(baseline["masses"]["skin_joining_parts"],total=baseline["masses"]["skin_joining"]))
    from rederive import leaves
    actual=dict(leaves(nominal))
    checks=[]
    for k,v in leaves(full["reproduce_028b"]):
        if k in actual:
            w=actual[k]
            checks.append(dict(path=k,filed=v,independent=w,delta=w-v,
                               ok=abs(w-v)<=max(1e-9,abs(v)*2e-6)))
    psi={}
    for name,values in [
        ("aluminium_dome_IDH_ref_1-1",(1.65,.10,.166,.0375,.33)),
        ("plastic_1-G",(1.57,.0191,.230,.0474,.35)),
        ("plastic_2-G",(1.60,.0239,.226,.0479,.35)),
        ("plastic_3-G",(1.25,.0153,.205,.0296,.35))]:
        psi[name]=dict(dimensions_in=values[:4],nu_inferred_not_specified_in_INPUTS=values[4],
                       psi=psi_single_skin(*values),filed=full["psi_record_domes"][name])
    ratios=dict(
        monocoque_low=.48/.6125,monocoque_high=.50/.6125,
        geodesic_1G=.348/.6125,geodesic_2G=.377/.6125,
        geodesic_3G_design_normalized=(3.96/4.03)*.4/.6125,
        aluminium_test=.52/1.225,handbook_co=.612*.425,
        Pineda_low=1/1.238,Pineda_high=1/1.0285,
        Ossola_plain_317_over_917=317/917,Ossola_isogrid_410p3_over_934=410.3/934,
        Ossola_sample_mean=statistics.mean([414,411,406]),
        Ossola_sample_sd=statistics.stdev([414,411,406]),
        Ossola_plain_nonlinear_error=(507/317-1),Ossola_isogrid_nonlinear_error=(448/410.3-1),
        TA01_test_classical=689.2/726.8,TA01_nonlinear_error=619.8/689.2-1,
        TA02_classical_kips=.4*726.8,TA02_LS4_test_classical=286.2/(.4*726.8),
        TA02_LS5_test_classical_280=280/(.4*726.8),TA02_LS5_test_classical_279p7=279.7/(.4*726.8),
        TA02_LS5_prediction_error_268_vs_280=268/280-1,
        TA02_LS5_prediction_error_267p6_vs_279p7=267.6/279.7-1,
        TA07_prediction_error=554/647-1,TA07_drop=1-312.2/647,
        STA8p1_test_above_pretest=743/697-1,STA8p1_final_prediction_error=754/743-1,
        STA8p1_intermediate_prediction_error=759/743-1,
        STA8p1_nonuniform_loading_reduction=1-754/759,
        STA8p1_imperfection_reduction=1-697/720,
        TA09_weld_and_imperfection_reduction=1-509/738,
        STA8p1_total_height_in=.500+.070)
    o5=full["concepts"][-1]["best_today_O5"]
    sic=full["concepts"][-2]["best_today_O5"]
    fp=o5["tf_mm"]/1000;cp=o5["tc_mm"]/1000
    dskin=E*fp*(fp+cp)**2/(2*(1-NU**2))
    equal_radius=o5["a_m"]*math.sqrt(math.sqrt(3)/(4*math.pi))
    circ_radius=o5["a_m"]/math.sqrt(3)
    circ_lambda=o5["lam_panel"]*circ_radius/equal_radius
    inscribed_lambda=circ_lambda/2
    diagnostics=dict(
        C2b_O5=dict(gamma_s_filed=o5["gamma_s"],isolated_tube_EI_over_a_Dskin=E*o5["section"]["I"]/(o5["a_m"]*dskin),
                   psi_identity=1+3*math.sqrt(3)/4*o5["gamma_s"],
                   cap_factor_exact_at_filed_lambda=.14+3.2/o5["lam_panel"]**2,
                   gamma_required_for_panel=1/o5["base"]["panel"],
                   Q_required=1/o5["base"]["wrinkle_per_Q"],
                   scarf_tau_required_Pa=o5["sig_face_MPa"]*1e6*30/901,
                   unrestricted_global_SF=.2*o5["base"]["global_unrestricted"],
                   wavelength_excluded_from_global_minimum_m=o5["lam_g"],
                   wavelength_cutoff_m=2*o5["a_m"],
                   equal_area_radius_m=equal_radius,circumscribed_radius_m=circ_radius,
                   circumscribed_lambda=circ_lambda,
                   circumscribed_cap_factor=.14+3.2/circ_lambda**2,
                   circumscribed_panel_SF=o5["base"]["panel"]*(.14+3.2/circ_lambda**2),
                   inscribed_lambda=inscribed_lambda,
                   inscribed_cap_factor=min(1/1.238,.14+3.2/inscribed_lambda**2),
                   pipe_Euler_pin_ended_SF=math.pi**2*E*o5["section"]["I"]/(o5["a_m"]**2*o5["section"]["F"])),
        SiC_O5=dict(mechanical_member_force_N=sic["section"]["F"],
                    compression_envelope_member_force_N=sic["sig_r"]*sic["section"]["A"],
                    omitted_thermal_force_N=sic["sig_r"]*sic["section"]["A"]-sic["section"]["F"],
                    scalar_sleeve_mass_if_scaled_to_compression_envelope_kg=157.7*sic["sig_r"]*sic["section"]["A"]/562200),
        boundary_sensitivity="Circumscribed/inscribed substitutions are sensitivity examples, not alternative validated triangular-cap rules.",
        missing_mode_sensitivity="Unrestricted smeared N(k) is a diagnostic; homogenization is itself unverified at wavelengths of only 1-2 bays.")
    from pathlib import Path
    prior=json.loads(Path("evidence/3fc568384c22184b-RESULTS.json").read_text())["model"]
    old_area=math.pi*(prior["r_o_m"]**2-(prior["r_o_m"]-prior["wall_m"])**2)
    continuum_length=AREA*2*math.sqrt(3)/2.04
    length_ratio=prior["arc_total_length_m"]/continuum_length
    diagnostics["026_layout"]=dict(
        tube_area_independent_m2=old_area,
        member_mass_from_area_and_reported_arc_length_kg=old_area*3100*prior["arc_total_length_m"],
        filed_026_member_mass_kg=prior["tube_mass_kg"],
        continuum_length_039_m=continuum_length,
        actual_026_arc_length_m=prior["arc_total_length_m"],
        actual_over_continuum_length=length_ratio,
        C2b_O5_mass_change_at_unchanged_tubes_kg=o5["lattice_kg"]*(length_ratio-1),
        note="Length-only sensitivity: actual load redistribution and joining require the discrete layout. 026 arc length is an input, not regenerated here.")
    elapsed=[]
    for fn in ["RUNS.json","RUNS-gs5.json"]:
        d=json.loads((OWNER/fn).read_text())
        delta=(datetime.fromisoformat(d["ended_local"])-datetime.fromisoformat(d["started_local"])).total_seconds()
        elapsed.append(dict(file=fn,measured_timestamp_delta_s=delta,filed_s=d["elapsed_s"],difference_s=delta-d["elapsed_s"]))
    results=dict(nominal_baseline_geometry=dict(tf_mm=f*1000,tc_mm=c*1000),
                 nominal_baseline=nominal,nominal_checks=checks,psi_calibration=psi,ratios=ratios,
                 diagnostics=diagnostics,elapsed=elapsed)
    (OUT/"SUPPLEMENTARY.json").write_text(json.dumps(results,indent=2)+"\n")
    assert all(x["ok"] for x in checks)
    print(json.dumps(dict(nominal_comparisons=len(checks),all_match=True,psi=psi,
                          diagnostics=diagnostics,elapsed=elapsed),indent=2))


if __name__=="__main__":
    run()
