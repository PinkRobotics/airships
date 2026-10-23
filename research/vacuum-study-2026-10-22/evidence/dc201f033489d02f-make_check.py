#!/usr/bin/env python3
"""Package the independent check and its evidence. Does not submit to the queue."""
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

a = load("CALCULATIONS.json")
s = load("SUPPLEMENTAL.json")
o = load("snapshots/RESULTS.json")
meta = load("CHECK-META.json")
ended = datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
fp = a["declared_point"]
refined = s["exact_continuous_least_set"]
rp = refined["point"]
summary = s["comparison_summary"]
assert summary["n"] == 218 and summary["passed"] == 216
assert {x["field"] for x in summary["failed"]} == {
    "floating_point.tolerance_015_at_needed_gamma.rms_worst_mm",
    "floating_point.tolerance_015_at_018_curve.rms_worst_mm",
}
assert all(x["matches_pin"] for x in load("PIN-AUDIT.json"))
assert all(x["match"] for x in load("UPSTREAM-PINS.json") + load("PINS-015.json"))
assert all(x["best"]["least_SF"] < 1 for x in a["full_bounds_32"] if x["mask"].bit_count() <= 2)

nfi = [
    dict(id="NFI-021B-CHECK-COMPRESSION", status="open", tag="QUESTIONABLE",
         field="case.face.sigma_today_Pa; O3 usage zero",
         card=345000000, check_demand_Pa=fp["stress_Pa"],
         issue="345 MPa is the SR-200 datasheet minimum tensile yield, used as compressive. It is not a sourced compressive minimum at 0.691748 mm or after forming. The historical 379.2 MPa compression is a 1.96 mm sheet lot, not a thin-sheet minimum.",
         implication="The three-of-five result is conditional on an additional, unvaried material transfer assumption. The card already flags this, so this is a carried source limitation, not an arithmetic error.",
         source="Materion DS-HPP-613; NASA CR-194164 PDF p.22 Tables 2–3",
         needed_evidence="Thin-sheet post-form compression and biaxial properties, with gauge and orientation."),
    dict(id="NFI-021B-CHECK-NU", status="open", tag="QUESTIONABLE",
         field="inherited isotropic nu=0.33",
         card=.33, historical_sheet_nu12=.0768, historical_sheet_nu21=.0752,
         same_geometry_global_at_needed=s["nu_00768_same_geometry"]["global_buckling"],
         same_geometry_needed_gamma_usage=s["nu_00768_needed"]["usage"]["O1_gamma"],
         same_set_reoptimized_usage=s["nu_00768_continuous_least_set"]["max_usage"],
         issue="The isotropic 0.33 value is inherited from aluminium, not established for SR-200. The cited lot has substantially lower in-plane Poisson ratios.",
         implication="At nu=.0768, fixed-geometry global SF is 0.961118. Retuning the same gamma/wrinkle/panel set works at usage about 0.883289. This scalar substitution is a sensitivity, not an orthotropic laminate solution.",
         source="NASA CR-194164 Tables 2–3; pinned 014b nu",
         needed_evidence="A consistent orthotropic shell model and sourced thin-sheet elastic tensor."),
    dict(id="NFI-021B-CHECK-TOLERANCE", status="open", tag="PROJECTION",
         fields=[x["field"] for x in summary["failed"]],
         exact_mismatches=summary["failed"],
         inherited_nu03=s["tolerance_015_convention_needed"],
         consistent_nu033=s["tolerance_at_needed"],
         issue="The two filed RMS values use nu=.30 for angular width, while mechanics inherit nu=.33. More substantially, amplitude is inverted from a lambda_I=1 fit and then the RMS width is set to 2.625; that is not a single defect with a demonstrated knockdown/amplitude/RMS tuple.",
         implication="45.819441 mm amplitude reproduces. With width nu=.33, the same lambda_I=1 Gaussian gives 0.654416 mm whole-sphere RMS; merely changing width gives 1.717842 mm, not a validated tolerance at the same knockdown. The filed 1.708852 mm is reproduced with width nu=.30.",
         source="Baizhikova et al., doi:10.1016/j.jmps.2025.106468, Eq.2–3 and section 4.1; MAINLINE-015",
         needed_evidence="State width and nu together; calculate a coupled defect response for the sandwich, including seams and multiple defects."),
    dict(id="NFI-021B-CHECK-GRADE-COUPLING", status="open", tag="QUESTIONABLE",
         field="subsets versus optimisms.O3_face_strength.E_full_Pa",
         card_full_E_Pa=293600000000, reproduced_search_E_Pa=290000000000,
         card_all_five_usage=.7193182727147767,
         coupled_full_lot_E_grid_usage=next(x for x in s["grid_strength_E2936"] if x["mask"] == 31)["best"]["max_usage"],
         issue="The complete subset table reproduces with E=290 GPa even when O3 is selected. Full-named-set mode and family calculations instead use 293.6 GPa. Thus the subset table does not literally couple every O3 strength choice to the stated alternate lot modulus.",
         implication="Using E=293.6 GPa whenever O3 is selected changes secondary scores, e.g. all five to 0.708874 on the same grid. No subset feasibility changes and no two-member set floats. The chosen three-member set has no O3, so its answer is unchanged.",
         needed_evidence="Declare whether keeping 290 GPa is intentional conservatism; if grade and strength co-vary, specify interpolation and recompute the usage objective."),
    dict(id="NFI-021B-CHECK-PRESSURE", status="open", tag="QUESTIONABLE",
         field="019 pressure-swing service assumption versus scored reference pressure",
         reference_pressure_Pa=o["case"]["p0_Pa"],
         plus_1pct_modes=s["pressure_plus_1pct_at_needed"],
         issue="The printed point scores the COMMON reference pressure. The inherited service package includes a 1% pressure swing; its high-pressure structural corner is separate from the low-pressure buoyancy corner.",
         implication="At +1% external pressure on the same geometry and needed values, global and wrinkle SF are 0.990099, compression 0.990103. This does not contradict the reference-case arithmetic but prevents treating that exact point as covering the complete service package.",
         needed_evidence="Retune against the specified pressure envelope and retain the separate low-pressure/hot buoyancy budget."),
    dict(id="NFI-021B-CHECK-PANEL-GAUGE", status="open", tag="PROJECTION",
         field="O4 today's panel width and headline 0.691748 mm faces",
         card_today_square_equivalent_m=.9144, required_panel_m=fp["panel_width_m"],
         gauge_minus_01016mm_modes=s["uniform_low_gauge_screen"],
         issue="The 609.6 by 1828.8 mm stock limit applies to gauges at least .059 inch; the maximum stock size at the required .0272 inch gauge is unspecified. Forming, joining and gauge retention at a 3.128 m square-equivalent panel are unestablished.",
         implication="Even the today panel endpoint is a thin-sheet transfer. A uniform minus-0.1016-mm gauge screen at fixed core reduces compression SF to 0.853129 and wrinkling SF to 0.787988; this is a sensitivity, not a prediction of the delivered gauge distribution.",
         source="Materion DS-HPP-613; MAINLINE-020 gauge/shape assessment",
         needed_evidence="Supplier-confirmed gauge and dimensions, curved panel takeoff, measured gauge and shape map."),
    dict(id="NFI-021B-CHECK-RESERVE-JOINTS", status="open", tag="PROJECTION",
         field="019 fixed reserve and unvaried seam/adhesive assumptions",
         check_fixed_kg=a["fixed_kg"], check_reserve_kg=fp["masses_kg"]["reserve_total"],
         issue="The correct mass closure still assumes sealed service, zero payload, the chosen weather/water condition, 60 mm strips, 0.2 mm seam adhesive, 1.5 mm core splice and no demonstrated Be/core bond at the nominated film weight. These are explicit inputs, not measured capabilities.",
         implication="3M lists .030 and .015 lb/ft² films, with .015 unsupported; nominal areal mass does not qualify the joint. 775.729 kg reserve is spent on the declared condition rather than spare payload. Other service, seal, coating or handling loads need a new budget.",
         source="MAINLINE-019/020; 3M AF 163-2 technical datasheet",
         needed_evidence="Weighed sealed sandwich/seam specimen with load transfer and gas-load measurements; declared site and payload."),
]
save("NFI.json", dict(schema=1, card="CHECK MAINLINE-021b", unit=UNIT,
                     rows=nfi, blocking=False, disposition="Record and route; none stops this completed check."))

