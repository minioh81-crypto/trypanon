"""Render every ending scene to tools/tests/out/end_<key>.png and a contact sheet end_sheet.png.
Usage: python3 tools/tests/endings.py [key,key,...]"""
import asyncio,sys
from playwright.async_api import async_playwright
from _common import page,prep,OUT
async def main():
    url=page("window.__E={keys:()=>[...Object.keys(EART),...Object.keys(EARTH)],art:k=>(EART[k]||EARTH[k])()};",'page_end.html')
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':320,'height':460});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await prep(pg,{'money':1e6,'mode':'hard','story':1,'rv':4,'bv5':1,'last':0,'name':'시추왕','wardSeen':1})
        await pg.goto(url);await pg.wait_for_timeout(1000)
        keys=sys.argv[1].split(',') if len(sys.argv)>1 else await pg.evaluate("window.__E.keys()")
        for k in keys:
            await pg.evaluate("k=>{let d=document.getElementById('__ev');if(!d){d=document.createElement('div');d.id='__ev';d.style.cssText='position:fixed;inset:0;z-index:99999;background:#000;width:320px;height:460px';document.body.appendChild(d);}d.innerHTML=window.__E.art(k);const v=d.querySelector('svg');if(v){v.setAttribute('width','320');v.setAttribute('height','460');}}",k)
            await pg.wait_for_timeout(2500);await pg.screenshot(path=str(OUT/f'end_{k}.png'),clip={'x':0,'y':0,'width':320,'height':460})
        await b.close()
    try:
        from PIL import Image,ImageDraw
        W,H=160,230;rows=[keys[i:i+10] for i in range(0,len(keys),10)];c=Image.new('RGB',(W*10,(H+14)*len(rows)),'white');d=ImageDraw.Draw(c)
        for r,row in enumerate(rows):
            for i,k in enumerate(row):c.paste(Image.open(OUT/f'end_{k}.png').resize((W,H)),(i*W,r*(H+14)+14));d.text((i*W+4,r*(H+14)),k,fill='black')
        c.save(OUT/'end_sheet.png')
    except ImportError:pass
    print(len(keys),'scenes →',OUT,'errors:',errs[:3] or 'none')
asyncio.run(main())
