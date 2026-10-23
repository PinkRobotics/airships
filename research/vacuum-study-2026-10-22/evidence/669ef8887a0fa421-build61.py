"""Build the reviewable handoff from computed results; no scientific reruns."""
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def pin(path):
    p = Path(path)
    raw = p.read_bytes()
    return {"path": str(p.resolve()), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(map(str, row)) + " |" for row in rows])


def num(x, digits=1):
    return "not alone" if x is None else f"{x:,.{digits}f}"


d = read("CALCULATIONS.json")
# The separate battery column changes this secondary target by <0.000001.
for x in d["p3"]:
    b = x["deficit"]["concept"]
    tube = b["bill_kg"]["SiC_tubes"] + b["growth_kg"]["SiC_tubes"]
    remainder = b["mass_before_growth_kg"] + b["growth_total_kg"] - tube
    x["additional_tube_mass_reduction_factor_if_other_items_fixed"] = tube / (b["lift_kg"] - remainder)
write("CALCULATIONS.json", d)

idx = read("SOURCE-INDEX.json")
used = []
unmapped = []
for p in sorted((ROOT / "sources").iterdir()):
    if not p.is_file() or "--" not in p.name or p.name.startswith("brief--"):
        continue
    label, name = p.name.split("--", 1)
    entry = idx.get(label, {}).get("artifacts", {}).get(name)
    if entry is None:
        unmapped.append(p.name)
        continue
    local = pin(p)
    assert local["sha256"] == entry["sha256"] and local["bytes"] == entry["bytes"], p
    used.append({"label": label, "name": name, "upstream": entry, "local_copy": local,
                 "use": "numerical input or inspected method/evidence; owner code not executed"})
assert not unmapped, unmapped
brief_root = Path("unpublished-local-ref:792ada9d1fcd5e54")
brief_hashes = {
    "CARD-061-IMPROVEMENT-TARGETS-WITH-GROWTH.md": "62acaa28ff9b2c30a06eedf7446a98c5670a62d194a9806942d9cbe286edb057",
    "COMMON.md": "2a7909da11b7b6925f8e21d0b0c0bde49d65c76ad5ff4e3ac798f262f516666a",
    "PROCESS-v2.md": "be858ac11e1e4adc8e164157752df002a8edce54b62f077eb6b95f89d3e7c11a",
}
briefs = []
for name, digest in brief_hashes.items():
    p = pin(ROOT / "sources" / ("brief--" + name))
    assert p["sha256"] == digest, name
    briefs.append({"local_copy": p, "original_path": str(brief_root / name),
                   "declared_sha256": digest})
inputs = {
    "schema": "mainline061-inputs-v1", "unit": UNIT, "order": ORDER, "tag": TAG,
    "briefs": briefs, "brief_integrity_and_authority_pins": read("BRIEF-PIN-RECOVERY.json"),
    "upstream_files_actually_copied_or_inspected": used,
    "upstream_report_ids": {k: v["report"] for k, v in idx.items() if "report" in v},
    "primary_web_sources": read("WEB-SOURCES.json"),
    "source_handbook": {
        "P2": "Pinned 040/048: Be sheet, CRIII 5056 3/8-1.0 core, bond film and NASA sandwich screens.",
        "P3": "Pinned 052: SiC f5-019 family and projected PBO membrane; 054 SIOX/3A seven-day service.",
        "history": "Pinned 017b trend records retain maker/paper URLs, dates, basis and uncertainty.",
        "mass_growth": "NASA NTRS 20120013284 Table VI-1; actual image checked, hardware/battery columns separated.",
    },
    "factor_definition": {
        "positive": "strength, modulus, gamma, Q, core shear and retention multiply; physical caps apply",
        "inverse": "density and mass factors divide the property",
        "reference": "all factors are relative to the stated endpoint or handbook basis, never a silently changed denominator",
    },
    "geometry_domains": {
        "P2": {"tc_m": "[0.0012*R/10, 1.4*R/10]", "tf_m": "[1e-6, min(.0195,.008*R/10)]"},
        "P3": {"topology": "f5-019, 252 nodes/750 members/500 bays", "g_over_R": .00868494175,
               "resizing": "minimum tube section in this family; continuous membrane gauge at every factor",
               "unresolved": "global topology/g-over-R reoptimization"},
    },
    "growth_rates": {"concept_structure": .15, "concept_hardware": .30,
                     "concept_thermal": .20, "concept_battery": .25,
                     "TRL7_nonbattery": .05, "TRL7_battery": .06},
    "material_constants": {
        "Be_density_kg_m3": 1850, "endpoint_E_Pa": 293.6e9, "endpoint_strength_Pa": 379.2e6,
        "handbook_E_Pa": 290e9, "handbook_strength_Pa": 345e6,
        "core_rho_kg_m3": 16.018463, "core_G_W_Pa": 46.884e6, "core_Ec_Pa": 103.421e6,
        "endpoint_Q": .82, "handbook_Q": .33,
        "endpoint_film_kg_m2_interface": .0732364, "finish_kg_m2_including_10pct": .00833272,
        "PBO_ply_strength_Pa": 5.8e9, "PBO_density_kg_m3": 1560,
        "ten_year_retention": .9511101304657719, "SiC_assumed_compression_Pa": 3.9e9,
    },
    "method": "METHOD.md; exact constants and equations in model61.py override rounded explanatory values",
    "generated": now,
}
write("INPUTS.json", inputs)

