import json,math,sys
G=json.load(open('japan.geojson'))
A=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
hs=A.get('hs',.5);hx=A.get('hx',140.12);ty=A.get('ty',.74);ex=A.get('ex',.85);W=A.get('W',320);H=A.get('H',560);M=A.get('m',6);YT=A.get('yt',20);YB=A.get('yb',548)
C=math.cos(math.radians(36))
def raw(lon,lat,hk=None):
  if (hk if hk is not None else (lat>41.6 and lon>139.3)):lon=hx+(lon-140.72)*hs;lat=41.78+(lat-41.78)*hs
  x=(lon-137.6)*C;y=36.4-lat
  if lon>140.6:x=3*C+(lon-140.6)*C*ex
  if lat>37.2:y=-.8-(lat-37.2)*ty
  return x,y
def keep(pid,clon,clat):
  if pid==47:return 'oki' if (126.5<clon<128.6 and clat>25.9) else None
  if pid==46 and clat<29.6:return None
  if clon<129.55:return None
  if pid==32 and clon>131.5 and clat>37.0:return None
  if pid==13 and clat<34.2:return None
  if pid==1 and clon>145.9:return None
  return 'main'
xs=[];ys=[]
for f in G['features']:
  pid=f['properties']['id'];g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  for poly in polys:
    r=poly[0];clon=sum(p[0] for p in r)/len(r);clat=sum(p[1] for p in r)/len(r)
    if keep(pid,clon,clat)=='main':
      for lo,la in r:x,y=raw(lo,la,pid==1);xs.append(x);ys.append(y)
X0,X1,Y0,Y1=min(xs),max(xs),min(ys),max(ys)
K=(W-2*M)/(X1-X0);KY=min(K*A.get('vs',1),(YB-YT)/(Y1-Y0))
LX=(W-(X1-X0)*K)/2;TY=YT
def P(lon,lat,hk=None):x,y=raw(lon,lat,hk);return (LX+(x-X0)*K,TY+(y-Y0)*KY)
OKI_T=tuple(A.get('oki',(50,506)));OK_K=A.get('ok',1.9);MT_T=tuple(A.get('mt',(282,508)))
ok_c=P(127.8,26.4)
def reg(i):return 'hokkaido' if i==1 else 'tohoku' if i<=7 else 'kanto' if i<=14 else 'chubu' if i<=23 else 'kinki' if i<=30 else 'chugoku' if i<=35 else 'shikoku' if i<=39 else 'kyushu'
COL={'hokkaido':'#b48ae8','tohoku':'#6fa0f0','kanto':'#f0788c','chubu':'#86c85a','kinki':'#f2c94a','chugoku':'#f2924a','shikoku':'#4cc2d6','kyushu':'#ee7ab8'}
ELE={'hokkaido':.9,'tohoku':.8,'kanto':.5,'chubu':1.2,'kinki':.6,'chugoku':.6,'shikoku':.7,'kyushu':.7}
def area(r):return abs(sum(r[i][0]*r[i-1][1]-r[i-1][0]*r[i][1] for i in range(len(r))))/2
def dp(pts,tol):
  if len(pts)<3:return pts
  a,b=pts[0],pts[-1];dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy);md,mi=0,0
  for i in range(1,len(pts)-1):
    p=pts[i];d=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L if L>1e-9 else math.hypot(p[0]-a[0],p[1]-a[1])
    if d>md:md,mi=d,i
  if md>tol:return dp(pts[:mi+1],tol)[:-1]+dp(pts[mi:],tol)
  return [a,b]
def ring_d(r,tol):
  n=len(r);k=max(range(n),key=lambda i:math.hypot(r[i][0]-r[0][0],r[i][1]-r[0][1]))
  s=dp(r[:k+1],tol)[:-1]+dp(r[k:]+[r[0]],tol)[:-1]
  return None if len(s)<3 else 'M'+'L'.join('%.1f,%.1f'%(x,y) for x,y in s)+'Z'
out=[];tide=[]
for f in G['features']:
  pid=f['properties']['id'];g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  R=reg(pid);ds=[];cx=cy=ca=0
  for poly in polys:
    ring=poly[0];clon=sum(p[0] for p in ring)/len(ring);clat=sum(p[1] for p in ring)/len(ring);kk=keep(pid,clon,clat)
    if not kk:continue
    pr=[P(lo,la,pid==1) for lo,la in ring];inset=kk=='oki'
    if inset:pr=[(OKI_T[0]+(x-ok_c[0])*OK_K,OKI_T[1]+(y-ok_c[1])*OK_K) for x,y in pr]
    a=area(pr)
    if a<(1.2 if inset else 2.5):continue
    d=ring_d(pr,.45)
    if d:
      ds.append(d)
      if not inset:
        cx+=sum(p[0] for p in pr)/len(pr)*a;cy+=sum(p[1] for p in pr)/len(pr)*a;ca+=a
        if a>14:
          t=ring_d(pr,1.4)
          if t:tide.append(t)
  if ds:out.append({'id':'p%d'%pid,'reg':R,'d':''.join(ds),'c':[round(cx/ca,1),round(cy/ca,1)] if ca else [0,0],'col':COL[R],'e':ELE[R]})
out.sort(key=lambda p:p['e'])
jpp=("const JPP=(lon,lat)=>{const C=Math.cos(36*Math.PI/180),K=%.4f;if(lat>41.6&&lon>139.3){lon=%s+(lon-140.72)*%s;lat=41.78+(lat-41.78)*%s;}let x=(lon-137.6)*C,y=36.4-lat;if(lon>140.6)x=3*C+(lon-140.6)*C*%s;if(lat>37.2)y=-.8-(lat-37.2)*%s;return [%.3f+(x-(%.5f))*K,%.3f+(y-(%.5f))*%.4f];};"%(K,hx,hs,hs,ex,ty,LX,X0,TY,Y0,KY))
json.dump({'prov':out,'tide':''.join(tide),'jpp':jpp,'oki':[OKI_T[0],OKI_T[1],OK_K],'mt':list(MT_T),'K':K},open('jp_map3.json','w'),separators=(',',':'))
print('K',round(K,2),'LX',round(LX,1),'KY',round(KY,2),'bbox h',round((Y1-Y0)*KY,1),'w',round((X1-X0)*K,1))
s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#2386cc"/>'+''.join(f'<path d="{p["d"]}" fill="{p["col"]}" stroke="#333" stroke-width=".3"/>' for p in out)
mt=P(153.98,24.28)
s+=f'<circle cx="{MT_T[0]}" cy="{MT_T[1]}" r="3" fill="#ff0"/></svg>'
open('prev3.svg','w').write(s)
