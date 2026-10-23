#!/usr/bin/env python3
"""Render the morning read, full register and provenance from the checked packet."""
import json
import re
from pathlib import Path

B=Path(__file__).resolve().parent
def load(name): return json.loads((B/name).read_text())
def write(name,text):
    if name!="REPORTS.md":
        # Readable prose spacing; immutable source fields remain in JSON.
        prose_words=("maximum","continuum","versus","and","are","carries","corrected",
                     "zeros","retains","creates","passes","periods","sealed","retaining",
                     "attachment","totals","leaving","overrunning","by","on","reductions",
                     "multipliers","optimum","trend","all","total","in","since","only",
                     "around","about","comparison","specification","amplitude","need",
                     "required","unknown","priority","factor","screen","witness",
                     "with","from","before","after","at","core","film","sheet","original",
                     "current","measured","surrogate","topology","frequency","rank")
        # Apply only outside Markdown link targets and inline identifiers.
        parts=re.split(r'(\]\([^)]*\)|`[^`]*`)',text)
        for i,part in enumerate(parts):
            if i%2: continue
            for word in prose_words:
                part=re.sub(r'\b('+word+r')(?=[0-9])',r'\1 ',part)
            part=re.sub(r'\b(SF|λ|Vc)(?=[0-9])',r'\1 ',part)
            part=re.sub(r'\b(038|034|026b|022d|030|033)(?=(?:s|check)\b)',r'\1 ',part)
            part=part.replace("Woody's3","Woody's 3")
            parts[i]=part
        text="".join(parts)
    (B/name).write_text(text.rstrip()+"\n")
def table(headers,rows):
    def cell(x): return str(x).replace("|"," / ").replace("\n"," ")
    return "\n".join(["| "+" | ".join(headers)+" |","|"+"|".join(["---"]*len(headers))+"|"]+
                     ["| "+" | ".join(cell(x) for x in row)+" |" for row in rows])
def link(report,name="CARD.md",label=None):
    p=B/"snapshots"/report/name
    if not p.exists(): p=B/"snapshots"/report/"CHECK.md"
    if not p.exists(): p=B/"snapshots"/report/"report.json"
    return f"[{label or report}]({p.relative_to(B)})"
r=load("RESULTS.json"); f=load("BUILD-FACTS.json"); aliases=f["aliases"]; p3=r["P3_lead"]; fold=r["P3_ordered_fold"]
cov=r["coverage"]; intake=load("INTAKE.json"); plan=r["physical_test_plan_038"]
def src(alias): return link(aliases[alias],label=("CHECK-"+alias[5:] if alias.startswith("CHECK") else "MAINLINE-"+alias))
p2rows=[]
for p in r["P2_leads"]:
    label=p["id"]
    if 10<p["R_m"]<11: label+="; full-endpoint threshold witness"
    p2rows.append([label,f'{p["gamma"]:.6f} / {p["gamma_factor"]:.6f}×',
                   f'{p["Q"]:.6f} / {p["Q_factor"]:.6f}×',
                   f'{1000*p["tf_m"]:.6f} / {1000*p["tc_m"]:.6f}',
                   f'{p["face_compression_required_Pa"]/1e6:.3f}',
                   f'{p["physical_joining_kg"]:.3f}',f'{min(p["modes"].values()):.6f}'])
p2table=table(["Lead / radius, m","γ / factor over .20","Q / factor over .33",
               "Face / core, mm","Face demand, MPa","Joining, kg","Least modeled SF"],p2rows)
paytable=table(["Radius, m","Handbook signed mass margin, kg","Full γ+Q, six modes, kg",
                "Full γ+Q + scarf, kg","Same scarf + retained floor, kg"],
 [[p["R_m"],*[f'{p[k]:.3f}' for k in ["handbook_kg","gamma_Q_full_six_modes_kg",
   "gamma_Q_full_with_scarf_kg","gamma_Q_full_with_scarf_and_floor_kg"]]] for p in r["P2_payload"]])
