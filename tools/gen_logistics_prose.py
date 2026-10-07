#!/usr/bin/env python3
"""Render the accepted-plan logistics comparisons; --check never writes."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT/'research/analysis'


def table(heads, rows):
    return '| ' + ' | '.join(heads) + ' |\n|' + '|'.join('---' for _ in heads) + '|\n' + ''.join(
        '| ' + ' | '.join(map(str, row)) + ' |\n' for row in rows)


def render():
    w = json.loads((A/'water-availability.json').read_text())
    d = json.loads((A/'delivery.json').read_text())
    names = {'P100':'P-100', 'P1000':'P-1000', 'P10000':'P-10000'}
    def number(x, fmt='.1f'):
        return 'not served' if x is None else format(x, fmt)
    rates = 'The flight model assumes a buoyant fleet for these logistics quotients; this does not establish that a drawn hull floats.\n\n' + table(['Class', '15 km worked example t/h', 'Median leg t/h', 'Mean accepted fire legs t/h', 'Mean accepted legs, hectare-weighted t/h'],
        [[names[cid]] + [number(c['throughputTph'][k], ',.1f') for k in
            ('atWorkedExample15km','atMedianByFire','meanOverFires','meanOverHectares')]
         for cid,c in w['classes'].items()])
    for key, label in [('workedExample','15 km worked example'),('medianByFire','median leg')]:
        rates += '\n' + label.capitalize() + ':\n\n' + table(
            ['Class','Leg km','State / mode','Released t','Retained t','Supplied MWh/cycle'],
            [[names[cid],number(c['acceptedPlans'][key]['km'],'.2f'),
              c['acceptedPlans'][key]['state']+' / '+str(c['acceptedPlans'][key]['mode']),
              *[number(c['acceptedPlans'][key][k],'.3f') for k in ('releasedT','retainedT','suppliedMWh')]]
             for cid,c in w['classes'].items()])
    rates += '\n' + table(['Class','Accepted fire legs','Not served','Stand-downs','Unavailable'],
        [[names[cid],*[c['logisticsService'][k] for k in ('acceptedFires','notServedFires','standDowns','unavailable')]]
         for cid,c in w['classes'].items()])
    rates += ('\nThe selector is `selectServedPlan`, requested balanced, record energy basis, '
              'still air. It chooses among the served pages\' bounded controls at each exact leg; '
              'this is not a global optimum. Stand-down or unavailable legs supply no rate and '
              'are excluded from both means. Geometric water access above is a separate count.\n')
    geometry = w['geometry']['P100']
    if geometry["drawTonnesPer12h"] is None:
        draw = "The P-100 worked example is not served; no twelve-hour drawdown quotient is supplied.\n"
    else:
        draw = (f"A P-100 repeating the accepted 15 km plan for twelve hours releases "
                f"{geometry['drawTonnesPer12h']:,} t, a geometric drawdown of "
                f"{geometry['drawdownMetresPer12hOnMinBody']*100:.1f} cm on a minimum-size body. "
                'Continuous supply and lake access are assumed.\n')
    onepass = table(['Swath','P-100 CL','P-1000 CL','P-10000 CL'],
        [[f'{s} m',*[number(d['classes'][cid]['coverageLevelBySwath'][f'{s} m']) for cid in names]]
         for s in (20,30,50,80)])
    onepass += '\n' + table(['Class','Released t','Run km','Retained t'],
        [[names[cid],number(c['payloadT'],'.3f'),number(c['runKm']),
          number(c['workedExamplePlan']['retainedT'],'.3f')] for cid,c in d['classes'].items()])
    onepass += '\nThese are tank-release quotients for the accepted 15 km plans, at assumed swaths. No ground deposition or suppression is established.\n'
    median = d['classes']['P100']['atRealMedianLeg']
    p = median['plan']
    daily = table(['Coverage level','Geometric line km per 24 h','Stored simplified perimeters no longer than that line'],
        [[f'CL {cl}',number(median[f'lineKmPer24hAtCL{cl}_30mSwath'])+' km',
          number(median[f'pctOfPerimetersLinedDailyAtCL{cl}'])+'%'] for cl in (2,4,6,8)])
    if median['tph'] is None:
        daily += f"\nThe median leg is {median['legKm']:.2f} km; its selector state is {p['state']}. No daily release, supplied-energy or perimeter quotient is available.\n"
        summary = 'The P-100 median leg is not served by an accepted plan; no daily line-length or perimeter comparison is supplied.\n'
    else:
        daily += (f"\nAt the {median['legKm']:.2f} km median shore-proxy distance the accepted {p['mode']} plan releases "
                  f"{p['releasedT']:.3f} t and retains {p['retainedT']:.3f} t per cycle. "
                  f"Its rate is {median['tph']:.1f} t/h, with {p['suppliedMWh']:.3f} MWh supplied "
                  f"per {p['cycleMin']:.3f} minute cycle. Repeating it for 24 hours gives "
                  f"{median['tonnesPer24h']:,} t released and requires "
                  f"{median['suppliedMWhPer24h']:.1f} MWh of supplied effort. "
                  f"Stand-downs across the fire-leg dataset: {w['classes']['P100']['logisticsService']['standDowns']}.\n\n"
                  'The table compares line length at an assumed 30 m swath with stored simplified '
                  'final perimeter lengths. Those outlines are lower bounds on a convoluted edge. '
                  'It establishes neither deposition nor coverage of an actual fire, continuous '
                  'operation or supply, suppression, or a changed fire outcome.\n')
        summary = (f"At the accepted median-leg rate, the conditional CL 4 line-length quotient is "
                   f"{median['lineKmPer24hAtCL4_30mSwath']:.1f} km per day, longer than "
                   f"{median['pctOfPerimetersLinedDailyAtCL4']:.1f}% of the stored simplified final "
                   'perimeters; this is a geometric comparison, with no fire-outcome inference.\n')
    return [
        ('research/analysis/water-availability.md','rates',rates),
        ('research/analysis/water-availability.md','drawdown',draw),
        ('research/analysis/delivery.md','one-pass',onepass),
        ('research/analysis/delivery.md','daily',daily),
        ('docs/VERIFICATION-PLAN.md','line-comparison',summary),
        ('docs/OPEN-QUESTIONS.md','line-summary',summary),
    ]


def main():
    args=argparse.ArgumentParser();args.add_argument('--check',action='store_true');args.add_argument('--emit',action='store_true');opts=args.parse_args()
    bad=[];outputs={}
    for file,key,body in render():
        path=ROOT/file; text=outputs.get(file,path.read_text())
        start=f'<!-- logistics:{key}:start -->';end=f'<!-- logistics:{key}:end -->'
        if text.count(start)!=1 or text.count(end)!=1:
            raise ValueError(f'{file}: missing unique logistics markers for {key}')
        left,rest=text.split(start);_,right=rest.split(end)
        fresh=left+start+'\n'+body+end+right
        outputs[file]=fresh
        if fresh!=text and not opts.emit:
            if opts.check:bad.append(file+':'+key)
            else:path.write_text(fresh)
    if opts.emit:
        print(json.dumps(outputs));return 0
    if bad:
        print('logistics prose RED: '+', '.join(bad));return 1
    print('logistics prose: six regions match accepted-plan outputs');return 0


if __name__=='__main__':sys.exit(main())
