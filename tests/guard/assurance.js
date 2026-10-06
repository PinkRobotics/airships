/* Runtime-assurance regression fixtures are invented. No agency requests. */
(async () => {
  const stamp = new URL(document.querySelector('script[src*="app/main.js"]').src).search;
  const sim = await import('/sim/index.js' + stamp);
  const {S} = await import('/app/store.js' + stamp);
  const feeds = await import('/app/feeds.js' + stamp);
  const fleet = await import('/app/fleet.js' + stamp);
  for (let i=0;i<1800 && (!S.ready || (!S.recordOnly && S.planning?.state!=='settled'));i++)
    await new Promise(r=>setTimeout(r,100));
  if (!S.ready) throw Error('page did not become ready');
  S.paused = true;
  const plain = () => ({defaultKeepOutKm:25,noFleet:[],fires:[],places:[]});
  const rect=(x,y,dx,dy)=>[[x-dx,y-dy],[x+dx,y-dy],[x+dx,y+dy],[x-dx,y+dy],[x-dx,y-dy]];
  if (PART === 'C-page') return {ok:S.guard.ok,reason:S.guard.reason,recordOnly:S.recordOnly,
    missions:S.missions.length,ready:S.missions.filter(m=>!m.idle).length,
    words:document.body.innerText,standDown:S.standDown};
  if (PART === 'A' || PART === 'B') {
    const detailed=[];
    for(let i=0;i<=240;i++) detailed.push([-124+i/240,50]);
    for(let i=1;i<=240;i++) detailed.push([-123,50+i/240]);
    detailed.push(detailed[0]);
    const rings = PART==='A' ? [rect(-124,50,.3,.3),rect(-123,50,.02,.02)] : [detailed];
    const geometry=PART==='A' ? {type:'MultiPolygon',coordinates:rings.map(r=>[r])} : {type:'Polygon',coordinates:rings};
    const point=PART==='A' ? [-123,50] : [-123.57,50.57];
    // Independent reference: use every supplied part and every last-to-first edge.
    // Local tangent-plane point-to-segment distance; deliberately no guard/normalizer calls.
    const reference = pt => rings.some(r=>{
      let inside=false, distance=Infinity;
      const kx=111.32*Math.cos(pt[1]*Math.PI/180),ky=110.57;
      for(let i=0,j=r.length-1;i<r.length;j=i++) {
        const a=r[j],b=r[i];
        if((a[1]>pt[1])!==(b[1]>pt[1]) && pt[0]<(b[0]-a[0])*(pt[1]-a[1])/(b[1]-a[1])+a[0]) inside=!inside;
        const ax=(a[0]-pt[0])*kx,ay=(a[1]-pt[1])*ky,bx=(b[0]-pt[0])*kx,by=(b[1]-pt[1])*ky;
        const dx=bx-ax,dy=by-ay,t=Math.max(0,Math.min(1,-(ax*dx+ay*dy)/(dx*dx+dy*dy||1)));
        distance=Math.min(distance,Math.hypot(ax+t*dx,ay+t*dy));
      }
      return inside || distance<=25;
    });
    const guard=plain();guard.fires=[{fire:'X10001',name:'Invented guarded fire',tier:2,basis:'order',keepOutKm:25,source:'https://example.test/source'}];
    S.guard=sim.loadGuard(guard);S.exercise=false;S.day='2030-09-01';S.daySource='day';S.recordOnly=false;S.heat=[];S.sel=null;
    const dispatch=async target=>{
      const fires={features:[{properties:{FIRE_NUMBER:'X10001',CURRENT_SIZE:1000,FIRE_STATUS:'Out of Control'},geometry:{type:'Point',coordinates:[-124,50]}},
        {properties:{FIRE_NUMBER:'X19999',CURRENT_SIZE:1000,FIRE_STATUS:'Out of Control'},geometry:{type:'Point',coordinates:target}}]};
      S.fires=feeds.applyGuard(feeds.normalize(fires,{features:[{properties:{FIRE_NUMBER:'X10001'},geometry}]}));
      S.water=[[target[0]-.003,target[1],10000,0,'Invented lake']];
      await fleet.rebuildMissions();
      let sampled=0,insideComplete=0;
      for(const m of S.missions.filter(m=>!m.idle))for(let i=0;i<60;i++) {
        sampled++;if(reference(sim.stateAt(m,m.cycleSec*i/60).ll))insideComplete++;
      }
      const normalized=S.fires[0].ring;
      return {missions:S.missions.length,ready:S.missions.filter(m=>!m.idle).length,sampled,insideComplete,
        refused:S.fires.find(f=>f.id==='X19999').heldOut,regions:S.regions.length,
        normalizedVertices:normalized.length,closed:JSON.stringify(normalized[0])===JSON.stringify(normalized.at(-1)),
        pointBlocked:!!sim.pointBlocked(S.regions,target)};
    };
    return {referenceContainsWitness:reference(point),blocked:await dispatch(point),control:await dispatch([-121.5,50])};
  }
  if (PART==='C') {
    const base=plain();base.places=[{name:'Invented place',ll:[-123,50],date:'2030-09-01',basis:'order',keepOutKm:25,source:'https://example.test/place'}];
    const bad=[];
    for(const ll of [[Infinity,50],[-Infinity,50],[NaN,50],[181,50],[-181,50],[-123,91],[-123,-91],['-123',50],[null,50]]) {
      const d=structuredClone(base);d.places[0].ll=ll;const g=sim.loadGuard(d);
      bad.push({label:String(ll),ok:g.ok,reason:g.reason,fleet:sim.dayKind(g,'2030-09-01').fleet});
    }
    const evac=ll=>({fires:[{fire:'X10001',everOrder:true,everAlert:true,firstSeen:'2030-09-01',lastSeen:'2030-09-02',orderOutlines:[[ll,[-122,50],[-123,51],ll]]}]});
    const outlines=[[181,50],[-123,91],[Infinity,50],[NaN,50]].map(ll=>sim.loadEvac(evac(ll)));
    const context=sim.loadGuard(plain(),{viewFires:[{id:'X19999',ll:[Infinity,50],ring:null}]});
    const control=sim.loadGuard(base);
    return {bad,outlines:outlines.map(g=>({ok:g.ok,reason:g.reason})),context:{ok:context.ok,reason:context.reason},
      control:{ok:control.ok,blocked:!!sim.pointBlocked(sim.keepOutsFor(control,[],{},'2030-09-01'),[-123,50])}};
  }
  if (PART==='D') {
    const fire={id:'X19999',ll:[-123,50],sizeHa:1,note:false,status:'Out of Control',ring:rect(-123,50,.02,.00001)};
    const m=sim.buildMission(fire,[[-123.10,50,1000,0,'Invented lake']],'balanced','P100',{src:{idx:0,km:7},relaxed:false});
    const direct=sim.dropSeg(m,fire.ll,false);
    let cycleOutside=0;
    if(m.segs?.length)for(let n=-5;n<=100;n++)if(sim.segAt(m,n).some(p=>!sim.insideFire(fire,p)))cycleOutside++;
    const checked={fire,heat:false,targets:[fire.ll],order:[0],segs:[[[-123.01,50.000009],[-122.99,50.000009]]]};
    const jitterBaseInside=checked.segs[0].every(p=>sim.insideFire(fire,p));
    let jitterOutside=0;
    for(let n=1;n<=200;n++)if(sim.segAt(checked,n).some(p=>!sim.insideFire(fire,p)))jitterOutside++;
    const impossible=sim.dropSeg({...m,fire:{...fire,ring:[[-123,50],[-123,50],[-123,50],[-123,50]]}},fire.ll,false);
    S.guard=sim.loadGuard(plain());S.exercise=false;S.day='2030-09-01';S.daySource='day';S.recordOnly=false;S.heat=[];S.sel=null;
    S.fires=feeds.applyGuard([fire]);S.water=[[-123.1,50,10000,0,'Invented lake']];await fleet.rebuildMissions();
    return {direct:direct===null?'refused':direct.map(p=>sim.insideFire(fire,p)),baseOutside:(m.segs||[]).filter(s=>s.some(p=>!sim.insideFire(fire,p))).length,
      cycleOutside,jitterBaseInside,jitterOutside,jitterSamples:200,impossible:impossible===null?'refused':'accepted',refusedTargets:m.refusedTargets?.length||0,
      dispatch:{ready:S.missions.filter(m=>!m.idle).length,heldOut:fire.heldOut,words:document.getElementById('firesTop').textContent}};
  }
  if (PART==='E') {
    const valid=plain();valid.noFleet=[{from:'2030-08-08',to:'2030-09-01',basis:'invented window',source:'https://example.test/window'}];
    const changed=structuredClone(valid);changed.noFleet[0].from='2030-08-32';const bad=sim.loadGuard(changed);
    const dates=['2030-02-31','2030-02-29','2100-02-29','2030-00-01','2030-13-01','2030-04-31'];
    const controls=['2032-02-29','2000-02-29','2030-02-28','0096-02-29'];
    return {validFleet:sim.dayKind(sim.loadGuard(valid),'2030-08-20').fleet,bad:{ok:bad.ok,reason:bad.reason,fleet:sim.dayKind(bad,'2030-08-20').fleet},
      invalid:dates.map(d=>({date:d,fleet:sim.dayKind(sim.loadGuard(plain()),d).fleet})),
      controls:controls.map(d=>({date:d,fleet:sim.dayKind(sim.loadGuard(plain()),d).fleet}))};
  }
  throw Error('unknown regression part '+PART);
})()
