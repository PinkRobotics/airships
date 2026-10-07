(async()=>{
 for(let i=0;i<600&&!window.AIRSHIPS;i++)await new Promise(r=>setTimeout(r,50));
 const A=window.AIRSHIPS;
 if(!A)throw new Error('simulation import unavailable');
 const S=A.app||A.concept, SIM=A.sim, rows=[];
 const wait=async predicate=>{for(let i=0;i<1000;i++){if(predicate())return;await new Promise(r=>setTimeout(r,50));}throw new Error('planning unavailable: deadline reached');};
 const add=(page,element,quantity,value,m,basis='record')=>rows.push({page,element,quantity,value,plan:{class:m.cls.id,km:m.legKm,basis,mode:m.selection.mode,model:SIM.modelIdentity(),windState:m.selection.windState,wind:m.wind??null},feasible:true,hull:m.name||'worked example'});
 if(A.app){
  await wait(()=>S.ready&&S.planning?.state==='settled');
  const original=S.sel; S.paused=true;
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
   const label=document.querySelector('[data-planned-mode]');
   if(label?.dataset.plannedMode!==m.selection.mode||label.textContent!==`Planned ${m.mode.label.toLowerCase()} mode`)throw new Error('mode label differs from planned mode');
   const routeNote=document.querySelector('#cpOps [data-plan-wind]');
   if(!routeNote||routeNote.closest('details')||(!m.plan.windUsed&&!routeNote.textContent.includes('wind not measured; still-air plan.')))throw new Error('operation wind qualification is hidden or differs from the plan');
   if(!document.getElementById('cpOps').textContent.includes('Battery hours are reported; they do not determine feasibility.'))throw new Error('operation panel does not define the feasibility scope');
   const current=SIM.stateAt(m,S.simTime);
   const cycleText=document.getElementById('opsCycle').textContent;
   if(!cycleText.includes(SIM.fmtMin(m.plan.cycleMin)+' per cycle'))throw new Error('displayed cycle duration differs from accepted plan');
   for(const [basis,p] of [['record',m.plan],['favourable',m.selection.favourable.plan]]){
    if(p&&!cycleText.includes(p.eCycleMWh.toFixed(1)+' MWh energy supplied · '+basis+':'))throw new Error('displayed cycle energy differs from accepted plan: '+basis);
    if(!p&&!cycleText.includes(basis+' cycle energy unavailable:'))throw new Error('infeasible paired cycle supplies a displayed energy');
   }
   const planText=document.getElementById('opsN3').textContent;
   for(const fragment of [SIM.fmtT(m.plan.deliveredT)+' delivered per drop',SIM.fmtMin(m.plan.cycleMin)+' per cycle',SIM.fmt(m.plan.tph)+' t/h',m.plan.kwhPerTonne.toFixed(0)+' kWh per delivered tonne']){
    if(!planText.includes(fragment))throw new Error('displayed narrative differs from accepted plan: '+fragment);
   }
   const channels={pwSol:current.gen.solar||0,pwRgn:current.gen.regen||0,pwPrp:(current.draw.prop||0)+(current.draw.rotors||0),pwPmp:(current.draw.pumps||0)+(current.draw.winch||0),pwCry:current.draw.cryo||0,pwHot:current.draw.hotel||0};
   for(const [id,mw] of Object.entries(channels)){
    const displayed=document.getElementById(id+'v')?.textContent;
    if(displayed!==SIM.fmt(mw,mw<10?1:0)+' MW')throw new Error('displayed power differs from accepted plan state: '+id+' '+displayed);
    add(location.pathname+location.search,'current power / '+id,'MW',mw,m);
   }
   const net=channels.pwSol+channels.pwRgn-channels.pwPrp-channels.pwPmp-channels.pwCry-channels.pwHot;
   if(!current.stopped&&document.querySelector('#pwNet b').textContent!==(net<0?'−':'+')+SIM.fmt(Math.abs(net),1)+' MW')throw new Error('displayed net power differs from accepted plan state');
   if(!current.stopped)add(location.pathname+location.search,'#pwNet','net MW',net,m);
   const pair=m.selection.favourable.plan;
   if(pair){
    const other=SIM.drawAt(m.cls,m.mode,pair,current.phase,current.prog);
    const otherNet=Object.values(other.gen).reduce((n,v)=>n+v,0)-Object.values(other.draw).reduce((n,v)=>n+v,0);
    if(!document.getElementById('pwNet').textContent.includes('favourable: '+SIM.fmt(otherNet,1)+' MW net;'))throw new Error('displayed favourable net power differs from exact paired plan');
    add(location.pathname+location.search,'#pwNet favourable','net MW',otherNet,m,'favourable');
   }
   const storage=m.battE===undefined?m.cls.battMWh:m.battE;
   const storageGauge=document.querySelector('#sysDials [aria-label="storage"]');
   const storageText=SIM.fmt(storage,storage<10?1:0)+' MWh';
   if(+storageGauge?.getAttribute('aria-valuenow')!==Math.round(storage*1000)/1000||storageGauge?.getAttribute('aria-valuetext')!==storageText||!storageGauge.textContent.includes(storageText))throw new Error('displayed storage differs from the accepted mission energy ledger');
   add(location.pathname+location.search,'storage gauge','stored MWh',storage,m);
   rows[rows.length-1].source='configured initial storage or app/loop.js integration of accepted instantaneous power; no endurance inferred';
   const waterGauge=document.querySelector('#sysDials [aria-label="water aboard"]');
   if(+waterGauge?.getAttribute('aria-valuenow')!==Math.round(current.water*1000)/1000||waterGauge?.getAttribute('aria-valuetext')!==SIM.fmtT(current.water))throw new Error('displayed water aboard differs from the accepted profile');
   add(location.pathname+location.search,'water aboard gauge','water aboard t',current.water,m);
   const forceWater=document.getElementById('fvP');
   const forceWaterText=SIM.fmt(current.water)+' t '+(current.water/Math.max(1,m.cls.payloadT)*100).toFixed(0)+'% of water requested '+SIM.fmt(m.cls.payloadT)+' t';
   if(forceWater.previousElementSibling.textContent!=='water aboard'||forceWater.textContent!==forceWaterText)throw new Error('water-aboard instrument confuses instantaneous load with delivery');
   add(location.pathname+location.search,'#fvP water aboard','water aboard t',current.water,m);
   for(const quantity of ['cycleMin','dropsPerHour','deliveredT','retainedT','eCycleMWh','kwhPerTonne','tph']){
    add(location.pathname+location.search,'cockpit / mission '+m.name,quantity,m.plan[quantity],m);
    if(m.selection.favourable.plan)add(location.pathname+location.search,'cockpit favourable / mission '+m.name,quantity,m.selection.favourable.plan[quantity],m,'favourable');
   }
   add(location.pathname+location.search,'cockpit requested water', 'requestedT',m.cls.payloadT,m);
   for(const el of document.querySelectorAll('[data-plan-hull][data-energy-quantity]')){
    const basis=el.dataset.energyBasis||'record', p=basis==='record'?m.plan:m.selection.favourable.plan;
    const expected=el.dataset.energyQuantity==='requestedT'?m.cls.payloadT:p[el.dataset.energyQuantity];
    if(+el.dataset.energyValue!==expected)throw new Error('rendered quantity differs from accepted plan');
    const expectedText=el.dataset.energyQuantity==='tph'?SIM.fmt(expected):SIM.fmtT(expected);
    if(el.textContent!==expectedText)throw new Error('displayed quantity differs from accepted plan');
   }
   // Every phase uses drawAt's selected vertical profile and airspeed, not another cycle.
   let start=0;
   for(const [phase] of SIM.PHASES){
    const sec=m.plan.dur[phase]*60,t=start+sec*.5-m.offset*m.cycleSec,st=SIM.stateAt(m,t),p=SIM.drawAt(m.cls,m.mode,m.plan,phase,.5);
    if(st.phase!==phase||Math.abs(st.alt-p.alt)>1e-6||Math.abs(st.gs-p.gs)>1e-6||Math.abs(st.airV-p.airV)>1e-6||Math.abs(st.vz-p.vz)>1e-6||Math.abs(st.water-p.water)>1e-6)throw new Error('animation differs from selected vertical profile');
    for(const [channel,mw] of Object.entries(p.draw))add(location.pathname+location.search,'power bars / '+phase,channel+' MW',mw,m);
    for(const [channel,mw] of Object.entries(p.gen))add(location.pathname+location.search,'generation / '+phase,channel+' MW',mw,m);
    start+=sec;
   }
  }
  for(const el of document.querySelectorAll('[data-energy-fleet-fire]')){
   const ms=S.missions.filter(m=>m.fire.id===el.dataset.energyFleetFire&&SIM.missionReady(m));
   const rate=ms.reduce((n,m)=>n+m.plan.tph,0);
   if(+el.dataset.energyValue!==rate)throw new Error('fleet rate includes an inactive or different plan');
   if(el.textContent!==SIM.fmt(rate)+' kL/h sim')throw new Error('displayed fleet rate differs from accepted contributors');
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
  // Use the model's bounded candidate set under measured wind, rather than
  // only proving the rendering of an artificially empty candidate list.
  const closingWind={spd:40,dir:270,bearing:90};
  const closingWindSelection=SIM.selectServedPlan(SIM.CLASSES.P100,15,closingWind,'rapid');
  if(closingWindSelection.state!=='ready')throw new Error('40 km/h reserved wind fixture does not close');
  SIM.auditServedPlan(SIM.CLASSES.P100,15,closingWind,closingWindSelection);
  const wind={spd:80,dir:270,bearing:90};
  const windySelection=SIM.selectServedPlan(SIM.CLASSES.P100,15,wind,'rapid');
  if(windySelection.state!=='stand-down')throw new Error('measured-wind stand-down fixture unexpectedly closes');
  const windyFire={...seed.fire,id:'wind-stand-down-fixture',sizeHa:1e9};
  const windy={...seed,name:'Wind stand-down fixture',cls:SIM.CLASSES.P100,mode:SIM.MODES.rapid,legKm:15,wind,fire:windyFire,
   selection:windySelection,plan:null,planState:windySelection.state,planReason:windySelection.reason,idle:true,served:true};
  windyFire.mission=windy;
  S.missions.push(windy);S.fires.push(windyFire);
  const tables=await import('./app/cockpit/tables.js?v='+SIM.modelIdentity().importStamp);
  try{
   const st=SIM.stateAt(windy,0),trace=SIM.narrate(windy,st),view=SIM.workedFigures(windy.cls,15,windySelection);
   if(st.phase!=='STAND_DOWN'||st.label!=='stands down'||!st.inactive||st.water!==0||st.ln2!==0)throw new Error('state.js: stand-down label, activity or loads differ');
   if(!trace.now.includes('unavailable')||!trace.next.includes('stands down')||!trace.plan.includes('No aircraft has flown'))throw new Error('narrate.js: stand-down trace supplies a cycle');
   if(view.rows.length||!view.status.includes('stands down')||!view.status.includes('unavailable'))throw new Error('served-view.js: stand-down supplies quantities');
   window.APP.selRow(S.missions.length-1);
   if(!document.querySelector('[data-plan-inactive]')?.textContent.includes('stands down')||document.querySelector('#cpOps [data-energy-quantity]'))throw new Error('operation panel: stand-down supplies quantities');
   tables.renderRoster();tables.renderFires();tables.updateRoster();tables.updateFires();
   const roster=document.querySelector(`#roster [data-mi="${S.missions.length-1}"] .ph`);
   const fire=document.querySelector('#firesTop [data-fid="wind-stand-down-fixture"]');
   if(roster?.textContent!=='stands down')throw new Error('tables.js: roster lost stand-down label after update');
   if(!fire?.textContent.includes('stands down')||fire.querySelector('[data-energy-fleet-fire]'))throw new Error('tables.js: stand-down contributes a fleet rate');
  }finally{
   S.missions.pop();S.fires.pop();tables.renderRoster();tables.renderFires();
  }
  // Stipulated along-track boundary wind: kinematic refusal must survive every UI path.
  const impossibleWind={spd:180,dir:270,bearing:90};
  const trackSelection=SIM.selectServedPlan(SIM.CLASSES.P100,4.71,impossibleWind,'balanced');
  if(trackSelection.state!=='stand-down'||!trackSelection.reason.includes('return leg has no positive ground speed'))
   throw new Error('track refusal missing from selector');
  const trackFire={...seed.fire,id:'track-refusal-fixture',sizeHa:1e9};
  const trackMission={...seed,name:'Track refusal fixture',cls:SIM.CLASSES.P100,legKm:4.71,wind:impossibleWind,
   fire:trackFire,selection:trackSelection,plan:null,planState:trackSelection.state,planReason:trackSelection.reason,idle:true,served:true};
  trackFire.mission=trackMission;S.missions.push(trackMission);S.fires.push(trackFire);
  try{
   window.APP.selRow(S.missions.length-1);
   if(!document.querySelector('[data-plan-inactive]')?.textContent.includes('return leg has no positive ground speed')||
      document.querySelector('#cpOps [data-energy-quantity]'))throw new Error('cockpit lost track refusal or publishes a rate');
   tables.renderRoster();tables.renderFires();
   const row=document.querySelector('#firesTop [data-fid="track-refusal-fixture"]');
   if(!row?.textContent.includes('return leg has no positive ground speed')||row.querySelector('[data-energy-fleet-fire]'))
    throw new Error('fleet totals lost track refusal or count refused rate');
  }finally{S.missions.pop();S.fires.pop();tables.renderRoster();tables.renderFires();}
  // Saved forecast magnitude on a representative perpendicular route; no service request.
  const forecast=(await (await fetch('tests/firstparty/fixtures/wind-response.json')).json())[0];
  const forecastDir=forecast.hourly.wind_direction_850hPa[0];
  const crossWind={spd:forecast.hourly.wind_speed_850hPa[0],dir:forecastDir,bearing:(forecastDir+90)%360};
  const crossSelection=SIM.selectServedPlan(SIM.CLASSES.P100,4.71,crossWind,'balanced');
  if(crossSelection.state!=='ready')throw new Error('crosswind rate fixture unavailable');
  const crossMission={...seed,name:'Triangle rate fixture',cls:SIM.CLASSES.P100,mode:SIM.MODES[crossSelection.mode],
   legKm:4.71,wind:crossWind,selection:crossSelection,plan:crossSelection.plan,planState:'ready',idle:false,served:true};
  S.missions.push(crossMission);
  try{
   window.APP.selRow(S.missions.length-1);
   const words=document.querySelector('#opsCycle')?.textContent||'';
   for(const basis of ['pressure-level wind vector per route','straight level legs','no shear, turns, gusts or vertical air motion'])
    if(!words.includes(basis))throw new Error('windy rate lacks its basis: '+basis);
  }finally{S.missions.pop();}
  // A fresh capture replaces mission objects. A retired selection must not publish
  // its old numbers while the replacement mission is being planned at new inputs.
  const savedMissions=S.missions;
  window.APP.selRow(0);
  S.missions=savedMissions.map((m,i)=>({...m,wind:i===0?{spd:15,dir:120,bearing:65,capture:'replanning fixture'}:m.wind}));
  const fleet=await import('./app/fleet.js?v='+SIM.modelIdentity().importStamp);
  const computing=fleet.planFleet();
  const pending=document.querySelector('[data-plan-inactive]')?.textContent||'';
  const pendingCorrect=S.missions.includes(S.sel?.m)&&pending.includes('pending')&&!document.querySelector('#cpOps [data-energy-quantity]');
  await computing;
  S.missions=savedMissions;
  await fleet.planFleet();
  for(const el of document.querySelectorAll('[data-energy-fleet-fire]')){
   const rate=S.missions.filter(m=>m.fire.id===el.dataset.energyFleetFire&&SIM.missionReady(m)).reduce((n,m)=>n+m.plan.tph,0);
   if(+el.dataset.energyValue!==rate||el.textContent!==SIM.fmt(rate)+' kL/h sim')throw new Error('restored fleet figures differ from accepted missions');
  }
  if(!pendingCorrect)throw new Error('retired mission selection still publishes quantities during replanning');
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
  const viewRow=SIM.workedFigures(m.cls,w.km,w.selection).rows.find(row=>row.quantity===key&&row.basis===basis);
  if(el.querySelector('b').textContent!==viewRow.text||el.querySelector('span').textContent!==viewRow.label)throw new Error('worked displayed number or label differs from accepted plan');
  add('concept/','#worked '+key,key,expected,m,basis);
 }
 if(!document.getElementById('workedNote').textContent.includes('planned '+SIM.MODES[w.selection.mode].label.toLowerCase()+' mode'))throw new Error('worked mode label differs from selected plan');
 return {view:'concept',width:innerWidth,timing:{totalMs:w.ms,firstPlanMs:w.ms,slowestMissionMs:w.ms},rows,note:document.getElementById('workedNote').textContent};
})()
