"""Shared helpers: build a test page from src/trypanon.html, serve three.js offline, block web fonts."""
import json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
SRC=ROOT/'src'/'trypanon.html'
OUT=ROOT/'tools'/'tests'/'out'; OUT.mkdir(parents=True,exist_ok=True)
THREE=ROOT/'tools'/'vendor'/'three.min.js'
def page(expose='',name='page.html'):
    """Write a standalone test page; `expose` is JS injected inside the game closure (e.g. window.__K={show})."""
    html=SRC.read_text()
    if expose:html=html.replace("\n})();\n</script>","\n"+expose+"\n})();\n</script>")
    p=OUT/name;p.write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>')
    return 'file://'+str(p)
async def prep(pg,save=None):
    await pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
    await pg.route('**/three.min.js',lambda r:r.fulfill(path=str(THREE),content_type='application/javascript'))
    if save is not None:await pg.add_init_script("localStorage.setItem('trypanon-save-v1',%s);"%json.dumps(json.dumps(save)))
GL=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']
