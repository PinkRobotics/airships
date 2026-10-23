#!/usr/bin/env python3
"""Render the requested card and unresolved issues from computed results."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT/"INPUTS.json").read_text())
O = json.loads((ROOT/"RESULTS.json").read_text())
op, co = O["scenarios"]["optimistic"], O["scenarios"]["conservative"]
L = I["case"]["lift0_kg"]
S = I["sources"]

issues = [
    ("SITE", "QUESTIONABLE", "No operating site, measured temperature/pressure/humidity envelope or cold-case minimum is specified. The selected weather cases are assumptions, not site return-period limits.", "Replace the declared envelope with station data and operating constraints; recompute both mass and maximum differential-pressure cases."),
    ("PAYLOAD", "QUESTIONABLE", "Zero payload is an unladen demonstrator choice. The former 009c5 payload/margin number cannot simultaneously be mission payload and contingency.", "Set payload and remaining float reserve separately. The +100 kg case is supplied."),
    ("LEAK", "QUESTIONABLE", "Whole-hull leakage, trapped core gas, moisture desorption and outgassing have not been measured. The 30-50 kg passive package is a bill-of-mass estimate, not demonstrated vacuum retention.", "Measure normalized total gas load through a complete representative panel/valve assembly, then the hull. For the stated 24 h, pstart=10 Pa at T0 and Tint<=320 K, Qref must be <=40.71949 Pa m3/s."),
    ("PANELS", "PROJECTION", "Neither 4 m nor 0.6 m curved thin S200F sandwich panels are established catalog products. The predecessor's 0.6-1.2 m rolled-sheet availability claim lacked a qualifying source. Required 18 m equivalent widths also exceed the local square-panel approximation's useful domain.", "Obtain a manufacturer-specific material grade, size, forming route, thickness tolerance and yield quote; replace 2A/w with a spherical seam-layout takeoff."),
    ("JOINTS", "QUESTIONABLE", "Two face strips, their bond lines, core splice and full-area face/core adhesive are now counted. Strip sizing and .015/.030 lb/ft2 film use are not qualified for Be, peel, thermal cycling or vacuum; .015 is only a mass lower choice.", "Test a complete seam and bond architecture and measure its installed mass, leak rate and stiffness; do not infer that seam-only panel width closes the full joint allowance."),
    ("SYSTEMS", "QUESTIONABLE", "The battery estimate assumes 150 Wh/kg packaged, 80% usable and 90% conversion. Catalog pump speed/power are not installed duty measurements; the smaller SV220B cannot meet the stated hot-gas flow at the fixed pressure cap.", "Measure the SV300B or alternative system's curve, input power, cooling, line conductance and duty cycle; procure a qualified power package. Passive and 8 h sensitivities isolate the endurance assumption."),
    ("MATERIAL-GRADE", "QUESTIONABLE", "The current Materion forms sheet lists 290 GPa for S200F and 303 GPa for S200FH. Main comparisons deliberately retain the pinned 303 GPa, 283 MPa compression and nu=0.33; the 290 GPa sensitivity is supplied.", "Reconcile the exact grade, compression basis, Poisson ratio and sheet/curved-face properties before revising the material point; do not substitute a tensile value for compression."),
    ("BRANCH", "QUESTIONABLE", "The inherited Vc=2 rule changes gamma from kd to 1. MAINLINE-018 owns its physical assessment. Under large reserve the aramid optimum leaves the crimp branch, invalidating constant-slope extrapolation.", "Resolve the knockdown/branch model and recompute the same margin lines; this card preserves the ordered scoring rule."),
    ("GETTERS", "QUESTIONABLE", "SAES explicitly offers room-temperature nitrogen sorption. The unfinished script's blanket denial and unsourced N2 capacity band cannot support its mass result. All-air getter lifetime including noble gases remains unsized.", "Use measured species loads, sorption speeds and capacities with activation conditions; do not award a getter-only all-air system a mass credit."),
    ("GEOMETRY-MODES", "PROJECTION", "The severe case mathematically selects about 0.056-0.057 mm Be faces and 6.8-8.3 mm core. These are unqualified fabrication and continuum-model geometries; every scored least factor is far below 1.", "Treat the result as an estimate of the gap, not a build point; local face/core geometry, buckling imperfections, seam load transfer and nonlinear validation remain open."),
    ("ENVIRONMENT", "QUESTIONABLE", "Water films are equivalent retained thickness over the whole area, not rainfall depths. Moisture absorbed in core, corrosion, thermal gradients and property derating are not separately quantified here. Gas temperature <=320 K is an acceptance condition, not a thermal prediction.", "Measure water shedding, conditioning, absorbed moisture and thermal response for the selected assembly."),
    ("OTHER-MASS", "QUESTIONABLE", "This closes the card's explicit budget, not every aircraft subsystem. Separate coating, hardpoint/spreader, mooring attachment, handling, navigation or propulsion masses are not individually sized. The optimistic case retains 70 kg of unused system allowance; the active case has no such spare allowance.", "Allocate each needed item explicitly before calling this a complete vehicle mass statement; do not spend retained allowance twice."),
    ("RESERVE", "QUESTIONABLE", "The summed margin is consumed at the declared design condition; it is not an additional residual flight contingency or positive safety factor. The cases do not form a statistical confidence interval.", "Specify residual operational lift reserve and contingency after the environmental/system charges; add that amount to the budget."),
    ("PREDECESSOR-ARITHMETIC", "QUESTIONABLE", "The inherited partial script was not runnable and omitted the 86400 divisor in gas throughput plus the g-to-kg conversion for getter mass. MAINLINE-016 used a linear temperature loss and a constant-final-ratio commissioning expression.", "Use this script's normalized throughput, exact p/T climate calculation and variable-pressure reversible integral. Actual ground pump-down energy still needs measurement."),
]
nfi = {
    "schema": 1, "card": "MAINLINE-019", "status": "OPEN_ISSUES_RECORDED",
    "certification": False,
    "rows": [dict(id="NFI-019-"+key, tag=tag, status="open", issue=issue, next_evidence=next_evidence)
             for key,tag,issue,next_evidence in issues],
}
(ROOT/"NFI.json").write_text(json.dumps(nfi,indent=2)+"\n")

lines = [
    "# MAINLINE-019 — float-margin budget",
    "",
    f"The declared optimistic case needs **{op['margin_kg']:.1f} kg ({op['margin_pct']:.2f}% of reference lift)**. "
    f"The declared conservative case needs **{co['margin_kg']:.1f} kg ({co['margin_pct']:.2f}%)**. "
    f"The old 5% reserve is {0.05*L:.1f} kg, short by {op['surplus_over_5pct_kg']:.1f} kg even in the optimistic case. "
    "These are conditional planning budgets, not measured site requirements or probability bounds. "
    "All inputs and estimates are QUESTIONABLE; unestablished panel/fabrication routes are PROJECTION. No certification.",
    "",
    "Both requested points are retained: Be / Hexcel HRH-10-4.8-32 aramid, and Be / Hexcel CR-III 5056 1/4-1.6 aluminium honeycomb. "
    "The pinned face properties and branch rule are unchanged. Payload is zero for this unladen demonstrator. "
    "The old margin is not also counted as payload.",
    "",
    "## Budget and accounting",
    "",
    "The optimistic package is ground-serviced and sealed for 24 h, with a projected 4 m panel width, "
    "0.1 mm equivalent retained water, +10 K, ±1% pressure, and 1 kPa vapour partial pressure. "
    "The conservative package has 24 h onboard electric pumping, an assumed 0.6 m panel width, "
    "1 mm retained water, +25.1 K, ±2% pressure, and 6 kPa vapour pressure. "
    "The panel sizes, weather and endurance are explicit design choices; no actual site or procurement establishes them.",
    "",
    "For each reserve M, S=(L−100−M)/1.05 is faces plus core. Each family independently maximises its least factor on that mass line. "
    "Then seam mass and the shrinking 0.05S joint allowance are recalculated. "
    "M is increased until BOTH families cover their item sums. The aluminium family sets the common budget below. "
    "Only expenditure above the existing 100 kg systems and 5% joint allowances is charged; unused allowance stays reserved.",
    "",
    "| Charge beyond the base hull (kg) | Optimistic | Conservative | Basis |",
    "|---|---:|---:|---|",
]
labels = [
    ("systems_excess_kg","Systems excess","Hardware + power + controls, less 100 kg"),
    ("joints_and_bondfilm_excess_kg","Joints and bond-film excess","Two face splices, core splice, both full-area bonds; less 0.05S"),
    ("retained_water_kg","Retained water","1000 A δ"),
    ("contamination_kg","Contamination","Owner allowance"),
    ("temperature_pressure_loss_kg","Temperature and pressure lift loss","Exact ideal-gas p/T ratio, low-pressure/hot corner"),
    ("humidity_loss_kg","Additional humidity loss","Ideal-mixture correction, assumed vapour pressure"),
    ("internal_gas_kg","Internal air","1% of reference lift; finite vacuum tolerance"),
    ("payload_kg","Payload","Unladen case; see sensitivity"),
]
for key,label,basis in labels:
    x,y = op["budgets"]["aluminium"]["lines"][key],co["budgets"]["aluminium"]["lines"][key]
    lines.append(f"| {label} | {x:.2f} | {y:.2f} | {basis} |")
lines.extend([
    f"| **Total** | **{op['margin_kg']:.2f}** | **{co['margin_kg']:.2f}** | Common sufficient reserve |",
    "",
    "The aramid totals are 529.92 and 4205.89 kg on the same two mass lines; the common reserves leave 6.03 and 23.19 kg above those sums. "
    "This reserve is spent on the stated condition, not left over afterward.",
    "",
    f"Systems total 30 kg optimistic (15 kg vacuum hardware, 10 kg power package, 5 kg controls; owner estimates). "
    f"The active total is {co['budgets']['aluminium']['systems']['total_kg']:.2f} kg: 223 kg pump, "
    f"{co['budgets']['aluminium']['systems']['power_package_kg']:.2f} kg battery package and 20 kg controls/plumbing. "
    "Battery mass is 5505 W × 24 h / (150 Wh/kg × 0.8 usable × 0.9 conversion); those battery factors are assumptions. "
    f"The pump reference is [Leybold SV300B, 50 Hz]({S['pump']['url']}), not the predecessor's ideal-work power estimate.",
    "",
    "Seams use 2A/w unique boundaries, with a strip and adhesive on EACH face plus one through-core splice. "
    "Strip widths 60/120 mm, local adhesive 0.2/0.3 mm, and core splice width 1.5/3 mm are inherited owner assumptions, not validated joints. "
    f"Both full-area face/core bonds add 184.06/368.13 kg at the published .015/.030 lb/ft² [3M film weights]({S['film']['url']}). "
    "Their Be-bond suitability remains unqualified. The pinned bare face/core masses contain no such adhesive.",
    "",
    f"Climate uses Lday/L0=[1−Δp−0.378 e/p0] T0/(T0+ΔT), the [ideal-mixture limit]({S['air']['url']}); "
    "the full CIPM metrology correlation is not extrapolated to 310 K. High-pressure structural loading is checked separately. "
    "A +25.1 K change alone loses 395.89 kg, not the first-order 430.77 kg; the old 5% hull still ends 151.41 kg heavy.",
    "",
    "## Both families on each margin line",
    "",
    "| Reserve | Core | Face tf (mm, each) | Core (mm) | Vc | gamma | Least SF |",
    "|---|---|---:|---:|---:|---:|---:|",
])
for margin_label, pts in [
    ("0%",{f:O["baseline_margin_sweep"][f]["0.0"] for f in I["cores"]}),
    ("5%",{f:O["baseline_margin_sweep"][f]["0.05"] for f in I["cores"]}),
    (f"{op['margin_pct']:.2f}%",op["points"]),
    (f"{co['margin_pct']:.2f}%",co["points"]),
]:
    for family,p in pts.items():
        lines.append(f"| {margin_label} | {family} | {1000*p['tf_m']:.6f} | {1000*p['core_m']:.5f} | {p['Vc']:.5f} | {p['gamma_d']:.2f} | {p['least_SF']:.9f} |")
lines.extend([
    "",
    "Direct evaluation reproduces filed 009c-5 at 0.650411843681 and the original 014b grid at 0.668649769509. "
    "The table uses continuous refinement, which accounts for the small increases at the reference rows. "
    "At the optimistic line, aramid balances crimp/global and wrinkling; aluminium balances global buckling and wrinkling. "
    "At the conservative line both are on the stiff branch, governed by global buckling. Every factor remains below 1.",
    "",
    f"The maximum-pressure corner gives optimistic least factors {op['points']['aramid']['worst_pressure_least_SF']:.6f}/"
    f"{op['points']['aluminium']['worst_pressure_least_SF']:.6f} and conservative "
    f"{co['points']['aramid']['worst_pressure_least_SF']:.6f}/{co['points']['aluminium']['worst_pressure_least_SF']:.6f} "
    "(aramid/aluminium). On a fixed geometry, only stiff-branch global buckling scales with kd; crimp-branch global/crimp uses gamma=1. "
    "Re-optimising at another kd may change the governing mode, so the whole least factor is not uniformly scaled.",
    "",
    "The 0→5% loss per 100 kg is 0.014311 for aramid and 0.021131 for aluminium, versus MAINLINE-006's different P2 systems at "
    "0.008646/0.009517. This is a scale check, not a transferable slope. Aramid's 0→30% slope is constant under this model, "
    "but it cannot be extended through the branch change at large reserve.",
    "",
    "## Vacuum route",
    "",
    "The lightest examined candidate is ground evacuation followed by sealed service: estimated 30–50 kg onboard, "
    "0 W pumping and 5 W monitoring. It is conditional, not a demonstrated vacuum-holding system. "
    "For 24 h, a 10 Pa start referenced to 284.9 K, a 954.61 Pa ceiling, and internal gas no hotter than 320 K, "
    "the total gas load normalised to 284.9 K must be at most 40.7195 Pa m³/s. "
    "The budget retains 48.89 kg for internal air. Exact p_inside=0 cannot be maintained by a finite real system; "
    "the scored pressure load still uses an empty hull, conservatively.",
    "",
    "At the inherited 1%-per-day air ingress, required effective speed is 174.53 m³/h at reference temperature and "
    "196.04 m³/h at 320 K and the fixed ceiling. The selected catalog reference has 240 m³/h nominal pumping performance "
    "and 5.5 kW maximum motor rating; inlet conductance, installed power and thermal duty still need measurement. "
    "Ground equipment is excluded from flying mass, not from project cost.",
    "",
    f"[SAES offers nitrogen sorption at room temperature]({S['getter']['url']}); the partial script's blanket rejection is incorrect. "
    f"[Hybrid NEG/ion systems]({S['getter_hybrid']['url']}) address additional species, but no capacity/rate data here size a full-air getter system. "
    "No getter mass credit is awarded. Correct throughput is 46.2807 Pa m³/s, not 86,400 times that; "
    "the unfinished getter result also missed grams-to-kilograms conversion. "
    "The reversible variable-pressure ground pump-down minimum to 1% pressure is 104.85 kWh; actual plant energy is unmeasured.",
    "",
    "## Panel size and present availability",
    "",
    "At the shared 5% line, the joint allowance is 216.43 kg. Seams ALONE fit it at optimistic square-equivalent widths "
    "2.684 m (aramid) and 2.801 m (aluminium), or conservative widths 5.716/5.950 m. "
    "With the optimistic full-area bond films included, the same algebra requires 17.946/18.731 m; "
    "those dimensions are outside the useful local-panel approximation and do not establish a buildable spherical layout. "
    "With the conservative films, adhesive alone exceeds the allowance: no panel width closes that 5% total-joint budget.",
    "",
    f"[Materion lists S200F as consolidated rod/bar/block]({S['be_forms']['url']}), not an established rolled-sheet panel. "
    "No examined primary source establishes the required multi-metre, sub-millimetre, curved S200F face panels today. "
    "Even the 0.6 m case is a procurement assumption, not a verified stock limit. The complete panel route stays PROJECTION. "
    "The same current sheet lists S200F at 290 GPa; keeping all else pinned but using 290 GPa gives optimistic factors "
    "0.601843/0.539000. Resolve that grade mismatch separately rather than silently altering the ordered lead points.",
    "",
    "## Sensitivities, evidence and handoff",
    "",
    "| Variant | Reserve kg | Reserve % | Aramid least SF | Aluminium least SF |",
    "|---|---:|---:|---:|---:|",
])
for label,key in [
    ("Conservative weather/panels, sealed service","conservative_environment_passive_service"),
    ("Conservative weather/panels, 8 h active power","conservative_environment_8h_active"),
    ("Optimistic plus 100 kg payload","optimistic_plus_100kg_payload"),
]:
    a = O["variants"][key]
    lines.append(f"| {label} | {a['margin_kg']:.2f} | {a['margin_pct']:.2f} | {a['points']['aramid']['least_SF']:.6f} | {a['points']['aluminium']['least_SF']:.6f} |")
lines.extend([
    "",
    "Removing the onboard pump does not rescue small-panel, wet, hot-day operation. These sums also leave coating, hardpoint, "
    "handling and any propulsion allocations unresolved; NFI.json records those gaps and the exact operational assumptions.",
    "",
    "Started from the predecessor's unfiled script and pinned 009c-5/014b/016/006 records. "
    "The delivered script independently reproduces the original points, refines both geometries and closes both scenario budgets. "
    "Validation includes 100,001-point search comparisons and independent 40-digit scalar pressure/mass calculations; "
    "34 file pins were rechecked. This is arithmetic verification, not structural qualification. "
    "RESULTS.json contains all six scored modes, geometry, line items, formulas, sensitivities and measured run times. "
    "INPUTS.json contains source pins and every scenario choice; NFI.json contains 14 open issues.",
    "",
    "The next evidence with the most value is a qualified seam/panel takeoff and measured whole-assembly gas load, "
    "paired with a specified site and payload. The brief names no executable successor: stop and file; the robotics seat supplies the next job.",
    "",
    "![Margin and budget comparison](margin-budget.png)",
    "",
    "Reproduce locally: `python3 prepare_inputs.py`, `python3 compute.py`, "
    "`TMPDIR=unpublished-local-ref:1ffe4110219d37c0 MPLCONFIGDIR=unpublished-local-ref:d7084a936ed02180 python3 check_and_plot.py`, "
    "`python3 build_card.py`. No other seat's files are written.",
])
(ROOT/"CARD.md").write_text("\n".join(lines)+"\n")
O["computed_at"] = O.get("computed_at",O["ended_at"])
O["ended_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
O["completion_scope"] = "Card, input record, issues, calculations and numerical verification completed; independent ship checker follows filing."
(ROOT/"RESULTS.json").write_text(json.dumps(O,indent=2,allow_nan=False)+"\n")
print(json.dumps({"card":str(ROOT/"CARD.md"),"open_issues":len(issues),"ended_at":O["ended_at"]}))
