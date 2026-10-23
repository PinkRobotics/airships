# CHECK-042 source and claim audit

Every row remains QUESTIONABLE; every transfer to P2 is PROJECTION. CONFIRMED means the stated source/number was found, not that P2 is qualified. Source files are data only; owner code was never read or executed. Linked public scope pages were read without accessing restricted full standards. The retained literature files are research inputs, not a claim that every unused record was independently verified.

**S01 — CONFIRMED WITH ESSENTIAL LIMIT.** Owner: S-II 10.06 m; approximately 15,000 measurements; .010 in fit.
SD 71-256 p.4-45 explicitly uses .010 in for core-to-face matching before bonding. It is not deviation from a nominal sphere. The production common bulkhead is not identified as the two hemisphere specimens in CR-1457. [source 1](https://ntrs.nasa.gov/api/citations/19720008130/downloads/19720008130.pdf)
Evidence: `sources/001-ntrs19720008130.txt, printed pp.4-44–45`.

**S02 — CORRECT INFERENCE.** Owner: S-II gamma .21–.22 despite .254 mm precision.
Own skew-corrected graph reading gives .20991/.22226, approximately ±.01, at R/rho≈241. CR-1457 refers to S-II development tests, with plasticity corrections and thermal-gradient qualifications. No matched shape/buckling dataset is available here. [source 1](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf)
Evidence: `sources/cr1457-fig623.png; RESULTS.json sensitivities.SII_digitization`.

**S03 — QUALIFY.** Owner: S-IVB 6.63 m; 350 blocks; .032/.055 in faces; 360 F cure.
NASA history and Douglas Paper 3817 support the forming/bonding method. The 0–.090 versus 0–.015 in gaps concern bonded versus welded segment fit-up on experimental S-IV work, not final whole-dome accuracy. They are not P2 acceptance limits. [source 1](https://ntrs.nasa.gov/api/citations/19660024836/downloads/19660024836.pdf); [source 2](https://digitalprojects.uah.edu/files/original/20/10318/thedevofaboncombulforsat_090707133327.pdf)
Evidence: `sources/000-sp4206.txt printed p.168; sources/006-uah10318.txt p.15`.

**S04 — CORRECT PRECISION LABEL.** Owner: Rohr 57 in: .050 in after forming, .150–.200 after milling.
The values are supported, but are residual contour errors before extensive hand forming to the welding jig. The report also describes a final creep-sizing tensile failure. They are not achieved final bulkhead precision. Conversions are 1.27 and 3.81–5.08 mm. [source 1](https://ntrs.nasa.gov/api/citations/19660014454/downloads/19660014454.pdf)
Evidence: `sources/009-ntrs66014454.txt PDF pp.3–4,25`.

**S05 — CONFIRMED WITH LIMIT.** Owner: CCTD 5.5 m; out-of-autoclave route toward 10 m.
Supported for graphite/epoxy laminate tank development. A 10 m capability objective is not a 20 m Be sandwich demonstration. [source 1](https://ntrs.nasa.gov/api/citations/20150021410/downloads/20150021410.pdf)
Evidence: `sources/019-ntrs20150021410.txt`.

**S06 — CORRECT STAGE.** Owner: Ares I weld mismatch ≤.041 in.
The .041 in value is the magnitude of the maximum post-tack effective mismatch on CBMDA #1, approximately 20% of its weld land thickness. It is not a demonstrated final shape tolerance; the subsequent full weld had PAUT indications. [source 1](https://ntrs.nasa.gov/api/citations/20120014602/downloads/20120014602.pdf); [source 2](https://ntrs.nasa.gov/api/citations/20100017376/downloads/20100017376.pdf)
Evidence: `sources/008-ntrs20120014602.txt Table 2`.

**S07 — PARTLY CONFIRMED.** Owner: Atlas 5.4 m vented-core fairing; 54 t mould; X-33 debonds.
ULA confirms the graphite/epoxy faces and vented aluminium core. NASA documents X-33 debond failure mechanisms. Beyond Gravity confirms an out-of-autoclave process. The 54 t mould detail remains secondary-only and receives no precision credit. [source 1](https://www.ulalaunch.com/docs/default-source/launch-booklets/AtlasV_USSF-7_mob.pdf); [source 2](https://ntrs.nasa.gov/api/citations/20200006023/downloads/20200006023.pdf); [source 3](https://www.beyondgravity.com/en/news/beyond-gravity-innovating-space-launches-reusable-payload-fairing-concept)
Evidence: `sources/013-ula_atlas.txt; sources/017-ntrs20200006023.txt; SOURCE-INDEX.json`.

**S08 — CONFIRMED WITH LIMIT.** Owner: CSO 10.4 m, 1.15 m panels, 150 µm rebound, 5–10 µm panels, <30 µm dish.
Leighton describes compensating the skin-induced panel rebound by pre-straining during cutting. Serabyn independently reports 5–10 µm panel RMS and a dish just below 30 µm. These are reflector measurements with adjustments, not wrinkle-band measurements on compressed Be. [source 1](https://doi.org/10.7907/75rd-4h66); [source 2](https://authors.library.caltech.edu/records/gwhtw-cx480)
Evidence: `sources/021-leighton_nsf.txt printed pp.20,51; sources/024-serabyn91.txt p.1`.

**S09 — CONFIRMED.** Owner: ALMA: .6 mm Ni, 20 mm core, 120 panels, five adjusters.
The construction is supported by Mangum Table 1 and the ESO 2011 announcement. Distinguish the ESO production description from the prototype test. [source 1](https://arxiv.org/pdf/astro-ph/0609329); [source 2](https://www.eso.org/public/announcements/ann11022/)
Evidence: `sources/030-alma_proto.txt pp.6–7; sources/eso-alma.html`.

**S10 — CORRECT CONTEXT.** Owner: ALMA 38 µm laser →55 µm holography→14 µm.
Values occur, but an intervening hard-stop accident led to a repeat laser measurement of 50 µm before 55 µm holography. Two full and one partial adjustments reached about 14 µm; later evaluation gives 16–17 µm. The sequence is not a pure instrument comparison. [source 1](https://arxiv.org/pdf/astro-ph/0609329)
Evidence: `sources/030-alma_proto.txt §5.1.1`.

**S11 — QUALIFY.** Owner: SMT 14–19 µm after 47 µm initial.
Individual scans of 14/19 µm are reported; the observatory's conclusion from averages is 16–19 µm, with repeatability limitations. Report the aggregate result separately from the best scan. [source 1](https://www3.mpifr-bonn.mpg.de/div/hhertz/holo97/holo97.html)
Evidence: `sources/028-hht_holo97.readable.txt`.

**S12 — CORRECT POPULATION.** Owner: LMT 98 µm, segments <20 µm.
The 98 µm overall optical RMS is supported. ≤20 µm applies to recent outer-ring segments; some inner segments remain 30–40 µm and 11 ring-4 segments require improvement. The claim cannot cover every segment. [source 1](https://www.inaoep.mx/~itziar/papers/2020Hughes_1144522LMT.pdf)
Evidence: `sources/033-lmt_hughes.txt PDF pp.7–8,13–14`.

**S13 — QUALIFY.** Owner: IRAM 50–60 µm; errors correlated over .3–.5 m.
The 2013 report states improvement from about 65 to 50 µm, and .3–.5 m for panel deformation correlations. This is not the 20–60 mm wrinkle band; the honeycomb construction detail is not independently established by that report. [source 1](https://web-archives.iram.fr/legacy-website/medias/uploads/eb2013-v8.2.pdf)
Evidence: `sources/034-iram_eb2013.txt`.

**S14 — CONFIRMED WITH LIMIT.** Owner: Nobeyama 21–71 µm.
The paper distinguishes older panels averaging 60 µm, older whole dishes averaging 71 µm, and new panels averaging 21 µm. Keep those three populations separate. [source 1](https://doi.org/10.1017/S0252921100019035)
Evidence: `sources/038-nma.txt PDF pp.1–2`.

**S15 — CONFIRMED WITH LIMIT.** Owner: Sandwich radomes to 23.5 m.
CPI lists 3–23.5 m and foam for larger radomes/honeycomb for smaller ones. Comtech lists 1.5–20 m foam sandwich. Neither supplies a compression-shell shape tolerance. [source 1](https://cpii.com/docs/related/184/CPI%20Sandwich%20Radomes%20Sheet%20Feb25.pdf); [source 2](https://comtech.com/wp-content/uploads/2025/10/ds_Radome_102025.pdf)
Evidence: `sources/045-radome_cpi_sheet.txt; sources/046-radome_comtech.txt`.

**S16 — CONFIRMED WITH LIMIT.** Owner: SNO 12 m, 122 panels; ±25 mm specified; ±6 mm typical.
Supported; room-temperature polymerized adhesive and >27.5 MPa bond test results concern acrylic. The geometric tolerance is a different structure, material, thickness and load case. [source 1](https://www.hep.upenn.edu/SNO/papers/sno_nim.pdf)
Evidence: `sources/075-sno-nim.txt PDF pp.9–10`.

**S17 — CORRECT METRICS.** Owner: Moss R18.3 m held <2 cm; JUNO ±50 mm; JT-60SA ±8 mm.
Moss <2 cm is a required deviation, not a demonstrated final-shell bound in the cited sentence. JUNO ±50 mm is a diameter requirement; panels require <6 mm deviation. JT-60SA ±8 mm is a specified spherical-radius tolerance. They are not interchangeable measured RMS values. [source 1](https://www.isprs.org/proceedings/XXIII/congress/part5/183_XXIII-B5.pdf); [source 2](https://arxiv.org/pdf/2311.17314); [source 3](https://conferences.iaea.org/event/214/contributions/17269/attachments/10004/14080/849_Y.Shibama_IAEA.poster.pdf)
Evidence: `sources/076-isprs-faig-1980.txt p.1; sources/074-arxiv-juno-cd-2311.17314.txt p.27; sources/077-jt60sa-cryostat.txt`.

**S18 — CONFIRMED WITH LIMIT.** Owner: Solar 1×2 ft Be panel, 10 ft radius, 1250 F, .003 in fit.
Supported for a brazed all-Be sandwich curved cylindrically. This does not establish full-size doubly curved SR-200 face blanks. A later panel's wrinkles only partly responded to additional bend/stretch forming. [source 1](https://ntrs.nasa.gov/api/citations/19730016169/downloads/19730016169.pdf)
Evidence: `sources/055-ntrs-19730016169.txt PDF pp.86,114`.

**S19 — CONFIRMED WITH LIMIT.** Owner: SR-200 .795 mm stock envelope and ±.102 mm tolerance.
The .025–.034 in gauge row specifies ±.004 in (=.1016 mm). At .020–.058 in, the manufacturer explicitly provides smaller dimensions than 24×72 in, without a numerical maximum. The assumed blank is not a procurement specification. [source 1](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6)
Evidence: `sources/050-mat-sr200-a.txt`.

**S20 — QUALIFY.** Owner: Forming at 1250–1350 F; chemical milling .001 in/3 min.
Historical process examples support hot forming, but not a qualified temperature window for this sheet and double curvature. The etch-rate entry is process-specific and includes thickness taper in its source. Neither is a current supplier capability guarantee. [source 1](https://ntrs.nasa.gov/api/citations/19730016169/downloads/19730016169.pdf); [source 2](https://ntrs.nasa.gov/api/citations/19720023297/downloads/19720023297.pdf); [source 3](https://ntrs.nasa.gov/api/citations/19720016923/downloads/19720016923.pdf)
Evidence: `sources/055-ntrs-19730016169.txt; sources/054-ntrs-19720023297.txt; LIT-B BS-5/BF rows`.

**S21 — CORRECT INTERPRETATION.** Owner: 345 MPa gives a 1.19e-3 elastic limit.
345/E=1.189655e-3 is the elastic strain component at a tensile proof/yield proxy, not a measured proportional limit or compression forming allowable. The listed 4.645152e-4 strain gives Eε=134.709408 MPa; 67.354704 MPa needs half that strain or another stated model. [source 1](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6)
Evidence: `RESULTS.json route and sensitivities; intake/upstream/028b-METHOD.md`.

**S22 — CORRECT EVIDENCE LEVEL.** Owner: AF163-2U's own verified 200 F/6 h cure.
The sheet says limited family-level results suggest useful performance at 200 F/6 h. Its numerical 200 F metal-to-metal table is AF163-2K .06 lb/ft² at 50 psi, not U .015 on this core/Be. A supplier process qualification remains open. [source 1](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf)
Evidence: `sources/072-3m-af163-2.txt sections V and VI`.

**S23 — ARITHMETIC CONFIRMED.** Owner: 037b cure fix: usage .972→1.052; 30.34:1; +.12 kg.
Independent mass/scarf equations reproduce baseline .971978 and 250 F 1.052282 usage. At 200 F, the exact nominal stress sizing gives 30.341397:1; the rounded 30.34 route reclosed on mass gives usage .972433. The +.12 kg magnitude is consistent. All are conditional homogenized calculations. 
Evidence: `RESULTS.json sensitivities.cure_rebuild; intake/upstream/028b-METHOD.md and 035/CARD.md`.

**S24 — CORRECT POINT IDENTITY.** Owner: A stress-free temperature above 54 C is the threshold.
The 54 C threshold in 037b concerns the separate 037 floated point. 028b's 30:1 scarf already binds at nominal load; positive added compression has no spare scarf margin. 
Evidence: `intake/upstream/035/CARD.md sections 1,2 and residual state`.

**S25 — QUALIFY.** Owner: Room-temperature seam; EA9394/9309 lap shear 29–33 MPa.
Supplier aluminium lap tests support those approximate values and room-temperature curing. They do not qualify the Be scarf, its peel, sealing, fatigue, applied film thickness, or the inherited 70 g/m² and 10 MPa seam assumptions. [source 1](https://datasheets.tdx.henkel.com/LOCTITE-EA-9394-AERO-en_US.pdf); [source 2](https://www.pccomposites.com/wp-content/uploads/2015/07/PCRS9309-3NAQT_TDS.pdf)
Evidence: `sources/069-henkel-ea9394.txt; sources/070-pcc-ea9309-3na.txt; intake/upstream/028b-METHOD.md`.

**S26 — CORRECT.** Owner: 028b closes with 2 kg to spare.
The selected 028b charged-total mass equals lift within numerical roundoff. Unallocated margin is approximately zero; its fixed reserve is already assigned. The 2 kg statement is not supported by the pinned point. 
Evidence: `RESULTS.json sensitivities.mass_residual_at_028b_kg; intake/upstream/004/RESULTS.json`.

**S27 — CORRECT GEOMETRY.** Owner: 43.4 kg trapped air in this 23.2 mm core.
034 used a 30.1182 mm core. At 028b, even a completely void thin-shell core contains at most 34.0851 kg at the specified 500 m atmosphere; a finite annulus with the stated solid fraction gives 33.7988 kg. Ground sea-level full-void upper estimate is 35.7709 kg. 
Evidence: `RESULTS.json sensitivities.trapped_core_air; intake/upstream/012/CARD.md`.

**S28 — ARITHMETIC / SCOPE CONFIRMED.** Owner: 30–50 kg sealed service; 1.061 sea-level proof factor.
The systems range remains an inherited 24-hour service estimate, not a qualified installed minimum. The pressure ratio reproduces 1.061430. Passing one evacuation would not establish operational reliability or a certified proof factor. 
Evidence: `RESULTS.json route.sea_level_overload; intake/upstream/012/CARD.md`.

**S29 — QUALIFY.** Owner: 4189 m³ sphere; 2321 m³ largest autoclave; 9.14 m diameter.
Sphere geometry and 30 ft=9.144 m conversion reproduce. Spirit's 2016 primary release calls its vessel one of the largest. 2321 m³ is a record-page claim, not an exhaustive current facility survey. No cited vessel accommodates this sphere; 'any oven' requires an actual facility/tooling envelope. [source 1](https://investor.spiritaero.com/news-presentations/news-details/2016/Spirit-AeroSystems-installing-one-of-the-worlds-largest-autoclaves-for-composite-manufacturing/default.aspx)
Evidence: `RESULTS.json envelope; LIT-B CF-1; source retrieval limitations in sources/WEB-PINS.json`.

**S30 — ARITHMETIC / LAYOUT LIMIT.** Owner: 5.7 km seams, 1189 blanks/skin, 24.1 mm new overlap.
The old 30:1 approximation gives 5683.0371 m and 1188.5606 panels/skin. At rounded 30.34:1: 5685.2254 m, 1189.2870 panels, minimum integer 1190; overlap 24.108894 mm. No actual spherical tiling, pole closures, scrap or manhole bill is supplied. 
Evidence: `RESULTS.json coverage and sensitivities`.

**S31 — CORRECT BOUND LABEL.** Owner: 1.22 mm upper gauge-patch deflection.
The value reproduces a first-order unconstrained local membrane estimate. Keeping the exact 1/(1−gauge_fraction) dependence gives 1.40410 mm before compatibility effects. Therefore 1.22 is not established as an upper bound. 
Evidence: `RESULTS.json sensitivities.low_gauge_independent_membrane_patch_mm`.

**S32 — ARITHMETIC CONFIRMED; PROJECTION.** Owner: 2 m support sag .11 mm; 5 m 4.2 mm; .5 psi inflation.
The stated strip approximation reproduces .106364 and 4.154826 mm; the .5 psi inner-skin stress is 21.691884 MPa. These do not determine a whole-shell jig load path or release distortion. The ~180 ratio uses k=1/(Rβ), a characteristic inverse length. 
Evidence: `RESULTS.json route`.

**S33 — QUALIFY.** Owner: 354 MPa for a locally heated 100 K seam forces room-temperature cure.
354.346886 MPa is the fully restrained biaxial elastic thermal screen. Actual constraint, stress relaxation, heating width and temporary supports were not solved. It motivates process development, not a universal impossibility theorem for local cure. 
Evidence: `RESULTS.json route.seam_hot_cure_stress_MPa_per_100K`.

**S34 — ARITHMETIC CONFIRMED; RANGE LIMIT.** Owner: 9.3–16.1 mm dimple; width .36 m.
Inverse amplitudes and .356777 m characteristic width reproduce. The Lee curve is a lower envelope over widths 1–5 and R/t=100,200; this shell has R/t=240.244. Its k=1 to 5 single-dimple RMS is .11754–.58770 mm, not one uniquely associated RMS. [source 1](https://groups.seas.harvard.edu/hutchinson/papers/SphericalShellsMIT-IT-2016.pdf)
Evidence: `sources/lee2016.txt §7; RESULTS.json gamma_need_028b`.

**S35 — CORRECT IMPLIED CREDIT.** Owner: Eq.3 values near .90–.95 from small fabrication errors.
The inverses/forward values reproduce, but .15/.254/1.27 mm examples are below d/t=.07, excluded from the fit's small-amplitude behavior. A monolithic-shell fit transferred through equivalent thickness does not validate sandwich buckling. [source 1](https://www.epfl.ch/labs/flexlab/wp-content/uploads/2025/12/Baizhikova-et-al.-2026-A-probabilistic-buckling-model-for-hemispherical-shells-with-non-interacting-localized-defects.pdf)
Evidence: `sources/baizhikova2026.txt Eq.3; RESULTS.json precedent_dimples`.

**S36 — ARITHMETIC CONFIRMED; PROJECTION.** Owner: Q .435 requires .075–.129 mm; reflector Q .59–.75.
CR-1457 inversion reproduces .07511795/.12877362 mm with the exact upstream Q. Whole-panel RMS×sqrt(2) assumes one sinusoid at the relevant wrinkle band. Neither that conversion nor cell-print-through depth is a measured band-limited hull wave. [source 1](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf)
Evidence: `RESULTS.json Q tables; intake/upstream/008,009,010 cards/check`.

**S37 — CORRECT COHORT.** Owner: Tap a90/95 43 manual, 28 automated.
Table 4 full cumulative logit values are 41.8 and 29 mm. 43.3/28 remove best and worst inspectors. The worst manual fit did not converge; worst automated is 70 mm. Test panels have .5 mm Al skins, 19 mm panel thickness, 4.76 mm cells and 91 kg/m³ core. [source 1](https://icaf.aero/icaf2023/proceedings/documents/55.pdf)
Evidence: `sources/087-icaf2023-genest-tap.txt Table 4 and test-panel description`.

**S38 — CORRECT POISSON CONVENTION.** Owner: Disbond buckling diameter 29.292–54.780 mm.
The inferred coefficients are 4.198 and 14.682. Solving the circular-plate boundary equations at Be nu=.0752 gives k=3.600503 and 14.681971, hence 27.127598 and 54.779991 mm. The lower value is below even the 28 mm selected-cohort tap statistic; actual flaw boundary/contact effects remain unknown. [source 1](https://pubs.rsc.org/en/content/articlehtml/2008/sm/b712324h)
Evidence: `RESULTS.json disbond_critical_diameter_mm; independent boundary derivation in METHOD.md`.

**S39 — CONFIRMED WITH LIMIT.** Owner: Shearography POD .95, 15 m²/h, 168 h both lines.
NASA's .95 result is for SOFI debonds approximately the foam thickness. Its strip tests require two shear directions. Dantec's 15 m²/h is a vendor hood rate; 167.5516 h is scan-area/rate only, excluding setup, access, repeated orientations and rescans. [source 1](https://ntrs.nasa.gov/api/citations/19960028755/downloads/19960028755.pdf); [source 2](https://seminare.dgzfp.de/portals/opm2015/BB/3.pdf)
Evidence: `sources/095-ntrs-19960028755.txt; sources/103-dgzfp-dantec-2015.txt p.5`.

**S40 — CONFIRMED WITH LIMIT.** Owner: UT 6.35 mm; E2580 flat panels.
The NLR experiment sees .25 in inserts with conventional 5 MHz UT in CFRP. ASTM E2580-24 is for flat parallel-surface panels and does not set accept/reject limits. Neither supplies Be honeycomb/scarf POD. [source 1](https://reports.nlr.nl/bitstreams/e872e818-2491-4185-9a35-bdf5ac956258/download); [source 2](https://store.astm.org/e2580-24.html)
Evidence: `sources/083-nlr-lut-fulltext.txt; public ASTM scope checked 2026-10-20`.

**S41 — QUALIFY.** Owner: Flash thermography likely blind; kissing bonds escape commercial NDE.
NASA's 8:1 result concerns its specific composite face/core-wall model, not .8 mm Be. The NASA bond-strength presentation describes limits of current commercial NDE, not impossibility of all methods. E2582-21(2025) excludes core and far-face interfaces and supplies no acceptance criterion. [source 1](https://ntrs.nasa.gov/api/citations/20150001252/downloads/20150001252.pdf); [source 2](https://ntrs.nasa.gov/api/citations/20230010345/downloads/QNDE%202023%20Conference%20Presentation_Takunju_FINAL.pdf); [source 3](https://store.astm.org/e2582-21r25.html)
Evidence: `sources/111-ntrs-20150001252.txt; sources/121-ntrs-20230010345.txt`.

**S42 — CONFIRMED WITH LIMIT.** Owner: Laser tracker .106/.191 mm at 10/20 m.
These are the AT960 scale-bar maximum permissible errors under specified tests, not whole-shell coordinate uncertainty. Registration, targets, temperature, line of sight and gauge access require a task-specific uncertainty budget. [source 1](https://atecorp.com/getmedia/457543d7-b91a-4596-825c-9da1d944b647/hexagon-mi-at960-datasheet-a4_en_1.pdf)
Evidence: `sources/141-at960-datasheet.txt ASME B89.4.19 table`.

**S43 — CONFIRMED WITH LIMIT.** Owner: Photogrammetry .043–.091 mm on 13.2 m tool; 1:100k–200k.
GSI Table 3 supports RMS coordinate differences against a tracker on that tool. The relative-accuracy projection gives .2–.1 mm over 20 m; it does not automatically apply to a stitched shell network. [source 1](https://www.geodetic.com/wp-content/uploads/2018/08/S-Acceptance-Test-Results-metric-version.pdf)
Evidence: `sources/133-gsi-vstars-accept.txt Table 3`.

**S44 — CONFIRMED WITH LIMIT.** Owner: RTC360 1.9/2.9 mm at 10/20 m.
These are supported 3D-point specifications, insufficient by themselves for .075 mm waviness. [source 1](https://infrabooking.aalto.fi/kokvar/tilakuvat/aaltoinfra/210907101508_leicartc360ds.pdf)
Evidence: `sources/143-leica-rtc360.txt`.

**S45 — CORRECT CAPABILITY CLAIM.** Owner: Profiler .4 µm repeatability means yes for .075 mm waviness.
The current LJ-X8060 page confirms .4 µm Z repeatability but separately specifies linearity and temperature effects. Repeatability is not accuracy or an installed-surface acceptance capability. [source 1](https://www.keyence.com/products/measure/laser-2d/lj-x8000/models/lj-x8060/)
Evidence: `sources/keyence-current.html; public page checked 2026-10-20`.

**S46 — CONFIRMED WITH LIMIT.** Owner: DIC .003 in (3σ); structured light .001 in; six systems.
NASA reports those case-specific uncertainties and full-scale 27.5 ft cylinder instrumentation. Geometry, viewing angle, calibration, spatial filtering and paint differ from a Be sphere. [source 1](https://ntrs.nasa.gov/api/citations/20180006177/downloads/20180006177.pdf); [source 2](https://ntrs.nasa.gov/api/citations/20180006174/downloads/20180006174.pdf)
Evidence: `sources/147-ntrs-20180006177.txt pp.8,11; sources/149-ntrs-20180006174.txt`.

**S47 — CORRECT METRIC.** Owner: Fibre sensing .65 mm pitch, ±5 µε.
The Luna sheet distinguishes measurement uncertainty from system accuracy: the .65 mm-pitch column has ±5 µε uncertainty but ±25 µε system accuracy. Pitch availability also depends on the 610x/600x mode. It is not full-field shape data. [source 1](https://erc-dreamon.ens-paris-saclay.fr/sites/erc_dream_on/files/media/downloads/ds_luna-odisi-6000-data-sheet_0.pdf)
Evidence: `sources/163-luna-odisi6000.txt specification table and notes 6–7`.

**S48 — CORRECT CAUSAL CLAIM.** Owner: OSHA .2 µg/m³ therefore every scarf must be supplier-cut.
The .2 value is an 8-hour TWA; the 15-minute STEL is 2.0 µg/m³. Controls and regulated-area criteria depend on exposure. Supplier-only cutting is the proposed process choice, not a categorical location requirement in this rule. [source 1](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1024)
Evidence: `official public rule checked 2026-10-20, paragraphs (b),(c),(e),(f)`.

**S49 — PARTLY CONFIRMED.** Owner: JCMT £2M/£5M; SMT $5–6M; ALMA $169M/25.
JCMT's 2011 talk supports the quoted historical estimates. General Dynamics' July 2005 company newsletter independently supports $169M/25; the pinned SEC report rounds to $170M. SMT's 1987 amount remains a secondary report. None is a P2 price or inflation-adjusted estimate. [source 1](https://www.roe.ac.uk/workshop/submm/presentations/walter-gear.pdf); [source 2](https://www.gdeb.com/news/ebnews/PDF/ebnews0705.pdf); [source 3](https://www.sec.gov/Archives/edgar/data/0000040533/000119312505214365/d10q.htm)
Evidence: `sources/037-jcmt_gear.txt slides22–23; sources/041-gd10q.readable.txt; GD newsletter visible in primary search excerpt, direct fetch failed`.

**S50 — ARITHMETIC CONFIRMED; PROJECTION.** Owner: Four ~1.65 kg F1 blanks at $10–50k/kg.
At exact .794624 mm gauge each raw blank is 1.638870 kg; four cost $65,554.82–327,774.08 under the inherited planning-price assumption. Tooling, labour, inspection, scrap and qualification remain unpriced. 
Evidence: `RESULTS.json sensitivities; intake/upstream/014/CARD.md`.

**S51 — QUALIFY.** Owner: No seam NDE method.
No matched Be scarf inspection qualification was found in this evidence packet. That is an evidence gap, not proof that no method can work. The proposed F1 sectioning and representative defect tests remain useful next work. 
Evidence: `intake/owner/LIT-C.json and NFI.json; source rows S37–S41`.

**S52 — CORRECT QUALIFICATION.** Owner: Published gamma/Q map supports .2 / about .6.
The arithmetic is a projection. The historical .2 handbook design factor, isolated defect maps and reflector RMS do not establish any measured installed P2 gamma or Q. Qualified values remain null. 
Evidence: `RESULTS.json; S02,S34–S36; CHECK.md`.
