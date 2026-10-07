"""Ground mass arithmetic and a context-specific wrong-manifest plant."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import check_analysis as gate

class PlantMass(unittest.TestCase):
    def test_source_output_match_and_wrong_manifest(self):
        spec=importlib.util.spec_from_file_location('mass_budget',ROOT/'research/analysis/mass-budget.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        figures=json.loads((ROOT/'research/figures.json').read_text())
        c=figures['classes']['P100']
        q=m.plant_comparisons(c['spec'],c['lift'],c['energy'],c['cycle'],figures['assumptions'])
        # Independently dimensionalised from the ground specification, printed page 11:
        # equipment kg / usable atmospheric litres/hour, with stipulated liquid density.
        expected=(2200/1000)/(21*0.808/1000)
        self.assertAlmostEqual(q['massPerOutputTph'],expected,places=10)
        self.assertAlmostEqual(q['inputTPerMW'],2200/(34/1000)/1000,places=10)
        output_tph=c['spec']['cryoMW']*1000/(figures['assumptions']['eLN2']*1000)
        self.assertEqual(q['outputMatched']['plantT'],round(output_tph*expected,2))
        # Generated source-caption inputs must retain the exact checked-region owner.
        import claims
        from claims_rules import Context
        targets={f"{q['source']['massKg']:.0f}",f"{q['source']['usableLitresHour']:.0f}"}
        occurrences=claims.extract(ROOT,ROOT/'dist.manifest')['occurrences']
        caption=[o for o in occurrences if o['file']=='research/analysis/mass-budget.md'
                 and o['text'].startswith('The ground StirLIN specification gives')
                 and o['raw'] in targets]
        self.assertEqual({o['raw'] for o in caption},targets)
        context=Context(ROOT,['research/analysis/mass-budget.md'])
        for occurrence in caption:
            self.assertEqual(occurrence['region'],'mass-budget:plant-comparators')
            self.assertEqual(context.generator_owner(occurrence),
                (dict(kind='generated',generator='tools/gen_mass_budget_prose.py',
                      region='mass-budget:plant-comparators'),'analysischeck'))
        print('GREEN source-caption claims: exact checked-region ownership retained')
        _,bad,_=gate.check_rows()
        self.assertEqual(bad,[])
        original=gate.MANIFEST
        field='classes/P100/plantComparisons/outputMatched/plantT'
        wrong='classes/P100/plantComparisons/inputMatched/plantT'
        try:
            gate.MANIFEST=[(md,name,wrong if path==field else path,fmt)
                           for md,name,path,fmt in original]
            # Retain the output-row context, so an input-row witness cannot pass.
            before=gate.CONTEXTS.get(('mass-budget.md',wrong))
            gate.CONTEXTS[('mass-budget.md',wrong)]=gate.CONTEXTS[('mass-budget.md',field)]
            _,bad,_=gate.check_rows()
            self.assertTrue(any('388.24' in e and 'mass-budget.md' in e for e in bad),bad)
            print('RED planted mass manifest: input-matched value refused in output row')
        finally:
            gate.MANIFEST=original
            if before is None:gate.CONTEXTS.pop(('mass-budget.md',wrong),None)
            else:gate.CONTEXTS[('mass-budget.md',wrong)]=before
        _,bad,_=gate.check_rows();self.assertEqual(bad,[])
        print('GREEN ground output arithmetic: specification input/output and restored manifest')

if __name__=='__main__':unittest.main()
