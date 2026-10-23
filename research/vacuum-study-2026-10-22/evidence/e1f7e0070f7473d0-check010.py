#!/usr/bin/env python3
"""Independent check of MAINLINE-010. Does not run the owner's script.

Formulas stated here, from COMMON.md and the card's mass rules:
  ISA: T = T0 - lapse*h
       p = p0 * (T/T0) ** (g0 / (lapse * Rspec))
       rho = p / (Rspec * T)
  g0 = 9.80665 m/s^2 (ISO 2533). The card names T0, p0, lapse and Rspec=287.05, not g0.
  The pinned 001 column used Rspec=287.053. This script uses the card's 287.05.
  lift = rho * (4/3)*pi*R^3 * (1-f)     # internal gas at the same T, p_int=f*p
  p_net = p * (1-f)
  buckling = kd * 4 * tf * separation * E / (R^2 * sqrt(1-nu^2))
  yield    = 4 * sigma * tf / R
  crush    = p_net / 2
  SF       = allowable / p_net
  mass     = (faces + core) * (1 + joint_fraction) + systems_per_sphere * n
  faces    = rho_al * area * 2 * tf
  core     = rho_core * area * core_thickness
  area     = 4 * pi * R^2
  margin   = (lift_total - mass_total) / lift_total
Cluster: total lift held at the single 10 m lift, each radius = 10 * n**(-1/3),
systems = 100 kg on every sphere.
"""

import hashlib
import json
import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

E = 68.9e9
NU = 0.33
SIG = 276e6
RHO_AL = 2700.0
RHO_CORE = 16.0
JOINT = 0.05
SYS = 100.0
KD = 0.2
T0 = 288.15
P0 = 101325.0
LAPSE = 0.0065
RSPEC = 287.05  # card INPUTS, not the pinned 287.053
G0 = 9.80665
R0 = 10.0

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

mismatches = []
worst = 0.0
ncomp = 0


def sha256(path):
    h = hashlib.sha256()
    data = Path(path).read_bytes()
    h.update(data)
    return h.hexdigest(), len(data)


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def check(row, field, card, mine, tol=1e-12):
    global worst, ncomp
    ncomp += 1
    d = rel(card, mine)
    worst = max(worst, d)
    if d > tol:
        mismatches.append((row, field, card, mine, d))


def half_up(value, nd):
    q = Decimal(1).scaleb(-nd)
    return Decimal(format(value, ".20f")).quantize(q, rounding=ROUND_HALF_UP)


def isa(h):
    T = T0 - LAPSE * h
    p = P0 * (T / T0) ** (G0 / (LAPSE * RSPEC))
    rho = p / (RSPEC * T)
    return T, p, rho


def sphere_volume(R):
    return (4.0 / 3.0) * math.pi * R ** 3


def sphere_area(R):
    return 4.0 * math.pi * R ** 2


def pressures(tf, sep, R, p_net):
    buckling = KD * 4.0 * tf * sep * E / (R ** 2 * math.sqrt(1.0 - NU ** 2))
    yield_p = 4.0 * SIG * tf / R
    return buckling, yield_p, buckling / p_net, yield_p / p_net, p_net / 2.0


def one_mass(R, tf, core, n_systems=1.0):
    area = sphere_area(R)
    faces = RHO_AL * area * 2.0 * tf
    core_m = RHO_CORE * area * core
    return (faces + core_m) * (1.0 + JOINT) + SYS * n_systems


def case_single(tf, core, sep, R, h, f):
    _T, p, rho = isa(h)
    p_net = p * (1.0 - f)
    lift = rho * sphere_volume(R) * (1.0 - f)
    mass = one_mass(R, tf, core)
    margin = (lift - mass) / lift
    buckling, yield_p, sf_b, sf_y, crush = pressures(tf, sep, R, p_net)
    struct = mass - SYS
    # Systems scaled with displaced volume, joints stay a fraction of sandwich.
    mass_scaled = struct + SYS * (R / R0) ** 3
    margin_scaled = (lift - mass_scaled) / lift
    return {
        "R_m": R,
        "mass_kg": mass,
        "lift_kg": lift,
        "float_margin": margin,
        "buckling_SF": sf_b,
        "yield_SF_QUESTIONABLE": sf_y,
        "crush_stress_Pa": crush,
        "buckling_Pa": buckling,
        "yield_Pa": yield_p,
        "p_net_Pa": p_net,
        "p_Pa": p,
        "rho_air": rho,
        "margin_if_systems_scaled_with_lift": margin_scaled,
        "allowance_spread_gain": margin - margin_scaled,
    }


