CHECK-041 uses exact file pins in `INPUTS.json`. A verified hash establishes which document was used; it does not qualify the material or transfer model.

| Input | Source and audit | Status in this check |
|---|---|---|
| Radius 10 m, pressure 95,460.8379139 Pa, closure mass 4,889.44215019 kg, reserve alternatives | Filed 022d witness JSON and MAINLINE-041 methods; treated as fixed problem inputs | QUESTIONABLE reference inputs |
| SiC density 3,100 kg/m³, Poisson ratio 0.14, nominal compression 3.9 GPa | Saint-Gobain Hexoloy SA sheet [source link unavailable in this public projection], property table | QUESTIONABLE vendor data; compression is not a full-size tube allowable |
| SiC E=410 GPa | Inherited comparison input; the same vendor sheet gives 430 GPa | PROJECTION; difference disclosed and retained |
| Fixed tensile screen 15.586 MPa | Inherited 022d size-transfer projection; no new tensile calibration in 041 or this check | PROJECTION |
| Zylon HM E=270 GPa, strength 5.8 GPa, density 1,560 kg/m³ | Toyobo April 2023 technical sheet [source link unavailable in this public projection], filament table | QUESTIONABLE filament data |
| Film effective strength 1.74 GPa per total gauge | 5.8 GPa × assumed 0.6 × one-half gauge in each direction | PROJECTION; does not establish a laminate or attachment allowable |
| Sleeve compression 1,470 MPa | Toray T700S legacy sheet [source link unavailable in this public projection], composite table normalized to 60% fiber volume with its stated resin | QUESTIONABLE coupon datum; sleeve transfer PROJECTION |
| Joint density 1,550 kg/m³ | Declared assembly assumption; Toray's 1,800 kg/m³ is a fiber datum and is not substituted | PROJECTION |
| Adhesive shear 28.9 MPa | Henkel EA 9394 sheet [source link unavailable in this public projection], room-temperature lap-shear table on prepared 2024-T3 aluminum | QUESTIONABLE test datum; SiC/CFRP joint transfer PROJECTION |
| Global multiplier 0.2 | Inherited screening convention, uncalibrated for this frame | PROJECTION |
| Local-wall γ·0.6Et/r_o and peak-compression interaction | Declared formulas in the filed 041 methods; no curved ceramic tube qualification supplied | PROJECTION |
| L/1000 bow, circular-cap sag, node/system allowances, ideal rigid/pinned joints, perfectly attached film tangent | Declared design/model assumptions | PROJECTION |

The SiC sheet's nominal compression, modulus, and density are successfully transcribed. They do not supply a strength distribution, full-size compression/tension allowables, manufacturing tolerances, or joint-contact qualification. This is a limit on inference, not an arithmetic discrepancy.

The independent beam energy uses the formulation discussion in [Vetter et al.](https://romanvetter.ethz.ch/publications/papers/2/preprint.pdf). [SciPy's eigsh documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html) supports the eigenvalue-selection terminology. Neither source validates the assembled vehicle or makes the two independent finite-rotation formulations identical.

The owner report, CARD, RESULTS, METHODS, source PDFs, nonlinear states, linear response arrays, and execution metadata are copied only through exact filed pins. File hashes and sizes were checked before use. Owner program contents are excluded from this intake.
