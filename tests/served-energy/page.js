(async()=>{
 for(let i=0;i<600&&!window.AIRSHIPS;i++)await new Promise(r=>setTimeout(r,50));
 const A=window.AIRSHIPS;
 if(!A)throw new Error('simulation import unavailable');
 const S=A.app||A.concept, SIM=A.sim, rows=[];
 const wait=async predicate=>{for(let i=0;i<1000;i++){if(predicate())return;await new Promise(r=>setTimeout(r,50));}throw new Error('planning unavailable: deadline reached');};
 const add=(page,element,quantity,value,m,basis='record')=>rows.push({page,element,quantity,value,plan:{class:m.cls.id,km:m.legKm,basis,mode:m.selection.mode,model:SIM.modelIdentity(),windState:m.selection.windState,wind:m.wind??null},feasible:true,hull:m.name||'worked example'});
 if(A.app){
  await wait(()=>S.ready&&S.planning?.state==='settled');
  const original=S.sel;
  for(let i=0;i<S.missions.length;i++){
   const m=S.missions[i];
   if(m.served!==true)throw new Error('mission bypasses served plan selector');
   SIM.auditServedPlan(m.cls,m.legKm,m.wind,m.selection,m.mode.id);
   if(m.planState!=='ready'){
    if(!m.idle||!SIM.stateAt(m,0).inactive)throw new Error('stand-down is shown flying');
    window.APP.selRow(i);
    if(!document.querySelector('[data-plan-inactive]')?.textContent.includes('unavailable')&&m.planState!=='pending')throw new Error('inactive quantities lack a reason');
    continue;
   }
   if(m.idle||m.plan!==m.selection.plan)throw new Error('displayed mission differs from selected plan');
   if(m.selection.favourable.state==='ready')SIM.auditServedPlan(m.cls,m.legKm,m.wind,{...m.selection,...m.selection.favourable},m.mode.id);
   window.APP.selRow(i);
   for(const quantity of ['cycleMin','dropsPerHour','deliveredT','retainedT','eCycleMWh','kwhPerTonne','tph']){
    add(location.pathname+location.search,'cockpit / mission '+m.name,quantity,m.plan[quantity],m);
    if(m.selection.favourable.plan)add(location.pathname+location.search,'cockpit favourable / mission '+m.name,quantity,m.selection.favourable.plan[quantity],m,'favourable');
   }
   add(location.pathname+location.search,'cockpit requested water', 'requestedT',m.cls.payloadT,m);
   for(const el of document.querySelectorAll('[data-plan-hull][data-energy-quantity]')){
    const basis=el.dataset.energyBasis||'record', p=basis==='record'?m.plan:m.selection.favourable.plan;
    const expected=el.dataset.energyQuantity==='requestedT'?m.cls.payloadT:p[el.dataset.energyQuantity];
    if(+el.dataset.energyValue!==expected)throw new Error('rendered quantity differs from accepted plan');
   }
   // Every phase uses drawAt's selected vertical profile and airspeed, not another cycle.
   let start=0;
   for(const [phase] of SIM.PHASES){
    const sec=m.plan.dur[phase]*60,t=start+sec*.5-m.offset*m.cycleSec,st=SIM.stateAt(m,t),p=SIM.drawAt(m.cls,m.mode,m.plan,phase,.5);
    if(st.phase!==phase||Math.abs(st.alt-p.alt)>1e-6||Math.abs(st.gs-p.gs)>1e-6||Math.abs(st.water-p.water)>1e-6)throw new Error('animation differs from selected vertical profile');
    for(const [channel,mw] of Object.entries(p.draw))add(location.pathname+location.search,'power bars / '+phase,channel+' MW',mw,m);
    for(const [channel,mw] of Object.entries(p.gen))add(location.pathname+location.search,'generation / '+phase,channel+' MW',mw,m);
    start+=sec;
   }
  }
  for(const el of document.querySelectorAll('[data-energy-fleet-fire]')){
   const ms=S.missions.filter(m=>m.fire.id===el.dataset.energyFleetFire&&SIM.missionReady(m));
   const rate=ms.reduce((n,m)=>n+m.plan.tph,0);
   if(+el.dataset.energyValue!==rate)throw new Error('fleet rate includes an inactive or different plan');
   for(const m of ms)add(location.pathname+location.search,'fire rate '+m.fire.id,'tph contribution',m.plan.tph,m);
  }
  // An actual page fixture exercises the stand-down label and the animation guard.
  const seed=S.missions[0], fixtureSelection=SIM.selectServedPlan(SIM.CLASSES.P10000,3,null,'balanced',[]);
  if(fixtureSelection.state!=='stand-down')throw new Error('stand-down fixture unexpectedly closes');
  const fixture={...seed,name:'Stand-down fixture',cls:SIM.CLASSES.P10000,legKm:3,selection:fixtureSelection,plan:null,planState:'stand-down',planReason:fixtureSelection.reason,idle:true};
  S.missions.push(fixture);window.APP.selRow(S.missions.length-1);
  const inactive=document.querySelector('[data-plan-inactive]')?.textContent||'';
  if(!inactive.includes('stands down')||!inactive.includes('unavailable')||!SIM.stateAt(fixture,0).inactive)throw new Error('stand-down label or animation guard failed');
  S.missions.pop();
  if(original?.m)window.APP.selRow(S.missions.indexOf(original.m));
  document.getElementById('introOv')?.click();
  return {view:S.exercise?'exercise':'replay',width:innerWidth,timing:S.planningRuns[0],planningRuns:S.planningRuns,rows,missionStates:S.missions.map(m=>({hull:m.name,state:m.planState,mode:m.mode.id,km:m.legKm,kept:m.plan?.retainedT??null,delivered:m.plan?.deliveredT??null}))};
 }
 await wait(()=>S.workedSelection);
 const w=S.workedSelection,m={cls:SIM.CLASSES[w.cls],legKm:w.km,selection:w.selection,wind:null};
 SIM.auditServedPlan(m.cls,w.km,null,w.selection,w.selection.mode);
 for(const el of document.querySelectorAll('#worked [data-energy-quantity]')){
  const basis=el.dataset.energyBasis,p=basis==='record'?w.selection.plan:w.selection.favourable.plan;
  const key=el.dataset.energyQuantity,expected=key==='requestedT'?m.cls.payloadT:p[key];
  if(+el.dataset.energyValue!==expected)throw new Error('worked example figure differs from accepted plan');
  add('concept/','#worked '+key,key,expected,m,basis);
 }
 return {view:'concept',width:innerWidth,timing:{totalMs:w.ms,firstPlanMs:w.ms,slowestMissionMs:w.ms},rows,note:document.getElementById('workedNote').textContent};
})()
