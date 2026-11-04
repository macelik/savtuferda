// Frame-accurate capture of a composed timeline -> H.264 MP4 (1080x1920, silent).
// Usage: node render.js <full.html|short.html> <out.mp4> [fps=30]
// Every CSS animation is paused and seeked to each frame time (window.seek), screenshotted, piped to ffmpeg.
const {chromium}=require('./pw.js')();const {spawn}=require('child_process');const path=require('path');
(async()=>{const [file,out,fpsArg]=process.argv.slice(2);if(!file||!out){console.error('usage: node render.js <timeline.html> <out.mp4> [fps]');process.exit(2)}
const FPS=+fpsArg||30;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(file));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1000);
const T=await p.evaluate(()=>window.TOTAL);
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',String(FPS),'-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
ff.on('error',()=>{console.error('ffmpeg not found: install ffmpeg (with libx264).');process.exit(2)});
const t0=Date.now();
for(let f=0;f<Math.round(FPS*T);f++){await p.evaluate(t=>seek(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:95});
  if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
  if(f%300===0)console.log(`frame ${f}/${Math.round(FPS*T)}  ${((Date.now()-t0)/1000).toFixed(0)}s`);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log(`done -> ${out} (${T}s) in ${((Date.now()-t0)/1000).toFixed(0)}s`);})();
