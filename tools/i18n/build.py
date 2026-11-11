import json
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
TARGET=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'..','..','src','trypanon.html')
os.chdir(HERE)
f=json.load(open('frags.json'))
ent={}
for l in open('dict.tsv').read().strip().split('\n'):
  k,e,j=l.split('\t');ent[k]=(e,j)
for n in range(1,6):
  for l in open(f'tr{n}.tsv').read().strip('\n').split('\n'):
    i,e,j=l.split('\t');ent[f[int(i)]]=(e,j)
# fixes: 능력치 ja
ent['능력치']=('Stats','能力値')
rows=['\t'.join([k,e.replace('\n',' '),j.replace('\n',' ')]) for k,(e,j) in ent.items()]
data=json.dumps('\n'.join(rows),ensure_ascii=False)
js=r"""// ===== i18n (English / 日本語): translates the DOM text by exact phrase, by template pattern ({} = any value), by sub-phrase, then by word =====
const UILANG=(()=>{try{return localStorage.getItem('tp-lang')||'ko';}catch(e){return 'ko';}})();
function renderLangSeg(){const e=$('#mLang');if(!e)return;e.innerHTML=[['ko','한국어'],['en','English'],['ja','日本語']].map(([k,n])=>`<button type="button" data-lang="${k}" aria-pressed="${UILANG===k}">${n}</button>`).join('');}
renderLangSeg();
$('#mLang').addEventListener('click',e=>{const b=e.target.closest('[data-lang]');if(!b||b.dataset.lang===UILANG)return;try{localStorage.setItem('tp-lang',b.dataset.lang);sessionStorage.setItem('tp-skipT','1');}catch(_){}try{save();}catch(_){}location.reload();});
if(UILANG!=='ko'){(()=>{const li=UILANG==='en'?1:2,en=li===1,HG=/[가-힣]/,D=new Map(),PAT=[],SUB=[];
  const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  for(const l of __DATA__.split('\n')){const p=l.split('\t'),k=p[0],v=p[li];if(!v)continue;
    if(k.includes('{}')){const lits=k.split('{}');const longest=lits.filter(x=>HG.test(x)).reduce((a,b)=>b.length>a.length?b:a,'');if(longest.trim().length<2)continue;PAT.push({re:new RegExp('^\\s*'+lits.map(x=>esc(x)).join('([\\s\\S]*?)')+'\\s*$'),lit:longest.trim(),v,n:lits.join('').length});}
    else{D.set(k,v);if(k.length>=3&&HG.test(k))SUB.push([k,v]);}}
  PAT.sort((a,b)=>b.n-a.n);SUB.sort((a,b)=>b[0].length-a[0].length);
  const C=new Map(),RUN=/[가-힣][가-힣0-9 ·]*[가-힣]|[가-힣]/g;
  const fmtEn=v=>v>=1e12?(v/1e12).toFixed(v>=1e13?0:1).replace(/\.0$/,'')+'T':v>=1e9?(v/1e9).toFixed(v>=1e10?0:1).replace(/\.0$/,'')+'B':v>=1e6?(v/1e6).toFixed(v>=1e7?0:1).replace(/\.0$/,'')+'M':v>=1e4?(v/1e3).toFixed(0)+'K':v.toLocaleString('en-US');
  const pf=a=>parseFloat(String(a).replace(/,/g,''));
  const NUM=en?[[/₩([\d,.]+)\s?억\s?([\d,.]+)\s?만/g,(m,a,b)=>'₩'+fmtEn(pf(a)*1e8+pf(b)*1e4)],[/₩([\d,.]+)\s?(억|만|조)/g,(m,a,u)=>'₩'+fmtEn(pf(a)*(u==='만'?1e4:u==='억'?1e8:1e12))],[/([\d,.]+)\s?(억|만)(?![가-힣])/g,(m,a,u)=>fmtEn(pf(a)*(u==='만'?1e4:1e8))],
     [/(\d+)\s?레벨/g,'Lv.$1'],[/(\d+)\s?부(?![가-힣])/g,'Part $1'],[/(\d+)\s?회차/g,'Run $1'],[/(\d+)\s?일째/g,'Day $1'],[/([\d,.]+)\s?시간/g,'$1h'],[/([\d,.]+)\s?초(?![가-힣])/g,'$1s'],[/([\d,.]+)\s?분(?![가-힣])/g,'$1 min'],[/([\d,.]+)\s?개(?![가-힣])/g,'$1'],[/(\d+)\s?층/g,'$1F'],[/(\d+)\s?칸/g,'$1 tiles'],[/(\d+)\s?판(?![가-힣])/g,'$1 spins'],[/(\d+)\s?배(?![가-힣])/g,'×$1'],[/(\d+)\s?단계/g,'tier $1'],[/(\d+)\s?주(?![가-힣])/g,'$1 wk'],[/(\d+)\s?달(?![가-힣])/g,'$1 mo'],[/(\d+)\s?회(?![가-힣])/g,'$1×'],[/(\d+)\s?종(?![가-힣])/g,'$1 kinds'],[/(\d+)\s?일(?![가-힣])/g,'$1 days'],[/(\d+)\s?점(?![가-힣])/g,'$1 pts'],[/(\d+)\s?차(?![가-힣])/g,'round $1'],[/(\d+)\s?년/g,'$1 yr'],[/(\d+)\s?번(?![가-힣])/g,'$1×'],[/(\d+)\s?명(?![가-힣])/g,'$1']]
   :[[/₩([\d,.]+)\s?만/g,'₩$1万'],[/₩([\d,.]+)\s?억/g,'₩$1億'],[/₩([\d,.]+)\s?조/g,'₩$1兆'],[/([\d,.]+)\s?만(?![가-힣])/g,'$1万'],[/([\d,.]+)\s?억(?![가-힣])/g,'$1億'],[/(\d+)\s?레벨/g,'Lv.$1'],[/(\d+)\s?부(?![가-힣])/g,'第$1部'],[/(\d+)\s?회차/g,'$1周目'],[/(\d+)\s?일째/g,'$1日目'],[/([\d,.]+)\s?시간/g,'$1時間'],[/([\d,.]+)\s?초(?![가-힣])/g,'$1秒'],[/([\d,.]+)\s?분(?![가-힣])/g,'$1分'],[/([\d,.]+)\s?개(?![가-힣])/g,'$1個'],[/(\d+)\s?층/g,'$1階'],[/(\d+)\s?칸/g,'$1マス'],[/(\d+)\s?판(?![가-힣])/g,'$1回'],[/(\d+)\s?배(?![가-힣])/g,'$1倍'],[/(\d+)\s?단계/g,'$1段階'],[/(\d+)\s?주(?![가-힣])/g,'$1週'],[/(\d+)\s?달(?![가-힣])/g,'$1ヶ月'],[/(\d+)\s?회(?![가-힣])/g,'$1回'],[/(\d+)\s?종(?![가-힣])/g,'$1種'],[/(\d+)\s?일(?![가-힣])/g,'$1日'],[/(\d+)\s?점(?![가-힣])/g,'$1点'],[/(\d+)\s?차(?![가-힣])/g,'$1次'],[/(\d+)\s?년/g,'$1年'],[/(\d+)\s?번(?![가-힣])/g,'$1回'],[/(\d+)\s?명(?![가-힣])/g,'$1人']];
  const word=r=>{let d=D.get(r);if(d!=null)return d;const t=r.trim();d=D.get(t);if(d!=null)return r.replace(t,d);if(t.includes('·')){const ps=t.split(/\s*·\s*/);if(ps.every(p=>D.has(p)))return r.replace(t,ps.map(p=>D.get(p)).join(' · '));}
    if(t.includes(' ')){const ws=t.split(' ');if(ws.every(w=>D.has(w)))return r.replace(t,ws.map(w=>D.get(w)).join(' '));}return r;};
  let depth=0;
  const tr=t=>{if(!t||!HG.test(t))return t;let o=C.get(t);if(o!=null)return o;const tt=t.trim();
    o=D.get(tt);if(o!=null)o=t.replace(tt,o);
    else{o=null;if(depth<4){for(const p of PAT){if(!tt.includes(p.lit))continue;const m=p.re.exec(tt);if(!m)continue;depth++;let i=0;const v=p.v.replace(/\{\}/g,()=>{i++;return tr(m[i]||'');});depth--;o=t.replace(tt,v);break;}}
      if(o==null){o=t;for(const [k,v] of SUB){if(o.length<k.length)continue;if(o.includes(k)){o=o.split(k).join(v);if(!HG.test(o))break;}}
        if(HG.test(o)){for(const [re,f] of NUM)o=o.replace(re,f);o=o.replace(RUN,word);}}}
    if(C.size>8000)C.clear();C.set(t,o);return o;};
  const AT=['title','aria-label','placeholder','alt'];
  const el=e=>{for(const a of AT){const v=e.getAttribute&&e.getAttribute(a);if(v&&HG.test(v)){const n=tr(v);if(n!==v)e.setAttribute(a,n);}}};
  const fitTags=root=>{const gs=(root.querySelectorAll?root:document).querySelectorAll('.ptags>g');gs.forEach(g=>{const t=g.querySelector('text'),r=g.querySelectorAll('rect');if(!t||!r.length)return;let w=0;try{w=t.getComputedTextLength();}catch(_){}if(!w)return;w+=4;r[0].setAttribute('x',-w/2);r[0].setAttribute('width',w);if(r[1]){r[1].setAttribute('x',-w/2+.6);r[1].setAttribute('width',w-1.2);}});};
  const svgFit=(p,old)=>{if(!old||!p.getComputedTextLength||p.closest('.node,.ptags,.slmarq'))return;let nw=0;try{nw=p.getComputedTextLength();}catch(_){}if(nw>old*1.12){const fs=parseFloat(getComputedStyle(p).fontSize)||0;if(fs)p.style.fontSize=(fs*Math.max(.45,old*1.12/nw)).toFixed(2)+'px';}};
  const tnode=x=>{const p=x.parentNode;if(!p||p.tagName==='SCRIPT'||p.tagName==='STYLE'||(p.closest&&p.closest('[data-noi18n]')))return;const n=tr(x.data);if(n===x.data)return;let old=0;const sv=p.namespaceURI==='http://www.w3.org/2000/svg'&&p.getComputedTextLength;if(sv){try{old=p.getComputedTextLength();}catch(_){}}x.data=n;if(sv)svgFit(p,old);};
  const walk=root=>{if(root.nodeType===3){tnode(root);return;}if(root.nodeType!==1||root.tagName==='SCRIPT'||root.tagName==='STYLE')return;el(root);
    const w=document.createTreeWalker(root,5,null);let x;while((x=w.nextNode())){if(x.nodeType===3)tnode(x);else el(x);}
    if(root.querySelector&&root.querySelector('.ptags'))requestAnimationFrame(()=>fitTags(root));};
  document.documentElement.lang=UILANG;document.title=tr(document.title);walk(document.body);
  const TL=en?{map:'Map',bore:'Bore',exp:'Trips',craft:'Craft',store:'Items',shop:'Book',invest:'Invest',land:'Land'}:{map:'地図',bore:'本坑',exp:'遠征',craft:'製作',store:'倉庫',shop:'図鑑',invest:'投資',land:'土地'};document.querySelectorAll('nav.tabs [data-tab]').forEach(t=>{const n=[...t.childNodes].find(x=>x.nodeType===3&&x.data.trim());if(n&&TL[t.dataset.tab])n.data=TL[t.dataset.tab];});
  new MutationObserver(ms=>{for(const m of ms){if(m.type==='characterData')walk(m.target);else if(m.type==='attributes')el(m.target);else for(const n of m.addedNodes)walk(n);}}).observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:AT});
  // canvas-drawn words (bore/expedition scenes, 3D signs) go through the same translator
  {const P=CanvasRenderingContext2D.prototype,F=P.fillText,St=P.strokeText,M=P.measureText;P.fillText=function(t,...a){return F.call(this,typeof t==='string'?tr(t):t,...a);};P.strokeText=function(t,...a){return St.call(this,typeof t==='string'?tr(t):t,...a);};P.measureText=function(t){return M.call(this,typeof t==='string'?tr(t):t);};}
  window.__tr=tr;})();}
""".replace('__DATA__',data)
p=TARGET;s=open(p).read()
i=s.index('// ===== i18n (English');j=s.index('\n})();\n</script>')
s=s[:i]+js+s[j:]
open(p,'w').write(s)
print(len(ent),len(data))
