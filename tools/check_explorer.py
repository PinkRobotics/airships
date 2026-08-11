#!/usr/bin/env python3
"""The 3D explorer must mount, render every level, and show ONLY the model's numbers.

    python3 tools/check_explorer.py

Same discipline as check_cell_parity.py, one page over: cell/explorer.html is a third
surface displaying the cell physics, and a surface that displays numbers is a surface that
can drift. This drives the page headless, walks all seven levels, and checks that what the
DOM shows equals what cell/model.js computes — through the page's own wiring, not a copy
of it.

It also drives the THREE TOURS, which are a second kind of drift. The connectors, the tube
and the skin all show the same cell and fly between stops on it — five printed joint
families, four cuts, four kinds of face — and their copy comes from two places at once:
cell/model.js for anything physical, and research/geometry/nodes/manifest.json (by way of a
generated module) for anything about the printed joints. So the gate clicks the real
#tourNext button through every stop of every tour and asserts, at each: the camera arrived
at the stop's own target, the panel is showing that stop's block, the label was read back
from the state with the tour's own noun, the surroundings are dimmed in tint RGB (where the
shader can see it) and not in alpha (where it cannot).

Then it takes EVERY data-n and data-s on those levels and resolves it against an
independent recomputation — the manifest regrouped here in Python, the cut schedule
rebuilt here from the article graph, and the model's own returns called again in the page.
A path that resolves in none of them fails: on a toured level there is no such thing as a
figure with no source. Plus the one thing no selector can see — a figure typed into the
prose with no data binding at all — caught by scanning the level's copy for naked digits.
"""
from __future__ import annotations

import json
import math
import pathlib
import subprocess
import sys
import tempfile
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import gen_node_families as GNF  # noqa: E402  (path set above)
import gen_display_meshes as GDM  # noqa: E402

