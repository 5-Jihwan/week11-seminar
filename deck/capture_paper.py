# -*- coding: utf-8 -*-
"""논문 PDF에서 캡처: deck/captures_part1.json 의 항목마다 잘라서 deck/fig_part1/<id>.png (2.5배).
자르는 방법은 둘 중 하나.
  region: [x0, y0, x1, y1]  쪽 크기 대비 비율. 표처럼 경계가 분명한 것.
  find: ["시작 구절", ...] (+ to: "끝 구절", ctx: 앞뒤로 더 넣을 줄 수)  구절이 든 줄부터 끝 구절이 든 줄까지를 줄 경계에 맞춰 자른다.
      좌우는 그 구절이 속한 문단(단) 폭. 줄 중간에서 잘리지 않는다.
강조(그림에 찍지 않고 위치를 fig_part1/hl.json에 저장. 덱이 그 위에 형광펜을 긋는다):
  hl: ["구절", ...]     그 구절에 형광펜(여러 줄에 걸쳐도 됨).
  hlrow: ["행 이름", ...]  표에서 그 행 전체에 형광펜.
그 밖: pad [왼,위,오,아래](pt, find 방식에서만, 기본 2·1·2·1), rotate(가로로 인쇄된 표는 -90).
실행: python deck/capture_paper.py [id ...]   (id를 주면 그것만)"""
import json, os, sys, io
import pymupdf
from PIL import Image, ImageOps
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "fig_part1"); os.makedirs(OUT, exist_ok=True)
SRC = r"C:/Users/ojh12/OneDrive/Desktop/사회자본과 공공정책 읽어야 할 페이퍼/11주차"
PDF = {"01_krishna": "How does social capital grow_ A seven-year study of villages in India.pdf",
       "02_freitag": "Bowling the State Back in_Political Institutions and the Creation of Social Capital.pdf",
       "03_lw": "Social Capital and Local Governance_Exploring the Institutional Design Variable.pdf",
       "04_mettler": "Bringing the State Back In to Civic Engagement_ Policy Feedback Effects of the G.I. Bill for World War II Veterans.pdf",
       "05_kr": "Making And Breaking Social Capital_The Impact of Welfare-state Institutions.pdf"}
SPEC = os.path.join(H, "captures_part1.json")
Z = 2.5


def text_lines(pg):
    """쪽의 글줄 상자 목록."""
    d = {}
    for x0, y0, x1, y1, _w, b, l, _n in pg.get_text("words"):
        r = d.setdefault((b, l), [x0, y0, x1, y1]); r[0] = min(r[0], x0); r[1] = min(r[1], y0); r[2] = max(r[2], x1); r[3] = max(r[3], y1)
    return sorted((pymupdf.Rect(*v) for v in d.values()), key=lambda r: (r.y0, r.x0))


def clip_for(pg, it):
    pr = pg.rect
    if it.get("region"):
        f = it["region"]; return pymupdf.Rect(pr.x0 + pr.width * f[0], pr.y0 + pr.height * f[1], pr.x0 + pr.width * f[2], pr.y0 + pr.height * f[3])
    found = []
    for q in it.get("find", []) + ([it["to"]] if it.get("to") else []):
        rs = pg.search_for(q)
        if not rs: print(f"  [{it['id']}] 못 찾음: {q!r} (PDF {it['page']}쪽)")
        found += rs
    if not found:
        print(f"  [{it['id']}] 쪽 전체 저장"); return pr
    pl, pt, prr, pb = it.get("pad", [2, 1, 2, 1])  # 줄 경계에 바짝 붙여 자른다(옆 줄이 비치지 않게). 여백은 저장할 때 흰 테두리로
    blocks = [pymupdf.Rect(b[:4]) for b in pg.get_text("blocks") if b[6] == 0]
    col = [b for b in blocks if any(b.intersects(r) for r in found)]
    cx0, cx1 = min(b.x0 for b in col), max(b.x1 for b in col)
    lines = [l for l in text_lines(pg) if l.x0 >= cx0 - 3 and l.x1 <= cx1 + 3]
    y0, y1 = min(r.y0 for r in found), max(r.y1 for r in found)
    idx = [i for i, l in enumerate(lines) if y0 - 1 <= (l.y0 + l.y1) / 2 <= y1 + 1]
    a, b = max(0, idx[0] - it.get("ctx", 0)), min(len(lines) - 1, idx[-1] + it.get("ctx", 0))
    return pymupdf.Rect(max(pr.x0, cx0 - pl), max(pr.y0, lines[a].y0 - pt), min(pr.x1, cx1 + prr), min(pr.y1, lines[b].y1 + pb))


def hl_boxes(pg, clip, it):
    """형광펜 상자(PDF 좌표). 읽는 순서로 정렬한다."""
    boxes = []
    for q in it.get("hl", []):
        rs = pg.search_for(q, clip=clip)
        if not rs: print(f"  [{it['id']}] 강조 구절 못 찾음: {q!r}")
        boxes += [(r.x0, r.y0, r.x1, r.y1) for r in rs]
    for q in it.get("hlrow", []):
        rs = pg.search_for(q, clip=clip)
        if not rs: print(f"  [{it['id']}] 강조 행 못 찾음: {q!r}")
        boxes += [(clip.x0 + 3, r.y0, clip.x1 - 3, r.y1) for r in rs[:1]]
    return sorted(boxes, key=lambda b: (round(b[1]), b[0]))


HLF = os.path.join(OUT, "hl.json")
HL = json.load(open(HLF, encoding="utf-8")) if os.path.exists(HLF) else {}
only = set(sys.argv[1:]); docs = {}
for it in json.load(open(SPEC, encoding="utf-8")):
    if only and it["id"] not in only: continue
    k = it["pdf"]; docs.setdefault(k, pymupdf.open(os.path.join(SRC, PDF[k]))); pg = docs[k][it["page"] - 1]
    clip = clip_for(pg, it)
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=clip, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    bx, by = (0, 0) if it.get("region") else (16, 12)  # 줄 경계로 자른 캡처에는 흰 테두리를 두른다
    if bx: im = ImageOps.expand(im, border=(bx, by), fill="white")
    boxes = hl_boxes(pg, clip, it)
    assert not (boxes and it.get("rotate")), "돌린 표에는 형광펜을 쓰지 않는다"
    HL.pop(it["id"], None)
    if boxes: HL[it["id"]] = [[round(((x0 - clip.x0) * Z + bx - 2) / im.width, 4), round(((y0 - clip.y0) * Z + by - 1) / im.height, 4), round(((x1 - clip.x0) * Z + bx + 2) / im.width, 4), round(((y1 - clip.y0) * Z + by + 1) / im.height, 4)] for x0, y0, x1, y1 in boxes]
    if it.get("rotate"): im = im.rotate(it["rotate"], expand=True)  # 가로로 인쇄된 표
    p = os.path.join(OUT, it["id"] + ".png"); im.save(p)
    print(it["id"], f"{im.width}x{im.height}", os.path.getsize(p) // 1024, "KB", f"형광펜 {len(boxes)}" if boxes else "")
json.dump(HL, open(HLF, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
