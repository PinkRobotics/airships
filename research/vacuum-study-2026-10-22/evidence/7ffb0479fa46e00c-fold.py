#!/usr/bin/env python3
"""Explicit 037b as-designed/fix comparison on the immutable 040 account."""
import csv
import hashlib
import importlib.util
import json
import math
import time
from dataclasses import replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "vacuum-mainline040-common-account-1020"


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def pin(p):
    p = p.resolve()
    b = p.read_bytes()
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))


# Keep all equation evaluations and their reported safety factors unchanged.
# The optional filter only allows a failed-edge design to be priced; it cannot
# turn shell_and_thermal_pass or modeled_assembly_pass into true.
source = (BASE / "model.py").read_text()
source = source.replace("B = Path(__file__).resolve().parent",
                        f"B = Path({str(BASE)!r})")
source = source.replace("    edge_scarf_interaction: bool = False",
                        "    edge_scarf_interaction: bool = False\n"
                        "    require_free_edge_pass: bool = True")
source = source.replace(
    "feasible = upper_good & (thermalsf >= 1-2e-10)",
    "feasible = upper_good & ((thermalsf >= 1-2e-10) if "
    "s.require_free_edge_pass else np.ones_like(thermalsf, dtype=bool))")
(HERE / "fold_model.py").write_text(source)
import fold_model as m

started = time.monotonic()
original = json.loads((BASE / "RESULTS.json").read_text())
rows, checks = [], []
edge_bounds = []
kb = .5 * 67e9 * m.C["rho"] / 2700
for r in [10, 12, 15, 20, 30]:
    cold = m.np.array(m.THERMAL[str(r)]["min_outer_K"])
    hot = m.np.array(m.THERMAL[str(r)]["max_outer_K"])
    dt = 1.002 * m.np.maximum(abs(394.2611111111111-hot),
                             abs(394.2611111111111-cold))
    sf = 25*6894.757293168361 / (
        (23.6e-6-11.3e-6)*dt*m.np.sqrt(2*kb*m.C["Gc_Pa"]))
    edge_bounds.append(dict(R_m=r, maximum_minimum_strength_edge_SF=float(sf.max()),
                            minimum_minimum_strength_edge_SF=float(sf.min()),
                            all_geometries_fail=bool(sf.max() < 1)))
    assert sf.max() < 1

for row in original["rows"]:
    fix = row["two_factor_endpoint"]
    sf = m.Settings(**fix["settings"])
    old = replace(sf, cure_temperature_K=394.2611111111111, scarf_ratio=30.,
                  require_free_edge_pass=False)
    r = row["R_m"]
    asdesigned = m.optimize(r, 11, 1., old)
    assert asdesigned is not None
    same = m.payload_at(r, fix["geometry"]["tf_m"], fix["geometry"]["tc_m"],
                        11, 1., old, True)
    reproduced = m.payload_at(r, fix["geometry"]["tf_m"],
                              fix["geometry"]["tc_m"], 11, 1., sf, True)
    assert abs(reproduced["signed_payload_kg"]-fix["signed_payload_kg"]) < 1e-8
    assert not asdesigned["modeled_assembly_pass"]
    assert not asdesigned["shell_and_thermal_pass"]
    assert asdesigned["modes"]["thermal_core_interface_screen"] < 1
    assert min(v for k, v in asdesigned["modes"].items()
               if k != "thermal_core_interface_screen") >= 1-2e-7
    assert abs(sum(asdesigned["bill_kg"].values()) +
               asdesigned["signed_payload_kg"]-asdesigned["lift_kg"]) < 1e-8
    checks.append(dict(id=row["id"], fix_payload_reproduction=True,
                       as_designed_edge_failure_preserved=True,
                       other_scalar_modes_pass=True, mass_closure=True))
    rows.append(dict(
        id=row["id"], R_m=r, weather=row["weather"], floor=row["floor"],
        pad=row["pad"], vented=row["vented"],
        as_designed=dict(
            strict_status="No admissible geometry: minimum free-edge strength fails throughout search domain.",
            least_optimism_set=None,
            conditional_endpoint=asdesigned,
            at_fix_geometry=same,
            conditional_price_only=True),
        fix=dict(endpoint=fix, least=row["least"]["least"],
                 least_status=row["least"]["status"]),
        delta_fix_minus_as_designed_kg=(
            fix["signed_payload_kg"]-asdesigned["signed_payload_kg"])))
    print(row["id"], round(asdesigned["signed_payload_kg"], 3),
          round(fix["signed_payload_kg"], 3), flush=True)
    dump("RESULTS.json", dict(complete=False, rows=rows))

dump("RESULTS.json", dict(
    tag="QUESTIONABLE / PROJECTION", complete=True, rows=rows,
    endpoint="028b endpoints: full gamma and Q=.82, E=290 GPa/Fcy=345 MPa, .015 lb/ft2 film/interface.",
    strict_as_designed_edge_bounds=edge_bounds,
    conditional_pricing="Only free-edge feasibility filter relaxed for pricing; actual minimum-strength failure stays in every recorded mode and pass flag.",
    elapsed_s=time.monotonic()-started))
dump("VALIDATION.json", dict(passed=True, configurations=len(rows),
                            checks=checks, edge_bounds=edge_bounds))
