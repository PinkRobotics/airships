// Text contract for the opening comparison; no conventional performance is simulated.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
test('both opening comparisons name scoopers and bound the proposal', () => {
  for (const name of ['01-brief','02-paper']) {
    const text = fs.readFileSync(`research/reports/${name}.md`, 'utf8');
    const opening = text.split('Buoyant flight')[0];
    assert.match(opening, /helicopter/i);
    assert.match(opening, /airtanker/i);
    assert.match(opening, /scoop/i);
    assert.match(opening, /CL-415/);
    assert.match(opening, /propos|under study/i);
    assert.doesNotMatch(opening.replace(/\s+/g,' '), /Nothing occupies|Nothing occupies it|dips like a helicopter/i);
  }
});
test('the briefing comparison declares its omitted conventional mission inputs', () => {
  const text = fs.readFileSync('research/reports/01-brief.md','utf8');
  assert.doesNotMatch(text, /eight sorties/i);
  assert.match(text, /Comparison boundary/);
  for (const item of ['scooping','source-to-target','fuel','support','tactical objective']) assert.ok(text.includes(item),item);
});
