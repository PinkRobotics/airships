/* Execute the pages' own pure context declarations; never execute their DOM tails. */
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
const read = file => fs.readFileSync(file,'utf8');
function declaration(file, start, end, expression) {
  const body=read(file),lo=body.indexOf(start),hi=body.indexOf(end,lo);
  if(lo<0||hi<=lo)throw new Error('missing page context boundaries: '+file);
  let code=body.slice(lo,hi).replaceAll("'../ship/","'./ship/");
  if(/document\s*\.|window\s*\./.test(code))throw new Error('DOM access in context declaration: '+file);
  code+='\nconsole.log(JSON.stringify('+expression+'));';
  const p=spawnSync(process.execPath,['--input-type=module','-e',code],{encoding:'utf8',timeout:30000});
  if(p.status!==0)throw new Error('page context failed: '+file);
  return JSON.parse(p.stdout);
}
const contexts={};
if(fs.existsSync('ship/index.html')) {
  const body=read('ship/index.html');
  if(!body.includes('fillNumbers({ ...api.ctx, ship: SHIP, band: BAND, grid: GRID, w: WALL })'))throw new Error('ship binder context changed');
  const {computeCtx}=await import('../ship/explorer.js');
  const {SHIP,BAND,GRID,WALL}=await import('../ship/catalog.js');
  contexts['ship/index.html']={...computeCtx(),ship:SHIP,band:BAND,grid:GRID,w:WALL};
}
if(fs.existsSync('engineering/engineering.js'))contexts['engineering/index.html']=declaration('engineering/engineering.js','import {','/* ---- the binder:','VALUES');
if(fs.existsSync('cell/levels.js'))contexts['cell/levels.html']=declaration('cell/levels.js','import {','function bindNumbers()','CTX');
if(fs.existsSync('cell/ship.html'))contexts['cell/ship.html']=declaration('cell/ship.html','import { ship0Summary','// THE VERDICT WORDS','ctx');
console.log(JSON.stringify(contexts));
