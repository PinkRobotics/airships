#!/usr/bin/env python3
"""Package independent MAINLINE-032 evidence, qualification findings and plots."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def read(name):
    return json.loads((ROOT/name).read_text())


def save(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")


def pin(path):
    data=path.read_bytes()
    return dict(path=str(path.resolve()),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))


def plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    spec=importlib.util.spec_from_file_location("own_032_check",ROOT/"check.py")
    own=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(own)  # Own equations only; main() is not called.
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout="constrained")
    data=[]
    colors=["#175b91","#b34a22"]
    for index,face in enumerate(own.FACES):
        color=colors[index]
        for strength,style in [(60,"-"),(35,"--")]:
            delta=np.linspace(0,0.00032,321)
            q=own.q_at(delta/face["tc_m"],strength)
            for axis,norm,xlabel in [(axes[0],face["tf_m"],"Amplitude / face thickness, δ / t_f"),
                                     (axes[1],own.CELL,"Amplitude / cell size, δ / s")]:
                axis.plot(delta/norm,q,color=color,linestyle=style,linewidth=1.7,
                          label=f"{face['name']}; Fc = {strength} psi")
                lead=own.amplitude(face,face["lead_Q"],strength)
                axis.scatter([lead["delta_m"]/norm],[face["lead_Q"]],color=color,
                             marker="o" if strength==60 else "s",s=27,zorder=4)
            for x,y in zip(delta,q):
                data.append(dict(face=face["name"],Fc_psi=strength,delta_mm=float(x*1000),
                                 delta_over_tf=float(x/face["tf_m"]),
                                 delta_over_cell=float(x/own.CELL),Q=float(y)))
    for axis in axes:
        for q in (0.371,0.609):
            axis.axhline(q,color="#666666",alpha=0.55,linewidth=0.8,linestyle=":")
        axis.set_ylim(0.14,0.85)
        axis.set_ylabel("Uniaxial waviness coefficient Q")
        axis.grid(alpha=0.15)
        axis.spines[["top","right"]].set_visible(False)
    axes[0].set_xlabel("Amplitude / face thickness, δ / t_f")
    axes[1].set_xlabel("Amplitude / cell size, δ / s")
    axes[0].set_xlim(0,0.47)
    axes[1].set_xlim(0,0.034)
    axes[0].legend(fontsize=8,loc="upper right",frameon=False)
    fig.suptitle("MAINLINE-032: independently reconstructed conditional waviness curves",fontsize=12)
    fig.supxlabel("η = 1; Ec = 15 ksi; brief geometry. Markers: each face's lead Q. Fc scenarios are not measured sandwich allowables.",
                  fontsize=8)
    fig.savefig(ROOT/"Q-WAVINESS.png",dpi=170)
    fig.savefig(ROOT/"Q-WAVINESS.pdf")
    plt.close(fig)
    with (ROOT/"CURVE-DATA.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(data[0]))
        writer.writeheader();writer.writerows(data)


def main():
    d=read("RESULTS.json")
    i=read("inputs/owner-INPUTS.json")
    old_nfi=read("inputs/owner-NFI.json")
    source_audit=[
        dict(id="NASA-EQ2212",source=NASA,location="printed p. 2-33; PDF page 75",
             status="verified_visually",
             finding="Numerator is 0.82*(Ec*tf/(eta*Ef*tc))^(1/2)*(eta*Ef); denominator is 1+0.64*Kdelta. Equation 2.2-13 defines Kdelta=delta*Ec/(tc*Fc).",
             evidence="sources/nasa-eq2212.png"),
        dict(id="NASA-FC",source=NASA,location="printed p. 2-29; PDF page 71",
             status="verified_visually",
             finding="Fc is the lowest flatwise core compression, core tension, and core-to-facing bond strength. Stabilized compression is only one candidate.",
             evidence="sources/nasa-fc-definition.png"),
        dict(id="HEXCEL-5056",source=HEXCEL,location="Table II, 3/8 inch, 1.0 pcf; PDF p. 5",
             status="verified_visually",
             finding="Bare compression 55 psi typical / 25 psi minimum average; stabilized 60 / 35 psi; compression modulus 15 ksi typical; crush strength 35 psi typical. Tests at 0.625 inch. The min column means minimum average for a product type.",
             evidence="sources/hexcel-table2.png"),
        dict(id="NASA-BIAXIAL",source=NASA,location="printed p. 2-33, Eqs. 2.2-15/16; rationale at p. 2-26",
             status="verified",
             finding="Wrinkling interaction Rx^3+Ry=1 uses separately normalized uniaxial critical loads. Equal critical loads and equal applied compression yield the scalar cubic. The earlier rationale is large-aspect-ratio flat plates.",
             evidence="sources/nasa-eq2212.png"),
        dict(id="NASA-DIMPLING",source=NASA,location="printed pp. 2-2, 2-4, 2-7",
             status="verified",
             finding="Intracell uniaxial coefficient K=2 uses cell size across flats. Its biaxial interaction is Rx+Ry=1, giving one half for equal compression. The text says sufficiently large dimples can precipitate wrinkling; separate scalar margins are not proof of independence."),
        dict(id="NASA-DESIGN033",source=NASA,location="printed pp. 2-32/33",
             status="verified",
             finding="0.33 is selected from test data, not a measured wave. The test subset excludes poor bonds with flatwise tension below compression and uses cases close to elastic behavior. Final matching-configuration tests are recommended."),
        dict(id="FPL1810A",source=FPLA,location="title; printed pp. 1–2, 5–6, 12–13",
             status="primary_pdf_retrieved",
             finding="Norris, Boller and Voss. Cell size affects wrinkling wavelength; fitted wavelength is not necessarily equal to cell size. Original-wave scaling assumptions differ between continuous and honeycomb cores.",
             evidence="sources/fpl1810a.pdf"),
        dict(id="FPL1810",source=FPL,location="Part I introduction, printed p. 2; authors cross-checked against CR-1457 ref. 2-9",
             status="primary_indexed_excerpt_read_full_download_unavailable",
             finding="Fourier components near the critical wavelength are amplified; neighboring wavelengths can also contribute. Complete cited author list: Norris, Ericksen, March, Smith and Boller. March, not Kommers, is the third author.",
             access_note="Direct PDF fetch returned HTTP 502; primary-source indexed passage was read in web search. No full local PDF or checksum is claimed."),
        dict(id="HEXCEL-TELEGRAPH",source=DESIGN,location="printed p. 5",
             status="primary_pdf_retrieved",
             finding="Larger cells with thin skins may telegraph into a dimpled surface; no numerical depth or qualified Be-bonded waveform tolerance is supplied.",
             evidence="sources/hexcel-design.pdf"),
        dict(id="FLATIRON",source=i["flatness_sources"][1]["url"],location="one-page stock-panel sheet",
             status="primary_pdf_retrieved",
             finding="Flatness is ±0.008 inch per radial foot. Selected stock variants have 0.040 inch faces, 3003 aluminum core and 5052-H32 faces. A separate 0.125 inch panel variant uses 0.020 inch faces. These are panel tolerances, not critical-mode amplitude measurements.",
             evidence="sources/flatiron.pdf"),
        dict(id="HONYLITE",source=i["flatness_sources"][2]["url"],location="Strength & Flatness",
             status="primary_page_retrieved",
             finding="Balanced aluminum panels: ±0.7 mm per radial metre, conditional on panel construction and fixturing.",
             evidence="sources/honylite.html"),
        dict(id="QC",source=i["flatness_sources"][3]["url"],location="flatness guarantee FG190101",
             status="primary_pdf_retrieved",
             finding="Wave ±1 mm and overall ±1/16 inch (printed parenthetic 1.5 mm) per 60 inch. The parenthetic metric number is a rounded manufacturer statement, not an exact inch conversion.",
             evidence="sources/qc.pdf"),
        dict(id="INDY",source=i["flatness_sources"][4]["url"],location="§6.1 and scope",
             status="primary_pdf_retrieved",
             finding="Finished welded metallic core within 0.010 inch under hold-down of no more than 7 psi; local steps no more than 0.003 inch. Scope lists titanium, nickel alloys and stainless steel, not this bonded aluminum/Be sandwich.",
             evidence="sources/indy.pdf"),
        dict(id="SAE",source="https://saemobilus.sae.org/standards/ams7902h-beryllium-sheet-plate-98be",
             location="official public record",
             status="scope_verified_flatness_classes_unverified",
             finding="Official H record confirms hot-rolled Be sheet/plate and the nominal thickness scope, but the retrieved public page does not expose §3.5.5 or quantitative flatness classes. This check cannot confirm the owner's three-class statement from primary text.",
             evidence="sources/sae.html"),
    ]
    save("SOURCE-AUDIT.json",dict(schema=1,unit=UNIT,rows=source_audit))
    findings=[
        ("FC","qualification",
         "60 psi typical and 35 psi stabilized compression are used as Fc scenarios.",
         "The correct Fc is min(compression, core tension, facing-core bond). Neither scenario establishes the bonded sandwich value. Typical crush 35 psi happens to equal minimum-average stabilized compression numerically, but represents a different property.",
         "Preserve the conditional labels; supply matching core tensile and Be-bond flatwise data before converting the scenario into an allowable.",["NASA-FC","HEXCEL-5056"],["fc-is-the-lower-of-three"]),
        ("MINIMUM-AVERAGE","qualification",
         "Owner calls 35 psi the stabilized minimum.",
         "Table II labels min as minimum average for a product type, not a guaranteed pointwise or full-hull minimum. Ec is typical. Pairing these values is a scenario, not a statistical lower tolerance bound.",
         "Use the precise source label and a qualified statistical/material basis for any design allowable.",["HEXCEL-5056"],[]),
        ("THICKNESS","open",
         "The table's compression data are from a 0.625 inch specimen.",
         "0.625 inch is 15.875 mm; the requested cores are 20.21 and 30.12 mm. No matching thickness/bonded-state validation was supplied.",
         "Retain QUESTIONABLE until relevant properties are measured or supported for the actual construction.",["HEXCEL-5056"],["sheet-thickness"]),
        ("ETA","open",
         "The map assumes elastic eta=1.",
         "Relative to sqrt(Ef*Ec*tf/tc), the effective coefficient is 0.82*sqrt(eta)/(1+0.64*Kdelta). For a fixed target Q, amplitude changes with eta. Plasticity in the nearly strength-limited faces is not calibrated.",
         "Use a measured constitutive/plasticity basis self-consistently; supplemental eta cases here are PROJECTION, not new material data.",["NASA-EQ2212","NASA-DESIGN033"],["eta"]),
        ("WAVELENGTH","open",
         "Amplitude/cell ratios are supplied beside inherited dimpling margins.",
         "Those ratios do not identify wavelength or mode separation. CR-1457 explicitly allows dimples to precipitate wrinkling. Dimpling uses a different biaxial factor (0.5) from wrinkling's cubic root.",
         "Measure the directional waveform spectrum and use a coupled assessment or matching experiment; do not apply the wrinkling multiplier to the dimpling formula.",["NASA-DIMPLING","FPL1810A","FPL1810"],["wavelength-versus-cell"]),
        ("SHOP-METRIC","open",
         "Commercial panel bows and core flatness are compared to the waviness amplitudes; Be class values were not read.",
         "Quoted product numbers reproduce, but geometry, material, ± convention, hold-down, wavelength and load state differ. The primary SAE public record does not verify the three-class claim or give flatness numbers.",
         "Obtain Be-specific finished/bonded-panel metrology near the relevant wavelengths; retain unverified SAE details as such.",["FLATIRON","HONYLITE","QC","INDY","SAE","HEXCEL-TELEGRAPH"],["shop-flatness-is-not-delta"]),
        ("BIAXIAL-TRANSFER","open",
         "b=0.6823 is applied to the uniaxial stress containing waviness.",
         "The algebra is correct for equal directional uniaxial capacities and does not count waviness twice. The handbook's flat-plate rule alone does not validate the loaded curved Be sandwich or establish equal directional capacity.",
         "Retain the algebraic result and QUESTIONABLE transfer; validate the actual biaxial construction and relevant directional capacities.",["NASA-BIAXIAL"],["biaxial-on-a-shell"]),
        ("DESIGN033","projection",
         "The 0.33 design coefficient is inverted as an illustrative wave amplitude.",
         "The arithmetic is correct but this is not a measured defect distribution or proof of why the empirical knockdown has that value. The owner already tags these rows PROJECTION.",
         "Keep the existing projection label and source-test limitations.",["NASA-DESIGN033"],["design-0-33-is-not-a-measured-wave"]),
        ("LEAD-RANGE","correction",
         "CARD says lead amplitudes span 0.0046–0.024 of the 9.525 mm cell.",
         "The lead-only ratios are 0.006847549228760197 and 0.01604921436707204. The printed endpoints are the two cross-Q rows among all four 60 psi cases. The underlying four rows are correct.",
         "Change the label to all four typical-strength cases, or use the lead-only range.",[],[]),
        ("ROUNDED-TARGET","qualification",
         "The specified brief rounds both geometry and required Q; many decimal digits are displayed.",
         "Using the full pinned 021/021b geometry and required Q gives conditional 60 psi amplitudes 0.15313481918912647 and 0.06513526466329604 mm. The brief-based rows differ by -0.1737373278% and +0.1345534421%, respectively. This is intentional input precision, not an error in the requested calculation.",
         "Use the full-input supplemental rows when interpreting the precise upstream SF=1 threshold; do not interpret decimal output as metrological accuracy.",[],[]),
    ]
    nfi=[]
    for suffix,status,reported,checked,next_step,sources,owner_ids in findings:
        row=dict(id="NFI-032-CHECK-"+suffix,status=status,disposition="non_blocking",
                 blocks_progress=False,tag="PROJECTION" if status=="projection" else "QUESTIONABLE",
                 reported=reported,checked=checked,followup=next_step,
                 source_audit_ids=sources,owner_nfi_ids=owner_ids)
        if suffix=="LEAD-RANGE":
            row["exact_values"]=d["prose_corrections"][0]
        if suffix=="ROUNDED-TARGET":
            row["exact_values"]=d["upstream_recalculation"]
        if suffix=="ETA":
            row["sensitivity_projection"]=d["inelastic_projection"]
        nfi.append(row)
    save("NFI.json",dict(schema=1,unit=UNIT,tag="QUESTIONABLE",blocks_progress=False,
                        findings=nfi,owner_nfi_dispositions=[
                            dict(id=row["id"],status="author_correction_verified" if row["id"]=="kommers" else "confirmed_open",
                                 original=row) for row in old_nfi["open"]],
                        next_job="none"))
    save("INPUTS.json",dict(
        schema=1,unit=UNIT,order=ORDER,owner_report="rpt-mainline032-grok-wrinkle-waviness-1020",
        authority=[ORDER],authority_owner_pins=read("inputs/pin-audit.json"),
        brief_pins=read("inputs/brief-pins.json"),upstream_pins=read("inputs/upstream-pins.json"),
        snapshots=[pin(p) for p in sorted((ROOT/"inputs").iterdir()) if p.is_file()],
        primary_sources=read("sources/manifest.json"),source_audit=str(ROOT/"SOURCE-AUDIT.json"),
        independent_inputs=d["independent_inputs"],
        methods=["Direct transcriptions of CR-1457 Eqs. 2.2-12, 2.2-13 and 2.2-15, visually verified.",
                 "Algebraic inversion in psi units so Fc/Ec cancels unit conversion; independent SI conversions.",
                 "60-digit Cardano solution for the equibiaxial cubic; exact substitution and rounding comparison.",
                 "Source-grounded intracell formula and its separate linear biaxial interaction.",
                 "Direct CARD/report token checks, with raw numerical deltas in CSV.",
                 "Full pinned 021/021b geometry used only for sensitivity and inherited dimpling/required-Q reconstruction; no optimisation rerun."],
        exclusions={"owner_elapsed_timer":"not independently reproduced; timestamps and timer preserved as metadata",
                    "SAE_class_tolerances":"not accessible in the primary public record",
                    "FPL1810_complete_PDF":"direct download unavailable; primary indexed introduction and NASA bibliography read"},
        foreign_scripts_read_or_executed=False,next_job="none"))

    table="| Face | Q | Fc psi | δ mm | δ/tf | δ/9.525 mm | Kδ |\n|---|---:|---:|---:|---:|---:|---:|\n"
    for index,row in enumerate(d["independent"]["amplitudes"]):
        face=("S-200F","SR-200")[(index%4)//2]
        fc=60 if index<4 else 35
        table+=f"| {face} | {row['Q']:.3f} | {fc} | {row['delta_mm']:.12f} | {row['delta_over_tf']:.12f} | {row['delta_over_cell_3_8_in']:.12f} | {row['K_delta']:.12f} |\n"
    design_table="| Face | Fc psi | Projected δ at Q=0.33, mm |\n|---|---:|---:|\n"
    for index,row in enumerate(d["independent"]["design_0_33_if_it_were_this_waviness"]):
        design_table+=f"| {('S-200F','SR-200')[index%2]} | {60 if index<2 else 35} | {row['delta_mm']:.12f} |\n"
    qtable="| δ/tc | Q at conditional Fc=60 psi | Q at conditional Fc=35 psi |\n|---:|---:|---:|\n"
    typical=d["independent"]["shared_curve_Q_versus_delta_over_tc"]["stabilised_typical_60_psi"]
    minimum=d["independent"]["shared_curve_Q_versus_delta_over_tc"]["stabilised_minimum_35_psi"]
    for a,b in zip(typical,minimum):
        qtable+=f"| {a['delta_over_tc']:.4f} | {a['Q']:.12f} | {b['Q']:.12f} |\n"
    finding_table="| Finding | Disposition | Exact point |\n|---|---|---|\n"
    for f in nfi:
        finding_table+=f"| {f['id']} | {f['status']} | {f['checked']} |\n"
    shop_table="| Primary source | Verified quantity | Comparison limit |\n|---|---|---|\n"
    for source,quantity,limit in [
        ("Flatiron", "±0.008 in/radial ft = ±0.2032 mm/radial ft; selected face 0.040 in = 1.016 mm", "Commercial aluminum panel, thicker selected faces; a spatial bow tolerance."),
        ("Honylite", "±0.7 mm/radial m", "Balanced aluminum panels; no critical-mode amplitude supplied."),
        ("QC Facades", "WAVE ±1 mm; ±1/16 in (printed 1.5 mm)/60 in", "Architectural surface categories; no critical-wavelength qualification."),
        ("Indy", "0.010 in = 0.254 mm overall; 0.003 in = 0.0762 mm steps", "Welded core under hold-down ≤7 psi, not this bonded Be/Al sandwich."),
        ("SAE AMS7902H", "Hot-rolled Be scope verified; no flatness-class values read", "Public primary page does not expose §3.5.5; three-class statement remains unverified here."),
        ("Hexcel design guide", "Telegraphing described; no amplitude depth", "No numerical as-bonded Be surface capability.")]:
        shop_table+=f"| {source} | {quantity} | {limit} |\n"
    check=f"""# MAINLINE-032 independent check — ESTIMATE / QUESTIONABLE

