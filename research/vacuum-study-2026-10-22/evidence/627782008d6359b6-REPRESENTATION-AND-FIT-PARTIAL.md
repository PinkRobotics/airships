# Representation/fit work reached and first missing premise

This records the phase4 design work, not a sealed implementation contract.
The coarsest gate passed independently. GENERAL-LOAD-CONTRACT's useful
2^-43 error bound requires selection of each of650 normalized coefficients
within2^-150. The first missing premise is a checked finite arithmetic
construction that achieves that selection bound with fully bounded
intermediates and a complete, useful operation/fit account. Neither the
old B recipe nor the seed supplies it. It cannot be filled by assigning
zero rounding error or by treating a storage estimate as a runtime bound.

## Candidate construction examined on paper

A way to avoid high-order interval-jet dependency is to extract load
Taylor coefficients by a fixed Cauchy sum. For each exact cell midpoint,
evaluate the complete clamped B expression and its first three x
derivatives at512 equally spaced points on the complex circle of radius
sigma=1/32 about the real load centre. Recover orders j=0..24 with the
normalized discrete Fourier sums, multiplied by(r/sigma)^j. No such
points, complex coefficients, fields or arrays have been evaluated here.

The new analytic disk proof at radius R=1/16 gives an exact alias estimate:
for f=y^(a), a<=3, |f|<=256*2^a, the jth normalized coefficient error from
the finite sum is at most

    256*2^a*(r/R)^j*(sigma/R)^512/[1-(sigma/R)^512]
        <2^-499.

This is an alias bound only; finite elementary-function and arithmetic
errors must be added. Roots of unity, complex square-root branches and
the clamped inverse must all be enclosed. Complex a,b primitive
denominators are 2(1+b) or2(1-b), not merely a real a^2 lower bound.
Their nonzero complex bounds must be used by an actual implementation.

Given the first four spatial Taylor coefficients, the ODE supplies the
rest to order25. With z_i=d_x^i*y^(i)/i!, its normalized recurrence is

 z_(i+4)=[-2lambda*d_x^2*(i+2)*(i+1)*z_(i+2)-d_x^4*z_i
          +d_x^(i+4)*f^(i)/i!]/[(i+4)*(i+3)*(i+2)*(i+1)].

The denominator is positive; d_x<=1/4 and ||lambda|| in the load-polynomial
l1 norm is below1. This recurrence is much better conditioned than
unscaled derivatives. The forcing is the exact constant plus the central
cosine, zero cosine outside. Quantize the completed normalized
coefficients to160 fractional bits only after an enclosure width proof.

A candidate fixed implementation would use131072 fractional bits for
the scalar complex enclosure stage, magnitude guards, finite Machin/sqrt/
Taylor counts, and4096 fractional bits for subsequent matrix interval
work. All integer products, shifted numerators and live expression
buffers need their own size bounds. Merely naming these precisions is
NOT a proof that2^-150 is attained. In particular the actual expanded
expression graph depth, elementary-function/jet error amplification and
coefficient-enclosure width have not been certified. A guessed graph
depth512 or primitive count2^16 is not admitted evidence. No implementer
may replace this missing proof by a retry or precision escalation.

This is the first indispensable premise that remains open. Consequently
the uniform general-load epsilon remains conditional, and no coefficient
generator, full finite certificate or evaluation is ready for execution.
No proof of physical failure or impossibility is supplied.

## Transparent inventory and provisional capacity arithmetic

The following are useful resource warnings, not a completed price. They
count all modes/parities/meshes rather than dropping them to make a quote.

* Lower boxes384 per mesh, upper reservation129: all513 accounted for.
* Parity blocks:384*129*3*2=297216.
* Degree96 Bernstein tests:97 per block, hence28829952 finite matrices.
* Sum of parity dimensions over all meshes is9228; total LDL rows across
  those97 tests is44340466176.
* With reflection reuse for coefficient construction only, there are
  384*420 cell/box coefficient locations and82575360 complex sample points
  for the proposed512-point construction.
* Without undeclared cross-mode or cross-parity reuse, local assembly has
  384*129*840=41610240 cell-sector visits.

For illustration, a padded2048-byte matrix interval and all97 lower-band
matrices at the largest parity dimension would occupy7860817920 bytes
before local polynomials, factors, buffers, interpreter overhead, logs and
results. This arithmetic is not an RSS measurement or a full storage seal.
Streaming one local residual pair avoids retaining120 full products, but
its actual allocation/lifetime implementation has not been verified.

The deliberately loose illustrative work allowances2^28 primitive steps
per complex sample,2^35 per cell-sector assembly, and512 per LDL row give

    coefficient: 22166154415964160,
    assembly:   1429716959829688320,
    LDL:           22702318682112,

whose sum is below2^61. These are proposed counting allowances, NOT
verified loop bounds or measurements. At8CPU for7200wall seconds, using
that sum as a sufficient fit bound would require more than
630167455106048/25 primitive steps per CPU second. No evidence supports
that rate. A loose upper bound does not prove a runtime lower bound, so
this does NOT prove that every better implementation is too slow.

The charter8CPU/40GiB/2hour limits are ceilings only. There is no measured
primitive-throughput or complete-output account for this proposed
representation, and no calibration is authorized by the paper order.
Native/package acquisition and historic StVK scope timings do not measure
this arithmetic kernel and cannot supply the missing fit evidence.

Thus there is no supported CPU/wall/memory/scratch/output/process quote
for the complete reference attempt. Giving the charter ceiling itself as
that quote would conceal the unsealed construction and fit premises.
The separate evaluation/map-price phase is NOT_RUN after this first
representation blocker. The remaining contract and any implementation
optimization/calibration require a separately ruled unit; none runs now.

## Scope of a next closure, without inventing an end-to-end price

The smallest specifically identified reference continuation is a paper
closure of the coefficient-selector graph/rounding proof and a tighter
complete operation account. It can retain the new gate proof, analytic
remainder bounds and exact-parameter treatment. It must establish the
2^-150 selector, count the new polynomial/Bernstein degrees and every
finite block, and produce a reviewable calibration or evaluation card.
A scalar calibration would itself need an implemented/pinned kernel,
prospective counters and a separate Ops-admitted price; a successful
scalar timing alone would not establish scientific positivity or map fit.

No complete map route is priced in the retained inputs. The axial
reference route still needs qualified native energy/tangent behaviour,
solid geometry and absolute event/transfer bounds, plus the declared
mapping to the hydrostatic H1 question. A direct h1/h2 hierarchy cell is
a charter-compatible candidate only after its actual geometry, controls,
closed form, qualification, mesh/imperfection work and prospective
comparator are frozen and priced. The published hierarchy exponent is
heuristic; it is not validated data. U2 likewise still needs load-matched
qualification. These missing prices are UNKNOWN, not zero.

The old advisory's Ref3 blockage is historical: held source access has
since closed. It is not revived as a reason to refuse either route. The
withdrawn5100 native estimate and U3 machinery3600 are not alternative
map-point prices. No global cheapest route is inferred from this incomplete
price information. A bounded next paper closure can be proposed by
Sciences, but this stopped owner neither grants it nor claims its time
would guarantee a useful implementation or a map point.
