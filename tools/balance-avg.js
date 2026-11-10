const {execFileSync}=require('child_process');
const R=[17,26,43,67,103,158,241,362,546,768,1071,1494,2081,2889,4021,5596,6400,7200,8000,8800];
const sets=JSON.parse(process.argv[2]),mode=process.argv[3]||'';
for(const [name,ov] of Object.entries(sets)){let hs=[];for(const j of [1,1.004,1.008,1.012,1.016,0.996,0.992]){const c=Object.assign({slow:1,RESC:R},ov);c.boreK=(c.boreK||1)*j;c.expK=(c.expK||1)*(2-j);if(mode)c.untilFull=1;
  const r=JSON.parse(execFileSync('node',[__dirname+'/balance-hard.js',JSON.stringify(c)]).toString());hs.push(+r.h);}
  hs.sort((a,b)=>a-b);const m=hs.reduce((a,b)=>a+b,0)/hs.length;console.log(name.padEnd(12),Math.round(m)+'h','(med '+hs[3]+')');}
