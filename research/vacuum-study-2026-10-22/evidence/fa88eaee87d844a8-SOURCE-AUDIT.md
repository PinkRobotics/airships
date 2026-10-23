# MAINLINE-048 source audit

All source properties are QUESTIONABLE when transferred to this hull; installed performance is PROJECTION. Missing measurements remain missing. A numerical screening choice is not a measured material property.

## The original water charge

The trace is 040 `model.py` → 033 reserve scaling → 028b/019 reserve → 016's surface-water assumption. Pinned copies of 016 and 019 are in `snapshots/`; their original paths and hashes are in `UPSTREAM-PINS.json`.

016 INPUTS calls 0.1–1 mm an owner-assumed retained surface-film band. Its CARD discusses weather, shedding, hydrophobic treatment and an operating window. 019 selects 0.1 mm with water density 1000 kg/m³. Thus

`M_external = 4πR² × 1000 × 0.0001 = 0.1 A`.

This gives 125.663706, 180.955737 and 282.743339 kg at R10, R12 and R15. It is not an AF 163-2U absorption measurement, a rain-depth forecast or a core saturation result. 040's assumed internal volatile inventory is a different account. Preseal drying does not prevent later exterior wetting.

## Finishes

**AZ-93.** The maker ties α = 0.15 ± 0.02 to thickness ≥5 mil (127 µm), with ε = 0.91 ± 0.02. Reducing thickness to the low end of the nominal application tolerance does not preserve that optical specification. The site supplies adhesion and space-exposure information but no dry density or installed areal mass. The 040 charge of 0.20 kg/m² therefore remains an allowance, not a verified AZ-93 weight. [AZ Technology](https://www.aztechnology.com/product/1/az-93).

**Z-93.** The NASA catalog gives α = 0.184, hemispherical ε = 0.880 and 4.5–6 mil recommended thickness; density is unavailable. It documents adhesion and UV results, but no matched Be/outdoor humidity qualification. A mass cannot be recovered from thickness alone. [NASA coating catalog, printed II-26](https://ntrs.nasa.gov/api/citations/19730017242/downloads/19730017242.pdf).

**SolarWhite.** ENBIO lists 150–220 µm, ε about 0.89–0.90, space heritage, nonporous construction and Be among successfully used substrates. It does not supply areal mass. Its web heading calls the 0.15–0.18 optical range “Solar Reflectance”; the model treats that range as absorptance only as an explicitly unresolved interpretation. No claim of a light qualified Be finish rests on it. [ENBIO](https://enbio.eu/solar-white/).

**FEP and polyimide tapes.** Selected catalog values are in `COATINGS.json`, with page numbers. Silver/FEP at 0.5 mil has α≤0.09, hemispherical ε≥0.40 and 88 g/m² including 3M966; its part number is TBD. The 1-mil stocked-number construction is 115 g/m². The bare film's 28 g/m² is not an installed-tape weight. The model adds 5% for overlap. Al/FEP and Al/polyimide alternatives are screened separately; thin aluminum-backed FEP and ordinary polyimide do not all meet the thermal criterion. Adhesion data are on stainless steel, not Be. [Sheldahl Red Book, pp. 51, 63, 65, 67, 89](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf).

**FEP durability.** Chemours reports very low moisture absorption and long outdoor stability for the base film, while excluding type C from its outdoor recommendation. That evidence does not qualify silver edges, acrylic attachment, overlaps or repairs. These remain separate humidity, peel and UV-aging questions. [Chemours film bulletin](https://www.chemours.com/en/-/media/files/teflon/teflon-fep-film-properties-bulletin.pdf).

**Deposited metal/dielectric stacks.** NASA's patent gives the classical CCAg layer recipe and an example with 80 alternating alumina/silica pairs, a NiCr tie layer, silver reflector and ITO topcoat. Applying bulk-density proxies gives 9.326–11.179 g/m² for classical CCAg and 7.575 g/m² for the multilayer example. These are our calculated deposited-layer masses, not catalog installed weights. Direct deposition on Be avoids a carrier film only as a manufacturing projection. Substrate roughness, stresses and adhesion remain material conditions. [NASA patent US 11,391,493](https://patents.justia.com/patent/11391493).

NASA separately reports multilayer variants below 2 µm, hemispherical emittance above 0.80 and absorptance below 0.09. Applying those class-level optical values to the patent's particular recipe and Be is a projection. The classical comparison uses α=.09, ε=.65; its optical statistic and surface-finish transfer also need confirmation. A 10% installation mass allowance is added to both. [NASA 2018, p. 39](https://ntrs.nasa.gov/api/citations/20180002012/downloads/20180002012.pdf), [NASA 2015, p. 19](https://ntrs.nasa.gov/api/citations/20150018109/downloads/20150018109.pdf).

The density calculation uses 3970 kg/m³ alumina, 2648 silica, 10500 silver and 7200 ITO. These are bulk material proxies, not measured deposited densities. NiCr uses an assumed 8400 kg/m³ for its 50 nm tie layer. [Alumina](https://www.lesker.com/newweb/deposition_materials/deposition-materials-notes.cfm?pgid=al6), [silica](https://www.lesker.com/newweb/deposition_materials/depositionmaterials_sputtertargets_1.cfm?pgid=si5), [silver](https://de.lesker.com/newweb/deposition_materials/depositionmaterials_sputtertargets_1.cfm?pgid=ag1), [ITO](https://www.lesker.com/newweb/deposition_materials/pdf/msds_ito.pdf).

The sources establish space applications, not the required atmospheric humidity/UV/rain life or adhesion to this Be lot. NASA also describes CCAg as vulnerable to handling damage in a flight mechanism. A thin optical coating cannot be assigned a structural or weathering qualification by its mass. [NASA mechanism report](https://ntrs.nasa.gov/api/citations/20140008875/downloads/20140008875.pdf).

**Bare and oxidized Be.** A historical NASA entry for chemically polished Brush QMV Be gives α=.50 and hemispherical ε=.10; it also notes corrosion-driven optical changes. That surface fails the requested daytime thermal benchmark in our model. A matched native-oxide thickness/optical pair was not established, so the oxidized-Be row has no invented factor or mass. [NASA, printed p. 48](https://ntrs.nasa.gov/api/citations/19690012311/downloads/19690012311.pdf).

## Moisture and primers

**AF 163-2U.** Four historical NASA records give WVR 0.09–0.20% and TML 2.59–4.85%, under differing cure histories. WVR is water regained over 24 h at 25 °C/50% RH after the vacuum test; it is neither full equilibrium uptake nor a 200 °F cure qualification. TML includes non-water losses. The main model uses the high WVR as a clearly identified added-water proxy, and preserves 040's nominal volatile pressure allowance without subtracting TML from structural mass. Exact rows and reference numbers are in `sources/nasa-outgassing-af163.json`. [NASA database guide](https://etd.gsfc.nasa.gov/capabilities/outgassing-database/user-guide).

**High-water sensitivity.** Yasuoka tested AF163-2M, cured at 121 °C, as approximately 1.21 mm free adhesive plates. After 70 °C vacuum drying to stable mass, samples were immersed in 70 °C water. Fitted absorption terms were 8.72–9.16 wt%, with dissolution also present; final net mass gains were lower. That is evidence for a severe wet-material sensitivity, not a room-humidity 2U uptake value. The reported diffusion coefficients are absorption fits, not a guaranteed dry-out time through metallic faces. [Yasuoka 2022, DOI 10.1299/transjsme.22-00284](https://www.jstage.jst.go.jp/article/transjsme/88/916/88_22-00284/_article/-char/en).

**Structural primer.** 040's explicit joining baseline has zero separate structural-primer mass and a 5 g/m²/interface sensitivity. This card charges both interfaces: 10 g/m² external area. EC-3917 provides humid-environment durability evidence for an adhesive system but no matched moisture isotherm in the sources examined. Its stated cure conditions also differ from the selected 200 °F bond cure. The 1% moisture fraction used here is an allowance. [3M EC-3917](https://www.3m.com/3M/en_US/p/dc/v000088346/).

**Paint primer.** MLP-300-AZ has nominal dry thickness 0.75±0.25 mil and dry density 1 g/cm³: calculated primer alone is 12.7–25.4 g/m². This is distinct from the structural primer. Its source lists no Be moisture uptake, and AZ's substrate guide does not list Be. It is not required on top of a directly deposited CCAg tie layer by assumption; any actual Be preparation layer must be weighed. [MLP-300-AZ](https://www.aztechnology.com/product/29/mlp-300-az), [AZ substrate guide](https://www.aztechnology.com/uploadimage/materials-substrate.pdf).

**5056 core.** Hexcel describes the CR III protection as an organometallic polymer system and provides salt-spray strength-retention evidence. It does not give water uptake for this core grade. Treating aluminum metal as nonabsorbing does not eliminate moisture on the coating, nodes, contamination or cell surfaces. The 0.1 wt% core value is the inherited planning assumption; the bounded NASA query found no “5056” record. [Hexcel CR III sheet](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).

**Finish moisture.** The FEP film has a source value below 0.01 wt% under its test, but no matching uptake for the whole 3M966/metal/FEP construction was established. The model assigns 1% to its adhesive and 0.01% to FEP. It assigns 1% to deposited-coating mass and seam polymers as sensitivity allowances. No measured CCAg or primer uptake is implied. AZ-93 can retain moisture: NASA observed removal in a <1% RH dry box or high vacuum, without giving the gravimetric inventory required here. [Chemours](https://www.chemours.com/en/-/media/files/teflon/teflon-fep-film-properties-bulletin.pdf), [NASA AZ-93 study](https://ntrs.nasa.gov/api/citations/20110022540/downloads/20110022540.pdf).

AZ-93 curing itself uses controlled humid conditions in the cited NASA application study. It would be incorrect to replace the maker's cure with unrestricted dry-gas processing. [NASA application study](https://ntrs.nasa.gov/api/citations/20205006191/downloads/CTCC%20Coating%20Study%20Report.pdf).

## Dry-out choices and water outside the hull

The bake scenario uses 70 °C as a demonstrated *coupon preconditioning temperature* from the AF163-2M study, with a **projected** 90% reduction of the modeled material-water inventory. It requires measured stable mass/water content; no duration or hull-wide achieved residual is claimed. All bake equipment is ground equipment. A 125 °C ASTM/NASA outgassing test is not silently prescribed for the selected 200 °F cure.

Dry-gas assembly receives **no removal credit for water already in materials**. Five ideal well-mixed enclosure exchanges are costed as a ground-gas scenario; they reduce airborne concentration by exp(−5) only under that mixing assumption. Pre-drying is a separate operation.

Onboard desiccant retains captured water aboard. The modeled bed has 10 wt% usable capacity and a 95% vapor-capture scenario; both are projections at hull pressure. The bed is sized for 110% of the initial modeled water/volatile inventory plus 0.1(R/10)³ kg ingress reserve, with a 2 kg cartridge. BASF's 4A catalog capacity is 21 wt% at 25 °C/80% RH; it is not the chosen vacuum capacity. Ground desiccant discarded before launch instead requires a measured final inventory. See the pinned BASF brochure in `sources/`.

External water is retained in the main rows. Separate zero-exterior-water rows describe a dry operating condition. Neither baking nor an internal sorbent establishes that condition. At the inherited 1 kPa water partial pressure, NIST's Antoine coefficients give a dew point of approximately 280 K. The dry-surface nighttime predictions fall below that temperature. This identifies a condensation/frost concern; it does not predict a retained layer or its duration. [NIST water vapor-pressure data](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=4).

## Retrieval record

Primary PDFs and accessible HTML are pinned locally. Sheldahl, ENBIO and the patent were readable through the web tool but their direct HTTP downloads returned 403/406/404; source-extract records identify these cases rather than claiming a local PDF snapshot. No source, supplier or other seat was contacted.
