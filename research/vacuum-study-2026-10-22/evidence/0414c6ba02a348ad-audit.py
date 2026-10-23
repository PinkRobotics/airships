"""Full non-code point arithmetic audit, with field-level differences."""
from pathlib import Path
import json, hashlib, collections, math
import model as m

ROOT=Path(__file__).resolve().parent
FILES=["RESULTS.json","DEBIT-COSTS.json","SENSITIVITIES.json","QUALIFICATION-AUDIT.json",
       "BASIS-RECONCILIATION.json","SEARCH-VERIFICATION.json","comparison-037/RESULTS.json"]

def findpoints(o,path=""):
    if isinstance(o,dict):
        if "signed_payload_kg" in o and "geometry" in o:
            yield path,o
        else:
            for k,v in o.items():yield from findpoints(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):yield from findpoints(v,path+"/"+str(i))

def leaves(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):yield from leaves(v,path+"/"+str(i))
    else:yield path,o

def normalsettings(p):
    s=dict(p["settings"])
    if "bond_model" not in s:
        s.update(bond_model="rigid037",scarf_ratio=30.)
    return s

def inputs(p):
    return dict(R=p["R_m"],tf=p["geometry"]["tf_m"],tc=p["geometry"]["tc_m"],
                mask=p["mask"],u=p["usage"],settings=normalsettings(p))

def main():
    points={}; refs=[]
    for f in FILES:
        data=json.loads((ROOT/"owner"/f).read_text())
        for path,p in findpoints(data):
            args=inputs(p)
            key=hashlib.sha256(json.dumps(args,sort_keys=True).encode()).hexdigest()
            points.setdefault(key,dict(key=key,inputs=args,owner=p,refs=[]))["refs"].append(f+path)
            refs.append((f+path,key))
    checks=0; mismatches=[]; missing=[]; mismatch_fields=collections.Counter()
    evaluated=[]
    with (ROOT/"POINT-ARITHMETIC.jsonl").open("w") as out:
        for key,row in points.items():
            p=row["owner"]; expected=m.evaluate(**row["inputs"])
            expected=json.loads(json.dumps(expected,default=m.serial))
            actual=dict(leaves(p)); n=0;bad=[]
            for path,value in leaves(expected):
                if path not in actual:
                    if "/core_cell_wall" not in path:missing.append((row["refs"][0],path))
                    continue
                old=actual[path]
                if isinstance(value,bool):
                    ok=value==old;delta=None
                elif isinstance(value,(float,int)) and isinstance(old,(float,int)):
                    delta=old-value
                    ok=math.isclose(old,value,rel_tol=1e-9,abs_tol=1e-7)
                elif old is None:
                    missing.append((row["refs"][0],path,"owner null"));continue
                else:continue
                checks+=1;n+=1
                if not ok:
                    record=dict(point_key=key,reference=row["refs"][0],field=path,
                                owner=old,independent=value,owner_minus_independent=delta)
                    mismatches.append(record);bad.append(record);mismatch_fields[path]+=1
            out.write(json.dumps(dict(key=key,refs=row["refs"],checks=n,differences=bad,
                                     independent=expected),separators=(",",":"))+"\n")
            evaluated.append(dict(key=key,refs=row["refs"],inputs=row["inputs"],
                                  owner_payload_kg=p["signed_payload_kg"],
                                  owner_least_SF=p["least_shell_and_thermal_SF"]))
    result=dict(unique_points=len(points),point_occurrences=len(refs),checked_fields=checks,
                matched_fields=checks-len(mismatches),differences=len(mismatches),
                mismatch_fields=mismatch_fields,missing_fields=missing)
    (ROOT/"ARITHMETIC-SUMMARY.json").write_text(json.dumps(result,indent=2)+"\n")
    (ROOT/"ARITHMETIC-DIFFERENCES.json").write_text(json.dumps(mismatches,indent=2)+"\n")
    (ROOT/"POINT-INPUTS.json").write_text(json.dumps(evaluated,indent=2)+"\n")
    print(json.dumps(result,indent=2)[:8000],flush=True)

if __name__=="__main__":main()
