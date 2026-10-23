"""Independent arithmetic for MAINLINE-032b; no owner code imports or execution."""
from pathlib import Path
import csv
import json
import math
from collections import Counter

ROOT = Path(__file__).resolve().parent
OWNER = json.loads((ROOT / "inputs/owner032b-RESULTS.json").read_text())
PSI = 6894.757293168361
EC = 15000 * PSI
EF = 290e9
CELL_MM = 3 / 8 * 25.4
GEOMETRIES = [
    ("Be S-200F", .371, .0008434, .02021),
    ("SR-200", .609, .0006917, .03012),
]
LEADS = []
for fc_psi, basis in [
    (60, "stabilised_typical_60_psi"),
    (35, "stabilised_minimum_35_psi"),
]:
    for face, q, tf, tc in GEOMETRIES:
        delta = tc * fc_psi * PSI / EC * (.82 / q - 1) / .64 * 1000
        LEADS.append(dict(face=face, Q=q, Fc_basis=basis, delta_mm=delta))

EXPECTED = {}
def put(path, value):
    assert path not in EXPECTED, path
    EXPECTED[path] = value

def ratios(path, quantity):
    for i, lead in enumerate(LEADS):
        p = f"{path}/{i}"
        put(p + "/Q", lead["Q"])
        put(p + "/needed_delta_mm", lead["delta_mm"])
        put(p + "/measured_over_needed", quantity / lead["delta_mm"])
        put(p + "/needed_amplitude_exceeded_as_a_number",
            quantity > lead["delta_mm"])

put("/not_a_certification", True)
put("/nothing_here_certifies_a_hull", True)
for i, lead in enumerate(LEADS):
    put(f"/needed_lead_amplitudes_mm/{i}/Q", lead["Q"])
    put(f"/needed_lead_amplitudes_mm/{i}/delta_mm", lead["delta_mm"])
put("/smallest_needed_mm", min(x["delta_mm"] for x in LEADS))
put("/largest_needed_mm", max(x["delta_mm"] for x in LEADS))

# Source quantities independently transcribed from Woody pp. 675 and 684.
# The 3 um quantity is template adjustment; the CARD's surface attribution fails.
WOODY_UM = {
    "worst_case_fabrication_rms": 24,
    "installed_estimate_rms": 24,
    "track_rms_typical_low": 10,
    "track_rms_typical_high": 15,
    "sheet_finish_under_10_mm": 2,
    "measurement_accuracy": 5,
    "cso_template_rms": 3,
    "cso_laboratory_estimate_rms": 10,
}
for key, value in WOODY_UM.items():
    put("/woody/figures_mm/" + key, value / 1000)
    ratios("/woody/versus_leads/" + key, value / 1000)
put("/woody/not_delta", True)
put("/woody/beryllium_face", False)

for key, inch in [("cell_scale_depth", .000065), ("cell_node_mismatch", .000057)]:
    p = "/nasa_er_1001/" + key
    put(p + "/printed_inch", inch)
    put(p + "/mm", inch * 25.4)
    ratios(p + "/versus_leads", inch * 25.4)
base = "/nasa_er_1001/three_eighths_cell_slopes_milliradian"
put(base + "/low", .5)
put(base + "/high", 1.6)
for i, millirad in enumerate([.5, 1.6]):
    p = base + f"/projection/{i}"
    rise = millirad / 1000 * CELL_MM
    sine = rise / (2 * math.pi)
    put(p + "/slope_milliradian", millirad)
    put(p + "/sine_zero_to_peak_mm", sine)
    put(p + "/rise_across_one_cell_mm", rise)
    put(p + "/rise_across_half_cell_mm", rise / 2)
    ratios(p + "/sine_versus_leads", sine)
    ratios(p + "/one_cell_rise_versus_leads", rise)

put("/nrao_65r_30/mm_from_printed_inch", .008 * 25.4)
put("/nrao_65r_30/printed_mm", .20)
ratios("/nrao_65r_30/versus_leads_using_inch_conversion", .008 * 25.4)
ratios("/nrao_65r_30/versus_leads_using_printed_mm", .20)
put("/ams7902/g_identity_read/sheet_inch/0", .020)
put("/ams7902/g_identity_read/sheet_inch/1", .250)
put("/ams7902/class_tolerances_read", False)

def scalar_leaves(value, path=""):
    if isinstance(value, dict):
        for key, val in value.items():
            yield from scalar_leaves(val, path + "/" + key)
    elif isinstance(value, list):
        for i, val in enumerate(value):
            yield from scalar_leaves(val, path + "/" + str(i))
    elif isinstance(value, (int, float, bool)):
        yield path, value

actual = dict(scalar_leaves(OWNER))
excluded = {"/elapsed_s": "Owner script timer; not an engineering result or review duration."}
assert set(actual) - set(excluded) == set(EXPECTED), (
    set(actual) - set(excluded) - set(EXPECTED),
    set(EXPECTED) - set(actual),
)
rows = []
for path, expected in EXPECTED.items():
    value = actual[path]
    boolean = isinstance(expected, bool)
    passed = value is expected if boolean else math.isclose(value, expected, rel_tol=3e-12, abs_tol=1e-12)
    rows.append(dict(path=path, kind="boolean" if boolean else "numeric",
                     owner=value, independent=expected,
                     delta="" if boolean else value-expected,
                     pass_=passed))
with (ROOT / "NUMERIC-CHECK.csv").open("w") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

