"""Write the U4 own-test invocation scripts (Ops card for ord-sciences-g1-ops-u4-own-tests-cards-and-grants-1018) and
print their sha256. One template, eight scripts: per builder tests-001..003 and x-001. Each is ONE synchronous bounded
invocation `bash <root>/<inv>/launch.sh <grant-id>`: fresh revalidation, read-only admit.py check of the live grant, an
ordinary `systemd-run --user --scope` (CPUQuota 200%, MemoryMax 4 GiB, swap 0, RuntimeMaxSec 130) running `env -i`
with the bound environment and the in-scope guard (u4guard.sh), which compares controls and environment and then execs
`timeout --kill-after=10s 120s <argv>`; bounded collection; protected cleanup; the payload's true exit.
`render(p)` is shared with u4smoke.py."""
import hashlib, os
D = os.path.dirname(os.path.abspath(__file__))
ADMIT = 'unpublished-local-ref:b7e8e118fec49648'
GUARD = os.path.join(D, 'u4guard.sh')
PY_SHA = hashlib.sha256(open('ref-cda51cdb7487692d10e7', 'rb').read()).hexdigest()
MUSE = 'unpublished-local-ref:e71220872c868338'
GROK = 'unpublished-local-ref:a2dff2f705ac6519'
BUILDERS = {
    'm': dict(root=MUSE, plugin=1, pytest='9.0.2',
              test=['ref-81e2f24e4e80426e80f0', '-m', 'pytest', f'{MUSE}/src/test_requirements_operator.py', '-q', '-p',
                    'no:cacheprovider'],
              x=['ref-81e2f24e4e80426e80f0', f'{MUSE}/src/requirements_operator.py', '--manifest',
                 f'{MUSE}/src/requirements_manifest.json', '--mode', 'requirements-only', '--out', f'{MUSE}/x-001/rows.json'],
              x_out=f'{MUSE}/x-001/rows.json'),
    'g': dict(root=GROK, plugin=0, pytest=None,
              test=['ref-cda51cdb7487692d10e7', '-m', 'unittest', 'test_floors.py'],
              x=['ref-cda51cdb7487692d10e7', f'{GROK}/src/floors.py', '--scenarios', f'{GROK}/src/scenarios.jsonl',
                 '--materials', f'{GROK}/src/materials.json', '--out',
                 f'{GROK}/src/proposed-ops-output/sweep-001/rows.jsonl'],
              x_out=f'{GROK}/src/proposed-ops-output/sweep-001/rows.jsonl'),
}
INVOCATIONS = [('tests-001', 't1', 'test'), ('tests-002', 't2', 'test'), ('tests-003', 't3', 'test'), ('x-001', 'x1', 'x')]


def q(s):
    return "'" + s.replace("'", "'\\''") + "'"


