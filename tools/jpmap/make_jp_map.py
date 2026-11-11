import json,math,sys
G=json.load(open('japan.geojson'))
TH=math.radians(float(sys.argv[1]) if len(sys.argv)>1 else -35);K=float(sys.argv[2]) if len(sys.argv)>2 else 30
C0=(137.6,36.4);CX,CY=float(sys.argv[3]) if len(sys.argv)>3 else 160,float(sys.argv[4]) if len(sys.argv)>4 else 285
def P(lon,lat):
  bx=(lon-C0[0])*math.cos(math.radians(36))*K;by=(C0[1]-lat)*K
  x=bx*math.cos(TH)-by*math.sin(TH);y=bx*math.sin(TH)+by*math.cos(TH)
  return (x+CX,y+CY)
# insets (in final coords): move Okinawa main islands & Minamitori into empty corners
OKI_T=(62,262);MT_T=(272,478)
ok_c=P(127.8,26.4);OKI=(OKI_T[0]-ok_c[0],OKI_T[1]-ok_c[1])
mt_c=P(153.98,24.28);MT=(MT_T[0]-mt_c[0],MT_T[1]-mt_c[1])
def reg(i):return 'hokkaido' if i==1 else 'tohoku' if i<=7 else 'kanto' if i<=14 else 'chubu' if i<=23 else 'kinki' if i<=30 else 'chugoku' if i<=35 else 'shikoku' if i<=39 else 'kyushu'
COL={'hokkaido':'#b48ae8','tohoku':'#6fa0f0','kanto':'#f0788c','chubu':'#86c85a','kinki':'#f2c94a','chugoku':'#f2924a','shikoku':'#4cc2d6','kyushu':'#ee7ab8'}
ELE={'hokkaido':.9,'tohoku':.8,'kanto':.5,'chubu':1.2,'kinki':.6,'chugoku':.6,'shikoku':.7,'kyushu':.7}
def area(r):return abs(sum(r[i][0]*r[i-1][1]-r[i-1][0]*r[i][1] for i in range(len(r))))/2
def dp(pts,tol):
  if len(pts)<3:return pts
  a,b=pts[0],pts[-1];dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy)
  md,mi=0,0
  for i in range(1,len(pts)-1):
    p=pts[i];d=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L if L>1e-9 else math.hypot(p[0]-a[0],p[1]-a[1])
    if d>md:md,mi=d,i
  if md>tol:return dp(pts[:mi+1],tol)[:-1]+dp(pts[mi:],tol)
  return [a,b]
def ring_d(r,tol):
  n=len(r);k=max(range(n),key=lambda i:math.hypot(r[i][0]-r[0][0],r[i][1]-r[0][1]))
  s=dp(r[:k+1],tol)[:-1]+dp(r[k:]+[r[0]],tol)[:-1]
  return None if len(s)<3 else 'M'+'L'.join('%.1f,%.1f'%(x,y) for x,y in s)+'Z'
out=[];tide=[];allx=[];ally=[]
for f in G['features']:
  pid=f['properties']['id'];g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  R=reg(pid);ds=[];cx=cy=ca=0
  for poly in polys:
    ring=poly[0];clon=sum(p[0] for p in ring)/len(ring);clat=sum(p[1] for p in ring)/len(ring);inset=False
    if pid==47:
      if not(126.5<clon<128.6 and clat>25.9):continue
      inset=True
    if pid==46 and clat<29.6:continue
    if pid==32 and clon>131.5 and clat>37.0:continue  # 독도는 넣지 않음
    if pid==13 and clat<34.2:continue
    if pid==1 and clon>145.9:continue   # 지도 밖 동쪽 섬들은 생략
    pr=[P(lo,la) for lo,la in ring]
    if inset:pr=[(OKI_T[0]+(x-ok_c[0])*2.4,OKI_T[1]+(y-ok_c[1])*2.4) for x,y in pr]
    A=area(pr)
    if A<(1.2 if inset else 2.5):continue
    d=ring_d(pr,.45)
    if d:
      ds.append(d)
      if not inset:
        allx+= [p[0] for p in pr];ally+=[p[1] for p in pr]
        cx+=sum(p[0] for p in pr)/len(pr)*A;cy+=sum(p[1] for p in pr)/len(pr)*A;ca+=A
        if A>14:
          t=ring_d(pr,1.4)
          if t:tide.append(t)
  if ds:out.append({'id':'p%d'%pid,'reg':R,'d':''.join(ds),'c':[round(cx/ca,1),round(cy/ca,1)] if ca else [0,0],'col':COL[R],'e':ELE[R]})
json.dump({'prov':out,'tide':''.join(tide),'oki':[round(OKI[0],2),round(OKI[1],2)],'mt':[round(MT[0],2),round(MT[1],2)],'th':math.degrees(TH),'K':K,'C0':C0,'CXY':[CX,CY]},open('jp_map2.json','w'),separators=(',',':'))
print('bbox',min(allx),max(allx),min(ally),max(ally),'size',sum(len(p['d']) for p in out)+len(''.join(tide)))
s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 560" width="640" height="1120"><rect width="320" height="560" fill="#2386cc"/>'+''.join(f'<path d="{p["d"]}" fill="{p["col"]}" stroke="#333" stroke-width=".3"/>' for p in out)
for n,(lo,la) in {'fuji':(138.73,35.36),'kita':(138.24,35.67),'ontake':(137.48,35.89),'haku':(136.77,36.15),'itoi':(137.86,36.94),'daisen':(133.54,35.37),'aso':(131.1,32.88),'saku':(130.66,31.58),'miya':(130.5,30.34),'asahi':(142.85,43.66),'nankai':(136.6,33.0),'trench':(144.2,38.4)}.items():
  x,y=P(lo,la);s+=f'<circle cx="{x}" cy="{y}" r="3" fill="red"/><text x="{x+4}" y="{y}" font-size="8">{n}</text>'
s+=f'<rect x="{OKI_T[0]-40}" y="{OKI_T[1]-40}" width="80" height="70" fill="none" stroke="#fff"/><rect x="{MT_T[0]-40}" y="{MT_T[1]-40}" width="80" height="70" fill="none" stroke="#fff"/></svg>'
open('prev2.svg','w').write(s)
