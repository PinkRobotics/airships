#!/usr/bin/env python3
"""CHECK-030d: this seat's own non-P2 checks of 030d (no 030d code read or run). Writes OWN-CHECKS.json.

- R30 beryllium supply: faces at 040's R30 ISA named endpoint and least point, from this seat's own 040-account run
  (MAINLINE-049's COMPUTE.json, which reproduces 040's 12 rows), against 433 t and 430 t.
- Weibull scales: weakest link with m = 10, sigma_req = 3.9 GPa x (ln(1 - Pf_3.9) / ln(1 - Pf_target))^(1/m).
- Intake: every mainline/check report the queue ingested between 030c's snapshot and 030d's intake, against 030d's
  folded list; the 408 pins; 030d's snapshot copies against the sources' pinned sha256; the card's links.
- Pending: 030d's PENDING list against the queue at 030d's filing and now.
- Counts: rows in REGISTER.json and rows in NFI.json against 104 and 1553; 98 + 6 and 961 + 583 + 9.
- Typography: tokens joined or broken in CARD.md."""
import datetime
import hashlib
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = "unpublished-local-ref:34191d50bbd0f9f9"
Q = "unpublished-local-ref:ab52dba26d6cc3a7"
C49 = "evidence/5750025a1b213d52-COMPUTE.json"
T030C = datetime.datetime.fromisoformat("2026-10-20T04:03:32-07:00")
INTAKE_AT = datetime.datetime.fromisoformat("2026-10-20T05:46:07.751385-07:00")
FILED_AT = datetime.datetime.fromisoformat("2026-10-20T05:51:14-07:00")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    out = {"at": datetime.datetime.now().astimezone().isoformat(), "basis": __doc__, "items": []}
    add = out["items"].append
    # supply
    C = json.load(open(C49))
    be = next(r for r in C["rows"] if r["case"].startswith("Be SR-200") and r["R_m"] == 30 and r["weather"] == "ISA"
              and not r["floor"])
    fn, fl = be["faces_at_028b_endpoint_kg"] / 1000, be["least"]["faces_kg"] / 1000
    for lab, mine, card, tol in (("R30 named-endpoint Be faces, t", fn, 102.230791, 5e-7),
                                 ("R30 least-point Be faces, t", fl, 103.146242, 5e-7),
                                 ("share of 433 t, %", fn / 433 * 100, 23.610, 5e-4), ("share of 430 t, %", fn / 430 * 100, 23.775, 5e-4)):
        add({"line": "15/120", "item": lab, "card": card, "mine": mine, "ok": abs(mine - card) <= tol})
    # Weibull scales
    def scale(pf, target, m=10, s=3.9):
        return s * (math.log1p(-pf) / math.log1p(-target)) ** (1 / m)
    for lab, pf, tgt, card in (("043 f5 member scale for Pf 1e-6, GPa", 0.002524170, 1e-6, 8.53751),
                               ("043 019 member scale for Pf 1e-6, GPa", 0.002142827, 1e-6, 8.39866),
                               ("051 f5 member scale for Pf 1e-3, GPa", 0.002524170, 1e-3, 4.278678),
                               ("051 019 member scale for Pf 1e-3, GPa", 0.002142827, 1e-3, 4.209090),
                               ("051 f5 1 cm3 scale for Pf 1e-3, GPa", 0.991132667, 1e-3, 9.088382),
                               ("051 019 1 cm3 scale for Pf 1e-3, GPa", 0.979046202, 1e-3, 8.907641)):
        v = scale(pf, tgt)
        add({"line": "31/224/228", "item": lab, "card": card, "mine": v, "ok": abs(v - card) < 5e-6})
    # intake, pins, snapshots, links
    it = json.load(open(f"{D}/INTAKE.json"))
    folded = [r["id"] for r in it["reports"]]
    window, after = [], []
    with os.scandir(Q) as sc:
        for e in sc:
            if not (e.name.startswith("rpt-") and e.name.endswith(".json")):
                continue
            try:
                d = json.load(open(e.path))
            except (OSError, ValueError):
                continue
            ing = d.get("ingested")
            if not ing:
                continue
            t = datetime.datetime.fromisoformat(ing)
            if T030C <= t <= INTAKE_AT:
                window.append(d["id"])
            elif t > INTAKE_AT:
                after.append((ing, d["id"]))
    missed = [i for i in window if i not in folded and i != "rpt-1228-mainline030c-design-register-1020"]
    add({"line": "19", "item": "reports folded vs reports ingested in the window", "card": 18, "mine": len(folded),
         "missed": missed, "ok": len(folded) == 18 and not missed})
    npins, same, differ, uncopied, kinds = 0, 0, [], 0, {}
    for i in folded:
        rep = json.load(open(f"{Q}/{i}.json"))
        sd = f"{D}/snapshots/{i}"
        have = set(os.listdir(sd)) if os.path.isdir(sd) else set()
        for a in rep.get("artifacts", []):
            npins += 1
            b = os.path.basename(a["path"])
            if b not in have:
                uncopied += 1
                ext = os.path.splitext(b)[1]
                kinds[ext] = kinds.get(ext, 0) + 1
            elif sha(f"{sd}/{b}") == a["sha256"]:
                same += 1
            else:
                differ.append(f"{i}/{b}")
    add({"line": "252", "item": "direct pins of the 18 reports", "card": 408, "mine": npins, "ok": npins == 408})
    add({"line": "-", "item": "030d snapshot copies against the sources' pinned sha256", "identical": same, "differing": differ,
         "not_copied": uncopied, "not_copied_by_type": kinds, "ok": not differ})
    card = open(f"{D}/CARD.md").read()
    links = re.findall(r"\]\(([^)]+)\)", card)
    unresolved = [x for x in links if not x.startswith("http") and not os.path.exists(os.path.join(D, x))]
    add({"line": "all", "item": "card links that resolve", "links": len(links), "unresolved": unresolved, "ok": not unresolved})
    # pending list
    P = json.load(open(f"{D}/PENDING.json"))
    pend = [p["item"] for p in P if p["status"] == "PENDING"]
    add({"line": "248", "item": "PENDING at filing", "card": pend, "filed_since": sorted(after), "ok": True})
    # counts
    R = json.load(open(f"{D}/REGISTER.json"))
    N = json.load(open(f"{D}/NFI.json"))
    cov = json.load(open(f"{D}/REGISTER-COVERAGE.json"))
    add({"line": "19", "item": "register rows", "card": 104, "mine": len(R["rows"]),
         "sum": cov["baseline_register_rows_preserved"] + cov["new_register_rows"], "ok": len(R["rows"]) == 104})
    add({"line": "19", "item": "attributed findings", "card": 1553, "mine": len(N["rows"]),
         "sum": cov["baseline_findings_preserved"] + cov["new_source_findings"] + cov["new_authored_findings"],
         "ok": len(N["rows"]) == 1553})
    G = json.load(open(f"{D}/GROUND-FIRST.json"))
    ext = [r["route"] for r in G.get("extensions_030d", [])]
    add({"line": "244", "item": "added grounding routes", "card_names": 4, "mine": ext, "found": len(ext),
         "note": "the card names four additions; GROUND-FIRST.json carries five (the fifth is 052's)", "ok": len(ext) == 4})
    # typography
    pats = [r"2, 027, 245", r"041d amage", r"f5stress", r"3\.27f4factor", r"At7149", r"325comparisons", r"Kapton, not the model's\.09",
            r"a4889\.444", r"A268\.099", r"31NFI", r"AtR30", r"At500", r"aboutISA", r"colderh 2", r"fromP2", r"theP3", r"Full052",
            r"Partial051", r"corrected:458", r"Pf\.000947798", r"Pf\.824296"]
    found = {p: len(re.findall(p, card)) for p in pats}
    add({"line": "various", "item": "joined or broken tokens in CARD.md", "found": {k: v for k, v in found.items() if v},
         "ok": False})
    out["sources"] = {"030d_card": {"path": f"{D}/CARD.md", "sha256": sha(f"{D}/CARD.md")}, "own_040_run": {"path": C49, "sha256": sha(C49)}}
    with open(os.path.join(HERE, "OWN-CHECKS.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "OWN-CHECKS.json.tmp"), os.path.join(HERE, "OWN-CHECKS.json"))
    for x in out["items"]:
        print(x["ok"], x["item"], {k: v for k, v in x.items() if k in ("card", "mine", "missed", "differing", "unresolved")})


if __name__ == "__main__":
    main()
