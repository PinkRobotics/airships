# MAINLINE-019 — float-margin budget

The declared optimistic case needs **535.9 kg (10.96% of reference lift)**. The declared conservative case needs **4229.1 kg (86.49%)**. The old 5% reserve is 244.5 kg, short by 291.5 kg even in the optimistic case. These are conditional planning budgets, not measured site requirements or probability bounds. All inputs and estimates are QUESTIONABLE; unestablished panel/fabrication routes are PROJECTION. No certification.

Both requested points are retained: Be / Hexcel HRH-10-4.8-32 aramid, and Be / Hexcel CR-III 5056 1/4-1.6 aluminium honeycomb. The pinned face properties and branch rule are unchanged. Payload is zero for this unladen demonstrator. The old margin is not also counted as payload.

## Budget and accounting

The optimistic package is ground-serviced and sealed for 24 h, with a projected 4 m panel width, 0.1 mm equivalent retained water, +10 K, ±1% pressure, and 1 kPa vapour partial pressure. The conservative package has 24 h onboard electric pumping, an assumed 0.6 m panel width, 1 mm retained water, +25.1 K, ±2% pressure, and 6 kPa vapour pressure. The panel sizes, weather and endurance are explicit design choices; no actual site or procurement establishes them.

For each reserve M, S=(L−100−M)/1.05 is faces plus core. Each family independently maximises its least factor on that mass line. Then seam mass and the shrinking 0.05S joint allowance are recalculated. M is increased until BOTH families cover their item sums. The aluminium family sets the common budget below. Only expenditure above the existing 100 kg systems and 5% joint allowances is charged; unused allowance stays reserved.

| Charge beyond the base hull (kg) | Optimistic | Conservative | Basis |
|---|---:|---:|---|
| Systems excess | 0.00 | 1366.33 | Hardware + power + controls, less 100 kg |
| Joints and bond-film excess | 124.65 | 939.69 | Two face splices, core splice, both full-area bonds; less 0.05S |
| Retained water | 125.66 | 1256.64 | 1000 A δ |
| Contamination | 5.00 | 25.00 | Owner allowance |
| Temperature and pressure lift loss | 213.04 | 485.76 | Exact ideal-gas p/T ratio, low-pressure/hot corner |
| Additional humidity loss | 18.70 | 106.76 | Ideal-mixture correction, assumed vapour pressure |
| Internal air | 48.89 | 48.89 | 1% of reference lift; finite vacuum tolerance |
| Payload | 0.00 | 0.00 | Unladen case; see sensitivity |
| **Total** | **535.95** | **4229.07** | Common sufficient reserve |

The aramid totals are 529.92 and 4205.89 kg on the same two mass lines; the common reserves leave 6.03 and 23.19 kg above those sums. This reserve is spent on the stated condition, not left over afterward.

