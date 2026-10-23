"""Independent CHECK-057; data-only input, no imported owner implementation."""
import json
import math
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
I = ROOT / "intake"
def read(p):
    return json.loads(p.read_text())
def write(n, x):
    (ROOT / n).write_text(json.dumps(x, indent=2, allow_nan=False) + "\n")
owner = read(I / "mga057.json")
brief = read(I / "RESULTS.json")
u48 = read(I / "files_read/vacuum-mainline048-fold-check040-1020/RESULTS-MLCCAg.json")["rows"]
u40 = read(I / "files_read/vacuum-mainline040-common-account-1020/RESULTS.json")["rows"]
u37 = read(I / "files_read/vacuum-mainline040-fold-037b-1020/RESULTS.json")["rows"]
u52 = read(I / "files_read/vacuum-mainline052-p3-common-account-1020/RESULTS.json")["rows"]
by48 = {x["id"]: x for x in u48}
by40 = {x["id"]: x for x in u40}
by37 = {x["id"]: x for x in u37}
by52 = {(x["R_m"], x["weather"], x["service"]): x for x in u52}
audit = []
def eq(row, field, actual, expected, kind="arithmetic", atol=2e-7, rtol=2e-10):
    if isinstance(actual, (int, float)) and not isinstance(actual, bool) and isinstance(expected, (int, float)):
        ok = math.isclose(actual, expected, rel_tol=rtol, abs_tol=atol)
        difference = actual - expected
    else:
        ok = actual == expected
        difference = None
    audit.append(dict(row=row, field=field, owner=actual, independent=expected,
                      difference=difference, pass_=ok, category=kind, atol=atol, rtol=rtol))
def compare(row, actual, expected, prefix="", kind="arithmetic"):
    if isinstance(expected, dict):
        for k, v in expected.items():
            compare(row, actual.get(k), v, prefix + ("/" if prefix else "") + k, kind)
    elif isinstance(expected, list):
        eq(row, prefix + "/length", len(actual), len(expected), kind)
        for i, (a, b) in enumerate(zip(actual, expected)):
            compare(row, a, b, prefix + "/" + str(i), kind)
    else:
        eq(row, prefix, actual, expected, kind)

# Transcribed independently from NASA Table VI-1, rendered page 10.
table = {
    "TRL 0-2": dict(structure=25, hardware=30, thermal=25, mechanisms=25, electrical_gt15kg=20),
    "TRL 3-5": dict(structure=15, hardware=20, thermal=20, mechanisms=15, electrical_gt15kg=15),
    "TRL 6": dict(structure=10, hardware=15, thermal=15, mechanisms=10, electrical_gt15kg=10),
    "TRL 7": dict(structure=5, hardware=6, thermal=5, mechanisms=5, electrical_gt15kg=5),
    "TRL 8": dict(structure=3, hardware=3, thermal=3, mechanisms=3, electrical_gt15kg=3),
    "TRL 9": dict(structure=0, hardware=0, thermal=0, mechanisms=0, electrical_gt15kg=0),
}
classes = {
    "P2": {
        "faces": ("structure", "calculated", 0), "core": ("structure", "calculated", 0),
        "charged_joining": ("hardware", "estimated", 0),
        "coating": ("thermal", "calculated", .1),
        "mooring_pad": ("structure", "calculated", 0),
        "structural_primer": ("hardware", "estimated", 0),
        "absorbed_water": ("thermal", "calculated", 0),
        "gas": (None, "allocation", 0), "systems": (None, "allocation", 0),
        "extra_service": (None, "allocation", 0), "water": (None, "environment", 0),
        "contamination": (None, "allocation", 0),
        "weather_headroom": (None, "environment", 0),
        "desiccant": ("hardware", "estimated", 0),
    },
    "P3": {
        "SiC_tubes": ("structure", "calculated", 0),
        "joint_sleeves_and_allowance": ("hardware", "estimated", None),
        "joint_bond_and_installation": ("hardware", "estimated", 0),
        "nodes": ("hardware", "estimated", 0),
        "PBO_two_plies": ("structure", "calculated", 0),
        "barrier_and_protection": ("thermal", "calculated", 0),
        "mooring_load_introduction": ("structure", "calculated", 0),
        "systems": (None, "allocation", 0), "vacuum_service": (None, "allocation", 0),
        "gas": (None, "allocation", 0), "exterior_water": (None, "environment", 0),
        "contamination": (None, "allocation", 0),
        "sag_lift_debit": (None, "lift debit", 0),
        "weather_headroom": (None, "environment", 0),
    },
}
for src in [owner, brief]:
    compare("source-table", src["mga_table"]["rows"], table, "mga_table")
    for lead, cs in classes.items():
        for item, (typ, maturity, margin) in cs.items():
            compare("classification/" + lead + "/" + item, src["classification"][lead][item],
                    dict(type=typ, maturity=maturity, own_margin=margin))