def case_cluster(tf, core, sep, n, h=500.0, f=0.0):
    r = R0 * n ** (-1.0 / 3.0)
    _T, p, rho = isa(h)
    p_net = p * (1.0 - f)
    # Total lift held equal to one 10 m sphere. Radius is the cube-root split.
    lift = rho * sphere_volume(R0) * (1.0 - f)
    mass = one_mass(r, tf, core) * n
    margin = (lift - mass) / lift
    buckling, yield_p, sf_b, sf_y, crush = pressures(tf, sep, r, p_net)
    return {
        "R_m": r,
        "r_m": r,
        "n": n,
        "mass_kg": mass,
        "lift_kg": lift,
        "float_margin": margin,
        "buckling_SF": sf_b,
        "yield_SF_QUESTIONABLE": sf_y,
        "crush_stress_Pa": crush,
        "buckling_Pa": buckling,
        "yield_Pa": yield_p,
        "p_net_Pa": p_net,
    }


def load_geometry():
    r2 = json.loads(PIN002.read_text())
    r3 = json.loads(PIN003.read_text())
    p2a = next(row for row in r2["rows"] if row["point_id"] == "P2-A")
    text = p2a["geometry"]
    tf_a = float(re.search(r"tf=([0-9.]+) m", text).group(1))
    core_a = float(re.search(r"core=([0-9.]+) m", text).group(1))
    p2e = next(row for row in r3["rows"] if row["point_id"] == "P2-E")
    tf_e = p2e["geometry"]["tf_m"]
    core_e = p2e["geometry"]["core_m"]
    sep_e = p2e["geometry"]["d_m"]
    return {
        "P2-A": {"tf": tf_a, "core": core_a, "sep": core_a + tf_a, "mass0": p2a["all_mass_kg"]},
        "P2-E": {"tf": tf_e, "core": core_e, "sep": sep_e, "mass0": p2e["all_mass_kg"]},
    }


def compare_dict(row_name, card, mine, keys):
    for key in keys:
        check(row_name, key, float(card[key]), float(mine[key]))


def display_equal(token, value):
    nd = len(token.split(".")[1]) if "." in token else 0
    rounded = half_up(value, nd)
    if nd == 0:
        text = format(rounded, "f").split(".")[0]
    else:
        text = format(rounded, f".{nd}f")
    return text == token


