# -*- coding: utf-8 -*-
"""2부 덱(2026-11-13 재설계 2판). 1부 덱(week11_part1.html)의 머리·CSS·넘기기 스크립트를 그대로 쓰고 장만 새로 만든다.
흐름: 표지 → 2부를 준비한 이유 → 진행 순서(QR) → 자료 → 만드는 순서 → 만드는 동안 → 모형 이야기 → 정리 → 감사 (+부록 2)
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


S, NOTES = [], []


def slide(title, sub, body, cap="", notes="", ap=False):
    NOTES.append(notes)
    S.append(f'<section class="slide" {"data-ap=1" if ap else ""}><div class="hd"><h2>{title}</h2>{f"<p class=s>{sub}</p>" if sub else ""}</div><div class="bd"><div class="in">{body}</div></div>{f"<div class=cap>{cap}</div>" if cap else ""}<aside class="notes">{notes}</aside></section>')


def cover(h1, sub, meta, notes):
    NOTES.append(notes)
    S.append(f'<section class="slide cover"><img src="{COVER_IMG}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55"><div style="position:absolute;inset:0;background:rgba(7,42,96,.55)"></div><div class="c" style="position:absolute"><h1>{h1}</h1><p class="sub">{sub}</p></div><div class="meta">{meta}</div><div style="position:absolute;right:40px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:600px;text-align:right">{CREDIT}</div>\n<aside class="notes">{notes}</aside></section>')


F = lambda n: img_uri(os.path.join(H, "fig_part2", n))

cover("국내 공개 데이터로 만드는 사회자본 연구모형", "11주차 발제 2부",
      "사회자본과 공공정책 · 2026-11-13 · 발제 오지환(석사과정 2학기) · 성균관대학교",
      "2부를 시작하겠습니다. 쉬는 시간 전에 다섯 편이 사회자본을 어떻게 재고 무엇과 관련지었는지를 봤는데, 2부에서는 그 일을 각자 국내 공개 자료로 직접 해 보려고 합니다.")

five = [("Krishna 2007", "병충해나 마을 다툼이 생기면 마을이 함께 나설 거라는 기대", "6문항, 마을 평균"),
        ("Freitag 2006", "단체 활동과 봉사에 참여하는 정도", "4문항, 칸톤 평균"),
        ("Lowndes &amp; Wilson 2001", "자료 없음", "이론 논문"),
        ("Mettler 2002", "가입한 단체 수와 정치참여", "1998년 회고 설문"),
        ("Kumlin &amp; Rothstein 2005", "사람들을 대체로 믿을 수 있는가", "0~10점 한 문항")]
slide("2부를 준비한 이유", "다섯 편이 사회자본으로 잰 것",
      '<div class="why5">' + "".join(f"<div><b>{a}</b><p>{b}</p><span>{c}</span></div>" for a, b, c in five) + '''</div>
<p class="whyq">이름은 모두 사회자본인데 잰 것이 다르고, 결과도 그만큼 달랐다. 저자들은 각자 가진 자료의 문항으로 사회자본을 정했다.</p>
<p class="whyn">학위논문에서 공개 자료를 쓰면 우리도 같은 결정을 한다. 오늘은 국내 공개 자료로 그 결정을 미리 해 본다.</p>''',
      "1부 각 논문의 측정 장 참고.",
      "2부를 왜 준비했는지부터 말씀드리겠습니다. 1부에서 다섯 편을 읽으면서 계속 마음에 걸렸던 것이, 다 같이 사회자본이라고 부르는데 실제로 잰 것은 꽤 달랐다는 점입니다. 화면 왼쪽부터 보시면 Krishna는 마을에 일이 생겼을 때 다 같이 나설 거라는 기대를 물었고, Freitag은 단체 활동과 봉사에 얼마나 참여하는지를 봤고, Mettler는 가입한 단체 수와 정치참여를, Kumlin과 Rothstein은 사람들을 대체로 믿을 수 있느냐는 한 문항을 썼습니다. 저자들이 각자 가진 자료에 있는 문항으로 사회자본을 정했고, 결과가 엇갈린 것도 상당 부분 여기서 왔다고 저는 봅니다. 저희도 학위논문에서 공개 자료를 쓰게 되면 어떤 문항을 사회자본으로 쓸지부터 정해야 하는데, 오늘은 그 결정을 국내 공개 자료로 미리 한번 해 보려고 합니다.")

flow = [(3, "2:15", "들어오기"), (12, "2:18", "모형 만들기"), (22, "2:30", "함께 보고 이야기하기"), (5, "2:52", "정리")]
slide("2부 진행 순서", "2:15~3:00",
      '<div class="f4">' + "".join(f'<div style="flex:{m}"><span>{t} · {m}분</span><b>{n}</b></div>' for m, t, n in flow) + f'''</div>
<div class="two" style="grid-template-columns:auto 1fr;gap:44px;align-items:center;margin-top:24px"><div class="qr"><img src="{qr_uri(CANVAS)}" alt="캔버스 주소 QR"><div class="url">5-jihwan.github.io/week11-seminar/model/canvas.html</div></div>
<ul class="tll"><li>노트북이 편하고, 폰은 문항 카드의 ＋ 버튼으로 만든다</li><li>이름 대신 별명을 쓴다. 낸 모형은 수업이 끝나면 지운다</li><li>종속변수 하나와 원인 하나를 화살표로 이으면 제출된다</li><li>원자료와 계수 추정은 없고, 조사표 문항으로 모형을 그리는 데까지 한다</li></ul></div>''',
      "", "진행은 위에 적은 순서대로입니다. 아래 QR로 들어오시면 되는데, 노트북이 편하고 폰에서도 문항 카드에 있는 더하기 버튼으로 똑같이 만들 수 있습니다. 이름 대신 별명을 써 주시고, 오늘 내신 모형은 이 수업 안에서만 보고 수업이 끝나면 서버에서 지우겠습니다. 모형은 12분 동안 만드는데, 종속변수 하나와 원인 하나만 화살표로 이어도 제출이 되어서 처음부터 다 갖추려고 하지 않으셔도 됩니다. 그다음 20분 남짓이 2부의 본론으로, 다 같이 결과를 보고 몇 분의 모형을 띄워서 이야기를 나누겠습니다. 원자료로 계수를 내는 단계는 없고 조사표 문항으로 모형을 그리는 데까지만 합니다.")

rows = [("한국복지패널", "보건사회연구원·서울대 · 16차(2021)", "개인·가구", "대인신뢰(3년 주기)", "선별·보편 수급 경험이 같은 사람에게 있음"),
        ("사회통합실태조사", "한국행정연구원 · 2023", "개인", "대인·기관 신뢰, 참여", "공정성 인식. 수급 경험 문항은 없음"),
        ("한국종합사회조사", "성균관대 서베이리서치센터 · 2012·2023", "개인", "신뢰·연결망·참여 문항이 가장 많음", "7개 권역, 도시·농촌"),
        ("사회조사", "국가데이터처 · 2023", "13세 이상", "단체 참여·기부·봉사, 사회 신뢰", "시도. 대인신뢰 문항은 없음"),
        ("지역사회건강조사", "질병관리청 · 2023", "개인", "이웃 신뢰(예/아니오), 단체 참여", "기초생활수급, 시군구"),
        ("청년삶실태조사", "국무조정실·보건사회연구원 · 2022", "19~34세", "사회 신뢰 0~10", "기초수급·실업급여, 시도"),
        ("노인실태조사", "보건복지부·보건사회연구원 · 2023", "65세 이상", "가족·이웃·정부 신뢰, 단체·봉사", "기초생활·기초연금 수급"),
        ("가계금융복지조사", "국가데이터처 · 2023", "가구", "신뢰·참여 문항 없음", "공적이전 9항목(원인으로만)")]
slide("고를 수 있는 국내 공개 자료", "한 모형은 한 자료 안의 문항으로",
      '<table style="font-size:14.5px;word-break:keep-all"><tr><th style="width:16%">자료</th><th style="width:25%">기관 · 차수</th><th style="width:10%">대상</th><th style="width:23%">사회자본 문항</th><th>함께 고를 수 있는 원인</th></tr>'
      + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in rows) + "</table>",
      "조사표·코드북 기준. 원자료는 쓰지 않음.",
      "고를 수 있는 자료는 여기 여덟 가지입니다. 복지 수급 경험과 신뢰를 한 사람 안에서 같이 보고 싶으시면 한국복지패널이나 청년삶실태조사, 노인실태조사, 지역사회건강조사에 둘 다 들어 있고, 기관신뢰나 공정성을 보고 싶으시면 사회통합실태조사가 맞습니다. 연결망이나 참여 문항은 한국종합사회조사에 가장 많고, 가계금융복지조사에는 신뢰나 참여 문항이 없어서 원인 쪽으로만 쓸 수 있습니다. 한 모형은 한 자료 안에서만 만들 수 있어서, 보고 싶은 원인이 어느 자료에 들어 있는지부터 찾으시면 고르기가 빠릅니다.")

steps = [("gate.png", "① 자료 고르기", "카드마다 단위와 들어 있는 사회자본 문항이 적혀 있다"),
         ("concept.png", "② 사회자본을 한 줄로 적기", "문항을 보기 전에 적는다"),
         ("canvas_def.png", "③ 문항을 변수로 놓고 잇기", "역할을 정하고 화살표로 이은 뒤 오른쪽 위 「제출」")]
slide("연구모형 만드는 순서", "캔버스 화면",
      '<div class="steps">' + "".join(f'<figure><img src="{F(f)}" alt=""><figcaption><b>{t}</b>{d}</figcaption></figure>' for f, t, d in steps) + "</div>",
      "오른쪽에 뜨는 닮은 선행연구는 규칙과 AI로 분류한 목록이며 사람이 검수하기 전이다.",
      "만드는 순서는 화면 세 개입니다. 왼쪽 화면에서 자료를 하나 고르고, 가운데 화면에서 사회자본이 무엇인지 한 줄로 적는데, 이건 문항을 보기 전에 적어 주십시오. 먼저 적어 두어야 나중에 고른 문항과 맞는지 비교해 볼 수 있습니다. 오른쪽이 실제 작업 화면으로, 왼쪽 목록에서 문항을 끌어다 놓으면 역할을 묻고, 종속변수와 원인을 정해서 화살표로 이은 다음 오른쪽 위 제출을 누르시면 됩니다. 작업하다 보면 오른쪽에 닮은 선행연구가 뜨는데, 규칙과 AI로 분류해 둔 목록이라 제가 하나하나 확인하지는 못했습니다. 인용하실 때는 원문을 꼭 확인해 주십시오.")

slide("모형 만드는 동안", "2:18~2:30",
      '''<ul class="tll big"><li>처음에 적은 정의와 종속변수로 고른 문항이 같은 것을 가리키는가. 어긋나면 오른쪽 「개념화·조작화」 탭에 표시된다</li>
<li>원인으로 놓은 것이 사회자본보다 먼저 생기는가</li>
<li>막히면 종속변수 하나와 원인 하나만 이어 먼저 낸다. 다시 내면 마지막 것만 센다</li></ul>''',
      "", "작업하시는 동안 이 화면을 띄워 두겠습니다. 만들다가 한 번씩 확인해 주셨으면 하는 것은, 처음에 적은 정의와 종속변수로 고른 문항이 같은 것을 가리키는지, 그리고 원인으로 놓은 것이 정말 사회자본보다 먼저 생기는지입니다. 앞의 것은 어긋나면 오른쪽 개념화 탭에 표시가 됩니다. 막히시면 종속변수 하나와 원인 하나만 이어서 먼저 내 주시고, 다시 내시면 마지막 것만 셉니다.")

slide("모형 이야기", "2:33~2:52 · 한 사람 4분 정도",
      '''<div class="two" style="align-items:start;gap:48px"><div><div class="tlh">한 사람 4분 정도</div><ul class="tll"><li>무엇을 사회자본으로 봤고 왜 그 문항을 골랐는지 1분</li><li>다른 분의 질문 하나</li><li>화면에 뜬 닮은 선행연구와 1부 다섯 편 가운데 가까운 연구를 같이 보기</li></ul></div>
<div><div class="tlh">이야기하면서 볼 것</div><ul class="tll"><li>말한 사회자본과 고른 문항이 같은가</li><li>한 시점 자료에서 원인과 결과를 어떻게 가를 수 있나</li></ul></div></div>''',
      "", "이제 몇 분의 모형을 화면에 띄워 보겠습니다. 자원해 주실 분이 계시면 그분부터 하고, 안 계시면 서로 다른 자료와 종속변수를 고르신 분들께 제가 부탁드리겠습니다. 한 분당 4분 정도로, 무엇을 사회자본으로 보셨고 왜 그 문항을 고르셨는지 1분쯤 말씀해 주시면 다른 분이 질문을 하나 드리고, 마지막에 화면에 뜬 닮은 선행연구와 1부 다섯 편 가운데 가까운 연구를 같이 보겠습니다. 이야기하면서는 오른쪽 두 질문을 보면 좋겠는데, 말한 사회자본과 고른 문항이 같은지, 그리고 한 시점 자료에서 원인과 결과를 어떻게 가를 수 있을지입니다.")

slide("연구로 옮길 때 쓸 수 있는 설계", "2부 정리",
      '''<ul class="tll big"><li>같은 사람을 여러 해 따라가는 패널: 한국복지패널</li>
<li>제도가 바뀐 전후 비교: 한국 아동수당은 2018년 9월 소득 하위 90%로 시작해 2019년 1월 소득 심사를 없앴다</li>
<li>지역 사이 비교: 지역사회건강조사의 시군구</li></ul>''',
      "", "정리하겠습니다. 오늘 내신 모형의 분포는 방금 대시보드로 같이 봤고, 마지막으로 오늘 만든 모형을 실제 연구로 옮길 때의 이야기를 하겠습니다. 국내 공개 자료 대부분이 한 시점 자료라서 원인과 결과의 순서를 가르기 어려운데, Kumlin과 Rothstein이 스스로 한계로 적은 것도 이 문제였습니다. 화면에 적은 것처럼 한국복지패널은 같은 사람을 여러 해 따라가고, 아동수당은 같은 급여가 선별에서 보편으로 바뀌어서 전후를 비교할 수 있고, 지역사회건강조사는 시군구끼리 비교할 수 있습니다. 저는 오늘 만든 모형에 이 가운데 하나를 붙이면 1부에서 본 한계를 조금 줄일 수 있다고 봅니다.")

cover("감사합니다", "1부와 2부에 함께해 주셔서 감사합니다.", "사회자본과 공공정책 · 11주차 발제 · 오지환(석사과정 2학기)",
      "오늘 1부와 2부에 끝까지 함께해 주셔서 감사합니다. 내신 모형은 말씀드린 대로 수업이 끝나면 서버에서 지우겠습니다. 이것으로 11주차 발제를 마치겠습니다.")

run = [("2:15", "표지 → 준비한 이유 → 진행 순서(QR)", "별명과 「끝나면 지운다」를 말로. 대시보드 「작업 중」 수가 오르는지"),
       ("2:18", "자료 → 만드는 순서 → 만드는 동안(띄워 둠)", "돌아다니며 막힌 사람 옆에. 2:24 「하나만 이어도 제출」, 2:28 「2분 남음」"),
       ("2:30", "대시보드(프로젝터 모드) 자료·종속변수 막대", "가장 많이 고른 종속변수를 고른 분 한 명에게 이유"),
       ("2:33", "모형 이야기 → 대시보드 spotlight", "한 사람 4분. 선행연구는 제목과 자료만, 「검수 전」"),
       ("2:52", "연구로 옮길 때 쓸 수 있는 설계", "대시보드에서 본 것을 한두 문장으로"),
       ("2:57", "감사합니다", "")]
slide("2부 진행표", "부록 · 발표자용",
      '<table style="font-size:14.5px;word-break:keep-all"><tr><th style="width:9%">시각</th><th style="width:38%">화면</th><th>할 일</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in run) + '''</table>
<p class="ppn" style="margin-top:14px">1부가 10분 늦게 끝나면 만들기 10분, 이야기 세 명, 정리 3분으로 줄인다. 2:30에 제출이 다섯 명보다 적으면 만들기를 3분 늘린다.</p>''',
      "", "(부록. 발표자용 진행표입니다.)", ap=True)
slide("와이파이나 서버가 끊길 때", "부록 · 발표자용",
      '''<ul class="tll"><li>대시보드에 「연결 실패」가 뜨면 새로고침하고 PIN을 다시 넣는다. 그래도 안 되면 노트북 Downloads 폴더의 2부_오프라인판_20261112에서 canvas.html과 dashboard.html을 같은 브라우저로 연다</li>
<li>오프라인판에서는 학생이 말하는 문항을 발표자가 대신 넣고 제출한다. 대시보드에 바로 뜬다</li>
<li>와이파이만 끊기면 이미 연 학생 화면은 계속 돌아가고 제출만 안 된다. 이야기 시간에는 학생 화면을 직접 보며 진행한다</li>
<li>수업 뒤에는 대시보드 「비우기」로 서버 기록을 지우고, 저장소 전체를 삭제한다(wrangler kv namespace delete)</li></ul>''',
      "", "(부록. 장애 대응입니다.)", ap=True)

# 대본 말투 검사(1부와 같은 금지 목록)
BAN = r"니까|[가이] 아니라|(라는|다는) 것입니다|쪽입니다|에 대한 답|다른 하나는|그렇다면|뜻입니다|자리|흐름|갈래|접점|넘어서|무너|버티|깎|움직|(두|세|네|다섯) 가지(입니다|가 있습니다|를)|(첫째|둘째|셋째)|다음 장에서|짚겠습니다|—"
hits = [(i + 1, m.group(0)) for i, n in enumerate(NOTES) for m in re.finditer(BAN, n)]
assert not hits, hits

CSS2 = """.f4{display:flex;gap:6px}.f4>div{min-width:150px;background:var(--navy);color:#fff;padding:14px 16px;display:flex;flex-direction:column;gap:6px}.f4 span{font-size:13px;opacity:.8}.f4 b{font-size:19px}
.qr{text-align:center}.qr img{width:260px;height:260px;image-rendering:pixelated;border:1px solid var(--line)}.qr .url{font-size:13px;color:var(--sub);margin-top:8px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.steps figure{margin:0}.steps img{width:100%;border:1px solid var(--line);border-radius:4px;display:block}.steps figcaption{font-size:14.5px;margin-top:10px;line-height:1.55;word-break:keep-all}.steps figcaption b{display:block;color:var(--navy);font-size:17px;margin-bottom:2px}
.why5{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.why5>div{border-top:3px solid var(--navy);background:var(--navyt);padding:12px 12px 14px;word-break:keep-all;display:flex;flex-direction:column}.why5 b{color:var(--navy);font-size:15px;line-height:1.3;min-height:40px}.why5 p{font-size:16px;line-height:1.5;margin:8px 0;flex:1}.why5 span{font-size:13px;color:var(--sub)}
.whyq{font-size:19px;line-height:1.6;margin-top:26px;word-break:keep-all}.whyn{font-size:19px;line-height:1.6;margin-top:10px;color:var(--navy);font-weight:700;word-break:keep-all}
.tlh{font-size:19px;font-weight:700;color:var(--navy);border-top:2px solid var(--navy);padding-top:10px;margin-bottom:8px}.tll li{font-size:16.5px;line-height:1.6;word-break:keep-all}.tll.big li{font-size:20px;line-height:1.65}.tll.big li+li{margin-top:16px}.ppn{font-size:15.5px;line-height:1.6;word-break:keep-all}
"""
head_end = base.index('<div id="stage">')
head = base[:head_end].replace("<title>" + re.search(r"<title>(.*?)</title>", base).group(1) + "</title>", "<title>2부 연구모형</title>", 1)
head = re.sub(r'@font-face\{[^}]*\}', "", head)
text = re.sub(r"<[^>]+>|data:[^\"']+", " ", "".join(S))
head = head.replace("<style>", "<style>" + face(html.unescape(text) + "0123456789·→①②③") + CSS2, 1)
tail = base[base.index('</div><div id="notes">'):]
out = head + '<div id="stage">\n' + "\n".join(S) + "\n" + tail
assert out.count('<section class="slide') == len(S) == 11 and "@font-face" in out
open(os.path.join(H, "week11_part2.html"), "w", encoding="utf-8").write(out)
print("week11_part2.html", len(out) // 1024, "KB", len(S), "장")