def allowance(lead, point, uniform=None, corrected_base=False):
    result = {}
    for k, m in point["bill"].items():
        typ, maturity, included = classes[lead][k]
        if typ is None:
            result[k] = 0.
            continue
        trl = uniform or ("TRL 0-2" if maturity == "estimated" else "TRL 3-5")
        rate = table[trl][typ] / 100
        if k == "joint_sleeves_and_allowance":
            actual = point["actual_sleeves"]
            result[k] = max(0., actual * (1 + rate) - m)
        else:
            base = m / (1 + included) if corrected_base else m
            result[k] = base * max(0., rate - included)
    return result

def evaluate(lead, p):
    hardware = math.fsum(m for k, m in p["bill"].items() if classes[lead][k][0] is not None)
    payload = p["lift_kg"] - math.fsum(p["bill"].values())
    source = allowance(lead, p)
    estimate = allowance(lead, p, "TRL 0-2")
    return dict(mask=p["mask"], axes=p["axes"], payload_kg=payload, hardware_kg=hardware,
                mga_sourced_kg=math.fsum(source.values()), payload_sourced_kg=payload-math.fsum(source.values()),
                mga_sourced_by_item=source, mga_estimated_kg=math.fsum(estimate.values()),
                payload_estimated_kg=payload-math.fsum(estimate.values()), mga_estimated_by_item=estimate,
                flat_tolerable_on_hardware=payload/hardware)

