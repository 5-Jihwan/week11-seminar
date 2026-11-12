# -*- coding: utf-8 -*-
"""1부 발표덱 빌드. 두 벌을 만든다.
  deck/week11_part1.html        공개판(GitHub). 쟁점 장은 밈 이미지 없이 캡션 카드
  deck/week11_part1_local.html  발표판(git 제외). 쟁점 장에 밈 템플릿 이미지 + 캡션
재료: deck/fig_part1/*.png(원문 캡처, capture_paper.py), deck/memes/*.jpg(발표판), docs/papers/*_구조.md(문구 출처), docs/PAPERS.md(수치).
실행: python deck/build_part1.py"""
import base64, io, json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fontface import face, FAMILY
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))


def uri(path, w=1400, q=80):
    im = Image.open(path).convert("RGB")
    if im.width > w: im = im.resize((w, int(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


FIG = {f[:-4]: uri(os.path.join(H, "fig_part1", f)) for f in os.listdir(os.path.join(H, "fig_part1")) if f.endswith(".png")}
MEME = {f[:-4]: uri(os.path.join(H, "memes", f), 1100, 78) for f in os.listdir(os.path.join(H, "memes"))} if os.path.isdir(os.path.join(H, "memes")) else {}
MASP = {f[:-4]: (lambda im: im.width / im.height)(Image.open(os.path.join(H, "memes", f))) for f in os.listdir(os.path.join(H, "memes"))} if os.path.isdir(os.path.join(H, "memes")) else {}
PHOTO, PCRED = {}, {}  # 장소 사진(deck/photos, fetch_photos.py). 없으면 남색 바탕
import json as _json
_pi = os.path.join(H, "photos", "index.json")
if os.path.exists(_pi):
    for k, v in _json.load(open(_pi, encoding="utf-8")).items():
        fp = os.path.join(H, "photos", v["file"])
        if os.path.exists(fp): PHOTO[k] = uri(fp, 1600, 78); PCRED[k] = f"{v['title'].replace('File:', '')} · {v['artist']} · {v['license']} · Wikimedia Commons"
PLAY, PINFO = {}, {}  # 80억 분의 1 플레이 화면(deck/play/, 원본은 git 제외). 있으면 2장에 넣는다
pd = os.path.join(H, "play")
if os.path.isdir(pd):
    for f in sorted(os.listdir(pd)):
        fp = os.path.join(pd, f)
        if f.lower().endswith(".webp"): PLAY[f] = "data:image/webp;base64," + base64.b64encode(open(fp, "rb").read()).decode()  # 움직이는 그림은 다시 저장하면 멈추므로 그대로
        elif f.lower().endswith((".jpg", ".jpeg", ".png")): PLAY[f] = uri(fp, 1200, 80)
    if os.path.exists(os.path.join(pd, "play_info.json")): PINFO = json.load(open(os.path.join(pd, "play_info.json"), encoding="utf-8"))

CSS = r"""
:root{--paper:#fff;--stage:#e9edf2;--ink:#15203a;--sub:#5a6577;--line:#e2e6ec;--navy:#072A60;--navyt:#e9eef6;--navy7:#1e3a5f;--green:#8DC63F;--greend:#4F7F1C;--greent:#f0f7e6;--orange:#D9640F;--gray:#9aa2ae}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--stage);font-family:__FAMILY__;color:var(--ink)}
#stage{position:fixed;inset:0;display:grid;place-items:center}
.slide{width:1280px;height:720px;background:var(--paper);position:absolute;display:none;overflow:hidden;transform-origin:center}.slide.on{display:block}
.hd{position:absolute;left:72px;top:48px;right:72px}.hd::before{content:"";display:block;width:32px;height:3px;background:var(--green);margin-bottom:12px}
.hd h2{margin:0;font-size:27px;font-weight:700;color:var(--navy);letter-spacing:-.01em;line-height:1.3}.hd .s{margin:5px 0 0;font-size:15px;color:var(--sub)}
.bd{position:absolute;left:72px;right:72px;top:138px;bottom:64px;display:flex;align-items:center;justify-content:center}.in{width:100%}
.cap{position:absolute;left:72px;right:150px;bottom:24px;font-size:12.5px;color:var(--sub);line-height:1.5}
.pg{position:absolute;right:40px;bottom:24px;font-size:13px;color:var(--gray);font-family:"IBM Plex Mono",monospace}
.notes{display:none}#notes{position:fixed;left:0;right:0;bottom:0;max-height:42vh;overflow:auto;background:rgba(21,32,58,.96);color:#fff;padding:18px 28px;font-size:17px;line-height:1.75;display:none;z-index:5}#notes.on{display:block}
p,li{font-size:18px;line-height:1.6;margin:0}ul,ol{margin:0;padding-left:22px}li+li{margin-top:7px}.k{font-size:14px;color:var(--sub);margin-bottom:6px}.num{font-family:"IBM Plex Mono",monospace}
.shot{display:block;max-width:100%;max-height:100%;border:1px solid var(--line);border-radius:4px;object-fit:contain}
.two{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center}
/* 표지·구분 */
.cover{background:var(--navy);color:#fff}.cover .c{position:absolute;left:88px;right:88px;top:200px}.cover .c::before{content:"";display:block;width:40px;height:4px;background:var(--green);margin-bottom:26px}
.cover h1{margin:0;font-size:46px;line-height:1.3;font-weight:700}.cover .sub{margin:18px 0 0;font-size:20px;opacity:.88;line-height:1.5}.cover .meta{position:absolute;left:88px;bottom:60px;font-size:15.5px;opacity:.85;line-height:1.7}
/* 정리 카드 */
.card{display:grid;grid-template-columns:1.1fr 1fr;gap:30px;align-items:start}.card .headimg{border:1px solid var(--line);border-radius:4px;overflow:hidden;background:#fafafa}.card .headimg img{width:100%;display:block}
.card dl{margin:0;display:grid;grid-template-columns:72px 1fr;gap:7px 12px;font-size:15.5px;line-height:1.55}.card dt{color:var(--sub);font-size:13.5px;padding-top:2px}.card dd{margin:0}
/* 논리 사다리 */
.ladder{display:grid;grid-template-columns:110px 1fr 1fr;gap:0 18px}.ladder>div{padding:9px 0;border-top:1px solid var(--line);font-size:15px;line-height:1.5}.ladder .l{color:var(--navy);font-weight:600}.ladder .q{color:var(--sub);font-size:13.5px;font-style:italic}.ladder .q i{font-style:normal;color:var(--gray)}
/* 측정: 왼쪽 원문, 오른쪽 구조 */
.meas{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center}.meas figure{margin:0;text-align:center}.meas figure img{display:inline-block;max-width:100%;max-height:400px}.meas figcaption{font-size:12.5px;color:var(--sub);margin-top:6px;text-align:left}
.mrows{display:grid;grid-template-columns:96px 1fr;gap:0 14px}.mrows>div{padding:8px 0;border-top:1px solid var(--line);font-size:15px;line-height:1.5}.mrows .l{color:var(--navy);font-weight:700}.mrows .l.f::after{content:"↓";display:block;color:var(--gray);font-weight:400;line-height:1.2}
.mcmp{margin-top:4px;padding:10px 14px;background:var(--navyt);font-size:14px;line-height:1.5}.mcmp b{display:block;color:var(--navy);font-size:13px;margin-bottom:2px}
/* 결과 */
.res{display:grid;grid-template-columns:1.15fr 1fr;gap:30px;align-items:center}.bars{display:grid;grid-template-columns:150px 1fr 70px;gap:8px 10px;align-items:center;font-size:14.5px}.bars .b{height:18px;background:var(--navy);border-radius:2px}.bars .b.g{background:var(--gray)}.bars .b.o{background:var(--orange)}.bars .v{font-family:"IBM Plex Mono",monospace;font-size:13px;text-align:right}.bars .lab{color:var(--ink)}
.take{margin-top:16px;font-size:17px;line-height:1.5}.take small{display:block;font-size:13.5px;color:var(--sub);margin-top:4px}
/* 한계 */
.lim{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}.lim ul{font-size:15px}.lim li{margin-top:6px;line-height:1.5}.lim .me{border-left:3px solid var(--green);padding-left:14px}.lim .me b{color:var(--greend);font-size:13.5px;display:block;margin-bottom:4px}
/* 쟁점 */
.issue{position:absolute;left:72px;right:72px;top:126px;bottom:58px}.issue .fig{position:relative;height:300px;border-radius:6px;overflow:hidden;background:#111}.issue .fig img{width:100%;height:100%;object-fit:cover;display:block}
.mc{position:absolute;color:#fff;font-weight:800;font-size:22px;line-height:1.25;text-shadow:0 0 6px #000,0 0 2px #000,2px 2px 0 #000,-1px -1px 0 #000;padding:4px 8px}
.card2{height:300px;border:1px solid var(--line);border-radius:6px;background:var(--navyt);padding:22px 26px;display:grid;grid-template-columns:1fr 1fr;gap:20px;align-content:center}.card2 .t{font-size:13px;color:var(--sub);margin-bottom:6px}.card2 .m{font-size:19px;font-weight:700;color:var(--navy);line-height:1.4}
.ch{display:grid;gap:10px}.ch .o{border-left:3px solid var(--navy);padding:6px 0 6px 18px;font-size:18px;line-height:1.55}.ch .o b{display:block;font-size:24px;color:var(--navy);line-height:1.35;margin-bottom:5px}.ch .vs{font-size:15px;color:var(--gray);font-weight:700;padding-left:21px}
.pr{grid-column:1/3;margin-top:6px;padding:11px 16px;background:var(--navyt);font-size:16px;line-height:1.5}
.issue.side{top:136px;display:grid;grid-template-columns:auto 1fr;gap:10px 36px;align-content:center;align-items:center}.issue.side .card2{width:460px;height:auto;min-height:300px;display:grid;grid-template-columns:1fr;gap:12px}
/* 한 줄과 다리 */
.bridge .one{font-size:30px;line-height:1.45;font-weight:600;color:var(--navy);padding:22px 28px;border-left:4px solid var(--green);background:var(--greent)}.bridge .next{margin-top:26px;font-size:17px;line-height:1.65;color:var(--ink)}
/* 논문 시작 표지 */
.pcover .nav{position:absolute;left:88px;right:88px;top:54px;display:flex;gap:26px;font-size:14.5px;color:rgba(255,255,255,.55)}.pcover .nav .on{color:#fff;font-weight:700;border-bottom:2px solid var(--green);padding-bottom:5px}
.pcover .c{bottom:84px}.pcover .no{font-size:15.5px;opacity:.85;margin-bottom:8px}.pcover h1{margin:0;font-size:48px;line-height:1.25;font-weight:700}.pcover .en{margin:12px 0 0;font-size:18px;line-height:1.5;opacity:.92;max-width:940px}.pcover .q{margin:28px 0 0;font-size:25px;line-height:1.45;font-weight:700;max-width:1000px}.pcover .d{margin:10px 0 0;font-size:16.5px;opacity:.9}
/* 보충 장 */
.add{display:grid;gap:30px;align-items:start}.add ul{padding-left:20px}.add li{font-size:15px;line-height:1.5;margin-top:6px}.add .k{font-size:13.5px;color:var(--navy);font-weight:700;margin-bottom:4px}
table.hyp{font-size:14px;table-layout:fixed}table.hyp td{line-height:1.45;padding:7px 9px}
.pg2{font-style:normal;color:var(--gray);font-size:.85em}
.pt2{margin-top:14px;padding:10px 14px;background:var(--greent);font-size:15px;line-height:1.5}.pt2 b{color:var(--greend);margin-right:10px}
/* 인트로·엔딩 */
.stat{display:grid;grid-template-columns:repeat(3,1fr);gap:36px;text-align:center}.stat .v{font-family:"IBM Plex Mono",monospace;font-size:84px;line-height:1;color:var(--navy);font-weight:500}.stat .l{font-size:16.5px;color:var(--sub);margin-top:14px;line-height:1.5}
.quote{border-left:4px solid var(--navy);padding:12px 18px;font-size:19px;line-height:1.6;color:var(--ink);background:#fafbfd}.quote small{display:block;color:var(--sub);font-size:13px;margin-top:8px}
table{border-collapse:collapse;width:100%;font-size:15.5px;line-height:1.4}th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:13px;color:var(--navy);font-weight:600;background:var(--navyt);border-bottom:1px solid var(--navy7)}td.r,th.r{text-align:right;white-space:nowrap}.photo{background:#0b1a33}.photo img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.photo .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,42,96,.35),rgba(7,42,96,.82))}.photo .c{position:absolute;left:88px;right:88px;bottom:96px;color:#fff}.photo .c::before{content:"";display:block;width:40px;height:4px;background:var(--green);margin-bottom:22px}.photo .one{font-size:36px;line-height:1.4;font-weight:700}.photo .one small{display:block;font-size:17px;font-weight:400;opacity:.85;margin-top:8px}.photo .next{margin-top:22px;font-size:16.5px;line-height:1.65;opacity:.95;max-width:1000px}.photo .cr{position:absolute;right:76px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:720px;text-align:right}.photo .pg{color:rgba(255,255,255,.6)}
.map{position:relative;height:430px;border-left:1px solid var(--line);border-bottom:1px solid var(--line)}.map .pt{position:absolute;width:14px;height:14px;border-radius:50%;background:var(--navy);transform:translate(-50%,-50%)}.map .lb{position:absolute;font-size:14px;line-height:1.35;transform:translate(10px,-50%)}.map .lb b{color:var(--navy);display:block;font-size:14.5px}.map .ax{position:absolute;font-size:12.5px;color:var(--sub)}
.steps{counter-reset:s}.steps li{list-style:none;position:relative;padding-left:30px;font-size:17px;margin-top:9px}.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:4px;width:20px;height:20px;border-radius:50%;background:var(--navy);color:#fff;font-size:11px;display:grid;place-items:center}
.intro2{display:grid;gap:30px;align-items:center}.intro2 li{font-size:15px;line-height:1.55}.play{display:flex;gap:12px}.play figure{margin:0;animation:rise .7s both}.play figure:nth-child(2){animation-delay:.35s}.play figure:nth-child(3){animation-delay:.7s}.play .ph{position:relative;width:204px;height:408px;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#f4f5f7}.play .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.play figcaption{position:relative;height:20px;margin-top:6px;font-size:12.5px;color:var(--sub);text-align:center}.play figcaption span{position:absolute;left:0;right:0}@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
#help{position:fixed;right:14px;top:10px;font-size:12px;color:#7b8494;z-index:6}:root:fullscreen #help{display:none}td.ck{cursor:pointer;text-align:center}
"""

S = []  # (html, notes, appendix?)


def slide(title, sub, body, cap="", notes="", ap=False, cls=""):
    S.append((f'<section class="slide {cls}" {"data-ap=1" if ap else ""}><div class="hd"><h2>{title}</h2>{f"<p class=s>{sub}</p>" if sub else ""}</div><div class="bd"><div class="in">{body}</div></div>{f"<div class=cap>{cap}</div>" if cap else ""}<aside class="notes">{notes}</aside></section>', None))


def photo(key, one, small, bridge, notes, title=""):
    img = f'<img class="bg" src="{PHOTO[key]}" alt="">' if key in PHOTO else ""
    cr = f'<div class="cr">{PCRED[key]}</div>' if key in PCRED else ""
    S.append((f'<section class="slide photo">{img}<div class="veil"></div><div class="c">{f"<div style=font-size:14px;opacity:.8;margin-bottom:10px>{title}</div>" if title else ""}<div class="one">{one}<small>{small}</small></div><p class="next">{bridge}</p></div>{cr}<aside class="notes">{notes}</aside></section>', None))


MKEY = {"krishna_items": "01_krishna", "freitag_meas": "02_freitag", "mettler_dv": "04_mettler", "kr_fig1": "05_kr"}  # 측정 장 캡처 → 보충 내용 키
MCHAIN = {"krishna_items": 4, "freitag_meas": 3, "lw_latent": 3, "kr_fig1": 3}  # 캡처별: 앞에서 몇 행이 순서(개념→문항→지수, 독립→매개→종속)인가


def meas(title, sub, fig, figcap, rows, cmp_, notes):
    """측정 장: 왼쪽에 원문 캡처, 오른쪽에 개념에서 지수까지의 단계와 앞 주차 문헌 비교."""
    if MKEY.get(fig) in ADD: rows = rows + [("자료와 변수", esc(ADD[MKEY[fig]]["data_row"]["t"]))]
    r = "".join(f'<div class="l{" f" if i < MCHAIN.get(fig, 0) - 1 else ""}">{l}</div><div>{t}</div>' for i, (l, t) in enumerate(rows))
    slide(title, sub, f'<div class="meas"><figure><img class="shot" src="{FIG[fig]}" alt="{figcap}"><figcaption>{figcap}</figcaption></figure><div><div class="mrows">{r}</div><div class="mcmp"><b>앞 주차 문헌</b>{cmp_}</div></div></div>', "", notes)


PNAMES = ["Krishna 2007", "Freitag 2006", "Lowndes &amp; Wilson 2001", "Mettler 2002", "Kumlin &amp; Rothstein 2005"]


def pcover(n, key, name, en, journal, q, data, notes):
    """논문 시작 표지: 위에 다섯 편 중 현재 위치, 아래에 서지·연구 질문·자료."""
    img = f'<img class="bg" src="{PHOTO[key]}" alt="">' if key in PHOTO else ""
    cr = f'<div class="cr">{PCRED[key]}</div>' if key in PCRED else ""
    nav = "".join(f'<span class="{"on" if i == n - 1 else ""}">{x}</span>' for i, x in enumerate(PNAMES))
    S.append((f'<section class="slide photo pcover">{img}<div class="veil"></div><div class="nav">{nav}</div><div class="c"><div class="no">지정문헌 {n} / 5</div><h1>{name}</h1><p class="en">{en}<br><i>{journal}</i></p><p class="q">{q}</p><p class="d">{data}</p></div>{cr}<aside class="notes">{notes}</aside></section>', None))


ADD = {}  # 논문별 보충 장 내용(deck/part1_add/*.json). 각 항목의 ev는 원문 근거 구절, p는 인쇄 쪽수
_ad = os.path.join(H, "part1_add")
for _f in (sorted(os.listdir(_ad)) if os.path.isdir(_ad) else []):
    if _f.endswith(".json"): ADD[_f[:-5]] = json.load(open(os.path.join(_ad, _f), encoding="utf-8"))
ALAB = {"03_lw": {"theory": "이론적 논의와 명제", "hyp": "명제", "nores": True, "r2": "제도 설계 변수 2 · 차원별 사례", "pol": "설계 원칙", "fut": "저자의 단서"}}


def _pg(x): return f' <i class="pg2">{x["p"]}</i>' if x.get("p") else ""
def _li(xs): return "".join(f'<li>{esc(x["t"])}{_pg(x)}</li>' for x in xs)
def _pt(t): return f'<div class="pt2"><b>짚을 점</b>{esc(t)}</div>'


def add_theory(key, paper):
    """보충 장 1: 왼쪽 선행 논의, 오른쪽 가설(명제) 표."""
    a = ADD[key]["theory"]; L = ALAB.get(key, {}); res = not L.get("nores")
    hy = "".join(f'<tr><td><b>{esc(x["name"])}</b></td><td>{esc(x["claim"])}{"" if res else _pg(x)}</td><td>{esc(x["source"])}</td>{f"<td>{esc(x['result'])}{_pg(x)}</td>" if res else ""}</tr>' for x in a["hypotheses"])
    cols = '<col style="width:17%"><col style="width:39%"><col style="width:24%"><col style="width:20%">' if res else '<col style="width:22%"><col style="width:50%"><col style="width:28%">'
    slide(f'{paper} {L.get("theory", "이론적 논의와 가설")}', esc(a["sub"]),
          f'<div class="add" style="grid-template-columns:.78fr 1.7fr"><div><div class="k">선행 논의</div><ul>{_li(a["background"])}</ul></div><table class="hyp"><colgroup>{cols}</colgroup><tr><th>{L.get("hyp", "가설")}</th><th>내용</th><th>근거 문헌</th>{f"<th>{L.get('res', '검증 결과')}</th>" if res else ""}</tr>{hy}</table></div>{_pt(a["point"])}', "", esc(a["notes"]))


def add_result2(key, paper):
    """보충 장 2: 왼쪽 원문 캡처, 오른쪽 수치와 해석."""
    a = ADD[key]["result2"]; L = ALAB.get(key, {})
    rows = "".join(f'<tr><td>{esc(x["label"])}</td><td>{esc(x["value"])}{_pg(x)}</td></tr>' for x in a["rows"])
    slide(f'{paper} {L.get("r2", "분석 결과 2")}', esc(a["sub"]),
          f'<div class="add" style="grid-template-columns:1fr 1.15fr"><img class="shot" style="max-height:420px;margin:0 auto" src="{FIG[key[3:] + "_r2"]}" alt=""><div><table class="hyp"><colgroup><col style="width:34%"><col style="width:66%"></colgroup>{rows}</table><ul style="margin-top:10px">{_li(a["reading"])}</ul></div></div>{_pt(a["point"])}', "", esc(a["notes"]))


def add_conclusion(key, paper):
    """보충 장 3: 왼쪽 저자의 결론과 기여, 오른쪽 함의와 후속 과제."""
    a = ADD[key]["conclusion"]; L = ALAB.get(key, {})
    right = (f'<div class="k">{L.get("pol", "저자가 말한 정책적 함의")}</div><ul>{_li(a["policy"])}</ul>' if a["policy"] else "") + (f'<div class="k" style="margin-top:14px">{L.get("fut", "후속 과제")}</div><ul>{_li(a["future"])}</ul>' if a["future"] else "")
    con = "".join(f"<li>{esc(c)}</li>" for c in a["contribution"])
    slide(f'{paper} 결론과 함의', esc(a["sub"]),
          f'<div class="add" style="grid-template-columns:1fr 1fr"><div><div class="k">저자의 결론</div><ul>{_li(a["author"])}</ul><div class="k" style="margin-top:14px">기여(발제자 평가)</div><ul>{con}</ul></div><div>{right}</div></div>{_pt(a["point"])}', "", esc(a["notes"]))


def raw(html):
    S.append((html, None))


def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# 캡션 좌표: 템플릿별 (위치 %, 폭 %)
MPOS = {"catyell": [("top:5%;left:2%;width:46%;text-align:center",), ("top:5%;left:52%;width:46%;text-align:center",)],
        "pigeon": [("top:7%;left:56%;width:40%",), ("top:34%;left:3%;width:42%",), ("bottom:5%;left:8%;width:84%;text-align:center",)],
        "buttons": [("top:8%;left:12%;width:30%",), ("top:4%;left:46%;width:32%",), ("bottom:6%;left:18%;width:64%;text-align:center",)],
        "drake": [("top:10%;left:52%;width:46%",), ("top:60%;left:52%;width:46%",)],
        "boyfriend": [("top:48%;left:20%;width:26%",), ("top:34%;left:50%;width:22%",), ("top:38%;left:75%;width:23%",)],
        "brain": [("top:3%;left:2%;width:46%",), ("top:28%;left:2%;width:46%",), ("top:53%;left:2%;width:46%",), ("top:78%;left:2%;width:46%",)],
        "fine": [("bottom:5%;left:5%;width:90%;text-align:center",)],
        "gru": [("top:6%;left:3%;width:42%",), ("top:6%;left:53%;width:42%",), ("top:56%;left:3%;width:42%",), ("top:56%;left:53%;width:42%",)],
        "handshake": [("bottom:8%;left:2%;width:32%",), ("bottom:8%;right:2%;width:32%;text-align:right",), ("top:12%;left:30%;width:40%;text-align:center",)],
        "whynotboth": [("top:5%;left:6%;width:88%;text-align:center",), ("bottom:6%;left:6%;width:88%;text-align:center",)],
        "exit": [("top:5%;left:8%;width:34%",), ("top:5%;left:52%;width:34%",), ("bottom:8%;left:20%;width:60%;text-align:center",)]}
MNAME = {"catyell": "고양이에게 소리치는 여자", "pigeon": "이게 비둘기인가요?", "buttons": "두 버튼", "drake": "드레이크", "boyfriend": "딴 데 보는 남자친구", "brain": "확장하는 뇌", "fine": "불타는 방의 개", "gru": "그루의 계획", "handshake": "두 팔 악수", "whynotboth": "둘 다 하면 안 돼요?", "exit": "고속도로 출구"}


# 공개판은 그림 파일을 저장소에 넣지 않고 imgflip 주소에서 불러온다. 안 열리면(오프라인) 캡션 카드가 대신 보인다
MCROP = {"fine": 1.03}  # 가로로 긴 두 칸 템플릿은 오른쪽 한 칸만 쓴다
MURL = {"catyell": "Woman-Yelling-At-Cat", "pigeon": "Is-This-A-Pigeon", "brain": "Expanding-Brain", "buttons": "Two-Buttons", "drake": "Drake-Hotline-Bling", "fine": "This-Is-Fine", "gru": "Grus-Plan",
        "handshake": "Epic-Handshake", "boyfriend": "Distracted-Boyfriend", "whynotboth": "Why-Not-Both", "exit": "Left-Exit-12-Off-Ramp"}


def memefig(meme, caps, local):
    """밈 그림(캡션은 그림 위에). 공개판은 그림을 imgflip에서 불러오고 안 열리면 캡션 카드가 대신 보인다. 그림 파일이 없으면 캡션 카드만."""
    card = f'<div class="card2"><div class="t">{MNAME[meme]} 형식 · 캡션</div>' + "".join(f'<div class="m">{esc(c)}</div>' for c in caps) + '</div>'
    if meme not in MASP: return card, False
    asp = MCROP.get(meme, MASP[meme]); H = int(min(400, 500 / asp)); w = int(H * asp)
    fit = "object-fit:cover;object-position:right" if meme in MCROP else "object-fit:fill"
    img = f'<img src="{MEME[meme]}" alt="" style="{fit}">' if local else f'<img src="https://imgflip.com/s/meme/{MURL[meme]}.jpg" alt="" style="{fit}" referrerpolicy="no-referrer" onerror="noimg(this)">'
    fs = 16 if w >= 420 else 14
    dark = meme in ("drake", "gru", "whynotboth", "catyell", "buttons")  # 밝은 바탕 템플릿은 남색 글자
    over = "".join(f'<div class="mc" style="{MPOS[meme][i][0]};font-size:{fs}px;{"color:#15203a;text-shadow:0 0 4px #fff,0 0 2px #fff,1px 1px 0 #fff" if dark else ""}">{esc(c)}</div>' for i, c in enumerate(caps))
    fig = f'<div class="fig" style="width:{w}px;height:{H}px;margin:0 auto">{img}{over}</div>'
    if not local: fig = f'<div class="mw">{fig}</div>' + card.replace('<div class="card2">', '<div class="card2" style="display:none">', 1)
    return fig, True


def _issue(title, sub, meme, caps, a, b, extra, local, how, notes):
    fig, has = memefig(meme, caps, local)
    body = f'<div class="issue side">{fig}<div class="ch"><div class="o"><b>{a[0]}</b>{a[1]}</div><div class="vs">vs</div><div class="o"><b>{b[0]}</b>{b[1]}</div></div>{extra}</div>'
    credit = ("밈 템플릿: imgflip 공개 템플릿, 수업 내부용 · " if local else "밈 템플릿: imgflip · ") if has else ""
    S.append((f'<section class="slide"><div class="hd"><h2>{title}</h2><p class="s">{sub}</p></div>{body}<div class="cap">{credit}{how}</div><aside class="notes">{notes}</aside></section>', None))


def choice(title, sub, meme, caps, c1, c2, result, local, notes):
    """논문별 첫 토론: 정책 선택 두 가지와 논문의 결과 한 줄."""
    _issue(title, sub, meme, caps, c1, c2, f'<div class="pr">{result}</div>', local, "토론 5분 · 손들기 뒤 지명 1명 + 자유 2~3명", notes)


def issue(title, sub, meme, caps, pro, con, q, local, notes):
    """논문별 두 번째 토론: 한 문장 찬·반, 손들기."""
    _issue(title, sub, meme, caps, pro, con, "", local, "손들기 1분", notes)


def build(local):
    S.clear()
    # ───────── 인트로 ─────────
    raw(f'''<section class="slide cover">{f'<img src="{PHOTO["landsgemeinde"]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55">' if "landsgemeinde" in PHOTO else ""}<div style="position:absolute;inset:0;background:rgba(7,42,96,.55)"></div><div class="c" style="position:absolute"><h1>국가는 사회자본을 만들 수 있는가</h1><p class="sub">Social Capital as Dependent Variable · 11주차 발제<br>Krishna 2007 · Freitag 2006 · Lowndes &amp; Wilson 2001 · Mettler 2002 · Kumlin &amp; Rothstein 2005</p></div><div class="meta">사회자본과 공공정책 · 2026-11-13 · 발제 오지환(석사과정 2학기) · 성균관대학교</div>{f'<div style="position:absolute;right:40px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:600px;text-align:right">{PCRED["landsgemeinde"]}</div>' if "landsgemeinde" in PCRED else ""}
<aside class="notes">안녕하십니까. 11주차 「국가는 사회자본을 만들 수 있는가」 세미나를 맡은 석사과정 2학기 오지환입니다. 오늘 주제는 Social Capital as Dependent Variable, 사회자본을 결과로 놓는 연구들입니다.</aside></section>''')
    # 플레이 화면 세 칸: 태어남 / 관계 사건의 선택(여러 장이 차례로 바뀜) / 죽음(움직이는 그림). 두 판 모두에 넣는다
    mids = [k for k in sorted(PLAY) if k.startswith("mid_")] or [k for k in ("02_choice.png", "02_choice_alt_decision20.png", "02_choice_alt_volunteer22.png") if k in PLAY]
    death = next((k for k in ("03_death.webp", "03_summary.png") if k in PLAY), None)
    shots = bool("01_birth.png" in PLAY and mids and death)
    play_html = ""
    if shots:
        n, d = len(mids), 3  # 가운데 칸은 장면마다 3초
        info = {m["file"]: m for m in PINFO.get("mid", [])}
        cyc = f"@keyframes cyc{{0%{{opacity:0}}{8 / n:.2f}%{{opacity:1}}{100 / n:.2f}%{{opacity:1}}{108 / n:.2f}%{{opacity:0}}100%{{opacity:0}}}}"
        ani = lambda i: f"animation:cyc {n * d}s {i * d}s infinite both"
        stack = "".join(f'<img src="{PLAY[k]}" alt="" style="{ani(i)}">' for i, k in enumerate(mids))
        caps = "".join(f'<span style="{ani(i)}">{info[k]["age"]}세 · {esc(info[k]["title"])}</span>' for i, k in enumerate(mids) if k in info) or "살면서 만나는 선택"
        play_html = f'<style>{cyc}</style><div class="play"><figure><div class="ph"><img src="{PLAY["01_birth.png"]}" alt=""></div><figcaption>태어남</figcaption></figure><figure><div class="ph">{stack}</div><figcaption>{caps}</figcaption></figure><figure><div class="ph"><img src="{PLAY[death]}" alt=""></div><figcaption>죽음</figcaption></figure></div>'
    slide("80억 분의 1", "172개국 실제 통계로 한 사람의 삶을 사는 시뮬레이션 (1in8b.life)",
          f'''<div class="intro2" style="grid-template-columns:{"auto 1fr" if shots else "1fr"}">{play_html}<div><ul><li>고를 수 있는 것은 태어날 해뿐. 나라는 그해 출생아 수의 확률로, 가정은 그 나라 소득분포의 확률로 정해진다</li><li>반영 통계: 출생아 수, 성별 기대수명, 영아 사망률, 소득 불평등 지수, 교육 접근성, 대학 진학률, 살인율, 흡연율, 조혼율. 전쟁·팬데믹 같은 사건도 반영</li><li>살면서 중매, 동네 봉사 모임, 부모 돌봄, 낯선 사람 돕기 같은 사건마다 선택하고, 그 결과가 건강·행복·지식·관계 수치로 표시된다</li></ul>
<div class="quote" style="font-size:14.5px;margin-top:14px">"우리 누구도 (태어날 곳을) 고르지 않았다. 원하는 나라가 나올 때까지 다시 했다는 반응은 오히려 이 시뮬레이션이 보여주려던 것과 닿아 있다. 태어난 곳이 삶을 얼마나 크게 바꾸는지 알기 때문에 다시 누르는 거니까. 현실에서는 그 버튼이 없다."<small>개발자 진휘어스 인터뷰, 한겨레21 1637호(2026-10-29) 재인용</small></div></div></div>''',
          ("화면: 1in8b.life 플레이 화면(2026-11-11~12 캡처, 태어날 해 1990년 선택). " if shots else "") + "한겨레21 1637호 「다시 태어나면 어디서 누구로 살고 싶은가… '80억 분의 1' 게임으로 오라」(2026-10-29). 한국인 개발자, 2026-10-07 출시, 무료.",
          "본격적으로 들어가기 전에 하나 여쭙겠습니다. '80억 분의 1'이라는 게임을 해 보셨거나 들어 보신 분 계십니까. 172개국 통계로 한 사람의 일생을 무작위로 사는 시뮬레이션입니다. 고를 수 있는 건 태어날 해뿐입니다. 저는 남양주에서 등교하는 길에 논문도 뉴스도 보기 싫을 때 이걸 합니다. 제 연구가 재미없어질 때도 합니다. 화면은 태어날 해로 1990년을 골라 무작위로 받은 삶입니다. 왼쪽이 태어난 순간입니다. 인도 마디아프라데시 농촌의 하위 20~40% 가정에서 태어난 여자아이입니다. 가운데에는 이 사람이 살면서 만난 선택이 차례로 지나갑니다. 스무 살의 중매 제안, 스물두 살의 동네 봉사 모임, 어머니께 고맙다는 말, 길에 쓰러진 낯선 사람, 아들의 결혼, 아버지 돌봄입니다. 이 게임에는 건강, 행복, 지식, 관계 네 수치가 있고, 이런 선택에 따라 관계 수치가 오르내립니다. 저는 사회자본을 공부하면서 이 관계 수치가 무엇 때문에 오르내리는지가 궁금해졌습니다. 오른쪽은 이 사람이 70세에 세상을 떠났을 때 나오는 장면입니다. 이 게임을 만든 사람은 한국인 개발자입니다. 출시 뒤 태어날 나라를 고르게 해 달라는 문의가 쏟아졌다고 합니다. 개발자의 답이 화면의 인용입니다.")
    slide("지정문헌이 다루는 선택", "모임 가입, 이사, 공청회 참석, 급여 신청, 복지 창구 방문",
          '''<div class="two" style="grid-template-columns:1fr 1.2fr"><div class="quote" style="font-size:17px">"'80억 분의 1'의 선택은 통계에 기반을 둬 설계됐다는 점에서, 그리고 선택의 결과가 수치로 명확하게 표현된다는 점에서 실제 우리 인생과 다르다. (…) 우리는 특정한 결과를 짐작하며 무언가를 선택하지만, 현실에서 짐작은 종종 빗나간다. 선택을 통해 얻은 것이 정확히 무엇인지도 바로 알기 어렵다."<small>한겨레21 1637호 기사 본문</small></div>
<div><div class="k">논문별 선택과 종속변수</div><table style="font-size:15.5px"><tr><th>선택</th><th>논문</th><th>종속변수</th></tr>
<tr><td>친구가 만든 모임에 가입했다</td><td>Krishna</td><td>마을의 협력 기대</td></tr><tr><td>주민투표를 하기 쉬운 지역으로 이사했다</td><td>Freitag</td><td>결사체 참여</td></tr><tr><td>구청 공청회에 갔지만 답장은 없었다</td><td>Lowndes &amp; Wilson</td><td>(측정 없음)</td></tr><tr><td>신청서 한 장으로 등록금을 받았다</td><td>Mettler</td><td>단체 가입 · 정치참여</td></tr><tr><td>복지 창구에서 서류 넷을 내고 한 달을 기다렸다</td><td>Kumlin &amp; Rothstein</td><td>대인신뢰 0~10</td></tr></table></div></div>''',
          "",
          "한겨레21 기사는 이 게임과 현실의 차이를 이렇게 정리했습니다. 게임에서는 선택의 결과가 숫자로 바로 나오지만, 현실에서는 내 선택이 무엇을 바꿨는지 바로 알기 어렵습니다. 오늘 읽을 다섯 편은 그 결과를 숫자로 재려고 한 연구입니다. 오른쪽 표에 논문마다 다룬 선택과 종속변수를 적었습니다.")
    slide("연구 대상과 분석 단위", "발제 순서: 원인을 사회 내부에서 찾은 연구부터 국가와 개인의 접촉을 다룬 연구까지",
          '''<div class="two" style="grid-template-columns:1.3fr 1fr"><div class="map">
<div class="pt" style="left:12%;top:82%"></div><div class="lb" style="left:12%;top:82%"><b>Krishna 2007</b>마을 내부의 자생 조직 · 규칙 · 신진 리더<br>인도 61개 마을, 7년 패널</div>
<div class="pt" style="left:30%;top:64%"></div><div class="lb" style="left:30%;top:64%"><b>Freitag 2006</b>칸톤의 정치제도<br>스위스 24개 칸톤</div>
<div class="pt" style="left:48%;top:46%"></div><div class="lb" style="left:48%;top:46%"><b>Lowndes &amp; Wilson 2001</b>지방정부 제도 설계의 네 차원<br>영국, 실증 없음</div>
<div class="pt" style="left:62%;top:28%"></div><div class="lb" style="left:62%;top:28%"><b>Mettler 2002</b>정책 하나의 집행 방식<br>미국 참전자 716명, 회고 설문</div>
<div class="pt" style="left:72%;top:10%"></div><div class="lb" style="left:72%;top:10%"><b>Kumlin &amp; Rothstein 2005</b>복지 창구 접촉의 공정성<br>스웨덴 서부 2,543명</div>
<div class="ax" style="left:0;bottom:-22px">← 사회 내부</div><div class="ax" style="right:0;bottom:-22px">국가와 개인의 접촉 →</div><div class="ax" style="left:-4px;top:-20px">개인</div><div class="ax" style="left:-4px;bottom:0">집합</div></div>
<div><div class="k">2~10주차와의 관계</div><ul style="font-size:15px"><li>6~10주차: 사회자본 → 민주주의(Paxton), 정부 성과(Knack 2002, Tavits), 성장(Knack &amp; Keefer)</li><li>4주차 문헌은 형성 요인으로 문화(Guiso), 개인 투자(Glaeser), 인구 구성(Rupasingha)을 제시</li><li>지정문헌 5편은 국가가 사회자본을 형성할 수 있는지를 묻는다. Freitag 125쪽의 구분으로는 사회자본을 외생으로 두는 접근(Putnam 1993)과 달리 내생으로 두는 접근(Levi 1996 · Tarrow 1996 · Skocpol 외 2000)에 해당</li></ul><div class="quote" style="font-size:14.5px;margin-top:14px">"The second approach endogenizes social capital as an outcome of social and political arrangements"<small>Freitag 2006: 125</small></div></div></div>''',
          "점의 위치는 발제자 배치. 세로축은 종속변수의 단위(마을·칸톤 평균 → 개인), 가로축은 원인 변수(사회 내부 → 국가).",
          "앞선 주차에서 사회자본은 주로 독립변수였습니다. 6주차부터 10주차까지 민주주의, 정부 성과, 경제 성장을 설명했습니다. 오늘 다섯 편에서는 사회자본이 종속변수이고, 국가와 제도가 그 원인인지를 묻습니다. 그림의 점은 왼쪽 아래에서 오른쪽 위로 갑니다. 원인 변수가 마을 내부에서 복지 창구로 바뀌고, 분석 단위는 마을 평균에서 개인으로 내려옵니다.")

    # ───────── 1 Krishna ─────────
    pcover(1, "rajasthan_village", "Krishna (2007)", "How Does Social Capital Grow? A Seven-Year Study of Villages in India", "Journal of Politics 69(4): 941–956",
           "같은 제도 아래 있는 마을들의 사회자본은 7년 동안 왜 다르게 변했는가", "인도 라자스탄 61개 마을 · 1997년과 2004년 패널 · 분석 단위 마을",
           "첫 논문은 Krishna의 2007년 연구입니다. 인도 라자스탄 61개 마을을 1997년과 2004년 두 번 조사했습니다. 이 마을들은 모두 같은 주의 같은 제도 아래 있습니다. 그런데도 사회자본이 7년 동안 마을마다 다르게 변했고, 저자는 그 원인을 찾습니다.")
    slide("Krishna (2007) 연구 개요", "How Does Social Capital Grow? A Seven-Year Study of Villages in India · <i>Journal of Politics</i> 69(4)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["krishna_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>사회자본은 7년 사이에 변화하는가. 변화한다면 그 요인은 무엇인가</dd>
<dt>자료</dt><dd>라자스탄 5개 구 61개 마을. 1997년 2,291명 → 2004년 1,731명 재면접(76%). 9개 마을 사례연구</dd>
<dt>설계</dt><dd>마을 단위 OLS. 종속변수는 2004년 집합행동 성향 6문항 지수(0~100). 독립변수 16개 중 11개는 1997년 측정값. 조직 가입 3종(정부·NGO·자생)은 7년간 신규 가입, 마을 갈등과 강우 실패는 7년간 빈도</dd>
<dt>결과</dt><dd>평균 58.4 → 59.7. 33개 마을 상승·28개 하락. 유의한 변수는 자생 조직 17.57*, 규칙 3.77*(p&lt;.001), 신진 리더 5.59*(p&lt;.01), 토지 불평등 −.13*. 정부 신뢰, 정부 조직, NGO 조직은 유의하지 않음</dd>
<dt>한계</dt><dd>모든 마을이 같은 주의 제도 아래 있어 제도 설계의 효과는 검증 불가(950). 교육처럼 장기에 걸친 효과는 7년 자료로 확인 불가(각주 19)</dd></dl></div>''',
          "계수는 Table 2(949), 평균과 마을 수는 946.",
          "Krishna는 Putnam이 역사가 결정한다고 본 사회자본이 7년 사이에 변화하는지를 묻습니다. 라자스탄 61개 마을을 1997년과 2004년에 두 번 측정했습니다. 평균은 거의 같았지만 마을별로는 33개가 오르고 28개가 내렸습니다. 유의한 변수는 주민이 만든 자생 조직, 규칙, 신진 리더, 토지 불평등 넷입니다. 정부가 만든 조직과 정부에 대한 신뢰는 유의하지 않았습니다.")
    slide("Krishna (2007) 연구 질문과 논리 전개", "",
          '''<div class="ladder">
<div class="l">질문</div><div>Putnam(1993)은 사회자본이 정부 성과에 결정적으로 중요하지만 의도적으로 늘릴 수는 없다고 보았다. 사회자본은 단기간에 변화할 수 있는가</div><div class="q">"Putnam (1993) presents us with a nagging conundrum" <i>941</i></div>
<div class="l">이론적 기대</div><div>가설을 5개 집단으로 나누어 비관적 관점에서 낙관적 관점 순으로 제시. 역사 의존(Putnam) · 제도 부산물(Rothstein 2001, Kumlin &amp; Rothstein 2005) · 집단 특성(Boix &amp; Posner 분열, Olson 규모) · 집단 행동(Ostrom 규칙, Oliver 리더) · 외부 개입(World Bank)</div><div class="q">"Different pathways, corresponding to different degrees of optimism" <i>943</i></div>
<div class="l">설계 선택</div><div>패널 설계: 횡단면 자료로는 인과 방향을 구분하기 어려움. 분석 단위는 마을: 집단 수준의 사회자본 개념만 다룬다고 명시(각주 2). 조직 가입 대신 6문항 지수: 공식 조직 가입률이 2% 미만이고 대부분 정부가 설립</div><div class="q">"Density of formal organizations is a particularly inappropriate indicator" <i>945</i></div>
<div class="l">결과</div><div>1997년 지수만 넣은 모형의 R²는 .23, 16개 변수를 넣은 모형은 .79. 1997년 지수 외에 유의한 변수는 4개. 가장 비관적인 두 가설(역사 의존, 제도 부산물)과 가장 낙관적인 가설(외부 개입)은 지지되지 않음(역사 의존은 부분적으로만 확인, 949)</div><div class="q">"only four variables are found significantly associated with higher gains" <i>952</i></div>
<div class="l">결론</div><div>사회자본은 공동체 내부에서 형성됨. 외부 기관은 불평등 완화, 자기조직화 여건 조성, 리더 육성을 통해 간접적·장기적으로만 기여</div><div class="q">"External agencies cannot directly raise social capital." <i>954</i></div></div>''',
          "", "다섯 단으로 읽겠습니다. 질문은 Putnam의 모순에서 나옵니다. 가설은 다섯 집단이고, 저자는 비관적인 가설부터 낙관적인 가설 순으로 배열했습니다. 어느 가설이 지지되는지에 따라 결론이 정해집니다. 설계에서는 조직 가입률을 지표로 쓰지 않은 점을 보시면 됩니다. 공식 조직 가입률이 2% 미만이어서 저자는 Putnam의 지표가 이 지역에 맞지 않는다고 판단했습니다. 결과에서는 집단 행동 가설과 집단 특성 가설의 일부만 지지되었습니다. 가장 비관적인 쪽도, 가장 낙관적인 쪽도 지지되지 않았습니다.")
    add_theory("01_krishna", "Krishna (2007)")
    meas("Krishna (2007) 사회자본 측정", "945~946쪽", "krishna_items", "Krishna 2007: 945. 문항 1~3(구조적 차원). 문항 4~6은 945~946쪽",
         [("개념적 정의", "Putnam(1995)의 정의를 따름. “networks, norms and social trust that facilitate coordination and cooperation”(942)"),
          ("구성 차원", "Uphoff의 구분을 적용. 구조적 차원은 연결망·역할·규칙·선례, 인지적 차원은 규범·가치·태도·믿음(945)"),
          ("측정 문항", "구조적 차원 3문항(병충해 공동 대응, 공유지 관리, 분쟁 해결)과 인지적 차원 3문항(호혜, 연대, 신뢰). 여섯 문항 모두 응답자 본인보다 마을 사람들의 행동, 규범, 선호를 물음"),
          ("지수 구성", "주성분 분석에서 단일 요인(분산의 55%), α .86. 여섯 문항을 같은 가중치로 합산해 0~100점으로 변환(각주 12·13)")],
         "Ostrom(1998, 2주차)은 신뢰를 타인의 행동에 대한 기대로 정의했고, 신뢰 문항(6번)이 같은 방식으로 물음. Dasgupta(2000, 9주차)는 믿음·규칙·연결망을 하나의 지수로 합산하는 데 반대(p.327)",
         "왼쪽이 945쪽 설문 문항 원문입니다. 저자는 Putnam의 정의를 따르고, Uphoff의 구분에 맞춰 구조적 차원과 인지적 차원을 세 문항씩 만들었습니다. 여섯 문항 모두 응답자 본인보다 마을 사람들의 행동과 규범, 선호를 묻습니다. 1번과 3번은 누가 나설지를, 6번은 친구가 어느 쪽을 고를지를 묻습니다. 2주차 Ostrom이 신뢰를 타인의 행동에 대한 기대로 정의한 것과 같은 방식입니다. 다만 9주차 Dasgupta는 믿음과 규칙과 연결망을 한 지수로 합치는 데 반대했습니다. 이어서 토론 1로 넘어가겠습니다.")
    choice("주민 모임을 늘리려면 정부는 어느 쪽에 예산을 써야 한다고 생각하십니까?", "Krishna · 토론 1", "pigeon",
          ["정부가 세운 청년회", "Putnam", "이것은 사회자본인가요?"],
          ("선택 1. 정부가 조직을 만들어 지원한다", "주민자치회처럼 틀을 먼저 만들고 사업비를 지원한다. 모임이 없는 지역에서도 바로 시작할 수 있다"),
          ("선택 2. 주민이 만든 모임을 뒤에서 돕는다", "이미 있는 모임과 리더에게 공간과 운영비를 지원한다. 모임이 없는 지역은 지원에서 빠질 수 있다"),
          "Krishna의 결과: 주민이 스스로 만든 조직만 7년 뒤 마을의 사회자본과 관련이 있었고, 정부와 NGO가 세운 조직은 유의하지 않았다(Table 2)", local,
          "토론 1입니다. 주민 모임을 늘리려면 정부가 어느 쪽에 예산을 써야 하는지 여쭙겠습니다. 선택 1은 정부가 틀을 만들어 지원하는 방식이고, 선택 2는 주민이 만든 모임을 뒤에서 돕는 방식입니다. 손을 들어 주시고, 한 분씩 이유를 듣겠습니다. Krishna의 결과는 선택 2에 가깝습니다. 다만 라자스탄에서는 공식 조직 가입률이 2% 미만이어서 정부 조직의 효과를 가려내기 어려웠을 수 있다는 제 해석도 함께 말씀드립니다. 3주차 Fukuyama도 사회자본은 정책으로 만들기 어렵다고 했습니다.")
    slide("Krishna (2007) 분석 결과", "Table 2 · 2004년 마을 지수에 대한 OLS, Model 2 N=60(Model 1은 61)",
          f'''<div class="res"><img class="shot" style="max-height:420px" src="{FIG["krishna_t2"]}" alt="Table 2"><div><div class="k">실질 효과 = 계수 × 변수 범위 (범위는 952쪽과 각주 20, 발제자 계산)</div><div class="bars">
<span class="lab">규칙(1997)</span><div class="b" style="width:100%"></div><span class="v">+12.5</span>
<span class="lab">신진 리더 접촉</span><div class="b" style="width:70%"></div><span class="v">+8.8</span>
<span class="lab">토지 불평등</span><div class="b o" style="width:33%"></div><span class="v">−4.1</span>
<span class="lab">자생 조직 가입</span><div class="b" style="width:31%"></div><span class="v">+3.9</span>
<span class="lab">정부 조직 가입</span><div class="b g" style="width:3%"></div><span class="v">n.s.</span>
<span class="lab">정부 신뢰</span><div class="b g" style="width:3%"></div><span class="v">n.s.</span></div>
<p class="take">계수는 자생 조직 가입(17.57)이 가장 크지만 실질 효과는 규칙(3.77)이 약 세 배 크다. 변수 범위가 각각 .00~.22와 .53~3.85로 다르기 때문이다.<small>유의수준 p&lt;.05 → 유의 4개(1997년 지수 제외) · 1997년 지수 SD 7.1 · R² .23(1997 지수만) → .79</small></p></div></div>''',
          "Krishna 2007: 946(각주 15), 949, 951(각주 20), 952.",
          "왼쪽이 원문 표입니다. 1997년 지수를 빼면 유의한 변수는 넷입니다. 오른쪽은 계수에 변수 범위를 곱한 실질 효과입니다. 계수만 보면 자생 조직이 17.57로 제일 크지만, 그 변수의 마을 간 범위는 0에서 0.22입니다. 규칙은 범위가 0.53에서 3.85여서 실질 효과가 약 세 배입니다. 저자도 952쪽에서 규칙과 신진 리더의 실질 효과가 더 크다고 썼습니다. 회색으로 표시한 아래 두 줄, 정부 조직 가입과 정부 신뢰는 유의하지 않았습니다.")
    add_result2("01_krishna", "Krishna (2007)")
    add_conclusion("01_krishna", "Krishna (2007)")
    slide("Krishna (2007) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>모든 마을이 같은 주의 제도 아래 있어 제도 설계의 효과는 검증 불가(950)</li><li>교육처럼 7년 이상 걸리는 효과는 확인하지 못함(각주 19)</li><li>자생 조직 가입은 1997~2004 증가분이라 내생성 우려(각주 27)</li><li>변화의 크기는 시기에 따라 달랐을 가능성(각주 23)</li><li>리더가 형성되는 과정은 설명하지 못함(954)</li></ul><img class="shot" style="width:100%;max-height:none;margin-top:14px" src="{FIG["krishna_950"]}" alt="950쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>종속변수 정의(945)의 구조 차원에 "rules"가 들어 있는데 951쪽에서는 Rules가 독립변수다. 저자는 측정에서는 중복되지 않는다고 설명하지만(953) 개념상의 중복은 인정한다</li><li>Table 1에는 60개 마을만 있다. 본문 평균 58.4·59.7은 61개 기준</li><li>952쪽은 집단 행동 변수가 "all assessed in 1997"이라고 서술하지만 자생 조직 가입은 증가분이다(각주 27과 불일치)</li><li>Table 1에서 1997년 1~4위 마을은 모두 하락하고 57~61위 마을은 모두 상승했다. 마을당 평균 약 38명(재면접자만 세면 약 28명)인 표본 평균의 변동과 구분해 해석할 필요가 있다</li></ul></div></div>''',
          "",
          "저자가 적은 한계는 다섯 가지이고, 그중 950쪽을 먼저 보시면 됩니다. 모든 마을이 같은 제도 아래 있어서 제도 설계의 효과는 검증할 수 없다고 했습니다. 오른쪽은 제가 원문을 대조하며 찾은 것입니다. 규칙이 종속변수 정의에도 들어 있고 독립변수이기도 합니다. 저자도 개념 수준에서는 겹친다고 인정합니다. 이 점은 토론으로 가져가지 않고 여기서만 짚습니다.")
    issue("7년간의 변화로 역사 의존 가설을 기각할 수 있는가", "Krishna · 토론 2", "catyell",
          ["사회자본은 역사가 정한다!", "7년 만에 바뀌던데요"],
          ("찬 · 기각할 수 있다", "같은 주, 같은 제도 아래 61개 마을 중 33개가 오르고 28개가 내렸다."),
          ("반 · 기각할 수 없다", "1997년 지수가 여전히 유의하고(.12*), 역사 의존은 수백 년 단위의 가설이다."),
          "", local,
          "토론 2입니다. 손을 들어 주십시오. 7년간의 변화로 역사 의존 가설을 기각할 수 있다고 보시는 분, 없다고 보시는 분. 저자는 949쪽에서 역사 의존이 부분적으로만 확인된다고 썼습니다.")

    # ───────── 2 Freitag ─────────
    pcover(2, "swiss_canton", "Freitag (2006)", "Bowling the State Back In: Political Institutions and the Creation of Social Capital", "European Journal of Political Research 45(1): 123–152",
           "정치제도가 다른 지역은 결사체 참여 수준도 다른가", "스위스 24개 칸톤 · 스위스 가구패널 1999 · 분석 단위 칸톤",
           "Krishna의 61개 마을은 모두 라자스탄 주에 속해서 제도가 같았습니다. 저자도 950쪽에서 제도 설계의 효과는 검증할 수 없었다고 밝혔습니다. 제도의 효과를 보려면 제도가 서로 다른 지역을 비교해야 합니다. 둘째 논문인 Freitag의 2006년 연구가 스위스 24개 칸톤으로 그 비교를 합니다.")
    slide("Freitag (2006) 연구 개요", "Bowling the State Back In: Political Institutions and the Creation of Social Capital · <i>EJPR</i> 45(1)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["freitag_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>정치제도(직접민주주의, 합의민주주의, 지방자치)는 결사체 참여 수준에 영향을 미치는가. Putnam의 국가 내 지역 비교 방법을 스위스에 적용</dd>
<dt>자료</dt><dd>24개 칸톤. 종속변수는 Swiss Household Panel 1999 4문항 주성분(N=7,799)의 칸톤 평균. 직접민주주의와 합의민주주의는 1980~1998년 평균, 지방자치는 1990년 조사 지수(Ladner 1994). 언어권은 1990년 인구조사, 도시화는 1990년 두 지표의 합성 척도(각주 9)</dd>
<dt>설계</dt><dd>이변량 분석에서 유의한 변수만 다변량 모형에 투입. N=24여서 모형당 변수는 4개로 제한. 신뢰는 통제변수(신뢰가 가입에 선행한다고 가정, 134)</dd>
<dt>결과</dt><dd>세 제도 변수 모두 이변량 분석에서 유의(.63~.71). 다변량 분석에서 직접민주주의는 다른 통제변수 모형에서 .41~.48로 유의하나 언어권을 통제한 모형에서는 .18로 유의하지 않음(Table 6 Model 5). 직접민주주의와 독일어권 비율의 상관 r=.86(각주 10)</dd>
<dt>한계</dt><dd>"only suggestive and explorative"(146). 공통 원인 가능성을 각주 10에서 인정</dd></dl></div>''',
          "수치는 Table 5·6·7(139~142).",
          "세 제도 변수 모두 이변량 분석에서 결사체 참여와 유의한 양의 관계였습니다. 그런데 언어권을 통제한 모형에서는 직접민주주의 계수가 .18로 유의하지 않습니다. 직접민주주의와 독일어권의 상관이 .86입니다. 저자 스스로 탐색적이라고 썼습니다.")
    slide("Freitag (2006) 연구 질문과 논리 전개", "",
          '''<div class="ladder">
<div class="l">질문</div><div>사회자본의 효과에 관한 연구는 많지만 형성 요인에 관한 연구는 드물다. 정치제도는 결사체 활동을 촉진하는가</div><div class="q">"little research has explicitly addressed the question of how social capital can be built" <i>123</i></div>
<div class="l">이론적 기대</div><div>Jackman &amp; Miller의 구분. 사회자본을 외생으로 두는 접근(Putnam 1993)과 내생으로 두는 접근(Levi, Tarrow, Skocpol). 저자는 후자를 따름. 세 제도의 공통 기제는 시민의 요구를 수렴하고 조정하는 능력. 정치적 결정요인에 관한 기존 이론이 "vague"하다고 평가(131)</div><div class="q">"The second approach endogenizes social capital as an outcome of social and political arrangements" <i>125</i></div>
<div class="l">설계 선택</div><div>한 국가 안의 24개 칸톤을 비교하는 최대유사체계 설계. 제도 변수는 모두 1999년 이전 자료로 측정(138). 인과 방향의 근거는 역사적 순서(직접입법 13~14세기, 결사체 18세기). 결사체 등록 자료가 없어 설문 자료를 사용</div><div class="q">"meet the demands of a most similar system research design in a particularly appropriate manner" <i>124</i></div>
<div class="l">결과</div><div>Table 5의 이변량 분석에서 세 제도 변수 모두 유의. Table 6에서 통제변수를 하나씩 추가하면 직접민주주의는 언어권을, 지방자치는 도시화를 통제할 때 유의성이 사라짐. Table 7에서는 직접민주주의와 언어권을 같은 모형에 투입하지 않음</div><div class="q">"the fit of the four models … further confirms the significance of the thesis" <i>140~142</i></div>
<div class="l">결론</div><div>정치제도가 사회자본 형성에 영향을 미침. Putnam이 말한 불신, 불참, 약한 민주주의의 악순환에서 벗어나는 하향식 경로를 시사</div><div class="q">"democratic institutions suggest a 'top-down' path" <i>145</i></div></div>''',
          "", "저자의 질문은 정치제도가 결사체 활동을 촉진하는가입니다. 이론적 기대 단에서 저자는 Jackman과 Miller의 구분을 인용해 Putnam을 외생 접근으로 분류하고, 자신은 내생 접근을 따릅니다. 4장에서 인용한 125쪽 문장이 이 부분입니다. 설계에서 저자는 인과 방향의 근거로 시간 순서를 듭니다. 제도 변수는 1999년 이전 자료로 측정했고, 직접입법은 13~14세기에, 결사체는 18세기에 시작되었다는 기록을 인용합니다. 결과 단에서 통제변수를 하나씩 넣는 방식이 나오는데, 이 방식은 한계 장에서 다시 검토합니다.")
    add_theory("02_freitag", "Freitag (2006)")
    meas("Freitag (2006) 사회자본과 제도 변수 측정", "127쪽, 각주 2", "freitag_meas", "Freitag 2006: 127. 종속변수 측정 문단",
         [("개념적 정의", "Coleman과 Putnam의 정의 “social networks, cooperative norms and interpersonal trust”(123) 가운데 결사체 참여를 분석 대상으로 선택"),
          ("측정 문항", "스위스 가구패널(SHP) 1999의 4문항. 동호회·단체 활동 참여, 명예직·봉사 활동, 월 봉사 시간, 9개 유형 결사체의 능동 회원 수(각주 2)"),
          ("지수 구성", "주성분 분석에서 한 차원으로 묶임(적재값 모두 .50 이상, KMO .71). 응답자 요인 점수의 칸톤 평균을 종속변수로 사용"),
          ("신뢰의 처리", "신뢰가 결사체 가입에 선행한다고 가정하고 통제변수로 투입(134). 이변량 분석에서 .41**(Table 5), 제도 변수 3개를 통제한 다변량 분석에서 .06으로 유의하지 않음(Table 6 Model 4)"),
          ("제도 변수", "직접민주주의는 주민발의·주민투표의 요건(서명 수, 기간, 재정 주민투표 기준)을 점수화한 지수(Stutzer 1999; Frey &amp; Stutzer 2000, 1~6점). 지수는 이 요건들로만 구성되며 투표 실시 횟수는 포함하지 않음(135)")],
         "Wollebaek &amp; Selle(4주차)는 수동적 회원도 신뢰가 높다고 보고했으나 이 논문의 넷째 문항은 능동 회원만 집계. Knack &amp; Keefer(10주차)는 단체 가입이 경제 성장과 무관하고 신뢰와 시민 규범이 유의하다고 보고",
         "왼쪽이 127쪽 측정 문단입니다. Freitag은 Coleman과 Putnam의 정의에서 결사체 참여만 골라 종속변수로 삼았습니다. 스위스 가구패널 네 문항을 주성분 분석으로 묶고, 칸톤 평균을 썼습니다. 신뢰는 가입보다 먼저 온다고 가정해서 통제변수로 넣었습니다. 신뢰의 계수는 이변량 분석에서 .41로 유의했고, 제도 변수 셋을 함께 넣은 모형에서는 .06으로 유의하지 않습니다. 제도 변수도 하나 짚겠습니다. 직접민주주의 지수는 주민투표를 시작하는 요건을 점수화한 값이라서, 투표가 실제로 몇 번 열렸는지는 담지 않습니다. 이 측정 방식이 다음 장의 토론 1로 이어집니다.")
    choice("주민 참여를 늘리려면 무엇을 먼저 바꿔야 한다고 생각하십니까?", "Freitag · 토론 1", "buttons",
          ["요건 완화", "조직 육성", "지자체장"],
          ("선택 1. 참여 제도의 요건을 낮춘다", "주민투표와 주민발의에 필요한 서명 수와 기간을 줄인다. 제도가 열리면 주민이 요구를 모으려고 모임을 만든다"),
          ("선택 2. 참여할 주민 조직부터 키운다", "모임과 단체가 먼저 있어야 제도를 쓴다. 조직이 없는 곳에서는 제도를 열어도 쓰이지 않는다"),
          "Freitag의 결과: 직접민주주의 지수가 높은 칸톤일수록 결사체 참여가 많았다. 다만 언어권을 통제하면 이 관계는 유의하지 않았다(Table 6)", local,
          "토론 1입니다. 주민 참여를 늘리려면 무엇을 먼저 바꿔야 하는지 여쭙겠습니다. 선택 1은 주민투표와 주민발의의 요건을 낮추는 쪽이고, 선택 2는 참여할 주민 조직부터 키우는 쪽입니다. 한국의 주민참여예산제를 떠올리셔도 좋습니다. Freitag의 결과는 선택 1을 지지하는 것처럼 보입니다. 그런데 직접민주주의 지수가 높은 칸톤은 거의 전부 독일어권이고, 언어권을 통제하면 관계가 유의하지 않습니다. 저자도 각주 10에서 언어권이 제도와 결사체 참여 둘 다의 원인일 수 있다고 적었습니다. 참여가 활발한 지역이 참여 제도를 먼저 갖췄을 가능성도 횡단면 자료로는 배제하기 어렵습니다.")
    slide("Freitag (2006) 분석 결과", "Table 6(141쪽) · 제도 변수 3개에 통제변수를 하나씩 추가한 9개 모형",
          f'''<div class="res"><img class="shot" style="max-height:430px" src="{FIG["freitag_t6"]}" alt="Table 6"><div><div class="k">직접민주주의 표준화 계수, 통제변수에 따라</div><div class="bars">
<span class="lab">+좌파 정당 (M1)</span><div class="b" style="width:100%"></div><span class="v">.47***</span>
<span class="lab">+사회 신뢰 (M4)</span><div class="b" style="width:98%"></div><span class="v">.46***</span>
<span class="lab">+도시화 (M6)</span><div class="b" style="width:100%"></div><span class="v">.47***</span>
<span class="lab">+언어권 (M5)</span><div class="b g" style="width:38%"></div><span class="v">.18 n.s.</span></div>
<div class="k" style="margin-top:14px">R², Table 7의 Model 1과 Model 2</div><div class="bars">
<span class="lab">제도 변수 3개 (M1)</span><div class="b" style="width:95%"></div><span class="v">.75</span>
<span class="lab">도시화 + 언어권 (M2)</span><div class="b g" style="width:100%"></div><span class="v">.79</span></div>
<p class="take">제도 변수 3개의 설명력(R² .75)보다 통제변수 2개의 설명력(R² .79)이 크다. 저자는 두 값을 설명력의 범위로만 적었고(142) 그 차이는 논하지 않았다.<small>직접민주주의와 언어권은 Table 7의 어느 모형에도 함께 투입되지 않는다 · N=24, 모형당 변수 4개(140)</small></p></div></div>''',
          "Freitag 2006: 141~142. Table 6의 Model k는 제도 변수 3개에 k번째 통제변수를 추가한 모형. 제도 변수 3개만 넣은 모형은 Table 7 Model 1.",
          "원문 표를 가로로 돌렸습니다. 아홉 모형은 전부 제도 셋에 통제를 하나씩 더한 것입니다. 오른쪽 위를 보시면, 직접민주주의 계수는 다른 통제변수를 넣은 여덟 모형에서 .41~.48로 유의하고, 언어권을 넣은 모형에서만 .18로 유의하지 않습니다. 아래는 Table 7의 설명력입니다. 제도 셋이 .75인데 도시화와 언어권 둘만 넣으면 .79입니다. 저자는 두 값을 범위로만 적고 그 차이는 논하지 않았습니다.")
    add_result2("02_freitag", "Freitag (2006)")
    add_conclusion("02_freitag", "Freitag (2006)")
    slide("Freitag (2006) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>"only suggestive and explorative"(146). 더 정교한 방법이 필요하다고 밝힘</li><li>언어권이 직접민주주의와 사회자본의 공통 원인일 수 있다(각주 10, r=.86)</li><li>이변량 분석에서 제외된 변수가 다변량 분석에서 유의할 가능성(각주 8)</li><li>N=24여서 모형당 변수를 4개로 제한(140, 저자는 설계상 제약으로 서술). 국가 수준 비교는 거의 불가능(146)</li><li>결사체는 연결망의 한 지표일 뿐, 가장 중요한 지표는 아닐 수 있다(126)</li><li>신뢰 변수는 다른 조사 자료이고 칸톤별 응답자가 24~351명이어서 해석에 주의가 필요하다고 밝힘(각주 6)</li></ul><img class="shot" style="width:100%;max-height:none;margin-top:14px" src="{FIG["freitag_146"]}" alt="146쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>제도 변수 3개는 모든 모형에 포함되고 통제변수는 하나씩만 추가된다. 제도 변수가 대부분의 모형에서 유의하다는 결과는 이 모형 구성의 영향을 받는다. 유의한 통제변수 2개(언어권, 도시화)를 함께 투입한 모형은 Table 6에 없다</li><li>개인 약 7,800명의 응답을 24개 칸톤 평균으로 집계했다. 세 기제(결사 유인, 숙의 기회, 반응성에 대한 확신)는 개인 수준의 과정인데 검증되지 않았다</li><li>직접민주주의 지수는 제도의 이용 요건을 측정하며 실제 이용 경험은 측정하지 않는다. 뒤의 세 논문은 제도를 실제로 경험하는 과정을 다룬다</li></ul></div></div>''',
          "",
          "저자가 적은 한계 중 둘째 줄이 핵심입니다. 공통 원인 가능성을 각주에서 스스로 인정했습니다. 제가 짚는 것은 설계입니다. 제도 셋은 늘 모형에 남고 통제는 하나씩만 들어갑니다. 제도 변수가 대부분의 모형에서 유의하다는 결과는 이 모형 구성의 영향을 받습니다. 마지막 줄의 측정 문제는 측정 장에서 말씀드렸습니다. 뒤의 세 논문은 제도를 실제로 경험하는 과정을 다룹니다.")
    issue("결사체 참여가 신뢰와 무관하다면 국가는 사회자본을 만든 것인가", "Freitag · 토론 2", "drake",
          ["신뢰를 종속변수로 두고 제도 효과를 본다", "신뢰는 통제변수에 넣고 .06이 나오면 넘어간다"],
          ("찬 · 만들었다", "결사체는 사회자본의 한 요소인 연결망이고, 모임에서 규범과 신뢰가 자란다(Putnam)."),
          ("반 · 만들지 못했다", "제도 변수 3개를 통제하면 신뢰는 결사체 참여와 유의한 관계가 없었다(.06, Table 6)."),
          "", local,
          "손을 들어 주십시오. 결사체 참여가 신뢰와 무관했다면 국가가 사회자본을 만들었다고 볼 수 있는지 여쭙겠습니다. 저자는 각주 6에서 신뢰 변수의 해석에 주의가 필요하다고 밝혔습니다. 이 질문은 12주차와 13주차의 신뢰 문헌으로 이어집니다.")

    # ───────── 3 Lowndes & Wilson ─────────
    pcover(3, "birmingham_council", "Lowndes &amp; Wilson (2001)", "Social Capital and Local Governance: Exploring the Institutional Design Variable", "Political Studies 49(4): 629–647",
           "지방정부의 제도 설계는 사회자본의 형성과 동원에 어떤 영향을 미치는가", "영국 지방정부 · 이론 논문, 자체 자료 없음",
           "Freitag은 제도와 결사체 참여가 함께 움직인다는 점까지 보여 줬습니다. 다만 어떤 설계가 왜 작동하는지는 설명하지 않았고, 신뢰가 왜 유의하지 않았는지도 남았습니다. 셋째 논문인 Lowndes와 Wilson의 2001년 연구는 자료 없이 제도 설계의 경로를 이론으로 정리합니다.")
    slide("Lowndes &amp; Wilson (2001) 연구 개요", "Social Capital and Local Governance: Exploring the Institutional Design Variable · <i>Political Studies</i> 49(4)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["lw_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>Putnam이 상수로 가정한 제도 설계는 사회자본의 창출과 동원에 어떤 영향을 미치는가</dd>
<dt>자료</dt><dd>없음. 영국 노동당의 '민주적 쇄신' 프로그램(1997~)과 저자들의 선행 조사(Lowndes et al. 1998, 2001), Audit Commission 1999를 근거로 한 이론 논문</dd>
<dt>설계</dt><dd>지방정부 제도 설계의 네 차원. ① 자발적 부문과의 관계 ② 시민 참여 기회 ③ 의사결정의 반응성 ④ 민주적 리더십과 사회적 포용</dd>
<dt>주장</dt><dd>여론조사 방식은 사회자본에 거의 기여하지 않을 것으로 보이고, 숙의형 참여는 사회자본을 창출할 수 있다. 우수 사례로 꼽힌 지방정부의 4분의 3이 협의 결과를 의사결정 과정에 연결하지 못했다. 반응하는 제도가 없으면 사회자본은 잠재 상태에 머물 수 있다</dd>
<dt>한계</dt><dd>"we have not set out specifically to evaluate the reforms"(641). 지정문헌 5편 중 유일하게 실증 분석이 없다</dd></dl></div>''',
          "수치는 638(4분의 3)과 639(12개 지표 중 민주주의 변수 0) 둘뿐.",
          "다섯 편 중 자료가 없는 유일한 논문입니다. 저자들은 자료 대신 지방 거버넌스 제도 설계의 네 차원을 분석틀로 제시합니다. 원문에 나오는 수치는 두 개입니다. 하나는 우수 사례로 꼽힌 지방정부의 4분의 3이 협의 결과를 의사결정 과정에 연결하지 못했다는 Audit Commission의 조사 결과입니다. 다른 하나는 Putnam의 제도 성과 지표 12개 가운데 민주주의와 관련된 변수가 하나도 없다는 저자들의 지적입니다.")
    slide("Lowndes &amp; Wilson (2001) 연구 질문과 주장", "",
          '''<div class="ladder">
<div class="l">질문</div><div>Putnam(1993: 10)의 가정을 비판한다. Putnam은 이탈리아 지역정부의 제도 설계가 동일하므로 다른 요인의 영향을 더 정확히 확인할 수 있다고 보았다. 저자들은 성과 차이가 큰데도 제도 설계가 같았다고 가정할 근거가 무엇인지 묻는다</div><div class="q">"why should we assume that their design remained constant?" <i>632</i></div>
<div class="l">이론적 기대</div><div>세 가지 전제(발제자 정리). 신제도주의에 따르면 제도에는 공식 조직 구조 외에 관행, 규범, 유인이 포함된다(632). 사회자본의 창출과 동원은 구분된다. 좋은 정부는 공익 지향적 시민과 공익 지향적 정부 행위자의 상호작용에서 나온다(Levi 1996)</div><div class="q">"Institutions are habits, not things" <i>Fox &amp; Miller 1995: 91, 632에서 재인용</i></div>
<div class="l">설계 선택</div><div>영국 노동당 정부의 지방정부 제도 개편을 사례로 네 차원을 검토한다. 제도 설계는 정밀과학이 아니며, 배제적 설계가 오히려 사회자본을 높인 사례(Newton 1976)도 있음을 전제로 밝힌다</div><div class="q">"Institutional redesign cannot, however, be a precise science" <i>633</i></div>
<div class="l">주장</div><div>발제자가 보기에 네 차원 중 셋째(의사결정의 반응성)가 논의의 중심. 참여를 가로막는 가장 큰 요인은 지방정부가 반응하지 않는다는 인식 또는 경험. 사회자본의 공급은 정치 과정의 수요와 연결되어야 한다</div><div class="q">"Social capital may, then, remain a 'latent' phenomenon in the absence of responsive political institutions" <i>638</i></div>
<div class="l">결론</div><div>설계 원칙 두 가지: 가치의 명확성, 다양성과 수정 가능성. 저자들은 Offe(1996)의 ‘제도 가꾸기’와 ‘제도 공학’ 대비를 빌려, 지역 여건에 맞춘 설계는 정착하기 쉬우나 급진적 변화를 일으키기 어렵다고 지적한다(645). 사회자본의 창출과 동원 전망은 설계 내용만큼 설계 과정에 좌우될 수 있다</div><div class="q">"may depend as much upon the process as upon the content of institutional redesign" <i>645</i></div></div>''',
          "", "저자들은 제도 설계가 상수였다는 Putnam의 가정을 문제 삼습니다. 저자들은 Fox와 Miller를 인용해 제도를 관행으로 봅니다. 저자들은 네 차원을 제시하기 전에 단서를 둡니다. 제도 재설계는 정밀과학이 될 수 없고, 나쁜 설계가 사회자본에 긍정적으로 작용한 사례도 있다고 적었습니다. 이 사례는 한계 장에서 셋째 차원의 주장과 견주어 다시 보겠습니다. 제가 보기에 논의의 중심은 셋째 차원인 의사결정의 반응성입니다. 저자들은 반응하는 제도가 없으면 사회자본이 잠재 상태로 남을 수 있다고 봅니다.")
    add_theory("03_lw", "Lowndes &amp; Wilson (2001)")
    meas("Lowndes &amp; Wilson (2001) 핵심 개념", "630~641쪽", "lw_latent", "Lowndes &amp; Wilson 2001: 638",
         [("개념적 정의", "Putnam(1995)의 정의를 사용. 규범(Coleman, Fukuyama), 구조(Bourdieu), 결과(Coleman, Ostrom)를 함께 포함(630)"),
          ("창출과 동원", "창출은 연결망과 규범이 만들어지는 과정(차원 ①②), 동원은 이미 있는 사회자본이 민주적 결정에 영향을 미치는 과정(차원 ③④, 차원 대응은 발제자 정리). “Participation is not, after all, the same as social capital”(637)"),
          ("잠재 상태", "사회자본이 있어도 이에 반응하는 정치 제도가 없으면 민주주의 성과로 이어지지 않는 상태(638). 결론에서는 조건이 “responsive and inclusive”로 늘어남(641)"),
          ("측정", "자체 자료와 측정 없음. 영국 지방정부 사례와 기존 연구를 근거로 논의")],
         "Coleman(1988, 3주차)은 사회자본을 기능으로 정의하므로, 기능하지 않는 잠재 사회자본은 그 정의와 맞지 않음. Dasgupta(2000, 9주차)가 비판한 이질적 요소의 합산(p.327)을 이 논문은 장점으로 평가",
         "이 논문은 자체 측정이 없어서 개념을 정리했습니다. 왼쪽이 638쪽 원문입니다. 저자들은 Putnam의 정의를 쓰는데, 그 정의에는 규범과 구조와 결과가 함께 들어 있습니다. 9주차 Dasgupta가 비판한 합산을 저자들은 장점으로 평가합니다. 그리고 사회자본이 만들어지는 과정과 동원되는 과정을 나눕니다. 사회자본이 있어도 제도가 반응하지 않으면 민주주의 성과로 이어지지 않는데, 저자들은 이 상태를 잠재라고 부릅니다. 3주차 Coleman처럼 사회자본을 기능으로 정의하면 잠재 사회자본이라는 개념이 성립하는지 따져 볼 수 있습니다. 이어지는 토론 1에서는 반응성 문제를 공청회 사례로 다루겠습니다.")
    choice("결과를 반영하기 어려운 사안에도 공청회를 열어야 한다고 생각하십니까?", "Lowndes &amp; Wilson · 토론 1", "fine",
          ["공청회는 열었습니다 (4분의 3은 결과를 의사결정에 연결하지 못함)"],
          ("선택 1. 연다", "주민이 서로 만나는 것만으로 새 모임이 생길 수 있다. 의견을 들을 기회는 그 자체로 필요하다"),
          ("선택 2. 열지 않는다", "의견을 듣고 반응하지 않으면 다음 참여가 줄어든다. 반영할 수 있는 사안에만 연다"),
          "Lowndes &amp; Wilson의 주장: 참여를 가로막는 가장 큰 요인은 지방정부가 반응하지 않는다는 인식이나 경험이다(638). 공청회는 주민이 만나 새 모임을 만드는 계기가 될 수 있다(637)", local,
          "토론 1입니다. 결과를 반영하기 어려운 사안에도 공청회를 열어야 하는지 여쭙겠습니다. Lowndes와 Wilson은 양쪽 근거를 모두 줍니다. 638쪽에서는 지방정부가 반응하지 않는다는 인식이 참여를 가로막는 가장 큰 요인이라고 썼습니다. 637쪽에서는 공청회가 주민이 서로 만나 새 모임을 만드는 계기가 될 수 있다고 썼습니다. 저자들은 결정자가 주민 의견에 반응할 능력을 갖추는 것을 지방정부의 과제로 들고, 반응이 주민 의견대로 결정하는 것과 같지는 않다고 덧붙입니다.")
    slide("Lowndes &amp; Wilson (2001) 제도 설계 변수", "차원별 설계 변수, 사회자본에 미치는 경로, 근거",
          f'''<div class="two" style="grid-template-columns:1.7fr 1fr;align-items:start;gap:30px"><table style="font-size:14.5px;table-layout:fixed"><colgroup><col style="width:20%"><col style="width:23%"><col style="width:35%"><col style="width:22%"></colgroup><tr><th>차원</th><th>설계 변수</th><th>사회자본에 미치는 영향</th><th>근거</th></tr>
<tr><td>① 자발적 부문과의 관계</td><td>보조금, 계약·파트너십 조건, 인정 요건</td><td>창출. 계약·파트너십 관계는 단체를 지방정부와 유사하게 만들 수 있고 소규모 단체와 캠페인형 단체에 불리</td><td>"Unless you're cute and big"(635, 공무원 발언 재인용)</td></tr>
<tr><td>② 시민 참여 기회</td><td>조사 → 공청회 → 시민배심·포럼</td><td>창출. 여론조사 방식은 거의 기여하지 않을 것으로 보이고 숙의형 참여는 창출할 수 있음</td><td>637</td></tr>
<tr><td>③ 의사결정의 반응성</td><td>협의 결과의 결정 연결, 집행부·의회 분리</td><td>동원. 반응이 없으면 참여가 줄고 사회자본은 잠재 상태에 머물 수 있음</td><td>Audit Commission 1999: 41(638)</td></tr>
<tr><td>④ 리더십과 포용</td><td>회의 시각·형식·언어, 직선 시장</td><td>동원의 분배. 절차가 참여자의 범위를 결정</td><td>Hall 1999: 사회자본은 "중산층·중년의 것"(641)</td></tr></table>
<div><img class="shot" style="width:100%;max-height:none" src="{FIG["lw_quarters"]}" alt="638쪽 Audit Commission"><p class="take" style="font-size:15.5px">수치 근거는 두 개이며 모두 셋째·넷째 차원에 해당한다. 이 논문의 기여는 창출(①②)보다 동원(③④)에 대한 논의에 있다.<small>12개 지표 중 민주주의 변수 0은 Putnam 1993 3장에 대한 지적(639)</small></p></div></div>''',
          "Lowndes &amp; Wilson 2001: 633~641. 표는 발제자 정리, 인용은 원문 쪽수.",
          "원문에 표가 없어서 네 차원을 제가 표로 정리했습니다. 왼쪽부터 설계 변수, 사회자본에 미치는 영향, 근거입니다. 연구 개요에서 말씀드린 수치 두 개는 모두 아래 두 줄인 셋째와 넷째 차원에 있습니다. 저는 이 논문이 새로 보탠 논의가 창출보다 동원에 있다고 봅니다. 사회자본이 있어도 민주주의 성과로 이어지지 않는 상태를 잠재라는 개념으로 정리한 것이 그 내용입니다.")
    add_result2("03_lw", "Lowndes &amp; Wilson (2001)")
    add_conclusion("03_lw", "Lowndes &amp; Wilson (2001)")
    slide("Lowndes &amp; Wilson (2001) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>개혁의 평가가 목적이 아님(641). 결과를 예측하기 어려움(643)</li><li>설계는 정밀과학이 아니며 의도치 않은 효과가 반복된다(633)</li><li>지방정부가 사회자본 측면의 성과를 측정하기 어렵다는 점을 언급(637)</li><li>지역 여건에 맞춘 설계는 정착하기 쉬우나 급진적 변화를 일으키기 어려움(645)</li></ul><img class="shot" style="width:100%;max-height:none;margin-top:14px" src="{FIG["lw_641"]}" alt="641쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>네 차원은 분류틀이며 인과적 설명을 제공하지 않는다. 어떤 관찰 결과도 네 차원 중 하나로 분류되므로 반증 가능성이 낮다. 사회자본 성과를 측정하기 어렵다는 점(637)은 이 분석틀에도 적용된다</li><li>Newton(1976)의 사례(633)는 셋째 차원의 주장과 상충한다. 소수민족 압력단체에 대한 지방정부의 배제가 잠재 상태로 이어지지 않고 동원과 의사결정 영향력 확대로 이어졌다. 저자들은 "With these caveats in mind"라고 언급한 뒤 이 사례를 다시 다루지 않는다</li><li>잠재의 조건이 638쪽 "responsive"에서 641쪽 "responsive and inclusive"로 확대된다</li><li>638쪽의 논리(무반응이 참여를 막는다)는 동원 실패가 창출을 저해한다는 것이다. 저자들은 네 차원이 상호작용한다고만 적고(633) 그 경로는 전개하지 않는다</li><li>숙의형 참여의 효과와 잠재 상태에 관한 핵심 주장은 "may"로 서술되어 있다</li></ul></div></div>''',
          "",
          "저자들은 평가가 목적이 아니라고 결론에서 말합니다. 제가 짚는 것은 둘째 줄입니다. 저자들이 직접 든 버밍엄 사례가 셋째 차원의 주장과 상충하는데, 저자들은 단서로만 언급하고 다시 다루지 않습니다. 이 점은 이어지는 토론 2의 질문과 연결됩니다.")
    issue("실증 자료가 없는 제도 설계 틀을 정책 근거로 쓸 수 있는가", "Lowndes &amp; Wilson · 토론 2", "gru",
          ["제도 설계의 네 차원을 짠다", "반응하는 제도가 사회자본을 동원한다", "자료는 없다", "자료는 없다"],
          ("찬 · 쓸 수 있다", "네 차원은 제도를 고치면 바꿀 수 있는 변수이고, 이후 연구가 검증할 목록이 된다."),
          ("반 · 쓸 수 없다", "어떤 관찰이 나오면 틀이 틀린 것인지 제시되어 있지 않다."),
          "", local,
          "손을 들어 주십시오. 실증 자료가 없는 설계 틀을 정책 근거로 쓸 수 있는지 여쭙겠습니다. 제도와 조직이 사회자본에 영향을 미치는지는 앞서 본 Freitag(2006)과 Krishna(2007)가 5~6년 뒤에 자료로 검증했습니다.")

    # ───────── 4 Mettler ─────────
    pcover(4, "us_veterans_1945", "Mettler (2002)", "Bringing the State Back In to Civic Engagement: Policy Feedback Effects of the G.I. Bill for World War II Veterans", "American Political Science Review 96(2): 351–365",
           "제대군인원호법(G.I. Bill) 교육 급여는 수급자의 시민참여를 높였는가", "미국 제2차 세계대전 참전자 716명 · 1998년 회고 설문 · 분석 단위 개인",
           "Lowndes와 Wilson은 제도 설계의 경로를 제시했지만 자료가 없었습니다. 그래서 한 사람이 제도를 경험한 뒤 무엇이 달라지는지는 알 수 없습니다. 넷째 논문인 Mettler의 2002년 연구는 정책 하나를 골라 개인 수준에서 확인합니다. 미국 제2차 세계대전 참전자 716명에게 1998년에 설문했고, 그중 61%가 제대군인원호법 교육 급여 이용자입니다.")
    slide("Mettler (2002) 연구 개요", "Bringing the State Back In to Civic Engagement: Policy Feedback Effects of the G.I. Bill · <i>APSR</i> 96(2)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["mettler_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>미국 제대군인원호법(G.I. Bill)의 교육 급여가 1950~64년 시민참여를 높였는가. 높였다면 자원 효과인가, 해석 효과인가</dd>
<dt>자료</dt><dd>참전자회 명단 4,000명 중 1,000명 우편조사(1998년 8월), 응답 716명(73.5%). 면접 28명. 남성, 백인 98.5%</dd>
<dt>설계</dt><dd>가설 4개(기존 특성, 부산물, 수동성, 정책 환류)를 배경 변수와 학력을 통제한 뒤 급여 이용 계수의 부호로 구분. 종속변수는 1950~64년 단체 가입 수와 정치참여. 생활수준과 급여 이용의 상호작용항으로 결정적 효과(critical effects) 가설을 검증</dd>
<dt>결과</dt><dd>학력을 통제해도 급여 이용자는 단체 가입 수가 .47, 정치참여가 .38 높음(Table 1·2, p=.01). 정치참여 모형에서 학력은 유의하지 않음. 호혜 변수는 단체 가입에서만 유의. 단체 가입에서 급여 효과는 아동기 생활수준 중하·중간 집단에서 유의하고 최하 집단에서는 유의하지 않으며(Table 6), 정치참여에서는 중상·상 집단의 계수(1.22)가 가장 큼(Table 7)</dd>
<dt>한계</dt><dd>회고 설문(부록 A). 표본의 고등교육 이용자는 입대 전 학력이 더 높고 직업훈련 이용자는 과소대표되어 효과가 과소추정될 가능성(부록 B, 각주 24). 정치참여에서 급여 이용의 효과는 1965년 이후 점차 유의하지 않게 됨(각주 15)</dd></dl></div>''',
          "Table 1~7(357~362). 표의 둘째 열은 표준화계수 β, 표준오차가 아님.",
          "이 논문은 제대군인원호법의 교육 급여가 1950~64년의 시민참여를 높였는지를 묻습니다. 높였다면 그 효과가 자원 효과인지 해석 효과인지도 묻습니다. 가설 넷을 배경 변수와 학력을 통제한 뒤 급여 이용 계수로 가릅니다. 학력을 통제한 뒤에도 급여 이용 계수가 유의하면 부산물 가설만으로는 결과를 설명할 수 없습니다. 분석 결과 급여 이용 계수는 단체 가입에서 .47, 정치참여에서 .38로 유의했습니다.")
    slide("Mettler (2002) 연구 질문과 논리 전개", "가설 4개의 예측을 배경 변수와 학력 통제 후 계수로 비교",
          f'''<div class="two" style="grid-template-columns:1.75fr 1fr;align-items:start;gap:26px"><div class="ladder" style="grid-template-columns:92px 1.9fr 1fr">
<div class="l">질문</div><div>시민참여가 가장 높았던 시기(1950~60년대)는 국가 개입이 확대된 직후였다. 두 현상의 시간적 선후는 우연인가</div><div class="q">"Was the sequencing … merely a coincidence?" <i>351</i></div>
<div class="l">이론적 기대</div><div>정책은 제도로 기능한다(Schattschneider, Lowi). Pierson의 자원 효과(참여 역량)와 해석 효과(참여 성향). 가설 4개의 예측: 기존 특성 가설은 배경 변수 통제 후, 부산물 가설은 학력 통제 후 계수 0, 수동성 가설은 음(−), 정책 환류 가설은 양(+)</div><div class="q">"policies function as institutions, imposing particular norms and rules on recipients" <i>352</i></div>
<div class="l">설계 선택</div><div>기존 대규모 조사에 급여 이용 변수가 없어 자료를 직접 수집. 전국 단위 무작위 표본틀이 없어 참전자회 명단을 사용. 분석 시기를 1950~64년으로 한정한 이유는 급여 이용 직후이고 Putnam이 지적한 단체 가입의 정점이기 때문</div><div class="q">"A national, random sample of all World War II veterans was not available" <i>355</i></div>
<div class="l">결과</div><div>정책 환류 가설의 예측과 일치(양의 계수). 학력 통제 후 .47(단체 가입), .38(정치참여). 정치참여 모형에서 학력은 .01로 유의하지 않음. 호혜 변수는 단체 가입에서만 유의. 결정적 효과 모형에서는 단체 가입에서 아동기 생활수준 중하·중간 집단의 상호작용항이 유의(Table 6)</div><div class="q">"the G.I. Bill benefits were not merely a conduit for higher levels of education" <i>357</i></div>
<div class="l">결론</div><div>급여가 수급자의 시민적 통합(incorporation)을 촉진했다. 정책 설계가 수급자에게 어떤 메시지를 전달하는지가 후속 연구 과제</div><div class="q">"It is time to 'bring the state back in' to the study of civic life." <i>363</i></div></div>
<div><img class="shot" style="max-height:330px" src="{FIG["mettler_fig1"]}" alt="Figure 1"><p class="k" style="margin-top:6px">Figure 1(353). 자원 효과는 참여 역량에, 해석 효과는 참여 성향에 영향. 자원 효과가 참여 성향에, 급여 자원이 해석 효과에 영향을 미치는 교차 경로도 있음</p></div></div>''',
          "", "이 논문은 가설 넷을 급여 이용 계수 하나의 부호로 구분합니다. 배경 변수와 학력을 통제했을 때 급여 이용 계수가 0이면 기존 특성이나 부산물, 음수면 수동성 가설, 양수면 정책 환류 가설입니다. 오른쪽은 Pierson의 두 효과를 Mettler가 참여 역량과 성향으로 연결해 확장한 그림입니다. 자원 효과는 역량으로, 해석 효과는 성향으로 갑니다. 결과는 양수였습니다.")
    add_theory("04_mettler", "Mettler (2002)")
    meas("Mettler (2002) 시민참여 측정", "356쪽", "mettler_dv", "Mettler 2002: 356. 종속변수 조작화",
         [("설명 대상", "전후 세대의 높은 결사체 가입률(Putnam의 ‘civic generation’). 사회자본은 정의 없이 세 번 언급되고(351·362·363) 신뢰 문항은 없음"),
          ("종속변수 1", "시민단체 가입 수. 1950~64년 우애단체, 이웃·주택소유자 협회, PTA, 기타 시민단체 가입 수의 합(356)"),
          ("종속변수 2", "정치참여. 정치단체 가입 수와 다섯 가지 활동(공직자 접촉, 선거운동, 위원회 참여, 기부, 시위) 참여 여부"),
          ("해석 효과 근거", "회귀에 투입한 태도 문항 1개 “I felt I owed something back to American society”(4점 척도, 평균 2.9, 359)과 면접 28명(355, 358~360). 해석 효과를 직접 측정한 변수는 없음")],
         "Glaeser 외(2002, 4주차)의 개인 투자 관점에서 이 급여는 교육 비용을 낮춘 외생적 변화. 저자는 Fukuyama 등의 의존 비판이 본래 자산조사형 공공부조를 겨냥한 것임을 밝히면서(353) 수동성 가설을 기각(357)",
         "왼쪽이 356쪽, 종속변수를 조작화한 문단입니다. 종속변수는 둘입니다. 하나는 1950년부터 64년까지의 시민단체 가입 수이고, 다른 하나는 정치단체 가입과 다섯 가지 정치 활동입니다. 신뢰 문항은 없습니다. 해석 효과의 근거는 설문 한 문항과 면접 28명입니다. 면접에서는 신청만 하면 수표가 왔다, 그냥 등록했다는 진술이 나옵니다. 따라서 해석 효과는 설문 한 문항과 면접 진술에서 추론한 결과이고, 직접 측정한 변수는 없습니다. 이 점은 토론 2에서 다시 다루겠습니다. 먼저 토론 1입니다.")
    choice("국가가 주는 장학금에 사회 기여 조건을 붙여야 한다고 생각하십니까?", "Mettler · 토론 1", "handshake",
          ["국가가 준 등록금과 월 75달러", "1950년대의 단체 가입", "빚졌다는 느낌 2.9점"],
          ("선택 1. 조건 없이 준다", "받은 사람이 스스로 갚을 방법을 찾는다. 조건을 붙이면 의무가 되어 자발적 참여가 줄 수 있다"),
          ("선택 2. 봉사나 지역 근무 조건을 붙인다", "세금으로 준 급여이므로 사회에 돌려주는 방법을 정해 둔다. 조건이 있어야 기여가 확실하다"),
          "Mettler의 결과: 급여에 사회 기여 조건은 없었지만, 사회에 갚을 것이 있다고 느낀 이용자일수록 1950~64년에 단체에 더 많이 가입했다(Table 3)", local,
          "토론 1입니다. 국가가 주는 장학금에 사회 기여 조건을 붙여야 하는지 여쭙겠습니다. 제대군인원호법 급여에는 수급 뒤의 사회 기여 조건이 없었습니다. 그런데 사회에 갚을 것이 있다고 느낀 이용자일수록 단체에 더 많이 가입했습니다. 다만 이 감정은 정치참여와는 관련이 없었고, 급여 자체가 군 복무 뒤에 받은 것이라는 점도 함께 보셔야 합니다.")
    slide("Mettler (2002) 분석 결과", "Table 1 · 1950~64년 단체 가입 수, OLS, N=393",
          f'''<div class="res"><img class="shot" style="max-height:420px" src="{FIG["mettler_t1"]}" alt="Table 1"><div><div class="k">비표준화 계수 b와 유의확률</div><div class="bars">
<span class="lab">G.I. Bill 이용</span><div class="b" style="width:100%"></div><span class="v">.47 (.01)</span>
<span class="lab">부모 시민활동</span><div class="b" style="width:60%"></div><span class="v">.28 (.00)</span>
<span class="lab">1960년대 생활수준</span><div class="b g" style="width:49%"></div><span class="v">.23 (.06)</span>
<span class="lab">최종 학력</span><div class="b" style="width:19%"></div><span class="v">.09 (.02)</span></div>
<div class="k" style="margin-top:14px">정치참여(Table 2, N=379)</div><div class="bars">
<span class="lab">G.I. Bill 이용</span><div class="b" style="width:100%"></div><span class="v">.38 (.01)</span>
<span class="lab">최종 학력</span><div class="b g" style="width:3%"></div><span class="v">.01 (.67)</span></div>
<p class="take">학력을 통제해도 급여 이용의 효과는 유의하고, 정치참여 모형에서 학력은 유의하지 않다.<small>유의수준 p&lt;.05 → 이용 .01 · 학력(정치) .67. 각주 15: 정치참여에서 1965년 이후 학력이 유의해지고 급여 이용은 점차 유의하지 않게 됨(Mettler & Welch 2001)</small></p></div></div>''',
          "Mettler 2002: 357~358. R²는 .14와 .08. 표의 둘째 열(β)은 생략.",
          "왼쪽이 Table 1 원문입니다. 급여 이용 .47, 학력 .09. 아래 정치참여에서는 학력이 .01, 비유의입니다. 학력을 통제해도 급여 이용 계수가 유의하기 때문에 부산물 가설만으로는 설명이 부족합니다. 그런데 각주 15를 보면 1965년 이후에는 결과가 달라집니다. 정치참여에서 학력이 유의해지고 급여 이용의 효과는 점차 유의하지 않게 됩니다. Mettler와 Welch는 시간이 지나면서 해석 효과가 약해지고, 학력 상승이라는 자원 효과가 고등교육 이용자의 참여를 높였다고 추론합니다.")
    add_result2("04_mettler", "Mettler (2002)")
    add_conclusion("04_mettler", "Mettler (2002)")
    slide("Mettler (2002) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>1998년에 1950~64년의 활동을 회고로 조사. 세부 활동 대신 전반적인 참여 여부만 묻고, 과거의 태도는 거의 묻지 않음(부록 A)</li><li>표본의 급여 이용률 60.8%(모집단 51%), 조사 시점에 참전자의 3분의 2가 사망. 표본의 고등교육 이용자는 입대 전 학력이 더 높고 직업훈련 이용자가 과소대표되어 효과가 과소추정될 가능성(부록 B, 각주 24)</li><li>남성, 백인 98.5%, 흑인 부대 미포함(355, 각주 4). 급여 집행 과정에 인종 차별이 있었음(각주 21)</li><li>결측으로 회귀 N은 393(716의 55%, 발제자 계산)</li><li>최하 집단에서 효과가 유의하지 않은 이유는 급여가 아동기 빈곤의 영향을 상쇄하지 못했기 때문으로 추정하고, 정확한 경로는 후속 과제로 남김(361)</li></ul><img class="shot" style="width:100%;max-height:none;margin-top:14px" src="{FIG["mettler_appA"]}" alt="부록 A"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>해석 효과는 직접 측정되지 않았고 학력 통제 후 남은 급여 이용 계수로 추론된다. 이 계수는 측정되지 않은 다른 자원(월 75~120달러 생활비, 대학에서 쌓은 동료 연결망, 급여 기간 12~48개월)의 효과일 수 있다</li><li>저자는 과거 태도를 많이 묻지 않기로 했다고 밝혔는데(부록 A), 호혜 문항과 Table 5의 문항은 1998년에 과거형으로 물은 회고 문항이다. 해석 효과의 설문 근거가 회고 응답에 의존한다</li><li>효과가 사회경제적 배경이 불리한 집단에서 크다는 해석은 두 종속변수 모두에서 유의한 중하 집단에만 성립. 계수는 단체 가입(.71, Table 6)과 정치참여(1.22, Table 7) 모두 중상·상 집단이 가장 큼</li><li>비이용자도 모두 참전자여서 군 복무를 경험했고, 원호법에는 교육 외에 다른 급여도 있었다(351). 비교집단을 정책 미경험 집단으로 보기 어렵다</li></ul></div></div>''',
          "",
          "저자가 밝힌 한계는 회고 설문과 표본 대표성이고, 부록 A와 B에서 각각 다룹니다. 제가 추가로 검토한 것은 오른쪽 첫 줄입니다. 해석 효과를 직접 재지 않았습니다. 저자는 학력을 통제한 뒤에도 유의한 급여 이용 계수에서 해석 효과를 추론합니다. 그런데 이 계수에는 월 75달러 생활비나 대학에서 쌓은 동료 연결망의 효과가 포함되어 있을 수 있습니다. 이 문제를 토론 2에서 여쭙겠습니다.")
    issue("급여의 효과는 받는 방식에서 온 것인가", "Mettler · 토론 2", "boyfriend",
          ["신청서 한 장, 다음 달 입금 (해석 효과)", "참전 군인", "졸업장과 소득 (자원 효과)"],
          ("찬 · 받는 방식에서 왔다", "고등교육 급여 이용자들은 절차가 간단했다고 기억했고, 정치참여에서 학력은 유의하지 않고 급여 이용은 유의했다(Table 2)."),
          ("반 · 받은 자원에서 왔다", "해석 효과를 직접 측정한 변수가 없고, 남은 계수는 생활비나 대학 동료 연결망의 효과일 수 있다."),
          "", local,
          "손을 들어 주십시오. 급여의 효과가 받는 방식에서 왔다고 보시는 분, 받은 자원에서 왔다고 보시는 분. 저자는 두 효과가 모두 있었다고 결론 내립니다. 다만 해석 효과를 직접 측정한 변수는 없습니다.")

    # ───────── 5 Kumlin & Rothstein ─────────
    pcover(5, "sweden_office", "Kumlin &amp; Rothstein (2005)", "Making and Breaking Social Capital: The Impact of Welfare-State Institutions", "Comparative Political Studies 38(4): 339–365",
           "선별 복지 기관과 보편 복지 기관 접촉은 대인신뢰에 각각 어떤 영향을 미치는가", "스웨덴 서부 2,543명 · 횡단면 설문 · 분석 단위 개인",
           "Mettler의 연구에는 남은 점이 셋 있습니다. 신뢰를 측정하지 않았고, 정책이 하나였고, 선별 프로그램과 직접 비교하지 않았습니다. 다섯째 논문인 Kumlin과 Rothstein의 2005년 연구는 같은 응답자가 선별 기관과 보편 기관을 각각 몇 곳 접촉했는지 세고, 종속변수를 대인신뢰로 둡니다.")
    slide("Kumlin &amp; Rothstein (2005) 연구 개요", "Making and Breaking Social Capital: The Impact of Welfare-State Institutions · <i>Comparative Political Studies</i> 38(4)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["kr_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>복지국가의 규모가 클수록 사회자본이 구축(crowding-out)된다는 주장은 스칸디나비아의 높은 신뢰 수준과 맞지 않는다. 저자들은 복지국가의 규모보다 제도 유형에 주목한다</dd>
<dt>자료</dt><dd>서부 스웨덴(Västra Götaland) SOM 1999 조사. 선별 기관 7(주거수당·사회부조·장애연금·노인 돌봄 등), 보편 기관 10(보육·도서관·보건소 등). 회귀 N=2,543</dd>
<dt>설계</dt><dd>종속변수는 대인신뢰 0~10 단일 문항. 독립변수는 선별 기관 접촉 수와 보편 기관 접촉 수, 통제변수 10개(단체 가입 포함). 매개 분석은 기관 이용자를 대상으로 공정 대우 지각과 신뢰의 관계를 확인</dd>
<dt>결과</dt><dd>선별 접촉 1곳당 −.26***, 보편 접촉 1곳당 +.07***(Table 5). 선별 접촉 0/1/2곳 이상의 평균 신뢰 6.7/6.0/5.7(Table 3). 기관 이용자 대상 분석에서 공정 대우 지각과 신뢰의 관계는 6개 기관 중 4개에서 유의(고용사무소는 p<.10)</dd>
<dt>한계</dt><dd>횡단면. "the opposite is always possible, especially when using nonexperimental data"(355)</dd></dl></div>''',
          "Table 1~7(351~358).",
          "마지막 논문입니다. 큰 복지국가는 사회자본을 밀어낸다는 통념이 있는데 스웨덴은 신뢰가 높습니다. 저자들은 복지국가의 규모보다 제도 유형을 봅니다. 욕구 심사를 거치는 선별 기관을 한 곳 더 접촉한 사람은 대인신뢰가 평균 0.26점 낮고, 누구나 이용하는 보편 기관은 한 곳당 0.07점 높습니다. 그리고 355쪽에서 자신들의 인과 해석이 틀렸을 가능성도 언제나 있다고 씁니다.")
    slide("Kumlin &amp; Rothstein (2005) 연구 질문과 논리 전개", "",
          '''<div class="ladder">
<div class="l">질문</div><div>복지국가가 호혜 관계와 결사체를 대체해 사회자본을 구축(crowding-out)한다면 스칸디나비아의 신뢰 수준이 높은 이유는 무엇인가. 저자들은 복지국가의 규모 대신 유형을 기준으로 삼는다</div><div class="q">"it is not how big a welfare state is but what type of welfare state one is dealing with" <i>343</i></div>
<div class="l">이론적 기대</div><div>절차공정성(Lind &amp; Tyler). 선별 급여는 자격 기준이 모호해 일선 관료(Lipsky)의 재량이 크고 신청자는 정보를 숨길 유인이 있어 불신의 악순환으로 이어지기 쉬움. 심리 기제 세 가지: 공무원에 대한 불신이 타인 일반에 대한 불신으로 확대, 급여를 받으려면 속여야 한다면 타인도 속일 것이라는 추론, 자신의 부정직한 행동에 근거한 타인에 대한 추론</div><div class="q">"a vicious spiral of distrust" <i>349</i></div>
<div class="l">설계 선택</div><div>1999년 서부 스웨덴 조사에 기관별 접촉 문항이 포함(350). 선별과 보편의 분류 기준은 욕구 심사를 거치는지 여부(348). 선별 7개 기관은 수급 자격 판단에 관료의 재량이 큰 곳으로 제시(350). 통제변수 10개(Table 5). 저자들은 지위 관련 변수 8개를 통제하고도 효과가 남은 것을 "tough empirical test"라 표현(355). 매개 분석은 기관 이용자만 대상</div><div class="q">"the minority who actually feel that they have been well treated … should demonstrate greater trust" <i>357</i></div>
<div class="l">결과</div><div>선별 −.26, 보편 +.07(Table 5). 제도 변수가 단체 참여(.09)보다 신뢰와 더 강하게 관련. 공정 대우 지각과 신뢰의 관계는 사회부조 .30** 등</div><div class="q">"the institutional welfare-state variables appear more strongly related to social trust than participation in voluntary organizations" <i>355</i></div>
<div class="l">결론</div><div>복지 제도는 유형에 따라 사회자본을 높이기도 하고 낮추기도 한다. 저자들은 1990년대 경제 위기로 선별 급여 수급이 늘어난 점을 우려한다. 결사체 참여는 신뢰의 원인보다 결과(symptom)일 가능성</div><div class="q">"such participation may be more a symptom of interpersonal trust than a cause" <i>362</i></div></div>''',
          "", "저자들이 스칸디나비아 퍼즐이라고 부른 질문입니다. 복지국가의 규모로는 설명되지 않아서 저자들은 제도 유형을 봅니다. 이론적 기대는 절차공정성 연구에서 가져옵니다. 욕구 심사를 거치는 기관에서는 일선 관료의 재량이 크고 신청자는 정보를 숨길 유인이 있습니다. 저자들은 이 경험이 타인 일반에 대한 불신으로 이어지는 심리 기제를 세 가지로 제시합니다. 결과 항목의 인용문에서 저자들은 제도 변수가 단체 참여보다 신뢰와 더 강하게 관련되는 것으로 보인다고 씁니다. 같은 문장에서 이 결과가 Putnam 이론의 예측과 반대라고 밝힙니다.")
    add_theory("05_kr", "Kumlin &amp; Rothstein (2005)")
    meas("Kumlin &amp; Rothstein (2005) 사회자본 측정", "344~356쪽", "kr_fig1", "Kumlin &amp; Rothstein 2005: 345, Figure 1과 신뢰 문항",
         [("독립변수", "선별 기관과 보편 기관 접촉 수. 선별은 욕구 심사를 거쳐 제공되는 서비스이고, 보편 급여의 예시에 아동수당이 포함(348)"),
          ("매개변수", "“받을 자격이 있는 서비스와 도움을 받았는가” 1~5점(356). 발제자 판단: 이론은 절차공정성인데 문항은 결과 평가에 가까움"),
          ("종속변수", "대인신뢰 한 문항. “According to your opinion, to what extent can people in general be trusted?” 0~10점(345, Table 3 주)"),
          ("분석 수준", "집계 수준의 상관만으로는 인과 기제를 알 수 없고 개인 수준의 근거가 필요하다고 봄(344~345). 신뢰만 본 이유를 따로 밝히지는 않음"),
          ("참여의 처리", "단체 가입 수(단체 유형 16개)를 통제변수로 투입(Table 5, .09***). Stolle(1998)의 패널 연구를 근거로 참여가 신뢰를 높인다는 인과를 의심(346)")],
         "Freitag은 신뢰를 통제변수로 두었고 이 논문은 참여를 통제변수로 둠. Putnam(2000, 3주차)은 복지국가를 사회자본 쇠퇴의 설명 후보 가운데 하나로 들었고, Fukuyama(2001: 18)는 국가가 시민사회의 일을 떠맡으면 사람들이 국가에 의존하게 된다고 보았다. 이 논문은 규모 대신 제도 유형을 구분",
         "왼쪽이 345쪽 Figure 1이고, 아래 주에 신뢰 문항이 있습니다. 제목은 사회자본인데 종속변수는 대인신뢰 한 문항입니다. 저자들은 집계 수준의 상관만으로는 인과 기제를 알 수 없다고 보고 개인 수준에서 분석합니다. 참여는 분석에서 통제변수로 들어갑니다. Freitag은 신뢰를 통제변수로 두었으니 두 논문의 선택이 반대입니다. 그리고 348쪽 보편 급여의 예시에 아동수당이 들어 있습니다. 다음 장의 토론 1에서 한국의 아동수당을 예로 여쭙겠습니다.")
    choice("복지 급여의 대상을 정할 때 무엇을 우선해야 한다고 생각하십니까?", "Kumlin &amp; Rothstein · 토론 1", "whynotboth",
          ["모두에게? 심사해서?", "신뢰도 따져 보면 안 되나요?"],
          ("선택 1. 심사 없이 모두에게 준다", "신청과 심사 절차가 줄고 받는 사람이 의심받지 않는다. 필요 없는 사람에게도 예산이 쓰인다"),
          ("선택 2. 심사해서 필요한 사람에게 준다", "같은 예산으로 필요한 사람에게 더 많이 줄 수 있다. 심사 과정에서 받는 사람이 의심과 재량을 경험한다"),
          "Kumlin &amp; Rothstein의 결과: 선별 기관 접촉이 한 곳 많은 사람은 대인신뢰가 0.26점 낮고, 보편 기관은 한 곳마다 0.07점 높았다(Table 5)", local,
          "다섯째 논문의 토론 1입니다. 복지 급여의 대상을 정할 때 무엇을 우선해야 하는지 여쭙겠습니다. 한국의 아동수당은 2018년 9월에 소득 하위 90%를 대상으로 시작했고 2019년 1월부터 소득 심사를 없앴습니다. Kumlin과 Rothstein의 결과로는 선별 기관을 접촉한 사람의 신뢰가 낮았습니다. 다만 응답자의 선별 기관 접촉은 평균 0.4곳 정도여서, 이 계수를 곱하면 표본 전체의 평균 신뢰 차이는 0.1점 남짓입니다. 이 숫자는 원문에 없는 제 계산입니다.")
    slide("Kumlin &amp; Rothstein (2005) 분석 결과", "Table 5 · 대인신뢰(0~10)에 대한 OLS, N=2,543",
          f'''<div class="res"><img class="shot" style="max-height:420px" src="{FIG["kr_t5"]}" alt="Table 5"><div><div class="k">접촉 한 곳당 신뢰 차이</div><div class="bars">
<span class="lab">선별 기관 접촉(0~2)</span><div class="b o" style="width:100%"></div><span class="v">−.26***</span>
<span class="lab">보편 기관 접촉(0~8)</span><div class="b" style="width:27%"></div><span class="v">+.07***</span>
<span class="lab">단체 가입 수(단체 유형 16개)</span><div class="b g" style="width:35%"></div><span class="v">+.09***</span>
<span class="lab">삶의 만족(1~4)</span><div class="b g" style="width:100%"></div><span class="v">+.63***</span></div>
<div class="k" style="margin-top:14px">Table 3 · 선별 접촉 수별 평균 신뢰</div><div class="bars">
<span class="lab">0곳 (n 2,411)</span><div class="b" style="width:100%"></div><span class="v">6.7</span>
<span class="lab">1곳 (n 829)</span><div class="b" style="width:90%"></div><span class="v">6.0</span>
<span class="lab">2곳 이상 (n 294)</span><div class="b" style="width:85%"></div><span class="v">5.7</span></div>
<p class="take">선별 기관 1곳 접촉의 계수는 보편 기관 약 4곳 접촉의 계수와 크기가 같다. 통제변수 중 계수가 가장 큰 변수는 삶의 만족이다.<small>유의수준 p&lt;.01 → 두 접촉 변수 모두 유의 · Adj R² .10 · 0곳과 1곳 집단의 차이(−.7)가 1곳과 2곳 이상 집단의 차이(−.3)보다 크다</small></p></div></div>''',
          "Kumlin &amp; Rothstein 2005: 352, 354. 비표준화 계수라 척도가 다른 변수끼리의 크기 비교는 참고용.",
          "원문 Table 5입니다. 선별 기관 접촉 한 곳당 −.26, 보편 기관 한 곳당 +.07입니다. 선별 기관 한 곳의 계수가 보편 기관 네 곳의 계수와 비슷한 크기입니다. 통제 중 가장 큰 것은 삶의 만족 .63인데, 저자들은 이 변수를 사회경제 요인이 신뢰에 영향을 미치는 경로 중 하나로만 다루고(355), 기관 접촉 경험의 결과일 가능성은 다루지 않았습니다. 아래 Table 3을 보면 0곳과 1곳 집단의 차이가 1곳과 2곳 이상 집단의 차이보다 큽니다. 접촉한 기관의 수보다 접촉 경험이 있는지가 더 중요할 가능성이 있습니다.")
    add_result2("05_kr", "Kumlin &amp; Rothstein (2005)")
    add_conclusion("05_kr", "Kumlin &amp; Rothstein (2005)")
    slide("Kumlin &amp; Rothstein (2005) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>횡단면. "the opposite is always possible, especially when using nonexperimental data"(355). 같은 문장의 앞부분은 "We obviously think that our causal interpretations are correct"</li><li>보편 접촉 6곳과 8곳 이상의 차이는 유의하지 않음(각주 5)</li><li>매개 문항은 절차를 "to a certain extent"만 측정(356)</li><li>매개 모형은 표본이 작아 통제변수 3개만 투입(각주 7)</li></ul><img class="shot" style="width:100%;max-height:none;margin-top:14px" src="{FIG["kr_355"]}" alt="355쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>선별 7개 중 4개(장애인 이동·장애연금·장애 돌봄·노인 돌봄)는 소득·자산 조사보다 건강·기능 상태 심사에 해당(348, 350). 건강 상태는 통제변수에 없다. 선별 접촉 효과의 일부는 건강 상태의 효과일 수 있다</li><li>Table 7에서 사회부조는 .30**이지만 주거수당은 −.02. 7개 기관을 합산한 계수 −.26이 어느 기관에서 비롯되는지는 제시되지 않았다</li><li>6개 기관 중 4개가 유의하다는 서술(357)에는 단서가 필요하다. 고용사무소 .13은 p&lt;.10, 보육 .12는 비유의</li><li>352쪽은 보편 접촉 0인 집단을 "majority"라고 서술했으나 실제 비율은 6%</li><li>제도 변수가 참여보다 강하게 관련된다는 서술(355)은 척도가 다른 비표준화 계수를 비교한 것이며 차이 검정은 없음</li><li>분석 자료는 서부 스웨덴 한 지역, 1999년 한 시점(350, 각주 1·2). Table 4의 평균 신뢰는 접촉 수에 따라 단조 증가하지 않는다</li></ul></div></div>''',
          "",
          "저자가 밝힌 한계의 첫 줄을 보십시오. 자신들의 인과 해석이 틀렸을 가능성은 언제나 있다고 썼습니다. 발제자의 추가 검토에서는 첫 줄을 말씀드리겠습니다. 선별 기관 7개 가운데 4개는 소득이나 자산보다 건강과 기능 상태를 심사합니다. 장애연금 수급자는 건강이 좋지 않을 가능성이 높은데, 건강 상태는 통제변수에 없습니다. 심리 기제 셋 가운데 둘은 급여를 받으려고 정보를 숨기거나 속이는 상황을 전제합니다. 장애연금 신청자에게도 그런 유인이 같은 정도로 있는지는 원문이 기관별로 나누어 다루지 않았습니다. 이 문제를 다음 장의 토론 2에서 여쭙겠습니다.")
    issue("신뢰가 낮은 사람이 선별 창구에 가는 것은 아닌가", "Kumlin &amp; Rothstein · 토론 2", "exit",
          ["선별 창구가 신뢰를 깎았다", "원래 못 믿던 사람이 창구에 갔다", "연구자 (355쪽: 반대일 가능성은 언제나 있다)"],
          ("찬 · 창구 경험이 신뢰를 낮춘다", "사회부조 이용자 가운데 받을 것을 제대로 받았다고 평가할수록 신뢰가 높았다(Table 7, .30)."),
          ("반 · 신뢰가 낮은 사람이 창구에 간다", "한 시점 자료이고, 선별 기관 7개 중 4개는 건강 상태를 심사하는데 건강은 통제되지 않았다."),
          "", local,
          "마지막 손들기입니다. 창구 경험이 신뢰를 낮췄다고 보시는 분, 신뢰가 낮은 사람이 창구에 갔다고 보시는 분. 저자들은 355쪽에서 자신들의 해석이 틀렸을 가능성도 있다고 썼습니다. 2부에서 각자 고를 자료에 이 문제를 가릴 변수가 있는지 보겠습니다.")

    # ───────── 엔딩 ─────────
    slide("지정문헌 종속변수 비교", "",
          '''<table><tr><th>논문</th><th>종속변수</th><th>출처</th><th>신뢰의 처리</th></tr>
<tr><td>Krishna</td><td>집합행동 성향 6문항 지수 0~100</td><td>944~946</td><td>지수 안의 한 문항</td></tr>
<tr><td>Freitag</td><td>결사체 4문항 주성분, 칸톤 평균</td><td>127, 각주 2</td><td>통제변수, 다변량에서 비유의</td></tr>
<tr><td>Lowndes &amp; Wilson</td><td>Putnam 혼합 정의 + 잠재/동원</td><td>630, 638</td><td>측정 없음</td></tr>
<tr><td>Mettler</td><td>단체 가입 수(4유형) + 정치참여 지표 6개</td><td>356</td><td>측정 없음</td></tr>
<tr><td>Kumlin &amp; Rothstein</td><td>대인신뢰 0~10 단일 문항</td><td>344~345, Figure 1</td><td>종속변수. 참여는 통제</td></tr></table>
<p class="take" style="margin-top:18px">결사체 참여를 종속변수로 둔 Freitag과 Mettler는 국가의 양(+)의 효과를, 대인신뢰를 종속변수로 둔 Kumlin &amp; Rothstein은 선별 제도의 음(−)의 효과를 보고했다.<small>Freitag의 다변량 분석에서 신뢰는 결사체 참여에 유의하지 않았다(Table 6 Model 4). Krishna는 Kumlin &amp; Rothstein을 인용했지만(943) 정부 신뢰의 효과는 유의하지 않았다(950).</small><small>한국의 아동수당은 2018년 9월 소득 하위 90% 대상으로 시작해 2019년 1월 소득 심사를 폐지했다. 같은 급여의 지급 방식이 선별에서 보편으로 바뀐 사례다.</small></p>''',
          "",
          "다섯 편의 종속변수를 한 표로 모았습니다. 넷째 열을 보시면 신뢰를 다룬 방식이 논문마다 다릅니다. 지수의 한 문항, 통제변수, 측정 없음, 측정 없음, 종속변수입니다. 결사체 참여를 종속변수로 둔 Freitag과 Mettler는 국가의 양의 효과를 보고했고, 대인신뢰를 종속변수로 둔 Kumlin과 Rothstein은 선별 제도의 음의 효과를 보고했습니다. 첫 논문 Krishna는 943쪽에서 Kumlin과 Rothstein을 인용했는데, 950쪽에서 정부 신뢰가 유의하지 않다고 보고했습니다. 두 연구는 종속변수와 분석 단위가 다르다는 점을 함께 보셔야 합니다. 그리고 Kumlin과 Rothstein은 355쪽에서 실험 자료를 쓴 후속 연구를 환영한다고 썼습니다. 한국의 아동수당은 2018년 9월에 소득 하위 90%를 대상으로 시작했고 2019년 1월부터 소득 심사를 없앴습니다. 같은 급여가 선별에서 보편으로 바뀐 사례이고, 2부에서 각자 국내 자료로 이어서 보겠습니다.")
    slide("주차별 주제와 11주차", "",
          '''<div class="two" style="grid-template-columns:1.2fr 1fr;align-items:start"><table style="font-size:14.5px"><tr><th>시기</th><th>연구 질문</th><th>이 강좌의 문헌</th></tr>
<tr><td>1960~1998</td><td>왜 합리적 개인은 협력하지 않는가</td><td>Olson, Hardin, Coase, Ostrom (2주)</td></tr>
<tr><td>1986~2001</td><td>협력을 가능하게 하는 자본은 무엇인가</td><td>Bourdieu, Coleman, Fukuyama, Putnam (3주)</td></tr>
<tr><td>1973~1999</td><td>관계 구조에서 자원의 위치</td><td>Granovetter, Burt, Lin (5주)</td></tr>
<tr><td>2002~2008</td><td>형성 요인: 문화, 개인 투자, 지역, 결사체</td><td>Guiso, Glaeser, Rupasingha, Wollebaek &amp; Selle (4주)</td></tr>
<tr><td>1997~2026</td><td>사회자본의 효과</td><td>Paxton, Boix &amp; Posner, Tavits, Knack, Knack &amp; Keefer (6~10주)</td></tr>
<tr style="background:var(--greent)"><td>2001~2007</td><td><b>국가는 사회자본을 형성하는가</b></td><td><b>Krishna, Freitag, Lowndes &amp; Wilson, Mettler, Kumlin &amp; Rothstein (11주)</b></td></tr>
<tr><td>1995~2007</td><td>신뢰는 사회자본과 같은가</td><td>Mayer, Rousseau, Hardin, Tyler, Keele (12~13주)</td></tr>
<tr><td>2000~2021</td><td>누구의 사회자본인가</td><td>Putnam 22장, Compton &amp; Meier, Gidengil (14주)</td></tr></table>
<div><div class="quote" style="font-size:15.5px">"두 개념(집단 지향과 개인 지향)은 문헌에 둘 다 있지만, 둘 사이에 다리가 놓인 적이 없고, 같은 개념을 가리키는지도 분명치 않다."<small>Krishna 2007: 942, 각주 2 (발제자 번역)</small></div><p style="font-size:15px;margin-top:14px;line-height:1.6">발제자가 보기에 11주차 지정문헌 5편은 모두 집단 수준의 사회자본 논의(Putnam 계열)에 속한다. 12~13주차 문헌은 그중 신뢰를 따로 다루고, 14주차 문헌은 사회자본의 분배를 다룬다. 신뢰를 다룬 토론 4·9·10은 12~13주차 주제와 이어진다.</p></div></div>''',
          "",
          "2주차부터 14주차까지의 주제를 한 표로 모았습니다. 초록 줄이 11주차입니다. 2주차 질문에서 시작해 3주차에 이름이 붙고, 6주차부터 원인으로 다뤘던 사회자본을 오늘은 4주차에 이어 다시 결과로 놓았고, 이번에는 원인이 국가입니다. 다음 주부터는 그 안에서 신뢰만 떼어 묻습니다. 오늘 토론 가운데 신뢰를 다룬 셋이 그 주제로 이어집니다.")
    raw(f'''<section class="slide cover">{f'<img src="{PHOTO["landsgemeinde"]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55">' if "landsgemeinde" in PHOTO else ""}<div style="position:absolute;inset:0;background:rgba(7,42,96,.55)"></div><div class="c" style="position:absolute"><h1>감사합니다</h1><p class="sub">긴 발표를 들어 주시고 토론에 참여해 주셔서 감사합니다.</p></div><div class="meta">사회자본과 공공정책 · 11주차 발제 · 오지환(석사과정 2학기)</div>{f'<div style="position:absolute;right:40px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:600px;text-align:right">{PCRED["landsgemeinde"]}</div>' if "landsgemeinde" in PCRED else ""}
<aside class="notes">긴 발표를 들어 주시고 토론에 참여해 주셔서 감사합니다. 1부는 여기까지입니다.</aside></section>''')
    # ───────── 부록 ─────────
    for t, sub, key, cap in [("Krishna Table 2 원문", "949쪽", "krishna_t2", "N 61/60, R² .23/.79"), ("Freitag Table 7 원문", "142쪽 · 공선 변수를 분리한 네 모형", "freitag_t7", "M1 제도 변수 3개 R² .75 · M2 도시화·언어권 .79 · M3 직접민주주의·도시화 .77 · M4 합의·지방자치·언어권 .78"),
                             ("Mettler Table 7 원문", "362쪽 · 정치참여, 생활수준 × 이용 상호작용", "mettler_t7", "생활수준 최하 .17(.57) · 중하 .40(.03) · 중간 .27(.13) · 중상·상 1.22(.00)"), ("Kumlin &amp; Rothstein Table 3 원문", "352쪽 · 선별 접촉 수별 평균 신뢰", "kr_t3", "0/1/2+ → 6.7/6.0/5.7, r=−.14"),
                             ("Kumlin &amp; Rothstein Table 7 원문", "358쪽 · 기관별 이용자 안에서 공정 대우 지각 → 신뢰", "kr_t7", "보건 .31*** · 보육 .12 · 교통 .27*** · 사회부조 .30** · 고용 .13* · 주거수당 −.02")]:
        slide(t, sub, f'<div style="display:flex;justify-content:center;height:470px"><img class="shot" src="{FIG[key]}" alt="{t}"></div>', cap, "", ap=True)

    html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>국가는 사회자본을 만들 수 있는가</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"><script>function noimg(m){{const w=m.closest('.mw');w.style.display='none';w.nextElementSibling.style.display='grid';}}</script><style>{face(''.join(h for h, _ in S) + '국가는 사회자본을 만들 수 있는가 ←/→ 이동 · N 노트 · F 전체화면 노트 없음 A0123456789')}{CSS.replace('__FAMILY__', FAMILY)}</style></head><body><div id="stage">
{"".join(h for h, _ in S)}
</div><div id="notes"></div><div id="help">←/→ 이동 · N 노트 · F 전체화면</div>
<script>
const S=[...document.querySelectorAll('.slide')];let i=0;const N=document.getElementById('notes');
function fit(){{const sc=Math.min(innerWidth/1280,innerHeight/720);S.forEach(s=>s.style.transform=`scale(${{sc}})`);}}
function grow(s){{const bd=s.querySelector('.bd'),n=s.querySelector('.in');if(!bd||!n||n.dataset.z||s.querySelector('.map')||document.readyState!=='complete')return;let z=1.3;for(;z>1.001;z-=.05){{n.style.zoom=z;if(n.getBoundingClientRect().height<=bd.getBoundingClientRect().height&&n.scrollWidth<=n.clientWidth+1)break;}}z=Math.max(1,z);n.style.zoom=z;const fits=()=>n.getBoundingClientRect().height<=bd.getBoundingClientRect().height&&n.scrollWidth<=n.clientWidth+1;for(;!fits()&&z>.76;z-=.03)n.style.zoom=z-.03;n.dataset.z=n.style.zoom;}}
function show(k){{i=Math.max(0,Math.min(S.length-1,k));S.forEach((s,j)=>s.classList.toggle('on',j===i));grow(S[i]);N.innerHTML=(S[i].querySelector('.notes')||{{}}).innerHTML||'<i>노트 없음</i>';location.hash=i+1;}}
let main=0,ap=0;S.forEach(s=>{{const p=document.createElement('div');p.className='pg';if(s.dataset.ap){{p.textContent='A'+(++ap);}}else{{main++;if(!s.classList.contains('cover'))p.textContent=main;}}s.appendChild(p);}});
addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown')show(i+1);else if(e.key==='ArrowLeft'||e.key==='PageUp')show(i-1);else if(e.key.toLowerCase()==='n')N.classList.toggle('on');else if(e.key.toLowerCase()==='f'){{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}}}});
addEventListener('load',()=>{{document.querySelectorAll('.mw img').forEach(m=>{{if(!m.naturalWidth)noimg(m);}});show(i);}});
addEventListener('click',e=>{{if(e.target.closest('#notes'))return;if(e.target.classList.contains('ck')){{e.target.textContent=e.target.textContent==='□'?'■':'□';return;}}show(i+(e.clientX>innerWidth/2?1:-1));}});
addEventListener('resize',fit);fit();show((+location.hash.slice(1)||1)-1);
</script></body></html>'''
    return html


for local, name in ((False, "week11_part1.html"), (True, "week11_part1_local.html")):
    out = build(local); open(os.path.join(H, name), "w", encoding="utf-8").write(out); print(name, len(out) // 1024, "KB", len(S), "장")
