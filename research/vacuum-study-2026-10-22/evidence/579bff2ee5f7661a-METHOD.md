**MAINLINE-028 calculation and carry**

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

The calculation is `python3 calculate.py` in this directory, or its absolute path from another directory. It uses only the Python standard library. `INPUTS.json` is the frozen input, and all output geometry is in SI units. The plotting helper is a separate optional presentation step.

Area is \(A=4\pi R^2\). Both faces use this same area, preserving the inherited thin-shell convention. The outer and inner exact areas are not substituted into only part of the inherited model. Each face carries \(N_f=pR/4\); the two faces together carry \(pR/2\). Neither N/m value is an adhesive stress.

For rectangular blanks, seam length counted once is \(L=A(1/a+1/b)\); individual skin seam length is \(2L\). This is an area approximation, not a spherical cutting pattern. A scarf with run/thickness ratio r consumes overlap \(r t_f\) in each blank dimension, giving \(L=A[1/(a-r t_f)+1/(b-r t_f)]\). The model therefore does not take the 020 zero-trim stock estimate as final scarf length. Curved cutting waste, polar caps and intersections remain NFI rows.

The two faces' scarf area per hull-seam metre is \(2t_f\sqrt{1+r^2}\). Its added adhesive mass is that area times the selected film areal mass. Complementary scarf wedges replace parent metal, unlike a full-thickness lap doubler. The membrane traction resolved on the scarf gives average shear \(\sigma_f r/(1+r^2)\) and normal compression \(\sigma_f/(1+r^2)\). End effects, biaxial redistribution, thermal residual stress and fracture are not represented by those averages.

The butt-strap width is \(W=2N_f/\tau_{\rm screen}\), because each side must transfer the full face resultant. Each face has a parent-gauge strap. Both skins add \(2\rho_f t_f W+2w_{\rm seam}W\) per hull metre. This screening arrangement is eccentric; a symmetric redesign needs its own installed mass and local buckling analysis.

A brazed scarf uses the same geometric area with the explicitly assumed filler gap and density. Its material shear number is a typical different-specimen result, not an allowable. Autogenous EB adds zero filler in the mass model, but retains the core-splice/sealing inventory and is evaluated at both 100% and assumed 80% parent compression strength. No evidence was found that selects the 100% assumption.

Core-splice material is `gap * core depth * density` per hull metre. The low-mass selected values and sealant allowance are owner projections, not measured installation minima. Primers are zero in the nominal arithmetic, with a separately declared 5 g/m²/line sensitivity; the residual allowance is stated so this exclusion cannot be mistaken for a demonstrated primer-free process.

Cell-edge braze mass is a separate filler-only screen. For hexagonal cells of flat-to-flat width s, unique wall length per projected area is \(2/s\). Two triangular fillets per wall, each leg a, have combined section \(a^2\). Thus \(w=\rho a^2 2/s\). It is not included as a validated alternative core in the SF optimization. Zero-filler diffusion or integral construction likewise has no quantified replacement-core mass and therefore no finite qualified hull result.

For optimization, structural mass S and core mass fraction f define
\[
t_f=(1-f)S/(2A\rho_f),\qquad d=fS/(A\rho_c).
\]
For each f, a bisection solves
\[
S+M_{\rm joining}(t_f,d)=0.95L_{\rm lift}-100.
\]
This replaces the original 5% joining allowance. The allowance is never added on top of explicit joining. A broad scan in f brackets the best solution; a local refinement resolves the maximum of the minimum modeled SF. The nominal stock case is checked on a four-times-denser scan. Exact reoptimized joining masses differ slightly from the original-geometry comparison in CARD.md, and are recorded separately.

Mode equations, with \(h=d+t_f\), follow the pinned 021 conventions:
\[
\sigma_0=Eh/[R\sqrt{1-\nu^2}],\quad
\sigma_{\rm crimp}=h^2G_c/(2t_fd),\quad V_c=\sigma_0/\sigma_{\rm crimp}.
\]
\(K_c=1-V_c/4\) for \(V_c\le2\), otherwise \(K_c=1/V_c\). Global SF is \(\gamma K_c\sigma_0/(N_f/t_f)\); face compression is \(\sigma_{\rm comp}/(N_f/t_f)\); crimp is \(\sigma_{\rm crimp}/(N_f/t_f)\). The inherited core-crush convention is \(\sigma_{\rm crush}/(p/2)\). Honeycomb wrinkling is \(b k_w\sqrt{EE_ct_f/d}/(N_f/t_f)\), with the pinned biaxial factor b. Equibiaxial dimpling is \(E(t_f/s)^2/[(1-\nu^2)(N_f/t_f)]\). This reproduces all six modes before applying new joining masses.

The table holds gamma and the wrinkle coefficient at 021-rev1's *needed* values, not its maximum optimism. The separate kd = 0.2 baseline is carried. For unchanged geometry and shear correction, global buckling SF is linear in kd; changing kd can change which mode governs. The optimizer is restricted to the same material/core family, and does not claim a global optimum across all materials.

The local interface displacement examples are constitutive screens, not solved buckling-mode amplitudes. Normal and shear stiffness through the actual joints must be measured. A crimp capacity derived from Gc cannot replace a bond shear-strength or toughness measurement. The optimized mathematical least SF excludes unknown core-bond modes; `overall_installed_hull_SF` is therefore null.

Learned: selective edge deposition is an evidenced low-mass laboratory route, while the lightest catalogue-film columns do not supply matching flatwise strength. A realistic complete joining inventory matters more than a filler-only number. Even a marginally sub-allowance commercial-film model loses its float-line SF to a small primer/tolerance increment. Panel-module size does not erase stock-sheet seams.

Deferred: structural and leak qualification, supplier thin-sheet dimensions, a true spherical panelization, installed joint stiffness, local nonlinear seam/disbond buckling, thermal distortion/fatigue and actual process/primer/repair mass. These require new measurements and are explicit NFI rows, not unfinished arithmetic.

Next event: one completed-card report to sciences, copied to co, xo and admiral-robotics-review-v2. CARD-028 names no executable successor; wait for the robotics seat's next assignment. Times are measured, never a budget.
