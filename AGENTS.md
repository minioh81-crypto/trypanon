# 트리파논: 코어 버스터 (TRYPANON: CORE BUSTER) — AI 작업 규칙

Claude(CLAUDE.md)와 ChatGPT Codex가 **같이 쓰는 규칙 파일**이다. 규칙을 바꿀 땐 이 파일만 고친다.

모바일 방치형 시추 게임. 한 파일짜리 HTML 게임이고 GitHub Pages(gh-pages 브랜치)로 배포한다.
공개 주소: https://minioh81-crypto.github.io/trypanon/
대화는 한국어로, 짧고 쉽게. 그림·화면을 바꾸면 스크린샷으로 확인하고 보여 준다.

## 파일 구조
- `src/trypanon.html` — **게임 원본(여기만 고친다)**. `<style>` + 마크업 + `<script>` 한 덩어리(약 2만 줄, doctype/head 없음).
- `index.html` — 배포용. 원본에서 만든다(직접 고치지 않음): `python3 tools/build-index.py src/trypanon.html index.html`
- `tools/i18n/` — 영어·일본어 번역. `dict.tsv`(한국어\t영어\t일본어, `{}` = 숫자/이름 자리) → `python3 tools/i18n/build.py`
- `tools/tests/` — Playwright 테스트 `smoke.py`(보통·하드, 오류 0이어야 함), `endings.py`, `perf.py`. 결과는 `tools/tests/out/`(git 제외)
- `tools/agent/release.py` — 출시 한 번에(버전·번역·스모크·빌드·CHANGELOG·커밋·푸시)
- `tools/agent/shots.py` — 화면 스크린샷(tour / inf / tunnel / tunnel-sea / tunnel-open / mj / all)
- `tools/agent/tunnel-sim.js` — 터널 브레이커 밸런스 시뮬레이터
- `tools/balance-*.js`, `hard*.json`, `normal*.json` — 본편 밸런스 시뮬레이터
- `tools/vendor/three.min.js` — three.js r128 오프라인 사본(테스트용; 게임은 cdnjs에서 불러옴)
- `CHANGELOG.md` — 버전별 변경 기록(한국어)

## 준비(처음 한 번)
`pip install playwright && python3 -m playwright install chromium` (스모크·스크린샷용), Node(시뮬레이터용)

## 고칠 때 규칙
1. 작업 전 `git pull` (Claude와 Codex가 같은 저장소를 번갈아 고친다. **동시에 고치지 않는다**).
2. 새 한국어 화면 문구를 넣으면 `tools/i18n/dict.tsv`에 줄을 추가하고 `python3 tools/i18n/build.py`.
3. 버전은 두 곳이 같이 바뀐다: 화면 문구 `게임 버전 vNNN · YYYY-MM-DD` 와 `const GVER=NNN` (release.py가 해 줌). 번호는 CHANGELOG 마지막 번호 + 1.
4. 밸런스를 바꾸면 시뮬레이터나 게임 함수로 수치를 확인하고 CHANGELOG에 남긴다.
5. 그림(SVG·3D)을 바꿨으면 `python3 tools/agent/shots.py ...`로 찍어서 눈으로 확인한다. 페이지 오류 0.
6. 코드 안 주석은 `/* v383 ... */` 처럼 막힌 주석으로(한 줄 안에 `//`를 넣으면 뒤 코드가 주석이 됨 — 실제 사고 있었음).
7. GitHub 비밀번호·토큰은 채팅에 붙여 넣지 않는다. 로그인은 브라우저/Git Credential Manager로.
8. 그림은 직접 그린 SVG·3D로만. 실제 사진이나 사진을 베낀/AI로 바꾼 그림, 큰 base64 이미지는 넣지 않는다(동상·건물 사진에도 저작권이 있음). 사진은 모양 참고만.

## 출시 순서
```
# changelog 한 섹션을 파일로 써 두고
python3 tools/agent/release.py 383 "제목" /tmp/cl.md            # Claude
python3 tools/agent/release.py 383 "제목" /tmp/cl.md --agent "ChatGPT Codex <noreply@openai.com>"   # Codex가 직접 배포할 때
```
release.py: 버전 올림 → 번역 → 스모크(보통·하드 오류 0) → index.html → CHANGELOG 추가(`## 383 — 제목 (v383)`) → 커밋(작성자 minioh81-crypto) → `git push origin main` + `main:gh-pages`.
Claude 세션만: 이어서 아티팩트 https://claude.ai/artifact/BycMex7TzF2SLMuDvvPWBi 도 `tools/tests/out/artifact-index.html`로 다시 게시.

