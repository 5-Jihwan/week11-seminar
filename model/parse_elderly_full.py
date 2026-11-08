# -*- coding: utf-8 -*-
"""2023년도 노인실태조사(안) 조사표 변환본(data/codebooks/others/elderly/elderly_2023_questionnaire.md, HTML 표)을 문항 전체 목록으로 푼다
→ model/full_elderly.json {"elderly2023": [...]}.
영역 제목 `# A. …` 으로 나누고, 그 영역 글자의 문항 번호(문B3-2.)마다 블록을 만든다. 셀 하나에 보기 번호가 2개 이상이면 척도,
1개면 행렬형 하위 항목. 짧은 머리글(문D6-1. 참여빈도)은 열 머리글로 보고 뒤따르는 하위 항목을 같은 묶음의 열 전체에 붙인다.
theme()는 parse_kipa_full.py 규칙 그대로(검색용). 실행: python model/parse_elderly_full.py"""
import collections, html, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "..", "data", "codebooks", "others", "elderly", "elderly_2023_questionnaire.md"), encoding="utf-8").read()
src = src.replace("\\*", "*").replace("\\~", "~").replace("\\_", "_")

OPT = re.compile(r"(?<![\d가-힣A-Za-z(~∼\-])(\d{1,2}(?:-\d)?)\)\s*|\((\d{1,2})\)\s*|([⓪ⓞ①-⑳])\s*")
STOP = r"(?!\s*(?:으로|로|이동|문항|에|의|과|와|를|을|=|~|∼|>|&gt;))"
def marker_re(letter):
    return re.compile(rf"(?<![A-Za-z가-힣\d<\-(;])(?:문\s?)?({letter}\d{{1,2}}(?:-\d{{1,2}}){{0,2}}(?:~{letter}\d{{1,2}})?)(?=\s*[.．]|\s|$){STOP}\s*[.．]?\s*")

def theme(s, text):  # parse_kipa_full.py 그대로
    s2 = s + " " + text
    if re.search(r"신뢰|믿", s2): return "TR"
    if re.search(r"단체|참여|모임|봉사|기부|투표|접촉|도움|교류|소통|친구|이웃", s2): return "NW"
    if re.search(r"공정", s2): return "FA"
    if re.search(r"복지|서비스|정부|제도|기관|지원|혜택|행정|정책|세금", s2): return "IN"
    if re.search(r"지역|거주|동네|마을", s2): return "RG"
    if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구", s2): return "DM"
    return "ET"

def clean(s):
    s = re.sub(r"[■★□]", " ", s)
    s = re.sub(r"\(\*[^)]*\)", " ", s)
    s = re.sub(r"\*.*?(?=\s\d{1,2}\)|$)", " ", s)  # 조사원 메모(*…)는 다음 보기 번호 앞까지 지움
    s = re.sub(r"\s*⇨.*", "", s)
    return re.sub(r"\s+", " ", s).strip(" .:")

def options(s):
    """보기 번호가 있는 문자열 → [(번호, 문구)] (번호순, 빈 문구 제외)."""
    parts = OPT.split(s)
    out = []
    for i in range(1, len(parts), 4):
        num = parts[i] or parts[i + 1] or parts[i + 2]
        txt = clean(parts[i + 3] or "")
        if txt and not re.match(r"^\d{1,2}\)", txt):
            out.append((num, txt))
    key = lambda n: int(re.sub(r"\D", "", n) or 0) if n[0].isdigit() else " ⓪ⓞ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳".find(n)
    return sorted(out, key=lambda o: key(o[0]))

def cells(block):
    """HTML/마크다운 덩어리 → 셀 문자열 목록. <br>는 공백(같은 셀), 셀·줄 끝은 경계."""
    b = re.sub(r"<br\s*/?>", " ", block)
    b = re.sub(r"</?t[dh]>|</?tr>|</?table>|^\s*#+ ", "\x00", b, flags=re.M)
    b = html.unescape(re.sub(r"<[^>]+>", " ", b)).replace("\xa0", " ")
    out = []
    for piece in b.split("\x00"):  # 표 밖의 마크다운 줄은 빈 줄까지 한 셀로 묶는다(보기가 한 줄에 하나씩 적혀 있음)
        for para in re.split(r"\n\s*\n", piece):
            para = re.sub(r"\s+", " ", para).strip()
            if para: out.append(para)
    return out

