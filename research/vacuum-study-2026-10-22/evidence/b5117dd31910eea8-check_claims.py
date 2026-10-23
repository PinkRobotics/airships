"""Independent displayed-precision, source-selection, credit and transfer sensitivities."""
from pathlib import Path
import json
import math
import csv
ROOT=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def write(n,x):(ROOT/n).write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
records=load(ROOT/"INDEPENDENT-RECORDS.json")
s=load(ROOT/"INDEPENDENT-SUMMARIES.json")
card=(ROOT/"intake/CARD.md").read_text()
rows=[]
def check(row,field,owner,independent,tol=1e-7):
    ok=abs(owner-independent)<=tol if isinstance(owner,(float,int)) and isinstance(independent,(float,int)) else owner==independent
    rows.append(dict(row=row,field=field,owner=owner,independent=independent,pass_=ok,tolerance=tol))
def point(lead,R,weather,source=None):
    return next(r for r in records if r["lead"]==lead and r["R_m"]==R and r["weather"]==weather
                and (lead=="P3" and r["service"]=="ground" or lead=="P2" and not r["floor"] and r["source"]==(source or "040 with 048 finish transfer")))
def num(text):return float(text.replace(",","").replace("−","-").replace("%","").strip().split()[0])

# Verify all printed numerical tables against recomputed data at their displayed precision.
tables=[];block=[]
for line in card.splitlines()+[""]:
    if line.startswith("|"):block.append([c.strip() for c in line.strip("|").split("|")])
    elif block:tables.append(block);block=[]
for ti,t in enumerate(tables):
    if t[0][0]=="lead" and t[0][1]=="radius":
        for j,rr in enumerate(t[2:]):
            lead,R,w=rr[0],int(rr[1][1:]),rr[2]
            e=point(lead,R,w,"048" if lead=="P2" and R==10 else None)["evaluated"][11 if lead=="P2" and R==10 else 15]
            check(f"CARD/table{ti}/row{j}","MGA_kg",num(rr[3]),round(e["mga_sourced_kg"]))
            check(f"CARD/table{ti}/row{j}","payload_kg",num(rr[4]),round(e["payload_sourced_kg"]))
    elif t[0][0]=="maturity":
        values=[("estimated","0–2",25,30,25),("calculated","3–5",15,20,20),("measured","8",3,3,3)]
        for j,(rr,expected) in enumerate(zip(t[2:],values)):
            for k in range(2,5):check(f"CARD/table{ti}/row{j}",t[0][k],num(rr[k]),expected[k])
    elif t[0][0]=="radius":
        for j,rr in enumerate(t[2:]):
            R=int(rr[0][1:])
            for k,(lead,w) in enumerate([("P2","ISA"),("P2","optimistic"),("P3","ISA"),("P3","optimistic")],1):
                if rr[k].startswith("TRL") or rr[k]=="none":
                    expected=next(x for x in s["maturity"] if (x["lead"],x["R_m"],x["weather"])==(lead,R,w))["least_mature_row_that_floats"]
                    check(f"CARD/table{ti}/row{j}",lead+"/"+w,rr[k].split(" (")[0],expected or "none")
                else:
                    expected=point(lead,R,w)["evaluated"][15]["payload_sourced_kg"]
                    check(f"CARD/table{ti}/row{j}",lead+"/"+w,num(rr[k]),round(expected))
    elif t[0][0]=="lead" and t[0][1]=="weather":
        for j,rr in enumerate(t[2:]):
            lead,w,R=rr[0],rr[1],int(rr[2])
            expected=next(x for x in s["flat"] if (x["lead"],x["R_m"],x["weather"])==(lead,R,w))
            for k,pct in enumerate(range(0,31,5),3):check(f"CARD/table{ti}/row{j}",f"flat_{pct}",num(rr[k]),round(expected[f"flat_{pct}"]))
            check(f"CARD/table{ti}/row{j}","tolerable",rr[-1],f"{expected['tolerable_flat']*100:.1f}%" if expected["tolerable_flat"]>=0 else "none")

# Printed bullet values, independently obtained from the recomputed R10 bills.
bullet_values={
 "P2":[("faces",3764.2,564.6),("core",455.,68.3),("charged_joining",215.6,64.7),
       ("mooring_pad",33.1,5.),("structural_primer",12.6,3.8),("coating",10.5,1.0)],
 "P3":[("SiC_tubes",4182.2,627.3),("PBO_two_plies",95.3,14.3),
       ("barrier_and_protection",95.8,19.2),("joint_sleeves_and_allowance",34.3,10.3),
       ("joint_bond_and_installation",10.1,3.0),("nodes",5.,1.5),("mooring_load_introduction",33.1,5.)]}
