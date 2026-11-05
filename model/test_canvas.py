"""model/canvas.html 걸음: 종속(복지패널 대인신뢰) → 독립(선별 수급) → 잇기 → 3초 뒤 검증 패널(계보 K&R) → 다른 조사 문항 회색 안내 → 거꾸로 화살표 오류 → 제출.
실행: python model/test_canvas.py"""
import os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(HERE, "canvas.html").replace("\\", "/")
SHOT = os.path.join(os.path.dirname(HERE), "data", "raw", "model_shots"); os.makedirs(SHOT, exist_ok=True)
errors = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 700})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL); pg.fill("#nick", "가")
    pg.click("#pal .card:has-text('대인신뢰')"); pg.click("#pop button:has-text('DV')")          # 역할 팝오버
    assert pg.locator("#npanel.on").count() == 1, "노드 패널이 안 열림"
    pg.click("#nbody .srv:has-text('한국복지패널') + .opt")                                         # 문항 고르기 → 자료 확정
    pg.click("#pal .card:has-text('선별 수급')"); pg.click("#pop button:has-text('IV')")
    pg.click("#nbody .srv:has-text('한국복지패널') + .opt")
    pg.click("#pal .card:has-text('공공서비스')"); pg.click("#pop button:has-text('IV')")
    grey = pg.locator("#nbody .opt.grey").count(); pg.locator("#nbody .opt.grey").first.click()
    assert pg.locator("#nbody .iss.err:has-text('같은 사람에게 없습니다')").count() == 1, "회색 안내 없음"
    pg.click("#del")                                                                                 # 못 쓰는 노드는 지움
    ids = pg.eval_on_selector_all("#nodes .node", "els => els.map(e => e.dataset.id)")
    pg.click(f"#nodes .node[data-id='{ids[1]}']"); pg.click(f"#nodes .node[data-id='{ids[0]}']")     # IV → DV 잇기
    pg.wait_for_selector("#vpanel.on", timeout=6000)                                                 # 3초 멈춤 → 자동 열림
    pg.screenshot(path=os.path.join(SHOT, "canvas_validator.png"))
    txt = pg.locator("#vbody").inner_text()
    print("회색", grey, "· 계보 OK" if "5장 K&R" in txt else "· 계보 MISMATCH", "· 가설", txt.count("H1."), "· 오류 배지:", pg.locator("#badge").inner_text())
    pg.click("[data-x=vpanel]"); pg.click(f"#nodes .node[data-id='{ids[0]}']"); pg.click("[data-x=npanel]")   # DV 선택 상태로
    pg.click(f"#nodes .node[data-id='{ids[0]}']"); pg.click(f"#nodes .node[data-id='{ids[1]}']")     # DV → IV (거꾸로)
    pg.wait_for_timeout(300); pg.click("#badge"); rev = pg.locator("#vbody .iss.err:has-text('거꾸로')").count()
    print("거꾸로 화살표 오류:", rev, "· 제출 버튼:", pg.locator("#submit").inner_text())
    pg.screenshot(path=os.path.join(SHOT, "canvas_reverse.png"))
    b.close()
print("page errors:", errors or "없음"); assert not errors and rev == 1
