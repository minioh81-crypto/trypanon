import asyncio,sys,os,io,base64
sys.path.insert(0,'/home/claude/trypanon/tools/tests')
from playwright.async_api import async_playwright
from _common import page,prep,GL
from PIL import Image
JS=r"""window.__shot=(which,views,W,H)=>{const T=THREE;const r=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setPixelRatio(1);r.setSize(W,H);document.body.appendChild(r.domElement);
const sc=new T.Scene();sc.background=new T.Color('#bcd6ea');sc.add(new T.HemisphereLight('#fff8ec','#506070',.85));const d=new T.DirectionalLight('#fff2d6',.85);d.position.set(-4,7,6);sc.add(d);const d2=new T.DirectionalLight('#9fd0ff',.35);d2.position.set(5,3,-6);sc.add(d2);
let ship;if(which==='old'){ship=s3Ship();for(const a of ship.userData.anims)a(1.3);ship.userData.fire.visible=false;}else{ship=tsShipPro();ship.position.y=-.3;ship.userData.tick(1.3);}
sc.add(ship);const w=s3Water();w.userData.tick(1.3);sc.add(w);const out=[];for(const v of views){const c=new T.PerspectiveCamera(v[6],W/H,.1,100);c.position.set(v[0],v[1],v[2]);c.lookAt(v[3],v[4],v[5]);r.render(sc,c);out.push(r.domElement.toDataURL());}r.domElement.remove();return out;};"""
async def main():
  ex=open('dragon.js').read()+open('ship2.js').read()
  url=page(ex+JS,'pship.html')
  async with async_playwright() as p:
    b=await p.chromium.launch(args=GL);errs=[];pg=await b.new_page();pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    await prep(pg,{'money':1});await pg.goto(url);await pg.wait_for_timeout(1500)
    V=[[-8.2,4.4,11.6,-1,1.3,0,32],[-1.1,1.6,15,-1.1,1.6,0,30]]
    W,H=800,520
    rows=[]
    V2=[[-10.4,5.4,14.6,-.8,2.1,0,32],[-.8,2.3,19.2,-.8,2.2,0,30]]
    for which,VV in [['old',V],['new',V2]]:
      ims=await pg.evaluate("([a,v,W,H])=>__shot(a,v,W,H)",[which,VV,W,H])
      rows.append([Image.open(io.BytesIO(base64.b64decode(s.split(',')[1]))) for s in ims])
    cl=await pg.evaluate("([a,v,W,H])=>__shot(a,v,W,H)",['new',[[-7.8,2.7,4.6,-3.1,1.5,0,30],[7,4,-13,0,2.2,0,32]],W,H])
    rows.append([Image.open(io.BytesIO(base64.b64decode(s.split(',')[1]))) for s in cl])
    c=Image.new('RGB',(W*2,H*3),'white')
    for j,row in enumerate(rows):
      for i,im in enumerate(row):c.paste(im,(i*W,j*H))
    c.save('out/ship_mock.png');c.resize((W,H*3//2)).save('out/ship_mock_s.png');print(errs[:3]);await b.close()
asyncio.run(main())
