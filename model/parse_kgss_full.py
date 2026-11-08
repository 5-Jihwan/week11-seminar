# -*- coding: utf-8 -*-
"""KGSS 2003-2025 누적 코드북(PyMuPDF 텍스트) → model/full_kgss.json {"kgss": [...]}.

블록 구조(코드북 본체 @@PAGE 38 ~ 가구원 특성 직전 @@PAGE 717):
  응답 범주 / 변수값03-08 2009 … 2025 전체 / (라벨, 변수값, 셀 13개)* / N … / 표N 제목 /
  [설문문항] … / [변수명] VAR / * 주석
연도 = 비해당(-1) 행을 뺀 어떤 행에서든 '-'가 아닌 셀이 있는 열. 03-08 묶음 열은
부록1 변수명 설문지(연도별 쪽머리)에서 변수명이 인쇄된 해로 푼다.
"""
import re, collections, json, os, re

H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "data", "codebooks", "kgss", "codebook_pymupdf.txt")
QNR = os.path.join(H, "..", "data", "codebooks", "kgss", "questionnaire_pymupdf.txt")
OUT = os.path.join(H, "full_kgss.json")
YEARS = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2016, 2018, 2021, 2023, 2025]
PAGE_FROM, PAGE_TO = 38, 717  # 제2부 1~4 (5. 가구원 특성 제외)
SKIP_VAR = re.compile(r"^FINALWT$|^ID$|^SAMPLEAB$|^YEAR$")


def theme(s):  # parse_kipa_full.py와 같은 규칙
    if re.search(r"신뢰|믿", s): return "TR"
    if re.search(r"단체|참여|모임|봉사|기부|투표|접촉|도움|교류|소통|친구|이웃", s): return "NW"
    if re.search(r"공정", s): return "FA"
    if re.search(r"복지|서비스|정부|제도|기관|지원|혜택|행정|정책|세금", s): return "IN"
    if re.search(r"지역|거주|동네|마을", s): return "RG"
    if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구", s): return "DM"
    return "ET"


def qnr_years():
    """부록1 설문지: 2003~2008 각 해에 변수명이 인쇄된 집합."""
    found, year = collections.defaultdict(set), None
    for ln in open(QNR, encoding="utf-8"):
        ln = ln.strip()
        m = re.match(r"^(200[3-8]) 한국종합사회조사", ln)
        if m: year = int(m.group(1)); continue
        if re.match(r"^20\d\d 한국종합사회조사", ln): year = None; continue
        if year and re.fullmatch(r"[A-Z][A-Z0-9_]{1,15}", ln): found[ln].add(year)
    return found


def body_lines():
    """지정 쪽 범위의 줄. @@PAGE·쪽번호·반복 머리글 제거."""
    out, page, skip_num = [], 0, False
    for ln in open(SRC, encoding="utf-8"):
        ln = ln.rstrip("\n")
        m = re.match(r"^@@PAGE (\d+)$", ln)
        if m: page = int(m.group(1)); skip_num = True; continue
        if not PAGE_FROM <= page <= PAGE_TO: continue
        if skip_num and re.fullmatch(r"\d+", ln.strip()): skip_num = False; continue
        skip_num = False
        if ln.strip() in ("", "KGSS 2003-2025 Cumulative Codebook"): continue
        out.append(ln.strip())
    return out


def wave_str(years):
    ys = sorted(set(years)); groups = []
    for y in ys:
        if groups and YEARS.index(y) == YEARS.index(groups[-1][-1]) + 1: groups[-1].append(y)
        else: groups.append([y])
    return "·".join(f"{g[0]}~{g[-1]}" if len(g) > 1 else str(g[0]) for g in groups)


def years_of(w):
    ys = set()
    for g in w.split("·"):
        if not g: continue
        a, b = (g.split("~") + [g])[:2]
        ys |= set(YEARS[YEARS.index(int(a)):YEARS.index(int(b)) + 1])
    return ys


STD_COLS = ["03-08"] + [str(y) for y in YEARS[6:]] + ["전체"]
TITLE = re.compile(r"^표\d+(\s|$)")
QMARK = re.compile(r"\[?설문문항\]")
CELL = re.compile(r"^(-|\d+\.\d)$")


