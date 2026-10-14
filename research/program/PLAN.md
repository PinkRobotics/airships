# Delivery plan

Status: redirected 2026-10-13. Follow the [programme](PROGRAM.md) and
[ranked design work](NEXT-STAGES.md). The target is an airship that floats confidently;
the current answer is `not shown`. No aircraft has been built or flown.

## First delivery

Prepare the programme redirect and the front-page scoreboard as a documentation-only
candidate immediately. Preserve generated README regions, existing public content and
historical numerical records. This candidate need not wait for a design result and
establishes no new scientific result or qualification.

For documentation, run `make readmecheck linkcheck buildercheck` with project scratch
configured. Run `buildercheck` after committing: it checks recorded commits. These checks
verify generated README regions, tracked local links and anchors, and Builder trailers.
They list external URLs without fetching them and do not qualify a physical design.

## Design iteration cycle

1. Select the strongest recorded candidate or bound and explain its limits. Freeze its
   source revision, geometry, structural concept, materials, scale and pressure assumptions.
2. Write matching mass and lift budgets. Separate the represented hull from equipment,
   fittings and payload; label missing values UNKNOWN. Keep altitude, pressure and safety
   factor explicit, and do not combine entries from different configurations.
3. State the margin on that same basis, confidence, weakest assumption and its sensitivity.
   A positive conditional hull margin is not evidence of an all-up floating vehicle.
4. Choose one concrete design change that could improve margin or confidence. Record the
   assumed default, why it ranks next and what would test it. A FAIL closes this hypothesis;
   choose the next change in the same hour. After acceptance, start the next assigned unit.
5. Update the short expert-confirmation ledger: assumption, why it matters, change in margin
   if wrong, and the dependent iteration. Use UNKNOWN for an unbounded effect.

Begin on paper with explicit assumed values. Verification supports the selected design
question; it is not a separate historical FIFO. Native solvers, CFD, FEA and other heavy
jobs require a bounded assigned execution envelope and applicable controls. The programme's
8 CPU / 40 GiB / no-swap parent envelope is not a worker allocation. Preserve historical
failed attempts and exhausted caps; a redirect does not grant a retry of an old hypothesis.

## Unit record and review

Record each iteration under `research/`, including FAIL or UNKNOWN. Record the question,
frozen assumptions, sources, result and practical limits. Distinguish PASS within its tested
scope, FAIL of a hypothesis, UNKNOWN, NOT RUN and control stops. Corrections add a disposition;
they do not rewrite old evidence or retroactively qualify incomplete monitoring.

Keep one bounded evidence file per unit, with exact candidate commit, tree and base,
changed paths, check commands and results, review referents and landing dependencies.
One reviewer checks custody. Documentation receives proportionate checks; code or scientific
changes receive their applicable review and [claim gate](../../docs/CLAIM-GATE.md).
Keep new calculations labelled internal, conditional hypotheses pending applicable review.

Prepare candidates in one isolated worker-owned disk-backed clone with a separate Git
directory and normal project governance; never put clones or worktrees on RAM scratch.
Include the [Builder trailer](../../CONTRIBUTING.md#name-the-builder). Submit the exact
candidate and evidence through the lead for XO signature and Captain landing. Workers do
not edit the primary, push or land. Keep the clone for subsequent assigned iterations.

## Daily progress

Put the same scoreboard line at the top of the 06:50 daily summary and on the repository
front page: whether the best candidate floats, margin, confidence and decisive assumption.
Keep it at or below 180 characters; until the evidence changes, it starts `not shown`.
Explain how it moved or why it did not. The morning reader truncates long lines.

Report actual per-repository landing counts, the first pending landing and reserved
decisions with their defaults and dates. Aim for at least one actual airships or site
landing daily; a branch commit or message does not count, and a site landing does not
replace that day's iteration record. Record acceptance and the actual landing without
calling a pending candidate delivered.

Resolve design questions internally. Money, physical work, new public scientific claims,
owner settings and root follow the reserved-decision route in [PROGRAM.md](PROGRAM.md).
Preserve all earlier stage evidence and scope limits; the 10-13 design queue replaces its
priority order, not its results.
