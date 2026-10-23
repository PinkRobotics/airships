#!/usr/bin/env python3
"""Compare target-load output before permitting the shorter elastic ramp."""
import json
from data_tools import ROOT,P0,summary,at_pressure,path

def main():
    reference="mesh512g2-f2c6-a1-cap"
    trial="target-ramp5-a1-cap"
    points=[]
    for sf in [1.,1.05]:
        a=at_pressure(reference,P0*sf)
        b=at_pressure(trial,P0*sf)
        assert a and b
        points.append(dict(SF=sf,reference_MPa=a["max_mises_MPa"],
            trial_MPa=b["max_mises_MPa"],
            difference_MPa=b["max_mises_MPa"]-a["max_mises_MPa"],
            trial_interpolation=b["interpolation"]))
    hist=path(trial)
    passed=(summary(trial)["endpoint_kind"]=="load_cap" and
        all(abs(p["difference_MPa"])<.01 and
            p["trial_interpolation"].startswith("native") for p in points) and
        all(p["max_peeq"]<=1e-10 for p in hist))
    result=dict(passed=passed,reference=reference,trial=trial,
        reference_increments=summary(reference)["increments"],
        trial_increments=summary(trial)["increments"],points=points,
        stress_agreement_tolerance_MPa=.01,
        scope="Identical pre-yield law and geometry at a=1 mm. Both load histories reach service and 1.05 service at native increments. Actual-yield boundary confirmations remain separate.",
        reference_solver_s=summary(reference)["solver"]["elapsed_s"],
        trial_solver_s=summary(trial)["solver"]["elapsed_s"])
    (ROOT/"TARGET-RAMP-CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result))
    assert passed

if __name__=="__main__":main()