base48 = by48["MLCCAg-R10-ISA-actual-bake70-retained_water-cure_included"]["two_factor_endpoint"]
base_water = base48["bill_kg"]["absorbed_water"]
records = []
extra = []
corrections = []
for lead, source_records in [("P2", owner["P2_records"]), ("P3", owner["P3_records"])]:
    for ri, rec in enumerate(source_records):
        rid = f"{lead}_records/{ri}"
        R = rec["R_m"]
        if lead == "P2":
            upstream = by48[rec["id"]] if rec["source"] == "048" else by40[rec["id"]]
            trials = {p["mask"]: p["solution"] for p in upstream["least"]["endpoint_trials"]}
        else:
            upstream = by52[R, rec["weather"], rec["service"]]
            trials = {p["mask"]: p for p in upstream["endpoints"]}
        new = {k: v for k, v in rec.items() if k not in ["masks", "evaluated", "least_endpoint"]}
        new["lead"] = lead
        new["masks"], new["evaluated"] = [], []
        for mi, p in enumerate(rec["masks"]):
            key = rid + f"/masks/{mi}"
            q = trials[p["mask"]]
            bill = dict(q["bill_kg"])
            if lead == "P2" and rec["source"] != "048":
                area = 4 * math.pi * R**2
                bill["coating"] = area * .00833272
                bill["structural_primer"] = area * .01
                bill["absorbed_water"] = base_water * (R/10)**2
            point = dict(mask=p["mask"], axes=q.get("selected_axes", q.get("axes")),
                         bill=bill, lift_kg=q["lift_kg"])
            point["payload_kg"] = point["lift_kg"] - math.fsum(bill.values())
            if lead == "P3":
                point["actual_sleeves"] = q["joint_actual_sleeves_kg"]
            if lead == "P2" and rec["source"] != "048":
                point["payload_040_kg"] = q["lift_kg"] - math.fsum(q["bill_kg"].values())
            compare(key, p, point, kind="upstream_bill_and_transfer")
            ev = evaluate(lead, point)
            compare(rid+f"/evaluated/{mi}", rec["evaluated"][mi], ev)
            new["masks"].append(point)
            new["evaluated"].append(ev)
            if lead == "P2":
                # An included 10% on CBE must be removed before applying another CBE percentage.
                fixed = allowance(lead, point, corrected_base=True)
                corrected_total = math.fsum(fixed.values())
                corrections.append(dict(row=rid+f"/evaluated/{mi}", field="mga_sourced_kg",
                                        owner=ev["mga_sourced_kg"], independent=corrected_total,
                                        correction_kg=corrected_total-ev["mga_sourced_kg"],
                                        coating_owner_kg=ev["mga_sourced_by_item"]["coating"],
                                        coating_independent_kg=fixed["coating"],
                                        corrected_payload_kg=ev["payload_kg"]-corrected_total,
                                        reason="Included 10% and target allowance must use the same unburdened CBE denominator."))
            # Separate missing allocation growth from environmental uncertainty.
            hidden = sum(bill.get(k, 0) for k in (["systems", "extra_service"] if lead == "P2" else ["systems", "vacuum_service"]))
            extra.append(dict(row=key, lead=lead, R_m=R, weather=rec["weather"],
                              hardware_excluded_as_allocation_kg=hidden,
                              extra_if_20pct_kg=.2*hidden, extra_if_30pct_kg=.3*hidden,
                              payload_with_source_and_30pct_allocations=ev["payload_sourced_kg"]-.3*hidden,
                              hardware_plus_allocation_tolerance=ev["payload_kg"]/(ev["hardware_kg"]+hidden)))
        if "least_endpoint" in rec:
            oe = rec["least_endpoint"]
            target = next(p for p in new["masks"] if p["mask"] == oe["mask"]) if oe else None
            if target:
                compare(rid+"/least_endpoint", oe, target)
            new["least_endpoint"] = target
        records.append(new)

def least(evs, field):
    positive = [p for p in evs if p[field] >= 0]
    if not positive:
        return None
    p = sorted(positive, key=lambda p: (len(p["axes"]), -p[field]))[0]
    return dict(axes=p["axes"], count=len(p["axes"]), payload_kg=p[field])

summaries = []
for ri, r in enumerate(records):
    e = next(p for p in r["evaluated"] if p["mask"] == 15)
    s = dict(lead=r["lead"], source=r["source"], R_m=r["R_m"], weather=r["weather"],
             floor=r.get("floor"), service=r.get("service"),
             all_axes_payload_kg=e["payload_kg"], all_axes_payload_sourced_mga_kg=e["payload_sourced_kg"],
             all_axes_payload_estimated_mga_kg=e["payload_estimated_kg"],
             all_axes_sourced_mga_kg=e["mga_sourced_kg"], all_axes_hardware_kg=e["hardware_kg"],
             flat_tolerable_on_hardware_at_all_axes=e["flat_tolerable_on_hardware"],
             least_set_no_mga=least(r["evaluated"], "payload_kg"),
             least_set_sourced_mga=least(r["evaluated"], "payload_sourced_kg"),
             least_set_estimated_mga=least(r["evaluated"], "payload_estimated_kg"))
    compare("summary/"+str(ri), owner["summary"][ri], s)
    summaries.append(s)

# Recover the report's selected data sources; also explicitly check the source described in prose.
def chosen(lead, radius, weather, intended=False):
    if lead == "P2":
        source = "048" if intended and radius <= 15 else "040 with 048 finish transfer"
        return next(r for r in records if r["lead"] == lead and r["R_m"] == radius and r["weather"] == weather and not r["floor"] and r["source"] == source)
    return next(r for r in records if r["lead"] == lead and r["R_m"] == radius and r["weather"] == weather and r["service"] == "ground")

selected = []
for idx, row in enumerate(brief["floating_with_sourced_mga"]):
    r = chosen(row["lead"], row["R_m"], row["weather"])
    s = next(s for s in summaries if all(s[k] == r.get(k) for k in ["lead", "source", "R_m", "weather", "floor", "service"]))
    compare("RESULTS/floating_with_sourced_mga/"+str(idx), row, {k:s[k] for k in row})
    selected.append(r)