Unit `{UNIT}`; order `{ORDER}`. No certification. The focused equations and conditional tolerance tables pass; the amplitudes are not established manufacturing allowables.

All **236** numerical, Boolean, source-constant, display and self-check comparisons pass at the stated precision. This covers all 155 engineering/Boolean scalar leaves in owner RESULTS; the sole excluded numeric field is its elapsed timer. INPUTS has 38 checked scalar fields and two pin-length metadata fields separately verified. One CARD range label is incorrect. Ten nonblocking findings record that correction and the outstanding material, measurement and transfer limits.

## What was checked

The initial ten owner/authority artifact pins match. The owner script was hashed only; it was never read as code or run. Own `check.py` uses primary equations, the pinned brief's rounded face/core geometry, and independently read source constants. `NUMERIC-CHECK.csv` contains reported value, checked value and exact floating-point difference for every comparison. Raw tolerances are relative 3e-12 or absolute 1e-12. The inherited dimpling values use their stated one/two-decimal precision; exact underlying values are reported below. All other input/source and snapshot pins also verify.

Comparison categories: 139 numerical values, 14 Booleans, four rounded upstream quantities, 36 source constants or conversions, seven owner PASS labels, 20 CARD amplitude tokens and 16 additional CARD/report tokens. No equation or table mismatch survives the appropriate precision comparison. Source facts and access limitations are recorded separately in `SOURCE-AUDIT.json`; an unavailable source passage is not treated as verified.

