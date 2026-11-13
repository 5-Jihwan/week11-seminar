# -*- coding: utf-8 -*-
"""발표자용 논문 5편 정리(docs/brief/*.md)를 자립 HTML 한 파일로. pandoc 필요.
실행: python docs/build_brief.py [출력 경로]"""
import glob, html, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, "발표자_논문5편_정리.html")
SRC = sys.argv[2] if len(sys.argv) > 2 else "brief"  # docs/ 아래 원고 폴더(brief 또는 methods)
TITLE = {"brief": "11주차 지정문헌 5편 · 발표자용 정리", "methods": "11주차 지정문헌 5편 · 방법론 정리"}[SRC]
parts = []
for f in sorted(glob.glob(os.path.join(H, SRC, "*.md"))):
    body = subprocess.run(["pandoc", "-f", "gfm+hard_line_breaks" if SRC == "methods" else "gfm", "-t", "html", f], capture_output=True, text=True, encoding="utf-8", check=True).stdout  # 방법론은 모형식을 줄마다 쓰므로 줄바꿈을 살린다
    sid = os.path.basename(f)[:2]
    parts.append((sid, re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S).group(1), f'<section id="p{sid}">{body}</section>'))
assert len(parts) == 6, [p[0] for p in parts]
toc = "".join(f'<a href="#p{s}">{re.sub("<[^>]+>", "", t)}</a>' for s, t, _ in parts)
CSS = """:root{--ink:#15203a;--sub:#5a6577;--line:#e2e6ec;--navy:#072A60;--navyt:#eef2f8;--paper:#fff}
@media (prefers-color-scheme:dark){:root{--ink:#e6e9ef;--sub:#a3acba;--line:#2c3442;--navy:#9fbaf0;--navyt:#1b2433;--paper:#11161f}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Pretendard,"Malgun Gothic","Apple SD Gothic Neo",sans-serif;font-size:16px;line-height:1.75;word-break:keep-all}
header{max-width:860px;margin:0 auto;padding:40px 16px 8px}header h1{font-size:26px;color:var(--navy);margin:0 0 4px}header p{color:var(--sub);margin:0}
nav{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--line);z-index:2}nav div{max-width:860px;margin:0 auto;padding:8px 16px;display:flex;gap:6px 16px;flex-wrap:wrap;font-size:14px}nav a{color:var(--navy);text-decoration:none}
main{max-width:860px;margin:0 auto;padding:8px 16px 80px}section{border-top:2px solid var(--navy);margin-top:44px;padding-top:6px}
h2{font-size:22px;color:var(--navy);margin:12px 0 6px}h3{font-size:17px;color:var(--navy);margin:28px 0 6px;padding-bottom:4px;border-bottom:1px solid var(--line)}
p,li{margin:6px 0}ul,ol{padding-left:22px}table{border-collapse:collapse;width:100%;font-size:14px;margin:10px 0;display:block;overflow-x:auto}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--navyt)}
code{font-size:13px}@media print{nav{display:none}section{break-before:page}body{font-size:12.5px}}"""
doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE.split(" · ")[1]}</title><style>{CSS}</style></head><body>
<header><h1>{TITLE}</h1><p>사회자본과 공공정책 · 2026-11-13 · 원문 PDF 인쇄 쪽 기준</p></header>
<nav><div>{toc}</div></nav><main>{"".join(p[2] for p in parts)}</main></body></html>"""
open(out, "w", encoding="utf-8").write(doc); print(out, len(doc) // 1024, "KB")
