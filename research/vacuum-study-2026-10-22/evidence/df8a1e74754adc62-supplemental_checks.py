"""Independent layer, water, ground-resource, service and R10 bill arithmetic."""
import csv
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import account_model as m

r=Path(__file__).resolve().parent
main=json.loads((r/"intake/owner/RESULTS.json").read_text())
byid={row["id"]:row for row in main["rows"]}
comparisons=[]


def cmp(row,field,old,new,rtol=2e-8,atol=2e-8):
    comparisons.append(dict(row=row,field=field,owner=old,independent=new,
                            delta=new-old,agrees=math.isclose(old,new,rel_tol=rtol,abs_tol=atol),
                            rtol=rtol,atol=atol))


def point(row):
    p=row["two_factor_endpoint"]
    return m.evaluate(p["R_m"],p["geometry"]["tf_m"],p["geometry"]["tc_m"],
                      p["mask"],p["usage"],p["settings"])


coatings=json.loads((r/"intake/owner/COATINGS.json").read_text())
mass_mlc=(.05*8.4+.12*10.5+1.2*3.97+.4*2.648+.01*7.2)/1000
mass_classical=[((.08+al)*3.97+.12*10.5+si*2.648+.01*7.2)/1000
                for al,si in ((1.6,.5),(1.9,.75))]
for c in coatings:
    if c["id"]=="MLCCAg":
        cmp(c["id"],"areal_mass_kg_m2",c["areal_mass_kg_m2"],mass_mlc)
    elif c["id"]=="CCAg":
        cmp(c["id"],"areal_mass_kg_m2",c["areal_mass_kg_m2"],mass_classical[0])
        for i,v in enumerate(mass_classical):
            cmp(c["id"],f"mass_band_kg_m2[{i}]",c["mass_band_kg_m2"][i],v)

drying=json.loads((r/"intake/owner/DRYING-COSTS.json").read_text())
dryrows=[]
for old in drying["rows"]:
    row=byid[old["id"]]
    p=point(row)
    b=p["bill_kg"]
    wi=p["material_water_initial_by_material_kg"]
    wr=p["material_water_remaining_by_material_kg"]
    removed=sum(wi.values())-sum(wr.values())
    area=p["geometry"]["area_m2"]
    v=p["geometry"]["volume_m3"]
    out=dict(material_water_initial_kg=sum(wi.values()),
             material_water_remaining_kg=sum(wr.values()),
             material_water_removed_ground_kg=removed,
             external_water_remaining_kg=b["water"],
             sorbent_and_cartridge_kg=b["desiccant"],
             sorbent_capacity_kg=p["vacuum"]["desiccant_water_capacity_kg"],
             external_water_max_for_endpoint_float_kg_m2=.1+p["signed_payload_kg"]/area,
             signed_payload_kg=p["signed_payload_kg"])
    if old["route"]=="dry_gas":
        out.update(dry_gas_five_exchanges_m3=5*v,
                   dry_gas_nitrogen_kg=5*v*m.P0*.0280134/(m.RU*m.TA))
    if old["route"]=="bake70":
        polymer=p["actual_joining"]["total"]+b["structural_primer"]+b["coating"]
        heat=(1825*b["faces"]+900*b["core"]+1000*polymer)*(343.15-m.TA)+2.45e6*removed
        out["ideal_bake_lower_bound_kWh"]=heat/3.6e6
    for k,vv in out.items():cmp(old["id"],k,old[k],vv)
    for category,values in (("water_initial_by_material_kg",wi),("water_remaining_by_material_kg",wr)):
        for k,vv in values.items():cmp(old["id"],category+"."+k,old[category][k],vv)
    dryrows.append(dict(id=old["id"],**out,water_initial_by_material_kg=wi,water_remaining_by_material_kg=wr))
cmp("drying_global","airborne_fraction_after_five_ideal_mixed_exchanges",
    drying["airborne_fraction_after_five_ideal_mixed_exchanges"],math.exp(-5))
dew=1838.675/(5.40221-math.log10(.01))-(-31.737)
cmp("drying_global","dewpoint_at_1kPa_K",drying["dewpoint_at_1kPa_K"],dew)

