# -*- coding: utf-8 -*-
r"""SLNA 연구 기획서(Word). 실행: python docs/build_slna_plan.py → Downloads\02_원고\사회자본과 공공정책(수업·중간과제)\SLNA_연구기획서_YYYYMMDD.docx"""
import csv, datetime, os, sys, collections
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
TODAY = datetime.date.today(); OUT = os.path.join(os.path.expanduser("~"), "Downloads", "02_원고", "사회자본과 공공정책(수업·중간과제)", f"SLNA_연구기획서_{TODAY:%Y%m%d}.docx")
NAVY = RGBColor(0x1E, 0x3A, 0x5F)

# 코퍼스 현황(studies.csv에서)
S = list(csv.DictReader(open(os.path.join(ROOT, "corpus", "studies.csv"), encoding="utf-8-sig")))
kci = [x for x in S if x["src"] == "kci"]; oa = [x for x in S if x["src"] == "openalex"]
yrs = sorted(int(x["year"][:4]) for x in kci if x["year"][:4].isdigit())
n = {"kci": len(kci), "oa": len(oa), "kci_comp": sum(1 for x in kci if x["dv_components"]), "oa_comp": sum(1 for x in oa if x["dv_components"]),
     "kci_dv": sum(1 for x in kci if x["sc_dv"]), "oa_dv": sum(1 for x in oa if x["sc_dv"]), "kci_data": sum(1 for x in kci if x["data"]), "oa_data": sum(1 for x in oa if x["data"]),
     "kci_y": f"{yrs[0]}~{yrs[-1]}" if yrs else "-", "seeds": sum(1 for x in S if x.get("seeds"))}

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Malgun Gothic"; st.font.size = Pt(10.5); st.element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2.2)

def para(t, size=10.5, bold=False, color=None, align=None, after=4, italic=False):
    p = doc.add_paragraph(); r = p.add_run(t); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.name = "Malgun Gothic"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
    if color: r.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.line_spacing = 1.25; return p
def H1(t): para(t, 14, True, NAVY, after=6).paragraph_format.space_before = Pt(16)
def H2(t): para(t, 11.5, True, NAVY, after=3).paragraph_format.space_before = Pt(8)
def P(t): para(t)
def UL(items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet"); r = p.add_run(it); r.font.size = Pt(10.5); r.font.name = "Malgun Gothic"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic"); p.paragraph_format.space_after = Pt(2)
def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexc); tcPr.append(sh)
def TBL(rows, widths=None, size=9):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.text = ""; p = c.paragraphs[0]; r = p.add_run(str(v)); r.font.size = Pt(size); r.font.name = "Malgun Gothic"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Malgun Gothic")
            if i == 0: r.bold = True; shade(c, "EEF2F7")
            if widths: c.width = Cm(widths[j])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ── 표지 ──
para("연구 기획서", 11, color=NAVY, after=2)
para("사회자본을 종속변수로 둔 연구의 지식 구조", 20, True, after=2)
para("체계적 문헌 네트워크 분석(SLNA): 국내 2002~2026 · 해외 1976~2026", 13, after=14)
para(f"오지환 · 성균관대학교 행정학과 석사과정 · {TODAY:%Y년 %m월 %d일} · 초안 v1", 10, color=RGBColor(0x5C, 0x62, 0x6D), after=20)

H1("요약")
P("사회자본 연구에서 사회자본은 대개 원인이었다. 이 연구는 사회자본을 결과로 둔 양적 연구만 체계적으로 모아, 그 연구들이 어떤 지식 계보를 따라 발전했고 어떤 군집으로 나뉘며 국내 연구가 그 구조의 어디에 있는지를 인용망으로 본다. "
  "자료는 KCI 전수(2002~2026)와 OpenAlex 전수(1976~2026)에서 규칙과 LLM으로 거른 양적 연구 코퍼스이고, 각 논문에 종속변수 구성 요소·종속 차원(인지·구조)·원인 축(사회·제도·개인·지역)·자료·단위·설계를 코딩한다. "
  "분석은 직접 인용망, 주경로(main path), 서지결합 군집, 공어망 넷이다. 핵심 질문은 \"국내 연구의 조작적 정의는 이론이 정하는가, 가용 자료가 정하는가\"이며, 11주차 발제에서 쓴 수집·코딩 파이프라인과 캔버스를 그대로 연구 도구로 쓴다.")