sources = load("sources/sources.json") + load("sources/ref-954ffee0678b4689fda3-sources.json")
inputfiles = [p for p in (HERE / "snapshots").iterdir() if p.is_file()]
inputs = dict(
    schema=1, unit=UNIT, authority=ORDER, source_card="MAINLINE-021b",
    started_at=meta["started_at"], ended_at=ended, times_are="measurements only",
    method="Independent equations, closed-form mass closure, exhaustive discrete search and continuous refinement. Owner programs were neither read nor executed/imported; copied only as opaque hash evidence.",
    snapshots=[pin(p) for p in sorted(inputfiles)],
    owner_pin_audit=load("PIN-AUDIT.json"), upstream_pin_audit=load("UPSTREAM-PINS.json"),
    tolerance_reference_pins=load("PINS-015.json"), primary_sources=sources,
    case=o["case"], source_and_tag_audit=[
        dict(input="47 honeycomb core tuples", source="Pinned 014b INPUTS cores_eligible", tag="QUESTIONABLE or PROJECTION per row",
             check="Names, density, Ec, W-direction Gc, crush and cell size are inherited with their tags; no source-free substitution."),
        dict(input="SR-200 E 290 GPa, density 1850, minimum tensile yield 345 MPa", source="Materion DS-HPP-613", tag="QUESTIONABLE",
             check="Datasheet values verified; compression and thin formed panel transfer unverified."),
        dict(input="Historical compression 379.2 MPa and lower E 293.6 GPa", source="NASA CR-194164 Tables 2–3", tag="QUESTIONABLE",
             check="Same 1.96 mm sheet lot, lower directional entries; not a modern specification minimum."),
        dict(input="Nu .33", source="Pinned aluminium-origin 014b case", tag="QUESTIONABLE",
             check="Not a sourced SR-200 value; NFI-021B-CHECK-NU."),
        dict(input="Five optimism endpoints", source="019/020/021b plus CR-1457 and source PDFs", tag="QUESTIONABLE; gamma curve/panel capability PROJECTION",
             check="Logarithmic usage independently inferred and reproduced; no linear interpolation assumption."),
        dict(input="Fixed reserve and seam geometry", source="019 declared optimistic scenario", tag="QUESTIONABLE/PROJECTION owner assumptions",
             check="Every mass term rederived; no default percentage reserve substituted."),
    ],
    equations=[
        "A=4*pi*R^2; J=c(f,w)*S+d(w)+2*A*film*(0.45359237/0.3048^2)",
        "c=(2/w)*(b*(1-f)+q*rho_splice*f/rho_core); d=(2*A/w)*2*b*t_adh*rho_adh",
        "S=min((L-100-F)/1.05,(L-100-F-d-films)/(1+c)); M=F+max(0,J-.05*S)",
        "tf=S*(1-f)/(2*A*rho_face); tc=S*f/(A*rho_core); h=tf+tc; applied=p*R/(4*tf)",
        "sigma0=E*h/(R*sqrt(1-nu^2)); sigmacrimp=Gc*h^2/(2*tf*tc); Vc=sigma0/sigmacrimp",
        "Kc=1-Vc/4 for Vc<=2, else 1/Vc; globalSF=gamma*Kc*sigma0/applied",
        "wrinkleSF=beta*C*sqrt(E*Ec*tf/tc)/applied; beta^3+beta=1",
        "dimplingSF=E*(tf/cell)^2/((1-nu^2)*applied); crushSF=2*crush/p",
        "u=max(0,log(required/today)/log(full/today)); panel/film endpoints geometric",
        "t_eq=sqrt(3)*h; delta/t_eq=-log((gamma-.45)/.51)/3.88",
        "beta0=lambda*sqrt(t_eq/R)/[12*(1-nu^2)]^(1/4); full-sphere small-angle RMS=delta*beta0/sqrt(8)",
    ],
    reproduction=["python3 check021b.py", "python3 supplemental.py", "python3 make_check.py"],
)
save("INPUTS.json", inputs)
results = dict(
    schema=1, unit=UNIT, card="CHECK MAINLINE-021b", status="COMPLETED_WITH_NFI",
    tag="QUESTIONABLE", certification="none", authority=ORDER,
    started_at=meta["started_at"], ended_at=ended, times_are="measurements, never limits",
    verdict="The conditional mass/mode result and all 32 feasibility classifications reproduce. Two RMS values use a different Poisson-ratio convention. Source and service qualifications remain.",
    arithmetic_comparisons=summary, all_32_feasibility_outcomes_match=True,
    pinned_material_count=47, owner_pins_match=7, additional_input_pins_match=13,
    fewest_named_optimisms=3, selected_set=["O1_gamma", "O2_wrinkle", "O4_panel_size"],
    declared_point=fp, continuous_refinement=refined, calculations=a, supplemental=s,
    nfi_ids=[x["id"] for x in nfi],
)
save("RESULTS.json", results)

