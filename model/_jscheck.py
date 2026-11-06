import re, subprocess, os
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
for f in ["canvas", "dashboard"]:
    h = open(os.path.join(H, f + ".html"), encoding="utf-8").read(); js = re.search(r"<script>([\s\S]*)</script>", h).group(1)
    tmp = os.path.join(H, "_tmp.js"); open(tmp, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True, encoding="utf-8", errors="replace"); print(f, "js ok" if r.returncode == 0 else "JS ERROR " + r.stderr[:900]); os.remove(tmp)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.on("pageerror", lambda e: print("PAGEERR", e)); pg.goto("file:///" + os.path.join(H, "canvas.html").replace("\\", "/")); pg.wait_for_timeout(1500); print("surv cards", pg.locator("#gate .surv").count()); b.close()
