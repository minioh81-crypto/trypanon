/* 거북선 시안 v3 (사진 참고: 모양만 따라 직접 만든 모델)
   - 길고 각진 선체, 평평한 뱃머리 벽 한가운데 청동 용머리
   - 뱃전 아래 멍에(가로보) 끝이 튀어나온 판자 턱, 그 아래에서 비스듬히 뒤로 뻗는 노
   - 위 벽은 판자 칸막이·둥근 포문, 네 모서리 기둥
   - 낮고 넓은 철갑 지붕: 마름모 철판 + 세로 띠 + 줄지어 박힌 쇠못
   - 돛대 2개: 꼭대기 가로대, 대나무 살이 든 흰 돛, 살 끝에서 모이는 돛 줄 */
function tsShip3(){
  const T=THREE,ship=new T.Group(),oars=[],P=Math.PI;
  const rnd=i=>(Math.sin(i*127.1+3.7)*43758.5453%1+1)%1;
  const tex=(k,w,h,draw,rx=1,ry=1)=>{const t=s3Tex(k,w,h,draw);t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(rx,ry);return t;};
  const M=(c,o={})=>new T.MeshPhongMaterial(Object.assign({color:c,shininess:8,specular:'#2a241c'},o));
  const add=(p,g,m,x=0,y=0,z=0)=>{const o=new T.Mesh(g,m);o.position.set(x,y,z);p.add(o);return o;};
  const strut=(p,m,a,b,r1,r2=r1,n=7)=>{const A=new T.Vector3(...a),B=new T.Vector3(...b),d=B.clone().sub(A);const o=add(p,new T.CylinderGeometry(r2,r1,d.length(),n),m,(A.x+B.x)/2,(A.y+B.y)/2,(A.z+B.z)/2);o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),d.normalize());return o;};
  const beam=(p,m,a,b,w,h)=>{const A=new T.Vector3(...a),B=new T.Vector3(...b),d=B.clone().sub(A);const o=add(p,new T.BoxGeometry(w,d.length(),h),m,(A.x+B.x)/2,(A.y+B.y)/2,(A.z+B.z)/2);o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),d.normalize());return o;};
  const line=(p,m,pts,r=.008)=>add(p,new T.TubeGeometry(new T.CatmullRomCurve3(pts.map(v=>new T.Vector3(...v))),Math.max(6,pts.length*6),r,4,false),m);
  const sheet=(p,m,n,k,f)=>{const pos=[],uv=[],idx=[];for(let i=0;i<=n;i++)for(let j=0;j<=k;j++){const a=i/n,b=j/k;pos.push(...f(a,b));uv.push(a,b);if(i<n&&j<k){const q=i*(k+1)+j;idx.push(q,q+1,q+k+1,q+1,q+k+2,q+k+1);}}
    const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();return add(p,g,m);};

  /* ---- 재질(캔버스 텍스처) ---- */
  const plank=tex('ts3Plank',512,256,(g,w,h)=>{for(let r=0;r<10;r++){const y=r*h/10;g.fillStyle=`hsl(30,${26+rnd(r)*10}%,${30+rnd(r+9)*12}%)`;g.fillRect(0,y,w,h/10);g.fillStyle='rgba(25,16,10,.75)';g.fillRect(0,y,w,2);
      for(let x=(r%3)*90;x<w;x+=260){g.fillStyle='rgba(25,16,10,.6)';g.fillRect(x,y,2,h/10);g.fillStyle='#2a1e14';g.beginPath();g.arc(x+8,y+8,2.2,0,7);g.arc(x+8,y+h/10-8,2.2,0,7);g.fill();}}
    for(let i=0;i<2600;i++){g.fillStyle=i%3?'rgba(30,20,12,.14)':'rgba(220,190,140,.14)';g.fillRect(rnd(i)*w,rnd(i+77)*h,6+rnd(i+5)*30,1);}},6,1);
  const panel=tex('ts3Panel',512,128,(g,w,h)=>{g.fillStyle='#6b5038';g.fillRect(0,0,w,h);
    for(let i=0;i<5200;i++){g.fillStyle=i%3?'rgba(30,20,12,.12)':'rgba(220,190,140,.12)';g.fillRect(rnd(i)*w,rnd(i+31)*h,1,4+rnd(i+3)*14);}
    for(let c=0;c<4;c++){const x=c*w/4;g.fillStyle='#4a3524';g.fillRect(x,0,12,h);g.fillStyle='#8a6a48';g.fillRect(x+12,0,2,h);
      g.strokeStyle='#3d2c1e';g.lineWidth=5;g.strokeRect(x+26,18,w/4-40,h-36);g.strokeStyle='rgba(200,160,110,.35)';g.lineWidth=1.5;g.strokeRect(x+30,22,w/4-48,h-44);
      g.fillStyle='#120c08';g.beginPath();g.arc(x+w/8+6,h*.52,10,0,7);g.fill();g.strokeStyle='#8a6a48';g.lineWidth=2;g.stroke();}
    g.fillStyle='#3d2c1e';g.fillRect(0,0,w,8);g.fillRect(0,h-8,w,8);},7,1);
  const iron=tex('ts3Iron',256,256,(g,w,h)=>{g.fillStyle='#7d858a';g.fillRect(0,0,w,h);
    for(let r=-1;r<9;r++)for(let c=-1;c<9;c++){const x=c*32+(r%2)*16,y=r*32;g.beginPath();g.moveTo(x,y-16);g.lineTo(x+16,y);g.lineTo(x,y+16);g.lineTo(x-16,y);g.closePath();
      g.fillStyle=`hsl(200,${5+rnd(r*9+c)*5}%,${44+rnd(r*7+c+3)*12}%)`;g.fill();g.strokeStyle='#3b4246';g.lineWidth=2;g.stroke();g.fillStyle='#c2c6c4';g.fillRect(x-1,y-1,2.5,2.5);}},10,3);
  const sailT=tex('ts3Sail',256,512,(g,w,h)=>{g.fillStyle='#ece5d2';g.fillRect(0,0,w,h);for(let y=0;y<h;y+=h/12){const gr=g.createLinearGradient(0,y,0,y+h/12);gr.addColorStop(0,'#c8bfa8');gr.addColorStop(.2,'#f4efe2');gr.addColorStop(.8,'#e6dfca');gr.addColorStop(1,'#bdb39b');g.fillStyle=gr;g.fillRect(0,y,w,h/12);}
    for(let x=0;x<w;x+=42){g.fillStyle='rgba(120,105,80,.25)';g.fillRect(x,0,1,h);}for(let i=0;i<1500;i++){g.fillStyle='rgba(110,95,70,.07)';g.fillRect(rnd(i)*w,rnd(i+9)*h,4,1);}});
  const wood=M('#8a6a4a',{map:plank,side:T.DoubleSide}),woodD=M('#4a3526'),woodL=M('#6e5238'),oarM=M('#8a6c4c'),walls=M('#fff',{map:panel,side:T.DoubleSide}),roofM=M('#858c90',{map:iron,shininess:22,specular:'#444',side:T.DoubleSide}),
    rail=M('#4e3a28'),spikeM=M('#3c4246',{shininess:60,specular:'#888'}),rope=M('#8f7a5a'),sail=M('#fff',{map:sailT,side:T.DoubleSide,shininess:4}),bat=M('#6b5236'),dark=M('#140e0a');

  /* ---- 치수 ---- */
  const L=6.4,fx=u=>L*(u-.5),W=u=>.98*(1-.36*Math.pow(Math.abs(2*u-1),2.4)),
    keel=u=>-.62+.4*Math.pow(Math.abs(2*u-1),2.6)+(u<.5?.06*Math.pow(1-2*u,2):0),LEf=u=>.5+.16*Math.pow(Math.abs(2*u-1),3),WTf=u=>1.16+.2*Math.pow(Math.abs(2*u-1),3),wallZ=u=>W(u)+.1;

  /* 아래 선체: 용골에서 뱃전 턱까지 둥글게 */
  for(const s of [-1,1])sheet(ship,wood,48,10,(a,b)=>{const u=.02+a*.96,k=keel(u),y=k+(LEf(u)-k)*b;return [fx(u),y,s*W(u)*(.38+.62*Math.sin(b*P/2))];});
  sheet(ship,wood,48,4,(a,b)=>{const u=.02+a*.96;return [fx(u),keel(u),(b*2-1)*W(u)*.38];});
  /* 뱃전 턱(멍에 판) + 튀어나온 가로보 끝 */
  for(const s of [-1,1]){
    sheet(ship,woodD,48,1,(a,b)=>{const u=.02+a*.96;return [fx(u),LEf(u),s*(W(u)+b*.2)];});
    sheet(ship,woodD,48,1,(a,b)=>{const u=.02+a*.96;return [fx(u),LEf(u)-.07*b,s*(W(u)+.2)];});
    for(let i=0;i<17;i++){const u=.05+i*.0565;add(ship,new T.BoxGeometry(.08,.08,.3),woodL,fx(u),LEf(u)-.04,s*(W(u)+.2));}
  }
  /* 위 벽: 판자 칸막이 + 포문 */
  for(const s of [-1,1])sheet(ship,walls,48,1,(a,b)=>{const u=.02+a*.96;return [fx(u),LEf(u)+b*(WTf(u)-LEf(u)),s*wallZ(u)];});
  for(const s of [-1,1]){line(ship,rail,Array.from({length:20},(_,i)=>{const u=.02+i/19*.96;return [fx(u),WTf(u),s*(wallZ(u)+.01)];}),.03);
    line(ship,rail,Array.from({length:20},(_,i)=>{const u=.02+i/19*.96;return [fx(u),LEf(u)+.02,s*(wallZ(u)+.01)];}),.025);}
  /* 뱃머리·고물 벽 */
  for(const [u,dx] of [[.02,-1],[.98,1]]){const x=fx(u);
    sheet(ship,wood,10,8,(a,b)=>{const y=keel(u)+(WTf(u)+.05-keel(u))*b;const w=y<LEf(u)?W(u)*(.38+.62*Math.sin(Math.min(1,(y-keel(u))/(LEf(u)-keel(u)))*P/2)):wallZ(u);return [x,y,(a*2-1)*w];});
    for(const z of [-1,-.33,.33,1])beam(ship,woodD,[x+dx*.03,keel(u)+.05,z*W(u)*.8],[x+dx*.03,WTf(u)+.08,z*W(u)*.95],.07,.06);
    beam(ship,woodD,[x+dx*.04,.2,-W(u)],[x+dx*.04,.2,W(u)],.08,.08);
    for(const s of [-1,1])beam(ship,woodL,[x,keel(u)+.2,s*(wallZ(u)+.02)],[x,WTf(u)+.38,s*(wallZ(u)+.02)],.12,.12);  /* 모서리 기둥 */
  }
  /* 지붕: 낮고 넓은 철갑 + 세로 띠 + 쇠못 */
  const rY=(u,v)=>WTf(u)+.05+.42*Math.pow(Math.max(0,1-v*v),.7)*(1-.35*Math.pow(Math.abs(2*u-1),4));
  sheet(ship,roofM,40,20,(a,b)=>{const u=.03+a*.94,v=b*2-1;return [fx(u),rY(u,v),v*wallZ(u)*1.02];});
  for(const u of [.03,.97])sheet(ship,roofM,16,2,(a,b)=>{const v=a*2-1;return [fx(u),WTf(u)+(rY(u,v)-WTf(u))*b,v*wallZ(u)*1.02];});
  const sp=new T.InstancedMesh(new T.ConeGeometry(.018,.12,5),spikeM,900),o3=new T.Object3D();let n=0;
  for(const v of [-.92,-.7,-.46,-.22,.22,.46,.7,.92]){
    line(ship,rail,Array.from({length:16},(_,i)=>{const u=.04+i/15*.92;return [fx(u),rY(u,v)+.012,v*wallZ(u)*1.02];}),.018);
    for(let i=0;i<46;i++){const u=.05+i*.02;if(Math.abs(u-.36)<.03||Math.abs(u-.6)<.03)continue;o3.position.set(fx(u),rY(u,v)+.06,v*wallZ(u)*1.02);o3.rotation.set(v*.5,0,0);o3.updateMatrix();sp.setMatrixAt(n++,o3.matrix);}}
  sp.count=n;ship.add(sp);
  line(ship,woodD,Array.from({length:16},(_,i)=>{const u=.04+i/15*.92;return [fx(u),rY(u,0)+.02,0];}),.04);  /* 가운데 마루 */
  /* 노: 턱 아래에서 뒤로 비스듬히 */
  for(const s of [-1,1])for(let i=0;i<9;i++){const u=.16+i*.085,x=fx(u),z=s*(W(u)+.12),og=new T.Group();og.position.set(x,LEf(u)-.1,z);og.scale.z=s;ship.add(og);
    strut(og,oarM,[-.1,.12,-.2],[.95,-1.35,.85],.028,.024,6);
    const dir=new T.Vector3(1.05,-1.47,1.05).normalize(),bl=add(og,new T.BoxGeometry(.02,.42,.13),oarM,.95+dir.x*.12,-1.35+dir.y*.12,.85+dir.z*.12);bl.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);
    oars.push({og,s,ph:i*.22});}
  /* 키(고물) */
  beam(ship,woodD,[fx(.98)+.12,1.0,0],[fx(.98)+.22,-.75,0],.1,.07);add(ship,new T.BoxGeometry(.5,.55,.05),wood,fx(.98)+.38,-.45,0).rotation.y=P/2;
  /* 용머리(청동 녹) — 뱃머리 벽 한가운데 */
  const head=tsDragonHead({body:'#23423b',body2:'#4d7466',gold:'#8aa38c',horn:'#3d5f55',mane:'#2f5047',beard:'#56786a',mouth:'#2c1612',tongue:'#55241f',tooth:'#b8b29a',scaleK:.35,shin:12,spec:'#4f665e'});
  head.rotation.y=P;head.scale.setScalar(.78);head.position.set(fx(.02)-.3,.96,0);ship.add(head);
  /* 돛대·돛 */
  const flags=[];
  function mast(u,h,sw,sh,bottom,tilt){const x=fx(u),g=new T.Group();g.position.set(x,0,0);g.rotation.y=tilt;ship.add(g);
    const base=rY(u,0);strut(g,woodD,[0,base-.1,0],[0,h,0],.07,.045,10);
    beam(g,woodD,[0,h-.12,-.45],[0,h-.12,.45],.07,.07);beam(g,woodD,[0,h-.32,-.18],[0,h-.32,.18],.05,.05);
    const top=h-.42,bot=bottom;
    sheet(g,sail,12,24,(a,b)=>{const z=(a-.5)*sw,y=bot+b*(top-bot);return [-.08-.08*Math.sin(a*P)*Math.sin(b*P),y,z];});
    const nb=12;for(let i=0;i<=nb;i++){const y=bot+i/nb*(top-bot);beam(g,bat,[-.1,y,-sw/2-.03],[-.1,y,sw/2+.03],.026,.026);
      line(g,rope,[[-.1,y,sw/2+.03],[-.3,(bot+y)/2,sw/2+.25],[-.6,base+.1,.55]],.006);}
    beam(g,bat,[-.1,top+.03,-sw/2-.06],[-.1,top+.03,sw/2+.06],.05,.05);
    return [x,h,0];}
  const f=mast(.37,6.0,2.0,0,2.0,.08),a=mast(.62,5.3,1.6,0,2.05,.05);
  line(ship,rope,[f,[fx(.0)-.1,2.2,0],[fx(.02)-.1,1.25,0]],.009);line(ship,rope,[a,[fx(1)+.2,2.4,0],[fx(.98)+.1,1.3,0]],.009);line(ship,rope,[f,[(f[0]+a[0])/2,5.4,0],a],.008);
  for(const s of [-1,1]){line(ship,rope,[f,[f[0]+.3,3,s*.7],[f[0]+.6,WTf(.45),s*wallZ(.45)]],.007);line(ship,rope,[a,[a[0]+.3,3,s*.6],[a[0]+.55,WTf(.7),s*wallZ(.7)]],.007);}
  ship.userData.tick=t=>{for(const o of oars){const w=t*1.6+o.ph;o.og.rotation.set(-o.s*.09*Math.cos(w),.22*Math.sin(w),0);}};
  return ship;
}
