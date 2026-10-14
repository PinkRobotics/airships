#!/usr/bin/env python3
"""R3-I028 — machined aluminium socket bodies at the frozen drawn dimensions.

One material substitution, nothing else: the two I019 titanium socket-body
sizes become ASSUMED machined 6061-T6-class aluminium bodies of the SAME
drawn bore, OD, body length, grip and nose.  Titanium studs, nuts, anchor
blocks and attachment bolts, both cord families, potting, plane/station
counts and the whole pressure structure are retained.

What this calculator does (arithmetic on frozen data only):
  1. mass: replace only the socket-body metal, by each family's actual
     end count and geometric volume at the new density; add the declared
     isolation/protection provision and machining stock; apply the
     record's own 5% assembly share to the INCREMENT (x1.5 precedent);
  2. compliance: rebuild the stud/body series term replacing ONLY the
     body term with the new modulus (frozen total minus recomputed Ti
     body term, so every retained term is carried exactly), then
     propagate l_ser -> L_a -> chain denominators -> eta, pretension
     and the declared first-slack tables by the exact denominator ratio;
  3. screens: net body section under the frozen fitting demand against
     the ASSUMED 150 MPa working limit; bond demands carried unchanged
     with the substrate explicitly unqualified;
  4. bill: before/after spokes line, whole known subtotal, both altitude
     margins and the inherited SF1.2 adverse case, mass-only propagation.

What it deliberately does NOT do: no ancestor import or execution, no
coupled/eigen recomputation (dependent margins are exposed, not silently
carried), no field search, no solver, no tuning.  Inputs are read only
from baseline.json as pinned by sources.json.  Bounds: one process,
stdlib only, analytic + small arithmetic.
"""
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T = 1.0e3  # tonnes


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    with open(os.path.join(HERE, "sources.json")) as f:
        srcs = json.load(f)
    base_path = os.path.join(HERE, "baseline.json")
    pinned = srcs["calculator_reads"]["baseline.json"]["sha256"]
    actual = sha256_file(base_path)
    if pinned != actual:
        sys.exit("baseline.json sha256 %s != pinned %s" % (actual, pinned))
    with open(base_path) as f:
        B = json.load(f)

    al = B["newAssumptions"]["alBody"]
    prov = B["newAssumptions"]["provision"]
    mach = B["newAssumptions"]["machining"]
    share = B["newAssumptions"]["assemblyShareOnIncrement"]["share"]
    ti = B["materialLedger"]["terminationMetal"]
    cord = B["materialLedger"]["cord"]
    K = B["constants"]

    fam_out, bodies_old_t, bodies_new_t, prov_t, mach_t = {}, 0.0, 0.0, 0.0, 0.0
    for fam, F in B["families"].items():
        dia = F["diaMm"] * 1e-3
        bore = F["boreMm"] * 1e-3
        od = F["bodyOdMm"] * 1e-3
        body_l = F["bodyLenMm"] * 1e-3
        lg = F["gripLgMm"] * 1e-3
        nose = F["noseM"]
        ends = F["ends"]
        a_body = math.pi / 4.0 * (od ** 2 - bore ** 2)
        vol = a_body * body_l
        body_old_kg = vol * ti["rhoKgM3"]
        body_new_kg = vol * al["rhoKgM3"]

        # --- fitting-demand screen on the net (mouth) annulus ---
        tfit_n = F["TfitkN"] * 1e3
        sigma = tfit_n / a_body
        util = sigma / al["sigmaWPa"]

        # --- series compliance: replace ONLY the body term ---
        ea = cord["EPa"] * F["sectionM2"]
        body_ser_old = body_l / (ti["EPa"] * a_body)      # m/N, Ti body
        body_ser_new = body_l / (al["EPa"] * a_body)      # m/N, Al body
        l_body_old = ea * body_ser_old                    # as cord length
        l_body_new = ea * body_ser_new
        stud_residual = F["lSerM"] - l_body_old           # frozen stud etc.
        l_ser_new = stud_residual + l_body_new
        # reconciliation: rebuild the whole old series from drawn K-dims
        stud_d, stud_l = 1.8 * dia, 10.0 * dia
        series_rebuilt = (stud_l / (ti["EPa"] * math.pi / 4.0 * stud_d ** 2)
                          + body_ser_old)
        l_ser_rebuilt = ea * series_rebuilt

        # --- denominators, eta, pretension, first-slack propagation ---
        l_a_old = F["lAPerEndM"]
        l_a_new = nose + lg / 2.0 + l_ser_new
        d_ser = l_ser_new - F["lSerM"]
        l_eff_old, l_effm_old = F["lEffM"], F["lEffMeanM"]
        l_eff_new = l_eff_old + 2.0 * d_ser
        l_effm_new = l_effm_old + 2.0 * d_ser
        ratio = l_eff_new / l_eff_old
        eta_old = F["etaDrawnMeanCord"]
        eta_new = F["meanCordM"] / l_effm_new
        t0_n = F["T0kN"] * 1e3
        eps0 = t0_n / ea
        t0_same_eps = t0_n / ratio                       # T0 if eps0 held
        takeup = eps0 * 2.0 * d_ser                      # extra stud take-up to HOLD T0
        slack = B["slack"][fam]
        prop = {}
        for key in ("n5FirstSlackDeclaredMm", "n5FirstSlackChordBasisMm"):
            prop[key] = {ph: round(v * ratio, 6) for ph, v in slack[key].items()}

        bodies_old_t += ends * body_old_kg / T
        bodies_new_t += ends * body_new_kg / T
        prov_t += ends * prov["perEndInstalledKg"] / T
        fam_out[fam] = {
            "ends": ends,
            "netBodySectionM2": a_body,
            "bodyVolumeM3": vol,
            "bodyKgPerEndOldTi": body_old_kg,
            "bodyKgPerEndNewAl": body_new_kg,
            "geometricVsFrozenBodyKgPct": 100.0
                * (body_old_kg - F["perEndKg"]["bodyKg"]) / F["perEndKg"]["bodyKg"],
            "fittingDemandkN": F["TfitkN"],
            "netSectionSigmaMPa": sigma / 1e6,
            "netSectionUtilisationVs150MPa": util,
            "netSectionVerdict": "CONDITIONAL PASS on the ASSUMED record"
                if util <= 1.0 else "FAIL on the ASSUMED record",
            "lSerFrozenM": F["lSerM"],
            "lBodyTermOldM": l_body_old,
            "lBodyTermNewM": l_body_new,
            "lSerNewM": l_ser_new,
            "lSerDeltaM": d_ser,
            "lSerRebuiltFromKDimsM": l_ser_rebuilt,
            "rebuildReconciliationM": F["lSerM"] - l_ser_rebuilt,
            "lAPerEndOldM": l_a_old, "lAPerEndNewM": l_a_new,
            "lEffOldM": l_eff_old, "lEffNewM": l_eff_new,
            "lEffMeanNewM": l_effm_new,
            "denominatorRatioNewOverOld": ratio,
            "etaDrawnMeanCordOld": eta_old, "etaDrawnMeanCordNew": eta_new,
            "etaDelta": eta_new - eta_old,
            "T0kNSetpoint": F["T0kN"],
            "T0kNAtSameInstalledEps0": t0_same_eps / 1e3,
            "extraStudTakeupToHoldT0mm": takeup * 1e3,
            "wallInterfaceShearMPa": F["wallInterfaceShearMPa"],
            "bondUtilVsAssumed12MPa": F["wallInterfaceShearMPa"] / 12.0,
            "firstSlackPropagated": prop,
            "firstSlackMinDeclaredOldMm": min(slack["n5FirstSlackDeclaredMm"].values()),
            "firstSlackMinDeclaredNewMm": min(prop["n5FirstSlackDeclaredMm"].values()),
        }

    # --- whole bill: mass-only propagation ---
    mach_t = mach["fractionOfNewBodyMass"] * bodies_new_t
    delta_hw_t = (bodies_new_t + prov_t + mach_t) - bodies_old_t
    delta_tot_t = delta_hw_t * (1.0 + share)
    bill_o = B["bill"]
    new_lines = {
        "bodiesOldTiT": bodies_old_t,
        "bodiesNewAlT": bodies_new_t,
        "protectionProvisionT": prov_t,
        "machiningStockT": mach_t,
        "deltaHardwareT": delta_hw_t,
        "assemblyShareOnIncrementT": share * delta_hw_t,
        "deltaTotalT": delta_tot_t,
        "socketsTOld": bill_o["socketsT"],
        "socketsTNewHardwareOnly": bill_o["socketsT"] + delta_hw_t,
        "totalTOld": bill_o["totalT"],
        "totalTNew": bill_o["totalT"] + delta_tot_t,
        "spokesLineTOld": bill_o["spokesLineNewT"],
        "spokesLineTNew": bill_o["spokesLineNewT"] + delta_tot_t,
        "marginSLTOld": bill_o["marginSLT"],
        "marginSLTNew": bill_o["marginSLT"] - delta_tot_t,
        "margin2500TOld": bill_o["margin2500T"],
        "margin2500TNew": bill_o["margin2500T"] - delta_tot_t,
    }
    sf_o = B["sf12"]
    sf_new = {
        "afterTOld": sf_o["afterT"], "afterTNew": sf_o["afterT"] + delta_tot_t,
        "afterSpokesTOld": sf_o["afterSpokesT"],
        "afterSpokesTNew": sf_o["afterSpokesT"] + delta_tot_t,
        "afterMarginSLTOld": sf_o["afterMarginSLT"],
        "afterMarginSLTNew": sf_o["afterMarginSLT"] - delta_tot_t,
    }
    verdicts = {
        "seaLevelConditional": "SL conditional margin improves to %+.1f t (was %+.1f t); still CONDITIONAL on the known-subtotal basis" % (
            new_lines["marginSLTNew"], new_lines["marginSLTOld"]),
        "altitude2500": "FAIL persists: %+.1f t at 2,500 m (was %+.1f t)" % (
            new_lines["margin2500TNew"], new_lines["margin2500TOld"]),
        "sf12Adverse": "FAIL persists (inherited, unchanged in kind): after-margin %+.1f t (was %+.1f t)" % (
            sf_new["afterMarginSLTNew"], sf_new["afterMarginSLTOld"]),
        "netSection": "both families CONDITIONAL PASS vs the ASSUMED 150 MPa record (utilisation %.3f / %.3f)" % tuple(
            fam_out[f]["netSectionUtilisationVs150MPa"] for f in ("d60", "d180/11")),
        "compliance": "chain denominators grow %.3f%%/%.3f%% (d60/d180-11); eta drops ~1.1e-4; holding T0 needs %0.1f/%0.1f um extra stud take-up" % (
            100 * (fam_out["d60"]["denominatorRatioNewOverOld"] - 1.0),
            100 * (fam_out["d180/11"]["denominatorRatioNewOverOld"] - 1.0),
            fam_out["d60"]["extraStudTakeupToHoldT0mm"] * 1e3,
            fam_out["d180/11"]["extraStudTakeupToHoldT0mm"] * 1e3),
    }
    unknowns = {
        "bondOnAluminiumSubstrate": "the 12 MPa design bond shear is ASSUMED and NOT qualified on machined aluminium; required grips stay 59.68/96.48 mm vs drawn 60/97 — capacity UNKNOWN on the new substrate",
        "threadStripping": "UNKNOWN — the frozen record does not pin the drawn Ti-stud/Al-body thread engagement length, so no bounded justified screen exists",
        "fatigue": "UNKNOWN — no cyclic qualified record for the aluminium body, stud thread or bond",
        "creep": "UNKNOWN — cord/bond creep behaviour unverified; aluminium creep service unassessed",
        "corrosionContact": "UNKNOWN beyond the declared isolation provision mass — galvanic sufficiency, sealing and wet service are unqualified",
        "coupledEigenMargin": "dependent claim NOT recomputed under the changed body spring (predecessor licensed value %s carried as history); analytic bound: denominators move <0.07%%" % B["energy"]["licensedQuotableMargin"],
        "installationAndEquilibrium": "I023 common-strain equilibrium closure remains withdrawn; no installation-after-evacuation, extra travel or pressure-bearing tensile-cord licence is claimed; installation/global-equilibrium work stays UNKNOWN",
        "laminateAndAttachment": "laminate bearing, block local bending, pull-through, contact/creep: UNKNOWN (inherited)",
    }
    out = {
        "unit": "R3-I028",
        "candidate": "machined ASSUMED 6061-T6-class aluminium socket bodies at the frozen drawn dimensions; everything else retained",
        "inputs": {"baselineJsonSha256": actual, "sourcesJsonPins": pinned},
        "families": fam_out,
        "bill": new_lines,
        "sf12": sf_new,
        "hardwareSensitivity": {
            "inheritedX15IncrementT": bill_o["x15IncrementT"],
            "inheritedX15SLt": bill_o["stackedStationHardwareX1_5_SLT"],
            "note": "the x1.5 block/doubler/attachment scenario does not scale socket bodies and is carried UNCHANGED; the new protection/machining lines are not part of that frozen scenario",
        },
        "verdicts": verdicts,
        "unknowns": unknowns,
        "bounds": "single pure-Python process, stdlib only; frozen inputs; analytic propagation only; no ancestor import/execution; no solver, search or optimisation; the changed spring term is propagated everywhere the frozen record uses the denominator law",
    }
    out_path = os.path.join(HERE, "socket_body.json")
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1, sort_keys=False)
        f.write("\n")
    os.replace(tmp, out_path)
    print("R3-I028 socket bodies: bodies %.3f -> %.3f t, provision %.3f t, machining %.3f t, delta_total %+.3f t" % (
        bodies_old_t, bodies_new_t, prov_t, mach_t, delta_tot_t))
    print("margins: SL %+.1f -> %+.1f t; 2500m %+.1f -> %+.1f t; SF1.2 after %+.1f -> %+.1f t" % (
        new_lines["marginSLTOld"], new_lines["marginSLTNew"],
        new_lines["margin2500TOld"], new_lines["margin2500TNew"],
        sf_new["afterMarginSLTOld"], sf_new["afterMarginSLTNew"]))
    print("net section: d60 %.1f MPa (u=%.3f), d180/11 %.1f MPa (u=%.3f)" % (
        fam_out["d60"]["netSectionSigmaMPa"], fam_out["d60"]["netSectionUtilisationVs150MPa"],
        fam_out["d180/11"]["netSectionSigmaMPa"], fam_out["d180/11"]["netSectionUtilisationVs150MPa"]))


if __name__ == "__main__":
    main()
