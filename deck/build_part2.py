# -*- coding: utf-8 -*-
"""2부 덱(2026-11-13 재설계). 1부 덱(week11_part1.html)의 머리·CSS·넘기기 스크립트를 그대로 쓰고 장만 새로 만든다.
2부 흐름: 접속·안내 3분 → 모형 만들기 12분 → 분포 보기와 모형 이야기 22분 → 정리 5분(+여유 3분).
실행: python deck/build_part2.py → deck/week11_part2.html (1부 덱을 먼저 빌드해 둘 것)"""
import base64, html, io, os, re, sys
import qrcode
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fontface import face
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
CANVAS = "https://5-jihwan.github.io/week11-seminar/model/canvas.html"
base = open(os.path.join(H, "week11_part1.html"), encoding="utf-8").read()
secs = re.findall(r'<section class="slide.*?</section>', base, re.S)
COVER_IMG = re.search(r'<img src="(data:[^"]+)"', secs[0]).group(1)
CREDIT = "Landsgemeinde Glarus, 2009.jpg · Marc Schlumpf, www.icarus-design.ch · CC BY-SA 3.0 · Wikimedia Commons"


def img_uri(path, w=1100, q=82):
    im = Image.open(path).convert("RGB"); im.thumbnail((w, w * 2)); b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def qr_uri(url):
    q = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M); q.add_data(url); q.make(fit=True)
    b = io.BytesIO(); q.make_image(fill_color="#072A60", back_color="white").save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


S = []


def slide(title, sub, body, cap="", notes="", ap=False):
    S.append(f'<section class="slide" {"data-ap=1" if ap else ""}><div class="hd"><h2>{title}</h2>{f"<p class=s>{sub}</p>" if sub else ""}</div><div class="bd"><div class="in">{body}</div></div>{f"<div class=cap>{cap}</div>" if cap else ""}<aside class="notes">{notes}</aside></section>')


def cover(h1, sub, meta, notes):
    S.append(f'<section class="slide cover"><img src="{COVER_IMG}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55"><div style="position:absolute;inset:0;background:rgba(7,42,96,.55)"></div><div class="c" style="position:absolute"><h1>{h1}</h1><p class="sub">{sub}</p></div><div class="meta">{meta}</div><div style="position:absolute;right:40px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:600px;text-align:right">{CREDIT}</div>\n<aside class="notes">{notes}</aside></section>')


F = lambda n: img_uri(os.path.join(H, "fig_part2", n))

# 1 표지
cover("국내 공개 데이터로 만드는 사회자본 연구모형",
      "11주차 발제 2부 · 자료 고르기, 사회자본 정의, 연구모형 설계, 모형 이야기",
      "사회자본과 공공정책 · 2026-11-13 · 발제 오지환(석사과정 2학기) · 성균관대학교",
      "2부를 시작하겠습니다. 1부에서는 다섯 편이 사회자본을 무엇으로 재고 어떤 제도와 관련지었는지를 읽었는데, 2부는 그 작업을 여러분이 직접 해 보는 시간입니다. 2주차부터 지금까지 사회자본의 정의와 양적 연구를 꽤 많이 읽었으니까, 한국에서 공개하고 있는 조사 자료 하나를 골라 사회자본을 종속변수로 둔 연구모형을 각자 하나씩 만들어 보고, 그 모형을 놓고 자유롭게 이야기해 보겠습니다.")

