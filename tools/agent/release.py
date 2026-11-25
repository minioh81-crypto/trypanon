#!/usr/bin/env python3
"""출시 한 번에: 버전 올림 → 번역 사전 → 스모크 테스트 → index.html 빌드 → CHANGELOG → 커밋 → 푸시(main + gh-pages).

사용법(저장소 맨 위에서):
  python3 tools/agent/release.py 383 "커밋 제목" changelog.md [--no-push] [--agent "GPT Codex"]

changelog.md 는 CHANGELOG에 붙일 한 섹션(예: "## 383 — 제목 (v383)\n- 바뀐 점 ...").
아티팩트용 파일: tools/tests/out/artifact-index.html (Claude 세션에서만 아티팩트에 다시 게시).
"""
import sys,re,subprocess,datetime,os,pathlib,argparse
ROOT=pathlib.Path(__file__).resolve().parents[2];os.chdir(ROOT)
ap=argparse.ArgumentParser();ap.add_argument('ver',type=int);ap.add_argument('title');ap.add_argument('changelog')
ap.add_argument('--no-push',action='store_true');ap.add_argument('--agent',default='');a=ap.parse_args()
V=a.ver;cl=open(a.changelog).read()
p='src/trypanon.html';s=open(p).read();old=int(re.search(r'const GVER=(\d+)',s).group(1))
if V<old:sys.exit(f'버전 {V} 이 현재 {old} 보다 작아요')
if old!=V:
    s=s.replace('const GVER=%d'%old,'const GVER=%d'%V);s=re.sub(r'게임 버전 v%d · \d{4}-\d\d-\d\d'%old,'게임 버전 v%d · %s'%(V,datetime.date.today().isoformat()),s);open(p,'w').write(s)
def run(c):return subprocess.run(c,shell=True,capture_output=True,text=True)
r=run('python3 tools/i18n/build.py');print('i18n',(r.stdout+r.stderr)[-200:])
r=run('timeout 600 python3 tools/tests/smoke.py');out=r.stdout[-400:];print(out)
if out.count('errors none')<2:sys.exit('스모크 테스트 실패\n'+r.stderr[-800:])
print(run('python3 tools/build-index.py src/trypanon.html index.html').stdout)
if '(v%d)'%V not in open('CHANGELOG.md').read():open('CHANGELOG.md','a').write('\n'+cl.strip()+'\n')
msg='v%d: %s'%(V,a.title)+(('\n\nCo-Authored-By: '+a.agent) if a.agent else '')
open('/tmp/_relmsg.txt','w').write(msg)
r=run('git add -A && git -c user.name=minioh81-crypto -c user.email=minioh81@gmail.com commit -q -F /tmp/_relmsg.txt');print(r.stdout,r.stderr[-300:])
if not a.no_push:
    r=run('git push -q origin main && git push -q origin main:gh-pages');print(r.stdout,r.stderr[-300:])
print(run('git log --oneline -1').stdout)
o=ROOT/'tools'/'tests'/'out';o.mkdir(parents=True,exist_ok=True);s=open(p).read()
(o/'artifact-index.html').write_text('<!DOCTYPE html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>트리파논</title></head><body>\n'+s+'\n</body></html>\n')
