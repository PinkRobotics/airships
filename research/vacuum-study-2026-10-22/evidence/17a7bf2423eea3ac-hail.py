"""045 contact-patch calculation and explicit, uncalibrated probability transfers.

All events are conditional on a direct tube strike. No lifetime or flight risk.
The orthotropic extension retains 045's approximate Winkler foundation and
replaces the plate stiffness by the laminate tensor. It is not an impact solve.
"""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma,j1,kv
from material_models import models,transform,model

ROOT=Path(__file__).resolve().parent
OLD=json.loads((ROOT/"intake/045/RESULTS.json").read_text())["compute"]["p3"]

def integral(a):
    b=np.exp(1j*math.pi/4)
    return -np.imag(b*kv(1,a*b))

def contact(mat,ro,t,angles=1024):
    Q=np.asarray(mat["Q_Pa"]);D=Q*t**3/12
    k=mat["Ehoop_Pa"]*t/ro**2
    theta=(np.arange(angles)+.5)*2*math.pi/angles
    co=np.cos(theta);si=np.sin(theta)
    den=D[0,0]*co**4+2*(D[0,1]+2*D[2,2])*co**2*si**2+D[1,1]*si**4
    ell=(den/k)**.25
    common=.012*ell*integral(.012/ell)/den
    mx=np.mean(common*(D[0,0]*co**2+D[0,1]*si**2))
    my=np.mean(common*(D[0,1]*co**2+D[1,1]*si**2))
    # Moment and surface stress per unit contact pressure.
    moments=np.array([mx,my,0.])
    strain=(t/2)*np.linalg.solve(D,moments)
    ply=[]
    for angle,weight in mat["layup"]:
        s=np.asarray(mat["lamina_Q_Pa"])@transform(np.asarray(mat["lamina_Q_Pa"]),angle)[1]@strain
        ply.append(dict(angle=angle,weight=weight,stress_per_contact_Pa=s.tolist()))
    return dict(Mx_per_pressure_m2=float(mx),My_per_pressure_m2=float(my),
        shell_surface_axial_per_pressure=float(6*mx/t**2),
        shell_surface_hoop_per_pressure=float(6*my/t**2),
        max_homogenized_tensile_stress_per_pressure=float(6*max(mx,my)/t**2),
        ply=ply,ell_minmax_m=[float(ell.min()),float(ell.max())])

def pf(s,scale,m):
    return float(-math.expm1(-((s/scale)**m)))

def populations(mat):
    key=mat["id"]
    if key in ["041-reference","Hexoloy-SA","UltraSiC-sintered"]:
        return [(name,x["sigma0_Pa"],x["m"],
                 "uncalibrated transfer: different tube/bar population and effective area; not P3 break probability")
                for name,x in OLD["weibull"].items()]
    if key=="CVD-PureSiC-HR":
        return [("PremaTech CVD flexure",424e6,11,
                 "uncalibrated cross-vendor flexural transfer; source effective size absent")]
    if key=="Tyranno-SA-CVI-scenario":
        return [("Yang2003 Tyranno-SA/CVI flexure",597e6/gamma(1+1/10.2),10.2,
                 "formal coupon-flexure transfer; composite damage is not complete member break")]
    return []

