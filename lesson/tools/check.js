// QA for a built lesson page: node lesson/tools/check.js lesson/output/X.html [outDir]
// Reports console errors + horizontal overflow, saves screenshots of key views.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const file=path.resolve(process.argv[2]);const out=process.argv[3]||'qa';fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch();const errs=[];
const shots=[['text','#siir',1300,'light',null],['word1','#kelime-1',1300,'light',null],['root-dark','#kelime-1',1300,'dark','2'],['practice','#pratik',1300,'light',null],['phone-examples','#kelime-1',390,'light','5']];
for(const [name,hash,w,scheme,key] of shots){
  const p=await b.newPage({viewport:{width:w,height:860},colorScheme:scheme});
  p.on('pageerror',e=>errs.push(`${name}: ${e.message}`));p.on('console',m=>{if(m.type()==='error')errs.push(`${name}: ${m.text()}`)});
  await p.goto('file://'+file+hash);await p.waitForTimeout(1200);
  if(key){await p.keyboard.press(key);await p.waitForTimeout(1500)}
  const sw=await p.evaluate(()=>document.documentElement.scrollWidth);if(sw>w)errs.push(`${name}: horizontal overflow ${sw}px > ${w}px`);
  await p.screenshot({path:path.join(out,name+'.png'),fullPage:w<500});await p.close();}
await b.close();console.log(errs.length?'PROBLEMS:\n'+errs.join('\n'):'OK: no errors, no overflow. Screenshots in '+out);process.exitCode=errs.length?1:0;})();
