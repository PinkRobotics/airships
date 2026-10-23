#!/usr/bin/env python3
"""MAINLINE-058: NFI.json and INPUTS.json; prints the artifact pins (CARD, RESULTS, NFI, INPUTS)."""
import hashlib
import json
from pathlib import Path

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline058-flyable-band-1020"
S = ME / "work/scripts/band058"
W = Path("unpublished-local-ref:7a5bf1cec24b249e")
SUB = Path("unpublished-local-ref:ab52dba26d6cc3a7")
SCR = Path("unpublished-local-ref:328c3cdb361f38a6"
           "62008c44-5149-4121-bd7d-8db0f4ad70e6/scratchpad")


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


NFI = [
    ("N058-01-COLD-EDGE", "open", "P2's cold edge is the inherited 037b/048 bond-interface screen (Be/Al CTE mismatch from the 200 F "
     "cure): outer-skin minimum >= 264.03 K. It is not validated by cold assembled-interface tests (050 NFI50-05). It applies on "
     "the ground as well as in flight: a moored hull also needs cover, heating or a low-emittance finish on cold clear nights."),
    ("N058-02-FINISH-TRANSFER", "PROJECTION", "Al + acrylic overcoat (Sheldahl film product, A 0.14, eps 0.05), TARC (a roof coating, "
     "cold state A ~0.25, sky-window eps 0.20) and the switchable eps 0.05 night state (050) are transfers to a Be skin. Installed "
     "mass, adhesion, UV and humidity life and wet optics are unknown; areal mass was held at MLCCAg's 8.33 g/m2. 048's legacy "
     "finish screen (037 day SF >= 1.678, full-cycle >= 1) was not evaluated. The static Al+AOC skin reaches 319 K by day at ISA. "
     "A switchable state must switch by skin temperature, not by sun: in its day state the edge is 269.7 K without sun credit."),
    ("N058-03-CLIMB-AIRSPACE", "open", "Relief by climbing needs room: at Heathrow the -30 hPa design climbs 268 m median, 426 m at the "
     "99th percentile and 510 m at most above the 100 m floor; the 0 hPa P3 design 60/198/270 m; floating free (no dump) 0.7-1.7 km. "
     "Airspace ceilings and traffic rules are not modelled."),
    ("N058-04-TRIM-AIR", "open", "Air admitted for relief or to dump lift cannot be pumped back in flight: 034's onboard pumps need "
     "264-416 h (E2M28) or 8,062-12,709 h (KNF N920) at R10. Re-evacuation is a ground task, about 16-20 h per flown day at 052's "
     "effective ground speed (1574.9 m3/h per 4188.8 m3), against 24.5 h for a full evacuation. Energy is bracketed: ideal "
     "isothermal 23-50 kWh (R10) to 900-1,530 kWh (R30) per day; Edwards GXS-class sets list 1,900-2,200 m3/h and 7.5-29.5 kW "
     "rated across the family (not tied to a model). P3 admitted air must be dried for the 052/054 dry cavity. After a pressure "
     "fall, trim air lowers lift with no in-flight recovery."),
    ("N058-05-BALLAST", "PROJECTION", "The water-ballast bladder is charged at 2 % of capacity; pillow-tank listings give 0.35-0.93 % "
     "for the fabric of 1,500-10,000 L ground tanks, not flight hardware. Capacity is the cold-day excess lift: 322-536 kg at R10 and "
     "13.9-19.7 t at R30 for the widest bands. Refill is at the mooring; drain control and load paths are not designed. The dump is "
     "needed only to hold altitude at fixed payload; a variable payload can absorb the excess."),
    ("N058-06-BOUNDARY-LAYER", "PROJECTION", "Heathrow 2 m observations are mapped to the 100 m centre with 050's 6.5 K/km lapse and a "
     "constant vapour mole fraction. Real night inversions (warmer aloft: helps P2's cold edge) and daytime superadiabatic layers "
     "(cooler aloft: helps lift) are not represented."),
    ("N058-07-SKY-AND-WIND", "PROJECTION", "The primary cold test applies 050's clear-sky depressions every night (24.9 K) and day "
     "(9.9 K, no sun credit): conservative. The cloud-aware sensitivity mixes clear and overcast (2 K) sky radiance by observed "
     "oktas; 3.1 % of hours have no cloud report and are treated as clear. Wind is fixed at 2 m/s."),
    ("N058-08-DAYS-METRIC", "open", "A day counts only if all 24 UTC hours lie inside the band; days with a missing hour are dropped "
     "(87,354 of 87,648 hours complete). One site, 2014-2023. Gusts beyond the 70 kn design, precipitation, hail (045), icing and "
     "lightning are outside the band. The fractions are not availability guarantees."),
    ("N058-09-P3-COLD", "open", "P3's account has no cold screen: SiC/PBO/sleeve CTE mismatch and the PBO film at low temperature are "
     "unscreened, so its band is open on the cold side. Its dry-cavity humidity limit tightens as the film gets colder (052), "
     "shortening the ground interval on cold days."),
    ("N058-10-P3-SCALING", "PROJECTION", "P3 mass against design load is a log-linear fit per item through 052's three loads "
     "(97.2-99.7 kPa): SiC tubes ~p^0.445 at the endpoints, PBO ~p^1.0, sleeves ~p^2. The full-range load 103.95 kPa is a 4.3 % "
     "extrapolation. 052's ISA payloads are reproduced within 0.06 kg; its force field and sizing were not re-solved."),
    ("N058-11-MGA", "open", "With 057's sourced concept-stage mass-growth allowance (15-30 %) no hull of either lead floats at any "
     "radius; every band here assumes flight-proven masses."),
    ("N058-12-DYNAMIC-LIFT", "PROJECTION", "Thrust: momentum theory with FM 0.70, motor/drive 0.85, 0.5 kg/kW, 108 Wh/kg usable. Kite: "
     "CL 1.0, 0.2 kg/m2 sail and spars, 1/7-power shear from 10 m. A kite needs a tether; load introduction into the shell is "
     "unscreened, as for 045's mooring."),
    ("N058-13-NIGHT-HEATING", "PROJECTION", "Heater, cable and battery integration are unpriced; 12-hour clear-night energy at 050's "
     "108 Wh/kg usable. Flight use is limited to about 1-2 K at R10; ground power on the mooring is assumed available."),
    ("N058-14-GROUND-CASE", "open", "On the ground (centre at z = R) on a high-pressure day the load exceeds the 100 m floor's; relief "
     "by admitting air covers it, but 050's grid starts at 100 m and the moored load path is not re-checked."),
    ("N058-15-MIL-MARKERS", "PROJECTION", "No relieved hull of either lead floats on any MIL-HDBK-310 hot marker up to R30: 10 % hot day "
     "at R30 P2 -2,956 to -3,853 kg, P3 -886 kg (0.7 % of its mass). This is not an impossibility proof beyond R30."),
    ("N058-16-LEAST-SETS", "limitation", "Least optimism sets are the fewest axes at their endpoints (usage 1) reaching a coverage "
     "target, with the best finish, design pressure and relief; common-usage roots below 1 were not refined."),
    ("N058-17-DESIGN-TEMPERATURE", "limitation", "Every fixed hull is sized at its finish's own clear-night cold threshold, as 050's "
     "builds; finish mass differences come from the day thermal gradient and curvature terms only."),
]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
