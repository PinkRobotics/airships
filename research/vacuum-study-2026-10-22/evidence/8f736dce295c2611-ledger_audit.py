"""Recalculate all supplied endpoint/least-point bills, never call owner code."""
from check_model import *
import csv

diff=[];records=[]
def compare(label,kind,old,new):
    for k,value in old.items():
        if k not in new or not isinstance(value,(int,float)) or isinstance(value,bool):continue
        delta=float(new[k])-value
        diff.append(dict(row=label,kind=kind,field=k,owner=value,checker=float(new[k]),delta=delta))

allrows=[("folded",x) for x in ROWS]
allrows += [("040",x) for x in read("owner/RESULTS.json")["rows_040_coating"]]
for origin,row in allrows:
    key=row.get("construction",LABELS[row["case"]])
    c=props(key)
    kwargs=dict(finish=row.get("finish","reference040"),variant=row.get("variant","primary"),
                climate=row["weather"],floor=row["floor"])
    label=f'{origin}|{key}|{kwargs["finish"]}|{kwargs["variant"]}|R{row["R_m"]}|{row["weather"]}|floor{row["floor"]}'
    geo=row.get("endpoint_all_geometry")
    if geo:
        result=bill(c,row["R_m"],geo["tf_m"],geo["tc_m"],**kwargs)
        compare(label,"all_endpoint.bill",row["endpoint_all_bill_kg"],result["bill_kg"])
        compare(label,"all_endpoint.joining",row.get("endpoint_all_joining",{}),result["joining"])
        compare(label,"all_endpoint.vacuum",row.get("endpoint_all_vacuum",{}),result["vacuum"])
        compare(label,"all_endpoint",{"payload_kg":row["endpoint_all_kg"]},result)
        records.append(dict(row=label,kind="all_endpoint",**result))
    least=row.get("least")
    if least:
        mask=sum(bit for name,bit in [("gamma",1),("Q",2),("face tuple",4),("film",8)] if name in row["least_axes"])
        result=bill(c,row["R_m"],least["tf_m"],least["tc_m"],mask=mask,u=row["least_usage"],**kwargs)
        compare(label,"least.bill",least.get("bill_kg",{}),result["bill_kg"])
        compare(label,"least",{"payload_kg":least["payload_kg"]},result)
        records.append(dict(row=label,kind="least",**result))

simple=dict(
    k13_qi_baseline=qi(59.5*6894.757293168361e6),k13_qi_projection=qi(935e9*(338/540)),
    k13_density_33wt_resin=1/(.67/2200+.33/1200),
    k13_implied_Vf=(.67/2200)/(.67/2200+.33/1200),
    k13_density_60Vf=.6*2200+.4*1200,k13_fibre_mass_fraction_60Vf=.6*2200/1800,
    k13_projection_E1=935e9*(338/540),
    k13_matrix_E_needed_for_60Vf=(935e9*(338/540)-.6*935e9)/.4,
    k13_voigt_E1_with_3GPa_matrix=.6*935e9+.4*3e9,
    k13_coherent_qi_3GPa=qi(.6*935e9+.4*3e9),
    m55_density=.6*1910+.4*1200,m55_min_gauge=6*.030/(.6*1910),
    m55_full_compression=313e6/(1-.308),
    k13_min_gauge=6*.061e-3,wind_pressure_Pa=WIND,beta=BETA,
    materion_391klb_t=391000*.45359237/1000,
    materion_implied_capacity_t=391000*.45359237/1000/.61)
projection=FOLD["constructions"][-2]["key"]
corrections=[]
for row in ROWS:
    if row["construction"]!=projection or row["variant"]!="primary" or row["finish"]!="MLCCAg" or row["floor"]:continue
    for kind,geo,mask,u in [("least",row.get("least"),7,row.get("least_usage")),("all_endpoint",row.get("endpoint_all_geometry"),15,1)]:
        if not geo:continue
        orig=bill(props(projection),row["R_m"],geo["tf_m"],geo["tc_m"],mask=mask,u=u,climate=row["weather"])
        new=bill(props(projection,dict(rho_f=1800,fibre_w=11/15)),row["R_m"],geo["tf_m"],geo["tc_m"],mask=mask,u=u,climate=row["weather"])
        corrections.append(dict(R=row["R_m"],weather=row["weather"],kind=kind,
           owner_model_payload=orig["payload_kg"],corrected_density_payload=new["payload_kg"],
           owner_faces=orig["bill_kg"]["faces"],corrected_faces=new["bill_kg"]["faces"],
           owner_fibre=orig["bill_kg"]["faces"]*.67,corrected_fibre=new["bill_kg"]["faces"]*11/15,
           corrected_pitch_capacity_share=new["bill_kg"]["faces"]*11/15/1.4e6))
with (ROOT/"LEDGER-COMPARISONS.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=list(diff[0]));w.writeheader();w.writerows(diff)
(ROOT/"LEDGER.json").write_text(json.dumps(dict(rows=records,scalar_checks=simple,density_corrections_fixed_geometry=corrections),indent=2)+"\n")
groups={}
for x in diff:
    k=x["kind"]+"."+x["field"]
    if k not in groups or abs(x["delta"])>abs(groups[k]["delta"]):groups[k]=x
(ROOT/"LEDGER-SUMMARY.json").write_text(json.dumps(dict(comparisons=len(diff),records=len(records),maxima=groups),indent=2)+"\n")
print(json.dumps(dict(comparisons=len(diff),records=len(records),worst=sorted(groups.values(),key=lambda x:abs(x["delta"]),reverse=True)[:10],scalar_checks=simple),indent=2))