flat = []
mixed = []
for idx, row in enumerate(brief["flat_sensitivity"]):
    r = chosen(row["lead"], row["R_m"], row["weather"])
    e = r["evaluated"][-1]
    x = {k:row[k] for k in ["lead","R_m","weather"]}
    x.update({f"flat_{pct}":e["payload_kg"]-e["hardware_kg"]*pct/100 for pct in range(0,31,5)})
    x["tolerable_flat"] = e["payload_kg"]/e["hardware_kg"]
    compare("RESULTS/flat_sensitivity/"+str(idx), row, x)
    compare("mga057/flat_sensitivity/"+str(idx), owner["flat_sensitivity"][idx], x)
    flat.append(x)
    if row["lead"] == "P2" and row["R_m"] <= 15:
        intended = chosen("P2", row["R_m"], row["weather"], intended=True)["evaluated"][-1]
        for field in ["all_axes_payload_kg", "all_axes_sourced_mga_kg", "all_axes_payload_sourced_mga_kg", "flat_tolerable_on_hardware_at_all_axes"]:
            ef = {"all_axes_payload_kg":"payload_kg","all_axes_sourced_mga_kg":"mga_sourced_kg","all_axes_payload_sourced_mga_kg":"payload_sourced_kg","flat_tolerable_on_hardware_at_all_axes":"flat_tolerable_on_hardware"}[field]
            mixed.append(dict(row=f"P2/R{row['R_m']}/{row['weather']}",field=field,owner=e[ef],independent=intended[ef],difference=e[ef]-intended[ef],reason="Prose says direct048 at R10–15; published table uses040 transfer."))

mature = []
for idx, row in enumerate(brief["maturity_sweep"]):
    r = chosen(row["lead"], row["R_m"], row["weather"])
    point = r["masks"][-1]
    x = {k:row[k] for k in ["lead","R_m","weather"]}
    x["payload_no_mga_kg"] = point["payload_kg"]
    for trl in table:
        x[trl] = point["payload_kg"]-math.fsum(allowance(r["lead"],point,trl).values())
    x["least_mature_row_that_floats"] = next((k for k in table if x[k]>=0), None)
    compare("RESULTS/maturity_sweep/"+str(idx),row,x)
    compare("mga057/maturity_sweep/"+str(idx),owner["maturity_sweep"][idx],x)
    mature.append(x)

transfers = []
for idx, row in enumerate(owner["transfer_check"]):
    src = chosen("P2",row["R_m"],row["weather"],intended=True)["masks"][row["mask"]]
    dst = chosen("P2",row["R_m"],row["weather"])["masks"][row["mask"]]
    x = dict(R_m=row["R_m"],weather=row["weather"],mask=row["mask"],payload_048_kg=src["payload_kg"],
             payload_040_transfer_kg=dst["payload_kg"],diff_kg=dst["payload_kg"]-src["payload_kg"])
    compare("mga057/transfer_check/"+str(idx),row,x)
    compare("RESULTS/transfer_check/"+str(idx),brief["transfer_check_040_to_048"][idx],x)
    transfers.append(x)

cost = []
for idx,row in enumerate(brief["optimism_cost"]):
    lead,R = row["lead"],row["R_m"]
    r = chosen(lead,R,"ISA",intended=True)
    if lead == "P2":
        zero = by48[r["id"]]["least"]["least"]
    else:
        zero = by52[R,"ISA","ground"]["least"]
    e = next(e for e in r["evaluated"] if e["mask"]==zero["mask"])
    u = zero["usage"]
    slope = e["payload_kg"]/(1-u)
    x = dict(lead=lead,R_m=R,least_set=e["axes"],usage_at_zero_payload=u,
             endpoint_payload_kg=e["payload_kg"],kg_per_unit_usage=slope,
             sourced_mga_kg=e["mga_sourced_kg"],usage_needed_with_mga=u+e["mga_sourced_kg"]/slope)
    compare("RESULTS/optimism_cost/"+str(idx),row,x)
    compare("mga057/optimism_cost/"+str(idx),owner["optimism_cost"][idx],x)
    cost.append(x)

