import hashlib
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def digest(p):
    b=p.read_bytes()
    return dict(path=str(p.resolve()),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))


def main():
    checks=[]
    for label,path,key in [("assignment",QUEUE/(ORDER+".json"),"artifacts"),
                           ("owner report",QUEUE/(REPORT+".json"),"artifacts"),
                           ("owner inputs",OWNER/"INPUTS.json","pins")]:
        d=json.loads(path.read_text())
        for pin in d[key]:
            actual=digest(Path(pin["path"]))
            checks.append(dict(origin=label,expected=pin,actual=actual,
                               ok=all(actual[k]==pin[k] for k in ["sha256","bytes"]),
                               code_hash_only=Path(pin["path"]).suffix==".py"))
    assert all(x["ok"] for x in checks)
    sources=[]
    urls={s["id"]:s["url"] for s in json.loads((OWNER/"INPUTS.json").read_text())["sources"]}
    urls.update({"TA02":"https://ntrs.nasa.gov/api/citations/20170005857/downloads/20170005857.pdf",
                 "TA07":"https://ntrs.nasa.gov/api/citations/20190000441/downloads/20190000441.pdf",
                 "STA8.1":"https://ntrs.nasa.gov/api/citations/20180001127/downloads/20180001127.pdf",
                 "ETTA2":"https://ntrs.nasa.gov/api/citations/20180006174/downloads/20180006174.pdf",
                 "Hilburger2012":"https://ntrs.nasa.gov/api/citations/20120008172/downloads/20120008172.pdf",
                 "Hilburger2018":"https://ntrs.nasa.gov/api/citations/20180006178/downloads/20180006178.pdf",
                 "SP-8007-2020":"https://ntrs.nasa.gov/citations/20205011530"})
    for p in sorted((OUT/"sources").iterdir()):
        record=digest(p)
        if p.suffix==".pdf":
            record.update(url=urls[p.stem],acquisition="Direct NTRS download" if p.stem in ["IDH","CR-62257"] else
                          "Archived primary PDF copied read-only from owner's known lit039/lit035 scratch paths; no code accessed")
        sources.append(record)
    result=dict(unit="vacuum-mainline039-check-1020",order=ORDER,owner_report=REPORT,
                checked_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(),
                documentary_roots=[digest(QUEUE/(ORDER+".json")),digest(QUEUE/(REPORT+".json"))],
                pin_checks=checks,pin_count=len(checks),all_pins_match=True,
                primary_sources_and_extractions=sources,
                scope="No owner source code opened, imported or executed. Code bytes hashed solely for report-pin verification. No seat contact.",
                download_note="SP-8032 mirror returned HTTP 403 in this check; archived identical PDF hash matches owner's pin.")
    (OUT/"INPUTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(pins=len(checks),all_match=True,source_files=len(sources)),indent=2))


if __name__=="__main__":
    main()