# 2 1부에서 넘어오는 표
slide("지정문헌 다섯 편의 사회자본 측정", "1부 종속변수 비교를 자료 중심으로 다시 정리",
      '''<table style="font-size:15.5px;word-break:keep-all"><tr><th style="width:15%">논문</th><th style="width:27%">자료</th><th style="width:27%">사회자본으로 잰 것</th><th style="width:8%">단위</th><th>결과</th></tr>
<tr><td>Krishna</td><td>인도 라자스탄 61개 마을, 1997·2004 두 번 조사</td><td>집합행동 성향 6문항 지수(0~100)</td><td>마을</td><td>자생 조직·규칙·신진 리더와 양(+)의 관계, 정부·NGO 조직은 유의하지 않음</td></tr>
<tr><td>Freitag</td><td>스위스 가구패널 1999, 24개 칸톤</td><td>결사체 참여 4문항 주성분의 칸톤 평균</td><td>칸톤</td><td>직접민주주의·합의민주주의·지방자치와 양(+)의 관계, 언어권을 통제하면 직접민주주의는 유의하지 않음</td></tr>
<tr><td>Lowndes &amp; Wilson</td><td>자료 없음(영국 지방정부 논의)</td><td>Putnam의 정의(연결망·규범·신뢰)</td><td>–</td><td>제도 설계 네 차원을 제시</td></tr>
<tr><td>Mettler</td><td>미국 2차 대전 참전자 716명 회고 설문</td><td>단체 가입 수, 정치참여 지표 6개</td><td>개인</td><td>교육 급여 이용과 양(+)의 관계(학력 통제 후)</td></tr>
<tr><td>Kumlin &amp; Rothstein</td><td>스웨덴 서부 SOM 1999 조사</td><td>대인신뢰 0~10 한 문항</td><td>개인</td><td>선별 기관 접촉 1곳당 −.26, 보편 기관 +.07</td></tr></table>
<p class="ppn" style="margin-top:16px">다섯 편은 각자 손에 있는 자료로 사회자본을 정의했고, 무엇으로 쟀느냐에 따라 결과의 방향도 달랐다. 2부에서는 같은 작업을 국내 공개 자료로 한다.</p>''',
      "1부 지정문헌 종속변수 비교 장과 각 논문 장의 원문 쪽수 참고.",
      "1부 끝에서 본 표를 자료 쪽으로 조금 바꿔서 다시 띄웠습니다. 다섯 편이 사회자본을 잰 방법이 마을 단위 지수, 칸톤 평균의 결사체 참여, 단체 가입 수, 대인신뢰 한 문항으로 다 달랐고, 결과의 방향도 그에 따라 달랐습니다. 저는 저자들이 처음부터 그렇게 정의했다기보다 손에 있던 자료가 정의를 정한 면이 크다고 봅니다. 2부에서는 같은 작업을 우리가 국내 공개 자료로 해 보겠습니다.")

# 3 진행 순서
flow = [(3, "2:15", "접속·안내", "QR로 들어와 별명 정하기"), (12, "2:18", "모형 만들기", "자료 고르기 → 사회자본 한 줄 정의 → 문항으로 변수 → 화살표 → 제출"),
        (22, "2:30", "분포 보기와 모형 이야기", "17명의 선택을 대시보드로 보고, 네댓 명의 모형을 화면에 띄워 이야기"), (5, "2:52", "정리", "오늘 모형과 선행연구, 다음 설계")]
slide("2부 진행 순서", "45분 · 2:15~3:00, 끝에 여유 3분",
      '<div class="f4">' + "".join(f'<div style="flex:{m}"><span>{t} · {m}분</span><b>{n}</b><i>{d}</i></div>' for m, t, n, d in flow) + '''</div>
<div class="two" style="margin-top:26px;align-items:start;gap:44px"><div><div class="tlh">제출 최소 조건</div><p class="ppn">종속변수 하나와 원인 하나를 화살표로 이으면 제출된다. 통제·조절·매개는 시간이 남으면 더한다.</p></div>
<div><div class="tlh">없는 것</div><p class="ppn">원자료와 계수 추정은 없다. 조사표의 문항으로 모형을 설계하는 데까지 한다.</p></div></div>''',
      "", "진행은 화면 순서대로입니다. 처음 3분 동안 접속하고 별명을 정한 다음에 12분 동안 모형을 만듭니다. 그다음 22분이 이 시간의 중심인데, 먼저 열일곱 명이 무엇을 골랐는지 대시보드로 함께 보고, 네댓 분의 모형을 화면에 띄워서 이야기를 나누겠습니다. 마지막 5분은 정리입니다. 제출은 종속변수 하나와 원인 하나만 화살표로 이어도 되니까 처음부터 완성된 모형을 만들려고 하지 않으셔도 됩니다. 그리고 원자료로 계수를 추정하는 단계는 없고, 조사표 문항으로 모형을 설계하는 데까지 합니다.")

