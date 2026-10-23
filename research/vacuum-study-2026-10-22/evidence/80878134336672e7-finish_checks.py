#!/usr/bin/env python3
from check_model import B
from check_grids import run as grid
from check_extras import run as extras
from build_check import run as build

for frozen in (False,True):
    label="FROZEN" if frozen else "COUPLED"
    for R in (10,12,15,20,30):
        if not (B/f"{label}-GRID-CHECK-R{R}.json").exists():
            grid(R,frozen)
extras()
build()
if not (B/"CHECK-HEADLINES.png").exists():
    import plot_check
