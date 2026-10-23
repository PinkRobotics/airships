"""041 fixed-demand material/section comparison, with optional fresh FE validation."""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
from material_models import models

ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/"intake/041/RESULTS.json").read_text())["best_closure_by_reserve"]
TAG="QUESTIONABLE / PROJECTION"

def section(ro,wall):
    ri=ro-wall
    return math.pi*(ro*ro-ri*ri), math.pi*(ro**4-ri**4)/4

def comp_root(a,b,e,S):
    d=a+b+S/e
    return 2*S/(d+np.sqrt(d*d-4*a*S/e))

def load_data(reserve):
    path=ROOT/f"intake/check041/runs/f5-{reserve}-m24"
    with np.load(path/"STATIC.npz") as ar:d={k:ar[k].copy() for k in ar.files}
    geo=json.loads((path/"RESULTS.json").read_text())["geometry"]
    return d,np.asarray(geo["member_arc_lengths_m"]),geo

def score(mat,ref,d,length,ro,wall,global_lambda=None):
    A,I=section(ro,wall)
    N=d["subelement_N"];M=d["subelement_M"];ids=d["subelement_member"]
    L=length[ids]
    euler=math.pi**2*mat["Eax_Pa"]*I/(L*L*N)
    aa=N/A;bb=(M+N*L/1000)*ro/I
    gamma=.099+.901*math.exp(-math.sqrt(ro/wall)/16)
    local=gamma*mat["local_classical_coefficient_Pa"]*wall/ro
    # The legacy local expression is retained as a separate isotropic sensitivity.
    legacy_local=gamma*.6*mat["Eax_Pa"]*wall/ro
    lam=global_lambda if global_lambda is not None else ref["modes"]["global_perfect_linear"]*(mat["Eax_Pa"]/410e9)*(I/ref["section"]["inertia_m4"])
    modes=dict(euler=float(euler.min()),local_axial=float(np.min(local/aa)),
        local_peak=float(np.min(comp_root(aa,bb,euler,local))),
        global_k0p2=.2*lam,film=ref["modes"]["film"],joint=ref["least_screened_SF"])
    Xc=mat["screen_compression_Pa"]
    modes["compression"]=None if Xc is None else float(np.min(comp_root(aa,bb,euler,Xc)))
    upper=min(v for k,v in modes.items() if v is not None and k!="local_axial")
    q=min(upper,.999999*float(euler.min()))
    peak1=None;required=None;ratio=None;mp=None;pf=None
    if euler.min()>1:
        seg=aa+bb/(1-1/euler)
        stress=np.full(750,-np.inf);np.maximum.at(stress,ids,seg)
        peak1=float(stress.max())
        required=math.exp((logsumexp(10*np.log(stress/1e9))-math.log(-math.log1p(-.001)))/10)*1e9
        if Xc is not None and mat["id"]!="Al6061T6":
            ratio=required/Xc
            hazard=float(np.exp(10*np.log(stress/Xc)).sum())
            pf=-math.expm1(-hazard)
            if Xc>stress.max():
                logs=np.log(stress/Xc)
                # Analytic upper bracket: n*max(ratio)^m <= target hazard.
                # An arbitrary m=5000 ceiling fails as peak stress approaches Xc.
                target=math.log(-math.log1p(-.001))
                hi=1.01*(math.log(len(stress))-target)/(-float(logs.max()))
                mp=brentq(lambda m:logsumexp(m*logs)-target,.001,hi)
    tube=mat["density_kgm3"]*A*length.sum()
    non=ref["mass_kg"]["total_with_reserve_and_sag"]-ref["mass_kg"]["tube"]
    return dict(tag=TAG,material=mat["id"],reserve=ref["reserve"],ro_m=ro,wall_m=wall,
        area_m2=A,inertia_m4=I,frame_tubes_kg=float(tube),frame_plus_joints_nodes_kg=float(tube+ref["mass_kg"]["joint"]+ref["mass_kg"]["nodes"]),
        total_mass_including_reserve_sag_kg=float(tube+non),lift_headroom_kg=float(4889.44215019-tube-non),
        mass_closure=bool(tube+non<=4889.44215019+1e-6),modes=modes,
        conditional_SF_or_ceiling=upper,
        strength_unknown=Xc is None,
        modes_incomplete=mat["kind"]=="composite",
        global_method="fresh FE" if global_lambda is not None else "fixed-demand EI scaling; GJ ratio not preserved",
        qualified_structural_SF=None,qualified_frame_Pf=None,
        legacy_isotropic_local_axial=float(np.min(legacy_local/aa)),
        legacy_isotropic_local_peak=float(np.min(comp_root(aa,bb,euler,legacy_local))),
        q1_peak_compression_Pa=peak1,
        q1_whole_member_scale_needed_m10_Pf1e3_Pa=required,
        hypothetical_m10_strength_multiplier_over_typical=ratio,
        hypothetical_m_needed_if_typical_is_whole_member_scale=mp,
        hypothetical_m10_Pf_if_typical_is_whole_member_scale=pf)