def main():
    mats={x["id"]:x for x in models()}
    checks=[]
    # Pinned run45.py:288 uses assumed nu=.16; 041 uses .14.
    oldiso=model("old-045",410,410,410/(2*1.16),.16,3100,kind="isotropic")
    old=contact(oldiso,.27508285638018676/2,.0011373648451578344)
    expected=OLD["tube_hail"][-1]["sigma_per_MPa_contact"]
    calc=old["max_homogenized_tensile_stress_per_pressure"]*1e6
    checks.append(dict(name="045 contact stress coefficient",actual=calc,expected=expected,
                       relative_error=calc/expected-1,passed=abs(calc/expected-1)<2e-6))
    for a in [.2,1.,2.,4.]:
        numerical=quad(lambda u:j1(a*u)*u*u/(u**4+1),0,200,limit=1000,epsabs=1e-10)[0]
        numerical+=quad(lambda u:j1(a*u)*u*u/(u**4+1),200,4000,limit=8000,epsabs=1e-10)[0]
        exact=float(integral(a))
        checks.append(dict(name=f"Kelvin/Bessel integral a={a}",actual=exact,
            quadrature=numerical,passed=abs(exact-numerical)<2e-7))
    section_rows=json.loads((ROOT/"FRAME-COMPARE.json").read_text())["rows"]
    if (ROOT/"WITNESSES.json").exists():
        section_rows += [x["comparison_geometry"] for x in json.loads((ROOT/"WITNESSES.json").read_text())["rows"]
                        if x["FE"]["section_policy"]!="minimum_wall_q1_screen"]
    rows=[];required=[];flat=[]
    for section in section_rows:
        if "wall_m" not in section:continue
        mat=mats[section["material"]]
        unit=contact(mat,section["ro_m"],section["wall_m"])
        coarse=contact(mat,section["ro_m"],section["wall_m"],512)
        error=max(abs(unit[k]/coarse[k]-1) for k in [
            "shell_surface_axial_per_pressure","shell_surface_hoop_per_pressure"])
        checks.append(dict(name="angular convergence "+mat["id"]+" "+section["reserve"]+" "+section["section_policy"],
                           relative_error=error,passed=error<1e-6))
        for threat in OLD["tube_hail"]:
            pflow=threat["q_flow_Pa"]
            factor=threat["sigma_shi_Pa"]/threat["sigma_flow_Pa"]
            estimates=[]
            for label,pcontact in [("flow",pflow),("Shi",pflow*factor)]:
                stress=unit["max_homogenized_tensile_stress_per_pressure"]*pcontact
                for pop,scale,m,caveat in populations(mat):
                    estimates.append(dict(pressure_model=label,population=pop,scale_Pa=float(scale),m=m,
                        uncalibrated_045_Pbreak_surrogate=pf(stress,scale,m),caveat=caveat))
                for m in [5,10,20,40]:
                    for target in [.001,1e-6]:
                        required.append(dict(material=mat["id"],reserve=section["reserve"],
                            section_policy=section["section_policy"],diameter_m=threat["D_m"],
                            pressure_model=label,m=m,target_conditional_strike_probability=target,
                            required_matching_contact_test_scale_Pa=stress/(-math.log1p(-target))**(1/m)))
            # A numerical answer for every construction under the SAME two
            # assumed contact-test distributions. This is explicitly a required
            # calibration scenario, not transferred fibre/laminate statistics.
            conditional_grid=[]
            for label,pcontact in [("flow",pflow),("Shi",pflow*factor)]:
                stress=unit["max_homogenized_tensile_stress_per_pressure"]*pcontact
                for scale,m in [(192e6,5.5),(299e6,4.6)]:
                    conditional_grid.append(dict(pressure_model=label,assumed_contact_scale_Pa=scale,m=m,
                        conditional_probability_if_contact_fit_applies=pf(stress,scale,m),
                        fit_measured_for_this_construction=False))
            # Maximum stress criteria identify a first-ply damage screen only.
            ply_util=[]
            for ply in unit["ply"]:
                s=np.abs(np.asarray(ply["stress_per_contact_Pa"])*pflow*factor)
                xt1=2.020e9 if mat["id"].startswith("M55J") else (2.860e9 if mat["id"].startswith("T700S") else None)
                xc1=None if mat["ply_Xc_GPa"] is None else mat["ply_Xc_GPa"]*1e9
                longitudinal=min(v for v in [xt1,xc1] if v is not None) if any(v is not None for v in [xt1,xc1]) else None
                limits=[longitudinal,None if mat["ply_transverse_tension_GPa"] is None else mat["ply_transverse_tension_GPa"]*1e9,
                        None if mat["ply_shear_GPa"] is None else mat["ply_shear_GPa"]*1e9]
                ply_util.append(dict(angle=ply["angle"],surface_stress_Pa=s.tolist(),
                    maximum_stress_utilization=[None if lim is None else float(v/lim) for v,lim in zip(s,limits)]))
            row=dict(tag="QUESTIONABLE / PROJECTION",material=mat["id"],reserve=section["reserve"],
                section_policy=section["section_policy"],radius_m=section["ro_m"],wall_m=section["wall_m"],
                diameter_m=threat["D_m"],velocity_m_s=threat["v_m_s"],patch_radius_m=.012,
                p_flow_Pa=pflow,p_Shi_Pa=pflow*factor,unit_contact=unit,
                stress_flow_Pa=unit["max_homogenized_tensile_stress_per_pressure"]*pflow,
                stress_Shi_Pa=unit["max_homogenized_tensile_stress_per_pressure"]*pflow*factor,
                sourced_population_surrogates=estimates,explicit_common_fit_scenarios=conditional_grid,
                ply_damage_screen_Shi=ply_util,
                measured_member_break_probability=None,identified_probability_bounds=[0,1],
                caveat="No dynamic ice/contact/preload/size calibration; laminate first damage != tube severance; conditional direct strike only")
            sx=unit["shell_surface_axial_per_pressure"]*pflow*factor
            sy=unit["shell_surface_hoop_per_pressure"]*pflow*factor
            row["hail_only_von_Mises_Shi_Pa"]=math.sqrt(sx*sx+sy*sy-sx*sy)
            row["Al_hail_only_yield_SF"]=.276e9/row["hail_only_von_Mises_Shi_Pa"] if mat["id"]=="Al6061T6" else None
            rows.append(row)
            if threat["D_m"]==.0508:
                flat.append(dict(material=mat["id"],reserve=section["reserve"],section_policy=section["section_policy"],
                    wall_mm=section["wall_m"]*1000,stress_flow_MPa=row["stress_flow_Pa"]/1e6,
                    stress_Shi_MPa=row["stress_Shi_Pa"]/1e6,
                    scenario_192m5p5_Shi=conditional_grid[-2]["conditional_probability_if_contact_fit_applies"],
                    scenario_299m4p6_Shi=conditional_grid[-1]["conditional_probability_if_contact_fit_applies"],
                    actual_probability="unknown"))
    assert all(c["passed"] for c in checks),[c for c in checks if not c["passed"]]
    (ROOT/"HAIL.json").write_text(json.dumps(dict(tag="QUESTIONABLE / PROJECTION",checks=checks,rows=rows,
        target_rows=required,old_045_coefficient_Pa_per_MPa=calc),indent=2,allow_nan=False)+"\n")
    with (ROOT/"HAIL-DESIGN.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    print(json.dumps(dict(rows=len(rows),target_rows=len(required),checks=len(checks),failed=sum(not c["passed"] for c in checks),old045=calc)))

if __name__=="__main__":main()
