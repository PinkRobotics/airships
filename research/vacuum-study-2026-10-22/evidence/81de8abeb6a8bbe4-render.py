"""Render the completed calculation; imports only this card's own calculator."""
import importlib.util
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

os.environ["MPLCONFIGDIR"] = "unpublished-local-ref:ffe18df165f154bf"
os.environ["TMPDIR"] = "unpublished-local-ref:1ffe4110219d37c0"
sys.dont_write_bytecode = True

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

B = Path(__file__).resolve().parent
I = json.loads((B / "INPUTS.json").read_text())
R = json.loads((B / "RESULTS.json").read_text())
spec = importlib.util.spec_from_file_location("own_calculation", B / "calculate.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
leads = ["P2", "P3_Kapton", "P3_Zylon_barrier"]
names = {"P2": "P2 · Be / aluminium honeycomb",
         "P3_Kapton": "P3 · SiC / Ti joints / Kapton",
         "P3_Zylon_barrier": "P3 · SiC / CFRP joints / Zylon + barrier"}
now = datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharex=True)
ts = np.linspace(0, 30, 401)
for col, lead in enumerate(leads):
    for case, upper, color, ls, label in [
        ("conditioned_reference", True, "#1769aa", "-", "Conditioned · constant source-rate envelope"),
        ("conditioned_reference", False, "#20836d", "--", "Conditioned · partial-pressure model"),
        ("unconditioned", True, "#b54c39", "-", "Unconditioned · constant source-rate envelope"),
    ]:
        src = R["runs"][lead][case]["sources"]
        samples = [model.state(lead, src, float(t), upper) for t in ts]
        axes[0, col].plot(ts, [s["pressure_after_instant_heat_to_320K_Pa"] for s in samples],
                          color=color, ls=ls, label=label, lw=1.8)
        axes[1, col].plot(ts, [s["gas_mass_kg"] for s in samples],
                          color=color, ls=ls, lw=1.8)
    axes[0, col].set_title(names[lead], fontsize=10)
    axes[0, col].axhline(R["pressure_ceiling_Pa"], color="#333333", ls=":", lw=1.2)
    axes[0, col].axhspan(R["pressure_ceiling_Pa"], 1800, color="#eeeeee", zorder=0)
    axes[0, col].set_ylim(0, 1800)
    axes[1, col].axhline(R["gas_mass_limit_kg"], color="#333333", ls=":", lw=1.2)
    axes[1, col].axhspan(R["gas_mass_limit_kg"], 90, color="#eeeeee", zorder=0)
    axes[1, col].set_ylim(0, 90)
    for row in range(2):
        axes[row, col].set_xlim(0, 30)
        axes[row, col].grid(alpha=.2)
        axes[row, col].spines[["top", "right"]].set_visible(False)
    axes[1, col].set_xlabel("Days after ground evacuation")
axes[0, 0].set_ylabel("Pressure after instant heating to 320 K (Pa)")
axes[1, 0].set_ylabel("Free gas inventory (kg)")
fig.suptitle("Holding the vacuum — conditional gas calculations", fontsize=16, y=.99)
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(.5, .04),
           ncol=3, fontsize=8, frameon=False)
fig.text(.5, .012,
         "PROJECTION: unmeasured leaks, source-to-service permeance and release kinetics. "
         "Grey exceeds the chosen limit. The 30 kg package has at most 9 days of monitoring energy.",
         ha="center", fontsize=8)
fig.tight_layout(rect=[0, .085, 1, .95])
fig.savefig(B / "pressure-and-inventory.png", dpi=180)
fig.savefig(B / "pressure-and-inventory.svg")
plt.close(fig)

source_rows = []
for filename in ["nasa-query-sources.json", "equipment-source-pins.json",
                 "additional-source-pins.json"]:
    source_rows.extend(json.loads((B / "sources" / filename).read_text()))
