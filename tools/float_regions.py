"""Generated-region contracts: exact markers, tracked producer, checked regeneration."""
import json
from pathlib import Path
import re
import subprocess


def tracked(root):
    p = subprocess.run(['git','ls-files','-z'],cwd=root,capture_output=True,text=True)
    return set(p.stdout.split('\0')) if p.returncode == 0 else set()


def region(body, start, end):
    lines = body.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip('\r\n') == start]
    ends = [i for i, line in enumerate(lines) if line.rstrip('\r\n') == end]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError('expected one pair of exact, ordered region markers')
    return ''.join(lines[starts[0]:ends[0]+1]), starts[0]+1, ends[0]+1


class Regions:
    def __init__(self, root, targets):
        self.root, self.targets = root, targets
        self.tracked = tracked(root)
        self.cache = {}
        self.emissions = {}

    def check(self, entry, hit):
        key = json.dumps({k:entry.get(k) for k in ('file','generator','gate','region','verifier')},sort_keys=True)
        if key not in self.cache:
            self.cache[key] = self.validate(entry)
        errors, bounds = self.cache[key]
        errors = list(errors)
        if bounds and not bounds[0] <= int(hit['line']) <= bounds[1]:
            errors.append('block is outside its generated region')
        return errors

    def validate(self, entry):
        errors = []
        gen, gate, verifier = (entry.get(k,'') for k in ('generator','gate','verifier'))
        if gen not in self.tracked or not (self.root/gen).is_file():
            errors.append('generated region requires an existing tracked generator')
        if gate not in self.targets or gate in ('ledgercheck','ledgercheck-selftest'):
            errors.append('generated region check must run in make check')
        if verifier not in self.tracked or not (self.root/verifier).is_file():
            errors.append('generated region requires a tracked regeneration verifier')
        if errors:
            return errors, None
        # A named target must actually invoke this verifier. The verifier must name the
        # producer; ledgercheck itself independently compares the fresh region below.
        p = subprocess.run(['make','-n',gate],cwd=self.root,capture_output=True,text=True)
        if p.returncode or verifier not in p.stdout or gen not in (self.root/verifier).read_text():
            errors.append('named check does not invoke the region regeneration verifier')
        markers = entry.get('region',{})
        start, end = markers.get('start',''), markers.get('end','')
        if not start or not end or start == end:
            return errors+['generated region requires distinct exact start and end markers'], None
        try:
            actual, lo, hi = region((self.root/entry['file']).read_text(),start,end)
        except (OSError,ValueError) as exc:
            return errors+[str(exc)], None
        command = ['node' if gen.endswith(('.mjs','.js')) else 'python3',gen,'--emit']
        try:
            if gen not in self.emissions:
                p = subprocess.run(command,cwd=self.root,capture_output=True,text=True,timeout=120)
                if p.returncode:
                    raise ValueError('fresh region regeneration failed')
                self.emissions[gen] = json.loads(p.stdout)
            outputs = self.emissions[gen]
            fresh, _, _ = region(outputs[entry['file']],start,end)
            if fresh != actual:
                errors.append('generated region differs from fresh regeneration')
        except (OSError,KeyError,TypeError,ValueError,subprocess.TimeoutExpired) as exc:
            errors.append(f'fresh generated region unavailable: {exc}')
        return errors, (lo,hi)
