(() => {
  const rows=window.AIRSHIPS.app.missions.filter(m=>!m.idle).map(m=>({class:m.cls.id,legKm:m.legKm}));
  const distances=rows.map(r=>r.legKm).sort((a,b)=>a-b),n=distances.length;
  return {source:'monitor allocator, seed=7 and data=snapshot',rows,
    min:distances[0],median:n%2?distances[(n-1)/2]:(distances[n/2-1]+distances[n/2])/2,max:distances[n-1]};
})()