# RAW string. The probe is full of regex escapes — \s, \d, \b — and in a cooked Python
# string \b is a BACKSPACE, which silently turned /\\bE\\d\\b/ into a regex that matched
# nothing and let a typed figure through the naked-digit scan. (It also emitted the
# SyntaxWarning this file used to print on every run.)
PROBE = r"""(() => {
  const out = { errors: window.__errs || [], mounted: !!window.EXPLORER };
  if (!window.EXPLORER) return out;
  const E = window.EXPLORER, C = window.CELL;
  out.levels = [];
  for (let i = 0; i < E.levels.length; i++) {
    E.setLevel(i, true);
    E.tick(0.016);
    const s = E.renderer.stats;
    out.levels.push({ id: E.levels[i].id, draws: s.drawCalls,
                      tris: s.triangles, lines: s.lines });
  }
  // The page's displayed numbers, against the model's own arithmetic.
  const wall = C.rhoAir(2500);
  out.checks = [];
  const shown = (sel) => document.querySelector(sel).textContent.replace(/,/g, '');
  out.checks.push(['wall', shown('[data-n="wallWork"]'), wall.toFixed(4)]);
  const chain = C.printerChain(C.MATERIALS.PAHT_Z).find(r => r.designPoint);
  out.checks.push(['strutM', shown('[data-n="design.strutM"]'),
                   Math.round(chain.strutM * 1000).toString()]);
  const demo = C.demonstrator(C.MATERIALS.PAHT_Z);
  out.checks.push(['demoKg', shown('[data-n="demo.totalKg"]'), demo.totalKg.toFixed(2)]);
  out.checks.push(['demoL', shown('[data-n="demo.enclosedL"]'),
                   demo.enclosedL.toFixed(0)]);
  const sw = C.sharedWall(2.0);
  out.checks.push(['shared', shown('[data-n="sw.sharedFractionPct"]'),
                   sw.sharedFractionPct.toFixed(1)]);
  // The hull length must be the MODEL's, everywhere it appears. A typed 177 survived on
  // this page for a day while the rail said 190 beside it.
  out.checks.push(['hullLen', shown('[data-n="hull.lengthM"]'),
                   E.ctx.hull.lengthM.toFixed(0)]);
  // Scoped, because 177 is now a legitimate figure on this page: the tie cut is 177 mm.
  // The stale value this guards against was a hull LENGTH in metres — '177 m', never
  // '177 mm'. A review predicted this exact collision before the copy was written.
  out.staleHullLength = /177\s*m(?!m)/.test(document.body.textContent);
  // The ladder's decisive row and the material figures the copy quotes.
  const lad = C.ladder(C.MATERIALS.M60J_LAM);
  out.checks.push(['level2', shown('[data-n="level2.total"]'), lad[2].total.toFixed(3)]);
  out.checks.push(['pahtZ', shown('[data-n="paht.zSigmaMPa"]'),
                   (C.MATERIALS.PAHT_Z.sigma / 1e6).toFixed(0)]);
  out.checks.push(['orthoPenalty', shown('[data-n="orthoPenalty"]'),
                   C.ORTHO_PENALTY.toFixed(3)]);
  // The hybrid stock build and the tie-corrected weightless rungs (2026-08-10).
  const st = C.stockBuild();
  out.checks.push(['stockPipeKg', shown('[data-n="stock.pipeKg"]'),
                   st.pipeKg.toFixed(2)]);
  out.checks.push(['stockEulerPinned', shown('[data-n="stock.eulerMarginPinned"]'),
                   st.eulerMarginPinned.toFixed(1)]);
  const wArt = C.weightlessArticle(wall);
  out.checks.push(['wM60rho', shown('[data-n="wM60.densityAtN1"]'),
                   wArt.find(r => r.key === 'M60J_LAM').densityAtN1.toFixed(3)]);
  out.checks.push(['wCFFminN', shown('[data-n="wCFF.minNSeaLevel"]'),
                   wArt.find(r => r.key === 'CFF').minNSeaLevel.toFixed(0)]);
  out.checks.push(['hexSpokes', shown('[data-n="demo.hexSpokeStruts"]'),
                   C.kelvinLatticeCounts(1).hexSpokeStruts.toFixed(0)]);
  // The bending check that governs the article — the page must quote the model's own
  // failure pressure for the UNBRACED rim, which is the whole reason the spokes exist.
  const el = C.filmEdgeLoads(C.demonstrator(C.MATERIALS.PAHT_Z).spanM);
  out.checks.push(['rimBareFails', shown('[data-n="edge.rows.0.failsAtAtm"]'),
                   el.rows[0].failsAtAtm.toFixed(2)]);
  out.checks.push(['bulgeUnbraced', shown('[data-n="edge.bulgeVolumeLostUnbracedPct"]'),
                   el.bulgeVolumeLostUnbracedPct.toFixed(1)]);
  // The page quoted the SIX SQUARES' subtotal as the whole article's load; there are
  // eight hexagons as well. Hold the total to the model.
  out.checks.push(['surfaceLoadTf', shown('[data-n="edge.totalSurfaceLoadTf"]'),
                   el.totalSurfaceLoadTf.toFixed(1)]);
  // The connectors level's model-sourced figures: what the hexagon hub is asked to carry,
  // and the rim SKU the printed socket does not yet match.
  out.checks.push(['hubShare', shown('[data-n="edge.hubShareN"]'),
                   Math.round(el.hubShareN).toLocaleString('en-US').replace(/,/g, '')]);
  out.checks.push(['tripodProp', shown('[data-n="edge.tripodPropN"]'),
                   Math.round(el.tripodPropN).toLocaleString('en-US').replace(/,/g, '')]);
  out.checks.push(['rimFails', shown('[data-n="edge.rows.2.failsAtAtm"]'),
                   el.rows[2].failsAtAtm.toFixed(2)]);
  out.checks.push(['rimCuts', shown('[data-n="stock.rimCuts"]'), st.rimCuts.toFixed(0)]);
  out.checks.push(['rimOd', shown('[data-n="stock.rimOdM"]'),
                   (st.rimOdM * 1000).toFixed(0)]);
  // The rim SKU and the joint's single pipe diameter are the contradiction two cards state
  // out loud — the corner that would receive that tube, and the cut that would be it.
  // While they disagree, both must carry the note; the day the generator takes a diameter
  // per member kind, both have to go.
  out.rimSkuNotes = ['section[data-level="strut"] [data-stop="rimVertex-7"] .note',
    'section[data-level="wall"] [data-stop="rimLong"] .note']
    .filter(q => document.querySelector(q)).length;
  // THE PARTS VIEW (2026-08-10). The level loop above only ever runs the default mode, so
  // a view that renders an empty canvas would be invisible to it. Drive the real button.
  // ...and it must be driven ON THE CELL LEVEL. The loop above ends on the hull, where
  // the button is not even shown; cycling there measured the hull's line count (1,165)
  // against the cell's member count and failed, correctly.
  E.setLevel(E.levels.findIndex(l => l.id === 'cell'), true);
  E.tick(0.016);
  const btn = document.getElementById('toggleParts');
  const seq = [];
  for (let i = 0; i < 3; i++) { btn.click(); seq.push(E.state.partsMode); E.tick(0.016);
    out.parts = out.parts || [];
    out.parts.push([E.renderer.stats.drawCalls, E.renderer.stats.triangles]);
    if (E.state.partsMode === 'joinery') out.ghostLines = E.renderer.stats.lines - 36; }
  out.partsCycle = seq.join(',');
  // Every pipe-family member must leave a ghost behind when it is hidden, or the joinery
  // view quietly loses part of the article. Counted from the model, never typed.
  const kc = C.kelvinLatticeCounts(1);
  out.ghostExpected = kc.struts + kc.rimStrutEquivalents + kc.hexSpokeStruts +
    kc.tieStruts + kc.hexTieStruts;
  out.partsLabel = btn.textContent;
  // The frame with everything back on, at the cell level: the baseline the connector
  // tour's print-resolution swap is measured against, stop by stop, below.
  E.tick(0.016);
  out.cellBaseTris = E.renderer.stats.triangles;
  // EVERY MEMBER-END MUST BE DRAWN WITH A RECEIVER. This gate did not exist, and its
  // absence let the 36 rim members render as pipes butting into a bare ball for weeks —
  // the builder even carried a comment saying "a rim arm, even though it draws no socket
  // cone". The designer caught it twice by eye and nothing here could confirm or deny him:
  // ghost centrelines counted MEMBERS, DOM figures counted NUMBERS, and no check ever
  // counted connector geometry. A member family that loses its joints must fail the build.
  // Counted through the page's OWN accessor, not a second tree walk: a probe that walks the
  // scene differently from the renderer can agree with itself and disagree with the screen.
  // THE NET MUST BE CUTTABLE. The designer laser-cuts this pattern, folds it around the
  // tube frame and tapes it closed, so "it animated nicely" is not the property that matters.
  // Drive the real button, run it to the end, and assert on the geometry that results: every
  // face coplanar with the root (a FOLD, not a projection), total flat area equal to the
  // model's own surface, and NO TWO FACES OVERLAPPING — an overlapping net cannot be cut and
  // looks perfectly fine on screen.
  E.setLevel(E.levels.findIndex(l => l.id === 'track'), true);
  E.tick(0.016);
  out.unfoldTrisShut = E.renderer.stats.triangles;
  document.getElementById('toggleUnfold').click();
  for (let i = 0; i < 300 && E.state.unfold < 0.999; i++) E.tick(0.05);
  out.net = E.netStats();
  // AND THE FRAME MUST ACTUALLY CHANGE. The gate asserted every property of the pattern —
  // flat, right area, no overlaps — and nothing about whether it could be SEEN, so it passed
  // with full confidence while the feature was invisible in a browser twice running: once
  // because the sheet sat edge-on, and once because stepUnfold lived only in api.tick(), which
  // the gate calls and the page's requestAnimationFrame loop does not. Measure the drawn frame
  // before and after, and drive it through the same advance() the real loop uses.
  out.unfoldTrisOpen = E.renderer.stats.triangles;
  out.netModelAreaM2 = C.kelvinFaces(E.ctx.demo.spanM).areaM2;
  document.getElementById('toggleUnfold').click();
  // Tick it fully shut. The ease takes 1.6 s of animation time and the tour walk below shares
  // this cell — leaving it half-open blanked every stop on the skin level.
  for (let i = 0; i < 300 && E.state.unfold > 0.001; i++) E.tick(0.05);
  // EVERY JOINT MUST BE DRAWN AS ITS GENERATED MESH — the successor to the receiver count.
  // The receivers used to be lathed cones, and a member family losing its joints was the
  // defect the count existed for; the joints are now the generator's own meshes, one scene
  // node per joint, so the honest count is joints against the manifest and pipe instances
  // against the cut schedule. Counted through the page's OWN accessor, as ever.
  const ik = E.instanceKeys();
  out.jointsDrawn = ik.filter(k => /^Joint_/.test(k)).length;
  out.repsDrawn = ik.filter(k => /^RepJoint_/.test(k)).length;
  out.pipesDrawn = ik.filter(k => /^Pipes_/.test(k) || k === 'HeroStrut#0').length;
  // Which cut group every drawn member landed in — the Python holds this to the generated
  // schedule's own counts, so a member that matches no group (and silently drew nothing)
  // is a failure with a name.
  out.memberGroups = {};
  for (const m of E.members) {
    const g = m.group || 'UNGROUPED';
    out.memberGroups[g] = (out.memberGroups[g] || 0) + 1;
  }
  // The breach table must not contradict the sentence above it: at the level-2 target,
  // every contingency row through L=3 floats.
  out.breachAllFloat =
    document.querySelectorAll('[data-t="breach"] tr').length >= 4 &&
    document.querySelectorAll('[data-t="breach"] .fail').length === 0;
  out.rail = document.querySelectorAll('#rail button').length;
  out.sections = document.querySelectorAll('#panel section').length;

  // THE PART TOURS (2026-08-11). A level can hold a list of stops and fly between them.
  // Everything below is driven through the real #tourNext button for the same reason the
  // parts view is: a control the probe cannot click is a control no gate covers.
  const levelFigs = (lid) => {
    // EVERY figure on this level, with the formatting the page applied, so the Python can
    // resolve each one against an independent source. Not filtered by prefix any more:
    // the tube and skin levels mix generated node data with model.js physics, and a filter
    // is exactly how a figure ends up with nothing checking it.
    const num = [], str = [];
    const sec = `#panel section[data-level="${lid}"]`;
    for (const el of document.querySelectorAll(`${sec} [data-n]`)) {
      num.push([el.dataset.n, el.dataset.mm ? 1 : 0,
                el.dataset.mul ? +el.dataset.mul : 1,
                el.dataset.f !== undefined ? +el.dataset.f : 0,
                el.textContent.replace(/,/g, '')]);
    }
    for (const el of document.querySelectorAll(`${sec} [data-s]`)) {
      str.push([el.dataset.s, el.textContent]);
    }
    return { num, str };
  };
  // THE MODEL, CALLED AGAIN. Not read off E.ctx — that is the page's own copy and checking
  // it against itself proves nothing. These are fresh calls to the same exported
  // functions, which is what every hand-written check above does, in bulk.
  {
    const paht = C.MATERIALS.PAHT_Z;
    const span = C.demonstrator(paht).spanM;
    const ladRef = C.ladder(C.MATERIALS.M60J_LAM);
    out.model = {
      stock: C.stockBuild(), edge: C.filmEdgeLoads(span),
      demo: C.demonstrator(paht), design: C.printerChain(paht).find(r => r.designPoint),
      ladRef, tRef: C.tubeStrut(C.MATERIALS.M60J_LAM),
      orthoPenalty: C.ORTHO_PENALTY, padDiaMm: C.PAD_R_M * 2000,
      tubeMat: C.MATERIALS.T700_LAM.name, tubeRho: C.MATERIALS.T700_LAM.rho,
      level1: { total: ladRef[1].total }, level2: { total: ladRef[2].total,
        margin: C.rhoAir(2500) / ladRef[2].total },
      paht: { zSigmaMPa: paht.sigma / 1e6, zEGPa: paht.E / 1e9,
              xySigmaMPa: C.MATERIALS.PAHT_XY.sigma / 1e6,
              xyEGPa: C.MATERIALS.PAHT_XY.E / 1e9 },
    };
    // THE MEMBRANE, recomputed the way the page composes it — through barrierKgPerM2 with
    // its own constants overridden, never a transcription of the closure inside
    // filmEdgeLoads. If the page's composition drifts, these stop agreeing.
    const f = C.kelvinFaces(span);
    const el2 = out.model.edge;
    const panel = (fr) => 2 * fr * f.edgeM;
    const T = (pp) => C.barrierKgPerM2(pp, { rhoF: 1, sigmaF: 1, sf: 1, eff: 1 });
    const th = (pp) => C.barrierKgPerM2(pp, { rhoF: 1 });
    const rB = (pp) => 2 * T(pp) / C.P_ATM;
    const dep = (pp) => rB(pp) - Math.sqrt(rB(pp) ** 2 - (pp / 2) ** 2);
    const hexP = panel(C.PANEL.hexSpoked), sqP = panel(C.PANEL.squareSpoked);
    const bareP = panel(C.PANEL.hexUnbraced);
    const sinA = (hexP / 2) / rB(hexP);
    out.model.skin = {
      hexM2: f.hexM2, sqM2: f.sqM2, areaM2: f.areaM2,
      hexTotalM2: 8 * f.hexM2, sqTotalM2: 6 * f.sqM2,
      hexSharePct: 100 * 8 * f.hexM2 / f.areaM2,
      hexPanelMm: hexP * 1000, sqPanelMm: sqP * 1000, barePanelMm: bareP * 1000,
      hexArealGM2: C.barrierKgPerM2(hexP) * 1000, sqArealGM2: C.barrierKgPerM2(sqP) * 1000,
      hexThicknessUm: th(hexP) * 1e6, sqThicknessUm: th(sqP) * 1e6,
      hexFilmG: 8 * f.hexM2 * C.barrierKgPerM2(hexP) * 1000,
      sqFilmG: 6 * f.sqM2 * C.barrierKgPerM2(sqP) * 1000,
      filmG: C.filmKg(span) * 1000,
      tensionHex: T(hexP), tensionSq: T(sqP), tensionBare: T(bareP),
      sinAlpha: sinA, alphaDeg: Math.asin(sinA) * 180 / Math.PI,
      allowMPa: T(hexP) / th(hexP) / 1e6, bulgeFrac: dep(hexP) / (hexP / 2),
      dihedralDeg: Math.acos(-1 / 3) * 180 / Math.PI,
      wBare: el2.rows[0].lineLoadNPerM, wRim: el2.rows[1].lineLoadNPerM,
      wSpoke: el2.rows[3].lineLoadNPerM, wSqTie: el2.rows[5].lineLoadNPerM,
      doublingX: el2.rows[1].lineLoadNPerM / el2.rows[3].lineLoadNPerM,
      bulgeHexMm: dep(hexP) * 1000, bulgeSqMm: dep(sqP) * 1000,
      bulgeBareMm: dep(bareP) * 1000,
      bulgeLostL: el2.bulgeVolumeLostPct / 100 * out.model.stock.enclosedL,
      padCollectsN: Math.PI * (C.PAD_R_M * 2) * T(hexP) * sinA,
      padNeedsDiaMm: 1000 * el2.hubShareN / (Math.PI * T(hexP) * sinA),
    };
  }
  // The article's own member list, as drawn, so the Python can check that the cut schedule
  // prices the members the page put on the screen and no others.
  out.memberKinds = {};
  for (const m of E.members) out.memberKinds[m.kind] = (out.memberKinds[m.kind] || 0) + 1;
  out.tours = [];
  for (let i = 0; i < E.levels.length; i++) {
    const t = E.tourFor(i);
    if (!t) continue;
    const lid = E.levels[i].id;
    E.setLevel(i, true);
    E.tick(0.016);
    const btn = document.getElementById('tourNext');
    const sel = (q) => [...document.querySelectorAll(
      `#panel section[data-level="${lid}"] ${q}`)].map(e => e.dataset.stop);
    const rec = {
      id: lid, shown: btn.style.display !== 'none', noun: t.noun,
      keys: t.stops.map(s => s.key),
      names: t.stops.map(s => s.name),
      targets: t.stops.map(s => s.target.slice()),
      radii: t.stops.map(s => s.radius),
      subjects: t.stops.map(s => s.subject.size),
      panel: sel('[data-stop]'),
      walk: [],
    };
    const everything = E.instanceKeys();
    // stops+1 clicks: every stop once, and the wrap back onto the first.
    for (let k = 0; k <= t.stops.length; k++) {
      btn.click();
      E.tick(0.016);
      const s = E.renderer.stats;
      const cur = t.stops[E.state.tourIdx];
      const one = [...cur.subject][0].split('#');
      // A NON-SUBJECT instance, found rather than assumed: the tube and skin levels light
      // whole runs of tube, so no fixed id is reliably outside the subject any more. If a
      // stop somehow lit everything there would be nothing to find, and the Python's
      // "not dimmed" branch is the right complaint — so hand it a null rather than throw.
      const offKey = everything.find(k2 => !cur.subject.has(k2));
      rec.walk.push({
        stop: E.state.tourStop, idx: E.state.tourIdx, label: btn.textContent,
        target: E.cam.target.slice(), dist: E.cam.distance,
        draws: s.drawCalls, tris: s.triangles,
        on: sel('[data-stop].on'),
        // The dim must land in RGB: a pipe is opaque, so a dim written into tint ALPHA is
        // discarded by the solid pass while a probe reading the array back reports success.
        offTint: offKey ? E.tintAt(offKey.split('#')[0],
          +offKey.split('#')[1]) : null,
        onTint: E.tintAt(one[0], +one[1]),
      });
    }
    rec.figs = levelFigs(lid);
    // The contradiction notes. While the model puts the rim on a bigger tube than every
    // printed socket is grown for, BOTH places that name that tube have to say so.
    rec.notes = [...document.querySelectorAll(
      `#panel section[data-level="${lid}"] [data-stop] .note`)].map(e => e.closest(
        '[data-stop]').dataset.stop);
    // NAKED DIGITS. Strip every data-bound span out of a copy of this level's panel and
    // look at the digits that are left. A hand-typed figure has no selector, so nothing
    // above can see it — this is the only check that catches "17.75 g" written into the
    // prose, which is precisely the failure this repository keeps finding. The allowlist
    // is four patterns and each one is a name, not a measurement:
    //   <110>      Miller indices — a direction, not a quantity
    //   E5         experiment ids from the test plan
    //   10 MPa     the adhesive allowable the manifest's own field name carries
    //              (glueMarginAt10MPa); it is an assumption, and it is named as one
    //   [0/±45/90] a ply schedule — the angles ARE the specification's name
    // A [data-t] table body goes too, but for a different reason: those are written by
    // fillTables out of ctx and nothing else, so every digit in one already came from the
    // model. Anything typed inside such a table would be typed into the page's script,
    // where it is at least in code the reader of this gate can find.
    const copy = document.querySelector(`#panel section[data-level="${lid}"]`)
      .cloneNode(true);
    for (const el of copy.querySelectorAll('[data-n],[data-s],[data-t]')) el.remove();
    let txt = copy.textContent;
    for (const re of [/⟨\d+⟩/g, /\bE\d\b/g, /10 MPa/g, /\[0\/(±45\/)?90\]/g]) {
      txt = txt.replace(re, '');
    }
    rec.naked = txt.match(/\d[\d.,]*/g) || [];
    out.tours.push(rec);
  }
  // THE STAGE HOLDS STILL. Two levels now display the same scene graph, so the dive
  // between them must not cross-fade it. `?still=1` snaps every move, so the animated path
  // is driven here by turning reduced motion off for the length of one dive — otherwise
  // the only code path a gate ever sees is the one that skips the interpolation.
  {
    const ci = E.levels.findIndex(l => l.id === 'cell');
    const si = E.levels.findIndex(l => l.id === 'strut');
    E.setLevel(ci, true); E.tick(0.016);
    E.state.reduced = false;
    E.setLevel(si);
    out.stageDive = [];
    for (let f = 0; f < 10; f++) {
      E.tick(0.15);
      const s = E.renderer.stats;
      out.stageDive.push([E.stageFade, s.drawCalls, s.triangles]);
    }
    E.state.reduced = true;
  }
  // The page's OWN arm histogram, counted off the joints it drew. Held to the manifest of
  // the 51 STLs, so the explorer cannot tour parts that are not the parts we print.
  out.hist = {};
  out.memberEnds = 0;
  for (const p of E.parts) {
    const k = `${p.role}-${p.arms}`;
    out.hist[k] = (out.hist[k] || 0) + 1;
    out.memberEnds += p.arms;
  }
  out.partCount = E.parts.length;
  // Back on the level that OWNS the cell. Two separate things are proven here, and they
  // were one before the page started opening on a structural reading:
  //   1. the DEFAULT GROUP survives the walk through the tours — a tour owns the dim on its
  //      own level, and must hand it back rather than leave the cell showing everything;
  //   2. clearing the group puts every tint back to 1 — a dim that never undims leaves the
  //      cell level grey, which is the original bug this assertion was written for.
  E.setLevel(E.levels.findIndex(l => l.id === 'cell'), true);
  E.tick(0.016);
  out.defaultGroup = E.group;
  // A member that reaches the centre joint against one that does not — read off the page's
  // own records, because which instance index is lit depends on the build order.
  {
    const lit = E.members.find(m => m.keys.includes('0,0,0'));
    const dim = E.members.find(m => !m.keys.includes('0,0,0'));
    out.groupLit = lit ? E.tintAt(lit.inst[0][0], lit.inst[0][1]) : null;
    out.groupDim = dim ? E.tintAt(dim.inst[0][0], dim.inst[0][1]) : null;
    out.groupLitCount = E.members.filter(m => m.keys.includes('0,0,0')).length;
  }
  E.setGroup('all');
  E.tick(0.016);
  out.clearedTint = E.tintAt('Joint_00', 0);
  out.clearedFrame = [E.renderer.stats.drawCalls, E.renderer.stats.triangles];
  return out;
})()"""


