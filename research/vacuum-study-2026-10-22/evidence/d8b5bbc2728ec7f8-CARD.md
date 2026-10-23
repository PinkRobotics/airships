# U3 pre-land simjob card (u3-preland-simjob-1018) — Ops, 2026-10-18T22:24:43-07:00

Authority: Sciences ord-sciences-g1-ops-u3-simjob-preland-card-1018, carrying the CO's ord-co27-sci-u3-two-part-landing-gate-1018
(disposition U3-TWO-PART-GATE-DISPOSITION-1018.json 88889895). This run is simjob's live acceptance (CO ord-co27-ops-simjob-live-acceptance-1018).

## Files (Ops-owned, pinned)
- preland-card.sh  sha256 f4e68dba679d5d4b1b51b8512e67d4d769022090ac06e6d98a6d1ccd2257cb72 — B copies it byte-identical to <R>/launch.sh and runs `bash <R>/launch.sh` ONCE.
- preland-inner.sh sha256 f5f0a9df7774b73640eca9e183075372a4e1c1f3d83a4ff23abb28f2c1338da2 — read in place by the card (pinned inside it); never copied or edited.
- R = unpublished-local-ref:cb6d636cf10c4bb1 (new: no v8/v9/v10 evidence touched).

## B prepares R (nothing else), then launches once
- R/src: a clean worktree of 5f96f32e (tree a8843701, 3281 entries) from the airships clone; nothing untracked.
- R/home, Runpublished-local-ref:3a42306d22ad024c empty owned 0700 directories. R/bin: owned 0700, containing ONLY the symlink chromium -> the CfT 153 chrome.
- unpublished-local-ref:e7366eb5df81b47d and unpublished-local-ref:bf13b1327c540a10 must NOT exist; the card creates them (0700) and removes them after.
- R/launch.sh = preland-card.sh byte-identical. No grant argument: simjob's admission at launch is the grant.

## The job (what simjob admits and enforces)
- simjob run --cores 8 --mem 16G --timeout 6960: scope simjob-<time>-<rand>.scope with CPUQuota 800%, MemoryMax 17179869184,
  MemorySwapMax 0, RuntimeMaxSec 6960; admission atomic against 24 cores / 36 GiB caps / MemAvailable-cap >= 20 GB / PSI < 5.
- Inside: env -i with exactly PATH=R/bin:Node22 bin:/usr/bin:/bin, CI=true, LANG=C.UTF-8, PYTHONDONTWRITEBYTECODE=1,
  PYTHONUNBUFFERED=1, OMP/OPENBLAS/MKL/NUMEXPR_NUM_THREADS=8, TMPDIR=AIRSHIPS_TMPDIR=unpublished-local-ref:e7366eb5df81b47d (22+69=91 <= 107),
  XDG_CACHE_HOME and A3D_CHROME_PROFILE under unpublished-local-ref:aa0cd2f8fc959081 (-> Runpublished-local-ref:e9671acd244849c5), HOME=R/home. No session bus, runtime dir, display,
  case selection, make flags or PYTHONPATH.
- In-scope guards (exit 97 before the payload if any fails): own scope is simjob-*.scope; cpu.max 800000 100000; memory.max
  17179869184; memory.swap.max 0; every variable above exact; short TMP real/empty/0700; runtime alias; chromium and node first on PATH; cwd = R/src.
- Payload (the disposition's logical argv, unchanged): ref-b49c1cde24372bb5448c --kill-after=30s 6840s ref-d9af09a16f3a81bf2ded CI=true
  FLOAT_PLANT_TIMEOUT=2000 FLOAT_PLANT_WORKERS=4 MAKEFLAGS= MFLAGS= ref-994275a3cda2dd1ca6ee -j1 ledgercheck-selftest
  (the recipe runs the five suites, then test_float_hardening with FLOAT_PLANT_CASES= FLOAT_PLANT_MODE=fast: 38 cases).
- After the payload the inner prints the scope's own cpu.stat, memory.peak, pids.peak and oom counters.
- Not set by simjob: TasksMax (pids.max reads the host default; v10 had 2048). Not required by the disposition; disclosed.

## Price (seconds)
| part | bound | expected |
|---|---|---|
| preparation and launch-time checks (pins 120, ten git checks 60 each, simjob status 60) | 780 | ~20 |
| payload | 6840 + 30 kill grace = 6870 | ~1500-3000 (v9: 2696 s at 4 CPU/2 workers with one plant capped) |
| scope (RuntimeMaxSec) | 6960; simjob's own backstop +120 = 7080 | = payload |
| simjob launcher, outer timeout | 7140 + 10 = 7150 (<= the 7200 job ceiling) | = payload + ~2 |
| collection (systemctl show 30, simjob status 60) | 90 | ~2 |
| cleanup (five removals 60 each, worktree remove 120) | 420 | ~5 |
| WHOLE card worst case | 8440 | ~1530-3030 |
Filing is B's, outside the card. B proves its own remaining time covers 8440 s before launch.

## Success (PASS rc 0) requires all of
simjob rc 0; "ENDED <scope>: exited 0 after ... reservation released"; payload_rc=0; six "OK" and six "Ran N tests" lines;
38 PLANT lines; exactly one "Plant suite: fast; 38 cases; 4 workers"; no FAILED/ERROR lines; the scope inactive, its cgroup gone
and its reservation absent from simjob status. Any failure: src kept, stop, report to the CO; no retry.

## Fresh fit (fit.txt, 22:24:23)
simjob 0 reservations (0/24 cores, 0/36 GiB); MemAvailable 53.67 GB - 17.18 GB = 36.48 GB >= 20 GB; PSI some avg10 0.06 < 5;
manual ledger empty. This is a reading, not a reservation: simjob re-measures atomically at launch.
