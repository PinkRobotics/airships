#!/usr/bin/env python3
"""Full requested factorial, saved after each radius/weather/account group."""
import itertools
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from model import *

start = time.monotonic()
rows = []
for r, weather, floor, padchoice, vented in itertools.product(
        I["radii_m"], ["ISA", "optimistic", "both"], [False, True],
        ["light20", "heavy70"], [True, False]):
    s = Settings(weather=weather, floor=floor, pad=padchoice, vented=vented)
    result = least(r, s)
    # 028b's two named factors already assume the thin film. That is mask 11
    # in this explicitly four-axis bookkeeping, not mask 3 (.030 film).
    endpoint = next(t["solution"] for t in result["endpoint_trials"] if t["mask"] == 11)
    row = dict(id=f"R{r}-{weather}-{'floor' if floor else 'actual'}-{padchoice}-"
                  f"{'vented' if vented else 'unvented'}",
               R_m=r, weather=weather, floor=floor, pad=padchoice, vented=vented,
               least=result, two_factor_endpoint=endpoint)
    rows.append(row)
    dump(B/"RESULTS.json", dict(rows=rows, elapsed_s=time.monotonic()-start, complete=False))
    lp = result["least"]
    print(row["id"], "least", None if lp is None else (lp["selected_axes"], round(lp["usage"],6)),
          "endpoint_kg", None if endpoint is None else round(endpoint["signed_payload_kg"],3),
          flush=True)
dump(B/"RESULTS.json", dict(rows=rows, elapsed_s=time.monotonic()-start, complete=True,
                           finished_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat()))
