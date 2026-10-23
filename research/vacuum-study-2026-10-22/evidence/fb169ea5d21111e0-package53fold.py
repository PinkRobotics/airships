"""Validate the addendum and prepare its one queue completion."""
from pathlib import Path
from datetime import datetime
import ast
import hashlib
import json
import re

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def load(path):
    def reject(value):
        raise ValueError(value)
    return json.loads(path.read_text(), parse_constant=reject)


def save(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))


outbox = WORKSPACE/".ship/outbox"
assert not (outbox/(REPORT_ID+".json")).exists()
validation = load(ROOT/"VALIDATION.json")
assert validation["failed"] == 0
checks = []


def check(label, passed, **detail):
    checks.append(dict(check=label, passed=bool(passed), **detail))


for p in ROOT.glob("*.json"):
    if p.name in ["MANIFEST.json", "PACKAGE-CHECK.json"]:
        continue
    load(p)
    check("strict JSON", True, path=p.name)
for p in ROOT.glob("*.py"):
    ast.parse(p.read_text())
    check("script syntax", True, path=p.name)
for r in load(ROOT/"UPSTREAM-REPORT-PIN-CHECKS.json"):
    current = pin(Path(r["path"]))
    check("completed checker artifact remains pinned",
          all(current[k] == r[k] for k in ["sha256", "bytes"]), path=r["path"])
for r in load(ROOT/"SOURCE-RETRIEVAL.json"):
    if r["retrieved"]:
        actual = pin(Path(r["path"]))
        check("new primary source pin", all(actual[k] == r[k] for k in ["sha256", "bytes"]),
              source=r["id"])

note = WORKSPACE/".ship/notes"/(NOTE_ID+".md")
note.write_text("""# MAINLINE-053 completed CHECK-048 fold

[Addendum](../work/outputs/vacuum-mainline053-fold-check048-complete-1020/CARD.md) ·
[Physical judgment](../work/outputs/vacuum-mainline053-fold-check048-complete-1020/PHYSICAL-JUDGMENT.json) ·
[Corrections](../work/outputs/vacuum-mainline053-fold-check048-complete-1020/CORRECTIONS.json)

Completed CHECK-048 confirms the thermal reconstruction from the owner's disclosed terms. Its 103,714 thermal comparisons include 26 separately reconciled legacy entries; 1,714,368 is the full-account tighter comparison count. Thirty-six equivalent primary accounts agree within 0.000062 kg, including least sets/usages.

Neither the owner's numerical coefficients nor CHECK-040's omitted convection/radiation terms establish a physically best-supported installed boundary. New high-Re/large-sphere literature and dimensionless diagnostics reinforce the existing qualification limits. Keep all four previously computed thermal alternatives. No new solver run or payload credit is justified.

The established maximum resized payload cost remains 4.388925 kg, with zero thermal-only float or least-set changes. Cure-inclusion changes reported by CHECK-048 are separate. Adopt SolarWhite mass/optical source correction, classical CCAg emittance-statistic correction and twelve null-field floating witnesses. Original MAINLINE-053 files remain immutable.

Nine MAINLINE-053 physical NFI groups carry. Completed CHECK-048's numerical/coverage/execution closures and remaining evidence/correction dispositions replace its partial status in this fold. Installed hull SF remains unknown. No live job, named successor or out-of-band contact.

Closes ord-admiral-rr2-mainline053-fold-chk048-complete-1020.
""")
for doc in [ROOT/"CARD.md", note]:
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", doc.read_text()):
        if "://" not in target:
            check("local artifact link", (doc.parent/target).exists(), path=str(doc), target=target)
    active = None
    for line in doc.read_text().splitlines():
        if line.startswith("|"):
            count = len(re.split(r"(?<!\\)\|", line))-2
            if active is None:
                active = count
            check("Markdown table columns", count == active, path=str(doc), line=line)
        else:
            active = None

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

The owner includes relevant buoyancy and core-radiation mechanisms, but its coefficients are not established as physically best supported. CHECK-040's omissions are likewise unqualified. Primary forced-convection, large-sphere and bonded-honeycomb evidence, plus explicit Re/Ra/Ri diagnostics, support retaining the four conditional alternatives and the open physical-boundary NFI.

Existing consequences remain: maximum resized payload cost 4.388925 kg; no thermal-only endpoint float or minimum/tied-set changes. Frozen scarf/global crossings and restored resized limits retain their previous disposition. CHECK-048's cure-inclusion float/set changes are a separate mechanical comparison.

Adopt SolarWhite .285 kg/m² and .18/.89 Al-source correction, classical CCAg normal-emittance/citation correction, and twelve null-field floating witnesses. Selected multilayer inputs and all mass debits remain unchanged.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]