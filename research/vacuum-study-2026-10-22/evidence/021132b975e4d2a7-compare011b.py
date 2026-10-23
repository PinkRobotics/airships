#!/usr/bin/env python3
"""Compare the checker's own MAINLINE-011b numbers (check011b.py -> RESULTS.json) with the owner's filed card.

The owner's RESULTS.json and CARD.md are read here and nowhere else, after the checker's numbers exist.
Writes COMPARE.json beside the checker's RESULTS.json and prints every mismatch.
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline011b-check-1019"
OWNER = Path("unpublished-local-ref:6d6611b67d773afa"
             "vacuum-mainline011b-p3-global-arcs-1019")
MODES = ("yield", "euler", "local", "film", "perry", "global")


def rel(a, b):
    if a == b:
        return 0.0
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def grade(a, b):
    r = rel(a, b)
    return "match_1e-9" if r <= 1e-9 else ("match_1e-6" if r <= 1e-6 else "MISMATCH")


def main():
    mine = json.loads((OUT / "RESULTS.json").read_text())
    own = json.loads((OWNER / "RESULTS.json").read_text())
    card = (OWNER / "CARD.md").read_text()
    cmp = {"rows": [], "named": [], "card_table": [], "summary": {}}

    def key(r):
        return (r["material"], r["grid"], float(r["k"]))

    my_grid = {key(r): r for r in mine["primary_joints_on_grid"]}
    my_ref = {key(r): r for r in mine["primary_joints_on_refined"]}
    my_solid = {key(r): r for r in mine["primary_joints_on_grid_solid_start"]}
    per_s = mine["refined_best_ro_per_grid_s"]
    for mat, rows in own["primary_joints_on"].items():
        for o in rows:
            k = (o["material"], o["grid"], float(o["k"]))
            m, f, so = my_grid[k], my_ref[k], my_solid[k]
            fields = []
            for name, ov, mv in (("s_m", o["s_m"], m["s_m"]), ("r_o_m", o["r_o_m"], m["r_o_m"]),
                                 ("t_w_m", o["t_w_m"], m["t_w_m"]), ("m_nodes_kg", o["m_nodes_kg"], m["m_nodes_kg"]),
                                 ("m_joint_kg", o["m_joint_kg"], m["m_joint_kg"]),
                                 ("m_tube_kg", o["m_tube_kg"], m["m_tube_kg"]), ("total_kg", o["total_kg"], m["total_kg"]),
                                 ("SF_least", o["SF_least"], m["SF_least"]),
                                 ("sigma_axial_Pa", o["sigma_axial_Pa"], m["sigma_axial_Pa"])) + tuple(
                    ("SF_" + md, o["SF_" + md], m["SF"][md]) for md in MODES):
                fields.append({"field": name, "card": ov, "mine": mv, "rel": rel(ov, mv), "grade": grade(ov, mv)})
            fields.append({"field": "governing", "card": o["governing"], "mine": m["governs"],
                           "grade": "match" if o["governing"] == m["governs"] else "MISMATCH"})
            fields.append({"field": "second", "card": o["second"], "mine": m["second"],
                           "grade": "match" if o["second"] == m["second"] else "MISMATCH"})
            cs = per_s[f"{k[0]}|{k[1]}|{k[2]}"].get(f"{o['s_m']:.2f}")
            cmp["rows"].append({
                "material": k[0], "grid": k[1], "k": k[2], "fields": fields,
                "refined": {"SF_least": f["SF_least"], "s_m": f["s_m"], "r_o_m": f["r_o_m"], "t_w_m": f["t_w_m"],
                            "governs": f["governs"], "second": f["second"],
                            "gain_over_card": f["SF_least"] / o["SF_least"] - 1},
                "continuous_at_card_s": {"SF_least": cs[0], "r_o_m": cs[1],
                                         "gain_over_card": cs[0] / o["SF_least"] - 1} if cs else None,
                "solid_start_grid": {"SF_least": so["SF_least"], "s_m": so["s_m"], "r_o_m": so["r_o_m"],
                                     "rel_SF_vs_card": rel(so["SF_least"], o["SF_least"])}})
    # the 36-row CARD.md table (r_o and t_w in mm there)
    pat = re.compile(r"^\| (\S+) \| (\S+) \| ([\d.]+) \| ([\d.]+) \| (\w+) \| (\w+) \| ([\d.]+) \| ([\d.]+) \| "
                     r"([\d.]+) \| ([\d.]+) \| ([\d.]+) \|$")
    for line in card.splitlines():
        mm = pat.match(line.strip())
        if not mm:
            continue
        mat, grid, k, sf, gov, sec, s, ro, tw, nk, jk = mm.groups()
        m = my_grid[(mat, grid, float(k))]
        out = {"material": mat, "grid": grid, "k": float(k), "fields": []}
        for name, cv, mv in (("least SF", float(sf), m["SF_least"]), ("s m", float(s), m["s_m"]),
                             ("r_o mm", float(ro), m["r_o_m"] * 1e3), ("t_w mm", float(tw), m["t_w_m"] * 1e3),
                             ("nodes kg", float(nk), m["m_nodes_kg"]), ("joints kg", float(jk), m["m_joint_kg"])):
            out["fields"].append({"field": name, "card": cv, "mine": mv, "rel": rel(cv, mv), "grade": grade(cv, mv)})
        out["fields"].append({"field": "governs", "card": gov, "mine": m["governs"],
                              "grade": "match" if gov == m["governs"] else "MISMATCH"})
        out["fields"].append({"field": "second", "card": sec, "mine": m["second"],
                              "grade": "match" if sec == m["second"] else "MISMATCH"})
        cmp["card_table"].append(out)
    # named numbers in CARD.md / the report body
    rp, ft = mine["rounded_point"], mine["filed_011_tube"]
    sens380 = {(r["grid"], r["k"]): r for r in mine["sens_SiC_380MPa"]}
    joff = {(r["grid"], r["k"]): r for r in mine["sens_6061_joints_off"]}
    g6061 = my_grid[("6061-T6", "equilateral_triangular", 0.2)]
    named = [
        ("rounded two-way perfect SF", 0.702903874926, rp["SF_two_way_perfect"]),
        ("rounded k0.2", 0.140580774985, rp["SF_two_way_k"]["0.2"]),
        ("rounded k0.4", 0.281161549970, rp["SF_two_way_k"]["0.4"]),
        ("rounded k0.5", 0.351451937463, rp["SF_two_way_k"]["0.5"]),
        ("line load w N/m", 143191.256871, rp["w_N_per_m"]),
        ("arch stress GPa", 1.18499087263, rp["sigma_arch_Pa"] / 1e9),
        ("chord sag m", 0.1125, rp["sag_m"]),
        ("bending fixed-end GPa", 2.10654485172, rp["sigma_bend_fixed_Pa"] / 1e9),
        ("bending simple GPa", 3.15981727758, rp["sigma_bend_simple_Pa"] / 1e9),
        ("filed tube Perry, joints off", 0.178765809625, ft["SF"]["perry"]),
        ("filed tube global k0.2 equilateral", 0.172381843325, ft["SF"]["global"]),
        ("SiC at 380 MPa, equilateral k0.2 (Perry)", 0.26224593556,
         sens380[("equilateral_triangular", 0.2)]["SF_least"]),
        ("6061 joints off, equilateral k0.2 (Perry)", 0.226595470313,
         joff[("equilateral_triangular", 0.2)]["SF_least"]),
        ("regression SF (011 filed 0.23313387024769294)", 0.23313387024769294,
         mine["regression_011"]["owner_grid"]["SF"]),
        ("regression r_o (011 filed)", 0.0866221663456903, mine["regression_011"]["owner_grid"]["r_o"]),
    ]
    for name, cv, mv in named:
        cmp["named"].append({"name": name, "card": cv, "mine": mv, "rel": rel(cv, mv), "grade": grade(cv, mv)})
    cmp["named"].append({"name": "6061 equilateral k0.2 chord sag vs r_o (m)",
                         "card": "inside the tube radius", "mine": [g6061["s_m"] ** 2 / 80, g6061["r_o_m"]],
                         "grade": "match" if g6061["s_m"] ** 2 / 80 < g6061["r_o_m"] else "MISMATCH"})
    cmp["named"].append({"name": "governing modes for SiC at 380 MPa and 6061 joints off",
                         "card": "perry, perry",
                         "mine": [sens380[("equilateral_triangular", 0.2)]["governs"],
                                  joff[("equilateral_triangular", 0.2)]["governs"]]})
    # summary
    allf = [f for r in cmp["rows"] for f in r["fields"]] + [f for r in cmp["card_table"] for f in r["fields"]] + \
        [n for n in cmp["named"] if "grade" in n]
    cmp["summary"] = {g: sum(1 for f in allf if f.get("grade") == g)
                      for g in ("match", "match_1e-9", "match_1e-6", "MISMATCH")}
    cmp["summary"]["max_refined_gain_over_card"] = max(r["refined"]["gain_over_card"] for r in cmp["rows"])
    cmp["summary"]["max_rel_solid_start_vs_card"] = max(r["solid_start_grid"]["rel_SF_vs_card"] for r in cmp["rows"])
    (OUT / "COMPARE.json").write_text(json.dumps(cmp, indent=1))
    print(json.dumps(cmp["summary"], indent=1))
    for r in cmp["rows"]:
        bad = [f for f in r["fields"] if f["grade"] == "MISMATCH"]
        if bad:
            print("ROW", r["material"], r["grid"], r["k"], [(f["field"], f["card"], f["mine"]) for f in bad])
    for r in cmp["card_table"]:
        bad = [f for f in r["fields"] if f["grade"] == "MISMATCH"]
        if bad:
            print("TABLE", r["material"], r["grid"], r["k"], [(f["field"], f["card"], f["mine"]) for f in bad])
    for n in cmp["named"]:
        print("NAMED", n["name"], n["card"], n["mine"], n.get("grade"))


if __name__ == "__main__":
    main()
