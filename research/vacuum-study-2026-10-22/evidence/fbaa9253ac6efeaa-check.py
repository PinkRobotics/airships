"""Independent MAINLINE-023 force, fitting, mass and shell calculations.

Only numeric snapshots are read. No nodes.py, arcs.py or floatpoint.py is
read/imported/executed. Run this file with Python 3 and numpy.
"""
from pathlib import Path
from datetime import datetime
import csv
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
PI = math.pi
R, P, LIFT = 10., 95460.8379139, 4889.44215019
E, RHO, SIGMA = 410e9, 3100., 3900e6
FILM_MASS, SYSTEMS, NODE_MASS = 97.515, 50., .02
FILM_T, FILM_SIGMA = .00008, 1.5e9
TAU_BOND, TAU_BRAZE = 28.9e6, 25e6
MATERIALS = {
    "ti_sleeve": (4430., 827e6),
    "invar_sleeve": (8050., 276e6),
    "cfrp_wrap": (1550., 1470e6),
}
CS = {k: rho/(2*PI*strength*TAU_BOND)
      for k, (rho, strength) in MATERIALS.items()}
CB = RHO/(2*PI*TAU_BRAZE)
MODES = ("yield", "euler", "local", "film", "perry", "global")


def load(name):
    return json.loads((ROOT/"inputs"/name).read_text())


def counts(s):
    v = 8*PI*R*R/(math.sqrt(3)*s*s)+2
    return v, 3*v-6


def force(s, old=False):
    return P*R*s/(2 if old else 2*math.sqrt(3))


def budget(s):
    return LIFT-FILM_MASS-SYSTEMS-NODE_MASS*counts(s)[0]


def fitting(kind, n, r, area):
    if kind == "percent5":
        return None, None, None
    if kind == "sic_braze":
        length = n/(2*PI*r*TAU_BRAZE)
        return RHO*area*length, length, None
    rho, strength = MATERIALS[kind]
    length = n/(2*PI*r*TAU_BOND)
    thickness = n/(2*PI*r*strength)
    return rho*(n/strength)*length, length, thickness


def section(s, r, kind, old=False, joint_load_factor=1.):
    _, members = counts(s)
    n = force(s, old)*joint_load_factor
    b = budget(s)
    if kind == "percent5":
        tube = b/1.05
        joint = tube*.05
        area = tube/(RHO*members*s)
    elif kind == "sic_braze":
        length = n/(2*PI*r*TAU_BRAZE)
        area = b/(RHO*members*(s+2*length))
        tube = area*RHO*members*s
        joint = 2*members*RHO*area*length
    else:
        joint = 2*members*CS[kind]*n*n/r
        tube = b-joint
        area = tube/(RHO*members*s)
    return area, tube, joint


def scores(s, r, area, k, old=False):
    # Vector-capable exact annulus geometry, with stable wall/I expressions.
    r = np.asarray(r)
    area = np.asarray(area)
    radicand = r*r-area/PI
    valid = (area > 0) & (radicand >= 0) & (r <= s/3+1e-12) & (r <= .25+1e-12)
    ri = np.sqrt(np.maximum(0, radicand))
    wall = area/(PI*(r+ri))
    inertia = area*(r*r+ri*ri)/4
    n = force(s, old)
    stress = n/area
    euler_stress = PI*PI*E*inertia/(area*s*s)
    eta = (s/1000)*r*area/inertia
    b = SIGMA+(1+eta)*euler_stress
    discriminant = np.maximum(0, b*b-4*SIGMA*euler_stress)
    # Stable small root of Perry's quadratic.
    perry = 2*SIGMA*euler_stress/(b+np.sqrt(discriminant))
    values = {
        "yield": SIGMA/stress,
        "euler": euler_stress/stress,
        "local": .6*E*wall/r/stress,
        "film": np.full(np.broadcast(r, area).shape, 2*FILM_SIGMA*FILM_T/(P*s)),
        "perry": perry/stress,
        "global": k*4*math.sqrt(1.5)*E*np.sqrt(np.maximum(0, inertia*area))/(s*R*R*P),
    }
    least = np.minimum.reduce(np.broadcast_arrays(*[values[x] for x in MODES]))
    least = np.where(valid, least, -np.inf)
    return ri, wall, inertia, stress, values, least