def dig(obj, path):
    """The page's data-n resolver, in Python — including its array indexing.

    edge.rows.0.failsAtAtm works in the browser because a JS array takes a string subscript.
    A Python list does not, so a digit part indexes; anything else is a key."""
    for part in path.split("."):
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def cut_schedule(groups, stock, mat_rho):
    """The purchased schedule, rebuilt here from the two authorities the page composes.

    Deliberately not a translation of cell/explorer.js: the group counts and deductions
    come from the article graph and the manifest (through gen_node_families, which regroups
    them from scratch), and the lengths, diameters and density come from the model as the
    page's own probe read them back. If either side moves, this stops agreeing.
    """
    wall = (stock["odM"] - stock["idM"]) / 2
    sku = {"main": (stock["odM"], stock["idM"]),
           "rim": (stock["rimOdM"], stock["rimOdM"] - 2 * wall)}
    length = {"long": stock["pipeCutM"], "short": stock["shortCutM"]}
    out = {"kerfMm": KERF_MM, "stockLenM": STOCK_LEN_M,
           "order": groups["order"], "groups": {}, "skus": {},
           "members": groups["members"]}
    for key in groups["order"]:
        g = dict(groups["groups"][key])
        od, idd = sku[g["sku"]]
        section = math.pi * ((od / 2) ** 2 - (idd / 2) ** 2)
        kg_per_m = section * mat_rho
        member_mm = length[g["lengthKey"]] * 1000
        cut_mm = member_mm - g["deductMm"]
        g.update(memberMm=member_mm, cutMm=cut_mm, kgPerM=kg_per_m,
                 odMm=od * 1000, idMm=idd * 1000, wallMm=(od - idd) / 2 * 1000,
                 sectionMm2=section * 1e6,
                 cutM=cut_mm * g["count"] / 1000, memberM=member_mm * g["count"] / 1000,
                 cutKg=kg_per_m * cut_mm * g["count"] / 1000,
                 memberKg=kg_per_m * member_mm * g["count"] / 1000)
        out["groups"][key] = g
    allg = [out["groups"][k] for k in groups["order"]]
    for s in ("main", "rim"):
        gs = [g for g in allg if g["sku"] == s]
        out["skus"][s] = {
            "odMm": gs[0]["odMm"], "idMm": gs[0]["idMm"], "wallMm": gs[0]["wallMm"],
            "sectionMm2": gs[0]["sectionMm2"], "kgPerM": gs[0]["kgPerM"],
            "rOverT": (gs[0]["odMm"] / 2) / gs[0]["wallMm"],
            "cuts": sum(g["count"] for g in gs),
            "cutM": sum(g["cutM"] for g in gs),
            "sticks": pack_sticks(gs),
            "sticksUnmixed": sum(-(-g["count"] // int(STOCK_LEN_M * 1000
                                                      // (g["cutMm"] + KERF_MM)))
                                 for g in gs),
        }
    sticks = out["skus"]["main"]["sticks"] + out["skus"]["rim"]["sticks"]
    cut_m = sum(g["cutM"] for g in allg)
    member_m = sum(g["memberM"] for g in allg)
    ref = out["groups"][groups["order"][0]]
    out.update(
        lengths=len({f"{g['cutMm']:.2f}" for g in allg}),
        cutM=cut_m, memberM=member_m, insideJointsM=member_m - cut_m,
        cutKg=sum(g["cutKg"] for g in allg), memberKg=sum(g["memberKg"] for g in allg),
        sticks=sticks, purchasedM=sticks * STOCK_LEN_M,
        sticksUnmixed=out["skus"]["main"]["sticksUnmixed"]
        + out["skus"]["rim"]["sticksUnmixed"],
        purchasedKg=out["skus"]["main"]["sticks"] * STOCK_LEN_M
        * out["skus"]["main"]["kgPerM"]
        + out["skus"]["rim"]["sticks"] * STOCK_LEN_M * out["skus"]["rim"]["kgPerM"],
        offcutPct=100 * (1 - cut_m / (sticks * STOCK_LEN_M)),
        freeLenMm=ref["cutMm"],
        eulerFreeX=stock["eulerMarginPinned"] * (ref["memberMm"] / ref["cutMm"]) ** 2,
        eulerFreeGainX=(ref["memberMm"] / ref["cutMm"]) ** 2,
    )
    return out


# The page's two declared choices, restated here rather than imported: a gate that reads
# its expected values out of the thing it is checking is not a gate. If the kerf or the
# stock length moves in cell/explorer.js, the stick count stops matching and somebody has
# to come here and agree with it on purpose.
KERF_MM = 2.0
STOCK_LEN_M = 2.0


def pack_sticks(groups, stock_mm=None, kerf_mm=None):
    """First-fit decreasing, one kerf per piece — the same rule, written independently."""
    stock_mm = STOCK_LEN_M * 1000 if stock_mm is None else stock_mm
    kerf_mm = KERF_MM if kerf_mm is None else kerf_mm
    items = sorted((g["cutMm"] for g in groups for _ in range(g["count"])), reverse=True)
    left: list[float] = []
    for it in items:
        for i, rem in enumerate(left):
            if rem >= it + kerf_mm:
                left[i] = rem - (it + kerf_mm)
                break
        else:
            left.append(stock_mm - (it + kerf_mm))
    return len(left)


def shown_as(v, digits):
    """What toLocaleString('en-US') would print, minus the commas the probe strips.

    Half-up, because that is what the browser does; Python's own round() is half-even and
    would disagree with the page on a figure that lands exactly on a half."""
    q = Decimal(1).scaleb(-digits)
    return str(Decimal(repr(float(v))).quantize(q, rounding=ROUND_HALF_UP))


def main() -> None:
    # The manifest, regrouped here, is the authority the page's node figures answer to.
    fresh = GNF.payload()
    generated = {"fam": fresh["families"], "nodes": fresh["totals"], "joint": fresh["joint"]}
    manifest = json.loads(GNF.MANIFEST.read_text())
    # The display-mesh module: what the page draws its joints from. Its own gate
    # (gen_display_meshes --check, in `make nodescheck`) holds it to its sources; here it
    # is the expectation the drawn frame is measured against, so a stale module must stop
    # the comparison rather than agree with the page about the wrong thing.
    if not GDM.OUT.exists() or GDM.parse_module()["meta"]["sourceHash"] != GDM.source_hash():
        sys.exit("check_explorer: cell/nodemeshes.generated.js is missing or stale — run "
                 "`python3 tools/gen_display_meshes.py`, then `make stamp`.")
    meshes = GDM.parse_module()

    with tempfile.TemporaryDirectory(dir=str(pathlib.Path.home() / "tmp")) as td:
        probe = pathlib.Path(td) / "probe.js"
        probe.write_text(PROBE)
        out = pathlib.Path(td) / "out.json"
        srv = subprocess.Popen([sys.executable, str(ROOT / "tools" / "serve.py"),
                                "--port", "8909", "--quiet"], cwd=ROOT)
        try:
            subprocess.run([sys.executable, str(ROOT / "tools" / "js_eval.py"),
                            "http://127.0.0.1:8909/cell/explorer.html?still=1",
                            str(probe), str(out), "10"], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            res = json.loads(out.read_text())
        finally:
            srv.terminate()
            srv.wait()

    bad = []
    if res.get("errors"):
        bad += [f"page error: {e}" for e in res["errors"]]
    if not res.get("mounted"):
        bad.append("EXPLORER did not mount (WebGL2 missing in the test browser?)")
    for lv in res.get("levels", []):
        if lv["draws"] < 3 or lv["tris"] <= 0:
            bad.append(f"level {lv['id']}: nearly empty frame "
                       f"({lv['draws']} draws, {lv['tris']} tris)")
    for name, got, want in res.get("checks", []):
        if got != want:
            bad.append(f"displayed {name}: page shows {got!r}, model computes {want!r}")
    if res.get("staleHullLength"):
        bad.append("the page still says '177' somewhere — the hull length must come from "
                   "the model")
    if res.get("breachAllFloat") is False:
        bad.append("breach table shows a failing row at the level-2 target — the table "
                   "contradicts the resilience claim above it")
    # The parts view must actually cycle, keep drawing, and tell the truth on its label.
    if res.get("partsCycle") != "joinery,pipes,all":
        bad.append(f"parts button cycled {res.get('partsCycle')!r}, expected "
                   "'joinery,pipes,all'")
    for i, (draws, tris) in enumerate(res.get("parts") or []):
        if draws < 3 or tris <= 0:
            bad.append(f"parts mode {i}: nearly empty frame ({draws} draws, {tris} tris)")
    if res.get("ghostLines") != res.get("ghostExpected"):
        bad.append(f"joinery view ghosts {res.get('ghostLines')} pipe centrelines, but the "
                   f"model counts {res.get('ghostExpected')} members in the pipe family")
    net = res.get("net") or {}
    if (net.get("u") or 0) < 0.999:
        bad.append(f"the net only reached u={net.get('u')} — it never opened")
    if (net.get("thicknessMm") or 99) > 0.01:
        bad.append(f"the unfolded net stands {net.get('thicknessMm'):.4f} mm out of plane — "
                   "it is a projection, not a fold")
    if abs((net.get("areaM2") or 0) - (res.get("netModelAreaM2") or 1)) > 1e-6:
        bad.append(f"net area {net.get('areaM2')} m2 against the model's "
                   f"{res.get('netModelAreaM2')} m2 — the pattern is not the cell's surface")
    if (res.get("unfoldTrisOpen") or 0) >= (res.get("unfoldTrisShut") or 0):
        bad.append(
            f"unfolding did not change the frame — {res.get('unfoldTrisShut')} triangles shut, "
            f"{res.get('unfoldTrisOpen')} open. The cell should hide and leave the net, so a "
            "frame that does not move means the animation is not reaching the renderer")
    if (res.get("unfoldTrisOpen") or 0) < 24:
        bad.append(f"only {res.get('unfoldTrisOpen')} triangles with the net open — the sheet "
                   "is not being drawn at all")
    if net.get("overlaps"):
        bad.append(f"{net.get('overlaps')} pairs of faces OVERLAP in the flat net — this "
                   "pattern cannot be cut, and nothing on screen would show it")
    if (net.get("folds"), net.get("cuts")) != (13, 23):
        bad.append(f"net has {net.get('folds')} folds and {net.get('cuts')} cuts, "
                   "expected 13 and 23 across the 36 edges")
    # THE JOINTS ARE MESHES NOW, so the receiver count's job — a member family drawn with
    # no joint on it, the way the rim went for weeks — is done by counting drawn joint
    # meshes against the manifest and drawn pipe instances against the cut schedule. Both
    # counted through the page's own accessors, both against generated authorities.
    if res.get("jointsDrawn") != len(manifest["nodes"]):
        bad.append(f"the cell draws {res.get('jointsDrawn')} joint meshes for the "
                   f"manifest's {len(manifest['nodes'])} printed joints")
    if res.get("repsDrawn") != len(meshes["reps"]):
        bad.append(f"{res.get('repsDrawn')} print-resolution representatives drawn, the "
                   f"display module carries {len(meshes['reps'])}")
    want_groups = {k: g["count"] for k, g in fresh["cuts"]["groups"].items()}
    if res.get("memberGroups") != want_groups:
        bad.append(f"drawn members land in cut groups {res.get('memberGroups')}, the "
                   f"schedule cuts {want_groups} — an UNGROUPED member drew no pipe at all")
    if res.get("pipesDrawn") != sum(want_groups.values()):
        bad.append(f"{res.get('pipesDrawn')} pipe instances drawn for "
                   f"{sum(want_groups.values())} members in the schedule")
    # THE PRINT-RESOLUTION SWAP MUST REACH THE FRAME. Each connector stop must draw
    # exactly its family's print mesh in place of the display mesh — asserted as triangle
    # arithmetic on the rendered frame, because this page has now shipped three visual
    # features that were verified by their state and invisible on screen.
    disp_by_file = {r["file"]: r for r in meshes["nodes"]}
    strut_walk = next((t for t in res.get("tours", []) if t["id"] == "strut"), None)
    base_tris = res.get("cellBaseTris") or 0
    if strut_walk:
        for w in strut_walk["walk"]:
            rep = meshes["reps"].get(w["stop"])
            if rep is None:
                bad.append(f"connector stop {w['stop']!r} has no print-resolution mesh")
                continue
            want = rep["tris"] - disp_by_file[rep["file"]]["tris"]
            got = w["tris"] - base_tris
            if got != want:
                bad.append(
                    f"connector stop {w['stop']}: frame moved {got:+d} triangles against "
                    f"the cell baseline, the swap to {rep['file']} should move {want:+d} — "
                    "the print-resolution mesh is not what is on screen")
    if res.get("partsLabel") != "parts: all":
        bad.append(f"parts button label {res.get('partsLabel')!r} after a full cycle — "
                   "the label must be read back from the state, not assumed")
    if res.get("rail") != len(res.get("levels", [])):
        bad.append(f"rail has {res.get('rail')} buttons for {len(res.get('levels', []))} levels")
    if res.get("sections") != len(res.get("levels", [])):
        bad.append(f"panel has {res.get('sections')} sections for "
                   f"{len(res.get('levels', []))} levels")

    # ---- the part tours -------------------------------------------------------------
    # The generated module must be current with the manifest first: everything below
    # compares the page against the manifest, and a stale module would make both wrong in
    # the same direction and the comparison would pass.
    if not GNF.OUT.exists() or GNF.OUT.read_text() != GNF.render(fresh):
        bad.append("cell/nodes.generated.js has drifted from "
                   "research/geometry/nodes/manifest.json — run "
                   "`python3 tools/gen_node_families.py`, then `make stamp`")
    # THE AUTHORITY every figure on a toured level answers to. Three independent sources,
    # merged: the manifest regrouped here, the cut schedule rebuilt here from the article
    # graph and the model's own numbers, and the model called again inside the page. A
    # data-n path that resolves in none of them is a figure with no source, which is the
    # thing this level of the page is not allowed to contain.
    model = res.get("model") or {}
    expected = dict(generated)
    expected.update(model)
    if model.get("stock"):
        expected["cuts"] = cut_schedule(fresh["cuts"], model["stock"], model["tubeRho"])
        # The one dimension the page DERIVES rather than reads: the rim SKU's bore, taken
        # as "the same wall as the other SKU". If that ever stops being true the mass on
        # the full member length would not come back to the model's own pipeKg.
        c2c = expected["cuts"]["memberKg"]
        if abs(c2c - model["stock"]["pipeKg"]) > 1e-9:
            bad.append(f"the cut schedule prices the members at {c2c:.6f} kg centre to "
                       f"centre, the model charges {model['stock']['pipeKg']:.6f} — the "
                       "derived rim bore no longer matches the section the model uses")
    # The schedule may only price members the page actually drew.
    want_kinds = fresh["totals"]["graph"]
    if res.get("memberKinds") != want_kinds:
        bad.append(f"the page draws members {res.get('memberKinds')}, the article graph "
                   f"has {want_kinds}")
    priced = sum(g["count"] for g in fresh["cuts"]["groups"].values())
    if priced != sum(want_kinds.values()):
        bad.append(f"the cut schedule prices {priced} members of {sum(want_kinds.values())}")
    want_hist = Counter(f"{n['role']}-{n['arms']}" for n in manifest["nodes"])
    got_hist = Counter(res.get("hist") or {})
    if got_hist != want_hist:
        bad.append(f"the page draws joints {dict(sorted(got_hist.items()))}, the manifest "
                   f"prints {dict(sorted(want_hist.items()))} — the explorer's joinery has "
                   "drifted from the 51 STLs on disk")
    if res.get("partCount") != len(manifest["nodes"]):
        bad.append(f"the page drew {res.get('partCount')} joints, the manifest has "
                   f"{len(manifest['nodes'])}")
    want_ends = sum(n["arms"] for n in manifest["nodes"])
    if res.get("memberEnds") != want_ends:
        bad.append(f"the page counts {res.get('memberEnds')} member-ends, the manifest "
                   f"counts {want_ends}")
    if not res.get("tours"):
        bad.append("no level declares a tour — the connectors level must walk the five "
                   "printed joint families")
    for t in res.get("tours") or []:
        lid, keys, names = t["id"], t["keys"], t["names"]
        if not t["shown"]:
            bad.append(f"{lid}: #tourNext is hidden on a level that has a tour")
        for k, n in zip(keys, t["subjects"]):
            if not n:
                bad.append(f"{lid}/{k}: the stop lights nothing — a stop with an empty "
                           "subject dims the whole article and points at no part of it")
        # A CUT TOUR MUST ACCOUNT FOR EVERY MEMBER. Each stop lights exactly the members
        # its generated group prices — one instance each — so the subject sizes are the
        # group counts and they sum to the whole article. A member whose two seat depths
        # matched no group would be silently unlit and unpriced, and nothing else here
        # would notice: the kind histogram would still be right.
        if t["noun"] == "cut":
            want = [fresh["cuts"]["groups"][k]["count"] for k in keys]
            if t["subjects"] != want:
                bad.append(f"{lid}: the cuts light {t['subjects']} members, the schedule "
                           f"prices {want}")
            if sum(t["subjects"]) != fresh["cuts"]["members"]:
                bad.append(f"{lid}: the cuts light {sum(t['subjects'])} of "
                           f"{fresh['cuts']['members']} members — some member is cut to a "
                           "length no stop shows")
        if t["panel"] != keys:
            bad.append(f"{lid}: the panel's stop blocks are {t['panel']}, the tour's stops "
                       f"are {keys} — every stop needs its copy and no copy may be orphaned")
        # stops+1 clicks starting at stop 0 visit 1..n-1, 0, 1: the cycle and the wrap.
        want_cycle = [keys[(k + 1) % len(keys)] for k in range(len(keys) + 1)]
        got_cycle = [w["stop"] for w in t["walk"]]
        if got_cycle != want_cycle:
            bad.append(f"{lid}: the tour cycled {got_cycle}, expected {want_cycle}")
        seen_targets = []
        for w in t["walk"]:
            if w["stop"] not in keys:
                continue
            i = keys.index(w["stop"])
            want_label = f"{t['noun']}: {names[i]}"
            if w["label"] != want_label:
                bad.append(f"{lid}/{w['stop']}: button says {w['label']!r}, the state says "
                           f"{want_label!r} — the label, noun included, must be read back "
                           "from the state")
            if w["draws"] < 3 or w["tris"] <= 0:
                bad.append(f"{lid}/{w['stop']}: nearly empty frame "
                           f"({w['draws']} draws, {w['tris']} tris)")
            # The camera must actually go there. A tour that relabels and dims but never
            # moves would otherwise pass green.
            d = max(abs(a - b) for a, b in zip(w["target"], t["targets"][i]))
            if d > 1e-9:
                bad.append(f"{lid}/{w['stop']}: camera target {w['target']} is {d:.2e} m "
                           f"from the stop's own target {t['targets'][i]}")
            if seen_targets and w["target"] == seen_targets[-1]:
                bad.append(f"{lid}/{w['stop']}: the camera did not move from the last stop")
            seen_targets.append(w["target"])
            if w["on"] != [w["stop"]]:
                bad.append(f"{lid}/{w['stop']}: the panel shows {w['on']}, not just this "
                           "stop's block")
            off, on = w["offTint"], w["onTint"]
            if not off or not (off[0] < 0.9 and off[1] < 0.9 and off[2] < 0.9):
                bad.append(f"{lid}/{w['stop']}: a non-subject instance has tint RGB {off} — "
                           "the surroundings are not dimmed")
            if not off or abs(off[3] - 1) > 1e-6:
                bad.append(f"{lid}/{w['stop']}: the dim is in tint ALPHA ({off}), which the "
                           "opaque pass discards — dim by scaling RGB")
            if not on or min(on[:3]) < 0.999:
                bad.append(f"{lid}/{w['stop']}: the subject's own instances are dimmed "
                           f"({on}) — the stop is dimming the thing it flew to")
        # EVERY figure on the page, recomputed independently and formatted the way the
        # page formatted it. Not a sample and not a prefix: all of them.
        figs = t.get("figs") or {"num": [], "str": []}
        for path, mm, mul, digits, got in figs["num"]:
            try:
                v = dig(expected, path) * (1000 if mm else 1) * mul
            except (KeyError, TypeError, IndexError, ValueError):
                bad.append(f"{lid}: data-n=\"{path}\" resolves to nothing the gate can "
                           "recompute — a toured level may not show a figure with no source")
                continue
            want = shown_as(v, digits)
            if got != want:
                bad.append(f"{lid}: {path} shows {got!r}, the source gives {want!r}")
        for path, got in figs["str"]:
            try:
                want = str(dig(expected, path))
            except (KeyError, TypeError, IndexError, ValueError):
                bad.append(f"{lid}: data-s=\"{path}\" resolves to nothing the gate can "
                           "recompute")
                continue
            if got != want:
                bad.append(f"{lid}: {path} shows {got!r}, the source gives {want!r}")
        if len(figs["num"]) < len(t["keys"]):
            bad.append(f"{lid}: {len(figs['num'])} bound figures across {len(t['keys'])} "
                       "stops — the copy is typed prose")
        if t.get("naked"):
            bad.append(f"{lid}: {sorted(set(t['naked']))} appear in the copy with no "
                       "data-n or data-s binding — a toured level's figures are all "
                       "generated, or the gate is only checking the ones that happen to "
                       "be wired")
    for i, (fade, draws, tris) in enumerate(res.get("stageDive") or []):
        if abs(fade - 1) > 1e-6:
            bad.append(f"frame {i} of the cell->connectors dive draws the shared article at "
                       f"fade {fade:.3f} — two stage levels show one scene graph, so the "
                       "dive must hold it at 1 and move only the camera")
        if draws < 3 or tris <= 0:
            bad.append(f"frame {i} of the cell->connectors dive is nearly empty "
                       f"({draws} draws, {tris} tris)")
    if not res.get("stageDive"):
        bad.append("the cell->connectors dive was never driven")
    # THE READING THE PAGE OPENS ON. The cell level lights the twelve members that reach the
    # centre joint and dims the other 204; a tour on a neighbouring level borrows the same
    # tint buffer, so coming back must restore the group rather than leave the cell showing
    # everything. Held to the graph: the centre node is 12-armed, so 12 members reach it.
    if res.get("defaultGroup") != "centre":
        bad.append(f"the cell level came back from the tours on group "
                   f"{res.get('defaultGroup')!r} — the page opens on 'centre' and a tour "
                   "must hand the dim back, not keep it")
    if res.get("groupLitCount") != 12:
        bad.append(f"{res.get('groupLitCount')} members reach the centre joint, not 12 — "
                   "the reading the page opens on is lighting the wrong set")
    lit, dim = res.get("groupLit"), res.get("groupDim")
    if not lit or min(lit[:3]) < 0.999:
        bad.append(f"a member that reaches the centre joint is drawn at tint {lit} — the "
                   "group's own subject must be fully lit")
    if not dim or max(dim[:3]) > 0.9:
        bad.append(f"a member that does not reach the centre joint is drawn at tint {dim} "
                   "— the group dims nothing, so the reading is invisible")
    # And clearing it must put the article back.
    cleared = res.get("clearedTint")
    if cleared and min(cleared) < 0.999:
        bad.append(f"the cell level is still dimmed after group 'all' ({cleared}) — "
                   "clearing the group must clear every tint")
    cf = res.get("clearedFrame") or [0, 0]
    if cf[0] < 3 or cf[1] <= 0:
        bad.append(f"the cell level draws a nearly empty frame after the tour ({cf})")
    # The standing contradiction, held to both of its sources and stated in both places
    # that name the rim tube: the corner that receives it and the cut that is it.
    rim_od_mm = (model.get("stock", {}).get("rimOdM") or 0) * 1000
    rim_mismatch = abs(manifest["paramsMm"]["pipe_od"] - rim_od_mm) > 1e-9
    if rim_mismatch and res.get("rimSkuNotes") != 2:
        bad.append(f"the rim edges are a {rim_od_mm:.0f} mm SKU and every printed socket is "
                   f"grown from {manifest['paramsMm']['pipe_od']:.0f} mm, but only "
                   f"{res.get('rimSkuNotes')} of the 2 cards that name that tube carry the "
                   "note saying so")
    if not rim_mismatch and res.get("rimSkuNotes"):
        bad.append("the generator now matches the rim SKU — the contradiction notes are "
                   "stale and must go")

    if bad:
        print("EXPLORER CHECK FAILED:\n")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    n = len(res["levels"])
    figs = sum(len(t["figs"]["num"]) + len(t["figs"]["str"]) for t in res["tours"])
    stops = sum(len(t["keys"]) for t in res["tours"])
    ids = ", ".join(t["id"] for t in res["tours"])
    # The joint and pipe counts go in the success line ON PURPOSE. Both sides of those
    # comparisons are read off the page, and two absent values compare equal — a check that
    # can pass by measuring nothing is the failure this whole file exists to prevent.
    # Printed, a zero is visible; silent, it is a green build over an article drawn with no
    # joints on it.
    print(f"explorer: {n} levels render, {len(res['checks'])} displayed figures match "
          f"the model, {res.get('jointsDrawn')} joint meshes + "
          f"{res.get('repsDrawn')} print-res reps + {res.get('pipesDrawn')} pipes drawn, "
          "no page errors.")
    # The net's figures are printed for the same reason the receiver count is: both sides of
    # those comparisons come off the page, and two absent values compare equal.
    _n = res.get("net") or {}
    print(f"          the skin unfolds to a flat net: {_n.get('folds')} folds / "
          f"{_n.get('cuts')} cuts, {_n.get('areaM2', 0):.4f} m2 inside "
          f"{_n.get('widthM', 0):.3f} x {_n.get('heightM', 0):.3f} m, "
          f"{_n.get('thicknessMm', 0):.5f} mm out of plane, "
          f"{_n.get('overlaps')} overlapping face pairs — it can be cut.")
    print(f"          {len(res['tours'])} tours ({ids}), {stops} stops driven through "
          f"#tourNext: camera, panel and dim agree.")
    print(f"          {figs} figures on those levels recomputed — the manifest of the "
          f"{res['partCount']} printed joints ({res['memberEnds']} member-ends), the "
          f"{res['memberKinds'] and sum(res['memberKinds'].values())}-member cut schedule, "
          "and the model itself.")


if __name__ == "__main__":
    main()