nfi_specs = [
    ("P2-PHYSICS", "QUESTIONABLE", "open",
     "Scalar global, wrinkling, scarf and thermal screens do not qualify a complete sandwich sphere.",
     "Tests/validated nonlinear analysis for the resized hull, joints, defects and coupled loads."),
    ("BE-ALLOWABLE", "QUESTIONABLE", "open",
     "Be endpoint and handbook tensile-yield/elastic values are transferred to thin-sheet compression; endpoint properties need not coexist in one product.",
     "Traceable compressive allowable and thermal properties for the proposed sheet and fabrication process."),
    ("DENSITY-TARGET", "PROJECTION", "open",
     "A lower-density face preserving all Be mechanics and thermal constants is synthetic; elemental Be cannot simply change density.",
     "A specific replacement material demonstrating the combined in-plane properties, compression, joining and thermal compatibility."),
    ("LARGE-R-THERMAL", "PROJECTION", "open",
     "R20/R30 use 040 temperatures with 048 finish mass; the later cure term changes global demand and hence the near-zero TRL7 result.",
     "Recomputed thermal/residual stress field for the exact large-R coating, geometry and cure history."),
    ("GAMMA-047", "QUESTIONABLE", "open",
     "047 has a conditional R10 dimple result, not an invertible gamma-to-tolerance law at resized R12/R20/R30.",
     "Imperfection sweeps with calibrated core in-plane law and measured seams for each target geometry."),
    ("CORE-COUPLING", "PROJECTION", "open",
     "Core specific-shear improvement is represented by G rising at fixed density/strength; thermal mismatch shear rises with sqrt(G).",
     "A complete alternate-core row including G, Ec, in-plane stiffness, conductivity, CTE, shear strength and bond behavior."),
    ("MASSLESS-FUNCTION", "PROJECTION", "open",
     "Reduced bond, finish, film and node masses retain structural, optical and barrier functions by assumption.",
     "Fabricated areal masses with function demonstrated at scale; minimum practical gauges and joint features."),
    ("MGA-MATURITY", "PROJECTION", "open",
     "15/30/20 plus separate battery growth is an inherited mixed-maturity scenario; many allocations and a system-level margin are excluded.",
     "Component-specific maturity evidence and a declared complete reserve policy; no TRL7 certification is asserted."),
    ("NASA-COLUMN", "QUESTIONABLE", "corrected_here_pending_REVIEW_A",
     "057/CHECK-057 used 6% TRL7 hardware; primary Table VI-1 has 5%, with 6% in the adjacent battery column.",
     "Independent confirmation of the table image and revised class arithmetic; no additional action is assigned by this report."),
    ("JOINING-FLOOR", "PROJECTION", "open",
     "Actual joining and the retained 5% structure floor produce different targets; 058 preserves that floor.",
     "A consistent declared joining reserve policy supported by a fabricated process mass account."),
    ("NUMERICAL-GLOBAL", "PROJECTION", "open",
     "The combined factor product is the best feasible multistart result in a bounded scalar model, not a certified global optimum.",
     "Independent search/analytic bounds if a global-minimum claim is needed; all seeds, bounds and witnesses are retained."),
    ("P3-GEOMETRY", "PROJECTION", "open",
     "P3 retains the calibrated constant-g/R f5-019 family. Its no-finite-factor result does not cover alternate topology, g/R or local-shell models.",
     "A new structural solution for tube geometry/topology and local buckling, including section-dependent node/joint and membrane costs."),
    ("P3-COMPRESSION", "QUESTIONABLE", "open",
     "The nominal 3.9 GPa SiC compression value is not a qualified whole-member allowable; about 1.055 GPa is required in the inherited family.",
     "Full tube/member compression and imperfection data for the actual length, wall, ends and temperature."),
    ("PBO-RETENTION", "QUESTIONABLE", "open",
     "5.8 GPa ply strength and ten-year retention transfer material/fibre assumptions to a stressed membrane system; perfect retention is only an upper bound.",
     "Biaxial membrane, seam, creep, humidity and aging data for the actual laminate."),
    ("DRY-CAVITY", "PROJECTION", "open",
     "The SIOX WVTR, 3A net capacity, release kinetics, bed conductance and capture hardware remain unqualified; R20/R30 extend the source beyond R15.",
     "Seven-day pressure/humidity capture experiment over the specified temperature range with full hardware and leakage mass."),
    ("RELIEF-ENVELOPE", "PROJECTION", "open",
     "058's 100 m floor/full-range history differs from 057's reference; a smaller pressure load requires air, altitude or ballast actions.",
     "One coupled pressure/altitude/temperature/air-mass/service trajectory. Repriced hulls here omit nonnegative debits only as upper bounds."),
    ("RELIEF-R12", "PROJECTION", "open",
     "The favorable fixed 058 trim hull raises the R12 optimistic payload upper bound by 58.3 kg but still leaves a 1,036.1 kg deficit before air/bladder costs.",
     "A coherent operational account before this conditional benefit can be credited; it is not an adopted material-closure result."),
    ("TREND-TRANSFER", "PROJECTION", "open",
     "017b historical routes and baselines differ. A film-strength trend cannot overcome the new tube floor, and Be's trend is flat/nonpositive.",
     "A positive, comparable demonstrated trend for the actually binding material/system property before forecasting a finite closing year."),
    ("BE-SUPPLY", "QUESTIONABLE", "open",
     "430 t is estimated 2025 world mined Be content, not rolled-sheet availability; face demand excludes scrap and manufacturing yield.",
     "Current producer capacity, qualified sheet gauge/size and fabrication-yield data for a procurement assessment."),
    ("WEIGHT-COUPLING", "PROJECTION", "open",
     "Mass growth is applied as a buoyancy account; additional local gravity, attachment and dynamic loads from the grown mass are not recomputed.",
     "Coupled structural loads and deformation for the fully grown mass distribution."),
    ("BRIEF-PIN", "QUESTIONABLE", "resolved_by_exact_recovery",
     "PROCESS-v2 changed from its declared 3404-byte version to 5343 bytes after first reading; final packaging detected the drift.",
     "The six originally verified brief/authority files were recovered byte-for-byte from this seat's native tool record and match all declared hashes; see BRIEF-PIN-RECOVERY.json."),
]
nfis = [{"id": "NFI061-" + key, "tag": tag, "status": status, "finding": finding,
         "evidence_needed": need} for key, tag, status, finding, need in nfi_specs]
