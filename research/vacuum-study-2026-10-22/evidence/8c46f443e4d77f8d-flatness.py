#!/usr/bin/env python3
"""MAINLINE-032b. Compare read panel figures to the 032 amplitudes.

Does not recompute Q, does not rerun waviness.py, and does not touch the
032 tree except to read RESULTS.json. Refuses a second stamp.
"""

from __future__ import annotations

import json
import math
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

UNIT = "vacuum-mainline032b-measured-flatness-1020"
HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "RESULTS.json"
NFI_PATH = HERE / "NFI.json"
ORIGIN_PATH = HERE / "ORIGIN.json"
PRIOR = (
    HERE.parent
    / "vacuum-mainline032-wrinkle-waviness-1020"
    / "RESULTS.json"
)
ZONE = ZoneInfo("America/Los_Angeles")
INCH_MM = 25.4
CELL_M = 0.375 * 0.0254  # 3/8 inch, exact

# Lead rows only. Copied by key from the 032 file at runtime, not recomputed.


def lead_rows(prior: dict) -> list[dict]:
    want = {
        ("Be S-200F", 0.371, "stabilised_typical_60_psi"),
        ("SR-200", 0.609, "stabilised_typical_60_psi"),
        ("Be S-200F", 0.371, "stabilised_minimum_35_psi"),
        ("SR-200", 0.609, "stabilised_minimum_35_psi"),
    }
    out = []
    for row in prior["amplitudes"]:
        key = (row["face"], row["Q"], row["Fc_basis"])
        if key in want and row.get("is_that_leads_Q") is True:
            out.append(
                {
                    "face": row["face"],
                    "Q": row["Q"],
                    "Fc_basis": row["Fc_basis"],
                    "delta_mm": row["delta_mm"],
                    "source": "032 RESULTS.json amplitudes, not recomputed",
                    "meaning": "zero-to-peak wrinkle component from CR-1457 eq 2.2-13",
                }
            )
    if len(out) != 4:
        raise SystemExit(f"expected 4 lead amplitudes, found {len(out)}")
    return out


def ratio(measured_mm: float, needed_mm: float) -> dict:
    return {
        "measured_over_needed": measured_mm / needed_mm,
        "needed_amplitude_exceeded_as_a_number": measured_mm > needed_mm,
    }


def against(measured_mm: float, leads: list[dict]) -> list[dict]:
    rows = []
    for lead in leads:
        rows.append(
            {
                "face": lead["face"],
                "Q": lead["Q"],
                "Fc_basis": lead["Fc_basis"],
                "needed_delta_mm": lead["delta_mm"],
                **ratio(measured_mm, lead["delta_mm"]),
            }
        )
    return rows


