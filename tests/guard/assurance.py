"""End-to-end invented guard regressions, integrated by check.py."""
import importlib.util, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('guard_gate',ROOT/'tests/guard/check.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def run(part):
    js=(ROOT/'tests/guard/assurance.js').read_text().replace('PART',json.dumps(part))
    with g.serve() as base:
        v=g.probe_once(base,'?view=exercise&seed=7',js,5)
    print(json.dumps(v,sort_keys=True),flush=True)
    if part in ('A','B'):
        assert v['referenceContainsWitness'],v
        assert v['blocked']['ready']==0 and v['blocked']['insideComplete']==0,v
        assert v['blocked']['pointBlocked'] and v['blocked']['refused'],v
        assert v['control']['ready']>0 and v['control']['sampled']>0 and v['control']['insideComplete']==0,v
        if part=='B': assert v['blocked']['closed'] and v['blocked']['normalizedVertices']==242,v
    elif part=='C':
        assert v['control']['ok'] and v['control']['blocked'],v
        assert all(not b['ok'] and not b['fleet'] and 'coordinate' in b['reason'] for b in v['bad']),v
        assert all(not b['ok'] and 'coordinate' in b['reason'] for b in v['outlines']),v
        assert not v['context']['ok'],v
        page_coordinate_refusal()
    elif part=='D':
        assert v['direct']=='refused' or all(v['direct']),v
        assert v['baseOutside']==v['cycleOutside']==0,v
        assert v['impossible']=='refused',v
        assert v['refusedTargets']>0,v
        assert v['dispatch']['heldOut'] and 'geometric' in v['dispatch']['words'],v
    elif part=='E':
        assert not v['validFleet'] and not v['bad']['ok'] and not v['bad']['fleet'],v
        assert 'calendar' in v['bad']['reason'],v
        assert all(not d['fleet'] for d in v['invalid']),v
        assert all(d['fleet'] for d in v['controls']),v
    return 'invented regression '+part+' passed, with valid control'

def page_coordinate_refusal():
    doc={'defaultKeepOutKm':25,'noFleet':[],'fires':[],'places':[{'name':'Invented place','ll':[123,50],'date':'2030-09-01','basis':'order','keepOutKm':25,'source':'https://example.test/place'}]}
    from serve import serve_tree
    outcomes=[]
    for malformed in (False,True):
        payload=json.dumps(doc).replace('[123, 50]','[1e400, 50]' if malformed else '[123, 50]').encode()
        class Inject(g.Handler):
            def do_GET(self):
                if self.path.split('?')[0]=='/data/season/2026.guard.json':
                    self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(payload)
                else:super().do_GET()
        js=(ROOT/'tests/guard/assurance.js').read_text().replace('PART',json.dumps('C-page'))
        with serve_tree(ROOT,handler=Inject) as base:
            v=g.probe_once(base,'?view=exercise&seed=7',js,5)
        outcomes.append({k:v[k] for k in ('ok','reason','recordOnly','missions','ready','standDown')})
        print(json.dumps(outcomes[-1],sort_keys=True),flush=True)
        if malformed:
            assert not v['ok'] and v['recordOnly'] and v['missions']==v['ready']==0,v
            assert 'coordinate' in v['reason'] and ('coordinate' in v['words'] or 'guard' in v['words']),v
        else:assert v['ok'] and not v['recordOnly'] and v['ready']>0,v
    return outcomes

if __name__=='__main__':
    for part in sys.argv[1:] or list('ABCDE'):
        print(run(part),flush=True)
