# Public-face source-count and phone check, 9 October 2026

This is a site-maintenance record. It adds no structural result or solver
qualification. Historical failures and the dated float case remain unchanged.

The catalogue in [sources.json](../sources.json), at science revision
`6278355e27f47865fbdb615c94c3638096eee6a7`, contains 123 source entries.
The estate home, research introduction and `llms.txt` still said 108; the
candidate updates those current-count statements to 123. The current catalogue also marks nine entries as `contradicts-us`; the
research introduction and `llms.txt` retain their source grades and update
this count from ten to nine. The August objection review and dated historical
statements are preserved. Sitemap dates change only
for the home, log and research pages actually edited, to 9 October 2026.
The existing `tyler@pinkai.ca` contact is added to the home and log footers.

## Float phone result: PASS for layout, unchanged scientific status

At the measured starting revision, [gen_float_pages.py](../../tools/gen_float_pages.py)
already generated scroll containers around all 14 tables in
[float/index.html](../../float/index.html). Its 1,240-pixel value limits the
page container; its 900-pixel value selects a narrow-screen media rule. Neither
is a fixed table width. A redundant generator patch would not repair a measured
defect, so the producer and generated pages are preserved.

A fresh Chromium 153 headless page, with CSS viewports of 1,440, 834 and 390
pixels, showed no document-wide horizontal overflow. All 14 table containers
stayed within each viewport; scrolling each container reached its final column.
The existing visible scroll cue, keyboard focus and heading-based group names
remain present. All 42 table-text hashes and heading associations matched the
starting revision. Captions, historical warnings and numeric cells are unchanged.
Home and log footer checks at the same widths also showed no horizontal overflow.
Visual inspection covered the phone table and the home/log footers, including
the contact link. Reduced motion was requested for these static checks.

The first browser launcher moved into a desktop scope; its resource containment
was not accepted. A second launch detected the same move and stopped. A corrected
launch disabled desktop-bus access for the owned browser process, verified its
cgroup before navigating, and completed inside the programme slice with one CPU,
a 2 GiB memory limit, no swap and CPU 7. No resource limit was raised. These were
control diagnostics, not scientific attempts.

## Destination evidence: UNKNOWN pending the canonical public links

The configured Git remotes identify the estate and science source repositories.
Anonymous GitHub requests returned 404 for those repositories and the proposed
Discussions endpoint. A public source/Discussions destination has therefore not
been asserted or invented; the coordinator has been asked for the canonical
existing destinations. Contact uses the address already published by the estate.

The float producer check and its 21 tests passed; the documentation link
checker and its 11 tests passed. The Builder history check passed initially, but
its 12-test suite first failed because `node` was absent from the command path.
Using the already-installed Node 24.21.0 exposed a second failure: the fixture
expected a TAP skip line while Node selected its human-readable reporter. With
that existing binary and an explicit `NODE_OPTIONS=--test-reporter=tap`, all 12
Builder tests passed. These failed check attempts are retained as environment
and reporter diagnostics; neither is a structural result. No source test or
installed setting was changed to obtain the pass.

The estate candidate edits no published science copy or live-fire data.
Deployment and acceptance are separate from this local candidate. Appropriate
source checks are `make floatpagecheck linkcheck buildercheck`; browser evidence
is kept with the unit handoff. No full numerical suite or solver was run.

## Estate word-budget result: FAIL, existing overage retained

The estate `tools/check_words.py` gate returned 1. Its visible-word counter
measured 561 home-page words at the starting estate revision and 562 in the
candidate, against a limit of 500. The added Contact label accounts for one word.
The existing over-budget page remains unresolved and needs a separate front-door
edit. Targeted contact, catalogue metadata and phone-layout checks passed; the
site-wide word-budget gate has not passed. This candidate is not deployment
acceptance.

## Later destination disposition: private repositories, contact only

After the anonymous checks above, Captain verified that both source repositories
are private and that no public source or Discussions destination exists. This
supersedes the earlier destination uncertainty. The supported footer uses the
existing contact address and omits GitHub/Discussions links. No public-link wait
or automatic repository-setting change remains. The earlier checks are retained
as the historical evidence available before that verification.

## Current correction: public mirror owner and footer destinations

The later private-repository conclusion above was based on the wrong owner.
The canonical public mirror is
[PinkRobotics/airships](https://github.com/PinkRobotics/airships), with existing
[Discussions](https://github.com/PinkRobotics/airships/discussions). Source and
Discussions links are now added beside Contact in both estate footers. The
earlier unknown and contact-only records remain as history; they no longer
define the destination disposition. No visibility or Discussions setting was
changed. On 9 October 2026, the supplied mirror status was landing 24, while the
private origin was at landing 25; this footer correction did not assert that the
newer origin content was public or that this candidate had landed.

The corrected home has 564 visible words against the 500-word budget: the
starting page had 561 and the contact-only candidate 562. Source and Discussions
add two more words. The gate remains FAIL, explicitly unresolved. A footer
change cannot remove the existing 61-word overage without editing other page
content; that broader front-door edit is deferred. The full estate gate also
reports the existing missing Pink AI page in this checkout. No all-checks PASS
or deployment acceptance is claimed.

The source gate is run with `make floatpagecheck linkcheck buildercheck`. Its
environment supplies the existing Node binary and
`NODE_OPTIONS=--test-reporter=tap` through leading `env NAME=value` arguments.
Commands and links use repository-relative paths; the public landing receipt
can name PATH without printing its host value. The reusable check launcher and
its read-only envelope check retain the existing one-CPU, 2 GiB, zero-swap
check lane. The float producer, generated pages, captions, numeric cells and
previous 14-table viewport evidence remain unchanged by this footer correction.

The corrected footers passed fresh 1,440-, 834- and 390-pixel viewport checks:
all Source, Discussions and Contact links stayed within the viewport, with no
document-wide horizontal overflow. Six footer screenshots were inspected with
reduced motion. The generated log snapshot is absent in the isolated checkout;
its existing unavailable-snapshot fallback was used, with no production-log
claim. The exact leading-env source gate passed: 21 float tests and matching
outputs, 11 link tests with zero link errors, and 12 Builder tests. The public
gate formatter and seal accepted the repository-relative command and kept only
the PATH variable name in the public receipt. These targeted passes do not
override the word-budget FAIL above.
