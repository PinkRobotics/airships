(async () => {
  const query = new URLSearchParams(location.search);
  if (!window.AIRSHIPS.app.exercise || query.get('view') !== 'exercise' || query.get('seed') !== '7')
    throw new Error('FLEET_DISTANCE_SOURCE_UNPINNED: expected seed=7&view=exercise');
  const {fleetDistanceSet}=await import('./research/analysis/fleet-distance-set.mjs');
  const rows=window.AIRSHIPS.app.missions.filter(m=>!m.idle).map(m=>({class:m.cls.id,legKm:m.legKm}));
  return {source:'Monitor allocator on the bundled invented exercise, seed=7&view=exercise; no captured incident day.',
    capture:{view:'exercise',seed:7,day:null,query:'seed=7&view=exercise',
      rerun:'python3 -B tools/gen_operations_records.py'},rows,...fleetDistanceSet(rows)};
})()
