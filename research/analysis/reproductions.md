# What the two shell reproductions establish

The executable is [reproductions.py](reproductions.py); its inputs and outputs are exercised by
[the labelled checker](../validation/check.py) and published in [the comparison report](../validation/report.md).
The source records, tolerances and failures belong to that report, so this note does not maintain
a second set of numerical results.

Akhmeteli and Gavrilin's final Discussion geometry is inserted into their equation (7).
That equation approximates each layer by area times thickness. It supplies shell mass and,
by subtracting from displaced-air mass, payload. Both are compared literally, with the original
rounding tolerances. The separately reported concentric-layer calculation expands the geometry
into finite spherical volumes; it is our geometric diagnostic, not an equation the paper prints,
and does not replace a missed comparison. Equation (9) is their semi-empirical sandwich term,
not classical buckling of a homogeneous sphere. The code labels it accordingly. It does not
rerun their finite-element analysis or reproduce the wrinkling and dimpling safety checks.

Jenett, Gregg and Cheung's equation (33) gives membrane stress. Section IV.D divides the load
among lattice elements, then sizes tubes by Euler buckling at a fixed radius/wall ratio.
The reproduction calls `vacuum-cell.py:ship_section` and `_ship_sigma_euler`, rather than
copying their section or Euler equations. These functions bind a project laminate card, so
Euler load is rescaled by the exact ratio of the paper's modulus to the bound modulus; mass
uses the paper's density instead of the section helper's laminate-specific `kgPerM`.
Neither the project material table nor its safety factors are changed.

A local sizing diagnostic explicitly interprets Figure 4 as a regular octahedron with pitch
as its axial diagonal and pinned members. It cannot establish that these are the Table 2
implementation's conventions. The missing inputs for a complete reproduction are its member
inventory (including edge sharing and boundary truncation), its pitch-to-member-length
convention, and its Euler effective-length factor. Table 1's voxel count alone does not specify
that inventory; scale-invariant design ratios do not determine how shared members were billed.
The function can accept an explicit equivalent member count for a conditional calculation,
but the labelled Table 2 rows leave it absent rather than fitting it to the target lift.

No atmosphere function is needed when a paper stipulates air density directly. No homogeneous
sphere primitive is substituted for a sandwich stability formula, and no volume-filling octet
model is substituted for the spherical lattice shell. This is a reproduction of the parts of
the published methods that are specified, not an assertion that either design can be built or
that the project's vehicle mass allowance is demonstrated.
