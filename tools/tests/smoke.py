"""Smoke test: every tab, every region popup, an expedition, wardrobe tabs, normal + hard. Prints fps and page errors.
Usage: python3 tools/tests/smoke.py"""
import asyncio
from playwright.async_api import async_playwright
from _common import page,prep,GL
REGS=['bukhan','gyeryong','songni','mai','taebaek','mudeung','jiri','seorak','juwang','halla','west','south','east','deep']
async def one(b,url,mode):
    errs=[];pg=await b.new_page(viewport={'width':400,'height':860})
    pg.on('pageerror',lambda e:errs.append('PE '+str(e)));pg.on('console',lambda m:errs.append('CON '+m.text) if m.type=='error' and 'ERR_FAILED' not in m.text else None)
    save={'money':9e7,'dl':40,'depth':900000,'story':1,'rv':4,'bv5':1,'last':0,'name':'테스트','mode':mode,'unl':REGS,'own':['sex:yi'],'char':{'sex':'m'},
      'land':{'lv':6,'tiles':{'3,0':'museum','0,3':'dog','1,3':'fox','0,0':'house_y'},'furn':{'bed':1,'cat':1,'penguin':1}}}
    await prep(pg,save);await pg.goto(url);await pg.wait_for_timeout(700)
    await pg.dispatch_event('#tStart','click');await pg.wait_for_timeout(400)
    fps=await pg.evaluate("new Promise(r=>{let n=0,t0=performance.now();const f=()=>{n++;if(performance.now()-t0<2000)requestAnimationFrame(f);else r(n/2)};requestAnimationFrame(f)})")
    for rid in REGS:
        await pg.dispatch_event(f'.node[data-id={rid}]','click');await pg.wait_for_timeout(120)
        if await pg.is_visible('#rpop'):await pg.dispatch_event('#rClose','click')
    await pg.dispatch_event('.node[data-id=jiri]','click');await pg.wait_for_timeout(200)
    await pg.dispatch_event('#card [data-act=go]','click');await pg.wait_for_timeout(1200)
    if await pg.is_visible('#eGo'):await pg.dispatch_event('#eGo','click');await pg.wait_for_timeout(1200)
    expOpen=await pg.is_visible('#exp')
    if await pg.is_visible('#eBack'):await pg.dispatch_event('#eBack','click')
    for t in ['bore','craft','store','shop','invest','land','map','exp','map']:
        await pg.dispatch_event(f'nav.tabs [data-tab={t}]','click');await pg.wait_for_timeout(450)
    await pg.dispatch_event('#avatarBtn','click');await pg.wait_for_timeout(200)
    for t in ['sex','hero','hair','hcol','eyes','skin','body','hat','outfit','item']:
        await pg.dispatch_event(f'[data-t={t}]','click');await pg.wait_for_timeout(120)
    await pg.dispatch_event('#wClose','click');await pg.wait_for_timeout(200)
    print(f'{mode:6} fps {fps:5.1f} | expedition opened {expOpen} | errors {errs[:4] or "none"}')
    await pg.close();return not errs
async def main():
    url=page()
    async with async_playwright() as p:
        b=await p.chromium.launch(args=GL)
        ok=[await one(b,url,m) for m in ('normal','hard')]
        await b.close()
    raise SystemExit(0 if all(ok) else 1)
asyncio.run(main())
