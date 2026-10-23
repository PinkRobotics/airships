# Lower-domain polynomial and finite-form contract

New owner paper derivation, not an evaluated coefficient field, matrix,
event or implementation. Inputs are the exact frozen form, admitted B and
the full-displacement tail/complement at their pinned scopes. The
representation below is deliberately explicit about its remaining
arithmetic/fit premise. It does not relabel B's original unbounded-rational
recipe as a bounded rounded implementation.

## Full-box approximation rather than a central-load error

The initial lower-domain worklist is J_j=[3j/512,3(j+1)/512], j=0..127.
Its single declared refinement level consists of both children of EVERY
J_j, not a favourable selected subset. Thus 128+256=384 distinct attempted
lower boxes are priced in the eventual worst case; each mesh uses the same
384 boxes. Reserve the other 129 of the frozen 513 for an unpriced upper
extension. No additional split, retry or precision increase is implied.
An eventual implementation may stop earlier; that does not alter the
inventory used for pricing. These are formulas for the future worklist,
not a generated mesh or load-response calculation.

On every box use its rational centre lambda_c, radius r<=3/1024 and
tau=(lambda-lambda_c)/r. On each of the frozen three-panel cells use its
exact midpoint x_c and half-length d_x, and xi=(x-x_c)/d_x. The coarse
outer half-length is (H-pi)/80<17/80<1/4, and the central one pi/40<1/4.
All three meshes have d_x>3/160. Keep exact geometry in these maps.

Approximate y by its tensor Taylor polynomial of degrees (25 in x,
24 in lambda), with coefficients scaled to xi,tau. Define the y_x
representative by differentiating that SAME polynomial. Approximate the
central G_x=sin(x)/10 by degree24 in xi, zero on the outer panels. Choose
dyadic coefficients with error strictly below 2^-150 per coefficient.
Use even reflection for y and odd reflection for G_x, and hence odd s.
No coefficient array is evaluated now. The finite arithmetic mechanism
that achieves this selection error is an explicit phase4 premise below.

Keep N=N_cl*lambda and the -nu*N part of Ny EXACTLY as affine parameter
terms in the polynomial form. Set shat=eta*(Ghat_x+yhat_x) and
Nyhat=(Et^2/R)*yhat-nu*N_cl*lambda. This is not a central Nbar, a deletion
of delta_N, or a claim of zero symmetric error for an endpoint lower form.
The same parameter lambda remains in every finite, coupling and
complement expression. Constants/geometry are exact mathematical
quantities whose eventual assembly enclosures must contain them.

## Uniform complex-parameter bound supplying the Taylor remainder

This is an analytic extension for remainder bounds, not physical coverage
above3/4. For any real lambda_c in[0,3/4], take the complex disk
|lambda-lambda_c|<=1/16. Choose the analytic positive-real branches of
a=sqrt((1-lambda)/2), b=sqrt((1+lambda)/2). On that disk

    |lambda|<=13/16, Re(a)>3/10, |a|<1,
    Re(b)>2/3, |b|<1, |Im(b)|<3/128.

Indeed Re(a)>=sqrt((1-Re(lambda))/2)>=sqrt(3/32)>3/10,
Re(b)>=sqrt(15/32)>2/3, and
2 Re(b) Im(b)=Im(lambda)/2. Also 16<H<17 and c>8/5.
These elementary geometric inequalities follow directly from
H=sqrt(600*sqrt(3))/2 and c=sqrt(273)/10.

Write E=exp(-2aH). Then |E|<exp(-48/5)<1/1024. One elementary justification
is exp(4/5)>1+4/5+(4/5)^2/2>2, so exp(48/5)>2^12.
|sin(2bH)| and |cos(2bH)| are less than exp(51/64)<3.
The clamped inverse denominator in B consequently obeys

    |d_det| >= (2/3)*(1-1/1024^2)-6/1024 >3/5.

Thus the formula has no inverse pole on these disks; the analytic branch
and its endpoint correction are retained, including at lambda0.

For v>=0 the complex Green kernel and its first three one-sided spatial
derivatives satisfy

    |K^(j)(v)| <= 3*2^j*exp(-v/4), j=0,1,2,3.

Expand the two exponentials of the sine/cosine representation: their
exponents have modulus less than2 and real part at most
-Re(a)+|Im(b)|<-1/4; their combined coefficient magnitude is less than
(1+|a/b|)/(4|a|)<3. K,K',K'' have no jumps, so the first three derivatives
of its convolution introduce no point-source terms. Integrating the
majorant on the real line gives |F^(j)|<=24*2^j. Since |p|<1/5 and
|lambda|/5<1/5, the particular solution has |y_inf^(j)|<5*2^j for j<=3.

