// QA for a built lesson page: node <skill>/scripts/check.js lessons/<slug>/X.html [outDir]
// Reports console errors + horizontal overflow, saves screenshots of key views.
const path=require('path');const fs=require('fs');
// Resolve Playwright from the skill folder, then from the user's working directory.
function loadPlaywright(){
  try{return require('playwright')}catch(e){}
  try{return require(require('module').createRequire(path.join(process.cwd(),'noop.js')).resolve('playwright'))}catch(e){}
  console.error('Playwright not found. In your working directory run:\n  npm i -D playwright\n  npx playwright install chromium');process.exit(2);
}
const {chromium}=loadPlaywright();
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
// One picture per card's animation (two moments, side by side in one file), to check motion graphics by eye.
{const p=await b.newPage({viewport:{width:1300,height:860}});p.on('pageerror',e=>errs.push(`anim: ${e.message}`));
 await p.goto('file://'+file+'#kelime-1');await p.waitForTimeout(800);
 const n=await p.evaluate(()=>JSON.parse(document.getElementById('data').textContent).cards.length);
 fs.mkdirSync(path.join(out,'anim'),{recursive:true});
 for(let i=1;i<=n;i++){await p.goto('file://'+file+'#kelime-'+i);
   for(const [t,tag] of [[700,'a'],[1900,'b']]){await p.waitForTimeout(t===700?700:1200);
     const el=await p.$('.stage .mg');if(!el){errs.push(`card ${i}: no animation rendered`);break}
     const box=await el.boundingBox();if(!box||box.width<50)errs.push(`card ${i}: animation has no size`);
     await el.screenshot({path:path.join(out,'anim',`card${String(i).padStart(2,'0')}-${tag}.png`)});}}
 await p.close();}
await b.close();console.log(errs.length?'PROBLEMS:\n'+errs.join('\n'):'OK: no errors, no overflow. Screenshots in '+out+' (animations: '+out+'/anim, two moments per card)');process.exitCode=errs.length?1:0;})();
