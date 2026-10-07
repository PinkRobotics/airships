"""Reject physical evidence language unsupported by the float ledger."""
import json
import re
from pathlib import Path
from browser_probe import run_probe

WORDS=re.compile(r'\b(?:built|billed|measured|weighed|tested|proven|tests?|proves?)\b',re.I)

def evidence_errors(blocks, ledger):
    # No physical row exists on the present ledger. A future measured row must carry
    # an object identity and evidence record before this checker can accept it.
    if 'measured' not in ledger['evidenceClasses']:return ['ledger has no physical evidence class']
    physical=[c for d in ledger['designs'] for c in d['cases'] if c.get('evidence')=='measured']
    errors=[]
    for text in blocks:
        for sentence in re.split(r'(?<=[.!?])\s+',text):
            if not WORDS.search(sentence):continue
            # Denials and explicit future requirements describe evidence that is absent.
            for clause in re.split(r'[,;:]|\b(?:but|however|and)\b',sentence,flags=re.I):
                previous_denial=False
                previous_end=0
                for word in WORDS.finditer(clause):
                    prefix=clause[:word.start()]
                    denial=(re.search(r'\b(?:not|never)(?:\s+(?:yet|been|physically|actually|ever))*\s*$',prefix,re.I) or
                        re.fullmatch(r'\s*(?:no\s+(?:cells?|joints?|nodes?|articles?|hardware|parts?)|neither|nothing)'
                        r'(?:\s+(?:on|in|this|the|page|here|has|have|was|were|is|are|been|physically|actually|ever))*\s*',prefix,re.I) or
                        (previous_denial and re.fullmatch(r'\s*or\s*',clause[previous_end:word.start()],re.I)))
                    previous_denial=bool(denial)
                    previous_end=word.end()
                    future=(word.group().lower() in ('test','tests') and
                            re.search(r'\b(?:needs?|would|will)\b[^.!?]*$',prefix,re.I))
                    if denial or future:continue
                    errors.append('unsupported physical evidence: '+clause.strip())
    if physical:errors.append('physical ledger rows need object-specific evidence bindings before page claims are accepted')
    return errors

PROBE=r"""(async()=>{
 const blocks=[...document.querySelectorAll('p, h1, h2, h3, figcaption, .lbl, .chip')].map(e=>e.innerText);
 const pane=document.querySelector('#pane-a');
 if(!pane)throw new Error('catalogue pane missing');
 const {CATS,CATALOG}=await import('../ship/catalog.js');
 const cards=[];let visits=0;
 for(const cat of CATS){
   pane.querySelector('[data-tab="'+cat.id+'"]').click();
   const items=CATALOG.filter(c=>c.cat===cat.id);
   for(const item of items){visits++;
     cards.push(...[...pane.querySelectorAll('.part-head,.part-role,.specs dd,.part-story,.flags li,.prov')].map(e=>e.innerText));
     pane.querySelector('[data-nav="1"]').click();
   }
 }
 return {blocks:blocks.concat(cards),cards:visits,expected:CATALOG.length};
})()"""

def check_served(root,td,base):
    probe=Path(td)/'evidence-probe.js';probe.write_text(PROBE)
    result=run_probe(root,base+'cell/levels.html',probe,Path(td)/'evidence.json',8)
    ledger=json.loads((root/'research/analysis/float-ledger.json').read_text())
    errors=evidence_errors(result['blocks'],ledger)
    if result['cards']!=result['expected']:errors.append('catalogue traversal missed cards')
    print(f"cell evidence: {result['cards']} served catalogue cards and cell text checked against ledger evidence classes; {len(errors)} errors")
    return errors
