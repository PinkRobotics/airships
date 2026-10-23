#!/usr/bin/env python3
"""CHECK MAINLINE-029: write NFI.json and INPUTS.json from RESULTS.json (built by build_check029.py), then print the pins
(path, sha256, bytes) of the check's files for the report."""
import hashlib
import json
from pathlib import Path

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline029-check-1020"
S = ME / "work/scripts/check029"
OWN = Path("unpublished-local-ref:1a1d51aea95bb074"
           "vacuum-mainline029-crimp-gamma-fe-1020")
BRIEFS = Path("unpublished-local-ref:792ada9d1fcd5e54")


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def main():
    res = json.loads((O / "RESULTS.json").read_text())
    e = res["extensions"]
    ser = e["eucass_imperfect_mesh_series"]
    coll = e["eucass_core_collapse"]
    cr = e["eucass_elastic_stress_at_paper_pressures"]["crossings_MPa"]
    at603 = e["eucass_elastic_stress_at_paper_pressures"]["eucass-flat-a2.955"]["at_6.03"]
    at1245 = e["eucass_elastic_stress_at_paper_pressures"]["eucass-flat-a0"]["at_12.45"]
    sens = e["eucass_linear_sensitivity_192x2fx6c_MPa"]["runs"]
    wr = e["lead021b_wrinkling"]["eigen_kPa_by_mesh"]
    wk = e["lead021b_wrinkling"]["winkler_estimate"]
    fy = e["first_face_yield_on_the_path"]
    stab = e["lead021b_refined_path_stability"]
    w33 = e["width_convention_015b_nu033"]
    Y241 = "S200F spec-minimum yield 241 MPa (Materion, the card's cited datasheet)"
    Y345 = "345 MPa, the line's SR-200 proxy (021b is sized to it)"
    Y379 = "379.2 MPa, one historical lot"

    def f(x, n=3):
        return f"{x:.{n}f}"

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    def at_thr(v, dd):
        """Pressure at which the path's core shear reaches the ellipticity threshold of its own direction at E_in 0.01."""
        for lab, val in v["p_kPa_at_tau"].items():
            if lab.startswith(f"ellipticity threshold, {dd} E_in 0.01"):
                return val
        return float("nan")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