for filename in ["edwards-e2m28-observation.json", "leybold-observation.json"]:
    d = json.loads((B / "sources" / filename).read_text())
    source_rows.append({"file": filename, "url": d["url"], "access": d["access"]})
(B / "SOURCE_CATALOG.json").write_text(json.dumps({
    "schema": 1, "sources": source_rows,
    "carried_primary_PDFs": [
        "sources/kapton-summary-fralock.pdf", "sources/kapton-hn-dupont.pdf",
        "sources/barrier-flex-pack-films-2001.pdf", "sources/zylon-hp-fiber-data.pdf"],
    "notes": "NASA current API queries supply the numerical rows. The retrieved 1997 scan/OCR is not the extraction basis. No owner code was inspected, imported or run."
}, indent=2) + "\n")

def ref(lead):
    return R["runs"][lead]["conditioned_reference"]

gas_rows, life_rows, pressure_rows, equip_rows, geometry_rows = [], [], [], [], []
for lead in leads:
    run, g, eq = ref(lead), R["geometry"][lead], R["equipment"][lead]
    src = run["sources"]
    water = src["permeation_zero_internal_kg_day"]["H2O"]
    dry = sum(src["permeation_zero_internal_kg_day"].values()) - water
    release = sum(src["release_inventory_by_species_kg"].values())
    gas_rows.append(
        f"| {lead.replace('_', ' ')} | {dry:.6g} | {water:.6g} | "
        f"{sum(src['leak_kg_day'].values()):.6g} | {release:.6g} |")
    t = run["times_constant_source_upper_envelope"]
    p = run["times_partial_pressure"]
    life_rows.append(
        f"| {lead.replace('_', ' ')} | {t['gas_inventory_limit_days']:.2f} | "
        f"{t['external_added_mass_limit_days']:.2f} | "
        f"{t['pressure_limit_days_instant_320K_envelope']:.2f} | "
        f"{p['pressure_limit_days_instant_320K_envelope']:.2f} |")
    one, seven = run["samples_constant_upper"][:2]
    pressure_rows.append(
        f"| {lead.replace('_', ' ')} | {one['pressure_after_instant_heat_to_320K_Pa']:.2f} | "
        f"{seven['pressure_after_instant_heat_to_320K_Pa']:.2f} | "
        f"{one['gas_mass_kg']:.3f} | "
        f"{run['max_total_leak_24h']['total_leak_Pa_m3_s']:.3f} |")
    pump = "KNF_N920_APDCB" if lead == "P2" else "Edwards_E2M28"
    equip_rows.append(
        f"| {lead.replace('_', ' ')} | 30–50 | "
        f"{eq['water_sorbent_only_24h']['dry_system_kg_assumed']:.2f} | "
        f"{eq[pump]['installed_system_kg_continuous_24h']:.2f} | "
        f"{eq[pump]['electrical_W']:.0f} |")
    geometry_rows.append(
        f"| {lead.replace('_', ' ')} | {g['gas_volume_m3']:.2f} | "
        f"{g['seam_m']:.2f} | {g['nodes']:.2f} |")

