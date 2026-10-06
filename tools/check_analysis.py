#!/usr/bin/env python3
"""Every number the analysis notes quote must be the number their own scripts produced.

    python3 tools/check_analysis.py

WHY THIS EXISTS, and it is the same lesson twice. `tools/check_figures_fresh.py` was written
because `figcheck` compared the reports against a COMMITTED CACHE and printed a success line
naming the model — "the gate was loudest exactly when it was lying". On 2026-08-10 the same
hole opened one directory over: `research/analysis/*.md` carry hand-transcribed numbers,
`tools/check_figures.py` globs `research/reports/*.md` only, and `make analysis` is outside
`make check`. A review caught five figures in `air-ballast.md` and four in `mass-budget.md`
sitting stale against their own JSON for seventeen minutes, while the documents asserted
"none is typed in".

So: below is an explicit manifest. Each row names a document, a value in one of the generated
JSON files, and how it is written in the prose. Every row must be found, and must match. A
figure that changes and is not transcribed fails the build; a claim that no longer has a
generated basis fails it too.

Adding a headline number to an analysis note without adding a row here is the defect this
file exists to catch, so keep the manifest ahead of the prose.
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import sys
import subprocess
from numeric_tokens import numeric_pattern

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "research" / "analysis"


def load(name: str) -> dict:
    p = A / f"{name}.json"
    if not p.exists():
        sys.exit(f"check_analysis: {p} is missing — run `make analysis` first.")
    return json.loads(p.read_text())


def dig(doc, path: str):
    """Walk a path. Separator is '/' and not '.', because several keys ARE numbers with
    dots in them ('0.508') and a dotted path cannot address them."""
    cur = doc
    for part in path.split("/"):
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def num(x, fmt: str) -> str:
    return "not served" if x is None else format(x, fmt)


def document_path(name: str, root=ROOT):
    return root / name if name.startswith('docs/') else root / 'research/analysis' / name


# (markdown file, json file, dotted path into it, python format spec)
# The format spec is how the number is written in the prose — so a change of units or of
# rounding in the note is caught as loudly as a change of value in the model.
MANIFEST = [
    ("vacuum-cell.md", "vacuum-cell", "sp8007Comparison/tubeROverT", ".4f"),
    ("vacuum-cell.md", "vacuum-cell", "sp8007Comparison/gammaEq9", ".6f"),
    ("vacuum-cell.md", "vacuum-cell", "sp8007Comparison/kLocal", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "sp8007Comparison/kLocalOverGamma", ".6f"),
    ("vacuum-cell.md", "vacuum-cell", "sp8007Comparison/tubeLOverR", ".4f"),
    ("mass-budget.md", "mass-budget", "classes/P100/shellDensityWallKgPerM3", ".3f"),
    ("mass-budget.md", "mass-budget", "classes/P100/cases/floor/overBy", ".2f"),
    ("mass-budget.md", "mass-budget", "classes/P100/rightSized/floor/overBy", ".2f"),
    ("mass-budget.md", "mass-budget", "classes/P100/rightSized/floor/totalT", ".1f"),
    ("mass-budget.md", "mass-budget",
     "classes/P100/rightSized/floor/hullThatCloses/0.508/volumeM3", ",d"),
    ("mass-budget.md", "mass-budget",
     "classes/P100/rightSized/floor/hullThatCloses/0.508/timesBaseline", ".2f"),

    ("water-availability.md", "water-availability", "classes/P100/distanceKm/byFire/p50", ".2f"),
    ("water-availability.md", "water-availability",
     "classes/P100/servedWithinClassSearchKm/pctFires", ".2f"),
    ("water-availability.md", "water-availability",
     "classes/P100/throughputTph/atMedianByFire", ".1f"),
    ("water-availability.md", "water-availability", "input/fires", ",d"),

    # 2026-10-01: descent.json is the one model's own descent (sim/power.js), no longer an
    # alternative integral; the old understatement/saving keys have no generated basis now.
    ("descent.md", "descent", "classes/P100/letdown/mwh", ".3f"),
    ("descent.md", "descent", "classes/P100/letdown/pctOfCycle", ".1f"),
    ("descent.md", "descent", "classes/P1000/geometry/rotorsAloneFailBelowAglM", ",d"),
    ("descent.md", "descent", "classes/P1000/letdown/clippedMinutes", ".2f"),
    ("descent.md", "descent", "classes/P10000/rotorsBlindToTheBag/creditSavesPctOfCycle", ".1f"),
    ("descent.md", "descent", "classes/P10000/withoutTheBag/bagCostsPerTonnePct", ".1f"),
    ("descent.md", "descent", "classes/P10000/withoutTheBag/bagBuysDeliveredT", ",.1f"),

    ("delivery.md", "delivery", "classes/P100/atRealMedianLeg/lineKmPer24hAtCL4_30mSwath", ".1f"),
    ("delivery.md", "delivery", "classes/P100/atRealMedianLeg/pctOfPerimetersLinedDailyAtCL4",
     ".1f"),
    ("delivery.md", "delivery", "classes/P100/atRealMedianLeg/pctOfPerimetersLinedDailyAtCL8",
     ".1f"),
    ("delivery.md", "delivery", "perimeters/km/p50", ".1f"),
    ("delivery.md", "delivery", "classes/P100/ownUpwash/end of release/airMassFlowKgS", ",d"),
    ("delivery.md", "delivery", "references/terminalMs/2.0", ".1f"),


    ("vacuum-cell.md", "vacuum-cell", "theWall/rhoAirAtWorkAltKgPerM3", ".4f"),
    ("vacuum-cell.md", "vacuum-cell", "designPoint/buildUp/total", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "designPoint/buildUp/lattice", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "designPoint/buildUp/interiorFilm", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "designPoint/tubeROverT", ".0f"),
    ("vacuum-cell.md", "vacuum-cell", "materials/PAHT_Z/totalKgPerM3", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "constants/orthotropicPenalty", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "hierarchy/ladder/2/totalKgPerM3", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "hierarchy/ladder/1/totalKgPerM3", ".3f"),
    ("vacuum-cell.md", "vacuum-cell",
     "designPoint/filmIsAChoiceAndTheModelPickedOneIncoherently/totalIfOuterEnvelopeOnly",
     ".3f"),

    ("air-ballast.md", "mass-budget", "classes/P100/descentWithoutNitrogen/cycleSavingPct", ".1f"),
    # (Eleven rows used to be repeated verbatim here. They checked nothing new and
    # inflated the success banner by eleven — the exact dishonesty this gate exists to
    # prevent, committed by the gate itself.)
    ("air-ballast.md", "mass-budget",
     "classes/P100/descentWithoutNitrogen/residualForRotorsT", ".1f"),

    # The printer chain: nozzle -> wall -> strut -> cell. The 44 here replaced a hand-typed
    # 45 the day this row was added, which is this file's whole argument made flesh.
    ("vacuum-cell.md", "vacuum-cell", "printerChain/rows/0.6 mm x 2/strutM", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "printerChain/rows/0.6 mm x 2/cellM", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "printerChain/rows/0.6 mm x 2/enclosedL", "d"),
    ("vacuum-cell.md", "vacuum-cell", "printerChain/rows/0.4 mm x 2/strutM", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "printerChain/rows/1.0 mm x 2/cellM", ".3f"),

    # Graded pressure, statics-correct third model: bulk numbers and the boundary band.
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/bulk/1/netLiftKgPerM3", "+.3f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/bulk/2/netLiftKgPerM3", "+.3f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/bulk/10/netLiftKgPerM3", "+.3f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/bulk/10/structureKgPerM3", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/netCostKgPerM3", "+.4f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/filmsDeltaKgPerM3", ".4f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/internalInterfaceAreaM2", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/interfaceCount", "d"),
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/filmSpanM", ".1f"),
    *[("vacuum-cell.md", "vacuum-cell", f"gradedPressure/band/resizedFilm/{field}", ".1f")
      for field in ("fullWorkingStressMPa", "reducedWorkingStressMPa",
                    "unchangedThicknessReducedStressMPa")],
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/outerSurfaceDifferentialAtm",
     ".1f"),

    # The demonstrator's mass, and the ladder's yield cap.
    ("vacuum-cell.md", "vacuum-cell", "demonstrator/totalKg", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "demonstrator/massOverDisplaced", ".0f"),

    # The weightless article: single-article densities at sea level, per rung.
    ("vacuum-cell.md", "vacuum-cell", "weightlessArticle/rows/M60J_LAM/densityAtN1", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "weightlessArticle/rows/CFF/densityAtN1", ".3f"),
    ("vacuum-cell.md", "vacuum-cell", "weightlessArticle/rows/T700_LAM/densityAtN1", ".3f"),

    # The hybrid stock build: purchased pipe, printed ties (the 2026-08-10 reframing).
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/totalKg", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/pipe/kg", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/pipe/eulerMarginPinned", ".1f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/pipe/perStrutDemandN", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/printed/nodesKg", ".2f"),
    # The article's own density, which is the number that answers "is this anywhere near
    # floating". It was hand-arithmetic in the prose and went stale the moment the per-arm
    # SKU moved the joints 0.444 -> 0.465 kg; nothing in this manifest was holding it.
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/kgPerM3", ".2f"),

    # ONE DEMAND PER FAMILY. The note used to quote a single crush number and the prose
    # called it "a primary's"; every family it was wrong for is held here by name, so the
    # table cannot go stale one row at a time.
    ("vacuum-cell.md", "vacuum-cell", "memberDemands/crushDivisor", "d"),
    ("vacuum-cell.md", "vacuum-cell", "memberDemands/families/rim/axialN", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "memberDemands/families/spoke/axialN", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "memberDemands/families/tripodProp/axialN", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "memberDemands/families/vertexTieInPlane/axialN",
     ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "memberDemands/octetStandaloneEntryN", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/pipe/rimEulerMargin", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/pipe/spokeEulerMargin", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "stockBuild/pipe/tieEulerMargin", ".2f"),

    # The bending check that governs the boundary, and the buoyancy the bulge eats.
    ("vacuum-cell.md", "vacuum-cell", "filmEdgeLoads/rows/0/failsAtAtm", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "filmEdgeLoads/rows/0/stressPinnedMPa", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "filmEdgeLoads/rows/2/failsAtAtm", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "filmEdgeLoads/bulgeVolumeLostUnbracedPct", ".1f"),
    ("vacuum-cell.md", "vacuum-cell", "filmEdgeLoads/bulgeVolumeLostPct", ".1f"),
    ("vacuum-cell.md", "vacuum-cell", "filmEdgeLoads/tripodPropN", ",.0f"),
    ("vacuum-cell.md", "vacuum-cell", "hierarchy/ladder/3/totalKgPerM3", ".3f"),
    ("vacuum-cell.md", "vacuum-cell",
     "designPoint/filmIsAChoiceAndTheModelPickedOneIncoherently/outerEnvelopeOnlyKgPerM3",
     ".3f"),

    # Film differential and structural margin occupy separate generated columns.
    *[("vacuum-cell.md", "vacuum-cell", f"pumpedPlenum/rows/{p}/{field}", ".2f")
      for p in ("1.00", "0.50", "0.25", "0.10")
      for field in ("plenumAtm", "filmPressureDifferenceFactor", "structureMarginX",
                    "permeationDriveX", "breachFloodsToAtm")],

    # Cell shape: the Kelvin cell's film saving over the cube baseline.
    ("vacuum-cell.md", "vacuum-cell", "cellShapes/truncatedOctahedron/filmSavingVsCubePct",
     ".1f"),
    ("vacuum-cell.md", "vacuum-cell", "cellShapes/truncatedOctahedron/coeff", ".3f"),

    # The helium question — the ledger, the break-even, the market, the fleet.
    ("helium.md", "helium", "ledger/vacuumLevel1/net", "+.3f"),
    ("helium.md", "helium", "ledger/vacuumLevel2/net", "+.3f"),
    ("helium.md", "helium", "ledger/hydrogen/net", "+.3f"),
    ("helium.md", "helium", "ledger/helium/net", "+.3f"),
    ("helium.md", "helium", "breakeven/structureToTieHydrogenKgPerM3", ".3f"),
    ("helium.md", "helium", "perShip/fillStdM3", ",d"),
    ("helium.md", "helium", "perShip/fillUsdM", ".1f"),
    ("helium.md", "helium", "perShip/makeupPctPerYr", ".1f"),
    ("helium.md", "helium", "fleet/pctOfUsAnnualConsumption", "d"),
    ("helium.md", "helium", "fleet/pctOfWorldAnnualProduction", "d"),
    ("helium.md", "helium", "usefulFraction/vacuumLevel2Pct", ".1f"),
    ("helium.md", "helium", "heliumMarket/priceRisePct", "d"),
    ("helium.md", "helium", "heliumMarket/price2021UsdPerM3", ".2f"),
]

# Capsule-area readers repaired on 2026-10-02, each tied to its generated field.
MANIFEST += [
    ('mass-budget.md', 'mass-budget', 'classes/P100/requiredKgPerM2', '.3f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/hullAreaM2', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/floor/lines/1/tonnes', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/credible/lines/1/tonnes', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/demonstrated/lines/1/tonnes', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/floor/lines/15/tonnes', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/credible/lines/15/tonnes', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/demonstrated/lines/15/tonnes', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/floor/totalT', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/floor/overBy', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/credible/totalT', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/credible/overBy', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/demonstrated/totalT', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/cases/demonstrated/overBy', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/totalT', '.1f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.264/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.264/timesBaseline', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.264/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.264/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.350/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.350/timesBaseline', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.350/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.350/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.508/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.508/timesBaseline', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.508/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.508/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.600/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.600/timesBaseline', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.600/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.600/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.750/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.750/timesBaseline', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.750/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.750/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.508/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/hullThatCloses/0.508/timesBaseline', '.2f'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.74/0.264/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.74/0.264/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.74/0.264/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.74/0.508/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.74/0.508/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.74/0.508/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.85/0.264/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.85/0.264/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.85/0.264/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.85/0.508/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.85/0.508/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=0.85/0.508/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.264/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.264/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.264/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.508/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.508/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.508/diaM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.750/volumeM3', ',d'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.750/lenM', 'd'),
    ('mass-budget.md', 'mass-budget', 'classes/P100/rightSized/floor/cellular/phi=1.0/0.750/diaM', 'd'),
]
MANIFEST = list(dict.fromkeys(MANIFEST))

MANIFEST += [
    ("water-availability.md", "water-availability", "geometry/P100/hullStationDiscHa", ".2f"),
    ("water-availability.md", "water-availability", "geometry/P10000/hullStationDiscHa", ".2f"),
    ("water-availability.md", "water-availability", "geometry/P100/conservatismVsHullDisc", ".1f"),
    ("water-availability.md", "water-availability", "geometry/P10000/conservatismVsHullDisc", ".1f"),
]

# Other permitted readers of the capsule correction. Dated notes retain their old
# text and place the current correction beside it.
MANIFEST += [
    ("../../docs/OPEN-QUESTIONS.md", "mass-budget", "classes/P100/rightSized/floor/hullThatCloses/0.508/volumeM3", ",d"),
    ("../../docs/OPEN-QUESTIONS.md", "mass-budget", "classes/P100/rightSized/floor/hullThatCloses/0.508/lenM", "d"),
    ("../../docs/VERIFICATION-PLAN.md", "mass-budget", "classes/P100/rightSized/floor/hullThatCloses/0.508/volumeM3", ",d"),
    ("../../docs/VERIFICATION-PLAN.md", "mass-budget", "classes/P100/rightSized/floor/hullThatCloses/0.508/lenM", "d"),
]
for cid in ("P100", "P1000", "P10000"):
    MANIFEST += [
        ("../../docs/PHYSICS.md", "mass-budget", f"classes/{cid}/hullAreaM2", ",d"),
        ("../../docs/PHYSICS.md", "mass-budget", f"classes/{cid}/requiredKgPerM2", ".2f"),
    ]


# Short values have unrelated witnesses (15 of 36 rows on the audited tree).
# Bind these rows to their quantity, or to the labelled table cell, as well as
# requiring a whole numeric token. {number} is always the shared matcher.
CONTEXTS = {
    ("delivery.md", "references/terminalMs/2.0"):
        r"For 2 mm drops, terminal speed is {number} m/s",
    ("vacuum-cell.md", "sp8007Comparison/tubeROverT"): r"model's R/t = {number}",
    ("vacuum-cell.md", "sp8007Comparison/gammaEq9"): r"Isotropic gamma = {number}",
    ("vacuum-cell.md", "sp8007Comparison/kLocal"): r"assumed K_LOCAL = {number}",
    ("vacuum-cell.md", "sp8007Comparison/kLocalOverGamma"): r"is {number} of that value",
    ("vacuum-cell.md", "sp8007Comparison/tubeLOverR"): r"tube has L/R = {number}",
    ("descent.md", "classes/P10000/rotorsBlindToTheBag/creditSavesPctOfCycle"):
        r"^\| P10000 \| record \|[^|]*\| {number} \|",
    ("descent.md", "classes/P10000/withoutTheBag/bagCostsPerTonnePct"):
        r"^\| P10000 \| record \|[^|]*\|[^|]*\| {number} \|",
    ("descent.md", "classes/P10000/withoutTheBag/bagBuysDeliveredT"):
        r"^\| P10000 \| record \|[^|]*\|[^|]*\|[^|]*\| {number} \|",
    ("vacuum-cell.md", "designPoint/tubeROverT"): r"optimum here is \*\*R/t ≈ {number}\*\*",
    ("air-ballast.md", "classes/P100/descentWithoutNitrogen/cycleSavingPct"):
        r"^\| P-100 \|[^|]*\|[^|]*\|[^|]*\| \*\*{number}%\*\* \|",
    ("vacuum-cell.md", "printerChain/rows/0.6 mm x 2/enclosedL"):
        r"^\| \*\*0\.6 mm\*\* \| \*\*2\*\* \|[^\n]*\*\*{number} L\*\* \|",
    ("vacuum-cell.md", "gradedPressure/band/netCostKgPerM3"):
        r"The complete band's net mass cost is \*\*{number} kg/m³\*\*",
    ("vacuum-cell.md", "gradedPressure/band/filmsDeltaKgPerM3"):
        r"Internal interface films cost \*\*{number} kg/m³\*\*",
    ("vacuum-cell.md", "gradedPressure/band/internalInterfaceAreaM2"):
        r"The interfaces total \*\*{number} m²\*\*",
    ("vacuum-cell.md", "gradedPressure/band/interfaceCount"):
        r"The band needs \*\*{number} complete internal interfaces\*\*",
    ("vacuum-cell.md", "gradedPressure/band/filmSpanM"):
        r"Each film is priced at a \*\*{number} m lateral span\*\*",
    ("vacuum-cell.md", "gradedPressure/band/resizedFilm/fullWorkingStressMPa"):
        r"The resized film at full differential works at \*\*{number} MPa\*\*",
    ("vacuum-cell.md", "gradedPressure/band/resizedFilm/reducedWorkingStressMPa"):
        r"The resized film at reduced differential also works at \*\*{number} MPa\*\*",
    ("vacuum-cell.md", "gradedPressure/band/resizedFilm/unchangedThicknessReducedStressMPa"):
        r"Retaining the original thickness instead gives \*\*{number} MPa\*\*",
    ("vacuum-cell.md", "gradedPressure/band/outerSurfaceDifferentialAtm"):
        r"outer surface sees\s+\*\*{number} atm\*\*",
    ("vacuum-cell.md", "demonstrator/massOverDisplaced"):
        r"all-printed variant[^\n]*about {number} times",
    ("vacuum-cell.md", "stockBuild/pipe/eulerMarginPinned"): r"Euler margins are ×{number} pinned",
    ("vacuum-cell.md", "stockBuild/printed/nodesKg"):
        r"article reads the manifest — \*\*{number} kg\*\*",
    ("vacuum-cell.md", "memberDemands/crushDivisor"): r"3 × 32 = \*\*{number}\*\*",
    ("vacuum-cell.md", "filmEdgeLoads/rows/0/failsAtAtm"): r"unbraced rim capacity is {number}\s+atmospheres",
    ("vacuum-cell.md", "filmEdgeLoads/bulgeVolumeLostPct"): r"spoked,\s+{number}%",
    ("vacuum-cell.md", "designPoint/filmIsAChoiceAndTheModelPickedOneIncoherently/outerEnvelopeOnlyKgPerM3"):
        r"^\| barrier on the outer envelope only \| {number} \|",
    ("helium.md", "breakeven/structureToTieHydrogenKgPerM3"): r"break-even structure to tie hydrogen is {number} kg/m³",
    ("helium.md", "perShip/fillUsdM"): r"standard m³ ≈ \*\*\${number}M",
    ("helium.md", "perShip/makeupPctPerYr"): r"make-up around {number}%/yr",
    ("helium.md", "fleet/pctOfUsAnnualConsumption"): r"{number}% of US\s+annual consumption",
    ("helium.md", "fleet/pctOfWorldAnnualProduction"): r"{number}% of world production",
    ("helium.md", "heliumMarket/priceRisePct"): r"\+{number}% in two years",
    ("mass-budget.md", "classes/P100/cases/floor/lines/1/tonnes"):
        r"^\| Gas barrier skin \| {number} \|",
    ("mass-budget.md", "classes/P100/cases/credible/lines/1/tonnes"):
        r"^\| Gas barrier skin \|[^|]*\| {number} \|",
    ("water-availability.md", "geometry/P100/hullStationDiscHa"): r"{number} ha for a P-100,",
}
for density in ("0.264", "0.350", "0.508", "0.600", "0.750"):
    # The right-sized table has one density per row; its final cell is length × diameter.
    CONTEXTS[("mass-budget.md", f"classes/P100/rightSized/floor/hullThatCloses/{density}/diaM")] = (
        r"^\| \*?\*?" + re.escape(density) + r"[^|]*\|[^|]*\|[^|]*\|[^|]*× {number} m")
for phi, densities in (("0.74", ("0.264", "0.508")), ("0.85", ("0.264", "0.508")),
                       ("1.0", ("0.264", "0.508", "0.750"))):
    column = {"0.74": 0, "0.85": 1, "1.0": 2}[phi]
    for density in densities:
        CONTEXTS[("mass-budget.md", f"classes/P100/rightSized/floor/cellular/phi={phi}/{density}/diaM")] = (
            r"^\| hull at shell " + re.escape(density) + r" \|" + r"[^|]*\|" * column
            + r"[^|]*× {number} m")


# Compression correction: every ladder density and paired-altitude ratio owns its row.
for level in range(5):
    for column, field, fmt in ((2, 'totalKgPerM3', '.3f'),
                               (3, 'liftToMassSeaLevel', '.3f'),
                               (4, 'liftToMassAt2500m', '.3f')):
        pointer = f'hierarchy/ladder/{level}/{field}'
        row = ('vacuum-cell.md', 'vacuum-cell', pointer, fmt)
        if row not in MANIFEST:
            MANIFEST.append(row)
        CONTEXTS[('vacuum-cell.md', pointer)] = (
            r'^\| ' + str(level) + r' \|' + r'[^|]*\|' * (column - 1) + r' {number} \|')
MANIFEST.append(('helium.md', 'helium', 'breakeven/minimumStructureOverHydrogenBreakEven', '.1f'))
CONTEXTS[('helium.md', 'breakeven/minimumStructureOverHydrogenBreakEven')] = r'deepest hierarchy level is {number} times'


MANIFEST.append(('vacuum-cell.md', 'vacuum-cell', 'hierarchy/ladder/2/solidStressOverStrength', '.0%'))
CONTEXTS[('vacuum-cell.md', 'hierarchy/ladder/2/solidStressOverStrength')] = r'Hierarchy level 2 runs at {number} of the model'
for field, phrase in (('usefulFraction/vacuumLevel2StructurePct', r'compression cap gives a {number}% structural share'),
                      ('breakeven/minimumStructureOverHydrogenBreakEven', r'deepest hierarchy level costs {number} times')):
    MANIFEST.append(('docs/PHYSICS.md', 'helium', field, '.1f'))
    CONTEXTS[('docs/PHYSICS.md', field)] = phrase

# Each plenum column owns its own pressure row, rather than a repeated witness.
for pressure in ("1.00", "0.50", "0.25", "0.10"):
    for field, preceding in (("filmPressureDifferenceFactor", ""),
                             ("structureMarginX", r"[^|]*\| "),
                             ("permeationDriveX", r"[^|]*\|[^|]*\| ")):
        CONTEXTS[("vacuum-cell.md", f"pumpedPlenum/rows/{pressure}/{field}")] = (
            r"^\| " + re.escape(pressure) + r" atm(?: \(no plenum\))? \| "
            + preceding + r"×{number} \|")
    CONTEXTS[("vacuum-cell.md", f"pumpedPlenum/rows/{pressure}/plenumAtm")] = (
        r"^\| {number} atm(?: \(no plenum\))? \|")
    CONTEXTS[("vacuum-cell.md", f"pumpedPlenum/rows/{pressure}/breachFloodsToAtm")] = (
        r"^\| " + re.escape(pressure) + r" atm(?: \(no plenum\))? \|"
        + r"[^|]*\|" * 3 + r" {number} atm \|")


def matches(text, want, context=None):
    pattern = numeric_pattern(want)
    if context is not None:
        pattern = context.replace("{number}", pattern)
    return re.search(pattern, text, re.M) is not None


def check_rows(directory=A):
    cache: dict[str, dict] = {}
    bad, checked = [], 0
    for md, jname, path, fmt in MANIFEST:
        if jname not in cache:
            cache[jname] = json.loads((directory / f"{jname}.json").read_text())
        doc = cache[jname]
        text = document_path(md, directory.parent.parent).read_text()
        try:
            value = dig(doc, path)
        except (KeyError, TypeError, IndexError, ValueError):
            bad.append(f"{md}: {jname}.json has no {path} — the manifest is stale")
            continue
        if value is None and jname not in ('water-availability', 'delivery'):
            bad.append(f'{jname}.json {path}: unexpected unavailable figure')
            continue
        want = num(value, fmt)
        checked += 1
        if not matches(text, want, CONTEXTS.get((md, path))):
            bad.append(f"{md}: does not contain {want!r} "
                       f"(from {jname}.json {path}) — the prose has drifted")
    return cache, bad, checked


def check_closure_bills(document, figures):
    """Rebuild each complete bill, without importing or solving closing_volume.

    Equipment lines are the same rounded tonnes that the closure input uses. Only
    barrier and solar grow with surface area. Sundries apply to shell AND equipment;
    payload is added separately. Volume is rounded to 1 m3, so its error is <=0.5 m3.
    The tolerance is 0.5 times the largest absolute bill-residual slope over that
    interval, plus 1e-8 t for floating-point arithmetic. There is no equipment-rounding
    allowance: these committed equipment lines are the inputs, not measurements.
    """
    bad, checked = [], 0
    rho = figures['atmosphere']['rhoAtWorkAlt']
    for cid, hull in document['classes'].items():
        spec = figures['classes'][cid]['spec']
        for case, budget in hull['rightSized'].items():
            fraction = document['evidence']['sundries_frac'][case]['value']
            groups = [('hullThatCloses', rho, budget['hullThatCloses'])]
            groups += [(f'cellular/{packing}', rho * float(packing.split('=')[1]), rows)
                       for packing, rows in budget['cellular'].items()]
            equipment = [line for line in budget['lines']
                         if not line['item'].startswith(('Vacuum shell', 'Sundries'))]
            for group, density, rows in groups:
                for shell, record in rows.items():
                    if not record['closes']:
                        continue
                    checked += 1
                    label = f'{cid}/{case}/{group}/{shell}'
                    effective = float(shell) * (1 + fraction)
                    if effective >= density:
                        bad.append(f'{label}: claims closure with effective shell density '
                                   f'{effective:.6f} >= lift density {density:.6f} kg/m3')
                        continue
                    volume = record['volumeM3']
                    if not math.isfinite(volume) or volume <= 0.5:
                        bad.append(f'{label}: invalid rounded volume')
                        continue
                    def bill(v):
                        shell_t = float(shell) * v / 1000
                        equipment_t = sum(line['tonnes'] *
                            ((v / spec['dispM3']) ** (2/3)
                             if line['item'].startswith(('Gas barrier', 'Solar')) else 1)
                            for line in equipment)
                        subtotal = shell_t + equipment_t
                        return spec['payloadT'] + subtotal + fraction * subtotal
                    area_t = sum(line['tonnes'] for line in equipment
                                 if line['item'].startswith(('Gas barrier', 'Solar')))
                    def slope(v):
                        return ((density - effective) / 1000 - (1 + fraction) *
                                area_t * (2/3) / spec['dispM3'] ** (2/3) / v ** (1/3))
                    tolerance = 0.5 * max(abs(slope(volume - 0.5)),
                                          abs(slope(volume + 0.5))) + 1e-8
                    residual = density * volume / 1000 - bill(volume)
                    if abs(residual) > tolerance:
                        bad.append(f'{label}: lift - complete bill = {residual:+.9f} t; '
                                   f'rounded-volume tolerance {tolerance:.9f} t')
    return bad, checked


def main() -> None:
    cache, bad, checked = check_rows()
    closure_bad, closures = check_closure_bills(cache['mass-budget'],
        json.loads((ROOT / 'research/figures.json').read_text()))
    bad.extend(closure_bad)
    print(f'Closure conservation: {closures} reported closures; {len(closure_bad)} failures')

    if subprocess.run(['node', 'tools/check_logistics.mjs'], cwd=ROOT).returncode:
        bad.append('logistics rates lack exact-input accepted plans')
    if subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                       '-s', 'tools/tests', '-p', 'test_logistics.py'], cwd=ROOT).returncode:
        bad.append('logistics refusal plants failed')

    if subprocess.run([sys.executable, '-B', 'tools/gen_logistics_prose.py', '--check'], cwd=ROOT).returncode:
        bad.append('accepted-plan logistics prose differs from generated numbers')

    if subprocess.run(['node', 'research/analysis/loaded-atmosphere.mjs', '--check'], cwd=ROOT).returncode:
        bad.append('loaded-atmosphere boundaries or qualified statements differ')
    if subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                       '-s', 'tools/tests', '-p', 'test_loaded_atmosphere.py'], cwd=ROOT).returncode:
        bad.append('loaded-atmosphere counterexample or drift plants failed')

    if subprocess.run(['node', 'research/analysis/solar-area.mjs', '--check'], cwd=ROOT).returncode:
        bad.append('projected solar areas differ from current capsule geometry')
    if subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                       '-s', 'tools/tests', '-p', 'test_solar_area.py'], cwd=ROOT).returncode:
        bad.append('solar collector fails to follow a hull dimension change')

    if subprocess.run([sys.executable, '-B', 'tools/gen_solar_prose.py', '--check'], cwd=ROOT).returncode:
        bad.append('current solar prose differs from generated power and energy')

    if subprocess.run([sys.executable, '-B', 'tools/gen_solar_budget_comparison.py', '--check'], cwd=ROOT).returncode:
        bad.append('solar budget comparison differs from fresh sizing diagnostics')

    if subprocess.run(['node', 'tools/gen_served_route_selections.mjs', '--check'], cwd=ROOT).returncode:
        bad.append('captured route inputs have stale served controls')

    if subprocess.run(['node', 'research/analysis/battery-ratios.mjs', '--check'], cwd=ROOT).returncode:
        bad.append('per-class battery ratios or complete-budget passages differ')
    if subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                       '-s', 'tools/tests', '-p', 'test_battery_ratios.py'], cwd=ROOT).returncode:
        bad.append('battery ratios drift plants failed')

    if subprocess.run([sys.executable, '-B', 'tools/gen_mass_budget_prose.py', '--check'], cwd=ROOT).returncode:
        bad.append('floor sentence differs from nominal and three-cycle budget records')
    if subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                       '-s', 'tools/tests', '-p', 'test_mass_budget_prose.py'], cwd=ROOT).returncode:
        bad.append('floor sentence drift plants failed')

    # Lift per nominal surface is explicitly an allowance, not a hull mass.
    budget = cache["mass-budget"]["classes"]
    physics = (ROOT / "docs/PHYSICS.md").read_text()
    for cid, row in budget.items():
        want = format(row["shellDensityWallKgPerM3"] * row["displacementM3"] / row["hullAreaM2"], ".2f")
        checked += 1
        if not matches(physics, want):
            bad.append(f"docs/PHYSICS.md: missing {cid} lift per capsule area {want}")

    # Current capsule dimensions are bound to the configuration, not a historical table.
    fleet = json.loads(subprocess.check_output(
        ['node', '--input-type=module', '-e',
         "import {CLASSES} from './sim/config.js'; console.log(JSON.stringify(CLASSES));"],
        cwd=ROOT, text=True))
    block = physics.split('<!-- fleet-dimensions:start -->', 1)[-1].split('<!-- fleet-dimensions:end -->', 1)[0]
    for cid, spec in fleet.items():
        checked += 1
        expected = f"| {spec['name']} | {spec['lenM']} × {spec['diaM']} |"
        if expected not in block:
            bad.append(f"docs/PHYSICS.md: configured dimensions differ for {cid}")
    air = (A / 'air-ballast.md').read_text()
    for cid, spec in fleet.items():
        checked += 1
        row = next((line for line in air.splitlines() if line.startswith(f"| {spec['name']} |")), '')
        expected = f"{budget[cid]['descentWithoutNitrogen']['cycleSavingPct']:.1f}%"
        if expected not in row:
            bad.append(f"air-ballast.md: {cid} current share differs from {expected}")

    for density, record in cache['mass-budget']['classes']['P100']['rightSized']['floor']['hullThatCloses'].items():
        if not record['closes'] and not re.search(r'^\| ' + re.escape(density) + r' kg/m³ \| \*\*never\*\*', (A / 'mass-budget.md').read_text(), re.M):
            bad.append(f'mass-budget.md: missing refusal for {density}')
    if subprocess.run([sys.executable, 'tools/gen_closure_docs.py', '--check'], cwd=ROOT).returncode:
        bad.append('closure prose differs from fresh generation')

    if subprocess.run([sys.executable, 'tools/gen_closure_audit.py', '--check'], cwd=ROOT).returncode:
        bad.append('closure audit differs from current records')

    result = subprocess.run([sys.executable, 'tools/check_member_census.py'], cwd=ROOT)
    if result.returncode:
        bad.append('member census and cap readings differ from fresh generation')

    if subprocess.run([sys.executable, 'docs/audit/26-10-02-structure-questions.py', '--check'], cwd=ROOT).returncode:
        bad.append('outside-structures questions differ from their measured records')

    if subprocess.run([sys.executable, 'tools/gen_structures_docs.py'], cwd=ROOT).returncode:
        bad.append('corrected structures tables differ from fresh generation')

    if bad:
        print("ANALYSIS GATE FAILED — the notes disagree with their own generated data:\n")
        for b in bad:
            print("  " + b)
        print("\nRegenerate with `make analysis`, then correct the prose.")
        sys.exit(1)
    print(f"{checked} analysis figures match the JSON their scripts produced.")


if __name__ == "__main__":
    main()