# 4 접속과 약속
slide("접속과 약속", "노트북 권장 · 폰도 작동",
      f'''<div class="two" style="grid-template-columns:auto 1fr;gap:48px;align-items:center"><div class="qr"><img src="{qr_uri(CANVAS)}" alt="캔버스 주소 QR"><div class="url">5-jihwan.github.io/week11-seminar/model/canvas.html</div></div>
<div><ul class="tll"><li>노트북에서는 문항 카드를 캔버스로 끌어 놓고, 폰에서는 카드의 ＋ 버튼을 누른다</li>
<li>이름 대신 별명을 쓴다. 대시보드와 화면에는 별명만 나온다</li>
<li>오늘 만든 모형은 이 수업 안에서만 보고, 수업이 끝나면 서버에서 지운다</li>
<li>화면의 선행연구 목록은 규칙과 AI로 분류한 것이며 사람이 검수하기 전이다. 인용하기 전에 원문을 확인한다</li></ul></div></div>''',
      "", "화면의 QR로 들어오시면 됩니다. 노트북이 편하고, 폰에서도 문항 카드의 더하기 버튼으로 똑같이 만들 수 있습니다. 이름 대신 별명을 써 주시고, 오늘 고르신 것은 이 수업 안에서만 보고 수업이 끝나면 서버에서 지운다는 점을 먼저 말씀드립니다. 화면 오른쪽에 닮은 선행연구가 뜨는데, 이 목록은 규칙과 AI로 분류해 둔 것이고 제가 하나하나 검수하지는 못했습니다. 인용하실 때는 원문을 꼭 확인해 주십시오.")

# 5 자료 여덟 가지
rows = [("한국복지패널", "보건사회연구원·서울대 · 16차(2021)", "개인·가구", "대인신뢰(3년 주기)", "선별·보편 수급 경험이 같은 사람에게 있음"),
        ("사회통합실태조사", "한국행정연구원 · 2023", "개인", "대인·기관 신뢰, 참여", "공정성 인식. 수급 경험 문항은 없음"),
        ("한국종합사회조사", "성균관대 서베이리서치센터 · 2012·2023", "개인", "신뢰·연결망·참여 문항이 가장 많음", "7개 권역, 도시·농촌"),
        ("사회조사", "국가데이터처 · 2023", "13세 이상", "단체 참여·기부·봉사, 사회 신뢰", "시도. 대인신뢰 문항은 없음"),
        ("지역사회건강조사", "질병관리청 · 2023", "개인", "이웃 신뢰(예/아니오), 단체 참여", "기초생활수급, 시군구"),
        ("청년삶실태조사", "국무조정실·보건사회연구원 · 2022", "19~34세", "사회 신뢰 0~10", "기초수급·실업급여, 시도"),
        ("노인실태조사", "보건복지부·보건사회연구원 · 2023", "65세 이상", "가족·이웃·정부 신뢰, 단체·봉사", "기초생활·기초연금 수급"),
        ("가계금융복지조사", "국가데이터처 · 2023", "가구", "신뢰·참여 문항 없음", "공적이전 9항목(원인 쪽으로만)")]
slide("고를 수 있는 국내 공개 자료", "조사표 문항 기준 · 한 모형은 한 자료 안의 문항으로",
      '<table style="font-size:14.5px;word-break:keep-all"><tr><th style="width:16%">자료</th><th style="width:25%">기관 · 차수</th><th style="width:10%">대상</th><th style="width:23%">사회자본 문항</th><th>함께 고를 수 있는 원인</th></tr>'
      + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in rows) + "</table>",
      "model/catalog.json(조사표·코드북 원문 대조). 원자료는 쓰지 않음. 문항 수는 자료마다 85~3,345개.",
      "고를 수 있는 자료는 여덟 가지입니다. 복지 수급 경험과 신뢰를 한 사람 안에서 보고 싶으시면 한국복지패널이나 청년삶실태조사, 노인실태조사, 지역사회건강조사가 맞고, 기관신뢰와 공정성을 보고 싶으시면 사회통합실태조사가 맞습니다. 연결망이나 참여 문항을 넉넉하게 쓰고 싶으시면 한국종합사회조사가 가장 문항이 많습니다. 가계금융복지조사에는 신뢰나 참여 문항이 없어서 원인 쪽으로만 쓸 수 있습니다. 한 모형은 한 자료 안의 문항으로만 만들게 되어 있으니, 먼저 보고 싶은 원인이 어느 자료에 있는지부터 보시면 고르기가 쉽습니다.")

