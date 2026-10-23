# REVIEW-A1 admissibility before numerical checks

Scope: the 17 claims listed first in LOAD-BEARING.md, covering 056 and 062 only.
No owner executable code is read or run.

The pinned reports, input tables, primary PDFs, raw pressure path and saved
finite-element mesh/state are admissible as **numerical evidence of the declared
conditional models**. They are not measurements of a qualified pressure hull.
Units are checked separately: the 056 field calculation uses mm/N/MPa, while
062's geometry/mass arithmetic uses m/Pa/kg and reports amplitudes in mm.

The 056 pressure state permits an independent virtual-work check. Reconstruct
quadratic serendipity interpolation from its nodal polynomial basis; derive the
deformation gradient, logarithmic strain, elastic stress from the saved plastic
strain, internal force and current-surface pressure force. Infer pressure from
equilibrium without using the saved pressure in that calculation. This checks
the decisive equilibrium state and independently identifies the sampled path
maximum. It does not rerun the complete plastic/contact history or validate
three-dimensional stability. The state file's undocumented tensor/point layout
must be checked explicitly; any ambiguity will be reported.

The source paper's hydrostatic foam calibration, steel-axis interpretation and
geometry/state import remain incomplete. A new physical calibration or
expensive nonlinear sweep would therefore not remove the source ambiguity.
This review performs focused field/accounting checks, not another parameter
sweep. The CR III catalog gives directional anchors but not the installed
nonlinear law; Be tensile yield is not a processed compressive allowable.

The two reported linear eigenvalue anchors also admit a direct independent
check: construct a fresh perfect hemisphere mesh, integrate small-strain
isotropic elasticity, solve the unit-pressure preload and form geometric
stiffness from that stress. The specified elastic constants and clamped
boundary conditions suffice for these two conditional anchors. These are
spot checks at the reported resolution, not a new nonlinear material sweep.

062's calibrated tolerance hypothesis can be independently checked by
eliminating its coefficient between the reference and target equations.
Its cost assumptions can be checked as arithmetic but remain unquoted
PROJECTION rates. Its complete mass claim can be checked by adding the stated
retained hardware and growth to the pinned upstream accounts. Precedents will be
spot-checked for measurement type rather than converted from RMS to a local
maximum.

Source and model gaps become NFI rows. Demonstrated numerical differences become
fix rows, explicitly unreviewed under the one-round process.
