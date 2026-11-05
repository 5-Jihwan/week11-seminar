"""model/canvas.html v3 걸음(마우스 끌기): 자료 고르기(사회통합실태조사) → 대인신뢰 문항을 빈 곳에 놓기(DV) → 도움 요청 문항을 그 변수 위에 놓아 묶기 → 이름 바꾸기
→ 공공서비스 문항을 빈 곳에(IV) → 잇기 → 3초 뒤 검증 패널(정의 문장·계보·닮은 선행연구·가설) → DV→IV 거꾸로 오류 → 제출 잠김.
실행: python model/test_canvas.py"""
import os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(HERE, "canvas.html").replace("\\", "/")
SHOT = os.path.join(os.path.dirname(HERE), "data", "raw", "model_shots"); os.makedirs(SHOT, exist_ok=True)
errors = []


def drag(pg, sel, x, y):  # 포인터 이벤트 기반이라 mouse로 끈다
    pg.locator(sel).first.scroll_into_view_if_needed()  # 팔레트가 길어 아래 카드는 스크롤해야 보인다
    b = pg.locator(sel).first.bounding_box(); pg.mouse.move(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2); pg.mouse.down()
    pg.mouse.move(x, y, steps=8); pg.mouse.up()


with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 760})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL); pg.fill("#nick", "가")
    pg.click("#gate .opt:has-text('사회통합실태조사')")
    assert pg.locator("#gate").is_hidden() and pg.locator("#pal .card").count() > 5, "자료 선택 뒤 팔레트가 안 채워짐"
    cv = pg.locator("#cv").bounding_box()
    drag(pg, "#pal .card:has-text('일반적으로 사람들을')", cv["x"] + cv["width"] * 0.72, cv["y"] + 120)   # 빈 곳 → 새 변수(DV)
    assert pg.locator("#nodes .node").count() == 1 and pg.locator("#npanel.on").count() == 1, "새 변수가 안 생김"
    pg.fill("#nm", "내 사회자본"); pg.press("#nm", "Tab")
    nb = pg.locator("#nodes .node").first.bounding_box()
    drag(pg, "#pal .card:has-text('도와줄 사람 수')", nb["x"] + nb["width"] / 2, nb["y"] + nb["height"] / 2)      # 변수 위 → 묶기
    n_items = pg.locator("#nbody .item").count(); assert n_items == 2, f"묶기 실패: {n_items}"
    deftxt = pg.locator("#nbody .iss.ok").inner_text()
    pg.click("[data-x=npanel]")
    drag(pg, "#pal .card:has-text('공공서비스를 경험')", cv["x"] + cv["width"] * 0.2, cv["y"] + 120)              # 빈 곳 → IV
    pg.click("[data-x=npanel]")
    ids = pg.eval_on_selector_all("#nodes .node", "els => els.map(e => e.dataset.id)")
    pg.click(f"#nodes .node[data-id='{ids[1]}']"); pg.click(f"#nodes .node[data-id='{ids[0]}']")                     # IV → DV
    pg.wait_for_selector("#vpanel.on", timeout=6000); pg.screenshot(path=os.path.join(SHOT, "v3_validator.png"), full_page=True)
    body = pg.locator("#vbody").inner_text(); titles = pg.eval_on_selector_all("#vbody .sec:has-text('닮은 선행연구') ~ .iss b", "els => els.slice(0,5).map(e => e.textContent)")
    print("정의:", deftxt.splitlines()[0]); print("닮은 선행연구:", titles[:3]); print("가설 H1:", "H1." in body, "· 배지:", pg.locator("#badge").inner_text())
    pg.click("[data-x=vpanel]"); pg.click(f"#nodes .node[data-id='{ids[0]}']"); pg.click("[data-x=npanel]")
    pg.click(f"#nodes .node[data-id='{ids[0]}']"); pg.click(f"#nodes .node[data-id='{ids[1]}']")                     # DV → IV 거꾸로
    pg.wait_for_timeout(300); pg.click("#badge"); rev = pg.locator("#vbody .iss.err:has-text('거꾸로')").count()
    print("거꾸로 오류:", rev, "· 제출 버튼:", pg.locator("#submit").inner_text())
    pg.screenshot(path=os.path.join(SHOT, "v3_reverse.png"))
    b.close()
print("page errors:", errors or "없음"); assert not errors and rev == 1 and len(titles) >= 3
