# -*- coding: utf-8 -*-
"""해외 50년(1976~) 전수 수집: OpenAlex에서 제목에 사회자본·신뢰·시민참여가 들어간 학술 논문(초록 있는 것)을 연도별로 모은다.
이어받기 가능: data/raw/harvest/openalex_{축}_{연도}.done 이 있으면 건너뛴다. 결과는 corpus/openalex_all.jsonl(한 줄 한 편, id로 중복 제거는 build 단계에서).
OpenAlex는 page 방식 상한이 10,000건이라 연도×축으로 나눈다. 폴라이트 풀(mailto) + 1초 간격. 키 불필요.
사용: python -I corpus/harvest_openalex.py [시작연도] [끝연도]"""
import json, os, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "openalex_all.jsonl")
CK = os.path.join(HERE, "..", "data", "raw", "harvest"); os.makedirs(CK, exist_ok=True)
API = "https://api.openalex.org/works"
AXES = {  # 축 이름: 제목 검색식. 종속변수로서의 사회자본에 쓰이는 이름들
    "sc": '"social capital"',
    "trust": '"social trust" OR "generalized trust" OR "interpersonal trust" OR "institutional trust" OR "political trust"',
    "civic": '"civic participation" OR "civic engagement" OR "associational" OR "volunteering" OR "voluntary association"',
}
FIELDS = "id,doi,title,publication_year,authorships,primary_location,cited_by_count,abstract_inverted_index,language,type,referenced_works_count"
UA = {"User-Agent": "week11-seminar-corpus/0.2 (mailto:ojh121523@gmail.com)"}


def get(url):
    i = 0
    while True:  # 네트워크가 끊겨도 포기하지 않는다(이동 중·절전 뒤 재연결 대비). 최대 2분 간격으로 무한 재시도
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except Exception as e:
            i += 1; wait = min(120, 10 * i)
            print(f"  retry {i} ({str(e)[:60]}) wait {wait}s", flush=True); time.sleep(wait)


def abstract(inv):
    if not inv:
        return ""
    return " ".join(w for _, w in sorted((p, w) for w, ps in inv.items() for p in ps))


def row(w, axis):
    loc = w.get("primary_location") or {}; src = loc.get("source") or {}
    return {"id": w["id"].rsplit("/", 1)[-1], "doi": (w.get("doi") or "").replace("https://doi.org/", ""), "title": w.get("title") or "", "year": w.get("publication_year") or "",
            "authors": "; ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:6]), "venue": src.get("display_name") or "", "cited_by": w.get("cited_by_count") or 0,
            "lang": w.get("language") or "", "abstract": abstract(w.get("abstract_inverted_index")), "axis": axis, "src": "openalex"}


def harvest(axis, q, year):
    flag = os.path.join(CK, f"openalex_{axis}_{year}.done")
    if os.path.exists(flag):
        return 0
    n, page = 0, 1
    with open(OUT, "a", encoding="utf-8") as f:
        while True:
            params = {"filter": f"title.search:{q},publication_year:{year},type:article,has_abstract:true", "per-page": 200, "page": page, "select": FIELDS, "mailto": "ojh121523@gmail.com"}
            data = get(API + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
            for w in data["results"]:
                f.write(json.dumps(row(w, axis), ensure_ascii=False) + "\n"); n += 1
            if len(data["results"]) < 200 or page >= 50:  # 50쪽 = 10,000건 상한
                break
            page += 1; time.sleep(1.0)
    open(flag, "w").write(str(n)); return n


if __name__ == "__main__":
    y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1976; y1 = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    total = 0
    for year in range(y1, y0 - 1, -1):  # 최근부터
        for axis, q in AXES.items():
            n = harvest(axis, q, year); total += n
            if n:
                print(f"{year} {axis}: {n}", flush=True); time.sleep(1.0)
    print("done, new rows", total, flush=True)
