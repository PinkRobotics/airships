# Calculation that becomes admissible after source/test closure

**PROJECTION: specification only; no authorization or execution of a new sweep.**

First establish a released material/process dataset. It must contain the finished
sheet's orthotropic elastic tensor, directional and biaxial compressive
stress–strain/failure data at the actual minimum gauges, formed/cured condition
and service temperatures. It must also contain the CR III coupon response in
normal compression and both transverse shears through peak, crushing,
unload/reload and densification, with in-plane coupling and mixed loading.
Record ribbon directions, density, cell geometry, perforations, specimen thickness
and lot scatter. Neither a PVC foam fit nor a numerical regularization supplies
these measurements.

For the exact bond and scarf, release thickness and installed mass, Be surface
preparation, primer, cure pressure/time/temperature, stress-free locking and
relaxation, normal/shear traction, mixed-mode fracture and unload/cycling data.
Include process witness panels and the full-size forming/cure/seam article
proposed by 042. Record contour and gauge maps before forming, after cure,
after closure/support removal and over the specified thermal cycle. A bonded
coupon with another carrier, substrate or cure is not the required release.

The first admissible FE case is one measured curved article with its measured
initial shape, gauge, core orientation and seams. Fit the material law on coupon
data; predict the article without adjusting parameters to its collapse load.
Use finite-strain orthotropic elasticity/plasticity or a validated cell model,
with directional crushing and unloading, a measured mixed-load interaction,
and a regularized damage law with objective dissipated energy if softening is
entered. Check positive-definite initial stiffness, consistent units, stress
measures and material-frame updates. Preserve stress and strain histories
through forming/cure/import rather than silently resetting them.

Use a three-dimensional model for the article's actual ribbon layout and seams,
with measured adhesive/contact behavior, support conditions, thermal residual
state and follower pressure. A whole-hull calculation must also resolve
nonaxisymmetric modes and orientation changes between panels. The existing
axisymmetric Q8 tools can provide homogeneous controls, but cannot validate that
layout by themselves.

At the measured article and each subsequently selected 057 geometry, compare:
first face yield or qualified brittle limit; first core normal/shear/mixed limit;
first bond/seam failure; first pressure-control instability; and the later
postbuckling branch. Retain them separately. Use displacement/arc-length control
where necessary to expose a descending branch, including admissibility and
energy checks. A solver stop or a later larger maximum is not the first
pressure-control capacity.

Refine mesh, through-thickness resolution and load increment on those selected
cases until the design-changing result is stable to a predeclared engineering
tolerance and the material energy law remains objective. Use independent
membrane and linear-eigenvalue controls and a withheld physical article.
Only then test the governing defect widths and an actual measured defect field
at R10/20/30. This is the next scientific evidence path; 062 itself runs none of it.

This specification carries 056's directional-law requirements. The inspected
[Altair honeycomb material documentation](https://2023.help.altair.com/2023/hwsolvers/rad/topics/solvers/rad/mat_026_honeycomb_lsdyna_r.htm)
illustrates the need for separate directional curves; it does not supply CR III
material data. The scalar normal/shear limits in
[Hexcel Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf)
are initial source anchors only. Source/test gaps remain in `NFI.json`.