with (HERE / "PAIRED-ROWS.csv").open("w") as f:
    names = ["id", "bond", "cure_K", "scarf_ratio", "tf_mm", "tc_mm",
             "signed_payload_kg", "cure_compression_MPa", "minimum_edge_SF",
             "typical_edge_SF", "scarf_SF", "priced_with_edge_failure",
             "modeled_assembly_pass"]
    writer = csv.DictWriter(f, fieldnames=names)
    writer.writeheader()
    for row in rows:
        for name, x in [("as-designed", row["as_designed"]["conditional_endpoint"]),
                        ("fix", row["fix"]["endpoint"])]:
            writer.writerow(dict(
                id=row["id"], bond=name, cure_K=x["settings"]["cure_temperature_K"],
                scarf_ratio=x["settings"]["scarf_ratio"],
                tf_mm=1000*x["geometry"]["tf_m"], tc_mm=1000*x["geometry"]["tc_m"],
                signed_payload_kg=x["signed_payload_kg"],
                cure_compression_MPa=x["properties"]["added_cure_compression_Pa"]/1e6,
                minimum_edge_SF=x["modes"]["thermal_core_interface_screen"],
                typical_edge_SF=1.4*x["modes"]["thermal_core_interface_screen"],
                scarf_SF=x["modes"]["scarf_average_shear_screen"],
                priced_with_edge_failure=name == "as-designed",
                modeled_assembly_pass=x["modeled_assembly_pass"]))

text = [
    "# MAINLINE-040 / 037b explicit bond rows",
    "",
    "QUESTIONABLE / PROJECTION. This addendum closes the late fold order. The filed "
    "040 account already uses the 200 °F cure and 30.341397:1 scarf fix. This "
    "addendum supplies its explicitly requested as-designed counterpart: 250 °F "
    "cure, 30:1 scarf, the compliant-core 037b model, and the same complete bill.",
    "",
    "The as-designed bond field survives cure in 037b's compliant-core model. "
    "The minimum-strength free-edge screen fails (about 0.83); the typical-strength "
    "screen is about 1.16. Those statements concern different locations and "
    "strength statistics. No as-designed row passes the complete 040 screen, "
    "regardless of the four optimism axes. A longer scarf alone cannot cure this "
    "edge failure. The fixed row retains approximately 1.07 minimum edge factor.",
    "",
    "For comparison, as-designed shell thicknesses are reoptimized with only the "
    "free-edge feasibility filter relaxed. This gives a conditional mass price, "
    "not an accepted float. Every reported safety factor and assembly flag keeps "
    "the failure. The fixed row is reproduced from immutable 040 output. All "
    "120 account combinations have both rows in PAIRED-ROWS.csv, plus a common "
    "fixed-geometry comparison in RESULTS.json.",
    "",
    "|R (m)|Weather|Account|As-designed conditional payload (kg)|Fix payload (kg)|As-designed edge SF|Fix edge SF|",
    "|---:|---|---|---:|---:|---:|---:|"]
for row in rows:
    if row["pad"] != "heavy70" or not row["vented"]:
        continue
    a, b = row["as_designed"]["conditional_endpoint"], row["fix"]["endpoint"]
    text.append(f"|{row['R_m']}|{row['weather']}|{'floor' if row['floor'] else 'actual'}|"
                f"{a['signed_payload_kg']:.3f}|{b['signed_payload_kg']:.3f}|"
                f"{a['modes']['thermal_core_interface_screen']:.6f}|"
                f"{b['modes']['thermal_core_interface_screen']:.6f}|")
text += [
    "",
    "On 037b's original 028b geometry, its reported 250 °F result adds 4.403 MPa "
    "balanced face compression, takes usage from 0.971978 to 1.052282 and gamma "
    "to 0.618429. Its 200 °F / 30.341397:1 repair adds 0.120151 kg there. These "
    "source values are not transplanted as a constant surcharge at all radii: "
    "our paired rows recompute geometry, joining mass and residual stress.",
    "",
    "The older comparison-037 directory in the filed report is the rigid, cold-"
    "reference thermal model. It is not the as-designed 037b row. The original "
    "040 report and its artifacts are unchanged.",
    "",
    "Validation: all 120 fixed rows reproduce their filed payload within 1e-8 kg; "
    "all 120 conditional rows preserve the failed edge and satisfy every other "
    "mode used by the optimizer; all mass sums close within 1e-8 kg. The edge "
    "failure bound covers every interpolation knot for all five radii and is "
    "independent of the four optimism axes.",
    "",
    "Installed-hull SF remains unknown. Free-edge homogenization, creep and "
    "fatigue, bond/core preparation, thermal cycles, hardpoints and the original "
    "040 qualifications remain open. This is an analytical comparison, not "
    "proof of an installed joint."
]
(HERE / "CARD.md").write_text("\n".join(text) + "\n")
dump("NFI.json", dict(tag="QUESTIONABLE / PROJECTION", findings=[
    dict(id="048F-edge", finding="250 F compliant-core field survival does not close minimum-strength free edges.",
         disposition="Strict as-designed account has no admissible point; conditional price retains failure."),
    dict(id="048F-qualification", finding="037b and 040 NFI remain in force.",
         references=[str(BASE/"NFI.json"), str(BASE/"inputs/037b/NFI.json")]),
    dict(id="048F-no-fixed-surcharge", finding="Source +0.120151 kg fix applies to original 028b geometry only.",
         disposition="Recomputed all joining and stress terms in paired rows.")
]))
inputs = [BASE / n for n in ["model.py", "RESULTS.json", "INPUTS.json",
                            "THERMAL-TABLE.json", "NFI.json",
                            "inputs/031/ATMOSPHERE.json", "inputs/034/INPUTS.json",
                            "inputs/037b/RESULTS.json", "inputs/037b/NFI.json"]]
inputs += [BASE.parent.parent.parent / "outbox" /
           "rpt-ref-b10363665c6202d8ef75.json"]
dump("INPUT-PINS.json", [pin(p) for p in inputs])
print("COMPLETE", len(rows), "paired configurations", flush=True)
