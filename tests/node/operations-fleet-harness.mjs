// Execute the actual allocator with only browser import bindings replaced.
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '../..');
const read = file => fs.readFileSync(path.join(root,file),'utf8');
const simURL = pathToFileURL(path.join(root,'sim/index.js')).href;
export const SIM = await import(simURL);
export const S = {fires:[],water:[],missions:[],regions:[],recordOnly:false,exercise:true,
  exerciseRegions:[],guard:null,seasonOfNote:new Set(),day:null,modeId:'balanced',
  heat:[],battByHull:{},sel:null};
globalThis.__operationsState = S;
const source = read('app/feeds.js');
const start = source.indexOf('export function needsShip('), end = source.indexOf('\n}\n',start);
if(start<0 || end<0) throw new Error('needsShip boundary absent');
const moduleURL = body => 'data:text/javascript;base64,'+Buffer.from(body).toString('base64');
const feed = await import(moduleURL('const S=globalThis.__operationsState;\n'+source.slice(start,end+3)));
globalThis.__operationsNeedsShip = feed.needsShip;
const code = read('app/fleet.js').replace(/^import .*;$/gm, line => {
  if(line.includes('../sim/index.js')) return line.replace(/'\.\.\/sim\/index.js\?v=[^']+'/,JSON.stringify(simURL));
  if(line.includes('./store.js')) return 'const S=globalThis.__operationsState;';
  if(line.includes('./feeds.js')) return 'const needsShip=globalThis.__operationsNeedsShip;';
  const names=line.match(/\{([^}]+)\}/)?.[1].split(',').map(s=>s.trim());
  if(!names) throw new Error('Unexpected allocator import: '+line);
  return 'const '+names.map(n=>n+'=()=>{}').join(',')+';';
});
export const {rebuildMissions} = await import(moduleURL(code));