# 6 만드는 순서
steps = [("gate.png", "① 자료 고르기", "여덟 가지 중 하나. 카드에 단위와 사회자본 문항이 적혀 있다"),
         ("concept.png", "② 사회자본 정의 한 줄", "문항을 보기 전에 적는다. 인지적·구조적, 개인의 자산·공동체의 속성을 고른다"),
         ("canvas_def.png", "③ 문항으로 변수 만들고 잇기", "역할(종속·원인·통제·조절·매개)을 정하고 화살표로 이은 뒤 오른쪽 위 「제출」")]
slide("연구모형 만드는 순서", "캔버스 화면",
      '<div class="steps">' + "".join(f'<figure><img src="{F(f)}" alt=""><figcaption><b>{t}</b>{d}</figcaption></figure>' for f, t, d in steps) + "</div>",
      "", "만드는 순서는 세 화면입니다. 왼쪽처럼 자료를 하나 고르고, 가운데 화면에서 사회자본이 무엇인지 한 줄로 적는데, 문항을 보기 전에 적는 게 중요합니다. 정의를 먼저 적어 두어야 나중에 고른 문항이 그 정의와 맞는지 볼 수 있습니다. 오른쪽이 실제 캔버스인데, 왼쪽 목록에서 문항을 끌어다 놓거나 더하기 버튼을 누르면 역할을 묻습니다. 종속변수와 원인을 정하고 화살표로 이은 다음 오른쪽 위 제출을 누르시면 됩니다.")

# 7 만들며 확인할 것
slide("모형을 만들며 확인할 것", "2:18~2:30 · 이 화면을 띄워 둔 채 작업",
      '''<ul class="chk"><li><b>정의와 측정</b>적어 둔 사회자본의 정의와 종속변수로 묶은 문항이 같은 것을 가리키는가. 오른쪽 「개념화·조작화」 탭에 어긋남이 표시된다</li>
<li><b>원인의 순서</b>원인으로 놓은 변수가 사회자본보다 먼저 생기는가, 같은 때에 잰 것인가</li>
<li><b>1부와의 거리</b>다섯 편 가운데 누구의 설계와 가장 닮았는가. 「분류 틀·유사한 선행연구」 탭</li>
<li><b>막히면</b>종속변수 하나와 원인 하나만 이어서 먼저 제출한다. 다시 내면 최신 것만 센다</li></ul>''',
      "", "작업하시는 동안 이 화면을 띄워 두겠습니다. 만들면서 세 가지를 봐 주시면 좋겠습니다. 적어 둔 정의와 종속변수로 묶은 문항이 같은 것을 가리키는지는 오른쪽 개념화 탭에 어긋남으로 표시되고, 원인으로 놓은 변수가 정말 사회자본보다 먼저 생기는지는 직접 따져 보셔야 합니다. 1부의 다섯 편 가운데 누구의 설계와 닮았는지는 분류 틀 탭에서 볼 수 있습니다. 막히시면 종속변수 하나와 원인 하나만 이어서 먼저 내 주십시오. 다시 내시면 최신 것만 셉니다.")

