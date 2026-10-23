# U3 ordinary gates: the exact operator card, v2 (unit vacuum-u3-ordinary-gates-1018)

v2 answers ord-sciences-g1-ops-u3-card-narrow-guard-corrections-1018. It is a CARD, not a grant. v1 is kept as CARD-v1.md
(db2b5e28), and its three launch files are superseded: they are no longer present and must not be used.

**Unchanged from v1** (Sciences accepted these):
- the target lists, the caps and the source reconstruction;
- HEAD 13f4b15f… plus patch d5bcc6ba… by `git apply --index`, giving tree **11b5a287a172a0f46e6119bf6548ef2281e3a885**
  with 3281 entries;
- the qualified CfT service profile, and the CO's ruling rpt-co27-sci-u3-gates-user-service-allowed-1018.

## Full pins (v2)
| File | sha256 | Bytes |
|---|---|---|
| group-A.sh (u3gate-a-1018.service) | 280daa18a4bde5943fbd91ea3da54d939f70edf3d344922eb9f944536182ed85 | 12190 |
| group-C.sh (u3gate-c-1018.service) | 1401ae10f10725c5f99beb5445ee9d99d044bc241475f1c47ad7240466d531cf | 12199 |
| group-B.sh (u3gate-b-1018.service) | a1ce059b1455d81f0461b737625a5ce10c3ef2de09e4982453e0f51aba7214f8 | 12108 |
| admit.py (parallel-sim-budget-1018/admit.py; each script pins it, and a copy is admit.py.at-card-v2) | acf07c35567cf15beeb7d7d4c9e78e94cf464cfe92596f904d8bf5fafc97ac0b | 14190 |
| card.py (the generator: one template) | 6e9b2a4b993d95dbcec2d56de3e300db809081e02f99adb2019b5e64d0b52353 | |
| smoke.py (the end-to-end smoke of that template) | 2307481cd8b75a9d8286495910d024ab807887f199ed55aa2e072ca5fe51ec40 | |

**Pinned inside every script and checked at launch:**
- CfT `unpublished-local-ref:43ba70015fd6b0a7 8c599d43…;
- Node `…/ref-741b462e28e96fb5cf31/.ship/toolchain/node-v22.23.3-linux-x64/bin/node` fde6a4bf…;
- the patch `…/u3-namespace-1018/diff-u3ns-1018.txt` d5bcc6ba…;
- admit.py acf07c35…;
- HEAD 13f4b15f7c7f0720f84516d866ffd6595d3f3eff, tree 11b5a287…, 3281 entries.

**Caps, per the CO:**
| Group | CPUQuota | MemoryMax | TasksMax | RuntimeMaxSec | Threads |
|---|---|---|---|---|---|
| A | 400% | 16 GiB | 4096 | 1200 | 4 |
| C | 400% | 16 GiB | 4096 | 1800 | 4 |
| B | 200% | 8 GiB | 2048 | 900 | 2 |

**Bounds** (startup is TimeoutStartSec=60 in each group):
| Group | Inner make timeout | Outer timeout of the single invocation |
|---|---|---|
| A | 1170 s | 1325 s |
| C | 1770 s | 1925 s |
| B | 870 s | 1025 s |

## The four corrections
1. **Admission fails closed (admit.py acf07c35):**
   - Every observation must succeed and parse, or `request` REFUSES and `status`/`check` report UNKNOWN (exit 4):
     meminfo, PSI, `systemctl show`, `journalctl` and the unit listing.
   - A failed query never frees caps and never hides a unit.
   - Stray units count in any of active, activating, deactivating or reloading.
   - `status` and the new `check` are READ-ONLY; only Ops' `request` and `lapse` write the ledger.
   - A second unsettled grant for the same unit is refused.
   - Proof (smoke2/admit-failclosed.txt): with systemctl unreachable, `status` gives UNKNOWN rc 4 and `request` gives
     REFUSE "observation failed" rc 3.
2. **Expected values are COMPARED before make.** The ExecStartPre lines fail the unit before the payload on any mismatch,
   and each guard stage first echoes `GUARD <stage>`, so stdout.log names where a stop happened:
   - **alias:** `RT/t` is a symlink and `-ef ROOT/<G>unpublished-local-ref:f2e62936e29c52c7;
   - **unset:** bus, XDG_RUNTIME_DIR, display and Wayland are empty;
   - **controls:** cpu.max is exactly `<cores×100000> 100000`, memory.max the cap bytes, memory.swap.max 0 and pids.max
     the TasksMax. The values are recorded first, then `grep -qx`;
   - **env:** every bound variable is recorded with `printenv`, then compared with `test ${VAR} = value`;
   - **browser:** `bin/chromium` is a symlink and `-ef` the CfT binary.
