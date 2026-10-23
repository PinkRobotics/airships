#!/usr/bin/env python3
"""CHECK-047: CHECK.md, RESULTS.json, NFI.json, INPUTS.json and FE-RUNS.json from A-ARITH.json, B-FE.json,
B-ACOUSTIC.json and the fe/*/result.json records."""
import datetime
import glob
import hashlib
import json
import os

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def brow(prefix):
    return next(r for r in B["rows"] if r["check"].startswith(prefix))


def arow(prefix):
    return next(r for r in A["rows"] if r["check"].startswith(prefix))


def res(name):
    return json.load(open(os.path.join(HERE, "fe", name, "result.json")))


def main():
    runs = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(HERE, "fe", "*", "result.json"))
                  if not os.path.basename(os.path.dirname(p)).startswith(("dbg", "t-allbe", "unit")))
    fe_runs = {n: res(n) for n in runs}
    g = B["governing"]
    s1p, s1f = g["SF1.0"]["passing"], g["SF1.0"]["failing"]
    s5p, s5f = g["SF1.05"]["passing"], g["SF1.05"]["failing"]
    nA = len(A["rows"])
    nA_ok = sum(1 for r in A["rows"] if r["agrees"])
    cmp_ = [r for r in B["rows"] if r["agrees"] is not None]
    nB, nB_ok = len(cmp_), sum(1 for r in cmp_ if r["agrees"])
    mesh = fe_runs["g-W332-a1.208988-hi"]["meta"]["mesh"]
    shear = A["simple_shear_ellipticity_MPa"]
    inh = min(v for v in shear["inherited"].values() if isinstance(v, float))
    reg = min(v for v in shear["regularized"].values() if isinstance(v, float))
    pf = {y: brow(f"perfect sphere {y} MPa first yield") for y in (255, 300, 345)}
    pe = {y: brow(f"perfect sphere {y} MPa numerical endpoint") for y in (345, 300, 255)}
    e_pass, e_fail = brow("1.10 division passing amplitude"), brow("1.10 division failing amplitude")
    big = brow("11.8 mm / 332.2 W: first face yield")
    big_c = brow("11.8 mm / 332.2 W: first minimum-average core shear")
    big_e = brow("11.8 mm / 332.2 W: 345 MPa numerical endpoint")
    reg_inh = brow("core in-plane law inherited")["mine"]
    reg_10 = brow("core in-plane law stiffer")["mine"]
    m1 = brow("mesh control at 1.208988: refined minus base max face stress")["mine"]
    eE1 = brow("face E 298.7 GPa minus 290 GPa: max face stress at 1.208988")["mine"]
    eEst = B["governing"]["E298.7_SF1_estimate_mm"]
    L332, W402 = brow("(332.216, 'L') SF 1 tolerance estimate"), brow("(401.856, 'W') SF 1 tolerance estimate")
    cd1, cd5 = brow("cure debit SF 1.0 estimate"), brow("cure debit SF 1.05 estimate")
    sig = arow("perfect sphere face stress at service")["mine"]
    p_isa = arow("service pressure = ISA 500 m")

    L = []
    a = L.append
    a("# CHECK-047: MAINLINE-047, the P2 dimple tolerance with face yield and core shear, checked behind its owner. ESTIMATE")
    a("")
    a(f"Unit vacuum-mainline047-check-1020. Order {ORDER}. Checked report {CHECKED}: owner ref-4bc9297546b34b47e7f1, "
      "CARD.md sha256 ad003407. Brief CHECK.md (03b357cb) with COMMON.md (6a6a596f). The owner's code was neither read nor run; its "
      "filed data files were read as data. Values are QUESTIONABLE, and PROJECTION where named. Started 07:31:39 PDT when the order was "
      "read; the end time is in RESULTS.json. Times are measurements, not limits.")
    a("")
    a("## Verdict")
    a("")
    a(f"Every number the order names re-derives. {nA_ok} of {nA} arithmetic rows agree. The check's own CalculiX model agrees on "
      f"{nB_ok} of {nB} compared FE rows. The one FE mismatch is a diagnostic in the larger-dimple table and is explained by mesh. "
      "Two objections become NFI rows: an unsourced face modulus and an unstated sweep mesh. Neither changes the card's conclusions; "
      "the modulus would move the SF 1 tolerance by about one bracket width.")
    a("")
    a("**Scope of the check's own FE:**")
    a("- the perfect sphere: three first yields and three endpoints;")
    a("- the governing W 332 brackets at both SF, on the pre-yield branch and at a real 345 MPa;")
    a("- the L 332 and W 401.9 SF 1 brackets, and both cure-debit brackets;")
    a("- the 1.10-division pair and one larger dimple (332.2 mm W, 11.8 mm);")
    a("- three sensitivities: mesh, core regularization and face modulus.")
    a("")
    a("The other footprints at SF 1.05, the 347.2 and 2181.4 mm widths and the other larger dimples are re-derived from the owner's "
      "filed data only.")
    a("")
    a(f"- **Criterion.** min(endpoint, first face yield, first core shear) >= SF x 95.46083791 kPa.")
    a(f"  - 95.46083791 kPa is ISA at 500 m, to {abs(p_isa['mine'] - p_isa['card']) / p_isa['card']:.1e}. The SF 1.05 target "
      "100.23387981 kPa follows.")
    a("  - Every tested boundary straddles 345 MPa with the core index below 1 and the converged path past the target.")
    a(f"- **Perfect-sphere first yield, own membrane statics.** The two faces carry the hemisphere load at {sig:.3f} MPa at service. "
      "That puts first yield at 80.95, 95.24 and 109.52 kPa for 255, 300 and 345 MPa. All three lie inside the card's brackets.")
    a(f"- **Perfect-sphere first yield, own FE.** {pf[255]['mine']:.3f} / {pf[300]['mine']:.3f} / {pf[345]['mine']:.3f} kPa, against "
      f"the card's {pf[255]['card']:.3f} / {pf[300]['card']:.3f} / {pf[345]['card']:.3f}.")
    a(f"- **Perfect-sphere endpoints, own FE.** {pe[255]['mine']:.3f} / {pe[300]['mine']:.3f} / {pe[345]['mine']:.3f} kPa, against "
      f"the card's {pe[255]['card']:.3f} / {pe[300]['card']:.3f} / {pe[345]['card']:.3f}.")
    a(f"- **345 MPa brackets.** The check's own model, a different and finer mesh, gives the same pass/fail at every tested pair:")
    a(f"  - **SF 1:** 1.208988 / 1.226988 mm carry {s1p['face_mises_max']:.3f} / {s1f['face_mises_max']:.3f} MPa (card "
      f"{brow('SF 1.0 passing amplitude')['card']:.3f} / {brow('SF 1.0 failing amplitude')['card']:.3f}).")
    a(f"  - **SF 1.05:** 0.737936 / 0.755936 mm carry {s5p['face_mises_max']:.3f} / {s5f['face_mises_max']:.3f} MPa (card "
      f"{brow('SF 1.05 passing amplitude')['card']:.3f} / {brow('SF 1.05 failing amplitude')['card']:.3f}).")
    a(f"  - **Estimates:** {g['SF1.0']['estimate_mm']:.4f} and {g['SF1.05']['estimate_mm']:.4f} mm, against the card's 1.2192 and 0.7478.")
    a("  - **At a real 345 MPa:** own runs yield exactly where the card's native confirmations do.")
    a(f"  - **Other pairs:** L 332, W 401.9 and both cure-debit pairs also reproduce (estimates within {max(abs(L332['difference']), abs(W402['difference']), abs(cd1['difference']), abs(cd5['difference'])):.4f} mm).")
    a(f"  - **Mesh:** own refinement adds {m1:+.2f} MPa, about {m1 / 39.6:.3f} mm.")
    a(f"- **Core law and admissibility.** The Hexcel CR III Table II values are verified from the pinned PDF.")
    a(f"  - **Simple shear, own exact minimisation:** the inherited 0.01/0.005 MPa law loses ellipticity at {inh:.4f} MPa (CHECK-029: "
      f"0.088). The regularized 1/0.5 MPa law holds until {reg:.2f} MPa.")
    a(f"  - **Regularized law at the governing passing state:** the exact acoustic minimum is "
      f"{AC['regularized']['exact_min_MPa']:+.3f} MPa. The card's sufficient bound, 0.314 MPa over all passing states, is a valid lower bound.")
    a(f"  - **Inherited law at the same state:** {AC['inherited']['exact_min_MPa']:+.6f} MPa (card's probe -0.005455).")
    a(f"  - **The regularization does not drive the answer:** moving the in-plane law from 0.01 to 10 MPa moves the governing face "
      f"stress {reg_inh:+.3f} to {reg_10:+.3f} MPa, at most {max(abs(reg_inh), abs(reg_10)) / 39.6:.3f} mm.")
    a(f"- **Endpoint division and transfer.** Own endpoints at the limiting 401.9 mm/W pair are {e_pass['mine']:.4f} / "
      f"{e_fail['mine']:.4f} kPa (card {e_pass['card']:.4f} / {e_fail['card']:.4f}).")
    a("  - Dividing by 1.10 gives the same 0.521-0.539 mm bracket.")
    a("  - The perfect sphere's endpoint / 1.10 is 99.71 kPa, below 100.23, so SF 1.05 fails even at zero amplitude.")
    a("  - 2.3146-2.4589 are CHECK-029's recorded factors. 109.68 / 2.3146 = 47.4 kPa, so no amplitude is admissible.")
    a("")
    a("## Mismatches, exactly")
    a("")
    a("| Where | Field | Card | Check | Note |")
    a("|---|---|---:|---:|---|")
    a(f"| Larger dimples, 332.2 mm / W, 11.8 mm | first face yield estimate, kPa | {big['card']:.3f} | {big['mine']:.3f} | Inside the card's native "
      "bracket 61.2-64.8. The card's sweep runs appear to use its coarse family: their native RSS, about 108 MB, matches its 256/1/4 "
      f"perfect-sphere runs, against 328 MB for the 512/2/6 boundary runs. The check uses a 4 mm mesh. The check's own two-point extrapolation from 60 and 61 kPa gives 63.69, so the estimator is not the cause. "
      f"It is a diagnostic: that row is governed by core shear at {big_c['card']:.3f} kPa (check {big_c['mine']:.3f}), and its endpoint agrees "
      f"({big_e['card']:.3f} / {big_e['mine']:.3f}). |")
    a("| Geometry | core thickness, mm | 23.23721790601544 | 23.23721790601548 | 037b's record; 15th digit |")
    a(f"| Service pressure | kPa | 95.46083791390515 | {p_isa['mine']:.8f} | ISA 500 m with the US 1976 constants; 8th digit |")
    a("")
    a(f"Nothing else differs, across {nA} arithmetic rows and {nB} compared FE rows (A-ARITH.json, B-FE.json).")
    a("")
    a("## Sources, tags and formulas")
    a("")
    a("- **Verified against pinned documents:**")
    a("  - Hexcel CR III Table II, 5056 3/8 1.0 pcf: shear W 25/35 psi and L 45/55 psi (minimum average / typical); moduli 6.8 / 15 ksi; "
      "compressive modulus 15 ksi; crush 35 psi.")
    a("  - NASA CR-194164 Table 2: nu 0.0768.")
    a("  - NASA 19660014454 p.25: 0.050 in after trimming, and 0.150-0.200 in after chemical milling.")
    a("  - NASA 19730016169 p.86: 0.003 in to the die.")
    a("  - 036: the 345 MPa basis is a tensile minimum, with compressive yield blank.")
    a("- **Traced to source reports:**")
    a("  - 037b: geometry, scarf 30.3414 and residual 3.41022257 MPa.")
    a("  - 029: widths and moduli.")
    a("  - 042: 9.32-16.06 mm.")
    a("  - 015b: 0.1393 / 0.6544 mm, at 015b's own widths.")
    a("  - CHECK-029: 0.088 MPa and 2.3146-2.4589.")
    a(f"- **Unsourced:** E = 290 GPa has no source in 047. The cited Table 2 gives 298.7 GPa (L) and 293.6 GPa (LT). At 298.7 GPa the "
      f"governing face stress falls {abs(eE1):.2f} MPa, and the SF 1 tolerance rises to {eEst:.4f} mm ({eEst - g['SF1.0']['estimate_mm']:+.4f} mm), "
      "about one bracket width. NFI-C047-02.")
    a("- **Tags:** the card carries QUESTIONABLE / PROJECTION, and all 14 NFI rows are tagged.")
    a("- **Bookkeeping:** 319 native runs, 1892 checks (all passed), 92 core records, 7913.98 s elapsed, 24053.62 CPU-s and 626.5 MiB "
      "peak all re-derive.")
    a("- **Formulas confirmed:**")
    a("  - the Gaussian offset;")
    a("  - the classical lengths: 347.1529189, 347.1845439 with face bending, and 2181.424825 full wave;")
    a("  - the exact full-sphere RMS, with the small-patch form 4.6e-5 high;")
    a("  - the quadratic interaction: the index exceeds the meridian ratio by an implied 0.0021 MPa hoop shear;")
    a("  - the Cholesky current-frame shear: the check's implementation reproduces the card's core shears to 0.0001 MPa;")
    a("  - the sufficient acoustic bound: the check derives it as a valid lower bound.")
    a("")
    a("## The check's own model")
    a("")
    a("fe047.py builds it from the card's and METHOD.md's stated definitions alone:")
    a("- **Geometry:** full sphere; every layer offset inward by a exp[-(R theta / w)^2], stress-free.")
    a(f"- **Mesh:** CAX8 elements. Own angular mesh: {mesh['h_fine_mm']:.0f} mm out to {mesh['s_fine_mm']:.0f} mm, growth 1.06, "
      f"{mesh['h_far_mm']:.0f} mm beyond. That is {mesh['n_theta']} angular elements and {mesh['nface']}+{mesh['ncore']}+{mesh['nface']} layers: "
      f"{mesh['elements']} elements and {mesh['nodes']} nodes.")
    a("- **Restraints:** the axis radially, and one south-pole node axially.")
    a("- **Faces:** E 290 GPa, nu 0.0768, *PLASTIC with NLGEOM. 10,000 MPa traces the pre-yield branch, as the card does.")
    a("- **Core:** StVK engineering constants on a cylindrical orientation about the out-of-plane axis, which gives the sphere's radial, "
      "meridian and hoop axes. W puts 6.8 ksi on the radial-meridian pair.")
    a("- **Load:** a follower pressure in steps that end exactly at the service and SF 1.05 targets. Endpoints are the last converged "
      "increment.")
    a("")
    a("- **Runs:** 31 solves ran serially through simjob on 4 cores, 0.4-5.2 min each. Twelve short single-core debug solves "
      "(seconds each) ran directly.")
    a("- **A setup error of the check's own:** CalculiX reads at most 20 characters a field, so pressures written with 16 digits were "
      "truncated, and the first trial ran at 100 times its load.")
    a("  - It was found from a 1,000-fold soft all-Be sphere and fixed to 12 digits.")
    a("  - The fix was verified against the membrane solution (0.0513 mm at 8 kPa) and a unit axisymmetric column before any compared run.")
    a("  - The check's first endpoint parser read the wrong .sta column. It was corrected and every endpoint re-parsed.")
    a("")
    a("## Then")
    a("")
    a("Stop and file. The robotics seat sends the next job. NFI.json carries the check's two rows.")
    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "CHECK.md.tmp"), "w") as fh:
        fh.write(text)
    os.replace(os.path.join(HERE, "CHECK.md.tmp"), os.path.join(HERE, "CHECK.md"))

    json.dump(fe_runs, open(os.path.join(HERE, "FE-RUNS.json"), "w"), indent=1, default=float)
    now = datetime.datetime.now().astimezone().isoformat()
    results = {"schema": 1, "check": "CHECK-047", "unit": "vacuum-mainline047-check-1020", "order": ORDER, "checked_report": CHECKED,
               "status": "ESTIMATE", "tag": "QUESTIONABLE / PROJECTION", "certification": "none", "owner_code_read_or_run": False,
               "job_started_at": JOB_STARTED, "job_ended_at": now, "times_are": "measurements only",
               "verdict": {"arithmetic_rows": nA, "arithmetic_agree": nA_ok, "fe_rows_compared": nB, "fe_agree": nB_ok,
                           "mismatches": ["larger-dimple 11.8 mm face-yield estimate 61.910 vs 63.596 kPa (mesh; diagnostic)",
                                          "core thickness 15th digit", "service pressure 8th digit"],
                           "governing_estimates_mm": {"SF1": g["SF1.0"]["estimate_mm"], "SF1.05": g["SF1.05"]["estimate_mm"]},
                           "regularization_effect_MPa": [reg_inh, reg_10], "E298.7_SF1_estimate_mm": eEst,
                           "simple_shear_ellipticity_MPa": shear, "acoustic": AC},
               "arithmetic": A["rows"], "fe": B["rows"], "fe_runs": sorted(fe_runs)}
    with open(os.path.join(HERE, "RESULTS.json.tmp"), "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "RESULTS.json.tmp"), os.path.join(HERE, "RESULTS.json"))
    items = [
        ("NFI-C047-01", "QUESTIONABLE", "The larger-dimple sweep, the perfect-sphere cases and the 1.10 calibration run on a coarser native "
         "family than the stated 512/2/6 boundary mesh: the perfect cases record 256/1/4, and the sweep's native RSS matches. CARD.md and "
         "METHOD.md describe only the boundary mesh. On a 4 mm own mesh the 11.8 mm face-yield estimate is 63.60 kPa, not 61.91, though "
         "inside the native bracket. Endpoints agree within 0.02 kPa, and the acceptance numbers are unaffected.",
         "State the mesh for every table; recompute the larger-dimple face-yield estimates on the boundary mesh."),
        ("NFI-C047-02", "QUESTIONABLE", "The face modulus E = 290 GPa has no source in 047. The cited NASA CR-194164 Table 2 gives 298.7 GPa "
         "(L) and 293.6 GPa (LT) for 1.96 mm SR-200 sheet. With 298.7 GPa the check's model lowers the governing face stress 0.57 MPa "
         "and raises the SF 1 tolerance about 0.015 mm, one bracket width.",
         "Name the modulus source, or carry the finished-sheet modulus range as a sensitivity (with 047-02)."),
    ]
    nfi = {"schema": 1, "check": "CHECK-047", "unit": "vacuum-mainline047-check-1020", "tag": "QUESTIONABLE", "status": "OPEN",
           "items": [{"id": i, "tag": t, "claim": c, "needed_to_ground": n} for i, t, c, n in items]}
    with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
        json.dump(nfi, fh, indent=1)
    os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))

    def pin(p, role):
        data = open(p, "rb").read()
        return {"path": p, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "role": role}
    pins = [pin(f"{B_}/CHECK.md", "brief"), pin(f"{B_}/COMMON.md", "brief"), pin(f"{Q}/{ORDER}.json", "order"),
            pin(f"{Q}/{CHECKED}.json", "checked report")]
    for n in ("CARD.md", "METHOD.md", "RESULTS.json", "CORE-RESULTS.json", "CORE-BOUNDARIES.json", "CORE-CALIBRATION.json",
              "CORE-SWEEP.csv", "NFI.json", "ALL-NATIVE-RUNS.csv", "RUN-RESOURCES.json", "EVIDENCE-CHECKS.json", "INPUT-CUSTODY.json"):
        pins.append(pin(f"{O}/{n}", "checked card's filed data (read as data)"))
    for p, role in ((f"{WS}/ref-4189c1615990eb515921/.ship/work/outputs/vacuum-mainline037b-bond-temperature-1020/RESULTS.json", "source report 037b"),
                    (f"{WS}/ref-ed3515d83349998d6b1b/.ship/work/outputs/vacuum-mainline029-crimp-gamma-fe-1020/RESULTS.json", "source report 029"),
                    (f"{WS}/ref-55cff924be25afe6f9dd/.ship/work/outputs/vacuum-mainline042-build-route-1020/RESULTS.json", "source report 042"),
                    (f"{WS}/ref-cca93dbfd236dcaa3a8b/.ship/work/outputs/vacuum-mainline015b-kd-precision-fix-1020/RESULTS.json", "source report 015b"),
                    (f"{WS}/ref-55cff924be25afe6f9dd/.ship/work/outputs/vacuum-mainline029-check-1020/RESULTS.json", "source report CHECK-029"),
                    (f"{WS}/ref-70f7af6d0a8d64c42272/.ship/work/outputs/vacuum-mainline036-be-sheet-compression-1020/EVIDENCE.json", "source report 036"),
                    (f"{SRC29}/criii.pdf", "source document"), (f"{SRC29}/sr200-nasa-cr194164.txt", "source document"),
                    (f"{SRC29}/ccx_2.21.txt", "solver manual"),
                    (f"{LIT}/P1/ntrs66014454/19660014454.pdf", "source document"), (f"{LIT}/B/ntrs-19730016169/doc.pdf", "source document")):
        pins.append(pin(p, role))
    for n in ("chk047a.py", "fe047.py", "runall.py", "runall2.py", "runall3.py", "chk047b.py", "card047.py", "simretry.sh",
              "A-ARITH.json", "B-FE.json", "B-ACOUSTIC.json", "FE-RUNS.json"):
        pins.append(pin(os.path.join(HERE, n), "this check's own code or intermediate"))
    inputs = {"schema": 1, "check": "CHECK-047", "unit": "vacuum-mainline047-check-1020", "pins": pins}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(len(text), "bytes check;", len(items), "NFI;", len(pins), "pins;", len(fe_runs), "FE runs")


if __name__ == "__main__":
    main()