H1("1. 배경과 목적")
H2("1.1 문제")
P("Putnam(1993) 이후 사회자본은 민주주의·정부 성과·성장·건강의 원인으로 다루어졌다. 1996년 Levi, Tarrow, Foley & Edwards, Skocpol이 \"국가는 어디 갔나\"를 물은 뒤 사회자본을 결과로 두는 연구가 생겼고, 정치학 계보(Krishna 2007, Freitag 2006, Lowndes & Wilson 2001)와 정책환류 계보(Mettler 2002, Kumlin & Rothstein 2005)로 갈라졌다. 그러나 이 종속변수 연구들이 하나의 지식 공동체인지, 몇 개의 섬인지, 그리고 국내 연구가 그 안에 있는지는 계량적으로 확인된 바 없다.")
H2("1.2 왜 SLNA인가")
P("체계적 문헌 고찰은 포함 기준을 명시해 코퍼스를 만들고, 인용망 분석은 그 코퍼스 안의 관계를 구조로 보여 준다(Colicchia & Strozzi 2012). 둘을 합치면 \"누가 누구를 읽었는가\"와 \"무엇을 어떻게 쟀는가\"를 한 자료에서 교차할 수 있다. 이 연구의 차별점은 인용망 위에 우리가 코딩한 측정 속성(구성 요소·차원·원인 축·자료)을 얹는 것이다. 군집이 이론으로 갈리는지 자료로 갈리는지가 거기서 드러난다.")
H2("1.3 목적")
UL(["사회자본을 종속변수로 둔 양적 연구의 코퍼스를 국내·해외 전수로 만들고 측정 구조를 코딩한다.",
    "인용망의 주경로와 군집을 찾고, 군집을 분류 틀(원인 축 × 종속 차원)과 대조한다.",
    "국내 연구가 해외 핵심을 인용하는지, 국내끼리 닫혀 있는지, 조작적 정의가 자료에 종속되는지를 본다."])

H1("2. 연구질문")
TBL([["번호", "질문", "자료·분석", "예상되는 두 답"],
     ["RQ1", "사회자본을 종속변수로 둔 연구는 어떤 지식 계보를 따라 발전했나", "직접 인용망 + 주경로(SPC)", "제도 중심 한 줄기(Levi→Rothstein) / 두 줄기(제도·사회)가 1990년대 말 갈라짐"],
     ["RQ2", "인용망 군집은 분류 틀의 칸과 겹치는가", "서지결합 군집 × 코딩 속성 교차", "겹침(틀이 공동체 구조 반영) / 안 겹침(군집은 자료·학문 분야로 갈림)"],
     ["RQ3", "국내 연구는 해외 핵심을 인용하는가, 섬인가", "국내↔해외 인용 비율, 외부 닻 인용", "해외 핵심 인용 / 국내 선행연구끼리 닫힘"],
     ["RQ4", "국내의 조작적 정의는 이론이 정하는가, 가용 자료가 정하는가", "자료별 구성 요소 분포, 자료 도입 연도 전후 비교", "자료가 정함(사회통합실태조사 2013 이후 단일 신뢰 문항 급증) / 이론이 정함"]], widths=[1.2, 5.2, 4.2, 6.0])

H1("3. 자료")
H2("3.1 코퍼스 현황 (11-06 기준)")
TBL([["층", "국내(KCI)", "해외(OpenAlex)", "비고"],
     ["수집 범위", "등재지 전체 훑기, 제목·초록에 사회자본, 발행 1996 이후", "제목에 social capital(+신뢰·시민참여 제목은 초록에 사회자본 있을 때), 초록 있는 article", "국내는 완료, 해외는 2020~2026 완료·1976~2019 수집 중"],
     ["사회자본 논문", "5,065", "8,638(부분)", "해외 전체는 약 2만 편 예상"],
     ["양적 연구(규칙)", f"{n['kci']}", f"{n['oa']}(부분)", "양적 단서 2종 이상, 서평·고찰 제외"],
     ["구성 요소 코딩됨", f"{n['kci_comp']}", f"{n['oa_comp']}", "규칙 코딩, 미검수"],
     ["종속 단서", f"{n['kci_dv']}", f"{n['oa_dv']}", "\"결정요인·형성·영향\" 문구. LLM 코딩으로 확정 예정"],
     ["자료명 잡힘", f"{n['kci_data']}", f"{n['oa_data']}", "초록에 조사명이 있는 것만"],
     ["연도", n["kci_y"], "2020~2026(부분)", "KCI 서지는 2002년 이전이 거의 없음"]], widths=[3.0, 4.2, 4.6, 4.8])
H2("3.2 포함·제외 기준")
UL(["포함: 사회자본(또는 그 구성 요소인 신뢰·참여·호혜·연결망)이 종속변수인 양적 연구. 개인·지역·국가 단위 모두.",
    "제외: 사회자본이 독립·매개로만 쓰인 연구, 서평·개념 논문·메타분석, 초록 없는 문헌, 학위논문(RISS 미포함).",
    "경계: KCI 등재지와 OpenAlex 색인 학술지. 단행본·보고서는 외부 닻으로만 들어온다."])
