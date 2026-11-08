"""model/canvas.html v5 걸음: 자료 → 개념화(구조적·개인) → 대인신뢰 문항을 빈 곳에(역할 팝 → DV) → 도움 문항을 그 변수 위에 묶기 → 이름 바꾸기
→ 공공서비스 문항(IV) → 잇기 → 개념·측정 간격 경고(구조적이라 했는데 신뢰만) → 호혜 문항 묶어 해소 → 성별을 조절(ZV)로 → ZV→DV → 조절 가설
→ 서랍(칸·선행연구) + 폭 조절 → DV→IV 역방향 오류 → 제출 잠김 → 제출 → dashboard.html 반영 · 17명 생성 · spotlight.
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


def drop_new(pg, sel, x, y, role):
    drag(pg, sel, x, y); pg.click(f"#pop button[data-r={role}]"); pg.wait_for_timeout(300)


def closep(pg):  # 검증·유사도 패널이 노드를 가리면 닫는다(실사용자는 X를 누름)
    pg.evaluate("() => {document.getElementById('vpanel').classList.remove('on'); document.getElementById('spanel').classList.remove('on');}")


def node_box(pg, i):  # draw()가 노드를 다시 그리는 순간이면 None이 올 수 있어 한 번 더 잰다
    for _ in range(5):
        bb = pg.locator("#nodes .node").nth(i).bounding_box()
        if bb: return bb
        pg.wait_for_timeout(200)
    raise AssertionError("노드 좌표를 못 잼")


with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1200, "height": 780}); pg = ctx.new_page()
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL); pg.fill("#nick", "가")
    pg.click("#gate .surv:has-text('사회통합실태조사')")
    assert pg.locator("#ctext").count() == 1, "개념화 단계가 안 뜸"
    pg.fill("#ctext", "어려울 때 도움을 주고받는 관계"); pg.click("#cdim button[data-v=structural]"); pg.click("#clevel button[data-v=individual]"); pg.click("#cgo")
    assert pg.locator("#gate").is_hidden() and pg.locator("#pcontent .vcard").count() > 5, "팔레트가 안 채워짐"
    cv = pg.locator("#cv").bounding_box()
    drop_new(pg, "#pcontent .vcard:has-text('일반적으로 사람들을')", cv["x"] + cv["width"] * 0.72, cv["y"] + 180, "DV")
    assert pg.locator("#nodes .node").count() == 1 and pg.locator("#dpanel.on").count() == 1, "새 변수·서랍이 안 열림"
    pg.fill("#nm", "내 사회자본"); pg.press("#nm", "Tab"); pg.wait_for_timeout(300)
    drop_new(pg, "#pcontent .vcard:has-text('공공서비스를 경험')", cv["x"] + cv["width"] * 0.12, cv["y"] + 180, "IV")
    ids = pg.eval_on_selector_all("#nodes .node", "els => els.map(e => e.dataset.id)")
    pg.click(f"#nodes .node[data-id='{ids[1]}']"); pg.click(f"#nodes .node[data-id='{ids[0]}']")                     # IV → DV
    pg.click("#vbtn"); gap1 = pg.locator("#vbody .iss.warn:has-text('구조적')").count()                             # 개념은 구조적인데 측정은 신뢰뿐
    nb = node_box(pg, 0); drag(pg, "#pcontent .vcard:has-text('도와줄 사람 수')", nb["x"] + nb["width"] / 2, nb["y"] + nb["height"] / 2)   # 호혜 문항 묶기 → 해소
    pg.wait_for_timeout(200); n_items = pg.locator("#dbody .item").count(); gap2 = pg.locator("#vbody .iss.warn:has-text('구조적')").count()
    deftxt = pg.locator("#dbody .def").first.inner_text().splitlines()[0]
    closep(pg); drop_new(pg, "#pcontent .vcard:has-text('성별')", cv["x"] + cv["width"] * 0.42, cv["y"] + 90, "ZV")               # 집단 비교
    ids = pg.eval_on_selector_all("#nodes .node", "els => els.map(e => e.dataset.id)"); closep(pg)
    pg.click(f"#nodes .node[data-id='{ids[2]}']"); pg.click(f"#nodes .node[data-id='{ids[0]}']")                     # ZV → DV
    pg.click("#vbtn"); pg.wait_for_timeout(150)  # 검증 패널을 열어야 가설 칸이 그려진다
    vb = " ".join(pg.locator("#vbody textarea").evaluate_all("els => els.map(e => e.value)")); zv_edge = pg.locator("#edges path.edge.zv").count()
    pg.click(".sbtn[data-d=studies]"); cell = pg.locator("#dbody .def b").inner_text(); me = pg.locator("#dbody td.me").count()
    titles = pg.eval_on_selector_all("#dbody .study .ti", "els => els.slice(0,5).map(e => e.textContent)")
    w0 = pg.locator("#dpanel").bounding_box()["width"]; h = pg.locator("#dhandle").bounding_box()
    pg.mouse.move(h["x"] + 3, h["y"] + 200); pg.mouse.down(); pg.mouse.move(h["x"] - 200, h["y"] + 200, steps=5); pg.mouse.up()
    w1 = pg.locator("#dpanel").bounding_box()["width"]; pg.screenshot(path=os.path.join(SHOT, "v5_studies.png"))
    print("간격 경고 전/후:", gap1, gap2, "· 묶인 문항:", n_items); print("정의:", deftxt); print("칸:", cell, "· 격자 표시:", me)
    print("닮은 선행연구:", titles[:3]); print("조절 가설:", "따라 다를" in vb, "· ZV 점선:", zv_edge, f"· 서랍 {w0:.0f}→{w1:.0f}px")
    pg.fill("#q", "공공서비스 경험은 신뢰와 관련이 있는가"); closep(pg)
    pg.click(f"#nodes .node[data-id='{ids[0]}']"); pg.click(f"#nodes .node[data-id='{ids[1]}']")                     # DV → IV 역방향
    pg.click("#vbtn"); pg.click("#vbtn"); rev = pg.locator("#vbody .iss.err:has-text('역방향')").count(); locked = pg.locator("#submit").is_disabled()
    print("역방향 오류:", rev, "· 제출 잠김:", locked); pg.screenshot(path=os.path.join(SHOT, "v5_reverse.png"))
    closep(pg); pg.keyboard.press("Control+z"); undo_ok = pg.locator("#edges path.edge").count() == 2                                  # 되돌리기(역방향 경로 사라짐)
    pg.click(".sbtn[data-d=studies]"); tiers = pg.locator("#tiers button").all_inner_texts(); tier_rows = pg.locator("#tierlist .item").count()
    pg.click("#tiers button[data-t=다름]"); tier_rows2 = pg.locator("#tierlist .item").count()
    pg.reload(); pg.wait_for_timeout(400); restored = pg.locator("#nodes .node").count()                                    # 새로고침 복원
    closep(pg); pg.click("#pcontent .vcard:has-text('최종 학력') .addk"); pg.click("#pop button[data-r=CV]"); pg.wait_for_timeout(200); added = pg.locator("#nodes .node.CV").count()   # + 버튼
    pg.click("#vbtn"); pg.fill("#vbody textarea[data-h='0']", "H1. 공공서비스를 겪은 사람은 신뢰가 높을 것이다."); pg.press("#vbody textarea[data-h='0']", "Tab")
    pg.click("#submit"); pg.wait_for_timeout(200); sub = pg.locator("#submit").inner_text().strip()
    d = ctx.new_page(); d.on("pageerror", lambda e: errors.append("dash:" + str(e))); d.goto(DASH)
    rows = d.locator(".tbl tr[data-i]").count(); first = d.locator(".tbl tr[data-i]").first.inner_text()
    d.click(".tbl tr[data-i]"); spot_nodes = d.locator("#diag .nd").count(); spot_c = d.locator("#mbox:has-text('개념화')").count(); hyp_edit = d.locator("#mbox:has-text('겪은 사람은')").count()
    d.click("#mbox [data-v='좋은 빈자리다']"); d.wait_for_timeout(200); d.screenshot(path=os.path.join(SHOT, "v5_dash_spot.png")); d.click("#mx")
    pg.bring_to_front(); pg.evaluate("pollVerdict()"); pg.wait_for_timeout(200); verdict = pg.locator("#verdict").inner_text()
    d.bring_to_front(); d.on("dialog", lambda dl: dl.accept()); d.click("#demo"); rows17 = d.locator(".tbl tr[data-i]").count()
    d.evaluate("() => {const s=document.getElementById('rw'); s.value=+s.min+60000; s.dataset.touched=1; rewind(+s.value);}"); rw = d.locator("#rwlab").inner_text()
    d.screenshot(path=os.path.join(SHOT, "v5_dash17.png"), full_page=True)
    pg.evaluate("loadPeers()"); pg.click(".sbtn[data-d=def]"); pg.click(".sbtn[data-d=studies]"); peers_n = pg.locator("#dbody:has-text('옆 사람')").count()
    print("제출:", sub, "· 대시보드 행:", rows, "· 첫 행:", first.replace("\t", " | ")[:110]); print("spotlight 노드:", spot_nodes, "개념화:", spot_c, "가설 수정 반영:", hyp_edit, "· 17명 후 행:", rows17)
    print("되돌리기:", undo_ok, "· 등급:", tiers, "닮음", tier_rows, "다름", tier_rows2, "· 복원 노드:", restored, "· + 버튼 CV:", added); print("판정 수신:", verdict, "· 되감기:", rw, "· 옆 사람:", peers_n)
    # 비동기 선행연구(studies.js)·같은 자료 빈자리·가중치 고지
    n_st = pg.evaluate("STUDIES.length"); pg.click("#sbtn"); pg.wait_for_timeout(200); sim_html = pg.locator("#sbody").inner_html()
    print("선행연구 적재:", n_st, "· 같은 자료 문구:", "결과로 본 선행연구" in sim_html, "· 가중치 고지:", "임의 가중치" in sim_html)
    # 폰(390px): 끌기 없이 + 버튼으로 변수 → 자동 맞춤, 배지 유지
    m = b.new_context(viewport={"width": 390, "height": 780}, is_mobile=True, has_touch=True).new_page(); m.on("pageerror", lambda e: errors.append("mobile:" + str(e)))
    m.goto(URL); m.evaluate("localStorage.clear()"); m.reload(); m.fill("#nick", "나"); m.click("#gate .surv:has-text('사회통합실태조사')")
    m.fill("#ctext", "믿음"); m.click("#cdim button[data-v=cognitive]"); m.click("#clevel button[data-v=individual]"); m.click("#cgo")
    m.click("#mobpick"); m.click("#pcontent .vcard:has-text('일반적으로 사람들을') .addk"); m.click("#pop button[data-r=DV]"); m.wait_for_timeout(300)
    m.click("#mobpick"); m.click("#pcontent .vcard:has-text('공공서비스를 경험') .addk"); m.click("#pop button[data-r=IV]"); m.wait_for_timeout(300)
    mob_nodes = m.locator("#nodes .node").count(); mob_in = m.evaluate("[...document.querySelectorAll('#nodes .node')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=390})")
    mob_badge = m.locator("#sbtn").is_visible(); m.screenshot(path=os.path.join(SHOT, "v5_mobile.png"))
    print("폰 노드:", mob_nodes, "· 화면 안:", mob_in, "· 유사도 배지:", mob_badge)
    b.close()
print("page errors:", errors or "없음")
assert n_st > 7000 and "결과로 본 선행연구" in sim_html and "임의 가중치" in sim_html and mob_nodes == 2 and mob_in and mob_badge
assert not errors and gap1 == 1 and gap2 == 0 and n_items == 2 and zv_edge == 1 and "따라 다를" in vb and me == 1 and rev == 1 and locked and len(titles) >= 3 and w1 > w0 + 100 and rows == 1 and spot_nodes == 4 and spot_c == 1 and rows17 == 17
assert undo_ok and restored == 3 and added == 1 and hyp_edit == 1 and "빈자리" in verdict and tier_rows > 0 and len(tiers) == 4 and "제출" in rw and peers_n == 1
