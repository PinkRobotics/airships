"""Check published decimal displays and the preserved first report's numbers."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import csv
import json
import math
import check

ROOT = Path(__file__).resolve().parent
r=json.loads((ROOT/"RESULTS.json").read_text())
o=json.loads((ROOT/"inputs/owner-RESULTS.json").read_text())
c=r["corrected_reproduction"]
sup=r["supplements"]
audit=[]


def add(label,published,value,scenario):
    target=Decimal(str(published))
    rounded=Decimal(str(value)).quantize(Decimal(1).scaleb(target.as_tuple().exponent),
                                        rounding=ROUND_HALF_UP)
    ok=(rounded==target or math.isclose(float(target),value,rel_tol=2e-10,abs_tol=3e-10))
    audit.append(dict(scenario=scenario,field=label,reported=str(published),
                      independently_derived=value,rounded=str(rounded),pass_check=ok))


def walk(expected,actual,prefix="display"):
    if isinstance(expected,dict):
        for key,value in expected.items():walk(value,actual[key],prefix+"."+key)
    elif isinstance(expected,list):
        for i,value in enumerate(expected):walk(value,actual[i],prefix+f"[{i}]")
    elif isinstance(expected,str):
        try:float(expected)
        except ValueError:
            assert expected==actual,(prefix,expected,actual)
        else:add(prefix,expected,actual,"corrected filing")


s0,r0,a0=(c["filed_011b_point"][key] for key in ["s_m","r_o_m","A_m2"])
held=sup["new_held"]["ti_sleeve"]
d=dict(N_kN=check.force(s0)/1000,N_twoway_kN=check.force(s0,True)/1000,
       pin_kg=c["pin_clevis_reference"]["mass_kg"],
       pin_d_mm=c["pin_clevis_reference"]["d_m"]*1000,
       bearing_GPa=c["pin_through_wall_bearing_Pa"]/1e9,
       wall_MPa=held["sigma_contact_Pa"]/1e6)
for kind,rows in c["joints"].items():
    f=rows["frozen_k0.2"];sc=f["scores"]
    d[kind]=dict(end_kg=f["m_end_kg"],joint_kg=f["m_joint_kg"],
        per_node_kg=f["m_joint_per_node_kg"],insert_mm=f["bond_or_insert_m"]*1000,
        sleeve_mm=None if f["sleeve_t_m"] is None else f["sleeve_t_m"]*1000,
        times_225=f["versus_225_kg"],frozen_tw_mm=sc["t_w_m"]*1000,
        frozen_SF=sc["SF_least"],frozen_gov=sc["governing"],
        contact_MPa=sc["sigma_axial_Pa"]/1e6,SF_on_3900=sc["SF_contact_on_3900"],
        SF_on_380=sc["SF_contact_on_flexure_380"])
    for k in (.2,.4):
        x=rows["reopt_k"+str(k)]
        d[kind]["reopt_k"+str(k)]=dict(s_m=x["s_m"],SF=x["SF_least"],gov=x["governing"],
            joint_kg=x["m_joint_kg"],tube_kg=x["m_tube_kg"],r_o_mm=x["r_o_m"]*1000,
            t_w_mm=x["t_w_m"]*1000)
d["scale_held_section"]=[]
for row in c["scale_at_held_section"]:
    x=dict(s_m=row["s_m"],N_kN=row["N_N"]/1000)
    for kind,f in row["kinds"].items():
        x[kind]=dict(end_kg=f["m_end_kg"],joint_kg=f["m_joint_kg"],per_node_kg=f["m_joint_per_node_kg"])
    d["scale_held_section"].append(x)
walk(o["display_half_up"],d)

old=r["original_force_reconstruction"]
h=sup["old_held"]["ti_sleeve"]
base=check.score_row(s0,r0,a0,.2,True)
items=[
    ("force kN","973.7",check.force(s0,True)/1000),
    ("spacing m","2.04",s0),
    ("frozen global SF","1.2255279468805444",base["SF_global"]),
    ("nodes","350.7",check.counts(s0)[0]),
    ("ends/node","5.97",h["ends_per_node"]),
    ("pin kg","0.461",sup["old_pin"]["mass_kg"]),
    ("bearing GPa","15.6",h["pin_bearing_Pa"]/1e9),
    ("filed wall mm","0.880",base["t_w_m"]*1000),
    ("Ti strength MPa","827",check.MATERIALS["ti_sleeve"][1]/1e6),
    ("bond shear MPa","28.9",check.TAU_BOND/1e6),
    ("allowance kg","225.5",c["filed_011b_point"]["m_joint_kg"]),
    ("Ti end kg","0.226",old["ti_sleeve"]["frozen_k0.2"]["m_end_kg"]),
    ("Ti mass kg","473.1",old["ti_sleeve"]["frozen_k0.2"]["m_joint_kg"]),
    ("Ti ratio","2.10",h["versus_allowance"]),
    ("Ti bond mm","43.4",old["ti_sleeve"]["frozen_k0.2"]["bond_or_insert_m"]*1000),
    ("Ti frozen SF","1.095",old["ti_sleeve"]["frozen_k0.2"]["scores"]["SF_least"]),
    ("Ti k.2 SF","1.159",old["ti_sleeve"]["reopt_k0.2"]["SF_least"]),
    ("Ti k.4 SF","1.560",old["ti_sleeve"]["reopt_k0.4"]["SF_least"]),
    ("Invar mass kg","2575.7",old["invar_sleeve"]["frozen_k0.2"]["m_joint_kg"]),
    ("Invar frozen SF","0.280",old["invar_sleeve"]["frozen_k0.2"]["scores"]["SF_least"]),
    ("braze shear MPa","25",check.TAU_BRAZE/1e6),
    ("braze insert mm","50.1",old["sic_braze"]["frozen_k0.2"]["bond_or_insert_m"]*1000),
    ("braze end kg","0.106",old["sic_braze"]["frozen_k0.2"]["m_end_kg"]),
    ("braze mass kg","221.7",old["sic_braze"]["frozen_k0.2"]["m_joint_kg"]),
    ("braze frozen SF","1.227",old["sic_braze"]["frozen_k0.2"]["scores"]["SF_least"]),
    ("braze k.2 SF","1.227",old["sic_braze"]["reopt_k0.2"]["SF_least"]),
    ("braze k.4 SF","1.699",old["sic_braze"]["reopt_k0.4"]["SF_least"]),
    ("wrap compression MPa","1470",check.MATERIALS["cfrp_wrap"][1]/1e6),
    ("wrap tensile unused MPa","2550",c["cfrp_allowable_Pa"]["tensile_not_used"]/1e6),
    ("wrap end kg","0.045",old["cfrp_wrap"]["frozen_k0.2"]["m_end_kg"]),
    ("wrap mass kg","93.1",old["cfrp_wrap"]["frozen_k0.2"]["m_joint_kg"]),
    ("wrap bond mm","43.4",old["cfrp_wrap"]["frozen_k0.2"]["bond_or_insert_m"]*1000),
    ("wrap frozen SF","1.232",old["cfrp_wrap"]["frozen_k0.2"]["scores"]["SF_least"]),
    ("wrap k.2 SF","1.261",old["cfrp_wrap"]["reopt_k0.2"]["SF_least"]),
    ("wrap k.4 SF","1.767",old["cfrp_wrap"]["reopt_k0.4"]["SF_least"]),
    ("wall stress MPa","1428.4",h["sigma_contact_Pa"]/1e6),
    ("compression SF","2.73",h["SF_contact_on_3900"]),
    ("flexure ratio","0.266",h["SF_contact_on_flexure_380"]),
    ("022 force kN","1423.8",sup["022_original_force_N"]/1000),
    ("022 wrap kg","83.3",sup["022_original_report_joint_masses"]["cfrp_wrap"]["m_joint_kg"]),
    ("022 braze kg","182.3",sup["022_original_report_joint_masses"]["sic_braze"]["m_joint_kg"]),
    ("022 sleeve kg","423.2",sup["022_original_report_joint_masses"]["ti_sleeve"]["m_joint_kg"]),
    ("022 allowance kg","216.4",check.load("mainline022.json")["carried_011b_k02"]["equilateral"]["m_joint_kg"]),
]
for name,published,value in items:add(name,published,value,"first report; superseded load")
with (ROOT/"REPORT-CHECK.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(audit[0]));w.writeheader();w.writerows(audit)
summary={"numeric_and_display_checks":len(audit),"failed":[x for x in audit if not x["pass_check"]],
         "original_report_numbers_checked":len(items),
         "scope":"First report's preserved body and corrected RESULTS display fields. Original artifact versions unavailable."}
(ROOT/"REPORT-AUDIT.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
