# -*- coding: utf-8 -*-
"""fetch_art.py에서 못 받은 후보를 커먼즈 검색(list=search, 파일 이름공간)으로 찾아 받는다. 요청 사이 6초 대기."""
import json, os, sys, io, time, urllib.request, urllib.parse, re, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "art"); IDX = os.path.join(OUT, "index.json")
UA = {"User-Agent": "week11-seminar-deck/0.1 (educational; contact via github 5-Jihwan)"}
idx = json.load(open(IDX, encoding="utf-8")) if os.path.exists(IDX) else {}
Q = [("tax_collectors", "Marinus van Reymerswaele Tax Collectors", "Reymerswaele, 세금 징수관 — 심사·창구"),
     ("moneylender", "Quentin Matsys Moneylender and his Wife", "Matsys, 환전상과 아내 — 계산·심사"),
     ("cardsharps", "Caravaggio Cardsharps Kimbell", "Caravaggio, 카드 사기꾼 — 속임·불신"),
     ("school_of_athens", "Raphael School of Athens Stanza della Segnatura", "Raphael, 아테네 학당 — 이론가들"),
     ("third_class", "Daumier Third-Class Carriage Metropolitan", "Daumier, 삼등 객차 — 계층"),
     ("syndics", "Rembrandt Syndics of the Drapers Guild Staalmeesters", "Rembrandt, 직물 길드 이사들 — 위원회·심사"),
     ("daumier_lawyers", "Daumier Three Lawyers Walters", "Daumier, 변호사 셋 — 절차·법"),
     ("washington_delaware", "Washington Crossing the Delaware Leutze 1851 Metropolitan", "Leutze, 델라웨어 도하 — 참전·국가"),
     ("tower_babel", "Pieter Bruegel Tower of Babel Vienna", "Bruegel, 바벨탑 — 설계와 건축"),
     ("oath_horatii", "Jacques-Louis David Oath of the Horatii Louvre", "David, 호라티우스 형제의 맹세 — 국가에 대한 서약"),
     ("ship_of_fools", "Hieronymus Bosch Ship of Fools Louvre", "Bosch, 바보들의 배 — 틀 없는 항해"),
     ("last_judgment_weighing", "Rogier van der Weyden Beaune Altarpiece weighing souls", "van der Weyden, 영혼의 무게 재기 — 심사·측정")]
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
for alias, q, note in Q:
    if alias in idx: continue
    try:
        time.sleep(6)
        s = api({"action": "query", "list": "search", "srsearch": q + " filetype:bitmap", "srnamespace": 6, "srlimit": 5, "format": "json"})
        hits = [h["title"] for h in s["query"]["search"] if h["title"].lower().endswith((".jpg", ".jpeg", ".png"))]
        if not hits: print("검색 결과 없음:", alias); continue
        got = False
        for title in hits[:3]:
            time.sleep(6)
            j = api({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1600, "format": "json"})
            page = next(iter(j["query"]["pages"].values())); ii = page.get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
            lic = md.get("LicenseShortName", {}).get("value", "")
            if not ("Public domain" in lic or lic.startswith("PD") or "CC0" in lic) or ii.get("width", 0) < 1200: continue
            artist = re.sub(r"<[^>]+>", "", html.unescape(md.get("Artist", {}).get("value", ""))).strip(); date = re.sub(r"<[^>]+>", "", md.get("DateTimeOriginal", {}).get("value", ""))[:40]
            time.sleep(4); data = urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=120).read()
            open(os.path.join(OUT, alias + ".jpg"), "wb").write(data)
            idx[alias] = {"title": title, "note": note, "license": lic, "artist": artist[:80], "date": date, "page": ii.get("descriptionurl", ""), "file": alias + ".jpg", "kb": len(data) // 1024}
            print("ok", alias, "|", title[:60], "|", lic, "|", len(data) // 1024, "KB"); got = True; break
        if not got: print("PD 후보 없음:", alias, hits[:3])
    except Exception as e:
        print("실패:", alias, str(e)[:80])
json.dump(idx, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("총", len(idx))
