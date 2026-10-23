**MAINLINE-028 — Joining the Be sandwich sphere. ESTIMATE.**

The lightest modeled combination is **39.49 kg at the published stock envelope, or 24.54 kg at 4 m**, using an 8 g/m² laboratory edge deposit and a zero-added-filler electron-beam seam with full parent compressive strength. That is **PROJECTION**, not an established load-carrying joint. A less metallurgically demanding adhesive-scarf projection gives **50.28 / 26.81 kg**. No source examined establishes the required thin-Be/low-density-Al-core bond and seam together, so **the lightest qualified joining mass and overall installed-hull SF remain UNKNOWN**.

The commercial-film/scarf calculation is much tighter: **214.24 / 190.76 kg** with nominal AF 163-2U at 0.015 lb/ft². At the stock envelope, only **2.19 kg** remains for all uncounted primers, closeouts, intersections and repairs. Adding an assumed 5 g/m² primer makes it **226.81 kg**. The eight numerical checks pass and input pins were separately verified; material inputs are **QUESTIONABLE**, and every proposed hull joint is **PROJECTION**.

**1. The point and the load.** This uses the pinned **MAINLINE-021 rev1**, which replaces its initial filing: E = 290 GPa, Be faces 0.843448 mm, CR-III 5056 3/8-1.0 core 20.213376 mm, R = 10 m. Joining replaces the **216.427 kg** allowance. Both faces together carry **477.304 kN/m**, each face **238.652 kN/m**, at **282.948 MPa compression**. The ideal symmetric membrane solution has **47.730 kPa radial compression** through the core and zero interface shear/tension. Those zeros are not design maxima: wrinkles, disbonds, seams and thermal mismatch generate the missing bond loads. The source pins and own equations are in [INPUTS.json](527a0f9fbf0b0809-INPUTS.json), [METHOD.md](579bff2ee5f7661a-METHOD.md) and [calculate.py](3624252d7cbe952e-calculate.py).

**2. Face-to-core adhesive routes.** Weights below are **per square metre of projected panel area, per bond line**; the sphere has two lines. A reported lap-shear strength is not a core-shear or flatwise allowable.

| Route; all material data QUESTIONABLE | kg/m²/line | Both lines, kg | Flatwise tension | Core-shear strength of this Be/core bond | Evidence state |
|---|---:|---:|---|---|---|
| AF 163-2U, 0.015 lb/ft², reticulated | 0.073236 | 184.06 | Not reported at this weight | Unknown | Product exists; hull transfer PROJECTION |
| HexBond 312, 70 g/m² | 0.070000 | 175.93 | Blank in this weight's table column | Unknown | Product exists; hull transfer PROJECTION |
| HexBond 312, 100 g/m² | 0.100000 | 251.33 | 5.4 MPa, aluminium coupon | Unknown | Tested product; different skins/core |
| AF 163-2U, 0.030 lb/ft² | 0.146473 | 368.13 | 5.52 MPa at 75°F; 3.45 MPa at 180°F | Unknown | Tested product; different skins/core |
| Selective cell-edge fillet deposition | 0.008–0.080 | 20.11–201.06 | Not supplied as a structural allowable | Not supplied | In the lab; Be/Al transfer PROJECTION |