mass=table(["022d component / debit","kg"],[[k,f"{v:.6f}"] for k,v in p3["mass_kg"].items()])
modes=table(["Mode","022d screened","After ordered 0.848 global sensitivity"],
            [[k,f'{(p3["SF"].get(k,p3["joint"].get(k.removeprefix("joint_")+"_SF",0))):.6f}',f'{v:.6f}']
             for k,v in fold["modes"].items()])
alts=[p for p in r["P3_all_rows"] if p["case"]["family"]=="cfrp_zylon"
      and p["case"]["grid"]=="equilateral" and p["case"]["band"]=="in_band"]
alttable=table(["022d reserve / sag model","Least SF","Spacing, m","Sized axial/bond target, MN"],
 [[p["case"]["reserve"]+" / "+p["case"]["branch"],f'{p["SF_least"]:.6f}',f'{p["s_m"]:.6f}',
   f'{p["joint"]["design_force_N"]/1e6:.6f}'] for p in alts])
pending=[p["item"] for p in r["pending"] if p["status"]=="PENDING"]
card=f"""# MAINLINE-030b — Morning design register

**QUESTIONABLE throughout; material/process and cross-geometry transfers are PROJECTION. Installed-hull safety factors remain unknown.**

P2 has a conditional R10 floating point with two adjustable factors on stock-size panels; the thin bond and unqualified material/joint assumptions remain fixed inputs. At the +1% pressure used by 033, the scarf-screened γ+Q threshold is about R10.35–10.36 m. Larger hulls reduce the required γ improvement and can carry modeled payload at the full endpoints. P3's corrected screened continuum point is SF **{p3["SF_least"]:.6f}**. The ordered 026b sensitivity moves only its global mode to **{fold["moved_least_SF"]:.6f}**, about **1.07**, with the same mass and other mode values. Neither hull is qualified.

This refile retains all **{cov["baseline_rows"]} original register rows**, **362 original unique source findings** and their **363 source pointers**, including both uses of N023. It adds **{cov["new_upstream_source_rows"]} source finding records** and **{cov["authored_rows"]} synthesis findings**: **{cov["total_unique_source_rows"]} total**, organized under **{cov["register_rows"]} rows**. Repeated findings in different filed reports remain attributed copies, not claimed new physical gaps. All raw fields and auxiliary dispositions are retained. Snapshot: **{r["snapshot_at"]}**.

Read [REGISTER.md](REGISTER.md) for all issues; [OPTIMISM-LEDGER.md](OPTIMISM-LEDGER.md) for every factor and evidence route; [GROUND-FIRST.md](GROUND-FIRST.md) for the physical sequence; [LEDGER.md](LEDGER.md) for corrections; [REPORTS.md](REPORTS.md) for every addition. Machine records are [RESULTS.json](RESULTS.json), [NFI.json](NFI.json) and [SOURCE-INDEX.json](SOURCE-INDEX.json).

## P2: current points and the assumptions attached to each

{p2table}

The 028b rows use p₀=95,460.837914 Pa, ν=.0752 and the retained joint floor max(J, .05S). The 033 rows use 1.01p₀, ν=.0768 and actual joining as their main account. The R10 028b pass and R10 033 scarf failure therefore have different bases. The exact 033 full-γ/Q threshold is **10.350852 m** with actual joining and **10.358194 m** with the retained floor. Its threshold witness uses Q=.82 with wrinkle SF1.929; it is not a minimum-Q point. The other 033 entries minimize the maximum normalized optimism usage. Their payload is approximately zero. Sources: {src("028b")}, its independent check in [REPORTS.md](REPORTS.md), and {src("033")}.

The nominal R10 face/core is 0.794624/23.237218 mm. Physical joining is 215.742 kg at the reoptimized point, not the old frozen 214.240 kg bill. The 5 g/m² primer variant needs γ=.578524 and Q=.428952; the laboratory cell-edge/ideal-weld route needs γ=.391500 and Q=.597089 but assumes a different unqualified process. For nominal R10, global, wrinkling and scarf screen all bind at one; face compression is 1.148724, crimp 2.441308, core crush 5.055822 and dimpling 6.758508. Every point's complete modes, mass geometry and provenance are in RESULTS.

O1 and O2 are the two adjustable factors. O3 strength and O4 panel enlargement are held at factor one, which does not close their evidence gaps. O5 is already consumed: .015 instead of .030 lb/ft² bond film is a 2× mass reduction. Stock blank dimensions are 0.6096×1.8288 m; required thin-gauge supply and formed compression remain unqualified. The scarf screen assumes 30:1 geometry and 10 MPa average shear, with peel, moment, cure and installed efficiency still open.

**Compression at every point.** {src("036")} finds no qualified minimum for finished thin SR-200 sheet. The 345 MPa catalog value is tensile yield. Required face stress is shown for each point above: about 300.333 MPa for the R10/R20/R30 scarf leads, 321.580 MPa for the ideal-weld alternative. Historical thicker-sheet 379.2 MPa compression is precedent, not an allowable. The roughly 382 MPa R20 requirement in 036 belongs to its older 027 η=.9 splice/elasticity model; it must not replace 033's own R20 demand. Finished gauge and further processing must be specified without deducting an already included etch twice.

{src("CHECK036")} reproduces all4,945 numerical comparisons, including150 threshold/sensitivity points, and confirms the historical379.2MPa value at1.96mm. It retains every qualification gap. Its sheet-scalar R20 requirements span381.612–381.639MPa across the stated elastic alternatives. One legacy label says.015lb/ft², but that olderR20 mass model correctly uses the governing.146472829kg/m² per interface, equivalent to.030lb/ft². This is a metadata correction, separate from the actual.015 film chosen for028b/033.

**Weather/altitude at every point.** Attach {src("031")} and CHECK-031 as requirements, not a solved retrofit onto these geometries. Its older 021b construction, reoptimized for an illustrative 100 m centre-altitude floor, needs 55.341 kg optimistic climate headroom or 441.770 kg for both weather sets; corresponding ISA equilibria are 617.075 and 1464.507 m. The first case uses γ=.448157, Q=.667241 as its selected input, and enlarged 2.863504 m panels. Its Q input is not necessarily a binding minimum. Spending all nominal lift permits below-sea-level roots in the hot/low/humid scenarios. Terrain-relative clearance, ceiling, weather envelope and control are the Admiral's choices. These mass reserves cannot be silently spent as payload in 033.

**Extra loads at every point.** {src("037")} evaluates 028b's full-endpoint R10 point (baseline SF1.006358), not all minimum-usage points or the larger 033 hulls. Its uniform 70-knot pressure excess lowers the screen to .998442; its 35 ft/s gust at 35 knots gives 1.003303. Coated thermal core-shear SF is 1.678 with an ambient stress-free reference but .917 with the cold-night reference; bare Be gives .388. An unreinforced mooring patch has SF .354. Nominal single-pad estimates of 8.65/33.14 kg and coating must be charged before reclosure. Wind, bond reference temperature, fatigue and local load transfer remain open.

### P2 payloads at full γ and Q endpoints

{paytable}

These are reoptimized full-endpoint results, separate from the minimum-usage points above. Positive values are modeled payload after that track's specified allowances; negative values are mass deficits. The scarf screen changes R20/R30 full-endpoint payload from 4,884.560/18,139.202 kg to **1,808.333/7,754.736 kg**. Retaining the unused 5% floor reduces those further to **1,106.350/4,559.419 kg**. Coating, pads, complete service hardware and a chosen weather mission still need a common audited account.

There is no qualifying singleton among 033's three bounded sliders on its primary basis. Its flat-γ=.20 ideal upper bound stays below one. A core/crimp branch using γ=1 is a different assumption; the Q+strength shell-only crossing near R16.28 m and retained-floor crossing near R40.47 m must retain that label. The formal γ+strength crossing near R103.89 m needs faces beyond the admitted sheet maximum.

## P3: corrected screened point and discrete sensitivity

Use {src("022d")} instead of the older 022b/022c or 017b optima. The selected equilateral, cap-sag, 5% reserve point has spacing **{p3["s_m"]:.6f} m**, actual arc **{p3["member_length_m"]:.6f} m**, OD **{2000*p3["r_o_m"]:.6f} mm**, wall **{1000*p3["wall_m"]:.6f} mm**, and total 0/90 Zylon gauge **{1e6*p3["film_total_m"]:.6f} μm** split equally between directions. SiC forms the tubes; CFRP identifies the end fittings. The half-wave/member ratio equals one. This passes the requested minimum screen only, not a validated continuum band, and spacing exceeds the older fixed 3 m cutoff.

{modes}

Per the follow-up order, **0.848 × {fold["original_global_SF"]:.12f} = {fold["moved_global_SF"]:.12f}**. The exact 026b frequency-4 ratio **{fold["source_exact_factor"]:.12f}** would give **{fold["exact_ratio_sensitivity_SF"]:.12f}**. Global then binds alone under held other-mode values. This is a **QUESTIONABLE sensitivity across different sections and topologies**, not a recalculated current frame or a new allowable. No reoptimization, added payload, nonlinear credit or reduction of existing joints is taken.

{mass}

The 244.472 kg reserve is already inside closure; it is not a second free payload. Both film plies are charged, and axial/bond joint mass is sized at the target multiplier, increasing the λ=1 mass 27.912764 kg to 44.191468 kg. The target joint load is 1.099425 MN. Barrier/seams/coating, adhesive and actual moments/anti-roll capacity remain open. The film effective design strength is 1.74 GPa at 1,560 kg/m³: a {p3["film_specific_strength_factor_vs_Kapton_design"]:.3f}× specific-strength comparison against the selected Kapton design value, not qualified complete-membrane performance.

The selected lead carries 3.9 GPa typical SiC crush as Fc; design-pressure maximum compression is .947377 GPa and compression at its original claimed multiplier is 1.198096 GPa. Full-size compression allowable and failure probability remain null. Its assumed 15.586 MPa tensile ceiling is also a projection; no tensile stress occurs at this selected target. Local-shell, column, curvature and contact interaction remain unresolved.

{alttable}

038's latest procurement example uses the **019** row and its **1.035188 MN** joint target. Use the **1.099425 MN** target for the 5% lead above; do not mix rows. Membrane sag is a separate branch. The overall long-span maximum1.397733 remains outside the half-wave screen. Mylar and Kapton/Ti alternatives remain below one. Two-way screened surrogate SF1.867825 lacks the in-plane shear mechanism required by C=4 and is not promoted to a lead.

**Discrete evidence.** {src("026")} and CHECK-026 retain the frequency-6 rigid linear λ6.465222 versus continuum6.127640, 61.400928 kg mass overrun and freely rolling pin mechanisms. {src("026b")} gives frequency-4 λ5.254644 versus6.193381 and frequency-2 λ2.183661 versus6.876245: 15.157% and68.243% below continuum. Free-pin mechanisms are1,080/480/120. Its mass-derived payloads −61.401/301.391/301.814 kg use different source accounts; frequency4 omits sag and frequency2 carries187.938 kg sag debit. They are not the corrected022d vehicle.

026b's new nonlinear tangent zeros5.082444/2.218113 are **not verified first-instability limits**: nearest-zero selection can skip a negative family. No nonlinear computation was run for this register. Eightfold member rise retains538.899 kN mean compression and creates4.248 GPa elastic bending; it does not divide thrust by eight. Rigid joints, film stiffness, contact and local/material failure must be resolved before an elastic frame multiplier becomes useful capacity evidence.

## Evidence, service and directions

{src("CHECK035")} revises {src("035")}: all112 comparable derived fields reproduce, but the source readings and conclusions need correction. S-II hemisphere graph centers read **about .21–.22**, with approximately **±.01** graph uncertainty; their Vc and plastic/thermal reductions remain unresolved. Add the omitted eleventh cylinder point near R/ρ=121, γ=.61, and use CR-1457's analytic curve instead of the eye fit. CTA8.3's printed .864 and load-ratio .865305 remain unresolved alternatives; CTA8.1 was out-of-autoclave and its measured thickness changes Vc.

Additional marine egg-shaped/ellipsoidal and foam-core-cylinder experiments invalidate categorical “nothing else found” or universal absence claims. Yang's12.44MPa result is plastic collapse; Sim's uniform-pressure results are FE. The defensible gap is **no compatible elastic sphere/dome datum with recoverable moderate Vc at the lead geometry established by this check**. Neither the current required γ nor a claim of unprecedented imperfection control is validated. Cylinder, monocoque and cap ratios cannot qualify the current sphere. The optimism ledger compares current γ to the corrected graph centers and their reading uncertainty, with that limited scope.

032 and 032b translate Q into conditional waviness. The combined check passes533 comparisons, corrects Woody's3 μm to **template-adjustment RMS**, identifies the .008-inch aluminium coupon faces, and adds Rion carbon/Nomex depth measurements near that system's own critical wavelength. Conditional full wrinkle periods37–40 mm sit near/below Woody's stated >40 mm measurement band. Cell depth, slope, panel RMS and the required modal amplitude remain distinct. No actual Be/CR-III matching-band measurement is established. Current point amplitudes at conditional Fc=35/60 psi are in the optimism ledger; Fc must be the weakest compression/tension/bond capacity and35 psi is minimum average.

{src("034")} identifies ground evacuation plus sealed24-hour service as a30–50 kg planning candidate while retaining100 kg systems. Gas-only pressure lifetimes do not prove electrical endurance. Its older geometries leave large gas inventories unless every cell/bore is vented; outgassing changes the phase of already carried mass, whereas ingress adds mass and getters retain it. Its older Zylon barrier/attachment57.546 kg plus service/fitting allowance totals91.624–111.624 kg, leaving8.376 kg or overrunning100 kg by11.624 kg. Recompute these inventories on022d/033 before claiming extra payload.

{src("017b")} adds a directional and historical-property study. Its P2 R10/R20 handbook results .528361/.571058 use ν=.08, variable scarf ratio and piecewise γ. Its lone-factor face-density reductions1.871/1.734, γ multipliers4.059/3.409 and face-modulus multipliers2.041/1.928 therefore retain those separate definitions; the modulus solutions sit at the fragile Vc2 step. Its pre-022d P3 optimum1.441 and film-trend14–25-year closure are superseded as current design predictions. No rerun of its direction optimization is implied. Historical source gaps, noncomparable properties and all15 findings remain in the register.

## Grounding and handoff

{src("038")} supplies nine physical test families. Its first three are **finished-sheet compression/specification**, **a weighed curved sealed scarf assembly**, and **same-batch wrinkle coupons**. The original five ground-first routes remain preserved in [GROUND-FIRST.json](GROUND-FIRST.json), with the physical sequence distinguished from FE preparation. 038's total43–158k USD including shared stock/process is a filed planning projection, not a quote or new spending recommendation. No supplier, lab or seat was contacted.

Unfiled at this snapshot: **{", ".join(pending) if pending else "none"}**. These belong in030c when filed. All filed additions found by the final bounded queue scan are indexed; no running-seat result is inferred. Coverage, provenance and local arithmetic checks are in [VALIDATION.json](VALIDATION.json); reproduction is in [METHOD.md](METHOD.md). Stop and file; the robotics seat sends the next job.
"""
write("CARD.md",card)

