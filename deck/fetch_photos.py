# -*- coding: utf-8 -*-
"""논문별 실제 장소 사진: 위키미디어 커먼즈 검색 → PD·CC0·CC BY·CC BY-SA 중 가로 1400px 이상 → deck/photos/<alias>.jpg + index.json(작가·라이선스·출처 URL).
실행: python deck/fetch_photos.py   (요청 사이 5초, 재실행하면 이미 받은 것은 건너뜀)"""
import json, os, sys, io, time, urllib.request, urllib.parse, re, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "photos"); os.makedirs(OUT, exist_ok=True); IDX = os.path.join(OUT, "index.json")
UA = {"User-Agent": "week11-seminar-deck/0.2 (educational; contact via github 5-Jihwan)"}
idx = json.load(open(IDX, encoding="utf-8")) if os.path.exists(IDX) else {}
Q = [("rajasthan_village", ["Rajasthan village houses", "village Rajasthan India rural"], "Krishna · 라자스탄 마을"),
     ("landsgemeinde", ["Landsgemeinde Glarus", "Landsgemeinde Appenzell"], "Freitag · 스위스 란츠게마인데(직접민주주의 주민총회)"),
     ("swiss_canton", ["Appenzell Innerrhoden village", "Glarus town Switzerland"], "Freitag · 칸톤 마을"),
     ("birmingham_council", ["Birmingham Council House", "Birmingham city council chamber"], "Lowndes & Wilson · 버밍엄 시의회"),
     ("uk_town_hall_meeting", ["public meeting town hall England council consultation", "parish council meeting"], "Lowndes & Wilson · 공청회"),
     ("gi_bill", ["GI Bill veterans college 1947", "veterans registering university 1946 GI Bill"], "Mettler · 제대군인원호법 수혜 학생"),
     ("us_veterans_1945", ["World War II veterans returning home 1945", "GI Bill signing Roosevelt 1944"], "Mettler · 참전자"),
     ("sweden_office", ["Försäkringskassan office", "Arbetsförmedlingen office Sweden"], "Kumlin & Rothstein · 스웨덴 복지 창구"),
     ("gothenburg", ["Gothenburg city centre", "Göteborg Västra Götaland"], "Kumlin & Rothstein · 예테보리(서부 스웨덴)"),
     ("korea_dong_office", ["주민센터", "Dong community service center Seoul"], "엔딩·2부 · 한국 주민센터"),
     ("korea_seoul_street", ["Seoul residential neighborhood alley", "Seoul apartment complex"], "한국 거리")]
OK = ("Public domain", "CC0", "CC BY ", "CC BY-SA", "CC-BY", "CC BY 4.0", "CC BY-SA 4.0", "CC BY 3.0", "CC BY-SA 3.0", "CC BY 2.0", "CC BY-SA 2.0")


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)


for alias, queries, note in Q:
    if alias in idx: continue
    got = False
    for q in queries:
        if got: break
        try:
            time.sleep(5)
            s = api({"action": "query", "list": "search", "srsearch": q + " filetype:bitmap", "srnamespace": 6, "srlimit": 8, "format": "json"})
            hits = [h["title"] for h in s["query"]["search"] if h["title"].lower().endswith((".jpg", ".jpeg"))]
            for title in hits[:5]:
                time.sleep(5)
                j = api({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1800, "format": "json"})
                ii = next(iter(j["query"]["pages"].values())).get("imageinfo", [{}])[0]; md = ii.get("extmetadata", {})
                lic = md.get("LicenseShortName", {}).get("value", "")
                if not any(lic.startswith(o) or o in lic for o in OK) or ii.get("width", 0) < 1400 or ii.get("width", 0) < ii.get("height", 0) * 1.1: continue
                artist = re.sub(r"<[^>]+>", "", html.unescape(md.get("Artist", {}).get("value", ""))).strip()[:60]
                time.sleep(3); data = urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=120).read()
                open(os.path.join(OUT, alias + ".jpg"), "wb").write(data)
                idx[alias] = {"title": title, "note": note, "license": lic, "artist": artist, "page": ii.get("descriptionurl", ""), "file": alias + ".jpg", "kb": len(data) // 1024}
                print("ok", alias, "|", title[:55], "|", lic, "|", artist[:25], "|", len(data) // 1024, "KB"); got = True; break
        except Exception as e:
            print("실패", alias, q, str(e)[:60])
    if not got: print("못 찾음:", alias)
json.dump(idx, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("총", len(idx))
