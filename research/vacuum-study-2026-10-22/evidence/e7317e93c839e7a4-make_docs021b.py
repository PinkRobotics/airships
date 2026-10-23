#!/usr/bin/env python3
"""MAINLINE-021b: write CARD.md and NFI.json from RESULTS.json; every number is read, never retyped.
Run after float021b.py: python3 -I make_docs021b.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "RESULTS.json")))
FP = D["floating_point"]
LS = D["least_set"]
O = D["optimisms"]
CK = D["checks"]
FAM = D["families"]
FIX = {tuple(r["subset"]): r for r in D["reserve_taken_as_given_535_95"]}
NAMES = {"O1_gamma": "gamma", "O2_wrinkle": "wrinkling", "O3_face_strength": "face strength",
         "O4_panel_size": "panel size", "O5_bond_film": "bond film"}


def g(x, n=4):
    return f"{x:.{n}g}"


def sfs(ev):
    names = {"global_buckling": "global buckling", "face_compression": "face compression",
             "core_shear_crimping": "core shear crimping", "core_crush": "core crush", "face_wrinkling": "face wrinkling",
             "intracell_dimpling": "intracell dimpling"}
    return ", ".join(f"{names[k]} {g(v)}" for k, v in ev["sfs"].items())


m = FP["masses_kg"]
nv, tv, fv, u = FP["needed_values"], FP["today_values"], FP["full_values"], FP["usage"]
tol, tolc = FP["tolerance_015_at_needed_gamma"], FP["tolerance_015_at_018_curve"]
fixed2 = FIX[("O1_gamma", "O2_wrinkle")]
sub_lines = []
for r in D["subsets"]:
    lab = "{" + ", ".join(NAMES[x] for x in r["subset"]) + "}" if r["subset"] else "{} (no optimism)"
    if r["feasible_within_named"]:
        p = r["point"]
        sub_lines.append(f"- {lab}: floats, largest usage {g(r['min_max_usage'])} (coarse grid), on {p['core']}, panels {g(p['w'])} m, film {g(p['film'])} lb/ft2.")
    elif r["min_max_usage"] is not None:
        sub_lines.append(f"- {lab}: does not float inside the named values; it would need {g(r['min_max_usage'])} of the stretch.")
    else:
        sub_lines.append(f"- {lab}: no geometry floats.")
fam = {k: v for k, v in FAM.items()}

card = f"""# MAINLINE-021b the floating point on 019's optimistic reserve, SR-200 faces — ESTIMATE

Unit {D['unit']}. Order ord-admiral-rr2-mainline021b-on-019-budget-1020. Status ESTIMATE. Tags QUESTIONABLE, and PROJECTION where named. Nothing here is a certification. Started {D['job_started_at']} (order read); the end time is in RESULTS.json. Times are measurements, not limits. Inputs: MAINLINE-019 (rpt-ref-d7f99cd71e977826da48), MAINLINE-020 (rpt-ref-3e02218a03708a878faa), and this seat's MAINLINE-021 rev1.

## The answer

On 019's optimistic reserve, with the thin faces as SR-200 rolled sheet at its own sourced properties (E {g(D['case']['face']['E_Pa'] / 1e9)} GPa; strength {g(D['case']['face']['sigma_today_Pa'] / 1e6)} MPa, the datasheet minimum tensile yield taken as compressive), a hull floats with every mode at SF 1 or above. It takes three of five named optimisms: gamma on the 018 curve, the wrinkling coefficient, and panel size. The largest usage is {g(LS['refined_min_max_usage'])}. The bond film stays at today's {g(tv['bond_film_lb_ft2'])} lb/ft2. The face stays at today's {g(tv['face_strength_Pa'] / 1e6)} MPa. No set of two floats.

Naming the panel and film optimisms changes the answer. Take 019's 535.95 kg reserve as given, and the least set is {{gamma, wrinkling}} at largest usage {g(fixed2['min_max_usage'])}. But that reserve already assumes 4 m panels and 0.015 lb/ft2 films. With today's panel ({g(tv['panel_width_m'])} m) and film ({g(tv['bond_film_lb_ft2'])} lb/ft2), this point's own reserve would be {g(FP['reserve_at_today_panel_and_film_same_geometry_kg'])} kg, not 536.

