"""Focused mesh checks and validation of the fixed-demand minimum-wall witnesses."""
import gc
from material_models import models
from frame_fe import solve

mats={m["id"]:m for m in models()}
for key in ["041-reference","K13D2U-50-20-20-10"]:
    for removed in [None,551,123]:
        solve(mats[key],"5",12,"same_tube_mass",removed)
        gc.collect()
for key in ["Hexoloy-SA","CVD-PureSiC-HR","M55J-50-20-20-10",
            "K13D2U-50-20-20-10","T700S-70-10-10-10","Al6061T6"]:
    for reserve in ["5","019"]:
        solve(mats[key],reserve,6,"minimum_wall_q1_screen")
        gc.collect()
