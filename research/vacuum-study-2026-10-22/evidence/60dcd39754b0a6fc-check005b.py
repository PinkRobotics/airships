#!/usr/bin/env python3
"""Independent check of MAINLINE-005b. Does not run the owner's script.

Model, as the brief's example and the card both state it:
  sigma_core = p_external / 2
Pinned p_external is the MAINLINE-001 pressure. The same value applies to every
P2 row because this model has no thickness in it.
Margin = stated_strength_Pa / sigma_core.
"""

import hashlib
import json
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

PINS = [
    ("evidence/33ee112c1cb1a4b5-CARD.md", "33ee112c1cb1a4b5fe2460554b46bd68963cb980f49b06964fe672199132c4d8", 5667),
    ("evidence/69d9ef27cb5c86f2-INPUTS.json", "69d9ef27cb5c86f2a20399210b65cfb12f911ab1c1c4cb6fdff9cca70ba14c5a", 15384),
    ("evidence/e7b2e4a33ab68eb0-RESULTS.json", "e7b2e4a33ab68eb0e195b83cb91faa86a77d7bc5b8970dfa3dd3cbae07a9cde5", 30175),
    ("evidence/63c812f02bde7cf4-CARD.md", "63c812f02bde7cf43d029e423b360014f9bb73c233bf33b46e525005378a0f07", 6977),
    ("evidence/f7365a5dbdda8ddd-INPUTS.json", "f7365a5dbdda8dddb18217e3a352457b372b3d0e2d94d7e692d78e62b48c7928", 1643),
    ("evidence/d728af6ca61595e1-RESULTS.json", "d728af6ca61595e116b2b133b23477cecaf54d050486202277f441234c25a2c0", 13071),
    ("evidence/b155c07e690eaa66-NFI.json", "b155c07e690eaa665db0f27994bcf36986d5ffe168aa7a45cc0ae403ddcd87a8", 2449),
    ("evidence/17dc1e39680f79f6-CARD.md", "17dc1e39680f79f6ba2fd9d3ac0ac4fba28dfc4e4c95824e55e544bbcd3f1a3e", 3907),
    ("evidence/a697a764919c3211-INPUTS.json", "a697a764919c3211bb47caf3b032d3ace7637e85971078a66ef3264beb6abbe9", 851),
    ("evidence/df5d268297e342bd-mainline003.json", "df5d268297e342bdce62fb6c4906a128e6c8729c8b56ae7a710ef9fdd73cd0db", 7995),
    ("evidence/2090c6e1f4ca8afb-NFI.json", "2090c6e1f4ca8afb62ff5a7a0e2efbe8757aa60a79a773be2fae359cdd446e97", 2978),
    ("evidence/dcfa7ae3942a9e4f-UNA600-MAINLINE003-REVIEW.md", "dcfa7ae3942a9e4f8a43ac06ff5ba62d2249d69414228ea756661cb1f020925b", 3351),
]

worst = 0.0
ncomp = 0
mismatches = []


def sha256(path):
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def check(row, field, card, mine, tol=1e-12):
    global worst, ncomp
    ncomp += 1
    d = rel(float(card), float(mine))
    worst = max(worst, d)
    if d > tol:
        mismatches.append((row, field, card, mine, d))


def half_up(value, nd):
    q = Decimal(1).scaleb(-nd)
    return Decimal(format(value, ".20f")).quantize(q, rounding=ROUND_HALF_UP)


