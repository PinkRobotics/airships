# Decision note — review-codex-default-0926 (worker)

## Starting state
Clean main 435 e8273ffd. Boyce DEMONSTRATED (log unpublished-local-ref:754ef667f069c90b):
`tools/review.py` round selection picked `codex gpt-5.6`; ChatGPT-account codex
refused it in 1.7 s (400 invalid_request_error, "model is not supported").

## What was learned
- The hardcoded default lived in one place: `helm/call/review_engines.py:144`,
  `EngineCandidate("codex", ..., "gpt-5.6", ...)`. Single-lane `--codex` was
  never broken (agent_runner `readonly_review` pins served `gpt-5.6-sol`); only
  the round path dispatched the refused id.
- The registry already agrees on the served replacement two independent ways:
  `harness_registry.command_model("codex")` = `gpt-6-sol` (launch-plan command
  default) and `model_currency.tracked_model("codex")` = newest `gpt-*-sol` =
  `gpt-6-sol` (probe-passed 2026-09-22). Catalog: sol/terra/luna/6-astra/6-sol.
- The two-flag and single-lane refusal paths already exited nonzero with a
  DEGRADED/LaneDidNotRun banner; the gap was the bound-evidence officer form
  (`--codex --claude --candidate --evidence-round`, no `--round`), where
  `_require_round_two_lanes` returned None and the round died with a generic
  exit 1 instead of the two-family ROUND_INCOMPLETE (88).

## What was changed (4 files)
1. `helm/call/review_engines.py` — new `default_codex_model()` resolving the
   launch plan's seated codex model via `harness_registry.command_model`,
   accepted only if catalogued for codex; else `CODEX_FALLBACK_MODEL` =
   `gpt-5.6-sol` (review pin + settings default + 16 runs/24 h). The plain-codex
   candidate now carries it; `codex-sol` anchor untouched (served).
2. `tools/review.py` — `_require_round_two_lanes` also gates the
   bound-evidence two-lane form (no `--round`): refused/absent lane →
   ROUND_INCOMPLETE (88), same message. Single-lane and unbound forms untouched.
3. `tests/test_review_engines_float.py` — updated stale `gpt-5.6` assertion;
   new: registry-resolution test, 5 fallback arms + registry-raise arm, gate
   unit tests (bound fires / single+unbound+clean pass through).
4. `tests/test_review_candidate_access.py` — new end-to-end: stubbed Boyce
   400 shape on codex + clean claude through the officer form → exit 88,
   status failed, `lanes_run == ["claude"]`, ROUND_INCOMPLETE on stderr.

## What was deferred (out of scope)
- `_EXPLICIT_ALIASES` still maps a user-typed `gpt-5.6` to the codex engine
  (now resolves to the served default at dispatch; an explicit `--model gpt-5.6`
  to the runner still refuses loudly at the gateway — correct per rule (e)).
- `codex-sol` R3 anchor stays pinned at `gpt-5.6-sol`; moving it to the tracked
  newest-sol is a separate register/currency decision.
- No external review round (Boyce ruled this small).

## Verification
- Focused: 11 (new engines/gate unit) + 4 (bound incl. new e2e) green;
  full files: 88 + 562 green (neighbors test_lane_run_state, test_review_script,
  test_review_chain).
- Canonical `./scripts/test.sh -n 8` on frozen tip: PENDING at note time —
  exact counts recorded in the hand-up. (Baseline note: an unrelated recent run
  showed 5 failed / 26565 passed; failures, if any, will be named concretely.)
