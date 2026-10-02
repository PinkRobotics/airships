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
import tempfile

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
BOUND = "bound only"

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
    verdict = "MISS" if "MISS" in verdicts else NC if NC in verdicts else \
        BOUND if BOUND in verdicts else "agrees"
    return {"id": check_id, "title": title, "class": category, "model_functions": calls,
            "inputs": inputs, "rows": rows, "tolerance": tolerance, "verdict": verdict,
            "limits": limits, "interpretation": paragraph}


def helium_output():
    # main() has no gas-density API or altitude parameter. Run it unchanged, with its own
    # committed auxiliary inputs; select only its atmosphere and gas outputs, not caches.
    # CI need not configure a system temporary directory: the explicit fallback stays
    # inside this generated-file directory and is cleaned on success or failure.
    scratch = os.environ.get("TMPDIR") or str(HERE)
    with tempfile.TemporaryDirectory(prefix="labelled-helium-", dir=scratch) as tmp:
        out = Path(tmp) / "helium.json"
        p = subprocess.run([sys.executable, "-B", "research/analysis/helium.py",
                            "--json", str(out)], cwd=ROOT, capture_output=True, text=True,
                           timeout=60, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if p.returncode:
            raise ValueError("helium.main could not run: " + safe_error(p.stderr))
        generated = json.loads(out.read_text())
    return {"atmosphere": generated["atmosphere"],
            "helium": generated["ledger"]["helium"],
            "hydrogen": generated["ledger"]["hydrogen"]}


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
    # Geometry and force-unit conversion for the public diskMW inputs, no power equation.
    args = {"heights": heights, "hindenburg_m3": n(10, "normal_volume_ft3") * FT_M ** 3,
            "tank_m3": n(15, "all_four_L") / 1000,
            "cruise_kph": cruise * KNOT_KPH,
            "scoop_seconds": t["cl415"]["scoop_midpoint_seconds"],
            "distances_km": [d * MILE_KM for d in distances],
            "rotor_density": n(0, "rho"),
            "disk_m2": 2 * math.pi * (n(22, "radius_ft") * FT_M) ** 2,
            "thrust_N": n(23, "design_gross_weight_lb") * LB_KG * n(7, "g0")}
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
    hind = check("2-hindenburg", "Hindenburg gross lift", "measured",
                 [function("sim/physics.js", "ledger")],
                 {"ledger_class": {"dispM3": args["hindenburg_m3"], "payloadT": 0}, "altMslM": 0,
                  "requested_gas": "hydrogen", "gas_reference": reference(refs, 14),
                  "volume_reference": reference(refs, 10)},
                 [row("evacuated displacement; hydrogen term unavailable", js["hindenburg"]["liftT"] * 1000,
                      hind_ref, "kg", hind_ref["value"] * t["hindenburg"]["relative"],
                      t["hindenburg"]["reason"], NC,
                      difference_meaning="evacuated displacement minus reported hydrogen gross lift; not model error")],
                 t["hindenburg"],
                 ["The model cannot be asked this question: ledger has no lifting-gas density, purity or fill-fraction argument.",
                  "Normal volume is used, not total volume. The report does not quantify purity or tie a fill fraction "
                  "to total lift; its standard temperature is unspecified.",
                  "No empty mass is inferred. The NIST hydrogen datum is retained but cannot be plumbed into ledger."],
                 "The callable ledger reports evacuated displacement at the report's normal gas volume. "
                 "That is not hydrogen gross lift. The diagnostic difference is shown without an agreement or "
                 "MISS claim; subtracting hydrogen in this checker would create a new buoyancy implementation.")

    cycle_rows = []
    for miles, output in zip(distances, js["cycles"]):
        key = f"{miles:g}_mile" if miles == 1 else f"{miles:g}_miles"
        cycle_rows.append(row(f"{miles:g} miles: transit + fill + return only", output["mapped_minutes"],
                              reference(refs, 18, key, number(v(18, key)), "min"), "min",
                              t["cl415"]["cycle_minutes"], t["cl415"]["reason"], NC,
                              difference_meaning="partial airship duration minus whole aircraft planning cycle",
                              full_airship_cycle_minutes=output["cycle_minutes"],
                              phase_minutes=output["duration_minutes"],
                              retained_t=output["retained_t"], delivered_t=output["delivered_t"]))
    cycle_rows.append(row("fill replay at input rate", js["cycles"][0]["duration_minutes"]["WATER_FILL"] * 60,
                          reference(refs, 19, "time_on_water", t["cl415"]["scoop_midpoint_seconds"], "s"),
                          "s", t["cl415"]["scoop_seconds"], t["cl415"]["reason"], BOUND,
                          note="Comparison to the printed interval only; the midpoint was supplied as an input."))
    cycle = check("3-cl415-cycle", "CL-415 scooping cycle", "measured",
                  [function("sim/plan.js", "planCycle"), function("sim/physics.js", "ledger"),
                   function("sim/physics.js", "diskMW"), function("sim/physics.js", "dragMW"),
                   function("sim/physics.js", "pumpMW")],
                  {"one_way_miles": distances, "one_way_km": args["distances_km"],
                   **js["cycle_inputs"], "capacity_source": reference(refs, 15),
                   "speed_source": reference(refs, 20), "scoop_source": reference(refs, 19),
                   "mapping": "Only cruise speed, water volume (model convention 1 tonne/m3), and fill-rate "
                              "plumbing replace P100 balanced defaults. Remaining class fields are airship assumptions.",
                   "unmapped_speeds": {"scoop": v(19, "scoop_speed"), "drop": v(20, "drop_speed")}},
                  cycle_rows, t["cl415"],
                  ["Agency planning times, medium confidence; not a measured regression.",
                   "Transit and filling map as kinematics, but the transit durations include airship hose/minimum-time "
                   "floors and a 15-percent acceleration ramp. Their sum is not a validated aircraft lower bound.",
                   "The model cannot be asked for an aircraft cycle: source approach, hose handling, drop run, "
                   "buoyancy escape, cryogenic return and descent authority do not map. Separate scoop/drop "
                   "airspeeds and aircraft turns are not parameters. Energy and throughput are not compared.",
                   "6137 L is used; the certificate also prints 6124 kg. The model's one-tonne/m3 convention "
                   "does not reproduce that certificated mass. The plan's inconsistent litre conversion is retained.",
                   "The 90-second next-to-fire possibility is retained in sources.json, not treated as a zero-distance fit."],
                  "The table compares the callable transit/fill subset with the whole planning list at 1, 3, 6, "
                  "10 and 15 miles, explicitly as different quantities. Complete airship cycles and individual "
                  "phases remain in JSON. An 11-second fill replays the supplied midpoint and is not validation "
                  "of scooping. The code cannot accept the printed independent scoop and drop speeds.")

    power = js["rotor_MW"]
    mrp = number(v(23, "takeoff_power").split("=")[1])
    installed = 2 * mrp
    rotor_rows = [row("required / two-engine takeoff rating", power,
                      reference(refs, 23, "takeoff_power", installed * HP_MW, "MW"),
                      "MW", None, t["rotor"]["reason"], BOUND,
                      ratio=power / (installed * HP_MW),
                      conversion="2 engines times the printed 4204 hp rating; interpretation stated, not a measured power"),
                  row("required / drive-system limit", power,
                      reference(refs, 23, "drive_system_limit_hp", n(23, "drive_system_limit_hp") * HP_MW, "MW"),
                      "MW", None, t["rotor"]["reason"], BOUND,
                      ratio=power / (n(23, "drive_system_limit_hp") * HP_MW))]
    rotor = check("4-helicopter-hover", "CH-47D hover power bound", "measured",
                  [function("sim/physics.js", "diskMW")],
                  {"diskM2": args["disk_m2"], "thrustN": args["thrust_N"],
                   "rotors": 2, "diameter_m_each": 2 * n(22, "radius_ft") * FT_M,
                   "config": js["rotor_config"], "rotor_source": reference(refs, 22),
                   "weight_power_source": reference(refs, 23),
                   "per_printed_4204_hp_ratio": power / (mrp * HP_MW)},
                  rotor_rows, t["rotor"],
                  ["No tabulated measured out-of-ground-effect shaft power was found.",
                   "Missing measurement: Airworthiness and Flight Characteristics Test of the CH-47D Helicopter, "
                   "USAAEFA Project No. 82-07, February 1984; Johnson reference 11. Not opened. Figure 17 not digitized.",
                   "Two isolated disk areas are argument plumbing. Tandem overlap, profile power, download, "
                   "transmission losses and ground effect are not represented; the printed disk loading is not recalculated.",
                   "CFG.rhoAir is set to the Table I sea-level density. CFG.propEta remains the model default; "
                   "K_hover=1.15 is not a measured efficiency and is not substituted.",
                   "Re-run after the energy-model worker changes the public diskMW function."],
                  "Public diskMW is called at the printed design gross weight and two 60-foot rotors, using "
                  "sea-level density. Required power is compared to an explicitly interpreted two-engine installed "
                  "rating and the lower transmission limit, with both ratios. This bounds a simplified model; "
                  "it does not reproduce a measured hover power or certify hover capability.")

    boron = {"name": v(26, "face"), "E": n(26, "face_modulus_GPa") * 1e9,
             "rho": n(26, "face_density_kg_m3"), "sigma": n(26, "face_compressive_strength_MPa") * 1e6,
             "orthotropic": False}
    toray = {"name": v(28, "material_example"), "E": n(28, "tensile_modulus_GPa") * 1e9,
             "rho": n(28, "density") * 1000, "sigma": n(28, "tensile_strength_GPa") * 1e9,
             "orthotropic": False}
    monolithic = cell.arch_monolithic(boron, p=n(26, "air_pressure") * 1000)
    lattice = cell.arch_tube_strut(toray, p=n(28, "Patm") * 1000)
    vacuum_rows = [
        row("Akhmeteli shell mass (unavailable)", None,
            reference(refs, 27, "example_shell_mass_kg", n(27, "example_shell_mass_kg"), "kg"),
            "kg", t["vacuum"]["akhmeteli_mass_kg"], t["vacuum"]["reason"], NC),
        row("Akhmeteli payload (unavailable)", None,
            reference(refs, 27, "example_payload_at_zero_buoyancy_kg",
                      n(27, "example_payload_at_zero_buoyancy_kg"), "kg"),
            "kg", t["vacuum"]["akhmeteli_payload_kg"], t["vacuum"]["reason"], NC)]
    for radius, lift in zip(v(29, "radius_m"), v(29, "lift_kg")):
        half_place = 0.5 * 10 ** (-len(lift.split(".")[1]) if "." in lift else 0)
        r = reference(refs, 29, "lift_kg", number(lift), "kg")
        r.update(printed_value=lift, radius_m=radius)
        vacuum_rows.append(row(f"Jenett R={radius} m net lift (unavailable)", None,
                               r, "kg", half_place, t["vacuum"]["reason"], NC))
    vacuum = check("5-vacuum-shells", "Two vacuum-shell calculations", "reproduction",
                   [function("research/analysis/vacuum-cell.py", "arch_monolithic"),
                    function("research/analysis/vacuum-cell.py", "arch_tube_strut")],
                   {"akhmeteli": {"material": boron, "p_Pa": n(26, "air_pressure") * 1000,
                                  "requested_air_density_kg_m3": n(26, "air_density_kg_m3"),
                                  "reference_design": reference(refs, 27)},
                    "jenett": {"material": toray, "p_Pa": n(28, "Patm") * 1000,
                               "requested_air_density_kg_m3": n(28, "rho_air_kg_m3"),
                               "reference_design": reference(refs, 28)},
                    "unavailable_arguments": "Neither function accepts air density, sphere radius, "
                                             "sandwich thicknesses or fixed lattice tube proportions."},
                   vacuum_rows, t["vacuum"],
                   ["The model cannot be asked this question: the callable branches are different architectures.",
                    "Akhmeteli: arch_monolithic uses a single-layer shell with nu=0.3 and K_SHELL=0.2. "
                    "The paper uses two boron-carbide faces (nu=0.17) and a honeycomb core; sandwich stiffness "
                    "and intracell buckling are absent from this function. Its FEA did not apply the 0.2 knockdown.",
                    "Jenett: arch_tube_strut is a volume-filling octet, with Euler/local co-critical optimized "
                    "R/t, K_CLASSICAL*K_LOCAL and LATTICE_SF. The paper uses a spherical lattice shell, "
                    "thickness/R=0.1, pitch/thickness=0.1 and fixed tube R/t=10; it defers imperfection factors.",
                    "Each paper's material and 101 kPa are passed unchanged. Its own air density is recorded "
                    "but cannot be passed to either architecture function. No ISA density is substituted.",
                    "The diagnostic kg/m3 outputs are not shell mass or net lift; their differences from "
                    "the paper's kg values are undefined."],
                   "Both candidate architecture functions run with the paper's material and pressure, but "
                   "neither can calculate that paper's design. Their raw outputs are retained in JSON; the "
                   "requested mass and lift rows remain unavailable. This is a documented limit of reproduction, "
                   "not a failed replication of either paper.")
    vacuum["model_diagnostics"] = {"akhmeteli_monolithic": monolithic, "jenett_tube_strut": lattice}

    he = helium_output()
    he_rows = [
        row("helium density: model at 2500 m / NIST at sea level", he["helium"]["gas"],
            reference(refs, 30, value=n(30), unit="kg/m3"), "kg/m3",
            n(30) * t["helium"]["density_relative"], t["helium"]["reason"], NC, difference=False),
        row("helium net lift: model at 2500 m / derived sea-level difference", he["helium"]["net"],
            reference(refs, 31, value=n(31), unit="kg/m3"), "kg/m3",
            t["helium"]["derived_lift_kg_m3"], t["helium"]["reason"], NC, difference=False,
            reference_class="equation; derived, not measured"),
        row("helium net lift: model at 2500 m / FAA sea-level lift", he["helium"]["net"],
            reference(refs, 32, "helium_gross_lift_lb",
                      n(32, "helium_gross_lift_lb") * LB_KG / n(32, "envelope_m3"), "kg/m3"),
            "kg/m3", t["helium"]["handbook_lift_kg_m3"], t["helium"]["reason"], NC, difference=False),
        row("Zeppelin envelope capacity at standard conditions (unavailable)", None,
            reference(refs, 34, "max_takeoff_weight_kg", n(34, "max_takeoff_weight_kg"), "kg"),
            "kg", None, t["helium"]["reason"], NC)]
    helium = check("6-helium", "Helium and a modern airship", "measured",
                   [function("research/analysis/helium.py", "main"),
                    function("research/analysis/helium.py", "isa")],
                   {"main_arguments": [], "model_atmosphere": he["atmosphere"],
                    "requested_conditions": {"temperature_K": n(0, "T_K"), "pressure_Pa": n(0, "P") * 100},
                    "zeppelin_volume": reference(refs, 33, "easa_issue_10_both_models_envelope_m3",
                                                  n(33, "easa_issue_10_both_models_envelope_m3"), "m3"),
                    "zeppelin_maximum_mass": reference(refs, 34, "max_takeoff_weight_kg",
                                                       n(34, "max_takeoff_weight_kg"), "kg")},
                   he_rows, t["helium"],
                   ["The model cannot be asked this question: helium.main fixes altitude to 2500 m and "
                    "the hull volume; density and net lift are local expressions, not parameterized functions.",
                    "The executable main is run unchanged. Its gas outputs are rounded to four decimals. "
                    "isa is callable at sea level but returns air, not helium; replacing it or copying gas "
                    "expressions here would manufacture a new model.",
                    "No difference is reported across unlike atmospheric conditions. Zeppelin 8425 m3 and "
                    "8050 kg are retained side by side; maximum weight is not measured gross lift.",
                    "Manufacturer weight has medium confidence. Neither empty mass nor printed gross lift "
                    "was found. Purity, ballonets, superheat, static heaviness and dynamic lift are not inferred.",
                    "The FAA handbook and the derived NIST/1976 lift remain separate references."],
                   "The existing helium executable runs, but only supplies its fixed 2500 m gas ledger. "
                   "It cannot supply helium density at the NIST state or standard-condition capacity for the "
                   "8425 m3 Zeppelin against the manufacturer's 8050 kg maximum mass. Those comparisons are "
                   "not comparable until the model exposes suitable inputs; the checker does not copy its equations.")
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
            lines += ["", "Required/available ratios: " +
                      "; ".join(f"{r['label']}: {r['ratio']:.9g}" for r in c["rows"]) + "."]
        if c["id"] == "5-vacuum-shells":
            lines += ["", "Callable diagnostic outputs (different architectures; no kilogram comparison): " +
                      "; ".join(f"{name}: {value['latticeKgPerM3']:.9g} kg/m3"
                                for name, value in c["model_diagnostics"].items()) + "."]
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
              "This report uses only the supplied source set; missing measurements remain missing.", ""]
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
            print("labelledcheck: 35 normalised source records pass schema")
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
        print("labelledcheck: 6 checks computed; 35 source records valid; reports " +
              ("updated" if args.update else "match"))
        print("; ".join(f"{c['id']}: {c['verdict']}" for c in report["checks"]))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, ImportError,
            ArithmeticError, subprocess.SubprocessError) as exc:
        print("labelledcheck: cannot run: " + safe_error(str(exc)), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