source_audit = """# Primary-source and tag audit — CHECK MAINLINE-021b

SR-200: E 290 GPa, density 1.85 g/cm³ and minimum tensile yield 345 MPa agree with the current datasheet. It supplies no thin-sheet compressive minimum. The 24×72 inch maximum stock size is limited to gauges at least .059 inch; smaller dimensions for .020–.058 inch sheet are unspecified. Thus the 0.9144 m square-equivalent “today” endpoint already assumes a transfer to thin stock. [Materion DS-HPP-613](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6).

The historical sheet compression and elastic entries reproduce: 379.2/382.7 MPa compression, E 298.7/293.6 GPa, nu12/nu21 .0768/.0752. The 1.96 mm lot is cited to Fenn et al. (1967); the original Fenn report was not opened. These measurements do not establish a minimum for the proposed .692 mm formed face. [NASA CR-194164, PDF p.22 Tables 2–3](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf).

The film catalogue lists .015 lb/ft² AF 163-2U without carrier, and .030 lb/ft² in several forms. Both areal masses are real catalogue entries. The sheet describes representative properties and tests on specified adherends; it does not qualify these Be/honeycomb joints. No cured mass reduction is assumed here. [3M AF 163-2, PDF p.1](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=AF163-2.pdf).

The climate formula follows the ideal-mixture p/T relation with a rounded water/dry-air molar-mass correction .378. The chosen weather and vapour pressure are planning assumptions. The full CIPM metrology correlation is not used. [CIPM-2007, Eq.1](https://www.nist.gov/system/files/documents/calibrations/CIPM-2007.pdf).

The imperfection paper defines Gaussian width and the exponential knockdown fit. Its .45, .51, 3.88 coefficients are averaged over R/t=100–1550 for fixed lambda_I=1. The paper specifically discusses width as a separate parameter. Its homogeneous hemispherical-shell study does not validate the equivalent-thickness transfer to this sandwich. The .30 width convention is inferred from exact numerical reproduction of 021b/015 RMS, while .33 is the pinned mechanical nu. Mixing a lambda_I=1 amplitude with a 2.625 width is an illustrative RMS calculation, not a validated tolerance pair. [Baizhikova et al., Eq.2–3 and §4.1](https://www.epfl.ch/labs/flexlab/wp-content/uploads/2025/12/Baizhikova-et-al.-2026-A-probabilistic-buckling-model-for-hemispherical-shells-with-non-interacting-localized-defects.pdf).

The six mode equations, biaxial wrinkle interaction and dimpling factor follow the opened handbook. The smooth 018 gamma curve remains the declared projection. Core constants retain the catalogue's tags, direction and source entries. [NASA CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf).

Exact PDF bytes and origins are pinned in INPUTS.json. Reused PDFs are from this seat's completed 021 source check. New film, climate and imperfection PDFs were fetched directly from the manufacturer, NIST and authors' university. No owner numerical program was read, executed or imported.
"""
(HERE / "SOURCE-AUDIT.md").write_text(source_audit)

