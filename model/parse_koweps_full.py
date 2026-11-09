# -*- coding: utf-8 -*-
"""한국복지패널 20차(2025) 조사설계서 코딩북(xlsx 3종: 가구용·가구원용·복지인식용) → model/full_koweps.json {"koweps": [...]}.
열: 변수명 | SYSMIS | 질문번호(원가구/신규) | 구분 | 변수설명 | 문항내용(값 라벨). 구분·질문번호는 세로 병합이라 앞 값을 이어받는다.
question = '구분 — 변수설명'(구분이 있으면), scale = 문항내용의 값 라벨, var = 변수명. ID·가중치·머지키·활용변수는 뺀다.
원본: data/codebooks/koweps/wave20/*.xlsx (Ji가 받은 조사설계서 beta1). 실행: python model/parse_koweps_full.py (openpyxl은 사용자 site에 있어 -I 금지)"""
import collections, glob, json, os, re, sys
import openpyxl
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(H, "..", "data", "codebooks", "koweps", "wave20"); OUT = os.path.join(H, "full_koweps.json")
SHEETS = [("가구용", "가구", "20차(2025)"), ("가구원용", "개인", "20차(2025)"), ("복지인식용", "개인", "20차(2025) 복지인식 부가조사")]
SKIP_VAR = re.compile(r"^(h20_(id|ind|sn|merkey|pind|pid|ws|wg|wsc|wgc|wsl|wgl)|h_new|p20_(ws|wg|wsc|wgc|wsl|wgl|fnum|pid)|wc20_(fnum|ws|wg|wsc|wgc))", re.I)
SKIP_SEC = ("표지", "활용변수", "가구식별변수", "가구원식별변수", "가중치")


def theme(s):  # parse_kipa_full.py와 같은 키워드 규칙(검색용이지 코딩 아님)
    if re.search(r"신뢰|믿", s): return "TR"
    if re.search(r"참여|단체|모임|이웃|도움|교류|왕래|기부|봉사|친구|친척", s): return "NW"
    if re.search(r"공정", s): return "FA"
    if re.search(r"복지|수급|서비스|기관|제도|정부|보험|연금|급여|지원|보조", s): return "IN"
    if re.search(r"지역|동네|거주지|시도|권역", s): return "RG"
    if re.search(r"성별|연령|학력|교육수준|소득|직업|혼인|종교|가구원수|출생", s): return "DM"
    return "ET"


def labels(txt):  # "1.결혼 2.직장 3.학업" / "0. 기존 1. 추가" → 라벨만 앞 7개
    if not txt: return ""
    parts = [p.strip(" .:") for p in re.split(r"(?:^|\s)\(?\d{1,3}\)?[.)]\s*", str(txt)) if p.strip(" .:")]
    parts = [re.sub(r"\s+", " ", p) for p in parts]
    return (" / ".join(parts[:7]) + (" …" if len(parts) > 7 else "")) if len(parts) >= 2 else re.sub(r"\s+", " ", str(txt))[:80]


items, seen = [], set()
for key, unit, wave in SHEETS:
    fs = [f for f in glob.glob(os.path.join(SRC, "*.xlsx")) if key in os.path.basename(f)]
    assert fs, key
    ws = openpyxl.load_workbook(fs[0], read_only=True)["코딩북"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c or "") for c in rows[0]]
    ci = {"var": 0, "sec": next(i for i, h in enumerate(hdr) if h.strip() == "구분"), "desc": next(i for i, h in enumerate(hdr) if "변수설명" in h), "lab": next(i for i, h in enumerate(hdr) if "문항내용" in h)}
    qi = [i for i, h in enumerate(hdr) if "질문" in h]
    sec = q = ""
    for r in rows[1:]:
        r = list(r) + [None] * 8
        var = str(r[ci["var"]] or "").strip()
        if r[ci["sec"]]: sec = re.sub(r"\s+", " ", str(r[ci["sec"]])).strip()
        if qi and r[qi[0]]: q = str(r[qi[0]]).strip()
        desc = re.sub(r"\s+", " ", str(r[ci["desc"]] or "")).strip()
        if not var or not desc or SKIP_VAR.match(var) or any(k in sec for k in SKIP_SEC) or any(k in desc for k in ("가중치", "패널 ID", "머지")): continue
        var = re.sub(r"\s+", "", var)
        if re.search(r"가구원\s*[2-9]|[2-9]번\s*가구원", sec): continue  # 가구원1~9 반복 블록은 1번만
        sec1 = re.sub(r"^\d+\.\s*|^[A-G]\.\s*|-?\s*가구원\s*1$|^1번\s*", "", sec).strip()  # 절 번호·가구원1 꼬리 제거
        dkey = re.sub(r"\s+", "", desc)
        if dkey in seen: continue
        seen.add(dkey)
        stem = sec1 if sec1 and sec1 != desc and len(sec1) <= 14 and not re.search(r",|및", sec1) else ""  # 짧은 구분만 줄기(절 제목은 제외)
        question = f"{stem} — {desc}" if stem else desc
        qn = re.sub(r"^문\s*", "", q) if q and q not in ("-", "활용변수", "표지") else ""
        items.append({"theme": theme(question), "wave": wave, "var": var + (f" (문{qn})" if qn else ""), "question": question, "scale": labels(r[ci["lab"]]), "unit": unit})

json.dump({"koweps": items}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
assert len(items) >= 400, len(items)
# 20차(beta1) 설계서에는 16차의 일반신뢰 문항(p1604_1)이 없다. 요약 문항(16차)이 그 자리를 맡는다
print("koweps 전체 문항", len(items), collections.Counter(i["theme"] for i in items).most_common(), "scale 없음", sum(1 for i in items if not i["scale"]))
for i in items[::60]: print(" ", i["unit"], i["var"], "|", i["question"][:60], "|", i["scale"][:50])
