"""Assemble the one-round review, preserving numerical/physical distinctions."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from source_a1 import ROOT, read

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

field=local("FIELD-CHECK.json")
linear=local("LINEAR-CHECK.json")
accounts=local("ACCOUNT-CHECK.json")
fixes=local("FIXES.json")
owner=read("062--RESULTS.json")
claims=local("CLAIMS.json")

evidence={
 "A1-01":("reproduces","EUCASS2023-367 §§3.1–3.2.1: experiments validate axial compression; 6.03 MPa is a pressure-postbuckling prediction.",
          ["sources/primary--eucass2023-367.pdf"]),
 "A1-02":("reproduces","Independent force equilibrium at the saved refined state gives 6.159020624266 MPa; original 6.159020624174. Independent raw-path maxima give 6.159020624–6.502271779 MPa. Scope: frozen-state equilibrium and sampled maxima, not a rerun of contact/plastic history or proof of physical instability.",
          ["FIELD-CHECK.json","check_field_a1.py"]),
 "A1-03":("reproduces","Independent ratios: +2.139645510%, mesh −0.115571622%, penalty −0.010452458%. These reproduce the printed rounding; they are observed numerical changes, not certified error bounds.",
          ["ACCOUNT-CHECK.json","FIELD-CHECK.json"]),
 "A1-04":("reproduces","Fresh Q8 elastic/prestress eigenproblems give 30.218153613699 MPa outer-radius and 28.074312431918 MPa midsurface-radius: +9.764451920% and +1.977161031% relative to 27.53 MPa.",
          ["LINEAR-CHECK.json","check_linear_a1.py"]),
 "A1-05":("reproduces","Withholding P2 gamma is supported: the benchmark is steel/PVC with unresolved calibration; Hexcel supplies distinct directional anchors, not a matched installed CR III crush/unload/mixed-load law.",
          ["sources/primary--eucass2023-367.pdf","sources/primary--criii.pdf","ADMISSIBILITY.md"]),
 "A1-06":("reproduces","The source record supports withholding physical tolerance release: 345 MPa is a tensile proxy; the in-plane core law, processed compression/bond and manufactured residual state remain unqualified.",
          ["sources/047--INPUTS.json","sources/primary--sr200.pdf","sources/primary--af163.pdf","ADMISSIBILITY.md"]),
 "A1-07":("reproduces","Materion SR-200 p.1 lists representative scalar E=290 GPa. Its mechanical minimums are tensile; the source does not identify a finished, formed, biaxial compressive allowable.",
          ["sources/primary--sr200.pdf"]),
 "A1-08":("reproduces","3M p.1 lists unsupported AF 163-2U at 0.015 lb/ft². Its p.15 200°F table concerns 2K 0.060 lb/ft², so product identity does not qualify the proposed Be/CR III process.",
          ["sources/primary--af163.pdf"]),
 "A1-09":("reproduces","Eliminating C between source and target equations gives 0.792569717998 mm at R10, SF1.05, with the declared cure debit.",
          ["ACCOUNT-CHECK.json","check_accounts_a1.py"]),
 "A1-10":("reproduces","The independent ratio gives 1.628412576678 mm at R20 under the same declared hypothesis.",
          ["ACCOUNT-CHECK.json","check_accounts_a1.py"]),
 "A1-11":("reproduces","The independent ratio gives 2.485983493740 mm at R30 under the same declared hypothesis.",
          ["ACCOUNT-CHECK.json","check_accounts_a1.py"]),
 "A1-12":("reproduces","Under homothety, R/tf and tc/tf are constant, so membrane stress, scaled residual debit and C are constant; d and allowed amplitude scale with R. This is a dimensional consequence of the hypothesis, not validation of C transfer.",
          ["ACCOUNT-CHECK.json","METHOD.md"]),
 "A1-13":("reproduces","Independent stock/labor/material arithmetic and supplied facility allowances reproduce $66,519,656.56–477,421,594.60. Rates are unquoted assumptions.",
          ["ACCOUNT-CHECK.json","sources/062--ASSUMPTIONS.json"]),
 "A1-14":("reproduces","The same conditional account reproduces $522,773,952.34–3,813,773,030.71.",
          ["ACCOUNT-CHECK.json","sources/062--ASSUMPTIONS.json"]),
 "A1-15":("reproduces","The same conditional account reproduces $1,834,656,370.48–13,448,336,376.35.",
          ["ACCOUNT-CHECK.json","sources/062--ASSUMPTIONS.json"]),
 "A1-16":("differs","All six negative signs reproduce, but inherited coating growth overcharges the stated 20% total allowance. Payload rises 0.095193/0.380771/0.856735 kg at R10/20/30 after removing the embedded-margin denominator error. Six unreviewed field corrections are listed in FIXES.json.",
          ["FIXES.json","ACCOUNT-CHECK.json"]),
 "A1-17":("reproduces","Seven records preserve the missing local-defect metrics. Spot checks confirm ALMA's adjusted/masked 16–17 µm RMS and S-II's 0.010 inch core-to-face gap; neither establishes this hull's maximum local defect.",
          ["sources/062--PRECEDENTS.json","sources/primary--alma-prototypes.pdf","sources/primary--sii-lessons.pdf"]),
}
for c in claims:
    status,detail,paths=evidence[c["id"]]
    c.update(disposition=status,reviewer_finding=detail,evidence=paths,tag=TAG,
             physical_qualification="open; no new hull/material qualification")
write("CLAIMS.json",claims)

nfi_specs=[
 ("056-PRESSURE-VALIDATION","QUESTIONABLE",
  "The pressure target is a simulation and the field check conditions on saved plastic strain and imported geometry. It does not independently reproduce the full plastic/contact history, a three-dimensional stability loss or a measured pressure failure.",
  "A declared constitutive/history/import deck and independent continuation/stability check, followed by a relevant pressure-shell experiment.",
  ["A1-01","A1-02"]),
 ("056-MATERIAL","QUESTIONABLE",
  "Foam hydrostatic/flow calibration and the steel-axis interpretation are unresolved. At the refined peak, 1543 core points exceed the retained hardening knots; minimum J≈0.398. Agreement at one pressure does not establish those properties.",
  "Matched foam multiaxial, unloading and densification data; confirmed steel curve units and compressive response.",
  ["A1-02","A1-05"]),
 ("CORE-TRANSFER","QUESTIONABLE",
  "CR III catalog direction/thickness/strength anchors do not identify its installed finite-strain tensor, postpeak crushing, unloading, shear failure or mixed loading.",
  "Matched directional core and bonded assembly tests at the proposed thickness, ribbon layout and temperature.",
  ["A1-05","A1-06"]),
 ("BE-PROCESS","QUESTIONABLE",
  "SR-200's scalar modulus and tensile minimums do not establish a processed, minimum-gauge biaxial compressive allowable.",
  "Purchased/forming/cure lot data and thin-sheet compression/fracture qualification for the actual gauges.",
  ["A1-06","A1-07"]),
 ("BOND-PROCESS","QUESTIONABLE",
  "Light 2U identity is established, but exact Be/CR III preparation, cure, residual stress and seam behavior are not.",
  "Exact-process bond and scarf strength/fracture/aging measurements and a released residual-state measurement.",
  ["A1-06","A1-08"]),
 ("TOLERANCE-TRANSFER","PROJECTION",
  "The amplitudes use a calibrated Gaussian family at reference pressure 95.4608379 kPa and a tensile proxy. Holding C across changed thickness/shear ratios and carrying a scalar cure debit do not model a complete thermal/weather/seam field.",
  "Measured defect spectra and residual fields, a specified combined load case, and independent prediction of a manufactured curved article before release as shop acceptance.",
  ["A1-09","A1-10","A1-11","A1-12"]),
 ("PRECEDENT-METRIC","QUESTIONABLE",
  "Supported reflector RMS, masked maps, optical segment figure and core-to-face fit do not bound a free pressure shell's local inward defect. ALMA captions mask faulty areas for both prototypes.",
  "Full signed contour data with local amplitude/span, support condition and acceptance masks for a comparable manufactured shell.",
  ["A1-17"]),
 ("STOCK-YIELD","PROJECTION",
  "The R10 thin-sheet class does not establish the inherited 24×72 inch blank layout; forming yield, usable gauge, core fit and purchased Be capacity remain unknown.",
  "Usable blank/gauge quotes, actual nesting and process-yield measurements; reprice seams and flight mass if they change.",
  ["A1-07","A1-13","A1-14","A1-15"]),
 ("COST-VALIDITY","PROJECTION",
  "The cost ranges reproduce only the stated planning assumptions. They are not quotes, measured confidence intervals or complete qualified-flight program totals.",
  "Supplier quotations, measured labor/yield, required article count and full-scale qualification/facility/program scope.",
  ["A1-13","A1-14","A1-15"]),
 ("FACILITY-SCALING","PROJECTION",
  "ASSUMPTIONS.json names R10 hall and handling rates without explicit radius exponents. Delivered cost lines imply R^2.5 and R^2. The review retains these lines as supplied allowances, not independently sourced predictions.",
  "Document those assumed scaling laws and obtain facility/handling scope and prices.",
  ["A1-14","A1-15"]),
 ("PASSIVE-SHAPE","PROJECTION",
  "The retained 0.020 kg/m² hardware/filler allowance and passive shape retention after support removal are not demonstrated. Additional structure, repair or growth-driven local loads would need a new bill.",
  "A released joined/closed process article demonstrating retained contour, mass and thermal/pressure response.",
  ["A1-06","A1-16"]),
]
nfis=[{"id":"NFI-A1-"+key,"tag":tag,"status":"open","finding":finding,
       "evidence_needed":need,"claims":ids}
      for key,tag,finding,need,ids in nfi_specs]
write("NFI.json",{"unit":UNIT,"tag":TAG,"items":nfis,
                  "scope":"Unresolved source/physical questions, not demonstrated arithmetic mismatches."})

sources=local("SOURCE-INDEX.json")
inputs={"schema":"review-a1-inputs-v1","unit":UNIT,"order":ORDER,"tag":TAG,
        "reviewed_reports":[sources[c]["report"] for c in ("056","062")],
        "dispatch_brief_pins":local("BRIEF-PINS.json"),
        "filed_artifact_pins":sources,
        "specifically_used_evidence":local("EVIDENCE-PINS.json"),
        "source_observations":[
          {"claim":"6.03 MPa provenance","url":"https://www.eucass.eu/doi/EUCASS2023-367.pdf",
           "locator":"PDF pp.6–7, §§3.1–3.2.1","access":"Browser open unavailable; pinned primary PDF independently read."},
          {"claim":"SR-200 scalar modulus/product limits","url":"https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6",
           "locator":"PDF pp.1–3","access":"Browser open unavailable; pinned primary PDF independently read."},
          {"claim":"2U identity and 200°F table","url":"https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf",
           "locator":"PDF pp.1,15","access":"Browser and pinned primary PDF."},
          {"claim":"Directional core anchors","url":"https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf",
           "locator":"Table II, PDF p.5","access":"Browser and pinned primary PDF."},
          {"claim":"ALMA accuracy metric","url":"https://arxiv.org/pdf/astro-ph/0609329",
           "locator":"PDF pp.8,12–14; Table 2 and Figs.4,6 captions","access":"Pinned primary PDF spot check."},
          {"claim":"S-II core-to-face fit","url":"https://ntrs.nasa.gov/api/citations/19720008130/downloads/19720008130.pdf",
           "locator":"PDF p.296, printed 4-45","access":"Pinned primary PDF spot check."}],
        "independence":{"owner_code_read":False,"owner_code_executed":False,
                        "owner_saved_states_used":True,"owner_result_tables_used_as_comparison":True,
                        "new_code":"Own virtual-work, linear eigenproblem and arithmetic scripts."}}
write("INPUTS.json",inputs)
results={"schema":"review-a1-results-v1","unit":UNIT,"order":ORDER,"tag":TAG,
         "status":"review complete; fixes explicitly unreviewed; physical qualification open",
         "claims":claims,"counts":{"claims":len(claims),"reproduces":sum(c["disposition"]=="reproduces" for c in claims),
                                   "differs":sum(c["disposition"]=="differs" for c in claims),
                                   "cannot_be_checked_without_a_source_or_test":0,
                                   "fix_rows":len(fixes["items"]),"nfi_rows":len(nfis)},
         "field_check":"FIELD-CHECK.json","linear_check":"LINEAR-CHECK.json",
         "account_check":"ACCOUNT-CHECK.json","fixes":"FIXES.json","nfi":"NFI.json",
         "decisions_changed":"None: 6.03 remains numerical; no P2 gamma or physical tolerance is released; all six concept-growth payloads remain negative.",
         "review_scope_limits":["Frozen-state pressure reconstruction is not a rerun of the entire plastic/contact path.",
                                "Cost reproduction is conditional on unquoted rates and supplied facility allowances.",
                                "No owner artifacts were changed; correction rows have not received another review."],
         "measured_times":local("EXECUTION.json"),
         "usage_measurements":{"attributed_tokens":None,"codex_points_before":None,"codex_points_after":None,
                               "reason":"No trustworthy task-specific token or points meter is exposed; values are not inferred from transcript length."}}
write("RESULTS.json",results)

claim_rows=[]
for c in claims:
    claim_rows.append([c["id"]+" / "+c["card"],c["disposition"],c["reviewer_finding"]])
sections=[
 "# REVIEW-A1 — MAINLINE-056 and MAINLINE-062",
 "**Sixteen of seventeen load-bearing claims reproduce in their stated conditional scope. One differs in its mass-account values: six inherited coating-growth corrections raise payload by 0.095–0.857 kg. All six cases remain negative.** Corrections are **unreviewed**, as required by the one-round process. No pressure-hull, material, fabrication tolerance or cost qualification is released.",
 f"Unit `{UNIT}` · order `{ORDER}`. **QUESTIONABLE / PROJECTION throughout.** The reviewer wrote 061, not 056 or 062. No owners' code was read or run. The 17 claims and their decision relevance were written first in [LOAD-BEARING.md](LOAD-BEARING.md). This half reviews only 056/062; the other half owns 058/061.",
 "## Claim dispositions",
 "“Reproduces” below means the specified source statement, conditional arithmetic or numerical output reproduces. It does not close the physical questions listed in NFI.json. Each claim has exactly one numerical/source disposition.",
 table(["Claim / card","Disposition","Independent result and scope"],claim_rows),
 "## 056: what the independent computation establishes",
 "The original paper describes axial-compression validation separately from its pressure calculations; 6.03 MPa belongs to the latter. It therefore supplies no measured pressure-collapse target for this comparison. [EUCASS2023-367, §§3.1–3.2.1](https://www.eucass.eu/doi/EUCASS2023-367.pdf).",
 "The review derived Q8 interpolation from an eight-term nodal polynomial basis, reconstructed deformation gradients and logarithmic elastic strains from the pinned mesh/displacement/plastic-state arrays, and integrated internal and current-surface pressure forces. The pressure obtained from free-node equilibrium was **6.159020624266 MPa**, only **9.16×10⁻¹¹ MPa** above the saved value. Relative free-force residual was **1.17×10⁻⁸**. No saved pressure entered that reconstruction. The standard [rr, zz, hoop, engineering-rz] plastic-strain layout with xi-outer Gauss ordering uniquely satisfies the checked equilibrium conventions; alternatives have residual ratios above 21.",
 "This independently checks the decisive **frozen equilibrium state**. The pressure-path samples separately confirm its maximum and following lower samples. It does not independently recreate the full indentation/plastic history or establish the first three-dimensional pressure-control instability. The check also recovers minimum J=0.398052588 and 1543 core points beyond the retained hardening knots. The documented source extrapolation and flow/history questions remain open.",
 "A second, fresh calculation built the perfect hemisphere and assembled elastic and unit-prestress geometric stiffness at 384 meridional elements, eight core layers and two layers per face. It reproduced both dead-pressure eigenvalues to within 10⁻⁹ MPa; eigen residuals are below 9×10⁻¹¹. The radius-reading gaps and the pressure/refinement percentages are therefore reproduced numerical quantities. Their closeness to the paper does not turn the unqualified steel/PVC model into Be/honeycomb capacity.",
 "## 062: source and scaling checks",
 "The source checks support the card's admissibility distinctions: SR-200 has a representative scalar modulus of 290 GPa, while its listed minimum mechanical strengths are tensile. Thin-stock availability also limits the assumed blank layout. [Materion SR-200, pp.1–3](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6). Light AF 163-2U exists; its identity does not transfer the guide's 2K 200°F aluminum-joint results to this proposed process. [3M guide, pp.1 and 15](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf). Directional coupon anchors remain distinct from a complete installed nonlinear core law. [Hexcel Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).",
 "The shape calculation eliminates the fitted coefficient between the reference and target equations. With `d=tf+tc`, `σm=SF pR/(4tf)`, it gives `aR=a0(dR/d0)[(Fy−σres,R)/σm,R−1]/[Fy/σm,0−1]`. Using the explicitly rounded CHECK047 reference and the 057 bill-derived gauges gives the three printed SF1.05 values. Under homothety, the dimensionless stress ratios stay fixed and d scales with R, so amplitude scales with R. Holding that coefficient across nonhomothetic gauges, defects and weather remains a PROJECTION.",
 table(["R (m)","Independent cure-debited SF1.05 amplitude (mm)","Printed (mm)"],
       [[x["R_m"],f'{next(z["amplitude_mm"] for z in x["tolerances"] if z["SF"]==1.05 and z["with_cure"]):.12f}',
         {10:"0.793",20:"1.628",30:"2.486"}[x["R_m"]]] for x in accounts["shape"]]),
 "The precedent check supports the metric distinction, not manufacturing acceptance. ALMA's 16–17 µm figures are adjusted reflector RMS, with faulty areas masked in the prototype maps. [ALMA prototype paper, Table 2 and Figs.4/6](https://arxiv.org/pdf/astro-ph/0609329). S-II's 0.010 inch figure is a permitted core-to-face bond gap, equivalent to 0.254 mm. It is not a maximum external dent. [S-II manufacturing record, printed p.4-45](https://ntrs.nasa.gov/api/citations/19720008130/downloads/19720008130.pdf). No RMS-to-maximum-defect conversion is supported.",
 "## Costs and the demonstrated mass correction",
 "Rebuilding the full rectangular stock takeoff, panel count, seams, material and labor charges reproduces the six cost totals exactly at stored precision. The hall and handling lines are retained as supplied allowances: their larger-radius values imply R^2.5 and R^2 scaling, which ASSUMPTIONS.json does not spell out. That documentation/price-evidence gap is NFI-A1-FACILITY-SCALING, not a demonstrated wrong total.",
 table(["R (m)","Low first-shell account (USD)","High first-shell account (USD)"],
       [[r]+[f'{next(x["independent_total_USD"] for x in accounts["cost"] if x["R_m"]==r and x["scenario"]==s):,.2f}'
              for s in ("low","high")] for r in (10,20,30)]),
 "The price intervals remain unquoted planning cases with incomplete qualified-flight program scope. This review establishes arithmetic, not affordability, availability, a cheapest feasible route or supplier performance.",
 "The inherited coating mass `m` already equals 1.10 times its unmarginated mass. To reach a 20% total allowance, the increment is `m(1.20/1.10−1)=m×0.10/1.10`. The carried 057 formula instead adds `m×0.10`, resulting in 21% total. The table below gives the six field corrections; owner files remain unchanged. These are one demonstrated inherited cause, six unreviewed correction rows.",
 table(["R (m)","Weather","Card payload (kg)","Corrected payload (kg)","Increase (kg)"],
       [[x["R_m"],x["weather"],f'{x["owner_payload_kg"]:.6f}',
         f'{x["corrected_embedded_margin_payload_kg"]:.6f}',f'{x["corrected_minus_owner_kg"]:.6f}']
        for x in accounts["mass"]]),
 "No float/no-float decision changes. 062's deliberate retention of the original 057 account explains the inheritance; it does not remove the denominator correction required by the stated 20% total coating allowance. The hypothetical flat-5% maturity sensitivity is not substituted for the concept-growth rows.",
 "## Handoff",
 "The review is complete in one round. Numerical status and physical qualification are separate in [RESULTS.json](RESULTS.json). [FIXES.json](FIXES.json) supplies six **unreviewed** field corrections; [NFI.json](NFI.json) supplies eleven source/qualification questions. Nothing here authorizes another run, review dispatch or physical release.",
 "Reproducible evidence: [INPUTS.json](INPUTS.json), [METHOD.md](METHOD.md), [FIELD-CHECK.json](FIELD-CHECK.json), [LINEAR-CHECK.json](LINEAR-CHECK.json), [ACCOUNT-CHECK.json](ACCOUNT-CHECK.json), [VALIDATION.json](VALIDATION.json), and [MANIFEST.json](MANIFEST.json). Simjob receipts record one-core jobs and released reservations; elapsed times are measurements, not budgets.",
]
(ROOT/"REVIEW.md").write_text("\n\n".join(sections)+"\n")
(ROOT/"CARD.md").write_text("# REVIEW-A1 complete\n\nSixteen claims reproduce; one mass-account claim has six small unreviewed coating corrections. All six concept-growth payloads remain negative. Physical qualification stays open.\n\nThe full single-round review is [REVIEW.md](REVIEW.md); machine-readable dispositions are [RESULTS.json](RESULTS.json), with [FIXES.json](FIXES.json) and [NFI.json](NFI.json).\n")
print("Built review:",results["counts"])