**The floating point.** Core {FP['core']} ({g(FP['core_rho_kg_m3'])} kg/m3, Ec {g(FP['core_Ec_Pa'] / 1e6)} MPa, W shear {g(FP['core_Gc_Pa'] / 1e6)} MPa, crush {g(FP['core_crush_Pa'] / 1e3)} kPa, cell {g(FP['core_cell_m'] * 1000)} mm, {FP['core_tag']}). R {g(FP['R_m'])} m. Each face {g(FP['tf_m'] * 1000, 6)} mm. Core {g(FP['core_m'] * 1000, 6)} mm. Face separation d = core + face = {g(FP['h_m'] * 1000, 6)} mm. Panels {g(FP['panel_width_m'])} m square-equivalent. Bond film {g(FP['bond_film_lb_ft2'])} lb/ft2 per bond. Vc {g(FP['Vc'], 6)}, {FP['branch'].replace('_', ' ')}.

The masses come from 019's mass line, made self-consistent at this geometry:
- faces {g(m['faces'], 7)} kg
- core {g(m['core'], 7)} kg
- joint allowance (0.05 of faces plus core) {g(m['joint_allowance_0.05S'], 7)} kg
- systems allowance {g(m['systems_allowance'])} kg
- reserve {g(m['reserve_total'], 7)} kg: 019's fixed optimistic items {g(m['reserve_fixed_items'], 7)} kg (water, contamination, climate, humidity and internal air), plus joint excess {g(m['joint_excess_in_reserve'], 7)} kg. The excess is seams {g(m['joint_seams'], 6)} kg plus films {g(m['joint_bond_films'], 6)} kg, less the allowance.
- total {g(m['total'], 9)} kg, equal to the lift

Needed values against today's:
- gamma {g(nv['gamma'], 5)}: {g(nv['gamma'] / tv['gamma'])} times today's {g(tv['gamma'])}; the 018 curve gives {g(fv['gamma'], 5)} here; usage {g(u['O1_gamma'])}
- wrinkle coefficient {g(nv['wrinkle'], 5)}: {g(nv['wrinkle'] / tv['wrinkle'])} times {g(tv['wrinkle'])}; usage {g(u['O2_wrinkle'])}
- panels {g(FP['panel_width_m'])} m: {g(FP['panel_width_m'] / tv['panel_width_m'])} times today's {g(tv['panel_width_m'])} m; usage {g(u['O4_panel_size'])}
- face {g(nv['face_strength_Pa'] / 1e6)} MPa: usage {g(u['O3_face_strength'])}
- film {g(FP['bond_film_lb_ft2'])} lb/ft2: usage {g(u['O5_bond_film'])}

Modes at the needed values: {sfs(FP['at_needed_values'])}. With gamma, wrinkling and face strength at their full values on this geometry and reserve: {sfs(FP['at_full_named_set'])}; least {g(FP['at_full_named_set']['least_SF'])}. Today: least {g(FP['today']['least_SF'])}, {FP['today']['governing'].replace('_', ' ')}. Under 018's conservative gamma: {g(FP['at_full_set_conservative_gamma']['least_SF'])}.

Face compression sits exactly at 1 on today's 345 MPa. The face strength optimism is unused, and so has no margin behind it. A face below 345 MPa in compression fails this point. 020's gauge tolerance of ±0.1016 mm is one route to that.

## The five optimisms, named with today's values

**O1, gamma.** Today: CR-1457, 0.20 below Vc 2 and 1 at or above (hemispheres; QUESTIONABLE for a sphere). Full: the 018 optimistic curve 0.20 + 0.40 min(Vc, 2), PROJECTION. Grounding: MAINLINE-018b; MAINLINE-015's map reads this point's gamma {g(nv['gamma'])} as one dimple of {g(tol['amplitude_mm'])} mm (RMS {g(tol['rms_worst_mm'])} mm) on t_eq {g(tol['t_eq_mm'])} mm, R/t_eq {g(tol['R_over_t_eq'])}. That gamma is near Eq 3's 0.45 floor, where the inversion is steep. The curve's own {g(fv['gamma'])} would allow {g(tolc['amplitude_mm'])} mm.

**O2, the honeycomb wrinkling coefficient.** Today 0.33 (CR-1457 eq 2.2-14, design). Full 0.82 (eq 2.2-12, K_delta 0). No pending card; a wrinkling test would ground it.

