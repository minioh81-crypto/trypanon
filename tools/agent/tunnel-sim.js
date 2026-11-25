// 터널 브레이커 밸런스 시뮬레이터(톡톡 없이, 남는 돈으로 부족한 공장 → 커터·추진 잭 순서로 자동 강화). 게임 수치(tuV·tuGain·tuFC·tuPC·tuNeed)를 바꾸면 여기도 같이 맞춘 뒤: node tools/agent/tunnel-sim.js
// 간단 시뮬: 남는 돈을 가장 싼 강화/공장에 계속 쓰며 남산·통영·죽령 완공 시간
const STG=[[0,1],[20,1.4],[55,1.9],[110,2.6],[190,3.6]];
const T=[[1.53,0,0],[.483,1,0],[4.6,0,0],[3.7,1,1],[6.927,1,0]];
const G=[.8,1,1.5,1.25];
let st={money:2000,p:{cut:0,jack:0,conv:0,pump:0},f:{cem:1,agg:1,mix:1,steel:1,boltf:1,wp:0},m:{cement:30,sand:30,gravel:30,concrete:20,rebar:10,hbeam:4,bolt:15,sheet:0,acc:0}};
const OUT={cem:{cement:.12},agg:{sand:.12,gravel:.12},steel:{rebar:.07,hbeam:.03},boltf:{bolt:.11},wp:{sheet:.045,acc:.025}};
let time=0;
for(let i=0;i<T.length;i++){const [km,sea,imm]=T[i],F=1+i,N=Math.ceil(km);let prog=0,sec=0;const t0=time;
 while(sec<N){const PL=st.p.cut+st.p.jack+st.p.conv+st.p.pump;let sm=1;for(const [l,m] of STG)if(PL>=l)sm=m;const g=G[(sec*7+i)%4];
  let v=(1/60)*(1+.05*st.p.cut)*(1+.03*st.p.jack)*sm/(g*(1+i*1.0));if(sea)v*=.6+Math.min(.9,.1*st.p.pump);
  const L=Math.min(1,km-sec);const need=imm?{concrete:160*F*L,rebar:67*F*L,sheet:42*F*L,acc:14*F*L}:Object.assign({concrete:126*F*L*(g==1.25?1.3:1),rebar:63*F*L,hbeam:25*F*L*(g>=1.25?1.5:1),bolt:105*F*L},sea?{sheet:45*F*L,acc:22*F*L}:{});
  const dt=10;for(const k in OUT){const lv=st.f[k];if(!lv)continue;for(const m in OUT[k])st.m[m]+=OUT[k][m]*(1+.25*(lv-1))/60*dt;}
  const mx=Math.min(.15*(1+.25*(st.f.mix-1))/60*dt,st.m.cement,st.m.sand,st.m.gravel);st.m.cement-=mx;st.m.sand-=mx;st.m.gravel-=mx;st.m.concrete+=mx*2;
  const end=Math.min(km*1000,(sec+1)*1000);
  if(prog<end){const d=Math.min(end-prog,v*dt);prog+=d;st.money+=d*120*(1+.08*st.p.conv)*(1+i*.6);}
  else if(Object.keys(need).every(k=>st.m[k]>=need[k])){for(const k in need)st.m[k]-=need[k];sec++;st.money+=1000*120*.4;}else st.money+=.4*v*120*(1+.08*st.p.conv)*(1+i*.6)*dt;
  // 지출: 부족한 자재 공장 우선, 아니면 커터
  const lack=Object.keys(need).filter(k=>st.m[k]<need[k]);const fmap={concrete:['cem','agg','mix'],cement:['cem'],rebar:['steel'],hbeam:['steel'],bolt:['boltf'],sheet:['wp'],acc:['wp']};
  let buy=[];for(const k of lack)buy.push(...fmap[k]);if(!buy.length)buy=['cut','jack'];
  for(const b of buy){const isF=b in st.f;const c=isF?(b=='mix'?650:b=='wp'?2600:500)*Math.pow(1.24,st.f[b])*(1+i*.6):1000*Math.pow(1.26,st.p[b]);if(st.money>=c){st.money-=c;if(isF)st.f[b]++;else st.p[b]++;break;}}
  time+=dt;if(time>3e7)break;}
 console.log(`${i} ${km}km: ${((time-t0)/3600).toFixed(1)}시간 (누적 ${(time/3600).toFixed(1)}시간) 부품Lv=${st.p.cut+st.p.jack}`);}
