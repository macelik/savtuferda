// Preview without rendering: one still per scene, taken once its entrance has finished.
// Usage: node stills.js <out_dir_of_compose> [full|short]   -> <out_dir>/stills-<cut>/NN-<type>.jpg
// Or:    node stills.js <timeline.html> <outDir> <t1> <t2> ...
const {chromium}=require('./pw.js')();const path=require('path');const fs=require('fs');
(async()=>{const a=process.argv.slice(2);let file,outDir,shots=[];
if(fs.existsSync(path.join(a[0],'timeline.json'))){const cut=a[1]||'full';file=path.join(a[0],cut+'.html');outDir=path.join(a[0],'stills-'+cut);
  JSON.parse(fs.readFileSync(path.join(a[0],'timeline.json')))[cut].forEach((s,i)=>shots.push([Math.min(s.start+4.2,s.end-0.6),`${String(i+1).padStart(2,'0')}-${s.type}`]));}
else{file=a[0];outDir=a[1];shots=a.slice(2).map(t=>[+t,'t'+t]);}
fs.mkdirSync(outDir,{recursive:true});const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];
p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+path.resolve(file));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
for(const [t,name] of shots){await p.evaluate(t=>seek(t),t);await p.screenshot({path:path.join(outDir,name+'.jpg'),type:'jpeg',quality:75});}
console.log(errs.length?'ERRORS:\n'+errs.join('\n'):`ok: ${shots.length} stills in ${outDir}`);await b.close();process.exitCode=errs.length?1:0;})();
