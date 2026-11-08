# -*- coding: utf-8 -*-
"""통계청 사회조사 2023 조사표 3종(가구주·가구원·청소년)과 가계금융복지조사 2023 조사표를 문항 전체 목록으로 푼다 → model/full_kostat.json
{"kostat_social": [...], "kostat_hfls": [...]}. 가구원표가 본체(unit 개인), 가구주표 고유 문항은 unit 가구, 청소년표 고유 문항만 추가.
추출 텍스트는 data/codebooks/kostat/*.txt 로 남긴다(사회조사 = pymupdf 스트림 순서, 가계금융복지 = 이미지 PDF라 kordoc --ocr 결과 hfls2023.txt를 그대로 읽음).
주제는 키워드로 대충 붙인다(검색용이지 코딩 아님). 실행: python model/parse_kostat_full.py"""
import collections, json, os, re, sys
import pymupdf
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(H, "..", "data", "codebooks", "kostat")
FORMS = [("가구원", "2. 2023년 사회조사표(가구원)", "social2023_member.txt", "개인"), ("가구주", "1. 2023년 사회조사표(가구주)", "social2023_head.txt", "가구"), ("청소년", "3. 2023년 사회조사표(청소년)", "social2023_youth.txt", "개인")]

def theme(s):
    if re.search(r"신뢰|믿", s): return "TR"
    if re.search(r"단체|참여|모임|봉사|기부|투표|친구|이웃|관계|도움|연락|만나|교류|소통|고립|외로|지지|의논", s): return "NW"
    if re.search(r"공정|차별", s): return "FA"
    if re.search(r"복지|수급|급여|지원|정책|정부|제도|서비스|혜택|행정|프로그램|기초생활|수당|연금|보험|공공", s): return "IN"
    if re.search(r"지역|거주|동네|시도|이사|주거|주택|거처", s): return "RG"
    if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구원|출생|학교|취업|근로|임금|자산|부채|생활비|소비|지출|가구주|교육", s): return "DM"
    return "ET"

# ---------- 사회조사: 문항 번호 줄(「12-1 ‌귀하는…」, 글자 앞 U+200C)을 줄기로 잡고, 나머지 텍스트 조각은 바로 위·같은 단의 줄기에 붙인다(2단 편집 대응)
STEM = re.compile(r"^\s*(\d{1,2}(?:-\d)?)(?:\s*‌\s*\x07?\s*(?=[가-힣‘(\[\d])|\s+(?=[가-힣‘(\[]))")
SUB = re.compile(r"^\s*(\d{1,2})\.\s*‌*\x07?\s*(\S.*)$")
OPT = re.compile(r"[①-⑳]\s*([^①-⑳\n]+)")
NOTE = re.compile(r"^\s*[※☞•✽–]|^\s*참\s*고")
SKIP = re.compile(r"^\s*\d+(?:-\d)?\s*‌?\x07?\s*항")  # 「→ 13 항으로」, 「17 항부터」
clean = lambda s: re.sub(r"\s+", " ", s.replace("‌", "").replace("\x07", "")).strip()