At the end, |r0|<5, |r1|<10. The four M entries are bounded respectively
by 2,1,2,2. Cramer's rule and |d_det|>3/5 therefore give |C|<50, |D_h|<50.
Each of the two end corrections and its jth derivative are bounded by
100*2^j. Altogether |y^(j)|<256*2^j for j=0,1,2,3.

Inside each aligned panel the ODE recurrence is

    y^(j+4)=-2lambda*y^(j+2)-y^(j)+f^(j),

where |f^(j)|<1, including j0. If the previous bounds hold, its right
side has magnitude at most 9*256*2^j+1 <256*2^(j+4).
Induction proves |y^(j)|<256*2^j for EVERY nonnegative j, with one-sided
derivatives at the joins. These bounds hold uniformly on each complex
lambda disk and on real x in the full physical interval.

Cauchy's coefficient estimate on radius1/16 now gives, for the normalized
load Taylor tail, t=16r<=3/64. Sum spatial coefficients with
sum (2d_x)^i/i! < exp(1/2)<2. The following outward errors follow:

    delta_y_space <= 256/(2^26*26!),
    delta_yx_space <= 512/(2^25*25!),
    delta_y_load <= 512*t^25/(1-t),
    delta_yx_load <= 1024*t^25/(1-t).

There are26*25=650 coefficients. Their selection contributes at most
650*2^-150 to y, and at most650*25*54*2^-150 to y_x, since 1/d_x<54.
The G_x polynomial contributes at most1/(10*4^25*25!)+25*2^-150.
Exact rational comparisons give

    delta_y <2^-95, delta_yx <2^-90, delta_Gx <2^-100.

Consequently delta_s<2^-93, using eta<1/10. These are full-cell/full-box
mathematical approximation bounds, CONDITIONAL on the specified finite
coefficient selection error. They are not evaluated interval widths from
an implementation. A method that cannot attain that selection width must
stop; it may not adopt these bounds as measured outputs.

## Propagation in the original norm, all finite modes

Use admitted B's form-error theorem, including its T_n-to-G conversion.
For n<=128, k*t<=32/125, L/t<400 and R/t=500, let D/t^2 be the common
normalizing unit in C_d,C_e. Then

    K_n<2^12,
    C_d*D/t^2 <2^31,
    C_e(1/8+delta_s)*D/t^2 <2^29,
    A*t^2/D*(1+nu)<16.

Thus its slope contribution is less than2^48*delta_s. Also
(delta_Ny*t^2/D)=(273/12500)*delta_y<delta_y/32 and
k^2*L^4/t^2<2^31. The y-dependent Ny contribution is less than
2^38*delta_y. The affine prestress pieces have no representation error
because their parameter dependence is exactly retained. Therefore

    ||Q(lambda)-Qhat(lambda)||_G
        <2^48*2^-93+2^38*2^-95 < epsilon =2^-43

on every declared lower box, for ALL modes0..128, both physical parities,
and all three meshes. Assembly/constant rounding is still separately
enclosed. No finite mode is omitted by this estimate, and no singleton
or midpoint load substitutes for the box. The admitted tail >=129 remains
in its own N_n norm and has not been converted to G without a theorem.

## Exact local residual and finite certificate

