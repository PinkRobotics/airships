#!/usr/bin/env python3
"""Two fixed capsule sizes, no net or membrane credit; not a vehicle qualification."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PINS = {
    "research/analysis/vacuum-cell.py": "21d5a26c3616bb09fab0585e9e8613f84be8ed786d5d509287fd1839efd564a5",
    "research/analysis/float-ledger.json": "d4c8085510bd80fb6feb0951b6bb33030cd16b5f9452f5fb7c015a97d2916126",
}


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-8), (a, b)


def takeoff(m, row):
    """Expose the frozen model's continuous/equivalent take-off, not shop cuts."""
    g, w, s = row["geom"], row["wall"], row["skeleton"]
    rho = m.MATERIALS["T700_LAM"]["rho"]
    barrel_area = 2 * math.pi * g["R"] * g["cylL"]
    long_length = g["cylL"] + 2 * min(math.sqrt(g["R"] * g["depthM"]), math.pi / 2 * g["rIn"])
    fan_length = math.hypot(g["depthM"], m.SHIP0["bayM"] / 2)
    families = {
        "rings": dict(lengthM=barrel_area / m.SHIP0["ringPitchM"], areaM2=w["ring"]["A"], addition=1.0),
        "bars": dict(lengthM=barrel_area / m.SHIP0["barPitchM"], areaM2=w["bar"]["A"], addition=1.0),
        "longerons": dict(count=g["nLong"], eachM=long_length, lengthM=g["nLong"] * long_length,
                          areaM2=s["longeron"]["A"], addition=1.05),
        "innerRings": dict(count=s["nInnerRings"], eachM=2 * math.pi * g["rIn"],
                           lengthM=s["nInnerRings"] * 2 * math.pi * g["rIn"], areaM2=s["innerRingAM2"], addition=1.05),
        "fanWebs": dict(equivalentCount=g["meridianM"] / m.SHIP0["bayM"] * 2 * g["nLong"], eachM=fan_length,
                        lengthM=g["meridianM"] / m.SHIP0["bayM"] * 2 * g["nLong"] * fan_length,
                        areaM2=s["web"]["A"], addition=1.05),
        "thetaWebs": dict(count=s["nThetaWebs"], eachM=s["thetaWebLenM"],
                          lengthM=s["nThetaWebs"] * s["thetaWebLenM"], areaM2=s["thetaWebAM2"], addition=1.05),
    }
    for name, family in families.items():
        family["baseKgPerM"] = family["areaM2"] * rho
        family["massT"] = family["lengthM"] * family["baseKgPerM"] * family["addition"] / 1000
        close(family["massT"], row["ledgerT"][name])
    # The cap grid is an areal allocation, including the separate bending-bar bill.
    cap_area = 4 * math.pi * g["R"] ** 2
    cap_grid = dict(areaM2=cap_area, axialKgM2=rho * row["sf"] * m.P_ATM * g["R"] / 1.45e9,
                    bendingKgM2=w["barKgM2"], massT=w["capGridT"])
    close(cap_grid["massT"], cap_area * (cap_grid["axialKgM2"] + cap_grid["bendingKgM2"]) / 1000)
    return dict(families=families, capGrid=cap_grid,
                basis="Continuous/equivalent model lengths. Inner rings use maximum inner circumference even on caps; fan count may be fractional. No fabrication or joint-detail completeness is implied.")


def no_credit_modes(m, row):
    """Independent arithmetic for the frozen ring/crimp series sum, n=2..12."""
    g, w, s = row["geom"], row["wall"], row["skeleton"]
    rho, young = (m.MATERIALS["T700_LAM"][key] for key in ("rho", "E"))
    extra = s["flangeDoublerT"] * 1000 / (rho * 2 * math.pi * g["R"] * g["cylL"])
    outer = w["ring"]["A"] / m.SHIP0["ringPitchM"] + extra
    inner = s["innerRingAM2"] / m.SHIP0["bayM"]
    inertia = outer * inner / (outer + inner) * g["depthM"] ** 2
    cosine = g["braceM"] / s["thetaWebLenM"]
    crimp = 2 * young * s["thetaWebAM2"] * g["depthM"] * cosine ** 2 / (
        m.SHIP0["bayM"] * s["thetaWebLenM"] * g["R"])
    modes = []
    for n in range(2, 13):
        ring = (n * n - 1) * young * inertia / g["R"] ** 3
        q = row["giKnockdown"] / (1 / ring + 1 / crimp)
        modes.append(dict(n=n, capacityPa=q, marginAtSF=q / (m.P_ATM * row["sf"]),
                          foundationPa=0.0, membranePa=0.0))
    # Cap sizing can add theta material after the frozen ovalisation result.
    assert min(v["marginAtSF"] for v in modes) >= s["ovalization"]["marginAtSF"] - 1e-10
    return modes


