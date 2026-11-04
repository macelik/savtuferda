// Deterministic frame capture -> H.264 MP4.
// Usage: node video/render.js <timeline.html> <out.mp4> <seconds> [fps=30]
// Every CSS animation is paused and seeked to t (window.seek in scene.html), screenshotted, piped to ffmpeg.
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
(async()=>{const [file,out,secs,fpsArg]=process.argv.slice(2);if(!file||!out||!secs){console.error('usage: node video/render.js <timeline.html> <out.mp4> <seconds> [fps]');process.exit(2)}
const FPS=+fpsArg||30,T=+secs;
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',String(FPS),'-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(file));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1000);
const t0=Date.now();
for(let f=0;f<FPS*T;f++){await p.evaluate(t=>seek(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:95});
  if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
  if(f%300===0)console.log(`frame ${f}/${FPS*T}  ${((Date.now()-t0)/1000).toFixed(0)}s`);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log(`done -> ${out} in ${((Date.now()-t0)/1000).toFixed(0)}s`);})();
