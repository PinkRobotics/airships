#!/usr/bin/env python3
"""MAINLINE-015b. Corrected tolerance map.

Own arithmetic. kd.py, the checker's check.py, and every owner
compute script are not executed. Nothing here is a certification.

The live map carries one Poisson ratio, the declared 0.33, and pairs
each amplitude with the width of that same lambda. The retired 015
column is computed only as an audit, and it is not a tolerance.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
T0 = datetime.now(ZONE).isoformat(timespec="seconds")

R = 10.0
NU = 0.33  # the only nu on the live map. COMMON.md and 015 INPUTS.
# Retired width convention in the filed 015 script. Audit only.
NU_RETIRED = 0.30
LAMBDA_MATCHED = 1.0
LAMBDA_RETIRED_WIDTH = 2.625
K_LEE_LO = 1.0
K_LEE_HI = 5.0

# Baizhikova 2026 Eq. 3, fixed lambda_I = 1, floor 0.45.
# Source material nu is 0.5. Small-amplitude asymptote below ~0.07
# is excluded by that paper. Fit R/t is 100 to 1550.
K0, A_EQ, B_EQ = 0.45, 0.51, 3.88
EQ3_DELTA_FLOOR = 0.07
EQ3_RT_LO, EQ3_RT_HI = 100.0, 1550.0

# Lee et al. 2016 Eq. 23, as printed:
# jd = 0.068 + 0.25 / (0.28 + delta/t)
# Lower envelope over width k = 1 to 5. Computed at R/t 100 and 200.
# Section 7 gives no FEM below delta/t 0.15 and no ODE below 0.2.
LEE_A, LEE_B, LEE_C = 0.068, 0.25, 0.28
LEE_FEM_MIN = 0.15
LEE_ODE_MIN = 0.20
LEE_RT = (100.0, 200.0)

# Order levels, plus the filed full-precision gammas, plus the
# lower-kd pair Eq. 3 cannot invert and Lee can.
LEVELS = (
    0.9,
    0.7,
    0.5,
    0.595,
    0.468,
    0.5953179642995181,
    0.46822856667720764,
    0.3,
    0.2,
)

# Geometries pinned from filed RESULTS. Not recomputed.
SHELLS = {
    "Al-P2-E": {
        "role": "aluminum faces, 002/003 P2-E, the 015 aluminum point",
        "tf_m": 0.000336094970395,
        "core_m": 0.113432052508,
    },
    "Be-015": {
        "role": "015 frozen 014b beryllium on CR-III 5056 at 1.6 pcf",
        "tf_m": 0.0006932231273823878,
        "core_m": 0.04154971376178697,
    },
    "Be-021": {
        "role": "021 floating point, beryllium faces, CR-III 5056 3/8-1.0",
        "tf_m": 0.0008434480441930918,
        "core_m": 0.02021337638749162,
        "filed_gamma": 0.5953179642995181,
    },
    "Be-021b": {
        "role": "021b floating point, SR-200 faces, CR-III 5056 3/8-1.0",
        "tf_m": 0.0006917479988347394,
        "core_m": 0.030118230884842855,
        "filed_gamma": 0.46822856667720764,
    },
}

# Checker's published matched-lambda, nu 0.33 figures. Truncated in CHECK.md.
CHECK_MATCHED = {
    ("Al-P2-E", 0.5): {"amplitude_mm": 117.946298130, "rms_mm": 3.237077190},
    ("Al-P2-E", 0.7): {"amplitude_mm": 36.208334144, "rms_mm": 0.993750329},
    ("Al-P2-E", 0.9): {"amplitude_mm": 6.356617048, "rms_mm": 0.174459567},
    ("Be-015", 0.5): {"amplitude_mm": 43.794314478, "rms_mm": 0.732408174},
    ("Be-015", 0.7): {"amplitude_mm": 13.444416632, "rms_mm": 0.224841986},
    ("Be-015", 0.9): {"amplitude_mm": 2.360257934, "rms_mm": 0.039472526},
}
CHECK_LEE_DELTA = {
    0.2: 1.613939394,
    0.3: 0.797586207,
    0.5: 0.298703704,
    0.7: 0.115569620,
    0.9: 0.020480769,
}
CHECK_LEE_AMP = {
    ("Al-P2-E", 0.2): 318.030327,
    ("Al-P2-E", 0.3): 157.166126,
    ("Al-P2-E", 0.5): 58.860225,
    ("Al-P2-E", 0.7): 22.773249,
    ("Al-P2-E", 0.9): 4.035781,
    ("Be-015", 0.2): 118.086963,
    ("Be-015", 0.3): 58.356921,
    ("Be-015", 0.5): 21.855228,
    ("Be-015", 0.7): 8.455872,
    ("Be-015", 0.9): 1.498515,
}
# 015 CARD display, half-up, from the mixed column.
FILED_CARD = {
    ("Al-P2-E", 0.9): {"amp": "6.36", "rms": "0.46"},
    ("Al-P2-E", 0.7): {"amp": "36.2", "rms": "2.59"},
    ("Al-P2-E", 0.5): {"amp": "118", "rms": "8.45"},
    ("Be-015", 0.9): {"amp": "2.36", "rms": "0.10"},
    ("Be-015", 0.7): {"amp": "13.44", "rms": "0.59"},
    ("Be-015", 0.5): {"amp": "43.79", "rms": "1.91"},
}
GBT_ASSEMBLED_M = 250e-6


def half_up(value: float, places: int) -> str:
    quant = Decimal("1").scaleb(-places)
    return str(Decimal(format(value, ".20f")).quantize(quant, rounding=ROUND_HALF_UP))


def delta_bar_eq3(kd: float):
    """Baizhikova Eq. 3 inverse at lambda_I = 1. None below the floor."""
    if kd <= K0:
        return None
    ratio = (kd - K0) / A_EQ
    if ratio <= 0.0 or ratio >= 1.0:
        return None
    return -math.log(ratio) / B_EQ


def delta_bar_lee(kd: float):
    """Lee 2016 Eq. 23 inverse. None at or below the printed floor 0.068."""
    if kd <= LEE_A:
        return None
    return LEE_B / (kd - LEE_A) - LEE_C


def width_factor(nu: float) -> float:
    return (12.0 * (1.0 - nu * nu)) ** 0.25


def beta0(t_eq: float, lam: float, nu: float) -> float:
    """beta0 = lambda_I * sqrt(t/R) / [12(1-nu^2)]^(1/4)."""
    return lam * math.sqrt(t_eq / R) / width_factor(nu)


def rms_mm(delta_m: float, beta: float) -> float:
    """One Gaussian dimple, small angle. Whole-sphere uncentred RMS."""
    return delta_m * beta / math.sqrt(8.0) * 1000.0


def t_eq_of(tf: float, core: float) -> dict:
    h = tf + core
    thin = math.sqrt(3.0) * h
    exact = math.sqrt(3.0 * h * h + tf * tf)
    return {"h_m": h, "t_eq_thin_m": thin, "t_eq_exact_m": exact}


def lee_disposition(delta_bar: float, r_over_t: float) -> dict:
    return {
        "fem_amplitude_at_or_above_0_15": delta_bar >= LEE_FEM_MIN,
        "ode_amplitude_at_or_above_0_20": delta_bar >= LEE_ODE_MIN,
        "r_over_t_is_100_or_200": any(abs(r_over_t - g) < 1e-9 for g in LEE_RT),
        "width_sweep_k": [K_LEE_LO, K_LEE_HI],
        "unique_rms": False,
    }


def row_for(t_eq: float, kd: float) -> dict:
    g = R / t_eq
    d_eq = delta_bar_eq3(kd)
    d_lee = delta_bar_lee(kd)
    beta_matched = beta0(t_eq, LAMBDA_MATCHED, NU)
    beta_retired = beta0(t_eq, LAMBDA_RETIRED_WIDTH, NU_RETIRED)
    beta_lee_lo = beta0(t_eq, K_LEE_LO, NU)
    beta_lee_hi = beta0(t_eq, K_LEE_HI, NU)
    out = {
        "kd": kd,
        "nu": NU,
        "lambda_matched": LAMBDA_MATCHED,
        "eq3": None,
        "lee": None,
    }
    if d_eq is None:
        out["eq3"] = {
            "status": "below_floor_0.45",
            "delta_bar": None,
            "amplitude_mm": None,
            "single_dimple_rms_mm": None,
        }
    else:
        delta = d_eq * t_eq
        out["eq3"] = {
            "status": "lambda_I_1_matched",
            "delta_bar": d_eq,
            "amplitude_mm": delta * 1000.0,
            "width_m": R * beta_matched,
            "single_dimple_rms_mm": rms_mm(delta, beta_matched),
            "inside_source_small_amplitude_exclusion": d_eq < EQ3_DELTA_FLOOR,
            "inside_source_R_over_t": EQ3_RT_LO <= g <= EQ3_RT_HI,
            "retired_mixed_rms_mm": rms_mm(delta, beta_retired),
            "retired_over_matched": LAMBDA_RETIRED_WIDTH
            * beta0(t_eq, 1.0, NU_RETIRED)
            / beta_matched,
        }
    if d_lee is None:
        out["lee"] = {"status": "at_or_below_floor_0.068", "delta_bar": None}
    else:
        delta_l = d_lee * t_eq
        disp = lee_disposition(d_lee, g)
        out["lee"] = {
            "status": "eq_23_lower_envelope",
            "equation": "kd = 0.068 + 0.25/(0.28 + delta/t)",
            "delta_bar": d_lee,
            "amplitude_mm": delta_l * 1000.0,
            "single_dimple_rms_mm_at_k_1": rms_mm(delta_l, beta_lee_lo),
            "single_dimple_rms_mm_at_k_5": rms_mm(delta_l, beta_lee_hi),
            "width_m_at_k_1": R * beta_lee_lo,
            "width_m_at_k_5": R * beta_lee_hi,
            "range": disp,
        }
    return out


def shell_block(name: str, spec: dict) -> dict:
    thick = t_eq_of(spec["tf_m"], spec["core_m"])
    t_eq = thick["t_eq_thin_m"]
    g = R / t_eq
    factor = width_factor(NU)
    beta1 = beta0(t_eq, 1.0, NU)
    block = {
        "role": spec["role"],
        "tf_m": spec["tf_m"],
        "core_m": spec["core_m"],
        "h_m": thick["h_m"],
        "t_eq_m": t_eq,
        "t_eq_definition": "sqrt(3)*(core+tf), the brief's thin-face form",
        "t_eq_exact_ad_m": thick["t_eq_exact_m"],
        "R_over_t_eq": g,
        "nu": NU,
        "length_scale_sqrt_R_t_m": math.sqrt(R * t_eq),
        "classical_wavelength_m": 2.0 * math.pi * math.sqrt(R * t_eq) / factor,
        "width_lambda_1_m": R * beta1,
        "beta0_lambda_1_rad": beta1,
        "levels": {},
    }
    if "filed_gamma" in spec:
        block["filed_gamma"] = spec["filed_gamma"]
    for kd in LEVELS:
        block["levels"][format(kd, ".16g")] = row_for(t_eq, kd)
    return block


def close_to_printed(got: float, printed: float) -> bool:
    """CHECK.md prints a truncation. Allow half a unit in the last digit."""
    text = f"{printed:.12f}".rstrip("0")
    places = len(text.split(".")[1]) if "." in text else 0
    tol = 0.6 * 10.0 ** (-places)
    return abs(got - printed) <= tol


def main() -> None:
    shells = {name: shell_block(name, spec) for name, spec in SHELLS.items()}
    checks = []

    def add(name: str, ok: bool, **extra) -> None:
        row = {"name": name, "pass": bool(ok)}
        row.update(extra)
        checks.append(row)

    add("live map uses one nu", all(s["nu"] == NU for s in shells.values()))
    # Retired mix is exactly 2.625 times the nu-0.30 narrow RMS, and the
    # nu step from 0.30 to 0.33 is the remaining scale.
    p2 = shells["Al-P2-E"]
    sample = p2["levels"][format(0.9, ".16g")]["eq3"]
    ratio = sample["retired_mixed_rms_mm"] / sample["single_dimple_rms_mm"]
    nu_scale = LAMBDA_RETIRED_WIDTH * width_factor(NU) / width_factor(NU_RETIRED)
    add(
        "retired mix over live RMS is lambda 2.625 times the nu 0.30 to 0.33 scale",
        abs(ratio - nu_scale) < 1e-12 and abs(sample["retired_over_matched"] - ratio) < 1e-12,
        got=ratio,
    )
    add("Eq 3 does not invert 0.2 or 0.3", delta_bar_eq3(0.2) is None and delta_bar_eq3(0.3) is None)
    add(
        "Lee inverse round-trips",
        abs((LEE_A + LEE_B / (LEE_C + delta_bar_lee(0.5))) - 0.5) < 1e-12,
    )

    for (name, kd), expect in CHECK_MATCHED.items():
        eq3 = shells[name]["levels"][format(kd, ".16g")]["eq3"]
        add(
            f"check amplitude {name} kd {kd}",
            close_to_printed(eq3["amplitude_mm"], expect["amplitude_mm"]),
            got=eq3["amplitude_mm"],
        )
        add(
            f"check matched RMS {name} kd {kd}",
            close_to_printed(eq3["single_dimple_rms_mm"], expect["rms_mm"]),
            got=eq3["single_dimple_rms_mm"],
        )

    for kd, printed in CHECK_LEE_DELTA.items():
        add(
            f"check Lee delta/t kd {kd}",
            close_to_printed(delta_bar_lee(kd), printed),
            got=delta_bar_lee(kd),
        )
    for (name, kd), printed in CHECK_LEE_AMP.items():
        amp = shells[name]["levels"][format(kd, ".16g")]["lee"]["amplitude_mm"]
        add(
            f"check Lee amplitude {name} kd {kd}",
            close_to_printed(amp, printed),
            got=amp,
        )

    for (name, kd), card in FILED_CARD.items():
        eq3 = shells[name]["levels"][format(kd, ".16g")]["eq3"]
        amp_places = 0 if card["amp"].find(".") < 0 else len(card["amp"].split(".")[1])
        rms_places = len(card["rms"].split(".")[1])
        add(
            f"015 card amplitude still the lambda-1 inverse {name} {kd}",
            half_up(eq3["amplitude_mm"], amp_places) == card["amp"],
            got=half_up(eq3["amplitude_mm"], amp_places),
        )
        add(
            f"015 card RMS was the retired mix {name} {kd}",
            half_up(eq3["retired_mixed_rms_mm"], rms_places) == card["rms"],
            got=half_up(eq3["retired_mixed_rms_mm"], rms_places),
        )

    # 021 and 021b quoted the retired mix. Reproduce their printed sentences
    # so the correction is against the number they filed.
    be21 = shells["Be-021"]["levels"][format(0.5953179642995181, ".16g")]["eq3"]
    be21b = shells["Be-021b"]["levels"][format(0.46822856667720764, ".16g")]["eq3"]
    add(
        "021 quoted amplitude 11.8 mm at its gamma",
        half_up(be21["amplitude_mm"], 1) == "11.8",
        got=be21["amplitude_mm"],
    )
    add(
        "021 quoted retired RMS 0.3639 mm",
        half_up(be21["retired_mixed_rms_mm"], 4) == "0.3639",
        got=be21["retired_mixed_rms_mm"],
    )
    add(
        "021b quoted amplitude 45.82 mm at its gamma",
        half_up(be21b["amplitude_mm"], 2) == "45.82",
        got=be21b["amplitude_mm"],
    )
    add(
        "021b quoted retired RMS 1.709 mm",
        half_up(be21b["retired_mixed_rms_mm"], 3) == "1.709",
        got=be21b["retired_mixed_rms_mm"],
    )

    display = {}
    order_levels = (0.9, 0.7, 0.5, 0.595, 0.468)
    for name in SHELLS:
        shell = shells[name]
        display[name] = {
            "t_eq_mm": half_up(shell["t_eq_m"] * 1000.0, 2),
            "R_over_t": half_up(shell["R_over_t_eq"], 2),
            "width_lambda_1_m": half_up(shell["width_lambda_1_m"], 4),
            "classical_wavelength_m": half_up(shell["classical_wavelength_m"], 4),
            "sqrt_R_t_m": half_up(shell["length_scale_sqrt_R_t_m"], 4),
        }
        for kd in order_levels:
            key = format(kd, ".16g")
            eq3 = shell["levels"][key]["eq3"]
            lee = shell["levels"][key]["lee"]
            prefix = f"kd_{key}"
            if eq3["amplitude_mm"] is None:
                display[name][prefix] = "eq3_below_floor"
            else:
                display[name][f"{prefix}_eq3_amp_mm"] = half_up(eq3["amplitude_mm"], 3)
                display[name][f"{prefix}_eq3_rms_mm"] = half_up(eq3["single_dimple_rms_mm"], 4)
                display[name][f"{prefix}_eq3_small"] = eq3["inside_source_small_amplitude_exclusion"]
                display[name][f"{prefix}_eq3_in_Rt"] = eq3["inside_source_R_over_t"]
            display[name][f"{prefix}_lee_amp_mm"] = half_up(lee["amplitude_mm"], 3)
            display[name][f"{prefix}_lee_rms_k1_mm"] = half_up(lee["single_dimple_rms_mm_at_k_1"], 4)
            display[name][f"{prefix}_lee_rms_k5_mm"] = half_up(lee["single_dimple_rms_mm_at_k_5"], 4)
            display[name][f"{prefix}_lee_fem"] = lee["range"]["fem_amplitude_at_or_above_0_15"]
            display[name][f"{prefix}_lee_ode"] = lee["range"]["ode_amplitude_at_or_above_0_20"]
        # Exact filed gammas, full precision in RESULTS; display half-up here.
        if "filed_gamma" in shell:
            key = format(shell["filed_gamma"], ".16g")
            eq3 = shell["levels"][key]["eq3"]
            lee = shell["levels"][key]["lee"]
            display[name]["filed_gamma_eq3_amp_mm"] = half_up(eq3["amplitude_mm"], 3)
            display[name]["filed_gamma_eq3_rms_mm"] = half_up(eq3["single_dimple_rms_mm"], 4)
            display[name]["filed_gamma_lee_amp_mm"] = half_up(lee["amplitude_mm"], 3)
            display[name]["filed_gamma_lee_rms_k1_mm"] = half_up(
                lee["single_dimple_rms_mm_at_k_1"], 4
            )
            display[name]["filed_gamma_lee_rms_k5_mm"] = half_up(
                lee["single_dimple_rms_mm_at_k_5"], 4
            )
            display[name]["filed_gamma_lee_fem"] = lee["range"]["fem_amplitude_at_or_above_0_15"]
            display[name]["filed_gamma_lee_ode"] = lee["range"]["ode_amplitude_at_or_above_0_20"]
            rms = eq3["single_dimple_rms_mm"] / 1000.0
            display[name]["filed_gamma_eq3_rms_over_0_25mm"] = half_up(
                rms / GBT_ASSEMBLED_M, 3
            )

    # Gap against the one manufacturing figure the check could support.
    gaps = {}
    for name in ("Al-P2-E", "Be-015", "Be-021", "Be-021b"):
        gaps[name] = {}
        for kd in order_levels:
            eq3 = shells[name]["levels"][format(kd, ".16g")]["eq3"]
            if eq3["single_dimple_rms_mm"] is None:
                continue
            ratio = (eq3["single_dimple_rms_mm"] / 1000.0) / GBT_ASSEMBLED_M
            gaps[name][format(kd, ".16g")] = {
                "matched_rms_over_GBT_0_25mm": ratio,
                "allowance_looser_than_0_25mm": ratio > 1.0,
            }

    out = {
        "schema": 1,
        "card": "MAINLINE-015b",
        "unit": "vacuum-mainline015b-kd-precision-fix-1020",
        "started_at": T0,
        "ended_at": datetime.now(ZONE).isoformat(timespec="seconds"),
        "certification": False,
        "tag": "QUESTIONABLE",
        "nu_live": NU,
        "nu_retired_audit_only": NU_RETIRED,
        "kd_for_SF_1": {
            "value": 0.5183040769,
            "source": "rpt-ref-88e650e7f8b713866e0b continuous threshold",
            "rescored_here": False,
            "why_unchanged": "The mode score already used nu 0.33. This card changes the tolerance map only.",
        },
        "equations": {
            "eq3": "kd = 0.45 + 0.51 exp(-3.88 delta/t) at lambda_I = 1",
            "lee_23": "kd = 0.068 + 0.25/(0.28 + delta/t)",
            "beta0": "lambda * sqrt(t_eq/R) / [12(1-nu^2)]^(1/4)",
            "rms": "delta * beta0 / sqrt(8), one Gaussian dimple",
            "t_eq": "sqrt(3)*(core+tf)",
        },
        "range_limits": {
            "eq3": {
                "lambda_I": 1,
                "source_nu": 0.5,
                "carried_nu": NU,
                "R_over_t": [EQ3_RT_LO, EQ3_RT_HI],
                "excluded_delta_over_t_below": EQ3_DELTA_FLOOR,
                "floor_kd": K0,
            },
            "lee_23": {
                "k": [K_LEE_LO, K_LEE_HI],
                "R_over_t_computed": list(LEE_RT),
                "no_FEM_below_delta_over_t": LEE_FEM_MIN,
                "no_ODE_below_delta_over_t": LEE_ODE_MIN,
                "unique_rms": False,
                "citation": "Lee et al. 2016, JAM, Eq. 23 and section 7",
            },
        },
        "shells": shells,
        "gaps_matched_rms_over_GBT_0_25_mm": gaps,
        "display_half_up": display,
        "checks": checks,
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    failed = [c for c in checks if not c["pass"]]
    print("checks", len(checks), "failed", len(failed))
    for c in checks:
        line = ("PASS " if c["pass"] else "FAIL ") + c["name"]
        if "got" in c:
            line += " got " + str(c["got"])
        print(line)
    print(json.dumps(display, indent=1))


if __name__ == "__main__":
    main()