op=load("OPTIMISM-LEDGER.json")
lines=["# MAINLINE-030b optimism ledger","",
       "QUESTIONABLE / PROJECTION. `precedent` means evidence in another property, process or geometry; `none` means no matched capacity evidence. No current lead has matched measured hull validation. All original030 lead/optimism records remain in RESULTS.original_030_history.","",
       "P2 factors use γ/.20 and Q/.33; face-strength factor uses the assumed345MPa tensile proxy. Panel factor one means no enlargement; thin-gauge availability remains open. Bond factor denotes mass reduction from.030lb/ft². P3 factors are the stated numerical comparators, not interchangeable property requirements.",""]
for lead in dict.fromkeys(x["lead"] for x in op["rows"]):
    lines+=["## "+lead,"",table(["ID / assumption","Factor or value","Evidence class","Evidence / limit","Ground route / 038 tests"],
      [[x["id"]+" / "+x["name"],x.get("factor") if x.get("factor") is not None else x.get("value",x.get("value_Pa","not assigned")),
        x["evidence_category"],x["evidence_state"],x["grounding_route"]+" / "+", ".join(x["physical_tests_038"])]
       for x in op["rows"] if x["lead"]==lead]),""]
lines+=["## Conditional metrology at every P2 point","",
        "These new inverse calculations use032's checked equation with the selected geometry and η=1. They are projections, not shop measurements.35psi is minimum-average stabilized compression; neither35 nor60psi establishes actual weakest core/bond Fc. The threshold row at Q=.82 has zero allowable δ in this idealization and is not a minimum-Q design.","",
        table(["Point","δ at35psi, mm","δ at60psi, mm","γ / corrected S-II centers","Including ±.01 graph uncertainty"],
          [[p["id"],f'{1000*p["waviness_projection"]["35"]:.6f}',
            f'{1000*p["waviness_projection"]["60"]:.6f}',
            "–".join(f"{v:.3f}" for v in p["gamma_over_different_hemisphere_graph_centers"]),
            "–".join(f"{v:.3f}" for v in p["gamma_over_hemisphere_graph_read_uncertainty_range"])] for p in r["P2_leads"]]),"",
        "CHECK-035's graph centers are approximately.20924/.22151, with ±.01 reading uncertainty. Different geometry, unknown Vc and unresolved plastic/thermal reductions prevent interpreting these as qualified improvement requirements. The uncertainty column is only a graph-reading interval, not an experimental confidence bound. Required face compression, weather, loads and joining are attached to every point in RESULTS and the morning card."]
