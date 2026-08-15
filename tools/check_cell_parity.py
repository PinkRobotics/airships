#!/usr/bin/env python3
"""ship/model.js must agree with research/analysis/vacuum-cell.py, to floating point.

    python3 tools/check_cell_parity.py

There are two copies of the cell physics: one in Python so the analysis is reproducible from
a shell, and one in JavaScript so the page can be dialled rather than read. Two copies of a
calculation is the failure this project keeps finding, so they are checked rather than
trusted — and on the day this file was written the check earned its place immediately, by
catching an ISA density expression that was 6% high in BOTH of them.

Runs the page in a real browser through tools/js_eval.py and diffs every architecture for
every material.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PY_JSON = ROOT / "research" / "analysis" / "vacuum-cell.json"
TOL = 1e-9

PROBE = """(() => {
  const C = window.CELL;
  const out = { rhoAir: {}, materials: {} };
  for (const h of [0, 1000, 2500, 5000]) out.rhoAir[h] = C.rhoAir(h);
  for (const [k, m] of Object.entries(C.MATERIALS)) {
    out.materials[k] = {
      monolithic: C.ARCHS.monolithic(m).rho,
      solidStrut: C.ARCHS.solidStrut(m).rho,
      tubeStrut: C.ARCHS.tubeStrut(m).rho,
      total: C.totalShell(m, 2.0).total,
      phi: C.ARCHS.tubeStrut(m).phi,
    };
  }
  out.ladders = {};
  for (const k of ['M60J_LAM', 'T700_LAM', 'CFF', 'PAHT_Z']) {
    out.ladders[k] = C.ladder(C.MATERIALS[k]).map(r => r.total);
  }
  out.printerChain = C.printerChain(C.MATERIALS.PAHT_Z).map(r => ({
    strutM: r.strutM, cellM: r.cellM, enclosedL: r.enclosedL,
    tubeRadiusMm: r.tubeRadiusMm }));
  const d = C.demonstrator(C.MATERIALS.PAHT_Z);
  out.demonstrator = { latticeKg: d.latticeKg, totalKg: d.totalKg,
                       massOverDisplaced: d.massOverDisplaced, enclosedL: d.enclosedL };
  const g = C.gradedPressure(C.MATERIALS.M60J_LAM, __WALL__);
  out.graded = { bulk: g.bulk.map(r => [r.structure, r.gas, r.films, r.netLift]),
                 bandCostPct: g.band.costPctOfNetLift,
                 bandNetCost: g.band.netCost };
  out.cellShapes = C.cellShapes();
  out.sharedWall = C.sharedWall(2.0);
  out.plenum = C.pumpedPlenum().map(r => r.cellOperatingMarginX);
  out.weightless = C.weightlessArticle(__WALL__).map(r =>
    [r.densityAtN1, r.minNSeaLevel === null ? -1 : r.minNSeaLevel,
     r.minNAt2500m === null ? -1 : r.minNAt2500m]);
  const s = C.stockBuild();
  out.stock = { pipeKg: s.pipeKg, nodesKg: s.nodesKg, skinKg: s.skinKg,
                totalKg: s.totalKg, demandN: s.perStrutDemandN,
                eulerPinned: s.eulerMarginPinned, eulerSocketed: s.eulerMarginSocketed,
                tieEuler: s.tieEulerMargin, longCuts: s.longCuts, shortCuts: s.shortCuts,
                nodesMeasuredConst: C.NODE_MASS_MEASURED_KG,
                rimDemandN: s.rimDemandN, rimEuler: s.rimEulerMargin,
                spokeDemandN: s.spokeDemandN, spokeEuler: s.spokeEulerMargin,
                tieDemandN: s.tieDemandN,
                kgPerM3: s.kgPerM3,
                massOverDisplaced: s.massOverDisplaced };
  // The per-family demands, at the SAME raw span the Python published them at — the
  // PINNED article span: the live chain's design point is free to move under corrected
  // physics, the built article is not.
  const spanRaw = 2 * C.DEMO_PITCH_PINNED_M;
  const md = C.memberDemands(spanRaw);
  out.demands = { families: md.families, scalars: {
    crushPerOctetStrutN: md.crushPerOctetStrutN,
    octetStandaloneEntryN: md.octetStandaloneEntryN,
    rimSquareHexEdgeN: md.rimSquareHexEdgeN,
    hexRingHoopN: md.hexRingHoopN, sqRingHoopN: md.sqRingHoopN,
    inPlanePullHexNPerM: md.inPlanePullHexNPerM,
    inPlanePullSqNPerM: md.inPlanePullSqNPerM,
    governingShortMemberN: md.governingShortMemberN },
    external: md.externalFilmShareAtSF, divisor: md.crushDivisor };
  const el = C.filmEdgeLoads(C.demonstrator(C.MATERIALS.PAHT_Z).spanM);
  out.edgeLoads = { hexFaceLoadN: el.hexFaceLoadN, tripodPropN: el.tripodPropN,
                    totalSurfaceLoadN: el.totalSurfaceLoadN,
                    rows: el.rows.map(r => [r.lineLoadNPerM, r.failsAtAtm]) };
  const kc = C.kelvinLatticeCounts(1), kc2 = C.kelvinLatticeCounts(2);
  out.counts = [kc.struts, kc.rimStrutEquivalents, kc.tieStruts, kc.hexTieStruts,
                kc.hexSpokeStruts, kc.hexNodes];
  out.counts2 = [kc2.struts, kc2.rimStrutEquivalents, kc2.hexSpokeStruts];
  // SHIP 0 — the film-on-rings port. The whole summary the pages bind, raw; the
  // Python record carries the published rounding and this gate holds them together.
  out.ship0 = C.ship0Summary();
  return out;
})()"""


def main() -> None:
    if not PY_JSON.exists():
        sys.exit("check_cell_parity: run `make analysis` first — vacuum-cell.json is missing.")
    py = json.loads(PY_JSON.read_text())

    with tempfile.TemporaryDirectory(dir=str(pathlib.Path.home() / "tmp")) as td:
        probe = pathlib.Path(td) / "probe.js"
        # The graded-pressure comparison must use the SAME wall value the Python used —
        # figures.json's, not a fresh rhoAir(2500) that rounds differently in the last digit.
        probe.write_text(PROBE.replace(
            "__WALL__", repr(py["theWall"]["rhoAirAtWorkAltKgPerM3"])))
        out = pathlib.Path(td) / "out.json"
        srv = subprocess.Popen([sys.executable, str(ROOT / "tools" / "serve.py"),
                                "--port", "8907", "--quiet"], cwd=ROOT)
        try:
            subprocess.run([sys.executable, str(ROOT / "tools" / "js_eval.py"),
                            "http://127.0.0.1:8907/cell/index.html", str(probe),
                            str(out), "10"], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            js = json.loads(out.read_text())
        finally:
            srv.terminate()
            srv.wait()

    bad, checked = [], 0

    for h, rec in py["nullResults"]["altitude"]["sweep"].items():
        got = js["rhoAir"][h.split()[0]]
        checked += 1
        if abs(round(got, 4) - rec["rhoAirKgPerM3"]) > 1e-4:
            bad.append(f"rhoAir({h}): python {rec['rhoAirKgPerM3']}, js {round(got, 4)}")

    # The JSON keys and the JS field names, paired.
    PAIRS = (("monolithicKgPerM3", "monolithic", 3),
             ("solidStrutKgPerM3", "solidStrut", 3),
             ("tubeLatticeKgPerM3", "tubeStrut", 4),
             ("totalKgPerM3", "total", 4))
    for key, prec in py["materials"].items():
        jsm = js["materials"].get(key)
        if jsm is None:
            bad.append(f"{key}: present in Python, missing from ship/model.js")
            continue
        for pykey, jskey, prec_dp in PAIRS:
            want, got = prec[pykey], jsm[jskey]
            checked += 1
            if abs(round(got, prec_dp) - want) > TOL:
                bad.append(f"{key}.{jskey}: python {want}, js {round(got, prec_dp)}")

    for key in js["materials"]:
        if key not in py["materials"]:
            bad.append(f"{key}: present in ship/model.js, missing from the Python")

    def cmp(label: str, want, got, dp: int) -> None:
        nonlocal checked
        checked += 1
        if abs(round(got, dp) - want) > TOL:
            bad.append(f"{label}: python {want}, js {round(got, dp)}")

    # Hierarchy ladders, four materials x five levels.
    for mat, totals in js["ladders"].items():
        pyl = py["hierarchy"]["ladders"][mat]
        for n, got in enumerate(totals):
            cmp(f"ladder[{mat}][{n}].total", pyl[str(n)]["totalKgPerM3"], got, 4)

    # The printer chain, all four rows.
    py_rows = list(py["printerChain"]["rows"].values())
    for i, row in enumerate(js["printerChain"]):
        cmp(f"printerChain[{i}].strutM", py_rows[i]["strutM"], row["strutM"], 3)
        cmp(f"printerChain[{i}].cellM", py_rows[i]["cellM"], row["cellM"], 3)
        cmp(f"printerChain[{i}].enclosedL", py_rows[i]["enclosedL"], row["enclosedL"], 0)
        cmp(f"printerChain[{i}].tubeRadiusMm", py_rows[i]["tubeRadiusMm"],
            row["tubeRadiusMm"], 1)

    # The demonstrator record.
    pd, jd = py["demonstrator"], js["demonstrator"]
    cmp("demonstrator.latticeKg", pd["latticeKg"], jd["latticeKg"], 3)
    cmp("demonstrator.totalKg", pd["totalKg"], jd["totalKg"], 3)
    cmp("demonstrator.massOverDisplaced", pd["massOverDisplaced"],
        jd["massOverDisplaced"], 1)
    cmp("demonstrator.enclosedL", pd["enclosedL"], jd["enclosedL"], 0)

    # Graded pressure: the bulk sweep and the boundary band.
    pg = py["gradedPressure"]
    for i, n in enumerate((1, 2, 5, 10)):
        prow, jrow = pg["bulk"][str(n)], js["graded"]["bulk"][i]
        for j, field in enumerate(("structureKgPerM3", "gasKgPerM3", "filmsKgPerM3",
                                   "netLiftKgPerM3")):
            cmp(f"graded.bulk[{n}].{field}", prow[field], jrow[j], 4)
    cmp("graded.band.costPctOfNetLift", pg["band"]["costPctOfNetLift"],
        js["graded"]["bandCostPct"], 1)
    cmp("graded.band.netCostKgPerM3", pg["band"]["netCostKgPerM3"],
        js["graded"]["bandNetCost"], 4)

    # Cell shapes and the shared-wall fractions.
    for name, rec in py["cellShapes"].items():
        cmp(f"cellShapes.{name}.coeff", rec["coeff"], js["cellShapes"][name]["coeff"], 4)
        cmp(f"cellShapes.{name}.saving", rec["filmSavingVsCubePct"],
            js["cellShapes"][name]["filmSavingVsCubePct"], 1)
    psw = py["sharedWall"]["2.0 m cells"]
    cmp("sharedWall.sharedFractionPct", psw["sharedFractionPct"],
        js["sharedWall"]["sharedFractionPct"], 1)
    cmp("sharedWall.interiorOverEnvelope", psw["interiorOverEnvelope"],
        js["sharedWall"]["interiorOverEnvelope"], 1)

    # The pumped plenum's operating-margin ladder.
    pp = list(py["pumpedPlenum"]["rows"].values())
    for i, got in enumerate(js["plenum"]):
        cmp(f"plenum[{i}].margin", pp[i]["cellOperatingMarginX"], got, 2)

    # The hybrid stock build: purchased pipe, printed ties, margins.
    ps, jsb = py["stockBuild"], js["stock"]
    cmp("stock.pipeKg", ps["pipe"]["kg"], jsb["pipeKg"], 3)
    cmp("stock.nodesKg", ps["printed"]["nodesKg"], jsb["nodesKg"], 3)
    cmp("stock.totalKg", ps["totalKg"], jsb["totalKg"], 3)
    cmp("stock.skinKg", ps["skinKg"], jsb["skinKg"], 3)
    cmp("stock.demandN", ps["pipe"]["perStrutDemandN"], jsb["demandN"], 0)
    cmp("stock.eulerPinned", ps["pipe"]["eulerMarginPinned"], jsb["eulerPinned"], 2)
    cmp("stock.eulerSocketed", ps["pipe"]["eulerMarginSocketed"], jsb["eulerSocketed"], 2)
    cmp("stock.tieEuler", ps["pipe"]["tieEulerMargin"], jsb["tieEuler"], 2)
    cmp("stock.massOverDisplaced", ps["massOverDisplaced"],
        jsb["massOverDisplaced"], 1)
    cmp("stock.kgPerM3", ps["kgPerM3"], jsb["kgPerM3"], 2)
    cmp("stock.longCuts", ps["pipe"]["longCuts"], jsb["longCuts"], 0)
    cmp("stock.shortCuts", ps["pipe"]["shortCuts"], jsb["shortCuts"], 0)
    cmp("stock.rimDemandN", ps["pipe"]["rimDemandN"], jsb["rimDemandN"], 0)
    cmp("stock.rimEuler", ps["pipe"]["rimEulerMargin"], jsb["rimEuler"], 2)
    cmp("stock.spokeDemandN", ps["pipe"]["spokeDemandN"], jsb["spokeDemandN"], 0)
    cmp("stock.spokeEuler", ps["pipe"]["spokeEulerMargin"], jsb["spokeEuler"], 2)
    cmp("stock.tieDemandN", ps["pipe"]["tieDemandN"], jsb["tieDemandN"], 0)

    # ONE DEMAND PER FAMILY. The defect this covers is the reverse of a drifting number: two
    # copies of a load path, one of which quietly keeps handing the octet's crush to a rim
    # or a spoke. Every family and every intermediate is held, so a change on one side has
    # nowhere to hide.
    pmd, jmd = py["memberDemands"], js["demands"]
    cmp("demands.crushDivisor", pmd["crushDivisor"], jmd["divisor"], 0)
    for fam, rec in pmd["families"].items():
        if fam not in jmd["families"]:
            bad.append(f"demands.{fam}: present in Python, missing from ship/model.js")
            continue
        cmp(f"demands.{fam}", round(rec["axialN"]), jmd["families"][fam], 0)
    for fam in jmd["families"]:
        if fam not in pmd["families"]:
            bad.append(f"demands.{fam}: present in ship/model.js, missing from the Python")
    for key, got in jmd["scalars"].items():
        cmp(f"demands.{key}", round(pmd[key]), got, 0)
    for key, got in jmd["external"].items():
        cmp(f"demands.film.{key}", round(pmd["externalFilmShareAtSF"][key]), got, 0)

    # THE MEASURED NODE MASS. ship/model.js cannot read the geometry manifest, so it
    # carries the number as a constant; this is what stops it drifting when the joints
    # are regenerated (the failure mode that produced NODE_MASS_FRAC in the first place).
    cmp("nodes.measuredKg", ps["printed"]["nodesKg"], jsb["nodesMeasuredConst"], 3)

    # The film's edge loads — the bending check that governs the boundary.
    pfe, jfe = py["filmEdgeLoads"], js["edgeLoads"]
    cmp("film.hexFaceLoadN", pfe["hexFaceLoadN"], jfe["hexFaceLoadN"], 0)
    cmp("film.tripodPropN", pfe["tripodPropN"], jfe["tripodPropN"], 0)
    cmp("film.totalSurfaceLoadN", pfe["totalSurfaceLoadN"], jfe["totalSurfaceLoadN"], 0)
    for i, prow in enumerate(pfe["rows"]):
        cmp(f"film.rows[{i}].w", prow["lineLoadNPerM"], jfe["rows"][i][0], 0)
        cmp(f"film.rows[{i}].failsAtAtm", prow["failsAtAtm"], jfe["rows"][i][1], 2)

    # The lattice counts, every family — the parity gate is what keeps the two graphs
    # identical, and it caught a doubled lattice once already.
    pc1 = py["kelvinFaces"]["1"]
    for k, idx in (("struts", 0), ("rimStrutEquivalents", 1), ("tieStruts", 2),
                   ("hexTieStruts", 3), ("hexSpokeStruts", 4), ("hexNodes", 5)):
        cmp(f"counts1.{k}", pc1[k], js["counts"][idx], 0)
    pc2 = py["kelvinFaces"]["2"]
    cmp("counts2.struts", pc2["struts"], js["counts2"][0], 0)
    cmp("counts2.rim", pc2["rimStrutEquivalents"], js["counts2"][1], 0)
    cmp("counts2.spokes", pc2["hexSpokeStruts"], js["counts2"][2], 0)

    # The weightless article: density at one cell and the minimum floating sizes.
    pw = list(py["weightlessArticle"]["rows"].values())
    for i, (rho, sl, alt) in enumerate(js["weightless"]):
        cmp(f"weightless[{i}].rho", pw[i]["densityAtN1"], rho, 3)
        cmp(f"weightless[{i}].minSL",
            -1 if pw[i]["minNSeaLevel"] is None else pw[i]["minNSeaLevel"], sl, 0)
        cmp(f"weightless[{i}].minAlt",
            -1 if pw[i]["minNAt2500m"] is None else pw[i]["minNAt2500m"], alt, 0)

    # SHIP 0 — the film-on-rings wall's whole record: both SFs, all three sigma
    # worlds, the ledger, the sections, the checks, the counts, the float window.
    # Missing-key detection both directions, like the materials block above.
    psh, jsh = py.get("ship0"), js.get("ship0")
    if psh is None or jsh is None:
        bad.append("ship0: missing on one side — the port must land in BOTH files "
                   "in one commit (parity is bidirectional)")
    else:
        for world, prow in psh["worlds"].items():
            jrow = jsh["worlds"].get(world)
            if jrow is None:
                bad.append(f"ship0.worlds.{world}: present in Python, missing from JS")
                continue
            cmp(f"ship0.{world}.totalT", prow["totalT"], jrow["totalT"], 1)
            cmp(f"ship0.{world}.ratioSL", prow["ratioSL"], jrow["ratioSL"], 3)
            cmp(f"ship0.{world}.residualSLT", prow["residualSLT"],
                jrow["residualSLT"], 1)
            cmp(f"ship0.{world}.ratio2500", prow["ratio2500"], jrow["ratio2500"], 3)
            checked += 1
            if bool(prow["floats"]) != bool(jrow["floats"]):
                bad.append(f"ship0.{world}.floats: python {prow['floats']}, "
                           f"js {jrow['floats']}")
        for world in jsh["worlds"]:
            if world not in psh["worlds"]:
                bad.append(f"ship0.worlds.{world}: present in JS, missing from Python")
        pp, jp = psh["planOfRecord"], jsh["planOfRecord"]
        for k, dp in (("diaM", 1), ("lenM", 1), ("vM3", 0), ("areaM2", 0),
                      ("liftSLT", 1), ("lift2500T", 1), ("ringPitchM", 2),
                      ("barPitchM", 2), ("nLong", 0), ("kFan", 0), ("depthM", 1),
                      ("bayM", 1), ("braceM", 3)):
            cmp(f"ship0.plan.{k}", pp[k], jp[k], dp)
        pm, jm = psh["mid"], jsh["mid"]
        cmp("ship0.mid.totalT", pm["totalT"], jm["totalT"], 1)
        cmp("ship0.mid.ratioSL", pm["ratioSL"], jm["ratioSL"], 3)
        cmp("ship0.mid.residualSLT", pm["residualSLT"], jm["residualSLT"], 1)
        cmp("ship0.mid.arealKgM2", pm["arealKgM2"], jm["arealKgM2"], 2)
        for k, want in pm["ledgerT"].items():
            if k not in jm["ledgerT"]:
                bad.append(f"ship0.ledger.{k}: present in Python, missing from JS")
                continue
            cmp(f"ship0.ledger.{k}", want, jm["ledgerT"][k], 1)
        for k in jm["ledgerT"]:
            if k not in pm["ledgerT"]:
                bad.append(f"ship0.ledger.{k}: present in JS, missing from Python")
        ps_, js_ = psh["sections"], jsh["sections"]
        for mem in ("ring", "bar", "longeron"):
            cmp(f"ship0.{mem}.odMm", ps_[mem]["odMm"], js_[mem]["odMm"], 0)
            cmp(f"ship0.{mem}.wallMm", ps_[mem]["wallMm"], js_[mem]["wallMm"], 1)
            cmp(f"ship0.{mem}.margin", ps_[mem]["marginAtSF"],
                js_[mem]["marginAtSF"], 2)
        for mem in ("ring", "longeron"):
            checked += 1
            if ps_[mem]["governs"] != js_[mem]["governs"]:
                bad.append(f"ship0.{mem}.governs: python {ps_[mem]['governs']}, "
                           f"js {js_[mem]['governs']}")
        cmp("ship0.filmGM2", ps_["filmGM2"], js_["filmGM2"], 0)
        cmp("ship0.ring.runsAtMPa", ps_["ring"]["runsAtMPa"],
            js_["ring"]["runsAtMPa"], 0)
        # The frame-practice matrix, the reported alternative world.
        for world, prow in psh["worldsFramePractice"].items():
            jrow = jsh["worldsFramePractice"].get(world)
            if jrow is None:
                bad.append(f"ship0.frame.{world}: missing from JS")
                continue
            cmp(f"ship0.frame.{world}.totalT", prow["totalT"], jrow["totalT"], 1)
            cmp(f"ship0.frame.{world}.ratioSL", prow["ratioSL"],
                jrow["ratioSL"], 3)
            checked += 1
            if bool(prow["floats"]) != bool(jrow["floats"]):
                bad.append(f"ship0.frame.{world}.floats: python "
                           f"{prow['floats']}, js {jrow['floats']}")
        pc_, jc_ = psh["checks"], jsh["checks"]
        for k, dp in (("giMarginHarsh", 2), ("giMarginFrame", 2),
                      ("giMarginK02", 2), ("giCritN", 0),
                      ("reserveKgM2", 2), ("capBuckleMargin", 1),
                      ("beamBendMargin", 0), ("torsionMargin", 1),
                      ("cradleFlangeMPa", 1), ("windMargin", 2),
                      ("jigPoints", 0)):
            cmp(f"ship0.checks.{k}", pc_[k], jc_[k], dp)
        for k in ("unpressurised", "unpressurisedAllOk", "checksPass"):
            checked += 1
            if bool(pc_[k]) != bool(jc_[k]):
                bad.append(f"ship0.checks.{k}: python {pc_[k]}, js {jc_[k]}")
        for k in ("rings", "bars", "panels", "clamps", "barrelRings"):
            cmp(f"ship0.counts.{k}", psh["counts"][k], jsh["counts"][k], 0)
        for k in ("longerons", "innerRings", "fanWebsPerColPerBay", "thetaWebs"):
            cmp(f"ship0.skeletonCounts.{k}", psh["skeletonCounts"][k],
                jsh["skeletonCounts"][k], 0)
        # The spoke net (2026-08-14): a length and a count, not a smeared area. Both
        # mirrors walk the same bay planes with the same polar cut-off, so a drift in
        # either one is a drift in the layout itself.
        for k, dp in (("planes", 0), ("planesTotal", 0), ("cords", 0),
                      ("lengthM", 0), ("meanCordM", 2), ("cordMm", 2), ("massT", 2)):
            cmp(f"ship0.spokeNet.{k}", psh["spokeNet"][k], jsh["spokeNet"][k], dp)
        for i, prow in enumerate(psh["floatWindow"]["curve"]):
            jrow = jsh["floatWindow"]["curve"][i]
            cmp(f"ship0.window[{i}].diaM", prow["diaM"], jrow["diaM"], 1)
            if prow["ratioSL"] is None:
                checked += 1
                if jrow["ratioSL"] is not None:
                    bad.append(f"ship0.window[{i}]: python None, js "
                               f"{jrow['ratioSL']}")
            else:
                cmp(f"ship0.window[{i}].ratioSL", prow["ratioSL"],
                    jrow["ratioSL"], 3)
        for edge in ("loM", "hiM"):
            pv, jv = psh["floatWindow"][edge], jsh["floatWindow"][edge]
            checked += 1
            if (pv is None) != (jv is None) or (pv is not None and pv != jv):
                bad.append(f"ship0.window.{edge}: python {pv}, js {jv}")
        for i, prow in enumerate(psh["floatWindowFrame"]["curve"]):
            jrow = jsh["floatWindowFrame"]["curve"][i]
            if prow["ratioSL"] is None:
                checked += 1
                if jrow["ratioSL"] is not None:
                    bad.append(f"ship0.windowFrame[{i}]: python None, js "
                               f"{jrow['ratioSL']}")
            else:
                cmp(f"ship0.windowFrame[{i}].ratioSL", prow["ratioSL"],
                    jrow["ratioSL"], 3)
        for edge in ("loM", "hiM"):
            pv = psh["floatWindowFrame"][edge]
            jv = jsh["floatWindowFrame"][edge]
            checked += 1
            if (pv is None) != (jv is None) or (pv is not None and pv != jv):
                bad.append(f"ship0.windowFrame.{edge}: python {pv}, js {jv}")
        # THE BAND — the two walls (operator ruling, 08-13 morning): crush at
        # SF exactly 1.0, sink at lift, both altitudes, the largest emergent
        # SF that still floats, the neutral ceiling. Three worlds; missing-key
        # detection both directions like every block above.
        pb, jb = psh.get("band"), jsh.get("band")
        if pb is None or jb is None:
            bad.append("ship0.band: missing on one side — the two walls must "
                       "land in BOTH mirrors in one commit")
        else:
            for wname, prow in pb.items():
                jrow = jb.get(wname)
                if jrow is None:
                    bad.append(f"ship0.band.{wname}: missing from JS")
                    continue
                for k, dp in (("crushT", 1), ("liftSLT", 1), ("lift2500T", 1),
                              ("bandSLT", 1), ("band2500T", 1),
                              ("neutralCeilM", 0)):
                    cmp(f"ship0.band.{wname}.{k}", prow[k], jrow[k], dp)
                psf, jsf = prow["sfFloat"], jrow["sfFloat"]
                if psf is None or jsf is None:
                    checked += 1
                    if (psf is None) != (jsf is None):
                        bad.append(f"ship0.band.{wname}.sfFloat: python "
                                   f"{psf}, js {jsf}")
                else:
                    cmp(f"ship0.band.{wname}.sfFloat", psf, jsf, 3)
            for wname in jb:
                if wname not in pb:
                    bad.append(f"ship0.band.{wname}: present in JS, missing "
                               "from Python")

    if bad:
        print("CELL PARITY FAILED — the page and the analysis disagree:\n")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print(f"cell parity: {checked} values identical across model.js and vacuum-cell.py "
          f"({len(py['materials'])} materials, 3 architectures, 4 ladders, printer chain, "
          f"demonstrator, graded pressure, shapes, ship 0)")


if __name__ == "__main__":
    main()