def main() -> None:
    if RESULTS_PATH.exists():
        raise SystemExit(f"refuse restamp: {RESULTS_PATH} exists")
    started = datetime.now(ZONE)
    mono0 = time.monotonic()
    prior = json.loads(PRIOR.read_text())
    leads = lead_rows(prior)
    smallest = min(leads, key=lambda r: r["delta_mm"])
    largest = max(leads, key=lambda r: r["delta_mm"])

    nasa_depth_inch = 0.000065
    nasa_depth_mm = nasa_depth_inch * INCH_MM
    nasa_peak_inch = 0.000057
    nasa_peak_mm = nasa_peak_inch * INCH_MM
    nrao_inch = 0.008
    nrao_mm_from_inch = nrao_inch * INCH_MM
    nrao_printed_mm = 0.20

    # Slope bound: |dz/dx| <= theta everywhere implies the rise over a
    # length L is at most theta*L. A cell dimple whose valley sits inside
    # one cell therefore has depth at most theta times one cell. The paper
    # did not print that depth. Tag PROJECTION.
    slopes_mrad = (0.5, 1.6)
    slope_bounds = []
    for mrad in slopes_mrad:
        theta = mrad * 1e-3
        sine_mm = (theta * CELL_M / (2.0 * math.pi)) * 1e3
        cell_rise_mm = (theta * CELL_M) * 1e3
        half_cell_mm = cell_rise_mm / 2.0
        slope_bounds.append(
            {
                "slope_milliradian": mrad,
                "tag": "PROJECTION",
                "assumption": (
                    "The printed maximum slope is treated as a bound on |dz/dx|. "
                    "A sine of wavelength one cell, and a rise held at that slope "
                    "across one cell or half a cell, are sketches. The page prints "
                    "the slope, not these depths."
                ),
                "sine_zero_to_peak_mm": sine_mm,
                "rise_across_one_cell_mm": cell_rise_mm,
                "rise_across_half_cell_mm": half_cell_mm,
                "sine_versus_leads": against(sine_mm, leads),
                "one_cell_rise_versus_leads": against(cell_rise_mm, leads),
            }
        )

    woody = {
        "id": "woody-leighton-1994",
        "tag": "QUESTIONABLE",
        "citation": (
            "Woody et al., Design, construction, and performance of the "
            "Leighton 10.4-m-diameter radio telescopes, Proceedings of the "
            "IEEE, vol. 82, no. 5, May 1994, pp. 675 and 684"
        ),
        "url": "http://www.cso.caltech.edu/wiki/_media/cso/publications/1994-woody-procieee.pdf",
        "process": (
            "Parabolic figure machined into the exposed aluminum honeycomb "
            "core, then a 1 mm aluminum sheet epoxied on. The CSO copy adds "
            "a three-disc rotating sander for small-scale defects."
        ),
        "scale_separation": (
            "The combined techniques measure scale sizes greater than 40 mm, "
            "accuracy about 5 micrometres. Laboratory samples are spaced under "
            "40 mm and each point averages a 10 mm diameter. Scales under "
            "10 mm are attributed to the commercial sheet finish, about "
            "2 micrometres, not to a separate cell-periodic depth. A 9.5 mm "
            "cell sits inside that average."
        ),
        "figures_mm": {
            "worst_case_fabrication_rms": 0.024,
            "installed_estimate_rms": 0.024,
            "track_rms_typical_low": 0.010,
            "track_rms_typical_high": 0.015,
            "sheet_finish_under_10_mm": 0.002,
            "measurement_accuracy": 0.005,
            "cso_template_rms": 0.003,
            "cso_laboratory_estimate_rms": 0.010,
        },
        "not_delta": True,
        "beryllium_face": False,
    }
    for name, mm in woody["figures_mm"].items():
        woody.setdefault("versus_leads", {})[name] = against(mm, leads)

    nasa = {
        "id": "nasa-er-1001-print-through",
        "tag": "QUESTIONABLE",
        "citation": (
            "A. Pintz, C.H. Castle and R.R. Reimer, Solar Concentrator "
            "Technology Development for Space Based Applications, Engineering "
            "Report ER-1001, 31 December 1992, NASA Lewis grant NCC 3-77. "
            "NTRS 19950020773. Depth sentence is on the page numbered 19; "
            "3/8-cell slopes are on the page numbered 20."
        ),
        "url": "https://ntrs.nasa.gov/citations/19950020773",
        "process": (
            "Adhesive-bonded aluminum-foil honeycomb coupons, vacuum bag, "
            "Dektak II traces. Specimens through 30 use 3/16-inch cells. "
            "Figure 24 is specimen 28 with a 0.005 inch face. Figure 25's "
            "face thickness is not named on that page. Specimens 32, 33 and "
            "34 are 3/8-inch, 1/4-inch and flexcore; their face thickness is "
            "not named on the slope page. Not a beryllium face and not "
            "CR-III 3/8-1.0."
        ),
        "cell_scale_depth": {
            "where": "Figure 25",
            "printed_inch": nasa_depth_inch,
            "mm": nasa_depth_mm,
            "cell": "3/16 inch class, specimens through 30",
            "kind": "print-through dimple depth, cell scale, not panel RMS",
            "versus_leads": against(nasa_depth_mm, leads),
        },
        "cell_node_mismatch": {
            "where": "Figure 24, specimen 28, 0.005 inch face",
            "printed_inch": nasa_peak_inch,
            "mm": nasa_peak_mm,
            "kind": "random peak-to-peak of neighbouring cell nodes, not the dimple depth",
            "versus_leads": against(nasa_peak_mm, leads),
        },
        "three_eighths_cell_slopes_milliradian": {
            "low": 0.5,
            "high": 1.6,
            "kind": "maximum slope of cell-dimple profiles, not a depth",
            "projection": slope_bounds,
        },
    }

    nrao = {
        "id": "nrao-65r-30-1969",
        "tag": "QUESTIONABLE",
        "citation": (
            "S. von Hoerner, Small Surface Plates for Large Radio Telescopes, "
            "NRAO report 30, 19 September 1969, page 2. Data from discussions "
            "with Rohr."
        ),
        "url": "https://library.nrao.edu/public/memos/65/65R/65R_030.pdf",
        "process": "Commercial honeycomb radio-telescope surface, 1969 vendor figure. Cell size unstated.",
        "printed": "0.008 inch = 0.20 mm rms",
        "mm_from_printed_inch": nrao_mm_from_inch,
        "printed_mm": nrao_printed_mm,
        "kind": "whole-surface manufacturing rms, not a cell depth and not a wrinkle component",
        "versus_leads_using_inch_conversion": against(nrao_mm_from_inch, leads),
        "versus_leads_using_printed_mm": against(nrao_printed_mm, leads),
    }

    ams = {
        "id": "ams7902",
        "tag": "QUESTIONABLE",
        "what_was_obtained": (
            "An AMS7902G file whose header says page 3 of 9 and whose pdfinfo "
            "reports 3 pages. Section 1.3 says there are three sheet and plate "
            "classifications based on flatness tolerances and points to 3.5.5. "
            "Section 3.5.5 is not in the file. Revision H was not opened."
        ),
        "doi_current": "https://doi.org/10.4271/AMS7902H",
        "g_identity_read": {
            "revision": "G",
            "issued": "1961-07",
            "revised": "2015-01",
            "reaffirmed": "2018-12",
            "sheet_inch": [0.020, 0.250],
            "sheet_finish": "no greater than 55 Ra (63 microinches, 1.6 micrometres), ASME B46.1",
        },
        "class_tolerances_read": False,
        "note": (
            "Sheet flatness, once the table is obtained, is a rolled-sheet "
            "allowance. It is not cell telegraphing of a bonded panel and not "
            "the wrinkle component. The 55 Ra figure is roughness, not delta. "
            "Lead faces 0.6917 mm and 0.8434 mm sit inside the sheet band. "
            "No class number is stated here."
        ),
    }

    answer = {
        "cell_scale": (
            "The only printed cell-scale depth, 0.001651 mm on an aluminum-foil "
            "coupon, is under every needed amplitude. The 3/8-inch cells in "
            "that report are slopes. A rise held at the larger slope across a "
            "whole cell is still under the smallest needed amplitude. That "
            "bound is a projection."
        ),
        "short_wave_not_cell": (
            "Leighton figures of 0.010 to 0.024 mm rms are under every needed "
            "amplitude as numbers, on scales longer than about 10 to 40 mm. "
            "They are not the wrinkle component, and the cell is inside the "
            "10 mm average."
        ),
        "whole_panel": (
            "The 1969 honeycomb rms, 0.2032 mm from the printed 0.008 inch, "
            "is larger than every needed amplitude. It is a panel rms. Stock "
            "per-foot bows on the 032 card are the same kind of mismatch."
        ),
        "exceeded_today": (
            "Needed amplitudes are exceeded as numbers by whole-panel honeycomb "
            "rms and by per-foot shop bows. They are not exceeded by the "
            "cell-scale depth that was printed, nor by the Leighton rms on the "
            "scales that instrument measured. No page gives a beryllium face "
            "on CR-III 3/8-1.0 at the wrinkle wavelength."
        ),
        "processes": [
            "1969 commercial honeycomb, Rohr figure via von Hoerner: panel rms above the needed amplitudes",
            "stock bonded panels, per-foot or per-metre bows already on the 032 card: above, wrong gauge length",
            "machined-core plus epoxied 1 mm aluminum sheet, Leighton: rms below, scales longer than a cell",
            "aluminum-foil vacuum-bag coupons, NASA ER-1001: cell dimple below",
        ],
    }

    ended = datetime.now(ZONE)
    elapsed = time.monotonic() - mono0
    payload = {
        "unit": UNIT,
        "tag": "QUESTIONABLE",
        "not_a_certification": True,
        "nothing_here_certifies_a_hull": True,
        "started": started.isoformat(timespec="microseconds"),
        "ended": ended.isoformat(timespec="microseconds"),
        "elapsed_s": elapsed,
        "needed_lead_amplitudes_mm": leads,
        "smallest_needed_mm": smallest["delta_mm"],
        "largest_needed_mm": largest["delta_mm"],
        "woody": woody,
        "nasa_er_1001": nasa,
        "nrao_65r_30": nrao,
        "ams7902": ams,
        "answer": answer,
    }
    nfi = {
        "open": [
            {
                "id": "ams7902-class-table-unread",
                "tag": "QUESTIONABLE",
                "note": (
                    "AMS7902G section 3.5.5 was not in the three-page file. "
                    "Current revision H, DOI 10.4271/AMS7902H, was not opened. "
                    "No class tolerance is stated."
                ),
            },
            {
                "id": "no-beryllium-face-at-wrinkle-wavelength",
                "tag": "QUESTIONABLE",
                "note": (
                    "No page read here gives a zero-to-peak amplitude of an "
                    "as-bonded beryllium face on CR-III 3/8-1.0 at the CR-1457 "
                    "wrinkle wavelength. That wavelength was not computed on 032 "
                    "and is not computed here."
                ),
            },
            {
                "id": "optical-bench-and-space-mirror-unread",
                "tag": "QUESTIONABLE",
                "note": (
                    "A space-mirror or optical-bench sandwich with a measured "
                    "cell-print depth was not opened. The space sandwich that "
                    "was opened is the aluminum solar-concentrator coupon, not "
                    "an optical bench. Publisher gates blocked a 2025 panel-unit "
                    "abstract on this pass."
                ),
            },
            {
                "id": "hexcel-telegraph-depth-still-unprinted",
                "tag": "QUESTIONABLE",
                "note": (
                    "A text extract of the local HexWeb attributes brochure "
                    "contains no telegraphing depth. This pass does not add a "
                    "depth Hexcel did not print."
                ),
            },
            {
                "id": "three-eighths-slope-is-not-a-depth",
                "tag": "PROJECTION",
                "note": (
                    "ER-1001 prints 0.5 to 1.6 milliradian on 3/8-inch cells "
                    "and does not print the matching depth. The sine and the "
                    "slope-times-cell sketches are labelled projections."
                ),
            },
            {
                "id": "transfer-to-the-lead-faces",
                "tag": "QUESTIONABLE",
                "note": (
                    "Leighton faces are 1 mm aluminum on a machined core. The "
                    "ER-1001 faces are aluminum foil, 0.003 to 0.016 inch in "
                    "the series, thinner than the lead sheets, and the core "
                    "on the depth trace is 3/16 inch. Neither is S-200F or "
                    "SR-200 on CR-III 3/8-1.0. Flatwise tension and the "
                    "beryllium bond remain unprinted, so the 60 psi amplitudes "
                    "stay an upper bound only if that F_c is real."
                ),
            },
            {
                "id": "panel-rms-is-not-delta",
                "tag": "PROJECTION",
                "note": (
                    "Treating the 0.20 mm honeycomb rms, or a per-foot shop bow, "
                    "as the wrinkle component exceeds the needed amplitudes only "
                    "by using the wrong spatial piece."
                ),
            },
        ]
    }
    origin = {
        "origin": started.isoformat(timespec="microseconds"),
        "origin_monotonic_s": mono0,
    }
    text = json.dumps(payload, indent=1) + "\n"
    nfi_text = json.dumps(nfi, indent=1) + "\n"
    origin_text = json.dumps(origin, indent=1) + "\n"
    RESULTS_PATH.write_text(text)
    NFI_PATH.write_text(nfi_text)
    ORIGIN_PATH.write_text(origin_text)
    print(f"elapsed_s {elapsed:.12g}")
    print(f"nasa_depth_mm {nasa_depth_mm:.12g}")
    print(f"nasa_peak_mm {nasa_peak_mm:.12g}")
    print(f"nrao_mm {nrao_mm_from_inch:.12g}")
    print(f"smallest_needed_mm {smallest['delta_mm']:.12g}")
    print(f"largest_needed_mm {largest['delta_mm']:.12g}")
    for bound in slope_bounds:
        print(
            "slope",
            bound["slope_milliradian"],
            "sine_mm",
            f"{bound['sine_zero_to_peak_mm']:.12g}",
            "one_cell_mm",
            f"{bound['rise_across_one_cell_mm']:.12g}",
            "half_cell_mm",
            f"{bound['rise_across_half_cell_mm']:.12g}",
        )
    depth_over = nasa["cell_scale_depth"]["versus_leads"]
    for row in depth_over:
        print(
            "depth_over",
            row["face"],
            row["Q"],
            row["Fc_basis"],
            f"{row['measured_over_needed']:.6g}",
            row["needed_amplitude_exceeded_as_a_number"],
        )


if __name__ == "__main__":
    main()