write("OPTIMISM-LEDGER.md","\n".join(lines))

g=load("GROUND-FIRST.json")
lines=["# MAINLINE-030b ground-first register","",
       "The original030 computational/evidence priority list is preserved below.038 supplies a separate physical purchase/test sequence. No physical result, quote, contact, purchase or qualification is inferred.","",
       "## 038 physical sequence","",
       table(["Rank / test","Test","Initial projected kUSD","Follow-on projected kUSD","Route"],
        [[str(t["rank"])+" / "+t["id"],t["title"],"–".join(map(str,t["initial_kUSD"])),
          "–".join(map(str,t["follow_on_kUSD"])),t["provider_type"]] for t in plan["tests"]]),"",
       "First three incremental23–68k; shared stock/process20–90k; total43–158k USD, all filed planning PROJECTION. Equal-biaxial follow-on18–45k is separate. T9 reuses the T2 fixture; do not charge it twice. Standards/provider examples and specimens are in "+
       src("038")+". No quote or availability is confirmed. For selected022d5% and019 joint targets use1.099425 and1.035188MN respectively; frozen022c tables remain historical.","",
       "## Routes and remaining evidence","",
       table(["ID / original rank","Route","Status","038 tests","Next evidence"],
        [[x["id"]+" / "+str(x["original_030_priority"]),x["route"],x["status"],", ".join(x["physical_tests_038"]),x["target"]]
         for x in g["routes"]]),"",
       "## Original030 ground-first list, preserved","",
       table(["Rank","What","Retires","Original owner"],
          [[x["rank"],x["what"],x["retires"],x["owner"]] for x in g["original_030_ground_first"]]),"",
       "The1m-diameter aluminum shell is a conditional model experiment. Assumed25µm face/1mm core fabrication floors imply minimum radii.3614/.4303m for old/current target geometry; no purchasable Be miniature is established. Honeycomb cell similarity, full imperfection fields, seam effects and normalization remain open. Sea-level evacuation offers only6.14% overload over the R10 design pressure. Survival without reaching collapse censors the result; it does not measure a collapse factor."]
