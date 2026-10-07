/* Shared write-or-compare boundary for the fast generated energy records. */
import fs from 'node:fs';
/* Complete-output boundary for producers that previously had no modes. */
export function producerCheckMode(command){
 const args=process.argv.slice(2);
 if(args.length>1||args.some(arg=>arg!=='--check')){
  console.error(`Usage: ${command} [--check]`);process.exit(2);
 }
 return args[0]==='--check';
}
export function writeOutputs(outputs,check){
 if(!check){for(const [path,text] of Object.entries(outputs))fs.writeFileSync(path,text);return;}
 const bad=[];
 for(const [path,text] of Object.entries(outputs)){
  if(!fs.existsSync(path))bad.push(`${path}: missing generated output`);
  else if(!fs.readFileSync(path).equals(Buffer.from(text)))bad.push(`${path}: stale generated output`);
 }
 for(const error of bad)console.error(error);
 if(bad.length)process.exitCode=1;
}
export function jsonRows(value){
 return '{\n'+Object.entries(value).map(([key,item])=>JSON.stringify(key)+':'+
  (Array.isArray(item)?'[\n'+item.map(row=>JSON.stringify(row)).join(',\n')+'\n]':JSON.stringify(item))).join(',\n')+'\n}\n';
}
export function writeGenerated(path,text){
 if(!process.argv.includes('--check')){
  if(!fs.existsSync(path)||fs.readFileSync(path,'utf8')!==text)fs.writeFileSync(path,text);
  return;
 }
 const old=fs.readFileSync(path,'utf8');
 if(old===text)return;
 const a=old.split('\n'),b=text.split('\n');let n=0;
 while(n<a.length&&n<b.length&&a[n]===b[n])n++;
 throw new Error(`${path}:${n+1}: generated energy content is stale; run its generator`);
}
