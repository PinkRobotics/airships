/* A sample of flown legs must support three different printed search distances. */
export function fleetDistanceSet(rows) {
  if (!Array.isArray(rows) || rows.some(r => !Number.isFinite(r.legKm) || r.legKm <= 0))
    throw new Error('FLEET_DISTANCE_SET_INVALID: every leg must be finite and positive');
  const legs = rows.map(r => r.legKm).sort((a,b) => a-b), n = legs.length;
  if (new Set(legs.map(km => +km.toFixed(6))).size < 3)
    throw new Error('FLEET_DISTANCE_SET_DEGENERATE: fewer than three distinct legs at six decimal kilometres');
  const min = legs[0], median = n%2 ? legs[(n-1)/2] : (legs[n/2-1]+legs[n/2])/2, max = legs[n-1];
  const printed = [min,median,max].map(km => +km.toFixed(6));
  if (!(printed[0] < printed[1] && printed[1] < printed[2]))
    throw new Error('FLEET_DISTANCE_SET_DEGENERATE: minimum, median and maximum must differ at printed precision');
  return {min,median,max};
}

export function validateFleetDistanceRecord(record) {
  const stats = fleetDistanceSet(record.rows);
  if (Object.keys(stats).some(key => record[key] !== stats[key]))
    throw new Error('FLEET_DISTANCE_SET_INVALID: recorded quantiles do not match the legs');
  const c = record.capture;
  if (c?.view !== 'exercise' || c.seed !== 7 || c.day !== null || c.query !== 'seed=7&view=exercise' ||
      c.rerun !== 'python3 -B tools/gen_operations_records.py')
    throw new Error('FLEET_DISTANCE_SOURCE_UNPINNED: use the stated seed-7 exercise capture');
  return stats;
}