# Additional calculations are projections/metric illustrations, not new measurements.
wavelengths = []
for face, q, tf, tc in GEOMETRIES:
    for nu in [0, .33]:
        d = EF * tf**3 / (12 * (1-nu**2))
        half = math.pi * (tc * d / (2*EC))**.25
        wavelengths.append(dict(
            face=face, tag="PROJECTION", poisson_assumption=nu,
            D_Nm=d, half_wavelength_mm=half*1000,
            full_period_mm=2*half*1000,
            half_wavelength_over_cell=half*1000/CELL_MM,
            model="NASA/CR-1999-208994 Eq.19, elastic symmetric flat-panel anti-plane core",
        ))

metric_examples = {
    "er1001_dimple_depth_mm": .000065*25.4,
    "er1001_symmetric_sine_amplitude_from_depth_mm_PROJECTION": .000065*25.4/2,
    "woody_24um_rms_single_sine_amplitude_mm_PROJECTION": math.sqrt(2)*.024,
    "woody_24um_rms_single_sine_amplitude_over_smallest_PROJECTION":
        math.sqrt(2)*.024/min(x["delta_mm"] for x in LEADS),
    "woody_35um_rms_single_sine_amplitude_mm_PROJECTION": math.sqrt(2)*.035,
    "woody_35um_rms_single_sine_amplitude_over_smallest_PROJECTION":
        math.sqrt(2)*.035/min(x["delta_mm"] for x in LEADS),
    "er1001_fig25_face_mm": .008*25.4,
    "er1001_fig30_face_mm": .008*25.4,
}
rion = {
    "provenance": "Rion 2008 thesis, primary experiment; not an as-bonded Be/CR-III measurement",
    "ply_thickness_mm": .07,
    "type1_single_ply_face_mm": .07,
    "type2_and_type3_two_ply_face_mm": .14,
    "core_cell_mm": 3.2,
    "core_thickness_mm": 8,
    "core_density_kg_m3": 29,
    "measured_height_definition": "Cell-wall level to lowest face point within a cell",
    "type1_maximum_depth_mm_at_minus_0p1_bar": .160,
    "type1_maximum_depth_mm_at_minus_0p9_bar": .370,
    "type1_context": "Deliberately exaggerated waves; some cell walls collapse, especially at high pressure.",
    "cross_section_plot_approximate_mean_height_range_mm": [.019, .101],
    "plot_reading_not_raw_data": True,
    "half_wavelength_from_cell_mm": math.sqrt(3)/2*3.2,
    "critical_half_wavelength_reported_mm": 2.79,
    "critical_wavelength_scope": "Two-ply model, Ec=50 MPa and 50 g/m2 adhesive; not the exaggerated single-ply specimens",
    "half_wavelength_ratio": (math.sqrt(3)/2*3.2)/2.79,
    "model_reduction_Wmeas_over_W0": 25,
    "reduction_is_empirical_not_universal": True,
    "one_shot_fit_at_minus_0p7_bar_mm_NOT_RAW_DATUM": 106*.7/1000,
    "two_step_fit_at_minus_0p7_bar_mm_NOT_RAW_DATUM": 105*.7**.3442/1000,
}
comparison = []
for label, mm, kind in [
    ("ER-1001 Fig.25", .001651, "Cell peak-to-valley depth"),
    ("Woody installed fabrication estimate", .024, "Multi-scale RMS estimate"),
    ("von Hoerner/Rohr", .2032, "1969 vendor whole-surface RMS"),
    ("Rion type1 low pressure", .160, "Measured maximum cell depth; exaggerated specimen"),
    ("Rion type1 high pressure", .370, "Measured maximum cell depth; damaged/exaggerated specimen"),
    ("Camarda mean maximum", .097, "Mean of panel maxima from 45-point face profiles"),
]:
    comparison.append(dict(label=label, value_mm=mm, quantity=kind,
                           ratios_as_numbers_only=[mm/x["delta_mm"] for x in LEADS]))

result = {
    "unit": "vacuum-mainline032-check-1020",
    "scope": "Combined 032 + 032b; 032 immutable verified report incorporated",
    "tag": "QUESTIONABLE",
    "prior_032_comparisons_passed": 236,
    "new_032b_scalar_checks": len(rows),
    "new_032b_counts": dict(Counter(x["kind"] for x in rows)),
    "new_032b_failures": [x for x in rows if not x["pass_"]],
    "total_prior_plus_new_comparisons": 236+len(rows),
    "coverage": {"owner_numeric_leaves": 229, "owner_boolean_leaves": 69,
                 "excluded_metadata": excluded, "uncovered_engineering_scalar_leaves": []},
    "lead_amplitudes_recomputed_mm": LEADS,
    "core_Fc_basis": "Conditional 60/35 psi; actual min(compression,tension,bond) not established",
    "wavelength_projections": wavelengths,
    "metric_examples": metric_examples,
    "omitted_primary_experiment": rion,
    "number_only_comparisons": comparison,
    "source_corrections_separate_from_arithmetic": [
        "Woody 3 um is parabolic-template adjustment, not finished CSO surface-versus-template RMS.",
        "ER-1001 Fig.22 identifies Fig.25/specimen30 as .008-inch H19 foil, Crest471, 3/16-inch core.",
        "ER-1001 Fig.30 identifies specimen32 as .008-inch face, APS, .015-inch fillet.",
        "Dimple depth, RMS, slope and modal amplitude remain different quantities.",
        "Rion provides omitted measured thin-face waviness near that system's critical wavelength.",
        "No retrieved source establishes an as-bonded Be/CR-III amplitude in the target wavelength band.",
    ],
}
(ROOT / "RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
assert not result["new_032b_failures"]
print(json.dumps({k:result[k] for k in [
    "new_032b_scalar_checks", "new_032b_counts", "new_032b_failures",
    "total_prior_plus_new_comparisons"]}, indent=2))

