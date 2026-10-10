# P4.5 formal sufficient conditions — PAPER, conditional only

All physical matrices, chi, measured masses, confidence and applicability are UNKNOWN/NULL. This note derives sufficient conditions for interpreting future evidence; it neither supplies measurements nor qualifies a physical model.

## Work-conjugate nine-port interface

Choose a registered right-handed common datum and a fixed j=1..9 port order. Axial forces t are tensile-positive, N; conjugate q are extension-positive, m, so t^T q is work. At port j the ordered small displacement is (ux,uy,uz,thetax,thetay,thetaz), m/rad; conjugate wrench is (Fx,Fy,Fz,Mx,My,Mz), N/N*m. With direction n_j and lever r_j, the wrench column is w_j=(n_j,r_j cross n_j). The reciprocal relation q_j=w_j^T y_j includes rotational displacement of the attachment. Stack these columns in W; projected anchor C_s=W^T H_s W has m/N units. H_s may be a larger constrained/condensed port compliance; the output contract does not require an invented measured54-dimensional matrix.

For any invertible compatible change of datum/coordinates y'=G y, force transforms as f'=G^(-T) f. Therefore H'=G H G^T and K'=G^(-T) K G^(-1). These formulas include translational shifts and moment arms, not merely rotation of a3x3 block. A common reference length can scale rotations and conjugate moments before mixed-unit comparisons. All comparisons below use a single compatible work-conjugate basis.

Nine independent small force patterns with all nine axial responses identify a linear C_s at one fixed pretension/contact/support/environment state: Q=C_s T, rank(T)=9. This supplies81 entries; verified reciprocity allows45 independent entries. The nine patterns are experimental input directions, not nine statistically independent specimens. Full transfer into an unspecified number of global output channels has no universal81-entry size. Linear identification, reciprocal/passive response and uncertainty are separate claims.

## Local compliance bound and coupled assembly

For all19440 active edges let D=diag(L_e/(E_e A_e)) be the positive cord compliance. Both ends' separately bounded compliance contributes C_end. Stack every site's force-incidence maps in S, using the force signs and end identities in C01; C_ports includes every within-site AND offsite response admitted by the chosen global frame model. Eliminating those passive internal responses yields C_conn=C_end+S^T C_ports S, and K_edge=(D+C_conn)^(-1). This formula assumes work-compatible assembly, no missing internal mechanism, linear tangent response and no double elimination of a shared physical frame.

For 0<chi_star<=1, suppose C_conn is symmetric positive semidefinite and

    0 <= C_conn <= (1/chi_star - 1) D.

Then D+C_conn <= D/chi_star. Positive-definite inversion reverses this order, hence

    K_edge >= chi_star D^(-1).

This is a sufficient axial NETWORK comparison. It is not established by checking C_s diagonals or isolated cord-end scalar tests. For a symbolic counterexample, a passive nine-port matrix c*1*1^T has diagonal c but common-direction eigenvalue9c: nine compliant ports can move together even when every diagonal passes an isolated limit. c here is symbolic, not a new measured case.

A collection of LOCAL bounds is enough for the above NETWORK condition only after a compatible global decomposition is proved. For example, require no unbounded intersite term, C_s <= R_s, and

    C_end + sum_s S_s^T R_s S_s <= (1/chi_star - 1) D.

The allocation must cover both endpoint sites of each cord, its two end compliances and all attachment/frame effects once. A degree9 interface alone cannot certify this decomposition. If measured frame response is included in C_ports, the same frame's elasticity cannot also be added as a separate independent compliance or credited again as retained structural stiffness. Alternatively retain the frame's coordinates explicitly and compare the full coupled energy before elimination. The reference and actual representations must describe the same physical load path.

The independent-series scalar specialization is k_eff=1/(L/(E A)+c_total). Relative to k_cord=E A/L, retention is 1/(1+E A c_total/L). Its sufficient condition c_total <= (1/chi_star-1)L/(E A) becomes c_total <= (1-chi_star)L/(E A0) at proposed A=A0/chi_star. At fixed c_total, attaining baseline E A0/L requires A>=A0/(1-E A0 c_total/L), with E A0 c_total/L<1. A nonpositive denominator supplies no finite-area solution. A model area increase therefore changes the permissible connection compliance; measured compliance cannot be treated as a fixed independently certified uniform chi. At chi_star=1 this independent positive-series model permits no additional compliance. No actual perfectly rigid joint is inferred.

## Global condition for a stipulated uniform multiplier

Assume the target model multiplies the cord-foundation contribution only. It does not degrade retained ring/crimp/compression terms, change fixedGM/gamma or introduce membrane/shear credit. At the same proposed areas define K_target(chi_star)=K_retained+chi_star K_cord,ideal, with identical prestress conventions, supports, geometry and coordinate registration. The precise physically meaningful stiffness is the tangent constrained assembly, not a separate per-port stiffness ratio.

Let x=Qv enforce the same constraints. Internal coordinates z are shared between actual and target representations. Define reduced energy as inf_z (x,z)^T K (x,z)/2, on the same compatible domain. If a complete full-assembly comparison K_actual >= K_target holds uniformly there, taking the two infima preserves the inequality. Equivalently, once a well-defined compatible condensation is justified, require

    Q^T [K_actual,cond - K_target,cond(chi_star)] Q >= 0

for EVERY admitted load/pretension/contact/environment/history state. Use certified measurement uncertainty to prove a lower envelope, not fitted central estimates. Project out documented rigid/gauge modes; on the remaining reference energy space the target must be positive definite, or explicitly restrict the comparison to its positive-energy quotient and separately exclude actual unrestrained mechanisms. Singular connection compliances represent rigid constraints only with compatible force ranges; singular stiffness cannot be inverted as though all ports were supported.

The axial NETWORK bound above implies the cord term of this global inequality only when B and its adjoint B^T, all constraints and eliminations are identical and complete, while retained/prestress contributions are demonstrably unchanged or conservatively bounded. Geometric stiffness from compression can be destabilizing; it cannot be silently assumed positive. Slack, contact changes, creep, slip, geometric/load transfer changes and unqualified material ratings break these prerequisites. No independent scalar end limit, local9x9 measurement or rank9 experiment alone establishes the full global condition.

A comparison restricted to any selected modal directions would not establish the unexamined modes or all4320 sites. Transporting a bound to a different domain would require evidence of the common operator, projection, mode/ring/plane transfer, reference normalization and stated assumptions. Physical extrapolation requires a supported class/state envelope. No modal-domain acceptance is asserted; global comparison and actual chi_star remain UNKNOWN.

## Pool consequence and preserved uncertainty

For bookkeeping only, stipulate a symbolic additions pool C-U/chi, where C and U are assumed budget and baseline cord-allocation symbols. This is not a measured pool, feasible witness, optimization bound or certificate. Its actual values and fit are UNKNOWN. Every addition is assigned to this same pool once; no threshold, infeasibility or certificate-slack outcome is asserted.

All34 canonical ledger rows, scientific values and numeric types, unqualified assumptions and actual_mass_t=NULL entries are retained in MASS-INVENTORY.json. Its duty map prevents a support, fixture, anchor, end, reinforcement or retained-member replacement from being free or billed twice. Gas, lost displacement, payload and useful reserve debit the same pool. Complete flight inventory and actual material/connection/frame/tautness/global-transfer evidence remain UNKNOWN.