H2("3.3 더 받을 자료")
TBL([["자료", "출처", "왜", "방법·조건"],
     ["참고문헌 목록(해외)", "OpenAlex referenced_works", "코퍼스 안 인용 엣지", "OpenAlex 키(무료). 약 2만 편, 반나절"],
     ["참고문헌 목록(국내)", "KCI 오픈 API kci_references", "국내 인용 엣지", "KCI 인증키(무료, 신청 필요)"],
     ["외부 닻", "코퍼스 밖 피인용 상위 50편", "경계 효과 완화", "Putnam 1993·Coleman 1988·Rothstein & Stolle 2008 등을 노드로"],
     ["검수 표본", "층화 200편(국내 100·해외 100)", "LLM 코딩 일치율", "연구자 손 코딩, 2명이면 더 좋음"]], widths=[3.4, 3.8, 3.6, 5.8])

H1("4. 코딩 틀")
H2("4.1 변수")
TBL([["변수", "값", "출처·방법"],
     ["종속 구성 요소", "일반신뢰 · 기관신뢰 · 이웃 신뢰 · 단체 참여 · 봉사·기부 · 연결망 · 호혜 · 정치 참여(복수)", "규칙 → Haiku 5.5(초록) → 표본 검수"],
     ["종속 차원", "인지적 · 구조적 · 둘 다 (Uphoff)", "구성 요소에서 유도"],
     ["원인 축", "사회 중심 · 제도 중심 · 개인 자원 · 지역 맥락 (Hooghe & Stolle 2003 + 2)", "독립변수 단서에서"],
     ["자료", "조사명(사회통합실태조사·복지패널·WVS·ESS 등)", "초록 패턴"],
     ["단위·설계", "개인·지역·국가·다수준 / 횡단·패널·준실험·실험", "초록 패턴"],
     ["매개·조절", "있음·없음", "초록 패턴"],
     ["국가·연도·학술지·피인용", "서지", "KCI·OpenAlex"]], widths=[3.4, 8.2, 5.0])
H2("4.2 분류 틀")
P("원인 축(행) × 종속 차원(열)의 격자. 11주차 다섯 편은 제도 중심 행에 넷(Freitag·Mettler 구조, K&R 인지, L&W 둘 다), 사회·지역 행에 하나(Krishna 둘 다)가 꽂힌다. 군집 분석 결과를 이 격자에 사상해 RQ2에 답한다.")
H2("4.3 코딩 품질")
UL(["규칙 코딩은 넓게 잡는다(국내 '연결망' 621편은 과다). LLM 코딩이 최종이고, 모델은 claude-haiku-5-5로 고정, 프롬프트와 스키마를 부록에 싣는다.",
    "검수 표본 200편으로 변수별 일치율(Cohen's κ)을 보고한다. κ < .6인 변수는 분석에서 빼거나 손 코딩으로 바꾼다.",
    "\"사회자본이 종속\" 판정이 가장 중요하다. 이것만은 표본을 300편으로."])

H1("5. 분석 설계")
TBL([["분석", "입력", "방법", "산출"],
     ["① 직접 인용망", "코퍼스 내 인용 + 외부 닻", "연결 성분, 밀도, 국내↔해외 인용 행렬", "그림 1 전체 망(국내 테두리), 표: 국내→해외·국내→국내 비율"],
     ["② 주경로", "①의 비순환 그래프", "SPC 가중 주경로(Hummon & Doreian), 1990 이후", "그림 2 등뼈. 다섯 편이 등뼈 위에 있는지"],
     ["③ 군집", "서지결합(공유 참고문헌) 또는 공인용", "Louvain, 해상도 민감도", "군집 × 코딩 속성 교차표, 격자 사상(그림 3)"],
     ["④ 공어망", "제목·초록 용어(국·영문 따로)", "동시출현, 군집", "조작화 어휘 지도(그림 4), 자료명과의 동시출현"],
     ["⑤ 시계열", "연도 × 구성 요소 × 자료", "자료 도입 연도 전후 비교(국내)", "그림 5 국내 조작적 정의의 변화"]], widths=[2.6, 4.0, 4.6, 5.4])
P("도구는 파이썬 networkx·igraph이며 주경로와 군집은 직접 구현한다(각 50줄 안팎). 그림은 11주차 대시보드의 그물망과 같은 방식으로 그려 발표와 논문에 함께 쓴다.")

