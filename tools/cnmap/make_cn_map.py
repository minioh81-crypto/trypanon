# 중국편 지도: 성(省) 경계(china.json) ∩ 실제 국경(Natural Earth 50m, 대만 제외) → 320×560 화면 좌표 SVG 경로
# 투영: 북쪽이 위 · 동경 100° 서쪽(티베트·신장)은 가로 0.45배로 접어 동부를 크게 · 세로는 가로의 1.5배까지 늘려 세로 화면을 채움
import json,math,sys
from shapely.geometry import shape,mapping
from shapely.ops import unary_union
A=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
W,H,M,YT,YB=320,560,6,A.get('yt',78),A.get('yb',548);WF=A.get('wf',.45);LW=A.get('lw',100);VS=A.get('vs',1.5)
G=json.load(open('china.json'));N=json.load(open('ne_50m_admin_0_countries.geojson'))
cn=unary_union([shape(f['geometry']) for f in N['features'] if f['properties']['ADMIN'] in('China','Hong Kong S.A.R.','Macao S.A.R')]).buffer(.02)
C=math.cos(math.radians(35))
def raw(lon,lat):x=(lon-LW)*C*(WF if lon<LW else 1);return x,36-lat
REG={'11':'north','12':'north','13':'north','14':'north','15':'north','21':'ne','22':'ne','23':'ne','31':'east','32':'east','33':'east','34':'east','35':'east','36':'east','37':'east','41':'central','42':'central','43':'central','44':'south','45':'south','46':'south','81':'south','82':'south','50':'sw','51':'sw','52':'sw','53':'sw','54':'sw','61':'nw','62':'nw','63':'nw','64':'nw','65':'nw'}
COL={'north':'#f2c94a','ne':'#6fa0f0','east':'#86c85a','central':'#f2924a','south':'#ee7ab8','sw':'#b48ae8','nw':'#e8b46a'}
ELE={'north':.7,'ne':.6,'east':.5,'central':.6,'south':.6,'sw':1.3,'nw':1.0}
geo=[]
for f in G['features']:
  pid=f['properties']['id']
  if pid not in REG:continue
  g=shape(f['geometry']).buffer(0).intersection(cn)
  if g.is_empty:continue
  geo.append((pid,g))
xs=[];ys=[]
for pid,g in geo:
  for poly in (g.geoms if g.geom_type=='MultiPolygon' else [g]):
    if poly.geom_type!='Polygon':continue
    for lo,la in poly.exterior.coords:x,y=raw(lo,la);xs.append(x);ys.append(y)
X0,X1,Y0,Y1=min(xs),max(xs),min(ys),max(ys);MR=A.get('mr',44);K=(W-M-MR)/(X1-X0);KY=min(K*VS,(YB-YT)/(Y1-Y0));LX=M;TY=A.get('ty',YT)
def P(lon,lat):x,y=raw(lon,lat);return (LX+(x-X0)*K,TY+(y-Y0)*KY)
def area(r):return abs(sum(r[i][0]*r[i-1][1]-r[i-1][0]*r[i][1] for i in range(len(r))))/2
def dp(pts,tol):
  if len(pts)<3:return pts
  a,b=pts[0],pts[-1];dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy) or 1e-9;md,mi=0,0
  for i in range(1,len(pts)-1):
    p=pts[i];d=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L
    if d>md:md,mi=d,i
  if md>tol:return dp(pts[:mi+1],tol)[:-1]+dp(pts[mi:],tol)
  return [a,b]
def ring_d(pr,tol):
  pr=pr[:-1];h=len(pr)//2
  if h<2:return ''
  q=dp(pr[:h+1],tol)[:-1]+dp(pr[h:]+[pr[0]],tol)
  if len(q)<4:return ''
  return 'M'+'L'.join('%.1f,%.1f'%p for p in q[:-1])+'Z'
out=[];tide=[];allp=[]
for pid,g in geo:
  R=REG[pid];ds=[];cx=cy=ca=0
  for poly in (g.geoms if g.geom_type=='MultiPolygon' else [g]):
    if poly.geom_type!='Polygon':continue
    pr=[P(lo,la) for lo,la in poly.exterior.coords];a=area(pr)
    if a<1.2:continue
    d=ring_d(pr,.45)
    if d:
      ds.append(d);cx+=sum(p[0] for p in pr)/len(pr)*a;cy+=sum(p[1] for p in pr)/len(pr)*a;ca+=a
  if ds:out.append({'id':'c'+pid,'reg':R,'d':''.join(ds),'c':[round(cx/ca,1),round(cy/ca,1)] if ca else [0,0],'col':COL[R],'e':ELE[R]})
# 바닷가 물결용: 나라 전체 윤곽(성 경계 없이)
whole=unary_union([g for _,g in geo]).buffer(0)
for poly in (whole.geoms if whole.geom_type=='MultiPolygon' else [whole]):
  pr=[P(lo,la) for lo,la in poly.exterior.coords]
  if area(pr)>14:
    t=ring_d(pr,1.4)
    if t:tide.append(t)
out.sort(key=lambda p:p['e'])
cnp="const CNP=(lon,lat)=>{const C=Math.cos(35*Math.PI/180);let x=(lon-%s)*C*(lon<%s?%s:1),y=36-lat;return [%.3f+(x-(%.5f))*%.4f,%.3f+(y-(%.5f))*%.4f];};"%(LW,LW,WF,LX,X0,K,TY,Y0,KY)
json.dump({'prov':out,'tide':''.join(tide),'cnp':cnp,'K':K,'KY':KY},open('cn_map.json','w'),separators=(',',':'))
print('K',round(K,2),'KY',round(KY,2),'h',round((Y1-Y0)*KY,1),'n',len(out),'bytes',sum(len(p['d']) for p in out))
s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}"><rect width="{W}" height="{H}" fill="#2386cc"/>'+''.join(f'<path d="{p["d"]}" fill="{p["col"]}" stroke="#333" stroke-width=".3"/>' for p in out)
x,y=P(117.1,36.25);s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="red"/></svg>'
open('prev.svg','w').write(s)