def main():
    pin_ok = 0
    for path, digest, nbytes in PINS:
        got, n = sha256(path)
        if got == digest and n == nbytes:
            pin_ok += 1
        else:
            print(f"PIN MISMATCH {path}")
    print(f"pins {pin_ok}/{len(PINS)}")
    print("COMMON", *sha256(COMMON))

    owner = json.loads(OWNER.read_text())
    for art in owner["artifacts"]:
        got, n = sha256(art["path"])
        print(("ok" if got == art["sha256"] and n == art["bytes"] else "MISMATCH"), Path(art["path"]).name)

    p_pin = json.loads(PIN001.read_text())["atmosphere"]["p_ext_Pa"]
    required = p_pin / 2.0
    print(f"p {p_pin:.20f}")
    print(f"p/2 {required:.20f}")

    results = json.loads((CARD_DIR / "RESULTS.json").read_text())
    check("model", "p_external_Pa", results["model_QUESTIONABLE"]["p_external_Pa"], p_pin)
    check("model", "sigma_core_Pa", results["model_QUESTIONABLE"]["sigma_core_Pa"], required)
    for row, value in results["required_core_strength_Pa"].items():
        check(row, "required_core_strength_Pa", value, required)

    r005 = json.loads(PIN005.read_text())
    # Confirm the five P2 ids are the rows this model names, and that 005 used the same pressure.
    ids = []
    def walk(node):
        if isinstance(node, dict):
            if "point_id" in node:
                ids.append(node["point_id"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(r005)
    print("005 point ids", sorted(set(ids)))
    for row in ("P2", "P2-A", "P2-C", "P2-K", "P2-E"):
        if row not in ids:
            print("MISSING 005 ROW", row)

    print("--- margins ---")
    for core in results["real_cores_QUESTIONABLE"]:
        strength = core["strength_Pa"]
        if strength is None:
            print(f"{core['core']}: no strength, tag {core.get('tag')}, source {core['source']}")
            continue
        margin = strength / required
        print(f"{core['core']}: density {core['density_kg_m3']} strength {strength} margin {margin:.10f} def {core['definition']}")
        if "source" not in core or not core["source"]:
            print("NO SOURCE", core["core"])

    # 1% scaling from the only 1% point.
    eps = next(c for c in results["real_cores_QUESTIONABLE"] if c["definition"] == "1% strain")
    ratio = required / eps["strength_Pa"]
    print(f"1% point {eps['density_kg_m3']} kg/m3 at {eps['strength_Pa']} Pa, strength ratio {ratio:.6f}")
    print(f"linear density {eps['density_kg_m3'] * ratio:.6f}")
    print(f"density-squared {eps['density_kg_m3'] * ratio ** 0.5:.6f}")
    print(f"density^1.5 {eps['density_kg_m3'] * ratio ** (1.0 / 1.5):.6f}")

    card = (CARD_DIR / "CARD.md").read_text()
    # Displayed margins and the required-strength token.
    shown = {
        "47730.4": required,
        "1.05": 50000 / required,
        "11.6": 552000 / required,
        "22": 1070000 / required,
        "13": 621000 / required,
        "23": 1100000 / required,
        "2.1": 102000 / required,
        "47.7": required / 1000.0,
    }
    for token, value in shown.items():
        nd = len(token.split(".")[1]) if "." in token else 0
        got = half_up(value, nd)
        text = format(got, f".{nd}f") if nd else format(got, "f").split(".")[0]
        print(("DISPLAY OK" if text == token else "DISPLAY MISMATCH"), token, text, value)

    # Range row arithmetic, strengths taken from the card sentence.
    lo, hi = 0.8e6 / required, 3.6e6 / required
    print(f"rohacell range margins {lo:.6f} {hi:.6f} display {half_up(lo, 0)} {half_up(hi, 0)}")
    if "Rohacell range" not in card and "Rohacell RIST" not in card:
        print("range sentence missing")
    names = [c["core"] for c in results["real_cores_QUESTIONABLE"]]
    print("range row in RESULTS", any("range" in n.lower() or "RIST" in n for n in names))

    # Honeycomb and PMI margins above 10, from 20 kg/m3.
    print("--- ten times ---")
    for core in results["real_cores_QUESTIONABLE"]:
        if core["strength_Pa"] is None:
            continue
        margin = core["strength_Pa"] / required
        kind = core["core"]
        above = core["density_kg_m3"] >= 20
        print(f"  {kind}: density {core['density_kg_m3']} margin {margin:.4f} above20 {above} ten {margin >= 10}")

    print("card at", owner["at"])
    print("007 at", json.loads(RPT007.read_text())["at"])
    print(f"comparisons {ncomp} worst_rel {worst:.6e} numeric_mismatches {len(mismatches)}")
    for item in mismatches:
        print("MISMATCH", item)

    # Tags.
    header = "Every sourced value is QUESTIONABLE" in card
    print("header QUESTIONABLE", header)
    print("microlattice PROJECTION", "PROJECTION" in card and any(c.get("tag") == "PROJECTION" for c in results["real_cores_QUESTIONABLE"]))


if __name__ == "__main__":
    main()
