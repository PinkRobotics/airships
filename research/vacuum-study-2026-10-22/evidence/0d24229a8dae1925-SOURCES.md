# MAINLINE-041 source and assumption ledger

Every inherited or sourced material value is **QUESTIONABLE**. Its transfer
to this frame, thin curved members, bonded joints or membrane is **PROJECTION**
until qualified. `INPUTS.json` records exact inherited copies and hashes;
`intake/technical/SOURCES.json` records this turn's additional browser reads.
The underlying archived sources below are primary manufacturer documents,
authored methods or software documentation.

| Quantity | Value used | Source and limitation |
|---|---:|---|
| SiC Young modulus | 410 GPa | Dispatched 022d/011b assumption. The pinned current Hexoloy-SA sheet gives 430 GPa; the comparison deliberately retains 410. |
| SiC density / Poisson ratio | 3,100 kg/m³ / 0.14 | Saint-Gobain Hexoloy-SA data, pinned through own 026. Typical values do not establish production variability. |
| SiC compression | 3.9 GPa | Hexoloy-SA typical compression; not an allowable for meter-long thin arcs, joints or contact. |
| SiC tension screen | 15.586 MPa | Fixed rounded 025/022d full-frame reliability projection, inherited unchanged. No new failure probability is inferred. |
| Zylon HM modulus | 270 GPa | Toyobo technical data, April 2023, filament value. |
| Zylon density / filament strength | 1,560 kg/m³ / 5.8 GPa | Same Toyobo PDF. The 0.6 strength factor, two orthogonal plies and 12 μm total floor are assumptions. |
| Zylon effective strength per total gauge | 1.74 GPa | 5.8 GPa ×0.6 /2, retaining the source's two equal directions. |
| CFRP compression / density | 1,470 MPa / 1,550 kg/m³ | Legacy Toray T700S sheet supports the compression scalar; composite joint density is an assumption. |
| Adhesive shear | 28.9 MPa | Henkel EA 9394 bulletin, July 2015, prepared-aluminum lap-shear result. SiC, curved bonds, peel and service exposure are unqualified. |
| Global knockdown | 0.2 | Inherited 022d screening assumption, not measured on this frame. |
| Local shell / crookedness | 0.6Et/ro × gamma / L/1000 | Inherited 022d conventions. NASA SP-8007 supplies the axial-cylinder context, not qualification for curved ceramic tubes under bending. |
| Nodes / systems | 20 g per node / 100 kg | Inherited mass allowances, not a completed hardware bill. |

[Saint-Gobain Hexoloy-SA data sheet](https://www.ceramicsrefractories.saint-gobain.com/sites/hps-mac3-cma-pcr/files/assetbank_media/hexoloy-sa-sic-en-1013-tds-215398.pdf)
is archived as `intake/technical/Hexoloy-SA.pdf`; the exact working source URL
is also preserved in `INPUTS.json`.
Toyobo's **ZYLON technical information, revised April 2023**, is pinned as
`intake/film/zylon-hp-fiber-data.pdf`.

The [legacy Toray T700S sheet](https://www.rockwestcomposites.com/downloads/T700SDataSheet.pdf)
is retained as `intake/joint/toray-legacy.pdf`. This card does not silently
replace it with a later edition. The sheet's fiber density is a different
quantity from the assumed composite sleeve density.

The [Henkel EA 9394 bulletin](https://dm.henkel-dam.com/is/content/henkel/EA-9394-Aero)
is retained as `intake/joint/henkel-ea9394.pdf`. Its scalar shear datum is
used in an explicit ring-bond projection; no claim of tested SiC adhesion is made.

[NASA SP-8007 Rev.2](https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf?attachment=true)
is carried through the pinned CHECK-022d source ledger. The present work
retains the owner's axial local convention and separately exposes a
peak-compression sensitivity, without calling that sensitivity a validated
interaction law.

The pressure-volume, beam and joint equations used here are specified in
`METHODS.md` and executable source. Additional method references:

- [Vetter et al., corotational beam formulation](https://romanvetter.ethz.ch/publications/papers/2/preprint.pdf), archived PDF from own 026.
- [Bleyer, elastic 3D beams](https://bleyerj.github.io/comet-fenicsx/tours/beams/beams_3D/beams_3D.html), archived HTML; supports the section-resultant conventions.
- [Bleyer, beam buckling](https://comet-fenics.readthedocs.io/en/latest/demo/beam_buckling/beam_buckling.html), browser-read this turn and archived from own 026; this turn's direct download returned HTTP 403.
- [SciPy eigsh](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html), archived from own 026; supports the distinction between smallest algebraic and shift-invert selection.
- [Oasys GSA material definitions](https://docs.oasys-software.com/structural/gsa/references/hidr-data-mat-anal/), archived HTML; directional axial modulus alone does not complete a fabric's constitutive data.

No source here establishes a gas-tight, durable 0/90 membrane, the required
joint rotational stiffness, long-arc strength statistics, or manufactured mass.
