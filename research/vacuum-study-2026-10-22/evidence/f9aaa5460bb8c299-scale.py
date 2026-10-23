#!/usr/bin/env python3
"""MAINLINE-004b: scale sealed SP-8032 rows to a sourced knockdown range.

Reads the sealed MAINLINE-004 RESULTS. Does not execute predecessor scripts.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SEAT = "ref-2543c559b19ffce7dfdd"
ref-4dd78496f9ad9abb5344 = "ref-44b53f348e892521e60b"
UNIT = "vacuum-mainline004b-kd-range-1019"
ROOT = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline004b-kd-range-1019"
)
STATE = Path(
    "unpublished-local-ref:89cd363716acb8e4"
)
SEALED = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline004-knockdown-owner1200-1019/RESULTS.json"
)
P003 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline003-p2-targets-owner1200-1019/RESULTS.json"
)
BRIEF = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-004b-KD-RANGE.md"
)
COMMON = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/COMMON.md"
)
WAGNER_PDF = Path(
    "unpublished-local-ref:ref-fd295680e8c2a867cd9f"
)

E_PA = 68.9e9
NU = 0.33
R_M = 10.0
P_EXT = 95460.83791390515
KD_CENTRAL = 0.20
KD_OPT = 0.90
KD_CLASSICAL = 1.0
KD_SANDWICH_FLAT = 0.22
KD_SANDWICH_DIMPLE = 0.20
TOL = 1e-12
ZONE = ZoneInfo("America/Los_Angeles")

EXPECTED = {
    BRIEF: (
        "0b25b6f4294b79a4595a6ee15156c8d368619bd73b8e8af7689ef98b5fd0c2fb",
        1754,
    ),
    COMMON: (
        "8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5",
        5874,
    ),
    SEALED: (
        "c5e1f04fd8e3e4f5b09fec52bd6e865ab277d54c5890bd5f0459348090e69567",
        5567,
    ),
}


def g(x: float) -> str:
    return format(x, ".12g")


def sha_bytes(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def pin(path: Path) -> dict:
    digest, nbytes = sha_bytes(path)
    return {"path": str(path), "sha256": digest, "bytes": nbytes}


def rel_err(a: float, b: float) -> float:
    denom = max(abs(a), abs(b), 1.0)
    return abs(a - b) / denom


def stamp() -> tuple[str, float]:
    return datetime.now(ZONE).isoformat(timespec="microseconds"), time.monotonic()


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")


def prepend_state(when: str, public: str) -> None:
    line = (
        f"WORKING · {SEAT} · {UNIT} · {SESSION} · {when}\n"
        f"public: {public}\n"
    )
    old = STATE.read_text(encoding="utf-8") if STATE.exists() else ""
    STATE.write_text(line + old, encoding="utf-8")


def factor_values(sf_sp: float, e_sp: float, kd_sp: float, p_cl: float, kd: float) -> dict:
    sf_scale = sf_sp * (kd / kd_sp)
    e_scale = e_sp * (kd_sp / kd)
    sf_id = kd * p_cl / P_EXT
    e_id = E_PA * P_EXT / (kd * p_cl)
    if rel_err(sf_scale, sf_id) > TOL or rel_err(e_scale, e_id) > TOL:
        raise SystemExit(
            f"scale identity failed kd={kd} sf {sf_scale} vs {sf_id} e {e_scale} vs {e_id}"
        )
    pressure = kd * p_cl
    return {
        "kd": kd,
        "buckling_SF": sf_id,
        "E_required_Pa": e_id,
        "buckling_pressure_Pa": pressure,
        "above_alloy_modulus": e_id > E_PA,
    }


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for path, (want_sha, want_n) in EXPECTED.items():
        digest, nbytes = sha_bytes(path)
        if digest != want_sha or nbytes != want_n:
            raise SystemExit(f"pin mismatch {path} {digest} {nbytes}")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    sealed = json.loads(SEALED.read_text(encoding="utf-8"))
    p003 = json.loads(P003.read_text(encoding="utf-8"))
    if p003["atmosphere"]["p_ext_Pa"] != P_EXT:
        raise SystemExit("p_ext mismatch against sealed 003")

    denom = R_M * R_M * math.sqrt(1.0 - NU * NU)
    rows_out = []
    for row in sealed["rows"]:
        geo = row["geometry"]
        tf = geo["tf_m"]
        d = geo["d_m"]
        kd_sp = row["knockdown"]
        sf_sp = row["buckling_SF"]
        e_sp = row["E_required_Pa"]
        p_cl = 4.0 * E_PA * tf * d / denom
        sf_id = kd_sp * p_cl / P_EXT
        e_id = E_PA * P_EXT / (kd_sp * p_cl)
        p_id = kd_sp * p_cl
        if (
            rel_err(sf_id, sf_sp) > TOL
            or rel_err(e_id, e_sp) > TOL
            or rel_err(p_id, row["buckling_pressure_Pa"]) > TOL
        ):
            raise SystemExit(
                f"sealed identity failed {row['point_id']} "
                f"sf {sf_id} {sf_sp} e {e_id} {e_sp} p {p_id} {row['buckling_pressure_Pa']}"
            )
        factors = {
            "conservative": factor_values(sf_sp, e_sp, kd_sp, p_cl, kd_sp),
            "central": factor_values(sf_sp, e_sp, kd_sp, p_cl, KD_CENTRAL),
            "optimistic": factor_values(sf_sp, e_sp, kd_sp, p_cl, KD_OPT),
            "classical_reference": factor_values(sf_sp, e_sp, kd_sp, p_cl, KD_CLASSICAL),
            "sandwich_flat": factor_values(sf_sp, e_sp, kd_sp, p_cl, KD_SANDWICH_FLAT),
            "sandwich_dimple": factor_values(
                sf_sp, e_sp, kd_sp, p_cl, KD_SANDWICH_DIMPLE
            ),
        }
        # Conservative must reproduce the sealed row exactly.
        if factors["conservative"]["buckling_SF"] != sf_id:
            raise SystemExit("conservative sf drift")
        if factors["conservative"]["kd"] != kd_sp:
            raise SystemExit("conservative kd drift")
        rows_out.append(
            {
                "point_id": row["point_id"],
                "dependency": "DEPENDENCY003_ESTIMATE_PENDING_UNA",
                "tag": "QUESTIONABLE",
                "geometry": geo,
                "lambda": row["lambda"],
                "R_over_t_eq": row["R_over_t_eq"],
                "strength_SF_QUESTIONABLE_unchanged": row[
                    "strength_SF_QUESTIONABLE_unchanged"
                ],
                "p_cl_Pa": p_cl,
                "sealed_sp8032_kd": kd_sp,
                "factors": factors,
                "optimistic_over_conservative": KD_OPT / kd_sp,
            }
        )

    end_utc, end_mono = stamp()
    elapsed = end_mono - origin_mono
    wagner_pin = pin(WAGNER_PDF) if WAGNER_PDF.exists() else None
    wagner_mtime = None
    if WAGNER_PDF.exists():
        wagner_mtime = datetime.fromtimestamp(
            WAGNER_PDF.stat().st_mtime, ZONE
        ).isoformat(timespec="seconds")

    results = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "dependency": "DEPENDENCY003_ESTIMATE_PENDING_UNA",
        "card": "MAINLINE-004b",
        "tag": "QUESTIONABLE",
        "certification": False,
        "map_point": False,
        "formula": {
            "p_cl": "4*E*tf*d/(R^2*sqrt(1-nu^2))",
            "d": "sealed 004 face separation, core thickness plus face thickness",
            "buckling_SF": "kd*p_cl/p_ext",
            "E_required": "E*p_ext/(kd*p_cl)",
            "scaling": "E_required proportional to 1/kd; a larger knockdown lowers required E",
            "scale_from_sealed": "SF_new = SF_sp*(kd_new/kd_sp); E_new = E_sp*(kd_sp/kd_new)",
            "identity_tolerance_relative": TOL,
            "E_Pa": E_PA,
            "nu": NU,
            "R_m": R_M,
            "p_ext_Pa": P_EXT,
        },
        "sources": {
            "conservative": "sealed MAINLINE-004 NASA SP-8032 per row",
            "central_kd": KD_CENTRAL,
            "central": (
                "Wagner, Huehne, Zhang and Tang, Int. J. Pressure Vessels and Piping "
                "179 (2020) 104015, doi 10.1016/j.ijpvp.2019.104015, elastic-region "
                "statement that equation (7) equals about 0.2 and seems independent of R/t. "
                "Equation (7) was not evaluated. Numerical lower bound 0.21 was not substituted."
            ),
            "optimistic_kd": KD_OPT,
            "optimistic_carry": True,
            "optimistic": (
                "Wagner 2020 Table 3 row 12, Krenzke and Kiernan, reliable yes, "
                "upper KDF 0.90. Highest reliable upper in that table."
            ),
            "classical_kd": KD_CLASSICAL,
            "classical": "perfect-shell bound, reference only, not the carry",
            "sandwich_flat_kd": KD_SANDWICH_FLAT,
            "sandwich_dimple_kd": KD_SANDWICH_DIMPLE,
            "sandwich": (
                "Sim, Lee, Kim, Park and Lee, Int. J. Aerospace Engineering 2024, "
                "doi 10.1155/2024/8765733. Dimple 0.20, flat 0.22. Not the carry."
            ),
        },
        "rows": rows_out,
        "checks": {
            "sealed_identity": "PASS",
            "scale_identity": "PASS",
            "tolerance_relative": TOL,
        },
        "measurements": {
            "origin_utc": origin_utc,
            "origin_monotonic_s": origin_mono,
            "end_utc": end_utc,
            "end_monotonic_s": end_mono,
            "elapsed_s": elapsed,
            "role": "measurements_only_not_limits",
            "wagner_pdf_mtime": wagner_mtime,
            "note": (
                "Source reading in this session preceded the origin file. "
                "Elapsed is origin to this write. No phase cap and no funded-seconds cap."
            ),
        },
    }
    dump(ROOT / "RESULTS.json", results)

    nfi = [
        {
            "NFI_id": "NFI-OPT-GAP",
            "gap": (
                "The carried optimistic knockdown is 0.90. The conservative knockdown "
                "is the sealed per-row SP-8032 factor near 0.1407. The ratio is about 6.4. "
                "This is the optimism that must later be grounded."
            ),
            "direction": "A knockdown test or formula at this sphere's lambda, on a sandwich.",
            "effect": "Required face modulus at 0.90 is lower than the SP-8032 modulus by that ratio.",
            "per_row_optimistic_over_conservative": {
                r["point_id"]: r["optimistic_over_conservative"] for r in rows_out
            },
        },
        {
            "NFI_id": "NFI-LAMBDA",
            "gap": (
                "No reliable row in Wagner 2020 Table 3 reaches lambda near 65-68. "
                "Krenzke's 0.11-0.90 range mixes R/t 10-212 and stiffened with unstiffened "
                "machined shells, so 0.90 may be a thick or stiffened specimen. "
                "Adam and King, reliable yes, reach 0.89 only to lambda 43.11."
            ),
            "direction": "Separate the Krenzke upper by R/t and by stiffened versus unstiffened.",
            "effect": "The carried 0.90 is an upper end of the tabulated reliable set, not a measurement at this slenderness.",
        },
        {
            "NFI_id": "NFI-TRANSFER",
            "gap": (
                "SP-8032, the Wagner 2020 elastic statement, and the Krenzke upper are "
                "monocoque or dome evidence. They are transferred onto a complete sandwich "
                "sphere with phi equal to pi and t_eq = (6*tf*d^2)^(1/3)."
            ),
            "direction": "Keep the transfer tagged QUESTIONABLE until a sandwich source at these proportions exists.",
            "effect": "The buckling safety factors are not validated sandwich knockdowns.",
        },
        {
            "NFI_id": "NFI-SANDWICH",
            "gap": (
                "The sourced foam-core factors are Sim et al. 2024: dimple 0.20 and flat 0.22, "
                "from numerical postbuckling of small-scale hemispheres. They do not support 0.90. "
                "The paper says NASA SP-8032 at 0.18 and NASA CR-1457 at 0.20 may not provide "
                "a suitable knockdown for hemispherical foam-core shells. Their 0.18 is not this card's SP-8032 row."
            ),
            "direction": "A sandwich knockdown at R = 10 m.",
            "effect": "Using 0.22 instead of 0.90 would raise required modulus by 0.90/0.22.",
        },
        {
            "NFI_id": "NFI-LRSM",
            "gap": (
                "Central uses the prose value 0.20. Wagner 2020 also states a numerical "
                "lower-bound knockdown of 0.21 for one deep dome, H/r about 0.5, R/t about 90, "
                "lambda about 15.7. Equation (7) was not evaluated and lambda_s was not computed. "
                "The 2018 Wagner, Huehne and Niemann threshold equation was not retrieved. "
                "The comparative-study equation rho = 5.172/lambda - 1.464 + 0.1296 was not applied; "
                "it is outside this lambda and the extract is ambiguous."
            ),
            "direction": "Recover the 2018 threshold equation before using it. Do not extrapolate equation (7) without lambda_s.",
            "effect": "Substituting 0.21 for 0.20 would rescale required modulus by 0.20/0.21.",
        },
        {
            "NFI_id": "NFI-CLASSICAL",
            "gap": "Classical knockdown 1.0 is the perfect-shell bound. It is reference only.",
            "direction": "Do not carry 1.0 as the optimistic estimate.",
            "effect": "None on the carried factor.",
        },
        {
            "NFI_id": "NFI-STRENGTH",
            "gap": "Strength safety factors stay at the sealed 003 QUESTIONABLE values. Knockdown does not rescale yield.",
            "direction": "Leave strength on its own card.",
            "effect": "Strength safety factor is unchanged at every knockdown.",
        },
    ]
    dump(ROOT / "NFI.json", nfi)

    inputs = {
        "schema": 1,
        "card": "MAINLINE-004b",
        "status": "ESTIMATE_PENDING_UNA",
        "dependency": "DEPENDENCY003_ESTIMATE_PENDING_UNA",
        "constants": {
            "E_Pa": E_PA,
            "nu": NU,
            "R_m": R_M,
            "p_ext_Pa": P_EXT,
            "p_ext_source": "sealed MAINLINE-003 RESULTS p_ext_Pa",
        },
        "knockdowns": {
            "conservative": "per-row sealed SP-8032",
            "central": KD_CENTRAL,
            "optimistic_carry": KD_OPT,
            "classical_reference": KD_CLASSICAL,
            "sandwich_flat": KD_SANDWICH_FLAT,
            "sandwich_dimple": KD_SANDWICH_DIMPLE,
        },
        "pins": {
            "brief": pin(BRIEF),
            "common": pin(COMMON),
            "sealed_004_results": pin(SEALED),
            "sealed_003_results": pin(P003),
            "wagner_2020_pdf": wagner_pin,
        },
        "not_used": [
            "Wagner 2018 analytic threshold equation, not retrieved",
            "comparative-study equation (19), outside this lambda",
            "Wagner 2020 equation (7), lambda_s not computed",
            "NASA SP-8032 value 0.18 quoted by Sim et al., not this card's lambda formula",
            "classical 1.0 as a carry",
        ],
    }
    dump(ROOT / "INPUTS.json", inputs)

    card = render_card(rows_out, origin_utc, end_utc, elapsed)
    (ROOT / "CARD.md").write_text(card, encoding="utf-8")

    print("elapsed_s", elapsed)
    print("origin", origin_utc)
    print("end", end_utc)
    for row in rows_out:
        print("---", row["point_id"], "ratio", g(row["optimistic_over_conservative"]))
        for name, fac in row["factors"].items():
            print(
                name,
                "kd",
                g(fac["kd"]),
                "SF",
                g(fac["buckling_SF"]),
                "E",
                g(fac["E_required_Pa"]),
                "above",
                fac["above_alloy_modulus"],
            )


def side(above: bool) -> str:
    return "above" if above else "below"


def render_card(rows_out, origin_utc, end_utc, elapsed) -> str:
    parts = []
    parts.append("# MAINLINE-004b knockdown range — ESTIMATE_PENDING_UNA")
    parts.append("")
    parts.append(
        "Dependency label DEPENDENCY003_ESTIMATE_PENDING_UNA. This card adds no map point. "
        "Una004 is not opened. Nothing here is a certification. Every knockdown is QUESTIONABLE."
    )
    parts.append("")
    parts.append(
        "Geometry, atmosphere, masses and the strength safety factors stay on the sealed "
        "MAINLINE-004 rows. Those rows already carry NASA SP-8032. This card does not rerun "
        "that curve. Buckling safety factor and required face modulus are scaled from the sealed numbers."
    )
    parts.append("")
    parts.append(
        "Face separation d is the sealed 004 value, core thickness plus face thickness. "
        "Classical sandwich pressure is p_cl = 4*E*tf*d/(R^2*sqrt(1-nu^2)) with "
        "E = 68.9e9 Pa, nu = 0.33 and R = 10 m. External pressure is 95460.83791390515 Pa. "
        "Buckling SF = kd*p_cl/p. Required face modulus E_req = E*p/(kd*p_cl). "
        "E_req scales as 1/kd, so a larger knockdown lowers required E. "
        "The same numbers from the sealed row are SF_new = SF_sp*(kd_new/kd_sp) and "
        "E_new = E_sp*(kd_sp/kd_new). Both forms matched within a relative tolerance of 1e-12 on every row."
    )
    parts.append("")
    parts.append(
        "Conservative knockdown: the sealed per-row SP-8032 factor. The text form is "
        "rho = 0.14 + 3.2/lambda^2 for lambda above 2, NASA SP-8032 as filed on MAINLINE-004. "
        "That monocoque cap curve is transferred with phi = pi and "
        "t_eq = (6*tf*d^2)^(1/3). The transfer is QUESTIONABLE."
    )
    parts.append("")
    parts.append(
        "Central knockdown: 0.20. Source: Wagner, Huehne, Zhang and Tang, International Journal "
        "of Pressure Vessels and Piping 179 (2020) 104015, doi 10.1016/j.ijpvp.2019.104015. "
        "The paper says equation (7) equals about 0.2 for shells which buckle in the elastic "
        "region and seems independent of the R/t ratio. The same paper's numerical lower bound "
        "for one deep dome is 0.21. Equation (7) was not evaluated for this sandwich, and "
        "lambda_s was not computed. This is monocoque dome evidence transferred onto the sandwich. "
        "It is QUESTIONABLE."
    )
    parts.append("")
    parts.append(
        "Optimistic knockdown, and the factor the main line should carry as its optimistic "
        "estimate: 0.90. Source: Wagner 2020 Table 3 row 12, Krenzke and Kiernan, Tests of "
        "stiffened and unstiffened machined spherical shells under external hydrostatic pressure, "
        "David Taylor Model Basin Report 1741, 1963, as tabulated there. The row is reliable = yes, "
        "n = 70, aluminium, R/t 10-212, lambda 1.58-33.18, H/r 0.072-1, KDF 0.11-0.90. "
        "It is the highest reliable upper in that table. The range mixes thick and thin shells "
        "and stiffened with unstiffened specimens. No reliable row reaches this sphere's lambda "
        "near 65-68. Adam and King, the same table row 11, reliable = yes, reach 0.89 at lambda "
        "up to 43.11 on PVC and are not the carried factor. The carry is QUESTIONABLE."
    )
    parts.append("")
    parts.append(
        "Classical knockdown 1.0 is the perfect-shell bound, for reference only. It is not the carry."
    )
    parts.append("")
    parts.append(
        "Sandwich-specific source, not the carry: Sim, Lee, Kim, Park and Lee, International "
        "Journal of Aerospace Engineering, 2024, doi 10.1155/2024/8765733. Numerical postbuckling "
        "of small-scale hemispherical foam-core shells gives a dimple factor 0.20 and a flat "
        "factor 0.22. The dimple factor is numerically equal to the central 0.20 and is a different "
        "source. The paper says NASA SP-8032 quoted at 0.18 and NASA CR-1457 at 0.20 may not "
        "provide a suitable knockdown for hemispherical foam-core shells. Their 0.18 is not the "
        "sealed lambda formula on this card. These factors do not support carrying 0.90. "
        "The transfer from a small hemisphere to this R = 10 m complete sphere is QUESTIONABLE."
    )
    parts.append("")
    parts.append(
        "The gap from the carried 0.90 to the per-row SP-8032 factor is NFI-OPT-GAP."
    )
    parts.append("")
    for row in rows_out:
        geo = row["geometry"]
        fac = row["factors"]
        parts.append(f"## {row['point_id']}")
        parts.append("")
        parts.append(
            f"Face {g(geo['tf_m'])} m, core {g(geo['core_m'])} m, face separation {g(geo['d_m'])} m, "
            f"lambda {g(row['lambda'])}. QUESTIONABLE strength SF stays {g(row['strength_SF_QUESTIONABLE_unchanged'])}."
        )
        parts.append("")
        for label, key in (
            ("Conservative", "conservative"),
            ("Central", "central"),
            ("Optimistic carry", "optimistic"),
            ("Classical reference", "classical_reference"),
            ("Sandwich flat", "sandwich_flat"),
        ):
            item = fac[key]
            parts.append(
                f"{label} knockdown {g(item['kd'])}. Buckling SF {g(item['buckling_SF'])}. "
                f"Required face modulus {g(item['E_required_Pa'])} Pa, {side(item['above_alloy_modulus'])} "
                f"the QUESTIONABLE alloy modulus 68.9 GPa."
            )
            parts.append("")
        parts.append(
            f"Sandwich dimple uses knockdown {g(fac['sandwich_dimple']['kd'])}, the same buckling SF "
            f"and required modulus as the central row, from the Sim et al. 2024 dimple model. "
            f"Optimistic over conservative is {g(row['optimistic_over_conservative'])}."
        )
        parts.append("")
    parts.append("## Measurements")
    parts.append("")
    parts.append(
        f"Start {origin_utc}. End {end_utc}. Elapsed {elapsed} s. "
        "These times are measurements only. There is no time budget and no phase cap on this card. "
        "The order deadline 2026-10-20T07:00:00-07:00 is a door check-in, not a work limit. "
        "Source reading in this session preceded the start stamp. Spend for this card is the elapsed value."
    )
    parts.append("")
    return "\n".join(parts)


if __name__ == "__main__":
    main()
