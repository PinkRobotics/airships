"""Execute the production browser predicates against delayed and absent signals.

A virtual clock represents a slow hosted runner without slowing the fast gate.
The expressions are extracted from the drivers, not reimplemented here.
"""
import ast
import asyncio
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


def constant(path, name):
    tree = ast.parse((ROOT / path).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return ast.literal_eval(node.value)


def wind_expression(mode):
    tree = ast.parse((ROOT / 'tests/firstparty/check.py').read_text())
    function = next(n for n in tree.body if isinstance(n, ast.AsyncFunctionDef)
                    and n.name == 'wait_wind')
    namespace = {'json': json, 'WIND_STATE': constant('tests/firstparty/check.py', 'WIND_STATE')}
    exec(compile(ast.Module(body=[function], type_ignores=[]), '<driver>', 'exec'), namespace)
    class Capture:
        async def evaluate(self, expression):
            self.expression = expression
            return {'ready': True, 'state': {}}
    page = Capture()
    asyncio.run(namespace['wait_wind'](page, mode))
    return page.expression


HARNESS = r"""
const vm = require('node:vm'), assert = require('node:assert/strict');
const {source, scenario, expected} = JSON.parse(require('node:fs').readFileSync(0,'utf8'));
let now=0, ticks=0;
const state={ready:false,recordOnly:false,missions:[],windOk:true,planning:{state:'pending'}};
const window={__ierr:[]};
const note={hidden:true,click(){},textContent: scenario==='stale'?'Still air · wind mirror stale':
 scenario==='missing'?'Still air · HTTP 404':'850 hPa wind · site mirror · fetched under a minute ago'};
function progress(){
 state.ready=now>=90000;
 state.planning.state=now>=120000?'settled':'pending';
 state.missions=[{planState:now>=120000?'ready':'pending',idle:now<120000,wind:scenario==='stale'||scenario==='missing'?null:{}}];
 state.windOk=!(scenario==='stale'||scenario==='missing');
 if(now>=70000&&scenario!=='absent')window.AIRSHIPS={app:state,sim:{}};
 if(scenario==='never')state.planning.state='pending';
 if(now>=420000&&scenario==='suite')window.__tests={pass:1,fail:0,suites:[]};
}
progress();
const context={window,document:{title:'test',getElementById:()=>note,querySelector:()=>null,
 querySelectorAll:()=>[],},performance:{now:()=>now,getEntriesByType:()=>[]},
 Date:{now:()=>now},setTimeout(callback,delay){
  if(++ticks>15000)throw Error('callback cap');
  queueMicrotask(()=>{now+=delay;progress();callback();});
 }};
Object.defineProperty(context,'AIRSHIPS',{get:()=>window.AIRSHIPS});
context.S=state;
(async()=>{
 try{
  const value=await vm.runInNewContext(source,context,{timeout:2000});
  if(expected==='refuse'){
   if(typeof value==='object' && value && value.ready===false) {}
   else if(typeof value==='string' && JSON.parse(value).error) {}
   else if(value===false) {}
   else throw Error('partial output accepted');
   assert.ok(now>=300000,'refusal must use the bounded readiness budget');
  }else{
   assert.ok(now>=(scenario==='suite'?420000:120000),'readiness accepted too early');
   if(value && typeof value==='object' && 'ready' in value)assert.equal(value.ready,true);
   else assert.notEqual(value,false);
  }
 }catch(e){
  if(expected!=='refuse')throw e;
  assert.match(String(e),/deadline|within/,'missing handle must refuse explicitly');
  assert.ok(now>=300000);
 }
 console.log('PASS '+scenario+' '+now+'ms');
})().catch(e=>{console.error(e);process.exitCode=1});
"""


class ReadinessWaits(unittest.TestCase):
    def run_expression(self, source, scenario='late', expected='ready'):
        result = subprocess.run(['node', '-e', HARNESS],
            input=json.dumps(dict(source=source, scenario=scenario, expected=expected)),
            text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fresh_wind_waits_for_all_plans_after_data_arrives(self):
        self.run_expression(wind_expression('fresh'))

    def test_stale_and_missing_wind_wait_for_still_air_replanning(self):
        for mode in ('stale', 'missing'):
            with self.subTest(mode=mode): self.run_expression(wind_expression(mode), mode)

    def test_wind_never_settled_or_missing_handle_refuses(self):
        for mode in ('never', 'absent'):
            with self.subTest(mode=mode): self.run_expression(wind_expression('fresh'), mode, 'refuse')

    def test_firstparty_boot_waits_for_planning(self):
        self.run_expression(constant('tests/firstparty/check.py', 'BOOT'))

    def test_firstparty_boot_refuses_unsettled_planning(self):
        self.run_expression(constant('tests/firstparty/check.py', 'BOOT'), 'never', 'refuse')

    def test_interaction_boot_waits_for_complete_fleet(self):
        source=constant('tests/interaction/check.py','BOOT')
        source=source[:source.index("  const ov =")]+"return {ready:true};})()"
        self.run_expression(source)
        self.run_expression(source,'never','refuse')

    def test_guard_probe_and_heat_require_ready_planning(self):
        for name in ('PROBE','HEAT_AND_NULL'):
            source=constant('tests/guard/check.py',name)
            source=source[:source.index('  S.paused') if name=='PROBE' else source.index("  document.getElementById")]+"return {ready:true};})()"
            with self.subTest(probe=name):
                self.run_expression(source)
                self.run_expression(source,'never','refuse')

    def test_fleet_envelope_waits_for_settled_planning(self):
        source=constant('tests/energy/fleet-envelope.py','PROBE')
        source=source[:source.index('  S.paused')]+"return {ready:true};})()"
        self.run_expression(source)
        self.run_expression(source,'never','refuse')

    def test_golden_model_and_ui_wait_for_ready_handle(self):
        for rel,marker in [('tests/golden/dump.js','  /* One dump'),
                           ('tests/golden/ui-dump.js','  const ov =')]:
            source=(ROOT/rel).read_text();source=source[source.index('(async () => {'):source.index(marker)]+"return {ready:true};})()"
            with self.subTest(script=rel):
                self.run_expression(source)
                self.run_expression(source,'absent','refuse')

    def test_operations_producer_waits_for_complete_planning(self):
        source=constant('tools/gen_operations_records.py','READY')+'readyApp()'
        self.run_expression(source)
        self.run_expression(source,'never','refuse')

    def test_served_energy_waits_for_handle_and_planning(self):
        source=(ROOT/'tests/served-energy/page.js').read_text()
        source=source[:source.index('  const original=')]+"return {ready:true};}})()"
        self.run_expression(source)
        self.run_expression(source,'absent','refuse')

    def test_guard_assurance_refuses_ready_but_pending_planning(self):
        source=(ROOT/'tests/guard/assurance.js').read_text()
        source='(async()=>{'+source[source.index("  for (let i=") if "  for (let i=" in source else source.index('  // The page'):source.index('  S.paused')]+"return {ready:true};})()"
        self.run_expression(source)
        self.run_expression(source,'never','refuse')

    def test_browser_suite_can_finish_after_four_minutes(self):
        self.run_expression(constant('tests/browser/run.py','GRAB'),'suite')


if __name__ == '__main__': unittest.main()
