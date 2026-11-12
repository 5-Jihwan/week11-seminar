# -*- coding: utf-8 -*-
"""1부 발표 대본(Word). 원본은 deck/part1_script.json이고 덱의 노트(N 키)도 같은 파일에서 만든다.
실행: python docs/build_script.py → docs/대본_11주차_1부.docx"""
import json, os, sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
NAVY, GRAY = RGBColor(0x07, 0x2A, 0x60), RGBColor(0x5a, 0x65, 0x77)
S = json.load(open(os.path.join(H, "..", "deck", "part1_script.json"), encoding="utf-8"))
main = [x for x in S if not x["title"].endswith("원문")]; ap = [x for x in S if x["title"].endswith("원문")]
chars = sum(len(p) for x in main for p in x["paras"] if not p.startswith("("))

d = Document()
for s in d.sections: s.left_margin = s.right_margin = Cm(2.4); s.top_margin = s.bottom_margin = Cm(2.2)
st = d.styles["Normal"]; st.font.name = "맑은 고딕"; st.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕"); st.font.size = Pt(10.5)


def P(text, size=None, bold=False, color=None, italic=False, after=6, keep=False):
    p = d.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.line_spacing = 1.45; p.paragraph_format.keep_with_next = keep
    return p


P("발표 대본 — 사회자본과 공공정책 11주차 1부", 17, True, NAVY, after=2)
P(f"본편 {len(main)}장 + 부록 {len(ap)}장 · 말하는 분량 약 {round(chars, -2):,}자 · 2026-11-13 · 오지환", 10.5, color=GRAY, after=10)
P("덱에서 N 키를 누르면 나오는 노트와 같은 내용이고, 그대로 읽어도 되게 썼습니다. 괄호 안은 말하지 않는 진행 표시입니다. 가려 둔 항목은 → 키를 누를 때 하나씩 나오고, 토론 장에서는 손들기가 끝난 뒤에 키를 눌러 논문의 결과를 보입니다. 토론은 논문마다 두 번인데 첫 번째는 5분, 두 번째는 2분으로 잡았습니다.", after=14)
for k, x in enumerate(S, 1):
    P((f"{k}. " if x in main else f"부록 A{ap.index(x) + 1}. ") + x["title"], 12, True, NAVY, after=3, keep=True)
    for p in x["paras"]:
        if p.startswith("("): P(p, 9.5, italic=True, color=GRAY, after=4)
        else: P(p)
out = os.path.join(H, "대본_11주차_1부.docx"); d.save(out); print(out, "| 본편", len(main), "장 | 말하는 분량", chars, "자")
