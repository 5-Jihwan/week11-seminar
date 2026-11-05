# -*- coding: utf-8 -*-
"""국내 30년(발행 1996~) 전수 수집: KCI OAI-PMH(무인증) ARTI 전체를 커서로 훑으며 사회자본·신뢰·시민참여 논문만 남긴다.
토큰 형식이 from:until:100:cursor 라 커서를 직접 만들어 어디서든 이어받는다. 체크포인트 data/raw/harvest/kci_w{n}.cursor, 결과 corpus/kci_w{n}.jsonl.
워커 셋으로 나눠 병렬(0~1M, 1M~2M, 2M~끝). 무한 재시도(이동 중 끊김 대비). 100건에 약 3초.
사용: python -I corpus/harvest_kci.py <워커번호 0|1|2> [시작커서 끝커서]"""
import json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); CK = os.path.join(HERE, "..", "data", "raw", "harvest"); os.makedirs(CK, exist_ok=True)
B = "http://open.kci.go.kr/oai/request?verb=ListRecords&resumptionToken="
RANGES = {0: (0, 1_000_000), 1: (1_000_000, 2_000_000), 2: (2_000_000, 10_000_000)}
PAT = re.compile(r"사회\s*적?\s*자본|social capital", re.I)  # 사회자본 논문만. 양적 여부는 코딩 단계(초록의 회귀·표본·조사 단서)에서 거른다
QUANT = re.compile(r"회귀|패널|구조방정식|다층|위계|로짓|프로빗|분석결과|유의|표본|조사\s*자료|설문|실태조사|패널조사|regression|panel|survey|sample|significant|SEM|multilevel", re.I)
R = lambda tag, x, attr="": (re.search(rf"<{tag}{attr}[^>]*>(.*?)</{tag}>", x, re.S) or [None, ""])[1].strip()


def parse(rec):  # 토큰 이어받기 응답은 항상 oai_dc 형식(키워드 없음, 초록·발행연월·학술지·artiId·피인용수 있음)
    ids = dict((m.group(1), m.group(2).strip()) for m in re.finditer(r'<dc:identifier[^>]*type="(\w+)"[^>]*>(.*?)</dc:identifier>', rec, re.S))
    jinfo = ids.get("journalInfo", ""); date = R("dc:date", rec)
    return {"id": ids.get("artiId", ""), "oai": R("identifier", rec), "journal": jinfo.split(",")[0].strip(), "jinfo": jinfo, "publisher": R("dc:publisher", rec), "year": date[:4], "date": date, "cited": ids.get("citedCnt", ""),
            "category": R("dc:subject", rec), "title": R("dc:title", rec, ' lang="original"'), "title_en": R("dc:title", rec, ' lang="english"'), "authors": R("dc:creator", rec),
            "abstract": R("dc:description", rec, ' lang="original"'), "abstract_en": R("dc:description", rec, ' lang="english"'), "keywords": "", "url": R("dc:url", rec), "lang": R("dc:language", rec), "src": "kci"}


def keep(d):
    try:
        if int(d["year"] or 0) < 1996:
            return False
    except ValueError:
        return False
    txt = " ".join([d["title"], d["title_en"], d["abstract"][:3000], d["abstract_en"][:3000]])
    if not PAT.search(txt):
        return False
    d["quant_hint"] = len(QUANT.findall(txt))  # 0이면 비양적일 가능성. 코딩 단계에서 최종 판단
    return True


def fetch(tok):
    i = 0
    while True:
        try:
            with urllib.request.urlopen(B + urllib.parse.quote(tok), timeout=180) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            i += 1; wait = min(120, 10 * i); print(f"  retry {i} ({str(e)[:60]}) wait {wait}s", flush=True); time.sleep(wait)


def main(w, start=None, end=None):
    lo, hi = RANGES[w]; start = lo if start is None else start; end = hi if end is None else end
    ckf = os.path.join(CK, f"kci_w{w}.cursor"); out = os.path.join(HERE, f"kci_w{w}.jsonl")
    cur = int(open(ckf).read().strip()) if os.path.exists(ckf) else start
    kept = seen = 0; t0 = time.time()
    with open(out, "a", encoding="utf-8") as f:
        while cur < end:
            x = fetch(f"2013-01-01:2026-12-31:100:{cur}")
            recs = re.findall(r"<record>(.*?)</record>", x, re.S)
            if not recs:
                if "<error" in x and "noRecordsMatch" in x or not recs:
                    print(f"w{w} end at cursor {cur}", flush=True); break
            for rec in recs:
                d = parse(rec); seen += 1
                if keep(d):
                    f.write(json.dumps(d, ensure_ascii=False) + "\n"); kept += 1
            f.flush()
            m = re.search(r"<resumptionToken[^>]*>[^<]*:(\d+)<", x); nxt = int(m.group(1)) if m else cur + len(recs)
            cur = nxt if nxt > cur else cur + 100  # 토큰이 안 늘면 100씩 강제 전진
            open(ckf, "w").write(str(cur))
            if seen % 5000 < 100:
                print(f"w{w} cursor {cur} seen {seen} kept {kept} {round((time.time()-t0)/60)}min", flush=True)
            time.sleep(0.3)
    print(f"w{w} done cursor {cur} seen {seen} kept {kept}", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else None, int(sys.argv[3]) if len(sys.argv) > 3 else None)