write("NFI.json", {"schema": "mainline061-nfi-v1", "unit": UNIT, "tag": TAG, "items": nfis,
                   "routing": "Evidence questions travel with this report; no separate queue requests or seat contacts."})

endpoint = [x for x in d["p2"] if x["basis"] == "endpoint"]
handbook = [x for x in d["p2"] if x["basis"] == "handbook"]
trends = read("sources/017b--RESULTS.json")["trends"]
comparison = []
for x in handbook:
    old = next(t for t in trends if t["id"] == "face_specific_stiffness")
    ng = next(t for t in x["without_growth_single"] if t["property"] == "face_density")["factor"]
    new = next(t for t in x["single"] if t["property"] == "face_density")["factor"]
    comparison.append({"R_m": x["R_m"], "weather": x["weather"],
                       "017b_R20_ISA_reference_factor": old["factor"]["R20"] if x["R_m"] == 20 and x["weather"] == "ISA" else None,
                       "061_handbook_no_growth_factor": ng, "061_handbook_concept_factor": new,
                       "growth_only_factor_ratio": new / ng, "tag": "PROJECTION",
                       "years_to_close": None, "reason": "Comparable Be specific-stiffness history has no positive trend."})
ranking = {
    "definition": "Payload gain for factor 1.10, geometry resized; capped variables may receive less than 10% physical improvement.",
    "P2_endpoint": [{"R_m": x["R_m"], "weather": x["weather"],
                     "top_three": sorted(x["marginal_10pct"], key=lambda z: z["gain_kg"] if z["gain_kg"] is not None else -1e30, reverse=True)[:3]}
                    for x in endpoint],
    "P3_named_levers": [{"R_m": x["R_m"], "weather": x["weather"],
                        "top_three": sorted(x["marginal_10pct"], key=lambda z: z["gain_kg"], reverse=True)[:3]}
                       for x in d["p3"]],
    "P3_binding_priority": "Local tube-shell stiffness/section/topology is outside the named strength/film/node levers and dominates their combined upper bound.",
}
compact = {
    "schema": "mainline061-results-v1", "card": "MAINLINE-061", "unit": UNIT, "order": ORDER,
    "status": "analysis complete; independent REVIEW-A pending", "tag": TAG,
    "qualified_hull_SF": None, "calculation_file": "CALCULATIONS.json",
    "payload_definition": "kg; positive means accounting headroom, negative means buoyancy deficit",
    "basis": "Favorable endpoint primary, handbook sensitivity; actual P2 joining primary and retained floor sensitivity.",
    "p2": d["p2"], "p3": d["p3"], "frozen_check057": d["frozen_check057"],
    "source_corrections": d["source_corrections"], "comparison_017b": comparison,
    "historical_projection": {
        "P2": {"years_to_close": None, "rate_per_year": next(t for t in trends if t["id"] == "face_specific_stiffness")["rate"]["per_year"],
               "reason": "No positive comparable Be/face trend; replacement material and joint qualification required."},
        "P3": {"old_film_factor": 3.7912376510354675, "old_projection_years": [13.900868099268974, 25.32054445241723],
               "new_named_lever_years_to_close": None,
               "reason": "No finite film/retention/strength/node factor closes the tube floor within this family; the old forecast route no longer closes."},
        "tag": "PROJECTION, not a calendar prediction",
    },
    "priority": ranking,
    "smallest_required_factor": {"lead": "P2", "R_m": 30, "ISA": 1.059313084130534,
                                 "optimistic": 1.1001179421734688,
                                 "scope": "best feasible product among studied endpoint families and radii; all other factors one",
                                 "not_global_certification": True},
    "beryllium": d["beryllium"], "058_repricing": d["058_repricing"],
    "review": {"independent": "pending REVIEW-A under PROCESS-v2", "self_checks": "VALIDATION.json and REPRODUCTION.json",
               "numerical_fixes_from_dense_scan": d["numerical_fixes"]},
    "nfi": "NFI.json", "inputs": "INPUTS.json", "method": "METHOD.md", "built": now,
}
write("RESULTS.json", compact)

