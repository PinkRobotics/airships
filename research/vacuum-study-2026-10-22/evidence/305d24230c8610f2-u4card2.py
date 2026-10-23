"""U4 own tests, card v2: ONE block grant per builder (the CO's rpt-co27-sci-u4-light-jobs-block-grant-1018).
  python3 u4card2.py hold <m|g>            write hold-u4<b>.sh (the block's reservation-holding service line)
  python3 u4card2.py scripts <m|g> <grant> write the four invocation scripts bound to that actual grant
admit.py is NOT changed (acf07c35 stays pinned by the U3 v2 card). The block is an ordinary ledgered grant whose unit is
simjob-u4<b>-blk-1018-hold.service: a do-nothing `sleep` under the block's caps (CPUQuota 200%, MemoryMax 4 GiB, swap 0)
with RuntimeMaxSec=3600, so admit.py counts the reservation as running from grant until Ops stops it at the last receipt
(release) or the window closes by itself. Invocations run in simjob-<grant>-<n>.scope, n = 1..3, serial, and each script
enforces the order: n1 test; n2 test only after n1 failed, or n2 X only after n1 passed; n3 X only after n2 test passed.
render() is shared with u4smoke2.py."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u4card as v1
D = v1.D
GUARD2 = os.path.join(D, 'u4guard2.sh')
WINDOW_S = 3600
# (script tag, n, kind, invocation dir, the receipt the sequence requires, the rc it requires: 0 or 'nonzero')
STEPS = [('n1-test', 1, 'test', 'tests-001', None, None),
         ('n2-test', 2, 'test', 'tests-002', 'tests-001', 'nonzero'),
         ('n2-x', 2, 'x', 'x-001', 'tests-001', '0'),
         ('n3-x', 3, 'x', 'x-001', 'tests-002', '0')]


def hold_line(b, uid=1000):
    unit = f'simjob-u4{b}-blk-1018-hold.service'
    return (f'#!/bin/bash\n# U4 {b} block reservation holder (Ops starts it at grant; Ops stops it at release).\n'
            f'systemd-run --user --quiet --collect --unit={unit} --property=Type=exec --property=StandardInput=null '
            f'--property=CPUQuota=200% --property=MemoryMax=4294967296 --property=MemorySwapMax=0 '
            f'--property=RuntimeMaxSec={WINDOW_S} -- ref-1887116e4fbd97023671 infinity\n'), unit


def render(p):
    """p: root, inv, n, kind, unit, hold, grant, argv, x_out, plugin, pytest, guard, uid, needs (inv dir or None),
    needs_rc ('0'|'nonzero'|None), scope_prefix, and optionally expect_mem (smoke only)."""
    r, inv, unit = p['root'], p['inv'], p['unit']
    i = f'{r}/{inv}'; uid = p['uid']; mem_b = 4 * 1024 ** 3
    cg = f'/sys/fs/cgroup/user.slice/user-{uid}.slice/user@{uid}.service/app.slice/{unit}'
    env = [f'HOME={i}/home', f'TMPDIR={i}unpublished-local-ref:e9671acd244849c5', 'PATH=ref-ccc203c53b7d040ba4dc:/bin', 'LANG=C.UTF-8', 'PYTHONDONTWRITEBYTECODE=1',
           'PYTHONUNBUFFERED=1'] + [f'{v}=2' for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                                       'NUMEXPR_NUM_THREADS')]
    if p['plugin']: env.append('PYTEST_DISABLE_PLUGIN_AUTOLOAD=1')
    q = v1.q; sha = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()
    products = 'launch.log status.txt stdout.txt stderr.txt guard.txt source-sha256.txt receipt.json'
    L = ['#!/bin/bash',
         f"# U4 block invocation n={p['n']} ({p['kind']}) for {r.split('/')[-1]} under block grant {p['grant']}: ONE synchronous bounded run.",
         f'# Usage: bash {i}/launch.sh        (no grant argument: the block grant is bound below)',
         '# Exit: the payload rc (0 = pass) | 97 guard mismatch (no payload) | 124/137 timeout | 10 collision | 11 pins',
         '#       | 12 source/output | 13 owned paths | 14 unit present or another invocation running | 15 block not alive',
         '#       | 16 sequence (three-total rule) | 17 owner precheck failed (10-17: nothing started) | 30 uncollected.',
         'set -u', 'umask 077',
         f'R={q(r)}; I={q(i)}; UNIT={q(unit)}; CG={q(cg)}; HOLD={q(p["hold"])}; GUARD={q(p["guard"])}; GRANT={q(p["grant"])}',
         f'for f in {products}; do [ ! -e "$I/$f" ] || {{ echo "STATUS REFUSED rc=10 collision: $I/$f exists"; exit 10; }}; done',
         'exec >>"$I/launch.log" 2>&1',
         'utc() { date -u +%Y-%m-%dT%H:%M:%S.%6NZ; }; mono() { cut -d" " -f1 /proc/uptime; }',
         'stamp() { echo "== $1 utc=$(utc) mono=$(mono)"; }',
         'finish() { echo "STATUS $1 rc=$2 $3"; printf "STATUS %s rc=%s %s\\n" "$1" "$2" "$3" > "$I/status.txt"; exit "$2"; }',
         'refuse() { finish REFUSED "$1" "$2"; }',
         f'stamp start; echo "block grant $GRANT invocation n={p["n"]} unit $UNIT dir $I"',
         f"sha256sum -c <<'PINS' || refuse 11 \"pin mismatch\"\n{v1.PY_SHA}  ref-cda51cdb7487692d10e7\n{sha(p['guard'])}  {p['guard']}\nPINS",
         '[ "$(readlink -f ref-81e2f24e4e80426e80f0)" = ref-cda51cdb7487692d10e7 ] || refuse 11 "python3 is not python3.14"']
    if p['pytest']:
        L.append(f'v=$(cd / && env -i HOME="$I/home" PATH=ref-ccc203c53b7d040ba4dc:/bin ref-81e2f24e4e80426e80f0 -c "import pytest; print(pytest.__version__)") '
                 f'&& [ "$v" = {p["pytest"]} ] || refuse 11 "pytest [$v]"')
    L += ['[ -d "$R/src" ] && [ ! -L "$R/src" ] || refuse 12 "no source directory $R/src"']
    if p.get('x_out'):
        L.append(f'[ ! -e {q(p["x_out"])} ] || refuse 12 "X output already exists"')
    if p.get('needs'):
        need = f"{r}/{p['needs']}/receipt.json"
        cond = '"$prc" = 0' if p['needs_rc'] == '0' else '"$prc" != 0'
        L += [f'prc=$(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))[\'rc\'])" {q(need)} 2>/dev/null) || refuse 16 "no receipt {p["needs"]}"',
              f'[ {cond} ] || refuse 16 "sequence: {p["needs"]} rc $prc does not allow invocation n={p["n"]} {p["kind"]}"']
    L += ['for d in home tmp; do',
          f'  [ -d "$I/$d" ] && [ ! -L "$I/$d" ] && [ "$(stat -c %u:%a "$I/$d")" = "{uid}:700" ] && [ -z "$(ls -A "$I/$d")" ] || refuse 13 "$I/$d not an owned empty 0700 directory"',
          'done',
          'hs=$(timeout 30 systemctl --user show "$HOLD" -p ActiveState --value) || refuse 15 "systemctl show failed"',
          '[ "$hs" = active ] || refuse 15 "block reservation $HOLD is [$hs]: window closed or released"',
          'ls=$(timeout 30 systemctl --user show "$UNIT" -p LoadState --value) || refuse 14 "systemctl show failed"',
          '[ "$ls" = not-found ] && [ ! -e "$CG" ] || refuse 14 "unit LoadState [$ls] or cgroup present"',
          f'run=$(timeout 30 systemctl --user list-units --no-legend --plain --state=active,activating,deactivating {q(p["scope_prefix"] + "-*.scope")}) || refuse 14 "list-units failed"',
          '[ -z "$run" ] || refuse 14 "another invocation of this block is running: $run"',
          "( cd \"$R/src\" && timeout 60 find . -type f -not -path './proposed-ops-output/*' -print0 | sort -z | xargs -0 -r sha256sum ) > \"$I/source-sha256.txt\" || refuse 12 \"source hashing failed\"",
          '# owner precheck inside the counted reservation (not admission): MemAvailable - 4 GiB >= 20 GB and PSI some avg10 < 5',
          'ma=$(awk \'/^MemAvailable:/ {print $2 * 1024}\' /proc/meminfo); psi=$(sed -n \'s/^some avg10=\\([0-9.]*\\).*/\\1/p\' /proc/pressure/memory)',
          'echo "precheck MemAvailable=$ma psi_some_avg10=$psi"',
          'python3 -I -c "import sys,math; ma=float(sys.argv[1]); p=float(sys.argv[2]); sys.exit(0 if math.isfinite(ma) and math.isfinite(p) and ma-4294967296>=20e9 and p<5 else 1)" "$ma" "$psi" || refuse 17 "precheck MemAvailable=$ma psi=$psi"',
          'cd "$R/src" || refuse 12 "cd src"',
          'stamp launch; T0=$(utc); M0=$(mono)',
          f'timeout --kill-after=15s 150s systemd-run --user --scope --collect --quiet --unit={unit} \\',
          f'  --property=CPUQuota=200% --property=MemoryMax={mem_b} --property=MemorySwapMax=0 --property=RuntimeMaxSec=130 \\',
          '  -- ref-d9af09a16f3a81bf2ded -i ' + ' '.join(q(e) for e in env) + ' \\',
          f'  /bin/bash "$GUARD" "$I/guard.txt" "$UNIT" {q("200000 100000")} {p.get("expect_mem", mem_b)} 2 {p["plugin"]} -- \\',
          '  ' + ' '.join(q(a) for a in p['argv']) + ' \\',
          '  < /dev/null > "$I/stdout.txt" 2> "$I/stderr.txt"',
          'RC=$?; T1=$(utc); M1=$(mono); echo "payload_rc=$RC"; tail -3 "$I/guard.txt"',
          'stamp collect',
          'S=$(timeout 30 systemctl --user show "$UNIT" -p LoadState,ActiveState,Result); src=$?; echo "show rc=$src $S"',
          'if [ "$src" = 0 ] && ! grep -qx "LoadState=not-found" <<<"$S"; then',
          '  timeout 30 systemctl --user stop "$UNIT"; echo "stop rc=$?"',
          '  timeout 30 systemctl --user reset-failed "$UNIT"; echo "reset-failed rc=$?"',
          '  S=$(timeout 30 systemctl --user show "$UNIT" -p LoadState,ActiveState,Result); src=$?; echo "show rc=$src $S"',
          'fi',
          'col=no; [ "$src" = 0 ] && grep -qx "LoadState=not-found" <<<"$S" && [ ! -e "$CG" ] && col=yes; echo "collected=$col"',
          'peak=$(sed -n "s/^memory.peak //p" "$I/guard.txt"); gok=$(grep -qx "GUARD OK" "$I/guard.txt" && echo yes || echo no)',
          f'python3 -I -c "import json,sys; a=sys.argv; json.dump(dict(grant=a[1], n={p["n"]}, kind={q(p["kind"])}, unit=a[2], start_utc=a[3], end_utc=a[4], start_mono=a[5], end_mono=a[6], rc=int(a[7]), precheck=dict(mem_available_b=a[8], psi_some_avg10=a[9]), memory_peak_b=a[10] or None, guard_ok=a[11]==\'yes\', collected=a[12]==\'yes\'), open(a[13], \'w\'), indent=1)" "$GRANT" "$UNIT" "$T0" "$T1" "$M0" "$M1" "$RC" "$ma" "$psi" "$peak" "$gok" "$col" "$I/receipt.json"',
          'cat "$I/receipt.json"',
          '[ "$col" = yes ] || finish UNCOLLECTED "$( [ "$RC" != 0 ] && echo "$RC" || echo 30 )" "payload_rc=$RC; no cleanup"',
          'stamp cleanup',
          'for d in tmp home; do',
          '  [ "$(realpath -e "$I/$d")" = "$I/$d" ] && timeout 60 rm -r --one-file-system "$I/$d"; [ ! -e "$I/$d" ] && echo "removed $d" || echo "NOT removed $d"',
          'done',
          '[ "$gok" = yes ] || finish GUARD_FAIL "$RC" "payload not started; collected"',
          'finish DONE "$RC" "payload_rc=$RC collected"']
    return '\n'.join(L) + '\n'


def params(b, grant, tag, n, kind, inv, needs, needs_rc):
    s = v1.BUILDERS[b]
    return dict(root=s['root'], inv=inv, n=n, kind=kind, unit=f'simjob-{grant}-{n}.scope',
                hold=f'simjob-u4{b}-blk-1018-hold.service', grant=grant, argv=s[kind],
                x_out=s['x_out'] if kind == 'x' else None, plugin=s['plugin'], pytest=s['pytest'], guard=GUARD2,
                uid=1000, needs=needs, needs_rc=needs_rc, scope_prefix=f'simjob-{grant}')


if __name__ == '__main__':
    if sys.argv[1] == 'hold':
        text, unit = hold_line(sys.argv[2]); f = os.path.join(D, f'hold-u4{sys.argv[2]}.sh'); open(f, 'w').write(text)
        print(os.path.basename(f), unit, hashlib.sha256(text.encode()).hexdigest())
    elif sys.argv[1] == 'scripts':
        b, grant = sys.argv[2], sys.argv[3]
        for tag, n, kind, inv, needs, needs_rc in STEPS:
            f = os.path.join(D, f'u4{b}-blk-{tag}.sh')
            open(f, 'w').write(render(params(b, grant, tag, n, kind, inv, needs, needs_rc)))
            print(os.path.basename(f), hashlib.sha256(open(f, 'rb').read()).hexdigest(), os.path.getsize(f))
