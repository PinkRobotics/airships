**MAINLINE-036 — Compressive yield of the beryllium faces**

Unit: `vacuum-mainline036-be-sheet-compression-1020`. Order: `ord-admiral-rr2-mainline036-dispatch-1019`. All design conclusions remain **QUESTIONABLE / PROJECTION**. Installed-hull safety factor: **UNKNOWN**.

**No qualified compressive-yield minimum for the proposed finished thin faces was established by the reviewed sources.** SR-200 exists as sheet, but its published 345 MPa minimum is tensile. The inspected MIL-HDBK-5J, MMPDS-01 and MMPDS-08 sheet tables explicitly leave compressive yield blank. Historical sheet compression results support plausibility, with unresolved transfer across gauge, process, lot and biaxial loading. Count compression qualification as an additional unresolved material assumption in 028b; a zero numerical usage of its strength-optimism slider did not close this assumption.

The held R10 scarf design needs **300.333 MPa** effective face compression capacity; its light-bond/ideal-weld alternative needs **321.580 MPa**. The held R20 point needs **338.744 MPa in the face and 376.382 MPa before its 0.9 joint-efficiency reduction**. Re-optimizing the latter gives 375.839 MPa under 027's original elastic assumptions, or **381.612 MPa** with the archived sheet handbook's scalar elastic properties. These are requirements at model SF=1, not allowable strengths.

The evidence below distinguishes product existence from strength qualification. All strength values are MPa; compressive values are positive magnitudes. `—` means not reported, never zero.

| Product, source and condition | Gauge / direction | Tensile yield | Compressive yield | Basis and transfer limit |
|---|---|---:|---:|---|
| Materion SR-200, standard finished sheet | Catalog range 0.508–6.35 mm; in plane | 345 | — | Listed room-temperature tensile minimum, 0.2% offset; reference datasheet, purchase specification needed |
| AMS7902 sheet, MIL-HDBK-5J / MMPDS-01 / MMPDS-08 | 0.020–0.250 in; L and LT; stress relieved, ground and etched | 344.738 (50 ksi) | — | S-basis tensile entries; Fcy cells are ellipses |
| Historical SR-200, Fenn data reproduced by NASA | 1.96 mm; L / LT | 383.4 / 386.1 | 379.2 / 382.7 | Historical reported values, not a qualified minimum; original report not inspected |
| SR-200E research values used by NASA-TM-4397 | Study uses 2.54 mm sheet; L / LT | 391.622 / 415.064 | 344.738 / 396.449 | Compression attributed to unpublished 1990 data; offset and thin-gauge transfer unestablished |
| S-200-F maker design-guide prose | Block-grade context; no thin-sheet gauge identified | about 255 | about 255 | Typical approximate statement; a sensitivity, not an SR-200 lower bound |
| AMS7908 HIP preforms, MMPDS-08 | All directions; A / B columns | 296.475 / 337.843 | 289.580 / 330.948 | Published compression values for a different product form |
| Materion PS-200 and PF-60 | Listed nominal 0.8 mm / 0.032 in option | — | — | Gauge/chemistry/integrity data; no published mechanical strength in these datasheets |