items = {}
for (name, reported),lead,mask in zip(brief["R10_item_tables"].items(),["P2","P3"],[11,15]):
    r=chosen(lead,10,"ISA",intended=True)
    p=r["masks"][mask]; e=r["evaluated"][mask]
    for ix,rr in enumerate(reported["rows"]):
        k=rr["item"]; typ,mat,margin=classes[lead][k]
        compare("RESULTS/R10_item_tables/"+lead+"/rows/"+str(ix),rr,
                dict(item=k,kg=p["bill"][k],type=typ,maturity=mat,own_margin=margin,mga_added_kg=e["mga_sourced_by_item"][k]))
    totals=dict(payload_kg=e["payload_kg"],mga_total_kg=e["mga_sourced_kg"],payload_with_mga_kg=e["payload_sourced_kg"],hardware_kg=e["hardware_kg"])
    compare("RESULTS/R10_item_tables/"+lead,reported,totals)
    items[lead]=dict(totals,rows=[dict(item=k,kg=v,mga_added_kg=e["mga_sourced_by_item"][k]) for k,v in p["bill"].items()])

# Transfer-water sensitivity: item mass fractions follow the current bill instead of area-only reference.
transfer_water=[]
for ri,r in enumerate(records):
    if r["lead"] != "P2" or r["source"] == "048":continue
    for pi,p in enumerate(r["masks"]):
        b=p["bill"]
        material_water=.1*(.002*b["charged_joining"]+.001*b["core"]+.01*b["structural_primer"]+.01*b["coating"])
        transfer_water.append(dict(row=f"record/{ri}/mask/{pi}",R_m=r["R_m"],weather=r["weather"],floor=r["floor"],
                                   mask=p["mask"],area_scaled_water_kg=b["absorbed_water"],bill_fraction_water_kg=material_water,
                                   payload_difference_kg=b["absorbed_water"]-material_water,
                                   corrected_payload_kg=p["payload_kg"]+b["absorbed_water"]-material_water))

# A conservative lower bound across all existing P2 subset geometries, independent of which original optimum was selected.
# This is not a global reoptimization; those unconstrained claims remain an NFI.
no_float=[]
for r in records:
    best=max(r["evaluated"],key=lambda e:e["payload_sourced_kg"])
    no_float.append(dict(lead=r["lead"],R_m=r["R_m"],weather=r["weather"],source=r["source"],floor=r.get("floor"),service=r.get("service"),
                         best_mask=best["mask"],best_payload_kg=best["payload_sourced_kg"],any_nonnegative=best["payload_sourced_kg"]>=0))

write("INDEPENDENT-RECORDS.json",records)
write("ARITHMETIC-AUDIT.json",audit)
write("ARITHMETIC-MISMATCHES.json",[a for a in audit if not a["pass_"]])
write("COATING-CBE-CORRECTIONS.json",corrections)
write("SOURCE-SELECTION-MISMATCHES.json",mixed)
write("ALLOCATION-SENSITIVITY.json",extra)
write("TRANSFER-WATER-SENSITIVITY.json",transfer_water)
write("INDEPENDENT-SUMMARIES.json",dict(summary=summaries,flat=flat,maturity=mature,cost=cost,transfer=transfers,R10=items,no_float=no_float))
counts=dict(records=len(records),points=sum(len(r["masks"]) for r in records),comparisons=len(audit),
            mismatches=sum(not a["pass_"] for a in audit),source_selection_fields=len(mixed),
            coating_corrections=len(corrections),all_source_scenarios_negative=all(not r["any_nonnegative"] for r in no_float),
            categories=dict(Counter(a["category"] for a in audit)))
write("COUNTS.json",counts)
print(json.dumps(counts))
print("R10",json.dumps({k:{f:v for f,v in r.items() if f!="rows"} for k,r in items.items()}))
print("TRANSFER RANGE",min(t["diff_kg"] for t in transfers),max(t["diff_kg"] for t in transfers))
print("MISMATCH SAMPLE",json.dumps([a for a in audit if not a["pass_"]][:12]))
