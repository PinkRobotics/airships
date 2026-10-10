# Monitor snapshot binding repair — 2026-10-09

Status: isolated source correction and regression preparation. Historical scientific results and the prior live lifecycle-coverage gap remain unchanged. This record supplies a narrow patch for future integration; it is not an executable release or a scientific rerun.

## Question and correction

The historical diagnostic driver imported `snapshot` from `mission_monitor` before `lifecycle_guard.install()` rebound the module attribute. Its local function binding therefore continued to call the original monitor. This binding diagnosis and isolated fixture do not establish coverage of any prior live execution; that coverage is UNKNOWN here. Historical execution counts and outcomes remain in their own unpublished records.

The [two-line patch](monitor-wiring.patch) imports the module and resolves `mission_monitor.snapshot` at each checkpoint. The installer, scientific calculations, numerical gates, source pins and historical counters are unchanged. Historical source and output are preserved. The derivative retains its historical expired admission, deadline and consumed-attempt checks; it provides no new execution authority.

## Isolated regression and review

Five regression cases passed using the actual historical overlay installer with synthetic monitor and owned-write interfaces and the extracted driver checkpoint wiring:

1. The old local binding reproduces the missing overlay.
2. The corrected checkpoint resolves the installed wrapper and forwards its four binding/contract pins.
3. An overlay verification rejection becomes a control stop before the base monitor is called or a sample is recorded.
4. A contract-load rejection stops installation before a monitor call.
5. A later module-attribute replacement is resolved by the corrected call site.

The fixture runs no driver main, process census, native solver or diagnostic computation. It does not test the actual ledger, descendant walk, cgroup state or every action outside the extracted checkpoint. It establishes binding and rejection propagation within the fixture, not live lifecycle coverage or whole-host resource control. Measurement sequencing outside the fixture remains outside this test's scope.

One artifact review round completed with Codex and Claude and found no demonstrated defect. Codex reran the five cases and checked that reversing the two changed lines recovers the original source hash. Claude traced the installer, driver and fixture and identified the same synthetic scope limits. The first Claude launch reached its caller timeout; one control retry completed. These artifact reviews were unbound to a repository candidate and are not canonical landing review evidence.

## Source identity and disposition

The original driver SHA-256 is `c2d7f3ee83c70c5add4de516b2b958777f35967caf2675a1b5be3c73abbc9ed0`; the isolated derivative is `da47bfd7bb8edfd7851542e9d65042f3612ea3c6403078f5dc7ea691650ecee4`. The actual installer fixture source is `5617e26a3d03a4fd2bea51e83c1223f83cbca8dc838822a1864726d551f2fb48`. The patch SHA-256 is `74ac171edac1652a383b9b0a6c1faff2d15ab3926d6ce17e91100e2f03e76755`. Exact runtime artifact and review references are retained in the unit evidence; the full historical execution environment has not been published, so reproduction from this repository alone remains UNKNOWN.

Regression wiring: PASS within the isolated fixture. Prior live coverage: UNKNOWN. This unit does not publish a disposition or count for earlier scientific attempts; their records remain unchanged. Native, diagnostic and scientific reruns: zero. Any future live integration must retain admission, accounting and appropriate control checks; this correction does not revive a prior GO or convert prior samples into overlay evidence.

The P1.6 assumed-value paper proceeds as a separate unit without waiting for physical measurements. Publication of this new research record remains subject to its applicable claim review; no old documentation verdict is reused.
