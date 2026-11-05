"""model/canvas.html v4(Galpi 화면 구조) 걸음: 자료 고르기 → 대인신뢰 문항을 빈 곳에(역할 팝 → DV) → 도움 문항을 그 변수 위에 놓아 묶기 → 이름 바꾸기
→ 공공서비스 문항을 빈 곳에(IV) → 잇기 → 검증 배지·서랍(정의·선행연구·가설) → 서랍 폭 끌어 조절 → DV→IV 거꾸로 오류 → 제출 잠김 → 제출 → dashboard.html 반영.
실행: python model/test_canvas.py"""
import os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(HERE, "canvas.html").replace("\\", "/")
DASH = "file:///" + os.path.join(HERE, "dashboard.html").replace("\\", "/")
SHOT = os.path.join(os.path.dirname(HERE), "data", "raw", "model_shots"); os.makedirs(SHOT, exist_ok=True)
errors = []


def drag(pg, sel, x, y):
    pg.locator(sel).first.scroll_into_view_if_needed()
    b = pg.locator(sel).first.bounding_box(); pg.mouse.move(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2); pg.mouse.down()
    pg.mouse.move(x, y, steps=8); pg.mouse.up()


with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 780}); pg = ctx.new_page()
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL); pg.fill("#nick", "가")
    pg.click("#gate .surv:has-text('사회통합실태조사')")
    assert pg.locator("#gate").is_hidden() and pg.locator("#pcontent .vcard").count() > 5, "자료 선택 뒤 팔레트가 안 채워짐"
    cv = pg.locator("#cv").bounding_box()
    drag(pg, "#pcontent .vcard:has-text('일반적으로 사람들을')", cv["x"] + cv["width"] * 0.72, cv["y"] + 140)   # 빈 곳 → 역할 팝
    pg.click("#pop button[data-r=DV]")
    assert pg.locator("#nodes .node").count() == 1 and pg.locator("#dpanel.on").count() == 1, "새 변수·서랍이 안 열림"
    pg.fill("#nm", "내 사회자본"); pg.press("#nm", "Tab"); pg.wait_for_timeout(300)  # 서랍이 열리며 노드가 캔버스 안으로 당겨진 뒤 좌표를 잰다
    nb = pg.locator("#nodes .node").first.bounding_box()
    drag(pg, "#pcontent .vcard:has-text('도와줄 사람 수')", nb["x"] + nb["width"] / 2, nb["y"] + nb["height"] / 2)      # 변수 위 → 묶기
    n_items = pg.locator("#dbody .item").count(); assert n_items == 2, f"묶기 실패: {n_items}"
    deftxt = pg.locator("#dbody .def").inner_text().splitlines()[0]
    drag(pg, "#pcontent .vcard:has-text('공공서비스를 경험')", cv["x"] + cv["width"] * 0.15, cv["y"] + 140)              # 빈 곳 → IV
    pg.click("#pop button[data-r=IV]")
    ids = pg.eval_on_selector_all("#nodes .node", "els => els.map(e => e.dataset.id)")
    pg.click(f"#nodes .node[data-id='{ids[1]}']"); pg.click(f"#nodes .node[data-id='{ids[0]}']")                     # IV → DV
    assert pg.locator("#edges path.edge").count() == 1, "경로가 안 생김"
    pg.click("#vbtn"); vb = pg.locator("#vbody").inner_text()
    pg.click(".sbtn[data-d=studies]"); titles = pg.eval_on_selector_all("#dbody .study .ti", "els => els.slice(0,5).map(e => e.textContent)")
    lin = pg.locator("#dbody .def b").inner_text()
    w0 = pg.locator("#dpanel").bounding_box()["width"]; h = pg.locator("#dhandle").bounding_box()                    # 서랍 폭 조절
    pg.mouse.move(h["x"] + 3, h["y"] + 200); pg.mouse.down(); pg.mouse.move(h["x"] - 200, h["y"] + 200, steps=5); pg.mouse.up()
    w1 = pg.locator("#dpanel").bounding_box()["width"]
    pg.screenshot(path=os.path.join(SHOT, "v4_studies.png"))
    print("정의:", deftxt); print("계보:", lin); print("닮은 선행연구:", titles[:3]); print("가설 H1:", "H1." in vb, "· 배지:", pg.locator("#vbtn").inner_text().strip(), f"· 서랍 {w0:.0f}→{w1:.0f}px")
    pg.fill("#q", "공공서비스 경험은 신뢰와 관련이 있는가")
    pg.click(f"#nodes .node[data-id='{ids[0]}']"); pg.click(f"#nodes .node[data-id='{ids[1]}']")                     # DV → IV 거꾸로
    pg.click("#vbtn"); rev = pg.locator("#vbody .iss.err:has-text('역방향')").count(); locked = pg.locator("#submit").is_disabled()
    print("역방향 오류:", rev, "· 제출 잠김:", locked)
    pg.screenshot(path=os.path.join(SHOT, "v4_reverse.png"))
    pg.evaluate("() => {st.edges.pop(); touch();}"); pg.click("#submit"); pg.wait_for_timeout(200)                    # 거꾸로 지우고 제출
    sub = pg.locator("#submit").inner_text().strip()
    d = ctx.new_page(); d.on("pageerror", lambda e: errors.append("dash:" + str(e))); d.goto(DASH)                   # 대시보드(같은 컨텍스트 → 같은 localStorage)
    rows = d.locator(".tbl tr[data-i]").count(); first = d.locator(".tbl tr[data-i]").first.inner_text()
    d.click(".tbl tr[data-i]"); spot_nodes = d.locator("#diag .nd").count(); d.screenshot(path=os.path.join(SHOT, "v4_dash_spot.png"))
    d.click("#mx"); d.on("dialog", lambda dl: dl.accept()); d.click("#demo"); rows17 = d.locator(".tbl tr[data-i]").count()
    d.screenshot(path=os.path.join(SHOT, "v4_dash17.png"), full_page=True)
    print("제출:", sub, "· 대시보드 행:", rows, "· 첫 행:", first.replace("\t", " | ")[:90]); print("spotlight 노드:", spot_nodes, "· 17명 생성 후 행:", rows17)
    b.close()
print("page errors:", errors or "없음")
assert not errors and rev == 1 and locked and len(titles) >= 3 and w1 > w0 + 100 and rows == 1 and spot_nodes == 2 and rows17 == 17
