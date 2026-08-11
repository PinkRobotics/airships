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
import pathlib
import re
import sys

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
    return format(x, fmt)


# (markdown file, json file, dotted path into it, python format spec)
# The format spec is how the number is written in the prose — so a change of units or of
# rounding in the note is caught as loudly as a change of value in the model.
MANIFEST = [
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

    ("descent.md", "descent", "classes/P100/integratedMWh/withAnchorWhereItReaches", ".3f"),
    ("descent.md", "descent", "classes/P100/ledgerSays/understatementVsIntegral", ".1f"),
    ("descent.md", "descent", "classes/P100/integratedMWh/anchorSavingPct", ".1f"),
    ("descent.md", "descent", "classes/P100/anchorAvailableForPctOfDescent", ".1f"),

    ("delivery.md", "delivery", "classes/P100/atRealMedianLeg/lineKmPer24hAtCL4_30mSwath", ".1f"),
    ("delivery.md", "delivery", "classes/P100/atRealMedianLeg/pctOfPerimetersLinedDailyAtCL4",
     ".1f"),
    ("delivery.md", "delivery", "classes/P100/atRealMedianLeg/pctOfPerimetersLinedDailyAtCL8",
     ".1f"),
    ("delivery.md", "delivery", "perimeters/km/p50", ".1f"),
    ("delivery.md", "delivery", "classes/P100/ownUpwash/end of release/airMassFlowKgS", ",d"),


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
    ("vacuum-cell.md", "vacuum-cell", "gradedPressure/band/costPctOfNetLift", ".1f"),
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

    # The pumped plenum: operating margin and permeation drive at the quoted pressures.
    ("vacuum-cell.md", "vacuum-cell", "pumpedPlenum/rows/0.50/cellOperatingMarginX", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "pumpedPlenum/rows/0.25/cellOperatingMarginX", ".2f"),
    ("vacuum-cell.md", "vacuum-cell", "pumpedPlenum/rows/0.10/cellOperatingMarginX", ".2f"),

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


def main() -> None:
    cache: dict[str, dict] = {}
    bad, checked = [], 0
    for md, jname, path, fmt in MANIFEST:
        doc = cache.setdefault(jname, load(jname))
        text = (A / md).read_text()
        try:
            value = dig(doc, path)
        except (KeyError, TypeError, IndexError, ValueError):
            bad.append(f"{md}: {jname}.json has no {path} — the manifest is stale")
            continue
        want = num(value, fmt)
        checked += 1
        # Word-boundary search, so 4.71 does not match inside 14.712.
        if not re.search(rf"(?<![\d.,]){re.escape(want)}(?![\d])", text):
            bad.append(f"{md}: does not contain {want!r} "
                       f"(from {jname}.json {path}) — the prose has drifted")

    if bad:
        print("ANALYSIS GATE FAILED — the notes disagree with their own generated data:\n")
        for b in bad:
            print("  " + b)
        print("\nRegenerate with `make analysis`, then correct the prose.")
        sys.exit(1)
    print(f"{checked} analysis figures match the JSON their scripts produced.")


if __name__ == "__main__":
    main()