secs = re.split(r"(?m)^# ([A-J])\. [^\n]*\n", src)
items, recs = [], {}
for si in range(1, len(secs), 2):
    letter, body = secs[si], re.split(r"(?m)^■\s*$", secs[si + 1])[0]  # J 뒤에 붙은 문C4 재제시 조각은 버림
    MK = marker_re(letter)
    recs_sec, group, range_stem = {}, [], {}
    def rec(var, stem):
        r = recs_sec.get(var)
        if r is None:
            core = re.sub(r"\(※[^)]*\)", "", stem).strip()
            r = recs_sec[var] = {"var": var, "q": stem, "subs": [], "scale": [], "gs": [], "gidx": 0, "glen": 1, "label": len(core) <= 20 and not core.endswith(("?", "까"))}
            items.append(r)
        return r
    for c in cells(body):
        pieces = MK.split(c)  # [앞글, var, 본문, var, 본문 …]
        lead = pieces[0]
        segs = [(pieces[i], pieces[i + 1]) for i in range(1, len(pieces), 2)]
        chunks = ([(None, lead)] if lead.strip() else []) + segs
        for var, text in chunks:
            if var is not None:
                if "~" in var:  # 문G1~G4: 줄기만 기억하고 열 머리글(G1. 동거자녀)에 붙인다
                    a, b = var.split("~"); n0, n1 = int(a[1:]), int(b[1:])
                    for n in range(n0, n1 + 1): range_stem[f"{letter}{n}"] = clean(text.split(" 1)")[0])
                    group = []; continue
                opts = options(text)
                m = OPT.search(text)
                stem = clean(text[:m.start()] if m else text)
                r = rec(var, stem)
                if r["label"] and var in range_stem and r["q"] == stem:
                    r["q"] = range_stem[var] + " — " + stem
                if opts and not r["scale"]: r["scale"] = opts
                if r["label"]:
                    group = group + [r] if group and all(g["label"] for g in group) else [r]
                    for k, g in enumerate(group): g["gidx"], g["glen"] = k, len(group)
                else:
                    group = [r]
                continue
            # 번호 없는 셀: 현재 묶음의 하위 항목이나 척도
            if not group or text.startswith("※"): continue
            opts = options(text)
            if len(opts) >= 2:
                if len(group) == 1 and not group[0]["scale"]: group[0]["scale"] = opts
                else:  # 열 머리글 묶음: 묶음이 닫힌 뒤 출력 때 배분(척도 수 == 열 수면 순서대로, 1개면 전체, 그 외 비움)
                    for g in group:
                        if opts not in g["gs"]: g["gs"].append(opts)
            elif len(opts) == 1 and OPT.match(text):
                kind = "paren" if text.startswith("(") else "num"
                for g in group:
                    g["subs"].append((kind, opts[0][1]))
    # 머리글(짧은 줄기)은 부모 문항 문구를 앞에 붙인다
    for r in recs_sec.values():
        if r["label"] and "—" not in r["q"]:
            par = recs_sec.get(re.sub(r"-\d+$", "", r["var"]))
            if par and par is not r and len(par["q"]) > 20: r["q"] = par["q"] + " — " + r["q"]

out, seen = [], set()
for r in items:
    letter = r["var"][0]
    subs = r["subs"]
    if any(k == "num" for k, _ in subs): subs = [t for k, t in subs if k == "num"]  # n)과 (n)이 섞이면 n)이 행, (n)은 안쪽 칸
    else: subs = [t for _, t in subs]
    subs = list(dict.fromkeys(subs))
    sc = r["scale"] or (r["gs"][r["gidx"]] if len(r["gs"]) == r["glen"] else r["gs"][0] if len(r["gs"]) == 1 else [])
    scale = " / ".join(t for _, t in sc[:7])
    unit = "가구" if letter == "A" or ("귀댁" in r["q"] and "응답 노인" not in r["q"].split(" — ")[-1]) else "개인"
    head, *lab = r["q"].split(" — ")  # 긴 줄기만 자르고 열 머리글·하위 항목은 살린다
    stem = " — ".join([head[:120]] + lab)
    rows = [(r["var"], stem, "")] if not subs or len(subs) > 30 else [(r["var"], f"{stem} — {t}", t) for t in subs]
    for var, q, sub in rows:
        k = var + q
        if k in seen or len(q) < 2: continue
        seen.add(k)
        out.append({"theme": theme(sub, r["q"]), "wave": "2023", "var": var, "question": q, "scale": scale, "unit": unit})

json.dump({"elderly2023": out}, open(os.path.join(H, "full_elderly.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
vars_ = {i["var"] for i in out}
assert len(out) >= 120 and {"B1", "D6", "D7", "F15", "H17", "J2"} <= vars_, (len(out), sorted(vars_)[:20])
print("노인실태조사 2023 문항", len(out), collections.Counter(i["theme"] for i in out).most_common())
print("영역별", sorted(collections.Counter(i["var"][0] for i in out).items()))
for i in out:
    if i["var"] in ("B1", "D6", "D6-1", "D7", "D10", "F15", "F16", "H4", "H17", "H18", "J2", "J3-1", "A3", "G1"):
        print(" ", i["var"], "|", i["unit"], i["theme"], "|", i["question"][:80], "|", i["scale"][:60])