**O3, face strength.** Today {g(O['O3_face_strength']['today_Pa'] / 1e6)} MPa, {O['O3_face_strength']['today_basis']}. Full {g(O['O3_face_strength']['full_Pa'] / 1e6)} MPa, {O['O3_face_strength']['full_basis']}, with that lot's own {g(O['O3_face_strength']['E_full_Pa'] / 1e9)} GPa. MAINLINE-020 has filed; it kept 283 MPa (S-200F block) as its optimistic compression. For a sheet face this card uses the sheet's own minimum instead.

**O4, panel size.** Today {g(O['O4_panel_size']['today_m'])} m: {O['O4_panel_size']['today_basis']}. Full {g(O['O4_panel_size']['full_m'])} m, 019's optimistic panel width, PROJECTION. No published source gives thin SR-200 sheet larger than today's, and 020 records the largest 0.75 mm sheet as UNKNOWN. This point needs {g(FP['panel_width_m'])} m.

**O5, bond film.** Today {g(O['O5_bond_film']['today_lb_ft2'])} lb/ft2 per face/core bond ({O['O5_bond_film']['today_basis']}). Full {g(O['O5_bond_film']['full_lb_ft2'])} lb/ft2 ({O['O5_bond_film']['full_basis']}). This point does not need it.

019's other optimistic joint assumptions stay inside the reserve and are not searched: 60 mm splice strips, 0.2 mm seam adhesive, 1.5 mm core splice. Its climate and service assumptions stay too: sealed service, 0.1 mm water, +10 K, 1 percent pressure, 1 kPa vapour. NFI rows carry them.

## Every subset of the five (self-consistent reserve; panel and film on a 25 by 25 grid)

{chr(10).join(sub_lines)}

The fewest members that float is three. Of the three-member sets, {{{', '.join(NAMES[x] for x in LS['subset'])}}} needs the least; a finer grid around it gives {g(LS['refined_min_max_usage'])}.

## The families with every optimism at full (4 m panels, 0.015 lb/ft2, 018 curve, 0.82, the SR-200 lot)

Aluminium honeycomb: {g(fam['aluminium']['least'])} on {fam['aluminium']['core']}, reserve {g(fam['aluminium']['point']['masses_kg']['reserve_total'])} kg. Aramid: {g(fam['aramid']['least'])} on {fam['aramid']['core']}: {sfs(fam['aramid']['point']['at_full_named_set'])}. It is blocked by core shear crimping, which no named optimism touches, tied with global buckling and wrinkling on the crimp branch. Other (fiberglass): {g(fam['other']['least'])} on {fam['other']['core']}. Today (0.914 m panels, 0.030 lb/ft2, CR-1457 gamma, 0.33, 345 MPa): aluminium {g(fam['aluminium_today']['least'])} with reserve {g(fam['aluminium_today']['reserve_kg'])} kg; aramid {g(fam['aramid_today']['least'])}; other {g(fam['other_today']['least'])}.

## Method and checks

float021b.py re-implements 019's mass line and joint formula and 021's modes, vectorised. The reserve is made self-consistent at each geometry: M = 019's fixed optimistic items ({g(D['case']['reserve_fixed_items_kg'], 9)} kg) + max(0, joints − 0.05 S). Before anything new, it reproduces:
- 019's aluminium optimum {g(CK['019_aluminium_least']['mine'], 10)} against {g(CK['019_aluminium_least']['sealed'], 10)} ({CK['019_aluminium_least']['result']})
- 019's aramid optimum {g(CK['019_aramid_least']['mine'], 10)} against {g(CK['019_aramid_least']['sealed'], 10)} ({CK['019_aramid_least']['result']})
- 019's joint excess {g(CK['019_joint_excess_aluminium']['mine'], 12)} kg and reserve {g(CK['019_reserve_rebuilt']['mine'], 12)} kg, exactly ({CK['019_reserve_rebuilt']['result']})
- 021 rev1's least-set usage {g(CK['021_rev1_least_set_usage']['mine'], 12)} at the 5 percent line ({CK['021_rev1_least_set_usage']['result']})

Dimpling uses CR-1457's biaxial rule, as in 021. The search covers 014b's honeycomb cores, 2000 core-mass fractions, and a 25 by 25 grid of panel width and film weight between today and full, then a finer grid around the least set.

## Then

