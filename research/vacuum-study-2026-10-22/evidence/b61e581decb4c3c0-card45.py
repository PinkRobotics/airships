#!/usr/bin/env python3
"""MAINLINE-045: CARD.md, RESULTS.json, NFI.json and INPUTS.json from COMPUTE.json."""
import datetime
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
DETJ = json.load(open(os.path.join(HERE, "DET.json")))
JOB_STARTED = "2026-10-20T03:29:16-07:00"   # order read and acknowledged; a measurement, never a limit


def mm(x, n=1):
    return "n/a" if x is None else f"{x * 1e3:.{n}f}"


def main():
    T, P2, P3, L = C["threats"], C["p2"], C["p3"], C["leak"]
    D2, D3 = C["DET"]["p2"], C["DET"]["p3"]
    th = {r["threat"]: r for r in P2["threats"]}
    pick = lambda head: next(r for r in P2["threats"] if r["threat"].startswith(head))  # noqa: E731
    h25, h35, h45 = pick("hail 25.0"), pick("hail 35.0"), pick("hail 45.0")
    h50, h75 = pick("hail 50.8"), pick("hail 75.0")
    t5, t35, t136 = pick("Boeing small"), pick("Airbus typical"), pick("Boeing large")
    bm, bf = pick("bird 1.81 kg at 20.0"), pick("bird 1.81 kg at 38.0")
    m1 = pick("mooring contact at 0.914")
    pr2 = P2["pricing"]
    need = pr2["design_hail_needs"]["Shi-calibrated k rho v2"]
    needE = pr2["design_hail_needs"]["all energy to the panel"]
    patch = {(r["edge"], round(r["D_m"], 4)): r for r in pr2["patch"]}
    em = {r["kg"]: r for r in pr2["extra_mass"]}
    core = {r["k"]: r for r in pr2["denser_core"]}
    tube = {round(r["D_m"], 4): r for r in P3["tube_hail"]}
    tdes, t25, t75 = tube[0.0508], tube[0.025], tube[0.075]
    fr = P3["frame"]
    f4 = fr["f4"]["rigid_joint_cases"]
    f5 = fr["f5"]["rigid_joint_cases"]
    sig_ratio = [r["sigma_ratio"] for r in f4 + f5]
    ten = [r["tension_max_Pa"] for r in f4 + f5]
    nratio = [r["N_ratio_max_anywhere"] for r in f4 + f5]
    film = P3["film"]
    tear = film["tear"]
    a_all = [v for e in tear.values() for v in e.values()]
    stop = film["stop_25mm_slit"]
    p3pr = P3["pricing"]
    holes = {round(h["hole_m"], 4): h for h in L["holes"]}
    thr = L["touchdown_thresholds_hole_m"]
    big = {(b["case"], b["cd_drag"]): b for b in L["big"]}
    valve = {round(v["descent_m_s"], 3): v for v in L["landing_valve"]}
    det = {v["resolution_Pa_per_h"]: v for v in L["pressure_detection"]}
    regs = L["regs"]
    sf3 = D3["lam"]
    cl, ss = D2["patch"]["clamped"]["D_crit_m"], D2["patch"]["ss"]["D_crit_m"]
    und = {round(r["diameter_m"], 4): r for r in P2["undetected"]}
    g = lambda b_mm, key: next(r for r in P2["growth"] if abs(r["b_m"] * 1e3 - b_mm) < 1e-6)[key]  # noqa: E731

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    items = [
        ("NFI-045-DENT-GROWTH", "QUESTIONABLE",
         "The dent-growth criterion is this seat's derivation: the face's fixed membrane force pR/4 on a paraboloid "
         "dent's curvature, against the core's crush strength less its share of the pressure, with the patch's plate "
         "buckling force taken off. No opened page prints it. Castanie, the CAI literature on face wrinkling over "
         "crushed core, and McGowan and Ambur's preload threshold support the mechanism, not the numbers.",
         "Compression-after-impact tests on beryllium-faced CR-III coupons at 300 MPa, dented at 0.25-2 mm over 30-100 mm."),
        ("NFI-045-PATCH-EDGE", "QUESTIONABLE",
         f"The lost-core patch is read clamped ({cl * 1e3:.1f} mm) and simply supported ({ss * 1e3:.1f} mm); the real "
         "edge, a face continuous over intact core, lies between. The pressure that holds the face on the crushed core "
         "is a barrier this static reading ignores.",
         "A plate-on-crushable-foundation analysis of the dented patch, or the coupon test above."),
        ("NFI-045-DENT-MODEL", "QUESTIONABLE",
         "The dent model (face membrane plus core crush over a plastic spread) is this seat's. It reads Pach's test "
         "within its 1.1-1.2 mm and 30 mm, and Clarke's FE at about half the FE depth. Hail is read three ways "
         "(fluid, Shi-calibrated, all energy) that span ten times in depth.",
         "Ice-ball tests on a beryllium-faced CR-III panel at 25-75 mm and IEC velocities."),
        ("NFI-045-BE-IMPACT", "QUESTIONABLE",
         "No impact, puncture or through-thickness ductility data exist for thin SR-200 sheet. NASA 1971 calls "
         "beryllium's impact resistance extremely low. A cracked outer face vents its core cells; whether the CR-III "
         "core is perforated (034's evacuation of every cell) decides whether a crack vents the whole core.",
         "Drop and ice-ball tests on 0.8 mm SR-200 sheet over honeycomb, and the core venting design."),
        ("NFI-045-AS-BUILT", "QUESTIONABLE",
         "Each dent is scored alone against gamma 0.564; the as-built imperfection already spends that allowance, so "
         "a dent and the as-built shape compete for it.",
         "015's map with two interacting imperfections, or a measured shell."),
        ("NFI-045-HAIL-FLUX", "PROJECTION",
         "No hail flux (stones per square metre per storm, by size) was sourced, so the number of tube strikes in a "
         "storm is not given.",
         "A hail climatology for the site."),
        ("NFI-045-TUBE-IMPACT", "QUESTIONABLE",
         "The tube's hail stress uses a shallow-shell-on-foundation reading of a cylinder, a static contact pressure "
         "(fluid or Shi-calibrated), no dynamic amplification, and the 14 mm Hexoloy tube data without size scaling. "
         "Birds, timber debris and tool drops on the tubes are not scored. No SiC tube impact test was found.",
         "Ice-ball tests on a 275 mm, 1.14 mm-wall SiC tube."),
        ("NFI-045-FILM", "PROJECTION",
         "No Zylon/PBO film exists as a sourced product: no modulus, toughness, puncture or tear data. The tear lengths "
         "use other films' toughness and a projected modulus. The film is also unprotected from daylight (35 percent "
         "strength after six months).",
         "A built 0/90 PBO film with barrier, tested for puncture, slit tear under biaxial load and UV."),
        ("NFI-045-CASCADE", "QUESTIONABLE",
         "The lost-member screen is linear, rigid-jointed, on f4/f5 geodesics not at 022d's spacing, with lumped "
         "pressure loads; joint stiffness is unknown and no nonlinear collapse was run. 026b's discrete model is the "
         "place to repeat it.",
         "A nonlinear frame analysis with one member removed, on 026b's model with the real joint stiffness."),
        ("NFI-045-MERGED-BAY", "PROJECTION",
         "The film over the two bays a lost member leaves is scored at the same rise-to-span, a tension 1.5 times "
         "higher; the real film shape after loss is not modelled.",
         "A membrane analysis of the rhombic bay."),
        ("NFI-045-DESCENT", "QUESTIONABLE",
         "The descent model is a rigid sphere in ISA with an isothermal fill, a constant drag coefficient 0.2-0.47, "
         "added mass 0.5 rho V and no wind; the neutral-buoyancy pressure result assumes the inside air takes the "
         "outside temperature.",
         "A coupled thermal and trajectory model, and the site's atmosphere."),
        ("NFI-045-HOLE-EDGE", "QUESTIONABLE",
         "At a hole the face reads twice its membrane stress and yields out to 3.9 hole radii; whether the edge crumples "
         "and the hole grows while the slow leak keeps the load on is not modelled.",
         "A hole-edge analysis of the sandwich at 300 MPa, or a punctured coupon under biaxial compression."),
        ("NFI-045-MOORING", "PROJECTION",
         "No mast contact speed was sourced; TAR 473 and 14 CFR 25.473 stand in, and the 0.5 m contact patch is "
         "assumed.",
         "A mooring system design and its contact envelope."),
        ("NFI-045-REGULATION", "QUESTIONABLE",
         "14 CFR 101.13 limits moored balloons to 152.4 m above the surface, below the 500 m design point; 101.19 "
         "requires a rapid-deflation device, which for a vacuum hull is a rapid air valve that lands it heavy.",
         "A regulatory route for a 500 m moored or free vacuum hull."),
        ("NFI-045-DETECTION", "QUESTIONABLE",
         "No inspection limit was sourced for beryllium faces, SiC tubes or PBO film; the tap-test PoD is for 0.5 mm "
         "aluminium and falls with face thickness. Access to a 1257 m2 hull at 500 m is not addressed.",
         "PoD trials on beryllium-faced coupons and an inspection-robot concept."),
        ("NFI-045-SOFT-BODY", "QUESTIONABLE",
         "Bird and hail readings disagree by reading: a moored 4 lb bird is stable on the fluid pressure and grows on "
         "the all-energy reading.",
         "Soft-body impact analysis on the sandwich."),
    ]
    nfi = {"schema": 1, "card": "MAINLINE-045", "unit": "vacuum-mainline045-damage-tolerance-1020", "tag": "QUESTIONABLE",
           "status": "OPEN", "items": [{"id": i, "tag": t, "claim": c, "needed_to_ground": n} for i, t, c, n in items]}
    with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
        json.dump(nfi, fh, indent=1)
    os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))

    def pin(path, role):
        data = open(path, "rb").read()
        return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "role": role}
    pins = [dict(v, role="input read; " + k) for k, v in C["pins"].items()]
    for name in ("run45.py", "card45.py", "COMPUTE.json"):
        pins.append(pin(os.path.join(HERE, name), "this card's own code or intermediate"))
    inputs = {"schema": 1, "card": "MAINLINE-045", "unit": "vacuum-mainline045-damage-tolerance-1020", "pins": pins,
              "sources_used": C["sources_used"],
              "reports_used": ["rpt-ref-d907de1e97319ecc3f9a", "rpt-ref-6c81b0b188ad134a3ea2",
                               "rpt-ref-4b8e7b08241bb7a45536", "rpt-ref-06668dbf12580ed0ffc3",
                               "rpt-ref-74e882831c201b1a953c", "rpt-ref-8c5de04c9c33dbcf7447",
                               "rpt-ref-d7f99cd71e977826da48", "ref-0c9ab80606a173c6adb6",
                               "rpt-ref-244f32e2449e729d312f", "rpt-ref-9a0319231d2fe686eb92",
                               "rpt-ref-536c47263ffe5f46fd19", "rpt-ref-39745602983887568501"]}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(len(text), "bytes card;", len(items), "NFI;", len(pins), "pins")


if __name__ == "__main__":
    main()