[3M's data sheet](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf), pp. 1 and 8, supports reticulation and the separate weight/test entries. Its ±0.005 lb/ft² weight tolerance puts nominal 0.015 film at **122.71–245.42 kg**, before seams. Reticulation moves resin onto the edges; it does not justify multiplying the purchased film weight by the core's solid fraction. Resin deliberately removed must be weighed.

[Hexcel's 312 sheet](https://www.hexcel.com/wp-content/uploads/2025/12/HexBond_312_DataSheet_eu.pdf), p. 2, reports **37 MPa aluminium lap shear at 70 g/m²**, but its **5.4 MPa flatwise result belongs to 100 g/m²**, not 70. Both manufacturers used much different aluminium sandwich specimens; neither result qualifies the proposed Be sandwich.

[Rion, Leterrier and Månson (2008)](https://infoscience.epfl.ch/server/api/core/bitstreams/28b8cc7a-f046-4da3-9fcc-5d5ad3c52a9d/content), DOI 10.1016/j.compositesa.2008.05.022, demonstrates **8–80 g/m²** deposited on cell edges in CFRP/Nomex experiments. This establishes a low-mass deposition route, not adequate strength at 8 g/m². **20 g/m²** is also carried as a less aggressive projection; it gives 50.27 kg for both bonds.

**3. What the bond must preserve.** The selected core's typical plate-shear strengths are **0.379 MPa L / 0.241 MPa W**; minimum-average entries are **0.310 / 0.172 MPa**, from [Hexcel Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf). These are useful bond-test targets to avoid introducing a weaker plane, not calculated in-service interface demand. For scale only, the local linear screen \(q=E_c\delta/d,\;\tau=G_c\Delta u/d\) gives **0.512 MPa normal / 0.232 MPa shear** for separate 0.10 mm relative displacements. Thus the 5.4 MPa coupon result exceeds that illustrative normal demand by 10.6×; its transfer to this core remains unproven. Neither the wrinkle coefficient nor the crimp SF specifies the displacement amplitude or a peel allowable. A measured installed stiffness, cohesive strength and defect limit are required together. A centimetre-scale global dimple is not this local relative displacement.

**4. Brazed, diffusion-bonded and adhesive-free core routes.** Materion documents Be adhesive, brazing, electron-beam and diffusion-joining processes, but supplies no mass/flatwise/core-shear tuple for Be on this 16 kg/m³ Al honeycomb. [Design guide, pp. 13–14](https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74). A **PROJECTION** using two triangular Al-density fillets along each cell wall gives **5.67 / 22.68 g/m² per line** for 0.10 / 0.20 mm fillet legs, or **14.25 / 56.99 kg** total. A continuous assumed 50 µm filler layer instead costs **339.29 kg**. These are geometric filler inventories, not demonstrated bonds.

Diffusion bonding has zero *added filler* as its lower limit; actual interface layers, altered core and processing stock are unknown. The current CR-III core has an organometallic coating and an H-39 temper; its heat-exposure evidence does not qualify a brazing cycle. A bare or welded replacement core needs new properties and mass. Integral Be/lattice manufacture is likewise **PROJECTION**: eliminating a separate bond does not retain the existing core's mass and stiffness for free. Flatwise and core-shear strengths for these specific routes are **UNKNOWN**.

**5. Seams.** The following masses count **both face seams per metre of coincident hull seam**. The shared allowance for core splicing/sealing is **0.007053 kg/m**: a projected 0.5 mm gap filled at 500 kg/m³ plus 0.002 kg/m sealant. Extra blocks, repairs and primer are not included in that allowance.

| Seam geometry, all PROJECTION | Face-joint addition, kg/m | Including core splice/seal, kg/m | Load screen |
|---|---:|---:|---|
| Bonded 30:1 scarf, 70 g/m² seam film | 0.003544 | 0.010598 | 25.30 mm overlap; average shear 9.42 MPa, normal compression 0.314 MPa |
| Be butt strap, 47.73 mm total width per face | 0.155637 | 0.162691 | 23.87 mm overlap on each side; average shear 10 MPa; strip itself carries face load |
| Al-Si brazed 3:1 scarf, assumed 50 µm gap | 0.000720 | 0.007773 | Average shear 84.88 MPa |
| Full-penetration autogenous EB butt seam | 0 added filler | 0.007053 | Requires 282.95 MPa joint compression at the original gauge |

The adhesive scarf uses an owner-selected **10 MPa average-shear screen**, not a qualified allowable. Hexcel documents scarf joint principles in its [bonding guide](https://www.hexcel.com/wp-content/uploads/2026/01/Adhesive_Bonding_Technology.pdf). Coupon strengths for different systems cannot be combined into a new product qualification. A single butt strap additionally has eccentric load/peel and local buckling issues; symmetric details could add mass.

Materion's guide gives **103.4 MPa average shear for Al-Si braze**, which clears the 3:1 scarf's *average* shear calculation by 1.22×; actual gauge, compression, edge peel and fatigue remain open. [NASA's Be joining programme](https://ntrs.nasa.gov/api/citations/19690025590/downloads/19690025590.pdf), pp. 11–21, found strong adhesive double-lap coupons but several weaker brazed designs. Thick Be/steel tensile tests do not establish these thin Be/Be seams.

For EB, the original face has only **0.0183% compression reserve**: required retained strength is **99.9817%**. Materion limits its positive EB description to less structurally demanding assemblies. No matching thin-sheet compression/imperfection evidence was found. At an explicitly assumed **80%** weld retention, even the light joining route reoptimizes to only **SF 0.853 / 0.856**. Whole-sphere closure, weld access, heat effects on adjacent bonds, distortion and leak integrity are unresolved. Brazing or welding face subassemblies before bonding the core avoids heating those initial bond lines; final hull closure still needs a demonstrated sequence.

**6. Panel size and total joining mass.** The 020 stock envelope is **609.6 × 1828.8 mm**, specified for thicker sheet; supplier-confirmed dimensions at 0.843 mm remain unknown. The smaller **304.8 × 609.6 mm** case is a planning assumption. Raw blanks of these sizes, 1 m, 2 m and 4 m are calculated, with scarf overlap deducted. Before that deduction their hull seam lengths are respectively **6.184, 2.749, 2.513, 1.257 and 0.628 km**. The stock-envelope scarf case becomes **2.847 km**. All panel-size applications here are **PROJECTION**. Assembling small sheets into a 4 m module does not remove its internal seams; the 4 m column assumes a true large face blank and suitable core.

| Joining route | Stock envelope mass, kg | 4 m mass, kg | Stock envelope reoptimized SF* | 4 m reoptimized SF* |
|---|---:|---:|---:|---:|
| 8 g/m² deposition + ideal EB, 100% retention | 39.49 | 24.54 | 1.04375 | 1.04747 |
| 8 g/m² deposition + brazed scarf | 41.55 | 24.99 | 1.04322 | 1.04735 |
| 8 g/m² deposition + adhesive scarf | 50.28 | 26.81 | 1.04098 | 1.04688 |
| 20 g/m² deposition + adhesive scarf | 80.44 | 56.97 | 1.03357 | 1.03946 |
| 70 g/m² HexBond film + adhesive scarf | 206.11 | 182.63 | 1.00270 | 1.00850 |
| Nominal AF 0.015 + adhesive scarf | 214.24 | 190.76 | 1.00064 | 1.00649 |
| AF 0.015 + scarf + assumed 5 g/m² primer | 226.81 | 203.33 | 0.99696 | 1.00339 |
| 100 g/m² HexBond film + scarf | 281.50 | 258.03 | 0.98095 | 0.98777 |
| 70 g/m² film + butt straps | 623.09 | 278.15 | 0.89173 | 0.98225 |
| 020-style optimistic bonded splice, resized to 021 | 1022.44 | 517.70 | 0.75085 | 0.84454 |

Mass columns use the original 021 geometry; SF columns independently resize faces and core **at the same 5% margin**, recomputing joining mass each time. *SF is the least **modeled known-mode** value, conditional on perfect installed core bonding and the stated seam screens; overall hull SF is unknown.* The reoptimization keeps the corrected Be/core tuple and 021's needed **gamma = 0.595318** and **wrinkle coefficient = 0.370681** fixed. It does not automatically increase those optimisms to rescue a heavier joint. At kd = 0.2 the original point's global SF is **0.335955**; each fixed-geometry global result scales linearly with kd. MAINLINE-006's different aluminium-family slope is not transferred to Be.

At the smaller planning size, nominal AF/scarf joining is **254.50 kg**, SF* **0.98892**. The laboratory 8 g/m²/scarf route is **90.55 kg**, SF* **1.03091**. At the stock envelope, AF's upper weight tolerance produces **275.59 kg**, SF* **0.98268**.

**7. What changes the conclusion.** At fixed original geometry, the joining-only ceiling permits **86.11 g/m² per bond line with no seams at all**. Nominal AF leaves 32.36 kg for seams and everything else. The modeled stock scarf consumes 30.18 kg of that, leaving just **0.87 g/m² per bond line** for additional area-applied material. The 8 g/m²/scarf projection consumes only **0.2323×** the allowance, but its strength and deposition coverage on Be/Al are unknown. The most informative next evidence is a weighed representative curved Be/Al panel with the selected low-weight fillets and scarf, tested for interface stiffness, flatwise tension, core shear, seam compression, defects and leak/thermal cycling. A low cured mass alone does not close the row.

**8. Handoff.** [NFI.json](4a6f636dbfa17be3-NFI.json) records each joining assumption, its present evidence state, numeric budget factors where meaningful, and the evidence needed to close it. [RESULTS.json](266652aa5589e0de-RESULTS.json) contains all 65 combinations; [VALIDATION.json](4cdd42c52c521596-VALIDATION.json) records eight passing checks, including all six reproduced 021 modes, independent film-unit conversion, mass closure, a denser optimization search and monotonic mass sensitivity. joining-trade.png [source link unavailable in this public projection] plots the comparison. No purchase, fabrication, certification or public action occurred. The brief's successor instruction is **stop and file; the robotics seat sends the next job**.
