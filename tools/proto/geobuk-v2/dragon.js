/* 거북선 용머리(시안): SDF로 깎고 부위별로 칠한다. 앞(주둥이)은 +x, 위 +y. 길이 약 1.4 */
function tsDragonHead(pal={}){
  const T=THREE,D=SDF,E=D.E,C=D.C;
  const skull=[
    E([0,0,0],[.30,.25,.25]),
    C([.08,.04,0],[.55,.05,0],.17,.125,.08),
    E([.62,.11,0],[.12,.105,.135],.06),            /* 위로 말린 코끝 */
    C([-.05,-.04,0],[-.62,-.34,0],.19,.235,.08),   /* 목 */
    E([.17,.19,0],[.2,.09,.2],.05),                 /* 이마 */
  ];
  for(const s of [-1,1]){
    skull.push(E([.2,.17,s*.15],[.13,.07,.085],.04));                 /* 눈두덩 */
    skull.push(E([.66,.17,s*.07],[.055,.05,.05],.03));                /* 콧망울 */
    skull.push(E([-.02,-.02,s*.2],[.12,.13,.07],.05));                /* 볼 */
  }
  const head=D.list(skull);
  const jawL=D.list([C([.04,-.17,0],[.54,-.4,0],.115,.07,0),E([.56,-.41,0],[.075,.05,.09],.03)]);
  const cavity=p=>D.smin(D.ell(p,[.4,-.18,0],[.34,.12,.11]),D.cap(p,[.08,-.11,0],[.66,-.22,0],.075,.06),.05);
  const teeth=[];
  for(let i=0;i<6;i++){const x=.2+i*.068,t=(x-.04)/.5,yb=-.07-t*.25;for(const s of [-1,1]){
    teeth.push(C([x,-.07,s*(.1-i*.006)],[x+.008,-.15,s*(.095-i*.006)],.021,.004,0));
    teeth.push(C([x,yb-.02,s*(.06-i*.003)],[x-.004,yb+.06,s*(.06-i*.003)],.017,.003,0));}}
  for(const s of [-1,1]){teeth.push(C([.6,-.05,s*.08],[.63,-.24,s*.07],.03,.004,0));teeth.push(C([.55,-.36,s*.055],[.57,-.2,s*.055],.026,.004,0));}
  const tooth=D.list(teeth);
  const tongue=D.list([C([.12,-.2,0],[.48,-.27,0],.05,.04,0),C([.48,-.27,0],[.72,-.17,0],.04,.018,.02)]);
  const eyeC=s=>[.27,.165,s*.19],eye=p=>Math.min(D.ell(p,eyeC(-1),[.075,.07,.07]),D.ell(p,eyeC(1),[.075,.07,.07]));
  const hornL=[],maneL=[],beardL=[];
  for(const s of [-1,1]){
    hornL.push(C([.04,.22,s*.1],[-.3,.42,s*.18],.055,.04,0),C([-.3,.42,s*.18],[-.62,.5,s*.24],.04,.016,.02),C([-.18,.34,s*.15],[-.24,.5,s*.12],.025,.01,.02));
    for(let i=0;i<5;i++){const y=.2-i*.11,z=s*(.17+i*.01),x=-.1-i*.08;
      maneL.push(C([x,y,z],[x-.2,y+.07,z+s*.08],.062,.034,.03),C([x-.2,y+.07,z+s*.08],[x-.3,y+.22,z+s*.04],.034,.006,.015));}
    beardL.push(C([.32,-.33,s*.08],[.12,-.52,s*.1],.035,.012,.02),C([.12,-.52,s*.1],[-.02,-.6,s*.06],.012,.004,.01),
      C([.62,.08,s*.11],[.85,.16,s*.3],.014,.006,0),C([.85,.16,s*.3],[1.02,.06,s*.42],.006,.003,0));   /* 수염 */
  }
  const horn=D.list(hornL),mane=D.list(maneL),beard=D.list(beardL);
  const scales=p=>{const [x,y,z]=p;return .006*Math.max(0,Math.sin(x*42+Math.abs(z)*20))*Math.max(0,Math.sin(y*38-x*10))*(x<.1?1:0);};
  const F=p=>{let d=D.smax(D.smin(head(p),jawL(p),.06),-cavity(p),.025);d+=scales(p);
    d=Math.min(d,tooth(p),tongue(p),eye(p));d=D.smin(d,horn(p),.02);d=D.smin(d,mane(p),.02);d=D.smin(d,beard(p),.015);return d;};
  const g=sdfAO(sdfMesh(F,[-1.15,-.78,-.62],[1.1,.72,.62],.011),F,.03);
  /* 부위별 색: 몸(청록·금 비늘), 입안·혀(붉은), 이빨(상아), 눈(금빛+검은 눈동자), 뿔(금), 갈기(주홍) */
  const P=g.attributes.position,Cc=g.attributes.color,col=new T.Color(),cBody=new T.Color(pal.body||'#1c5248'),cBody2=new T.Color(pal.body2||'#3a8a68'),cRed=new T.Color(pal.mouth||'#b3261e'),cTongue=new T.Color(pal.tongue||'#e0504a'),
    cTooth=new T.Color(pal.tooth||'#f3ead2'),cGold=new T.Color(pal.gold||'#e3b341'),cBlack=new T.Color('#141414'),cMane=new T.Color(pal.mane||'#d9572b'),cBeard=new T.Color(pal.beard||'#e8c25a'),cHorn=new T.Color(pal.horn||pal.gold||'#e3b341');
  const q=[0,0,0];
  for(let i=0;i<P.count;i++){q[0]=P.getX(i);q[1]=P.getY(i);q[2]=P.getZ(i);
    const dd={tooth:tooth(q),tongue:tongue(q),eye:eye(q),horn:horn(q),mane:mane(q),beard:beard(q),cav:Math.abs(cavity(q))+.004};
    let k='body',m=.012;for(const n in dd)if(dd[n]<m){m=dd[n];k=n;}
    if(k==='tooth')col.copy(cTooth);else if(k==='tongue')col.copy(cTongue);else if(k==='cav')col.copy(cRed);
    else if(k==='eye'){const sg=q[2]<0?-1:1,e=eyeC(sg),v=[(q[0]-e[0])/.075,(q[1]-e[1])/.07,(q[2]-e[2])*sg/.07],dp=v[0]*.62+v[1]*.1+v[2]*.78;col.copy(dp>.72?cBlack:cGold);}
    else if(k==='horn')col.copy(cHorn);else if(k==='mane')col.copy(cMane);else if(k==='beard')col.copy(cBeard);
    else{col.copy(cBody).lerp(cBody2,Math.max(0,Math.min(1,.5+q[1]*1.6)));if(scales(q)>.003)col.lerp(cGold,pal.scaleK??.45);}
    const a=Cc.getX(i);Cc.setXYZ(i,col.r*a,col.g*a,col.b*a);}
  Cc.needsUpdate=true;
  return new T.Mesh(g,new T.MeshPhongMaterial({vertexColors:true,shininess:pal.shin??38,specular:pal.spec||'#555'}));
}
