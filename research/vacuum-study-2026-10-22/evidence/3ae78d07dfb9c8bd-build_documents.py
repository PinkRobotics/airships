"""Package completed results and source observations. No scientific simulation."""
from pathlib import Path
import json
import csv

R=Path(__file__).resolve().parent
TAG="QUESTIONABLE / PROJECTION"
t=json.loads((R/"TARGETS.json").read_text())
fold=json.loads((R/"intake/043-fold/RESULTS.json").read_text())
prior=json.loads((R/"intake/041/RESULTS.json").read_text())["best_closure_by_reserve"]

evidence=[
 dict(id="Hexoloy-SA",form="sintered monolith",compression_MPa=3900,compression_basis="manufacturer typical; specimen unspecified",
      other_statistics="listed m10 old sheet / m8 current web page, test mode not established as compression; flexure bars3x4x45mm",source="https://www.ceramicsrefractories.saint-gobain.com/sites/hps-mac3-cma-pcr/files/assetbank_media/hexoloy-sa-sic-en-1013-tds-215398.pdf"),
 dict(id="CVD-PureSiC",form="CVD monolith",compression_MPa=None,compression_basis="blank in manufacturer table",
      other_statistics="HR/LR flexure447/590MPa; no m or size basis",source="https://www.coorstek.com/media/4249/silicon-carbides.pdf"),
 dict(id="CVD-PremaTech",form="CVD monolith",compression_MPa=None,compression_basis="not reported",
      other_statistics="four-point flexure scale424MPa m11; geometry/effective size unspecified",source="https://www.prematechac.com/wp-content/uploads/2019/05/18437-CVD-Silicon-Carbide-Data-Sheet.pdf"),
 dict(id="UltraSiC",form="direct-sintered monolith",compression_MPa=3500,compression_basis="manufacturer typical; size unspecified",
      other_statistics="no compression distribution",source="https://www.coorstek.com/media/4249/silicon-carbides.pdf"),
 dict(id="SCS-6",form="monofilament for composite",compression_MPa=None,compression_basis="no tube compression population",
      other_statistics="maker tensile3900MPa; historical25mm tensile fibre m8.2, NASA19910011930; not compression",source="https://www.specmaterials.com/silicon-carbide-fiber-1"),
 dict(id="SCS-Ultra",form="monofilament for composite",compression_MPa=None,compression_basis="not reported",
      other_statistics="maker metric tensile5900MPa; m/size absent; page has unit/diameter inconsistencies",source="https://www.specmaterials.com/silicon-carbide-fiber-1"),
 dict(id="Hi-Nicalon-S-bundle",form="multifilament bundle",compression_MPa=None,compression_basis="not reported",
      other_statistics="tensile25mm bundle n26 m9 scale1730MPa; filament m8.42 scale3062MPa is another population",source="https://pmc.ncbi.nlm.nih.gov/articles/PMC7452681/"),
 dict(id="HNS-MI-SiC",form="melt-infiltrated CMC",compression_MPa=1000,compression_basis="reported greater than1000MPa in hot turbine component property averages; not RT tube",
      other_statistics="public m and size absent; private statistically derived curves mentioned but not supplied",source="https://bulletin.ceramics.org/article/ceramic-matrix-composites-taking-flight-at-ge-aviation/"),
 dict(id="Tyranno-SA-CVI",form="woven CVI composite",compression_MPa=None,compression_basis="not reported",
      other_statistics="flexure mean597MPa SD70 m10.2;34 bars25x4x2mm span16mm",source="https://www.jstage.jst.go.jp/article/matertrans/44/9/44_9_1797/_pdf"),
 dict(id="Tyranno-SA3-triplex",form="CVD/composite/CVD short tube",compression_MPa=None,compression_basis="not reported",
      other_statistics="ultimate hoop mean282.4MPa m11.05;first drop226.95MPa m5.30;10mm long ID8.5mm OD9.8-10.1mm",source="https://www.kns.org/files/pre_paper/33/15S-417%EA%B9%80%EB%8C%80%EC%A2%85.pdf"),
 dict(id="M55J-epoxy",form="composite coupon; proposed tube",compression_MPa=890,compression_basis="Toray2025 reference lot average,Vf60%,#2500epoxy130C,SACMA; not allowable",
      other_statistics="compression m and complete-tube size basis absent",source="https://www.toraycma.com/wp-content/uploads/M55J-Data-Sheet.pdf"),
 dict(id="K13D2U",form="fibre for composite tube",compression_MPa=None,compression_basis="not found",
      other_statistics="fibre tensile3700MPa E935GPa rho2.20; not composite compression",source="https://www.m-chemical.co.jp/carbon-fiber/pdf/dialead/composites.pdf"),
 dict(id="T700S-epoxy",form="composite coupon; proposed tube",compression_MPa=1450,compression_basis="Toray2025 reference lot average,Vf60%,epoxy130C,SACMA; not allowable",
      other_statistics="compression m and complete-tube size basis absent",source="https://www.toraycma.com/wp-content/uploads/T700S-Data-Sheet.pdf"),
 dict(id="Al6061T6",form="ductile metal tube",compression_MPa=None,compression_basis="source gives tensile yield276MPa; no compression fit used",
      other_statistics="tensile elongation12%; brittle Weibull rupture law inappropriate without evidence",source="https://online.kaiseraluminum.com/depot/PublicProductInformation/Document/1071/Kaiser_Aluminum_6061_Pipe_Tube.pdf")
]
for x in evidence:
    x.update(tag=TAG,compression_weibull_m=None,complete_member_compression_scale_MPa=None,
        qualified_compression_allowable_MPa=None,recomputed_frame_mass_kg=None,
        recomputed_P3_SF=None,strength_gap_multiplier=None,m_gap_multiplier=None,
        actual_hail_break_probability=None,dynamic_lost_member_cascade=None,
        computation_status="not executed after compare-01 admission refusal")