Systems total 30 kg optimistic (15 kg vacuum hardware, 10 kg power package, 5 kg controls; owner estimates). The active total is 1466.33 kg: 223 kg pump, 1223.33 kg battery package and 20 kg controls/plumbing. Battery mass is 5505 W × 24 h / (150 Wh/kg × 0.8 usable × 0.9 conversion); those battery factors are assumptions. The pump reference is [Leybold SV300B, 50 Hz](https://www.leybold.com/content/dam/brands/leybold/downloads/brochures/product-brochures-fore-vacuum/oil-rotary-vane-pumps-single-stage/3611041002_SOGEVAC_Overview_EN_web.pdf), not the predecessor's ideal-work power estimate.

Seams use 2A/w unique boundaries, with a strip and adhesive on EACH face plus one through-core splice. Strip widths 60/120 mm, local adhesive 0.2/0.3 mm, and core splice width 1.5/3 mm are inherited owner assumptions, not validated joints. Both full-area face/core bonds add 184.06/368.13 kg at the published .015/.030 lb/ft² [3M film weights](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=AF163-2.pdf). Their Be-bond suitability remains unqualified. The pinned bare face/core masses contain no such adhesive.

Climate uses Lday/L0=[1−Δp−0.378 e/p0] T0/(T0+ΔT), the [ideal-mixture limit](https://www.nist.gov/system/files/documents/calibrations/CIPM-2007.pdf); the full CIPM metrology correlation is not extrapolated to 310 K. High-pressure structural loading is checked separately. A +25.1 K change alone loses 395.89 kg, not the first-order 430.77 kg; the old 5% hull still ends 151.41 kg heavy.

## Both families on each margin line

| Reserve | Core | Face tf (mm, each) | Core (mm) | Vc | gamma | Least SF |
|---|---|---:|---:|---:|---:|---:|
| 0% | aramid | 0.792903 | 21.75269 | 3.50794 | 1.00 | 0.685398477 |
| 0% | aluminium | 0.693182 | 41.55572 | 0.60459 | 0.20 | 0.668710748 |
| 5% | aramid | 0.752430 | 20.64235 | 3.32888 | 1.00 | 0.650413022 |
| 5% | aluminium | 0.650968 | 40.42067 | 0.56810 | 0.20 | 0.617050785 |
| 10.96% | aramid | 0.704176 | 19.31853 | 3.11540 | 1.00 | 0.608701338 |
| 10.96% | aluminium | 0.600798 | 39.04435 | 0.52468 | 0.20 | 0.556669198 |
| 86.49% | aramid | 0.055891 | 6.80916 | 0.25420 | 0.20 | 0.009665364 |
| 86.49% | aluminium | 0.057424 | 8.28042 | 0.05057 | 0.20 | 0.012716418 |

Direct evaluation reproduces filed 009c-5 at 0.650411843681 and the original 014b grid at 0.668649769509. The table uses continuous refinement, which accounts for the small increases at the reference rows. At the optimistic line, aramid balances crimp/global and wrinkling; aluminium balances global buckling and wrinkling. At the conservative line both are on the stiff branch, governed by global buckling. Every factor remains below 1.

The maximum-pressure corner gives optimistic least factors 0.602675/0.551158 and conservative 0.009476/0.012467 (aramid/aluminium). On a fixed geometry, only stiff-branch global buckling scales with kd; crimp-branch global/crimp uses gamma=1. Re-optimising at another kd may change the governing mode, so the whole least factor is not uniformly scaled.

The 0→5% loss per 100 kg is 0.014311 for aramid and 0.021131 for aluminium, versus MAINLINE-006's different P2 systems at 0.008646/0.009517. This is a scale check, not a transferable slope. Aramid's 0→30% slope is constant under this model, but it cannot be extended through the branch change at large reserve.

## Vacuum route

The lightest examined candidate is ground evacuation followed by sealed service: estimated 30–50 kg onboard, 0 W pumping and 5 W monitoring. It is conditional, not a demonstrated vacuum-holding system. For 24 h, a 10 Pa start referenced to 284.9 K, a 954.61 Pa ceiling, and internal gas no hotter than 320 K, the total gas load normalised to 284.9 K must be at most 40.7195 Pa m³/s. The budget retains 48.89 kg for internal air. Exact p_inside=0 cannot be maintained by a finite real system; the scored pressure load still uses an empty hull, conservatively.

At the inherited 1%-per-day air ingress, required effective speed is 174.53 m³/h at reference temperature and 196.04 m³/h at 320 K and the fixed ceiling. The selected catalog reference has 240 m³/h nominal pumping performance and 5.5 kW maximum motor rating; inlet conductance, installed power and thermal duty still need measurement. Ground equipment is excluded from flying mass, not from project cost.

[SAES offers nitrogen sorption at room temperature](https://www.saesgetters.com/industrial-getters-dispensers/solution/non-evaporable-getters-neg/); the partial script's blanket rejection is incorrect. [Hybrid NEG/ion systems](https://www.saesgetters.com/highvacuum/portable-ultra-high-vacuum-systems/) address additional species, but no capacity/rate data here size a full-air getter system. No getter mass credit is awarded. Correct throughput is 46.2807 Pa m³/s, not 86,400 times that; the unfinished getter result also missed grams-to-kilograms conversion. The reversible variable-pressure ground pump-down minimum to 1% pressure is 104.85 kWh; actual plant energy is unmeasured.

## Panel size and present availability

At the shared 5% line, the joint allowance is 216.43 kg. Seams ALONE fit it at optimistic square-equivalent widths 2.684 m (aramid) and 2.801 m (aluminium), or conservative widths 5.716/5.950 m. With the optimistic full-area bond films included, the same algebra requires 17.946/18.731 m; those dimensions are outside the useful local-panel approximation and do not establish a buildable spherical layout. With the conservative films, adhesive alone exceeds the allowance: no panel width closes that 5% total-joint budget.

[Materion lists S200F as consolidated rod/bar/block](https://hkvxni.files.cmp.optimizely.com/download/assets/Beryllium%2BUses%2Band%2BDescriptions.pdf/c3141b9ea04211ee9a7b2a5d2cb825d4), not an established rolled-sheet panel. No examined primary source establishes the required multi-metre, sub-millimetre, curved S200F face panels today. Even the 0.6 m case is a procurement assumption, not a verified stock limit. The complete panel route stays PROJECTION. The same current sheet lists S200F at 290 GPa; keeping all else pinned but using 290 GPa gives optimistic factors 0.601843/0.539000. Resolve that grade mismatch separately rather than silently altering the ordered lead points.

## Sensitivities, evidence and handoff

| Variant | Reserve kg | Reserve % | Aramid least SF | Aluminium least SF |
|---|---:|---:|---:|---:|
| Conservative weather/panels, sealed service | 3215.08 | 65.76 | 0.066727 | 0.098064 |
| Conservative weather/panels, 8 h active power | 3623.80 | 74.11 | 0.038827 | 0.054265 |
| Optimistic plus 100 kg payload | 637.85 | 13.05 | 0.594118 | 0.535895 |

Removing the onboard pump does not rescue small-panel, wet, hot-day operation. These sums also leave coating, hardpoint, handling and any propulsion allocations unresolved; NFI.json records those gaps and the exact operational assumptions.

Started from the predecessor's unfiled script and pinned 009c-5/014b/016/006 records. The delivered script independently reproduces the original points, refines both geometries and closes both scenario budgets. Validation includes 100,001-point search comparisons and independent 40-digit scalar pressure/mass calculations; 34 file pins were rechecked. This is arithmetic verification, not structural qualification. RESULTS.json contains all six scored modes, geometry, line items, formulas, sensitivities and measured run times. INPUTS.json contains source pins and every scenario choice; NFI.json contains 14 open issues.

The next evidence with the most value is a qualified seam/panel takeoff and measured whole-assembly gas load, paired with a specified site and payload. The brief names no executable successor: stop and file; the robotics seat supplies the next job.

Margin and budget comparison [source link unavailable in this public projection]

Reproduce locally: `python3 prepare_inputs.py`, `python3 compute.py`, `TMPDIR=unpublished-local-ref:1ffe4110219d37c0 MPLCONFIGDIR=unpublished-local-ref:d7084a936ed02180 python3 check_and_plot.py`, `python3 build_card.py`. No other seat's files are written.