parts = [
    "# MAINLINE-061 — improvement targets with growth carried",
    f"Unit `{UNIT}` · order `{ORDER}`. **QUESTIONABLE inputs; PROJECTION targets.** Analysis complete; independent REVIEW-A pending. No qualified hull safety factor or flight-readiness claim.",
    "The best feasible factor-product search favors **P2 at R30**: divide face density by **1.0593 in ISA** or **1.1001 in optimistic weather**, holding the already favorable endpoint's mechanical and thermal properties. These correspond to **5.60% and 9.10% density reductions**, not to a demonstrated way of making Be lighter. All other factors remain one. P3 has **no finite combination of the named levers within the inherited constant-g/R frame family**: local tube-shell compression leaves too much frame mass even after generous deletion of film, nodes and service hardware.",
    "The primary endpoint already assumes E=293.6 GPa, strength=379.2 MPa, Q=0.82, favorable γ(Vc), and half the baseline bond-film mass. From the handbook basis, the best products at R30 are much larger: **2.1435 ISA and 2.2480 optimistic**, again all assigned to face-density reduction. The favorable endpoint must not be presented as today's qualified hull.",
    "## Payload after the complete mass account",
    "Kilograms; negative values are deficits. Each P2 column reoptimizes its geometry under the stated allowance. P3 includes the seven-day SIOX/3A cavity service. The optimistic label is inherited and does not mean that it is easier than ISA.",
    table(["Lead", "R (m)", "Weather", "No growth", "TRL7 allowance", "Concept allowance"],
          [[lead.upper(), x["R_m"], x["weather"]] + [num(x["deficit"][m]["payload_kg"]) for m in ("none", "TRL7", "concept")]
           for lead, rows in (("p2", endpoint), ("p3", d["p3"])) for x in rows]),
    "NASA Table VI-1 gives **5% hardware at TRL7**, while **6% belongs to batteries**. This corrects 057/CHECK-057's hardware column; the primary concept P2 targets are unchanged. The P3 battery is separately priced at 25% concept/6% TRL7. Other concept rates remain the inherited 15% calculated structure, 30% estimated hardware and 20% thermal scenario. Existing margins are not added twice. [NASA primary paper, PDF p.10](https://ntrs.nasa.gov/api/citations/20120013284/downloads/20120013284.pdf).",
    "R12 reproduces CHECK-057 directly. At R20/R30, adding the later cure-compression term to global demand and resizing absorbed water changes the scalar scenario. The original frozen bills remain visible below; they are not silently overwritten.",
    table(["R (m)", "Weather", "Frozen CHECK-057 no growth", "Frozen TRL7, corrected column", "Frozen concept"],
          [[x["R_m"], x["weather"]] + [num(x["payloads_kg"][m]) for m in ("none", "TRL7", "concept")]
           for x in d["frozen_check057"]]),
    "The R20 optimistic TRL7 sign therefore depends on the large-R mechanics transfer: +14.7 kg on the frozen bill after the NASA correction, versus −29.9 kg with the 061 cure term. Neither is a robust positive margin.",
    "## P2 single-property targets and combination",
    "A factor multiplies strength/modulus/γ/Q/core shear and divides density/film/finish mass. “Not alone” means no closure within the declared model and factor domain, not impossibility for every possible material. Every property trial resizes both face and core thickness.",
    table(["R (m)", "Weather", "Face density ÷", "Face E ×", "γ ×", "Best product", "Face ρ target kg/m³"],
          [[x["R_m"], x["weather"]] +
           [num(next(s for s in x["single"] if s["property"] == p)["factor"], 4) for p in ("face_density", "face_modulus", "gamma")] +
           [num(x["combination"]["factor_product"], 4), num(x["combination"]["solution"]["properties"]["density_kg_m3"], 1)]
           for x in endpoint]),
    "The combined product puts the entire improvement into density at all six endpoints; the other seven factors equal one within numerical precision. This is the best feasible multistart result found, not a global-optimality certificate. The modulus-only alternatives require approximately 532.0 GPa at R20 ISA and 443.7 GPa at R30 ISA, beyond an ordinary Be polycrystal; increasing modulus also raises thermal stresses.",
    table(["Property", "All-six endpoint result", "Next binding constraint / reason"],
          [["Face strength", "Not alone", "Scarf average shear and global buckling; stronger face does not strengthen the scarf"],
           ["Wrinkling Q", "Not alone", "Already at the 0.82 cap; scarf/global modes remain"],
           ["Core shear/density", "Not alone", "G-only change at fixed density raises mismatch shear; scarf/global and thermal interface remain"],
           ["Bond-film mass", "Not alone", "Even near-zero film leaves the face/core deficit"],
           ["Finish mass", "Not alone", "Finish mass is too small; this lever preserves optics"],
           ["E where not closed", "Not alone", "Scarf/crimp/thermal competition; extra nonmonotonic scan finds no missed closure"],
           ["γ where not closed", "Not alone", "γ≤1 plus scarf/core demands; higher γ cannot eliminate face compression mass"]]),
    "Endpoint density-closure geometries and the retained joining-floor sensitivity:",
    table(["R (m)", "Weather", "Each face tf (mm)", "Core tc (mm)", "Density factor with 5% joining floor"],
          [[x["R_m"], x["weather"],
            num(1000*x["combination"]["solution"]["geometry"]["tf_m"], 4),
            num(1000*x["combination"]["solution"]["geometry"]["tc_m"], 3),
            num(x["retained_joining_floor"]["face_density_factor"], 4)] for x in endpoint]),
    "047 does **not** supply a qualified conversion from these resized γ targets to fabrication tolerance. Its conditional R10, 345 MPa face-screen result brackets the SF=1 dimple at 1.209–1.227 mm (about 14.32 µm RMS); adding its 10% endpoint debit narrows that to 0.521–0.539 mm. Its SF=1.05 result is 0.738–0.756 mm without that debit and fails at zero dimple with it. These are references with an uncalibrated core in-plane law, not R12/R20/R30 tolerance specifications. The requested physical precision factor remains **unidentified**, recorded as NFI061-GAMMA-047.",
    "## P3 single-property targets and missing lever",
    "Whole-member SiC compression, PBO ply strength, ten-year retention, film mass and node mass each fail to close alone at every radius/weather. The minimum tube section in the inherited f5-019 family is fixed by local tube-shell compression; raising its 3.9 GPa nominal material strength does not reduce that section. The required whole-member allowable is about 1.055 GPa and still needs qualification. Membrane gauge and capture service are recomputed at each factor; retention is capped at one.",
    table(["R (m)", "Weather", "All named levers at generous limits: payload kg",
           "Delete film/nodes/joints/cavity: upper bound kg", "Also overcredit 058 relief: upper bound kg",
           "Extra tube-mass ÷ factor with other items fixed"],
          [[x["R_m"], x["weather"], num(x["combination"]["infinite_improvements"]["payload_kg"]),
            num(x["combination"]["irreducible_payload_upper_bound_kg"]),
            num(x["combination"]["relief_generous_payload_upper_bound_kg"]),
            num(x["additional_tube_mass_reduction_factor_if_other_items_fixed"], 4)] for x in d["p3"]]),
    "The last column is a missing-lever target, not an achieved design: it requires lighter tubes through a different stiffness/section/topology solution. This card does not equate it with a compressive-strength factor or extrapolate it into a new g/R FE result. The combination has no finite product **within the declared family**; broader frame optimization remains NFI061-P3-GEOMETRY.",
    "## Which three improvements matter most",
    "For equal 1.10 factors at the favorable endpoint, P2 ranks **face density, face modulus, γ** at every size; P3's named levers rank **film mass, ply strength, retention**. The entries below are reoptimized payload gains, kg, for ISA / optimistic. A 1.10 mass factor means a 9.09% mass reduction; retention clips at its physical maximum.",
    table(["R (m)", "P2 density", "P2 E", "P2 γ", "P3 film mass", "P3 ply strength", "P3 retention"],
          [[r] + [
              " / ".join(num(next(z for z in next(x for x in rows if x["R_m"] == r and x["weather"] == w)["marginal_10pct"]
                                   if z["property"] == prop)["gain_kg"], 1) for w in ("ISA", "optimistic"))
              for rows, prop in ((endpoint, "face_density"), (endpoint, "face_modulus"), (endpoint, "gamma"),
                                 (d["p3"], "film_mass"), (d["p3"], "ply_strength"), (d["p3"], "retention"))]
           for r in (12, 20, 30)]),
    "These are marginal rankings, not three independent closing routes. For P3, resolving the local tube-shell mass floor takes priority over any of those three named-property gains. At the handbook P2 basis the marginal ranking changes to density, Q, γ; the favorable endpoint has already spent the Q improvement.",
    "## Operational levers and the earlier trend forecast",
    "058's full-range pressure (103,953 Pa) starts above the 057 ISA design; its relieved pressure is 98,019 Pa. Crediting its full-to-relieved saving again would use incompatible starting hulls. Repricing its actual hulls shows one small possible benefit: the R12 optimistic trim hull gives a **−1,036.1 kg payload upper bound**, 58.3 kg better than the primary concept row, before air/bladder costs. The other compared frozen trim hulls are worse. All remain negative. Low-emissivity finishes can extend the cold edge, but do not provide a mass-budget closure in these repriced rows. Full per-variant records are in RESULTS.json.",
    "017b's R20 ISA face-density factor was **1.7339** in its older no-growth model. The 061 handbook factor without growth is **1.7866**, rising to **2.2113** with concept growth. That same-basis growth-only increase is about **23.8%**; comparing 1.7339 directly with the already favorable endpoint's 1.0766 would confound several changed assumptions.",
    table(["R (m)", "Weather", "061 handbook, no growth density factor", "061 handbook, concept", "Growth-only ratio"],
          [[x["R_m"], x["weather"], num(x["061_handbook_no_growth_factor"], 4),
            num(x["061_handbook_concept_factor"], 4), num(x["growth_only_factor_ratio"], 4)] for x in comparison]),
    "017b's Be specific-stiffness history has a nonpositive fitted rate (about −0.077%/year, reflecting differing published values). It provides **no finite years-to-close forecast** for the replacement face. Its old P3 film-specific-strength factor 3.7912 and 14–25 year projection concerned the older film route (about 2.2–4.1%/year, with an existing material contributing part of the factor). Under this frame and seven-day service account, even an unlimited film improvement leaves the tube deficit. Thus there is **no finite closing year from that named trend** here. All such extrapolations are PROJECTION; no calendar promise follows.",
    "## Be quantity and decision",
    "Pure-Be face demand for the no-growth reference geometry is compared with estimated 2025 world mine production of **430 tonnes of Be content**. The extra column is the 15% face growth budget, not a prediction of actual Be consumption. [USGS Mineral Commodity Summaries 2026, Beryllium](https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-beryllium.pdf).",
    table(["R (m)", "Weather", "Nominal Be faces (t)", "Nominal / world output", "15% face budget (t)", "Budget / world output"],
          [[x["R_m"], x["weather"], num(x["nominal_face_Be_kg"]/1000, 2),
            num(x["nominal_share_percent"], 2)+"%", num(x["concept_face_budget_kg"]/1000, 2),
            num(x["concept_face_budget_share_percent"], 2)+"%"] for x in d["beryllium"]]),
    "R30 requires the smallest improvement factor, while using roughly a quarter of the reported annual world mined Be content for one reference shell's faces. Mine output does not establish sheet availability, and fabrication yield, scrap and spares would add demand. The hypothetical lower-density replacement-face route must not be described as procurable Be.",
    "## Evidence and review status",
    "Direct P2 R10/R12 frozen bills reproduce exactly; the maximum no-growth optimizer difference is below 0.00003 kg. All six R10/R12/R15 seven-day P3 payloads reproduce within 2×10⁻¹⁰ kg. Sixteen closing single-property witnesses and all combined results pass denser geometry checks; the nonmonotonic modulus scan found no missed closure. These are the author's own arithmetic checks. NASA classification and large-R mechanics changes are **not yet independently reviewed**.",
    "Files: [RESULTS.json](RESULTS.json), [INPUTS.json](INPUTS.json), [NFI.json](NFI.json), [METHOD.md](METHOD.md), [REVIEW.md](REVIEW.md), [VALIDATION.json](VALIDATION.json), [REPRODUCTION.json](REPRODUCTION.json), [CALCULATIONS.json](CALCULATIONS.json), and [MANIFEST.json](MANIFEST.json). The dispatch-pinned PROCESS-v2 assigns independent checking to REVIEW-A after 061/062; this card issues no extra review dispatch. That source changed on disk after the original verified read. The six original brief/authority files were recovered from this seat's own tool record and their declared hashes verified exactly; [BRIEF-PIN-RECOVERY.json](BRIEF-PIN-RECOVERY.json) records the drift and recovery.",
]
(ROOT / "CARD.md").write_text("\n\n".join(parts) + "\n")