def calculate():
    for name, wanted in PINS.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == wanted, name
    spec = importlib.util.spec_from_file_location("i008_frozen_model", ROOT / "research/analysis/vacuum-cell.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    saved = m.SHIP0["eSpoke"]
    cases = []
    try:
        # Private instance only. Zero is a capacity switch for NO INSTALLED NET,
        # not a new material property. The source file is never changed.
        m.SHIP0["eSpoke"] = 0.0
        for diameter in (80.0, 112.0):
            args = dict(sigma_key="s1450", sf=1.2, dia_m=diameter, gi_knockdown=0.65,
                        gi_chordal=False, gi_membrane=False, basis="favourable")
            row = m.ship0(**args)
            assert row["ledgerT"]["spokes"] == 0.0 and row["skeleton"]["spokeAM2PerM2"] == 0.0
            close(sum(row["ledgerT"].values()), row["totalT"])
            volume = row["geom"]["vM3"] - row["geom"]["areaM2"] * 0.03125
            # Prescribed screening state: uniform dry air, 1000 Pa, 288.15 K.
            # Keep full-vacuum structural demand; do not also subtract gas from lift.
            gas = 1000.0 * volume / (287.05 * 288.15) / 1000
            subtotal = row["totalT"] + gas
            altitudes = []
            for altitude, field in ((0, "liftSLT"), (2500, "lift2500T")):
                lift = m.rho_air(altitude) * volume / 1000
                close(lift, row[field])
                altitudes.append(dict(altitudeM=altitude, rhoAirKgM3=m.rho_air(altitude), liftT=lift,
                                      idealVacuumHullMarginT=lift - row["totalT"],
                                      knownSubtotalMarginT=lift - subtotal,
                                      volumeLossOnePercentCostT=0.01 * lift))
            cases.append(dict(arguments=args, model=row, memberTakeoff=takeoff(m, row),
                              noCreditModes=no_credit_modes(m, row), effectiveVolumeM3=volume,
                              gas=dict(pressurePa=1000.0, temperatureK=288.15, gasConstant=287.05, massT=gas,
                                       per100PaT=gas / 10), knownSubtotalT=subtotal, at=altitudes,
                              allUpMassT=None, allUpMarginT=None, physicalConfidence="UNKNOWN"))
    finally:
        m.SHIP0["eSpoke"] = saved
    ledger = json.loads((ROOT / "research/analysis/float-ledger.json").read_text())
    sizes = next(d for d in ledger["designs"] if d["id"] == "sizes")
    ids = {f"hull-{d}m/both-moves/gamma-0.65/chord-1450/sf-1.2" for d in (80, 112)}
    historical = [c for c in sizes["cases"] if c["id"] in ids]
    assert len(historical) == 2
    current = cases[0]
    gap = -current["at"][0]["knownSubtotalMarginT"]
    frame = (current["model"]["ledgerT"]["innerRings"] + current["model"]["ledgerT"]["thetaWebs"]) / 0.85
    g = current["model"]["geom"]
    next_length = math.sqrt(g["R"] ** 2 + g["rIn"] ** 2 - 2 * g["R"] * g["rIn"] * math.cos(4 * math.pi / g["nLong"]))
    return dict(unit="R3-I008", sourceRevision="afb2c2d1726b9d9a805f9781085c3dd6a52913e5", sourceHashes=PINS,
                modelCalls=2, noNetSwitch=dict(parameter="SHIP0.eSpoke", originalPa=saved, scenarioValuePa=0.0,
                                             sourceUnchanged=True, meaning="No installed cords, anchors or credited net stiffness."),
                cases=cases, historicalBothMovesSensitivity=historical,
                result="FAIL for this member bill; all-up mass and physical confidence UNKNOWN",
                nextGeometry=dict(diameterM=80, change="Reprice a two-column circumferential X-web panel, outer j to inner j+/-2, at unchanged diameter/depth and with no net/membrane credit.",
                                  angleRad=4 * math.pi / g["nLong"], straightEndpointLengthM=next_length,
                                  tested=False, requiredSeaLevelSavingT=gap, savingPercentCurrentHull=100 * gap / current["model"]["totalT"],
                                  currentInnerAndThetaIncludingJointsT=frame, maximumRemainingFrameBillT=frame-gap,
                                  requiredCurrentPitchErectionClampCapacityN=1.5 * current["model"]["unpressurised"]["erectionClampN"]))


def drawing(data):
    """Dimensioned family sketch; selected lines only, not a fabrication drawing."""
    g = data["cases"][0]["model"]["geom"]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 730" role="img" aria-labelledby="title desc">',
             '<title id="title">R3-I008: 80 m capsule without a tension net</title>',
             '<desc id="desc">Side elevation and barrel section show the 80 by 160 metre capsule, 4.615 metre wall depth and 111 column positions. The fan detail shows a 2 metre bay. Capacity and fabrication remain unqualified.</desc>',
             '<style>text{font:16px sans-serif;fill:#172b45}.small{font-size:13px}.label{font-weight:700}.frame{fill:none;stroke:#243c57;stroke-width:2}.inner{fill:none;stroke:#028078;stroke-width:2}.detail{fill:none;stroke:#ac4d13;stroke-width:2}.dim{fill:none;stroke:#77879b;stroke-width:1}</style>',
             '<rect width="1100" height="730" fill="#fafcfe"/>',
             '<text x="50" y="35" class="label">R3-I008 · 80 m capsule · SF1.2 screening geometry · no installed tension net</text>',
             '<text x="50" y="60" class="small">Conceptual family drawing. Selected members shown; the bill uses the frozen continuous/equivalent take-off.</text>',
             '<rect x="60" y="90" width="480" height="240" rx="120" class="frame"/>',
             f'<rect x="{60+3*g["depthM"]:.3f}" y="{90+3*g["depthM"]:.3f}" width="{480-6*g["depthM"]:.3f}" height="{240-6*g["depthM"]:.3f}" rx="{3*g["rIn"]:.3f}" class="inner"/>']
    for x in range(180, 421, 24):
        parts.append(f'<path d="M{x} 90V330" class="dim"/>')
    for y in (120, 165, 210, 255, 300):
        parts.append(f'<path d="M180 {y}H420" class="inner"/>')
    parts.extend(['<path d="M60 350V375M540 350V375M60 365H540" class="dim"/>',
                  '<text x="250" y="390">160 m overall</text>',
                  '<text x="223" y="205" class="label">80 m barrel</text>',
                  '<text x="65" y="420" class="small">Heads: hemispheres R40 m · inner radius 35.385 m · cap grid is an areal allocation</text>',
                  '<circle cx="825" cy="210" r="120" class="frame"/>',
                  f'<circle cx="825" cy="210" r="{3*g["rIn"]:.3f}" class="inner"/>'])
    for j in range(g["nLong"]):
        angle=2*math.pi*j/g["nLong"]
        parts.append(f'<circle cx="{825+120*math.cos(angle):.3f}" cy="{210+120*math.sin(angle):.3f}" r="1.6" fill="#243c57"/>')
    for j in range(0,g["nLong"],14):
        angle=2*math.pi*j/g["nLong"]
        parts.append(f'<path d="M{825+120*math.cos(angle):.3f} {210+120*math.sin(angle):.3f}L{825+3*g["rIn"]*math.cos(angle):.3f} {210+3*g["rIn"]*math.sin(angle):.3f}" class="dim"/>')
    parts.extend(['<text x="753" y="203" class="label">No cords</text>',
                  '<text x="739" y="226">No foundation credit</text>',
                  '<path d="M705 350V375M945 350V375M705 365H945" class="dim"/>',
                  '<text x="775" y="390">80 m diameter</text>',
                  '<text x="710" y="417" class="small">111 column positions · pitch 2.264 m</text>',
                  '<text x="60" y="460" class="label">Local meridional fan detail (enlarged, not the elevation scale)</text>',
                  '<path d="M100 500H500M100 630H500" class="frame"/>',
                  '<path d="M150 500L300 630L450 500" class="detail"/>',
                  '<path d="M150 480H450M150 473V487M450 473V487M520 500V630M513 500H527M513 630H527" class="dim"/>',
                  '<text x="267" y="476" class="small">2 m bay</text>',
                  '<text x="530" y="570" class="small">4.615 m depth</text>',
                  '<text x="137" y="575" class="small">4.722 m leg</text>',
                  '<text x="60" y="668" class="small">Fan tube 130 × 1 mm; outer hoop 166 × 6 mm; longeron 182 × 8 mm (OD × wall).</text>',
                  '<text x="685" y="470" class="label">Explicit limits</text>',
                  '<text x="685" y="500">Film grid: 0.5 m; film SF4.</text>',
                  '<text x="685" y="530">No in-surface membrane credit.</text>',
                  '<text x="685" y="560">Inner/θ areas need realised sections.</text>',
                  '<text x="685" y="590">Caps, joints and terminations unresolved.</text>',
                  '<text x="685" y="620">Erection-wind clamps fail the model.</text>',
                  '<text x="60" y="707" class="label">FAIL for this member bill · all-up mass and physical confidence UNKNOWN</text>', '</svg>'])
    svg = '\n'.join(parts)+'\n'
    # Presentation attributes also support SVG renderers with limited CSS support.
    for name, colour, width in (("frame", "#243c57", 2), ("inner", "#028078", 2),
                                ("detail", "#ac4d13", 2), ("dim", "#77879b", 1)):
        svg = svg.replace(f'class="{name}"',
                          f'class="{name}" fill="none" stroke="{colour}" stroke-width="{width}"')
    return svg


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data=calculate()
    outputs={'budget.json':json.dumps(data,indent=2,allow_nan=False)+'\n','geometry.svg':drawing(data)}
    if args.write:
        for name,text in outputs.items(): (HERE/name).write_text(text)
    elif args.check:
        for name,text in outputs.items():
            assert (HERE/name).read_text()==text, f'{name} differs from the two-case calculation'
        print('R3-I008: PASS for reproduction, component/length sums, lift and no-credit mode arithmetic; physical confidence UNKNOWN.')
    else:
        print(outputs['budget.json'],end='')


if __name__ == '__main__':
    main()