Use the reviewed seed's literal sigma1,sigma2,tau and fluxes, with the
parameter-polynomial shat,Nyhat and exact affine N just specified. The
G-complement traces U,V,W,W' vanish at every cell end; U',V' annihilate
P3 and W'' annihilates P2. Consequently

    rU=(I-Pi3)[sigma1-I_cell(-k*tau)],
    rV=(I-Pi3)[tau-I_cell(k*sigma2)],
    rW=(I-Pi2)[D W''-I_cell(shat*sigma1+(2Dk^2-N)W')
                    +I_cell^2(sigma2/R-k*shat*tau+(Dk^4+Nyhat*k^2)W)],
    H(p,p)=sum integral(rU^2/m+rV^2/m+rW^2/D).

All integrals and projections are on the same exact cell. Cauchy-Schwarz
gives |Qhat(p,z)|^2<=H(p,p)G(z). Keeping the exact continuum complement
C>=1/4, Young with theta1 proves

    Schur_exact >= Ahat-8H-(epsilon+8epsilon^2)G.

Choose diagnostic alpha=1/100000 and define
F(lambda)=Ahat-8H-(epsilon+8epsilon^2+alpha)G in actual basis coordinates.
No coefficient-array identity is misidentified with a Gram-norm eigenvalue.
If F is strictly positive definite uniformly on J, exact Schur>=alpha G.
No second epsilon is subtracted from the already-exact complement.

The new polynomial degrees are, in (xi,tau),
 yhat:(25,24), shat:(24,24), Nyhat:(25,24),
 rU:(29,24), rV:(28,24), rW:(54,48), H:(108,96).
Thus F has load degree at most96. These replace the seed's linear-slope
degree counts; pretending H still has degree16 would be wrong.

Express F exactly in the degree96 Bernstein basis on J:
F(lambda)=sum(l=0..96) beta_l(lambda) F_l, beta_l>=0, sum beta_l=1.
An outward finite-matrix certificate with every F_l strictly positive
therefore proves F positive over the ENTIRE box. This is97 finite tests,
not one midpoint test. Conversion coefficients, assembly and Gram entries
must be enclosed outward. An indefinite/zero-containing interval pivot
means INCONCLUSIVE, never a negative physical mode.

For each interval symmetric matrix use its lower triangle as the sole
input, copy the upper entries exactly, and apply ordinary unpivoted LDL
recurrences with interval operations. Every division requires a strictly
positive prior D interval. By induction the intervals enclose the exact
LDL of every matrix represented by that enclosure; strictly positive D
intervals certify positivity. There is no tolerance-based pivot clipping,
symmetry averaging or diagonal regularization. An inability to establish
these premises is a first blocker, not a request for extra precision.

## Parity, angular equivalence and event interface

Reflection is T(U,V,W)(X)=(-U(-X),V(-X),W(-X)). Exact even y, odd s and
constant/ even other coefficients make the full form and G commute with T.
The spaces split into its two orthogonal eigenspaces. On the half interval
the plus sector imposes U(0)=0,W'(0)=0 and the minus sector V(0)=0,W(0)=0;
the remaining centre traces are free. In particular no spurious V'(0)
constraint is imposed on the H1 finite space. Outer clamps are retained.
The full forms are twice their half-interval integrals; cancel that common
factor in form and norm. Each parity has dimension(11M-4)/2, namely
658,1318,2638. Full U at n0, its global reaction, V, n1 and all finite
modes are kept. Cell local DOFs remain at most15, half-bandwidth at most14
in the ordered left-traces/interiors/right-traces basis; eliminating
boundary traces does not increase it. A code must implement this basis,
not an unspecified reordered dense array.

For n>0, (U cos(nphi),V sin(nphi),W cos(nphi)) and
(U sin(nphi),-V cos(nphi),W sin(nphi)) have identical reduced forms and
pi*R norms. Coefficients depend only on X and lambda and the actual frozen
angular operator has that rotational invariance; these paired sectors are
isometric. n0 instead has its full constant U,V,W sector with2*pi*R.
This proves the permitted angular collapse for this continuum operator,
not for an unqualified native discretization.

A reference bracket requires positivity certificates covering EVERY
earlier load for all finite n/parities and the admitted tail, together
with a certified negative Rayleigh value at an upper endpoint in the
appropriate parity. A candidate rational finite vector v is negative
only if an outward upper bound for Ahat(v,v)+epsilon*G(v) is strictly
negative; a failed lower certificate supplies no such vector.

For completeness the direct-bracket alternative has this precise scope.
C is uniformly positive; hence the Schur operator is a finite continuous
symmetric family on each finite sector. The admitted precritical base
branch is continuous and has Delta'(N)>0 on this lower domain. If all
sectors are positive throughout[0,ell] and one has negative Rayleigh at u,
continuity and the finite union of sectors place the first loss in(ell,u].
The positive tail excludes an omitted angular event. This does not assume
a simple crossing and remains valid for multiple roots. Obtain separate
even, odd and full intervals, with full first loss the minimum; unresolved
cluster multiplicity/turning correspondence is explicitly reported and
is NOT a completed transfer certificate.

For a proved positive ell, set L_ref=ell, c_ref=(ell+u)/2,
u_ref=(u-ell)/2. Require u_ref<=.0075*L_ref. Both adjacent mesh centre
changes must be<=.01 times the smaller positive certified lower endpoint.
The remaining five errors and their frozen total .05 remain separate;
no absent native/transfer/geometry/output error is zero. Source-plot
compatibility uses the even interval and retained hull only; it is not
an error bound or a way to choose a later root.

This supplies a conditional mathematical contract. Attaining2^-150
coefficient selection, interval assembly/pivot widths, a complete bounded
representation and the full resource fit are the next phase's explicit
unsealed premises. No actual event, H matrix, LDL pivot, vector, error
budget acceptance, map point or upper-domain coverage is asserted.
