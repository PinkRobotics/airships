"""Two ledger checks the design point did not resize. QUESTIONABLE. PROJECTION."""
import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "model"))
import model63  # noqa: E402

RUN = json.load(open(os.path.join(OUT, "RUN.json")))
FACTOR = RUN["design"]["factor_used"]
TF = RUN["design"]["primary"]["geometry"]["tf_m"]
TC = RUN["design"]["primary"]["geometry"]["tc_m"]
FACTORS = {"Q": 1.0, "face_density": FACTOR}
REVERT = ("Q", "gamma")


def main():
    natural = float(model63.BETA)
    model63.BETA = 1.0
    point = model63.p2(
        30, "optimistic", TF, TC, factors={"Q": 1.0, "face_density": FACTOR},
        basis="endpoint", maturity="concept", detail=True,
        revert=("Q", "gamma", "face_modulus"))
    modes = {key: float(value) for key, value in point["modes"].items()}
    print("modulus_frozen", float(point["payload_kg"]),
          "buck", modes["global_buckling"], "wr", modes["face_wrinkling"],
          "min", min(modes.values()))
    model63.BETA = natural
    resized = model63.p2_opt(
        30, "optimistic", FACTORS, basis="endpoint", maturity="concept",
        n=200, revert=REVERT)
    frozen = model63.p2(
        30, "optimistic", TF, TC, factors=FACTORS, basis="endpoint",
        maturity="concept", detail=True, revert=REVERT)
    print("beta_natural", natural)
    print("beta_frozen_payload", float(frozen["payload_kg"]),
          "wr", float(frozen["modes"]["face_wrinkling"]),
          "buck", float(frozen["modes"]["global_buckling"]))
    print("beta_resized_payload", None if resized is None else float(resized["payload_kg"]),
          "floats", resized is not None and float(resized["payload_kg"]) >= 0)


if __name__ == "__main__":
    main()