def score_row(s, r, area, k, old=False):
    ri, wall, inertia, stress, values, least = scores(s, r, area, k, old)
    vals = {key:float(v) for key,v in values.items()}
    return dict(r_i_m=float(ri),t_w_m=float(wall),I_m4=float(inertia),
                sigma_axial_Pa=float(stress),
                **{"SF_"+name:v for name,v in vals.items()},
                governing=min(vals,key=vals.get),SF_least=float(least),
                sigma_contact_compression_Pa=float(stress),
                SF_contact_on_3900=SIGMA/float(stress),
                SF_contact_on_flexure_380=380e6/float(stress))


def row(s, r, kind, k=.2, old=False, frozen=False, allowance=None, joint_factor=1.):
    v, members = counts(s)
    area,tube,joint = (float(x) for x in section(s,r,kind,old,joint_factor))
    end,length,thick = fitting(kind,force(s,old)*joint_factor,r,area)
    out = dict(s_m=s,r_o_m=r,A_m2=area,nodes=v,members=members,
               m_tube_kg=tube,m_joint_kg=joint,m_end_kg=end,
               bond_or_insert_m=length,sleeve_t_m=thick,
               ends_per_node=2*members/v,m_joint_per_node_kg=joint/v)
    sc = score_row(s,r,area,k,old)
    if frozen:
        out.update(legal_at_frozen_radius=math.isfinite(sc["SF_least"]),
                   budget_kg=budget(s),versus_225_kg=joint/allowance,scores=sc)
    else:
        out.update(sc)
    out["mass_residual_kg"] = tube+joint+NODE_MASS*v+FILM_MASS+SYSTEMS-LIFT
    if kind != "percent5":
        out["nominal_joint_SF"] = joint_factor
        out["least_including_nominal_joint_SF"] = min(sc["SF_least"],joint_factor)
    return out


def optimise(kind,k,old=False,joint_factor=1.):
    best=None
    # Independent explicit grid, matching the resolution inferred from the
    # filed coordinates; every returned owner's point is also evaluated below.
    with np.errstate(divide="ignore",invalid="ignore"):
        for tick in range(10,151):
            s=tick/50
            radii=np.arange(1,4001)*min(.25,s/3)/4000
            area,_,_=section(s,radii,kind,old,joint_factor)
            least=scores(s,radii,area,k,old)[-1]
            index=int(np.argmax(least))
            if best is None or float(least[index])>best["SF_least"]:
                best=row(s,float(radii[index]),kind,k,old,joint_factor=joint_factor)
    return best


def pin(n):
    tau=.6*827e6
    diameter=math.sqrt(2*n/(PI*tau))
    length=3*diameter
    return dict(d_m=diameter,length_m=length,
                mass_kg=4430*PI*diameter**2*length/4,tau_Pa=tau)


def held(s,r,area,kind,allowance,old=False,n_override=None):
    n=force(s,old) if n_override is None else n_override
    v,m=counts(s)
    end,length,t=fitting(kind,n,r,area)
    pinrow=pin(n)
    wall=area/(PI*(r+math.sqrt(r*r-area/PI)))
    return dict(m_end_kg=end,bond_or_insert_m=length,sleeve_t_m=t,
                m_joint_kg=2*m*end,m_joint_per_node_kg=2*m*end/v,
                ends_per_node=2*m/v,versus_allowance=2*m*end/allowance,
                sigma_contact_Pa=n/area,SF_contact_on_3900=SIGMA/(n/area),
                SF_contact_on_flexure_380=380e6/(n/area),
                pin_kg=pinrow["mass_kg"],pin_d_m=pinrow["d_m"],
                pin_bearing_Pa=n/(2*wall*pinrow["d_m"]))


def compare(path, a, b, rows, missing):
    if isinstance(a,bool) or a is None:
        return
    if isinstance(a,(int,float)):
        if b is None:
            missing.append(path)
            return
        same=math.isclose(a,b,rel_tol=2e-10,abs_tol=3e-10)
        rows.append(dict(field=path,owner=a,check=b,difference=b-a,within_rounding=same))
    elif isinstance(a,dict):
        for key,value in a.items():
            compare(path+"."+key,value,b.get(key) if isinstance(b,dict) else None,rows,missing)
    elif isinstance(a,list):
        for i,value in enumerate(a):
            compare(path+f"[{i}]",value,b[i] if isinstance(b,list) and i<len(b) else None,rows,missing)


