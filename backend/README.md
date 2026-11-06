# 저장 백엔드

둘 중 하나를 쓴다. 기본은 Cloudflare Worker(관리자 확인을 서버에서 하고, 키는 시크릿).

## Cloudflare Worker (기본)

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

배포 뒤 `model/canvas_v5.html.tpl`의 `SAVE_URL`과 `model/dashboard.html.tpl`의 `READ_URL`에 워커 주소를 넣고 `python model/build_canvas.py`. 대시보드는 같은 PIN을 헤더로 보낸다.

수업 뒤: `wrangler kv namespace delete --namespace-id=<id>` (가드레일 5).

## Google Apps Script (대안)

`apps-script.gs`를 시트에 붙여 웹앱으로 배포. 인증 없음, 수업 1회용.
