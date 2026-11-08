# -*- coding: utf-8 -*-
"""지역사회건강조사 2023 원시자료 이용지침서 변환본(data/codebooks/chs/guide/g2023_01.md) 제4부 변수설명 → 문항 전체 목록 → model/full_chs.json {"chs": [...]}.
영역마다 「설문 및 해당 변수」(문항 문구·보기) 뒤에 「변수설계」 표(문항번호·변수명·라벨·코드)가 온다. 변수설계 행을 1순위 원본으로 삼고,
문항 문구·보기는 같은 영역의 설문 글에서 문항번호로 찾는다(없으면 변수라벨·코드명). 2023 조사표 PDF(chs_2023_3)는 이미지라 쓰지 않는다.
ID·가중치·조사원 기록은 뺀다(기본정보에서는 만나이·성별·동읍면·주택유형만). 가구조사 영역은 unit 가구. 실행: python model/parse_chs_full.py [-v]"""
import html, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "..", "data", "codebooks", "chs", "guide", "g2023_01.md"), encoding="utf-8").read()
src = src[src.index("# 01 기본정보"):src.index("# 01 질병관리청원시자료공개절차")]
T = lambda s: re.sub(r"[ \t\r\f\v]+", " ", html.unescape(re.sub(r"<br\s*/?>", "\n", s)).replace("\xa0", " ")).strip()
NONSUB = re.compile(r"^(응답거부|비해당|모름)")
BASIC = {"age", "sex", "dong_ty_code", "house_ty_code"}
NUM = r"\d{1,2}(?:-\d{1,2})?"

def theme(s):
    if re.search(r"신뢰|믿", s): return "TR"
    if re.search(r"단체|참여|모임|봉사|기부|투표|친구|이웃|관계|도움|연락|만나|교류|소통|고립|외로|은둔|지지|의논", s): return "NW"
    if re.search(r"공정|차별", s): return "FA"
    if re.search(r"복지|수급|급여|지원|정책|정부|제도|서비스|혜택|행정|프로그램|기초생활|장려금|수당|바우처", s): return "IN"
    if re.search(r"지역|거주|동네|시도|이사|주거|주택", s): return "RG"
    if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구원|출생|학교|취업|근로|임금|자산|부채|생활비", s): return "DM"
    return "ET"

def questions(survey_html):
    """설문 글에서 {번호: (문구, [보기])}. 문구는 다음 번호나 ① 앞까지, 보기는 그 뒤 다음 번호 앞까지의 ①②…."""
    flat = re.sub(r"\s+", " ", T(re.sub(r"<[^>]+>", " ", survey_html)))
    flat = re.sub(r"\|\s*\d+\s*\|[^|]*\|\s*\|\s*---\s*\|\s*---\s*\||!\[image\]\([^)]*\)", " ", flat)  # 쪽 꼬리글·그림
    flat = re.sub(r"\b[a-z]\w*_\w+\b|\(\s*➡?[^()]*번 문항으로\s*\)", " ", flat)  # 변수명·건너뛰기 표시 제거
    q = {}
    for m in re.finditer(rf"(?<![\d/~\-])({NUM})\.\s*(.*?)(?=\s(?:{NUM})\.\s|\s?[①-⑳]|$)(.*?)(?=\s(?:{NUM})\.\s|$)", flat):
        no, text = m.group(1), re.split(r"\s\d{2,}\.\s", re.sub(r"\s+", " ", m.group(2)))[0].strip(" .:")  # '888. 비해당' 류 코드 설명 앞까지
        opts = [o.strip(" .#") for o in re.findall(r"[①-⑳]\s*([^①-⑳]+?)(?=\s*[①-⑳]|$)", m.group(3))]
        if no not in q and len(text) > 3 and not NONSUB.match(text):
            q[no] = (text, opts)
    return q

