// Preview frames without rendering the whole video.
// Usage: node video/stills.js <timeline.html> <outDir> <t1> <t2> ...   (seconds)
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const [file,outDir,...ts]=process.argv.slice(2);fs.mkdirSync(outDir,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];
p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+path.resolve(file));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
for(const t of ts.map(Number)){await p.evaluate(t=>seek(t),t);await p.screenshot({path:path.join(outDir,`t${t}.jpg`),type:'jpeg',quality:75});}
console.log(errs.join('\n')||`ok: ${ts.length} stills in ${outDir}`);await b.close();})();
