"""Prepare the immutable manifest and one atomic-outbox candidate."""
from pathlib import Path
from datetime import datetime
import hashlib
import json

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def read(name):
    return json.loads((ROOT/name).read_text())


def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

now = datetime.now().astimezone()
timing = read("TIMING.json")
timing["completed"] = now.isoformat()
timing["elapsed_wall_seconds"] = (now-datetime.fromisoformat(timing["started"])).total_seconds()
timing["completion_scope"] = "Scientific work, assembly and delivery preparation; outbox validation follows."
save("TIMING.json", timing)
files = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.name == "MANIFEST.json" and path.parent == ROOT:
        continue
    if "__pycache__" in path.parts or path.suffix == ".pyc":
        continue
    files.append(dict(**pin(path), relative=str(path.relative_to(ROOT))))
save("MANIFEST.json", dict(schema=1, unit=UNIT, generated_at=now.isoformat(),
                           file_count=len(files), excludes=["MANIFEST.json (self)", "__pycache__"],
                           files=files))
body = f"""MAINLINE-053 complete; QUESTIONABLE/PROJECTION. Owner convection-floor and core-gap terms explain the discrepancy. All 118,499 independent comparisons pass. The routed owner boundary reply is incorporated; its 46 supplied reference entries also match.

Four explicit R10–30 thermal alternatives, 9,640 thickness rows and 52 finish screens are filed. Physical boundary and installed-hull qualification remain open; no single validated temperature table is claimed.

All 5,760 endpoint witnesses across 360 accounts were evaluated. No endpoint float sign, minimum optimism-axis choice or tied set changes. Largest resized payload loss is 4.388925 kg. Under forced/conduction, cure-inclusive retained-floor/bake ISA payloads are 118.088578/325.606508/808.781562 kg at R10/12/15; optimistic values are −29.863021/62.148681/294.119183 kg.

All 288 frozen scarf comparisons cross below one (largest deficit 0.0366%); 85 frozen global crossings also occur. Resizing restores the stated constraints. Free-edge, wall and multilayer finish screens remain passing. All mass debits and inherited qualifications carry.

31,460 accounting checks and {validation['checks']} delivery checks pass. Manifest pins {len(files)} files; all 142 frozen inputs match. One later COMMON amendment adds the simjob rule already followed. Nine new nonblocking NFI groups and six inherited registers remain open.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]