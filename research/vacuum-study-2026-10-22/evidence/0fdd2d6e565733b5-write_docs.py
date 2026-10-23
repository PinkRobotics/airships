#!/usr/bin/env python3
"""Render the 030c morning card and complete additive evidence registers."""
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from intake import B, load
R = load(B / "RESULTS.json")
ALIASES = R["source_aliases"]
P = R["P2_selected_lead"]
A = R["P2_as_designed_250F"]
P35 = R["P3_selected_lead_041"]
P319 = R["P3_019_variant_041"]
N = load(B / "NFI.json")
reg = load(B / "REGISTER.json")
optimism = load(B / "OPTIMISM-LEDGER.json")
ledger = load(B / "LEDGER.json")
ground = load(B / "GROUND-FIRST.json")
intake = load(B / "INTAKE.json")
coverage = R["coverage"]


def text(name, value):
    (B / name).write_text(value.rstrip() + "\n")


def esc(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    lines += ["| " + " | ".join(esc(x) for x in row) + " |" for row in rows]
    return "\n".join(lines)


def src(alias, name="CARD.md"):
    return f" snapshots/{ALIASES[alias]}/{name}".strip()


def pretty(value):
    return json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)


snapshot = datetime.fromisoformat(R["snapshot_at"]).astimezone(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
fixed39 = next(x for x in R["stiffened_039_checked_constructive_points"] if x["mode"] == "float")
mass39 = next(x for x in R["stiffened_039_checked_constructive_points"] if x["mode"] == "mass")
pending = [x["item"] for x in R["pending"] if x["status"] == "PENDING"]
common = R["P2_common_account_040"]
q30 = next(x["point"] for x in common["necessary_points"] if x["id"] == "R30-ISA-actual-heavy70-vented")
q30w = next(x["point"] for x in common["necessary_points"] if x["id"] == "R30-optimistic-actual-heavy70-vented")
summary = f"""# MAINLINE-030c — morning design register

**QUESTIONABLE / PROJECTION throughout. Installed-hull SF is unknown. Snapshot {snapshot}.**

| Lead or retained comparison | Least modeled SF | Evidence state |
| --- | --- | --- |
| **P2 lead: 040 common account, R30 ISA / optimistic weather** | **1.000 / 1.000**, conditional | Least usage .601233 / .789568; both-weather has no float |
| P2 retained R10 construction: 028b + 037b 200 °F / 30.3414:1 | Structural module **{P['least_including_minimum_free_edge_SF']:.3f}** | Complete bill: **no float**, ISA endpoint −109.65 kg |
| P2 as designed, 250 °F / 30:1 | **{A['least_including_minimum_free_edge_SF']:.3f}** including minimum free-edge screen | γ {A['gamma']:.3f}, usage {A['usage']:.3f}, beyond named stretch |
| **P3: 041 direct f5, 5% / 019 reserve** | **{P35['least_screened_SF']:.6f} / {P319['least_screened_SF']:.6f}**; local sensitivity **{P35['least_including_local_max_compression_sensitivity']:.6f} / {P319['least_including_local_max_compression_sensitivity']:.6f}** | Best found model witnesses; physical allowables unresolved |
| 039 Be-frame alternative, CHECK-039 | **{fixed39['least_SF']:.6f}** at fixed lift | SF 1 needs +{mass39['mass_shift_kg']:.1f} kg; constructive point, not optimum proof |

**P2:** first ISA floats at R12–15; R30 needs least optimism. **Coating+primer (assumed .20 kg/m²) and retained water are the largest assumed debits.** R30 ISA O1 γ **×{q30['properties']['gamma']/.2:.4f}**, O2 Q **×{q30['properties']['Q']/.33:.4f}**; R10 module **×{P['gamma_factor']:.4f} / ×{P['Q_factor']:.4f}**. Gamma remains unvalidated/adverse in 029; Q lacks matched evidence. O3 strength and O4 panel **×1** do not qualify compression or supply. O5 bond mass **×2** at full endpoints, **×1** at R30 minimum. **O6**, formerly 039 “O5”, grants bay γ **×{fixed39['bay_factor_over_020']:.3f}** without clamping evidence.

**P3 assumptions:** membrane specific strength ×13.713 and crush/flexural proxy ×10.263 are comparisons, not qualified allowables; global k=.20 and tensile ceiling 15.586 MPa remain conditional. Local bending interaction, joint rigidity/mass, manufactured shape, weather, loads and sealed service have no supported single multiplier.

**First three tests:** finished-sheet compression/specification; weighed curved sealed scarf (042 F1 expands this to full-blank forming/seaming); same-batch wrinkle coupons. CHECK-038 preserves this order.

**Changed:** 040 removes the R10 common-bill float; 041 replaces the P3 transfer; 029 challenges the dimple map; CHECK-037's ten masses/84 missing fields and CHECK-037b/039 corrections carried; 042–044 add build, reliability and life gaps. **Failure probability and hull life remain unknown.** Pending: **{', '.join(pending)}**.
"""

p2table = table(
    ["P2 point", "γ / Q", "γ× / Q×", "Usage", "Face / core, mm", "Structural / with minimum edge SF"],
    [[p["id"], f"{p['gamma']:.9f} / {p['Q']:.9f}",
      f"{p['gamma_factor']:.6f} / {p['Q_factor']:.6f}",
      f"{p['usage']:.9f}", f"{p['tf_m']*1000:.6f} / {p['tc_m']*1000:.6f}",
      f"{p['least_structural_screen_SF']:.6f} / {p['least_including_minimum_free_edge_SF']:.6f}"]
     for p in [P, A]])
gammatable = table(
    ["029 geometry / meridian", "015 dimple, mm", "Endpoint, kPa", "Endpoint / p₀", "Endpoint γH / required γH"],
    [[x["case"] + " / " + x["direction"], x["dimple_mm"],
      f"{x['endpoint_MPa']*1000:.6f}", f"{x['endpoint_over_operating_pressure']:.6f}",
      f"{x['endpoint_gamma_handbook']:.6f} / {x['required_gamma_handbook']:.6f}"]
     for x in R["gamma_FE_029"]["lead_specified_defects"]])
masstable = table(
    ["CHECK-037 source path / case", "Filed tube kg", "Corrected SiC/arc kg", "Difference kg"],
    [[x["row"] + " / " + x["case"], f"{x['card_value']:.6f}",
      f"{x['check_value']:.6f}", f"{x['delta']:+.6f}"]
     for x in R["P3_tube_mass_corrections_CHECK037"]])
oldpoints = table(
    ["Preserved 030b variant", "γ / Q", "Least scored SF", "Basis"],
    [[p["id"], f"{p['gamma']:.6f} / {p['Q']:.6f}", f"{min(p['modes'].values()):.6f}", p["basis"]]
     for p in R["P2_leads"]])
payloads = R["P2_payload"]
p3newtable = table(
    ["041 resized f5", "5% reserve", "019 reserve"],
    [["Least declared screen", f"{P35['least_screened_SF']:.9f}", f"{P319['least_screened_SF']:.9f}"],
     ["Peak-compression local sensitivity", f"{P35['least_including_local_max_compression_sensitivity']:.9f}", f"{P319['least_including_local_max_compression_sensitivity']:.9f}"],
     ["OD / wall, mm", f"{2*P35['section']['r_o_m']*1000:.6f} / {P35['section']['wall_m']*1000:.6f}", f"{2*P319['section']['r_o_m']*1000:.6f} / {P319['section']['wall_m']*1000:.6f}"],
     ["Tube / film / joint, kg", " / ".join(f"{P35['mass_kg'][k]:.6f}" for k in ("tube","film","joint")), " / ".join(f"{P319['mass_kg'][k]:.6f}" for k in ("tube","film","joint"))],
     ["Reserve / sag debit, kg", f"{P35['mass_kg']['reserve']:.6f} / {P35['mass_kg']['sag_lift_loss']:.6f}", f"{P319['mass_kg']['reserve']:.6f} / {P319['mass_kg']['sag_lift_loss']:.6f}"],
     ["Closure sum, kg", f"{P35['mass_kg']['total_with_reserve_and_sag']:.6f}", f"{P319['mass_kg']['total_with_reserve_and_sag']:.6f}"],
     ["Required extreme compression, GPa", f"{P35['required_SiC_extreme_compression_at_screened_limit_Pa']/1e9:.6f}", f"{P319['required_SiC_extreme_compression_at_screened_limit_Pa']/1e9:.6f}"]])
commontable = table(
    ["R / weather", "Actual endpoint kg", "Floor endpoint kg", "Actual / floor least usage"],
    [[f"{rad} / {weather}",
      f"{next(x for x in common['primary_rows'] if x['R_m']==rad and x['weather']==weather and not x['floor'])['full_gamma_Q_endpoint_payload_kg']:.3f}",
      f"{next(x for x in common['primary_rows'] if x['R_m']==rad and x['weather']==weather and x['floor'])['full_gamma_Q_endpoint_payload_kg']:.3f}",
      " / ".join(f"{x['least_usage']:.6f}" if x["least_usage"] is not None else "none"
                 for floor in [False,True]
                 for x in common["primary_rows"]
                 if x["R_m"]==rad and x["weather"]==weather and x["floor"]==floor)]
     for rad in [10,12,15,20,30] for weather in ["ISA","optimistic","both"]])

body = f"""
The register preserves **{coverage['baseline_register_rows_preserved']} rows and {coverage['baseline_findings_preserved']} attributed findings** from 030b, including every original source pointer. It adds **{coverage['new_source_findings']} source records and {coverage['new_authored_findings']} synthesis findings** under {coverage['total_register_rows']} rows: **{coverage['total_attributed_findings']} total attributed findings**. Duplicates and resolved findings remain attributed history, not new open physical gaps. [Complete register](REGISTER.md), [optimism ledger](OPTIMISM-LEDGER.md), [corrections](LEDGER.md), [grounding](GROUND-FIRST.md), [all new reports](REPORTS.md).

## P2: 040 common-account lead and retained construction comparisons

**P2 is now stated on 040's whole bill: R10 does not float within the named ranges; first ISA floats occur at R12–15, and R30 needs least optimism.** Construction remains 028b with 037b's 200 °F / 30.3414:1 fix. With coating, retained water, the governing wind envelope, resized 70 kn pad, vented cells and nested daily service, the R10 full γ/Q endpoint deficits are **109.649 kg ISA, 257.973 kg optimistic weather and 596.529 kg both weather sets** under actual joining. [040]({src('040')})

{commontable}

The table's endpoint payloads use **.015 lb/ft² film and full γ/Q endpoints**, separate from minimum-usage points. Among the five tested radii, **R30 minimizes the count of improvements then maximum log usage**: ISA .601233 actual/.675318 floor; optimistic .789568/.883491. No both-weather float is found in the stated ranges. All 120 source cases—including light pads and unvented alternatives—remain pinned; a lighter mass balance is not an assembly pass.

At R30 actual joining, necessary coefficients after removing slack are **γ={q30['properties']['gamma']:.9f}, Q={q30['properties']['Q']:.9f}** under ISA and **γ={q30w['properties']['gamma']:.9f}, Q={q30w['properties']['Q']:.9f}** under optimistic weather. These minimum-usage points use **.030 film**, so O5 is ×1 there. The corresponding full-endpoint payloads use .015 and are **9,357.973 / 5,342.079 kg**, or **6,100.222 / 1,964.195 kg** with the retained floor. The common account retains max(actual joining, .05 structural), never both, and nests 30–50 kg service inside 100 kg systems; +30/+50 alternatives cover an otherwise committed systems line.

040 uses ν=.0768 and a wind/pressure envelope. **Coating+primer, assumed at .20 kg/m², and retained water are the largest assumed debits:** respectively **251.327 / 125.664 kg at R10**, **1,005.310 / 502.655 kg at R20**, and **2,261.947 / 1,130.973 kg at R30** in the ISA endpoint bill. These assumptions require measurement; removing a debit while retaining its benefit does not define a buildable hull. The pad load path, service scalability, cure state and omission of balanced residuals from global stability remain unqualified. Its corrected thermal quadrature is a new declared model, not recovery of 037's missing original inputs. The face-tuple axis couples E with Fcy; compression strength alone is nonbinding, and marginal tuple-dependent floats disappear if E is fixed. Its common static/service bill does **not** establish 044's fatigue life.

**The source construction module and as-designed comparison are retained separately:**

{p2table}

The retained R10 construction module is **028b with 037b's 200 °F panel cure and 30.341397:1 scarf**. At required γ and Q its structural screen is one, and its free-edge factors are 1.506325 typical / 1.075947 minimum-average. The latter is a conditional material screen, not a bond qualification. Source usage is 0.972190; usage measures consumption of the named optimism range and is **not SF**. The 0.120151 kg is the source's added joining allowance evaluated at its lead geometry. The selected hull account is 040's separately recomputed whole bill above. [037b]({src('037b')})

At the selected geometry, pressure plus residual face compression is {P['face_pressure_plus_residual_MPa']:.6f} MPa; the compression screen is {P['modes_at_required_values']['face_345']:.6f} using a 345 MPa tensile proxy. Q is now **0.439513**, not the old 0.434628. The as-designed 250 °F/30:1 point needs γ **0.618429** and Q **0.409438**, usage **1.052282**. Its structural screen at those required values is one, but the minimum-strength free edge is **0.833325**. At 037's different floated geometry the scarf screen becomes 0.992515. These are separate cases.

037b's argument transfers core in-plane force to cell-wall deformation and balanced face compression. Its free-edge model, foil properties, actual stress-free temperature and treatment of residual stress in global stability remain QUESTIONABLE. CHECK-037's missing thermal inputs remain missing in that source. “Bond survives its cure” is the source model's conditional conclusion; it does not establish the assembly's capability.

**CHECK-037b now reproduces the principal numbers**, including the low-cure fix. Its product correction adds HexBond 679's omitted 30 g/m² support at both interfaces: the rejected alternative rises from 444.255345 to **519.653569 kg**, +75.398224 kg; rejection stands. Sixteen L-direction precision path differences remain, while W governs. Family cure guidance and 2K metal tests do not qualify the light 2U Be/honeycomb process or its 50 psi tooling. Creep is not established as zero. [CHECK-037b]({src('CHECK037b')})

The original 030b variants remain intact:

{oldpoints}

The no-residual nominal is historical. 033's larger hulls use **1.01p₀, ν=.0768 and actual joining**, while 028b/037b uses **p₀, ν=.0752 and a retained joining floor**. No 037b cure or 042 build closure has been transferred automatically to the larger hulls. CHECK-033 retains the explicit/floor distinction: R30 full γ/Q payload is 18,139.202 kg for six modes or 7,754.736 kg with scarf; the retained-floor pair is 15,516.287 / 4,559.419 kg. Minimum-usage points and these full-endpoint payloads are distinct geometries. Active-constraint crossings are 10.350852134 m (actual bill + scarf) and 10.358193829 m (retained floor + scarf). Its Q+strength branch takes γ=1 on the crimp branch; the formal γ+strength root 103.892078332 m lies beyond stock gauge. All 241 exact path findings remain in the check packet. [CHECK-033]({src('CHECK033')}); [preserved 030b account](baseline030b/CARD.md).

## Gamma: 029 changes the evidence state

{gammatable}

These are **last-converged numerical endpoints, not established collapse pressures or hull SF**. The weak-meridian endpoints are below p₀=95.460837914 kPa at the two 015 amplitudes. They do not support the target at those sizes. Within this model a workable shape requirement would have to be tighter than the named 015 amplitudes; **no quantitative physical tolerance has been calibrated**. Strong-meridian cases omit weak circumferential/nonaxisymmetric modes and depend materially on Poisson ratio. 029 did not solve the current joined 028b/037b point. [029]({src('029')})

The benchmark itself is unresolved: the flat/dimple paper linear values are 30.21717/30.19659 MPa versus 27.53/27.56; imperfect elastic endpoints are 13.956916/13.843652 MPa versus 6.03/5.63 (about 2.31×/2.46×). Missing foam crush, face plasticity, contact-generated defect and finite-strain convention differences remain explicit. The independent linear mismatch remains about 10%; it is not explained away by nonlinear material differences. Outer-face Cauchy equivalent-stress diagnostics span 661–1,304 MPa. Face survival is unestablished.

Both lead points have Vc<2. The targets .595318/.468229 use handbook pressure Kc·pclassical; weak-meridian targets under p/pcrimp are .464110/.323009. No normalization may be swapped without Kc·Vc. 79 native runs are retained in 029; excluded multicore eigen spectra, reduced-integration spectra and initial overlarge reference-load spectra remain exclusions. This register performs no new solve.

## P3: 041 direct discrete point, with earlier results preserved

**041 has filed and replaces the transferred 1.067 shortcut for its directly modeled designs.** The unchanged selected 022d section on an integer f4 frame gives SF **1.133450616** under the inherited .2-times-linear convention, but its closure sum is **5063.886039 kg**, a **174.443889 kg deficit** at the 5% reserve. The tube mass alone rises by 178.318674 kg. Resizing selects f5 as best found in the tested uniform-section family:

{p3newtable}

Both witnesses have 252 nodes, 750 members and 500 cells. The axial local wall, film and sized end joints bind. The local peak-compression sensitivity is **not a calibrated interaction law**, but its **0.978132** at the 019 reserve means that witness cannot be described as robustly above unity. No film-stiffness credit enters these resized results. Source E=410 GPa is retained for the comparison; 041 flags the vendor edition at 430 GPa. Neither value resolves full-size ceramic reliability. [041]({src('041')})

The selected perfect f4 frame's new sampled nonlinear tangent loss is **5.430902212**, bracket [5.430880209, 5.430924214], with smallest-algebraic eigenvalue audits. It resolves family selection for that **new sampled path**, not the frozen 026b paths or every interval between samples. Applying .2 to it gives the separate 1.086180 sensitivity; the f5 resize still uses linear eigenvalues and an uncalibrated .2. No perfect-frame result establishes material/joint collapse. The bare pin frame has 480 roll mechanisms; the projected film tangent is separate and unqualified.

**Preserved continuum history:** the earlier checked 022d and ordered 026b-transfer rows below remain evidence, not the selected current discrete design.

CHECK-022d reproduces the screened equilateral lead **SF 1.258252476558** at s=3.170758569 m, true arc length 3.184193539 m, OD 275.082856 mm and wall 1.137365 mm. Both Zylon plies total 214.541558 kg; joints sized at the target weigh 44.191468 kg for 1.099425 MN. Vehicle 4545.249624 kg + reserve 244.472108 kg + sag debit 99.720419 kg closes to lift 4889.442150 kg. Full-size compression allowable and failure probability remain null. Fifty differences in square-membrane sensitivity fields come from coefficient precision; maximum SF effect is 3.98e-9 and the primary lead is unchanged. [CHECK-022d]({src('CHECK022d')})

The earlier ordered **.848 global-only sensitivity gives 1.066998100121**; exact f4 ratio .848428912828 gives 1.067537780749. Other modes and masses stayed fixed. CHECK-026b independently reproduces its linear/mass/baseline-force results, but its rise8 solve was refused before launch. The 538.899 kN rise8 force and 4.248 GPa bending remain owner-reported, unverified here. Its nonlinear first-loss values stay null; the top-level unverified disposition overrides raw “first loss” labels. 041 does not retroactively validate them. [CHECK-026b]({src('CHECK026b', 'CHECK.md')})

CHECK-037's ten corrections apply to its **older 022c** cases. All tubes are SiC at 3100 kg/m³; Ti/CFRP name the fittings. The two repeated projection rows have different film CTE assumptions.

{masstable}

Exact paths and evidence are in [P3-TUBE-MASS-CORRECTIONS.json](P3-TUBE-MASS-CORRECTIONS.json). CHECK-037 also leaves **84 thermal/projection fields unrecovered: 60 P3 temperatures, 10 P2 temperatures/swings and 14 coefficients**. Missing boundary conditions, optical data, stress-free temperatures and angular samples prevent treating those fields as checked temperatures. At held filed temperatures, its CTE/load corrections are sensitivities, not a repaired thermal solution. [CHECK-037]({src('CHECK037')})

The filed-polynomial maxima are 8.292853/14.851720 K, not the quoted 5.788444/17.145083 K. Adding steady flight pressure gives 479.847608 Pa and a conditional P2 screen 1.001324769. Pad proposals depend on support, boss size, preload and force direction. No pad mass or restoration factor becomes an installed design without reclosure.

## Stiffening: O6 and the filed independent check

**P2-O5 remains the 2× bond-film mass reduction. P2-O6 is 039's frame-bay cap transfer, called “O5” in that source.** The original source label is preserved only as an alias.

CHECK-039 reproduces the filed arithmetic but improves the attained Be-frame points: **SF {fixed39['least_SF']:.9f}** at the fixed 4889.442150 kg account, or **+{mass39['mass_shift_kg']:.6f} kg** for SF {mass39['least_SF']:.9f}. The latter total is 6016.513503 kg. These supersede claims that .689108 / +1329.819 kg were best achievable; the old values remain grid witnesses. The conditional plain sandwich remains the selected P2 route. [CHECK-039]({src('CHECK039')}); [039 source]({src('039')})

At the checked fixed-mass point O6 grants cap γ=.596482496, **×{fixed39['bay_factor_over_020']:.6f}** over .20. At the owner's older point the correct value is .601013192, not .603. A numeric gamma_s≥10 threshold and equal-area circular mapping do not demonstrate triangular-bay clamping. The handbook's .425 recommendation does not provide the owner's psi≥28 gate. Intermediate coupled modes, one-sided framing, local material and bond limits remain open.

The check also corrects the plain-Ti ratio to 317/917=.345692475 while retaining the source's printed 33% inconsistency; STA8.1's 759,000 and 754,000 lb predictions are successive model refinements. At the owner's mass-added point Q, scarf and tube-local screens already pass, so the fixed-mass failure list must not be copied onto that point. No tested floating stiffened hull is established.

## Reliability and life: 043 and 044 are filed, with qualified values null

043 finds **no matched compression Weibull modulus, characteristic strength and reference size for finished curved members**. Typical 3.9 GPa compression divided by stress cannot establish frame survival. Its conditional 433-member, m=10, complete-member-scale example needs **4.38651/8.75267 GPa** for frame Pf of 10⁻³/10⁻⁶, compared with an *assumed* 3.9 GPa scale. The multipliers 1.12475/2.24427 are hypothesis comparisons, not known material improvements. Source size and scatter can change the result drastically; qualified frame and lifetime Pf remain null. [043]({src('043')})

Those requirements use the old 022d 1.19810 GPa demand and 433-member bookkeeping, not 041's 750-member f5 frame or its different stresses. The joint-moment proxy raises old demand to 1.26913 GPa but is not a directly solved 041 load. The proposed proof example is 1.37428 MN and exceeds the source stability multiplier; it is not a ready proof protocol. Joint/contact, common-cause flaws, membrane and lifetime growth still consume an unallocated risk budget.

044 keeps **qualified hull life null**. Under its declared R10 annual spectrum, original six-pad underlying core static SF is **.7143**, so a plate-only Miner damage-one index of **949.846 days** is not a survival prediction or lower bound. Its 037b 200 °F fix thermal-only core index is about **18,816 days**, transferred from denser-core fatigue data with a mean-stress model; Be-sheet and scarf fatigue are unqualified. [044]({src('044')})

For its R10 fix geometry, conservative combined thermal/cure scarf screen is **.9950**, falling to **.9891** with added flight/weather loads. These extrema are not a time-correlated solution, but the small 037b scarf change cannot be said to close every load case. Its conditional six-pad/60:1 scarf candidate adds **36.661 kg**, reaching 4926.103 kg against 4889.442 kg lift, before further hardware. The 70 kn plate option alone is 109.849 kg. These six-pad assumptions differ from 040's resized single-pad model and cannot be applied to R30 as a validated retrofit.

044 also flags the **120 °C HexBond 312 scarf cure**: a later whole-panel cure could invalidate the assumed 200 °F face/core residual state. 042's room-temperature seam proposal is another process; neither sequence is qualified. Daily vacuum top-up is not full venting: the pressure/stress cycle differs by orders of magnitude. Inspection/replacement does not reset core/scarf/face damage, and no demonstrated defect-growth/detection law establishes ten years.

## Service, build route and first tests

CHECK-034 preserves the **30–50 kg daily ground-serviced sealed estimate** and the full 100 kg systems line. Ten kilograms of battery supports at most nine days of 5 W monitoring under the assumed pack factors. The **Edwards continuous 24-hour installation is 292.333 kg** and its assumed installed speed is 2.307% short for the stated Kapton envelope. KNF's separate 24-hour illustration is 56.833 kg; it is not interchangeable with the Edwards gas-load case. Gas-only projected lifetimes are not autonomous endurance. The +10% area sensitivity must also charge film/attachment mass and release inventory: the Zylon vacuum/barrier/bond subtotal becomes 96.878937–116.878937 kg plus additional structural fiber. None of these older inventories grants payload on 022d/037b. [CHECK-034]({src('CHECK034')})

042 has now filed, so it is **not pending**. It supplies a proposed manufacturing/inspection chain, not a qualified route. Its nominal 028b map permits 9.3–16.1 mm dimples and .075–.129 mm waviness, mapping γ=.69–.95, but these are conditional transfers; **029's adverse sandwich evidence prevents treating the map as validated tolerance**. S-II's roughly .21–.22 gamma is unmatched precedent, not a demonstrated Be-hull value. Smaller reflector measurements do not establish Be wrinkle-band finish. [042]({src('042')})

042 adopts 037b's 200 °F panel bond and proposes in-place room-temperature seams. Their materials, cure, mass and strength must be specified separately. Full-size thin-sheet supply, double curvature, residual stress, kilometre-scale scarfs and Be-specific seam/bond inspection remain unresolved. Its F1 full-blank forming-and-seam article follows T1, expands T2 and may supply T3 coupons; it does not replace T7's knockdown evidence.

CHECK-038 retains the first three: **T1 finished-sheet compression/specification; T2 weighed curved sealed scarf; T3 same-batch wrinkle coupons**. The nine families and original five ground-first routes remain in [GROUND-FIRST.md](GROUND-FIRST.md). Two historical end-mass differences are coefficient rounding; current targets are unchanged. The full-envelope .8 mm blank is not established by the maker catalog; the cited F1249-20 edition is superseded by -25. The 43–158k USD initial campaign estimate remains a source PROJECTION, not a quote or authorization to buy. [CHECK-038]({src('CHECK038')})

## Filing state

**PENDING for the next register:** {', '.join(pending)}. Status means no completed canonical report in the recorded scan; it is not an observation of a live seat. [PENDING.json](PENDING.json) includes filed dispositions. Later filings belong to 030d.

All {len(intake['reports'])} new canonical reports and their {coverage['new_report_artifact_pins']} direct artifact pins are indexed. [METHOD.md](METHOD.md) defines preservation, source selectors and arithmetic scope; [VALIDATION.json](VALIDATION.json) records integrity checks. Stop and file one report; the robotics seat sends the next job.
"""
text("CARD.md", summary + body)

# Every finding is rendered under its preserved or explicitly assigned register row.
byuid = {x["uid"]: x for x in N["rows"]}
parts = ["# MAINLINE-030c — complete issue register",
         "\nQUESTIONABLE / PROJECTION. Current 030c annotations govern; original source fields and dispositions remain verbatim history. Counts include attributed duplicates and resolved records.\n"]
for row in reg["rows"]:
    parts += [f"## {row['rid']} — {row.get('gap', row.get('topic_name'))}", ""]
    if row.get("current_030c"):
        parts += ["**Current 030c:** " + row["current_030c"]["text"], ""]
    if row.get("current_030b"):
        parts += ["**030b source history:** " + str(row["current_030b"]), ""]
    if row.get("unknown"):
        parts += ["**Original question:** " + row["unknown"], ""]
    ids = [s["uid"] for s in row.get("sources", [])]
    ids += [s["uid"] for s in row.get("updates_030b", [])]
    ids += [s["uid"] for s in row.get("updates_030c", [])]
    for uid in ids:
        n = byuid[uid]
        parts += [f"### {uid} — {n['row_id']}",
                  f"\nSource `{n['report']}`; original file `{n['file']}`; pointer `{n.get('source_json_pointer', 'retained original identity')}`.",
                  "\n```json\n" + pretty(n["fields"]) + "\n```\n"]
text("REGISTER.md", "\n".join(parts))

parts = ["# MAINLINE-030c — optimism ledger", "",
    "QUESTIONABLE / PROJECTION. Every 030b row is retained. The current P2 hull account is 040's whole bill: R10 does not float, R12–15 gives the first ISA floats, and R30 needs least optimism. It uses 028b+037b-200F-scarf-fix construction. Original 028b/037b module rows and old variants retain their separate bases.",
    "", "**Label map:** P2-O5 = .015/.030 lb/ft² bond-film mass reduction. P2-O6 = 039's former O5 frame-bay cap assumption. Multipliers with different denominators are not interchangeable.", ""]
for lead in dict.fromkeys(x["lead"] for x in optimism["rows"]):
    rows = [x for x in optimism["rows"] if x["lead"] == lead]
    parts += ["## " + lead, "", table(
        ["ID / assumption", "Multiplier or value", "Evidence / state", "Grounding"],
        [[x["id"] + " / " + x["name"], x.get("factor") if x.get("factor") is not None else "not established",
          x.get("current_evidence_030c", x.get("evidence_state", "")),
          x.get("grounding_route", "") + " / " + ", ".join(x.get("physical_tests_038", []))]
         for x in rows]), ""]
parts += ["The original conditional waviness and graph-reading comparisons remain in [the 030b ledger](baseline030b/OPTIMISM-LEDGER.md), attached to their original geometries. They are not recalibrated by 029."]
text("OPTIMISM-LEDGER.md", "\n".join(parts))

parts = ["# MAINLINE-030c — corrections ledger", "", "QUESTIONABLE / PROJECTION. All 118 original entries are retained; new source/check dispositions follow.", ""]
for i, x in enumerate(ledger["rows"], 1):
    parts += [f"## L{i:03d}", "\n```json\n" + pretty(x) + "\n```\n"]
text("LEDGER.md", "\n".join(parts))

parts = ["# MAINLINE-030c — ground-first list", "",
    "QUESTIONABLE / PROJECTION. First T1 compression/specification, T2 weighed curved sealed scarf, T3 same-batch wrinkle. CHECK-038 retains the order. 042 F1 follows T1 and expands T2 to a full-blank forming-and-seam article; it may supply T3 coupons.",
    "", table(["Route", "Status", "Next evidence"],
      [[x["id"] + " / " + x["route"], x["status"], x["target"]] for x in ground["routes"]]),
    "", "## Preserved 030b physical sequence and original five priorities",
    "", "Historical pending labels below are source history. Current route status is the table above.",
    "", (B / "baseline030b/GROUND-FIRST.md").read_text().replace("](snapshots/", "](baseline030b/snapshots/")]
text("GROUND-FIRST.md", "\n".join(parts))

parts = ["# MAINLINE-030c — filed additions", "", f"Snapshot {snapshot}; all report bodies below are source records, not new independent validation.", ""]
for r in intake["reports"]:
    parts += ["## " + r["id"], "", "Canonical ingestion: " + str(r.get("ingested")), "",
              r["body"], "", table(["Artifact", "SHA256", "Bytes"],
               [[f"[{Path(a['path']).name}]({Path(a['snapshot']).relative_to(B)})" if a.get("snapshot")
                 else str(a["path"]), a["sha256"], a["bytes"]] for a in r["artifacts"]]), ""]
text("REPORTS.md", "\n".join(parts))

text("METHOD.md", """# MAINLINE-030c — method and reproduction

This is an additive register update, extending 030b's intake, source identity, routing, selected-point and ledger workflow. Its code and all 431 manifest entries are retained in baseline030b, with hash/byte checks. No upstream numerical model is imported or executed. No new finite-element analysis, optimization, literature claim, supplier contact or physical test is made.

1. `intake.py` verifies the canonical 030b report and all baseline manifest files, copies them without modifying source bytes, then verifies/copies new canonical mainline/check reports absent from the predecessor index. Discovery uses aware ingestion timestamps after 02:47:05 PDT. Repeated scans retain immutable snapshots and reject changed report bytes.
2. `normalize.py` preserves every field in each new NFI collection, including resolved-source findings and document-level fields. Identity is report, original path and JSON pointer; UIDs remain stable. Repeated issues in separate reports remain attributed copies.
3. `ROUTING.json` explicitly assigns each new source finding to one primary issue row. Every old row and source reference is retained verbatim. `build_register.py` adds current annotations, eight synthesis findings, current selected points and correction/optimism/grounding entries. Old historical fields remain intact and do not override the current annotation.
4. Retained P2 construction points come from 037b RESULTS.compute.fixes[6] and [0]. Factor arithmetic is gamma/.20 and Q/.33. Conditional combined SF is the minimum of structural and minimum-average free-edge screens. Same-geometry handbook comparison uses min(.20/gamma_needed, .33/Q_needed, remaining modes, edge screen). Face demand is pR/(4tf)+residual stress. The current whole-hull lead uses 040's vented, heavy-pad common bill, with R30 ISA/optimistic necessary points copied from QUALIFICATION-AUDIT.json. Those coefficients have slack removed and differ from the common usage ceiling. The old joining delta remains a source allowance; 040 separately recomputes joining. Neither account establishes measured capacity.
5. CHECK-039's finite constructive points replace unsupported claims of best grid performance; O6 factors divide their cap gamma by .20. P3 mass corrections select all ten exact MISMATCH/tube_mass_kg audit rows from CHECK-037, retaining row indices and the two duplicate projection cases. P3 continuum and discrete sensitivities stay separate.
6. `write_docs.py` renders the morning card, every issue finding, all optimism/correction entries and the ground-first list. `validate_packet.py` checks source preservation, pins, routing, selected-point arithmetic, mass corrections, labels, source coverage and current links. These are synthesis checks; they do not rerun or certify any source calculation.

Reproduce in this directory with Python 3: `python3 normalize.py`, `python3 build_register.py`, `python3 write_docs.py`, `python3 validate_packet.py`. Refresh intake only when deliberately reviewing new filings; every new report/finding requires an explicit semantic disposition before final filing.

Nonstandard Infinity/NaN values in some infeasible 037b source alternatives remain in the verbatim source snapshot. Selected exported current values are finite strict JSON. All times are measurements only. Only the own seat workspace is written. Canonical queue reports are the evidence boundary; running seats are not inspected. Stop after one final report; no successor is named.
""")
print("RENDERED CARD WORDS", len((summary + body).split()), "SUMMARY WORDS", len(summary.split()))