(R/"MATERIAL-EVIDENCE.json").write_text(json.dumps(evidence,indent=2)+"\n")
with (R/"MATERIAL-EVIDENCE.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=evidence[0].keys());w.writeheader();w.writerows(evidence)

nfi=[
 ("admission","blocking","Frame comparison, per-construction gap/ranking and damage work incomplete. compare-01 refused before start: PSI some avg10=5.64 >=5.00, exit75. No retry or alternate job.", "New authorized work needs host admission; this filing does not resume the refused work."),
 ("compression-statistics","open","No retrieved complete curved-member compression distribution for the required geometry, finish, joint load transfer and batch.", "Obtain matched compression strength distribution, sample counts, confidence limits and fracture-mode evidence."),
 ("compression-law","open","Tensile weakest-link Weibull volume scaling is not automatically valid in compression.", "Calibrate or reject the assumed compression hazard law."),
 ("catalogue-strength","open","Typical strength and coupon average are not characteristic scale or statistical allowable.", "Keep nominal, mean, scale and confidence-qualified allowable separate."),
 ("cvd-manufacture","open","No CVD 3m, roughly250mm OD, roughly1mm wall curved-tube qualification; maker compression entries absent.", "Establish geometry capability, dimensional flaws, handling strength and member tests."),
 ("scs-load-sharing","open","SCS fibre tensile data lack an assembled tube compression population; page units/diameters conflict.", "Specify matrix, Vf, orientation, transverse restraint and product grade before a member distribution."),
 ("cmc-population","open","HNS bundle statistics, GE hot MI compression and Tyranno flexure/hoop data describe different populations and mechanisms.", "Supply exact architecture/resin-or-matrix tube tests; do not splice strengths and m across them."),
 ("cfrp-allowable","open","M55J/T700S source compression averages lack full-tube size statistics; K13D2U compression absent.", "Define resin, cure, Vf, voids, fibre waviness, joints and full-member compression distribution."),
 ("orthotropy","open","Axial E alone does not set cylindrical-shell buckling. Draft transverse moduli and layup transfers unvalidated.", "Measure laminate A/B/D, Eax/GJ, imperfections and combined compression/bending limits."),
 ("frame-instability","open","041 k=.2 and rigid-joint assumptions remain unqualified;019 local peak sensitivity0.978132 is below1.", "Validate joints/global knockdown and a proper local-buckling/bending interaction."),
 ("hail-transfer","open","045 maps old022d shell stress into tensile C-ring/sectored populations without matched effective area. No computed041 or composite hail probability.", "Test actual loaded tubes under ice impacts and fit residual compression/rupture distributions."),
 ("cascade","open","045 static straight-frame redistribution is not a progressive dynamic cascade of resized curved041 members.", "Recompute load transfer with lost edge, merged skin bay, joint compliance, fracture and transient redistribution."),
 ("system-reliability","open","Target Pf excludes membrane,joints,instability,dependence,impact and lifetime degradation.", "Define mission/system failure event and common-cause populations."),
 ("nonbrittle-ranking","open","CFRP is not a ductile metal; no demonstrated higher-mass construction closes lift and damaged-capacity constraints.", "Compare actual complete-member residual strength and redundancy at the same lift/mass budget."),
 ("common-source-drift","nonblocking","Live COMMON.md changed after intake. The copy pinned by this order still verifies; no new content or authority was silently substituted.", "Use INPUT-CHECK.json to distinguish the unchanged pinned copy from the changed live original."),
]
(R/"NFI.json").write_text(json.dumps(dict(tag=TAG,work_complete=False,
    rows=[dict(id=f"051-{i:02d}-{key}",status=status,finding=finding,resolution=resolution) for i,(key,status,finding,resolution) in enumerate(nfi,1)]),indent=2)+"\n")
execution=[json.loads((R/"execution"/label/"END.json").read_text()) for label in ["targets-01","compare-01"]]
(R/"EXECUTION.json").write_text(json.dumps(dict(tag=TAG,task_time_limit=None,phase_time_limit=None,
    runs=execution,subsequent_numerical_work=False),indent=2)+"\n")
result=dict(unit="vacuum-mainline051-p3-frame-targets-1020",tag=TAG,status="PARTIAL_HELD_RESOURCE_ADMISSION",
    work_complete=False,qualified_frame_Pf=None,qualified_lifetime_Pf=None,qualified_structural_SF=None,
    completed=["288-row reliability target surface m5..40;actual lengths/coupon/3m references","592 arithmetic checks","primary-source material and damage-method evidence review"],
    incomplete=["material-by-material frame mass/SF recalculation","material-by-material numerical strength/m gaps","041-section hail calculation","lost-member/cascade recalculation","evidence-backed construction ranking"],
    target_summary=t["summary"],materials=evidence,execution=execution,
    prior_041_reference=[dict(reserve=k,mass_kg=prior[k]["mass_kg"],screened_SF=prior[k]["least_screened_SF"],
        local_peak_sensitivity_SF=prior[k]["local_max_compression_sensitivity_SF"]) for k in ["5","019"]],
    successor="none; stop and file; robotics owns progress")
(R/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")

lines=[
"**MAINLINE-051 — P3 complete-member targets and current material evidence**",
"",
"**PARTIAL / HELD: the reliability surface is complete; the construction comparison is unfinished. All scientific results are QUESTIONABLE / PROJECTION.** The host refused `compare-01` before execution at memory PSI some avg10=5.64 against <5.00. No retry or bypass was attempted. Material-specific frame mass, SF, hail probability and cascade calculations remain null. This is not a complete answer to the brief.",
"",
"The strongest completed finding is that the load level matters. Under the deliberately hypothetical **whole-member** scale 3.9 GPa and compression m=10, frame Pf at **operating pressure q=1** is 0.000643916 / 0.000947308 for the 5% / 019 reserves. Both meet 1e-3 within that restricted model. At the higher own-screen loads, Pf is 0.00252417 / 0.00214283. A current tube has not been shown to possess that distribution.",
"",
"**Target surface**",
"",
"The frame has 750 members. Each member's own peak compression is used, including FE bending and L/1000 bow with Euler magnification. The table gives required *equal complete-member characteristic compression*, GPa, at each point's own screened load. [All 288 rows](TARGET-SURFACE.csv) include every integer m=5…40, both loads and both probability targets.",
"",
"| m | 5%: Pf=1e-3 | 019: Pf=1e-3 | 5%: Pf=1e-6 | 019: Pf=1e-6 |",
"|---:|---:|---:|---:|---:|"
]
for m in [5,8,10,11,15,20,30,40]:
    row=[]
    for pf,reserve in [(1e-3,"5"),(1e-3,"019"),(1e-6,"5"),(1e-6,"019")]:
        x=next(x for x in t["rows"] if x["reserve"]==reserve and x["load"]=="own_screen" and x["m"]==m and x["frame_Pf_target"]==pf)
        row.append(f'{x["equal_complete_member_scale_GPa"]:.4f}')
    lines.append("| "+str(m)+" | "+" | ".join(row)+" |")
lines += [
"",
"![Conditional compression targets](TARGET-SURFACE.png)",
"",
"The grey line is the assumed 3.9 GPa scale, not measured complete-tube data. `019` denotes the fixed reserve from MAINLINE-019, not a 19% reserve.",
"",
"For m=10, the own-screen Pf=1e-3 target is **4.278678 / 4.209090 GPa**. The prior fold's strength multipliers over the assumed 3.9 GPa are shown below; alternatively m must reach **10.743153 / 10.603653** with that whole-member scale unchanged. For Pf=1e-6, m must reach **16.302396 / 16.089455**.",
"",
"| Reserve | Strength multiplier at m10, Pf1e-3 | Strength multiplier at m10, Pf1e-6 |",
"|---|---:|---:|"
]
for point in fold["points"]:
    case=next(x for x in point["load_cases"] if x["label"]=="own_screen")
    vals=[]
    for pf in [.001,.000001]:
        x=next(x for x in case["required_characteristics"] if x["calibration"]=="whole_member" and x["m"]==10 and x["frame_target"]==pf)
        vals.append(f'{x["factor_over_assumed_3p9GPa"]:.6f}')
    lines.append("| "+point["reserve"]+" | "+" | ".join(vals)+" |")
lines += [
"",
"**Coupon-to-member size effect**",
"",
"Actual f5 arc lengths are 1.984730–2.623498 m, mean 2.399569 m. The requested 3 m member is a reference size, not the actual mesh. With a compatible volume-flaw law, `sigma0_3m = sigma0_coupon (Vcoupon/(A×3m))^(1/m)`. For the 5% section the 3 m material volume is 2,292.464 cm³. The 1 cm³-to-3 m strength retention is 0.2128 at m5, 0.4613 at m10, 0.6792 at m20 and 0.8241 at m40.",
"",
"At m10, the required **1 cm³ coupon** scale for the actual frame at its own screen is **9.088382 / 8.907641 GPa** for Pf1e-3 and **18.134612 / 17.773969 GPa** for Pf1e-6. Equivalently the common **3 m reference** scales for Pf1e-3 are 4.192338 / 4.124156 GPa. Those differ from the equal-complete-member convention because it assigns an identical distribution to members of unequal lengths.",
"",
"If 3.9 GPa instead describes a 1 cm³ coupon, m must be **16.812530 / 16.563301** at the own screen for Pf1e-3; simply relabeling that coupon number as whole-member strength is invalid. At q=1 the same coupon hypothesis still gives Pf 0.700001 / 0.818685. All size laws remain uncalibrated compression hypotheses.",
"",
"**Today's members: what is established and what remains unknown**",
"",
"[SOURCES.md](SOURCES.md) gives the primary citations, strengths, m, modes and size bases for 14 construction/evidence families. [MATERIAL-EVIDENCE.json](MATERIAL-EVIDENCE.json) and its CSV preserve missing quantities as null.",
"",
"The essential distinction is between constituent data and a compression-qualified member. Sintered SiC has a typical 3.9 GPa compression number but no retrieved complete-member compression distribution. Commercial CVD sheets give flexural statistics or leave compression blank. SCS-6/Ultra values are fibre tension. HNS bundles and Tyranno composite flexure/hoop tests document load-sharing structures, but not P3 axial compression. [HNS bundle measurements](https://pmc.ncbi.nlm.nih.gov/articles/PMC7452681/) with m=9 and scale 1.73 GPa on a 25 mm gauge are not interchangeable with filament m=8.42 and scale 3.062 GPa.",
"",
"The current [Toray M55J](https://www.toraycma.com/wp-content/uploads/M55J-Data-Sheet.pdf) and [T700S](https://www.toraycma.com/wp-content/uploads/T700S-Data-Sheet.pdf) sheets give composite compression averages of 890 and 1,450 MPa, respectively; these are useful screening inputs, not pultruded-tube allowables or Weibull scales. [Mitsubishi K13D2U](https://www.m-chemical.co.jp/carbon-fiber/pdf/dialead/composites.pdf)'s 935 GPa is fibre tensile modulus; its complete-tube compression strength and m remain unestablished. The proposed composite tube also needs hoop/shear stiffness, resin support, fibre orientation and waviness, local shell stability and joint transfer data. No retrieved evidence supplies the requested complete-member statistical comparison.",
"",
"The only numerical frame masses/SFs carried forward here are the **existing 041 assumed-SiC references**, not newly calculated candidate results:",
"",
"| Reserve | Tube mass kg | Total including reserve/sag kg | 041 screened SF | Local peak sensitivity SF |",
"|---|---:|---:|---:|---:|"
]
for key in ["5","019"]:
    p=prior[key];lines.append(f'| {key} | {p["mass_kg"]["tube"]:.6f} | {p["mass_kg"]["total_with_reserve_and_sag"]:.6f} | {p["least_screened_SF"]:.9f} | {p["local_max_compression_sensitivity_SF"]:.9f} |')
lines += [
"",
"The **019 local sensitivity is below unity**. Neither nominal material strength nor the quoted headline SF resolves that issue. `material_models.py` and `frame_compare.py` are retained as unexecuted, syntax-checked drafts, with explicit assumptions; they have no numerical result to validate. They must not be read as a finished optimization.",
"",
"**Damage: correction to the brief's premises**",
"",
"045's 1.1–5.3% is a hypothetical local tensile-fracture result at the **older 022d** section and its higher ice-pressure model, using two Hexoloy tube-test populations. It is neither a measured strike probability nor a result for resized 041 members. Its lower fluid-pressure cases give different results. The C-ring/sectored test sizes and flaw populations also do not establish an ice-contact probability transfer. [The original tube-test report](https://lwrs.inl.gov/content/uploads/11/2024/03/M3LW-13IN0504053-Silicon_Carbide_Ceramic_Matrix_Composite_Failure_Mode_Analysis.pdf) distinguishes those test modes.",
"",
"Similarly, 045's f5 deleted-edge model uses straight beams and the old tube section. Its f5 peak stress factors are 2.427/2.480, while neighbor axial-force factors are 1.281/1.210; the larger 3.27 stress factor belongs to f4. A static stress amplification is not a simulated progressive cascade. No new 041 damage run was admitted.",
"",
"Actual hail break probability and dynamic cascade status are **null for every proposed construction**. Applying ceramic C-ring m to CFRP would omit delamination, fibre kinking and residual compression strength. Under 045's separate merged-bay span rule, lost-edge film demand increases by 1.5; both 041 film screens are below 1.5. Changing only tube strength would therefore leave an independent skin-support problem.",
"",
"**Answer supported by the completed portion**",
"",
"No evidence-backed “closest current construction” or higher-mass non-brittle winner can be selected from this filing. That part is incomplete after the resource refusal, and key tube statistics are absent. Conditional on already possessing the assumed whole-member distribution, the old SiC reference meets Pf=1e-3 at q=1. To retain both higher own-screen loads instead, the narrow statistical gap closes at scale 4.278678 GPa with m=10, or at m=10.743153 with scale 3.9 GPa. This does not close impact, skin-support, joint or buckling gaps.",
"",
"CFRP may offer load redistribution and damage-tolerant architectures, but “non-brittle” is not an established property of these tubes. [NASA's impact/CAI work](https://ntrs.nasa.gov/api/citations/20160010546/downloads/20160010546.pdf) explicitly addresses brittle composite damage and subsequent compression failure. Higher mass must also fit the fixed lift budget; neither condition was demonstrated here.",
"",
"The direction established by the evidence is to measure and improve **the complete tube's compression distribution and damaged residual capacity**, while preserving shell/frame stiffness and skin support. A fibre-tensile improvement alone is not a demonstrated answer. The prior 017b trend concerns historical specific stiffness; it does not prove that all SiC strength, processing or damage properties are frozen.",
"",
"**Coverage and handoff**",
"",
"592 numerical checks passed for the 288 completed target rows. One job completed and released; one was refused without starting. Fifteen NFIs retain the resource blocker, physical evidence gaps and source drift. The live COMMON.md changed after intake; its order-pinned copy remains intact. [INPUT-CHECK.json](INPUT-CHECK.json) records both hashes. [METHOD.md](METHOD.md), [EXECUTION.json](EXECUTION.json), [NFI.json](NFI.json) and the pinned input/source records define the limits. No other seat was contacted. Brief says stop and file; robotics owns the next job. This report preserves an incomplete assignment, not a completion claim.",
]
(R/"CARD.md").write_text("\n".join(lines)+"\n")
print("Wrote evidence, NFI, execution, results and partial card from completed data.")
