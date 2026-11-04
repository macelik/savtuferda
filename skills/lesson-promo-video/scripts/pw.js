// Resolve Playwright from the skill folder, then from the user's working directory.
const path=require('path');
module.exports=function loadPlaywright(){
  try{return require('playwright')}catch(e){}
  try{return require(require('module').createRequire(path.join(process.cwd(),'noop.js')).resolve('playwright'))}catch(e){}
  console.error('Playwright not found. In your working directory run:\n  npm i -D playwright\n  npx playwright install chromium');process.exit(2);
};
