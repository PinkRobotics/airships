# U3 13f4 exclusive full-plants slot: Sciences order ord-sciences-g1-ops-u3-13f4-exclusive-plants-slot-1018

The order was ingested 04:44:10. Both attachments were sha256-verified at 04:45: the test-completion disposition d403b4c0
and the conditional full-plants brief fb9948d8. The CO's route report rpt-co27-sci-u3-plants-route-standard-recipe-four-workers-1018
was read. This is allocation only: nothing was armed, started, woken or installed.

## Slot
- **Holder:** ref-741b462e28e96fb5cf31 (B).
- **Unit and source:** vacuum-u3-13f4-fullplants-1018 on source 13f4b15f7c7f0720f84516d866ffd6595d3f3eff (tree 0d82ce5d).
- **Recipe:** CO Route 1, `make floatplants`, FLOAT_PLANT_WORKERS=4, FLOAT_PLANT_TIMEOUT=1800, job cap 7200 s.
- **Resources:** CPUQuota 3200% (cpu.max 3200000/100000), MemoryMax 10 GiB, MemorySwapMax 0, TasksMax 1024, no GPU.
- **Window:**
  - Opens when the handoff is admitted.
  - Latest start is 06:30:00 PDT.
  - Expires 08:50:00 PDT, which is 06:30:00 + 8400 s. Any start up to 06:30:00 has at least 8400 s for the whole unit.
- **Release:** B's terminal queue report after cleanup, cc Operations, or expiry, whichever comes first.

## Measured (capacity.txt from measure.sh, read-only, 04:47:43)
- **CPU:** 32 logical CPUs online (Ryzen 9 9950X, 16 cores / 32 threads), none isolated, one NUMA node.
  - The user manager's affinity is 0-31, and so is the shell's.
  - cpu.max is `max 100000` on user.slice, user-1000.slice and [address]
  - The user manager delegates cpu, memory and pids, but no cpuset. So 32 CPUs is a quota ceiling over the whole host, not
    dedicated cores.
  - Load was 8.2 of 32 and CPU PSI was 0.
- **Memory:** MemAvailable 62.8 GB of 94.1 GB, and memory PSI was near 0. Swap is about 94% used, which is the normal zram
  state; the job runs with swap 0. No memory.max or memory.high is set above the user manager.
- **Disk:** the output-root filesystem has 1.43 TB free.
- **Exclusivity:**
  - No python, make or node process names the plants checker.
  - No user unit names plants, fp-, u3 or 13f4.
  - No queue item in 3 days carries a `reservations` field.
  - Engineering's fingerprint is landed (LAND 97, 00:22), and its builder c3de is retired.
  - No other open order runs full plants. ref-d697b9b2c19e874d4cc4's Q0 work is deferred until U3 lands.
- **Shared, not reserved:**
  - helm-backup has been running since 03:33:54. Past runs took 1h33m to 3h11m and are mostly I/O; its find uses about one CPU.
  - Two vLLM engines hold the GPUs, using about half a CPU.
  - The ordinary collector timers keep running.

## Not done and not claimed
- No unit was armed and no controls were applied: B measures the actual controls before launch.
- No seat was woken, and B's old units were not touched.
- No prediction that the run fits in 7200 s.