3. **One bounded, synchronous invocation with true status:**
   - `bash ROOT/<G>/launch.sh <grant-id>` runs fresh revalidation, then the read-only grant check, then
     `timeout --kill-after=10s <outer> systemd-run --user --wait --collect …`, then bounded collection, then protected
     cleanup.
   - **Collection:** `systemctl show` of the exact unit (timeout 30 s). If it is still loaded: `stop`, then
     `reset-failed`, then `show` again, each bounded to 30 s and by the exact name. Collected means LoadState not-found,
     the cgroup absent and the runtime directory absent.
   - **Literal status:** `ROOT/<G>/status.txt`, plus a full timestamped `launch.log`. Real UTC and monotonic stamps are
     taken at start, launch, collect and cleanup.
   - **Exit codes:**

     | Code | Meaning |
     |---|---|
     | 0 | PASS, only when the manager rc is 0, `Finished with result: success`, `status=0/SUCCESS` and collection all hold |
     | 10 | collision |
     | 11 | pins |
     | 12 | source |
     | 13 | owned paths |
     | 14 | unit or runtime present |
     | 15 | grant check (nothing started for 10–15) |
     | the manager's own rc | any non-zero manager rc, e.g. 1 for a failed unit or 124 for the outer timeout |
     | 21 | the manager rc was 0 but the success facts are incomplete |
     | 30 | collection unproven, with no cleanup |

   - The background-watcher instruction is removed. The harness note is under Limits.
4. **Fresh guards at launch, inside the same invocation, after the grant:**
   - all pins (sha256sum -c);
   - source: HEAD, `--show-toplevel` equal to `ROOT/<G>/src`, `write-tree` 11b5a287…, `diff --quiet`, no untracked
     files, 3281 entries (each git call bounded to 60 s);
   - owned `home`, `tmp` and `bin` (uid 1000, mode 0700, not symlinks), with `home` and `tmp` empty and `bin` holding
     only the `chromium` alias;
   - unit LoadState not-found, with `RT` and the cgroup absent;
   - then `admit.py check`. The grant must be live and unsettled, under 900 s old, for this unit and this exact launch.sh
     sha. The host is re-measured NOW (MemAvailable minus the cap at least 20 GB, PSI under 5, running caps within
     24/36) with this grant's own reservation excluded.
   - A lapsed grant is no authority. Unknown or failed checks stop. There is no scratch removal until collection is
     proven, and the next group starts only after PASS.

## Procedure (executing seat B) under Sciences' finite order: serial A → C → B, one attempt each, the first failure stops
1. **Prepared state for each group:**
   - **A** is prepared by B under NEW900, as in the U3-GROUP-A-SOURCE-PREPARATION brief:
     - `ROOT/A/src` is a detached worktree of CLONE at 13f4… with `git apply --index` of the patch;
     - `ROOT/A/home`, `tmp` and `bin` are 0700;
     - its SOURCE-PREPARATION.json is the receipt.
   - **C and B** are prepared the same way under the run order: `mkdir -m 0700` of ROOT/<G> and of its `home`, `tmp` and
     `bin`; the worktree and `apply --index`.
   - **For every group:** `ln -s <CfT path> ROOT/<G>/bin/chromium` if it is absent.
   - Copy Ops' `group-<G>.sh` to `ROOT/<G>/launch.sh` and verify its sha256 from the table.
   - **Collision rule:** any other pre-existing content that the launch checks reject is a collision and stops the work.
     That covers run products (launch.log, status.txt, systemd-run.log, stdout.log, stderr.log), non-empty home or tmp,
     extra files in bin, and a source that is not at the exact tree.
