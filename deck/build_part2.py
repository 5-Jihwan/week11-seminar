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

slide("2부 진행 방식", "",
      f'''<div class="two" style="grid-template-columns:auto 1fr;gap:48px;align-items:center"><div class="qr"><img src="{qr_uri(CANVAS)}" alt="캔버스 주소 QR"><div class="url">5-jihwan.github.io/week11-seminar/model/canvas.html</div></div>
<div><p class="whyq" style="margin-top:0">국내 공개 조사 여덟 가지 가운데 하나를 골라, 사회자본을 종속변수로 둔 연구모형을 각자 하나씩 만든다. 다 만들면 제출하고, 모인 모형을 대시보드로 함께 본다.</p>
<ul class="tll" style="margin-top:18px"><li>노트북이 편하고, 폰은 문항 카드의 ＋ 버튼으로 만든다</li><li>이름 대신 별명을 쓴다. 낸 모형은 수업이 끝나면 지운다</li><li>원자료와 계수 추정은 없고, 조사표 문항으로 모형을 그리는 데까지 한다</li></ul></div></div>''',
      "", "진행은 단순하게 하려고 합니다. 국내 공개 조사 여덟 가지 가운데 하나를 골라서 사회자본을 종속변수로 둔 연구모형을 각자 하나씩 만들고, 다 만드시면 제출해 주시면 됩니다. 모인 모형은 마지막에 대시보드로 같이 보겠습니다. 왼쪽 QR로 들어오시면 되는데 노트북이 편하고, 폰에서도 문항 카드에 있는 더하기 버튼으로 만들 수 있습니다. 이름 대신 별명을 써 주시고, 오늘 내신 모형은 이 수업 안에서만 보고 수업이 끝나면 서버에서 지우겠습니다. 원자료로 계수를 내는 단계는 없고 조사표 문항으로 모형을 그리는 데까지만 합니다.")

build = [("조사표 문항", "5,636개", "국내 공개 조사 8종의 조사표와 코드북에서 문항 문구를 옮겼다. 원자료는 쓰지 않는다. 자주 쓰는 문항 108개는 신뢰·참여·연결망 같은 개념 20개로 묶었다"),
         ("선행연구", "7,690편", "국내는 KCI(1996년 이후), 해외는 OpenAlex(1976년 이후)에서 사회자본·신뢰·시민참여를 다룬 양적 연구를 모았다. 초록을 Claude Haiku로 읽혀 자료, 분석 단위, 설계, 종속변수 구성 요소, 원인을 코딩했다. 사람이 검수하기 전이다"),
         ("비교 규칙", "모형 ↔ 선행연구", "내 모형의 종속변수 구성 요소와 원인을 선행연구의 같은 칸과 맞대어, 겹치는 정도로 닮은 연구를 고른다. 분류 틀은 Hooghe &amp; Stolle(2003)의 원인 축과 Uphoff의 인지·구조 차원")]
slide("실습 화면을 만든 자료와 구조", "조사표 문항, 선행연구, 비교 규칙",
      '<div class="b3">' + "".join(f"<div><span>{a}</span><b>{n}</b><p>{d}</p></div>" for a, n, d in build) + '''</div>
<p class="ppn" style="margin-top:18px">AI 코딩 기준으로 선행연구의 약 83%가 한 시점 자료였고, 같은 사람을 여러 번 조사한 패널 연구는 851편이었다.</p>''',
      "선행연구 수는 중복을 뺀 캔버스 기준. 코딩은 AI가 했고 사람 검수 전.",
      "들어가시기 전에 이 화면이 무엇으로 만들어졌는지 말씀드리겠습니다. 왼쪽은 문항인데, 국내 공개 조사 여덟 가지의 조사표와 코드북에서 문항 문구 5,636개를 옮겨 왔고 원자료는 쓰지 않았습니다. 그 가운데 자주 쓰는 문항 108개는 신뢰나 참여, 연결망 같은 개념 스무 개로 묶어서 먼저 보이게 했습니다. 가운데는 선행연구로, 국내는 KCI에서 1996년 이후 논문을, 해외는 OpenAlex에서 1976년 이후 논문을 모아 사회자본과 신뢰, 시민참여를 다룬 양적 연구 7,690편을 추렸습니다. 이 논문들의 초록을 Claude Haiku로 읽혀서 어떤 자료를 썼는지, 분석 단위와 설계가 무엇인지, 종속변수와 원인으로 무엇을 넣었는지를 칸마다 코딩했는데, 사람이 하나하나 검수하지는 못했습니다. 오른쪽이 둘을 잇는 규칙으로, 여러분이 만든 모형의 종속변수 구성 요소와 원인을 선행연구의 같은 칸과 맞대어 겹치는 정도로 닮은 연구를 골라 줍니다. 코딩해 보니 선행연구의 83% 정도가 한 시점 자료였습니다.")

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

