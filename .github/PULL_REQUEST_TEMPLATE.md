<!--
Delete whatever does not apply. A one-line typo fix does not need six headings; a change
under sim/ needs all of them, because a change under sim/ moves published numbers.
-->

## What changed

## Why

What is wrong with the current behaviour, or what this makes possible. If it fixes a
reported problem, link the issue.

## Which tests cover it

Name them. If nothing covers it, say that plainly and say why — "this is a comment change"
is a complete answer; silence is not. A change to the model that no test would have caught
is the one that needs a new test most.

- [ ] `make check` passes (import boundaries, golden, browser suites)
- [ ] `make test-node` passes, or I have no node and CI will run it

---

## For any change under `sim/`

`sim/` computes every number the pages publish. `tests/golden/` is a recording of those
numbers at `?seed=7&data=snapshot`, and a change here will move some of them. That is
allowed. It is not allowed to be a surprise.

**Paste the golden diff.** `make golden` prints it. Then explain *every* line of it:

| Output | Was | Is now | Why it moved |
| --- | --- | --- | --- |
|  |  |  |  |

"Rounding" and "floating point" are not explanations on their own — say which operation
reordered and why the new order is the right one. An output that moved for a reason you
cannot state is the bug this section exists to catch.

- [ ] The golden diff is pasted above and every changed number is accounted for
- [ ] `tests/golden/` has been re-recorded in this pull request, in its own commit, so the
      re-recording can be reviewed separately from the change that caused it
- [ ] `sim/selftest.js` still passes in the browser (`?selftest=1`), and if this change
      makes an assertion in it wrong, that assertion has been updated here too
- [ ] Any figure quoted in prose — `index.html`, `concept/`, the READMEs — has been updated
      to the new value, or is listed here as still needing it

**Does this close one of the three known defects?** If so, say which, and say whether it
closes it completely or only in part. If it changes the model's behaviour for a reason
unrelated to those defects, say that too — the two kinds of change are easier to review
apart than together.
