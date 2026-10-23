"""Read-only primary-document retrieval; writes only this seat's output."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from datetime import datetime, timezone
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
DEST=ROOT/"sources"
DEST.mkdir(exist_ok=True)
data=json.loads((ROOT/"inputs/owner/COMPUTE.json").read_text())["sources_used"]
urls={}
for key,value in data.items():
    urls.setdefault(value["url"],[]).append(key)
urls["https://www.grc.nasa.gov/www/k-12/airplane/mflchk.html"]=["nasa_choking"]
urls["https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-of-a-sphere/"]=["nasa_sphere_drag"]
excluded=("wikipedia.org","lmnoeng.com","grahamwindows.com")
def get(url,keys):
    if any(host in urlparse(url).netloc for host in excluded):
        return dict(url=url,keys=keys,status="secondary source not adopted as primary evidence")
    name=keys[0]
    try:
        with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=40) as r:
            content=r.read(30_000_001); final=r.url
        if len(content)>30_000_000:raise ValueError("document exceeds retrieval limit")
        suffix=".pdf" if content.startswith(b"%PDF") else ".html"
        path=DEST/(name+suffix);path.write_bytes(content)
        row=dict(url=url,final_url=final,keys=keys,status="retrieved",path=str(path.relative_to(ROOT)),
                 bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),
                 retrieved=datetime.now(timezone.utc).isoformat())
        if suffix==".pdf":
            textpath=path.with_suffix(".txt")
            proc=subprocess.run(["pdftotext","-layout",str(path),str(textpath)],capture_output=True,text=True)
            row["text_extraction_exit"]=proc.returncode
        return row
    except Exception as exc:
        return dict(url=url,keys=keys,status="failed",error=str(exc))
rows=[]
with ThreadPoolExecutor(max_workers=8) as pool:
    futures=[pool.submit(get,u,k) for u,k in urls.items()]
    for future in as_completed(futures):
        row=future.result();rows.append(row)
        print(row["keys"][0],row["status"],row.get("bytes",row.get("error","")),flush=True)
(ROOT/"SOURCE-INTAKE.json").write_text(json.dumps(rows,indent=2)+"\n")
