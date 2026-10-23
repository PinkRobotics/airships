import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
mats=materials();rows=[]
for i,row in enumerate(read("FRAME-COMPARE.json")["rows"]):
    if row["material"]!="M55J-50-20-20-10" or row["section_policy"]!="minimum_wall_q1_screen":continue
    mat=mats[row["material"]];res=row["reserve"];_,arr,_=base_data(res)
    tests=[]
    for perturb in [-1e-8,0.,1e-8]:
        t=row["wall_m"]*(1+perturb)
        ss,_=peak(arr,mat,row["ro_m"],t,1)
        s0=mat["screen_compression_Pa"]
        tests.append(dict(relative_wall_change=perturb,peak_over_scale=float(ss.max()/s0),
             m_needed=shape_needed(ss,s0,.001),required_scale_m10_Pa=scale(ss,10,.001)))
    rows.append(dict(frame_row=i,material=row["material"],reserve=res,owner_m=row["hypothetical_m_needed_if_typical_is_whole_member_scale"],tests=tests))
joints=[]
for res in ["5","019"]:
    label=f"K13D2U-50-20-20-10-{res}-same_tube_mass-m6-intact"
    x=json.loads((ROOT/"fe"/(label+".json")).read_text())
    modes=x["modes"].copy();modes["joint_sleeve"]*=1450/1470
    joints.append(dict(reserve=res,legacy_sleeve_strength_MPa=1470,
        alternative_T700S_sheet_strength_MPa=1450,original_screen=x["conditional_SF_or_ceiling"],
        alternative_screen_or_ceiling=min(v for v in modes.values() if v is not None),
        status="Sensitivity only: matching sleeve construction and allowable remain unqualified"))
dump("SENSITIVITIES.json",dict(ill_conditioned_m=rows,joint_reference_sensitivity=joints))
print(json.dumps(dict(ill_conditioned_m=rows,joint_reference_sensitivity=joints),indent=1))
