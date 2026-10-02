/* Execute the drawing's functions offline. Scene sinks record geometry, not pixels. */
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
const imp=p=>import(pathToFileURL(path.join(root,p)).href);
const {SHIP:baseShip,GRID:baseGrid,WALL:baseWall}=await imp('ship/catalog.js');
const M=await imp('ship/model.js');
const {CLASSES}=await imp('sim/config.js');
const realG=await imp('ship/explorer-geom.js');
const geom=await imp('3d/model/geom.js');
const source=fs.readFileSync('ship/explorer.js','utf8');
const extract=name=>{const i=source.indexOf(`function ${name}(`);if(i<0)throw Error(name);return source.slice(i,source.indexOf('\n}',i)+2);};
const dist=(a,b)=>Math.hypot(...a.slice(0,3).map((v,i)=>v-b[i]));
function splitLength(a,b,half) {
  const ts=[0,1];if(a[0]!==b[0])for(const x of [-half,half]){const t=(x-a[0])/(b[0]-a[0]);if(t>0&&t<1)ts.push(t);}
  ts.sort((a,b)=>a-b);const out={barrel:0,cap:0};for(let i=1;i<ts.length;i++){const mid=(ts[i]+ts[i-1])/2;out[Math.abs(a[0]+(b[0]-a[0])*mid)<=half+1e-9?'barrel':'cap']+=dist(a,b)*(ts[i]-ts[i-1]);}return out;
}
function segmentStats(ss,D,ring=false){const out={count:ss.length,lengthM:0,barrelM:0,capM:0,barrelCount:0,capCount:0,transitionCount:0};
 for(const x of ss){const a=x.a||x[0],b=x.b||x[1];const parts=splitLength(a,b,D.cylL/2);out.lengthM+=dist(a,b);out.barrelM+=parts.barrel;out.capM+=parts.cap;out[parts.barrel<1e-9?'capCount':parts.cap<1e-9?'barrelCount':'transitionCount']++;}
 if(ring){
   out.rings=new Set(ss.map(x=>x.s)).size;
   out.arcM=0;out.barrelArcM=0;out.capArcM=0;
   for(const {a,b} of ss){
     const radius=Math.hypot(a[1],a[2]);
     if(Math.abs(radius-Math.hypot(b[1],b[2]))>1e-8)throw Error('ring endpoints have different radii');
     const angle=Math.atan2(Math.abs(a[1]*b[2]-a[2]*b[1]),a[1]*b[1]+a[2]*b[2]);
     const length=radius*angle;
     out.arcM+=length;out[Math.abs(a[0])<=D.cylL/2+1e-9?'barrelArcM':'capArcM']+=length;
   }
 }
 return out;
}
// Measure smooth meridians between the actual drawing endpoints. No sampled interval is omitted.
function meridianStats(segments,D,offset=0){
 const radius=D.R-offset,half=D.cylL/2;
 const position=p=>p[0]<-half ? -half-radius*Math.atan2(-half-p[0],Math.hypot(p[1],p[2])) :
   p[0]>half ? half+radius*Math.atan2(p[0]-half,Math.hypot(p[1],p[2])) : p[0];
 const out={arcM:0,barrelArcM:0,capArcM:0,members:0};let previous=null;
 for(const {a,b} of segments){
   if(!previous||dist(previous,a)>1e-8)out.members++;
   const start=Math.min(position(a),position(b)),end=Math.max(position(a),position(b));
   const barrel=Math.max(0,Math.min(end,half)-Math.max(start,-half));
   out.arcM+=end-start;out.barrelArcM+=barrel;out.capArcM+=end-start-barrel;previous=b;
 }
 return out;
}
function meshStats(g,D){const pos=g.pos,idx=g.idx;const out={vertices:pos.length/3,triangles:idx.length/3,areaM2:0,barrelM2:0,capM2:0,volumeM3:0};for(let i=0;i<idx.length;i+=3){const ps=[0,1,2].map(j=>Array.from(pos.slice(idx[i+j]*3,idx[i+j]*3+3)));const [a,b,c]=ps;const u=b.map((x,j)=>x-a[j]),v=c.map((x,j)=>x-a[j]);const cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];const area=Math.hypot(...cross)/2;out.areaM2+=area;out[Math.abs((a[0]+b[0]+c[0])/3)<=D.cylL/2?'barrelM2':'capM2']+=area;out.volumeM3+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6;}out.volumeM3=Math.abs(out.volumeM3);return out;}
function run(dia=M.SHIP0.diaM,details=false){const g=M.shipGeom(dia);const SHIP={...baseShip,diaM:dia,lenM:g.lenM},GRID={...baseGrid,depthM:g.depthM,nLong:g.nLong},WALL={...baseWall};
 const records=[];let pending=null;
 const G={...realG,strutInstances:(pts,pairs)=>{pending=pairs.map(([i,j])=>({a:pts[i],b:pts[j]}));return {xf:new Float32Array(pairs.length*16),count:pairs.length};}};
 const node=x=>({...x,children:[]});
 const inst=(parent,spec,xf,count)=>{const x={...spec,count,xf,segments:pending};pending=null;records.push(x);return x;};
 const pipesFromSegs=(parent,id,segments,rOut)=>{const x={id,segments,rOut,count:segments.length};records.push(x);return x;};
 const lineNode=(parent,id,segments)=>{const x={id,segments,count:segments.length};records.push(x);return x;};
 const solidNode=(parent,id,mesh)=>{const x={id,mesh,count:1};records.push(x);return x;};
 let body=['shipDims','shipStation','shipSkeletonSegs','shipCellPlacements','shipWrapGeom','buildShip','buildGrid'].map(extract).join('\n');
 const vessel=extract('buildVessel');body+='\n'+vessel.slice(0,vessel.indexOf('  // THE ENVIRONMENT v2'))+'\nreturn {root};\n}';
 const names=['SHIP','GRID','WALL','G','node','inst','pipesFromSegs','lineNode','solidNode','XM','TOKENS','boxGeom','latheWithScale'];
 const vals=[SHIP,GRID,WALL,G,node,inst,pipesFromSegs,lineNode,solidNode,{}, {},geom.boxGeom,(p,n,fn)=>geom.latheGeom(p,n,fn)];
 const go=new Function(...names,body+'\nconst wrapGeomShared=shipWrapGeom; const segLines=arr=>arr.map(g=>[g.a,g.b]); return {D:shipDims(),bones:shipSkeletonSegs(shipDims()),ship:()=>buildShip(),grid:()=>buildGrid(),vessel:()=>buildVessel(),placements:()=>shipCellPlacements(shipDims()),wrap:()=>shipWrapGeom(shipDims())};');
 const api=go(...vals);const D=api.D;api.ship();
 const families=Object.fromEntries(Object.entries(api.bones).map(([k,ss])=>[k,segmentStats(ss,D,k==='hoops'||k==='hoopsInner')]));
 const shipRecords=records.splice(0);const bars=shipRecords.find(x=>x.id==='ShipBars');
 families.bars={...segmentStats(bars.segments,D),...meridianStats(bars.segments,D)};
 families.bars.meridians=families.bars.members;
 Object.assign(families.longs,meridianStats(api.bones.longs,D,GRID.depthM));
 const stations=Array.from({length:D.nBays+1},(_,i)=>{const s=D.total*i/D.nBays;const st= new Function('D','s',extract('shipStation')+'\nreturn shipStation(D,s);')(D,s);return {s,rInner:st.r-st.nr*GRID.depthM,rOuter:st.r,region:s>=D.sCap&&s<=D.sCap+D.cylL?'barrel':'cap'};});
 const result={dia,D,GRID:{depthM:GRID.depthM,nLong:GRID.nLong,bayM:GRID.bayM},families,stations,sections:shipRecords.filter(x=>x.rOut).map(x=>({id:x.id,outerDiameterM:x.rOut*2})),spokeNet:M.shipSpokeNet(g)};
 if(details){result.film=meshStats(api.wrap(),D);result.film.billAreaM2=D.area;const places=api.placements();result.placements={total:places.length,barrel:places.filter(x=>x.s>=D.sCap&&x.s<=D.sCap+D.cylL).length};api.grid();result.grid=records.splice(0).map(x=>({id:x.id,count:x.count,...(x.segments?segmentStats(x.segments,D):{})}));api.vessel();result.outfit=records.splice(0).map(x=>({id:x.id,count:x.count,...(x.segments?segmentStats(x.segments,D):{})}));}
 return result;
}
const out={record:run(M.SHIP0.diaM,true),nominal:{}};
for(const c of Object.values(CLASSES))out.nominal[c.diaM]=run(c.diaM,false);
process.stdout.write(JSON.stringify(out));
