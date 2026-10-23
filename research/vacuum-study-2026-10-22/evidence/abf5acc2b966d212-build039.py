#!/usr/bin/env python3
"""MAINLINE-039: compact RUNS.json (and the gamma_s >= 5 sensitivity) into RESULTS.json and print the card tables."""
import datetime
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline039-stiffened-sandwich-1020"
LABEL = {"baseline": "plain sandwich (028b family)", "C1": "C1 Be isogrid tee ribs", "C2": "C2 SiC tube frame (026)",
         "C2b": "C2b Be tube frame"}
MODE_KEYS = ("global", "panel", "face", "wrinkle", "rib_yield", "crimp", "dimple", "crush_uniform", "crush_rib_line",
             "scarf_screen", "core_shear_rib_line", "rib_crippling", "tube_local", "sic_compression")


def point(b):
    if b is None:
        return None
    keep = {k: b.get(k) for k in ("least_SF", "governs", "tf_mm", "tc_mm", "lattice_kg", "psi", "gamma_s", "heavy",
                                  "adequate", "cap_regime", "lam_panel", "lam_gr", "teq", "fr", "Vc", "sig_face_MPa",
                                  "shape", "section", "lattice_joining_parts", "O5_frame_bay", "seam_screen")}
    keep["SF"] = {k: round(v, 6) for k, v in (b.get("SF") or {}).items() if k in MODE_KEYS}
    keep["sig_r_MPa"] = (b.get("sig_r") or 0) / 1e6
    keep["masses"] = b.get("masses")
    keep["today_endpoints"] = {k: v[0] for k, v in (b.get("today_full") or {}).items()}
    return keep


def lset(c):
    if c is None:
        return None
    return {k: c.get(k) for k in ("subset", "max_usage", "needed", "today_at_point", "needed_over_today", "lattice_kg",
                                  "tf_mm", "tc_mm", "psi", "gamma_s", "heavy", "adequate", "cap_regime", "masses",
                                  "section", "shape", "lam_panel")}

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
