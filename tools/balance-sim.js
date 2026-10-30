// Progression simulator for TRYPANON balance (effective seconds of play)
const REG=[['bukhan','화강암',1,0,'land',0],['gyeryong','장석',1.2,0,'land',0],['songni','석영',1.5,0,'land',0],['mai','역암',1.4,0,'land',0],['taebaek','텅스텐',1.6,0,'land',0],
 ['mudeung','응회암',2.2,200,'land',0],['jiri','편마암',3,1000,'land',0],['seorak','운모',4,2000,'land',0],['juwang','화산유리',5.5,4000,'land',0],['halla','현무암 섬유',7,8000,'land',0],
 ['west','규사',1,0,'sea',4],['south','원유',1.6,0,'sea',6],['east','천연가스',3,500,'sea',8],['deep','가스 하이드레이트',6,20000,'sea',14]].map(([id,res,diff,un,t,water])=>({id,res,diff,un,t,water}));
const PARTS=[['bit','텅스텐'],['housing','화강암'],['bearing','장석'],['shock','역암'],['sensor','석영','규사'],['heat','응회암'],['press','편마암'],['insul','운모'],['cool','화산유리','규사'],['cable','현무암 섬유']].map(([id,res,sub])=>({id,res,sub}));
function run(C,log=false){
  const S={ir:{priv:0,gov:0,mid:0,big:0,org:0},blocks:0,sea:0,blk:0,depth:0,dl:1,parts:Object.fromEntries(PARTS.map(p=>[p.id,0])),money:0,res:{},dig:{},t:0,inv:{}};
  const L=id=>S.parts[id];
  const dpsOf=()=>(3+2*L('housing'))*(1+C.bitK*L('bit'))*(1+.12*L('bearing'))*(1+.25*L('cable'));
  const pmv=C.pm||1,perks=()=>(S.inv.vc?1+.15*pmv:1)*(S.inv.inst?1+.25*pmv:1)*(S.inv.space?1+.1*pmv:1)*(C.rounds?1+.01*Math.min(20,S.ir.gov)*pmv:1);
  const layerAt=m=>C.LAY.find(l=>m<l.to)||C.LAY[C.LAY.length-1];
  const dlCost=dl=>Math.round(C.dlBase*Math.pow(C.dlGrow,dl-2));
  const partReq=dl=>Math.min(C.MAXLV,Math.floor((dl-1)/C.reqStep));
  const cost=p=>{const l=L(p.id),c={};c[p.res]=Math.ceil(C.RESC[l]);if(p.sub)c[p.sub]=Math.ceil(C.RESC[l]*.5);c.money=C.MONC[l];return c;};
  const can=c=>Object.entries(c).every(([k,v])=>k==='money'?S.money>=v:(S.res[k]||0)>=v);
  const pay=c=>{for(const[k,v]of Object.entries(c)){if(k==='money')S.money-=v;else S.res[k]-=v;}};
  const expHP=(r,i)=>r.t==='sea'&&i<r.water?2:C.expBase*r.diff*Math.pow(1+.1*(i-(r.water||0)),C.expGrow);
  const yieldOf=(r,i)=>Math.max(2,Math.round(C.yBase*Math.pow(expHP(r,i)/(C.expBase*r.diff),C.yExp)))*(1+.08+.05*L('sensor'));
  const INV=C.INV;let marks=[],lastDl=0,regCur=null,regHP=0;
  const dt=5;
  while(S.depth<6371000&&S.t<3e7){
    const l=layerAt(S.depth);
    // investors
    for(const v of INV)if(!S.inv[v.id]&&v.cond(S,L)){S.inv[v.id]=1;S.money+=v.amt*(C.inv||1);}
    if(C.rounds){const sumL=Object.values(S.parts).reduce((a,b)=>a+b,0),ra=(k,r)=>Math.max(200,k*dlCost(Math.min(C.DLOPEN,S.dl+1))*(C.inv||1)*(1+.04*r));
      const RC={priv:[()=>S.depth>=300*Math.pow(2.3,S.ir.priv),.1],gov:[()=>S.dl>=3+4*S.ir.gov,.18],mid:[()=>S.blocks>=60*Math.pow(1.75,S.ir.mid),.14],big:[()=>sumL>=12+8*S.ir.big,.2],org:[()=>S.t/3600*1.2>=2+3*S.ir.org,.12]};
      for(const k in RC){while(RC[k][0]()){S.money+=ra(RC[k][1],S.ir[k]);S.ir[k]++;}}}
    // bore
    if(l.req>S.dl)S.blk+=dt;if(l.req<=S.dl){const d=dpsOf()*perks()*Math.pow(C.dlMul,S.dl-1)*dt*(S.depth>=35000?1+(C.hk||0)*L('heat'):1)*(S.depth>=660000?1+(C.pk||0)*L('press'):1);const m=Math.min(d/l.H,l.to-S.depth);S.depth+=m;S.money+=m*l.v*C.moneyMul*(C.rounds?1+.01*Math.min(20,S.ir.priv)*pmv:1);}
    // pick needed part & region
    const req=partReq(Math.min(C.DLOPEN,S.dl+1));
    let need=PARTS.filter(p=>L(p.id)<req);if(!need.length)need=PARTS.filter(p=>L(p.id)<C.MAXLV);
    need.sort((a,b)=>L(a.id)-L(b.id));
    let target=null;for(const p of need){const c=cost(p);for(const[k,v]of Object.entries(c))if(k!=='money'&&(S.res[k]||0)<v){const r=REG.find(x=>x.res===k);if(r&&S.depth>=r.un){target=r;break;}}if(target)break;}
    if(!target){const un=REG.filter(r=>S.depth>=r.un&&r.t==='land');target=un[un.length-1];}
    if(target){const r=target,g=S.dig[r.id]=S.dig[r.id]||{i:0,hp:0};if(!g.hp)g.hp=expHP(r,g.i);
      let d=dpsOf()*perks()*(1+.1*L('insul'))*C.expDpsMul*dt*(C.wxG||1)*(S.inv.paleo?1+.1*pmv:1)*(r.t==='sea'?(1+(C.sk||0)*L('press'))*(S.inv.ship?1+.15*pmv:1):1);
      while(d>0){if(g.hp>d){g.hp-=d;d=0;}else{d-=g.hp;const below=r.t==='sea'?g.i-r.water:g.i;if(below>=0){S.res[r.res]=(S.res[r.res]||0)+yieldOf(r,g.i)*(C.wxY||1);S.blocks++;if(r.t==='sea')S.sea++;S.money+=C.exMoney*r.diff*Math.pow(expHP(r,g.i)/(C.expBase*r.diff),C.exMExp);}g.i++;g.hp=expHP(r,g.i);}}}
    // buy parts
    for(const p of need){const c=cost(p);if(L(p.id)<C.MAXLV&&can(c)){pay(c);S.parts[p.id]++;}}
    const nx=S.dl+1;if(nx<=C.DLOPEN&&PARTS.every(p=>L(p.id)>=partReq(nx))&&S.money>=dlCost(nx)){S.money-=dlCost(nx);S.dl=nx;}
    if(log&&S.dl!==lastDl&&S.dl%10===0){marks.push(`dl${S.dl}@${(S.t/3600).toFixed(1)}h d=${(S.depth/1000).toFixed(1)}km`);}lastDl=S.dl;
    S.t+=dt;}
  return {h:S.t/3600,blockedH:S.blk/3600,dl:S.dl,parts:Object.values(S.parts).join(','),marks,money:Math.round(S.money),dig:Object.fromEntries(Object.entries(S.dig).map(([k,v])=>[k,v.i]))};
}
module.exports={run,REG,PARTS};