def main():
    started=datetime.now().astimezone().isoformat()
    owner=load("owner-RESULTS.json")
    up=load("mainline011b.json")
    for rec in load("upstream-pins.json"):
        path=ROOT/"inputs"/Path(rec["snapshot"]).name
        assert hashlib.sha256(path.read_bytes()).hexdigest()==rec["actual_sha256"]
    # Radius is the explicitly held published geometry, not an optimum taken
    # from the target algorithm. All other case numbers are recalculated.
    point=next(x for x in up["primary_joints_on"]["SiC-alpha-Hexoloy-SA"]
               if x["grid"]=="equilateral_triangular" and x["k"]==.2)
    assert point["r_o_m"]==owner["filed_011b_point"]["r_o_m"]
    s0,r0=2.04,point["r_o_m"]
    a0,tube0,joint0=section(s0,r0,"percent5")
    frozenbase=row(s0,r0,"percent5",frozen=True,allowance=joint0)
    sourcepoint={"s_m":s0,"r_o_m":r0,"A_m2":a0,"SF_least":frozenbase["scores"]["SF_global"],
                 "m_joint_kg":joint0,"m_tube_kg":tube0,
                 "nodes":counts(s0)[0],"members":counts(s0)[1],"k":.2}
    coeff={k:{"C_end_kg_m_per_N2":v} for k,v in CS.items()}
    coeff["sic_braze"]={"C_end_per_area_1_per_N":CB}
    reproduced=dict(member_force_N={"s_2.04_equilateral":force(s0),
                                   "s_2.04_twoway":force(s0,True)},
                    mass_coefficients=coeff,filed_011b_point=sourcepoint,
                    pin_clevis_reference=pin(force(s0)),
                    pin_through_wall_bearing_Pa=held(s0,r0,a0,"ti_sleeve",joint0)["pin_bearing_Pa"],
                    cfrp_allowable_Pa={"compression":1470e6,"tensile_not_used":2550e6})
    reproduced["regression_percent5"]={}
    optimums={}
    for label,old,k in [("equilateral_k0.2",False,.2),("equilateral_k0.4",False,.4),("twoway_k0.2",True,.2)]:
        target=owner["regression_percent5"][label]
        reproduced["regression_percent5"][label]=row(target["s_m"],target["r_o_m"],"percent5",k,old)
        optimums["percent5_"+label]=optimise("percent5",k,old)
    reproduced["regression_percent5"]["frozen_equilateral"]=frozenbase
    reproduced["checks"]=[
        {"got":force(s0)},
        {"got":force(s0,True)/force(s0)},
        {"got_s":optimums["percent5_twoway_k0.2"]["s_m"],
         "got_sf":optimums["percent5_twoway_k0.2"]["SF_least"]},
        {"got":frozenbase["scores"]["SF_least"]},
    ]
    reproduced["joints"]={}
    old_rows={}
    for kind in ("ti_sleeve","invar_sleeve","sic_braze","cfrp_wrap"):
        reproduced["joints"][kind]={"frozen_k0.2":row(s0,r0,kind,frozen=True,allowance=joint0)}
        old_rows[kind]={"frozen_k0.2":row(s0,r0,kind,old=True,frozen=True,allowance=joint0)}
        for k in (.2,.4):
            label="reopt_k"+str(k)
            target=owner["joints"][kind][label]
            reproduced["joints"][kind][label]=row(target["s_m"],target["r_o_m"],kind,k)
            optimums[kind+"_"+str(k)]=optimise(kind,k)
            old_rows[kind][label]=optimise(kind,k,old=True)
    reproduced["scale_at_held_section"]=[]
    for target in owner["scale_at_held_section"]:
        s=target["s_m"];v,m=counts(s)
        reproduced["scale_at_held_section"].append(dict(
            s_m=s,N_N=force(s),nodes=v,members=m,ends_per_node=2*m/v,
            r_o_held_m=r0,A_held_m2=a0,
            kinds={kind:held(s,r0,a0,kind,joint0) for kind in CS.keys()|{"sic_braze"}}))
    comp,missing=[],[]
    for name,value in reproduced.items():
        compare(name,owner[name],value,comp,missing)
    # Original report's 022 numbers used its filed arch thrust. Preserve that
    # scenario separately from the physically corrected equilateral force.
    p22=load("mainline022.json")["carried_011b_k02"]["equilateral"]
    old22={kind:held(p22["s_m"],p22["r_o_m"],p22["A_m2"],kind,p22["m_joint_kg"],
                    n_override=p22["N_N"]) for kind in CS.keys()|{"sic_braze"}}
    new22={kind:held(p22["s_m"],p22["r_o_m"],p22["A_m2"],kind,p22["m_joint_kg"])
           for kind in CS.keys()|{"sic_braze"}}
    n=force(s0);v,m=counts(s0)
    area_bond=n/TAU_BOND
    supplements={
        "equilibrium_force_derivations":{
            "global_cut":P*R*s0/(2*math.sqrt(3)),
            "sixfold_node":P*(math.sqrt(3)/2)*s0*s0/(6*s0/(2*R)),
            "tributary_arch":(P*s0/(2*math.sqrt(3)))*s0*s0/(8*(s0*s0/(8*R)))},
        "pressure_load_sixfold_node_N":P*math.sqrt(3)/2*s0*s0,
        "joint_stiffness_or_hub_mass_sized":False,
        "braze_coefficient_correct_units":"kg/(N*m) = s^2/m^2, not 1/N",
        "bond_area_one_end_m2":area_bond,
        "adhesive_total_per_100um_gap_kg":2*m*area_bond*.0001*1360,
        "adhesive_gap_is_design_assumption":True,
        "pin_length_3d_m":pin(n)["length_m"],
        "tube_outer_diameter_m":2*r0,
        "pin_mass_at_minimum_2r_span_kg":pin(n)["mass_kg"]*2*r0/pin(n)["length_m"],
        "tube_arc_length_m":2*R*math.asin(s0/(2*R)),
        "tube_arc_over_chord":2*R*math.asin(s0/(2*R))/s0,
        "omitted_arc_tube_mass_at_filed_section_kg":tube0*(2*R*math.asin(s0/(2*R))/s0-1),
        "old_pin":pin(force(s0,True)),
        "old_held":{kind:held(s0,r0,a0,kind,joint0,old=True) for kind in CS.keys()|{"sic_braze"}},
        "new_held":{kind:held(s0,r0,a0,kind,joint0) for kind in CS.keys()|{"sic_braze"}},
        "022_original_force_N":p22["N_N"],"022_corrected_equilibrium_force_N":force(p22["s_m"]),
        "022_original_report_joint_masses":old22,"022_corrected_held_section_joint_masses":new22}
    invariance=[x["kinds"]["ti_sleeve"]["m_joint_kg"] for x in reproduced["scale_at_held_section"]]
    largest_residual=max(abs(x["mass_residual_kg"]) for x in optimums.values())
    mode_scaling={key:frozenbase["scores"]["SF_"+key]/score_row(s0,r0,a0,.2,True)["SF_"+key]
                  for key in MODES}
    verifications={
        "numeric_fields_compared":len(comp),"outside_rounding":sum(not x["within_rounding"] for x in comp),
        "missing_numeric_paths":missing,"largest_mass_closure_residual_kg":largest_residual,
        "constant_sleeve_total_range_kg":max(invariance)-min(invariance),
        "fixed_geometry_force_factor_scaling":mode_scaling,
        "all_three_force_derivations_agree":max(supplements["equilibrium_force_derivations"].values())
                                             -min(supplements["equilibrium_force_derivations"].values())<1e-8,
        "all_optima_at_least_filed_objective":all(
            optimums[kind+"_"+str(k)]["SF_least"]+1e-10>=owner["joints"][kind]["reopt_k"+str(k)]["SF_least"]
            for kind in reproduced["joints"] for k in (.2,.4))}
    assert largest_residual<1e-8
    assert verifications["all_three_force_derivations_agree"]
    assert verifications["all_optima_at_least_filed_objective"]
    result=dict(schema=1,unit="vacuum-mainline023-check-1020",certification=False,
                tag="QUESTIONABLE arithmetic/model; fabricated joints and film PROJECTION",
                started_at=json.loads((ROOT/"WORK.json").read_text())["started_at"],
                compute_started_at=started,compute_ended_at=datetime.now().astimezone().isoformat(),
                owner_scripts_read_or_executed=False,case=dict(R_m=R,p_Pa=P,lift_kg=LIFT,
                film_kg=FILM_MASS,systems_kg=SYSTEMS,node_point_kg=NODE_MASS),
                corrected_reproduction=reproduced,independent_optima=optimums,
                original_force_reconstruction=old_rows,supplements=supplements,
                numeric_comparisons=comp,verification=verifications)
    (ROOT/"RESULTS.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    with (ROOT/"NUMERIC-CHECK.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(comp[0]));writer.writeheader();writer.writerows(comp)
    print(json.dumps(verifications,indent=2))
    print("NEW OPTIMA",json.dumps({k:{a:v[a] for a in ("s_m","r_o_m","SF_least","governing")}
                                  for k,v in optimums.items()},indent=2))
    print("OLD OPTIMA",json.dumps({k:{a:b["SF_least"] for a,b in v.items() if "SF_least" in b}
                                  for k,v in old_rows.items()},indent=2))


if __name__=="__main__":
    main()