2. **Ask Ops for the live grant** by a queue item naming the group, with SOURCE-PREPARATION.json's path and sha for A.
   - Ops verifies the receipt names HEAD 13f4…, tree 11b5a287… and 3281 entries, then runs:
     `admit.py request --seat ref-741b462e28e96fb5cf31 --job u3gate-<g> --cores <4|4|2> --mem-gib <16|16|8> --hours <0.33333333|0.5|0.25> --line-file unpublished-local-ref:c12424ea8f5de38e<G>.sh --unit u3gate-<g>-1018.service --cwd ROOT/<G>`.
   - Ops replies GRANT with its id and the measured values, or REFUSE with the measured reasons.
3. **Within 900 s of the grant, invoke once:** `bash ROOT/<G>/launch.sh <grant-id>`. Its exit status and
   `ROOT/<G>/status.txt` are the result.
4. **Report the group** with the hashes of status.txt, launch.log, systemd-run.log, stdout.log and stderr.log.
   - Ops then ledgers the launch-time `check` output from launch.log against the grant. That is the CO's "measured at
     launch and ledgered".
   - On PASS, go to the next group's step 1. On anything else, stop. A retry on the same root is a collision by design,
     and only Sciences disposes of it.

## Proof (smoke2/; the SAME template on Ops' own names: tiny two-file repo, 1 core / 1 GiB / 64 tasks / 60 s, a trivial make target; no U3 gate, no su3cft, no B path)
| Case | Exit | What the evidence shows |
|---|---|---|
| P (normal) | 0, PASS | Every guard passed in order. The compared controls read `100000 100000`, 1073741824, 0 and 64. The payload ran with OMP=1, chromium resolved to the owned alias, and HOME and TMPDIR were owned. Then CHECK OK, manager_rc 0 and collected (not-found, cgroup and runtime absent). tmp, home, bin and src were all removed, and only the logs stayed. |
| N (pids expected 63, actual 64) | 1, FAIL | stdout.log ends at `GUARD controls` with NO payload line. The manager result was `exit-code`; collected; src kept. |
| M (a bad grant id) | 15, REFUSED | `CHECK REFUSED … 0 grant records`. No systemd-run.log: nothing started. |
| P rerun | 10 | Collision. |

Afterwards, 0 smoke units remained and the runtime directory was absent.

## Measured eligibility
None is claimed in v2. The 13:34:48 reading in v1 is historical, and every grant and launch measures afresh.

## Limits (precise)
- **What the smoke proves:** the template's control flow, guards, comparisons, collection, cleanup and exit mapping at
  small scale. It proves no U3 gate's outcome and no long-run timing.
- **Not exercised:** the outer timeout, the RuntimeMaxSec kill, the stop/reset-failed branch (collection was immediate),
  and UNCOLLECTED (30).
- **Harness:** the invocation is synchronous (`systemd-run --wait` inside). Its outer bound (A 1325 s, C 1925 s,
  B 1025 s) exceeds a Claude Code foreground call (600 s maximum). So the single invocation is held as the executing
  harness's own tracked job, acting on its exit notice, not as a file-polling watcher. If the run order needs another
  holding form, that is Sciences' call.
- **CPU:** CPUQuota limits CPU time, not affinity. The CO approved the quota only, and there is no AllowedCPUs.
- **The pins are bound:** the scripts pin admit.py's bytes, so any later admit.py change needs regenerated scripts. A
  stale script refuses at 11.
- **Ops' reconstruction receipt:** the tree is the measured value from v1 (two ways, B's repo untouched). B's own
  receipt binds it for A when filed.
- **Writes:** Ops wrote nothing under B's paths and launched no U3 gate.
