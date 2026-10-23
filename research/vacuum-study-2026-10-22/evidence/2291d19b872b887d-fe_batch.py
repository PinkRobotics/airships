from pathlib import Path
import json
from fe_check import path_run

ROOT=Path(__file__).resolve().parent
labels=["S1-be-sphere-d16","S2-be-sphere-d9","S3-be33-sphere-d16",
        "S4-al-sphere-d16","S5-al-sphere-d9",
        "C1-be-cap1500-d16","C2-be-cap2000-d16","C3-be-cap2500-d16","C4-be-cap3000-d16",
        "C5-al-cap2000-d16","C6-al-cap2500-d16","C7-al-cap3000-d16","C8-al-cap1500-d16",
        "D1-be-sphere-d1","D2-be-sphere-d2","D4-be-sphere-d4","D6-be-sphere-d6",
        "R30a-be-sphere","R30b-be-cap3000","R30c-be-cap2500"]
summary=[]
for label in labels:
    existing=ROOT/"fe-runs"/(label+".json")
    if existing.exists() and json.loads(existing.read_text()).get("status")=="complete":
        r=json.loads(existing.read_text())
    else:
        r=path_run(label)
    summary.append({k:r[k] for k in ("label","limit_kPa","gamma_H_elastic",
                                    "relative_limit_difference","crossings_kPa","elapsed_seconds")})
    (ROOT/"FE-BATCH.json").write_text(json.dumps(summary,indent=2)+"\n")
aliases={"L1-be-sphere-d16-loc":"S1-be-sphere-d16",
         "L3-be-cap2500-d16-loc":"C3-be-cap2500-d16",
         "L4-be-cap3000-d16-loc":"C4-be-cap3000-d16"}
for alias,original in aliases.items():
    a=json.loads((ROOT/"intake/owner-runs"/(alias+".json")).read_text())
    b=json.loads((ROOT/"intake/owner-runs"/(original+".json")).read_text())
    assert {k:v for k,v in a["args"].items() if k!="label"}=={k:v for k,v in b["args"].items() if k!="label"}
    assert [r["pole_dz_mm"] for r in a["path"]]==[r["pole_dz_mm"] for r in b["path"]]
(ROOT/"FE-ALIASES.json").write_text(json.dumps(aliases,indent=2)+"\n")
print("Completed all 20 distinct models and verified 3 exact-input aliases.",flush=True)