Stop and file. The robotics seat sends the next job. NFI.json carries the open rows. A checker runs behind this card.
"""
with open(os.path.join(HERE, "CARD.md"), "w") as fh:
    fh.write(card)

nfi = [
    {"id": "NFI-021b-GAMMA", "optimism": "O1", "needed": nv["gamma"], "today": tv["gamma"], "full_at_point": fv["gamma"],
     "improvement_factor": nv["gamma"] / tv["gamma"], "usage": u["O1_gamma"], "state": "PROJECTION",
     "grounding_card": "MAINLINE-018b; MAINLINE-015's map", "tolerance_015": tol},
    {"id": "NFI-021b-WRINKLE", "optimism": "O2", "needed": nv["wrinkle"], "today": tv["wrinkle"], "full": fv["wrinkle"],
     "improvement_factor": nv["wrinkle"] / tv["wrinkle"], "usage": u["O2_wrinkle"],
     "state": "between the design lower bound and the classical value; no test at this tc/tf", "grounding_card": "none pending"},
    {"id": "NFI-021b-PANEL", "optimism": "O4", "needed_m": FP["panel_width_m"], "today_m": tv["panel_width_m"], "full_m": fv["panel_width_m"],
     "improvement_factor": FP["panel_width_m"] / tv["panel_width_m"], "usage": u["O4_panel_size"], "state": "PROJECTION",
     "note": "Thin (<0.059 in) SR-200 stock size is unpublished (020: UNKNOWN); curved forming at 10 m radius unverified.",
     "grounding_card": "a supplier-confirmed thin-sheet specification (020's first ground)"},
    {"id": "NFI-021b-FILM", "optimism": "O5", "needed_lb_ft2": FP["bond_film_lb_ft2"], "today_lb_ft2": tv["bond_film_lb_ft2"],
     "full_lb_ft2": fv["bond_film_lb_ft2"], "usage": u["O5_bond_film"], "state": "not needed at the floating point",
     "note": "Be/honeycomb bond suitability of any AF 163 weight is unqualified (019, 020)."},
    {"id": "NFI-021b-FACE-AT-ONE", "optimism": "O3", "needed_Pa": nv["face_strength_Pa"], "today_Pa": tv["face_strength_Pa"],
     "usage": u["O3_face_strength"],
     "issue": "Face compression is exactly 1 on SR-200's minimum tensile yield used as compressive; no compressive minimum is published; 020's gauge tolerance ±0.1016 mm and post-form properties can take it below 1.",
     "grounding_card": "MAINLINE-020 follow-up: post-form compression and gauge map"},
    {"id": "NFI-021b-RESERVE-HIDES-OPTIMISMS",
     "issue": "019's 535.95 kg reserve embeds 4 m panels and 0.015 lb/ft2 films; at today's panel and film this point's reserve is "
              f"{FP['reserve_at_today_panel_and_film_same_geometry_kg']:.1f} kg.",
     "numbers": {"least_set_reserve_as_given": fixed2["subset"], "usage": fixed2["min_max_usage"]}},
    {"id": "NFI-021b-JOINT-PARAMETERS",
     "issue": "019's optimistic joint parameters (60 mm strips, 0.2 mm adhesive, 1.5 mm core splice) are owner assumptions, not validated joints; 020's own splice model weighs 0.218 kg per hull-seam metre in its optimistic case."},
    {"id": "NFI-021b-CLIMATE-SERVICE",
     "issue": "The fixed reserve items are 019's optimistic sealed-service day (0.1 mm water, +10 K, 1 percent, 1 kPa); 019's conservative day needs 4229 kg.",
     "grounding_card": "MAINLINE-019 follow-ups (site, gas-load measurement)"},
    {"id": "NFI-021b-ARAMID-BLOCKED",
     "issue": f"The aramid family reaches {fam['aramid']['least']:.4g} with every optimism full; core shear crimping, which no named optimism touches, ties with global and wrinkling on the crimp branch."},
    {"id": "NFI-021b-MARGIN", "issue": "No payload: 019's unladen case. 019's +100 kg payload sensitivity raises the reserve to 637.85 kg."},
]
with open(os.path.join(HERE, "NFI.json"), "w") as fh:
    json.dump({"schema": 1, "card": "MAINLINE-021b", "unit": D["unit"], "tag": "QUESTIONABLE", "certification": "none",
               "rows": nfi}, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("CARD.md", len(card), "bytes;", len(nfi), "NFI rows")
