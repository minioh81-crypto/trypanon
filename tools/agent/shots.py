#!/usr/bin/env python3
"""화면 확인용 스크린샷(390×844 폰 화면, 결과는 tools/tests/out/shot_*.png).

  python3 tools/agent/shots.py tour            # 세계 투어(타이틀)
  python3 tools/agent/shots.py inf             # 무한의 땅: 시추·강화·드론·지도 탭
  python3 tools/agent/shots.py tunnel          # 터널 브레이커: 굴진(가까이/멀리)·강화·자재·현장·개통식
  python3 tools/agent/shots.py tunnel-sea      # 해저 TBM 터널(통영) + 침매터널(가덕) 밖/안
  python3 tools/agent/shots.py tunnel-open     # 개통한 터널(차량)
  python3 tools/agent/shots.py mj              # 중국 사천성 마작 + 힌트
  python3 tools/agent/shots.py all

3D는 tools/vendor/three.min.js(오프라인)로 그림. 그림을 바꿨으면 꼭 찍어서 눈으로 확인할 것.
"""
import asyncio,sys,json,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'tests'))
from playwright.async_api import async_playwright
from _common import page,prep,GL,OUT
HOOK=r"""window.__A={
 tu:(c,o)=>{o=o||{};localStorage.setItem('tp-tunnel',JSON.stringify(Object.assign({money:5e4,cur:c,done:[],p:{cut:20,jack:0,conv:0,pump:0},prog:{[c]:300}},o)));tuTab='dig';tuOpenWin();},
 tab:k=>{tuTab=k;tuRender();},cam:(y,d,p,t)=>{tu3.yaw=y;tu3.dist=d;tu3.pitch=p;tu3.dbgT=t||null;},close:()=>tuClose(),cer:k=>tuCeremony(k,123456),
 inf:()=>{infOpenWin();SI.money=5e9;SI.p={bit:30,motor:30,cool:30,coll:30};SI.depth=61*300+120;SI.best=63*300;infTab='bore';infRender();},itab:k=>{infTab=k;infRender();},
 mj:()=>{mjOpen();for(let k=0;k<5;k++){const P=mjPairs();if(!P.length)break;mjTap(P[0][0]);mjTap(P[0][1]);}document.getElementById('mjHint').click();}
};"""
async def shot(pg,name,box=None):
    f=OUT/f'shot_{name}.png'
    if box:await pg.screenshot(path=str(f),clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    else:await pg.screenshot(path=str(f))
    print('저장',f.name)
async def tu3box(pg):return await pg.evaluate("(()=>{const r=document.querySelector('.tu3').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
async def stopauto(pg,b):
    await pg.mouse.move(b[0]+200,b[1]+150);await pg.mouse.down();await pg.mouse.move(b[0]+201,b[1]+150);await pg.mouse.up()
async def run(what):
    url=page(HOOK,'shots.html')
    async with async_playwright() as p:
        br=await p.chromium.launch(args=GL);errs=[]
        pg=await br.new_page(viewport={'width':390,'height':844},device_scale_factor=2);pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
        await prep(pg);await pg.add_init_script("localStorage.setItem('tp-jptest','1');localStorage.setItem('tp-cntest','1');")
        await pg.goto(url);await pg.wait_for_timeout(1500)
        if what in('tour','all'):
            e=await pg.query_selector('#tTour');await e.screenshot(path=str(OUT/'shot_tour.png'));print('저장 shot_tour.png')
        if what in('inf','all'):
            await pg.evaluate("__A.inf()");await pg.wait_for_timeout(1500);await shot(pg,'inf_bore')
            for t in ['up','dr','map']:
                await pg.evaluate(f"__A.itab('{t}')");await pg.wait_for_timeout(900);await shot(pg,'inf_'+t)
            await pg.goto(url);await pg.wait_for_timeout(1200)
        if what in('tunnel','all'):
            await pg.evaluate("__A.tu('namsan')");await pg.wait_for_timeout(2500);b=await tu3box(pg);await shot(pg,'tu_dig')
            await stopauto(pg,b)
            for n,cm in [('tu_face',".2,5,.2,[1.6,1.4,0]"),('tu_dump',".45,3.2,.2,[-4.3,.5,-.45]"),('tu_gantry',".6,4.5,.15,[-6.5,1.8,-.9]")]:
                await pg.evaluate(f"__A.cam({cm})");await pg.wait_for_timeout(2500);await shot(pg,n,b)
            for t in ['tbm','mat','site']:
                await pg.evaluate(f"__A.tab('{t}')");await pg.wait_for_timeout(1500);await shot(pg,'tu_'+t)
            await pg.evaluate("__A.cer('namsan')");await pg.wait_for_timeout(3500);await shot(pg,'tu_ceremony');await pg.evaluate("__A.close()")
        if what in('tunnel-sea','all'):
            await pg.evaluate("__A.tu('tongyeong',{done:['namsan']})");await pg.wait_for_timeout(2500);await shot(pg,'tu_sea');await pg.evaluate("__A.close()")
            for v in ['place','inside']:
                await pg.evaluate(f"__A.tu('gadeok',{{done:['namsan','tongyeong','jukryeong'],immView:'{v}'}})");await pg.wait_for_timeout(3000);await shot(pg,'tu_imm_'+v);await pg.evaluate("__A.close()")
        if what in('tunnel-open','all'):
            await pg.evaluate("__A.tu('namsan',{done:['namsan'],prog:{namsan:1530}})");await pg.wait_for_timeout(2500);await shot(pg,'tu_open');await pg.evaluate("__A.close()")
        if what in('mj','all'):
            save={'money':9e5,'depth':2000,'dl':5,'story':True,'jstory':1,'mode':'normal','own':[],'leg':[]}
            await pg.evaluate("localStorage.setItem('tp-stage','cn');localStorage.setItem('trypanon-save-cn',%s)"%json.dumps(json.dumps(save)))
            await pg.goto(url);await pg.wait_for_timeout(1500);await pg.evaluate("document.getElementById('tStart').click()");await pg.wait_for_timeout(1200)
            for _ in range(8):
                if await pg.is_visible('#sSkip'):await pg.dispatch_event('#sSkip','click');await pg.wait_for_timeout(200)
            await pg.evaluate("__A.mj()");await pg.wait_for_timeout(700);await shot(pg,'mj_hint')
        print('페이지 오류:',errs[:6] or '없음');await br.close()
if __name__=='__main__':asyncio.run(run(sys.argv[1] if len(sys.argv)>1 else 'all'))
