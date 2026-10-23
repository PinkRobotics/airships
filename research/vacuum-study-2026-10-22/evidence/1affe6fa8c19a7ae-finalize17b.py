#!/usr/bin/env python3
"""MAINLINE-017b: RESULTS.json, NFI.json and INPUTS.json from COMPUTE.json, TRENDS.json and EXTRA.json."""
import datetime
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "unpublished-local-ref:6e94df3272e3fba2"
C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
T = {t["id"]: t for t in json.load(open(os.path.join(HERE, "TRENDS.json")))["trends"]}
X = json.load(open(os.path.join(HERE, "EXTRA.json")))
JOB_STARTED = "2026-10-20T01:25:38-07:00"


def pin(path, role):
    b = open(path, "rb").read()
    return {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "role": role}


def tidy(rec):
    """Drop the bulky per-step geometry dictionaries' numpy-free duplicates; keep everything numeric."""
    return rec

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

nfi = {"schema": 1, "card": "MAINLINE-017b", "unit": "vacuum-mainline017b-improvement-directions-1020",
       "tag": "QUESTIONABLE", "status": "OPEN", "items": [
    {"id": "NFI-017b-VC2-STEP", "tag": "QUESTIONABLE",
     "claim": "Face modulus alone reaches SF 1 only at Vc 2, where CR-1457's gamma steps from 0.20 to 1; the point is a "
              "knife edge that re-optimisation cannot hold (the crimp-branch answers re-check at 0.756/0.789).",
     "needed_to_ground": "MAINLINE-029's measured crimp-branch gamma at the lead geometry."},
    {"id": "NFI-017b-JOINT-ALLOWANCE", "tag": "QUESTIONABLE",
     "claim": "Explicit 028 joining replaces the 5% joint allowance, as 028 did. Under the 5% floor of 019, 021b and 027, "
              "sheet size and bond film stop being levers at all. The reserve is 019's optimistic (sealed-service) set, "
              "scaled with radius by 027's laws.",
     "needed_to_ground": "A ruling on whether the 5% allowance is a floor once joining is explicit."},
    {"id": "NFI-017b-POISSON", "tag": "QUESTIONABLE",
     "claim": "nu 0.08 is the S-200F VHP mean (IAEA) transferred to SR-200 sheet; the inherited 0.33 reads 2.0 percent "
              "higher (0.5387 / 0.5818 against 0.5284 / 0.5711).",
     "needed_to_ground": "A measured in-plane Poisson ratio for cross-rolled SR-200 sheet."},
    {"id": "NFI-017b-GAMMA-TRANSLATION", "tag": "QUESTIONABLE",
     "claim": "The brief's translation of gamma into core shear stiffness per density cannot reach SF 1 (Kc caps at 1). "
              "As shape precision, MAINLINE-015's monocoque-equivalent map (t_eq = sqrt(3) h) gives a 2.47 mm dimple at "
              "R 10 and 13.1 mm at R 20; that map is a cylinder/monocoque fit applied to a sandwich sphere.",
     "needed_to_ground": "An imperfection-controlled sandwich-sphere or dome buckling test series."},
    {"id": "NFI-017b-FLATNESS-TRANSLATION", "tag": "QUESTIONABLE",
     "claim": "Q is translated to waviness with CR-1457 eq 2.2-12/13 using Fc = 60 psi (typical stabilised "
              "compression, taken as the lowest flatwise strength). The lever holds K_delta; physical waviness depends "
              "on Ec and Fc (0.347 mm today's equivalent at R 10; 0.099 mm in the Be-kept material combination).",
     "needed_to_ground": "Measured flatwise tension and bond strength for the Be/CR-III bond, and measured face waviness."},
    {"id": "NFI-017b-SIC-ALLOWABLE", "tag": "QUESTIONABLE",
     "claim": "Every P3 route to SF 1 needs a qualified SiC design compressive strength of 0.83-1.20 GPa (projection row "
              "0.91 GPa). No design compressive allowable exists; flexure is 380 MPa and 3900 MPa is an unqualified "
              "typical value.",
     "needed_to_ground": "Full-size curved tube compression tests with a Weibull (or other probabilistic) basis."},
    {"id": "NFI-017b-TUBE-MATERIAL", "tag": "PROJECTION",
     "claim": "Tube specific stiffness x1.41 (186 MPa per kg/m3) is beyond SiC (best CVD 145). A carbon-fibre tube "
              "would need a sourced compressive strength near 0.8-1.2 GPa with that stiffness.",
     "needed_to_ground": "Sourced UHM carbon tube compressive strength and modulus."},
    {"id": "NFI-017b-FACE-MATERIAL", "tag": "PROJECTION",
     "claim": "A lighter face at beryllium's E and strength (x1.73-1.87, 272-293 MPa per kg/m3) has no thin isotropic "
              "candidate: quasi-isotropic carbon is about 100 (a worker estimate with assumed matrix constants); "
              "nano-carbon films are lab only.",
     "needed_to_ground": "Sourced in-plane-isotropic properties of nano-carbon or other candidate face sheets."},
    {"id": "NFI-017b-CORE-EC", "tag": "QUESTIONABLE",
     "claim": "With beryllium and handbook values kept, the core needs through-thickness stiffness per density of 41-57 "
              "MPa per kg/m3, beyond aluminium's 24.8; no carbon-honeycomb compressive modulus was sourced, and the "
              "Ultracor shear value is secondary (a 2023 paper quoting 2012).",
     "needed_to_ground": "A primary carbon-honeycomb datasheet with stabilised compressive modulus."},
    {"id": "NFI-017b-P3-SEARCH", "tag": "QUESTIONABLE",
     "claim": "P3 uses 022c's equilateral rows only; the two-way grid is not scored. The finer film grid and polish lift "
              "022c's rows by 1.1 and 1.7 percent (0.7017 to 0.7097; 1.4170 to 1.4412).",
     "needed_to_ground": "022's owner's view on the two-way grid's stability with the film."},
    {"id": "NFI-017b-FILM-RULE", "tag": "QUESTIONABLE",
     "claim": "024's half-of-tensile design rule is carried to every film in the trend (Upilex-S comparison); barrier, "
              "creep and seaming are not scored. The 1975 Kapton H row prints no density; Kapton HN's 1420 is used.",
     "needed_to_ground": "Film design allowables with barrier and creep for Upilex-S class films."},
    {"id": "NFI-017b-TREND-GAPS", "tag": "QUESTIONABLE",
     "claim": "Eras not found: beryllium datasheets of about 2006 and 2016; Hexoloy datasheets of about 1996 and 2016; "
              "any carbon-honeycomb history; Wright 1965 and JGJ 7-2010 (the lattice 0.4 and 0.2) were not read; "
              "Krenzke 1963 not opened. Identical Hexcel tables may mean no re-testing rather than no progress.",
     "needed_to_ground": "The missing datasheets (Wayback rate limits blocked some)."},
    {"id": "NFI-017b-CORE-CHOICE", "tag": "QUESTIONABLE",
     "claim": "Directions are computed on the lead's CR-III 5056 3/8-1.0; 5056 1/4-1.6 is 2.7 percent better today "
              "(0.5425 / 0.5939).",
     "needed_to_ground": "None for the ranking; factors on 1/4-1.6 would be slightly smaller."},
    {"id": "NFI-017b-SCARF", "tag": "PROJECTION",
     "claim": "The scarf is steepened beyond 30:1 to meet 028's 10 MPa average-shear screen, which is owner-selected, "
              "not an allowable; bond and seam strengths are unmeasured (028's rows).",
     "needed_to_ground": "028's evidence needs: a weighed, load-tested curved Be/Al panel."},
    {"id": "NFI-017b-COMBINATION-METRIC", "tag": "QUESTIONABLE",
     "claim": "The product of factors depends on how a property is parametrised (Q against Ec = Q^2; K_delta against "
              "physical waviness). Each lever's definition is stated so a reader can re-weight.",
     "needed_to_ground": "None; a reading note."},
]}
with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
    json.dump(nfi, fh, indent=1)
