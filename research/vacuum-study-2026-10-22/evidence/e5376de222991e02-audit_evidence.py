#!/usr/bin/env python3
"""Verify pinned non-code evidence, inherited quantities, and displayed claims."""
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads((ROOT / path).read_text())


def save(path, value):
    (ROOT / path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


checks = []


def check(label, actual, expected, evidence, absolute=2e-10, relative=2e-12):
    tolerance = absolute + relative * abs(expected)
    checks.append({
        "quantity": label, "checked_value": actual, "independent_reference": expected,
        "difference": actual - expected, "tolerance": tolerance,
        "pass": abs(actual - expected) <= tolerance, "evidence": evidence,
    })


pin_rows = read("INPUT-PINS.json") + read("SOURCE-INTAKE-PINS.json") + [read("ORIGINAL-BRIEF-PIN.json")]
pin_checks = []
for p in pin_rows:
    rel = p["snapshot"]
    assert Path(rel).suffix not in [".py", ".sh", ".ipynb"], rel
    data = (ROOT / rel).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    pin_checks.append({
        "path": rel, "sha256": digest, "bytes": len(data),
        "pass": digest == p["sha256"] and len(data) == p["bytes"],
    })
save("INPUT-PIN-CHECKS.json", {"count": len(pin_checks), "checks": pin_checks,
                              "passed": all(p["pass"] for p in pin_checks)})

I = read("inputs/034/INPUTS.json")
D = read("INDEPENDENT-RESULTS.json")
g, runs = D["geometry"], D["runs"]
up = "inputs/034-extra/upstream/"
p2 = read(up + "021b/RESULTS.json")
fp = p2["floating_point"]
for key, expected in {
    "face_thickness_m": fp["tf_m"], "core_thickness_m": fp["core_m"],
    "face_mass_kg": fp["masses_kg"]["faces"], "core_mass_kg": fp["masses_kg"]["core"],
    "core_cell_m": fp["core_cell_m"], "panel_width_m": fp["panel_width_m"],
    "systems_allowance_kg": fp["masses_kg"]["systems_allowance"],
    "face_density_kg_m3": p2["case"]["face"]["rho"],
    "bond_film_kg_m2_per_face": fp["bond_film_lb_ft2"] * .45359237 / (.3048 ** 2),
}.items():
    check("P2 inherited " + key, I["P2"][key], expected, up + "021b/RESULTS.json")
check("P2 core mass from material density and geometry", I["P2"]["core_mass_kg"],
      D["reference_area_m2"] * I["P2"]["core_thickness_m"] * fp["core_rho_kg_m3"],
      up + "021b/RESULTS.json")
p3 = read(up + "022c/SAG.json")["cap"]
for key, original in [("kapton", "ti_kapton_019"), ("zylon_barrier", "cfrp_zylon_019")]:
    for field, value in I["P3"][key].items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            check("P3 inherited " + key + "/" + field, value,
                  p3[original]["equilateral"][field], up + "022c/SAG.json#cap/" + original)
old = read(up + "019/INPUTS.json")
for current, source in {
    "sealed_vacuum_hardware_kg": "vacuum_hardware_kg",
    "sealed_power_package_kg": "power_package_kg",
    "sealed_controls_kg": "controls_kg", "monitoring_W": "monitoring_W",
}.items():
    check("019 systems " + current, I["systems"][current],
          old["scenarios"]["optimistic"][source], up + "019/INPUTS.json")
for current, source in {
    "battery_Wh_kg": "battery_pack_Wh_kg",
    "battery_usable_fraction": "usable_fraction",
    "power_conversion_efficiency": "electrical_efficiency",
}.items():
    check("019 power " + current, I["systems"][current],
          old["scenarios"]["conservative"][source], up + "019/INPUTS.json")
for current, source in {
    "R_m": "radius_m", "p_external_Pa": "p0_Pa", "T_K": "T0_K",
    "lift_reference_kg": "lift0_kg",
}.items():
    check("019 environment " + current, I["environment"][current],
          old["case"][source], up + "019/INPUTS.json")
scarf = read(up + "028/INPUTS.json")["assumptions"]
for current, source in {
    "scarf_run_ratio": "scarf_ratio", "scarf_film_kg_m2": "scarf_seam_adhesive_kg_m2",
    "core_splice_gap_m": "core_splice_gap_m",
    "core_splice_density_kg_m3": "core_splice_density_kg_m3",
    "seal_mass_kg_per_unique_m": "sealing_total_both_faces_kg_m",
}.items():
    check("028 joining " + current, I["P2"][current], scarf[source], up + "028/INPUTS.json")
allowables = read(up + "023-corrected/INPUTS.json")["allowables"]
tau = next(x["tau_Pa"] for x in allowables if x["id"] == "EA-9394")
check("Inherited EA9394 nominal shear", I["P3"]["joint_adhesive"]["tau_Pa_from_023"], tau,
      up + "023-corrected/INPUTS.json")

# Primary NASA numerical rows; conditioning and service applicability are separately qualified.
SOURCE = "inputs/034-extra/sources/"
material_rows = []
for fn, ref, expected in [
    ("nasa-outgassing-af163.json", "GSFC22348", 2.59),
    ("nasa-outgassing-af163.json", "GSFC22351", 3.17),
    ("nasa-outgassing-af163.json", "GSFC22354", 4.85),
    ("nasa-outgassing-af163.json", "GSFC22357", 4.42),
    ("nasa-outgassing-kapton-film.json", "GSFC10365", .97),
    ("nasa-outgassing-mylar.json", "GSFC32902", .26),
    ("nasa-outgassing-graphite-epoxy.json", "GSFC12224", .57),
    ("nasa-outgassing-ea9394.json", "GSFC35448", 2.63),
]:
    data = read(SOURCE + fn)["data"]
    row = next(row for row in data["data"] if row[1] == ref)
    check("NASA TML percent " + ref, float(row[3]), expected, SOURCE + fn)
    material_rows.append(dict(zip(data["headers"], row)))
save("NASA-ROWS-CHECKED.json", material_rows)

# Values independently read from manufacturer tables and curve.
for species, value in {"CO2": 6840, "O2": 3800, "H2": 38000, "N2": 910, "He": 63080}.items():
    check("Kapton source transmission " + species, I["kapton"]["gas_ml_m2_day_MPa"][species],
          value, SOURCE + "kapton-summary-fralock.pdf#Table10")
for label, actual, expected, evidence in [
    ("Kapton water g/m2/day at 25um", I["kapton"]["water_g_m2_day"], 54, "kapton-summary-fralock.pdf#Table10"),
    ("Kapton equilibrium moisture", I["kapton"]["moisture_fraction_50RH"], .018, "kapton-summary-fralock.pdf#Table10"),
    ("Mylar oxygen cc/m2/day", I["mylar"]["O2_cc_m2_day_pure_O2"], .5, "barrier-flex-pack-films-2001.pdf"),
    ("Mylar water strict source upper bound g/m2/day", I["mylar"]["water_g_m2_day_upper"], 1, "barrier-flex-pack-films-2001.pdf"),
    ("PET density kg/m3", I["zylon"]["barrier_PET_density_kg_m3"], 1390, "mylar-physical-thermal.pdf"),
    ("Zylon HM moisture fraction", I["zylon"]["moisture_fraction"], .006, "zylon-hp-fiber-data.pdf#moisture"),
    ("KNF APDCB mass kg", I["systems"]["KNF_N920_APDCB"]["pump_kg"], 8.5, "knf-n920.pdf#page1"),
    ("KNF APDCB electrical W", I["systems"]["KNF_N920_APDCB"]["input_W"], 100, "knf-n920.pdf#page3"),
    ("KNF APDCB ultimate upper limit Pa", I["systems"]["KNF_N920_APDCB"]["ultimate_Pa"], 150, "knf-n920.pdf#page3"),
    ("Edwards mass kg", I["systems"]["Edwards_E2M28"]["pump_kg"], 44, "Edwards manual A37310880_X Table3, independently read through web"),
    ("Edwards 50Hz speed m3/h", I["systems"]["Edwards_E2M28"]["nominal_speed_50Hz_m3_h"], 27.5, "Edwards manual A37310880_X Table2"),
    ("Edwards mechanical W", I["systems"]["Edwards_E2M28"]["motor_mechanical_W"], 750, "Edwards manual A37310880_X Table5"),
    ("Edwards water kg/h", I["systems"]["Edwards_E2M28"]["max_water_kg_h"], .7, "Edwards manual A37310880_X Table2"),
    ("Edwards ultimate with ballast Pa", I["systems"]["Edwards_E2M28"]["ultimate_with_ballast_Pa"], 3, "Edwards manual A37310880_X Table2"),
    ("BASF4A catalog kgwater/kgbed", I["getters"]["water_capacity_kg_kg_catalog"], .21, "basf-sorbead-air.pdf#Table1"),
    ("SAES D100-5 NEG mass kg", I["getters"]["NEXTorr_D100_5_getter_kg"], .0135, "saes-nextorr-2017.pdf#D100-5"),
    ("SAES D100-5 N2 TorrL", I["getters"]["NEXTorr_capacity_Torr_l_single_run"]["N2"], .3, "saes-nextorr-2017.pdf#D100-5"),
    ("SAES D100-5 O2 TorrL", I["getters"]["NEXTorr_capacity_Torr_l_single_run"]["O2"], 5, "saes-nextorr-2017.pdf#D100-5"),
]:
    check(label, actual, expected, evidence)
source_count = len(checks)

# Compare every numerical cell of the five CARD tables at its printed precision.
tables, current = [], []
for line in (ROOT / "inputs/034/CARD.md").read_text().splitlines():
    if line.startswith("|"):
        current.append([s.strip() for s in line.strip().strip("|").split("|")])
    elif current:
        tables.append(current)
        current = []
if current:
    tables.append(current)
assert len(tables) == 5
names = ["P2", "P3_Kapton", "P3_Zylon_barrier"]
for index, table in enumerate(tables):
    for material, row in zip(names, table[2:]):
        ref = runs[material]["conditioned_reference"]
        src, eq = ref["sources"], D["equipment"][material]
        env = ref["times_constant_source_upper_envelope"]
        if index == 0:
            expected = [g[material][k] for k in ["gas_volume_m3", "seam_m", "nodes"]]
        elif index == 1:
            rates = src["permeation_zero_internal_kg_day"]
            expected = [sum(v for k, v in rates.items() if k != "H2O"), rates["H2O"],
                        sum(src["leak_kg_day"].values()),
                        sum(src["release_inventory_by_species_kg"].values())]
        elif index == 2:
            expected = [env["gas_inventory_limit_days"], env["external_added_mass_limit_days"],
                        env["pressure_limit_days_instant_320K_envelope"],
                        ref["times_partial_pressure"]["pressure_limit_days_instant_320K_envelope"]]
        elif index == 3:
            samples = ref["samples_constant_upper"]
            expected = [samples[0]["pressure_after_instant_heat_to_320K_Pa"],
                        samples[1]["pressure_after_instant_heat_to_320K_Pa"],
                        samples[0]["gas_mass_kg"], ref["max_total_leak_24h"]["total_leak_Pa_m3_s"]]
        else:
            pump = eq["KNF_N920_APDCB" if material == "P2" else "Edwards_E2M28"]
            expected = [[30, 50], eq["water_sorbent_only_24h"]["dry_system_kg_assumed"],
                        pump["installed_system_kg_continuous_24h"], pump["electrical_W"]]
        for col, (cell, val) in enumerate(zip(row[1:], expected), start=1):
            tokens, values = (cell.split("–"), val) if isinstance(val, list) else ([cell], [val])
            for token, number in zip(tokens, values):
                d = Decimal(token)
                half_unit = float(Decimal(10) ** d.as_tuple().exponent / 2)
                check(f"CARD table {index+1}/{material}/column{col}/{token}",
                      float(d), number, "inputs/034/CARD.md", absolute=half_unit + 1e-12, relative=0)

# Narrative arithmetic, independently derived rather than copied from filed results.
P2, K, Z = g["P2"], g["P3_Kapton"], g["P3_Zylon_barrier"]
L = D["systems_ledger"]
for label, printed, val in [
    ("P2 face mm", ".691748", P2["face_thickness_m"]*1000),
    ("P2 core mm", "30.1182", P2["core_thickness_m"]*1000),
    ("P2 panel m", "3.12780", I["P2"]["panel_width_m"]),
    ("P2 AF mass kg", "368.126", P2["bond_film_mass_kg"]),
    ("P2 scarf kg", "2.351", P2["scarf_both_faces_mass_kg"]),
    ("P2 splice kg", "6.091", P2["core_splice_mass_kg"]),
    ("P2 seal kg", "1.618", P2["seal_mass_kg"]),
    ("Kapton gauge um", "549.901", K["film_thickness_m"]*1e6),
    ("Zylon gauge um", "110.783", Z["film_thickness_m"]*1e6),
    ("Zylon fiber kg", "217.175", Z["structural_film_mass_kg"]),
    ("Zylon CFRP wraps kg", "23.181", Z["joint_mass_kg"]),
    ("Zylon SiC tubes kg", "3957.589", Z["tube_mass_kg"]),
    ("Kapton sag volume m3", "49.845", K["sag_loss_m3"]),
    ("Zylon sag volume m3", "153.577", Z["sag_loss_m3"]),
    ("Sphere film area", "1256.637", D["reference_area_m2"]),
    ("P2 trapped air kg", "43.39", P2["unvented_core_air_kg"]),
    ("Kapton trapped air kg", "88.15", K["unvented_tube_air_kg"]),
    ("Zylon trapped air kg", "76.11", Z["unvented_tube_air_kg"]),
    ("Pressure ceiling Pa", "954.608", D["pressure_ceiling_Pa"]),
    ("Gas allowance kg", "48.8944", D["gas_mass_limit_kg"]),
    ("Scarf path mm", "20.764", P2["scarf_path_m"]*1000),
    ("Scarf gap um", "56", P2["scarf_gap_m"]*1e6),
    ("Scarf path area/length", "2.18157", P2["scarf_diffusion_area_over_length_m"]),
    ("P2 all-species permeation kg/day", "1.737e-6",
     sum(runs["P2"]["conditioned_reference"]["sources"]["permeation_zero_internal_kg_day"].values())),
    ("BASF catalog bed kg/kgwater", "4.76", 1/I["getters"]["water_capacity_kg_kg_catalog"]),
    ("SAES N2 getter kg/kg", "29868", D["getter_conversion"]["N2"]["kg_getter_per_kg_gas"]),
    ("SAES O2 getter kg/kg", "1569", D["getter_conversion"]["O2"]["kg_getter_per_kg_gas"]),
    ("KNF installed speed", ".675", D["equipment"]["P2"]["KNF_N920_APDCB"]["effective_speed_m3_h_assumed"]),
    ("P2 hot speed", ".403", D["equipment"]["P2"]["required_effective_speed_m3_h_at_320K"]),
    ("Edwards installed speed", "20.625", D["equipment"]["P3_Kapton"]["Edwards_E2M28"]["effective_speed_m3_h_assumed"]),
    ("Kapton hot speed", "21.112", D["equipment"]["P3_Kapton"]["required_effective_speed_m3_h_at_320K"]),
    ("Zylon hot speed", "8.456", D["equipment"]["P3_Zylon_barrier"]["required_effective_speed_m3_h_at_320K"]),
    ("Kapton pump shortfall %", "2.3", 100*(1-D["equipment"]["P3_Kapton"]["Edwards_E2M28"]["steady_speed_ratio_at_320K"])),
    ("Kapton installed fraction needed", ".768", L["P3_Kapton_E2M28_minimum_speed_fraction_hot_source_envelope"]),
    ("Edwards extra kg", "192.33", D["equipment"]["P3_Kapton"]["Edwards_E2M28"]["excess_over_100kg"]),
    ("30day monitor battery kg", "33.33", L["sealed_system_mass_vs_duration"][2]["minimum_battery_kg_at_assumed_pack_factors"]),
    ("365day monitor battery kg", "405.56", L["sealed_system_mass_vs_duration"][3]["minimum_battery_kg_at_assumed_pack_factors"]),
    ("PET barrier kg", "20.961", Z["barrier_mass_bill_kg"]["PET"]),
    ("Al barrier kg", ".170", Z["barrier_mass_bill_kg"]["Al_assumed_50nm"]),
    ("Barrier attachment kg", "31.416", Z["barrier_mass_bill_kg"]["attachment_lamination_assumed"]),
    ("Total barrier kg", "57.546", L["P3_Zylon_added_barrier_attachment_bill_kg"]),
    ("Kapton joint adhesive kg", "12.565", K["additional_joint_adhesive_kg"]),
    ("Zylon joint adhesive kg", "4.078", Z["additional_joint_adhesive_kg"]),
    ("Zylon lower total kg", "91.624", L["P3_Zylon_system_plus_barrier_plus_joint_bond_kg"][0]),
    ("Zylon upper total kg", "111.624", L["P3_Zylon_system_plus_barrier_plus_joint_bond_kg"][1]),
    ("Zylon residual kg", "8.376", L["P3_Zylon_remaining_of_100kg_at_low_bill"]),
    ("Zylon overage kg", "11.624", L["P3_Zylon_excess_over_100kg_at_high_bill"]),
]:
    d = Decimal(printed)
    half_unit = float(Decimal(10) ** d.as_tuple().exponent / 2)
    check("CARD narrative " + label, float(d), val, "inputs/034/CARD.md",
          absolute=half_unit + 1e-12, relative=0)

validation = read("inputs/034/VALIDATION.json")
check("Owner validation report count (not an owner-code rerun)", validation["count"],
      len(validation["checks"]), "inputs/034/VALIDATION.json", absolute=0, relative=0)
assert all(c["pass"] for c in validation["checks"])
summary = {
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "checks": len(checks), "passed": sum(c["pass"] for c in checks),
    "source_and_inheritance_checks": source_count,
    "display_and_validation_metadata_checks": len(checks)-source_count,
    "pinned_snapshot_checks": len(pin_checks),
    "owner_code_opened_or_executed": False,
}
save("EVIDENCE-CHECKS.json", {"summary": summary, "checks": checks,
                              "mismatches": [c for c in checks if not c["pass"]]})
print(json.dumps(summary, indent=2))
for c in checks:
    if not c["pass"]:
        print(json.dumps(c))
assert all(p["pass"] for p in pin_checks)
assert all(c["pass"] for c in checks)
