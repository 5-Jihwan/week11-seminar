# 저장 백엔드

Cloudflare Worker 하나다(관리자 확인을 서버에서 하고, 키는 시크릿). 클라이언트가 워커 경로(/submit·/peers·/control)와 기기 토큰을 쓰므로 다른 백엔드로 바꾸려면 같은 경로를 구현해야 한다.

## Cloudflare Worker

```
cd backend/worker
wrangler kv namespace create W11        # 나온 id를 wrangler.toml에
wrangler secret put ADMIN_PIN           # 네 자리
wrangler secret put ANTHROPIC_API_KEY   # 선택
wrangler deploy                         # https://w11-seminar.<계정>.workers.dev
```

| 요청 | 누가 | 무엇 |
| --- | --- | --- |
| `POST /submit` | 학생 | 제출·초안·투표. 별명만. 초안은 기기당 최신 하나 |
| `GET /rows?stage=model` | 관리자(헤더 `X-Admin-Pin`) | 제출 전부 |
| `POST /control` | 관리자 | 교수님 판정·지목 |
| `GET /control?dev=` | 학생 | 자기 기기 앞으로 온 판정 |
| `POST /ai` | 학생(선택) | 연구질문 한 줄 코멘트. 목록 밖 논문 언급 금지 |
| `GET /rows?stage=all` | 관리자 | 제출·초안을 목록 조회 한 번으로(대시보드 기본) |
| `POST /reset` | 관리자 | 제출·초안·판정 삭제(기기 등록 tok:은 남김). 대시보드 「비우기」가 수업판에서 부른다 |

**무료 요금제 한도(2026-11-12 반영)**: KV는 하루 읽기 100,000 · 쓰기 1,000 · 목록 1,000 · 삭제 1,000(00:00 UTC = 오전 9시 초기화, 넘으면 그 종류 요청이 오류). 그래서 판정은 `verdict:<기기>` 키 읽기(목록 없음), 학생 초안은 최소 90초 간격, 옆 사람 목록은 선행연구 패널이 열려 있을 때만 2분에 한 번, 대시보드는 20초마다 `/rows?stage=all` 한 번, 워커는 /peers 30초·/rows 8초를 isolate 메모리에 캐시한다. 17명 45분 추정: 쓰기 약 600 이하, 목록 약 300~650. 대시보드는 Ji 노트북 하나만 연다(교수님 기기에 따로 열면 목록 조회가 두 배).

**2026-11-09 배포됨**: `https://w11-seminar.safepic.workers.dev` (KV W11, ADMIN_PIN 시크릿 설정, ANTHROPIC_API_KEY 미설정이라 /ai는 503). 주소는 `model/build_canvas.py`의 WORKER 상수에 있고 `--class` 빌드만 SAVE_URL/READ_URL에 심는다(데모·테스트 빌드는 localStorage). PIN 변경은 `wrangler secret put ADMIN_PIN`. 수업 뒤 KV 삭제는 `wrangler kv namespace delete --namespace-id=<wrangler.toml의 id>`. 데모는 `python model/build_canvas.py`(전부·미검수 표시), 수업판은 `python model/build_canvas.py --class`(verified=TRUE가 있으면 그것만. 하나도 없으면 멈추고, `--unverified-ok`를 붙여야 전부 심고 「검수 전」 표시로 나간다. 시연 버튼은 숨김). 선행연구는 `model/studies.js`로 따로 나오므로 Pages에는 canvas.html·dashboard.html·studies.js 세 파일을 같은 폴더에 둔다. 대시보드는 열 때 PIN을 묻고 세션에만 두며 헤더로 보낸다. PIN은 소스에 없다.

기기 토큰: 학생 브라우저가 처음 보낼 때 만든 토큰을 워커가 기기 ID와 함께 기억하고, 이후 같은 토큰만 받는다(남의 제출·초안 덮어쓰기 방지). /peers는 기기 ID를 내보내지 않는다.

수업 뒤: `wrangler kv namespace delete --namespace-id=<id>` (가드레일 5).
