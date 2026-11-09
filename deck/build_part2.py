# -*- coding: utf-8 -*-
"""2부 발표덱 빌드: deck/fig_part2/uris.json(실제 화면 JPEG data URI, data/raw/tmp/deck_shots.py가 만든다)을 심어 deck/week11_part2.html.
실행: python deck/build_part2.py"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
IMG = json.load(open(os.path.join(H, "fig_part2", "uris.json")))

HTML = r"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>2부 연구모형 캔버스</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--paper:#fff;--stage:#e9edf2;--ink:#15203a;--sub:#5a6577;--line:#e2e6ec;--navy:#072A60;--navyt:#e9eef6;--green:#8DC63F;--greend:#4F7F1C;--greent:#f0f7e6;--orange:#D9640F;--gray:#9aa2ae}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--stage);font-family:Pretendard,"Noto Sans KR",system-ui,-apple-system,sans-serif;color:var(--ink)}
#stage{position:fixed;inset:0;display:grid;place-items:center}
.slide{width:1280px;height:720px;background:var(--paper);position:absolute;display:none;overflow:hidden;transform-origin:center}
.slide.on{display:block}
.hd{position:absolute;left:72px;top:52px;right:72px}.hd::before{content:"";display:block;width:32px;height:3px;background:var(--green);margin-bottom:14px}
.hd h2{margin:0;font-size:28px;font-weight:700;color:var(--navy);letter-spacing:-.01em}.hd .s{margin:6px 0 0;font-size:16px;color:var(--sub)}
.bd{position:absolute;left:72px;right:72px;top:146px;bottom:70px;display:flex;align-items:center;justify-content:center}.in{width:100%;max-width:1136px}
.cap{position:absolute;left:72px;right:140px;bottom:28px;font-size:13px;color:var(--sub);line-height:1.5}
.pg{position:absolute;right:40px;bottom:26px;font-size:13px;color:var(--gray);font-family:"IBM Plex Mono",monospace}
.notes{display:none}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:40vh;overflow:auto;background:rgba(21,32,58,.96);color:#fff;padding:18px 28px;font-size:17px;line-height:1.7;display:none;z-index:5}#notes.on{display:block}
p,li{font-size:18.5px;line-height:1.65;margin:0}ul,ol{margin:0;padding-left:22px}li+li{margin-top:8px}
.num{font-family:"IBM Plex Mono",monospace}.k{font-size:14.5px;color:var(--sub);margin-bottom:6px}
.shot{display:block;width:100%;border:1px solid var(--line);border-radius:6px;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center}
.cover{background:#000;color:#fff}.cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9}.cover .veil{position:absolute;inset:0;background:rgba(7,42,96,.72)}
.cover .c{position:absolute;left:88px;right:88px;top:210px}.cover .c::before{content:"";display:block;width:40px;height:4px;background:var(--green);margin-bottom:26px}
.cover h1{margin:0;font-size:48px;line-height:1.3;font-weight:700}.cover .sub{margin:18px 0 0;font-size:20px;opacity:.9}.cover .meta{position:absolute;left:88px;bottom:60px;font-size:15.5px;opacity:.85;line-height:1.7}.cover .src{position:absolute;right:40px;bottom:30px;font-size:12px;opacity:.65}
.step{border-top:2px solid var(--navy);padding-top:10px}.step .n{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--sub)}.step h3{margin:2px 0 6px;font-size:20px;color:var(--navy)}.step p{font-size:16px}
table{border-collapse:collapse;width:100%;font-size:17px}th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:14px;color:var(--sub);font-weight:600}td.r,th.r{text-align:right;white-space:nowrap}
.role{display:grid;grid-template-columns:140px 1fr;gap:10px 16px;align-items:center;font-size:16.5px}
.node{display:inline-block;padding:8px 12px;border-radius:8px;border:1.5px solid var(--navy);background:#fff;font-weight:600;font-size:14px;text-align:center;min-width:130px}
.node.dv{background:var(--navyt);border-width:2.5px}.node.mv{border-style:dashed;border-color:#8aa4cf}.node.zv{border-style:dotted;border-color:#94a3b8;color:#475569}.node.cv{border-color:#cbd5e1;color:#64748b;background:#f8fafc}
.stat{display:grid;grid-template-columns:repeat(3,1fr);gap:36px;text-align:center}.stat .v{font-family:"IBM Plex Mono",monospace;font-size:84px;line-height:1;color:var(--navy);font-weight:500}.stat .l{font-size:17px;color:var(--sub);margin-top:14px;line-height:1.5}
.cell{border-collapse:collapse;font-size:15px;width:100%}.cell th,.cell td{border:1px solid var(--line);padding:10px 8px;text-align:center}.cell th{background:#f6f7f9;color:var(--sub);font-weight:600}.cell td b{color:var(--navy)}
.callout{position:absolute;background:var(--navy);color:#fff;font-size:12.5px;font-weight:600;padding:3px 9px;border-radius:4px;line-height:1.4}
.figwrap{position:relative}
#help{position:fixed;right:14px;top:10px;font-size:12px;color:#7b8494;z-index:6}
</style></head><body>
<div id="stage">

<section class="slide cover">
 <img src="{{dash_net}}" alt=""><div class="veil"></div>
 <div class="c"><h1>연구모형 캔버스</h1><p class="sub">국내 조사 8종의 문항으로 각자 사회자본을 정의하고, 선행연구 7,690편과 견준다</p></div>
 <div class="meta">사회자본과 공공정책 · 11주차 발제 2부 · 2026-11-13<br>발제 오지환 · 성균관대학교</div>
 <div class="src">배경: 관리자 대시보드의 선행연구 유사도 연결망(시연 자료 17명)</div>
 <aside class="notes">1부에서 다섯 번 고르셨습니다. 측정을 바꾸자 결론이 바뀌었습니다. 이제 같은 일을 여러분 손으로 합니다. 자료 하나를 골라, 사회자본이 무엇인지 적고, 문항으로 잽니다. 35분이면 끝납니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>지정문헌 다섯 편의 사회자본 측정</h2><p class="s">같은 개념, 자료마다 다른 조작적 정의</p></div>
 <div class="bd"><div class="in">
 <table><tr><th>논문</th><th>자료</th><th>사회자본의 측정</th><th>모형에서의 자리</th></tr>
 <tr><td>Krishna (2007)</td><td>인도 라자스탄 61개 마을, 7년 패널</td><td>집합행동 성향 6문항 지수 0–100</td><td>종속</td></tr>
 <tr><td>Freitag (2006)</td><td>스위스 24개 칸톤</td><td>결사체 참여 4문항 주성분, 칸톤 평균</td><td>종속</td></tr>
 <tr><td>Lowndes &amp; Wilson (2001)</td><td>없음(이론)</td><td>Putnam의 혼합 정의, 측정 없음</td><td>이론 틀</td></tr>
 <tr><td>Mettler (2002)</td><td>미국 G.I. Bill 수혜자 회고 설문(1998)</td><td>단체 가입 수 + 정치활동 6종</td><td>종속</td></tr>
 <tr><td>Kumlin &amp; Rothstein (2005)</td><td>스웨덴 횡단면 설문</td><td>대인신뢰 0–10 단일 문항</td><td>종속</td></tr></table>
 <p style="margin-top:26px;font-size:17.5px;color:var(--sub)">측정 열의 네 가지(지수·주성분·가입 수·단일 문항)는 모두 자료가 가진 문항에서 나왔다. 오늘 각자가 고를 자료도 같은 제약을 준다.</p>
 </div></div>
 <div class="cap">원문 대조 docs/PAPERS.md. 1부 투표 분포는 당일 1부 결과 화면으로 대체.</div>
 <aside class="notes">셋째 열만 보십시오. 지수, 주성분, 가입 수, 단일 문항. 전부 사회자본이라고 불렀습니다. 넷째 열은 전부 종속입니다. 오늘 여러분도 종속변수부터 정합니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>캔버스 작업 순서</h2><p class="s">자료 선택, 개념화, 조작화, 제출. 화면이 이 순서로 열린다</p></div>
 <div class="bd"><div class="in two" style="grid-template-columns:1fr 1.25fr">
  <div>
   <div class="step"><div class="n">1</div><h3>자료</h3><p>조사 하나를 고른다. 한 모형에는 같은 응답자에게 물은 문항만 들어간다</p></div>
   <div class="step" style="margin-top:16px;border-top-color:var(--green)"><div class="n">2</div><h3>개념화</h3><p>사회자본이 무엇인지 한 문장. 차원(인지적·구조적·둘 다)과 수준(개인·공동체)</p></div>
   <div class="step" style="margin-top:16px"><div class="n">3</div><h3>조작화</h3><p>문항을 끌어 변수를 만들고 역할을 고른다. 변수 둘을 차례로 누르면 경로</p></div>
   <div class="step" style="margin-top:16px"><div class="n">4</div><h3>제출</h3><p>별명으로 제출. 프로젝터에 모이고, 유사한 선행연구와 교수님 판정이 돌아온다</p></div>
  </div>
  <div><img class="shot" src="{{concept}}" alt="개념화 단계 화면"><p class="k" style="margin-top:8px">2단계 화면. 정의 문장을 먼저 적고 차원과 수준을 고른 뒤에야 문항 목록이 열린다</p></div>
 </div></div>
 <aside class="notes">순서가 중요합니다. 문항을 먼저 보면 문항이 개념을 정합니다. 그래서 2단계에서 정의부터 적게 해 두었습니다. 그 정의와 3단계의 문항이 어긋나면 노란 경고가 뜹니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>접속 주소와 규칙</h2><p class="s">노트북 권장. 폰은 끌기 대신 ＋ 버튼</p></div>
 <div class="bd"><div class="in two">
  <div><div class="k">주소</div><p style="font-size:25px;font-weight:600;color:var(--navy);word-break:break-all;line-height:1.4">5-jihwan.github.io/week11-seminar/<br>model/canvas.html</p>
   <div class="k" style="margin-top:26px">자료 8종, 전체 문항 5,636</div>
   <table style="font-size:15px"><tr><td>한국복지패널 20차</td><td class="r num">730</td><td>사회통합실태조사 2023</td><td class="r num">197</td></tr>
   <tr><td>한국종합사회조사 2003–2025</td><td class="r num">3,345</td><td>청년삶실태조사 2024</td><td class="r num">447</td></tr>
   <tr><td>사회조사 2023</td><td class="r num">232</td><td>노인실태조사 2023</td><td class="r num">434</td></tr>
   <tr><td>가계금융복지조사 2023</td><td class="r num">85</td><td>지역사회건강조사 2023</td><td class="r num">166</td></tr></table></div>
  <div><div class="k">규칙</div><ul style="font-size:17.5px">
   <li>이름 대신 별명. 오늘 선택은 이 수업 안에서만 쓰고 끝나면 지운다</li>
   <li>선행연구 7,690편은 규칙과 AI가 코딩한 것으로 사람 검수 전. 화면에도 그렇게 표시된다</li>
   <li>유사도 점수는 임의 가중치이며 추정치가 아니다</li>
   <li>새로고침해도 작업은 남는다. 자료를 바꾸면 모형은 지워진다(경고 뒤)</li></ul></div>
 </div></div>
 <div class="cap">기본 화면에는 선행연구에서 자주 쓰는 요약 문항 108개. 전체 문항은 「전체」 버튼과 검색.</div>
 <aside class="notes">주소를 치시고 별명을 넣으십시오. 두 가지만 말씀드립니다. 이름은 안 씁니다, 끝나면 지웁니다. 그리고 뒤에 나올 선행연구 7천 편은 AI가 코딩한 것이고 아직 사람이 검수하지 않았습니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>변수 역할과 경로 규칙</h2><p class="s">문항에는 역할이 미리 붙어 있지 않다. 놓을 때 고른다</p></div>
 <div class="bd"><div class="in two" style="grid-template-columns:1fr 1.35fr">
  <div class="role">
   <span class="node dv">DV 종속변수</span><span>설명하려는 결과. 하나만. 문항을 여럿 묶으면 지수</span>
   <span class="node">IV 독립변수</span><span>원인으로 보는 것. 둘 이상 가능</span>
   <span class="node mv">MV 매개변수</span><span>원인과 결과 사이. 들어오는 경로와 나가는 경로가 둘 다 필요</span>
   <span class="node zv">ZV 조절변수</span><span>집단에 따라 효과가 다른지. 변수가 아니라 경로 위에 붙인다</span>
   <span class="node cv">CV 통제변수</span><span>영향을 빼고 보려는 것. 경로 없이 둔다</span>
  </div>
  <div><img class="shot" src="{{canvas_sim}}" alt="캔버스 화면"><p class="k" style="margin-top:8px">공공서비스 접촉 경험 → 내 사회자본(일반신뢰 + 호혜), 성별을 경로 위 조절변수로. 3초 멈추면 유사한 선행연구 패널이 뜬다</p></div>
 </div></div>
 <div class="cap">종속에서 나가는 화살표는 오류(역인과). 독립끼리 이으면 경고. 가설 문장은 경로에서 자동으로 만들어지고 고쳐 쓸 수 있다.</div>
 <aside class="notes">역할은 다섯입니다. 종속은 하나만 둡니다. 조절은 변수에 잇는 게 아니라 화살표 위에 붙입니다. 그래야 "이 관계가 집단에 따라 다른가"라는 뜻이 됩니다. 종속에서 밖으로 나가는 화살표를 그으면 빨간 오류가 뜹니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>작업 10분 안내</h2><p class="s">노트북 둘째 화면용. 프로젝터는 대시보드</p></div>
 <div class="bd"><div class="in two" style="grid-template-columns:1fr 1.2fr">
  <div><ol style="font-size:19px;line-height:1.8">
   <li>자료 하나, 사회자본 정의 한 문장, 차원과 수준</li>
   <li>종속변수 하나(문항 1개 이상 묶기)와 원인 하나를 잇는다</li>
   <li>별명 확인 뒤 제출. 고치면 다시 제출(최신 것만 센다)</li></ol>
   <div class="k" style="margin-top:26px">막히면</div><ul style="font-size:16.5px">
   <li>끌기가 안 되면 문항 카드의 ＋ 버튼</li>
   <li>문항이 안 보이면 검색창 또는 「전체」</li>
   <li>오른쪽 「정의」 탭에 개념화와 조작화의 간격이 뜬다</li></ul></div>
  <div><img class="shot" src="{{canvas_def}}" alt="정의 탭"><p class="k" style="margin-top:8px">「정의」 탭. 위가 말로 정한 정의, 아래가 문항으로 잰 정의. 둘이 어긋나면 그 사이에 경고가 끼어든다</p></div>
 </div></div>
 <div class="cap">5분 시점 안내: 종속 하나와 원인 하나만 이어도 제출된다. 8분 시점 안내: 오른쪽 정의 탭.</div>
 <aside class="notes">10분 드립니다. 세 가지만 하시면 됩니다. 돌아다니겠습니다. 막히면 손 드십시오.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>원인 축과 종속 차원의 분류 틀</h2><p class="s">Hooghe &amp; Stolle (2003)의 사회 중심·제도 중심에 개인 자원·지역 맥락을 더하고, Uphoff (2000)의 인지적·구조적과 교차</p></div>
 <div class="bd"><div class="in two" style="grid-template-columns:1.3fr 1fr">
  <table class="cell"><tr><th style="width:120px"></th><th>인지적<br><span style="font-weight:400">신뢰·규범</span></th><th>구조적<br><span style="font-weight:400">연결망·참여</span></th><th>인지적 + 구조적</th></tr>
  <tr><th>제도 중심</th><td><b>Kumlin &amp; Rothstein</b></td><td><b>Freitag · Mettler</b></td><td><b>Lowndes &amp; Wilson</b></td></tr>
  <tr><th>사회 중심</th><td>·</td><td>·</td><td><b>Krishna</b></td></tr>
  <tr><th>개인 자원</th><td>·</td><td>·</td><td>·</td></tr>
  <tr><th>지역 맥락</th><td>·</td><td>·</td><td><b>Krishna</b></td></tr></table>
  <div><img class="shot" src="{{dash_grid}}" alt="대시보드 격자"><p class="k" style="margin-top:8px">대시보드의 종속 구성 × 독립 묶음 격자(시연 자료). 빈 칸은 오늘 아무도 안 간 조합</p></div>
 </div></div>
 <div class="cap">다섯 편은 모두 제도 중심 줄. 학생 모형의 칸은 대시보드 「분류 틀의 칸」 막대. 칸별 선행연구 편수는 캔버스 「선행연구」 탭(규칙·AI 코딩, 검수 전).</div>
 <aside class="notes">세로축은 원인이 어디서 오느냐, 가로축은 사회자본을 무엇으로 쟀느냐입니다. 다섯 편은 전부 윗줄입니다. 여러분은 어디 계십니까. 대시보드를 보겠습니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>유사도 점수와 교수님 판정</h2><p class="s">spotlight 3명 — 같은 자료에서 다른 정의, 개념과 측정의 어긋남, 조절이나 매개</p></div>
 <div class="bd"><div class="in two" style="grid-template-columns:1fr 1.3fr">
  <div><div class="k">유사도 = 가중치 합 ÷ 11, 가중치는 임의</div>
   <table style="font-size:15.5px"><tr><td>종속변수 구성 요소 겹침(자카드)</td><td class="r num">× 3</td></tr><tr><td>같은 자료</td><td class="r num">2</td></tr><tr><td>같은 원인 축</td><td class="r num">1.5</td></tr><tr><td>같은 단위 · 매개 있음 · 같은 차원 · 사회자본이 종속</td><td class="r num">각 1</td></tr><tr><td>국내 연구</td><td class="r num">0.5</td></tr></table>
   <div class="k" style="margin-top:22px">판정 네 가지</div>
   <table style="font-size:15.5px"><tr><td>개념·측정 일치</td><td>말한 차원과 묶은 문항이 같다</td></tr><tr><td>개념·측정 불일치</td><td>「어긋남」 표시. 고쳐 다시 내면 표가 바뀐다</td></tr><tr><td>인과 방향 재검토</td><td>연구질문이 "영향", 또는 종속에서 나가는 화살표</td></tr><tr><td>선행연구 공백</td><td>선행연구 15편 미만 칸</td></tr></table></div>
  <div><img class="shot" src="{{dash_spot}}" alt="spotlight 화면"><p class="k" style="margin-top:8px">행을 누르면 열리는 spotlight. 위 판정 버튼을 누르면 그 학생 화면에 바로 뜬다</p></div>
 </div></div>
 <div class="cap">선행연구 7,690편(국내 2,362 · 해외 5,328), 사회자본이 종속인 연구 1,903편. 출처 KCI·OpenAlex, 코딩 Haiku 5.5, 검수 전.</div>
 <aside class="notes">한 분씩 띄우겠습니다. 왜 이 문항을 묶으셨는지 여쭙고, 가장 비슷한 선행연구를 읽어 드리겠습니다. 그 다음 교수님께 판정을 부탁드립니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>선행연구 유사도 연결망</h2><p class="s">점은 선행연구, 금색은 오늘 제출된 모형</p></div>
 <div class="bd"><div class="in two" style="grid-template-columns:2.3fr 1fr;gap:28px">
  <img class="shot" src="{{dash_net}}" alt="연결망" style="width:100%">
  <ul style="font-size:17px">
   <li>점 하나가 선행연구 한 편. 국내 먼저 최대 1,200편, 테두리는 국내</li>
   <li>선은 구성 요소와 원인 축이 같은 이웃 4편</li>
   <li>금색 점은 제출 모형. 가장 비슷한 4편의 평균 자리에 놓인다</li>
   <li>되감기 슬라이더로 10분 전 분포</li>
   <li>색은 원인 축(제도·사회·지역·개인)</li></ul>
 </div></div>
 <div class="cap">3D 힘 배치, 외부 라이브러리 없음. 시연 자료 17명 기준 화면.</div>
 <aside class="notes">회전을 멈추겠습니다. 점이 선행연구, 금색이 여러분입니다. 슬라이더를 10분 전으로 끌면 여러분이 어디서 출발했는지 보입니다.</aside>
</section>

<section class="slide">
 <div class="hd"><h2>오늘의 결과</h2><p class="s">제출 모형과 선행연구의 분포를 같은 틀에서 본다</p></div>
 <div class="bd"><div class="in">
  <div class="stat"><div><div class="v">5</div><div class="l">지정문헌. 자료가 다른 다섯 가지 조작적 정의, 모두 종속</div></div><div><div class="v">17</div><div class="l">오늘의 모형. 분류 틀의 칸과 빈 칸</div></div><div><div class="v">7,690</div><div class="l">국내 30년, 해외 50년의 양적 선행연구</div></div></div>
  <p style="margin-top:56px;text-align:center;font-size:21px;color:var(--navy)">개념화를 먼저 적게 한 이유: 문항이 정의를 대신 정하지 않도록</p>
 </div></div>
 <div class="cap">수업 뒤 제출 기록은 삭제. 캔버스와 선행연구 목록은 저장소에 공개(github.com/5-Jihwan/week11-seminar).</div>
 <aside class="notes">다섯 편은 자료가 정의를 정했고, 오늘 여러분 화면에서도 그랬습니다. 교수님.</aside>
</section>

<section class="slide" data-ap="1">
 <div class="hd"><h2>캔버스 화면 지도</h2><p class="s">부록. 질문 대응용</p></div>
 <div class="bd"><div class="in figwrap">
  <img class="shot" src="{{canvas_studies}}" alt="캔버스 전체">
  <span class="callout" style="left:12px;top:60px">① 문항 목록 · 검색 · 전체</span>
  <span class="callout" style="left:400px;top:60px">② 캔버스 · 확대 · 자동배치 · PNG</span>
  <span class="callout" style="left:760px;top:60px">③ 오른쪽 패널 · 변수 / 정의 / 선행연구 / 리뷰</span>
  <span class="callout" style="left:400px;bottom:14px">④ 검증 배지 · 유사도 배지</span>
  <span class="callout" style="right:12px;top:14px">⑤ 자료 칩 · 별명 · 제출</span>
 </div></div>
 <aside class="notes"></aside>
</section>

<section class="slide" data-ap="1">
 <div class="hd"><h2>검증 규칙</h2><p class="s">부록. 오류 6, 경고 7, 정보 4</p></div>
 <div class="bd"><div class="in" style="display:grid;grid-template-columns:repeat(3,1fr);gap:30px">
  <div><div class="k" style="color:var(--orange)">오류, 제출 잠김</div><ul style="font-size:16px"><li>종속변수 없음</li><li>독립변수 없음</li><li>문항 없는 변수</li><li>종속에서 나가는 경로(역인과)</li><li>매개에서 독립으로</li><li>조절이 잘못된 경로 위, 조절로 들어오는 화살표</li></ul></div>
  <div><div class="k">경고</div><ul style="font-size:16px"><li>경로 없음</li><li>개념은 인지적인데 측정은 구조적만</li><li>개념은 구조적인데 측정은 신뢰만</li><li>단위 다름(가구 수급과 가구원 신뢰)</li><li>독립끼리 연결</li><li>고립된 변수</li><li>매개에 경로 한쪽만</li></ul></div>
  <div><div class="k" style="color:var(--greend)">정보</div><ul style="font-size:16px"><li>개념은 둘 다인데 측정은 한쪽만</li><li>공동체 속성인데 개인 응답</li><li>종속에 사회자본 밖 문항</li><li>통제변수에 경로</li></ul></div>
 </div></div>
 <div class="cap">규칙은 순수 함수(validate, gap)라 대시보드와 같은 값을 본다.</div>
 <aside class="notes"></aside>
</section>

<section class="slide" data-ap="1">
 <div class="hd"><h2>자료별 한계와 다음 설계</h2><p class="s">부록. 캔버스 「리뷰」 탭의 카드</p></div>
 <div class="bd"><div class="in">
  <table style="font-size:15px"><tr><th style="width:170px">자료</th><th>한계</th><th>다음 설계</th></tr>
  <tr><td>한국복지패널</td><td>아동수당이 보편화된 해라 심사 효과의 변이 없음. 신뢰는 가구원, 수급은 가구</td><td>14차(선별)와 16차를 같은 사람으로 이어 전환 전후 설계</td></tr>
  <tr><td>사회통합실태조사</td><td>한 해 횡단면, 역인과 못 가림. 수급 문항 없음</td><td>2021~2025 다섯 해 추세, 공공서비스 만족을 매개로</td></tr>
  <tr><td>한국종합사회조사</td><td>수급 문항 없어 공정성과 신뢰의 관계만</td><td>2012년 지역 집단토론 참여 변수로 Lowndes &amp; Wilson 설계</td></tr>
  <tr><td>사회조사</td><td>참여는 상세하나 수급·대인신뢰 없음</td><td>시도 단위로 가계금융복지조사 수급률과 결합</td></tr>
  <tr><td>지역사회건강조사</td><td>신뢰가 예/아니오, 0–10과 다름</td><td>시군구 226개로 Freitag의 24개 한계 극복</td></tr></table>
 </div></div>
 <div class="cap">전문은 model/build_index.py의 REVIEWS. 교수님 설명 뒤 수정 가능.</div>
 <aside class="notes"></aside>
</section>

</div>
<div id="notes"></div><div id="help">←/→ 이동 · N 노트 · F 전체화면</div>
<script>
const S=[...document.querySelectorAll('.slide')];let i=0;const N=document.getElementById('notes');
function fit(){const sc=Math.min(innerWidth/1280,innerHeight/720);S.forEach(s=>s.style.transform=`scale(${sc})`);}
function show(k){i=Math.max(0,Math.min(S.length-1,k));S.forEach((s,j)=>s.classList.toggle('on',j===i));N.innerHTML=(S[i].querySelector('.notes')||{}).innerHTML||'<i>노트 없음</i>';location.hash=i+1;}
let main=0,ap=0;S.forEach(s=>{const p=document.createElement('div');p.className='pg';if(s.dataset.ap){p.textContent='A'+(++ap);}else{main++;if(!s.classList.contains('cover'))p.textContent=main;}s.appendChild(p);});
addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown')show(i+1);else if(e.key==='ArrowLeft'||e.key==='PageUp')show(i-1);else if(e.key.toLowerCase()==='n')N.classList.toggle('on');else if(e.key.toLowerCase()==='f'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}});
addEventListener('click',e=>{if(e.target.closest('#notes'))return;show(i+(e.clientX>innerWidth/2?1:-1));});
addEventListener('resize',fit);fit();show((+location.hash.slice(1)||1)-1);
</script>
</body></html>
"""
for k, v in IMG.items():
    HTML = HTML.replace("{{" + k + "}}", v)
assert "{{" not in HTML, "치환 안 된 그림 자리"
out = os.path.join(H, "week11_part2.html"); open(out, "w", encoding="utf-8").write(HTML)
print("week11_part2.html", len(HTML) // 1024, "KB")