def parse():
    q03 = qnr_years()
    lines = body_lines()
    items, i, n = [], 0, len(lines)
    while i < n:
        if lines[i] != "응답 범주": i += 1; continue
        i += 1
        cols = []  # 열 머리
        while i < n and not re.search(r"(전체|TOTAL)$", lines[i]):
            cols += [t for t in lines[i].replace("변수값", " ").split() if t]; i += 1
        cols += lines[i].split()[:-1] + ["전체"]; i += 1  # "2025 TOTAL"처럼 붙은 줄
        ncol = len(cols)
        if ncol == 13: cols = STD_COLS  # 원문 오타(2017, TOTAL)는 자리로 바로잡음
        rows = []  # (label, value, cells); 셀이 ncol보다 적은 행(원문 열 누락)도 그대로 둔다
        label, cells, value = [], [], None
        while i < n and lines[i] != "N" and not TITLE.match(lines[i]):
            ln = lines[i].replace("　", " ").strip()
            toks = ln.split()
            if cells and not all(CELL.match(t) for t in toks):  # 새 행 시작 → 앞 행 마감
                rows.append((" ".join(label), value, cells)); label, cells, value = [], [], None
            if value is not None and toks and all(CELL.match(t) for t in toks):
                cells += toks
                if len(cells) >= ncol:
                    rows.append((" ".join(label), value, cells[:ncol])); label, cells, value = [], [], None
            elif re.fullmatch(r"-?\d+", ln):
                if value is not None: label.append(value)  # 앞 정수는 라벨이었음
                value = ln
            else:
                if value is not None: label.append(value); value = None
                label.append(ln)
            i += 1
        if cells: rows.append((" ".join(label), value, cells))
        while i < n and not TITLE.match(lines[i]): i += 1
        if i >= n: break
        title = re.sub(r"^표\d+\s*", "", lines[i]); i += 1
        while i < n and not QMARK.match(lines[i]) and lines[i] != "응답 범주":
            title += " " + lines[i]; i += 1  # 표 제목이 두 줄로 꺾인 경우
        if i >= n or not QMARK.match(lines[i]): continue
        q = []
        while i < n and not lines[i].startswith("[변수명]"):
            q.append(lines[i]); i += 1
        if i >= n: break
        var = lines[i].replace("[변수명]", "").strip(); i += 1
        question = re.sub(r"\s+", " ", QMARK.sub("", " ".join(q))).strip()
        if SKIP_VAR.search(var): continue  # 가구원 특성 절(쪽 718~)은 범위 밖, 면접원 변수 블록은 본체에 없음
        # 연도: 비해당(-1) 행 제외, '-' 아닌 열
        years = set()
        for _, v, cs in rows:
            if v == "-1": continue
            for c, col in zip(cs, cols[:-1]):
                if c == "-": continue
                if re.fullmatch(r"\d{4}", col): years.add(int(col))
                elif re.fullmatch(r"0[3-8]-0[3-8]", col):
                    a, b = (2000 + int(x) for x in col.split("-"))
                    years |= q03.get(var, set()) & set(range(a, b + 1)) or set(range(a, b + 1))
        labels = [l for l, v, _ in rows if not v.startswith("-") and l]
        scale = " / ".join(labels[:7])
        if "..." in question:
            stem, sub = question.split("...", 1)
            question = f"{stem.strip()} — {sub.strip()}" if sub.strip() else stem.strip()
        items.append({"theme": theme(question + " " + title), "wave": wave_str(years), "var": var,
                      "question": question, "scale": scale, "unit": "개인"})
    return items


if __name__ == "__main__":
    items = parse()
    seen, out = set(), []
    for it in items:
        k = (it["var"], it["question"][:40])
        if k not in seen: seen.add(k); out.append(it)
    try:  # PyMuPDF 추출은 한국어 띄어쓰기가 빠져 있다 → kiwipiepy로 복원(검색·가독성). 없으면 그대로
        from kiwipiepy import Kiwi
        kw = Kiwi(); sp = lambda t: kw.space(t, reset_whitespace=True) if re.search(r"[가-힣]{6,}", t) else t
        for it in out:
            it["question"] = sp(it["question"]); it["scale"] = " / ".join(sp(x) for x in it["scale"].split(" / ")) if it["scale"] else ""
    except ImportError:
        print("kiwipiepy 없음: 띄어쓰기 복원 생략")
    json.dump({"kgss": out}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    assert len(out) >= 300, len(out)
    v = {i["var"]: i for i in out}
    assert {2012, 2023} <= years_of(v["CANTRUST"]["wave"]), v.get("CANTRUST")
    assert "MEMB1" in v and v["MEMB1"]["wave"] == "2012·2023", v.get("MEMB1")
    assert " — " in v["MEMB1"]["question"]
    print("kgss 전체 문항", len(out), collections.Counter(i["theme"] for i in out).most_common())
    print("wave 없음", sum(1 for i in out if not i["wave"]), "scale 없음", sum(1 for i in out if not i["scale"]))
    for i in out:
        if i["theme"] == "TR" and {2012, 2023} <= years_of(i["wave"]):
            print(" ", i["var"], i["wave"], "|", i["question"][:60], "|", i["scale"][:50])
