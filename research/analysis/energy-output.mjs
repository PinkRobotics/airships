/* Shared write-or-compare boundary for the fast generated energy records. */
import fs from 'node:fs';
export function writeGenerated(path,text){
 if(!process.argv.includes('--check')){fs.writeFileSync(path,text);return;}
 const old=fs.readFileSync(path,'utf8');
 if(old===text)return;
 const a=old.split('\n'),b=text.split('\n');let n=0;
 while(n<a.length&&n<b.length&&a[n]===b[n])n++;
 throw new Error(`${path}:${n+1}: generated energy content is stale; run its generator`);
}