service=json.loads((r/"intake/owner/SERVICE-AUDIT.json").read_text())
service_rows=[]
for old in service:
    row=byid[old["id"]];op=row["two_factor_endpoint"];p=point(row)
    rad=op["R_m"];tf=op["geometry"]["tf_m"];tc=op["geometry"]["tc_m"]
    v=p["geometry"]["volume_m3"]
    free=4*math.pi/3*(rad-2*tf-tc)**3+p["vacuum"]["pore_volume_m3"]
    out=dict(free_volume_m3=free,refined_pressure_Pa=10*320/m.TA+(p["vacuum"]["hot_pressure_24h_upper_Pa"]-10*320/m.TA)*v/free)
    no_capture=dict(op["settings"],desiccant_capture_fraction=0)
    v0=m.vacuum(rad,tf,tc,p["actual_joining"],sum(p["material_water_initial_by_material_kg"].values()),
                sum(p["material_water_remaining_by_material_kg"].values()),p["nominal_volatile_inventory_kg"],no_capture)
    out["no_capture_pressure_Pa"]=v0["hot_pressure_24h_upper_Pa"]
    # Removing nominal conditioning increases that finite release by factor ten.
    # This variant takes no capture credit, as an explicit upper-pressure audit.
    unconditioned=m.vacuum(rad,tf,tc,p["actual_joining"],sum(p["material_water_initial_by_material_kg"].values()),
                          sum(p["material_water_remaining_by_material_kg"].values()),
                          10*p["nominal_volatile_inventory_kg"],no_capture)
    out["no_nominal_conditioning_pressure_Pa"]=unconditioned["hot_pressure_24h_upper_Pa"]
    for k,vv in out.items():cmp(old["id"],k,old[k],vv)
    service_rows.append(dict(id=old["id"],**out))

olddata=json.loads((r/"intake/base040/03/RESULTS.json").read_text())
targets=[]
def find_old(x,path):
    if isinstance(x,dict):
        if x.get("signed_payload_kg")==-109.64920782047648:
            targets.append((path,x));return
        for k,v in x.items():find_old(v,path+"."+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):find_old(v,path+f"[{i}]")
find_old(olddata,"old040")
oldpath,oldpoint=targets[0]
sett=dict(oldpoint["settings"],finish_id="reference040",structural_primer_kg_m2=0,
          moisture_scale=0,finish_water_kg_m2=0,desiccant=False)
oldtab=json.loads((r/"intake/base040/04/THERMAL-TABLE.json").read_text())["10"]
base=m.evaluate(10,oldpoint["geometry"]["tf_m"],oldpoint["geometry"]["tc_m"],
                oldpoint["mask"],oldpoint["usage"],sett,oldtab)
for k,v in oldpoint["bill_kg"].items():cmp(oldpath,"bill_kg."+k,v,base["bill_kg"][k])
cmp(oldpath,"signed_payload_kg",oldpoint["signed_payload_kg"],base["signed_payload_kg"])
new=point(byid["MLCCAg-R10-ISA-floor-bake70-retained_water"])
owner_recon=json.loads((r/"intake/owner/R10-RECONCILIATION.json").read_text())
gain={k:base["bill_kg"].get(k,0)-new["bill_kg"].get(k,0)
      for k in owner_recon["payload_gains_by_bill_term_kg"]}
for k,v in gain.items():cmp("reconciliation","payload_gains_by_bill_term_kg."+k,
                           owner_recon["payload_gains_by_bill_term_kg"][k],v)
for k,v in dict(original040_payload_kg=base["signed_payload_kg"],
                new_payload_kg=new["signed_payload_kg"],total_gain_kg=sum(gain.values()),
                closure_error_kg=base["signed_payload_kg"]+sum(gain.values())-new["signed_payload_kg"]).items():
    cmp("reconciliation",k,owner_recon[k],v,atol=1e-8)

with (r/"SUPPLEMENTAL-COMPARISONS.csv").open("w") as f:
    writer=csv.DictWriter(f,fieldnames=list(comparisons[0]));writer.writeheader();writer.writerows(comparisons)
bad=[x for x in comparisons if not x["agrees"]]
out=dict(comparisons=len(comparisons),mismatches=bad,layer_mass_kg_m2=dict(MLCCAg=mass_mlc,CCAg=mass_classical),
         drying=dryrows,service=service_rows,reconciliation=gain,old040_source_point_path=oldpath,
         scope="Independent scalar equations at pinned geometries and thermal inputs.")
(r/"SUPPLEMENTAL-RESULTS.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
print(json.dumps(dict(comparisons=len(comparisons),mismatches=len(bad),first_mismatches=bad[:8])))