card = f"""# CHECK MAINLINE-021b — conditional result reproduced

Independent check complete under `{ORDER}`. The self-consistent mass, six mechanical modes and all 32 subset feasibility outcomes reproduce. There are **216 matching comparisons out of 218**; the two differences are RMS values whose width calculation uses nu=.30 rather than the mechanical nu=.33. Those convention mismatches and six other source/model issues are recorded in seven NFI rows. No NFI stops work.

The least named set remains **gamma, wrinkling and panel size**. No pair works across the 47 pinned honeycomb cores. Even the best pair at its full endpoints reaches only **0.900488 SF**. The filed point closes at **4,889.442150 kg**, including **775.729374 kg** reserve. Required gamma is **0.468228567**, wrinkle coefficient **0.609201444**, and panel width **3.127802787 m**. Compression demand is **344.998605 MPa**, against the assumed 345 MPa.

Continuous refinement gives maximum logarithmic usage **{refined['max_usage']:.12f}**, compared with the filed **0.834205134848**. It uses f={rp['fraction']:.12f}, panel width **{rp['panel_width_m']:.9f} m**, face **{rp['tf_m']*1000:.9f} mm**, core **{rp['core_m']*1000:.9f} mm**, and reserve **{rp['masses_kg']['reserve_total']:.6f} kg**. The selected set is unchanged.

This is conditional arithmetic: 345 MPa is a tensile minimum transferred to compression; thin stock dimensions, forming and bonds remain unverified; isotropic nu=.33 is inherited. A nu=.0768 sensitivity still permits the same set after retuning, at usage about .883289. The exact filed needed-value point falls to SF .990099 at +1% pressure. The alternate lot's E=293.6 GPa improves some secondary subset scores; it does not change which subsets work.

All seven owner pins, nine selected upstream pins and four tolerance-reference pins match. Owner programs were copied only for hashes; none was read, run or imported. [CHECK.md](CHECK.md) gives equations and comparisons, [RESULTS.json](RESULTS.json) contains the search, [NFI.json](NFI.json) records exact issues, and [SOURCE-AUDIT.md](SOURCE-AUDIT.md) grounds sources.

Started {meta['started_at']}; completed {ended}. Measurements only. ESTIMATE/QUESTIONABLE, with PROJECTION where named; no certification. Stop and file. No successor is named by this check order.
"""
(HERE / "CARD.md").write_text(card)