# 8 모형 이야기
slide("모형 이야기", "2:33~2:52 · 한 사람 4분, 네댓 명",
      '''<div class="two" style="align-items:start;gap:48px"><div><div class="tlh">한 사람 4분</div><ul class="tll"><li>1분 · 무엇을 사회자본으로 보았고 왜 이 문항을 골랐는지</li><li>2분 · 다른 분의 질문 하나와 답</li><li>1분 · 닮은 선행연구와 1부 다섯 편 가운데 가까운 설계</li></ul>
<p class="ppn" style="color:var(--sub)">자원하신 분부터. 없으면 서로 다른 자료와 다른 종속변수를 고른 분을 고른다.</p></div>
<div><div class="tlh">함께 볼 질문</div><ul class="chk sm"><li><b>정의와 측정</b>말한 사회자본과 잰 문항이 같은가</li><li><b>원인의 순서</b>한 시점 자료에서 원인과 결과를 어떻게 가를 수 있는가</li><li><b>다음 설계</b>패널, 제도가 바뀐 전후, 지역 비교 가운데 무엇으로 보완할 수 있는가</li></ul></div></div>''',
      "", "이제 모형을 몇 개 화면에 띄워 보겠습니다. 먼저 자원해 주실 분이 계시면 그분부터 하고, 안 계시면 서로 다른 자료와 종속변수를 고르신 분들을 제가 모시겠습니다. 한 분당 4분 정도로, 무엇을 사회자본으로 보셨고 왜 그 문항을 고르셨는지 1분 정도 말씀해 주시면, 다른 분들이 질문을 하나 드리고, 마지막에 화면에 뜬 닮은 선행연구와 1부 다섯 편 가운데 가까운 설계를 같이 보겠습니다. 이야기할 때는 오른쪽 세 질문을 기준으로 삼으면 좋겠습니다. 정의와 측정이 맞는지, 한 시점 자료에서 원인과 결과를 어떻게 가를지, 그리고 그 한계를 패널이나 제도 변화 전후 비교, 지역 비교 가운데 무엇으로 보완할지입니다.")

# 9 정리
slide("2부 정리", "오늘 제출된 모형과 다음 설계",
      '''<div class="two" style="align-items:start;gap:48px"><div><div class="tlh">대시보드에서 확인할 것</div><ul class="tll"><li>가장 많이 고른 자료와 종속변수</li><li>정의와 측정이 어긋난 모형의 수</li><li>아무도 고르지 않은 원인과 종속변수의 조합, 선행연구가 적은 조합</li></ul></div>
<div><div class="tlh">한 시점 자료를 넘어서는 설계</div><ul class="tll"><li>같은 사람을 여러 해 따라가는 패널: 한국복지패널</li><li>제도가 바뀐 전후 비교: 한국 아동수당은 2018년 9월 소득 하위 90%로 시작해 2019년 1월 소득 심사를 없앴다</li><li>지역 사이 비교: 지역사회건강조사의 시군구</li></ul></div></div>''',
      "", "정리하겠습니다. 왼쪽 세 가지는 지금 대시보드에서 오늘 결과로 바로 말씀드리겠습니다. 가장 많이 고른 자료와 종속변수가 무엇이었는지, 정의와 측정이 어긋난 모형이 몇 개였는지, 그리고 아무도 가지 않은 조합이 어디인지입니다. 오른쪽은 오늘 만든 모형을 실제 연구로 옮길 때의 이야기인데, 공개 자료 대부분이 한 시점 자료라서 원인의 순서를 가르기 어렵습니다. 한국복지패널처럼 같은 사람을 따라가는 패널이 있고, 아동수당처럼 같은 급여가 선별에서 보편으로 바뀐 전후를 비교할 수 있는 제도 변화가 있고, 지역사회건강조사처럼 시군구를 비교할 수 있는 자료가 있습니다. Kumlin과 Rothstein이 스스로 한계로 적은 역인과 문제를 우리 자료로는 이런 방법으로 다룰 수 있다고 봅니다.")

# 10 감사
cover("감사합니다", "1부 세미나와 2부 연구모형 설계에 함께해 주셔서 감사합니다.", "사회자본과 공공정책 · 11주차 발제 · 오지환(석사과정 2학기)",
      "오늘 1부와 2부에 끝까지 함께해 주셔서 감사합니다. 제출해 주신 모형은 말씀드린 대로 수업이 끝나면 서버에서 지우겠습니다. 이것으로 11주차 발제를 마치겠습니다.")

# 부록: 발표자용 진행표와 장애 대응
run = [("2:15", "표지 → 측정 → 진행 순서 → 접속", "별명·삭제 고지. 대시보드 「작업 중」 수가 오르는지"),
       ("2:18", "자료 → 만드는 순서 → 확인할 것(띄워 둠)", "돌아다니며 막힌 사람 옆에. 2:24 「하나만 이어도 제출」, 2:28 「2분 남음」"),
       ("2:30", "대시보드(프로젝터 모드) 자료·종속 막대", "가장 많이 고른 종속변수를 고른 분 한 명에게 이유"),
       ("2:33", "모형 이야기 → 대시보드 spotlight", "한 사람 4분. 선행연구는 제목과 자료만, 「검수 전」"),
       ("2:52", "2부 정리 + 대시보드", "오늘 결과 세 줄을 말로"),
       ("2:57", "감사합니다", "")]