os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))

pins = [dict(v, role="input read; " + k) for k, v in C["pins"].items()]
for name in ("be-face", "core-film", "knockdown", "p3-materials"):
    pins.append(pin(f"{SRC}/{name}.json", "this seat's sourcing file (sub-worker)"))
    pins.append(pin(f"{SRC}/{name}.md", "this seat's sourcing summary (sub-worker)"))
for name in ("model17b.py", "val17b.py", "scan17b.py", "combo17b.py", "run17b.py", "extra17b.py", "trend17b.py",
             "card17b.py", "finalize17b.py", "COMPUTE.json", "EXTRA.json", "TRENDS.json"):
    pins.append(pin(os.path.join(HERE, name), "this card's own code or intermediate"))
inputs = {"schema": 1, "card": "MAINLINE-017b", "unit": "vacuum-mainline017b-improvement-directions-1020",
          "pins": pins,
          "reports_used": ["rpt-ref-769a7442efd5a04681e9",
                           "rpt-ref-1080d4f6a1af4cfa8c67",
                           "rpt-ref-2519e14e5d71b9eb18f3", "rpt-ref-2898e43e4928e833af6d",
                           "rpt-ref-d7f99cd71e977826da48", "rpt-mainline022c-grok-sag-in-scan-1020",
                           "rpt-mainline022b-grok-equilibrium-1020", "rpt-mainline022-grok-p3-optimistic-floating-point-1020",
                           "rpt-ref-a4768f77870336c8cdbb", "rpt-ref-4f09fd6b4c4dd848ebb0",
                           "rpt-ref-2bb3c2b520a8e5f8c750", "rpt-ref-58c781cbea9c220eb5b4",
                           "rpt-ref-ab7c8365b0b450980f1f",
                           "rpt-mainline017-improvement-directions-lead4f19-1019"]}
with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
    json.dump(inputs, fh, indent=1)
os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
print("RESULTS", os.path.getsize(os.path.join(HERE, "RESULTS.json")), "NFI", len(nfi["items"]), "pins", len(pins))
