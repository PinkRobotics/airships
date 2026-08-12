/* CFG: the one mutable object in the model.
 *
 * Everything else is a pure function of its arguments plus this. That makes CFG the only
 * place where a test can leak into the next one, so these tests are also the specification
 * for how the rest of the suite is allowed to touch it: patch, assert, resetConfig in a
 * finally.
 */
import { close, deepEq, describe, eq, it, ok, throws } from '../harness.js';
import {
  CFG, CLASSES, DEFAULTS, MODES,
  planCycle, resetConfig, setConfig,
} from '../../sim/index.js?v=0286418c';

const KEYS = Object.keys(DEFAULTS);

describe('config · the defaults', () => {
  it('every default is a finite number', () => {
    ok(KEYS.length > 0, 'DEFAULTS is empty');
    for (const k of KEYS) ok(typeof DEFAULTS[k] === 'number' && isFinite(DEFAULTS[k]), `${k} = ${DEFAULTS[k]}`);
  });

  it('CFG starts as a copy of DEFAULTS, not a reference to it', () => {
    resetConfig();
    deepEq(Object.assign({}, CFG), Object.assign({}, DEFAULTS), 'CFG vs DEFAULTS');
    ok(CFG !== DEFAULTS, 'CFG and DEFAULTS are the same object; a patch would rewrite the defaults');
    try {
      setConfig({ speedMul: 3 });
      eq(DEFAULTS.speedMul, 1.0, 'patching CFG changed DEFAULTS');
    } finally { resetConfig(); }
  });
});

describe('config · setConfig', () => {
  it('rejects an unknown key rather than accepting a typo', () => {
    resetConfig();
    try {
      throws(() => setConfig({ propEtta: 0.9 }), 'a misspelled key was accepted');
      throws(() => setConfig({ rhoAIR: 1.2 }), 'a miscased key was accepted');
      throws(() => setConfig({ '': 1 }), 'an empty key was accepted');
      eq(CFG.propEta, DEFAULTS.propEta, 'a rejected patch still changed propEta');
      ok(!('propEtta' in CFG), 'the unknown key was written anyway');
    } finally { resetConfig(); }
  });

  it('names the offending key in the error', () => {
    resetConfig();
    let msg = '';
    try { setConfig({ notAKey: 1 }); } catch (e) { msg = String(e.message || e); }
    ok(msg.includes('notAKey'), `the error did not name the key: ${JSON.stringify(msg)}`);
  });

  it('writes every key it is given', () => {
    resetConfig();
    try {
      const patch = {};
      KEYS.forEach((k, i) => { patch[k] = 100 + i; });
      setConfig(patch);
      for (const k of KEYS) eq(CFG[k], patch[k], `${k} was not written`);
    } finally { resetConfig(); }
  });

  it('an empty patch is a no-op', () => {
    resetConfig();
    setConfig({});
    deepEq(Object.assign({}, CFG), Object.assign({}, DEFAULTS), 'CFG after an empty patch');
  });

  it('is NOT atomic: keys before the bad one are already written', () => {
    // Documented, not endorsed. A patch that throws has still moved the model, so any code
    // that catches a setConfig error must resetConfig rather than assume nothing happened.
    resetConfig();
    try {
      throws(() => setConfig({ speedMul: 2, nope: 1, fillMul: 5 }), 'the bad key was accepted');
      eq(CFG.speedMul, 2, 'the key before the bad one was rolled back');
      eq(CFG.fillMul, DEFAULTS.fillMul, 'a key after the bad one was applied');
    } finally { resetConfig(); }
  });

  it('the same object stays live: holders of CFG see the change', () => {
    resetConfig();
    const held = CFG;
    try {
      setConfig({ Cd: 0.09 });
      eq(held.Cd, 0.09, 'CFG was reassigned instead of mutated');
    } finally { resetConfig(); }
    eq(held, CFG, 'resetConfig reassigned CFG');
  });
});

describe('config · resetConfig', () => {
  it('restores every documented default', () => {
    for (const k of KEYS) {
      resetConfig();
      setConfig({ [k]: DEFAULTS[k] + 7.5 });
      resetConfig();
      eq(CFG[k], DEFAULTS[k], `${k} was not restored`);
    }
  });

  it('restores all of them at once', () => {
    const patch = {};
    KEYS.forEach((k, i) => { patch[k] = -1 - i; });
    setConfig(patch);
    resetConfig();
    deepEq(Object.assign({}, CFG), Object.assign({}, DEFAULTS), 'CFG after resetConfig');
  });

  it('does not remove keys a caller added by hand', () => {
    // resetConfig is Object.assign, not a replacement: it puts the documented keys back and
    // leaves anything else alone. Worth knowing before relying on it to clean up.
    resetConfig();
    CFG.__scribble = 1;
    resetConfig();
    eq(CFG.__scribble, 1, 'resetConfig deleted an undocumented key');
    delete CFG.__scribble;
  });

  it('puts the published figures back', () => {
    resetConfig();
    const before = planCycle(CLASSES.P1000, MODES.balanced, 15);
    setConfig({ speedMul: 0.4, fillMul: 3, cryoMul: 0.1, propEta: 0.4, Cd: 0.2 });
    resetConfig();
    const after = planCycle(CLASSES.P1000, MODES.balanced, 15);
    close(after.cycleMin, before.cycleMin, 1e-12, 'cycleMin');
    close(after.eCycleMWh, before.eCycleMWh, 1e-12, 'eCycleMWh');
    close(after.tph, before.tph, 1e-12, 'tph');
  });
});