## Equation and strength definition

The printed [NASA CR-1457]({NASA}) pages 2-29 and 2-33 were inspected visually. Its equations give

`sigma_u = 0.82 sqrt(eta Ef Ec tf/tc) / (1 + 0.64 Kdelta)`,
`Kdelta = delta Ec/(tc Fc)`.

For the elastic case, define `Q=sigma_u/sqrt(Ef Ec tf/tc)`. Then

`Q = 0.82/(1+0.64 Kdelta)` and
`delta = (tc Fc/Ec) (0.82/Q - 1)/0.64`.

This is a monotone amplitude ceiling when the model, properties, wavelength interpretation and target Q apply. It gives zero amplitude at Q=0.82; positive amplitude for 0<Q<0.82. No face thickness enters this inverse at fixed Q, although tf enters the normalization δ/tf and the required stress.

**Fc is the lowest flatwise core-compressive, core-tensile and core-to-facing bond strength.** Stabilized compression is the relevant compression candidate for a bonded core; it is not automatically the controlling Fc. Bare compression and post-crush resistance are different quantities. The owner states the lower-of-three qualification in its NFI, and that statement is correct.

[Hexcel Table II]({HEXCEL}) confirms, for CR-III 5056 3/8-1.0, stabilized compression 60 psi typical / 35 psi minimum average and normal compression modulus 15 ksi typical. The separately listed typical crush value is also 35 psi. Its numerical equality to the compression column does not make the properties interchangeable. The table's “min” means a minimum average for a product type. Tests used 0.625 inch thickness. No matching Be-bond or flatwise tensile strength is supplied.

