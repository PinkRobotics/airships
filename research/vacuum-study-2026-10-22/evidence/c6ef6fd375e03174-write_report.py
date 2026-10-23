"""Assemble provenance and nonblocking dispositions for this combined review."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import csv

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / "vacuum-mainline032-check-1020"

def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + "\n")

def pin(path):
    data = path.read_bytes()
    return dict(path=str(path.resolve()), sha256=hashlib.sha256(data).hexdigest(),
                bytes=len(data))

work = json.loads((ROOT/"WORK.json").read_text())
r = json.loads((ROOT/"RESULTS.json").read_text())
prior_nfi = json.loads((PRIOR/"NFI.json").read_text())

findings = [
    dict(id="NFI-032B-CHECK-CSO-TEMPLATE", status="correction_needed",
         tag="QUESTIONABLE", blocks_progress=False,
         claim="CARD attributes 3 um to the completed CSO surface against its template.",
         evidence="Woody p.684 assigns 3 um to parabolic-template adjustment; the laboratory surface estimate is 10 um.",
         disposition="Relabel the 3 um result and its ratios. Numeric conversion passes; surface attribution does not."),
    dict(id="NFI-032B-CHECK-COUPON-IDENTITY", status="resolved_in_this_check",
         tag="ADDITION", blocks_progress=False,
         claim="The source text pages do not name the face thicknesses.",
         evidence="ER-1001 Fig.22 maps Fig.25 specimen30 to .008-in H19/Crest471/3/16-in core. Fig.30 gives .008-in face/APS/.015-in fillet for specimen32.",
         disposition="The report's figures fill the identity gap. They do not establish Be or CR-III equivalence."),
    dict(id="NFI-032B-CHECK-METRIC", status="open_qualification",
         tag="QUESTIONABLE", blocks_progress=False,
         claim="Numerical depth/RMS/slope-to-delta comparisons can be mistaken for modal comparisons.",
         evidence="Dimple depth is not zero-to-peak Fourier amplitude; RMS requires a spatial model. A sine uses depth/2 or sqrt(2)*RMS.",
         disposition="Keep number-only labels and metrology bandwidth. Single-sine examples are projections, not fitted measurements."),
    dict(id="NFI-032B-CHECK-MISSED-RION", status="omitted_evidence_added",
         tag="QUESTIONABLE", blocks_progress=False,
         claim="032b did not retrieve the Rion thin-face waviness experiment.",
         evidence="Rion 2008 thesis has direct cell-depth measurements near its own calculated wrinkle half-wavelength; detailed values and material scope are in CHECK/RESULTS.",
         disposition="Evidence exists for a different system; no measured Be/CR-III modal amplitude follows. Preserve the empirical shape conversion."),
    dict(id="NFI-032B-CHECK-WAVELENGTH", status="partly_addressed",
         tag="PROJECTION", blocks_progress=False,
         claim="The target wrinkle wavelength was not computed in 032/032b.",
         evidence="Elastic symmetric flat-panel Eq.19 gives full periods 38.5470 and 36.7051 mm at nu=0; alternative nu=.33 is only sensitivity.",
         disposition="A conditional band is now specified. Curvature, biaxiality, material tangent properties, other modes and actual measured spectrum remain unresolved."),
    dict(id="NFI-032B-CHECK-HISTORICAL-EVIDENCE", status="open_qualification",
         tag="QUESTIONABLE", blocks_progress=False,
         claim="The 'exceeded today' field includes a 1969 honeycomb vendor RMS.",
         evidence="Von Hoerner p.2 attributes the .008-in figure to discussions with Rohr; no new honeycomb-cell measurements are supplied there.",
         disposition="Label it historical whole-surface capability evidence; do not infer a current production distribution or wrinkle-band exceedance."),
]
owner_dispositions = [
    dict(id="ams7902-class-table-unread", status="confirmed_open",
         note="G preview has three pages and no 3.5.5. H public listing does not supply class values."),
    dict(id="no-beryllium-face-at-wrinkle-wavelength", status="confirmed_open_for_target_system",
         note="No matching Be/CR-III measurement retrieved. Conditional wavelength projection and different-material Rion data added."),
    dict(id="optical-bench-and-space-mirror-unread", status="not_closed",
         note="A 2022 CFRP mirror abstract lead has global optical RMS; full methods and target-band measurements were not obtained."),
    dict(id="hexcel-telegraph-depth-still-unprinted", status="retained",
         note="Earlier primary-source audit retained; this pass does not manufacture a Hexcel amplitude."),
    dict(id="three-eighths-slope-is-not-a-depth", status="confirmed",
         note="Slope conversions pass as projections. Figure 30 supplies the omitted face thickness."),
    dict(id="transfer-to-the-lead-faces", status="confirmed_open",
         note="Different faces, core and processes. Actual minimum compression/tension/bond strength remains unestablished."),
    dict(id="panel-rms-is-not-delta", status="confirmed",
         note="Historical RMS and bow cannot identify a modal component without spatial information."),
]
dump("NFI.json", dict(
    schema=1, unit=work["unit"], tag="QUESTIONABLE", blocks_progress=False,
    prior_032_findings_retained=prior_nfi["findings"],
    prior_032_original_owner_dispositions=prior_nfi["owner_nfi_dispositions"],
    new_findings=findings, combined_finding_records=16,
    owner_032b_dispositions=owner_dispositions,
    next_job="none",
))

urls = {
    "ER1001": "https://ntrs.nasa.gov/api/citations/19950020773/downloads/19950020773.pdf",
    "Woody": "http://www.cso.caltech.edu/wiki/_media/cso/publications/1994-woody-procieee.pdf",
    "vonHoerner": "https://library.nrao.edu/public/memos/65/65R/65R_030.pdf",
    "Rion": "https://infoscience.epfl.ch/bitstreams/204993d8-6c72-4dca-a688-8293bdab6018/download",
    "Camarda": "https://ntrs.nasa.gov/api/citations/19810003663/downloads/19810003663.pdf",
    "NASA1999": "https://ntrs.nasa.gov/api/citations/19990017863/downloads/19990017863.pdf",
    "AMSG": "https://img.antpedia.com/standard/files/pdfs_ora/20230614/SAE/AMS/SAE%20AMS%207902G-2018.pdf",
    "AMSG_official": "https://saemobilus.sae.org/standards/ams7902g-beryllium-sheet-plate-98be",
    "mirror2022": "https://www.sciencedirect.com/science/article/abs/pii/S0254058422003340",
}
audits = [
    dict(id="032-incorporated", status="immutable_prior_check_pins_verified",
         evidence=pin(PRIOR/"SOURCE-AUDIT.json"),
         finding="Prior fourteen-source audit incorporated; no changed source artifacts."),
    dict(id="ER1001-depth", url=urls["ER1001"], local="sources/er1001.pdf",
         locator="printed p.19 (PDF26), Fig.25 (PDF88)",
         status="verified_source_number_with_metric_qualification",
         finding=".000065 in = .001651 mm. Figure shows a local dimple depth, not a Fourier coefficient."),
    dict(id="ER1001-identities", url=urls["ER1001"], local="sources/er1001.pdf",
         locator="Fig.22 (PDF85), Fig.25 (PDF88), Fig.30 (PDF93)",
         status="additional_source_reading",
         finding="Both relevant coupons have .008-in faces; specimen30 H19/Crest471/3/16-in core, specimen32 APS/.015-in fillet/3/8-in core."),
    dict(id="ER1001-slopes", url=urls["ER1001"], local="sources/er1001.pdf",
         locator="printed p.20 (PDF27), Fig.30 (PDF93)",
         status="verified_projection_inputs",
         finding=".5-1.6 mrad range reproduced. No paired depth published for this range."),
    dict(id="Woody", url=urls["Woody"], local="sources/woody1994.pdf",
         locator="printed pp.675,680,684 (PDF3,8,12)",
         status="numeric_values_verified_one_attribution_correction",
         finding="3 um refers to template adjustment. Metrology and RMS are multi-scale; they do not extract a cell or target wrinkle component."),
    dict(id="vonHoerner", url=urls["vonHoerner"], local="sources/vonhoerner1969.pdf",
         locator="printed p.2 / PDF2, Table1",
         status="verified_historical_vendor_figure",
         finding=".008 in converts to .2032 mm; source prints .20 mm RMS. Rohr discussion, not a measured wrinkle spectrum."),
    dict(id="Rion", url=urls["Rion"], local="sources/rion2008_thesis.pdf",
         locator="Table3-3 p.75/PDF77; pp.166-171/PDF168-173; p.177/PDF179; p.181/PDF183",
         status="omitted_primary_experiment_added",
         finding="Measured thin-face cell-depth data near that system's own critical half-wavelength. Shape conversion and material-system limitations are retained.",
         numerical_reading="RESULTS.omitted_primary_experiment; graph means approximate, fitted values explicitly not raw data"),
    dict(id="Camarda", url=urls["Camarda"], local="sources/camarda1980.pdf",
         locator="p.23/PDF34; AppendixA.3 pp.42-43/PDF53-54; Fig.46 p.129/PDF140",
         status="omitted_profile_measurements_added_not_modal_data",
         finding="Mean of maximum waviness .0097 cm and 45-point face profiles; no measured critical-band Fourier amplitude."),
    dict(id="NASA1999-wavelength", url=urls["NASA1999"],
         local="sources/nasa_wrinkling1999.pdf",
         locator="Eq.19 p.24/PDF34; pp.31-32/PDF41-42",
         status="conditional_model_projection",
         finding="Eq.19 is explicitly a half-wavelength. Multiplying by two gives the periods compared with Woody's scale band."),
    dict(id="FPL1810A", url="https://ir.library.oregonstate.edu/downloads/2f75rc704",
         local=str(PRIOR/"sources/fpl1810a.pdf"),
         status="reused_verified_primary",
         finding="Earlier FPL fitted imperfection parameters are not relabeled as new direct measurements."),
    dict(id="AMS7902G", url=urls["AMSG"], official_listing=urls["AMSG_official"],
         local="sources/ams7902g-preview.pdf", locator="sections1.1.1,1.3,3.2.1; three-page excerpt",
         status="primary_document_on_third_party_mirror",
         finding="Three classes and sheet interval confirmed; class table absent. Roughness wording transcribed literally, not converted into flatness."),
    dict(id="mirror2022", url=urls["mirror2022"], doi="10.1016/j.matchemphys.2022.126028",
         status="indexed_primary_abstract_only_full_methods_not_retrieved",
         finding="Optical mirror RMS lead; no verified target Be/CR-III wrinkle-band measurement. Not used to calculate any limit."),
]
dump("SOURCE-AUDIT.json", dict(schema=1, audits=audits,
     retrieval_limits="NASA/Caltech web-reader failures were resolved by direct public HTTP retrieval where successful. Caltech HTTPS hostname validation failed; the cited public HTTP URL succeeded without disabling TLS.",
     search_scope="Assigned reports; primary NASA references to surface waviness; process-pressure/thin-face experiment; precision-mirror abstract lead. Not an exhaustive nonexistence claim."))

manifest = json.loads((ROOT/"sources/manifest.json").read_text())
for row in manifest:
    # A CDN response's expiring signed query is unnecessary to reproduce the public request.
    if "final_url" in row and "Signature=" in row["final_url"]:
        row["final_url"] = row["final_url"].split("?")[0]
        row["redirect_note"] = "Public repository redirected to an expiring CDN download; cite original repository URL."
(ROOT/"sources/manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
source_pins = [pin(p) for p in sorted((ROOT/"sources").iterdir())
               if p.suffix in [".pdf", ".png", ".txt"]]
source_pins += [pin(PRIOR/"sources/fpl1810a.pdf")]
dump("SOURCE-PINS.json", dict(schema=1, files=source_pins))
snapshots = [pin(p) for p in sorted((ROOT/"inputs").iterdir())]
dump("INPUTS.json", dict(
    schema=1, unit=work["unit"], order=work["order"],
    owner_reports=["rpt-mainline032-grok-wrinkle-waviness-1020",
                   "rpt-mainline032b-grok-measured-flatness-1020"],
    incorporated_report="rpt-ref-a30a669ed3e245f1473b",
    snapshots=snapshots, source_manifest=pin(ROOT/"sources/manifest.json"),
    source_pins=pin(ROOT/"SOURCE-PINS.json"),
    prior_report_pins="inputs/pin-audit.json",
    original_032_owner_pins="inputs/pin-audit-original032.json",
    search_log=pin(ROOT/"SEARCH-LOG.json"),
    constants=dict(mm_per_inch=25.4, Pa_per_psi=6894.757293168361,
                   Ef_Pa=290e9, Ec_psi=15000, cell_inch=.375,
                   core_strength_scenarios_psi=[60,35]),
    geometry_source="Same rounded brief inputs independently checked in the immutable 032 check",
    method="Explicit source quantities and analytic formulas in check.py; exhaustive scalar-path coverage; source interpretation assessed separately",
    tolerance=dict(relative=3e-12, absolute=1e-12),
    prohibitions_observed=["No owner code read or run", "No foreign-seat writes",
                           "No out-of-band messages, restores, wakeups, or waiter"],
    absence_claim="No matching target-system measurement found in the documented bounded search",
))

with (ROOT/"MEASUREMENT-MAP.csv").open("w") as f:
    writer=csv.DictWriter(f,fieldnames=["label","value_mm","quantity","ratios_as_numbers_only"])
    writer.writeheader()
    writer.writerows(r["number_only_comparisons"])
card = """# MAINLINE-032 + 032b: independent check