for lead,values in bullet_values.items():
    p=point(lead,10,"ISA","048" if lead=="P2" else None)
    p=p["evaluated"][11 if lead=="P2" else 15]
    b={x["item"]:x for x in s["R10"][lead]["rows"]}
    for item,m,a in values:
        check("CARD/R10/"+lead,item+"/mass",m,round(b[item]["kg"],1))
        check("CARD/R10/"+lead,item+"/allowance",a,round(p["mga_sourced_by_item"][item],1))
for lead,val in [("P2",4491),("P3",4456)]:
    check("CARD/R10/"+lead,"hardware_kg",val,round(s["R10"][lead]["hardware_kg"]))

transfers=s["transfer"]
largest=max(transfers,key=lambda x:abs(x["diff_kg"]))
smallest=min(transfers,key=lambda x:abs(x["diff_kg"]))
endpoint=[x for x in transfers if x["mask"] in [11,15]]
range_result=dict(all_96_min_signed_kg=min(x["diff_kg"] for x in transfers),
                  all_96_max_signed_kg=max(x["diff_kg"] for x in transfers),
                  all_96_min_absolute_kg=min(abs(x["diff_kg"]) for x in transfers),
                  all_96_max_absolute_kg=max(abs(x["diff_kg"]) for x in transfers),
                  endpoint_masks_11_15_min_absolute_kg=min(abs(x["diff_kg"]) for x in endpoint),
                  endpoint_masks_11_15_max_absolute_kg=max(abs(x["diff_kg"]) for x in endpoint),
                  largest=largest,smallest=smallest)

# Correct the whole affected allowance fields on the unburdened mass denominator, not just one headline.
credit=[]
percentages=[("sourced",.2),("estimated",.25)]
for ri,r in enumerate(records):
    if r["lead"]!="P2":continue
    for mi,(p,e) in enumerate(zip(r["masks"],r["evaluated"])):
        for label,rate in percentages:
            old=e[f"mga_{label}_by_item"]["coating"]
            replacement=p["bill"]["coating"]/1.1*(rate-.1)
            for field,ov,iv in [
                (f"mga_{label}_by_item/coating",old,replacement),
                (f"mga_{label}_kg",e[f"mga_{label}_kg"],e[f"mga_{label}_kg"]-old+replacement),
                (f"payload_{label}_kg",e[f"payload_{label}_kg"],e[f"payload_{label}_kg"]+old-replacement)]:
                credit.append(dict(row=f"P2_records/{ri}/evaluated/{mi}",field=field,owner=ov,independent=iv,category="CBE-denominator"))

source_changes=[]
for name in ["flat","maturity"]:
    for i,old in enumerate(s[name]):
        if old["lead"]!="P2" or old["R_m"]>15:continue
        r=point("P2",old["R_m"],old["weather"],"048");e=r["evaluated"][15];p=r["masks"][15]
        if name=="flat":
            updated={f"flat_{f}":e["payload_kg"]-f/100*e["hardware_kg"] for f in range(0,31,5)}
            updated["tolerable_flat"]=e["payload_kg"]/e["hardware_kg"]
        else:
            updated={"payload_no_mga_kg":e["payload_kg"]}
            for trl,rates in [("TRL 0-2",(25,30,25)),("TRL 3-5",(15,20,20)),("TRL 6",(10,15,15)),("TRL 7",(5,6,5)),("TRL 8",(3,3,3)),("TRL 9",(0,0,0))]:
                b=p["bill"]
                a=rates[0]/100*(b["faces"]+b["core"]+b["mooring_pad"])
                a+=rates[1]/100*(b["charged_joining"]+b["structural_primer"]+b.get("desiccant",0))
                a+=rates[2]/100*b["absorbed_water"]+max(0,rates[2]/100-.1)*b["coating"]
                updated[trl]=e["payload_kg"]-a
            revised=next((trl for trl in ["TRL 0-2","TRL 3-5","TRL 6","TRL 7","TRL 8","TRL 9"] if updated[trl]>=0),None)
            if revised!=old["least_mature_row_that_floats"]:
                updated["least_mature_row_that_floats"]=revised
        for f,v in updated.items():
            source_changes.append(dict(row=f"{name}/{i}",field=f,owner=old[f],independent=v,category="direct048-vs-transfer"))

# Check ancillary 053 / 054 claims strictly at the mass-account boundary.
supp=ROOT/"intake/supplement"
r53=load(supp/"vacuum-mainline053-thermal-table-settled-1020/RESULTS.json")
thermal=[]
for x in r53["primary_rows"]:
    if x["R_m"]==10 and x["weather"]=="ISA" and x["cure_in_global"]:
        total=math.fsum(v for k,v in x.items() if k.startswith("mass_"))
        lift=point("P2",10,"ISA","048")["masks"][11]["lift_kg"]
        y=lift-total
        check("053/"+x["model"],"payload_kg",x["payload_kg"],y)
        thermal.append(dict(model=x["model"],payload_kg=y,loss_from_owner_kg=s["R10"]["P2"]["payload_kg"]-y))