slide("모형 만드는 동안", "약 20분",
      '''<ul class="tll big"><li>처음에 적은 정의와 종속변수로 고른 문항이 같은 것을 가리키는가. 어긋나면 오른쪽 「개념화·조작화」 탭에 표시된다</li>
<li>원인으로 놓은 것이 사회자본보다 먼저 생기는가</li>
<li>막히면 종속변수 하나와 원인 하나만 이어 먼저 낸다. 다시 내면 마지막 것만 센다</li></ul>''',
      "", "작업하시는 동안 이 화면을 띄워 두겠습니다. 만들다가 한 번씩 확인해 주셨으면 하는 것은, 처음에 적은 정의와 종속변수로 고른 문항이 같은 것을 가리키는지, 그리고 원인으로 놓은 것이 정말 사회자본보다 먼저 생기는지입니다. 앞의 것은 어긋나면 오른쪽 개념화 탭에 표시가 됩니다. 막히시면 종속변수 하나와 원인 하나만 이어서 먼저 내 주시고, 다시 내시면 마지막 것만 셉니다.")

slide("연구로 옮길 때 쓸 수 있는 설계", "2부 정리",
      '''<ul class="tll big"><li>같은 사람을 여러 해 따라가는 패널: 한국복지패널</li>
<li>제도가 바뀐 전후 비교: 한국 아동수당은 2018년 9월 소득 하위 90%로 시작해 2019년 1월 소득 심사를 없앴다</li>
<li>지역 사이 비교: 지역사회건강조사의 시군구</li></ul>''',
      "", "정리하겠습니다. 오늘 내신 모형은 방금 대시보드로 같이 봤고, 마지막으로 오늘 만든 모형을 실제 연구로 옮길 때의 이야기를 하겠습니다. 국내 공개 자료 대부분이 한 시점 자료라서 원인과 결과의 순서를 가르기 어렵고, 앞에서 말씀드린 대로 선행연구의 83% 정도도 한 시점 자료였습니다. Kumlin과 Rothstein이 스스로 한계로 적은 것도 이 문제였습니다. 화면에 적은 것처럼 한국복지패널은 같은 사람을 여러 해 따라가고, 아동수당은 같은 급여가 선별에서 보편으로 바뀌어서 전후를 비교할 수 있고, 지역사회건강조사는 시군구끼리 비교할 수 있습니다. 저는 오늘 만든 모형에 이 가운데 하나를 붙이면 1부에서 본 한계를 조금 줄일 수 있다고 봅니다.")

cover("감사합니다", "1부와 2부에 함께해 주셔서 감사합니다.", "사회자본과 공공정책 · 11주차 발제 · 오지환(석사과정 2학기)",
      "오늘 1부와 2부에 끝까지 함께해 주셔서 감사합니다. 내신 모형은 말씀드린 대로 수업이 끝나면 서버에서 지우겠습니다. 이것으로 11주차 발제를 마치겠습니다.")

run = [("2:15", "표지 → 준비한 이유 → 진행 방식(QR) → 실습을 만든 자료와 구조", "별명과 「끝나면 지운다」를 말로. 대시보드 「작업 중」 수가 오르는지"),
       ("2:22", "자료 → 만드는 순서 → 만드는 동안(띄워 둠)", "약 20분. 돌아다니며 막힌 사람 옆에. 끝나기 3분 전에 「종속변수 하나와 원인 하나만 이어도 제출됩니다」"),
       ("2:42", "대시보드(프로젝터 모드)", "자료·종속변수 막대와 연결망을 함께 보며 두세 분께 가볍게 고른 이유. 모형을 띄울 때는 선행연구를 제목과 자료만, 「검수 전」"),
       ("2:52", "연구로 옮길 때 쓸 수 있는 설계", "대시보드에서 본 것을 한두 문장으로"),
       ("2:57", "감사합니다", "")]
slide("2부 진행표", "부록 · 발표자용",
      '<table style="font-size:14.5px;word-break:keep-all"><tr><th style="width:9%">시각</th><th style="width:38%">화면</th><th>할 일</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in run) + '''</table>
<p class="ppn" style="margin-top:14px">1부가 늦게 끝나면 만들기 시간을 줄이고 대시보드는 막대만 본다. 만들기가 끝날 때 제출이 다섯 명보다 적으면 3분 더 준다.</p>''',
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
.b3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.b3>div{border-top:3px solid var(--navy);background:var(--navyt);padding:14px 16px;word-break:keep-all}.b3 span{font-size:14px;color:var(--sub)}.b3 b{display:block;font-size:26px;color:var(--navy);margin:2px 0 8px}.b3 p{font-size:15.5px;line-height:1.6;margin:0}
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
