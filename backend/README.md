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

배포 뒤 `model/canvas_v5.html.tpl`의 `SAVE_URL`과 `model/dashboard.html.tpl`의 `READ_URL`에 워커 주소를 넣고 빌드한다. 데모는 `python model/build_canvas.py`(전부·미검수 표시), 수업판은 `python model/build_canvas.py --class`(verified=TRUE가 있으면 그것만. 하나도 없으면 멈추고, `--unverified-ok`를 붙여야 전부 심고 「검수 전」 표시로 나간다. 시연 버튼은 숨김). 선행연구는 `model/studies.js`로 따로 나오므로 Pages에는 canvas.html·dashboard.html·studies.js 세 파일을 같은 폴더에 둔다. 대시보드는 열 때 PIN을 묻고 세션에만 두며 헤더로 보낸다. PIN은 소스에 없다.

기기 토큰: 학생 브라우저가 처음 보낼 때 만든 토큰을 워커가 기기 ID와 함께 기억하고, 이후 같은 토큰만 받는다(남의 제출·초안 덮어쓰기 방지). /peers는 기기 ID를 내보내지 않는다.

수업 뒤: `wrangler kv namespace delete --namespace-id=<id>` (가드레일 5).
