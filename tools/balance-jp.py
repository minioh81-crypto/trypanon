import asyncio,sys,json
import os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'tests'))
from playwright.async_api import async_playwright
from _common import page,prep,GL
JS=r"""window.__SIM=(o)=>{const dt=o.dt||60;S.ex={active:null,dig:{}};S.unl=REG.filter(r=>r.un<=0).map(r=>r.id);S.res={};if(!o.all){S.fos={};S.relic={};S.inv={};S.leg=[];S.land={lv:1,tiles:{},furn:{}};}S.dz=null;S.part=1;S.depth=0;S.dl=1;S.money=0;S.done=false;S.parts={};PARTS.forEach(p=>S.parts[p.id]=0);if(o.hk){const m=MODES.jp;m.Hm=m.Hm.map(x=>x*o.hk);m.Hm2=m.Hm2.map(x=>x*o.hk);}if(o.vk){const m=MODES.jp;m.vmul=m.vmul.map(x=>x*o.vk);m.vmul2=m.vmul2.map(x=>x*o.vk);}applyMode();
  let t=0,spent=0,earned=0,hist=[],marks=[],lastL=-1,buys=[];const own=o.own||[];S.own=o.pre||[];if(o.all){S.fos={};FOSSILS.forEach(f=>S.fos[f.id]=[0,1,2,3,4]);RELICS.forEach(r=>S.relic[r.id]=GR.length-1);S.inv={};INV.forEach(v=>S.inv[v.id]=1);S.leg=['sex:yi','sex:yi2','sex:kim','sex:kim2','ship:turtle','horse:silla','sword:yi','sword:kim'];S.land={lv:6,tiles:{'0,0':'house_ry','3,0':'jinja','6,0':'azuchi','0,3':'torii'},furn:{}};}
  const upTo=lv=>{let c=0;PARTS.forEach(p=>{while(S.parts[p.id]<lv){c+=MONC[S.parts[p.id]]||0;S.parts[p.id]++;}});return c;};
  const partCost=lv=>PARTS.reduce((a,p)=>{let c=0;for(let k=S.parts[p.id];k<lv;k++)c+=MONC[k]||0;return a+c;},0);
  while(!S.done&&t<o.maxH*3600){const m0=S.money;boreAdvance(boreDps()*dt,false);if(!o.noExp){const rs=REG.filter(r=>isUnl(r)&&(!o.land||r.t!=='sea'));const r=rs.sort((a,b)=>b.un-a.un)[0];if(r){S.ex.active=r.id;exDamage(r,expDps(r.id)*dt,false);}}earned+=S.money-m0;t+=dt;
    if(o.earnK)S.money+=(S.money-m0)*(o.earnK-1),earned+=(S.money-m0)*0;
    for(let g=0;g<5;g++){const nx=S.dl+1;if(nx>DLOPEN)break;const lv=dlPartReq(nx),c=dlCost(nx)+partCost(lv);if(S.money<c)break;S.money-=c;spent+=c;upTo(lv);S.dl=nx;}
    hist.push(earned);if(hist.length>3600/dt)hist.shift();const rate=(earned-hist[0])/(hist.length*dt/3600);
    for(const b of own){if(S.own.includes(b.k))continue;if(S.money>=b.p&&b.p<=(o.hrs||1e9)*rate){S.money-=b.p;S.own.push(b.k);buys.push([b.k,+(t/3600).toFixed(1)]);}}
    const li=LAY.indexOf(layerAt(Math.min(S.depth,GOAL()-1)));if(li!==lastL){lastL=li;marks.push([li,+(t/3600).toFixed(1),S.dl,Math.round(incomePerSec()*3600),Math.round(earned)]);}}
  return {lt:LAY.map((_,i)=>{const a=marks.find(m=>m[0]===i),b=marks.find(m=>m[0]===i+1);return a?((b?b[1]:t/3600)-a[1]):0;}),h:+(t/3600).toFixed(1),dl:S.dl,done:S.done,marks,buys,earned:Math.round(earned)};};
window.__TUNE=(o)=>{const m=MODES.jp,out=[];if(o.init)Object.assign(m,JSON.parse(JSON.stringify(o.init)));for(let r=0;r<o.rounds;r++){const x=window.__SIM(Object.assign({},o,{hk:0,vk:0}));out.push([x.h,x.lt.map(v=>+v.toFixed(1))]);
  const req=[...m.LREQ,...m.LREQ2],dlAt=i=>{const k=x.marks.find(q=>q[0]===i);return k?k[2]:x.dl;};
  x.lt.forEach((a,i)=>{const f=Math.pow(Math.max(.25,Math.min(4,o.tgt[i]/Math.max(.05,a))),o.al||.7);let g=1;if(i<14){const gap=(req[i+1]+(o.over||2))-dlAt(i+1);g=Math.pow(1.115,Math.max(-12,Math.min(12,gap))*(o.be||.6));}
    if(i<9){m.Hm[i]*=f;m.vmul[i]*=g;}else{m.Hm2[i-9]*=f;m.vmul2[i-9]*=g;}});
  out[out.length-1].push(LAY.map((_,i)=>dlAt(i)));}
  return {out,Hm:m.Hm.map(v=>+v.toPrecision(4)),vmul:m.vmul.map(v=>+v.toPrecision(4)),Hm2:m.Hm2.map(v=>+v.toPrecision(4)),vmul2:m.vmul2.map(v=>+v.toPrecision(4))};};"""
async def run(setup,simo):
  url=page('window.__K={};'+JS,'psim.html')
  async with async_playwright() as p:
    b=await p.chromium.launch(args=GL);pg=await b.new_page()
    await prep(pg);await pg.add_init_script("localStorage.setItem('tp-stage','jp');localStorage.setItem('trypanon-save-jp',JSON.stringify(%s));"%json.dumps(setup))
    await pg.goto(url);await pg.wait_for_timeout(900)
    r=await pg.evaluate("o=>window[o.fn||'__SIM'](o)",simo);await b.close();return r
if __name__=='__main__':
  setup=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
  base={'money':0,'depth':1,'dl':1,'story':True,'leg':[],'mode':'hard'};base.update(setup)
  simo=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
  simo.setdefault('maxH',2000)
  r=asyncio.run(run(base,simo))
  if simo.get('fn')=='__TUNE':
    for h,lt,dl in r['out']:print('%.0fh'%h,lt,dl)
    print(json.dumps({k:r[k] for k in ['Hm','vmul','Hm2','vmul2']}));sys.exit()
  print('hours',r['h'],'dl',r['dl'],'done',r['done'],'earned %.3g'%r['earned'])
  for m in r['marks']:print('  layer%2d at %6.1fh dl%3d income/h %.3g  earned %.3g'%tuple(m))
  if r['buys']:print('buys',r['buys'])