H1("6. 산출물")
UL(["논문 1편: 국내 학술지(행정학·정책학) 목표. 제목 가안 \"사회자본을 종속변수로 둔 연구의 지식 구조: 국내·해외 인용망과 조작적 정의\".",
    "공개 자료: 코퍼스 서지·코딩 표(초록 제외), 코드(수집·거르기·코딩·망 분석), 검수 표본과 일치율.",
    "수업 도구: 11주차 캔버스의 선행연구 비교가 이 코퍼스를 쓴다. 검수 뒤 수업판(verified)을 갱신한다."])

H1("7. 일정")
TBL([["주", "일", "산출"],
     ["세미나 전(~11-13)", "해외 수집 완료, 규칙 코딩, 캔버스 반영", "코퍼스 v1"],
     ["1주차", "OpenAlex 참고문헌 수집(키), KCI 참고문헌 수집(키), 외부 닻 선정", "인용 엣지 표"],
     ["1주차", "Haiku 코딩 배치, 검수 표본 추출·손 코딩", "코딩 표 v2, κ"],
     ["2주차", "인용망·군집·주경로·공어망", "그림 1~5, 표"],
     ["2주차", "해석, 초고", "초고 v1"],
     ["3주차", "교수님 검토, 수정", "투고본"]], widths=[3.2, 9.0, 4.4])

H1("8. 한계와 대응")
TBL([["한계", "대응"],
     ["코퍼스 안 인용만 세면 경계 효과가 크다", "외부 닻 50편을 노드로 넣고, 닻 인용 비율을 따로 보고"],
     ["OpenAlex 참고문헌은 2000년 이전이 성기다", "주경로는 1990 이후로 한정, 이전은 서술로"],
     ["KCI 인용은 등재지끼리만 잡힌다", "국내 '섬' 결과의 일부는 자료 한계임을 명시, 외부 닻으로 보정"],
     ["인용은 영향이지 동의가 아니다", "주경로 노드는 원문을 읽어 비판 인용을 표시"],
     ["규칙·LLM 코딩의 오류", "검수 표본과 κ 보고, 낮은 변수는 제외"],
     ["제목 기준 수집이 사회자본을 본문에서만 다룬 연구를 놓친다", "초록 검색 축을 보조로 두되 본 분석은 제목 축으로, 민감도 분석"]], widths=[7.0, 9.6])

H1("9. 필요한 것")
UL(["OpenAlex API 키(무료): 참고문헌 2만 편 수집. 없으면 하루 100번 제한으로 수 주.",
    "KCI 오픈 API 인증키(무료, 신청): 국내 참고문헌. 없으면 RQ3의 국내 인용은 불가.",
    "Anthropic API 키: Haiku 5.5 배치 코딩. 1만 편에 약 10달러.",
    "검수 손 코딩 시간: 200~300편, 편당 2~3분, 10시간 안팎. 2인이면 κ가 더 의미 있다."])

H1("부록 A. 파이프라인 파일")
TBL([["파일", "역할"],
     ["corpus/harvest_kci.py", "KCI OAI 전수 수집(커서 토큰, 워커 병렬, 체크포인트)"],
     ["corpus/harvest_openalex.py", "OpenAlex 연도×축 수집(체크포인트, 무한 재시도, 키 지원)"],
     ["corpus/screen_quant.py", "양적 연구 거르기"],
     ["corpus/code_rules.py", "규칙 코딩 → studies.csv"],
     ["corpus/code_studies.py", "Haiku 5.5 배치 코딩(같은 스키마)"],
     ["(예정) corpus/fetch_refs.py", "참고문헌 수집(OpenAlex·KCI)"],
     ["(예정) corpus/slna.py", "인용망·주경로·군집·공어망, 그림"],
     ["model/build_canvas.py", "코퍼스를 수업 캔버스·대시보드에 심기"]], widths=[5.2, 11.4])
H1("부록 B. 참고문헌(틀)")
UL(["Colicchia, C., & Strozzi, F. (2012). Supply chain risk management: a new methodology for a systematic literature review. Supply Chain Management, 17(4), 403–418.",
    "Hummon, N. P., & Doreian, P. (1989). Connectivity in a citation network: The development of DNA theory. Social Networks, 11(1), 39–63.",
    "Hooghe, M., & Stolle, D. (Eds.). (2003). Generating Social Capital: Civil Society and Institutions in Comparative Perspective. Palgrave.",
    "Uphoff, N. (2000). Understanding social capital: Learning from the analysis and experience of participation. In Dasgupta & Serageldin (Eds.), Social Capital: A Multifaceted Perspective. World Bank.",
    "Kumlin, S., & Rothstein, B. (2005). Making and breaking social capital: The impact of welfare-state institutions. Comparative Political Studies, 38(4), 339–365."])

os.makedirs(os.path.dirname(OUT), exist_ok=True); doc.save(OUT); print("saved", OUT)
