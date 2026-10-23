import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
mats=materials();audit=Audit();cache={};outputs=[]
ferows=read("FE-ALL.json")["rows"]
designs={(v["material"],v["reserve"],v["section_policy"]):v for v in read("FRAME-COMPARE.json")["rows"]}
def load_case(matname,res,policy):
    key=matname,res,policy
    if key not in cache:
        mat=mats[matname]
        if policy=="same_section":
            ref=designs[key];ro=ref["ro_m"];t=ref["wall_m"]
            _,arr,_=base_data(res);calc=fixed_score(res,mat,ro,t)
        else:
            label=f"{matname}-{res}-{policy}-m6-intact"
            ref=next(v for v in ferows if v["label"]==label)
            ro=ref["radius_m"];t=ref["wall_m"]
            calc=json.loads((ROOT/"fe"/(label+".json")).read_text())
            ar=np.load(ROOT/"fe"/(label+".npz"),allow_pickle=False);arr={k:ar[k] for k in ar.files}
        cache[key]=ro,t,calc,arr
    return cache[key]

for i,row in enumerate(read("GAPS.json")["rows"]):
    mat=mats[row["material"]];res=row["reserve"];policy=row["section_policy"]
    ro,t,case,arr=load_case(mat["id"],res,policy);A,I=section(ro,t)
    q=1. if row["load_case"]=="operating" else case["conditional_SF_or_ceiling"]
    ss,ten=peak(arr,mat,ro,t,q)
    s0=mat["screen_compression_Pa"]
    reliable_s0=s0 if mat["id"]!="Al6061T6" else None
    calc=dict(q=q,frame_tubes_kg=case["frame_tubes_kg"],
       total_mass_kg=case["total_mass_including_reserve_sag_kg"],
       conditional_mechanical_SF_or_ceiling=case["conditional_SF_or_ceiling"],modes=case["modes"],
       assumed_typical_as_whole_member_scale_Pa=s0,euler_stable_at_this_q=ss is not None,
       peak_Pa=None if ss is None else float(ss.max()))
    if ss is not None:
        mneeded=None if reliable_s0 is None else shape_needed(ss,reliable_s0,.001)
        calc.update(hypothetical_Pf_m10_if_typical_is_member_scale=None if reliable_s0 is None else probability(ss,10,reliable_s0),
          hypothetical_m_needed_for_Pf1e3=mneeded,m_factor_over_assumed10=None if mneeded is None else mneeded/10,
          no_finite_m_at_assumed_scale=None if reliable_s0 is None else bool(ss.max()>=reliable_s0))
        loc=(.099+.901*math.exp(-math.sqrt(ro/t)/16))*mat["local_classical_coefficient_Pa"]*t/ro
        calc.update(local_shell_coefficient_factor_at_fixed_demands=float(ss.max()/loc),
          compression_strength_factor_for_deterministic_q1=None if s0 is None else float(ss.max()/s0),
          global_knockdown_or_eigenvalue_factor_for_q1=1/case["modes"]["global_k0p2"])
        for j,target in enumerate(row.get("targets",[])):
            m,pf=target["m"],target["Pf"]
            whole=scale(ss,m,pf)
            cur=dict(whole_member_scale_needed_Pa=whole,
               common_3m_scale_needed_Pa=scale(ss,m,pf,arr["L"]/3),
               coupon_1cm3_scale_needed_Pa=scale(ss,m,pf,A*arr["L"]/1e-6),
               whole_member_strength_factor_over_typical=None if s0 is None else whole/s0,
               coupon_to_3m_retention=(A*3/1e-6)**(-1/m))
            audit.fields(f"gap[{i}]/target[{j}]",target,cur,rtol=3e-6,atol=1e-7)
    if "hypothetical_reliability_q_Pf1e3_m10" in row:
        def h(q):
            ss,_=peak(arr,mat,ro,t,q)
            return math.log(scale(ss,10,.001)/s0)
        _,_,e=demands(arr,mat,ro,t)
        qr=brentq(h,1e-8,float(e.min())*(1-1e-8),xtol=1e-12)
        calc.update(hypothetical_reliability_q_Pf1e3_m10=qr,
                    joint_mechanical_and_hypothetical_reliability_q=min(qr,case["conditional_SF_or_ceiling"]))
    audit.fields(f"gap[{i}]/{mat['id']}/{res}/{policy}/{row['load_case']}",row,calc,rtol=3e-6,atol=1e-7)
    outputs.append(dict(index=i,**calc))

for i,row in enumerate(read("WITNESSES.json")["rows"]):
    ref=row["FE"];label=ref["label"];calc=json.loads((ROOT/"fe"/(label+".json")).read_text())
    audit.fields(f"witness[{i}]/{label}",ref,{k:v for k,v in calc.items() if k not in
       ["eigen_relative_residuals","equilibrium_relative_residual","load_rigid_projection_ratio","individual_secondary_failure_members_at_q1","merged_bay"]},rtol=3e-6,atol=1e-7)
    audit.check(f"witness[{i}]","q1_screen_pass",True,calc["conditional_SF_or_ceiling"]>=1-1e-7)
    geo=row["comparison_geometry"]
    own=fixed_score(row["reserve"],mats[row["material"]],ref["radius_m"],ref["wall_m"])
    # comparison_geometry retains fixed-force stress fields but substitutes the fresh global eigenvalue.
    own["modes"]["global_k0p2"]=calc["modes"]["global_k0p2"]
    own["conditional_SF_or_ceiling"]=min(v for v in own["modes"].values() if v is not None)
    audit.fields(f"witness[{i}]/comparison_geometry",geo,own,rtol=3e-6,atol=1e-7)

for i,row in enumerate(read("DAMAGE.json")["rows"]):
    mat,res,edge=row["material"],row["reserve"],row["removed_member"]
    label=f"{mat}-{res}-same_tube_mass-m6-lost{edge}"
    calc=json.loads((ROOT/"fe"/(label+".json")).read_text())
    _,_,intact,_=load_case(mat,res,"same_tube_mass")
    peakratio=None if calc["q1_peak_compression_Pa"] is None or intact["q1_peak_compression_Pa"] is None else calc["q1_peak_compression_Pa"]/intact["q1_peak_compression_Pa"]
    cur=dict(conditional_SF_or_ceiling=calc["conditional_SF_or_ceiling"],modes=calc["modes"],
      compression_amplification=peakratio,
      axial_amplification=calc["max_axial_N"]/intact["max_axial_N"],
      bending_amplification=calc["max_bending_Nm"]/intact["max_bending_Nm"],
      q1_peak_compression_Pa=calc["q1_peak_compression_Pa"],q1_peak_tension_Pa=calc["q1_peak_tension_Pa"],
      conditional_second_failure_trigger=calc["conditional_SF_or_ceiling"]<1,
      failure_member_counts={k:None if v is None else len(v) for k,v in calc["individual_secondary_failure_members_at_q1"].items()},
      merged_bay=calc["merged_bay"],proven_dynamic_cascade=None)
    audit.fields(f"damage[{i}]/{label}",row,cur,rtol=3e-6,atol=1e-7)
dump("INDEPENDENT-GAPS.json",outputs)
audit.save("GAPS-WITNESSES-DAMAGE-CHECK.json")