SL = R["systems_ledger"]
kp = R["geometry"]["P3_Kapton"]
zp = R["geometry"]["P3_Zylon_barrier"]
p2 = R["geometry"]["P2"]
card = f"""# MAINLINE-034 — holding the vacuum

**For the inherited 24-hour mission, the lightest examined maintenance option is ground evacuation followed by sealed service, for both leads: an estimated 30–50 kg onboard.** Keep each current model's 100 kg systems allowance reserved. This choice is conditional on measured assembly gas load and evacuation of all internal cells and tube bores. No measured sealed-service life or qualified minimum system mass is established.

Unit `{I['unit']}`; order `{I['order']}`. Started {I['started_at']}; calculation {R['calculated_at']}; card {now}. Times are measurements. Material/source inputs are QUESTIONABLE; service transfers, inventories, leak rates and installation bills are PROJECTION. No certification.

The source-rate calculation gives pressure-limited lives of **398.21 / 7.76 / 19.49 days** for P2 / Kapton P3 / Zylon-barrier P3 under the conditioned reference assumptions. These are gas calculations, not mission endurance. The assumed 10 kg power package can supply 5 W monitoring for at most nine days under the stated battery factors, even if its entire mass is battery. Daily ground re-evacuation is the selected planning interval; longer intervals require measured evidence.

## Geometry and what is actually sealed

P2 adopts 021b's 0.691748 mm Be faces, 30.1182 mm aluminium honeycomb and 3.12780 m square-equivalent panels. Both full-area AF 163-2U bonds total 368.126 kg at 0.030 lb/ft² per bond. The 028 **30:1 scarf method** is re-sized to these faces; its 70 g/m² scarf film is a separate, unqualified adhesive route. It adds 2.351 kg, plus 6.091 kg core splice and 1.618 kg sealing allowance. The older 021b joining reserve is retained; this card does not convert the difference into payload.

P3 adopts 022c's equilateral, 019-reserve rows. The Kapton gauge is **549.901 µm**, rather than 024's 843.031 µm. The Zylon 0/90 structural gauge is 110.783 µm, 217.175 kg of fibre. Both frames retain **SiC tubes**. “Titanium” and “CFRP” name the 023 end fittings; CFRP outgassing is applied to the 23.181 kg of wraps, not the 3957.589 kg of ceramic tubes. An independent mass/section/length check gives 3100 kg/m³ for both tube rows.

| Lead | Gas volume used, m³ | Unique barrier seams, m | Extra node/intersection count |
|---|---:|---:|---:|
{chr(10).join(geometry_rows)}

P2 gas volume subtracts known solid inventory from the reference sphere. P3 volume subtracts the filed cap-sag losses of 49.845 and 153.577 m³; small internal solid volumes are neglected. Film area remains 1256.637 m², with a separate +10% sensitivity. Seam and node counts are continuum approximations, not a manufactured spherical layout.

**Trapped air is consequential.** P2's estimated honeycomb void retains {p2['unvented_core_air_kg']:.2f} kg at ambient conditions if unvented. The P3 tube bores retain {kp['unvented_tube_air_kg']:.2f} kg with Kapton and {zp['unvented_tube_air_kg']:.2f} kg with Zylon if sealed at ambient pressure. That mass is aboard before any release into the main cavity. The base cases require communicating evacuation paths; adding such paths is not silently assumed structurally qualified.

## Inflow and finite outgassing inventories

Nominal conditions are 500 m, 95460.84 Pa, 284.9 K and a stated 1 kPa external water partial pressure inherited from 019's optimistic scenario. Initial internal pressure is 10 Pa. No local weather observation is claimed. The pressure limit is 954.608 Pa, and the gas-inventory and net-added-mass limits are each reported separately at 48.8944 kg.

**P2 permeation.** Through intact Be and aluminium, bulk ambient-gas permeation is set to zero as a screening assumption, not a measured upper bound. The full-area adhesive is behind Be; charging its entire area with the external pressure drop would invent a path. With the core vented inward, the exposed outer scarf supplies the polymer path: 20.764 mm long, assumed 56 µm adhesive gap, area/length 2.18157 m. At an explicitly assumed 10 Barrer it admits 1.737e-6 kg/day; 100 Barrer multiplies that by ten. There is no matched AF/scarf permeability measurement. Pinholes and discontinuities belong in the leak term.

**P3 permeation.** [DuPont's Kapton table](sources/kapton-summary-fralock.pdf) supplies thickness-normalized CO₂/O₂/H₂/N₂/He transmission; Ar is assumed equal to N₂. Its water row is 54 g/(m² day) at 25 µm. The [DuPont Teijin packaging table](sources/barrier-flex-pack-films-2001.pdf) supplies OD3 metallized 12 µm Mylar oxygen transmission of 0.5 cc/(m² day) and water below 1 g/(m² day) at its test conditions. Zylon supplies mechanical reinforcement, with no independent gas barrier. Unmeasured Mylar gas permeances are explicit ratios to oxygen, including a tenfold N₂ sensitivity. Temperature and water-driving-pressure transfers to service remain projections.

**Outgassing is finite in this calculation.** [NASA's database](https://outgassing.nasa.gov/outgassing-data-table) and [test guide](https://etd.gsfc.nasa.gov/capabilities/outgassing-database/user-guide) describe a 125°C, 24-hour test. AF 163-2U records span 2.59–4.85% TML; Kapton-film proxy GSFC10365 is 0.97%; aluminized-Mylar proxy GSFC32902 is 0.26%. CFRP-wrap and EA9394 proxies are 0.57% and 2.63%. These historical lots do not establish service rates. CVCM is not added to TML. The local API extracts preserve the exact rows.

The reference assigns 10% of each screened inventory to post-conditioning release with a one-day exponential time constant; the unconditioned case assigns 100%. [Toyobo's HM moisture value](sources/zylon-hp-fiber-data.pdf), 0.6% at 20°C/65% RH, supplies Zylon's water inventory. P2 core release is an assumed 0.1% of core mass; ceramic surface release is an assumed 0.1 g/m² over inner and outer tube surfaces. Attachment/seal inventories are stated separately. These assumptions are not demonstrated conditioning performance.

Leakage uses 0.001 mbar L/s per metre and per extra node, plus 0.01 mbar L/s for ports, with 0.00001 and 0.1 sensitivity values. P2 counts its outer pressure-barrier seams once; P3 assumes individually joined bays. Frame joints are not automatically pressure penetrations. One mbar L/s equals 0.1 Pa m³/s.

| Reference case | Dry permeation, kg/day | Source water rate, kg/day | Humid-air leaks, kg/day | Residual release inventory, kg |
|---|---:|---:|---:|---:|
{chr(10).join(gas_rows)}

Water dominates the sourced P3 rate. The table is an initial/source-condition calculation, not a measured 500 m whole-hull leak test. The Zylon water entry uses the reported upper value, and the assumed dry-gas contribution is not silently treated as sourced.

## Pressure rise and sealed service

For each species, partial pressure is nRT/V. The calculation integrates permeation proportional to its pressure difference, a stated constant leak load, and finite release B(1−exp(−t/τ)). It also reports a constant source-rate envelope that takes no permeation backpressure credit. The water coefficient in the pressure-dependent case is mapped to the assumed 1 kPa exterior water pressure; the source does not qualify that mapping.

The hot-pressure column is an instantaneous rise to 320 K for the accumulated inventory; no favourable permeability-temperature correction is taken. The explicit solution and dimensions are in [METHOD.md](METHOD.md), with all species, rates, samples and sensitivity cases in [RESULTS.json](RESULTS.json).

| Lead | Days to 48.894 kg free gas, constant-rate envelope | Days to 48.894 kg net external uptake, same envelope | Days to hot pressure ceiling, same envelope | Days to hot pressure ceiling, pressure-dependent model |
|---|---:|---:|---:|---:|
{chr(10).join(life_rows)}

Pressure reaches its limit before the free-gas mass criterion in these cases. A kilogram of water vapour produces more pressure than a kilogram of air. Long mass-crossing times after the pressure limit are diagnostic continuations, not usable operating intervals. The P2 multi-month value depends almost entirely on an unmeasured leak assumption and is not a service-life claim.

| Lead | Hot pressure after 1 day, Pa | After 7 days, Pa | Free gas after 1 day, kg | Maximum total leak for 24 h, Pa m³/s |
|---|---:|---:|---:|---:|
{chr(10).join(pressure_rows)}

These last columns use the constant-rate envelope and conditioned inventory. The total-leak allowance leaves room for the separately modeled permeation and release; it is not an additional leak entitlement. Whole-assembly acceptance must demonstrate the same thermal and gas-load assumptions. High-leak and unconditioned cases in RESULTS show why the reference rates cannot be assumed from adhesive strength or a coupon barrier test.

![Conditional pressure and gas inventory](pressure-and-inventory.png)

**Mass accounting:** gas released by adhesive, film or surfaces was already aboard. It changes phase and pressure, not total vehicle mass a second time. Net external ingress adds vehicle mass. A getter moves gas into a sorbent and retains that external mass; only expulsion, such as pumping, removes it. The free-gas criterion is therefore distinct from the lift debit.

## Maintenance choice and complete mass statement

For a 24-hour ground-serviced cycle, use the sealed route as the lightest examined candidate: 15 kg vacuum hardware, 10 kg power package, 5 kg controls, with a 20 kg installation contingency giving the 30–50 kg range. These remain 019 owner estimates. Pumping power is zero; monitoring is 5 W. Ground equipment is excluded from flying mass, not project cost. Both current lead geometries already carry 100 kg systems, rather than the older 024 50 kg line.

| Lead | Selected sealed system, kg | Water-sorbent-only system, dry kg | Continuous-pump benchmark with 24 h battery, kg | Pump electrical power, W |
|---|---:|---:|---:|---:|
{chr(10).join(equip_rows)}

The sorbent column includes 30 kg base hardware, a 2 kg cartridge and a bed sized at an assumed 10 wt% usable capacity for one day's source-rate water plus release. It does not remove all dry gases. [BASF](sources/basf-sorbead-air.pdf) lists 21 wt% water at 25°C/80% RH, equivalent to 4.76 kg dry bed/kg water; the vacuum planning value is 10 kg/kg. Neither is a measured complete-hull getter result.

[SAES's D100-5 sheet](sources/saes-nextorr-2017.pdf) gives a 13.5 g getter with single-run room-temperature capacities of 0.3 Torr L N₂ and 5 Torr L O₂. At its 25°C condition these correspond to approximately 29,868 and 1,569 kg getter/kg gas. These are separate pure-gas UHV capacity illustrations, not additive mixed-gas capacities or a useful rough-vacuum hull design. Noble gases use its powered ion section. [SAES COMBO](https://www.saesgetters.com/industrial-getters-dispensers/solution/non-evaporable-getters-neg/) does sorb N₂ at room temperature; its opened page does not give capacity/rate data to size this hull. No generic claim that nitrogen cannot be gettered is made.

The P2 pump benchmark is [KNF N920 APDCB](sources/knf-n920.pdf): 8.5 kg and 100 W, with about 0.9 m³/h read from its 10 mbar inlet-speed curve. Assuming 75% installed speed gives 0.675 m³/h against 0.403 m³/h required by the hot steady source envelope. The curve, rather than its 21 STP L/min rating, is used. Transient outgassing still needs inventory storage or ground conditioning.

The P3 benchmark is [Edwards E2M28](sources/edwards-e2m28-observation.json): 44 kg and 27.5 m³/h at 50 Hz, with 0.7 kg/h listed water capacity. The manual's 750 W is mechanical motor output; 1000 W electrical is an explicit planning assumption. The assumed 75% installed speed gives 20.625 m³/h. Hot source-envelope requirements are 21.112 m³/h for Kapton and 8.456 m³/h for Zylon/barrier. Thus the single-pump Kapton benchmark is 2.3% short at that conductance assumption; it requires at least a 0.768 installed/nominal fraction or a larger installation. Its 292.33 kg continuous-duty system exceeds the existing allowance by 192.33 kg before additional membrane assembly costs. Ideal isothermal work is not substituted for electric power.

Battery figures use 150 Wh/kg, 80% usable and 90% conversion, all assumptions. Monitoring alone requires 33.33 kg battery for 30 days and 405.56 kg for a year. Thus a long gas-only life cannot justify the 30 kg package for equally long autonomous operation.

**Zylon assembly debit:** the [Mylar density sheet](sources/mylar-physical-thermal.pdf) gives 1390 kg/m³, making the 12 µm PET substrate 20.961 kg. Add assumed 50 nm Al, 0.170 kg; 25 g/m² attachment/lamination, 31.416 kg; and 5 kg seam installation: **{SL['P3_Zylon_added_barrier_attachment_bill_kg']:.3f} kg**. This is a worked illustrative bill, not a qualified minimum.

The inherited 023 fitting bill also omits bond adhesive. Using its nominal bond area, assumed 0.2 mm gap and 1400 kg/m³ density adds **{kp['additional_joint_adhesive_kg']:.3f} kg** for the Ti/Kapton row or **{zp['additional_joint_adhesive_kg']:.3f} kg** for the CFRP-wrap/Zylon row. This is booked separately, with a NASA EA9394 proxy for release.

For Zylon, the vacuum system, barrier/attachment and fitting adhesive together total **{SL['P3_Zylon_system_plus_barrier_plus_joint_bond_kg'][0]:.3f}–{SL['P3_Zylon_system_plus_barrier_plus_joint_bond_kg'][1]:.3f} kg**. Reallocating the existing 100 kg line leaves only {SL['P3_Zylon_remaining_of_100kg_at_low_bill']:.3f} kg at the low bill; the high bill exceeds it by {SL['P3_Zylon_excess_over_100kg_at_high_bill']:.3f} kg. Other installation and protection terms remain unclosed. Keep the full allowance reserved and award no payload credit.

## Evidence and carry

[INPUTS.json](INPUTS.json) states every value and tag. [SOURCE_CATALOG.json](SOURCE_CATALOG.json), [UPSTREAM_PINS.json](UPSTREAM_PINS.json) and [PRIOR_CHECK_PINS.json](PRIOR_CHECK_PINS.json) preserve provenance. NASA API data, manufacturer PDFs and the KNF curve image are local. Edwards and Leybold were read through the web tool; their direct downloads returned 403, recorded explicitly instead of claiming local PDF pins.

[VALIDATION.json](VALIDATION.json) contains **36 passing checks**, including independent adaptive integration against the analytic pressure curves, integrated external mass flow, threshold residuals, source conversion reproduction and both SiC density identities. No upstream script was inspected, imported or executed. [NFI.json](NFI.json) retains 17 open physical/source issues.

This work does not change structural SF. In particular, the inherited equilateral Kapton row is below unity; the Zylon and P2 structural assumptions remain conditional. The next decisive evidence is a complete-assembly gas-load test after demonstrated conditioning, including every internal cavity, seam and attachment.

The brief says stop and file. No successor is named.
"""
(B / "CARD.md").write_text(card)