QUESTIONABLE. All 533 retained/new comparisons pass: 236 from the immutable 032 check and 297 new 032b scalar checks. Source meaning is assessed separately.

Conditional lead δ limits, mm: S-200F 0.152868766846 at 60 psi and 0.089173447327 at 35 psi; SR-200 0.065222906404 and 0.038046695402. Actual Fc remains the minimum compression/tension/bond strength, not an established 60 or 35 psi.

Correct 032's lead-only δ/cell interval to 0.00684754923–0.01604921437. Correct 032b's 3 μm CSO attribution to parabolic-template adjustment. NASA's figures identify both relevant coupons as 0.008-inch faces.

Keep dimple depth, slope, RMS and modal amplitude separate. Historical whole-panel RMS cannot establish current target-band exceedance. The conditional flat-panel model gives full wrinkle periods about 37–40 mm, with unresolved shell transfer.

An omitted thin-face experiment exists near its own critical wavelength: Rion's carbon/epoxy–Nomex study. Its measured cell heights require a fitted shape conversion in its model. No retrieved source measures the proposed Be/CR-III wrinkle component.

CHECK.md supplies source links and precise scope. RESULTS.json and NUMERIC-CHECK.csv supply independent calculations; NFI.json retains ten earlier findings and adds six nonblocking records. No successor job.
"""
(ROOT/"CARD.md").write_text(card)
now=datetime.now().astimezone()
work["ended_at"]=now.isoformat(timespec="seconds")
work["elapsed_instrumented_review_s"]=(now-datetime.fromisoformat(work["started_at"])).total_seconds()
work["timing_scope"]="Own recorded review interval begins after initial order/report intake. Owner script timers are not review duration."
dump("WORK.json",work)
r["review_timing"]=work
dump("RESULTS.json",r)
print(json.dumps(dict(audits=len(audits),prior_findings=10,new_findings=len(findings),
                     source_files_pinned=len(source_pins),ended_at=work["ended_at"],
                     elapsed_s=work["elapsed_instrumented_review_s"]),indent=2))
