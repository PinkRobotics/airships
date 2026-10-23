"""Focused smoke of card5.render5 on Ops' OWN fixtures (no B path, no B job, no governance): python3 smoke5.py <scratch>.
Each case is its own tiny repo whose tools/float_ledger.py behaves per case; --check always re-derives and compares.
U unchanged pair, J json only, M md only, B both -> PASS; T extra tracked change, N extra untracked file, S shard drift,
G git failure (worktree link removed), H HEAD drift (commit), I index drift (changed ledger.json, then git add) -> FAIL 22. Evidence -> smoke-v5/."""
import hashlib, json, os, shutil, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import card3, card5
S = sys.argv[1]; EV = os.path.join(D, 'smoke-v5'); os.makedirs(EV, exist_ok=True)
def sh(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
def git(*a): r = sh(['git', *a]); assert r.returncode == 0, (a, r.stderr); return r.stdout.strip()
NEW = '{"reason": "reviewed"}\n'; NEW_SHA = hashlib.sha256(NEW.encode()).hexdigest()
ACT = {'U': '', 'J': 'J', 'M': 'M', 'B': 'JM', 'T': 'T', 'N': 'N', 'S': 'S', 'G': 'G', 'H': 'H', 'I': 'JI'}
EXPECT = {'U': 0, 'J': 0, 'M': 0, 'B': 0, 'T': 22, 'N': 22, 'S': 22, 'G': 22, 'H': 22, 'I': 22}
def generator(acts):
    return ('import pathlib, subprocess, sys, os\nr = pathlib.Path(".")\nA = ' + repr(acts) + '\n'
            'want = {"ledger.json": "{\\"v\\": 1}\\n" + ("j\\n" if "J" in A else ""), "ledger.md": "# l\\n" + ("m\\n" if "M" in A else "")}\n'
            'if "--check" in sys.argv:\n    sys.exit(0 if all((r / k).read_text() == v for k, v in want.items()) else 1)\n'
            'for k, v in want.items(): (r / k).write_text(v)\n'
            'if "T" in A: (r / "other.txt").write_text("changed\\n")\n'
            'if "N" in A: (r / "new-untracked.txt").write_text("n\\n")\n'
            'if "S" in A: (r / "shard.json").write_text("{\\"reason\\": \\"drifted\\"}\\n")\n'
            'if "H" in A: subprocess.run(["git", "-c", "user.email=s@l", "-c", "user.name=s", "commit", "--allow-empty", "-q", "-m", "drift"], check=True)\n'
            'if "I" in A: subprocess.run(["git", "add", "ledger.json"], check=True)\n'
            'if "G" in A: os.rename(".git", ".git-moved")\n')
admit = f'{S}/admit/admit.py'; os.makedirs(os.path.dirname(admit)); shutil.copy2(card3.ADMIT, admit)
pins = [(hashlib.sha256(open(f, 'rb').read()).hexdigest(), f) for f in (card3.COMMON['pins'][0][1], card3.COMMON['pins'][1][1])]
results = {}
for name, acts in ACT.items():
    clone = f'{S}/clone-{name}'; os.makedirs(f'{clone}/tools')
    git('init', '-q', clone); git('-C', clone, 'config', 'user.email', 'ops@local'); git('-C', clone, 'config', 'user.name', 'ops')
    open(f'{clone}/tools/float_ledger.py', 'w').write(generator(acts))
    for n, t in (('shard.json', '{"reason": "old"}\n'), ('ledger.json', '{"v": 1}\n'), ('ledger.md', '# l\n'), ('other.txt', 'x\n')):
        open(f'{clone}/{n}', 'w').write(t)
    git('-C', clone, 'add', '-A'); git('-C', clone, 'commit', '-qm', 'base')
    head = git('-C', clone, 'rev-parse', 'HEAD'); tree = git('-C', clone, 'rev-parse', 'HEAD^{tree}')
    g = name; cache = f'opsu3s5{name.lower()}'
    p = dict(card3.COMMON, root=f'{S}/root', clone=clone, head=head, tree=tree, entries=5, pins=pins, rtname='opsu3s5r',
             admit=admit, group=g, src_group=g, cache=cache, unit=f'opsu3-smoke5-{name.lower()}-1018.service',
             cores=1, mem=1, tasks=64, runtime=60, targets='REPAIRCHAIN')
    r = f'{S}/root/{g}'; os.makedirs(f'{S}/root', mode=0o700, exist_ok=True)
    for d in ('', '/home', 'unpublished-local-ref:e9671acd244849c5', '/bin'): os.makedirs(r + d, mode=0o700, exist_ok=True); os.chmod(r + d, 0o700)
    os.symlink(card3.COMMON['chrome'], f'{r}/bin/chromium')
    git('-C', clone, 'worktree', 'add', '-q', '--detach', f'{r}/src', head)
    open(f'{r}/src/shard.json', 'w').write(NEW)
    line = os.path.join(EV, f'group-{g}.sh')
    open(line, 'w').write(card5.render5(p, shard='shard.json', shard_sha=NEW_SHA, generated=['ledger.json', 'ledger.md']))
    shutil.copy2(line, f'{r}/launch.sh')
    out = sh(['python3', '-I', admit, 'request', '--seat', 'operations-smoke', '--job', p['unit'].split('.')[0], '--cores', '1',
              '--mem-gib', '1', '--hours', repr(60 / 3600), '--line-file', line, '--unit', p['unit'], '--cwd', r]).stdout.splitlines()
    assert out[-2].startswith('GRANT '), out[-3:]; gid = out[-2].split()[1]
    rc = sh(['bash', f'{r}/launch.sh', gid], timeout=400).returncode
    st = open(f'{r}/status.txt').read().strip() if os.path.exists(f'{r}/status.txt') else '(none)'
    for f in ('launch.log', 'status.txt'):
        if os.path.exists(f'{r}/{f}'): shutil.copy2(f'{r}/{f}', os.path.join(EV, f'{g}-{f}'))
    ok = rc == EXPECT[name]
    results[name] = {'acts': acts, 'expect': EXPECT[name], 'rc': rc, 'as_expected': ok, 'status': st}
    print(name, 'expect', EXPECT[name], 'rc', rc, 'OK' if ok else 'MISMATCH', '|', st[:150])
    shutil.rmtree(f'unpublished-local-ref:4d7c5da4fdbd5289{cache}', ignore_errors=True)
results['units_left'] = sh(['systemctl', '--user', 'list-units', '--all', '--no-legend', 'opsu3-smoke5-*']).stdout.strip()
results['cache_left'] = sorted(x for x in os.listdir('unpublished-local-ref:8e591a9489706044') if x.startswith('opsu3s5'))
results['all_as_expected'] = all(v['as_expected'] for k, v in results.items() if isinstance(v, dict))
json.dump(results, open(os.path.join(EV, 'results.json'), 'w'), indent=1)
print('all as expected:', results['all_as_expected'], 'units left', repr(results['units_left']), 'cache left', results['cache_left'])
