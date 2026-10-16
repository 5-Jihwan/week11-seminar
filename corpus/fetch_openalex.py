"""OpenAlex에서 선행연구 후보를 모은다 (키 불필요, 표준 라이브러리만).

수집 경로 (PLAN §5-1):
  1. 지정문헌 5편을 인용한 후속 연구 전부
  2. 키워드 검색 (사회자본·신뢰의 결정요인, 제도·복지국가·정책환류)
출력: candidates.csv (id, doi, title, year, authors, venue, cited_by, seeds, queries, abstract)

사용: python -I corpus/fetch_openalex.py corpus/candidates.csv
"""
import csv, json, sys, time, urllib.parse, urllib.request

API = "https://api.openalex.org/works"
SEEDS = {  # 약칭: DOI
    "krishna": "10.1111/j.1468-2508.2007.00600.x",
    "freitag": "10.1111/j.1475-6765.2005.00293.x",
    "lw": "10.1111/1467-9248.00334",
    "mettler": "10.1017/S0003055402000217",
    "kr": "10.1177/0010414004273203",
}
SEED_TITLES = {  # DOI 조회 실패 시 제목 검색
    "lw": "Social Capital and Local Governance: Exploring the Institutional Design Variable",
}
QUERIES = [
    '"social capital" "welfare state" trust',
    '"generalized trust" institutions determinants',
    '"social trust" "policy feedback"',
    '"social capital" "political institutions" determinants',
    '"interpersonal trust" "means-tested" OR "universal" welfare',
    '"social capital" "direct democracy" OR "local government" participation',
    '"institutional trust" "social trust" causal',
    '"social capital" Korea trust determinants',
]
FIELDS = "id,doi,title,publication_year,authorships,primary_location,cited_by_count,abstract_inverted_index,language"


def get(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "week11-seminar-corpus/0.1"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # ponytail: 단순 백오프. 401/429는 순간 제한으로 보고 더 기다린다
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def paged(params, cap=2000):
    # cursor 2페이지째부터 401이 나서 page 번호 방식(최대 10,000건)을 쓴다
    params = dict(params, **{"per-page": 200, "page": 1, "select": FIELDS})
    out = []
    while True:
        data = get(API + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
        out += data["results"]
        if len(data["results"]) < 200 or len(out) >= cap:
            return out
        params["page"] += 1
        time.sleep(1.0)


def abstract(inv):
    if not inv:
        return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)


def row(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return {
        "id": w["id"].rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": w.get("title") or "",
        "year": w.get("publication_year") or "",
        "authors": "; ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:6]),
        "venue": src.get("display_name") or "",
        "cited_by": w.get("cited_by_count") or 0,
        "lang": w.get("language") or "",
        "abstract": abstract(w.get("abstract_inverted_index")),
    }


def main(out_path):
    works = {}  # id -> row (+ seeds, queries)
    def add(w, seed=None, query=None):
        r = works.setdefault(w["id"], dict(row(w), seeds=set(), queries=set()))
        if seed: r["seeds"].add(seed)
        if query: r["queries"].add(query)

    for name, doi in SEEDS.items():
        try:
            seed = get(f"{API}/doi:{doi}?select=id,title,cited_by_count")
        except Exception:
            q = urllib.parse.urlencode({"search": SEED_TITLES.get(name, name), "per-page": 1, "select": "id,title,cited_by_count"})
            seed = get(API + "?" + q)["results"][0]
        sid = seed["id"].rsplit("/", 1)[-1]
        citing = paged({"filter": f"cites:{sid}"})
        print(f"[seed] {name}: {seed['title'][:60]} … cited_by={seed['cited_by_count']} fetched={len(citing)}", file=sys.stderr)
        for w in citing:
            add(w, seed=name)

    for q in QUERIES:
        res = paged({"filter": f'title_and_abstract.search:{q},publication_year:>1995', "sort": "cited_by_count:desc"}, cap=200)
        print(f"[query] {q[:50]} … {len(res)}", file=sys.stderr)
        for w in res:
            add(w, query=q)

    rows = sorted(works.values(), key=lambda r: (-len(r["seeds"]), -r["cited_by"]))
    cols = ["id", "doi", "title", "year", "authors", "venue", "cited_by", "lang", "seeds", "queries", "abstract"]
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        for r in rows:
            r["seeds"] = "|".join(sorted(r["seeds"]))
            r["queries"] = "|".join(sorted(r["queries"]))
            wr.writerow({k: r[k] for k in cols})
    multi = sum(1 for r in rows if r["seeds"].count("|") >= 1)
    print(f"total {len(rows)} rows, {multi} cite 2+ seeds, {sum(1 for r in rows if r['abstract'])} with abstract", file=sys.stderr)


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8")
    main(sys.argv[1] if len(sys.argv) > 1 else "candidates.csv")