write("GROUND-FIRST.md","\n".join(lines))

ledger=load("LEDGER.json")
lines=["# MAINLINE-030b corrections ledger","",
       f'{ledger["baseline_rows"]} original ledger records remain verbatim in LEDGER.json; the table below is the additive030b lead reconciliation. A reproduced number does not qualify the design.',"",
       table(["Correction","Effect on current lead","Filed evidence"],
         [[x["correction"],x["effect_on_lead"],", ".join(link(v,label=v) for v in x["by"])]
          for x in ledger["rows"] if x.get("register_version")=="030b"]),"",
       "All checks, full report statements and retained findings are in [CHECK-VERDICTS.json](CHECK-VERDICTS.json). Original corrections remain in [the030 ledger](snapshots/baseline030/LEDGER.json)."]
write("LEDGER.md","\n".join(lines))

issues={x["uid"]:x for x in load("NFI.json")["rows"]}
lines=["# MAINLINE-030b complete issue register","",
       f'{cov["total_unique_source_rows"]} source/authored records under{cov["register_rows"]} topics/rows. Original fields stay verbatim in REGISTER.json; all source fields stay verbatim in NFI.json. Historical “today” and “needed” fields below are explicitly the030 record, not silently current values.030b additions and dispositions follow each row. Nothing closes merely because it was merged.',"",
       "[Morning read](CARD.md) · [All raw findings](NFI.json) · [Coverage](REGISTER-COVERAGE.json) · [Corrections](LEDGER.md)",""]