def rows(design_html):
    for tr in re.findall(r"<tr>(.*?)</tr>(?=\s*<tr>|\s*</table>)", design_html, re.S):
        if "<table>" in tr: tr = tr[:tr.index("<table>")]  # 건수(%) 중첩표 제거
        tds = re.findall(r"<t[dh]([^>]*)>(.*?)</t[dh]>", tr, re.S)
        if len(tds) < 3: continue
        yield [(a, T(re.sub(r"<(?!br)[^>]+>", "", b))) for a, b in tds]

out = []
for sec in re.split(r"\n(?=# \d\d )", src):
    name = sec.split("\n", 1)[0].lstrip("# ")
    basic = "기본정보" in name
    unit = "가구" if "가구조사" in name else "개인"
    for ch in re.split(r"설문 및 해당 변수", sec):
        parts = re.split(r"변수설계", ch, maxsplit=1)
        survey, design = (parts[0], parts[1]) if len(parts) == 2 else ("", parts[0])
        qs = questions(survey)
        for r in rows(design):
            has_no = not basic and not re.match(r"^[a-z]", r[0][1])
            no = re.sub(r"\s*\n\s*", " ", r[0][1]).replace(" -", "-") if has_no else ""
            var, label = (r[1][1], r[2][1]) if has_no else (r[0][1], r[1][1])
            var = var.replace(" ", "")
            if not re.match(r"^[a-z][a-z0-9_]+$", var): continue
            if basic and var not in BASIC: continue
            k = 3 if has_no else 2  # 코드 열 시작
            text, opts = qs.get(no, (None, []))
            if "colspan" in r[k][0] or len(r) < k + 2 or not re.match(r"^\d+\.", r[k][1]):
                scale = r[k][1].replace("\n", " ")[:80]  # 수치 입력(□□ 명 등)
            elif len(opts) >= 2:
                scale = " / ".join(f"{i} {o}" for i, o in enumerate(opts[:7], 1)) + (" …" if len(opts) > 7 else "")
            else:  # 설문 글에 보기가 없으면 변수설계 코드명(줄바꿈된 코드명은 어긋날 수 있음)
                cs = [(c.rstrip("."), n) for c, n in zip(r[k][1].split("\n"), r[k + 1][1].split("\n"))]
                o = [f"{c} {n}" for c, n in cs if not NONSUB.match(n)]
                scale = " / ".join(o[:7]) + (" …" if len(o) > 7 else "")
            stem = qs.get(no.split("-")[0], (None,))[0] if "-" in no else None
            if text and stem and not re.search(r"(까|오)\s*\??$", text):  # 행렬형 하위 항목만 줄기를 붙인다
                text = f"{stem} — {text}"
            label = label.replace("\n", " ")
            question = text or label
            out.append({"theme": theme((label + " " + question).replace("만나이", "나이")), "wave": "2023", "var": var,
                        "question": question, "scale": scale, "unit": unit, "_sec": name, "_label": label, "_no": no})
seen, items = set(), []
for i in out:
    if i["var"] not in seen:
        seen.add(i["var"]); items.append(i)
assert len(items) >= 120, len(items)
assert any(i["var"] == "ena_01a1" and "신뢰" in i["question"] and i["question"].count(" — ") == 1 for i in items)
assert any(i["var"] == "fma_04z1" and i["unit"] == "가구" and "3 아니다" in i["scale"] for i in items)
pub = [{k: v for k, v in i.items() if not k.startswith("_")} for i in items]
json.dump({"chs": pub}, open(os.path.join(H, "full_chs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("chs 2023 문항", len(items), collections.Counter(i["theme"] for i in items).most_common())
print("라벨로 대체(설문 글에서 번호 못 찾음):", sum(1 for i in items if i["question"] == i["_label"]))
if "-v" in sys.argv:
    for i in items:
        print(f"{i['_sec'][:10]:10}|{i['_no']:5}|{i['var']:14}|{i['theme']}|{i['unit']}| {i['question'][:110]} | {i['scale'][:70]}")
