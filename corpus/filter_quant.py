"""candidates.csv에서 양적 연구만 남긴다 (규칙, API 없음). 지정문헌 5편 자체는 뺀다.

사용: python -I corpus/filter_quant.py corpus/candidates.csv corpus/candidates_quant.csv
"""
import csv, re, sys

SEED_DOIS = {"10.1111/j.1468-2508.2007.00600.x", "10.1111/j.1475-6765.2005.00293.x",
             "10.1111/1467-9248.00334", "10.1017/S0003055402000217", "10.1177/0010414004273203"}
QUANT = re.compile(r"\b(regression|survey data|survey|panel|longitudinal|cross-?sectional|OLS|logit|probit|"
                   r"multilevel|hierarchical linear|fixed[- ]effects|difference-in-differences|experiment|"
                   r"respondents|N\s?=\s?\d|sample of|data from|World Values Survey|European Social Survey|"
                   r"quantitative|correlat|coefficient)", re.I)
NOT = re.compile(r"\b(book review|this (book|volume|chapter)|review essay|literature review|we review|"
                 r"conceptual paper|theoretical paper)\b", re.I)


def main(src, dst):
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    keep = []
    for r in rows:
        if r["doi"].lower() in {d.lower() for d in SEED_DOIS} or not r["abstract"]:
            continue
        if NOT.search(r["abstract"]) and not re.search(r"\bN\s?=\s?\d|regression", r["abstract"], re.I):
            continue
        hits = len(set(m.group(0).lower() for m in QUANT.finditer(r["abstract"])))
        if hits >= 2:
            r["quant_hits"] = hits
            keep.append(r)
    keep.sort(key=lambda r: (-len(r["seeds"].split("|")) if r["seeds"] else 0, -int(r["cited_by"] or 0)))
    cols = list(rows[0].keys()) + ["quant_hits"]
    with open(dst, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(keep)
    print(f"{len(rows)} -> {len(keep)} quantitative candidates", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