topic=None
for row in load("REGISTER.json")["rows"]:
    if row["topic"]!=topic:
        topic=row["topic"];lines+=["## "+topic+" — "+row["topic_name"],""]
    lines+=['<a id="'+row["rid"]+'"></a>',"### "+row["rid"]+" — "+row["gap"],"",
            "**Original030 unknown:** "+str(row["unknown"]),""] if row["sources"] else ["### "+row["rid"]+" — "+row["gap"],""]
    for key in ["today","needed"]:
        if row[key]: lines+=["**Original030 "+key+":** "+"; ".join(row[key]),""]
    if row.get("current_030b"): lines+=["**Current030b:** "+row["current_030b"],""]
    refs=row["sources"]+row["updates_030b"]
    records=[]
    for ref in refs:
        x=issues[ref["uid"]];fields=x["fields"]
        if isinstance(fields,dict):
            texts=[str(fields[k]) for k in ["title","topic","issue","claim","unknown","finding","note","question","need","needed_to_ground","disposition","implication"] if k in fields]
            summary="; ".join(texts) if texts else json.dumps(fields,ensure_ascii=False)
        else: summary=str(fields)
        source=Path(x.get("snapshot",x["file"]))
        target=str(source.relative_to(B)) if source.is_relative_to(B) else str(source)
        records.append([x["uid"],x["row_id"],"030b addition" if ref in row["updates_030b"] else "030 retained",
                        summary,f'[{x["report"]}]({target})'])
    lines+=[table(["UID","Source row","Version","Finding / disposition (full raw fields in NFI.json)","Source"],records),""]
