/* Alter module responses in owned scratch; never edit the model during a proof. */
import {mkdtempSync,writeFileSync,rmSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
export function proveMutations(script,mutations) {
 if(!process.env.TMPDIR)throw new Error('TMPDIR must name test scratch');
 const dir=mkdtempSync(join(process.env.TMPDIR,'energy-diagnostic-'));
 try{
  const loader=join(dir,'loader.mjs');
  writeFileSync(loader,`export async function load(url,context,next){
   const result=await next(url,context),change=JSON.parse(process.env.DIAGNOSTIC_CHANGE);
   if(!change||!new URL(url).pathname.endsWith(change.file))return result;
   const source=String(result.source);
   if(source.split(change.old).length!==2)throw new Error('Mutation needs exactly one target');
   return {...result,source:source.replace(change.old,change.replacement)};
  }`);
  for(const change of [null,...mutations,null]){
   const child=spawnSync(process.execPath,['--no-warnings','--experimental-loader',loader,script],
    {cwd:resolve('.'),env:{...process.env,DIAGNOSTIC_PROBE:'1',DIAGNOSTIC_CHANGE:JSON.stringify(change)},encoding:'utf8'});
   const expected=change?1:0;
   console.log(`${change?'RED '+change.label:'GREEN restored fixtures'}: exit ${child.status}`);
   if(child.stdout)process.stdout.write(child.stdout);
   if(change){
    const diagnostic=child.stderr.split('\n').filter(l=>l.includes('AssertionError')||l.includes(change.assertion)).join('\n');
    console.log(diagnostic);
    if(!child.stderr.includes(change.assertion))throw new Error('Mutation did not reach its intended assertion: '+change.label);
   }
   if(child.status!==expected)throw new Error('Unexpected mutation outcome: '+(change?.label??'restored')+'\n'+child.stderr);
  }
 }finally{rmSync(dir,{recursive:true,force:true});}
}