def segments(page):
    """블록을 줄 단위로 읽어 문항 번호 줄에서 끊은 조각 [(x0,y0,x1,y1,[lines]), …]. 한 블록에 문항 두 개가 붙은 경우(62·63 성별·생년월일) 대비."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0 or b["bbox"][1] >= 805 or b["bbox"][0] >= 590: continue  # 바닥글·옆 색인 탭 제외
        for ln in b["lines"]:
            t = "".join(s["text"] for s in ln["spans"])
            if not t.strip(): continue
            if STEM.match(t) and not SKIP.match(t) or not out or out[-1][4] is None: out.append([*ln["bbox"], [t]])
            else:
                seg = out[-1]; seg[0] = min(seg[0], ln["bbox"][0]); seg[2] = max(seg[2], ln["bbox"][2]); seg[3] = max(seg[3], ln["bbox"][3]); seg[4].append(t)
        if out: out.append([0, 0, 0, 0, None])  # 블록 경계 표시
    return [s for s in out if s[4] is not None]

def parse_social(pdf, txt):
    d = pymupdf.open(pdf); qs = []; cur = None
    open(txt, "w", encoding="utf-8").write("".join(f"\n=== PAGE {i+1} ===\n" + p.get_text("text") for i, p in enumerate(d)))
    for pno, p in enumerate(d):
        if pno == 0: continue  # 표지
        segs = segments(p); stems = []
        for s in segs:
            m = STEM.match(s[4][0])
            if m and not SKIP.match(s[4][0]):
                q = {"var": m.group(1), "stem": clean(" ".join([s[4][0][m.end():]] + s[4][1:])), "box": s[:4], "lines": []}; stems.append(q); qs.append(q); s.append(q)
        for s in sorted(segs, key=lambda s: (round(s[1]), s[0])):
            if len(s) > 5: continue
            cand = [q for q in stems if q["box"][1] <= s[1] + 2 and q["box"][0] - 10 <= s[2] and s[0] <= q["box"][2] + 10]
            if cand: tgt = max(cand, key=lambda q: q["box"][1])
            elif stems and s[1] >= stems[0]["box"][1]: tgt = max(stems, key=lambda q: q["box"][1] if q["box"][1] <= s[1] + 2 else -1)
            else: tgt = cur  # 앞 쪽에서 이어지는 문항
            if tgt is not None: tgt["lines"] += s[4] + ["\x00"]  # \x00 = 조각 경계
        if stems: cur = stems[-1]
    for q in qs:
        subs, opts, i = [], [], 0
        L = [l for l in q["lines"] if l.strip() and not SKIP.match(l)]
        while i < len(L):
            l = L[i]; m = SUB.match(l)
            if m and int(m.group(1)) == len(subs) + 1:
                t = m.group(2); i += 1
                while i < len(L) and not (SUB.match(L[i]) or OPT.search(L[i]) or NOTE.match(L[i]) or L[i] == "\x00") and len(L[i]) < 60:
                    t += " " + L[i]; i += 1
                parts = re.split(r"\s+(?=\d{1,2}\.\s)", clean(t))  # 한 줄에 「1. 가족 2. 친척 3. …」로 붙은 하위 항목
                subs.append(parts[0])
                for p in parts[1:]:
                    n, _, body = p.partition(". ")
                    if n.isdigit() and int(n) == len(subs) + 1: subs.append(body.strip())
                    else: subs[-1] += " " + p
                continue
            if NOTE.match(l) and not OPT.search(l): i += 1; continue
            if l != "\x00" and not (subs or opts or OPT.search(l) or NOTE.match(l) or STEM.match(l)) and re.search(r"[가-힣]", l) and len(q["stem"]) < 300 and not q["stem"].endswith(("?", ".", "오", "다")):
                q["stem"] = clean(q["stem"] + " " + l); i += 1; continue  # 줄기가 다음 조각으로 이어짐
            for o in OPT.findall(l):
                o = clean(o)
                if o and o not in opts and not re.search(r"’|주십시오|괄호", o): opts.append(o)  # 「‘① 있다’에 표시하여 주십시오」 같은 안내문 제외
            i += 1
        q["subs"] = subs if len(subs) <= 30 else []; q["scale"] = " / ".join(opts[:7])
    return qs

social, seen = [], set()
for form, pdf, txt, unit in FORMS:
    for q in parse_social(os.path.join(K, "social2023_forms", pdf + ".pdf"), os.path.join(K, txt)):
        key = re.sub(r"[^가-힣]", "", re.sub(r"^.*?분만 응답해 주십시오\.", "", q["stem"]))[:25]
        if not key or key in seen: continue  # 가구원표와 같은 문항은 가구주·청소년표에서 건너뜀
        seen.add(key)
        rows = [(f"{form} {q['var']}-{k}", f"{q['stem']} — {s}") for k, s in enumerate(q["subs"], 1)] or [(f"{form} {q['var']}", q["stem"])]
        for var, qq in rows:
            social.append({"theme": theme(qq), "wave": "2023", "var": var, "question": qq, "scale": q["scale"], "unit": unit})

# ---------- 가계금융복지조사: OCR 텍스트(hfls2023.txt)를 문항 번호 줄로 분할
hfls = []
HT = os.path.join(K, "hfls2023.txt")  # 만들기: kordoc --ocr --no-tables -o hfls2023.txt hfls2023_form.pdf (PP-OCRv5, 약 10분)
HQ = re.compile(r"(?:^|[\s|→>\\])(\d{1,2}(?:-\d{1,2})?)\s*\\?\|?\s*((?:[가-힣(‘]|\d+년).*?(?:까\?|십시오\.?))(.{0,40})$")  # 뒤 꼬리 = 같은 줄에 붙은 보기(「있음 ②없음」)
HSUB = re.compile(r"^[-\s]*(\d{1,2})\s*((?!억|만원)[가-힣][^:①-⑳억]{1,50})$")
HSUBC = re.compile(r"^[-\s]*(?:[①-⑳ㄱㄷㅁ]|기(?=\s))\s*((?!억|만원|없음|있음)[가-힣][^:①-⑳억]{1,40}?)\s*(?:\|?\s*억.*)?$")  # 써넣기 행렬(소득·지출)의 ①②… 행. ㄱ·ㄷ·ㅁ·기 = OCR이 ①을 잘못 읽은 것
if os.path.exists(HT):
    lines = [re.sub(r"<[^>]+>|\\\|", " ", l).replace("\\~", "~").strip() for l in open(HT, encoding="utf-8")]
    start = next(i for i, l in enumerate(lines) if re.match(r"^[IⅠ]\s*가구 구성", l))  # 앞은 표지·작성 요령·예시
    qs = []
    for l in lines[start:]:
        m = HQ.search(l)
        if m and not re.search(r"번[의)]|작성하여|이동하여", l):
            v, t = m.group(1), m.group(2).strip()
            if re.fullmatch(r"\d+-\d{2}", v): v, t = v[:-1], v[-1] + t  # OCR 「25-11년 후」= 25-1 + 1년 후
            qs.append({"var": v, "stem": re.sub(r"\s+", " ", t), "lines": [m.group(3)]}); continue
        if qs and l: qs[-1]["lines"].append(l)
    for q in qs:
        subs, opts = [], []
        fill = q["stem"].endswith("써넣어 주십시오.")  # 소득·지출 써넣기 행렬: ①②… 줄이 보기가 아니라 하위 항목
        for l in q["lines"]:
            if l.startswith(("※", "*", "\\*")): continue
            m = HSUBC.match(l) if fill else None
            if m: subs.append(re.sub(r"\s+", " ", m.group(1)).strip()); continue
            m = HSUB.match(l)
            if m and (fill or int(m.group(1)) == len(subs) + 1): subs.append(re.sub(r"\s+", " ", m.group(2)).strip()); continue
            if re.search(r"[①-⑳]", l):
                for o in re.split(r"[①-⑳]", l):  # 첫 보기 ①은 OCR이 네모칸으로 읽어 번호가 자주 빠짐
                    o = re.sub(r"\s+", " ", re.sub(r"[-#\[\]|\\]", " ", o)).strip(" \t-")
                    if o and o not in opts and len(o) < 40 and not re.search(r"^\d|억|만원|^회$|가구원|구분", o): opts.append(o)
        if len(set(subs)) < len(subs): subs = []  # 가구원 1~7 반복 칸을 하위 항목으로 잘못 읽은 경우
        unit = "개인" if re.search(r"가구원\s*번호|가구원별|가구원당", " ".join(q["lines"][:12])) else "가구"
        rows = [(f"{q['var']}-{k}", f"{q['stem']} — {s}") for k, s in enumerate(subs, 1)] if 2 <= len(subs) <= 20 else [(q["var"], q["stem"])]
        for var, qq in rows:
            hfls.append({"theme": theme(qq), "wave": "2023", "var": var, "question": qq, "scale": "금액 써넣기" if fill else " / ".join(opts[:7]), "unit": unit})

out = {"kostat_social": social, "kostat_hfls": hfls}
json.dump(out, open(os.path.join(H, "full_kostat.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for k, v in out.items():
    print(k, len(v), collections.Counter(i["theme"] for i in v).most_common())
    for i in v[:3] + v[-2:]: print("  ", i["var"], "|", i["question"][:70], "|", i["scale"][:50])
assert len(social) >= 120, "사회조사 문항 수 부족"
