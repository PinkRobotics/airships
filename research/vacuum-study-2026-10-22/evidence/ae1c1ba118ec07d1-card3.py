"""Write the U3 gate-group launch scripts, VERSION 3 (group-v3-A2.sh, group-v3-C.sh, group-v3-B.sh): the CO's one-relaunch
ruling rpt-co27-sci-u3-group-a-one-relaunch-card-fix-1018. TMPDIR and AIRSHIPS_TMPDIR become ONE short REAL canonical
directory on the HOME volume, unpublished-local-ref:4d7c5da4fdbd5289<name>, created by the service itself (CacheDirectory=, mode 0700), with
no symlink in any component; the qualified su3cft/t alias stays, for the profile and cache only. Group A2 reuses the
retained A/src in place under a fresh receipt root A2. A failed removal can no longer PASS. Built on version 2 (ord-sciences-g1-ops-u3-card-narrow-guard-corrections-1018): each script is ONE synchronous, bounded
invocation `bash ROOT/<G>/launch.sh <grant-id>` that (1) revalidates everything at launch, (2) checks the live grant
read-only through admit.py, (3) launches the qualified service whose ExecStartPre guards COMPARE the actual controls,
environment, alias and browser before make, (4) collects within bounds, (5) cleans up only after proven collection and
(6) returns the true exit. The CO's ruling rpt-co27-sci-u3-gates-user-service-allowed-1018 fixes profile and caps; the
qualified property set is B's cft-wrapper.py 553a7c0a build_argv. Absolute paths only.
`render(p)` is shared with smoke.py, which runs the same template on Ops' own names."""
import hashlib, os
D = os.path.dirname(os.path.abspath(__file__))
SEAT = 'unpublished-local-ref:7e000a46e292f857'
ADMIT = 'unpublished-local-ref:b7e8e118fec49648'
COMMON = dict(
    root=f'{SEAT}/.ship/work/outputs/u3-ordinary-gates-1018',
    clone=f'{SEAT}/.ship/work/airships',
    head='13f4b15f7c7f0720f84516d866ffd6595d3f3eff', tree='11b5a287a172a0f46e6119bf6548ef2281e3a885', entries=3281,
    node_bin=f'{SEAT}/.ship/toolchain/node-v22.23.3-linux-x64/bin',
    pins=[('8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e',
           'unpublished-local-ref:37fd3d1d48bd5751'),
          ('fde6a4bf8d0562f7751d1a2d6cb9b417c4cfe107bbcb0aa3e9a24e125e348f48',
           f'{SEAT}/.ship/toolchain/node-v22.23.3-linux-x64/bin/node'),
          ('d5bcc6ba5f27b74ac7f1e852b84bda79c1421fd697c96372f933aae1cb3f6a03',
           f'{SEAT}/.ship/work/outputs/u3-namespace-1018/diff-u3ns-1018.txt'),
          ('83bb63455ad461380133cb1f2467edbab6855f5a1f49e4ac427cfa14a5f80d21',
           f'{SEAT}/.ship/work/outputs/u3-namespace-1018/pin-manifest-post-u3ns-1018.json')],
    chrome='unpublished-local-ref:37fd3d1d48bd5751',
    rtname='su3cft', admit=ADMIT, start_s=60, uid=1000)
SOCKET_TAIL = 69   # len('/browser-check-XXXXXXXX') + len('/.org.chromium.Chromium.XXXXXX') + len('/SingletonSocket')
GROUPS = {
    'A2': dict(src_group='A', cache='u3a2', cores=4, mem=16, tasks=4096, runtime=1200,
              targets='readmecheck linkcheck buildercheck claimsrestore claimscheck ledgercheck floatplantcheck portcheck'),
    'C': dict(src_group='C', cache='u3c', cores=4, mem=16, tasks=4096, runtime=1800,
              targets='reposizecheck noticecheck floatpagecheck firstparty pdfcheck analysischeck fallbackcheck ciparity evaccheck'),
    'B': dict(src_group='B', cache='u3b', cores=2, mem=8, tasks=2048, runtime=900, targets='ledgercheck-selftest'),
}


def q(s):
    return "'" + s.replace("'", "'\\''") + "'"


