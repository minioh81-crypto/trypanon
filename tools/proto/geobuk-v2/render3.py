import asyncio,sys,io,base64
sys.path.insert(0,'/home/claude/trypanon/tools/tests')
from playwright.async_api import async_playwright
from _common import page,prep,GL
from PIL import Image
JS=r"""window.__shot=(views,W,H,sea)=>{const T=THREE;const r=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setPixelRatio(1);r.setSize(W,H);document.body.appendChild(r.domElement);
const sc=new T.Scene();sc.background=new T.Color('#c9ced0');sc.fog=new T.Fog('#c9ced0',18,40);sc.add(new T.HemisphereLight('#fff8ec','#5a6470',.8));const d=new T.DirectionalLight('#fff2d6',.9);d.position.set(-4,7,6);sc.add(d);const d2=new T.DirectionalLight('#9fd0ff',.3);d2.position.set(5,3,-6);sc.add(d2);
const ship=tsShip3();ship.userData.tick(1.3);if(sea){ship.position.y=-.1;const w=s3Water();w.userData.tick(1.3);sc.add(w);}sc.add(ship);const out=[];for(const v of views){const c=new T.PerspectiveCamera(v[6],W/H,.1,100);c.position.set(v[0],v[1],v[2]);c.lookAt(v[3],v[4],v[5]);r.render(sc,c);out.push(r.domElement.toDataURL());}r.domElement.remove();return out;};"""
async def main(name,views,W,H,sea):
  ex=open('dragon.js').read()+open('ship3.js').read()
  url=page(ex+JS,'pship3.html')
  async with async_playwright() as p:
    b=await p.chromium.launch(args=GL);errs=[];pg=await b.new_page();pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    await prep(pg,{'money':1});await pg.goto(url);await pg.wait_for_timeout(1500)
    ims=await pg.evaluate("([v,W,H,s])=>__shot(v,W,H,s)",[views,W,H,sea])
    ims=[Image.open(io.BytesIO(base64.b64decode(s.split(',')[1]))) for s in ims]
    c=Image.new('RGB',(W*len(ims),H))
    for i,im in enumerate(ims):c.paste(im,(i*W,0))
    c.save(f'out/{name}.png');print(errs[:3]);await b.close()
import json
asyncio.run(main(sys.argv[1],json.loads(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]=='1'))