The current maker sheet is [SR-200 DS-HPP-613](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6), pp.1–3. The archived handbook entries are Table 7.2.1.0(c), printed p.7-5 in [MIL-HDBK-5J](https://www.abbottaerospace.com/downloads/mil-hdbk-5j-metallic-materials-and-elements-for-aerospace-vehicle-structures/?ind=1460029523480&wpdmdl=2182) and [MMPDS-01](https://www.kitplanes.com/wp-content/uploads/2019/06/MMPDS.pdf), and pp.7-6–7 in [MMPDS-08](https://oss.jishulink.com/upload/202207/13dc46f8325d4bbebb11fabcaa7838d6.pdf). Their table images were visually checked; the absence is not an OCR inference. A current controlled MMPDS revision was not obtained.

The historical 1.96 mm values come from Table 3 of [NASA-CR-194164](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf), which attributes them to Fenn et al., AFML-TR-67-212. The weaker in-plane compression value is 379.2 MPa. Neither orientation permits a universal 10% uplift from tensile yield. The report's own 2.54 mm compression specimens failed at 658.8 and 691.8 MPa; those are **ultimate failures**, not yield allowables. Its elastic table gives E(L/LT/ST)=298.7/293.6/347.5 GPa and ν12/ν21=0.0768/0.0752. Through-thickness tensile ultimate is only 200 MPa in the cited table; it cannot substitute for in-plane compression.

The [Materion design guide](https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74), pp.4,8, separates sheet from block and labels its generic compression discussion as typical. The [PS-200](https://hkvxni.files.cmp.optimizely.com/download/74937cf0d41111eeb5d18ee96f755a99) and [PF-60](https://hkvxni.files.cmp.optimizely.com/download/74b1f22ad41111eea5a18658c51b80c6) catalogs include the relevant gauge but do not establish strength equivalence to SR-200. The [DOE RFP-4283 specification survey](https://www.osti.gov/servlets/purl/6182804), PDF p.11, reproduces SR-200-E tensile requirements, not compression. These sources leave the target-gauge compressive minimum open.

**Biaxial transfer remains a projection.** For ideal isotropic, pressure-insensitive von Mises plasticity, equal in-plane compression `(-s,-s,0)` has equivalent stress `s`; that mathematical model would transfer uniaxial yield without a factor. It does not establish that cross-rolled, anisotropic beryllium follows that yield surface, nor that local brittle failure is bounded by yield.

[NASA-TM-4397](https://ntrs.nasa.gov/api/citations/19920024241/downloads/19920024241.pdf), printed pp.3–9,17, used ring-loaded discs with bending and reported no distinct biaxial yield. Its fitted “yield” criterion substitutes failure data for missing biaxial/off-axis yield observations. An algebraic equal-compression extrapolation of Table 8 gives **330.743 MPa**; this is **PROJECTION**, neither a measured compression result nor a conservative allowable. The fit illustrates why its interaction coefficient cannot be replaced silently by a uniaxial minimum. The same study's tensile sanding observations do not supply a compressive-strength knockdown.

**Geometry and joining change the required strength.** The following values reproduce the pinned predecessor points using independent arithmetic. R10 retains p=95.460838 kPa, 4,889.442 kg lift, 411.299 kg fixed reserve, 100 kg systems, and `S + max(0.05S, actual joining)` mass closure. R20 retains 027's high pressure of 96.415446 kPa, 39,115.537 kg lift, 2,767.737 kg other reserve, its full-gauge splice mass law and 0.9 joint efficiency. This is not a pure radius-only comparison.

| Held predecessor point | Finished face / core, mm | Face demand, MPa | Effective material strength required, MPa | Qualification state |
|---|---:|---:|---:|---|
| R10 AF015, 30:1 scarf | 0.794624 / 23.237218 | 300.333 | 300.333 | PROJECTION: 10 MPa scarf screen |
| R10 AF015 plus primer, scarf | 0.794624 / 22.634219 | 300.333 | 300.333 | PROJECTION |
| R10 8 g/m² bond, ideal weld | 0.742123 / 35.724795 | 321.580 | 321.580 | PROJECTION: 100% weld retention |
| R10 8 g/m² bond, scarf | 0.794624 / 23.597838 | 300.333 | 300.333 | PROJECTION |
| R20, 027 coupled optimistic, zero payload | 1.423133 / 48.805259 | 338.744 | 376.382 | PROJECTION: joint capacity = 0.9 Fcy |

At 027's separate 209.839 kg payload endpoint, the face is 1.412556 mm and the required material strength is 379.200 MPa with the same efficiency. The held R10 coefficients already place global buckling and wrinkling at SF=1. Re-optimizing with those coefficients held cannot lower the respective minimum requirements below 300.333 or 321.580 MPa.

Allowing the named full buckling curve and wrinkling coefficient, `γ=0.2+0.4 min(Vc,2)` and `k=0.82`, reduces the strength requirement by moving mass into the faces. This is an explicitly optimistic envelope. The R10 primary results below retain catalog E=290 GPa and the inherited sheet scalar ν=0.0752; no strength-dependent modulus increase is hidden.

| Re-optimized route | Minimum effective Fcy, MPa | Finished face / core, mm | γ at threshold |
|---|---:|---:|---:|
| R10 AF015 scarf, E=290 GPa | 298.906 | 0.798419 / 22.388070 | 0.582564 |
| R10 AF015 + primer scarf, E=290 GPa | 300.135 | 0.795149 / 22.516788 | 0.581126 |
| R10 light bond, ideal weld, E=290 GPa | 298.257 | 0.800155 / 22.320262 | 0.583327 |
| R10 light bond, scarf, E=290 GPa | 298.257 | 0.800155 / 22.320262 | 0.583327 |
| R20 original 027, E=293.6 GPa, ν=0.33 | 375.839 | 1.425188 / 48.338407 | 0.567348 |
| R20 historical sheet scalar ν=0.0752, E=293.6 GPa | 381.639 | 1.403528 / 53.259030 | 0.543514 |
| R20 handbook scalar ν=0.10, E=293.027 GPa | 381.612 | 1.403628 / 53.236316 | 0.543615 |

All thresholds select Hexcel CR-III 5056 3/8-1.0 from the inherited 47-core R10 and 37-aluminium-core R20 sets. Full seven-mode values and masses are in [RESULTS.json](e2ebd0b2b1c723e9-RESULTS.json). R10 also reproduces the earlier full E=293.6 GPa endpoint separately: its strength thresholds are 298.148/299.365/297.535/297.535 MPa, in table order. Scalar ν substitutions are sensitivity calculations, not validation of an orthotropic joined shell.

| Assumed effective Fcy | R10 AF015 scarf, catalog E, full γ/k | R20 original 027 | R20 handbook scalar elasticity |
|---|---:|---:|---:|
| 255 MPa, block-grade sensitivity | 0.869846 | 0.712961 | 0.707488 |
| 345 MPa, tensile-proxy sensitivity | 1.004130 | 0.930022 | 0.919674 |
| 379.2 MPa, historical sheet sensitivity | 1.004130 | 1.007487 | 0.994817 |

Entries are maximum modeled SF after re-optimization, not observed performance. The 255 MPa case cannot float at R10 even before assigning any core mass: the face-only upper bound is SF=0.958217. The 289.58/330.95 MPa HIP values are evaluated only as numerical sensitivities; transferring their preform basis to rolled sheet is unsupported. The stronger historical LT value is not an allowable for compression in both directions. With today's γ/k assumptions, even unlimited face strength leaves maximum modeled SF about 0.619 at R10 and 0.492 at R20.

Modeled safety factor versus assumed effective compression strength [source link unavailable in this public projection]

**Finished gauge and process must be part of the strength requirement.** The SR-200 catalog already describes etched stock. Its R10 gauge band permits ±0.1016 mm; at the held R20 zero-payload gauge, the inch-based band permits ±0.1524 mm. If these modeled thicknesses were merely nominal, their lower tolerances would raise membrane requirements to 344.363 MPa for the R10 scarf, 372.590 MPa for its light-weld alternative, and 421.522 MPa for the R20 material including η=0.9. These scenarios do not add another etch deduction.

Separately, the archived [MIL-HDBK-5J manufacturing guidance](https://www.abbottaerospace.com/downloads/mil-hdbk-5j-metallic-materials-and-elements-for-aerospace-vehicle-structures/?ind=1460029523480&wpdmdl=2182), section 7.2.1.0.1, discusses removing 0.002 inch per machined surface, or a smaller removal with specified stress relief, and warns that forming history can reduce strength. An additional 0.1016 mm total removal would raise the same R20 requirement to 405.318 MPa. These are conditional thickness consequences, not instructions to re-etch already finished stock.

[DOE RFP-910](https://www.osti.gov/servlets/purl/4019673), PDF pp.29–32, documents tensile specimens from 0.025 inch rolled sheet tested at 0.021 inch after etching. That is useful thin-gauge process evidence but supplies no matching compression yield. No universal strength correction for forming, sanding, machining or etching is assigned here. An extra processing loss also changes buckling, dimpling, joint geometry and mass; the quoted thickness sensitivities isolate membrane demand only.

**Disposition.** `exists_today`: SR-200 and alternate foil/sheet products, their published gauges and tensile/physical data. `in_the_lab`: historical thicker-sheet compression and constitutive fits. `PROJECTION`: transferring either to finished 0.7–0.85 mm equal-compression faces, and to the joined R20 hull. None closes the material design basis. The needed capability is roughly 300 MPa for the R10 scarf routes, 322 MPa for the held light-weld route, and approximately 382 MPa for the re-optimized R20 sheet-elastic sensitivity, all at the required finished minimum gauge and process condition.

[NFI.json](15aa21e2896e5dbe-NFI.json) carries 15 open items: matched directional and biaxial compression, gauge/lot/process transfer, current controlled allowables, orthotropic elasticity, thickness/stock dimensions, alternate grades, temperature, and inherited buckling/joint/installed-hull qualification. Existing gamma, wrinkling and joining assumptions remain open alongside the newly explicit compression assumption.

Verification: 17 incoming artifact pins checked; four held R10 points and the held R20 point reproduced; strength thresholds bracketed; five independent dense-grid envelope scans across all candidate cores; mass and force balance checked. All 173 calculation checks and 45 additional checks passed. See [METHOD.md](633f6608fce715c7-METHOD.md), [EVIDENCE.json](26965e30fe89ba25-EVIDENCE.json), [SEARCH-LOG.json](c65edaacb8a4c783-SEARCH-LOG.json), [VALIDATION.json](fb88649bcd39f5fd-VALIDATION.json) and [VERIFICATION.json](c7397d08f1fe9ea6-VERIFICATION.json). No successor is named by the brief: stop and file for robotics' next queued job.