(ROOT / "REVIEW.md").write_text("""# MAINLINE-061 review status

Independent review: **PENDING REVIEW-A** under the pinned PROCESS-v2. No reviewer seat was contacted, restored or awakened. The author performed the following numerical checks; these do not constitute independent review.

* Reconstructed direct P2 mass bills and the six published seven-day P3 capture rows using own equations and source pins.
* Reoptimized all successful single-factor and combined P2 witnesses with a denser geometry grid; separately scanned nonmonotonic modulus response.
* Repriced actual 058 hulls and proved the declared P3-family impossibility bound still negative after an intentionally generous relief credit.
* Checked the primary NASA table image: corrected TRL7 hardware 6% to 5%, retained 6% for batteries, and separated the concept battery allowance.
* Preserved CHECK-057's frozen large-R account alongside the 061 cure-demand scenario and resized absorbed-water account.

Review-required changes: the NASA column correction, battery class separation, large-R cure term/thermal transfer, and all extrapolated material/cavity/geometry claims. The dense modulus scan reported zero missed intervals in its sampled domain. Numerical convergence is not physical validation or a global-optimality proof.

The complete open-question list is NFI.json; quantitative self-check outcomes are VALIDATION.json and REPRODUCTION.json. No finding is marked independently cleared.
""")
print(f"Built CARD, RESULTS, INPUTS, NFI and REVIEW; {len(used)} local source pins; {len(nfis)} NFI entries.")
