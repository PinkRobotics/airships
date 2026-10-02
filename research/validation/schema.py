"""Small, dependency-free schema for the supplied source-record format."""
import json
import re

REQUIRED = {'check', 'class', 'quantity', 'value', 'unit', 'conditions', 'document',
            'locator', 'url', 'licence', 'quote', 'confidence', 'confidence_reason', 'limits'}
CHECKS = {'1-atmosphere': 10, '2-hindenburg': 5, '3-cl415-cycle': 7,
          '4-helicopter-hover': 5, '5-vacuum-shell-akhmeteli': 2,
          '5-vacuum-shell-jenett': 2, '6-helium': 5}


def public_text(text):
    forbidden = ('/' + 'home/', '/' + 'Users/', '~' + '/', 'file:' + '//')
    if any(s in text for s in forbidden):
        raise ValueError('private filesystem path is forbidden')
    if re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text):
        raise ValueError('email address is forbidden')


def printed(value):
    if isinstance(value, dict):
        if not value:
            raise ValueError('empty reference value')
        for v in value.values():
            printed(v)
    elif isinstance(value, list):
        if not value:
            raise ValueError('empty reference list')
        for v in value:
            printed(v)
    elif not isinstance(value, str) or not value.strip():
        raise ValueError('printed reference digits/text must remain strings')
    elif value.lstrip().startswith(('{', '[')):
        raise ValueError('reference value must be normalised, not a repr string')


def validate(data):
    public_text(json.dumps(data, ensure_ascii=False))
    if not isinstance(data, dict) or not {'order', 'lane', 'date', 'rule', 'records'} <= data.keys():
        raise ValueError('missing source metadata or records')
    records = data['records']
    if not isinstance(records, list) or len(records) != 36:
        raise ValueError('expected 35 original records and the primary hover record, including do not use')
    counts = dict.fromkeys(CHECKS, 0)
    for i, r in enumerate(records):
        if not isinstance(r, dict) or not REQUIRED <= r.keys():
            raise ValueError(f'record {i}: missing required fields')
        if r['check'] not in counts or r['class'] not in {'equation', 'reproduction', 'measured'}:
            raise ValueError(f'record {i}: invalid check or class')
        counts[r['check']] += 1
        if r['confidence'] not in {'high', 'medium'}:
            raise ValueError(f'record {i}: invalid confidence')
        for key in REQUIRED - {'value', 'document'}:
            if not isinstance(r[key], str) or not r[key].strip():
                raise ValueError(f'record {i}: {key} must be nonempty text')
        if len(r['quote'].split()) >= 25:
            raise ValueError(f'record {i}: quotation must be under 25 words')
        doc = r['document']
        if not isinstance(doc, dict) or not {'title', 'authors', 'year'} <= doc.keys():
            raise ValueError(f'record {i}: document must be a normalised object')
        if not all(isinstance(doc[k], str) and doc[k].strip() for k in ('title', 'authors')):
            raise ValueError(f'record {i}: document title/authors must be text')
        if type(doc['year']) is not int:
            raise ValueError(f'record {i}: document year must be an integer')
        printed(r['value'])
    if counts != CHECKS:
        raise ValueError('source coverage changed')
    excluded = records[6]
    if 'do not use' not in excluded['quantity'] or 'silently corrected' not in excluded['limits']:
        raise ValueError('the excluded gas-constant record and its reason must be retained')
