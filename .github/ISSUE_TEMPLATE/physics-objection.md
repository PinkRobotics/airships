---
name: Physics objection
about: A published number you think is wrong, in a form someone else can check
title: '[physics] '
labels: physics
---

<!--
No such aircraft exists. Every number on these pages is arithmetic on stated assumptions,
and the assumptions are the interesting part — so an objection is welcome and does not need
to be polite. It does need to be reproducible. The sections below exist to turn an argument
into something a third party can settle without asking you a follow-up question.

Before writing: three defects are already known and tracked, and reporting one of them
again costs you time rather than us. They are listed at the bottom of this template.
-->

## The figure you are disputing

Which page, which label, and the value exactly as printed, with units.

## Where it is computed

File and line under `sim/`. A permalink (open the file on GitHub, click the line number,
press `y`) is ideal, because line numbers move.

## What you get instead

Your value, with units, and the arithmetic that produced it. Show the working; a number on
its own cannot be checked, and "this is obviously wrong" cannot be acted on.

## The inputs you used

Which of our assumptions you kept, which you replaced, and what you replaced them with. If
you changed one, say where your value comes from — a citation settles this and an assertion
does not. If our figure is right given our assumptions but our assumptions are wrong, say
so plainly; that is a different and usually more interesting bug.

## Reproduction

The URL you were looking at, including the determinism parameters:

    https://…/index.html?seed=7&data=snapshot

`?seed=N` pins every random choice the model makes. `?data=snapshot` pins the input data to
the dataset in `data/` — fires, perimeters and satellite heat become fixed, and the wind
becomes still air. Without both, two people looking at "the same" page are not looking at
the same run, and neither of them can reproduce the other.

If you ran anything in the console, paste it. The model is on the page as `AIRSHIPS.sim`,
so for example:

    AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P100, AIRSHIPS.sim.MODES.balanced, 15)

## Does the in-page selftest still pass for you?

Load the page with `?selftest=1`. Every assertion in `sim/selftest.js` runs and the result
is appended to the browser tab's title and logged to the console. Paste what you get.

- [ ] `SELFTEST PASS`
- [ ] it fails — paste the failing assertion

This matters because a failure tells us the model contradicts *itself*, which we can fix
without agreeing with you about physics first. A pass tells us the disagreement is about
the assumptions, which is the longer conversation.

## Is it one of the three already-known defects?

- [ ] No, or I am not sure
- [ ] **Buoyancy at altitude** — the lift ledger uses sea-level air density while the ships
      cruise at 1500 m above ground. At their working altitude all three classes are net
      heavy, which contradicts the page's claim that the rotors only ever push down.
- [ ] **Two disagreeing power models** — `planCycle`'s energy budget gives 82.5 MWh per
      P-10000 cycle; integrating `stateAt`'s per-system draw over the same cycle gives
      211 MWh.
- [ ] **The unexplained `Math.min(6, …)` window** — it sets 53% of the P-10000's published
      cycle energy and nothing states why it is there or why 6.

Two further things are known and worth not re-reporting: retained descent ballast is zero
by construction for every class and every setting, and the cryogenic plant is numerically
inert, while the copy on the page describes both as live.

If your objection is one of the above, a comment on the existing issue with your numbers is
more useful than a new report.

## Optional: does `make golden` move?

If you have a fix, `make golden` replays the model at seed 7 and diffs every output against
`tests/golden/`; `make goldenui` checks the rendered page. The diff is the honest description of what your change does, and we will
ask for it eventually, so it may as well come with the argument.
