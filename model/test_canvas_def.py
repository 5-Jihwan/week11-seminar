"""정의 노드 걸음: 사회자본(내 정의) → 사회통합실태조사 → 대인신뢰 + 도움 요청 + 단체 참여 문항 묶기 → 공공서비스(IV) 잇기 → 검증 패널에 정의 문장·닮은 선행연구 5편.
실행: python model/test_canvas_def.py"""
import os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(HERE, "canvas.html").replace("\\", "/")
SHOT = os.path.join(os.path.dirname(HERE), "data", "raw", "model_shots")
errors = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 760})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL)
    pg.click("#pal .card:has-text('사회자본(내 정의)')")
    pg.click("#nbody .opt:has-text('사회통합실태조사')")
    for q in ["일반적으로 사람들을", "도와줄 사람 수", "사회단체에 대하여"]: pg.click(f"#nbody .opt:has-text('{q}')")
    deftxt = pg.locator("#nbody .iss.ok").inner_text(); pg.screenshot(path=os.path.join(SHOT, "canvas_def_panel.png"))
    pg.click("[data-x=npanel]")
    pg.click("#pal .card:has-text('공공서비스')"); pg.click("#pop button:has-text('IV')"); pg.click("#nbody .srv:has-text('사회통합실태조사') + .opt")
    ids = pg.eval_on_selector_all("#nodes .node", "els => els.map(e => e.dataset.id)")
    pg.click(f"#nodes .node[data-id='{ids[1]}']"); pg.click(f"#nodes .node[data-id='{ids[0]}']")
    pg.wait_for_selector("#vpanel.on", timeout=6000); pg.screenshot(path=os.path.join(SHOT, "canvas_def_validator.png"), full_page=True)
    body = pg.locator("#vbody").inner_text()
    n_match = pg.locator("#vbody .sec:has-text('닮은 선행연구')").count(); titles = pg.eval_on_selector_all("#vbody .sec:has-text('닮은 선행연구') ~ .iss b", "els => els.slice(0,5).map(e => e.textContent)")
    print("정의:", deftxt.splitlines()[0]); print("닮은 선행연구 섹션", n_match, "·", titles)
    print("계보:", "5장 K&R 매개" in body or "밖" in body or "K&R" in body, "· 오류 배지:", pg.locator("#badge").inner_text())
    b.close()
print("page errors:", errors or "없음"); assert not errors and n_match == 1 and len(titles) >= 3
