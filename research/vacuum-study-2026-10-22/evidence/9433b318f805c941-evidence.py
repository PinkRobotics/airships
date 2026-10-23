"""Auditable evidence and unresolved qualification requirements."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S = ROOT / "sources"
KSI = 6.894757293168361
sources = {}
for path in sorted(S.glob("*.source.json")):
    meta = json.loads(path.read_text())
    name = path.name.removesuffix(".source.json")
    pdf = S / f"{name}.pdf"
    if pdf.exists():
        data = pdf.read_bytes()
        meta.update(local_pdf=str(pdf), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    sources[name] = meta

rows = [
    dict(id="SR200-catalog", material="Materion SR-200", product="hot-rolled sheet",
         source="sr200", pages_pdf=[1,2,3], directions=["in_plane"],
         gauge_mm=[.508,6.35], target_gauge_in_catalog_range=True,
         Fty_MPa=345, Fcy_MPa=None, Ftu_MPa=483,
         yield_definition="0.2% offset tensile, ASTM E8", basis="listed tensile minimum; datasheet is reference, contract specification required",
         condition="hot rolled, ground, stress relieved, etched", temperature="room temperature",
         state="exists_today", tag="QUESTIONABLE",
         limit="No compressive minimum or biaxial yield reported. Full 24 by 72 inch blank applies only at >=0.059 inch; narrower/shorter below that."),
    dict(id="AMS7902-archived-handbooks", material="AMS 7902 beryllium", product="sheet, not preform",
         source=["mil5j","mmpds01","mmpds08"], pages_pdf=[1185,1185,278],
         locator="Table 7.2.1.0(c); printed 7-5, 7-5, 7-6",
         editions=["MIL-HDBK-5J 31 January 2003","MMPDS-01 31 January 2003","MMPDS-08 1 April 2013"],
         directions=["L","LT"], gauge_mm=[.508,6.35], Fty_MPa=50*KSI,
         Fcy_MPa=None, Ftu_MPa=70*KSI, basis="S (specification minimum) for listed strengths; Fcy entries are ellipses",
         E_GPa=42.5*KSI, Ec_GPa=42.5*KSI, nu_L_LT=.10,
         condition="stress relieved, ground and etched", state="exists_today", tag="QUESTIONABLE",
         limit="Archived tables visually checked. Current approved handbook/specification revision not obtained. An Ec entry is not an Fcy entry."),
    dict(id="SR200-Fenn-L", material="SR-200", product="cross-rolled sheet", source="sr200_lot",
         pages_pdf=[22], locator="Table 3; Fenn et al. 1967 reproduced in NASA-CR-194164",
         directions=["L"], gauge_mm=1.96, Fty_MPa=383.4, Fcy_MPa=379.2, Ftu_MPa=537.6,
         Fcu_MPa=659.1, basis="historical reported values; not a design minimum",
         yield_definition=None, state="in_the_lab", tag="QUESTIONABLE",
         limit="Original AFML-TR-67-212 not inspected; exact offset/statistics/finish not recoverable from reproduced table. No 0.7-0.85 mm transfer."),
    dict(id="SR200-Fenn-LT", material="SR-200", product="cross-rolled sheet", source="sr200_lot",
         pages_pdf=[22], locator="Table 3", directions=["LT"], gauge_mm=1.96,
         Fty_MPa=386.1, Fcy_MPa=382.7, Ftu_MPa=564., Fcu_MPa=591.5,
         basis="historical reported values; not a design minimum", yield_definition=None,
         state="in_the_lab", tag="QUESTIONABLE",
         limit="In-plane value; cannot replace through-thickness properties or the weaker rolling direction."),
    dict(id="SR200E-NASA1992-L", material="SR-200E", product="cross-rolled sheet",
         source="nasa4397", pages_pdf=[25], locator="Table 7, printed 17",
         directions=["L"], study_nominal_gauge_mm=2.54,
         compression_coupon_gauge_individually_documented_in_table=False,
         Fty_MPa=56.8*KSI, Fcy_MPa=50*KSI, Ftu_MPa=75*KSI, Fcu_MPa=95.6*KSI,
         basis="Fcy attributed to unpublished Roschke et al. 1990 data",
         yield_definition="Table labels yield; compression offset not stated. Study's own tensile onset differs from 0.2% offset.",
         condition="study specimens machined and etched; no supplier minimum", state="in_the_lab", tag="QUESTIONABLE",
         limit="Thicker-sheet research evidence; not independent qualification of modern thin SR-200."),
    dict(id="SR200E-NASA1992-LT", material="SR-200E", product="cross-rolled sheet",
         source="nasa4397", pages_pdf=[25], locator="Table 7, printed 17",
         directions=["LT"], study_nominal_gauge_mm=2.54,
         Fty_MPa=60.2*KSI, Fcy_MPa=57.5*KSI, Ftu_MPa=72.1*KSI, Fcu_MPa=100.3*KSI,
         basis="same unpublished compression data provenance as L; not minimum",
         state="in_the_lab", tag="QUESTIONABLE",
         limit="Do not select the stronger LT value for equal compression along both in-plane directions."),
    dict(id="NASA-actual-compression-failure", material="SR-200", product="cross-rolled sheet",
         source="sr200_lot", pages_pdf=[99,100,102,104], locator="Section 5.2, Table 14, printed 86-91",
         directions=["L","LT"], gauge_mm=2.54, specimens=2, Fcy_MPa=None,
         Fcu_MPa=[658.8,691.8], Ec_GPa=[300,306],
         basis="one catastrophic failure in each direction", state="in_the_lab", tag="QUESTIONABLE",
         limit="These are ultimate compressive failures, not yield minima. 12.7 mm unsupported length and special end fixtures."),
    dict(id="S200F-maker-prose", material="S-200-F", product="structural block grade; no thin-sheet coupon identified",
         source="materion-design", pages_pdf=[4], Fty_MPa=255, Fcy_MPa=255, gauge_mm=None,
         basis="about/typical, not a minimum", yield_definition="0.2% offset compression in prose",
         temperature="room temperature", state="exists_today", tag="QUESTIONABLE",
         limit="A sensitivity value, not a conservative certified SR-200 thin-sheet allowable. Generic 10% compression uplift is not a guarantee."),
    dict(id="AMS7908-HIP-A", material="AMS 7908", product="HIP near-net preforms",
         source="mmpds08", pages_pdf=[279], locator="Table 7.2.1.0(d), printed 7-7",
         directions=["all"], Fty_MPa=43*KSI, Fcy_MPa=42*KSI, Ftu_MPa=60*KSI, basis="A column",
         state="exists_today", tag="QUESTIONABLE",
         limit="Wrong product form. Cannot assign 289.58 MPa to cross-rolled sheet; table has anomalous thickness heading/500 in2 entry, not interpreted."),
    dict(id="AMS7908-HIP-B", material="AMS 7908", product="HIP near-net preforms",
         source="mmpds08", pages_pdf=[279], locator="Table 7.2.1.0(d), printed 7-7",
         directions=["all"], Fty_MPa=49*KSI, Fcy_MPa=48*KSI, Ftu_MPa=63*KSI, basis="B column",
         state="exists_today", tag="QUESTIONABLE", limit="Wrong product form; 330.95 MPa is not a sheet design basis."),
    dict(id="PS200-catalog", material="PS-200", product="foil/sheet", source="ps200",
         pages_pdf=[1,2], nominal_target_gauge_mm=.8, exact_inch_gauge_mm=.032*25.4,
         Fty_MPa=None, Fcy_MPa=None, basis="chemistry, gauge and integrity specification only",
         state="exists_today", tag="QUESTIONABLE",
         limit="0.032 inch listed +/-0.002 inch. No tensile/compressive design strength published; >=18 inch width/length by inquiry."),
    dict(id="PF60-catalog", material="PF-60", product="foil/sheet", source="pf60",
         pages_pdf=[1,2,3], nominal_target_gauge_mm=.8, exact_inch_gauge_mm=.032*25.4,
         Fty_MPa=None, Fcy_MPa=None, basis="chemistry, gauge and integrity specification only",
         state="exists_today", tag="QUESTIONABLE",
         limit="A gauge match does not establish mechanical equivalence to SR-200. No compressive yield published."),
    dict(id="DOE-specification-survey", material="SR-200-E", product="hot rolled VHP block into sheet",
         source="doe-specs", pages_pdf=[11], locator="RFP-4283 (1990), current specifications table",
         Fty_MPa=50*KSI, Ftu_MPa=70*KSI, Fcy_MPa=None, gauge_mm=None,
         basis="1974 Brush grade specification reproduced in historical survey",
         state="in_the_lab", tag="QUESTIONABLE",
         limit="Only tensile strength fields; does not independently fill the compressive-yield gap."),
    dict(id="DOE-ingot-thin", material="ingot-sheet beryllium", product="can-rolled then bare-rolled sheet",
         source="doe-ingot", pages_pdf=[29,31,32], locator="RFP-910, mechanical-property tests and Table IX",
         as_rolled_gauge_mm=.025*25.4, tested_gauge_mm=.021*25.4,
         extra_etch_each_side_mm=.002*25.4, Fcy_MPa=None,
         tensile_example={"gauge_mm":.075*25.4,"cross_rolled_Fty_MPa":28000*.006894757293,
                          "cross_rolled_Ftu_MPa":49000*.006894757293},
         basis="tensile tests, not compression", state="in_the_lab", tag="QUESTIONABLE",
         limit="Shows a real finishing/gauge effect, not a thin-sheet compression qualification.")
]
evidence = {
    "schema":1,"card":"MAINLINE-036","unit":"vacuum-mainline036-be-sheet-compression-1020",
    "sources":sources,"rows":rows,
    "design_allowable_for_finished_target_sheet_MPa":None,
    "scope":"No matched minimum or statistically qualified equibiaxial compressive yield was found in the inspected sources. This is not proof that no proprietary data exist.",
    "biaxial":{
        "source":"nasa4397","pages_pdf":[11,13,17,25],
        "test":"Ring-loaded discs with bending; no distinct biaxial yield reported.",
        "fit":"Table 8 uses failure stresses for missing biaxial/off-axis yield observations.",
        "computed_extrapolation_in_RESULTS":"NASA4397_unqualified_polynomial_extrapolation",
        "status":"PROJECTION; not an equibiaxial compression test or an allowable",
        "von_mises_transfer":"For (-s,-s,0), equivalent stress equals s, conditional on isotropic pressure-insensitive plasticity. Cross-rolled orthotropic Be is not thereby qualified."
    },
    "anisotropy":{
        "source":"sr200_lot","page_pdf":22,
        "E_L_LT_ST_GPa":[298.7,293.6,347.5],
        "nu12_nu21":[.0768,.0752],"ST_Ftu_MPa":200,
        "ST_Fcy_MPa":None,"limit":"No substitution of through-thickness ultimate strength for in-plane yield; scalar shell sensitivities do not validate an orthotropic formed shell."
    },
    "finish":{
        "handbook_source":"mmpds08","pages_pdf":[275,276],
        "standard_postmachining_etch_each_surface_mm":.002*25.4,
        "alternate_etch_after_specified_stress_relief_each_surface_mm":.0005*25.4,
        "scope":"The archived handbook's material-property guidance assumes etched surfaces. These are documentation findings, not shop instructions.",
        "no_double_count":"Catalog SR-200 already arrives etched. Additional removal is charged only when later processing requires it.",
        "NASA_sanding_result":"NASA-TM-4397 found tensile ultimate/ductility damage with little tensile-yield change; this is not a compression knockdown law."
    }
}
(ROOT/"EVIDENCE.json").write_text(json.dumps(evidence,indent=2)+"\n")

r=json.loads((ROOT/"RESULTS.json").read_text())
models={x["id"]:x for x in r["models"]}
nfis=[]
def nfi(key,issue,state,needed,today,source,closure):
    nfis.append(dict(id="NFI-036-"+key,status="OPEN",issue=issue,state=state,
        tag="QUESTIONABLE" if state!="PROJECTION" else "PROJECTION",needed=needed,today=today,
        improvement_factor=None,null_factor_reason="No matched qualified baseline; a scalar improvement ratio would be misleading.",
        source=source,closure=closure))
nfi("finished-sheet-Fcy","Obtain a minimum compressive strength for the finished SR-200 face product in both in-plane directions.",
    "exists_today",{"R10_scarf_MPa":300.3333333333333,"R10_lab_weld_MPa":321.580390796927,
                    "R20_as_filed_including_eta09_MPa":376.3819067936061},
    {"tensile_minimum_MPa":345,"matched_compressive_minimum_MPa":None},"sr200; mil5j; mmpds01; mmpds08",
    "Supplier specification plus traceable post-form/post-finish compression data at 0.7-0.85 mm and around 1.4 mm, rolling directions, offset definition and lower-basis statistics.")
nfi("biaxial","Validate transfer from directional uniaxial compression to equal in-plane compression.",
    "PROJECTION",{"stress_state":"(-s,-s,0)","matched_yield_locus":True},None,"nasa4397; sr200_lot",
    "Matched biaxial compression yield/failure data or validated anisotropic constitutive and fracture model; distinguish membrane, bending and local 3-D stresses.")
nfi("historical-transfer","Resolve gauge, lot and finish transfer of the 379.2 MPa historical value.",
    "in_the_lab",{"modern_target_gauges_mm":[.7,.85,1.4]}, {"historical_gauge_mm":1.96,"Fcy_L_MPa":379.2},
    "sr200_lot Table 3","Obtain original AFML-TR-67-212 and qualification data for the purchased thin sheet; historical reported values remain non-minimum evidence.")
nfi("current-handbook","Check current authorized material allowables and purchase specification.",
    "exists_today",{"approved_revision":True},{"reviewed":"MIL-HDBK-5J/MMPDS-01 (2003), MMPDS-08 (2013)","sheet_Fcy":None},
    "mil5j; mmpds01; mmpds08","Controlled current MMPDS/AMS7902 review and supplier-specific compression requirement; no assumption that a blank archived cell proves absence in all later/private data.")
nfi("sheet-elastic-model","Resolve the scalar elastic approximation and legacy nu=0.33.",
    "in_the_lab",{"R20_scalar_sheet_threshold_MPa":models["R20_handbook_elastic"]["threshold"]["Fcy_Pa"]/1e6},
    {"handbook_E_GPa":42.5*KSI,"nu":.10,"historical_nu12_nu21":[.0768,.0752]},"mmpds08; sr200_lot",
    "Use measured post-form orthotropic stiffness, including shear moduli and reciprocity, in validated shell buckling analysis.")
nfi("minimum-gauge","Specify minimum finished gauge rather than an unqualified nominal gauge.",
    "exists_today",{"R10_scarf_finished_mm":.7946240669858892,"R20_027_finished_mm":1.4231326177653178},
    {"R10_catalog_tolerance_mm":.1016,"R20_catalog_tolerance_mm":.1524},"sr200 pp2-3; RESULTS thickness",
    "Thickness map and guaranteed minimum after forming, machining and any new etch; mass accounting includes actual supplied gauge.")
nfi("forming-finish","Determine strength after the actual forming and finishing history.",
    "PROJECTION",{"same_thermal_mechanical_history_as_hull":True},None,"mmpds08; nasa4397; doe-ingot",
    "Matched finished coupons, defect inspection and compressive/rupture tests; do not transfer a tensile sanding result into a compression factor.")
nfi("stock-size","Confirm available blank dimensions at the required thin gauges.",
    "PROJECTION",{"width_m":.6096,"length_m":1.8288},{"catalog_full_envelope_minimum_mm":1.4986},
    "sr200 p3","Supplier-confirmed usable dimensions at final gauge; rerun seams/mass if smaller.")
nfi("other-sheet-grades","Qualify PS-200 or PF-60 mechanically before substitution.",
    "exists_today",{"Fcy_MPa":"route-specific requirement"},{"catalog_nominal_mm":.8,"Fty_MPa":None,"Fcy_MPa":None},
    "ps200; pf60","Actual in-plane compression and biaxial qualification for the candidate grade, finish, gauge and size.")
nfi("gamma-wrinkle","Retain the unresolved buckling and wrinkling assumptions after adding strength.",
    "PROJECTION",{"gamma_model":".2+.4 min(Vc,2) for full endpoint","wrinkle_max":.82},
    {"today_gamma":.2,"today_wrinkle":.33},"028b; 027; RESULTS today_infinite_strength_screens",
    "Representative joined-shell imperfection tests and actual face/core wrinkling/bond characterization. High Fcy alone does not close these modes.")
nfi("scarf","Qualify the assumed scarf compression/shear/peel capacity.",
    "PROJECTION",{"ratio":30,"mean_shear_screen_MPa":10},None,"028b",
    "Exact Be/adhesive/core process testing under equal compression, including peel and local buckling.")
nfi("lab-bond-weld","Qualify the 8 g/m2 bond and weld strength retention.",
    "PROJECTION",{"bond_each_interface_g_m2":8,"assumed_weld_retention":1},
    {"matched_hull_bond_weld_properties":None},"028b",
    "Matched bonded/welded thin-sheet specimens; HAZ, brittle failure, debonding, fatigue and leak integrity.")
nfi("R20-joint","Qualify the inherited R20 0.9 joint efficiency and full-gauge splice model.",
    "PROJECTION",{"eta":.9},None,"027",
    "Compression qualification of actual splice geometry/process with the purchased face grade.")
nfi("environment","Cover mission temperature and cycling in the strength basis.",
    "PROJECTION",{"post_process_and_operating_envelope":True},{"published_strengths":"mostly room-temperature"},
    "sr200; nasa4397; 027/028b","Temperature-dependent yield/fracture and cyclic/thermal durability for the actual face and joint.")
nfi("installed-hull","Establish installed capacity including unmodeled local failures.",
    "PROJECTION",{"installed_SF":">= project requirement"},{"installed_SF":None},
    "027; 028b; this card","Close bond, peel, fracture, local instability, defect, thermal and leak modes and validate the joined geometry; model SF=1 is not certification.")
(ROOT/"NFI.json").write_text(json.dumps(dict(schema=1,card="MAINLINE-036",
    unit="vacuum-mainline036-be-sheet-compression-1020",
    overall_installed_hull_SF=None,rows=nfis),indent=2)+"\n")
log=dict(
    scope="Public primary documents and primary documents hosted in public mirrors; no supplier or other seat contacted.",
    queries=[
        "beryllium cross rolled sheet compressive yield 0.030 thin SR-200",
        "MIL HDBK 5J pdf beryllium 7.2.1",
        "site.materion.com PF-60 PS-200 sheet beryllium data sheet",
        '"beryllium" "compressive yield" "sheet" "0.030"',
        '"beryllium" "compressive yield" "0.032"',
        '"Fenn" "1967" "beryllium" "212"',
        '"beryllium" "biaxial compression" sheet'],
    inspected_primary_sources=list(sources),
    failed_retrievals=[sources["historical-design"]],
    exclusions=[
        "Search snippets and aggregator property ranges were not used as design properties.",
        "Fenn original report not obtained; attributed through NASA reproduction only.",
        "Latest MMPDS controlled data not inspected; no claim about all newer editions.",
        "HIP preforms, block, ingot-sheet tensile tests and tube properties do not qualify thin cross-rolled SR-200.",
        "No matched 0.7-0.85 mm biaxial compression minimum found in the reviewed set."],
    visual_checks=["MIL5J Table7.2.1.0(c)","MMPDS01 Table7.2.1.0(c)",
        "MMPDS08 Tables7.2.1.0(c),(d)","NASA4397 Tables7,8",
        "Materion design guide pp4,8"])
(ROOT/"SEARCH-LOG.json").write_text(json.dumps(log,indent=2)+"\n")
print({"evidence_rows":len(rows),"NFI_rows":len(nfis),"sources":len(sources)})