slide("2부 진행표", "부록 · 발표자용",
      '<table style="font-size:14.5px;word-break:keep-all"><tr><th style="width:9%">시각</th><th style="width:38%">화면</th><th>할 일</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in run) + '''</table>
<p class="ppn" style="margin-top:14px">1부가 10분 늦게 끝나면 만들기 10분, 이야기 세 명, 정리 3분으로 줄인다. 2:30에 제출이 다섯 명보다 적으면 만들기를 3분 늘린다.</p>''',
      "", "(부록. 발표자용 진행표입니다.)", ap=True)
slide("와이파이나 서버가 끊길 때", "부록 · 발표자용",
      '''<ul class="tll"><li>대시보드 「연결 실패」: 새로고침 후 PIN 다시 입력. 그래도 안 되면 노트북 Downloads 폴더의 2부_오프라인판_20261112에서 canvas.html과 dashboard.html을 같은 브라우저로 연다</li>
<li>오프라인판에서는 학생이 말하는 문항을 Ji가 대신 넣고 제출한다. 대시보드에 바로 뜬다</li>
<li>와이파이만 끊기면 이미 연 학생 화면은 계속 작동하고 제출만 안 된다. 이야기 시간에는 학생 화면을 직접 보며 진행</li>
<li>수업 뒤: 대시보드 「비우기」로 서버 기록 삭제 후, 저장소 전체 삭제(wrangler kv namespace delete)</li></ul>''',
      "", "(부록. 장애 대응입니다.)", ap=True)

CSS2 = """.f4{display:flex;gap:6px}.f4>div{min-width:150px;background:var(--navy);color:#fff;padding:14px 16px;display:flex;flex-direction:column;gap:6px}.f4 span{font-size:13px;opacity:.8}.f4 b{font-size:19px}.f4 i{font-style:normal;font-size:14px;line-height:1.5;opacity:.92;word-break:keep-all}
.qr{text-align:center}.qr img{width:300px;height:300px;image-rendering:pixelated;border:1px solid var(--line)}.qr .url{font-size:13px;color:var(--sub);margin-top:8px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.steps figure{margin:0}.steps img{width:100%;border:1px solid var(--line);border-radius:4px;display:block}.steps figcaption{font-size:14.5px;margin-top:10px;line-height:1.55;word-break:keep-all}.steps figcaption b{display:block;color:var(--navy);font-size:17px;margin-bottom:2px}
.chk{list-style:none;padding:0;margin:0}.chk li{border-top:1px solid var(--line);padding:12px 0 12px 150px;position:relative;font-size:18px;line-height:1.55;word-break:keep-all}.chk li b{position:absolute;left:0;top:12px;color:var(--navy)}.chk.sm li{padding-left:110px;font-size:16.5px}
.tlh{font-size:19px;font-weight:700;color:var(--navy);border-top:2px solid var(--navy);padding-top:10px;margin-bottom:8px}.tll li{font-size:16.5px;line-height:1.6;word-break:keep-all}.ppn{font-size:15.5px;line-height:1.6;word-break:keep-all}
"""
# 1부 덱의 머리·CSS·스크립트를 쓰고 글꼴만 2부 글자로 다시 내장
head_end = base.index('<div id="stage">')
head = base[:head_end].replace("<title>" + re.search(r"<title>(.*?)</title>", base).group(1) + "</title>", "<title>2부 연구모형</title>", 1)
head = re.sub(r'@font-face\{[^}]*\}', "", head)
text = re.sub(r"<[^>]+>|data:[^\"']+", " ", "".join(S))
head = head.replace("<style>", "<style>" + face(html.unescape(text) + "0123456789·→①②③") + CSS2, 1)
tail = base[base.index('</div><div id="notes">'):]
out = head + '<div id="stage">\n' + "\n".join(S) + "\n" + tail
assert out.count('<section class="slide') == len(S) == 12 and "@font-face" in out
open(os.path.join(H, "week11_part2.html"), "w", encoding="utf-8").write(out)
print("week11_part2.html", len(out) // 1024, "KB", len(S), "장")