lines = [
    "# Independent CHECK MAINLINE-021b",
    "",
    "The headline conditional result reproduces. This check uses its own equations and search; it never executes or imports the owner's calculation. The filed CARD, results, inputs and program bytes match their pins. Copies are fixed in snapshots/.",
    "",
    "## Mass and mechanical equations",
    "",
    "Let S be faces plus core, f its core fraction, A=4πR², w the square-equivalent panel width and F the fixed reserve. Seam length is 2A/w. Two face strips, two local adhesive layers and one through-core splice give J=cS+d+films. The direct solution is S=min[(L−100−F)/1.05, (L−100−F−d−films)/(1+c)]. Reserve is F+max(0,J−.05S). This avoids iterating an already geometry-dependent reserve.",
    "",
    "The seven fixed reserve lines independently sum to 411.298944071647 kg. Water is 1000A×.0001; climate is L[1−.99T0/(T0+10)]; humidity is L×.378×1000/p0×T0/(T0+10); internal gas is .01L. Contamination adds 5 kg. Systems excess and payload are zero. The retained 100 kg systems allowance is not spent twice.",
    "",
    "CR-1457 mechanics use h=tf+tc, applied stress pR/(4tf), σ0=Eh/[R√(1−ν²)], σcrimp=Gch²/(2tftc), Vc=σ0/σcrimp and Kc=1−Vc/4 below Vc=2, otherwise 1/Vc. Global SF=γKcσ0/applied. Honeycomb wrinkling uses βC√(EEctf/tc), with β³+β=1. Equibiaxial dimpling is E(tf/cell)²/(1−ν²). Core crush uses twice core strength divided by p. No extra knockdown is applied to gamma.",
    "",
    "## Filed floating point",
    "",
    "| Quantity | Independent value |",
    "|---|---:|",
]
for key in ["faces", "core", "joint_allowance_0_05S", "joint_seams", "joint_bond_films", "joint_excess_in_reserve", "reserve_fixed_items", "reserve_total", "systems_allowance", "total"]:
    lines.append(f"| {key} (kg) | {fp['masses_kg'][key]:.12f} |")