def render(p):
    """p: group, unit, root, clone, head, tree, entries, node_bin, pins, chrome, rtname, admit, start_s, uid, cores,
    mem (GiB), tasks, runtime, targets, and optionally expect_pids (a deliberate mismatch, smoke only)."""
    g, unit = p['group'], p['unit']
    r = f"{p['root']}/{g}"; rt = f"unpublished-local-ref:e954680c048ccc3b{p['uid']}/{p['rtname']}"
    srcd = p.get('src') or f"{p['root']}/{p['src_group']}/src"
    tmpr = p.get('tmp_real') or f"unpublished-local-ref:4d7c5da4fdbd5289{p['cache']}"
    assert len(tmpr) + SOCKET_TAIL <= 107, (tmpr, len(tmpr) + SOCKET_TAIL)
    cg = f"/sys/fs/cgroup/user.slice/user-{p['uid']}.slice/user@{p['uid']}.service/app.slice/{unit}"
    c = p['cores']; mem_b = p['mem'] * 1024 ** 3
    inner = p['runtime'] - 30; outer = p['start_s'] + p['runtime'] + 5 + 60
    path = f"{r}/bin:{p['node_bin']}:/usr/bin:/bin"
    env = [('PATH', path), ('CI', 'true'), ('LANG', 'C.UTF-8'), ('PYTHONDONTWRITEBYTECODE', '1'),
           ('PYTHONUNBUFFERED', '1'), ('OMP_NUM_THREADS', str(c)), ('OPENBLAS_NUM_THREADS', str(c)),
           ('MKL_NUM_THREADS', str(c)), ('NUMEXPR_NUM_THREADS', str(c)), ('TMPDIR', tmpr),
           ('AIRSHIPS_TMPDIR', tmpr), ('XDG_CACHE_HOME', f'{rt}/t/cache'), ('A3D_CHROME_PROFILE', f'{rt}/t/profile'),
           ('HOME', f'{r}/home')]
    props = ['Type=exec', 'KillMode=control-group', 'StandardInput=null',
             f'CPUQuota={c * 100}%', f'MemoryMax={mem_b}', 'MemorySwapMax=0', f"TasksMax={p['tasks']}",
             f"TimeoutStartSec={p['start_s']}", f"RuntimeMaxSec={p['runtime']}", 'TimeoutStopSec=5',
             f"RuntimeDirectory={p['rtname']}", 'RuntimeDirectoryMode=0700', f"CacheDirectory={tmpr.rsplit('/', 1)[1]}",
             'CacheDirectoryMode=0700', f'WorkingDirectory={srcd}']
    props += [f'Environment={k}={v}' for k, v in env]
    props += ['UnsetEnvironment=DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR DISPLAY WAYLAND_DISPLAY']
    guards = [
        'ref-940157c79b6dbec9f226 GUARD alias', f'ref-850c21bb3e265fec592a -s {r}unpublished-local-ref:e9671acd244849c5 {rt}/t', f'ref-92c4697c0cd9aa41a9c7 -L {rt}/t',
        f'ref-92c4697c0cd9aa41a9c7 {rt}/t -ef {r}unpublished-local-ref:e9671acd244849c5',
        'ref-940157c79b6dbec9f226 GUARD tmpreal',
        f'ref-81e2f24e4e80426e80f0 -I -c "import os,sys; d=sys.argv[1]; s=os.stat(d); print(d, len(d) + {SOCKET_TAIL}, oct(s.st_mode & 0o777), s.st_uid); '
        f'sys.exit(0 if os.path.isdir(d) and not os.path.islink(d) and os.path.realpath(d) == d and not os.listdir(d) '
        f'and (s.st_mode & 0o777) == 0o700 and s.st_uid == {p["uid"]} and len(d) + {SOCKET_TAIL} <= 107 else 1)" {tmpr}',
        'ref-940157c79b6dbec9f226 GUARD unset', 'ref-92c4697c0cd9aa41a9c7 -z ${DBUS_SESSION_BUS_ADDRESS}${XDG_RUNTIME_DIR}${DISPLAY}${WAYLAND_DISPLAY}',
        'ref-940157c79b6dbec9f226 GUARD controls', f'ref-9cf73c8df0e2d9666934 -v {cg}/cpu.max {cg}/memory.max {cg}/memory.swap.max {cg}/pids.max',
        f"ref-91905432c508abf116c5 -qx '{c * 100000} 100000' {cg}/cpu.max", f'ref-91905432c508abf116c5 -qx {mem_b} {cg}/memory.max',
        f'ref-91905432c508abf116c5 -qx 0 {cg}/memory.swap.max', f"ref-91905432c508abf116c5 -qx {p.get('expect_pids', p['tasks'])} {cg}/pids.max",
        'ref-940157c79b6dbec9f226 GUARD env', 'ref-2490bbb4a60c6712c196 ' + ' '.join(k for k, _ in env)]
    guards += [f'ref-92c4697c0cd9aa41a9c7 ${{{k}}} = {v}' for k, v in env]
    guards += ['ref-940157c79b6dbec9f226 GUARD browser', f'ref-92c4697c0cd9aa41a9c7 -L {r}/bin/chromium',
               f"ref-92c4697c0cd9aa41a9c7 {r}/bin/chromium -ef {p['chrome']}", 'ref-940157c79b6dbec9f226 GUARD done']
    props += [f'ExecStartPre={x}' for x in guards]
    props += [f'StandardOutput=append:{r}/stdout.log', f'StandardError=append:{r}/stderr.log']
    pins = '\n'.join(f'{s}  {f}' for s, f in p['pins'])
    run_products = 'launch.log status.txt systemd-run.log stdout.log stderr.log'
    L = []
    L += ['#!/bin/bash',
          f"# U3 gate group {g}: ONE synchronous bounded invocation, only under Ops' live grant for {unit}.",
          f'# Usage: bash {r}/launch.sh <grant-id>     (status line: {r}/status.txt; full log: {r}/launch.log)',
          '# Exit: 0 PASS (collected, cleaned) | 10 collision | 11 pins | 12 source | 13 owned paths | 14 unit/runtime',
          '#       | 15 grant check | 2 usage  (10-15: nothing started) | the manager rc itself when it is non-zero',
          '#       | 21 manager rc 0 but success facts incomplete | 30 collection unproven (no cleanup).',
          'set -u', 'umask 077',
          'GRANT=${1:-}', '[ -n "$GRANT" ] || { echo "usage: launch.sh <grant-id>"; exit 2; }',
          f'R={q(r)}; SRC={q(srcd)}; TMPR={q(tmpr)}; UNIT={q(unit)}; RT={q(rt)}; CG={q(cg)}; CLONE={q(p["clone"])}',
          f'HEAD={q(p["head"])}; TREE={q(p["tree"])}; ENTRIES={p["entries"]}; ADMIT={q(p["admit"])}',
          'LOG="$R/launch.log"; STATUS="$R/status.txt"',
          f'for f in {run_products}; do [ ! -e "$R/$f" ] || {{ echo "STATUS REFUSED rc=10 collision: $R/$f exists (a previous run)"; exit 10; }}; done',
          'exec >>"$LOG" 2>&1',
          'stamp() { echo "== $1 utc=$(date -u +%Y-%m-%dT%H:%M:%S.%6NZ) mono=$(cut -d" " -f1 /proc/uptime)"; }',
          'finish() { echo "STATUS $1 rc=$2 $3"; printf "STATUS %s rc=%s %s\\n" "$1" "$2" "$3" > "$STATUS"; exit "$2"; }',
          'refuse() { finish REFUSED "$1" "$2"; }',
          'stamp start; echo "grant $GRANT unit $UNIT root $R"',
          '# -- fresh revalidation at launch (nothing has started yet) --',
          f'sha256sum -c <<\'PINS\' || refuse 11 "pin mismatch"\n{pins}\nPINS',
          f'echo "{hashlib.sha256(open(p["admit"], "rb").read()).hexdigest()}  $ADMIT" | sha256sum -c || refuse 11 "admit.py changed"',
          'h=$(timeout 60 git -C "$SRC" rev-parse HEAD) && [ "$h" = "$HEAD" ] || refuse 12 "HEAD [$h]"',
          'top=$(timeout 60 git -C "$SRC" rev-parse --show-toplevel) && [ "$top" = "$SRC" ] || refuse 12 "toplevel [$top]"',
          't=$(timeout 60 git -C "$SRC" write-tree) && [ "$t" = "$TREE" ] || refuse 12 "write-tree [$t]"',
          'timeout 60 git -C "$SRC" diff --quiet || refuse 12 "worktree differs from index"',
          'u=$(timeout 60 git -C "$SRC" ls-files --others --exclude-standard) && [ -z "$u" ] || refuse 12 "untracked [$u]"',
          'n=$(timeout 60 git -C "$SRC" ls-files | wc -l) && [ "$n" = "$ENTRIES" ] || refuse 12 "entries [$n]"',
          'echo "source HEAD $h tree $t entries $n clean"',
          'for d in home tmp bin; do',
          f'  [ -d "$R/$d" ] && [ ! -L "$R/$d" ] && [ "$(stat -c %u:%a "$R/$d")" = "{p["uid"]}:700" ] || refuse 13 "$R/$d not an owned 0700 directory"',
          'done',
          '[ -z "$(ls -A "$R/home")" ] && [ -z "$(ls -A "$Runpublished-local-ref:e9671acd244849c5")" ] || refuse 13 "home or tmp not empty"',
          f'[ -L "$R/bin/chromium" ] && [ "$R/bin/chromium" -ef {q(p["chrome"])} ] && [ "$(ls -A "$R/bin")" = chromium ] || refuse 13 "bin/chromium alias"',
          'ls=$(timeout 30 systemctl --user show "$UNIT" -p LoadState --value) || refuse 14 "systemctl show failed"',
          '[ "$ls" = not-found ] || refuse 14 "unit LoadState [$ls]"',
          '[ ! -e "$RT" ] && [ ! -e "$CG" ] || refuse 14 "runtime dir or cgroup exists"',
          '[ ! -e "$TMPR" ] && [ ! -L "$TMPR" ] || refuse 14 "short TMP $TMPR already exists"',
          'for c in /home unpublished-local-ref:a9d2d1a1856e1673 unpublished-local-ref:8e591a9489706044; do [ -d "$c" ] && [ ! -L "$c" ] || refuse 13 "TMP parent $c is not a real directory"; done',
          'timeout 60 python3 -I "$ADMIT" check --grant "$GRANT" --unit "$UNIT" --line-file "$R/launch.sh"; ck=$?',
          '[ "$ck" = 0 ] || refuse 15 "grant check rc $ck"',
          '# -- the launch: the qualified service; its ExecStartPre guards compare before make --',
          'stamp launch',
          f'timeout --kill-after=10s {outer}s systemd-run --user --wait --collect --unit={unit} \\']
    L += [f'  -p {q(x)} \\' for x in props]
    L += [f"  ref-b49c1cde24372bb5448c --kill-after=5s {inner}s ref-994275a3cda2dd1ca6ee --no-print-directory {p['targets']} \\",
          '  > "$R/systemd-run.log" 2>&1',
          'MRC=$?; echo "manager_rc=$MRC"; cat "$R/systemd-run.log"',
          '# -- bounded collection by the exact unit name --',
          'stamp collect',
          'S=$(timeout 30 systemctl --user show "$UNIT" -p LoadState,ActiveState,SubState,Result); src=$?; echo "show rc=$src $S"',
          'if [ "$src" = 0 ] && ! grep -qx "LoadState=not-found" <<<"$S"; then',
          '  timeout 30 systemctl --user stop "$UNIT"; echo "stop rc=$?"',
          '  timeout 30 systemctl --user reset-failed "$UNIT"; echo "reset-failed rc=$?"',
          '  S=$(timeout 30 systemctl --user show "$UNIT" -p LoadState,ActiveState,SubState,Result); src=$?; echo "show rc=$src $S"',
          'fi',
          'col=no; [ "$src" = 0 ] && grep -qx "LoadState=not-found" <<<"$S" && [ ! -e "$CG" ] && [ ! -e "$RT" ] && col=yes',
          'echo "collected=$col cgroup_absent=$([ ! -e "$CG" ] && echo yes || echo no) runtime_absent=$([ ! -e "$RT" ] && echo yes || echo no)"',
          '[ "$col" = yes ] || finish UNCOLLECTED "$( [ "$MRC" != 0 ] && echo "$MRC" || echo 30 )" "manager_rc=$MRC; no cleanup"',
          'ok=no; [ "$MRC" = 0 ] && grep -q "Finished with result: success$" "$R/systemd-run.log" \\',
          '  && grep -q "Main processes terminated with: code=exited, status=0/SUCCESS$" "$R/systemd-run.log" && ok=yes',
          '# -- protected cleanup: owned disposable paths only, after proven collection --',
          'stamp cleanup',
          'cln=yes',
          'for d in "$Runpublished-local-ref:e9671acd244849c5" "$R/home" "$R/bin" "$TMPR"; do',
          '  [ -e "$d" ] && [ "$(realpath -e "$d")" = "$d" ] && timeout 60 rm -r --one-file-system "$d"',
          '  if [ ! -e "$d" ]; then echo "removed $d"; else echo "NOT removed $d"; cln=no; fi',
          'done',
          'if [ "$ok" = yes ]; then',
          '  [ "$cln" = yes ] || finish INCOMPLETE_CLEANUP 31 "manager_rc=0 success collected, but disposable removal failed; src kept"',
          '  timeout 120 git -C "$CLONE" worktree remove --force "$SRC"; echo "worktree remove rc=$?"',
          '  [ ! -e "$SRC" ] || finish INCOMPLETE_CLEANUP 31 "manager_rc=0 success collected, but src removal failed"',
          '  echo "removed src"; finish PASS 0 "manager_rc=0 success collected; tmp, home, bin, short TMP and src removed"',
          'fi',
          '[ "$MRC" != 0 ] && finish FAIL "$MRC" "manager_rc=$MRC collected; disposable removal $cln; src kept"',
          'finish FAIL 21 "manager_rc=0 but success facts incomplete; collected; disposable removal $cln; src kept"']
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    for g, s in GROUPS.items():
        p = dict(COMMON, **s, group=g, unit=f'u3gate-{g.lower()}-1018.service')
        f = os.path.join(D, f'group-v3-{g}.sh')
        open(f, 'w').write(render(p))
        print(f'group-{g}.sh', hashlib.sha256(open(f, 'rb').read()).hexdigest(), os.path.getsize(f))
