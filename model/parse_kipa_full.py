# -*- coding: utf-8 -*-
"""사회통합실태조사 2023 조사표 변환본(data/codebooks/kipa/q2023.md, HTML 표)을 문항 전체 목록으로 푼다 → model/full_items.json 의 'kipa' 키.
문항 번호 <th>N</th> 다음 <th>문항 문구</th>, 하위 항목 <td>(k) 문구</td>, 보기 ① ② …. 주제는 키워드로 대충 붙인다(검색용이지 코딩 아님).
실행: python model/parse_kipa_full.py"""
import html, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "..", "data", "codebooks", "kipa", "q2023.md"), encoding="utf-8").read()
T = lambda s: html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ").strip()
T2 = lambda s: re.sub(r"\s+", " ", T(s))
blocks = re.split(r"(?=<tr><th><table>\s*<tr><th></th><th></th><th>\d+(?:-\d+)?</th></tr>\s*</table></th>)", src)
items = []
for b in blocks:
    m = re.match(r"<tr><th><table>\s*<tr><th></th><th></th><th>(\d+(?:-\d+)?)</th></tr>\s*</table></th><th>(.*?)</th>", b, re.S)
    if not m:
        continue
    q, text = m.group(1), T2(m.group(2))
    if not text or len(text) < 4:
        continue
    subs = [(k, T2(t)) for k, t in re.findall(r"<td>\((\d+)\)\s*(.*?)</td>", b, re.S)]
    hdr = re.search(r"<th>항\s*목</th>(.*?)</tr>", b, re.S)  # 행렬형: 머리글이 척도
    if hdr:
        opts = [T2(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", hdr.group(1), re.S)]
    else:  # 단일형: ① 보기 ② 보기 …
        opts = [o.strip() for o in re.findall(r"[①-⑳]\s*([^①-⑳<]{1,40})", T(b))]
    opts = [o for o in opts if o and not re.match(r"^\(\d+\)", o)]
    scale = (f"{len(opts)}점: " if hdr else "") + " / ".join(opts[:7]) if opts else ""
    def theme(s):
        s2 = s + " " + text
        if re.search(r"신뢰|믿", s2): return "TR"
        if re.search(r"단체|참여|모임|봉사|기부|투표|접촉|도움|교류|소통|친구|이웃", s2): return "NW"
        if re.search(r"공정", s2): return "FA"
        if re.search(r"복지|서비스|정부|제도|기관|지원|혜택|행정|정책|세금", s2): return "IN"
        if re.search(r"지역|거주|동네|마을", s2): return "RG"
        if re.search(r"성별|연령|나이|학력|소득|직업|혼인|가구", s2): return "DM"
        return "ET"
    if subs and len(subs) <= 30:
        for k, t in subs:
            items.append({"survey": "kipa", "wave": "2023", "var": f"Q{q}-{k}", "question": f"{text} — ({k}) {t}", "scale": scale, "unit": "개인", "theme": theme(t)})
    else:
        items.append({"survey": "kipa", "wave": "2023", "var": f"Q{q}", "question": text, "scale": scale, "unit": "개인", "theme": theme("")})
seen, out = set(), []
for i in items:
    k = i["var"] + i["question"][:40]
    if k not in seen:
        seen.add(k); out.append(i)
p = os.path.join(H, "full_items.json")
full = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
full["kipa"] = out
json.dump(full, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
import collections
print("kipa 전체 문항", len(out), collections.Counter(i["theme"] for i in out).most_common())
for i in out[:3] + out[-2:]:
    print(" ", i["var"], i["question"][:70], "|", i["scale"][:40])
