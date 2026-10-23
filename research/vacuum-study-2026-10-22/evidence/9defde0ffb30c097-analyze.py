"""Consolidate completed calculations and evaluate explicit material gaps."""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from material_models import models
from frame_compare import BASE,load_data,section

ROOT=Path(__file__).resolve().parent
TAG="QUESTIONABLE / PROJECTION"

def dump(name,x):
    (ROOT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")

def needed_m(stress,scale,pf):
    if scale is None or max(stress)>=scale:return None
    logs=np.log(stress/scale);target=math.log(-math.log1p(-pf))
    hi=1.01*(math.log(len(stress))-target)/(-float(logs.max()))
    return float(brentq(lambda m:logsumexp(m*logs)-target,.001,hi))

def stress_for_q(mat,row,d,L,q):
    ro=row["ro_m"];A,I=section(ro,row["wall_m"])
    N=d["subelement_N"];M=d["subelement_M"];ids=d["subelement_member"]
    e=math.pi**2*mat["Eax_Pa"]*I/(L[ids]**2*N)
    if np.min(e)<=q:return None
    s=q*N/A+q*(M+N*L[ids]/1000)*ro/I/(1-q/e)
    peak=np.zeros(750);np.maximum.at(peak,ids,s)
    return peak

def main():
    mats={m["id"]:m for m in models()}
    dump("MATERIAL-MODELS.json",list(mats.values()))
    comparison=json.loads((ROOT/"FRAME-COMPARE.json").read_text())["rows"]
    if (ROOT/"WITNESSES.json").exists():
        comparison += [x["comparison_geometry"] for x in json.loads((ROOT/"WITNESSES.json").read_text())["rows"]
                       if x["FE"]["section_policy"]!="minimum_wall_q1_screen"]
    fe=[]
    for p in sorted((ROOT/"runs").glob("*/RESULTS.json")):
        fe.append(json.loads(p.read_text()))
    basefe={(x["material"],x["reserve"],x["section_policy"]):x for x in fe if x["segments"]==6 and x["removed_member"] is None}
    gaps=[];checks=[]
    for row in comparison:
        if "wall_m" not in row:continue
        mat=mats[row["material"]];old,L,geo=load_data(row["reserve"])
        fresh=basefe.get((row["material"],row["reserve"],row["section_policy"]))
        d=old;basis="041 fixed pressure forces; EI-scaled eigenvalue"
        if fresh:
            with np.load(ROOT/"runs"/fresh["label"]/"STATIC.npz") as z:
                d={k:z[k].copy() for k in z.files if k in ["subelement_N","subelement_M","subelement_member"]}
            basis="fresh 6-segment/member FE; independent axial and torsional moduli"
        sf=fresh["conditional_SF_or_ceiling"] if fresh else row["conditional_SF_or_ceiling"]
        modes=fresh["modes"] if fresh else row["modes"]
        X=mat["screen_compression_Pa"]
        for load,q in [("operating",1.),("mechanical_screen",sf)]:
            stress=stress_for_q(mat,row,d,L,q)
            data=dict(tag=TAG,material=mat["id"],reserve=row["reserve"],section_policy=row["section_policy"],
                load_case=load,q=q,force_basis=basis,frame_tubes_kg=row["frame_tubes_kg"],
                total_mass_kg=row["total_mass_including_reserve_sag_kg"],
                conditional_mechanical_SF_or_ceiling=sf,modes=modes,
                assumed_typical_as_whole_member_scale_Pa=X,
                assumption_is_measured_distribution=False,
                qualified_reliability=None,qualified_SF=None,euler_stable_at_this_q=stress is not None)
            if stress is not None:
                targets=[]
                A,_=section(row["ro_m"],row["wall_m"])
                for m in [5,8,10,11,15,20,30,40]:
                    for pf in [.001,1e-6]:
                        hazard=-math.log1p(-pf)
                        def scale(weights):
                            return float(np.exp((logsumexp(m*np.log(stress/1e9)+np.log(weights))-math.log(hazard))/m)*1e9)
                        req=scale(np.ones(750))
                        targets.append(dict(m=m,Pf=pf,whole_member_scale_needed_Pa=req,
                            common_3m_scale_needed_Pa=scale(L/3),
                            coupon_1cm3_scale_needed_Pa=scale(A*L/1e-6),
                            whole_member_strength_factor_over_typical=None if X is None else req/X,
                            coupon_to_3m_retention=(3*A/1e-6)**(-1/m)))
                data["peak_Pa"]=float(max(stress));data["targets"]=targets
                if X is not None and mat["id"]!="Al6061T6":
                    H=float(np.exp(10*np.log(stress/X)).sum())
                    data["hypothetical_Pf_m10_if_typical_is_member_scale"]=-math.expm1(-H)
                    mneed=needed_m(stress,X,.001)
                    data["hypothetical_m_needed_for_Pf1e3"]=mneed
                    data["m_factor_over_assumed10"]=None if mneed is None else mneed/10
                    data["no_finite_m_at_assumed_scale"]=bool(max(stress)>=X)
                else:
                    data["hypothetical_Pf_m10_if_typical_is_member_scale"]=None
                    data["hypothetical_m_needed_for_Pf1e3"]=None
                    data["m_factor_over_assumed10"]=None
                    data["no_finite_m_at_assumed_scale"]=None
                if load=="operating":
                    gamma=.099+.901*math.exp(-math.sqrt(row["ro_m"]/row["wall_m"])/16)
                    local=gamma*mat["local_classical_coefficient_Pa"]*row["wall_m"]/row["ro_m"]
                    data["local_shell_coefficient_factor_at_fixed_demands"]=float(max(stress)/local)
                    data["compression_strength_factor_for_deterministic_q1"]=None if X is None else float(max(stress)/X)
                    data["global_knockdown_or_eigenvalue_factor_for_q1"]=1/modes["global_k0p2"]
            else:
                data["targets"]=[];data["peak_Pa"]=None
                data["unavailable_reason"]="Euler instability at this pressure; strength alone cannot give a finite amplified stress"
            gaps.append(data)
        if X is not None and mat["id"]!="Al6061T6":
            # Maximum q satisfying the illustrative m10 / typical-as-scale Pf.
            upper=.999999*modes["euler"]
            def r(q):
                s=stress_for_q(mat,row,d,L,q)
                return logsumexp(10*np.log(np.maximum(s,1e-200)/X))-math.log(-math.log1p(-.001))
            qrel=float(brentq(r,1e-8,upper,xtol=1e-12))
            gaps[-2]["hypothetical_reliability_q_Pf1e3_m10"]=qrel
            gaps[-2]["joint_mechanical_and_hypothetical_reliability_q"]=min(qrel,sf)
    damage=[]
    for x in fe:
        if x["segments"]!=6 or x["section_policy"]!="same_tube_mass" or x["removed_member"] is None:continue
        intact=basefe[(x["material"],x["reserve"],x["section_policy"])]
        comp0=intact["q1_peak_compression_Pa"];comp=x["q1_peak_compression_Pa"]
        damage.append(dict(tag=TAG,material=x["material"],reserve=x["reserve"],removed_member=x["removed_member"],
            conditional_SF_or_ceiling=x["conditional_SF_or_ceiling"],modes=x["modes"],
            compression_amplification=None if comp is None or comp0 is None else comp/comp0,
            axial_amplification=x["max_axial_N"]/intact["max_axial_N"],
            bending_amplification=x["max_bending_Nm"]/intact["max_bending_Nm"],
            q1_peak_compression_Pa=comp,q1_peak_tension_Pa=x["q1_peak_tension_Pa"],
            conditional_second_failure_trigger=x["secondary_failure_trigger_at_q1"],
            failure_member_counts={k:None if v is None else len(v) for k,v in x["individual_secondary_failure_members_at_q1"].items()},
            projected_cascade="secondary overload / collapse trigger; progression not simulated",
            proven_dynamic_cascade=None,merged_bay=x["merged_bay"]))
    for x in fe:
        for name,value,limit in [("equilibrium",x["equilibrium_relative_residual"],2e-6),
                                 ("load balance",x["load_rigid_projection_ratio"],1e-12),
                                 ("eigen residual",max(x["eigen_relative_residuals"]),2e-6)]:
            checks.append(dict(name=name,label=x["label"],value=value,limit=limit,passed=value<limit))
    for x in fe:
        if x["segments"]==12:
            coarse=next(y for y in fe if all(y[k]==x[k] for k in [
                "material","reserve","section_policy","removed_member"]) and y["segments"]==6)
            for key in ["conditional_SF_or_ceiling","q1_peak_compression_Pa"]:
                a,b=x[key],coarse[key]
                if a is not None and b is not None:
                    err=abs(b/a-1)
                    checks.append(dict(name="m6/m12 "+key,label=x["label"],
                        relative_error=err,passed=err<.01))
    # Baseline m6 against independent m24 CHECK-041 data.
    for reserve in ["5","019"]:
        x=basefe[("041-reference",reserve,"same_tube_mass")]
        lam24=BASE[reserve]["modes"]["global_perfect_linear"]
        err=x["linear_multipliers"][0]/lam24-1
        checks.append(dict(name="reference eigen m6/m24",reserve=reserve,relative_error=err,passed=abs(err)<.001))
    assert len([x for x in fe if x["segments"]==6 and x["section_policy"]=="same_tube_mass"])==108
    assert len(damage)==72
    assert all(c["passed"] for c in checks),[c for c in checks if not c["passed"]]
    dump("GAPS.json",dict(tag=TAG,rows=gaps))
    dump("DAMAGE.json",dict(tag=TAG,rows=damage))
    dump("FE-CHECKS.json",dict(checks=checks,passed=sum(c["passed"] for c in checks),failed=sum(not c["passed"] for c in checks)))
    dump("FE-ALL.json",dict(rows=fe))
    flat=[]
    for x in gaps:
        if x["load_case"]!="operating":continue
        target=next((y for y in x["targets"] if y["m"]==10 and y["Pf"]==.001),{})
        flat.append(dict(material=x["material"],reserve=x["reserve"],section_policy=x["section_policy"],
            tubes_kg=x["frame_tubes_kg"],total_kg=x["total_mass_kg"],
            SF_or_ceiling=x["conditional_mechanical_SF_or_ceiling"],
            target_whole_scale_GPa=(target.get("whole_member_scale_needed_Pa") or 0)/1e9 if target else None,
            strength_factor_over_typical=target.get("whole_member_strength_factor_over_typical"),
            m_needed=x.get("hypothetical_m_needed_for_Pf1e3"),
            hypothetical_Pf=x.get("hypothetical_Pf_m10_if_typical_is_member_scale"),
            force_basis=x["force_basis"]))
    with (ROOT/"GAPS.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    labels=[m for m in mats if m!="041-reference"]
    fig,axes=plt.subplots(1,2,figsize=(14,9),layout="constrained")
    for j,reserve in enumerate(["5","019"]):
        xx=[next(r for r in flat if r["material"]==m and r["reserve"]==reserve and r["section_policy"]=="same_tube_mass") for m in labels]
        axes[0].scatter([r["SF_or_ceiling"] for r in xx],np.arange(len(labels))+(j-.5)*.18,label="5% reserve" if j==0 else "019 reserve",s=35)
        axes[1].scatter([r["target_whole_scale_GPa"] for r in xx],np.arange(len(labels))+(j-.5)*.18,s=35)
    axes[0].axvline(1,color="black",ls="--",lw=1);axes[0].legend(loc="lower right")
    axes[0].set_yticks(np.arange(len(labels)),labels);axes[0].invert_yaxis()
    axes[1].set_yticks(np.arange(len(labels)),[""]*len(labels));axes[1].invert_yaxis()
    axes[0].set_xlabel("Conditional mechanical SF or ceiling\nSame tube mass, fixed OD; fresh FE + projected wall/joint screens")
    axes[1].set_xlabel("Required whole-member compression scale, GPa\nm=10; frame Pf=0.001; operating q=1")
    for ax in axes:ax.grid(axis="x",alpha=.25)
    fig.suptitle("QUESTIONABLE / PROJECTION — no candidate has a measured complete-tube compression fit")
    fig.savefig(ROOT/"MATERIAL-COMPARISON.png",dpi=160)
    fig.savefig(ROOT/"MATERIAL-COMPARISON.pdf")
    print(json.dumps(dict(gap_rows=len(gaps),damage_rows=len(damage),FE_runs=len(fe),checks=len(checks))))

if __name__=="__main__":main()
