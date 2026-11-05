# -*- coding: utf-8 -*-
"""수집(jsonl) → 사회자본 양적 연구만 남긴 후보 표. 국내·해외 같은 규칙(국문 단서 추가), id로 중복 제거.
규칙: 초록이 있고, 양적 단서가 2종 이상이며, 서평·개념 논문 단서가 없을 것. 최종 판단은 코딩 단계(Haiku 5.5)에서 한 번 더.
사용: python -I corpus/screen_quant.py  → corpus/candidates_kci.csv, corpus/candidates_oa.csv (+ 화면에 집계)"""
import csv, glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
QUANT = re.compile(r"\b(regression|survey data|survey|panel|longitudinal|cross-?sectional|OLS|logit|probit|multilevel|hierarchical linear|fixed[- ]effects|difference-in-differences|experiment|"
                   r"respondents|N\s?=\s?\d|sample of|data from|World Values Survey|European Social Survey|quantitative|correlat|coefficient|SEM|structural equation)\b|"
                   r"회귀|패널|종단|횡단|구조방정식|경로분석|다층|위계적|로짓|프로빗|고정효과|이중차분|실험|응답자|표본|조사\s*자료|설문|실태조사|패널조사|상관|계수|유의|매개효과|조절효과|분석\s*결과", re.I)
NOT = re.compile(r"\b(book review|this (book|volume|chapter)|review essay|literature review|we review|conceptual paper|theoretical paper|systematic review|meta-analysis)\b|서평|문헌\s*고찰|개념적\s*고찰|이론적\s*고찰|체계적\s*문헌|메타분석|연구\s*동향", re.I)
COLS = ["id", "doi", "title", "title_en", "year", "authors", "venue", "category", "cited", "lang", "src", "axis", "quant_hits", "url", "abstract", "abstract_en"]


def screen(rows):
    seen, keep = set(), []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        txt = " ".join([r.get("abstract", ""), r.get("abstract_en", "")]).strip()
        if not txt:
            continue
        if NOT.search(r.get("title", "") + " " + txt[:400]) and not re.search(r"\bN\s?=\s?\d|regression|회귀|표본", txt, re.I):
            continue
        hits = len(set(m.group(0).lower() for m in QUANT.finditer(txt)))
        if hits >= 2:
            keep.append({**{c: r.get(c, "") for c in COLS}, "quant_hits": hits, "venue": r.get("venue") or r.get("journal", ""), "cited": r.get("cited") or r.get("cited_by", "")})
    return keep


def main():
    for name, pat in [("kci", "kci_w*.jsonl"), ("oa", "openalex_all.jsonl")]:
        rows = [json.loads(l) for p in glob.glob(os.path.join(HERE, pat)) for l in open(p, encoding="utf-8") if l.strip()]
        keep = screen(rows); keep.sort(key=lambda r: (-(int(r["cited"] or 0)), str(r["year"])))
        dst = os.path.join(HERE, f"candidates_{name}.csv")
        with open(dst, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(keep)
        yrs = sorted(str(r["year"])[:4] for r in keep)
        print(f"{name}: 수집 {len(rows)} → 중복 제거·초록 있음·양적 {len(keep)}  연도 {yrs[0] if yrs else '-'}~{yrs[-1] if yrs else '-'}  → {os.path.basename(dst)}")


if __name__ == "__main__":
    main()
