#!/usr/bin/env python3
"""Package MAINLINE-022d; assert completeness before emitting the report."""
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import platform
from zoneinfo import ZoneInfo

os.environ.setdefault("MPLCONFIGDIR", "unpublished-local-ref:25a5423c18537494")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy
import scipy

import scan

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def write_json(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def run():
    saved = json.loads((ROOT / "SCAN.json").read_text())
    sens = json.loads((ROOT / "SENSITIVITIES.json").read_text())
    verification = json.loads((ROOT / "VERIFICATION.json").read_text())
    assert saved["complete"] and sens["complete"] and verification["status"] == "PASS"
    assert len(saved["rows"]) == 64 and verification["optimized_sensitivity_witnesses_checked"] == 112
    rows = saved["rows"]
    index = {r["key"]: r for r in rows}
    assert len(index) == 64
    assert all("film" in r["binding_modes"] for r in rows)
    assert all(h["success"] for r in rows for h in r["search"]["history"]
               if h["method"] == "differential_evolution")
    now = datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")

    def get(branch="cap", grid="equilateral", reserve="5", family="cfrp_zylon", band="in_band"):
        return index["/".join((branch, grid, reserve, family, band))]

    def best(band, grid=None):
        return max((r for r in rows if r["case"]["band"] == band
                    and (grid is None or r["case"]["grid"] == grid)), key=lambda r:r["target_multiplier"])

    overall, screened = best("overall"), best("in_band")
    tri_all, tri_screened = best("overall", "equilateral"), best("in_band", "equilateral")
    out_of_band = sum(not r["passes_member_screen"] for r in rows if r["case"]["band"] == "overall")
    corrected = [
        {"change": "Zylon 0/90", "implemented": "Total gauge carries both plies; each tensile direction gets t_total/2.",
         "status": "DEMONSTRATED arithmetic correction; complete membrane remains PROJECTION"},
        {"change": "Joint multiplier", "implemented": "Each sleeve/wrap end is sized at lambda*N; exact 023 C and lambda² mass enter every trial.",
         "status": "DEMONSTRATED arithmetic correction; adhesive/SiC and structural joint qualifications remain open"},
        {"change": "Tensile bending", "implemented": "Ft=15.586 MPa and amplified opposite-face tension are constraints.",
         "status": "PROJECTION; not a calibrated reliability or allowable claim"},
        {"change": "Continuous gauge", "implemented": "s, r_o, total film gauge and lambda are continuous variables in the final search.",
         "status": "Numerical search completed, not a mathematical global certificate"},
        {"change": "030 screen", "implemented": "Each combination has an overall result and half-wave>=curved-member-length result.",
         "status": "Necessary comparison screen only; no continuum/discrete validation claimed"},
    ]
    result = {
        "schema": 1, "card": "MAINLINE-022d", "unit": UNIT, "order": ORDER,
        "status": "QUESTIONABLE", "certification": False, "created_at": now,
        "qualified_structural_SF": None, "qualified_full_size_compression_allowable_Pa": None,
        "qualified_assembly_failure_probability": None, "primary_combinations": 32, "primary_witnesses": 64,
        "corrections": corrected, "best_overall_numerical_surrogate": overall,
        "best_screened_numerical_surrogate": screened,
        "best_equilateral_overall": tri_all, "best_equilateral_screened": tri_screened,
        "overall_witnesses_failing_member_screen": out_of_band,
        "all_primary_rows": rows, "verification": {k:verification[k] for k in (
            "status", "checks", "max_mass_closure_error_kg", "max_direct_SF_difference",
            "optimized_sensitivity_witnesses_checked")},
        "sensitivity_counts": {k:len(v) for k,v in sens.items() if isinstance(v,list)},
        "elapsed_is_measured_not_a_limit": True,
        "next": "none", "stops_other_work": False,
    }
    write_json("RESULTS.json", result)

    # Flat numerical tables preserve full machine precision.
    flat = []
    for r in rows:
        c, m = r["case"], r["mass_kg"]
        f = {k:c[k] for k in ("branch", "grid", "reserve", "family", "band")}
        f.update({"classification": "QUESTIONABLE", "target_multiplier":r["target_multiplier"],
                  "least_scored_SF":r["SF_least"], "binding_modes":"+".join(r["binding_modes"]),
                  "s_m":r["s_m"], "member_length_m":r["member_length_m"], "half_wave_m":r["half_wave_m"],
                  "half_wave_over_member":r["half_wave_over_member"], "OD_m":2*r["r_o_m"],
                  "wall_m":r["wall_m"], "total_film_m":r["film_total_m"],
                  "nodes":r["nodes"], "members":r["members"],
                  "tension_at_limit_Pa":r["stresses"]["at_limit"]["max_tension_Pa"],
                  "joint_capacity_status":r["joint"]["strength_status"]})
        f.update({"mass_"+k+"_kg":v for k,v in m.items()})
        f.update({"SF_"+k:v for k,v in r["SF"].items()})
        flat.append(f)
    with (ROOT / "TABLES.csv").open("w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(flat[0]))
        writer.writeheader()
        writer.writerows(flat)

    tables = [
        "# MAINLINE-022d — all primary witnesses",
        "",
        "**QUESTIONABLE throughout.** All mass columns are kg. Each row also carries 100 kg systems and "
        "the reserve named above its table. Tube + film + joint + node + systems + reserve + sag lift loss "
        "= 4,889.44215019 kg. Sag is lost buoyancy, not physical hardware mass.",
        "",
        "`overall` is the best numerical witness in the search domain; `screened` additionally requires "
        "030 half-wave / curved member length ≥1 within solver tolerance. This is not proof of a valid continuum mode. "
        "Two-way rows keep 022c's triangular sag surrogate and a common 030 wave screen; their C=4 shear assumption "
        "is unresolved. Square-cell alternatives are in SENSITIVITIES.md.",
        "",
        "Bindings: L=local axial shell; G=smeared global; P=Perry maximum compression; "
        "T=projected tensile bending; F=film. Sleeve/wrap axial and bond capacities also equal the target "
        "by sizing. The two 5% allowance families have UNKNOWN joint capacity.",
        "",
    ]
    mode_short = {"local":"L", "global":"G", "perry":"P", "tension":"T", "film":"F",
                  "compression":"C", "euler":"E"}
    for branch in ("cap", "membrane"):
        for grid in ("equilateral", "two_way"):
            for reserve in ("5", "019"):
                tables += [f"**{branch}; {grid}; reserve {reserve} = {scan.RESERVES[reserve]:.6f} kg**", "",
                    "| Family | Search | Least SF | Binding | s, m | half/L | Tubes | Film | Joints | Nodes | Sag loss |",
                    "|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
                for family in NAMES:
                    for band in ("overall", "in_band"):
                        r = get(branch, grid, reserve, family, band)
                        m = r["mass_kg"]
                        binds = "+".join(mode_short[k] for k in r["binding_modes"])
                        tables.append(
                            f"| {SHORT[family]} | {'screened' if band=='in_band' else band} | {r['SF_least']:.9f} "
                            f"| {binds} | {r['s_m']:.6f} | {r['half_wave_over_member']:.6f} "
                            f"| {m['tube']:.6f} | {m['film']:.6f} | {m['joint']:.6f} | {m['nodes']:.6f} | {m['sag_lift_loss']:.6f} |")
                tables.append("")
    (ROOT / "TABLES.md").write_text("\n".join(tables) + "\n")

    methods = r"""# MAINLINE-022d — model and source ledger

Every result is **QUESTIONABLE**. Unvalidated material and geometry transfers are **PROJECTION**.
The source snapshots and their supplied hashes are in INPUT-PINS.json. Existing owner scripts were read
as evidence and never imported or executed. scan.py, sensitivities.py and verify.py belong to this seat.

**Scope and inherited contracts**

The requested primary matrix is 2 sag branches × 2 grids × 2 reserves × 4 film/joint families.
Each has an unconstrained numerical optimum and an optimum satisfying the specified half-wave screen.
The source is the pinned 022c SAG.json, with 023, 024, the completed 025 work, the independent 022b/022c
check and 030's CONTINUUM.json. The order itself is snapshotted as inputs/ORDER.json.

R=10 m, p=95,460.8379139 Pa, buoyancy mass=4,889.44215019 kg, E=410 GPa,
SiC density=3,100 kg/m³, systems=100 kg and each nominal node=0.02 kg.
Reserve is 244.4721075095 kg (5%) or 411.2989440716474 kg (019's inherited fixed reserve).
The 019 reserve is not recomputed as a new equipment design.

| Family | Film density, kg/m³ | Directional stress used with total gauge | Total gauge floor | Joint rule | SiC Fc |
|---|---:|---:|---:|---|---:|
| Projected film | 970 | 1.5 GPa | 80 µm | 5% of tube+film+nodes | 3.9 GPa |
| Mylar | 1400 | 22 ksi = 151.684660450 MPa | 12.192 µm | same 5% rule | 380 MPa |
| Kapton/Ti | 1420 | 231×0.5 =115.5 MPa | 25 µm | sized Ti sleeve | 3.9 GPa |
| Zylon/CFRP | 1560 | (5800×0.6)/2 =1740 MPa | 12 µm | sized CFRP wrap | 3.9 GPa |

Zylon's scalar 1740 MPa is only a bookkeeping equivalent: total gauge t comprises two t/2 plies,
each checked against the assumed fiber stress 3480 MPa. All total ply mass is charged.
The 12 µm inherited floor is not a sourced membrane specification; it is inactive at all reported points.
None of the four continuous gauge floors is active. Arbitrary thick, seamless film supply is not established.
Mylar's 380 MPa is an inherited flexural proxy, not a qualified compression allowable.
The 3.9 GPa input is also not a full-size arc allowable. Actual qualified values remain null.

**Geometry and force**

s is chord/node spacing, L=2R asin(s/(2R)) the member arc length, and S=4πR².
Equilateral: faces=S/(√3 s²/4), members=1.5 faces, nodes=0.5 faces+2,
N=pRs/(2√3), global coefficient C=4√(3/2).
Two-way: faces=S/s², members=2 faces=2 nodes−4, nodes=faces+2,
N=pRs/2 and inherited C=4. These are continuous lattice counts, not an integer mesh.
An unbraced two-way grid lacks the in-plane shear stiffness assumed by its scalar global surrogate
(NFI-030-TWO-WAY). No computed two-way multiplier establishes a physical frame capacity.

**Sag**

Curvature radius ρ=s is retained. The cap branch uses a circular cap over the triangle inradius
b=s/(2√3): h=ρ−√(ρ²−b²), mean=h²(ρ−h/3)/b². This is a circular-cap approximation.
For an equal-tension, small-slope equilateral membrane, −∇²w=2/ρ and zero edge displacement:
w=(3s²/(2ρ)) b1 b2 b3 in barycentric coordinates. The mean of b1 b2 b3 is 1/60,
so the **exact mean within that linear membrane model** is s²/(40ρ).
At ρ=s this is 1.1660029709329 times the chosen cap mean. It does not claim an exact nonlinear
stressed membrane, measured shape or gas-barrier assembly.
Lost lift is 3×buoyancy mass×mean/R, the inherited first-order volume correction.
Film mass uses S and omits extra sagged area, seams and separate barrier coatings.

For the primary two-way comparison, both sag laws are retained literally from 022c, and the
triangular-to-square transfer is flagged. A separate 32-witness sensitivity uses square inradius s/2
for the cap and the exact linear square membrane mean 0.0702885074776 s²/ρ.
The latter follows either a double sine series or an independently checked single series.
This choice changes more than the five requested corrections and is therefore separately identified.

**Coupled mass and joint sizing**

At each candidate (s,r_o,t_film,λ), film mass is Sρ_f t_film and node mass is 0.02×nodes.
Available structural mass is buoyancy−reserve−sag loss−systems.
For 5% joints: assembly=available/1.05, M_joint=0.05 assembly,
M_tube=assembly−M_film−M_nodes. This is an allowance; there is no joint strength law for these two families.

For a sized end at its own load λN:
A_joint=λN/σ_joint, overlap=λN/(2πr_o τ), m_end=ρ_joint A_joint overlap,
and M_joint=2×members×m_end is removed before finding tube area.
Thus m_end=C_joint(λN)²/r_o, not C_joint N²/r_o.
Using 023's unrounded inputs:
Ti: density 4430, axial 827 MPa; CFRP: density 1550, compression 1470 MPa;
both use adhesive shear 28.9 MPa. C_Ti=2.949989740284e−14 and
C_CFRP=5.806797113962e−15 kg·m/N².
The adhesive result was measured on aluminum adherends; transfer to SiC is unqualified.
No adhesive layer, peel, moment stiffness, sleeve buckling or end load spreading mass is added by this law.
Both sized capacities equal λ by construction, with no additional joint reserve.
For λ<1, the computed joint is sized below operating load; that row is a failed design, not a
demonstration at full pressure. This explains why resizing sub-unity Kapton/Ti cases can raise
their numerical optimum relative to joints sized at N.

**Section and modes**

A=M_tube/(3100×members×L), r_i=√(r_o²−A/π), t=r_o−r_i,
I=π(r_o⁴−r_i⁴)/4. Invalid annuli and nonpositive tube budgets are excluded.
The separately scored linear load factors are:
compression Fc A/N; Euler N_E/N with N_E=π²EI/L²;
local [γ×0.6Et/r_o]A/N, γ=0.099+0.901 exp[−√(r_o/t)/16];
film 2σ_effective t_film/(ps); global 0.2 C E√(IA)/(sR²p).
The local correlation is inherited from NASA SP-8007 Rev.2, printed pp.23–25,
equations 9–10; application to long, curved ceramic members remains unqualified.
Primary source: https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf

Initial bow e=L/1000. At load qN below Euler:
M=qNe/(1−qN/N_E), σ_c=qN/A+Mr_o/I,
σ_t=max(0,Mr_o/I−qN/A). Perry limits σ_c≤Fc.
The added tensile constraint is σ_t≤15.586 MPa, explicitly **PROJECTION**.
That number is the rounded, deliberately hypothetical 025 m=10 full-volume screen
at a specified reference assembly and assumed probability; it is held fixed here to reproduce
the previous check's sensitivity. It is not recalibrated for each optimized tube volume and
does not establish an actual failure probability. 0, 7.192 and 380 MPa alternatives are reported.
No finite elastic stress is reported past the Euler pole.
Taking the minimum of modes does not validate coupled shell/column/bending instability.

**Half-wave and search**

030 uses D/Y=(9/8)I/A for the equilateral smear. Its half-wave is
ℓ=π[(9/8)(I/A)R²]^(1/4)=π√(√(9/8) r_g R), r_g=√(I/A).
The primary additional condition is ℓ≥L, the actual curved member length.
Both ℓ/L and 030's original ℓ/s are recorded. A pass at one member is only the requested
minimum screen; homogenization ordinarily needs multiple cells and remains unresolved.
The same 030 expression is shown on primary two-way diagnostic rows for comparison,
without claiming it is a validated two-way wave.
The square-cell sensitivity uses D/Y=I/A, consistent with the inherited scalar C=4 closure;
it still supplies no missing two-way shear stiffness.

Primary bounds: 0.4≤s≤8 m, 0.003≤r_o≤min(0.25,s/3) m, 0.001≤λ≤5,
and continuous total film gauge between the inherited floor and the mass-only upper bound.
The objective maximizes λ subject to every strength, mass, section and optional half-wave constraint.
An initial three-variable search selects the minimum film needed at λ; the final
four-variable differential-evolution search frees film gauge, followed by multiple SLSQP refinements.
All 64 four-variable global-search runs terminate successfully. Multiple starts and the initial
witnesses agree in load factor. This is numerical evidence, not a proof of the mathematical global optimum.
No primary spacing/radius bound is active. Sixteen cap/5% cases were additionally searched over
0.15≤s≤19.9 m and 0.001≤r_o≤min(1,s/3) m; none improved beyond numerical tolerance.
Bindings are modes within 2e−6 of the optimized multiplier. Accepted feasibility uses 2e−9
absolute load-factor tolerance; the independent verification uses 3e−9. Boundary ratios are
therefore interpreted at numerical precision, not as manufactured tolerances.

verify.py independently reconstructs annulus masses, member forces, D and Y, direct
Euler-magnified moments, compression/tension roots, directional film loading and joint
area/overlap capacities. It reproduces 030's seven published half-waves, verifies both sag
integrals and the source snapshots, and checks all 112 optimized sensitivity witnesses.
The comparison is numerical/model evidence only.

Reproduce: run scan.py, sensitivities.py, verify.py, then assemble.py in this folder.
SEED-SCAN.json preserves the initial three-variable starting witnesses. The final search
does not rely on executing another seat's programs. No external seat, supplier or shared runtime
file was written by this work. The order is completed by its queue report; no next job is named.
"""
    (ROOT / "METHOD.md").write_text(methods)

    # Retain unresolved issues with exact links to the earlier records.
    issues = [
        ("FILM", ["NFI-C022-ZYLON-DIRECTION"],
         "The doubled directional mass is corrected in this model; a complete 0/90 Zylon membrane with a barrier, seams, biaxial/creep allowables and this gauge is still unsourced. The 1.5 GPa film is also PROJECTION.",
         "Qualify a complete membrane and its full mass, durability and boundary load transfer."),
        ("JOINT", ["NFI-C022-JOINT-MULTIPLIER", "NFI-C022-DISCRETE-JOINTS"],
         "023 axial/bond dimensions now use each candidate's lambda and their lambda-squared mass. SiC adhesion, peel, moment transfer, local bearing, sleeve stability and adhesive mass remain unknown. Percent joints have no scored capacity.",
         "Use qualified end-joint stiffness/capacity and complete mass in the discrete structure."),
        ("TENSION", ["NFI-C022-TENSILE-BENDING", "MAINLINE-025"],
         "Amplified tensile bending is screened at assumed Ft=15.586 MPa. This fixed reference-volume ceiling is PROJECTION, not a full-stress-field weakest-link model or measured allowable. Eight overall equilateral witnesses bind it; no screened optimum has tensile stress at its target.",
         "Calibrate full-size tensile surface/volume populations with the actual stress field and end-contact demands."),
        ("CONTINUUM", ["NFI-030-CONTINUUM", "NFI-030-P3-INBAND", "NFI-C022-DISCRETE-JOINTS"],
         "Sixteen overall optima fail half-wave>=arc length. Their screened alternatives are filed, but a wavelength of exactly one member does not establish homogenization, an integer mesh or discrete stability.",
         "Analyze an explicit imperfect curved frame and actual node rotational stiffness."),
        ("TWO-WAY", ["NFI-030-TWO-WAY"],
         "The unbraced two-way lattice has no demonstrated in-plane shear stiffness supporting inherited C=4. Primary half-wave and triangular-sag transfers are diagnostic only. Square-cell sensitivity does not repair shear.",
         "Supply bracing and its mass or solve the actual frame and identify its shear/global modes."),
        ("SAG", ["NFI-C022-SAG-GEOMETRY"],
         "The exact equilateral mean is now derived for the linear constant-tension membrane. Cap is a circular surrogate; nonlinear shape, extra membrane area and loaded edge movement remain open. Primary two-way rows intentionally preserve 022c's geometry; square-cell alternatives are separate.",
         "Close actual cell shape, tension distribution, loaded volume and film area consistently for each lattice."),
        ("ALLOWABLE", ["NFI-C022-ALLOWABLE", "MAINLINE-025"],
         "Neither 3900 MPa bulk crush nor 380 MPa flexure is a qualified full-size curved SiC compression allowable. No qualified assembly failure probability is known.",
         "Use process/size-specific compression and failure data; keep qualified allowable and failure probability null."),
        ("INTERACTION", ["NFI-C022-LOCAL-INTERACTION"],
         "Separate local, Euler and Perry/tension minima leave shell-column-curvature interaction unresolved. The optional magnified-local diagnostic is not a validated law and is excluded from the primary least SF.",
         "Resolve coupled instability with a justified theory or calibrated nonlinear model."),
        ("MANUFACTURE", ["NFI-C022-MANUFACTURE", "MAINLINE-025"],
         "No complete diameter, wall, arc length, curvature and tolerance combination is production-qualified by this scan. Continuous film and fractional node counts are optimization surrogates.",
         "Carry the full geometry, tolerance and process specification into fabrication evidence and full-size tests."),
        ("MASS", ["MAINLINE-023", "MAINLINE-024", "MAINLINE-025"],
         "The inherited mass contract omits independent barrier/seam/coating and some joint process masses; sag volume is first-order. Two reserve choices are carried assumptions, not an audited vehicle budget.",
         "Close complete operating hardware, membrane and joint masses against measured loaded volume."),
        ("SEARCH", ["NFI-C022-SEARCH-RESOLUTION"],
         "The 12-film-gauge discretization is removed. Continuous DE, constrained refinements, independent residual checks and 16 expanded-domain cases agree, but no mathematical global certificate is claimed.",
         "Preserve source-pinned witnesses and reoptimize when qualified physics or mass inputs change."),
    ]
    nfi = {"schema":1, "unit":UNIT, "status":"QUESTIONABLE", "stops_work":False,
           "card_work_complete":True, "rows":[
               {"id":"NFI-022D-"+id, "status":"OPEN", "classification":"QUESTIONABLE; unvalidated transfers PROJECTION",
                "source_rows":sources, "finding":finding, "next":next_action}
               for id,sources,finding,next_action in issues]}
    write_json("NFI.json", nfi)

    write_json("INPUTS.json", {
        "schema":1, "unit":UNIT, "classification":"QUESTIONABLE", "authority":ORDER,
        "snapshot_pins":"INPUT-PINS.json", "methods":"METHOD.md", "corrections":corrected,
        "constant_Ft_projection_Pa":scan.FT, "qualified_compression_allowable_Pa":None,
        "qualified_failure_probability":None, "R_m":scan.R, "p_Pa":scan.P, "lift_kg":scan.LIFT,
        "systems_kg":scan.SYSTEMS, "node_kg":scan.NODE, "reserves_kg":scan.RESERVES,
        "film_inputs_density_effective_strength_total_floor":scan.FILMS,
        "joint_inputs_density_axial_bond":scan.JOINTS, "families":scan.FAMILIES,
        "wave_primary":"030 triangle expression, evaluated on both diagnostic grids; threshold uses arc length",
        "two_way_primary_sag":"Inherited 022c triangular surrogate; square-cell alternatives separately reported",
        "two_way_square_sensitivity_mean_coefficient":verification["square_membrane_mean_coefficient"],
        "software":{"python":platform.python_version(), "numpy":numpy.__version__,
                    "scipy":scipy.__version__, "matplotlib":matplotlib.__version__},
        "reproduction":["scan.py","sensitivities.py","verify.py","assemble.py"],
    })

    # Compact sensitivity tables identify the altered assumptions.
    sensitivity_text = [
        "# MAINLINE-022d — assumption sensitivities", "", "**QUESTIONABLE. All alternatives are PROJECTION.**", "",
        "Square-cell alternatives use square inradius for the cap or the exact linear square membrane mean, "
        "and the scalar two-way D/Y=I/A half-wave. They remain unvalidated for the shear-free lattice.", "",
        "| Branch | Reserve | Family | Overall SF | Screened SF | Screened s, m |",
        "|---|---|---|---:|---:|---:|",
    ]
    square_index = {x["primary_key"]:x["result"] for x in sens["two_way_square_cell"]}
    for branch in ("cap","membrane"):
        for reserve in ("5","019"):
            for family in NAMES:
                a = square_index[f"{branch}/two_way/{reserve}/{family}/overall"]
                b = square_index[f"{branch}/two_way/{reserve}/{family}/in_band"]
                sensitivity_text.append(f"| {branch} | {reserve} | {SHORT[family]} | {a['SF_least']:.9f} | "
                                        f"{b['SF_least']:.9f} | {b['s_m']:.6f} |")
    sensitivity_text += ["", "Tensile ceiling alternatives below show cap/5% equilateral results. "
                         "All 48 optimized tensile alternatives, including membrane and 019, are in SENSITIVITIES.json.", "",
                         "| Family | Search | Ft, MPa | Least SF | s, m |",
                         "|---|---|---:|---:|---:|"]
    for alt in sens["tensile_projection"]:
        if not alt["primary_key"].startswith("cap/equilateral/5/"):
            continue
        r = alt["result"]
        sensitivity_text.append(f"| {SHORT[r['case']['family']]} | {r['case']['band']} | "
                                f"{alt['Ft_projection_Pa']/1e6:.3f} | {r['SF_least']:.9f} | {r['s_m']:.6f} |")
    expanded_delta = max(abs(x["change_SF"]) for x in sens["expanded_search"])
    spacing_delta = max(x["change_SF"] for x in sens["spacing_instead_of_arc_screen"])
    sensitivity_text += ["",
        f"Expanded spacing/radius bounds leave all 16 cap/5% optima unchanged within {expanded_delta:.3g} SF. "
        f"Using chord spacing instead of the longer arc in the 16 active screens raises SF by at most {spacing_delta:.9f}.",
        "",
        "The separate magnified-local diagnostic applies the axial shell threshold to the amplified maximum "
        "compression face at fixed primary geometry. It is **not a validated interaction rule** and is not substituted "
        "into the main results.", "",
        "| Primary key | Primary SF | Unvalidated diagnostic multiplier |",
        "|---|---:|---:|"]
    for alt in sens["unvalidated_local_bending_diagnostic"]:
        sensitivity_text.append(f"| {alt['primary_key']} | {alt['primary_SF']:.9f} | {alt['diagnostic_multiplier']:.9f} |")
    (ROOT/"SENSITIVITIES.md").write_text("\n".join(sensitivity_text)+"\n")

    cap5, cap019 = get(), get(reserve="019")
    mem5, mem019 = get(branch="membrane"), get(branch="membrane", reserve="019")
    sq = square_index["cap/two_way/5/projection/in_band"]
    tri_table = [
        "| Family | Reserve | Cap overall | Cap screened | Membrane overall | Membrane screened |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for family in NAMES:
        for reserve in ("5","019"):
            vals = [get(b,"equilateral",reserve,family,m)["SF_least"]
                    for b,m in (("cap","overall"),("cap","in_band"),("membrane","overall"),("membrane","in_band"))]
            tri_table.append(f"| {SHORT[family]} | {reserve} | "+" | ".join(f"{v:.6f}" for v in vals)+" |")
    mass = tri_screened["mass_kg"]
    card = f"""# MAINLINE-022d — corrected P3 scan

**QUESTIONABLE throughout.** Completed all 32 branch/grid/reserve/family combinations, with 64 primary numerical
witnesses. Both Zylon plies, each sleeve/wrap's own load multiplier and joint mass, projected tensile bending,
continuous film gauge and the requested half-wave screen are included. These are conditional calculations;
qualified full-structure SF, compression allowable and assembly failure probability remain unknown.

The **best equilateral overall** witness is Zylon 0/90/CFRP, cap, 5% reserve:
SF **{tri_all['SF_least']:.9f}**, s={tri_all['s_m']:.6f} m, half-wave/member={tri_all['half_wave_over_member']:.6f}.
It fails the half-wave screen. The **best equilateral screened** witness is the same family at
SF **{tri_screened['SF_least']:.9f}**, s={tri_screened['s_m']:.6f} m and arc length={tri_screened['member_length_m']:.6f} m;
half-wave equals one member at numerical precision. Local shell, smeared global and film capacities bind;
the assumed sleeve/wrap axial and bond capacities equal the target by sizing. The tensile demand is zero.
This single-member boundary is the requested minimum screen, not a validated continuum limit.

Across the full inherited surrogate matrix, the largest numerical values occur in the **two-way projected-film**
cap/5% family: overall **{overall['SF_least']:.9f}** at s={overall['s_m']:.6f} m,
and screened **{screened['SF_least']:.9f}** at s={screened['s_m']:.6f} m.
These cannot establish a real frame capacity: NFI-030-TWO-WAY identifies absent in-plane shear stiffness
behind the inherited C=4 coefficient. The 5% joint allowance also has no capacity model.
Both grids' full rows are retained, with this qualification attached.

**Each equilateral family's least modeled SF**

{chr(10).join(tri_table)}

Reserve 5 is 244.472108 kg; reserve 019 is 411.298944 kg. Both also carry 100 kg systems.
Mylar uses the inherited Fc=380 MPa proxy; all other families use Fc=3900 MPa, each unqualified for the full arc.
The two lower-strength film families' overall optima already pass the screen.
Sixteen of the 32 overall optima fail it. Film is a binding mode at every continuous optimum.

[TABLES.md](TABLES.md) gives **all 64 least factors, binding modes, spacings and complete mass rows**;
[TABLES.csv](TABLES.csv) adds full-precision dimensions, stresses and individual modes.
The best equilateral screened cap/5% point closes as:
tubes {mass['tube']:.6f}, film {mass['film']:.6f}, joints {mass['joint']:.6f}, nodes {mass['nodes']:.6f},
systems 100, reserve {mass['reserve']:.6f}, sag lift loss {mass['sag_lift_loss']:.6f} kg,
summing to 4,889.44215019 kg. Its OD is {2000*tri_screened['r_o_m']:.6f} mm,
wall {1000*tri_screened['wall_m']:.6f} mm and total 0/90 gauge {1e6*tri_screened['film_total_m']:.6f} µm.
Each directional ply gets half that gauge. Membrane sag reduces this family's screened SF to
{mem5['SF_least']:.9f} at 5% reserve and {mem019['SF_least']:.9f} at 019 reserve.

**What changed and what remains assumed**

Zylon now uses 024's two-direction contract, equivalent to 1.74 GPa acting on total gauge.
For every sleeve/wrap trial, end area=λN/σ and overlap=λN/(2πrτ);
the resulting mass is charged before closing tube area. Thus joint mass scales as λ² at fixed geometry.
The two percentage-joint families retain 022c's 5% of tube+film+nodes rule and UNKNOWN joint capacity.
Sub-unity Kapton/Ti rows size joints below operating load, as the order's candidate-multiplier rule requires;
their improved numerical result remains a failure at pressure multiplier one.

The added ceiling Ft=15.586 MPa is the prior check's fixed **PROJECTION** screen, not a measured allowable
or a size-corrected assembly reliability claim. Initial bow is L/1000, with Euler-amplified bending and an
explicit opposite-face tensile check. All eight screened equilateral projected-film/Zylon witnesses
remain unchanged across 24 alternatives with ceilings of 0, 7.192 or 380 MPa: their limit has no tensile stress.
Separate local/column/bending interaction remains open.

The equilateral membrane mean is exactly s²/(40ρ) **within the linear constant-tension membrane model**,
with ρ=s, giving 1.166002970933 times 024's circular-cap mean.
Primary two-way rows preserve 022c's triangular sag surrogate and evaluate the common 030 wave expression.
The separately filed square-cell/D-over-Y sensitivity lowers the two-way cap/5% projected-film screened
value to **{sq['SF_least']:.9f}**. It does not supply the missing shear stiffness.
Using arc length rather than chord spacing for the screen is slightly stricter; the largest difference
in the 16 active comparisons is {spacing_delta:.9f} SF.

**Verification and evidence**

All 64 final four-variable differential-evolution searches terminated successfully and were refined
with constrained multiple starts. Opening spacing/radius bounds in 16 cap/5% cases improved nothing beyond
{expanded_delta:.3g} SF. They are best numerical witnesses, not certified mathematical global optima.
Independent reconstruction passed **{verification['checks']:,} checks**, including 112 optimized sensitivity
witnesses, direct force/moment capacities, both membrane integrations, all seven 030 source half-waves
and source pins. Maximum primary mass-closure error is {verification['max_mass_closure_error_kg']:.3g} kg.
No owner script was executed.

[METHOD.md](METHOD.md) contains the equations, inputs and source ledger;
[SENSITIVITIES.md](SENSITIVITIES.md) separates the altered assumptions;
[NFI.json](NFI.json) keeps eleven open qualification issues linked to the prior records.
No sourced complete high-strength membrane, full-size ceramic arc allowable, discrete frame stability,
complete joint qualification or manufacturing specification is established.
Work is complete under {ORDER}; no successor job is named. Times are measurements only.
"""
    (ROOT / "CARD.md").write_text(card)

    # Standalone research figure for the meaningful equilateral comparison.
    plt.rcParams.update({"font.size":10, "axes.spines.top":False, "axes.spines.right":False,
                         "svg.fonttype":"none"})
    fig, axes = plt.subplots(1,2,figsize=(11.5,4.7),sharey=True)
    colors = {"cap":"#165a91", "membrane":"#bd6222"}
    for ax,reserve in zip(axes,("5","019")):
        for i,family in enumerate(NAMES):
            for branch,dy in (("cap",.10),("membrane",-.10)):
                a=get(branch,"equilateral",reserve,family,"overall")["SF_least"]
                b=get(branch,"equilateral",reserve,family,"in_band")["SF_least"]
                y=3-i+dy
                ax.plot([b,a],[y,y],color=colors[branch],linewidth=2)
                ax.scatter([a],[y],facecolors="white",edgecolors=colors[branch],s=52,zorder=3)
                ax.scatter([b],[y],color=colors[branch],s=22,zorder=4)
        ax.axvline(1,color="#686868",linestyle="--",linewidth=1)
        ax.set(xlim=(.3,1.5),ylim=(-.4,3.45),xlabel="Least modeled load multiplier",
               title=f"{'5%' if reserve=='5' else '019'} reserve")
        ax.grid(axis="x",alpha=.15)
        ax.set_yticks(range(4),[SHORT[x] for x in reversed(NAMES)])
    handles=[
        Line2D([0],[0],color=colors["cap"],lw=2,label="Cap sag"),
        Line2D([0],[0],color=colors["membrane"],lw=2,label="Membrane sag"),
        Line2D([0],[0],marker="o",color="none",markeredgecolor="#333",markerfacecolor="white",label="Overall"),
        Line2D([0],[0],marker="o",color="none",markerfacecolor="#333",markeredgecolor="#333",label="Half-wave ≥ member"),
    ]
    fig.legend(handles=handles,loc="lower center",ncol=4,bbox_to_anchor=(.56,.02),frameon=False)
    fig.suptitle("Equilateral P3 surrogate — QUESTIONABLE",x=.57,y=.98,fontsize=14)
    fig.text(.57,.91,"Ft = 15.586 MPa is PROJECTION; passing the screen does not validate the structure.",
             ha="center",fontsize=9)
    fig.subplots_adjust(left=.20,right=.98,bottom=.23,top=.78,wspace=.12)
    fig.savefig(ROOT/"COMPARISON.svg")
    fig.savefig(ROOT/"COMPARISON.png",dpi=160)
    plt.close(fig)

    # Pin the delivered package only after all outputs are final.
    artifacts=[]
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.name=="MANIFEST.json" and p.parent==ROOT or "__pycache__" in p.parts:
            continue
        b=p.read_bytes()
        artifacts.append({"path":str(p),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
    write_json("MANIFEST.json", {"schema":1,"unit":UNIT,"created_at":now,
                                "scope":"All delivered calculations, source snapshots and reports; excludes this root manifest and caches",
                                "artifacts":artifacts})
    print(json.dumps({"unit":UNIT,"artifacts":len(artifacts),"checks":verification["checks"],
                      "primary_rows":len(rows),"nfi_rows":len(issues),
                      "best_equilateral_overall_SF":tri_all["SF_least"],
                      "best_equilateral_screened_SF":tri_screened["SF_least"],
                      "created_at":now},indent=2))


if __name__ == "__main__":
    run()
