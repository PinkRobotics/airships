import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import test from 'node:test';

const paths = ['sim/config.js', 'research/reports/02-paper.md',
  'research/reports/03-diligence.md', 'docs/OPEN-QUESTIONS.md', 'research/evidence-map.md'];

test('the former unqualified diameter illustrations are absent from current rope prose', () => {
  for (const file of paths.slice(0, 3)) assert.equal(/(?:440|163|128)\s*mm/i.test(readFileSync(file, 'utf8')),
    false, file + ': specify strength and safety policy before a diameter');
});

test('every live rope disclosure names minimum strength, pickup and safety policy', () => {
  for (const file of paths) {
    const text = readFileSync(file, 'utf8');
    const region = text.match(/anchor-rope:basis:start([\s\S]*?)anchor-rope:basis:end/);
    assert.ok(region, file + ': missing rope basis disclosure');
    assert.match(region[1], /minimum break strength/i, file);
    assert.match(region[1], /quasi-static pickup/i, file);
    assert.match(region[1], /safety factor[^\n]*5/i, file);
    assert.match(region[1], /(?:self-weight|self weight)/i, file);
    assert.match(region[1], /dry-mass budget/i, file);
  }
});

test('the bottom-up budget charges the cable at its stated strength and safety policy', () => {
  const code = `import importlib.util,json
s=importlib.util.spec_from_file_location('budget','research/analysis/mass-budget.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
f=json.loads(b.FIGURES.read_text());b.ATMOSPHERE=f['atmosphere']
r=[]
for name,d in f['classes'].items():
 spec=d['spec']
 for case in ['floor','credible','demonstrated']:
  lines=b.budget(spec,d['lift'],d['energy'],d['cycle'],case)
  cable=next(x for x in lines if x['item']=='Anchor cable')
  r.append(dict(name=name,case=case,pull=spec['anchorBagT']*9810,length=spec['anchorCableM'],sf=b.ev('rope_safety_factor',case),specific=b.ev('rope_n_per_kg_per_m',case),tonnes=cable['tonnes'],components=[x['item'] for x in lines]))
print(json.dumps(r))`;
  const p = spawnSync('python3', ['-B', '-c', code], {encoding: 'utf8'});
  assert.equal(p.status, 0, p.stderr);
  for (const r of JSON.parse(p.stdout)) {
    // The explicit prose policy: assumed minimum strength, not a selected product.
    assert.equal(r.sf, {floor: 3, credible: 5, demonstrated: 7}[r.case]);
    assert.equal(r.specific, {floor: 2.0e6, credible: 1.5e6, demonstrated: 1.4e6}[r.case]);
    const expected = r.pull * r.sf / r.specific * r.length / 1000;
    assert.ok(Math.abs(r.tonnes - expected) < 0.005000001, `${r.name}/${r.case}`);
    for (const component of ['Anchor cable', 'Anchor bag', 'Winch']) assert.ok(r.components.includes(component));
  }
});