lines += [
    "",
    "| Mode | Today at frozen geometry | Needed values | Full grade/coefficients | Full set, gamma .20 |",
    "|---|---:|---:|---:|---:|",
]
for mode in fp["today"]:
    lines.append("| " + mode + " | " + " | ".join(f"{fp[b][mode]:.12f}" for b in ["today", "at_needed_values", "at_full_named_set", "at_full_set_conservative_gamma"]) + " |")
lines += [
    "",
    "These today/full mode columns hold geometry and reserve fixed; they do not claim the geometry fits today's panel/film mass budget. Replacing its seams/films with today's endpoints gives 1229.431530407718 kg reserve, reproducing the card.",
    "",
    "## All 32 subsets",
    "",
    "Usage is logarithmic, u=max[0,ln(required/today)/ln(full/today)]; film uses the inverse ratio. It is not a linear fraction of improvement. The independent exhaustive grid uses 1999 interior fractions k/2000 and all 25×25 endpoint-spaced panel/film combinations on 47 cores. All outcome classifications agree. The largest score residual is below 2.5e−8; this is below the declared 5e−8 numerical comparison tolerance. Headline scalar mass/modes agree to floating-point precision.",
    "",
    "| Set (G gamma, W wrinkle, S strength, P panel, B film) | Filed usage | Own same-grid usage | Within endpoints |",
    "|---|---:|---:|---|",
]
letters = ["G", "W", "S", "P", "B"]
for row in sorted(a["grid_32"], key=lambda r: (r["mask"].bit_count(), r["mask"])):
    owner = next(x for x in o["subsets"] if x["subset"] == row["subset"])
    label = ",".join(letters[k] for k in range(5) if row["mask"] & (1 << k)) or "∅"
    value = row["best"]["max_usage"] if row["best"] else None
    lines.append(f"| {label} | {fmt(owner['min_max_usage'])} | {fmt(value)} | {'yes' if row['feasible_within_named'] else 'no'} |")
lines += [
    "",
    "A second search maximizes the weakest SF at each subset's full endpoints, refines every located maximum and includes both sides of every Vc=2 crossing. Increasing panel width or reducing film increases allowable S and all scored capacities, so full endpoint geometry provides an upper envelope for a subset within its named bounds. All 47 per-core maxima for every subset are in CALCULATIONS.json. The strongest pair is G+W at .900488404807. Of the triples, only G+W+P reaches 1; full-endpoint maximum is 1.045398208390.",
    "",
    f"Continuous G+W+P refinement yields u={refined['max_usage']:.12f}, f={rp['fraction']:.12f}, w={rp['panel_width_m']:.12f} m. Exact root solving then enforces compression demand=345 MPa and equal gamma/panel usage; residuals are 0 Pa and about 1e−16 in usage. Required gamma={rp['needed_values']['gamma']:.12f}, C={rp['needed_values']['wrinkle']:.12f}. This is a refinement, not a contradiction of the card's disclosed grid.",
    "",
    "## Family and predecessor checks",
    "",
    "| Family | Filed full-set SF | Independently refined full-set SF | Refined today SF |",
    "|---|---:|---:|---:|",
]
for fam in ["aluminium", "aramid", "other"]:
    lines.append(f"| {fam} | {o['families'][fam]['least']:.12f} | {a['families'][fam]['least_SF']:.12f} | {a['families'][fam+'_today']['least_SF']:.12f} |")
