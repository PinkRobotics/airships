import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
import csv
audit=Audit();mats=materials()
for i,row in enumerate(read("FRAME-COMPARE.json")["rows"]):
    if row["section_policy"]!="minimum_wall_q1_screen":continue
    mat=mats[row["material"]];res=row["reserve"];ro=row["ro_m"]
    _,arr,rr=base_data(res);base=BASE[res]
    def sf(t):
        A,I=section(ro,t);a,b,e=demands(arr,mat,ro,t)
        S=(.099+.901*math.exp(-math.sqrt(ro/t)/16))*mat["local_classical_coefficient_Pa"]*t/ro
        vals=[float(e.min()),float(load_roots(a,b,e,S).min()),
              .2*rr["linear_multipliers"][0]*mat["Eax_Pa"]*I/(410e9*base["section"]["inertia_m4"])]
        if mat["screen_compression_Pa"] is not None:vals.append(float(load_roots(a,b,e,mat["screen_compression_Pa"]).min()))
        return min(vals)-1
    t=brentq(sf,1e-7,ro*.95,xtol=1e-15)
    audit.check(f"minimum_wall[{i}]","wall_m",row["wall_m"],t,atol=1e-12)
    audit.check(f"minimum_wall[{i}]","root_screen",1.,sf(t)+1,rtol=1e-8)

def csv_rows(name):
    with (OWNER/name).open() as f:return list(csv.DictReader(f))
def csv_compare(name,cs,js):
    audit.check(name,"row_count",len(cs),len(js))
    for i,(c,j) in enumerate(zip(cs,js)):
        for field,owner in c.items():
            if field not in j:continue
            expected=j[field]
            if expected is None:v=None if owner=="" else owner
            elif isinstance(expected,bool):v=owner=="True"
            elif isinstance(expected,(float,int)):v=float(owner)
            else:v=owner
            audit.check(f"{name}[{i}]",field,v,expected,rtol=1e-12,atol=1e-12)
csv_compare("TARGET-SURFACE.csv",csv_rows("TARGET-SURFACE.csv"),read("TARGETS.json")["rows"])
frame=[]
for row in read("FRAME-COMPARE.json")["rows"]:
    frame.append({**row,**{"SF_"+k:v for k,v in row["modes"].items()}})
csv_compare("FRAME-COMPARE.csv",csv_rows("FRAME-COMPARE.csv"),frame)
gaps=[]
for row in read("GAPS.json")["rows"]:
    if row["load_case"]!="operating":continue
    target=next((v for v in row.get("targets",[]) if v["m"]==10 and v["Pf"]==.001),None)
    gaps.append(dict(material=row["material"],reserve=row["reserve"],section_policy=row["section_policy"],
      tubes_kg=row["frame_tubes_kg"],total_kg=row["total_mass_kg"],SF_or_ceiling=row["conditional_mechanical_SF_or_ceiling"],
      target_whole_scale_GPa=None if target is None else target["whole_member_scale_needed_Pa"]/1e9,
      strength_factor_over_typical=None if target is None else target["whole_member_strength_factor_over_typical"],
      m_needed=row.get("hypothetical_m_needed_for_Pf1e3"),hypothetical_Pf=row.get("hypothetical_Pf_m10_if_typical_is_member_scale"),
      force_basis=row["force_basis"]))
csv_compare("GAPS.csv",csv_rows("GAPS.csv"),gaps)
hail=[]
for row in read("HAIL.json")["rows"]:
    if row["diameter_m"]!=.0508:continue
    common={v["assumed_contact_scale_Pa"]:v["conditional_probability_if_contact_fit_applies"]
        for v in row["explicit_common_fit_scenarios"] if v["pressure_model"]=="Shi"}
    hail.append(dict(material=row["material"],reserve=row["reserve"],section_policy=row["section_policy"],
      wall_mm=row["wall_m"]*1000,stress_flow_MPa=row["stress_flow_Pa"]/1e6,stress_Shi_MPa=row["stress_Shi_Pa"]/1e6,
      scenario_192m5p5_Shi=common[192e6],scenario_299m4p6_Shi=common[299e6],actual_probability="unknown"))
csv_compare("HAIL-DESIGN.csv",csv_rows("HAIL-DESIGN.csv"),hail)
combined=read("RESULTS.json")
for k,f,key in [("target_surface","TARGETS.json",None),("material_models","MATERIAL-MODELS.json",None),
                ("material_gaps","GAPS.json","rows"),("witnesses","WITNESSES.json","rows"),
                ("damage","DAMAGE.json","rows")]:
    data=read(f);data=data if key is None else data[key]
    audit.check("RESULTS.json",k+"_identical_to_detail",True,combined[k]==data)
audit.save("SECTIONS-TABLES-CHECK.json")