Own unit conversions give 15 ksi = 103421359.3975254 Pa, 60 psi = 413685.4375901016 Pa, 35 psi = 241316.50526089262 Pa, 1 pcf = 16.0184633739601 kg/m³, and 3/8 inch = 9.525 mm. The owner correctly keeps its separate 9.5 mm brief-normalization column.

## Recomputed curves and inverses

For the two specified geometries, a single curve describes Q versus δ/tc. Their absolute amplitudes differ by 30.12/20.21 = 1.49035131123206. Switching the conditional Fc from 60 to 35 psi multiplies every amplitude by 7/12 = 0.583333333333333.

{qtable}
The four Q/face combinations at each strength are:

{table}
The two lead cases at 60 psi are **0.152868766846361 mm** for S-200F at Q=0.371 and **0.0652229064039409 mm** for SR-200 at Q=0.609. At the 35 psi scenario they become **0.0891734473270440 mm** and **0.0380466954022988 mm**. These reproduce the filed values. The table includes the cross-Q cases explicitly, so they cannot be mistaken for each face's lead requirement.

The Q=0.33 inversions also reproduce:

{design_table}
These are correctly tagged PROJECTION by the owner. Algebraically, 0.33/0.82 = 0.402439024390244. The empirical design coefficient does not identify a measured wave amplitude.