def parse_tables(card_text):
    sections = re.split(r"\n## ", card_text)
    tables = {}
    for section in sections:
        if section.startswith("Lever 1"):
            key = "1"
        elif section.startswith("Lever 2"):
            key = "2"
        elif section.startswith("Lever 3"):
            key = "3"
        elif section.startswith("Lever 4"):
            key = "4"
        else:
            continue
        rows = []
        for line in section.splitlines():
            if not line.startswith("| P2-"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
        tables[key] = rows
    return tables


def main():
    pin_ok = 0
    for path, digest, nbytes in PINS:
        got, n = sha256(path)
        if got == digest and n == nbytes:
            pin_ok += 1
        else:
            print(f"PIN MISMATCH {path} {got} {n} expected {digest} {nbytes}")
    print(f"pins {pin_ok}/{len(PINS)}")

    common_sha, common_n = sha256(COMMON)
    print(f"COMMON {common_sha} {common_n}")

    owner = json.loads(OWNER_RPT.read_text())
    for art in owner["artifacts"]:
        got, n = sha256(art["path"])
        status = "ok" if got == art["sha256"] and n == art["bytes"] else "MISMATCH"
        print(f"owner artifact {status} {Path(art['path']).name} {n}")

    geom = load_geometry()
    inputs = json.loads((CARD_DIR / "INPUTS.json").read_text())
    for name, g in geom.items():
        stated = inputs["baselines"][name]
        check(name + " inputs", "tf", stated["tf_m"], g["tf"], tol=0.0)
        check(name + " inputs", "core", stated["core_m"], g["core"], tol=0.0)
        check(name + " inputs", "separation", stated["separation_m"], g["sep"], tol=0.0)
        print(f"{name} tf {g['tf']} core {g['core']} sep {g['sep']} mass0 {g['mass0']}")

    pin_p = json.loads(PIN001.read_text())["atmosphere"]["p_ext_Pa"]
    _T, p500, rho500 = isa(500.0)
    print(f"p500 {p500:.12f} pin {pin_p:.12f} delta {p500 - pin_p:.6f} Pa")
    print(f"within 0.1 Pa {abs(p500 - pin_p) < 0.1}")

    results = json.loads((CARD_DIR / "RESULTS.json").read_text())
    print(f"tag {results['tag']}")

    built = {"1": {}, "2": {}, "3": {}, "4": {}}
    for name, g in geom.items():
        built["1"][name] = [case_single(g["tf"], g["core"], g["sep"], R, 500.0, 0.0) for R in (5.0, 10.0, 20.0, 40.0)]
        built["2"][name] = []
        for h in (0.0, 500.0, 2000.0, 5000.0):
            row = case_single(g["tf"], g["core"], g["sep"], R0, h, 0.0)
            row["alt_m"] = h
            built["2"][name].append(row)
        built["3"][name] = []
        for f in (0.0, 0.1, 0.25, 0.5):
            row = case_single(g["tf"], g["core"], g["sep"], R0, 500.0, f)
            row["f_int"] = f
            built["3"][name].append(row)
        built["4"][name] = [case_cluster(g["tf"], g["core"], g["sep"], n) for n in (1, 4, 8, 27)]

    lever_keys = {
        "1_radius": ["R_m", "mass_kg", "lift_kg", "float_margin", "buckling_SF", "yield_SF_QUESTIONABLE", "crush_stress_Pa", "buckling_Pa", "yield_Pa", "p_net_Pa", "margin_if_systems_scaled_with_lift", "allowance_spread_gain"],
        "2_altitude": ["R_m", "mass_kg", "lift_kg", "float_margin", "buckling_SF", "yield_SF_QUESTIONABLE", "crush_stress_Pa", "buckling_Pa", "yield_Pa", "p_net_Pa", "alt_m", "p_Pa", "rho_air"],
        "3_partial_vacuum": ["R_m", "mass_kg", "lift_kg", "float_margin", "buckling_SF", "yield_SF_QUESTIONABLE", "crush_stress_Pa", "buckling_Pa", "yield_Pa", "p_net_Pa", "f_int"],
        "4_cluster": ["R_m", "mass_kg", "lift_kg", "float_margin", "buckling_SF", "yield_SF_QUESTIONABLE", "crush_stress_Pa", "buckling_Pa", "yield_Pa", "p_net_Pa", "n", "r_m"],
    }
    index = {"1_radius": "1", "2_altitude": "2", "3_partial_vacuum": "3", "4_cluster": "4"}
    for lever_name, keys in lever_keys.items():
        for geom_name, card_rows in results["levers"][lever_name].items():
            mine_rows = built[index[lever_name]][geom_name]
            if len(card_rows) != len(mine_rows):
                print(f"ROW COUNT {lever_name} {geom_name} card {len(card_rows)} mine {len(mine_rows)}")
            for card_row, mine_row in zip(card_rows, mine_rows):
                label = f"{lever_name} {geom_name} R={card_row.get('R_m')} alt={card_row.get('alt_m')} f={card_row.get('f_int')} n={card_row.get('n')}"
                compare_dict(label, card_row, mine_row, keys)

    base_keys = ["R_m", "mass_kg", "lift_kg", "float_margin", "buckling_SF", "yield_SF_QUESTIONABLE", "crush_stress_Pa", "buckling_Pa", "yield_Pa", "p_net_Pa"]
    for geom_name, card_row in results["baseline_10m_500m"].items():
        mine_row = built["1"][geom_name][1]
        compare_dict(f"baseline {geom_name}", card_row, mine_row, base_keys)

    # Equal-margin identity and a real thickness rescale.
    print("--- rescale ---")
    for geom_name, g in geom.items():
        base = built["3"][geom_name][0]
        for row in built["3"][geom_name]:
            f = row["f_int"]
            if f == 0.0:
                continue
            ident_b = row["buckling_SF"] * (1.0 - f)
            ident_y = row["yield_SF_QUESTIONABLE"] * (1.0 - f)
            print(
                f"identity {geom_name} f={f} buckling {ident_b:.16g} vs {base['buckling_SF']:.16g} "
                f"yield {ident_y:.16g} vs {base['yield_SF_QUESTIONABLE']:.16g}"
            )
            # Faces and core scale together. Systems stay 100 kg per sphere.
            target = base["mass_kg"] * (1.0 - f)
            struct0 = base["mass_kg"] - SYS
            scale = (target - SYS) / struct0
            sf_b = base["buckling_SF"] * scale * scale / (1.0 - f)
            sf_y = base["yield_SF_QUESTIONABLE"] * scale / (1.0 - f)
            print(
                f"rescale-fixed-systems {geom_name} f={f} s={scale:.16g} "
                f"buckling_SF {sf_b:.16g} yield_SF {sf_y:.16g} "
                f"baseline_b {base['buckling_SF']:.16g} baseline_y {base['yield_SF_QUESTIONABLE']:.16g}"
            )
            # Systems also scale with the floatable mass.
            scale_s = 1.0 - f
            sf_b2 = base["buckling_SF"] * scale_s
            sf_y2 = base["yield_SF_QUESTIONABLE"]
            print(
                f"rescale-systems-with-lift {geom_name} f={f} s={scale_s:.16g} "
                f"buckling_SF {sf_b2:.16g} yield_SF {sf_y2:.16g}"
            )

    both_pass = []
    for lever_name, geoms in built.items():
        for geom_name, rows in geoms.items():
            for row in rows:
                if row["buckling_SF"] >= 1.0 and row["yield_SF_QUESTIONABLE"] >= 1.0:
                    both_pass.append((lever_name, geom_name, row.get("n", row["R_m"]), row["buckling_SF"], row["yield_SF_QUESTIONABLE"], row["mass_kg"] / row["lift_kg"]))
    print("both SF pass 1:", both_pass)

    e27 = built["4"]["P2-E"][-1]
    e10 = built["1"]["P2-E"][1]
    e5 = built["1"]["P2-E"][0]
    print(f"ratio n27 buckling {e27['buckling_SF'] / e10['buckling_SF']:.12f}")
    print(f"ratio R5 buckling {e5['buckling_SF'] / e10['buckling_SF']:.12f}")
    e5000 = built["2"]["P2-E"][-1]
    print(f"ratio 5000 buckling {e5000['buckling_SF'] / e10['buckling_SF']:.12f}")
    print(f"mass/lift n27 {e27['mass_kg'] / e27['lift_kg']:.12f}")
    for row in built["1"]["P2-E"]:
        print(
            f"spread R={row['R_m']} gain {row['allowance_spread_gain']:.12f} "
            f"margin {row['float_margin']:.12f}"
        )

    card_text = (CARD_DIR / "CARD.md").read_text()
    tables = parse_tables(card_text)
    display_bad = []

    def expect(cells, values):
        # values aligned with the numeric cells after the geometry name
        for token, value in zip(cells[1:], values):
            if not display_equal(token, value):
                display_bad.append((token, value, str(half_up(value, len(token.split('.')[1]) if '.' in token else 0))))

    for cells in tables["1"]:
        geom_name, radius = cells[0], float(cells[1])
        row = next(r for r in built["1"][geom_name] if r["R_m"] == radius)
        expect(cells, [radius, row["float_margin"], row["buckling_SF"], row["yield_SF_QUESTIONABLE"], row["crush_stress_Pa"]])
    for cells in tables["2"]:
        geom_name, alt = cells[0], float(cells[1])
        row = next(r for r in built["2"][geom_name] if r["alt_m"] == alt)
        expect(cells, [alt, row["float_margin"], row["buckling_SF"], row["yield_SF_QUESTIONABLE"], row["crush_stress_Pa"]])
    for cells in tables["3"]:
        geom_name, frac = cells[0], float(cells[1])
        row = next(r for r in built["3"][geom_name] if abs(r["f_int"] - frac) < 1e-15)
        expect(cells, [frac, row["float_margin"], row["buckling_SF"], row["yield_SF_QUESTIONABLE"], row["crush_stress_Pa"]])
    for cells in tables["4"]:
        geom_name, n = cells[0], int(cells[1])
        row = next(r for r in built["4"][geom_name] if r["n"] == n)
        expect(cells, [n, row["R_m"], row["float_margin"], row["buckling_SF"], row["yield_SF_QUESTIONABLE"], row["crush_stress_Pa"]])

    num = r"([0-9]+\.[0-9]+|[0-9]+)"
    intro_a = re.search(rf"P2-A buckling SF {num}, yield SF {num}, margin {num}", card_text)
    intro_e = re.search(rf"P2-E buckling SF {num}, yield SF {num}, margin {num}", card_text)
    base_a = built["1"]["P2-A"][1]
    base_e = built["1"]["P2-E"][1]
    for label, match, row in (("intro P2-A", intro_a, base_a), ("intro P2-E", intro_e, base_e)):
        tokens = match.groups()
        vals = [row["buckling_SF"], row["yield_SF_QUESTIONABLE"], row["float_margin"]]
        for token, value in zip(tokens, vals):
            if not display_equal(token, value):
                display_bad.append((label + " " + token, value, "intro"))
    print(f"display mismatches {len(display_bad)}")
    for item in display_bad:
        print("DISPLAY", item)

    # Filing order of 007 and 008 against this card.
    print(f"card at {owner['at']}")
    print(f"007 at {json.loads(RPT007.read_text())['at']}")
    print(f"008 at {json.loads(RPT008.read_text())['at']}")

    print(f"comparisons {ncomp} worst_rel {worst:.6e} numeric_mismatches {len(mismatches)}")
    for item in mismatches:
        print("MISMATCH", item)


if __name__ == "__main__":
    main()
