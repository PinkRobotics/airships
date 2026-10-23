from check_model import *
from check_thermal import js
import time,csv
diff=[];independent=[];timing=[]
def compare(label,field,old,new,basis):
    diff.append(dict(row=label,field=field,owner=old,checker=float(new),delta=float(new)-old,basis=basis))
for origin,rows in [("folded",ROWS),("040",read("owner/RESULTS.json")["rows_040_coating"])]:
    for row in rows:
        key=row.get("construction",LABELS[row["case"]]);c=props(key);R=row["R_m"]
        f=row.get("finish","reference040");v=row.get("variant","primary")
        label=f'{origin}|{key}|{f}|{v}|R{R}|{row["weather"]}|floor{row["floor"]}'
        geo=row.get("endpoint_all_geometry")
        if not geo:continue
        modes=["independent"]
        if c["core"].startswith("CR-III") and (f=="reference040" or R==15):modes.append("pinned")
        for mode in modes:
            result=mechanics(c,R,geo["tf_m"],geo["tc_m"],finish=f,variant=v,climate=row["weather"],thermal_mode=mode)
            for k,old in row.get("endpoint_all_modes",{}).items():compare(label,k,old,result["modes"][k],mode)
            independent.append(dict(row=label,basis=mode,**result))
with (ROOT/"MECHANICS-COMPARISONS.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=list(diff[0]));w.writeheader();w.writerows(diff)
(ROOT/"MECHANICS.json").write_text(json.dumps(independent,default=js,indent=2)+"\n")
summary={}
for x in diff:
    k=x["basis"]+"."+x["field"]
    if k not in summary or abs(x["delta"])>abs(summary[k]["delta"]):summary[k]=x
(ROOT/"MECHANICS-SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
for key in CONS:
    if not CONS[key]["core"].startswith("CR-III") or ("200 F" in key and not key.startswith("Be")):continue
    t=time.monotonic();result=optimize(props(key),30)
    timing.append(dict(key=key,seconds=time.monotonic()-t,point=result))
    print(key,timing[-1]["seconds"],result["payload_kg"] if result else None,flush=True)
(ROOT/"SEARCH-SMOKE.json").write_text(json.dumps(timing,indent=2)+"\n")
