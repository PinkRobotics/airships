"""Read primary source documents, retaining HTTP and custody metadata."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent
DEST = ROOT/"sources"
DEST.mkdir(exist_ok=True)
URLS = {
    "whitaker1972": "https://www.researchgate.net/profile/Stephen-Whitaker-3/publication/229709417_Forced_convection_heat_transfer_correlations_for_flow_in_pipes_past_flat_plates_single_cylinders_single_spheres_and_for_flow_in_packed_beds_and_tube_bundles/links/59d73bda0f7e9b42a6b0694a/Forced-convection-heat-transfer-correlations-for-flow-in-pipes-past-flat-plates-single-cylinders-single-spheres-and-for-flow-in-packed-beds-and-tube-bundles.pdf",
    "nasa_honeycomb1968": "https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf",
    "nasa_honeycomb1978": "https://ntrs.nasa.gov/api/citations/19780023143/downloads/19780023143.pdf",
    "nasa_ccag2018": "https://ntrs.nasa.gov/api/citations/20180002012/downloads/20180002012.pdf",
    "hexcel_criii": "https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf",
    "coat_recipe": "https://patents.google.com/patent/US11391493B2/en",
    "faa_heat_balance": "https://ntrs.nasa.gov/api/citations/19730017242/downloads/19730017242.pdf",
}


def fetch(item):
    key, url = item
    result = dict(key=key, url=url, retrieved_at=datetime.now(timezone.utc).isoformat())
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=50) as response:
            data = response.read(50_000_001)
            if len(data) > 50_000_000:
                raise ValueError("source exceeds 50 MB intake limit")
            result.update(http_status=response.status, final_url=response.url)
        pdf = data.startswith(b"%PDF")
        path = DEST/(key+(".pdf" if pdf else ".html"))
        path.write_bytes(data)
        result.update(path=str(path.relative_to(ROOT)), bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest(), status="retrieved",
                      is_pdf=pdf)
        if pdf:
            text_path = path.with_suffix(".txt")
            done = subprocess.run(["pdftotext", "-layout", str(path), str(text_path)],
                                  capture_output=True)
            result["text_extraction_exit"] = done.returncode
    except Exception as error:
        result.update(status="failed", error=str(error))
    return result


with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(fetch, URLS.items()))
(ROOT/"SOURCE-INTAKE.json").write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps([{k: r[k] for k in ["key", "status", "bytes", "error"] if k in r}
                  for r in results], indent=2))