method = r"""# MAINLINE-034 method and units

This calculator reads only its own frozen INPUTS.json. It does not execute upstream code.

For species i, use molar inventory n_i and p_i=n_i RT/V. Each source-derived or
assumed initial permeation rate q_i is in mol/day, at zero internal partial pressure.
Its linear pressure dependence is q_i(1-p_i/p_ext,i). The separate leak term l_i is
constant over the near-vacuum operating range. A finite material inventory B_i,
in moles, releases with a declared time constant tau in days:

    dn_i/dt = q_i - k_i*n_i + l_i + B_i/tau*exp(-t/tau)
    k_i = q_i*R*T/(V*p_ext,i)

The closed form is

    n_i(t) = n_i(0)*exp(-k_i*t)
           + (q_i+l_i)*(1-exp(-k_i*t))/k_i
           + (B_i/tau)*(exp(-t/tau)-exp(-k_i*t))/(k_i-1/tau).

Continuous limits are used at zero k and at k=1/tau. expm1 avoids cancellation
in the constant-source integration. The no-backpressure envelope sets k=0:

    n_i(t) = n_i(0)+(q_i+l_i)*t+B_i*(1-exp(-t/tau)).

The latter is a source-rate envelope, not a measured universal service bound.
In particular, water-vapour transmission may change with temperature, humidity,
stress, coating cracks and fabrication. The partial-pressure model maps the
source water rate to the assumed 1000 Pa exterior water pressure. This mapping
is explicitly PROJECTION.

Leaks quoted in mbar L/s multiply by 0.1 to give Pa m3/s. Moles/day are Q*86400/(RT).
Standard-volume film rates use 22414 cc/mol. Kapton's gas coefficient includes
MPa in its denominator; Mylar's rate is normalized to an assumed one-atmosphere
pure-oxygen test. All gases are handled separately. Dry-air fractions are
normalized; 1000 Pa of the 500 m atmosphere is assigned to water.

For gas mass, sum M_i*n_i. For net external uptake, subtract initial free gas
and the cumulative material release from free-gas mass. The same net external
uptake is independently checked by integrating external flux. No getter or
pump is included in these sealed curves. Hot-pressure values multiply the
computed pressure by 320/284.9, representing rapid heating of stored inventory.
No permeability-temperature benefit is assumed.

First crossings of the free-gas mass, net external uptake and pressure limits
are independently bracketed and solved. Continuations after the pressure limit
are diagnostic only. The 24-hour leak budget is solved using the source-rate
envelope and all three criteria, including instantaneous heating to 320 K.

P2: two face/core bonds have mass 2*A*w. A square-equivalent scarf loses r*t_f
of blank span, so unique outer seams total 2*A/(panel_width-r*t_f).
Diffusion path is t_f*sqrt(1+r^2), with gap w_scarf/rho_assumed; gas-path
area/length is seam_length*gap/path. Only the outer barrier is used when
honeycomb is connected inward. This does not invent full-area adhesive
permeation through metal. Two-skin scarf mass is booked separately.

P3: volume is the original sphere minus the 022c sag-equivalent volume.
The full original area is used for baseline film transmission, with a +10%
sensitivity. Both frame rows use SiC tubes. The bore volume is
pi*(r_outer-wall)^2*total_length; it must be included in evacuation. SiC
surface inventory uses the sum of internal and external lateral areas.
CFRP inventory uses only end-wrap mass.

The previously unbooked joint-bond estimate is 2*members*N/tau_adhesive times
an assumed 0.2 mm gap and 1400 kg/m3 density. It is a mass/gas screen at the
inherited nominal shear sizing, not a qualified joint design.

Pump comparison uses effective inlet volumetric speed Q/p, not STP delivery.
Continuous battery mass is electric power times duration divided by
150 Wh/kg, 0.8 usable fraction and 0.9 conversion efficiency. Passive monitoring
energy is treated separately. Getter capacity is dry sorbent mass per captured
gas mass; retained external gas still adds vehicle mass.

Numerical validation uses DOP853 integration, relative tolerance 1e-12,
absolute 1e-13 and maximum step 0.25 day, independently against the analytic
solution. A first RK45 dense-interpolation difference of 1.73e-7 Pa exceeded
the comparison target. The integration was tightened rather than loosening
the analytic check. This is numerical verification, not physical qualification.

Reproduce with `python3 calculate.py`, then `python3 render.py` from this folder.
The rendering script routes its plotting cache and temporary files to
unpublished-local-ref:1ffe4110219d37c0. NumPy/SciPy/Matplotlib versions are recorded in RUN.json.
"""
(B / "METHOD.md").write_text(method)
import scipy
(B / "RUN.json").write_text(json.dumps({
    "card_finished_at": now, "python": sys.version,
    "numpy": np.__version__, "scipy": scipy.__version__,
    "matplotlib": matplotlib.__version__,
    "times_are_measurements": True,
    "upstream_owner_code_executed": False,
    "own_calculator_executed": True,
}, indent=2) + "\n")
print(json.dumps({"card_bytes": (B / "CARD.md").stat().st_size,
                  "method_bytes": (B / "METHOD.md").stat().st_size,
                  "figure": str(B / "pressure-and-inventory.png"),
                  "finished_at": now}))
