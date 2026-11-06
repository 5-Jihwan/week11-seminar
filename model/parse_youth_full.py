# -*- coding: utf-8 -*-
"""청년삶실태조사 2024 파일설계서(xlsx, 항목정보·코드정보) → 변수 전체 목록 → model/full_items.json 의 'youth2022'(캔버스의 조사 id. 회차는 2024로 표기).
항목명이 문항 문구 대신이고, 코드 의미를 척도로 붙인다(코드 7개까지). 주제는 키워드(검색용). 실행: python model/parse_youth_full.py"""
import json, os, re, sys, collections
import openpyxl
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); X = os.path.join(H, "..", "data", "codebooks", "youth", "youth2024_layout.xlsx")
wb = openpyxl.load_workbook(X, read_only=True)
codes = collections.defaultdict(list)
for i, row in enumerate(wb["코드정보"].iter_rows(values_only=True)):
    if i < 2 or row[0] is None: continue
    codes[str(row[0]).strip()].append((str(row[2]).strip(), str(row[3] or "").strip()))
def theme(s):
    if re.search(r"신뢰|믿", s): return "TR"
    if re.search(r"단체|참여|모임|봉사|기부|투표|친구|이웃|관계|도움|연락|만나|교류|소통|고립|외로|은둔|지지|의논", s): return "NW"
    if re.search(r"공정|차별", s): return "FA"
    if re.search(r"복지|수급|급여|지원|정책|정부|제도|서비스|혜택|행정|프로그램|기초생활|장려금|수당|바우처", s): return "IN"
    if re.search(r"지역|거주|동네|시도|이사|주거|주택", s): return "RG"
    if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구원|출생|학교|취업|근로|임금|자산|부채|생활비", s): return "DM"
    return "ET"
out = []
for i, row in enumerate(wb["항목정보"].iter_rows(values_only=True)):
    if i < 3 or row[0] is None: continue
    no, name, ln, typ, cno = (str(c).strip() if c is not None else "" for c in row[:5])
    if not name: continue
    cs = codes.get(cno, []) if typ == "Y" else []
    scale = (f"{len(cs)}범주: " + " / ".join(f"{c} {m}" for c, m in cs[:7]) + (" …" if len(cs) > 7 else "")) if cs else ("수치" if typ == "N" else "텍스트" if typ == "T" else "")
    out.append({"survey": "youth2022", "wave": "2024", "var": f"V{no}", "question": name, "scale": scale[:140], "unit": "개인(19~34세)", "theme": theme(name + " " + " ".join(m for _, m in cs[:4]))})
p = os.path.join(H, "full_items.json"); full = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
full["youth2022"] = out
json.dump(full, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("청년삶실태조사 2024 변수", len(out), collections.Counter(i["theme"] for i in out).most_common())
for it in [x for x in out if x["theme"] in ("TR", "NW", "IN")][:12]:
    print(" ", it["var"], "|", it["question"][:60], "|", it["scale"][:70])