r54=load(supp/"vacuum-mainline054-p3-dry-cavity-1020/RESULTS.json")
capture=next(x for x in r54["capture"] if x["R_m"]==10 and x["weather"]=="ISA" and x["days"]==7 and x["account"]=="endpoint" and x["candidate"]=="SIOX")
with (supp/"vacuum-mainline054-p3-dry-cavity-1020/MASS-ACCOUNT.csv").open() as f:
    csv54=list(csv.DictReader(f))
row54=next(x for x in csv54 if x["R_m"]=="10" and x["weather"]=="ISA" and x["days"]=="7" and x["account"]=="endpoint" and x["candidate"]=="SIOX")
mass54=math.fsum(float(v) for k,v in row54.items() if k not in ["R_m","weather","account","candidate","days","route","tag","lift_kg","total_charged_kg","payload_kg"])
payload54=float(row54["lift_kg"])-mass54
check("054/R10/ISA/7d/SIOX","total_charged_kg",float(row54["total_charged_kg"]),mass54)
check("054/R10/ISA/7d/SIOX","payload_kg",capture["payload_kg"],payload54)
check("054/R10/ISA/7d/SIOX","incremental_bill_kg",capture["incremental_bill_kg"],capture["capture_system_kg"]+capture["barrier_delta_kg"]+capture["reserve_extra_kg"])
check("CARD/053","thermal_loss_kg",.6,round(next(t["loss_from_owner_kg"] for t in thermal if t["model"]=="forced_conduction"),1))
check("CARD/054","seven_day_payload_kg",1.1,round(payload54,1))

sens=[]
for R in [10,12,15,20,30]:
    for w in ["ISA","optimistic"]:
        for lead in ["P2","P3"]:
            r=point(lead,R,w);e=r["evaluated"][15];p=r["masks"][15]
            zero=sum(p["bill"].get(k,0) for k in (["systems","extra_service"] if lead=="P2" else ["systems","vacuum_service"]))
            allocation30=.3*zero
            # CBE margin repair only affects P2 coating, whose included +10% is documented.
            credit_correction=p["bill"]["coating"]*.1/11 if lead=="P2" else 0
            case=dict(lead=lead,R_m=R,weather=w,payload_no_mga_kg=e["payload_kg"],
                      mga_kg=e["mga_sourced_kg"],payload_sourced_kg=e["payload_sourced_kg"],
                      tolerance_pct=100*e["payload_kg"]/e["hardware_kg"],
                      zero_allocated_hardware_kg=zero,extra_30pct_allocation_kg=allocation30,
                      payload_plus_30pct_allocation_kg=e["payload_sourced_kg"]-allocation30,
                      corrected_coating_payload_kg=e["payload_sourced_kg"]+credit_correction)
            sens.append(case)

# A mixed protection bill cannot be proven all-thermal without a mapping.
# Sensitivity: apply 30% to attachment and seams, leave PET/Al/white at20%.
protection=[]
u52=load(ROOT/"intake/files_read/vacuum-mainline052-p3-common-account-1020/RESULTS.json")
for rec in u52["rows"]:
    for p in rec["endpoints"]:
        parts=p["protection_kg"]
        uplift=.1*(parts["attachment"]+parts["seams"])
        protection.append(dict(R_m=rec["R_m"],weather=rec["weather"],service=rec["service"],mask=p["mask"],
                               owner_thermal_20pct=.2*p["bill_kg"]["barrier_and_protection"],
                               mixed_thermal20_hardware30=.2*p["bill_kg"]["barrier_and_protection"]+uplift,
                               extra_kg=uplift))

result=dict(comparisons=len(rows),mismatches=sum(not r["pass_"] for r in rows),rows=rows,
            transfer_range=range_result,thermal=thermal,week_aloft=dict(payload_kg=payload54,total_charged_kg=mass54),
            all_radii=sens,credit_correction_fields=len(credit),source_correction_fields=len(source_changes))
write("CARD-AND-ANCILLARY-AUDIT.json",result)
write("CBE-CREDIT-EXACT-FIELDS.json",credit)
write("DIRECT048-EXACT-FIELDS.json",source_changes)
write("PROTECTION-CLASS-SENSITIVITY.json",protection)
print(json.dumps({k:v for k,v in result.items() if k not in ["rows","all_radii"]}))
print("MISMATCHES",json.dumps([r for r in rows if not r["pass_"]]))
print("R30",json.dumps([x for x in sens if x["R_m"]==30]))
