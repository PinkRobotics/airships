#!/usr/bin/env python3
"""Regenerate labelled comparisons in memory; --update writes the reviewed artefacts."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import public_text, validate

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/validation"
LB_KG = 0.45359237
FT_M = 0.3048
MILE_KM = 1.609344
KNOT_KPH = 1.852
HP_MW = 745.6998715822702 / 1e6  # mechanical horsepower
NC = "not comparable"
BOUND = "bound holds"
BOUND_FAIL = "bound fails"

LOCAL_SOURCES = {
    "1-atmosphere": "noaa-1976-us-standard-atmosphere",
    "5-vacuum-shell-akhmeteli": "akhmeteli-gavrilin-2021-vacuum-balloon",
    "5-vacuum-shell-jenett": "jenett-2019-lattice-vacuum-airship",
}


def number(text):
    """Read a leading printed number, optionally a printed power of ten; no physics."""
    text = text.replace("−", "-").replace(",", "")
    m = re.match(r"^\s*([+-]?\d+(?:\.\d+)?)(?:\s*×\s*10\^([+-]?\d+))?", text)
    if not m:
        raise ValueError("unrecognised printed number")
    return float(m[1]) * 10 ** int(m[2] or 0)


def load_model(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem.replace("-", "_"), ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def function(path, name):
    text = (ROOT / path).read_text()
    pattern = rf"^(?:export function|def) {re.escape(name)}\("
    found = [i for i, line in enumerate(text.splitlines(), 1) if re.match(pattern, line)]
    if len(found) != 1:
        raise ValueError(f"cannot locate model function {path}:{name}")
    return {"file": path, "line": found[0], "name": name}


def reference(records, index, field=None, value=None, unit=None):
    r = records[index]
    original = r["value"] if field is None else r["value"][field]
    result = {"record": f"sources.json#/records/{index}", "field": field,
              "printed_value": original, "value": original if value is None else value,
              "unit": unit or r["unit"], "document": r["document"],
              "locator": r["locator"], "url": r["url"], "confidence": r["confidence"],
              "limits": r["limits"]}
    if r["check"] in LOCAL_SOURCES:
        source_id = LOCAL_SOURCES[r["check"]]
        result.update(catalogue=f"research/sources.json#{source_id}",
                      local_document=f"research/papers/{source_id}.pdf",
                      provenance=f"research/papers/{source_id}.pdf.prov.json")
    return result


def row(label, model, ref, unit, tolerance, reason, verdict=None, difference=True, **details):
    delta = model - ref["value"] if difference and isinstance(model, (float, int)) \
        and isinstance(ref["value"], (float, int)) else None
    if verdict is None:
        if delta is None or tolerance is None:
            raise ValueError("an agreement needs comparable numeric values and a tolerance")
        verdict = "agrees" if abs(delta) <= tolerance else "MISS"
    return {"label": label, "model_value": model, "reference": ref, "unit": unit,
            "difference": delta, "tolerance": tolerance, "tolerance_reason": reason,
            "verdict": verdict, **details}


def check(check_id, title, category, calls, inputs, rows, tolerance, limits, paragraph):
    verdicts = {r["verdict"] for r in rows}
    verdict = BOUND_FAIL if BOUND_FAIL in verdicts else "MISS" if "MISS" in verdicts else \
        NC if NC in verdicts else BOUND if BOUND in verdicts else "agrees"
    return {"id": check_id, "title": title, "class": category, "model_functions": calls,
            "inputs": inputs, "rows": rows, "tolerance": tolerance, "verdict": verdict,
            "limits": limits, "interpretation": paragraph}


def bound_row(label, model, ref, unit, tolerance, reason, direction="<=", **details):
    holds = model <= ref["value"] + tolerance if direction == "<=" else model >= ref["value"] - tolerance
    return row(label, model, ref, unit, tolerance, reason,
               BOUND if holds else BOUND_FAIL, inequality=f"model {direction} reference", **details)


def generate():
    data = json.loads((HERE / "sources.json").read_text())
    validate(data)
    refs = data["records"]
    t = json.loads((HERE / "tolerances.json").read_text())
    v = lambda i, key=None: refs[i]["value"] if key is None else refs[i]["value"][key]
    n = lambda i, key=None: number(v(i, key))
    heights = [n(i, "H_m") for i in range(5)]
    distances = [number(k.split("_")[0]) for k in v(18) if k.endswith("_mile") or k.endswith("_miles")]
    # Select the source's knot reading, preserving the inconsistent mph reading in the data.
    cruise = number(re.search(r"\((\d+) knots", v(20, "maximum_cruise"))[1])
    scoop_range = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", v(19, "time_on_water"))]
    if len(scoop_range) != 2 or not 0 < scoop_range[0] <= scoop_range[1]:
        raise ValueError("cannot read the printed scoop interval")
    # Geometry and force-unit conversion for the public diskMW inputs, no power equation.
    args = {"heights": heights, "hindenburg_m3": n(10, "normal_volume_ft3") * FT_M ** 3,
            "tank_m3": n(15, "all_four_L") / 1000,
            "cruise_kph": cruise * KNOT_KPH,
            "scoop_seconds": t["cl415"]["scoop_midpoint_seconds"],
            "distances_km": [d * MILE_KM for d in distances],
            "rotor_density": n(0, "rho"),
            "disk_m2": 2 * math.pi * (n(22, "radius_ft") * FT_M) ** 2,
            "thrust_N": n(23, "design_gross_weight_lb") * LB_KG * n(7, "g0"),
            "standard_pressure_Pa": n(0, "P") * 100, "standard_temperature_K": n(0, "T_K"),
            "hover": {"pressure_altitude_m": n(35, "pressure_altitude_ft") * FT_M,
                      "temperature_K": n(35, "temperature_C") + 273.15,
                      "disk_m2": n(35, "rotor_disk_area_ft2") * FT_M**2,
                      "thrust_N": n(35, "gross_weight_lb") * LB_KG * n(7, "g0")}}
    p = subprocess.run(["node", "research/validation/model.mjs"], input=json.dumps(args),
                       text=True, capture_output=True, cwd=ROOT, timeout=60)
    if p.returncode:
        raise ValueError("JavaScript model could not run: " + safe_error(p.stderr))
    js = json.loads(p.stdout)
    cell = load_model("research/analysis/vacuum-cell.py")
    gas = load_model("research/analysis/helium.py")
    calls_isa = [function("sim/atmosphere.js", name) for name in
                 ("isaTemperatureK", "isaPressurePa", "airDensity")]
    calls_isa += [function("research/analysis/vacuum-cell.py", name) for name in
                  ("isa_temperature", "isa_pressure", "rho_air")]
    calls_isa += [function("research/analysis/helium.py", "isa")]
    rows, parity = [], []
    for i, h in enumerate(heights):
        triple = gas.isa(h)
        implementations = {"sim": js["isa"][i],
                           "vacuum-cell": dict(zip(("temperature_K", "pressure_Pa", "density_kg_m3"),
                                                  (cell.isa_temperature(h), cell.isa_pressure(h), cell.rho_air(h)))),
                           "helium": dict(zip(("temperature_K", "pressure_Pa", "density_kg_m3"), triple))}
        spread = {key: max(a[key] for a in implementations.values()) -
                  min(a[key] for a in implementations.values()) for key in js["isa"][i]}
        parity.append({"H_m": h, "implementations": implementations, "max_minus_min": spread,
                       "agree_to_roundoff": all(spread[k] <= t["atmosphere"]["implementation_parity"][k]
                                                 for k in spread)})
        for impl, values in implementations.items():
            for key, field, scale, unit in (("temperature_K", "T_K", 1, "K"),
                                             ("pressure_Pa", "P", 100, "Pa"),
                                             ("density_kg_m3", "rho", 1, "kg/m3")):
                rows.append(row(f"{impl}, H={h:g} m, {key}", values[key],
                                reference(refs, i, field, n(i, field) * scale, unit), unit,
                                t["atmosphere"][key], t["atmosphere"]["reason"]))
    atmosphere = check("1-atmosphere", "Air density with altitude", "equation", calls_isa,
                       {"geopotential_heights_m": heights, "density_anchor": "each function's default"},
                       rows, t["atmosphere"],
                       ["A stipulated atmosphere, not weather observations.",
                        "All three formulas apply lapse directly to the argument: it is effectively geopotential height. "
                        "The JS interface says metres MSL and does not convert geometric height.",
                        "At geometric 2500 m the source gives H=2499 m and T=271.906 K. Passing 2500 "
                        "directly yields the geopotential temperature; geometric use slightly understates "
                        "temperature, pressure and density. The rounded Z column is not a conversion algorithm."],
                       "All three project ISA implementations are evaluated at the five Table I geopotential "
                       "heights. Their independent agreement with the printed table is distinct from their "
                       "mutual agreement: the table below retains all three values. The JS constant R=287.0528 "
                       "differs from the Python value 287.05. None converts geometric height.")
    atmosphere["implementation_comparison"] = parity

    hind_ref = reference(refs, 11, "total_lift_lb", n(11, "total_lift_lb") * LB_KG, "kg")
    purity = hind_ref["value"] / js["hindenburg"]
    hind = check("2-hindenburg", "Hindenburg gross lift", "measured",
                 [function("sim/physics.js", "grossLiftKg"), function("sim/physics.js", "ledger")],
                 {"volume_m3": args["hindenburg_m3"], "temperature_K": args["standard_temperature_K"],
                  "pressure_Pa": args["standard_pressure_Pa"], "gas": "hydrogen", "purity": 1,
                  "fill_fraction": 1, "volume_reference": reference(refs, 10),
                  "purity_needed_at_full_volume": purity},
                 [row("full normal volume, 100% hydrogen", js["hindenburg"], hind_ref, "kg",
                      hind_ref["value"] * t["hindenburg"]["relative"], t["hindenburg"]["reason"])],
                 t["hindenburg"],
                 ["The report does not specify purity, fill fraction or the temperature meant by standard conditions. "
                  "288.15 K and 101325 Pa are declared comparison assumptions, not recovered historical conditions.",
                  f"At that state, matching the printed lift would require purity {purity:.9g} "
                  "at full normal volume with dry-air contamination; equivalently this is the full-purity fill fraction. "
                  "This limit is reported, never passed back into the comparison.",
                  "Ideal hydrogen, no humidity or superheat; no empty mass or useful payload is inferred."],
                 "The new public grossLiftKg computes gas lift before structure. The existing class ledger calls "
                 "the same function for vacuum, retaining its density dial and multiplication order exactly. "
                 "The hydrogen row is now a conditional comparison with the report's total lift.")

    cycle_rows = []
    for miles, output in zip(distances, js["cycles"]):
        key = f"{miles:g}_mile" if miles == 1 else f"{miles:g}_miles"
        cycle_rows.append(bound_row(f"{miles:g} miles: cruise round trip + scoop lower bound",
                              output["mapped_minutes"],
                              reference(refs, 18, key, number(v(18, key)), "min"), "min",
                              t["cl415"]["cycle_minutes"], t["cl415"]["reason"],
                              ground_speed_out_kph=output["ground_speed_out_kph"],
                              ground_speed_return_kph=output["ground_speed_return_kph"]))
    cycle_rows.append(row("scoop duration input replay (not an independent validation)",
                          js["cycles"][0]["duration_minutes"]["WATER_FILL"] * 60,
                          reference(refs, 19, "time_on_water", sum(scoop_range) / 2, "s"),
                          "s", t["cl415"]["scoop_seconds"], t["cl415"]["reason"]))
    cycle = check("3-cl415-cycle", "CL-415 scooping cycle", "measured",
                  [function("sim/plan.js", "planCycle")],
                  {"one_way_miles": distances, "one_way_km": args["distances_km"],
                   **js["cycle_inputs"], "speed_source": reference(refs, 20),
                   "scoop_source": reference(refs, 19), "source_interval_seconds": scoop_range,
                   "mapping": "distance / public planCycle ground speed for each leg, plus WATER_FILL only; "
                              "no complete-cycle or energy comparison"},
                  cycle_rows, t["cl415"],
                  ["Climb-out, circuit, approach, acceleration, deceleration and drop run are unmapped. "
                   "The sum is a lower bound on turnaround, never a complete aircraft cycle.",
                   "No wind; the printed maximum cruise 185 knots is used. The source's 223 mph is inconsistent "
                   "with it and remains preserved. Constant maximum speed understates transit time.",
                   "The public planCycle speed and fill outputs are used; its airship ramp, hose floors, "
                   "buoyancy escape, descent and retained-water assumptions are not aircraft evidence.",
                   "Scoop 11 seconds replays the supplied midpoint of 10-12 seconds. Agreement proves plumbing only. "
                   "The planning table's half-minute allowance is retained; no operational capability is established."],
                  "Only straight-line cruise transit and the printed scoop duration map. "
                  "The necessary inequality is partial time <= listed turnaround (plus the predeclared "
                  "0.5-minute planning tolerance). Shorter mapped times do not validate the missing phases.")

    power = js["rotor_MW"]
    mrp = number(v(23, "takeoff_power").split("=")[1])
    installed = 2 * mrp
    rotor_rows = [bound_row("CH-47D required / two-engine takeoff rating", power,
                      reference(refs, 23, "takeoff_power", installed * HP_MW, "MW"),
                      "MW", 0, t["rotor"]["reason"], ratio=power / (installed * HP_MW)),
                  bound_row("CH-47D required / drive-system limit", power,
                      reference(refs, 23, "drive_system_limit_hp", n(23, "drive_system_limit_hp") * HP_MW, "MW"),
                      "MW", 0, t["rotor"]["reason"], ratio=power / (n(23, "drive_system_limit_hp") * HP_MW))]
    hover_t = t["order_9c_before_first_comparison"]["hover_measurement"]
    hover_ref = reference(refs, 35, "engine_power_hp", n(35, "engine_power_hp") * HP_MW, "MW")
    rotor_rows.append(row("XH-59A measured OGE total engine power", js["hover"]["power_MW"],
                         hover_ref, "MW", hover_ref["value"] * hover_t["relative"], hover_t["reason"]))
    rotor = check("4-helicopter-hover", "Rotor hover power: flight test and CH-47D bounds", "measured",
                  [function("sim/physics.js", "diskMW"), function("sim/atmosphere.js", "isaPressurePa"),
                   function("sim/atmosphere.js", "altitudeForDensity")],
                  {"ch47d": {"diskM2": args["disk_m2"], "thrustN": args["thrust_N"],
                             "config": js["rotor_config"]},
                   "xh59a": {**args["hover"], **js["hover"], "source": reference(refs, 35)}},
                  rotor_rows, {"reason": "CH-47D retains power-rating bounds with zero slack. XH-59A: " + hover_t["reason"]},
                  ["CH-47D inequalities test required power <= installed power and <= transmission limit; "
                   "neither rating is measured hover power or proof of hover capability.",
                   "The named 1984 CH-47D report was opened; its crowded nondimensional Figure 10 was not digitized. "
                   "The alternative primary XH-59A Table 2 supplies a dimensional point. Search/fetch record: hover-search.md.",
                   "XH-59A uses its printed 1018 ft2 coaxial footprint once, not two independent disks. "
                   "Thrust is weight; total engine horsepower includes download, coaxial interference and accessories. "
                   "This tests the default propEta as an effective aircraft figure of merit, not rotor-only merit.",
                   "Equivalent density altitude is derived from printed pressure altitude and temperature, not reported as measured. "
                   "The low-resolution primary scan warrants medium confidence. One point is not validation of an envelope.",
                   "Re-run after the energy-model worker changes the public sim/physics.js:diskMW function."],
                  "Call the public diskMW at a measured OGE state from Arents' 1977 flight test, leaving its "
                  "efficiency assumption unchanged. Keep the older CH-47D power-rating bounds separately labelled.")

    rep = load_model("research/analysis/reproductions.py")
    ak_inputs = dict(radius_m=n(27, "example_R_m"), face_ratio=n(27, "face_thickness_over_R"),
                     core_ratio=n(27, "core_thickness_over_R"), face_density=n(26, "face_density_kg_m3"),
                     core_density=50.0, air_density=n(26, "air_density_kg_m3"),
                     face_modulus=n(26, "face_modulus_GPa") * 1e9)
    ak = rep.akhmeteli(**ak_inputs)
    je_inputs = dict(pressure_Pa=n(28, "Patm") * 1000, air_density=n(28, "rho_air_kg_m3"),
                     modulus_Pa=n(28, "tensile_modulus_GPa") * 1e9, material_density=n(28, "density") * 1000)
    je = [rep.jenett(number(radius), **je_inputs) for radius in v(29, "radius_m")]
    vacuum_rows = [
        row("Akhmeteli shell mass, literal thin-layer Eq.(7)", ak["thin_shell_mass_kg"],
            reference(refs, 27, "example_shell_mass_kg", n(27, "example_shell_mass_kg"), "kg"),
            "kg", t["vacuum"]["akhmeteli_mass_kg"], t["vacuum"]["reason"]),
        row("Akhmeteli payload, literal thin-layer Eq.(7)", ak["thin_payload_kg"],
            reference(refs, 27, "example_payload_at_zero_buoyancy_kg",
                      n(27, "example_payload_at_zero_buoyancy_kg"), "kg"),
            "kg", t["vacuum"]["akhmeteli_payload_kg"], t["vacuum"]["reason"])]
    for radius, lift, out in zip(v(29, "radius_m"), v(29, "lift_kg"), je):
        half_place = 0.5 * 10 ** (-len(lift.split(".")[1]) if "." in lift else 0)
        r = reference(refs, 29, "lift_kg", number(lift), "kg")
        r.update(printed_value=lift, radius_m=radius)
        vacuum_rows.append(row(f"Jenett R={radius} m net lift", out["net_lift_kg"],
                               r, "kg", half_place, t["vacuum"]["reason"], NC,
                               missing_inputs=out["missing_inputs"]))
    paper_terms = {
        "akhmeteli": ["Eq.(7): two-face/honeycomb mass balance at the paper's air density",
                      "Eq.(9): semi-empirical sandwich buckling pressure (diagnostic, not FEA)",
                      "Discussion p.489: final face/core thickness ratios and material card",
                      "Concentric finite-layer volumes: explicit geometric expansion, not a printed paper equation; diagnostic only"],
        "jenett": ["Eq.(33): spherical membrane stress and IV.D force per lattice cell",
                   "IV.D: shell/radius=0.1, pitch/thickness=0.1, tube radius/wall=10",
                   "Figure 4 regular-octahedron force resolution with stated diagnostic pitch and pinned-end conventions",
                   "VI: displaced mass minus member inventory mass; inventory unavailable"]}
    vacuum = check("5-vacuum-shells", "Two vacuum-shell calculations", "reproduction",
                   [function("research/analysis/reproductions.py", "akhmeteli"),
                    function("research/analysis/reproductions.py", "jenett"),
                    function("research/analysis/reproductions.py", "euler_load"),
                    function("research/analysis/vacuum-cell.py", "ship_section"),
                    function("research/analysis/vacuum-cell.py", "_ship_sigma_euler")],
                   {"akhmeteli": ak_inputs, "jenett": je_inputs}, vacuum_rows, t["vacuum"],
                   ["Every paper-specific term is listed below and in reproductions.py; these are not validations "
                    "of the project's volume-filling lattice or its dry-mass allowance.",
                    "Akhmeteli uses the final Discussion ratios, not the earlier analytical optimum. "
                    "The table applies printed Eq.(7) literally. Finite concentric layers are a separate geometric "
                    "diagnostic, not a post-result replacement of a MISS. Adhesives and joints remain excluded. "
                    "No FEA eigenvalue, face wrinkling or intracell buckling result is claimed.",
                    "Jenett IV.D local sizing calls the project's Euler and tube-section functions, rescaling the "
                    "bound T700 modulus algebraically to the paper's 588 GPa. No material table is changed. "
                    "The project's corrected laminate properties cannot replace the paper's fibre card.",
                    "Missing for Table 2: equivalent member inventory with shared-edge/boundary counting, "
                    "and explicit pitch/member-length and Euler end-condition conventions. Table 1 supplies "
                    "1,460,192 voxels without the radius or member-sharing rule. No count is fitted to net lift. "
                    "The local diagnostic assumes a regular octahedron and pinned struts; it cannot establish global stability.",
                    "The paper densities 1.29 and 1.225 kg/m3 are used as printed; no ISA is substituted."],
                   "The sandwich mass balance is askable and can miss. Its finite-layer geometric diagnostic "
                   "is shown separately. Jenett's local member-sizing method is askable, but the published "
                   "net-lift table lacks the member inventory needed to complete the mass calculation.")
    vacuum["model_diagnostics"] = {"akhmeteli": ak, "jenett": je}
    vacuum["paper_terms"] = paper_terms

    he_T, he_P = n(0, "T_K"), n(0, "P") * 100
    density = gas.gas_density(he_T, he_P, "helium")
    lift = gas.net_lift(he_T, he_P, density)
    handbook_T = (n(32, "temperature_F") - 32) * 5/9 + 273.15
    handbook_P = n(32, "pressure_in_hg") * 3386.389
    handbook_lift = gas.net_lift(handbook_T, handbook_P, gas.gas_density(handbook_T, handbook_P))
    volume = n(33, "easa_issue_10_both_models_envelope_m3")
    he_rows = [
        row("helium density at NIST state", density,
            reference(refs, 30, value=n(30), unit="kg/m3"), "kg/m3",
            n(30) * t["helium"]["density_relative"], t["helium"]["reason"]),
        row("gross gas lift at NIST state / derived air-minus-helium", lift,
            reference(refs, 31, value=n(31), unit="kg/m3"), "kg/m3",
            t["helium"]["derived_lift_kg_m3"], t["helium"]["reason"],
            reference_class="equation; derived, not measured"),
        row("gross helium lift at the FAA handbook's printed state", handbook_lift,
            reference(refs, 32, "helium_gross_lift_lb",
                      n(32, "helium_gross_lift_lb") * LB_KG / n(32, "envelope_m3"), "kg/m3"),
            "kg/m3", t["helium"]["handbook_lift_kg_m3"], t["helium"]["reason"]),
        bound_row("Zeppelin full pure-helium static capacity >= maximum weight", volume * lift,
            reference(refs, 34, "max_takeoff_weight_kg", n(34, "max_takeoff_weight_kg"), "kg"),
            "kg", 0, t["helium"]["reason"], direction=">=")]
    helium = check("6-helium", "Helium and a modern airship", "measured",
                   [function("research/analysis/helium.py", "gas_density"),
                    function("research/analysis/helium.py", "net_lift")],
                   {"nist_state": {"temperature_K": he_T, "pressure_Pa": he_P},
                    "handbook_state": {"temperature_K": handbook_T, "pressure_Pa": handbook_P},
                    "zeppelin_volume": reference(refs, 33, "easa_issue_10_both_models_envelope_m3", volume, "m3"),
                    "zeppelin_maximum_mass": reference(refs, 34, "max_takeoff_weight_kg",
                                                       n(34, "max_takeoff_weight_kg"), "kg")},
                   he_rows, t["helium"],
                   ["Density is ideal-gas with unchanged R_HE=2077.1, R_AIR=287.05. "
                    "NIST is a real-gas equation of state; its tolerance is not expanded to hide that difference.",
                    "The handbook's rounded 29.92 inHg is converted literally, not silently replaced by 101325 Pa. "
                    "Its 1966 reference atmosphere and printed lift remain separate from the NIST-derived difference.",
                    "Zeppelin: full envelope, pure helium, no superheat, at the declared NIST state. "
                    "For wholly static support, gross gas lift must be >= supported total mass. This screen holds "
                    "or fails only under those conditions; maximum takeoff weight is not measured gross lift. "
                    "Real fill, purity, ballonets, overpressure, static heaviness and dynamic lift are not inferred.",
                    "No empty mass or payload is derived from maximum weight. Main's fixed-altitude "
                    "published gas ledger is byte-compared separately."],
                   "Public state-parameterized gas_density and net_lift now answer both helium references. "
                   "The modern airship is a conditional capacity bound, not an agreement claim about measured lift.")
    report = {"schema_version": 1, "generated_by": "research/validation/check.py",
              "sources_sha256": hashlib.sha256((HERE / "sources.json").read_bytes()).hexdigest(),
              "tolerances": t, "excluded_reference": {
                  "record": "sources.json#/records/6",
                  "reason": "Kept to preserve the printed error, not silently correct it. "
                            "Table 2's gas-constant exponent is explicitly do not use."},
              "policy": "Agreement is not model validation. MISS rows are published and do not fail the gate. "
                        "Unavailable questions are not comparable; an actual function/import/runtime failure fails.",
              "checks": [atmosphere, hind, cycle, rotor, vacuum, helium]}
    finite(report)
    return report


def finite(value):
    if isinstance(value, dict):
        for child in value.values():
            finite(child)
    elif isinstance(value, list):
        for child in value:
            finite(child)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("nonfinite model result")


def fmt(value):
    if value is None:
        return "unavailable"
    if isinstance(value, (int, float)):
        return f"{value:.9g}"
    return str(value).replace("|", r"\|").replace("\n", " ")


def markdown(report):
    lines = ["# Six labelled checks", "",
             "Generated by research/validation/check.py. References and printed digits are in "
             "[sources.json](sources.json); full calls, inputs, differences and limits are in "
             "[report.json](report.json). Tolerances were written before the first run in "
             "[tolerances.json](tolerances.json). A MISS stays published and does not fail the gate.", "",
             "| Check | Class | Verdict | Scope |", "| --- | --- | --- | --- |"]
    for c in report["checks"]:
        lines.append(f"| {c['title']} | {c['class']} | {c['verdict']} | {len(c['rows'])} labelled rows |")
    for c in report["checks"]:
        lines += ["", f"## {c['title']}", "", c["interpretation"], "", "**Called:** " +
                  "; ".join(f"{f['file']}:{f['line']} ({f['name']})" for f in c["model_functions"]),
                  "", "**Tolerance:** " + c["tolerance"]["reason"], "",
                  "| Comparison | Model | Reference | Difference | Tolerance | Verdict |",
                  "| --- | ---: | ---: | ---: | ---: | --- |"]
        for r in c["rows"]:
            ref = r["reference"]
            idx = ref["record"].split("/")[-1]
            label = r["label"]
            lines.append(f"| {label} ({r['unit']}) | {fmt(r['model_value'])} | "
                         f"{fmt(ref['value'])} [source {idx}](sources.json) | "
                         f"{fmt(r['difference'])} | {fmt(r['tolerance'])} | {r['verdict']} |")
        if c["id"] == "1-atmosphere":
            lines += ["", "Mutual density comparison (kg/m3); agreement here means numerical roundoff only.", "",
                      "| H (m) | sim | vacuum-cell | helium | All T/P/density agree to roundoff |",
                      "| ---: | ---: | ---: | ---: | --- |"]
            for p in c["implementation_comparison"]:
                values = [p["implementations"][name]["density_kg_m3"] for name in ("sim", "vacuum-cell", "helium")]
                lines.append(f"| {p['H_m']:g} | " + " | ".join(f"{v:.12g}" for v in values) +
                             f" | {p['agree_to_roundoff']} |")
        if c["id"] == "4-helicopter-hover":
            h = c["inputs"]["xh59a"]
            lines += ["", f"XH-59A comparison state: pressure altitude {h['pressure_altitude_m']:.9g} m, "
                      f"temperature {h['temperature_K']:.9g} K, density {h['density_kg_m3']:.9g} kg/m3; "
                      f"equivalent ISA density altitude {h['density_altitude_m']:.9g} m (derived). "
                      f"Unchanged effective efficiency: {h['config']['propEta']:.9g}."]
            lines += ["", "Required/available ratios: " +
                      "; ".join(f"{r['label']}: {r['ratio']:.9g}" for r in c["rows"] if "ratio" in r) + "."]
        if c["id"] == "5-vacuum-shells":
            ak = c["model_diagnostics"]["akhmeteli"]
            lines += ["", f"Finite-layer geometric diagnostic only: shell {ak['shell_mass_kg']:.9g} kg, "
                      f"payload {ak['payload_kg']:.9g} kg. The literal Eq.(7) rows above remain unchanged.",
                      "", "**The paper's terms, not the project's:**"]
            for paper, terms in c["paper_terms"].items():
                lines += ["", f"- {paper}: " + "; ".join(terms) + "."]
            lines += ["", "Jenett's missing Table 2 inputs: " +
                      "; ".join(c["model_diagnostics"]["jenett"][0]["missing_inputs"]) + "."]
        if c["id"] == "6-helium":
            lines += ["", f"Requested Zeppelin comparison: {c['inputs']['zeppelin_volume']['value']:g} m3 "
                      f"versus {c['inputs']['zeppelin_maximum_mass']['value']:g} kg maximum takeoff mass."]
        lines += ["", "**Limits:** " + " ".join(c["limits"]), "",
                  "**Locators:**"]
        seen = set()
        for r in c["rows"]:
            ref = r["reference"]
            key = (ref["document"]["title"], ref["locator"])
            if key not in seen:
                seen.add(key)
                lines += ["", f"- {key[0]}. {key[1]}"]
    lines += ["", "The excluded Table 2 gas-constant record is preserved as printed and never used. "
              "The original source set is retained and one primary hover measurement added; see hover-search.md.", ""]
    return "\n".join(lines)


def safe_error(text):
    # Tool errors can include absolute runtime paths; do not print those in public receipts.
    return text.replace(str(ROOT), "<repo>").replace(str(Path.home()), "<user>")[-1600:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="regenerate report.json and report.md; review the diff")
    parser.add_argument("--schema-only", action="store_true", help="check all source records without running models")
    args = parser.parse_args()
    try:
        if args.schema_only:
            validate(json.loads((HERE / "sources.json").read_text()))
            print("labelledcheck: 36 normalised source records pass schema")
            return 0
        report = generate()
        outputs = {"report.json": json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                   "report.md": markdown(report)}
        for text in outputs.values():
            public_text(text)
        drift = []
        for name, text in outputs.items():
            path = HERE / name
            if args.update:
                path.write_text(text)
            else:
                old = path.read_text() if path.exists() else ""
                if old != text:
                    drift.append(name)
                    print(f"labelledcheck: {name} is stale", file=sys.stderr)
                    diff = difflib.unified_diff(old.splitlines(), text.splitlines(),
                                                fromfile=name, tofile="recomputed/" + name, lineterm="")
                    print("\n".join(list(diff)[:45]), file=sys.stderr)
        if drift:
            print("Run python3 research/validation/check.py --update and review every moved number.", file=sys.stderr)
            return 1
        print("labelledcheck: 6 checks computed; 36 source records valid; reports " +
              ("updated" if args.update else "match"))
        print("; ".join(f"{c['id']}: {c['verdict']}" for c in report["checks"]))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, ImportError,
            ArithmeticError, subprocess.SubprocessError) as exc:
        print("labelledcheck: cannot run: " + safe_error(str(exc)), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
