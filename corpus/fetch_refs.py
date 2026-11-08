# -*- coding: utf-8 -*-
"""SLNA 엣지 층: 해외 양적 후보(candidates_oa.csv · candidates_quant.csv)의 참고문헌(referenced_works)과 저자 소속 국가를 OpenAlex에서 받는다.
50편씩 묶어 /works?filter=openalex_id:W..|W.. (list 요청, 1크레딧). 결과 corpus/refs_oa.jsonl(한 줄 한 편: id, refs[], countries[], cited_by). 받은 id는 건너뛰므로 이어받기 가능. 무한 재시도.
키: 환경변수 OPENALEX_API_KEY(없으면 IP 공용 예산). 실행: python -I corpus/fetch_refs.py"""
import csv, json, os, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "refs_oa.jsonl")
UA = {"User-Agent": "week11-seminar-corpus/0.3 (mailto:ojh121523@gmail.com)"}
ids = []
for fn in ["candidates_oa.csv", "candidates_quant.csv"]:
    p = os.path.join(H, fn)
    if os.path.exists(p):
        ids += [r["id"] for r in csv.DictReader(open(p, encoding="utf-8-sig")) if r["id"].startswith("W")]
ids = list(dict.fromkeys(ids))
done = set(json.loads(l)["id"] for l in open(OUT, encoding="utf-8")) if os.path.exists(OUT) else set()
todo = [i for i in ids if i not in done]
print(f"대상 {len(ids)} · 이미 받음 {len(done)} · 남음 {len(todo)}", flush=True)


def get(url):
    i = 0
    while True:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except Exception as e:
            i += 1; wait = min(120, 10 * i); print(f"  retry {i} ({str(e)[:70]}) wait {wait}s", flush=True); time.sleep(wait)


with open(OUT, "a", encoding="utf-8") as f:
    for k in range(0, len(todo), 50):
        chunk = todo[k:k + 50]
        params = {"filter": "openalex_id:" + "|".join(chunk), "per-page": 50, "select": "id,referenced_works,authorships,cited_by_count,publication_year", "mailto": "ojh121523@gmail.com"}
        if os.environ.get("OPENALEX_API_KEY"): params["api_key"] = os.environ["OPENALEX_API_KEY"]
        data = get("https://api.openalex.org/works?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
        got = set()
        for w in data.get("results", []):
            wid = w["id"].rsplit("/", 1)[-1]; got.add(wid)
            cc = sorted({ins.get("country_code") for a in w.get("authorships", []) for ins in a.get("institutions", []) if ins.get("country_code")})
            f.write(json.dumps({"id": wid, "year": w.get("publication_year"), "cited_by": w.get("cited_by_count"), "countries": cc, "refs": [x.rsplit("/", 1)[-1] for x in w.get("referenced_works", [])]}, ensure_ascii=False) + "\n")
        for wid in chunk:
            if wid not in got:
                f.write(json.dumps({"id": wid, "missing": True}) + "\n")  # 삭제·병합된 ID. 다시 묻지 않도록 표시
        f.flush()
        if (k // 50) % 10 == 0:
            print(f"{k + len(chunk)}/{len(todo)}", flush=True)
        time.sleep(1.0)
print("done", flush=True)
