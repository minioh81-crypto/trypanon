"""Performance pass on a 4x-throttled CPU (phone-like): fps / long tasks per screen. Usage: python3 tools/tests/perf.py [warmup_ms]"""
import asyncio,sys
from playwright.async_api import async_playwright
from _common import page,prep,GL
PROBE="""window.__lt=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push(Math.round(e.duration))}).observe({type:'longtask',buffered:true});
window.__fps=ms=>new Promise(r=>{let n=0;const t0=performance.now();const f=t=>{n++;if(t-t0<ms)requestAnimationFrame(f);else r(+(n*1000/(t-t0)).toFixed(1))};requestAnimationFrame(f);});"""
async def main():
    url=page("window.__K={show,openWard};",'page_perf.html')
    async with async_playwright() as p:
        b=await p.chromium.launch(args=GL);pg=await b.new_page(viewport={'width':390,'height':844})
        await prep(pg,{'money':9e9,'mode':'hard','dl':80,'depth':3000000,'story':1,'rv':4,'bv5':1,'last':0,'name':'a','wardSeen':1,'own':['sex:kim','horse:silla','ship:turtle'],'char':{'sex':'kim'}})
        await pg.add_init_script(PROBE);cdp=await pg.context.new_cdp_session(pg)
        await pg.goto(url);await pg.wait_for_timeout(1000);await pg.dispatch_event('#tStart','click')
        await pg.wait_for_timeout(int(sys.argv[1]) if len(sys.argv)>1 else 20000)
        await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
        for v in ['map','bore','craft','store','invest','shop','land','map']:
            await pg.evaluate("window.__lt=[]");await pg.evaluate(f"window.__K.show('{v}')");await pg.wait_for_timeout(1200)
            print(f'{v:7} fps {await pg.evaluate("window.__fps(2500)"):5} long tasks {sorted(await pg.evaluate("window.__lt"),reverse=True)[:3]}')
        await b.close()
asyncio.run(main())
