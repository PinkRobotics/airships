"""Independent geometry searches, with explicitly separated thermal bases."""
from check_model import *
from datetime import datetime,timezone
import argparse,time
from itertools import combinations
p=argparse.ArgumentParser();p.add_argument("--mode",choices=["independent","pinned"],default="independent")
p.add_argument("--corrections",action="store_true")
a=p.parse_args()

def least_audit(c,R,endpoint,kwargs):
    if endpoint is None or endpoint["payload_kg"]<0:return None,[]
    tried=[];candidates=[]
    for count in range(5):
        for subset in combinations([1,2,4,8],count):
            mask=sum(subset)
            x=endpoint if mask==15 else optimize(c,R,mask=mask,**kwargs)
            tried.append(dict(mask=mask,payload_kg=x["payload_kg"] if x else None))
            if not x or x["payload_kg"]<0:continue
            lo=0.;hi=1.
            for _ in range(24):
                mid=(lo+hi)/2
                y=optimize(c,R,mask=mask,u=mid,**kwargs)
                if y and y["payload_kg"]>=0:hi=mid
                else:lo=mid
            candidates.append(dict(mask=mask,usage=hi,point=optimize(c,R,mask=mask,u=hi,**kwargs)))
        if candidates:return min(candidates,key=lambda x:x["usage"]),tried
    return None,tried

start=time.monotonic()
if a.corrections:
    results=[]
    key=FOLD["constructions"][-2]["key"]
    variants=[
      ("original",{}),
      ("density1800",dict(rho_f=1800,fibre_w=11/15)),
      ("density1800_E1_Voigt_3GPa",dict(rho_f=1800,fibre_w=11/15,
       E_today_Pa=qi(.6*935e9+.4*3e9)[0],E1=qi(.6*935e9+.4*3e9)[0],
       nu=qi(.6*935e9+.4*3e9)[1],Fc1=220e6/(1-qi(.6*935e9+.4*3e9)[1])))]
    for name,over in variants:
        for R in [15,20,30]:
            for climate in ["ISA","optimistic"]:
                c=props(key,over);kw=dict(climate=climate,thermal_mode="pinned" if R==15 else "independent")
                ep=optimize(c,R,**kw);least,tried=least_audit(c,R,ep,kw)
                record=dict(variant=name,R_m=R,weather=climate,thermal_basis=kw["thermal_mode"],
                            properties=over,endpoint=ep,least=least,subsets=tried)
                results.append(record)
                (ROOT/"CORRECTED-SEARCHES.json").write_text(json.dumps(results,indent=2)+"\n")
                print(name,R,climate,ep["payload_kg"] if ep else None,least["usage"] if least else None,flush=True)
else:
    output=ROOT/f"SEARCH-{a.mode.upper()}.jsonl"
    rows=[("folded",x) for x in ROWS]
    rows += [("040",x) for x in read("owner/RESULTS.json")["rows_040_coating"]]
    with output.open("w") as out:
        for i,(origin,row) in enumerate(rows):
            key=row.get("construction",LABELS[row["case"]]);c=props(key);R=row["R_m"]
            f=row.get("finish","reference040");variant=row.get("variant","primary")
            if a.mode=="pinned" and not (c["core"].startswith("CR-III") and (f=="reference040" or R==15)):continue
            kw=dict(finish=f,variant=variant,climate=row["weather"],floor=row["floor"],thermal_mode=a.mode)
            ep=optimize(c,R,**kw)
            least,tried=least_audit(c,R,ep,kw)
            # Today and named 028b endpoint are separate reoptimizations.
            today=next((x for x in tried if x["mask"]==0),None)
            if today is None:
                t=optimize(c,R,mask=0,**kw);today=dict(payload_kg=t["payload_kg"] if t else None)
            p028=optimize(c,R,mask=11,**kw)
            rec=dict(index=i,origin=origin,construction=key,R_m=R,weather=row["weather"],floor=row["floor"],
                finish=f,variant=variant,thermal_basis=a.mode,
                owner=dict(endpoint_all_kg=row.get("endpoint_all_kg"),
                  least_usage=row.get("least_usage"),least_axes=row.get("least_axes"),
                  endpoint_today_kg=row.get("endpoint_today_kg"),endpoint_028b_kg=row.get("endpoint_028b_kg")),
                endpoint=ep,least=least,subsets=tried,
                endpoint_today_kg=today["payload_kg"],endpoint_028b=p028)
            out.write(json.dumps(rec)+"\n");out.flush()
            if i%12==0:print(i,len(rows),key,R,"elapsed",time.monotonic()-start,flush=True)
print("completed",datetime.now(timezone.utc).isoformat(),"elapsed",time.monotonic()-start,flush=True)