write("REGISTER.md","\n".join(lines))

lines=["# Filed additions to MAINLINE-030","",
       "Snapshot "+intake["sampled_at"]+". Source-artifact pins verified on intake. Original030 INDEX retained separately, including its historical provenance defects. Four Oct19 administrative reports are context only and confer no new instructions. Repeated NFI files are retained under each report identity.",""]
for report in intake["reports"]:
    count=sum(x["report"]==report["id"] for x in issues.values())
    lines+=["## "+report["id"],"",report["at"]+"; "+str(count)+" retained finding records.","",
            report["body"],"",
            "Artifacts: "+", ".join(f'[{Path(a["snapshot"]).name}]({Path(a["snapshot"]).relative_to(B)})'
               for a in report["artifacts"] if a.get("snapshot")),""]
write("REPORTS.md","\n".join(lines))
write("METHOD.md","""# MAINLINE-030b method and reproduction

This is an additive synthesis, not a new hull optimization or a qualification. Only own `.ship` files were written. No owner code, solver, upstream test suite, supplier contact or other-seat message was run.

1. Pin the dispatch, brief and original030 packet; preserve86 original register rows,362 unique findings,363 pointers,88 ledger entries and35 check records.
2. `intake.py` scans the named queue submission directory with bounded mainline/check filename patterns and aware timestamps. Filed additions absent from baseline INDEX are retained even if their timestamp precedes030's declared snapshot. Each first-seen artifact is SHA256/byte checked. Readable files are copied; code/binaries are pinned without execution. Repeated refreshes retain initial immutable snapshots.
3. `normalize.py` retains source fields, row IDs, classifications and auxiliary disposition documents. UID identity is report/path/row ID. Repeated findings in separate reports are attributed copies. `ROUTING.json` maps every addition to a row; no unmapped finding is allowed. Combined032/032b findings retain both primary collections and all disposition lists.
4. `build_register.py` preserves original fields, appends findings, and selects current points from filed JSON. Source selectors and hashes accompany the leads. Existing named optimisms and old lead records remain in RESULTS history. The main source contracts differ and are stated explicitly.
5. The only new scientific arithmetic is conditional inverse waviness, numerical evidence comparisons and the ordered026b global-only sensitivity. Waviness uses δ=tc Fc/(.64 Ec)(.82/Q−1), Ec=15ksi and Fc scenarios35/60psi at η=1. Fc remains the weakest flatwise core/bond strength, not established by the compression scenarios. Gamma comparisons use CHECK-035's corrected S-II graph centers.20924155/.22151060 and a separate ±.01 reading interval, with unmatched geometry, unknownVc and unresolved plasticity. The superseded.22/.24 readings remain only in original source history. Film specific-strength compares1740MPa/1560 with115.5MPa/1420. The ordered factor.848 multiplies022d's global mode once; other modes/mass stay fixed. The exact026b ratio is a separate sensitivity, never a universal correction.
6. `write_docs.py` renders the card, complete issue register, optimism, corrections, grounding and source-report pages from the packet. `validate_packet.py` independently checks coverage, preserved fields, source pointers/pins, equations, mass arithmetic and links. These are local synthesis checks, not reruns of every owner simulation or checks of material capability.

Reproduce with Python3, `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=unpublished-local-ref:55d45bae31a12320, in this directory: run normalize, build_register, write_docs and validate_packet in that order. Refreshing intake requires human/agent review and explicit routing of new findings before build. The packet is filed only after the final intake is incorporated. All times are measurements, not execution budgets.

The bound of the claim is all relevant filed reports found by the recorded final scan; running seats and unfiled artifacts supply no result. Pending items are for030c. Inputs, validation and the artifact manifest are pinned by the filed report.
""")
print("Rendered CARD, REGISTER, OPTIMISM-LEDGER, GROUND-FIRST, LEDGER, REPORTS and METHOD.")
