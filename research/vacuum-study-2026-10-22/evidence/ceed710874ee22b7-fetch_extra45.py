from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from datetime import datetime,timezone
import hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parent
urls={
 "pach_full":"https://espace.rmc.ca/jspui/bitstream/11264/2883/1/AlekPach_Thesis_Submitted.pdf",
 "prior_full":"https://espace.rmc.ca/jspui/bitstream/11264/961/1/prior26Apr2016thesis.pdf",
}
for section,vol in [("25-571",1),("25-631",1),("25-473",1),("31-27",1),("101-13",2),("101-19",2)]:
    urls["cfr_"+section]=f"https://www.govinfo.gov/content/pkg/CFR-2026-title14-vol{vol}/pdf/CFR-2026-title14-vol{vol}-sec{section}.pdf"
if len(sys.argv)>1:
    year=sys.argv[1]
    urls={k+"_"+year:v.replace("2026",year) for k,v in urls.items() if k.startswith("cfr_")}
    urls["nasa_orifice_Cd"]="https://ntrs.nasa.gov/api/citations/19930002961/downloads/19930002961.pdf"

def retrieve(item):
    name,url=item
    try:
        with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=50) as response:
            content=response.read(150_000_001);final=response.url
        if len(content)>150_000_000:raise ValueError("PDF exceeds 150 MB")
        if not content.startswith(b"%PDF"):raise ValueError("Response is not a PDF")
        path=ROOT/"sources"/(name+".pdf");path.write_bytes(content)
        subprocess.run(["pdftotext","-layout",str(path),str(path.with_suffix(".txt"))],capture_output=True,check=True)
        out=dict(key=name,url=url,final_url=final,path=str(path.relative_to(ROOT)),
                 bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),
                 status="retrieved",at=datetime.now(timezone.utc).isoformat())
    except Exception as exc:
        out=dict(key=name,url=url,status="failed",error=str(exc))
    print(name,out["status"],out.get("bytes",out.get("error")),flush=True)
    return out

with ThreadPoolExecutor(max_workers=8) as pool:
    rows=list(pool.map(retrieve,urls.items()))
(ROOT/("SOURCE-REGULATORY-"+sys.argv[1]+".json" if len(sys.argv)>1 else "SOURCE-ADDITIONAL.json")).write_text(json.dumps(rows,indent=2)+"\n")