lines += [
    "",
    "Every full-set family geometry, mass and mode is also evaluated at its reported grid fraction. Aramid remains below 1, constrained by crimp/global and wrinkle. All family winners agree.",
    "",
    f"At the 019 fixed reserve, the two named cores independently refine to SF {s['references_019']['aluminium']['least_SF']:.12f} aluminium and {s['references_019']['aramid']['least_SF']:.12f} aramid. Rebuilt aluminium reserve is {s['references_019']['aluminium']['rebuilt_reserve']:.12f} kg. All eight fixed-reserve subset values reproduce, including G+W usage .665635107091. The 021-rev1 E290/283 MPa, 5%-margin grid check reproduces .958071728400.",
    "",
    "## Numerical and source qualifications",
    "",
    "There are 218 explicit scalar comparisons: 216 within tolerance and two retained RMS convention differences. The differences are not discarded or silently normalized.",
    "",
    "| Field | Filed | Own with mechanical nu=.33 | Own with inherited width nu=.30 |",
    "|---|---:|---:|---:|",
    f"| needed-gamma rms_worst_mm | {o['floating_point']['tolerance_015_at_needed_gamma']['rms_worst_mm']:.12f} | {s['tolerance_at_needed']['rms_worst_mm']:.12f} | {s['tolerance_015_convention_needed']['rms_worst_mm']:.12f} |",
    f"| full-curve rms_worst_mm | {o['floating_point']['tolerance_015_at_018_curve']['rms_worst_mm']:.12f} | {s['tolerance_at_full_curve']['rms_worst_mm']:.12f} | {s['tolerance_015_convention_full_curve']['rms_worst_mm']:.12f} |",
    "",
    "The amplitude values 45.819441454003 mm and 21.806317396351 mm reproduce. Their lambda_I=1 fit and width-2.625 RMS must not be treated as a coupled tolerance at the same knockdown. SOURCE-AUDIT.md links the actual equation and fit domain. The near-.45 inversion floor also makes inferred amplitude sensitive to small gamma changes.",
    "",
    "The current-grade subset table uses E290 even for O3. Coupling selection of O3 to E293.6 on the same grid changes G+W+S+P from .773437596848 to .762656524691, G+W+S+B from .919468771067 to .912124640700 and all five from .719318272715 to .708874022151. This is conservative inconsistency in interpretation, not a lost feasibility margin. Every subset's yes/no outcome and the chosen no-O3 triple remain unchanged.",
    "",
    "The critical source transfer is tensile 345 MPa to thin formed-sheet compression. The exact point has only 0.00000404 compression SF above 1. A historical lower-nu scalar screen gives fixed-geometry global SF .961118; retuning the same set reaches 1 within the endpoints at usage .883289. A full orthotropic calculation remains needed. At +1% pressure the printed needed-value point has minimum SF .990099; at uniformly minus .1016 mm face gauge it has wrinkle SF .787988. These are stated sensitivities, not a claim that an unmeasured condition occurs.",
    "",
    "All seven NFI rows are open evidence tasks, not vetoes. Original NFI rows are retained in snapshots/NFI.json. The grade, core, adhesive, climate and source tags are explicitly audited in INPUTS.json and SOURCE-AUDIT.md.",
    "",
    "## Reproduction and scope",
    "",
    "Run `python3 check021b.py`, `python3 supplemental.py`, then `python3 make_check.py` from this output directory. CALCULATIONS.json and SUPPLEMENTAL.json preserve independent searches, exact residuals and sensitivities; RESULTS.json packages them. No owner program is used as an oracle. Material transfer and model validation are distinct from reproducing arithmetic.",
    "",
    f"Started {meta['started_at']}; ended {ended}. Times are measurements only. The checker submits one report and ends the turn; the robotics seat assigns further work.",
]
(HERE / "CHECK.md").write_text("\n".join(lines) + "\n")
meta.update(ended_at=ended, status="complete", output_files=["CARD.md", "CHECK.md", "RESULTS.json", "INPUTS.json", "NFI.json"])
save("CHECK-META.json", meta)
print(json.dumps(dict(status="packaged", comparisons=summary["n"], matching=summary["passed"],
                     explicit_mismatches=len(summary["failed"]), nfi_rows=len(nfi),
                     ended_at=ended, artifacts=[pin(HERE / p) for p in meta["output_files"]]), indent=2))
