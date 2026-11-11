# TRYPANON (트리파논) — 작업 안내

모바일 방치형 시추 게임. 한 파일짜리 HTML 게임이고, GitHub Pages(gh-pages 브랜치)로 배포한다.
대화는 한국어로, 짧고 쉽게. 결과 화면은 스크린샷으로 보여 준다.

## 파일 구조
- `src/trypanon.html` — **게임 원본(여기를 고친다)**. `<style>` + 마크업 + `<script>` 한 덩어리(doctype/head 없음).
- `index.html` — 배포용. 원본에서 만든다: `python3 tools/build-index.py src/trypanon.html index.html` (직접 고치지 않는다).
- `tools/i18n/` — 영어·일본어 번역. `dict.tsv`(한국어\t영어\t일본어, `{}` = 숫자/이름 자리), `tr1~5.tsv`, `frags.json`, `build.py`.
- `tools/tests/` — Playwright 테스트(`smoke.py`, `endings.py`, `perf.py`), 결과는 `tools/tests/out/`(git 제외).
- `tools/balance-*.js`, `hard*.json`, `normal*.json` — 밸런스 시뮬레이터(`node tools/balance-hard.js '{"slow":1}'`, 평균은 `balance-avg.js`).
- `tools/vendor/three.min.js` — three.js r128 오프라인 사본(테스트용; 게임은 cdnjs에서 불러옴).
- `CHANGELOG.md` — 버전별 변경 기록(한국어).

## 고칠 때 규칙
- 작업 전 `git pull` (클라우드 세션과 노트북이 같은 저장소를 고친다).
- 새 한국어 화면 문구를 넣으면 `tools/i18n/dict.tsv`에 줄을 추가하고 `python3 tools/i18n/build.py`를 실행한다(원본 안의 번역 사전을 다시 만든다).
- 버전을 올릴 때 두 곳을 같이 바꾼다: 화면 문구 `게임 버전 vNNN · YYYY-MM-DD` 와 `const GVER=NNN`.
- 밸런스를 바꾸면 시뮬레이터나 게임 함수로 수치를 확인하고, 결과를 CHANGELOG에 남긴다.

## 출시 순서
1. 테스트: `python3 tools/tests/smoke.py` (보통·하드, 오류 0이어야 함). 그림을 바꿨으면 해당 화면 스크린샷 확인.
2. `python3 tools/build-index.py src/trypanon.html index.html`
3. `CHANGELOG.md`에 `## 번호 — 제목 (vNNN)` 섹션 추가.
4. 커밋 — 작성자 `minioh81-crypto <minioh81@gmail.com>`:
   `git -c user.name=minioh81-crypto -c user.email=minioh81@gmail.com commit -m "vNNN: ..."`
5. `git push origin main && git push origin main:gh-pages`
6. (claude.ai 세션만) 아티팩트 https://claude.ai/artifact/BycMex7TzF2SLMuDvvPWBi 도 같은 원본으로 다시 게시.

## 보안
- GitHub 비밀번호·토큰은 채팅에 붙여 넣지 않는다. 로그인은 브라우저/Git Credential Manager로.
