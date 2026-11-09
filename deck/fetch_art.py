# -*- coding: utf-8 -*-
"""쟁점 장 명화 후보: 위키미디어 커먼즈 API로 파일 정보(라이선스·작가·연도)와 1600px 썸네일을 받아 deck/art/ 에 저장, deck/art/index.json 에 출처를 기록.
퍼블릭 도메인(PD-Art/PD-old)인 것만 남긴다. 실행: python deck/fetch_art.py"""
import json, os, sys, io, urllib.request, urllib.parse, re, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "art"); os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "week11-seminar-deck/0.1 (educational; contact via github 5-Jihwan)"}
# (별칭, 커먼즈 파일명, 쓰일 쟁점 느낌)
CANDS = [
    ("hogarth_polling", "File:William Hogarth 031.jpg", "Hogarth, The Polling(1755) — 투표·직접민주주의"),
    ("hogarth_canvassing", "File:William Hogarth 029.jpg", "Hogarth, Canvassing for Votes — 표를 사는 정치"),
    ("tax_collectors", "File:Marinus van Reymerswaele - The Tax Collectors - WGA19325.jpg", "Reymerswaele, 세금 징수관 — 심사·창구"),
    ("moneylender", "File:Quentin Massys - The Moneylender and his Wife - WGA14281.jpg", "Metsys, 환전상 부부 — 계산·심사"),
    ("cardsharps", "File:Caravaggio - I Bari.jpg", "Caravaggio, 카드 사기꾼 — 속임·불신"),
    ("doubting_thomas", "File:Caravaggio - The Incredulity of Saint Thomas.jpg", "Caravaggio, 의심하는 토마 — 증거 없이는 못 믿음"),
    ("anatomy_lesson", "File:Rembrandt - The Anatomy Lesson of Dr Nicolaes Tulp.jpg", "Rembrandt, 해부학 강의 — 해부·분해"),
    ("netherlandish_proverbs", "File:Pieter Bruegel the Elder - The Dutch Proverbs - Google Art Project.jpg", "Bruegel, 네덜란드 속담 — 마을·온갖 행동"),
    ("peasant_wedding", "File:Pieter Bruegel the Elder - Peasant Wedding - Google Art Project 2.jpg", "Bruegel, 농민의 결혼 — 마을 모임"),
    ("blind_leading", "File:Pieter Bruegel the Elder (1568) The Blind Leading the Blind.jpg", "Bruegel, 장님을 이끄는 장님 — 틀 없는 실천"),
    ("zaporozhian", "File:Repin Cossacks.jpg", "Repin, 자포로제 카자크의 답장 — 집단 서명·집합행동"),
    ("death_of_socrates", "File:David - The Death of Socrates.jpg", "David, 소크라테스의 죽음 — 토론·논증"),
    ("school_of_athens", "File:%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg", "Raphael, 아테네 학당 — 이론가들"),
    ("gleaners", "File:Jean-François Millet - Gleaners - Google Art Project 2.jpg", "Millet, 이삭 줍는 여인들 — 최저층"),
    ("third_class", "File:Honoré Daumier - The Third-Class Carriage - Google Art Project.jpg", "Daumier, 삼등 객차 — 계층"),
    ("card_players", "File:Les Joueurs de cartes, par Paul Cézanne.jpg", "Cézanne, 카드놀이 — 두 사람의 대결"),
    ("night_watch", "File:The Night Watch - HD.jpg", "Rembrandt, 야경 — 시민 민병대·결사체"),
    ("syndics", "File:Rembrandt - De Staalmeesters- het college van staalmeesters (waardijns) van het Amsterdamse lakenbereidersgilde - Google Art Project.jpg", "Rembrandt, 직물 길드 이사들 — 위원회·심사"),
    ("daumier_lawyers", "File:Honoré Daumier - Three Lawyers - Walters 37112.jpg", "Daumier, 변호사 셋 — 절차·법"),
    ("washington_delaware", "File:Washington Crossing the Delaware by Emanuel Leutze, MMA-NYC, 1851.jpg", "Leutze, 델라웨어 도하 — 참전·국가"),
]
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
idx = {}
for alias, title, note in CANDS:
    try:
        j = api({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1600, "format": "json"})
        page = next(iter(j["query"]["pages"].values()))
        if "imageinfo" not in page: print("없음:", alias, title); continue
        ii = page["imageinfo"][0]; md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", ""); artist = re.sub(r"<[^>]+>", "", html.unescape(md.get("Artist", {}).get("value", ""))).strip()
        date = re.sub(r"<[^>]+>", "", md.get("DateTimeOriginal", {}).get("value", ""))[:40]
        if "Public domain" not in lic and "PD" not in lic and "CC0" not in lic: print("PD 아님:", alias, lic); continue
        data = urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=120).read()
        ext = ".jpg"; p = os.path.join(OUT, alias + ext); open(p, "wb").write(data)
        idx[alias] = {"title": title, "note": note, "license": lic, "artist": artist[:80], "date": date, "page": ii.get("descriptionurl", ""), "file": alias + ext, "kb": len(data) // 1024}
        print("ok", alias, lic, "|", artist[:40], "|", date, "|", len(data) // 1024, "KB")
    except Exception as e:
        print("실패:", alias, str(e)[:80])
json.dump(idx, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("저장", len(idx))