def render(p):
    """p: root, inv, unit, argv (list), x_out (or None), plugin, pytest, admit, guard, uid, cores, mem_gib, and
    optionally expect_mem (a deliberate guard mismatch, smoke only)."""
    r, inv, unit = p['root'], p['inv'], p['unit']
    i = f'{r}/{inv}'; c = p['cores']; mem_b = p['mem_gib'] * 1024 ** 3; uid = p['uid']
    cg = f'/sys/fs/cgroup/user.slice/user-{uid}.slice/user@{uid}.service/app.slice/{unit}'
    env = [f'HOME={i}/home', f'TMPDIR={i}unpublished-local-ref:e9671acd244849c5', 'PATH=ref-ccc203c53b7d040ba4dc:/bin', 'LANG=C.UTF-8', 'PYTHONDONTWRITEBYTECODE=1',
           'PYTHONUNBUFFERED=1'] + [f'{v}={c}' for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                                          'NUMEXPR_NUM_THREADS')]
    if p['plugin']: env.append('PYTEST_DISABLE_PLUGIN_AUTOLOAD=1')
    products = 'launch.log status.txt stdout.txt stderr.txt guard.txt source-sha256.txt'
    sha = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()
    L = ['#!/bin/bash',
         f"# U4 own-test invocation {inv} for {r.split('/')[-1]}: ONE synchronous bounded invocation, only under Ops' live grant for {unit}.",
         f'# Usage: bash {i}/launch.sh <grant-id>      (status: {i}/status.txt; log: {i}/launch.log)',
         '# Exit: the payload rc (0 = pass) | 97 in-scope guard mismatch (no payload) | 124/137 timeout | 10 collision',
         '#       | 11 pins | 12 source/output | 13 owned paths | 14 unit present | 15 grant check (10-15: nothing started)',
         '#       | 30 collection unproven (no cleanup) | 2 usage.',
         'set -u', 'umask 077',
         'GRANT=${1:-}', '[ -n "$GRANT" ] || { echo "usage: launch.sh <grant-id>"; exit 2; }',
         f'R={q(r)}; I={q(i)}; UNIT={q(unit)}; CG={q(cg)}; ADMIT={q(p["admit"])}; GUARD={q(p["guard"])}',
         f'for f in {products}; do [ ! -e "$I/$f" ] || {{ echo "STATUS REFUSED rc=10 collision: $I/$f exists"; exit 10; }}; done',
         'exec >>"$I/launch.log" 2>&1',
         'stamp() { echo "== $1 utc=$(date -u +%Y-%m-%dT%H:%M:%S.%6NZ) mono=$(cut -d" " -f1 /proc/uptime)"; }',
         'finish() { echo "STATUS $1 rc=$2 $3"; printf "STATUS %s rc=%s %s\\n" "$1" "$2" "$3" > "$I/status.txt"; exit "$2"; }',
         'refuse() { finish REFUSED "$1" "$2"; }',
         'stamp start; echo "grant $GRANT unit $UNIT invocation $I"',
         f"sha256sum -c <<'PINS' || refuse 11 \"pin mismatch\"\n{PY_SHA}  ref-cda51cdb7487692d10e7\n{sha(p['admit'])}  {p['admit']}\n{sha(p['guard'])}  {p['guard']}\nPINS",
         '[ "$(readlink -f ref-81e2f24e4e80426e80f0)" = ref-cda51cdb7487692d10e7 ] || refuse 11 "python3 is not python3.14"']
    if p['pytest']:
        L.append(f'v=$(cd / && env -i HOME="$I/home" PATH=ref-ccc203c53b7d040ba4dc:/bin ref-81e2f24e4e80426e80f0 -c "import pytest; print(pytest.__version__)") '
                 f'&& [ "$v" = {p["pytest"]} ] || refuse 11 "pytest [$v]"')
    L += ['[ -d "$R/src" ] && [ ! -L "$R/src" ] || refuse 12 "no source directory $R/src"']
    if p.get('x_out'):
        L.append(f'[ ! -e {q(p["x_out"])} ] || refuse 12 "X output already exists"')
    L += ['for d in home tmp; do',
          f'  [ -d "$I/$d" ] && [ ! -L "$I/$d" ] && [ "$(stat -c %u:%a "$I/$d")" = "{uid}:700" ] && [ -z "$(ls -A "$I/$d")" ] || refuse 13 "$I/$d not an owned empty 0700 directory"',
          'done',
          'ls=$(timeout 30 systemctl --user show "$UNIT" -p LoadState --value) || refuse 14 "systemctl show failed"',
          '[ "$ls" = not-found ] && [ ! -e "$CG" ] || refuse 14 "unit LoadState [$ls] or cgroup present"',
          "( cd \"$R/src\" && timeout 60 find . -type f -not -path './proposed-ops-output/*' -print0 | sort -z | xargs -0 -r sha256sum ) > \"$I/source-sha256.txt\" || refuse 12 \"source hashing failed\"",
          'echo "source files $(wc -l < "$I/source-sha256.txt") hashed to source-sha256.txt"',
          'timeout 60 python3 -I "$ADMIT" check --grant "$GRANT" --unit "$UNIT" --line-file "$I/launch.sh"; ck=$?',
          '[ "$ck" = 0 ] || refuse 15 "grant check rc $ck"',
          'stamp launch',
          'cd "$R/src" || refuse 12 "cd src"',
          f'timeout --kill-after=15s 150s systemd-run --user --scope --collect --quiet --unit={unit} \\',
          f'  --property=CPUQuota={c * 100}% --property=MemoryMax={mem_b} --property=MemorySwapMax=0 --property=RuntimeMaxSec=130 \\',
          '  -- ref-d9af09a16f3a81bf2ded -i ' + ' '.join(q(e) for e in env) + ' \\',
          f'  /bin/bash "$GUARD" "$I/guard.txt" "$UNIT" {q(f"{c * 100000} 100000")} {p.get("expect_mem", mem_b)} {c} {p["plugin"]} -- \\',
          '  ' + ' '.join(q(a) for a in p['argv']) + ' \\',
          '  < /dev/null > "$I/stdout.txt" 2> "$I/stderr.txt"',
          'RC=$?; echo "payload_rc=$RC"; tail -3 "$I/guard.txt"',
          'stamp collect',
          'S=$(timeout 30 systemctl --user show "$UNIT" -p LoadState,ActiveState,Result); src=$?; echo "show rc=$src $S"',
          'if [ "$src" = 0 ] && ! grep -qx "LoadState=not-found" <<<"$S"; then',
          '  timeout 30 systemctl --user stop "$UNIT"; echo "stop rc=$?"',
          '  timeout 30 systemctl --user reset-failed "$UNIT"; echo "reset-failed rc=$?"',
          '  S=$(timeout 30 systemctl --user show "$UNIT" -p LoadState,ActiveState,Result); src=$?; echo "show rc=$src $S"',
          'fi',
          'col=no; [ "$src" = 0 ] && grep -qx "LoadState=not-found" <<<"$S" && [ ! -e "$CG" ] && col=yes',
          'echo "collected=$col"',
          '[ "$col" = yes ] || finish UNCOLLECTED "$( [ "$RC" != 0 ] && echo "$RC" || echo 30 )" "payload_rc=$RC; no cleanup"',
          'stamp cleanup',
          'for d in tmp home; do',
          '  [ "$(realpath -e "$I/$d")" = "$I/$d" ] && timeout 60 rm -r --one-file-system "$I/$d"; [ ! -e "$I/$d" ] && echo "removed $d" || echo "NOT removed $d"',
          'done',
          'grep -qx "GUARD OK" "$I/guard.txt" || finish GUARD_FAIL "$RC" "payload not started; collected"',
          'finish DONE "$RC" "payload_rc=$RC collected"']
    return '\n'.join(L) + '\n'


def params(b, inv, tag, kind):
    s = BUILDERS[b]
    return dict(root=s['root'], inv=inv, unit=f'u4{b}-{tag}-1018.scope', argv=s[kind],
                x_out=s['x_out'] if kind == 'x' else None, plugin=s['plugin'], pytest=s['pytest'],
                admit=ADMIT, guard=GUARD, uid=1000, cores=2, mem_gib=4)


if __name__ == '__main__':
    for b in BUILDERS:
        for inv, tag, kind in INVOCATIONS:
            f = os.path.join(D, f'u4{b}-{inv}.sh')
            open(f, 'w').write(render(params(b, inv, tag, kind)))
            print(os.path.basename(f), hashlib.sha256(open(f, 'rb').read()).hexdigest(), os.path.getsize(f))
