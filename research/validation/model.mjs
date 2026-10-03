// Argument plumbing only. Import the same stamped dependencies the model imports,
// so setConfig changes the actual singleton used by planCycle and diskMW.
import { readFileSync } from 'node:fs';

const root = new URL('../../', import.meta.url);
async function dependency(parent, file) {
  const text = readFileSync(parent, 'utf8');
  const spec = [...text.matchAll(/from\s+['"]([^'"]+)['"]/g)]
    .map(m => m[1]).find(s => s.split('?')[0] === `./${file}`);
  if (!spec) throw new Error(`missing model dependency ${file}`);
  const url = new URL(spec, parent);
  return { url, module: await import(url.href) };
}
const planURL = new URL('sim/plan.js', root);
const plan = await import(planURL.href);
const physics = await dependency(planURL, 'physics.js');
const atmosphere = await dependency(physics.url, 'atmosphere.js');
const config = await dependency(physics.url, 'config.js');
const planConfig = await dependency(planURL, 'config.js');
if (planConfig.module.CFG !== config.module.CFG) throw new Error('split model config singleton');
const { CFG, CLASSES, MODES, resetConfig, setConfig } = config.module;
const args = JSON.parse(readFileSync(0, 'utf8'));
resetConfig();
const isa = args.heights.map(h => ({
  temperature_K: atmosphere.module.isaTemperatureK(h),
  pressure_Pa: atmosphere.module.isaPressurePa(h),
  density_kg_m3: atmosphere.module.airDensity(h),
}));
const hindenburg = physics.module.grossLiftKg(args.hindenburg_m3,
  { pressurePa: args.standard_pressure_Pa, temperatureK: args.standard_temperature_K }, 'hydrogen', 1);
const cls = { ...CLASSES.P100, payloadT: args.tank_m3,
  cruiseKph: args.cruise_kph, fillM3s: args.tank_m3 / args.scoop_seconds };
const mode = { ...MODES.balanced };
const cycles = args.distances_km.map(km => {
  const p = plan.planCycle(cls, mode, km, null);
  return { duration_minutes: p.dur, cycle_minutes: p.cycleMin,
    // Kinematic lower bound, not planCycle's airship phase times. Only its public
    // ground speeds and fill replay map to the aircraft. No ramp or hose-time floor.
    mapped_minutes: km / p.gsOut * 60 + p.dur.WATER_FILL + km / p.gsRet * 60,
    delivered_t: p.deliveredT, retained_t: p.retainedT,
    ground_speed_out_kph: p.gsOut, ground_speed_return_kph: p.gsRet };
});
setConfig({ rhoAir: args.rotor_density });
const rotorConfig = { ...CFG };
const rotor = physics.module.diskMW({ diskM2: args.disk_m2 }, args.thrust_N, args.rotor_density);
const hoverPressure = atmosphere.module.isaPressurePa(args.hover.pressure_altitude_m);
const hoverDensity = hoverPressure / (atmosphere.module.ISA.R * args.hover.temperature_K);
setConfig({ rhoAir: hoverDensity });
const hover = {
  pressure_Pa: hoverPressure, density_kg_m3: hoverDensity,
  density_altitude_m: atmosphere.module.altitudeForDensity(hoverDensity),
  power_MW: physics.module.diskMW({ diskM2: args.hover.disk_m2 }, args.hover.thrust_N, hoverDensity),
  config: { ...CFG },
};
resetConfig();
process.stdout.write(JSON.stringify({ isa, hindenburg, cycles, cycle_inputs: { cls, mode,
  config: { ...CFG }, wind: null }, rotor_MW: rotor, rotor_config: rotorConfig, hover }));
