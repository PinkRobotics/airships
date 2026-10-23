# Source and assumption ledger for the 022b/022c check

Every numerical scenario remains **QUESTIONABLE**. A manufactured filament, coupon or flat film does not establish the proposed full structure. Unvalidated material/process transfers are **PROJECTION**. All inherited artifacts below were copied only after recording their supplied hashes; `INPUT-PINS.json` records the verification. No owner script was run or imported.

| Input | Value used | Source chain and disposition |
|---|---|---|
| Sphere, pressure and lift | R=10 m; p=95,460.8379139 Pa; lift=4,889.44215019 kg | Pinned COMMON and original 022 inputs/code. Assigned scenario, QUESTIONABLE. |
| Systems and node mass | 100 kg; 0.02 kg/node | Original 022 mass contract. QUESTIONABLE estimates. |
| Reserve | 244.4721075095 kg or 411.2989440716474 kg | Five percent of lift, or 535.9459071525378−124.6469630808904 from the carried 019 budget. Arithmetic checked; the underlying equipment budget remains QUESTIONABLE. |
| Five-percent joints | 0.05×(tube+film+node mass) | Original 022 contract. This is different from 011b's 0.05×tube mass. Reproduction preserves the stated 022 rule. |
| SiC | E=410 GPa; density=3,100 kg/m³; compression input 3,900 or 380 MPa | Original 022 inputs and prior 011b inheritance. QUESTIONABLE properties. Both full-tube compression inputs remain PROJECTION as allowables; 025 establishes neither a qualified compression allowable nor a size law. |
| Bow and section | a₀=arc length/1,000; exact circular annulus | Stated 022 model. QUESTIONABLE geometric imperfection assumption. |
| Global stiffness | k=0.2; coefficients 4√(3/2) and 4 | Stated triangular/two-way surrogate. k=0.4 doubles only the global mode. Real joint rotational stiffness and a discrete curved frame remain unqualified. |
| Local shell | 0.6Et/rₒ multiplied by γ | NASA correlation is implemented correctly. The inherited 0.6 coefficient and outer-radius convention are explicit. Application to the long curved ceramic struts remains PROJECTION. [NASA SP-8007 Rev.2, pp.23–25](https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf). |
| Mylar 850H | 22 ksi=151.684660449916 MPa; 1,400 kg/m³; minimum candidate gauge 12.192 µm | `inputs/022/INPUTS.json` points to the supplied Mylar sheet. QUESTIONABLE coupon/film inputs, not demonstrated long-term biaxial allowables. The present check verifies their arithmetic use and traceability, not a new material qualification. |
| Carried 011 film | 1.5 GPa; 970 kg/m³; 80 µm lower search gauge | Original inherited projection. **PROJECTION**: no demonstrated complete membrane specification. |
| Kapton HN | 115.5 MPa; 1,420 kg/m³; 25 µm lower gauge | Pinned 024: 231 MPa ultimate multiplied by an assumed 0.5 knockdown. Its source PDFs are pinned by `inputs/024/INPUTS.json`. Existing film, QUESTIONABLE allowable transfer. |
| Zylon HM 0/90 | Filament stress 3.48 GPa; density 1,560 kg/m³ | Pinned 024 derives 3.48 GPa from 5.8 GPa×0.6, then explicitly doubles total thickness for two directions. The 022b/022c scalar film formula omits that factor. The membrane is **PROJECTION**; the 12 µm search floor is not a qualified Zylon membrane catalogue gauge. |
| Sleeve/wrap coefficients | Ti 2.950×10⁻¹⁴; CFRP 5.807×10⁻¹⁵ kg·m/N² per end | Pinned 023 derives C=ρ/(2πστ), with τ=28.9 MPa. Exact source coefficients and rounding differences are in `SOURCE-CHECKS.json`. The adhesive test used aluminum adherends; transfer to SiC is QUESTIONABLE. The CFRP wound joint is **PROJECTION**. |
| Braze and pin comparisons | 130.611003 kg braze at the reclosed held-radius budget; pin bearing 11.8894 GPa | Independently reproduced from the pinned 023 sizing equations and inputs. These are calculations, not proof of joint performance. |
| 022b sag | lift×s/(16R) | Approximate crown s/24 with half-crown mean. Explicit QUESTIONABLE model. |
| 022c cap sag | Circular cap of radius s over triangle inradius; lift×3×mean/R | Pinned 024 sag report. Correctly reproduced as the chosen circular-cap approximation. It is not an exact triangular membrane surface integral. |
| 022c membrane sensitivity | mean=s/40 | Stated sensitivity. The resulting factor over the chosen cap mean is 1.16600297093, not the order's approximate 1.19. Its use on two-way cells also needs a cell-specific justification. |
| Tensile sensitivities | Ft=7.192, 15.586 or 380 MPa; zero-tension boundary | Explicit **PROJECTION** screens, carried from 025's assumptions or typical flexure. These are not qualified tensile or compressive allowables. Actual positive-stress volume, surface populations and contact fields remain unknown. |

The report body's two quoted prior-check values reproduce at **1.2052348902087753** and **1.1304496317335904**. They use the earlier fixed-film/chord model with 50 kg/zero reserve or 100 kg/five-percent reserve. They are not outputs of 022b's new arc-length, film-thickness and sag scan.

The material-value chain is present, but its limitations must travel with the results. In particular, “today” in a case label cannot qualify the full ceramic member, adhesive/ceramic joint, gas barrier, or coupled instability model.