`Q-WAVINESS.png` and `Q-WAVINESS.pdf` plot the independently derived curves against δ/tf and δ/cell; `CURVE-DATA.csv` supplies the plotted points. The strength cases are conditional scenarios, not a measured confidence interval.

## Biaxial transfer and the dimpling distinction

The [source wrinkling interaction]({NASA}#page=75) is `Rx³+Ry=1`, with each ratio referred to that direction's uniaxial capacity. For equal capacities and equal applied compression, solve `b³+b=1`. The independent 60-digit solution is

`b = {d['root_60_digit_decimal']}`.

The card uses 0.6823, giving `card-root = -2.7803828019257182e-5` and cubic residual `-6.663623299996146e-5`, as filed. Its relative rounding change is about -0.00407485%. Multiplying the already waviness-adjusted uniaxial stress by this factor does not duplicate the waviness reduction. This algebra does not establish equal directional strengths or validate a curved Be sandwich under pressure.

Intracell dimpling uses a [different source interaction]({NASA}#page=49), `Rx+Ry=1`. Its equal-compression multiplier is 0.5. Applying it to the uniaxial expression `2 Ef/(1-nu²) (tf/s)²`, and using the full pinned upstream geometry with membrane stress `pR/(4tf)`, gives:

| Upstream point | Applied stress MPa | Formal elastic equibiaxial dimpling SF | Filed rounded SF |
|---|---:|---:|---:|
| 021 S-200F | 282.948186824093 | 9.018853684781929 | 9.0 |
| 021b SR-200 | 344.998605253324 | 4.975309121115971 | 4.98 |

The raw printed-minus-derived differences are -0.018853684781929 and +0.004690878884029, both consistent with rounding. These are conditional elastic-model factors, not validated physical failure margins. NASA notes that dimples can develop into wrinkling; [FPL 1810-A]({FPLA}) also relates wrinkles to cell geometry. A small amplitude/cell ratio alone does not show independence. Neither cell size nor the pictured shop bow is a measured critical wavelength.

## Exact prose correction and input precision

The CARD's sentence saying the **lead amplitudes** span 0.0046–0.024 of the cell is mislabeled. The actual lead-only ratios are

`0.006847549228760197 to 0.01604921436707204`.

The endpoints for all four typical-strength rows are

`0.004594587314516719 to 0.02391896767621028`.

The latter round to the printed sentence. Correct its label to all four cases, or use the lead-only endpoints. None of the four underlying rows needs recalculation.

The brief itself requests rounded Q and geometry. Using full pinned upstream values instead gives:

| Point | Full required Q | Full core mm | Conditional 60 psi amplitude mm | Brief minus full amplitude mm |
|---|---:|---:|---:|---:|
| 021 | 0.37068071372338524 | 20.21337638749162 | 0.15313481918912647 | -0.000266052342765333 |
| 021b | 0.6092014443376216 | 30.118230884842855 | 0.06513526466329604 | +0.000087641740644823 |

These differences are -0.1737373278% and +0.1345534421% relative to the full-input amplitudes. They are input-precision effects, not failures of the requested brief-based calculation. In particular, a quoted Q of 0.609 must not be read as the exact 021b SF=1 threshold.

For nonelastic eta, the coefficient relative to the elastic square-root scale is `0.82 sqrt(eta)/(1+0.64 Kdelta)`. Thus a target Q would give

`delta = (tc Fc/Ec) [0.82 sqrt(eta)/Q - 1]/0.64`,

only when the bracket is nonnegative. Even a perfect facing cannot reach the two targets if eta is below 0.204701070791196 or 0.551577929803688 respectively. At an illustrative eta=0.8, the 60 psi amplitudes become 0.123394816285189 and 0.0384630596694614 mm. These are PROJECTION sensitivities, not claims about Be's actual eta. A stress-dependent eta must be treated self-consistently.

## Manufacturing and source audit

The retrieved manufacturer specifications support the quoted magnitudes:

{shop_table}
[Flatiron]({i['flatness_sources'][1]['url']}), [Honylite]({i['flatness_sources'][2]['url']}), [QC Facades]({i['flatness_sources'][3]['url']}) and [Indy]({i['flatness_sources'][4]['url']}) specify different geometry and measurement conditions. The owner's warning that these are not delta is appropriate. The [official SAE record](https://saemobilus.sae.org/standards/ams7902h-beryllium-sheet-plate-98be) confirms scope but not the missing quantitative flatness comparison. The [Hexcel design guide]({DESIGN}) describes telegraphing without a depth.

The [FPL 1810 primary indexed introduction]({FPL}) discusses amplification of Fourier components near the critical wavelength, including nearby components. Its full PDF was not retrieved in this check; the direct request failed. Its bibliography, independently confirmed in CR-1457, lists Norris, Ericksen, March, Smith and Boller. The owner's correction of the brief's Kommers attribution to March as third author is supported. The retrieved FPL 1810-A lists Norris, Boller and Voss.

## Nonblocking findings

{finding_table}
Seven of the owner's eight open NFI topics remain valid qualifications; the author correction is independently verified. Three additional entries distinguish the minimum-average label, the lead-only range and rounded target precision. No finding is a stop gate.

## Record and disposition

`SOURCE-AUDIT.json` records exact source locations, access limits and page images. `INPUTS.json` pins the evidence, copied upstream data and authority. All original files were left unchanged.

The owner's elapsed timer is metadata, not an engineering value that can be independently recreated without executing foreign code. The printed timestamps differ by 0.000275 s; its recorded elapsed timer differs from that by about 0.00000132201 s. Distinct clocks/read points can account for this; no duration discrepancy is asserted.

Work began {d['started_at']}; the independent calculation completed {d['calculated_at']}. Final assembly/end time is in WORK.json. Times are measurements, not limits. The check is complete and will be filed once; no successor job is named.
"""
    (ROOT/"CHECK.md").write_text(check)
    (ROOT/"CARD.md").write_text(f"""# MAINLINE-032 independent check — ESTIMATE / QUESTIONABLE

Unit {UNIT}; order {ORDER}. No certification.

The equations, conditional amplitudes and biaxial arithmetic reproduce. All 236 comparisons pass, including all 155 engineering/Boolean RESULTS scalar leaves and independently reconstructed inherited dimpling factors.

At Fc=60 psi, lead amplitudes are 0.152868766846361 mm (S-200F, Q=0.371) and 0.0652229064039409 mm (SR-200, Q=0.609). At 35 psi: 0.0891734473270440 and 0.0380466954022988 mm.

Fc must be the lowest core-compressive, core-tensile and core-facing-bond strength. Stabilized compression supplies a conditional candidate; Hexcel's 35 psi is a minimum average. Bond/tension data remain missing.

The wrinkling factor is b=0.6823278038280193; waviness already in the uniaxial capacity is not counted twice. Intracell dimpling uses its separate 0.5 interaction factor and reproduces 9.0188536848 and 4.9753091211.

Correct the CARD's lead-only amplitude/cell range to 0.00684754923–0.01604921437. Its printed 0.0046–0.024 spans all four typical-strength cases.

Manufacturing spectra, actual strengths, plasticity and shell transfer remain unvalidated. Ten nonblocking NFI entries record the qualifications and correction. The author correction is verified. CHECK.md contains derivations, sources and exact deltas; Q-WAVINESS.pdf/PNG visualizes the map. Stop and file; no successor job.
""")
    plot()
    print(json.dumps(dict(comparisons=d["comparison_total"],mismatches=d["mismatches"],
                          prose_corrections=len(d["prose_corrections"]),findings=len(nfi),
                          source_audit_rows=len(source_audit))))


if __name__=="__main__":
    main()
