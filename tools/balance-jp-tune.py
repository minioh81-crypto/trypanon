import json,subprocess,sys
T=[2,6,10,14,20,22,26,32,28,28,26,24,20,14,8];tgt=[x*190/300 for x in T]
ALL=["sex:kuki","sex:kuki2","sex:oda","sex:oda2","ship:tekko","sword:fan","sword:teppo","sword:katana"]
o={'fn':'__TUNE','rounds':int(sys.argv[1]) if len(sys.argv)>1 else 8,'tgt':tgt,'all':1,'pre':ALL,'dt':120,'maxH':3000,'al':float(sys.argv[2]),'be':float(sys.argv[3]),'over':int(sys.argv[6]) if len(sys.argv)>6 else 2}
if len(sys.argv)>4:o['init']=json.load(open(sys.argv[4]))
r=subprocess.run(['timeout','2400','python3',__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'balance-jp.py'),'{}',json.dumps(o)],capture_output=True,text=True)
print(r.stdout[-5000:],r.stderr[-1500:])
import re
j=[l for l in r.stdout.splitlines() if l.startswith('{')]
if j:open(sys.argv[5] if len(sys.argv)>5 else 'cur.json','w').write(j[-1])