def main():
    mats=models()
    (ROOT/"MATERIAL-MODELS.json").write_text(json.dumps(mats,indent=2)+"\n")
    results=[]
    checks=[]
    for reserve in ["5","019"]:
        ref=BASE[reserve];d,length,geo=load_data(reserve)
        for mat in mats:
            ro=ref["section"]["r_o_m"];original=ref["section"]["wall_m"]
            area_budget=ref["mass_kg"]["tube"]/(mat["density_kgm3"]*length.sum())
            masswall=ro-math.sqrt(ro*ro-area_budget/math.pi)
            for name,wall in [("same_section",original),("same_tube_mass",masswall)]:
                ans=score(mat,ref,d,length,ro,wall);ans["section_policy"]=name;results.append(ans)
            # Minimum thickness meeting q=1 deterministic screen, at unchanged OD.
            # This is a lower bound when strength or additional modes are missing.
            def residual(w):
                return score(mat,ref,d,length,ro,w)["conditional_SF_or_ceiling"]-1
            if residual(.02)>0:
                w=brentq(residual,.0001,.02,xtol=1e-12)
                ans=score(mat,ref,d,length,ro,w);ans["section_policy"]="minimum_wall_q1_screen";results.append(ans)
            else:
                results.append(dict(tag=TAG,material=mat["id"],reserve=reserve,section_policy="minimum_wall_q1_screen",solution=None))
        old=next(x for x in results if x.get("reserve")==reserve and x.get("material")=="041-reference" and x.get("section_policy")=="same_section")
        for key,actual,expected in [("tube_mass",old["frame_tubes_kg"],ref["mass_kg"]["tube"]),("legacy_local",old["legacy_isotropic_local_axial"],ref["modes"]["local_axial"]),("peak_q1",old["q1_peak_compression_Pa"],float(max(float(x["peak_compression_Pa"]) for x in csv.DictReader((ROOT/f"intake/043-fold/MEMBERS-f5-{reserve}-operating.csv").open()))))]:
            ok=bool(abs(actual-expected)<1e-7*abs(expected)+1e-7)
            checks.append(dict(reserve=reserve,field=key,actual=actual,expected=expected,passed=ok))
            assert ok
    (ROOT/"FRAME-COMPARE.json").write_text(json.dumps(dict(tag=TAG,rows=results,checks=checks),indent=2)+"\n")
    flat=[]
    for x in results:
        y={k:v for k,v in x.items() if not isinstance(v,dict)}
        y.update({"SF_"+k:v for k,v in x.get("modes",{}).items()});flat.append(y)
    fields=list(dict.fromkeys(k for x in flat for k in x))
    with (ROOT/"FRAME-COMPARE.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(flat)
    print(json.dumps(dict(models=len(mats),rows=len(results),checks=checks),indent=2))

if __name__=="__main__":main()
