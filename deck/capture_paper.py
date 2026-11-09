# -*- coding: utf-8 -*-
"""논문 PDF에서 캡처: deck/captures_part1.json 의 항목마다 (pdf 키, PDF 쪽, 검색 문자열들) → 문자열들의 합집합 상자에 여백을 두고 2.5배로 잘라 deck/fig_part1/<id>.png.
spec 항목: {"id": "krishna_t2", "pdf": "01_krishna", "page": 9, "find": ["Table 2", "Adjusted R"], "pad": [20, 10, 20, 10], "full_width": true}
- find 문자열이 하나도 안 잡히면 그 쪽 전체를 저장하고 경고. full_width면 좌우를 본문 폭으로 넓힌다.
실행: python deck/capture_paper.py  (spec이 없으면 예시 spec을 만들어 둔다)"""
import json, os, sys, io
import pymupdf
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "fig_part1"); os.makedirs(OUT, exist_ok=True)
SRC = r"C:/Users/ojh12/OneDrive/Desktop/사회자본과 공공정책 읽어야 할 페이퍼/11주차"
PDF = {"01_krishna": "How does social capital grow_ A seven-year study of villages in India.pdf",
       "02_freitag": "Bowling the State Back in_Political Institutions and the Creation of Social Capital.pdf",
       "03_lw": "Social Capital and Local Governance_Exploring the Institutional Design Variable.pdf",
       "04_mettler": "Bringing the State Back In to Civic Engagement_ Policy Feedback Effects of the G.I. Bill for World War II Veterans.pdf",
       "05_kr": "Making And Breaking Social Capital_The Impact of Welfare-state Institutions.pdf"}
SPEC = os.path.join(H, "captures_part1.json")
if not os.path.exists(SPEC):
    json.dump([{"id": "krishna_t2", "pdf": "01_krishna", "page": 9, "find": ["TABLE 2"], "pad": [16, 12, 16, 12], "full_width": True}], open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("예시 spec 생성:", SPEC)
docs = {}
for it in json.load(open(SPEC, encoding="utf-8")):
    k = it["pdf"]; docs.setdefault(k, pymupdf.open(os.path.join(SRC, PDF[k]))); d = docs[k]
    pg = d[it["page"] - 1]; rects = []
    for q in it["find"]:
        rs = pg.search_for(q)
        if not rs: print(f"  [{it['id']}] 못 찾음: {q!r} (쪽 {it['page']})")
        rects += rs
    if it.get("to"):  # 끝 문자열까지: find 첫 상자 위에서 to 상자 아래까지
        rs = pg.search_for(it["to"]); rects += rs
    pr = pg.rect
    if rects:
        x0 = min(r.x0 for r in rects); y0 = min(r.y0 for r in rects); x1 = max(r.x1 for r in rects); y1 = max(r.y1 for r in rects)
        pl, pt, prr, pb = it.get("pad", [16, 12, 16, 12])
        if it.get("full_width"):
            x0, x1 = pr.x0 + 36, pr.x1 - 36
        clip = pymupdf.Rect(max(pr.x0, x0 - pl), max(pr.y0, y0 - pt), min(pr.x1, x1 + prr), min(pr.y1, y1 + pb))
    else:
        clip = pr; print(f"  [{it['id']}] 쪽 전체 저장")
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), clip=clip, alpha=False)
    p = os.path.join(OUT, it["id"] + ".png"); pix.save(p); print(it["id"], f"{pix.width}x{pix.height}", os.path.getsize(p) // 1024, "KB")
