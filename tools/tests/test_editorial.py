"""Counterexamples for editorial record bindings; no feeds or physical tests."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import gen_assembly_prose as assembly

class AssemblyProse(unittest.TestCase):
    def test_current_counts_and_all_failures(self):
        text=assembly.outputs()[assembly.FILE]
        self.assertIn('12 of the 16 proofs pass',text)
        self.assertIn('P12 passes',text)
        for name in ('P8','P11','P13','P16'):self.assertIn('| '+name+' —',text)
        self.assertIn('18 frozen defects',text)
    def test_changed_report_status_cannot_hide_in_summary(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as folder:
            root=Path(folder)
            for file in (assembly.FILE,'research/geometry/nodes/assembly.json','research/geometry/nodes/contract.json'):
                p=root/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((assembly.ROOT/file).read_bytes())
            p=root/'research/geometry/nodes/assembly.json';j=json.loads(p.read_text());j['proofs'][0]['passed']=False;p.write_text(json.dumps(j))
            with self.assertRaises(AssertionError):assembly.outputs(root)
    def test_typed_counts_are_rejected(self):
        result=assembly.outputs()[assembly.FILE]
        self.assertNotIn('The five proofs still failing',result)

from check_cell_evidence import evidence_errors
class EvidenceWords(unittest.TestCase):
    def setUp(self):self.ledger=json.loads((assembly.ROOT/'research/analysis/float-ledger.json').read_text())
    def test_old_cell_and_catalogue_claims_are_red(self):
        for text in ('one cell, as built & billed','billed from the measured saw table and the weighed joints','kg, measured','proven on the article'):
            self.assertTrue(evidence_errors([text],self.ledger),text)
    def test_denial_and_proposed_tests_are_not_evidence_claims(self):
        for text in ('No cell has been built and no joint has been physically weighed or tested.','equipment lines: named, not yet weighed','A future programme would test joints.','Closing the gap needs knockdown tests.'):
            self.assertEqual(evidence_errors([text],self.ledger),[],text)
    def test_computation_cannot_launder_physical_word(self):
        self.assertTrue(evidence_errors(['Computed mass; the joints have been weighed.'],self.ledger))
        self.assertTrue(evidence_errors(['No cell has been built, but its joints have been weighed.'],self.ledger))
        self.assertTrue(evidence_errors(['The programme needs tests and the joints are tested.'],self.ledger))
        self.assertTrue(evidence_errors(['No uncertainty remains: the joints have been weighed.'],self.ledger))
        self.assertTrue(evidence_errors(['The model is not final because the joints were weighed.'],self.ledger))

import gen_editorial_prose as editorial
class ReportFences(unittest.TestCase):
    def test_known_balanced_report_fences_preserve_prose(self):
        import md2tex
        for src,name in [('02-paper.md','anchor-rope:basis'),('03-diligence.md','anchor-rope:basis'),('03-diligence.md','editorial:drop-hull')]:
            text=f'<!-- {name}:start -->\nA qualified model paragraph.\n<!-- {name}:end -->\n'
            result=md2tex.convert(text,set(),src)
            self.assertIn('A qualified model paragraph.',result)
            self.assertNotIn('<!--',result)
    def test_unknown_inline_duplicate_reversed_and_unbalanced_fences_fail(self):
        import md2tex
        start='<!-- anchor-rope:basis:start -->';end='<!-- anchor-rope:basis:end -->'
        for src,text in [('02-paper.md',start+'\nMissing end.\n'),('02-paper.md',end+'\nReversed.\n'+start),('02-paper.md',start+'\n'+start+'\nDuplicate.\n'+end),('02-paper.md','Inline '+start+' text '+end),('01-brief.md',start+'\nWrong report.\n'+end),('02-paper.md','<!-- unknown:basis:start -->\nUnknown.\n<!-- unknown:basis:end -->')]:
            with self.subTest(src=src,text=text):
                with self.assertRaises(SystemExit):md2tex.convert(text,set(),src)

class CurrentHull(unittest.TestCase):
    def test_lengths_follow_record_mutation(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as folder:
            root=Path(folder);f='research/analysis/energy-documents.json';p=root/f;p.parent.mkdir(parents=True)
            for name in ('editorial-controls','mass-budget','descent','release-states'):
                q=root/('research/analysis/'+name+'.json');q.write_bytes((editorial.ROOT/q.relative_to(root)).read_bytes())
            j=json.loads((editorial.ROOT/f).read_text());j['classes'][0]['lengthM']=123;j['classes'][-1]['lengthM']=567;p.write_text(json.dumps(j))
            s=editorial.sections(root)
            self.assertIn('123 m reference hull',s['certification']);self.assertIn('567 m',s['drop-hull']);self.assertIn('567 m',s['turbulence'])
    def test_current_cooling_location(self):self.assertEqual(editorial.cooling_errors(),[])
    def test_original_cooling_premise_is_red(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as folder:
            root=Path(folder)
            for f in ('docs/VERIFICATION-PLAN.md','research/analysis/mass-budget.md'):
                p=root/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('What do drives need to reject heat with no convection?')
            self.assertTrue(editorial.cooling_errors(root))

class CurrentEnergy(unittest.TestCase):
    def test_record_changes_propagate_to_register_and_conclusions(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as folder:
            root=Path(folder)
            files=('energy-documents','editorial-controls','mass-budget','descent','release-states')
            for name in files:
                f='research/analysis/'+name+'.json';p=root/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((editorial.ROOT/f).read_bytes())
            p=root/'research/analysis/mass-budget.json';j=json.loads(p.read_text());j['classes']['P100']['descentWithoutNitrogen']['cycleSavingPct']=12.3;j['classes']['P100']['descentWithoutNitrogen']['marginX']=4.5;p.write_text(json.dumps(j))
            p=root/'research/analysis/editorial-controls.json';j=json.loads(p.read_text());j['classes']['P100']['doubledDiscChangePct']=33.333;j['classes']['P100']['netNitrogenPct']=12.345;p.write_text(json.dumps(j))
            s=editorial.sections(root)
            self.assertIn('12.3%',s['nitrogen-register']);self.assertIn('4.5×',s['nitrogen-register']);self.assertIn('33.3%',s['disc-register']);self.assertIn('12.3%',s['nitrogen-conclusion'])
            self.assertIn('not a saving in operation',s['disc-register'])

class AcceptedRelease(unittest.TestCase):
    def test_replay_refuses_changed_water_record(self):
        import subprocess
        script="""import {replayRelease,record} from './tools/gen_release_states.mjs';
        const r=record().classes.P100;let failed=false;
        try{replayRelease('P100',{...r.plan,retainedT:r.plan.retainedT+1});}catch(e){failed=true;}
        if(!failed)process.exit(1);
        if(replayRelease('P100',{state:'unavailable'}).states)process.exit(2);
        console.log('release refusal: altered water record rejected; unavailable plan has no estimate');"""
        p=subprocess.run(['node','--input-type=module','-e',script],cwd=editorial.ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
    def test_basis_and_local_density_are_visible(self):
        s=editorial.sections()['release-illustration']
        self.assertIn('Local density',s);self.assertIn('retaining',s);self.assertIn('ideal-disc',s)
        self.assertIn('Neither quantity measures outlet flow',s)
