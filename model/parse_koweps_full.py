# -*- coding: utf-8 -*-
"""한국복지패널 16차(2021년 조사) 전체 문항 → model/full_koweps.json ({"koweps": [...]}).
변수명·문항(라벨)·단위는 17차 이용자 가이드의 변수이력표(data/codebooks/koweps/guide17_variable_history.tsv, 16차 열)에서 가져온다.
pdftotext로 푼 조사표(survey16_*.txt)는 표 안 글자가 뒤섞여 보기(①②)를 문항에 붙이면 틀린 척도가 붙어 쓰지 않는다
(시도해 보니 116건 중 대부분이 다른 문항의 보기였다). 척도는 변수이력표의 단위 열(만원·4점척도·코딩북 참조 등)만 쓴다.
행렬형은 "구분 — 세부항목"으로 쓴다. 주제는 키워드(검색용, parse_youth_full.py와 같은 규칙).
실행: python -I model/parse_koweps_full.py"""
import collections, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(H, "..", "data", "codebooks", "koweps", "guide17_variable_history.tsv")

def theme(s):
    if re.search(r"신뢰|믿", s): return "TR"
    if re.search(r"단체|참여|모임|봉사|기부|투표|친구|이웃|관계|도움|연락|만나|교류|소통|고립|외로|은둔|지지|의논|왕래", s): return "NW"
    if re.search(r"공정|차별", s): return "FA"
    if re.search(r"복지|수급|급여|지원|정책|정부|제도|서비스|혜택|행정|프로그램|기초생활|장려금|수당|바우처|보험|연금", s): return "IN"
    if re.search(r"지역|거주|동네|시도|이사|주거|주택", s): return "RG"
    if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구원|출생|학교|취업|근로|임금|자산|부채|생활비", s): return "DM"
    return "ET"

def scale(u):
    fixed = {"-": "", "": "", "단위": "", "코딩북 참조": "범주(코딩북 참조)", "텍스트": "텍스트", "주관식": "텍스트"}
    return fixed[u] if u in fixed else (u if "척도" in u else f"수치({u})")

SKIP = re.compile(r"ID|패널|머지|키변수|가중치|이름|성명|조사원|방문|번호\d*$|동일\)")  # 비문항·"(가구원1과 동일)" 참조행
sheet, area, grp, label, items, seen = "", "", "", "", [], set()
for l in open(TSV, encoding="utf-8").read().split("\n"):
    if l.startswith("### SHEET"): sheet = l[10:]; area = grp = label = ""; continue
    c = [x.strip() for x in l.split("\t")]
    if len(c) < 20 or not re.match(r"가구(원)?용데이터 변수이력표", sheet): continue
    area, grp = c[0] or area, c[1] or grp
    label = c[2] or ("" if c[1] else label)  # 빈 세부항목은 앞 라벨의 연속 변수(수급형태2 등)
    var = c[19]
    if not re.fullmatch(r"n?[hp]16\w+", var) or not label or SKIP.search(label): continue
    unit = "가구" if sheet.startswith("가구용") else "개인"
    stem = re.sub(r"^\d+\.\s*", "", grp or area)
    q = label if (not stem or stem == label) else f"{stem} — {label}"
    key = (unit, re.sub(r"\d", "", q))
    if key in seen: continue  # 가구원1~9 반복 블록, 연속 변수는 첫 변수만
    seen.add(key)
    items.append({"theme": theme(f"{area} {stem} {label}"), "wave": "16차(2021)", "var": var, "question": q, "scale": scale(c[3]), "unit": unit})

assert len(items) >= 150, len(items)
json.dump({"koweps": items}, open(os.path.join(H, "full_koweps.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("koweps 16차 문항", len(items), collections.Counter(i["theme"] for i in items).most_common(),
      "| 가구", sum(i["unit"] == "가구" for i in items), "개인", sum(i["unit"] == "개인" for i in items), "| 척도 있음", sum(bool(i["scale"]) for i in items))
for i in [x for x in items if x["theme"] in ("TR", "NW")][:8] + items[:2]:
    print(" ", i["var"], "|", i["question"][:60], "|", i["scale"][:40])
