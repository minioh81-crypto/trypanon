const {run}=require('./balance-sim.js');
const mk=(rows)=>rows.map(([from,to,H,v,req])=>({from,to,H,v,req}));
const LAY0=[[0,30,36,3,1],[30,15000,30,2,1],[15000,35000,396,4,6],[35000,660000,137,1,16],[660000,2900000,374,.8,26],[2900000,5150000,1587,2,36],[5150000,6371000,2193,4,46]];
const INV=[['mom',100,S=>true],['kim',300,S=>S.depth>=100],['prof',800,S=>S.t>3600*3],['tuber',2500,S=>S.depth>=1000],['sea',6000,S=>S.t>3600*8],['vc',15000,(S,L)=>Object.values(S.parts).reduce((a,b)=>a+b,0)>=20],['inst',60000,S=>S.depth>=12262],['global',500000,S=>S.depth>=35000],
 ['farm',1200,S=>S.blocks>=40],['miner',9000,S=>S.depth>=5000],['museum',22000,S=>S.t>3600*8],['paleo',30000,S=>S.t>3600*10],['ship',45000,S=>S.sea>=400],['energy',300000,S=>S.depth>=200000],['space',1500000,S=>S.depth>=660000]].map(([id,amt,cond])=>({id,amt,cond}));
function cfg(o){const b={INV,dlBase:150,dlGrow:1.2,MAXLV:10,reqStep:5,DLOPEN:50,bitK:.6,dlMul:1.1,expBase:100,expGrow:1.6,yBase:2,yExp:.55,moneyMul:1.4,expDpsMul:1,exMoney:5,exMExp:0,rounds:1};
  const c=Object.assign(b,o);const H=c.Hm||[1,1,1,1,1,1,1];c.LAY=mk(LAY0).map((l,i)=>Object.assign({},l,{H:l.H*(i>=2?c.Hmul:1)*H[i],v:l.v*(c.vmul?c.vmul[i]:1),req:c.req?c.req[i]:l.req}));return c;}
module.exports={cfg,run};
if(require.main===module){const o=JSON.parse(process.argv[2]);const r=run(cfg(o),true);console.log(JSON.stringify({h:+r.h.toFixed(1),blk:+r.blockedH.toFixed(1),rst:r.rst,marks:r.marks,money:r.money,yi:r.yiH}));}
