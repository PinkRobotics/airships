"""Evidence integrity, numeric coverage and independent plate boundary checks."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT / "INPUTS.json").read_text())
R = json.loads((ROOT / "RESULTS.json").read_text())
T = json.loads((ROOT / "THERMAL-COMPARISON.json").read_text())
A = json.loads((ROOT / "AUDIT.json").read_text())
checks = list(R["checks"]) + list(T["validation"])
for p in D["pins"]:
    b = Path(p["path"]).read_bytes()
    checks.append({"check": "source pin " + p["path"],
                   "passed": len(b) == p["bytes"] and hashlib.sha256(b).hexdigest() == p["sha256"]})
checks.append({"check": "all numeric leaves covered",
               "passed": R["summary"]["numeric_fields"] == R["summary"]["numeric_fields_covered"] == 541})
checks.append({"check": "one audit row per path",
               "passed": len(A) == len({(a["row"], a["field"]) for a in A})})

# Solve the piecewise axisymmetric plate boundary conditions numerically.
# This independently checks the proposed uniform-boss, simply-supported model.
# Normalize force, outer radius and flexural rigidity to one.
for ratio in [.065, .1, .25, .5, 1.]:
    nu, a, b, force, rigidity = .33, 1., ratio, 1., 1.
    q = force / (math.pi * b*b)
    fixed = force / (8 * math.pi * rigidity)

    def boundary(z):
        c0, c1, B, C, d0 = z
        w1 = q * b**4 / 64 + c1 * b*b + c0
        dw1 = q * b**3 / 16 + 2*c1*b
        ddw1 = 3*q*b*b / 16 + 2*c1
        w2 = fixed*b*b*math.log(b) + B*b*b + C*math.log(b) + d0
        dw2 = fixed*b*(2*math.log(b)+1) + 2*B*b + C/b
        ddw2 = fixed*(2*math.log(b)+3) + 2*B - C/b**2
        w_at_a = B + d0
        mr_at_a = -(fixed*3 + 2*B - C + nu*(fixed + 2*B + C))
        return np.array([w1-w2, dw1-dw2, ddw1-ddw2, w_at_a, mr_at_a])

    offset = boundary(np.zeros(5))
    matrix = np.column_stack([boundary(np.eye(5)[i])-offset for i in range(5)])
    solution = np.linalg.solve(matrix, -offset)
    moment = -2*(1+nu)*solution[1]
    proposed = force/(4*math.pi)*((1+nu)*math.log(a/b)+1-(1-nu)*b*b/(4*a*a))
    error = float(max(abs(boundary(solution))))
    checks.append({"check": f"plate boundary-value solution b/a={ratio}",
                   "moment_from_boundary_solution": moment, "proposed_moment": proposed,
                   "max_boundary_residual": error,
                   "passed": math.isclose(moment, proposed, rel_tol=1e-11, abs_tol=1e-12) and error < 1e-11})

passed = sum(bool(c["passed"]) for c in checks)
record = {
    "tag": "Numerical verification of specified equations; no physical qualification",
    "checks": checks, "total": len(checks), "passed": passed,
    "numeric_audit_summary": R["summary"],
    "source_pins_checked": len(D["pins"]),
    "owner_executable": "hash only; never inspected/imported/executed"
}
(ROOT / "VALIDATION.json").write_text(json.dumps(record, indent=2) + "\n")
assert passed == len(checks), [c for c in checks if not c["passed"]]
print(json.dumps({"total": len(checks), "passed": passed, "source_pins": len(D["pins"])}))