## Claude ↔ Codex 이어 달리기
- **작업 표시판 `NOW.md`:** 시작하자마자 `git pull` → `NOW.md`에 「작업 중: Claude(또는 Codex) · 시작 시각 · 할 일 한 줄」을 적어 커밋·푸시. 끝나면 「비어 있음」으로 되돌리고 「마지막 작업」 줄을 갱신해 커밋·푸시. 다른 쪽 이름이 「작업 중」이면 그 일을 건드리지 말고 사용자에게 먼저 묻는다(사용자가 이미 끝났다고 하면 비워도 됨).
- **커밋은 작게, 자주:** 한 가지 바뀜 = 한 커밋. 메시지 첫 줄은 `vNNN: 한국어 요약` 또는 `대기: 한국어 요약 (Codex)`. 끝나면 반드시 `main`까지 푸시(또는 PR)해서 다음 사람이 받을 수 있게 한다.
- **Codex(ChatGPT)가 작업할 때:** 고치고 → 스모크·스크린샷 확인 → CHANGELOG 맨 끝에 `## 대기 — 제목 (Codex)` 섹션으로 바뀐 점 기록 → PR. 버전 번호와 배포는 하지 않는다(사용자가 급하다고 하면 release.py로 직접 해도 됨).
- **Claude가 이어받을 때:** PR이 합쳐진 뒤 `git pull` → `대기` 섹션 읽기 → shots.py로 확인·다듬기 → 그 섹션을 새 버전 번호로 바꿔 release.py로 출시 + 아티팩트 게시.

## 코드 지도 (src/trypanon.html 안에서 이름으로 검색)
- **공통 상태·저장:** `S`(나라별 저장, localStorage `trypanon-save-kr/jp/cn`), `save()`, `isJP`/`isCN`, `GVER`, `won()`, `fmtD()`, `toast()`, `$()`
- **본편 시추(캔버스):** `drawDrill`, `TIERS`(드릴 단계), `view`('bore' 등), 엔딩 `playStab` 외
- **나라 영웅 이벤트:** `playYi`(이순신), `playKim`(김유신), `playJpGen`, `playCnGen`, `playSup`; 음성 `yiVoice`/`kimVoice`/`jpVoice`/`cnVoice`; 창이 열려 있으면 미루는 `evBlock()`
- **미니게임:** 허브 `ghOpen`/`ghRender`, 드릴 타이밍 `gh.dt`(`dtStart`/`dtStop`), 사천성 마작 `mj*`(`mjPath` 길 찾기, `mjDeal`, `mjTap`, `mjDraw`)
- **세계 투어(타이틀):** `tourHTML`, 그림 `TOURART.kr/jp/cn`, `INFANIM`, `TUART`, `tStart`(숨김 버튼)
- **무한의 땅:** 상태 `SI`, `infOpenWin`, `infRender`, `infTab`(bore/up/dr/map/sk), 단계 `INF_STG`, 드론 `INF_DL`, 지도 `infMapSVG`, 드릴 SVG의 배기 불꽃 `motorF`
- **터널 브레이커:** 상태 `TU`(localStorage `tp-tunnel`), 터널 `TU_T`(km·sea·imm·vf), 재료 `TU_M`, 공장 `TU_F`, 부품 `TU_P`, 진화 `TU_STG`
  - 수치: `tuV`(m/초, 기본 1/60), `tuGain`(원/m), `tuNeed`(구간 자재), `tuFC`/`tuPC`(비용), `tuRun`(시간 진행)
  - 화면: `tuOpenWin`/`tuClose`, `tuRender`(탭 dig/mat/tbm/site), `tuTick`, `tuTap`(톡톡·폭주), `tuCeremony`(개통식 SVG)
  - 3D(three.js r128): `tu3Mount`(카메라 `tgt()`·`tuKey()`), `tuScene`(굴진 현장), `tuOpenScene`(개통 후 차량), `tuImmScene`/`tuImmInside`(침매터널 밖/안, `tuImmPh`), `tuShowScene`(강화 탭 전시)
  - 모델: `tuTBM(stage)`, `tuDump`, `tuExc`, `tuCarrier`, `tuCargo`, `tuWorker(pose,{harness})`, `tuCar(type,color)`, `tuSea`(바다 생물)
  - 재질·도구: `tuTex`(캔버스 텍스처 캐시), `tuRB`(둥근 상자), `tuPaint`(때 묻은 도장), `tuWheel`, `tuHaz`, `tuSoft`
  - 소리: `tuHum`(드릴), `tuSfx`(weld/beep/dump/hyd/truck/horn/clank/tap), 배경음 `SONGS.tun`
- **소리 공통:** `sndInit`, `tone()`, `noise()`, `sfx()`, `SONGS`, 배경음 스케줄러(`want=` 분기)
