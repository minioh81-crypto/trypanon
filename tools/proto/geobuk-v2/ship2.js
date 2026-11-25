function tsShipPro(){
  const T=THREE,ship=new T.Group();ship.name='geobukseon';
  const random = i => (Math.sin(i*127.1+3.7)*43758.5453%1+1)%1;
  function texture(key,w,h,draw){
    const map=s3Tex(key,w,h,(g,w,h)=>{
      draw(g,w,h);
    });
    
    return map;
  }
  const grain=texture('tsTurtleWood',768,256,(g,w,h)=>{
    for(let r=0;r<12;r++){
      const y=r*h/12, tone=39+random(r+11)*16;
      g.fillStyle=`hsl(31,34%,${tone}%)`;g.fillRect(0,y,w,h/12);
      g.fillStyle='#3d2e29';g.fillRect(0,y,w,1.8);
      g.fillStyle='#a58965';g.fillRect(0,y+2,w,.8);
      for(let x=(r%3)*72;x<w;x+=232){g.fillStyle='#513728';g.fillRect(x,y+2,1,h/12-2);}
    }
    for(let i=0;i<2130;i++){
      const x=random(i)*w,y=random(i+2411)*h;
      g.fillStyle=i%3?'rgba(44,29,23,.13)':'rgba(224,194,142,.18)';
      g.fillRect(x,y,4+random(i+89)*24,.5+random(i+22)*.8);
    }
  });
  const iron=texture('tsTurtleRoof',440,224,(g,w,h)=>{
    g.fillStyle='#66757a';g.fillRect(0,0,w,h);
    for(let row=-1;row<10;row++)for(let col=-1;col<16;col++){
      const x=col*33+(row%2)*16.5,y=row*26,j=(row+2)*32+col;
      g.beginPath();g.moveTo(x-16,y);g.lineTo(x-9,y-12);g.lineTo(x+9,y-12);g.lineTo(x+16,y);g.lineTo(x+9,y+12);g.lineTo(x-9,y+12);g.closePath();
      g.fillStyle=`hsl(195,${10+random(j)*6}%,${36+random(j+57)*8}%)`;g.fill();
      g.strokeStyle='#374952';g.lineWidth=1.7;g.stroke();
      g.fillStyle='#a3a9a1';g.fillRect(x-2,y-4,2.2,2.2);
    }
  });
  const textile=texture('tsTurtleSail',256,512,(g,w,h)=>{
    g.fillStyle='#ded2af';g.fillRect(0,0,w,h);
    for(let y=0;y<h;y+=h/9){
      const v=g.createLinearGradient(0,y,0,y+h/9);
      v.addColorStop(0,'#b6a57c');v.addColorStop(.23,'#e9dfc0');v.addColorStop(.69,'#dcd0ab');v.addColorStop(1,'#b9a67f');
      g.fillStyle=v;g.fillRect(0,y,w,h/9);
      g.fillStyle='#917a56';g.fillRect(0,y,w,1.25);
    }
    for(let x=23;x<w;x+=54){g.fillStyle='rgba(103,85,62,.26)';g.fillRect(x,0,.9,h);}
    for(let i=0;i<1350;i++){g.fillStyle=i%2?'rgba(108,94,65,.08)':'rgba(255,247,222,.17)';g.fillRect(random(i)*w,random(i+1800)*h,3+random(i+52)*5,.8);}
  });
  function surface(color,map=null,shininess=20,side=T.FrontSide){
    return L3M(color,{map,shininess,specular:'#3a3026',side});
  }
  iron.wrapS=iron.wrapT=T.RepeatWrapping;iron.repeat.set(7,2.2);
  const timber=surface('#b07a48',grain,10,T.DoubleSide);
  const rail=surface('#5a3a22',null,14);
  const deep=surface('#2e2018',null,10);
  const deck=surface('#6d7980',iron,30,T.DoubleSide);
  const metal=surface('#5d6468',null,60);
  const rope=surface('#c9b38a',null,6);
  const cloth=surface('#f2e8cf',textile,6,T.DoubleSide);
  const jade=surface('#2f6f66',null,24);
  const ridge=surface('#c79b45',null,40);
  const dark=surface('#1a1512',null,15);
  const tooth=surface('#efe6cc',null,24);
  const amber=surface('#e8b84a',null,35);
  const red=surface('#a8322a',null,18),blue=surface('#2f5d8a',null,18),gold=surface('#d9a640',null,55);
  function add(p, geo, material, x=0, y=0, z=0) {
    const o=new T.Mesh(geo,material);o.position.set(x,y,z);p.add(o);return o;
  }
  function orb(p,mat,x,y,z,a,b,c) {
    const o=add(p,new T.SphereGeometry(1,20,14),mat,x,y,z);o.scale.set(a,b,c);return o;
  }
  function strut(p,mat,start,end,r1,r2=r1,count=8) {
    const from=new T.Vector3(...start),to=new T.Vector3(...end),d=to.clone().sub(from),mid=from.clone().addScaledVector(d,.5);
    const o=add(p,new T.CylinderGeometry(r2,r1,d.length(),count),mat,mid.x,mid.y,mid.z);
    o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),d.normalize());
    return o;
  }
  function cable(p,mat,points,r=.014) {
    return add(p,new T.TubeGeometry(new T.CatmullRomCurve3(points.map(v=>new T.Vector3(...v))),Math.max(9,points.length*5),r,5,false),mat);
  }
  const length=6.1,oars=[];
  const width=u=>1.28*(.38+.62*Math.pow(Math.max(0,Math.sin(Math.PI*u)),.52))*(1-.19*(u-.5));
  const rim=u=>1.08+.24*Math.pow(Math.abs(u-.51)*1.95,2.6)+.12*(1-u);
  const roofY=(u,v)=>rim(u)+.075+.78*Math.pow(Math.max(0,1-v*v),.8);
  const fx=u=>length*(u-.5);
  function sheet(p,mat,n,m,formula) {
    const positions=[],uv=[],indices=[];
    for(let i=0;i<=n;i++)for(let j=0;j<=m;j++){
      const a=i/n,b=j/m;positions.push(...formula(a,b));uv.push(a,b);
      if(i<n&&j<m){const k=i*(m+1)+j;indices.push(k,k+1,k+m+1,k+1,k+m+2,k+m+1);}
    }
    const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(positions,3));geo.setAttribute('uv',new T.Float32BufferAttribute(uv,2));geo.setIndex(indices);geo.computeVertexNormals();
    return add(p,geo,mat);
  }
  for(const s of [-1,1]){
    sheet(ship,timber,54,18,(u,v)=>{
      const beam=width(u),foot=-.62+.48*Math.pow(Math.abs(u-.5)*2,2.2);
      return [fx(u)+(1-v)*.13*Math.sign(.5-u),foot+(rim(u)-foot)*v,s*(beam*(.30+.70*Math.pow(v,.58)))];
    });
    for(const v of [.34,.57,.76,.945,1.012]){
      const points=Array.from({length:34},(_,i)=>{
        const u=i/33,foot=-.62+.48*Math.pow(Math.abs(u-.5)*2,2.2);
        return [fx(u)+(1-v)*.13*Math.sign(.5-u),foot+(rim(u)-foot)*v,s*(width(u)*(.30+.70*Math.pow(v,.58))+.013)];
      });
      cable(ship,v>.9?rail:deep,points,v>.9?.042:.028);
    }
    for(let i=0;i<15;i++){
      const u=.06+i*.063,x=fx(u),z=width(u)*s;
      strut(ship,rail,[x-.025,rim(u)-.39,z*.98],[x,rim(u)+.039,z*1.006],.032,.03);
      if(i===14)continue;
      const p=u+.030,xp=fx(p),zp=width(p)*s*.984, y=rim(p)-.219;
      const opening=add(ship,new T.CylinderGeometry(.071,.075,.021,14),deep,xp,y,zp);
      opening.rotation.x=Math.PI/2;
      orb(ship,dark,xp,y,zp+s*.018,.049,.045,.014);
    }
    for(let i=0;i<10;i++){
      /* 노: 뱃전 노걸이에서 물로 비스듬히 · 넓적한 노깃 · 젓는 움직임 */
      const u=.14+i*.076,x=fx(u),z=width(u)*s*.93,og=new T.Group();og.position.set(x,.06,z);og.scale.z=s;ship.add(og);
      add(ship,new T.BoxGeometry(.09,.07,.07),rail,x,.06,z);
      strut(og,rail,[0,.28,-.5],[0,-.62,1.55],.034,.027,7);
      const dir=new T.Vector3(0,-.9,2.05).normalize(),bl=add(og,new T.BoxGeometry(.026,.56,.15),timber,0,-.62+dir.y*.18,1.55+dir.z*.18);
      bl.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir);
      oars.push({og,s,ph:i*.18});
    }
  }
  for(const [u,s] of [[0,-1],[1,1]]){
    sheet(ship,timber,9,12,(a,v)=>[fx(u)+s*(.012-.095*(1-v)), -.14+(rim(u)+.14)*v, (a*2-1)*width(u)*(.58+.42*v)]);
    for(const z of [-.44,0,.44])strut(ship,rail,[fx(u)+s*.02,.12,z*.72],[fx(u)+s*.021,rim(u)+.11,z],.038);
  }
  sheet(ship,deck,48,24,(a,b)=>{
    const u=.044+a*.918,v=b*2-1;
    const min=.87+.13*Math.sin(Math.PI*a);
    return [fx(u),roofY(u,v),width(u)*v*min];
  });
  for(const u of [.044,.962])sheet(ship,deck,24,3,(a,b)=>{const v=a*2-1,mn=.87+.13*Math.sin(Math.PI*a),r=rim(u)-.02;return [fx(u),r+(roofY(u,v)-r)*b,width(u)*v*mn*(1-.02*b)];});
  for(const s of [-1,1]){
    cable(ship,rail,Array.from({length:27},(_,i)=>{const u=.044+i/26*.918;return [fx(u),roofY(u,1)+.018,s*width(u)*(.87+.13*Math.sin(i/26*Math.PI))];}),.044);
  }
  const thorn=new T.ConeGeometry(.024,.17,6),spikes=new T.InstancedMesh(thorn,metal,100),point=new T.Object3D();
  let n=0;
  for(let row=0;row<5;row++)for(let col=0;col<20;col++){
    const u=.075+col*.044+(row%2)*.011,v=(row-2)*.41;
    if(Math.abs(fx(u)+.96)<.14||Math.abs(fx(u)-1.24)<.13)continue;
    point.position.set(fx(u),roofY(u,v)+.097,width(u)*v);
    point.rotation.set(v*.39,0,-.07);point.updateMatrix();spikes.setMatrixAt(n++,point.matrix);
  }
  spikes.count=n;ship.add(spikes);
  /* 용머리: 따로 깎은 채색 조각을 뱃머리에 얹는다 */
  const head=tsDragonHead();head.rotation.y=Math.PI;head.scale.setScalar(1.18);head.position.set(-3.42,1.72,0);ship.add(head);
  /* 단청 띠: 뱃전 윗부분에 붉은·푸른·초록 문양 */
  const dc=s3Tex('tsDancheong',512,32,(g,w,h)=>{g.fillStyle='#a8322a';g.fillRect(0,0,w,h);g.fillStyle='#2f5d8a';g.fillRect(0,5,w,h-10);
    for(let x=0;x<w;x+=32){g.fillStyle='#2f7a55';g.beginPath();g.arc(x+16,h/2,9,0,7);g.fill();g.fillStyle='#f2e3b8';g.beginPath();g.arc(x+16,h/2,5,0,7);g.fill();g.fillStyle='#a8322a';g.beginPath();g.arc(x+16,h/2,2.2,0,7);g.fill();
      g.fillStyle='#f2e3b8';g.fillRect(x,6,2,h-12);}g.fillStyle='#e9d9a8';g.fillRect(0,4,w,1.2);g.fillRect(0,h-5,w,1.2);});
  dc.wrapS=T.RepeatWrapping;dc.repeat.set(9,1);
  for(const s of [-1,1])sheet(ship,L3M('#fff',{map:dc,shininess:8,side:T.DoubleSide}),54,2,(u,v)=>{const vv=.84+v*.11,foot=-.62+.48*Math.pow(Math.abs(u-.5)*2,2.2);
    return [fx(u)+(1-vv)*.13*Math.sign(.5-u),foot+(rim(u)-foot)*vv,s*(width(u)*(.30+.70*Math.pow(vv,.58))+.012)];});
  /* 포문마다 검은 총통 */
  for(const s of [-1,1])for(let i=0;i<14;i++){const p=.06+i*.063+.03,c=add(ship,new T.CylinderGeometry(.04,.05,.22,10),dark,fx(p),rim(p)-.219,width(p)*s*.984+s*.06);c.rotation.x=Math.PI/2;}
  function sail(x,w,bottom,top,angle) {
    const mast=new T.Group();mast.position.x=x;mast.rotation.y=angle;ship.add(mast);
    const y=roofY((x/length)+.5,0);
    strut(mast,rail,[0,y,0],[0,top+.48,0],.065,.031,10);
    for(const v of [bottom,top])strut(mast,rail,[-.089,v,-w*.53],[-.089,v,w*.53],.034,.031);
    strut(mast,deep,[0,top+.25,-w*.23],[0,top+.25,w*.23],.025);
    sheet(mast,cloth,30,42,(a,b)=>{
      const z=(a-.5)*w, height=bottom+b*(top-bottom)+.034*Math.sin(a*Math.PI);
      const bulge=(.036+.235*Math.sin(a*Math.PI)*Math.sin(b*Math.PI)+.026*Math.abs(Math.sin(b*9*Math.PI))*Math.sin(Math.PI*a));
      return [-bulge,height,z];
    });
    for(const s of [-1,1]){
      cable(mast,rope,[[0,top+.42,0],[-.10,top+.18,s*w*.23],[-.084,top,s*w*.52]],.012);
      cable(mast,rope,[[-.088,top,s*w*.498],[-.11,(top+bottom)/2,s*w*.506],[-.09,bottom,s*w*.51]],.010);
      strut(mast,rope,[-.09,bottom,s*w*.51],[.29,y-.12,s*.84],.011);
    }
    for(let i=0;i<=14;i++){
      const z=(i/14-.5)*w;
      strut(mast,rope,[-.08,top+.04,z],[-.087,top-.056,z],.012);
    }
    return [x,top+.44,0];
  }
  const fore=sail(-.93,2.33,2.18,5.53,.145);
  const aft=sail(1.26,1.84,2.02,4.89,.105);
  cable(ship,rope,[fore,[-2.12,3.2,-.06],[-2.97,1.38,-.14]],.014);
  cable(ship,rope,[aft,[2.09,3.02,.27],[2.96,1.39,.53]],.014);
  cable(ship,rope,[fore,[.20,5.08,0],aft],.012);
  /* 돛대 꼭대기 깃발(붉은 수기) */
  const flags=[];for(const [m,c] of [[fore,red],[aft,blue]]){const fg=sheet(ship,c,10,4,(a,b)=>[m[0]+a*.9,m[1]+.1-b*.5*(1-a*.6),0]);fg.material=fg.material.clone();fg.material.side=T.DoubleSide;flags.push(fg);}
  ship.userData.tick=t=>{for(const o of oars){const w=t*1.7+o.ph;o.og.rotation.set(o.s*.11*Math.cos(w)*-1,.27*Math.sin(w),0);}
    flags.forEach((fg,k)=>{const p=fg.geometry.attributes.position;for(let i=0;i<p.count;i++){const a=Math.floor(i/5)/10;p.setZ(i,Math.sin(t*5+a*6+k)*.12*a);}p.needsUpdate=true;});};
  return ship;
}
