"""model/index.html 데모 자동 걸음: 세 조합을 끝까지 눌러 결과 카드·계보·회색 안내·집계를 확인하고 화면을 찍는다.
실행: python model/test_index.py (playwright 필요)"""
import os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(HERE, "index.html").replace("\\", "/")
SHOT = os.path.join(os.path.dirname(HERE), "data", "raw", "model_shots"); os.makedirs(SHOT, exist_ok=True)
CASES = [  # (별명, 종속 라벨, 문항 조사명 일부, 독립 라벨들, 매개 라벨, 질문, 기대 계보)
    ("가", "대인신뢰", "한국복지패널", ["선별 수급"], "없음", "수급 심사 경험은 대인신뢰와 관련이 있는가", "5장 K&R"),
    ("나", "이웃 신뢰", "지역사회건강조사", ["선별 수급", "지역"], "없음", "", "1장 Krishna"),  # 규칙 6(지역)이 10(수급)보다 먼저
    ("다", "단체 참여", "사회통합실태조사", ["공공서비스"], "공정성", "참여 제도가 단체 참여에 영향을 미치는가", "밖"),
]
errors = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 420, "height": 860})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    for n, (nick, dv, srv, ivs, med, q, want) in enumerate(CASES, 1):
        pg.goto(URL); pg.fill("#nick", nick); pg.click("#next")
        pg.click(f"#dv .opt:has-text('{dv}')"); pg.click("#next")
        pg.screenshot(path=os.path.join(SHOT, f"c{n}_s2.png"), full_page=True)
        pg.click(f"#items .srv:has-text('{srv}') + .opt"); pg.click("#next")
        grey = pg.locator("#iv .opt.grey").count()
        if grey: pg.locator("#iv .opt.grey").first.click(); assert pg.locator("#ivwhy .why").count() == 1, "회색 안내 없음"
        for iv in ivs: pg.click(f"#iv .opt:not(.grey):has-text('{iv}')")
        pg.screenshot(path=os.path.join(SHOT, f"c{n}_s3.png"), full_page=True); pg.click("#next")
        pg.click(f"#med .opt:not(.grey):has-text('{med}')"); pg.click("#next")
        pg.fill("#q", q); pg.click("#next")
        pg.screenshot(path=os.path.join(SHOT, f"c{n}_s6.png"), full_page=True); pg.click("#next")
        pg.screenshot(path=os.path.join(SHOT, f"c{n}_s7.png"), full_page=True)
        lin = pg.locator("#cards .lin").inner_text(); n_rev = pg.locator("#cards .card").nth(2).locator("p").count()
        print(f"[{nick}] {dv}·{srv}·{ivs}·{med} → 회색 {grey} · 계보 '{lin.splitlines()[0]}' · 리뷰 문단 {n_rev} · 기대 {want} {'OK' if want in lin else 'MISMATCH'}")
    agg = pg.locator("#agg").inner_text(); print("집계:", agg.splitlines()[0] if agg else "(없음)")
    b.close()
print("page errors:", errors or "없음")
assert not errors
