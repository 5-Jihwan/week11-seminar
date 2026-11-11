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
PLAY = {}  # Ji의 80억 분의 1 플레이 화면. deck/play/*.jpg|png 가 있으면 3장 인트로에 넣는다
pd = os.path.join(H, "play")
if os.path.isdir(pd):
    for f in sorted(os.listdir(pd)):
        if f.lower().endswith((".jpg", ".jpeg", ".png")): PLAY[f] = uri(os.path.join(pd, f), 1200, 80)

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
.pc{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:12px;font-size:15.5px;line-height:1.5}.pc b{display:block;color:var(--navy);font-size:15px;margin-bottom:3px}
.iq{margin-top:10px;font-size:19px;color:var(--navy);font-weight:600;line-height:1.4}
/* 한 줄과 다리 */
.bridge .one{font-size:30px;line-height:1.45;font-weight:600;color:var(--navy);padding:22px 28px;border-left:4px solid var(--green);background:var(--greent)}.bridge .next{margin-top:26px;font-size:17px;line-height:1.65;color:var(--ink)}
/* 인트로·엔딩 */
.stat{display:grid;grid-template-columns:repeat(3,1fr);gap:36px;text-align:center}.stat .v{font-family:"IBM Plex Mono",monospace;font-size:84px;line-height:1;color:var(--navy);font-weight:500}.stat .l{font-size:16.5px;color:var(--sub);margin-top:14px;line-height:1.5}
.quote{border-left:4px solid var(--navy);padding:12px 18px;font-size:19px;line-height:1.6;color:var(--ink);background:#fafbfd}.quote small{display:block;color:var(--sub);font-size:13px;margin-top:8px}
table{border-collapse:collapse;width:100%;font-size:15.5px;line-height:1.4}th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:13px;color:var(--navy);font-weight:600;background:var(--navyt);border-bottom:1px solid var(--navy7)}td.r,th.r{text-align:right;white-space:nowrap}.photo{background:#0b1a33}.photo img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.photo .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,42,96,.35),rgba(7,42,96,.82))}.photo .c{position:absolute;left:88px;right:88px;bottom:96px;color:#fff}.photo .c::before{content:"";display:block;width:40px;height:4px;background:var(--green);margin-bottom:22px}.photo .one{font-size:36px;line-height:1.4;font-weight:700}.photo .one small{display:block;font-size:17px;font-weight:400;opacity:.85;margin-top:8px}.photo .next{margin-top:22px;font-size:16.5px;line-height:1.65;opacity:.95;max-width:1000px}.photo .cr{position:absolute;right:40px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:720px;text-align:right}.photo .pg{color:rgba(255,255,255,.6)}
.map{position:relative;height:430px;border-left:1px solid var(--line);border-bottom:1px solid var(--line)}.map .pt{position:absolute;width:14px;height:14px;border-radius:50%;background:var(--navy);transform:translate(-50%,-50%)}.map .lb{position:absolute;font-size:14px;line-height:1.35;transform:translate(10px,-50%)}.map .lb b{color:var(--navy);display:block;font-size:14.5px}.map .ax{position:absolute;font-size:12.5px;color:var(--sub)}
.steps{counter-reset:s}.steps li{list-style:none;position:relative;padding-left:30px;font-size:17px;margin-top:9px}.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:4px;width:20px;height:20px;border-radius:50%;background:var(--navy);color:#fff;font-size:11px;display:grid;place-items:center}
.play{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.play img{width:100%;border:1px solid var(--line);border-radius:4px}.play .ph{height:240px;border:1px dashed var(--gray);border-radius:4px;display:grid;place-items:center;color:var(--sub);font-size:14px;text-align:center;padding:12px}
#help{position:fixed;right:14px;top:10px;font-size:12px;color:#7b8494;z-index:6}:root:fullscreen #help{display:none}td.ck{cursor:pointer;text-align:center}
"""

S = []  # (html, notes, appendix?)


def slide(title, sub, body, cap="", notes="", ap=False, cls=""):
    S.append((f'<section class="slide {cls}" {"data-ap=1" if ap else ""}><div class="hd"><h2>{title}</h2>{f"<p class=s>{sub}</p>" if sub else ""}</div><div class="bd"><div class="in">{body}</div></div>{f"<div class=cap>{cap}</div>" if cap else ""}<aside class="notes">{notes}</aside></section>', None))


def photo(key, one, small, bridge, notes, title=""):
    img = f'<img class="bg" src="{PHOTO[key]}" alt="">' if key in PHOTO else ""
    cr = f'<div class="cr">{PCRED[key]}</div>' if key in PCRED else ""
    S.append((f'<section class="slide photo">{img}<div class="veil"></div><div class="c">{f"<div style=font-size:14px;opacity:.8;margin-bottom:10px>{title}</div>" if title else ""}<div class="one">{one}<small>{small}</small></div><p class="next">{bridge}</p></div>{cr}<aside class="notes">{notes}</aside></section>', None))


MCHAIN = {"krishna_items": 4, "freitag_meas": 3, "lw_latent": 3, "kr_fig1": 3}  # 캡처별: 앞에서 몇 행이 순서(개념→문항→지수, 독립→매개→종속)인가


def meas(title, sub, fig, figcap, rows, cmp_, notes):
    """측정 장: 왼쪽에 원문 캡처, 오른쪽에 개념에서 지수까지의 단계와 앞 주차 문헌 비교."""
    r = "".join(f'<div class="l{" f" if i < MCHAIN.get(fig, 0) - 1 else ""}">{l}</div><div>{t}</div>' for i, (l, t) in enumerate(rows))
    slide(title, sub, f'<div class="meas"><figure><img class="shot" src="{FIG[fig]}" alt="{figcap}"><figcaption>{figcap}</figcaption></figure><div><div class="mrows">{r}</div><div class="mcmp"><b>앞 주차 문헌</b>{cmp_}</div></div></div>', "", notes)


def raw(html):
    S.append((html, None))


def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# 캡션 좌표: 템플릿별 (위치 %, 폭 %)
MPOS = {"pigeon": [("top:7%;left:56%;width:40%",), ("top:34%;left:3%;width:42%",), ("bottom:5%;left:8%;width:84%;text-align:center",)],
        "buttons": [("top:8%;left:12%;width:30%",), ("top:4%;left:46%;width:32%",), ("bottom:6%;left:18%;width:64%;text-align:center",)],
        "drake": [("top:10%;left:52%;width:46%",), ("top:60%;left:52%;width:46%",)],
        "boyfriend": [("top:48%;left:20%;width:26%",), ("top:34%;left:50%;width:22%",), ("top:38%;left:75%;width:23%",)],
        "brain": [("top:3%;left:2%;width:46%",), ("top:28%;left:2%;width:46%",), ("top:53%;left:2%;width:46%",), ("top:78%;left:2%;width:46%",)],
        "fine": [("top:5%;left:6%;width:88%;text-align:center",), ("bottom:6%;left:6%;width:88%;text-align:center",)],
        "gru": [("top:6%;left:3%;width:42%",), ("top:6%;left:53%;width:42%",), ("top:56%;left:3%;width:42%",), ("top:56%;left:53%;width:42%",)],
        "handshake": [("bottom:8%;left:2%;width:32%",), ("bottom:8%;right:2%;width:32%;text-align:right",), ("top:12%;left:30%;width:40%;text-align:center",)],
        "whynotboth": [("top:5%;left:6%;width:88%;text-align:center",), ("bottom:6%;left:6%;width:88%;text-align:center",)],
        "exit": [("top:5%;left:8%;width:34%",), ("top:5%;left:52%;width:34%",), ("bottom:8%;left:20%;width:60%;text-align:center",)]}
MNAME = {"pigeon": "이게 비둘기인가요?", "buttons": "두 버튼", "drake": "드레이크", "boyfriend": "딴 데 보는 남자친구", "brain": "확장하는 뇌", "fine": "불타는 방의 개", "gru": "그루의 계획", "handshake": "두 팔 악수", "whynotboth": "둘 다 하면 안 돼요?", "exit": "고속도로 출구"}


# 공개판은 그림 파일을 저장소에 넣지 않고 imgflip 주소에서 불러온다. 안 열리면(오프라인) 캡션 카드가 대신 보인다
MURL = {"pigeon": "Is-This-A-Pigeon", "brain": "Expanding-Brain", "buttons": "Two-Buttons", "drake": "Drake-Hotline-Bling", "fine": "This-Is-Fine", "gru": "Grus-Plan",
        "handshake": "Epic-Handshake", "boyfriend": "Distracted-Boyfriend", "whynotboth": "Why-Not-Both", "exit": "Left-Exit-12-Off-Ramp"}


def issue(title, sub, meme, caps, pro, con, q, local, notes):
    card = f'<div class="card2"><div style="grid-column:1/3"><div class="t">{MNAME[meme]} 형식 · 캡션</div></div>' + "".join(f'<div><div class="t">{["①","②","③","④"][i]}</div><div class="m">{esc(c)}</div></div>' for i, c in enumerate(caps)) + '</div>'
    has = meme in MASP
    if has:
        img = f'<img src="{MEME[meme]}" alt="" style="object-fit:fill">' if local else f'<img src="https://imgflip.com/s/meme/{MURL[meme]}.jpg" alt="" style="object-fit:fill" referrerpolicy="no-referrer" onerror="noimg(this)">'
        w = min(1136, int(300 * MASP[meme])); fs = 21 if w >= 700 else 16 if w >= 480 else 13
        dark = meme in ("drake", "gru", "whynotboth")  # 밝은 바탕 템플릿은 남색 글자
        over = "".join(f'<div class="mc" style="{MPOS[meme][i][0]};font-size:{fs}px;{"color:#15203a;text-shadow:0 0 4px #fff,0 0 2px #fff,1px 1px 0 #fff" if dark else ""}">{esc(c)}</div>' for i, c in enumerate(caps))
        if MASP[meme] < 0.95:  # 세로로 긴 템플릿: 그림 왼쪽, 캡션은 오른쪽에 순서대로
            fig = f'<div style="display:flex;gap:22px;align-items:center;justify-content:center;height:300px"><div class="fig" style="width:{w}px;height:300px">{img}</div><ol style="font-size:16.5px;line-height:1.5;max-width:560px">' + "".join(f"<li>{esc(c)}</li>" for c in caps) + "</ol></div>"
        else:
            fig = f'<div class="fig" style="width:{w}px;margin:0 auto">{img}{over}</div>'
        if not local: fig = f'<div class="mw">{fig}</div>' + card.replace('<div class="card2">', '<div class="card2" style="display:none">', 1)
    else:
        fig = card
    body = f'<div class="issue">{fig}<div class="pc"><div><b>{pro[0]}</b>{pro[1]}</div><div><b>{con[0]}</b>{con[1]}</div></div><div class="iq">{q}</div></div>'
    credit = ("밈 템플릿: imgflip 공개 템플릿, 수업 내부용 · " if local else "밈 템플릿: imgflip · ") if has else ""
    S.append((f'<section class="slide"><div class="hd"><h2>{title}</h2><p class="s">{sub}</p></div>{body}<div class="cap">{credit}토론 2분 30초 · 지명 1명 + 자유 1~2명</div><aside class="notes">{notes}</aside></section>', None))


def build(local):
    S.clear()
    # ───────── 인트로 ─────────
    raw(f'''<section class="slide cover">{f'<img src="{PHOTO["landsgemeinde"]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55">' if "landsgemeinde" in PHOTO else ""}<div style="position:absolute;inset:0;background:rgba(7,42,96,.55)"></div><div class="c" style="position:absolute"><h1>국가는 사회자본을 만들 수 있는가</h1><p class="sub">Social Capital as Dependent Variable · 11주차 발제<br>Krishna 2007 · Freitag 2006 · Lowndes &amp; Wilson 2001 · Mettler 2002 · Kumlin &amp; Rothstein 2005</p></div><div class="meta">사회자본과 공공정책 · 2026-11-13 · 발제 오지환(석사과정 2학기) · 성균관대학교</div>{f'<div style="position:absolute;right:40px;bottom:26px;font-size:11px;color:rgba(255,255,255,.65);max-width:600px;text-align:right">{PCRED["landsgemeinde"]}</div>' if "landsgemeinde" in PCRED else ""}
<aside class="notes">안녕하십니까. 11주차 「국가는 사회자본을 만들 수 있는가」 세미나를 맡은 석사과정 2학기 오지환입니다. 오늘 주제는 Social Capital as Dependent Variable, 사회자본을 결과로 놓는 연구들입니다.</aside></section>''')
    play_html = '<div class="play">' + ("".join(f'<img src="{v}" alt="">' for v in list(PLAY.values())[:3]) if PLAY else '<div class="ph">플레이 화면 1<br>출생 카드</div><div class="ph">플레이 화면 2<br>관계 수치가 보이는 선택 장면</div><div class="ph">플레이 화면 3<br>생애 요약 카드</div>') + '</div>'
    slide("80억 분의 1", "172개국 실제 통계로 한 사람의 삶을 사는 시뮬레이션 (1in8b.life)",
          play_html + '''<div class="two" style="margin-top:12px;align-items:start"><ul style="font-size:14.5px"><li>고를 수 있는 것은 태어날 해뿐. 나라는 그해 출생아 수의 확률로, 가정은 그 나라 소득분포의 확률로 정해진다</li><li>반영 통계: 출생아 수, 성별 기대수명, 영아 사망률, 소득 불평등 지수, 교육 접근성, 대학 진학률, 살인율, 흡연율, 조혼율. 전쟁·팬데믹 같은 사건도 실제 확률로</li><li>두 살부터 기질·활동·진학·진로·지출을 고르고 건강·행복·지식·관계·소득이 숫자로 따라온다. 끝나면 생애 기록</li></ul>
<div class="quote" style="font-size:15px">"우리 누구도 태어날 곳을 고르지 않았다. 원하는 나라가 나올 때까지 다시 했다는 반응은 오히려 이 시뮬레이션이 보여주려던 것과 닿아 있다. 태어난 곳이 삶을 얼마나 크게 바꾸는지 알기 때문에 다시 누르는 거니까. 현실에서는 그 버튼이 없다."<small>개발자 진휘어스 인터뷰, 한겨레21 1637호(2026-10-29) 재인용</small></div></div>''',
          "한겨레21 1637호 「다시 태어나면 어디서 누구로 살고 싶은가… '80억 분의 1' 게임으로 오라」(2026-10-29). 한국인 개발자, 2026-10-07 출시, 무료.",
          "본격적으로 들어가기 전에 하나 여쭙겠습니다. '80억 분의 1'이라는 게임을 해 보셨거나 들어 보신 분 계십니까. 172개국 통계로 한 사람의 일생을 무작위로 사는 시뮬레이션입니다. 고를 수 있는 건 태어날 해뿐입니다. 저는 남양주에서 등교하는 길에 논문도 뉴스도 보기 싫을 때 이걸 합니다. 제 연구가 재미없어질 때도 합니다. 도피입니다. 화면의 삶은 제가 지난주에 산 삶입니다. 처음에는 그냥 선택지 중 하나였던 '관계' 수치가, 사회자본을 공부하고 논문을 쓰면서 다르게 보이기 시작했습니다. 이 수치는 무엇 때문에 오르내리는가. 이 게임을 만든 사람은 한국인 개발자입니다. 출시 뒤 가장 많이 받은 요청이 '태어날 나라를 고르게 해 달라'였답니다. 개발자의 답이 화면의 인용입니다.")
    slide("지정문헌이 다루는 선택", "모임 가입, 이사, 공청회 참석, 급여 신청, 복지 창구 방문",
          '''<div class="two" style="grid-template-columns:1fr 1.2fr"><div class="quote" style="font-size:17px">"'80억 분의 1'의 선택은 통계에 기반을 둬 설계됐다는 점에서, 그리고 선택의 결과가 수치로 명확하게 표현된다는 점에서 실제 우리 인생과 다르다. (…) 우리는 특정한 결과를 짐작하며 무언가를 선택하지만, 현실에서 짐작은 종종 빗나간다. 선택을 통해 얻은 것이 정확히 무엇인지도 바로 알기 어렵다."<small>한겨레21 1637호 기사 본문</small></div>
<div><div class="k">논문별 선택과 종속변수</div><table style="font-size:15.5px"><tr><th>선택</th><th>논문</th><th>종속변수</th></tr>
<tr><td>친구가 만든 모임에 가입했다</td><td>Krishna</td><td>마을의 협력 기대</td></tr><tr><td>주민투표를 하기 쉬운 지역으로 이사했다</td><td>Freitag</td><td>결사체 참여</td></tr><tr><td>구청 공청회에 갔지만 답장은 없었다</td><td>Lowndes &amp; Wilson</td><td>(측정 없음)</td></tr><tr><td>신청서 한 장으로 등록금을 받았다</td><td>Mettler</td><td>단체 가입 · 정치참여</td></tr><tr><td>복지 창구에서 서류 넷을 내고 한 달을 기다렸다</td><td>Kumlin &amp; Rothstein</td><td>대인신뢰 0~10</td></tr></table></div></div>''',
          "",
          "한겨레21 기사는 이 게임과 현실의 차이를 이렇게 정리했습니다. 게임에서는 선택의 결과가 숫자로 바로 나오지만, 현실에서는 내 선택이 무엇을 바꿨는지 바로 알기 어렵습니다. 오늘 읽을 다섯 편은 그 결과를 숫자로 재려고 한 연구입니다. 오른쪽 표에 논문마다 다룬 선택과 종속변수를 적었습니다. 논문이 끝날 때마다 이 표의 해당 줄을 다시 보겠습니다.")
    slide("연구 대상과 분석 단위", "발제 순서: 원인을 사회 내부에서 찾은 연구부터 국가와 개인의 접촉을 다룬 연구까지",
          '''<div class="two" style="grid-template-columns:1.3fr 1fr"><div class="map">
<div class="pt" style="left:12%;top:82%"></div><div class="lb" style="left:12%;top:82%"><b>Krishna 2007</b>마을 내부의 자생 조직 · 규칙 · 신진 리더<br>인도 61개 마을, 7년 패널</div>
<div class="pt" style="left:30%;top:64%"></div><div class="lb" style="left:30%;top:64%"><b>Freitag 2006</b>칸톤의 정치제도<br>스위스 24개 칸톤</div>
<div class="pt" style="left:48%;top:46%"></div><div class="lb" style="left:48%;top:46%"><b>Lowndes &amp; Wilson 2001</b>지방정부 제도 설계의 네 차원<br>영국, 실증 없음</div>
<div class="pt" style="left:62%;top:28%"></div><div class="lb" style="left:62%;top:28%"><b>Mettler 2002</b>정책 하나의 집행 방식<br>미국 참전자 716명, 회고 설문</div>
<div class="pt" style="left:72%;top:10%"></div><div class="lb" style="left:72%;top:10%"><b>Kumlin &amp; Rothstein 2005</b>복지 창구 접촉의 공정성<br>스웨덴 서부 2,543명</div>
<div class="ax" style="left:0;bottom:-22px">← 사회 내부</div><div class="ax" style="right:0;bottom:-22px">국가와 개인의 접촉 →</div><div class="ax" style="left:-4px;top:-20px">개인</div><div class="ax" style="left:-4px;bottom:0">집합</div></div>
<div><div class="k">2~10주차와의 관계</div><ul style="font-size:15px"><li>6~10주차: 사회자본 → 민주주의(Paxton), 정부 성과(Knack 2002, Tavits), 성장(Knack &amp; Keefer)</li><li>4주차 형성 논문들이 원인을 물었지만 문화(Guiso), 개인 투자(Glaeser), 인구 구성(Rupasingha)이었다</li><li>지정문헌 5편은 국가를 원인으로 둔다. Freitag 125쪽의 구분으로는 사회자본을 외생으로 두는 접근(Putnam 1993)과 달리 내생으로 두는 접근(Levi 1996 · Tarrow 1996 · Skocpol 2000)에 해당</li></ul><div class="quote" style="font-size:14.5px;margin-top:14px">"The second approach endogenizes social capital as an outcome of social and political arrangements"<small>Freitag 2006: 125</small></div></div></div>''',
          "점의 위치는 발제자 배치. 세로축은 종속변수의 단위(마을·칸톤 평균 → 개인), 가로축은 원인 변수(사회 내부 → 국가).",
          "10주차까지 사회자본은 독립변수였습니다. 6주차부터 10주차까지 민주주의, 정부 성과, 경제 성장을 설명했습니다. 오늘 다섯 편에서는 국가가 독립변수이고 사회자본이 종속변수입니다. 그림의 점은 왼쪽 아래에서 오른쪽 위로 갑니다. 원인 변수가 마을 내부에서 복지 창구로 바뀌고, 분석 단위는 마을 평균에서 개인으로 내려옵니다. 첫 논문은 같은 제도 아래 있는 인도 라자스탄 61개 마을을 7년 동안 본 연구입니다. 제도가 같은데 마을마다 사회자본이 다르게 변했다면 무엇이 달랐을까요.")

    # ───────── 1 Krishna ─────────
    slide("Krishna (2007) 연구 개요", "How Does Social Capital Grow? A Seven-Year Study of Villages in India · <i>Journal of Politics</i> 69(4)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["krishna_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>사회자본이 7년 안에 움직이는가. 움직인다면 무엇이 움직이는가</dd>
<dt>자료</dt><dd>라자스탄 5개 구 61개 마을. 1997년 2,291명 → 2004년 1,731명 재면접(76%). 9개 마을 사례연구</dd>
<dt>설계</dt><dd>마을 단위 OLS. 종속 = 2004년 집합행동 성향 6문항 지수(0~100). 독립은 모두 1997년 측정(자생 조직 가입만 7년 증가분)</dd>
<dt>결과</dt><dd>평균 58.4 → 59.7. 33개 마을 상승·28개 하락. 유의한 원인은 자생 조직 17.57*, 규칙 3.77*(p&lt;.001), 신진 리더 5.59*(p&lt;.01), 토지 불평등 −.13*. 정부 신뢰·정부 조직·NGO 조직은 비유의</dd>
<dt>한계</dt><dd>같은 주 제도 아래라 제도 설계 효과는 검증 불가(950). 교육 같은 장기 효과는 7년에 안 보임(각주 19)</dd></dl></div>''',
          "수치는 Table 2(949).",
          "Krishna의 질문은 하나입니다. Putnam이 역사가 정한다고 한 사회자본이 7년 안에 움직이는가. 라자스탄 61개 마을을 1997년과 2004년에 두 번 쟀습니다. 평균은 거의 그대로인데 마을은 움직였습니다. 33개가 오르고 28개가 내렸습니다. 올린 것은 마을 안에서 나온 것들이었습니다. 주민이 만든 조직, 규칙, 새 리더. 정부가 만든 조직과 정부에 대한 신뢰는 아무 상관이 없었습니다.")
    slide("Krishna (2007) 연구 질문과 가설", "",
          '''<div class="ladder">
<div class="l">질문</div><div>Putnam(1993)은 사회자본이 정부 성과를 정한다면서 그 자체는 키울 수 없다고 했다. 그렇다면 왜 중요한가. 단기에 움직이는가</div><div class="q">"Putnam (1993) presents us with a nagging conundrum" <i>941</i></div>
<div class="l">이론적 기대</div><div>가설 다섯 묶음을 비관에서 낙관 순으로. 역사 의존(Putnam) · 제도 부산물(Rothstein 2001, Kumlin &amp; Rothstein 2005) · 집단 특성(Boix &amp; Posner 분열, Olson 규모) · 집단 행동(Ostrom 규칙, Oliver 리더) · 외부 개입(World Bank)</div><div class="q">"Different pathways, corresponding to different degrees of optimism" <i>943</i></div>
<div class="l">설계 선택</div><div>패널: 횡단면은 원인과 결과를 못 가른다. 마을 단위: 각주 2에서 집단 지향 개념만 다룬다고 선언. 회원 수 대신 6문항: 공식 조직 가입률 2% 미만, 거의 전부 정부 산물</div><div class="q">"Density of formal organizations is a particularly inappropriate indicator" <i>945</i></div>
<div class="l">결과</div><div>1997년 지수만으로 R² .23, 열여섯 변수로 .79. 유의한 것은 넷. 가장 비관적인 두 가설(역사·제도 부산물)과 가장 낙관적인 가설(외부 개입)이 함께 기각</div><div class="q">"only four variables are found significantly associated with higher gains" <i>952</i></div>
<div class="l">결론</div><div>사회자본은 안에서 만들어진다. 외부 기관은 불평등 완화·자기조직화 조건·리더 육성으로 간접·장기로만</div><div class="q">"External agencies cannot directly raise social capital." <i>954</i></div></div>''',
          "", "다섯 단으로 읽겠습니다. 질문은 Putnam의 모순에서 나옵니다. 가설은 다섯 묶음인데 비관에서 낙관 순으로 늘어놓은 점이 이 논문의 설계입니다. 어느 묶음이 살아남느냐가 곧 답입니다. 설계에서 눈여겨볼 것은 회원 수를 버린 선택입니다. 가입률 2%짜리 사회에서 Putnam의 지표는 못 씁니다. 결과는 가운데 묶음만 살았습니다. 가장 비관적인 쪽도, 가장 낙관적인 쪽도 떨어졌습니다.")
    meas("Krishna (2007) 사회자본 측정", "945~946쪽", "krishna_items", "Krishna 2007: 945. 문항 1~3(구조적 차원). 문항 4~6은 945~946쪽",
         [("개념적 정의", "Putnam(1995)의 정의를 따름. “networks, norms and social trust that facilitate coordination and cooperation”(942)"),
          ("구성 차원", "Uphoff의 구분을 적용. 구조적 차원은 연결망·역할·규칙·선례, 인지적 차원은 규범·가치·태도·믿음(945)"),
          ("측정 문항", "구조적 차원 3문항(병충해 공동 대응, 공유지 관리, 분쟁 해결)과 인지적 차원 3문항(호혜, 연대, 신뢰). 여섯 문항 모두 마을 사람들이 어떻게 행동할지를 물음"),
          ("지수 구성", "주성분 분석에서 단일 요인(분산의 55%), α .86. 여섯 문항을 같은 가중치로 합산해 0~100점으로 변환(각주 13)")],
         "Ostrom(1998, 2주차)은 신뢰를 타인의 행동에 대한 기대로 정의했고, 신뢰 문항(6번)이 같은 방식으로 물음. Dasgupta(2000, 9주차)는 믿음·규칙·연결망을 하나의 지수로 합산하는 데 반대(p.327)",
         "왼쪽이 945쪽 설문 문항 원문입니다. 저자는 Putnam의 정의를 따르고, Uphoff의 구분에 맞춰 구조적 차원과 인지적 차원을 세 문항씩 만들었습니다. 여섯 문항 모두 누가 나설 것 같은가를 묻습니다. 응답자 자신의 신뢰보다 마을 사람들의 행동에 대한 예상을 잰 셈입니다. 2주차 Ostrom이 신뢰를 타인의 행동에 대한 기대로 정의한 것과 같은 방식입니다. 다만 9주차 Dasgupta는 믿음과 규칙과 연결망을 한 지수로 합치는 데 반대했습니다. 이 점이 첫 쟁점과 이어집니다.")
    issue("정부가 만든 모임은 사회자본을 못 키우는가", "Krishna · 쟁점 1", "pigeon",
          ["정부가 세운 청년회", "Putnam", "이것은 사회자본인가요?"],
          ("찬 · 정부가 만든 모임은 사회자본을 못 키운다", "라자스탄에서 정부와 NGO가 세운 조직에 가입한 마을은 7년 뒤 사회자본이 오르지 않았고, 주민이 스스로 만든 조직에 가입한 마을만 올랐다(Table 2). 외부에서 만든 모임은 돈과 사업이 끝나면 함께 끝나지만 안에서 만든 모임은 책임이 남기 때문이다. Fukuyama(3주)는 사회자본이 정책으로 만들기 어렵다고 했고, Knack(7주)은 미국 주 정부도 거의 못 키운다고 했다."),
          ("반 · 이 자료로는 그렇게 말할 수 없다", "라자스탄에서 공식 조직에 가입한 사람은 2%도 안 되고 그 조직도 거의 전부 정부가 세운 것이다(945). 변이가 없는 변수로는 효과가 있는지 없는지 알 수 없다. 실제로 정부 조직 계수는 7.42인데 표준오차가 7.38이다. “효과 없음”이 아니라 “식별 안 됨”이다. Paxton(6주)은 자율적 시민사회가 보통 국가의 후원으로 생긴다는 Tong을 인용했다."),
          "한국의 마을공동체 지원사업과 주민자치회는 어느 쪽인가. 정부가 만든 모임이 자생 모임이 되려면 무엇이 바뀌어야 하는가", local,
          "첫 쟁점입니다. 정부가 만든 모임은 사회자본을 못 키우는가. 라자스탄 결과는 못 키운다 쪽입니다. 그런데 그 결과가 나온 자료를 보면 공식 조직에 가입한 사람이 2%도 안 됩니다. 정부 조직 계수 7.42의 표준오차가 7.38입니다. 효과가 없는 건지, 변이가 없어 못 본 건지 가를 수 없습니다. 한국의 마을공동체 지원사업을 떠올리며 어느 쪽이 그럴듯한지 말씀해 주십시오.")
    slide("Krishna (2007) 분석 결과", "Table 2 · 2004년 마을 지수에 대한 OLS, N=60",
          f'''<div class="res"><img class="shot" style="max-height:420px" src="{FIG["krishna_t2"]}" alt="Table 2"><div><div class="k">실질 효과 = 계수 × 변수 범위 (952쪽 범위 기준, 발제자 계산)</div><div class="bars">
<span class="lab">규칙(1997)</span><div class="b" style="width:100%"></div><span class="v">+12.5</span>
<span class="lab">신진 리더 접촉</span><div class="b" style="width:70%"></div><span class="v">+8.8</span>
<span class="lab">토지 불평등</span><div class="b o" style="width:33%"></div><span class="v">−4.1</span>
<span class="lab">자생 조직 가입</span><div class="b" style="width:31%"></div><span class="v">+3.9</span>
<span class="lab">정부 조직 가입</span><div class="b g" style="width:13%"></div><span class="v">n.s.</span>
<span class="lab">정부 신뢰</span><div class="b g" style="width:4%"></div><span class="v">n.s.</span></div>
<p class="take">계수가 가장 큰 자생 조직(17.57)보다 규칙(3.77)의 실질 효과가 세 배 크다. 범위가 .00~.22 대 .53~3.85이기 때문이다.<small>판정 기준 p&lt;.05 → 유의 4개 · 1997년 지수 SD 7.1 · R² .23(1997 지수만) → .79</small></p></div></div>''',
          "Krishna 2007: 949, 952. 실질 효과는 계수에 변수 범위를 곱한 발제자 계산.",
          "왼쪽이 원문 표입니다. 유의한 것이 넷입니다. 오른쪽은 계수에 변수 범위를 곱한 실질 효과입니다. 계수만 보면 자생 조직이 17.57로 제일 크지만, 그 변수는 0에서 0.22 사이에서만 움직입니다. 규칙은 0.5에서 3.85까지 움직여서 실질 효과가 세 배입니다. 그래서 저자가 '규칙이 인과적으로 앞선다'고 썼습니다. 아래 두 줄, 정부 조직과 정부 신뢰는 회색입니다.")
    slide("Krishna (2007) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>같은 주 제도 아래라 제도 설계 효과는 검증 불가(950)</li><li>교육처럼 7년보다 오래 걸리는 효과는 못 본다(각주 19)</li><li>자생 조직 가입은 1997~2004 증가분이라 내생성 우려(각주 27)</li><li>결과가 특정 역사 국면에 달려 있을 수 있다(각주 23)</li><li>리더가 어떻게 생기는지는 모른다(954)</li></ul><img class="shot" style="max-height:120px;margin-top:12px" src="{FIG["krishna_950"]}" alt="950쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>종속변수 정의(945)의 구조 차원에 "rules"가 들어 있는데 951쪽에서는 Rules가 독립변수다. 저자는 측정 수준에서는 겹치지 않는다고 답하지만(953) 개념 수준의 겹침은 인정한다</li><li>Table 1에는 60개 마을만 있다. 본문 평균 58.4·59.7은 61개 기준</li><li>952쪽은 집단 행동 변수가 "all assessed in 1997"이라 쓰지만 자생 조직은 증가분이다(각주 27과 충돌)</li><li>Table 1에서 1997년 1~4위 마을이 모두 내려오고 57~61위가 모두 올라왔다. 마을당 28~38명 표본 평균의 요동과 구분해 읽어야 한다</li></ul></div></div>''',
          "",
          "저자가 스스로 적은 한계가 다섯입니다. 가장 중요한 것이 950쪽 문장입니다. 같은 제도 아래라 제도 효과는 검증할 수 없다. 오른쪽은 제가 원문을 대조하며 찾은 것입니다. 규칙이 종속변수 정의에도 들어 있고 독립변수이기도 합니다. 저자도 개념 수준에서는 겹친다고 인정합니다. 이 점은 토론으로 가져가지 않고 여기서만 짚습니다.")
    issue("사회자본이 7년 만에 바뀐다면 역사는 무엇을 정하는가", "Krishna · 쟁점 2", "brain",
          ["역사가 정한다 (Putnam 1993)", "제도가 정한다 (Rothstein)", "규칙과 리더가 정한다 (Krishna)", "그런데 1997년 지수도 여전히 유의하다 (.12*)"],
          ("찬 · 7년이면 바뀐다", "61개 마을 중 33개가 오르고 28개가 내렸고, 16개 마을은 한 표준편차 넘게 올랐다. 역사가 전부를 정한다면 같은 역사를 가진 이웃 마을들이 7년 사이 이렇게 갈릴 수 없다. 갈린 이유가 규칙과 새 리더처럼 사람이 바꿀 수 있는 것이었다는 점이 더 중요하다."),
          ("반 · 7년은 역사가 아니다", "1997년 지수는 열여섯 변수를 다 넣어도 여전히 유의하다(.12*). 과거가 현재를 설명하는 힘은 남아 있다. Guiso 외(4주)가 말한 역사 의존은 500년 단위라, 7년 사이 오르내린 것으로 그 가설을 기각할 수는 없다. 저자도 결과가 특정 시기에 달렸을 수 있다고 적었다(각주 23)."),
          "7년 변화로 “역사가 정한다”를 기각할 수 있는가. 기각할 수 없다면 이 논문이 보여 준 것은 무엇인가", local,
          "둘째 쟁점입니다. 사회자본이 7년 만에 바뀌었다면 역사가 정한다는 말은 틀렸는가. 위에서 아래로 갈수록 낙관적인 답입니다. 그런데 맨 아래 줄을 보십시오. 1997년 지수가 여전히 유의합니다. 4주차 Guiso가 말한 역사는 500년 단위였습니다. 7년 변화가 그 가설을 건드리는지, 어느 쪽인지 말씀해 주십시오.")
    photo("rajasthan_village", "친구가 만든 모임에 가입했다.", "정부가 만든 모임은 같은 카드에서 수치를 움직이지 못했다(Table 2).", '''Krishna는 제도를 검증하지 않은 것이 아니라 하지 못했다. 61개 마을이 전부 라자스탄 주 아래 있었다. "Since all the villages studied here share the same macro-institutional framework, it is not possible to test whether changing institutional designs will help build social capital"(950). 제도를 비교하려면 제도가 다른 단위가 필요하다. 스위스 24개 칸톤이 그 단위다.''', "80억 분의 1 카드로 돌아가면 이 논문은 한 줄을 넣습니다. 친구가 만든 모임에 가입했다. 정부가 만든 모임은 수치를 못 움직였습니다. 그런데 Krishna는 제도를 검증하지 않은 게 아니라 못 했습니다. 61개 마을이 전부 같은 주 아래 있었습니다. 제도를 비교하려면 제도가 다른 단위가 있어야 합니다. 스위스 24개 칸톤으로 갑니다.")

    # ───────── 2 Freitag ─────────
    slide("Freitag (2006) 연구 개요", "Bowling the State Back In: Political Institutions and the Creation of Social Capital · <i>EJPR</i> 45(1)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["freitag_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>정치제도(직접민주주의·합의민주주의·지방자치)가 결사체 참여를 만드는가. Putnam의 하위체계 비교법을 스위스에 적용</dd>
<dt>자료</dt><dd>24개 칸톤. 종속 = Swiss Household Panel 1999 4문항 주성분(N=7,799)의 칸톤 평균. 제도는 1980~1998 평균, 언어권·도시화는 1990 인구조사</dd>
<dt>설계</dt><dd>양변량에서 유의한 변수만 다변량으로. N=24라 모형당 변수 4개. 신뢰는 통제변수(신뢰 → 가입 방향을 가정, 134)</dd>
<dt>결과</dt><dd>세 제도 모두 양변량 유의(.63~.71). 다변량에서 직접민주주의는 언어권을 넣으면 .47 → .18 비유의(Table 6 Model 5). 직접민주주의–독일어권 r=.86(각주 10)</dd>
<dt>한계</dt><dd>"only suggestive and explorative"(146). 공통 원인 가능성을 각주 10에서 자인</dd></dl></div>''',
          "수치는 Table 5·6·7(139~142).",
          "Freitag은 Krishna가 못 한 일을 합니다. 제도가 다른 24개 칸톤을 비교합니다. 세 제도 모두 결사체 참여와 같이 움직였습니다. 그런데 독일어권이라는 변수 하나를 넣자 직접민주주의 효과가 사라집니다. 직접민주주의와 독일어권의 상관이 .86입니다. 저자 스스로 탐색적이라고 썼습니다.")
    slide("Freitag (2006) 연구 질문과 가설", "",
          '''<div class="ladder">
<div class="l">질문</div><div>사회자본의 효과 연구는 많은데 형성 연구는 없다. 정치제도가 결사체 생활을 만드는가</div><div class="q">"little research has explicitly addressed the question of how social capital can be built" <i>123</i></div>
<div class="l">이론적 기대</div><div>Jackman &amp; Miller의 구분. 사회자본을 외생으로 두는 접근(Putnam 1993)과 내생으로 두는 접근(Levi, Tarrow, Skocpol). 후자를 택한다. 공통 기제는 제도가 시민 요구를 듣고 중재하는 능력. 이론은 "vague"하다고 인정(131)</div><div class="q">"The second approach endogenizes social capital as an outcome of social and political arrangements" <i>125</i></div>
<div class="l">설계 선택</div><div>같은 나라 안 24개 칸톤 = 최대유사체계. 제도는 1999년 이전 값으로 시간 순서 확보. 방향의 근거는 역사: 직접입법 13~14세기, 결사체 18세기. 결사체 명부가 없어 설문 자료</div><div class="q">"meet the demands of a most similar system research design in a particularly appropriate manner" <i>124</i></div>
<div class="l">결과</div><div>Table 5 양변량 세 제도 모두 유의. Table 6 통제를 하나씩 넣으면 직접민주주의는 언어권에, 지방자치는 도시화에 무너짐. Table 7에서 직접민주주의와 언어권을 같은 모형에 넣지 않음</div><div class="q">"the fit of the four models … further confirms the significance of the thesis" <i>140–142</i></div>
<div class="l">결론</div><div>제도가 중요하다. Putnam의 불신·불참·약한 민주주의 악순환에서 벗어나는 하향식 경로</div><div class="q">"democratic institutions suggest a 'top-down' path" <i>145</i></div></div>''',
          "", "질문은 분명합니다. 제도가 결사체를 만드는가. 이론 자리에서 저자는 Putnam을 외생 접근으로, 자기를 내생 접근으로 놓습니다. 이게 5장에서 본 축 뒤집기의 원문입니다. 설계의 핵심은 시간 순서입니다. 제도를 1999년 이전 값으로 재고, 역사도 끌어옵니다. 직접입법은 13세기, 결사체는 18세기. 결과 단에서 통제를 하나씩 넣는 방식이 나오는데, 이 방식이 뒤에 쟁점이 됩니다.")
    meas("Freitag (2006) 사회자본과 제도 변수 측정", "127쪽, 각주 2", "freitag_meas", "Freitag 2006: 127. 종속변수 측정 문단",
         [("개념적 정의", "Coleman과 Putnam의 정의 “social networks, cooperative norms and interpersonal trust”(123) 가운데 결사체 참여를 분석 대상으로 선택"),
          ("측정 문항", "스위스 가구패널(SHP) 1999의 4문항. 동호회·단체 활동 참여, 명예직·봉사 활동, 월 봉사 시간, 9개 유형 결사체의 능동 회원 수(각주 2)"),
          ("지수 구성", "주성분 분석에서 한 차원으로 묶임(적재값 모두 .50 이상, KMO .71). 응답자 요인 점수의 칸톤 평균을 종속변수로 사용"),
          ("신뢰의 처리", "신뢰가 결사체 가입에 선행한다고 가정하고 통제변수로 투입(134). 다변량 분석에서 .06으로 유의하지 않음"),
          ("제도 변수", "직접민주주의는 주민발의·주민투표의 요건(서명 수, 기간, 재정 주민투표 기준)을 점수화한 지수(Frey &amp; Stutzer 2000, 1~6점). 투표 실시 횟수는 반영하지 않음")],
         "Wollebaek &amp; Selle(4주차)는 수동적 회원도 신뢰가 높다고 보고했으나 이 논문의 넷째 문항은 능동 회원만 집계. Knack &amp; Keefer(10주차)는 단체 가입이 경제 성장과 무관하고 신뢰만 유의하다고 보고",
         "왼쪽이 127쪽 측정 문단입니다. Freitag은 Coleman과 Putnam의 정의에서 결사체 참여만 골라 종속변수로 삼았습니다. 스위스 가구패널 네 문항을 주성분 분석으로 묶고, 칸톤 평균을 썼습니다. 신뢰는 가입보다 먼저 온다고 가정해서 통제변수로 넣었습니다. 그 신뢰의 계수가 다변량 분석에서 .06이고 유의하지 않습니다. 제도 변수도 하나 짚겠습니다. 직접민주주의 지수는 주민투표를 시작하는 요건을 점수화한 값이라서, 투표가 실제로 몇 번 열렸는지는 담지 않습니다. 이 측정 방식이 첫 쟁점으로 이어집니다.")
    issue("참여 제도를 만들면 참여가 느는가, 참여하는 사람들이 그 제도를 만든 것인가", "Freitag · 쟁점 1", "buttons",
          ["주민투표제를 도입한다", "주민투표 할 사람들이 사는 동네로 이사한다", "지자체장"],
          ("찬 · 제도가 먼저다", "스위스에서 직접입법 제도는 13~14세기에 생겼고 결사체는 18세기에 늘었다. 순서가 분명하다. 투표를 시작하기 쉬운 칸톤일수록 사람들은 요구를 모으려고 모임을 만들고, 그 모임이 다시 참여를 낳는다. Knack &amp; Keefer(10주)도 정부를 제약하는 제도가 있는 나라에서 신뢰가 높다고 했다."),
          ("반 · 참여하는 사람들이 제도를 만들었다", "직접민주주의가 활발한 칸톤은 거의 전부 독일어권이고 둘의 상관이 .86이다. 저자 스스로 지역 배경이 제도와 사회자본 둘 다를 낳았을 수 있다고 각주에 썼다(각주 10). 언어권을 넣는 순간 직접민주주의 효과가 사라지는데(.47 → .18), 저자는 마지막 표에서 둘을 같은 모형에 넣지 않았다. 13세기와 1999년 사이 700년의 자료는 없다."),
          "한국의 주민참여예산제는 어느 쪽인가. 도입한 지자체와 참여율의 관계로 이 논쟁을 가를 수 있는가, 아니면 같은 함정에 빠지는가", local,
          "두 버튼 중 하나를 눌러야 하는 지자체장입니다. 주민투표제를 도입할 것인가, 주민투표 할 사람들이 사는 동네로 이사할 것인가. 농담이지만 Freitag의 자료가 딱 이 상황입니다. 직접민주주의가 활발한 칸톤은 전부 독일어권입니다. 제도가 먼저인지 사람이 먼저인지 24개 칸톤으로는 가를 수 없습니다. 한국의 주민참여예산제를 놓고 어느 쪽인지 말씀해 주십시오.")
    slide("Freitag (2006) 분석 결과", "Table 6(141쪽) · 제도 변수 3개에 통제변수를 하나씩 추가한 9개 모형",
          f'''<div class="res"><img class="shot" style="max-height:430px" src="{FIG["freitag_t6"]}" alt="Table 6"><div><div class="k">직접민주주의 표준화 계수, 통제변수에 따라</div><div class="bars">
<span class="lab">+좌파 정당 (M1)</span><div class="b" style="width:100%"></div><span class="v">.47***</span>
<span class="lab">+사회 신뢰 (M4)</span><div class="b" style="width:98%"></div><span class="v">.46***</span>
<span class="lab">+도시화 (M6)</span><div class="b" style="width:100%"></div><span class="v">.47***</span>
<span class="lab">+언어권 (M5)</span><div class="b g" style="width:38%"></div><span class="v">.18 n.s.</span></div>
<div class="k" style="margin-top:14px">R², Table 7의 네 모형</div><div class="bars">
<span class="lab">제도 셋 (M1)</span><div class="b" style="width:95%"></div><span class="v">.75</span>
<span class="lab">도시화 + 언어권 (M2)</span><div class="b g" style="width:100%"></div><span class="v">.79</span></div>
<p class="take">제도 셋이 설명하는 분산(.75)보다 통제 둘만의 설명(.79)이 크다. 저자는 이 비교를 쓰지 않았다.<small>직접민주주의와 언어권은 Table 7의 어느 모형에도 함께 들어가지 않는다 · N=24, 모형당 변수 4개(140)</small></p></div></div>''',
          "Freitag 2006: 141~142. Table 6의 Model k = 제도 셋 + k번째 통제(11-09 PDF 화면 확인). 제도 셋만의 모형은 Table 7 Model 1.",
          "원문 표를 가로로 돌렸습니다. 아홉 모형은 전부 제도 셋에 통제를 하나씩 더한 것입니다. 오른쪽 위, 직접민주주의 계수는 어떤 통제를 넣어도 .47 근처에서 버티다가 언어권을 넣는 순간 .18로 떨어져 비유의가 됩니다. 아래는 Table 7의 설명력입니다. 제도 셋이 .75인데 도시화와 언어권 둘만 넣으면 .79입니다. 저자는 이 비교를 하지 않았습니다.")
    slide("Freitag (2006) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>"only suggestive and explorative"(146). 방법이 더 정교해야 한다</li><li>언어권이 직접민주주의와 사회자본의 공통 원인일 수 있다(각주 10, r=.86)</li><li>양변량 선별에서 떨어진 변수가 다변량에서 유의해질 수 있다(각주 8)</li><li>N=24라 모형당 변수 4개(140). 국가 수준 비교는 거의 불가능(146)</li><li>결사체는 연결망의 한 지표일 뿐, 가장 중요한 지표는 아닐 수 있다(126)</li></ul><img class="shot" style="max-height:80px;margin-top:10px" src="{FIG["freitag_146"]}" alt="146쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>제도 셋은 모든 모형에 남고 통제는 하나씩만 들어간다. 제도가 "거의 모든 모형에서 버틴다"는 결과는 설계가 보장한 것이다. 유의한 통제 둘(언어권·도시화)을 함께 넣은 모형은 Table 6에 없다</li><li>개인 7,799명 자료를 칸톤 24개로 접었다. 세 기제(옹호 유인·숙의·반응 확신)는 개인 수준인데 하나도 검증되지 않았다</li><li>직접민주주의 지수는 제도의 "있음"(문턱)이지 "쓰임"(투표 경험)이 아니다. 이 구분이 다음 세 논문의 출발점이다</li></ul></div></div>''',
          "",
          "저자가 적은 한계 중 둘째 줄이 핵심입니다. 공통 원인 가능성을 각주에서 스스로 인정했습니다. 제가 짚는 것은 설계입니다. 제도 셋은 늘 모형에 남고 통제는 하나씩만 들어갑니다. 제도가 버틴다는 결과는 그 설계가 만든 것입니다. 그리고 마지막 줄. 직접민주주의 지수는 제도가 있다는 것이지 썼다는 것이 아닙니다. 다음 세 논문은 전부 쓰임을 봅니다.")
    issue("모임은 늘었는데 신뢰가 안 늘었다면 국가는 사회자본을 만든 것인가", "Freitag · 쟁점 2", "drake",
          ["신뢰를 종속변수로 두고 제도 효과를 본다", "신뢰는 통제변수에 넣고 .06이 나오면 넘어간다"],
          ("찬 · 국가는 사회자본을 만들었다", "Putnam(3주)의 정의에서 사회자본은 연결망과 규범과 신뢰 셋인데, 결사체는 그중 연결망이다. 사람이 모이면 거기서 규범과 신뢰가 자라는 것이 Putnam의 논리이고, Wollebaek &amp; Selle(4주)는 노르웨이 자료로 가입이 신뢰를 키운다는 것을 보였다. 모임을 늘렸다면 나머지는 따라온다."),
          ("반 · 모임을 만든 것이지 사회자본을 만든 것이 아니다", "신뢰는 이 논문에서 결과가 아니라 통제변수였고, 다변량에서 .06으로 아무 관계가 없었다(Table 6). 저자는 신뢰가 가입을 낳는다고 가정했지(134) 가입이 신뢰를 낳는지는 보지 않았다. Knack &amp; Keefer(10주)는 단체 가입이 성장과 무관하고 신뢰만 유의하다고 했고, Kumlin &amp; Rothstein은 참여를 신뢰의 원인이 아니라 증상이라 부른다."),
          "결사체 참여 지수가 오른 칸톤에서 사람들은 서로를 더 믿게 되었는가. 이 논문으로 그것을 알 수 있는가", local,
          "드레이크 형식입니다. 신뢰를 종속변수로 두는 것은 싫고, 통제변수에 넣어 .06이 나오면 넘어가는 것은 좋다. Freitag이 한 일이 이것입니다. 모임은 늘었습니다. 그런데 신뢰가 늘었는지는 이 논문으로 모릅니다. 국가가 만든 것이 모임인지 사회자본인지, 어느 쪽인지 말씀해 주십시오.")
    photo("swiss_canton", "주민투표를 하기 쉬운 지역으로 이사했다. 모임은 늘고, 신뢰는 그대로였다.", "그리고 그 지역은 전부 독일어권이었다(각주 10).", '''Freitag은 제도와 결사체가 같이 움직인다는 데까지 보여 줬다. 답하지 못한 것이 둘이다. 어떤 설계가 왜 작동하는가. 문턱 지수와 득표율과 자기평가 점수는 제도의 크기이지 작동 방식이 아니다. 그리고 신뢰는 왜 안 움직였는가. 다음 논문은 자료 없이 설계만으로 첫 질문에 답하려 한다. 반응하는 제도가 없으면 사회자본은 잠재 상태로 남는다는 명제로 둘째 질문의 자리를 만든다.''', "카드에 넣는 한 줄입니다. 주민투표를 하기 쉬운 지역으로 이사했다, 모임은 늘고 신뢰는 그대로였다. 지수가 투표 횟수가 아니라 문턱이라 '쉬운'이라고 썼습니다. Freitag이 못 답한 것이 둘입니다. 어떤 설계가 왜 작동하는가, 신뢰는 왜 안 움직였는가. 다음 논문은 자료 없이 설계만 말합니다.")

    # ───────── 3 Lowndes & Wilson ─────────
    slide("Lowndes &amp; Wilson (2001) 연구 개요", "Social Capital and Local Governance: Exploring the Institutional Design Variable · <i>Political Studies</i> 49(4)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["lw_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>Putnam이 상수로 둔 제도 설계가 사회자본의 창출과 동원을 어떻게 좌우하는가</dd>
<dt>자료</dt><dd>없음. 영국 노동당의 '민주적 쇄신' 프로그램(1997~)과 저자들의 위탁연구, Audit Commission 1999를 근거로 한 이론 논문</dd>
<dt>설계</dt><dd>지방정부 제도 설계의 네 차원. ① 자발부문과의 관계 ② 시민 참여 기회 ③ 의사결정의 반응성 ④ 민주적 리더십과 사회적 포용</dd>
<dt>주장</dt><dd>여론조사는 거의 기여 없고 숙의형만 사회자본을 만든다. 모범 지자체의 4분의 3이 협의 결과를 결정에 반영하지 않는다. 반응하는 제도가 없으면 사회자본은 잠재 상태</dd>
<dt>한계</dt><dd>"we have not set out specifically to evaluate the reforms"(641). 다섯 편 중 유일하게 실증이 없다</dd></dl></div>''',
          "수치는 638(4분의 3)과 639(12개 지표 중 민주주의 변수 0) 둘뿐.",
          "다섯 편 중 자료가 없는 유일한 논문입니다. 대신 설계도를 그립니다. 지방정부가 손댈 수 있는 네 차원입니다. 숫자는 둘뿐입니다. 모범 지자체의 4분의 3이 협의 결과를 결정에 반영하지 않았다는 것, 그리고 Putnam의 제도 성과 지표 12개에 민주주의 변수가 하나도 없다는 것.")
    slide("Lowndes &amp; Wilson (2001) 연구 질문과 주장", "",
          '''<div class="ladder">
<div class="l">질문</div><div>Putnam 1993: 10의 한 문장을 공격한다. 이탈리아 지역정부의 제도 설계가 상수라서 다른 요인을 더 믿을 만하게 찾을 수 있다는 말. 성과가 그렇게 갈렸는데 왜 설계가 같았다고 가정하는가</div><div class="q">"why should we assume that their design remained constant?" <i>632</i></div>
<div class="l">이론적 기대</div><div>신제도주의 셋. 제도는 조직도가 아니라 습관·규범·유인. 창출과 동원은 다른 일. 좋은 정부는 시민 지향 시민과 시민 지향 정부 행위자의 상호작용(Levi 1996)</div><div class="q">"Institutions are habits, not things" <i>632</i></div>
<div class="l">설계 선택</div><div>영국 노동당의 체계적 제도 재설계가 네 차원을 한 번에 비춘다. 설계는 정밀과학이 아니고 '나쁜 설계'가 사회자본을 키운 반례(Newton 1976)도 있다는 단서를 미리 둔다</div><div class="q">"Institutional redesign cannot, however, be a precise science" <i>633</i></div>
<div class="l">주장</div><div>네 차원 중 셋째가 중심. 참여를 막는 최대 요인은 "의회가 아무것도 안 할 것"이라는 인식. 공급된 사회자본은 정치 과정의 수요와 만나야 한다</div><div class="q">"Social capital may, then, remain a 'latent' phenomenon in the absence of responsive political institutions" <i>638</i></div>
<div class="l">결론</div><div>설계 원칙 둘: 가치의 명확성, 변이와 수정 가능성. 정원 가꾸기 대 건축. 결과는 내용만큼 과정에 달렸다</div><div class="q">"may depend as much upon the process as upon the content of institutional redesign" <i>645</i></div></div>''',
          "", "질문은 Putnam의 한 문장을 향합니다. 제도 설계가 상수라는 말. 이론 자리에서 제도는 조직도가 아니라 습관이라고 합니다. 설계 자리에서 미리 단서를 둡니다. 설계는 정밀과학이 아니고, 나쁜 설계가 사회자본을 키운 사례도 있다고. 이 단서가 나중에 저자 자신을 겨눕니다. 주장의 중심은 셋째 차원, 반응성입니다. 반응하는 제도가 없으면 사회자본은 잠재 상태로 남는다.")
    meas("Lowndes &amp; Wilson (2001) 핵심 개념", "630~638쪽", "lw_latent", "Lowndes &amp; Wilson 2001: 638",
         [("개념적 정의", "Putnam(1995)의 정의를 사용. 규범(Coleman, Fukuyama), 구조(Bourdieu), 결과(Coleman, Ostrom)를 함께 포함(630)"),
          ("창출과 동원", "창출은 연결망과 규범이 만들어지는 과정(차원 ①②), 동원은 이미 있는 사회자본이 민주적 결정에 영향을 미치는 과정(차원 ③④). “Participation is not, after all, the same as social capital”(637)"),
          ("잠재 상태", "사회자본이 있어도 이에 반응하는 정치 제도가 없으면 민주주의 성과로 이어지지 않는 상태(638). 결론에서는 조건이 “responsive and inclusive”로 늘어남(641)"),
          ("측정", "자체 자료와 측정 없음. 영국 지방정부 사례와 기존 연구를 근거로 논의")],
         "Coleman(1988, 3주차)은 사회자본을 기능으로 정의하므로, 기능하지 않는 잠재 사회자본은 그 정의와 맞지 않음. Dasgupta(2000, 9주차)가 비판한 이질적 요소의 합산(p.327)을 이 논문은 장점으로 평가",
         "이 논문은 자체 측정이 없어서 개념을 정리했습니다. 왼쪽이 638쪽 원문입니다. 저자들은 Putnam의 정의를 쓰는데, 그 정의에는 규범과 구조와 결과가 함께 들어 있습니다. 9주차 Dasgupta가 비판한 합산을 저자들은 장점으로 평가합니다. 그리고 사회자본이 만들어지는 과정과 동원되는 과정을 나눕니다. 사회자본이 있어도 제도가 반응하지 않으면 민주주의 성과로 이어지지 않는데, 저자들은 이 상태를 잠재라고 부릅니다. 3주차 Coleman처럼 사회자본을 기능으로 정의하면 잠재 사회자본이라는 개념이 성립하는지 따져 볼 수 있습니다. 첫 쟁점입니다.")
    issue("답하지 않을 공청회라면 아예 열지 않는 편이 나은가", "Lowndes &amp; Wilson · 쟁점 1", "fine",
          ["협의는 했습니다", "모범 지자체 4분의 3이 결과를 결정에 반영하지 않음 (Audit Commission 1999)"],
          ("찬 · 열지 않는 편이 낫다", "사람들이 참여를 그만두는 가장 큰 이유는 “어차피 의회는 아무것도 안 한다”는 인식이다(638). 의견을 물어 놓고 반영하지 않으면 그 인식을 매번 확인시켜 주는 셈이다. 저자들 스스로 참여가 형식적이거나 냉소적일 수 있다고 썼다(637). 답할 생각이 없으면 묻지 않는 편이 신뢰를 덜 깎는다."),
          ("반 · 그래도 여는 편이 낫다", "저자들이 직접 든 반례가 있다. 버밍엄 시의회가 소수민족 단체를 배제하자 그 단체들은 사라지지 않고 오히려 조직되어 결정에 영향을 미치게 됐다(633, Newton 1976). 답이 없어도 공청회에서 사람들은 서로를 알게 되고 새 모임이 생긴다(637). Fukuyama(3주) 식으로 보면 국가가 너무 잘 답해 주면 시민은 스스로 조직하는 힘을 잃는다."),
          "한국의 공청회·주민설문·국민청원 중 답이 돌아오지 않는 것들은 사회자본을 깎고 있는가, 아니면 다른 곳으로 흘려보내고 있는가", local,
          "불타는 방에서 커피를 마시는 개입니다. 자막은 '협의는 했습니다'. 모범 지자체의 4분의 3이 협의 결과를 결정에 반영하지 않았습니다. 그러면 답하지 않을 공청회는 아예 열지 않는 편이 나은가. 저자들 논리로는 그렇습니다. 그런데 저자들이 직접 든 반례가 있습니다. 버밍엄에서는 배제가 오히려 동원을 낳았습니다. 어느 쪽인지 말씀해 주십시오.")
    slide("Lowndes &amp; Wilson (2001) 제도 설계 변수", "차원별 설계 변수, 사회자본에 미치는 경로, 근거",
          f'''<div class="two" style="grid-template-columns:1.25fr 1fr;align-items:start"><table style="font-size:14.5px"><tr><th>차원</th><th>지자체가 손댈 수 있는 것</th><th>사회자본에 닿는 경로</th><th>근거</th></tr>
<tr><td>① 자발부문과의 관계</td><td>보조금, 계약·파트너십 조건, 인정 요건</td><td>창출. 계약은 단체를 지자체 닮게 만들고 작은 단체·캠페인형을 밀어낸다</td><td>"Unless you're cute and big"(635)</td></tr>
<tr><td>② 시민 참여 기회</td><td>조사 → 공청회 → 시민배심·포럼</td><td>창출. 여론조사는 거의 기여 없음, 숙의형만 사회자본을 만든다</td><td>637</td></tr>
<tr><td>③ 의사결정의 반응성</td><td>협의 결과의 결정 연결, 집행부·의회 분리</td><td>동원. 반응이 없으면 참여가 꺾이고 사회자본은 잠재</td><td>Audit Commission 1999: 41(638)</td></tr>
<tr><td>④ 리더십과 포용</td><td>회의 시각·형식·언어, 직선 시장</td><td>동원의 분배. 누가 들어오는지를 절차가 정한다</td><td>Hall 1999: 사회자본은 "중산층·중년의 것"(641)</td></tr></table>
<div><img class="shot" style="max-height:150px" src="{FIG["lw_quarters"]}" alt="638쪽 Audit Commission"><p class="take" style="font-size:15.5px">다섯 편 중 숫자가 둘뿐인 논문. 그 둘이 모두 셋째·넷째 차원에 있다. 창출(①②)보다 동원(③④)이 이 논문의 기여다.<small>12개 지표 중 민주주의 변수 0은 Putnam 1993 3장에 대한 지적(639)</small></p></div></div>''',
          "Lowndes &amp; Wilson 2001: 633~641. 표는 발제자 정리, 인용은 원문 쪽수.",
          "표가 없으니 네 차원을 표로 정리했습니다. 왼쪽부터 지자체가 손댈 수 있는 것, 사회자본에 닿는 경로, 근거입니다. 숫자가 둘뿐인데 둘 다 아래 두 줄, 동원 쪽에 있습니다. 이 논문의 기여는 창출이 아니라 동원입니다. 사회자본이 있어도 꺼내 쓰지 못하는 상태를 이름 붙인 것입니다.")
    slide("Lowndes &amp; Wilson (2001) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>개혁을 평가하려 한 것이 아니다(641). 결과 예측은 어렵다(643)</li><li>설계는 정밀과학이 아니며 의도치 않은 효과가 반복된다(633)</li><li>사회자본 산출은 재기 어렵다(637). 자기 틀도 같은 어려움을 안는다</li><li>단정한 문장은 Putnam 비판과 "참여 ≠ 사회자본", "참여 ≠ 민주주의"뿐. 나머지는 "may"</li><li>지역에 맞는 설계는 뿌리내리지만 급진적 변화를 일으키기 어렵다(645)</li></ul><img class="shot" style="max-height:90px;margin-top:10px" src="{FIG["lw_641"]}" alt="641쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>네 차원은 분류이지 설명이 아니다. 어떤 관찰이 나와도 네 차원 중 하나로 흡수되어 반박할 길이 없다</li><li>Newton 1976 반례(633)는 셋째 차원과 정면으로 어긋난다. 무반응이 잠재가 아니라 동원과 결정 영향을 낳았다. 저자는 "With these caveats in mind" 한 구절로 넘기고 다시 다루지 않는다</li><li>잠재의 조건이 638쪽 "responsive"에서 641쪽 "responsive and inclusive"로 늘어난다</li><li>창출과 동원을 나눠 처방하지만 Audit Commission 논리 자체가 동원 실패가 창출을 막는다는 것이다. 둘은 독립이 아니다</li></ul></div></div>''',
          "",
          "저자들은 평가가 아니라고 처음부터 말합니다. 제가 짚는 것은 둘째 줄입니다. 저자들이 직접 든 버밍엄 사례가 셋째 차원과 정면으로 어긋나는데, caveat 한 구절로 넘기고 다시 다루지 않습니다. 이게 둘째 쟁점입니다.")
    issue("제도 설계로 사회자본을 만들 수 있다는 믿음은 어디까지 가는가", "Lowndes &amp; Wilson · 쟁점 2", "gru",
          ["제도 설계의 네 차원을 짠다", "반응하는 제도가 사회자본을 꺼낸다", "데이터는 없다", "데이터는 없다"],
          ("찬 · 설계가 길이다", "네 차원은 전부 지자체가 내일부터 바꿀 수 있는 것들이다. 보조금 조건, 회의 시각, 협의 결과를 결정에 연결하는 규칙. 자료가 없다는 것은 아직 안 쟀다는 뜻이지 틀이 틀렸다는 뜻이 아니다. 2주차 Ostrom은 제도가 신뢰 형성을 돕는가를 열린 질문으로 두었고, 이 논문은 그 질문에 답할 변수 목록을 만들었다. 6년 뒤 Krishna와 Freitag이 그 질문을 쟀다."),
          ("반 · 설계가 아니라 시간이다", "이 논문에는 자료가 없다(641). 네 차원 중 어느 것이 틀렸는지 보여 줄 관찰이 무엇인지도 적혀 있지 않다. 저자들도 마지막에 제도는 건축이 아니라 정원 가꾸기라고 했다(645). 뿌리내린 제도는 튼튼하지만 설계도대로 바뀌지 않는다는 뜻이다. 버밍엄 반례는 설계와 반대 방향으로 사회자본이 움직인 경우다."),
          "네 차원 중 하나가 틀렸다면 어떤 관찰이 나와야 그것을 알 수 있는가. 알 수 없다면 이 틀은 무엇을 한 것인가", local,
          "그루의 계획입니다. 네 차원을 짠다, 반응하는 제도가 사회자본을 꺼낸다, 그리고 데이터는 없다. 농담 같지만 저자들도 알고 있었습니다. 그래서 마지막에 정원 가꾸기를 말합니다. 설계로 만들 수 있다는 믿음과 시간이 만든다는 믿음, 어느 쪽에 서시겠습니까.")
    photo("birmingham_council", "구청 공청회에 갔지만 답장은 없었다.", "넷 중 셋은 결정에 반영하지 않았다(638). 수치는 움직이지 않는다. 이 논문은 재지 않았다.", '''Lowndes와 Wilson은 제도가 사회자본을 어디서 키우고 어디서 잠재우는지 설계도를 그렸다. 설계도에는 사람이 없다. 자료도 없고, 한 사람이 제도를 만나 무엇이 바뀌는지도 없다. 반응하는 제도가 사람 안에서 어떻게 작동하는지, 돈이 바뀌는지 생각이 바뀌는지는 이 논문으로 알 수 없다. 다음 논문은 그 빈칸을 한 정책으로 채운다. 미국 제대군인원호법을 받은 716명에게 50년 뒤 물었다.''', "카드의 한 줄입니다. 구청 공청회에 갔지만 답장은 없었다. 수치는 움직이지 않습니다. 이 논문은 재지 않았으니까요. 설계도에는 사람이 없습니다. 다음 논문은 그 빈칸을 사람으로 채웁니다. 제대군인원호법을 받은 716명에게 50년 뒤에 물었습니다.")

    # ───────── 4 Mettler ─────────
    slide("Mettler (2002) 연구 개요", "Bringing the State Back In to Civic Engagement: Policy Feedback Effects of the G.I. Bill · <i>APSR</i> 96(2)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["mettler_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>미국 제대군인원호법(G.I. Bill)의 교육 급여가 1950~64년 시민참여를 높였는가. 높였다면 돈 때문인가, 받은 방식 때문인가</dd>
<dt>자료</dt><dd>참전자회 명단 4,000명 중 1,000명 우편조사(1998년 8월), 응답 716명(73.5%). 면접 28명. 남성, 백인 98.5%</dd>
<dt>설계</dt><dd>가설 넷(기존 특성·부산물·수동화·정책환류)을 학력 통제 하나로 가른다. 종속 = 1950~64 단체 가입 수, 정치참여. 생활수준×이용 상호작용으로 결정적 효과 검증</dd>
<dt>결과</dt><dd>학력을 통제해도 이용자는 단체 .47개, 정치참여 .38 더(Table 1·2, p=.01). 정치참여에서 학력은 비유의. 호혜 변수는 단체 가입에만 유의. 효과는 저중·중에서 유의, 최저층 비유의, 정치참여는 상위층 1.22가 최대</dd>
<dt>한계</dt><dd>회고(부록 A), 표본이 유리한 쪽이라 과소추정(부록 B). 1965년 이후 해석 효과는 사라지고 자원 효과만 남음(각주 15)</dd></dl></div>''',
          "Table 1~7(357~362). 표의 둘째 열은 표준화계수 β, 표준오차가 아님.",
          "Mettler는 정책 하나를 봅니다. 제대군인원호법의 교육 급여입니다. 질문이 좋습니다. 급여가 참여를 높였다면 돈 때문인가, 받은 방식 때문인가. 가설 넷을 학력 통제 하나로 가릅니다. 학력을 넣어도 급여 이용 효과가 남으면 교육의 부산물이 아니라는 뜻이 됩니다. 남았습니다. 단체 .47개, 정치참여 .38.")
    slide("Mettler (2002) 연구 질문과 가설", "가설 4개의 예측을 학력 통제 후 계수로 비교",
          f'''<div class="two" style="grid-template-columns:1.25fr 1fr;align-items:start"><div class="ladder" style="grid-template-columns:100px 1fr 1fr">
<div class="l">질문</div><div>참여의 정점(1950~60년대)이 국가 개입 확대 직후에 왔다. 우연인가</div><div class="q">"Was the sequencing … merely a coincidence?" <i>351</i></div>
<div class="l">이론적 기대</div><div>정책은 제도다(Lowi). Pierson의 자원 효과(역량)와 해석 효과(성향). 가설 넷의 예측: 기존 특성·부산물이면 학력 통제 후 계수 0, 수동화면 음수, 정책환류면 양수</div><div class="q">"policies function as institutions, imposing particular norms and rules on recipients" <i>352</i></div>
<div class="l">설계 선택</div><div>대형 조사에 프로그램 변수가 없어 직접 수집. 전국 무작위 명단이 없어 참전자회 명단. 1950~64로 한정한 이유: 급여 직후이고 Putnam이 말한 가입의 정점</div><div class="q">"A national, random sample of all World War II veterans was not available" <i>355</i></div>
<div class="l">결과</div><div>양수. 학력 통제 후 .47(단체), .38(정치). 정치참여에서 학력 .01 비유의. 호혜는 단체 가입만 설명. 결정적 효과는 저중·중에서</div><div class="q">"the G.I. Bill benefits were not merely a conduit for higher levels of education" <i>357</i></div>
<div class="l">결론</div><div>급여가 수급자를 시민으로 편입시켰다. 어떤 메시지를 어떤 설계로 전하는가가 다음 질문</div><div class="q">"It is time to 'bring the state back in' to the study of civic life." <i>363</i></div></div>
<div><img class="shot" style="max-height:330px" src="{FIG["mettler_fig1"]}" alt="Figure 1"><p class="k" style="margin-top:6px">Figure 1(353). 자원 효과는 역량으로, 해석 효과는 성향으로. 자원이 성향에도 닿는 셋째 화살표</p></div></div>''',
          "", "이 논문의 설계는 한 문장입니다. 가설 넷을 계수 하나의 부호로 가른다. 학력을 통제했을 때 급여 이용 계수가 0이면 기존 특성이나 부산물, 음수면 수동화, 양수면 정책환류. 오른쪽이 Pierson의 도식을 가져온 그림입니다. 자원 효과는 역량으로, 해석 효과는 성향으로 갑니다. 결과는 양수였습니다.")
    meas("Mettler (2002) 시민참여 측정", "356쪽", "mettler_dv", "Mettler 2002: 356. 종속변수 조작화",
         [("설명 대상", "전후 세대의 높은 결사체 가입률(Putnam의 ‘civic generation’). 사회자본은 정의 없이 세 번 언급되고(351·362·363) 신뢰 문항은 없음"),
          ("종속변수 1", "시민단체 가입 수. 1950~64년 우애단체, 이웃·주택소유자 협회, PTA, 기타 시민단체 가입 수의 합(356)"),
          ("종속변수 2", "정치참여. 정치단체 가입 수와 다섯 가지 활동(공직자 접촉, 선거운동, 위원회 참여, 기부, 시위) 참여 여부"),
          ("해석 효과 근거", "설문 1문항 “I felt I owed something back to American society”(4점 척도, 평균 2.9)과 면접 28명(360). 해석 효과를 직접 측정한 변수는 없음")],
         "Glaeser 외(2002, 4주차)의 개인 투자 관점에서 이 급여는 교육 비용을 낮춘 외생적 변화. Fukuyama(3주차)의 의존 가설은 지지되지 않았으나, 저자는 보편 프로그램이어서 직접 검증은 아니라고 밝힘(353)",
         "왼쪽이 356쪽, 종속변수를 조작화한 문단입니다. 종속변수는 둘입니다. 하나는 1950년부터 64년까지의 시민단체 가입 수이고, 다른 하나는 정치단체 가입과 다섯 가지 정치 활동입니다. 신뢰 문항은 없습니다. 해석 효과의 근거는 설문 한 문항과 면접 28명입니다. 면접에서는 신청만 하면 수표가 왔다, 그냥 등록했다는 진술이 나옵니다. 따라서 해석 효과는 면접 진술에서 추론한 결과이고, 직접 측정한 변수는 없습니다. 첫 쟁점입니다.")
    issue("국가에 빚졌다는 감정이 시민을 만드는가", "Mettler · 쟁점 1", "handshake",
          ["국가가 준 등록금과 월 75달러", "1950년대의 단체 가입", "빚졌다는 느낌 2.9점"],
          ("찬 · 빚졌다는 감정이 시민을 만든다", "면접한 참전자 거의 전원이 급여를 권리가 아니라 특권이자 선물로 여겼고, “국가에 빚졌다”는 느낌이 강할수록 1950년대에 더 많은 단체에 가입했다(Table 3, .32). 받은 것을 갚으려는 마음이 공동체 활동으로 나타난 것이다. 이것이 Pierson이 말한 해석 효과의 가장 직접적인 증거다."),
          ("반 · 다른 것이 시민을 만든다", "빚졌다는 느낌은 단체 가입만 설명하고 정치참여에는 아무 관계가 없었다(Table 4, −.02). 정치참여 효과가 가장 컸던 집단은 가장 유복한 참전자들이었다(Table 7, 1.22). 감사의 마음이 작용했다면 가장 가난한 집 아들에게서 가장 커야 하는데 거기서는 효과가 없었다. 빚은 참여만이 아니라 복종이나 침묵도 낳을 수 있다. Lin(4주)의 말대로 원래 가진 사람이 더 가져간 것일 수 있다."),
          "한국의 국가장학금과 병역은 받은 사람에게 어떤 감정을 남기는가. 그 감정이 참여로 가는가, 아니면 다른 데로 가는가", local,
          "두 팔 악수입니다. 왼팔은 국가가 준 등록금, 오른팔은 1950년대 단체 가입, 맞잡은 손이 빚졌다는 느낌 2.9점입니다. 이 손이 정말 둘을 잇는가. 단체 가입에는 .32로 유의한데 정치참여에는 −.02입니다. 한국의 국가장학금과 병역을 떠올리며 말씀해 주십시오.")
    slide("Mettler (2002) 분석 결과", "Table 1 · 1950~64년 단체 가입 수, OLS, N=393",
          f'''<div class="res"><img class="shot" style="max-height:420px" src="{FIG["mettler_t1"]}" alt="Table 1"><div><div class="k">비표준화 계수 b와 유의확률</div><div class="bars">
<span class="lab">G.I. Bill 이용</span><div class="b" style="width:100%"></div><span class="v">.47 (.01)</span>
<span class="lab">부모 시민활동</span><div class="b" style="width:60%"></div><span class="v">.28 (.00)</span>
<span class="lab">생활수준 1960s</span><div class="b g" style="width:49%"></div><span class="v">.23 (.06)</span>
<span class="lab">최종 학력</span><div class="b" style="width:19%"></div><span class="v">.09 (.02)</span></div>
<div class="k" style="margin-top:14px">정치참여(Table 2, N=379)</div><div class="bars">
<span class="lab">G.I. Bill 이용</span><div class="b" style="width:100%"></div><span class="v">.38 (.01)</span>
<span class="lab">최종 학력</span><div class="b g" style="width:3%"></div><span class="v">.01 (.67)</span></div>
<p class="take">학력을 통제해도 급여 이용은 남고, 정치참여에서는 학력이 아무 설명을 못 한다.<small>판정 기준 p&lt;.05 → 이용 .01 · 학력(정치) .67. 각주 15: 1965~79, 1980~98에는 학력이 유의해지고 이용은 비유의</small></p></div></div>''',
          "Mettler 2002: 357~358. R²는 .14와 .08. 표의 둘째 열(β)은 생략.",
          "왼쪽이 Table 1 원문입니다. 급여 이용 .47, 학력 .09. 아래 정치참여에서는 학력이 .01, 비유의입니다. 학력을 넣어도 급여 효과가 남으니 교육의 부산물은 아닙니다. 그런데 각주 15를 보면 1965년 이후에는 반대가 됩니다. 학력이 유의해지고 급여는 사라집니다. 저자는 이것을 해석 효과의 유통기한으로 읽습니다.")
    slide("Mettler (2002) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>1998년에 1950년대를 물었다. 세부가 아니라 "대체로 활동했나"만, 과거 태도는 거의 묻지 않았다(부록 A)</li><li>표본의 이용률 60.8%(모집단 51%), 참전자 3분의 2가 사망. 효과는 과소추정 쪽(부록 B)</li><li>남성, 백인 98.5%, 흑인 부대 미포함(각주 4). 행정에 인종 차별은 흔했다(각주 21)</li><li>결측으로 회귀 N이 716의 55%(각주 10)</li><li>최저층 비효과는 "어린 시절 가난의 힘"(361), 추후 과제</li></ul><img class="shot" style="max-height:110px;margin-top:10px" src="{FIG["mettler_appA"]}" alt="부록 A"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>해석 효과는 측정되지 않고 학력 통제 후 잔차로 읽힌다. 남은 계수는 측정 안 된 다른 자원(월 75~120달러 생활비, 대학에서 쌓은 동료 연결망, 급여 기간 1~48개월)일 수 있다</li><li>부록 A에서 과거 태도는 안 묻는다고 했지만 호혜 문항과 Table 5 문항은 1998년에 물은 1950년대 태도다. 해석 효과의 유일한 설문 증거가 자기 규칙 밖에 있다</li><li>"덜 가진 쪽에서 큼"은 저중 한 칸에서만 성립. 정치참여는 상위층 1.22가 최대(Table 7)</li><li>비이용자도 군복무와 다른 급여(주택대출·실업수당)로 국가를 만났다. 비교집단이 깨끗하지 않다</li></ul></div></div>''',
          "",
          "저자가 자인한 한계는 회고와 표본입니다. 부록 둘이 그 답입니다. 제가 짚는 것은 첫 줄입니다. 해석 효과를 직접 재지 않았습니다. 학력을 통제하고 남은 계수를 해석 효과라고 부른 것입니다. 남은 계수는 월 75달러 생활비일 수도, 대학에서 만난 친구들일 수도 있습니다. 이게 둘째 쟁점입니다.")
    issue("심사 없는 급여가 심사 있는 급여보다 시민을 더 만드는가", "Mettler · 쟁점 2", "boyfriend",
          ["신청서 한 장, 다음 달 입금 (해석 효과)", "참전 군인", "졸업장과 소득 (자원 효과)"],
          ("찬 · 받는 방식이 시민을 만든다", "참전자들은 “그냥 등록했다, 아무것도 할 필요가 없었다”고 기억했고, 그 아버지 세대는 대공황 구호를 수치로 여겨 거부했다(360). 같은 돈이라도 심사 없이 누구에게나 바로 주면 존엄을 주고, 심사하면 낙인을 준다. 정치참여에서 학력이 아무 설명을 못 하고 급여 이용만 남는 결과(Table 2)가 이 해석과 맞는다. Kumlin &amp; Rothstein의 선별 창구 −.26도 같은 방향이다."),
          ("반 · 돈과 졸업장이 시민을 만든다", "해석 효과는 직접 잰 변수가 없다. 학력을 통제하고 남은 계수를 해석 효과라고 부른 것이다. 남은 계수는 월 75달러 생활비, 급여 기간 1~48개월의 차이, 대학에서 만난 동료 연결망일 수 있고 이것들은 변수에 없다(Glaeser 외, 4주). 저자는 부록 A에서 과거 태도는 묻지 않는다고 해 놓고, 유일한 태도 변수인 호혜 문항은 1998년에 1950년대 마음을 물은 것이다."),
          "같은 등록금을 소득 심사 뒤에 줬다면 .47은 어느 쪽으로 움직였겠는가. 한국의 아동수당과 기초연금 보편화는 이 가설의 검증 자리인가", local,
          "딴 데 보는 남자친구입니다. 참전 군인이 졸업장과 소득이라는 여자친구 옆에서 신청서 한 장을 돌아봅니다. 저자는 돌아본 쪽, 받는 방식이 참여를 만들었다고 합니다. 그런데 해석 효과를 직접 잰 변수는 없습니다. 같은 등록금을 소득 심사 뒤에 줬다면 .47이 어떻게 됐을지, 어느 쪽인지 말씀해 주십시오.")
    photo("us_veterans_1945", "신청서 한 장으로 등록금과 월 75달러를 받았다. 1950년대에 모임을 더 다녔다.", "가장 가난한 집 아들에게는 효과가 없었다(Table 6·7).", '''Mettler가 하지 못한 것이 셋이다. 신뢰를 재지 않았다. 국가가 모임을 늘렸다는 것과 사람을 믿게 했다는 것은 다른 주장이다. 정책이 하나다. 보편 프로그램 하나의 양의 효과를 보였을 뿐 선별 프로그램과 나란히 놓은 적이 없다. 선별과 보편의 대비는 암시다. 구호를 거부한 아버지들의 회상과 Skocpol 인용뿐이다. 다음 논문은 같은 사람들이 선별 창구와 보편 창구를 각각 몇 번 만났는지를 세고, 종속변수를 신뢰로 바꾼다.''', "카드의 한 줄입니다. 신청서 한 장으로 등록금과 월 75달러를 받았다. 모임을 더 다녔다. 가장 가난한 집 아들에게는 효과가 없었습니다. Mettler가 못 한 것이 셋입니다. 신뢰를 안 쟀고, 정책이 하나이고, 선별과 보편의 대비는 암시입니다. 다음 논문은 그 셋을 다 합니다. 스웨덴으로 갑니다.")

    # ───────── 5 Kumlin & Rothstein ─────────
    slide("Kumlin &amp; Rothstein (2005) 연구 개요", "Making and Breaking Social Capital: The Impact of Welfare-State Institutions · <i>Comparative Political Studies</i> 38(4)",
          f'''<div class="card"><div class="headimg"><img src="{FIG["kr_head"]}" alt=""></div><dl>
<dt>질문</dt><dd>큰 복지국가가 사회자본을 밀어낸다는 통념과 스칸디나비아의 높은 신뢰가 왜 어긋나는가. 답은 크기가 아니라 설계</dd>
<dt>자료</dt><dd>서부 스웨덴(Västra Götaland) SOM 1999 우편조사. 선별 기관 7(주거수당·사회부조·장애연금·노인 돌봄 등), 보편 기관 10(보육·도서관·보건소 등). 회귀 N=2,543</dd>
<dt>설계</dt><dd>종속 = 대인신뢰 0~10 단일 문항. 선별·보편 접촉 수를 독립으로, 통제 10개(단체 가입 포함). 매개는 이용자 안에서 "받을 자격이 있는 것을 받았나" → 신뢰</dd>
<dt>결과</dt><dd>선별 접촉 1곳당 −.26***, 보편 접촉 1곳당 +.07***(Table 5). 접촉 0/1/2+ 평균 신뢰 6.7/6.0/5.7. 이용자 안에서 공정 대우 지각 → 신뢰는 6개 기관 중 4개 유의</dd>
<dt>한계</dt><dd>횡단면. "the opposite is always possible, especially when using nonexperimental data"(355)</dd></dl></div>''',
          "Table 1~7(351~358).",
          "마지막 논문입니다. 큰 복지국가는 사회자본을 밀어낸다는 통념이 있는데 스웨덴은 신뢰가 높습니다. 저자들의 답은 크기가 아니라 설계입니다. 소득을 심사하는 창구를 한 곳 더 만날 때마다 신뢰가 0.26점 내려가고, 누구나 쓰는 창구는 0.07점 올립니다. 그리고 355쪽에 이렇게 씁니다. 반대 방향은 언제나 가능하다.")
    slide("Kumlin &amp; Rothstein (2005) 연구 질문과 가설", "",
          '''<div class="ladder">
<div class="l">질문</div><div>복지국가가 호혜와 결사체를 대신해 사회자본을 밀어낸다면(crowding-out) 스칸디나비아는 왜 신뢰가 높은가. 크기 축을 버린다</div><div class="q">"it is not how big a welfare state is but what type of welfare state one is dealing with" <i>343</i></div>
<div class="l">이론적 기대</div><div>절차공정성(Lind &amp; Tyler). 선별 급여는 규정이 모호해 일선 관료(Lipsky)의 재량이 크고 신청자는 정보를 숨길 유인이 있다. 불신의 악순환. 심리 기제 셋: 관료를 못 믿으면 사람도, 받으려면 속여야 하면 남도 그럴 것, 나도 그러니 나 같은 사람도</div><div class="q">"a vicious spiral of distrust" <i>349</i></div>
<div class="l">설계 선택</div><div>전국 조사에 없는 기관별 접촉 문항이 1999년 서부 스웨덴판에 있다. 분류 기준은 "자격 판단에 관료 재량이 있는가". 통제 10개로 "tough empirical test". 매개는 이용자 안에서만</div><div class="q">"the minority who actually feel that they have been well treated … should demonstrate greater trust" <i>357</i></div>
<div class="l">결과</div><div>선별 −.26, 보편 +.07(Table 5). 제도 변수가 단체 참여(.09)보다 신뢰와 강하게 관련. 공정 대우 지각 → 신뢰는 사회부조 .30** 등</div><div class="q">"the institutional welfare-state variables appear more strongly related to social trust than participation in voluntary organizations" <i>355</i></div>
<div class="l">결론</div><div>제도는 사회자본을 만들기도 부수기도 한다. 1990년대 위기로 선별 접촉이 늘어난 것은 경고. 참여는 신뢰의 원인이라기보다 증상일 수 있다</div><div class="q">"such participation may be more a symptom of interpersonal trust than a cause" <i>362</i></div></div>''',
          "", "질문은 퍼즐입니다. 크기로는 안 풀리니 설계로 갑니다. 이론 자리에 절차공정성이 들어옵니다. 소득을 심사하는 창구에는 재량이 크고, 신청자는 숨길 유인이 있고, 그 경험이 사람 일반에 대한 불신으로 번진다는 기제 셋입니다. 결과 단에서 눈여겨볼 문장이 하나 있습니다. 제도 변수가 단체 참여보다 신뢰와 더 강하게 관련된다. Putnam과 반대입니다.")
    meas("Kumlin &amp; Rothstein (2005) 사회자본 측정", "344~356쪽", "kr_fig1", "Kumlin &amp; Rothstein 2005: 345, Figure 1과 신뢰 문항",
         [("독립변수", "선별 기관과 보편 기관 접촉 수. 선별은 욕구 심사를 거쳐 제공되는 서비스이고, 보편 급여의 예시에 아동수당이 포함(348)"),
          ("매개변수", "“받을 자격이 있는 서비스와 도움을 받았는가” 1~5점(356). 이론은 절차 공정성인데 문항은 결과 평가에 가까움"),
          ("종속변수", "대인신뢰 한 문항. “According to your opinion, to what extent can people in general be trusted?” 0~10점(345)"),
          ("한정 이유", "인과 기제가 개인 수준에서 작동하므로 집계 지표로는 검증하기 어려움(344~345). 결사체 참여를 지표에 넣으면 종속변수에 원인 변수가 섞임"),
          ("참여의 처리", "단체 가입 수(0~16)를 통제변수로 투입(Table 5, .09***). Stolle(1998)의 패널 연구를 근거로 참여가 신뢰를 높인다는 인과를 의심(346)")],
         "Freitag은 신뢰를 통제변수로 두었고 이 논문은 참여를 통제변수로 둠. Putnam(2000, 3주차)과 Fukuyama(2001)는 복지국가의 규모를 원인으로 보았고 이 논문은 제도 유형을 구분",
         "왼쪽이 345쪽 Figure 1이고, 아래 주에 신뢰 문항이 있습니다. 제목은 사회자본인데 종속변수는 대인신뢰 한 문항입니다. 저자들은 한정한 이유를 둘 듭니다. 인과 기제가 개인 수준에서 작동한다는 점, 그리고 참여를 지표에 넣으면 종속변수에 원인 변수가 섞인다는 점입니다. 그래서 참여는 통제변수로 넣었습니다. Freitag은 신뢰를 통제변수로 두었으니 두 논문의 선택이 반대입니다. 그리고 348쪽 보편 급여의 예시에 아동수당이 들어 있습니다. 첫 쟁점입니다.")
    issue("복지는 신뢰의 문제인가, 효율과 형평의 문제인가", "Kumlin &amp; Rothstein · 쟁점 1", "whynotboth",
          ["효율이냐 형평이냐로 싸우는 복지 논쟁", "신뢰라는 세 번째 기준을 올려도 되는가"],
          ("찬 · 신뢰도 기준이다", "같은 사람이 선별 창구를 한 곳 더 만날 때마다 남을 믿는 정도가 0.26점 내려가고 보편 창구는 0.07점 올린다(Table 5). 심사를 받으면 관료를 의심하고, 받으려면 속여야 하는 구조라면 남도 그럴 것이라 여기게 된다(349). 효율과 형평만으로 복지를 설계하면 이 비용이 보이지 않는다. 9주차 Fedderke는 국가가 사회자본을 만들기도 유지하기도 한다고 했다."),
          ("반 · 기준으로 세우기에는 작다", "개인 수준 −.26을 지역 평균으로 바꾸면 선별 창구를 한 번이라도 간 사람(32%) 전부가 안 갔다고 가정해도 평균 신뢰는 0.1점 남짓 오른다(발제자 계산). 스웨덴 66% 대 미국 48%의 격차는 이것으로 설명되지 않는다. Putnam(3주)이 복지국가를 쇠퇴 원인으로 의심한 것은 개인의 창구 경험이 아니라 사회 전체의 호혜 규범 이야기라, 이 자료로는 그 가설을 반박할 수 없다."),
          "한국에서 선별과 보편을 가를 때 신뢰를 세 번째 기준으로 세울 만한가. 세운다면 어떤 자료로 그 비용을 재겠는가", local,
          "둘 다 하면 안 돼요, 소녀입니다. 효율이냐 형평이냐로 싸우는 복지 논쟁에 신뢰라는 세 번째 접시를 올려도 되는가. 저자들은 올리자는 쪽입니다. 그런데 개인 수준 −.26을 지역 평균으로 바꾸면 0.1점 남짓입니다. 스웨덴과 미국의 격차를 설명하기엔 작습니다. 한국에서 선별과 보편을 가를 때 신뢰를 기준으로 세울 만한지 말씀해 주십시오.")
    slide("Kumlin &amp; Rothstein (2005) 분석 결과", "Table 5 · 대인신뢰(0~10)에 대한 OLS, N=2,543",
          f'''<div class="res"><img class="shot" style="max-height:420px" src="{FIG["kr_t5"]}" alt="Table 5"><div><div class="k">접촉 한 곳당 신뢰 변화</div><div class="bars">
<span class="lab">선별 창구(0~2)</span><div class="b o" style="width:100%"></div><span class="v">−.26***</span>
<span class="lab">보편 창구(0~8)</span><div class="b" style="width:27%"></div><span class="v">+.07***</span>
<span class="lab">단체 가입 수(0~16)</span><div class="b g" style="width:35%"></div><span class="v">+.09***</span>
<span class="lab">삶의 만족(1~4)</span><div class="b g" style="width:100%"></div><span class="v">+.63***</span></div>
<div class="k" style="margin-top:14px">Table 3 · 선별 접촉 수별 평균 신뢰</div><div class="bars">
<span class="lab">0곳 (n 2,411)</span><div class="b" style="width:100%"></div><span class="v">6.7</span>
<span class="lab">1곳 (n 829)</span><div class="b" style="width:90%"></div><span class="v">6.0</span>
<span class="lab">2곳 이상 (n 294)</span><div class="b" style="width:85%"></div><span class="v">5.7</span></div>
<p class="take">선별 창구 한 곳이 보편 창구 네 곳과 맞먹는다. 통제 중 가장 큰 것은 삶의 만족이다.<small>판정 기준 p&lt;.01 → 두 접촉 변수 모두 통과 · Adj R² .10 · 첫 접촉의 낙폭(−.7)이 둘째(−.3)보다 크다</small></p></div></div>''',
          "Kumlin &amp; Rothstein 2005: 352, 354. 비표준화 계수라 척도가 다른 변수끼리의 크기 비교는 참고용.",
          "원문 Table 5입니다. 선별 창구 한 곳당 −.26, 보편 한 곳당 +.07. 선별 하나가 보편 넷과 맞먹습니다. 통제 중 가장 큰 것은 삶의 만족 .63인데, 이 변수가 무엇을 하는지 저자들은 한 줄도 쓰지 않았습니다. 아래 Table 3을 보면 첫 접촉의 낙폭이 둘째보다 큽니다. 수가 아니라 경험 유무일 수 있습니다.")
    slide("Kumlin &amp; Rothstein (2005) 한계와 추가 검토", "",
          f'''<div class="lim"><div><div class="k">저자가 밝힌 한계</div><ul><li>횡단면. "the opposite is always possible, especially when using nonexperimental data"(355). 바로 앞 문장은 "We obviously think that our causal interpretations are correct"</li><li>보편 접촉 6곳과 8곳 이상의 차이는 비유의(각주 5). Table 4는 단조 증가가 아니다</li><li>매개 문항은 절차를 "to a certain extent"만 잡는다(356)</li><li>매개 모형은 소표본이라 통제 셋뿐(각주 7)</li><li>서부 스웨덴 한 지역, 1999년 한 시점(각주 2)</li></ul><img class="shot" style="max-height:90px;margin-top:10px" src="{FIG["kr_355"]}" alt="355쪽"></div>
<div class="me"><b>발제자의 추가 검토</b><ul><li>선별 7개 중 4개(장애인 이동·장애연금·장애 돌봄·노인 돌봄)는 자산조사가 아니라 건강·기능 심사(348). 건강은 통제에 없다. "선별 접촉 효과"의 일부는 건강 효과일 수 있다</li><li>Table 7에서 사회부조 .30**는 뚜렷하지만 주거수당은 −.02. 7개를 합친 −.26이 어느 기관에서 오는지 논문은 보여 주지 않는다</li><li>"6개 중 4개 유의"(357)에는 단서가 붙는다. 고용 .13은 p&lt;.10, 보육은 비유의</li><li>352쪽은 보편 접촉 0인 집단을 "majority"라 썼지만 실제 6%</li><li>"참여보다 강하다"(355)는 척도가 다른 비표준화 계수 비교, 검정 없음</li></ul></div></div>''',
          "",
          "저자가 자인한 것 중 첫 줄이 유명한 문장입니다. 반대 방향은 언제나 가능하다. 제가 짚는 것은 첫 줄입니다. 선별 7개 기관 중 4개는 소득 심사가 아니라 건강 심사입니다. 장애연금을 받는 사람은 건강이 나쁩니다. 그런데 건강은 통제에 없습니다. 심리 기제 셋은 '속여야 받는' 자산조사에 맞춰 쓰였는데, 장애연금 신청자가 속일 유인이 있는지는 다른 문제입니다. 이게 둘째 쟁점으로 이어집니다.")
    issue("신뢰가 낮은 사람이 선별 창구에 가는 것은 아닌가", "Kumlin &amp; Rothstein · 쟁점 2", "exit",
          ["선별 창구가 신뢰를 깎았다", "원래 못 믿던 사람이 창구에 갔다", "연구자 (355쪽: 반대 방향은 언제나 가능하다)"],
          ("찬 · 창구가 신뢰를 깎는다", "선별 창구 이용자 안에서 “받을 자격이 있는 것을 받았다”고 느낀 소수는 그렇지 않은 다수보다 신뢰가 높았다(Table 7, 사회부조 .30). 같은 창구를 갔는데 대우가 달랐다면 그 차이가 신뢰 차이를 만든 것이지 원래 신뢰 차이가 대우를 바꾼 것은 아니다. 한국은 2018년 9월 선별로 시작한 아동수당을 2019년 1월에 보편으로 바꿨으니, 같은 급여를 다른 창구로 받은 사람들이 있다."),
          ("반 · 신뢰가 낮은 사람이 창구에 간다", "자료가 한 시점 횡단면이고 저자들도 반대 방향이 언제나 가능하다고 썼다(355). 통제변수 중 가장 큰 것이 삶의 만족(.63)인데 그것이 창구 경험의 결과인지 창구에 가게 만든 원인인지 알 수 없다. 저자들은 참여에는 자기선택 논리(Stolle 1998)를 적용하면서 창구 접촉에는 적용하지 않았다. 선별 창구 7개 중 4개는 소득이 아니라 건강 심사라, 건강이 나쁜 사람이 창구에도 가고 신뢰도 낮은 것일 수 있다."),
          "어느 쪽이 더 그럴듯한가. 그 판단을 뒤집으려면 어떤 자료가 필요한가. 2부에서 각자 고를 자료에 그 변수가 있는가", local,
          "고속도로 출구입니다. 직진은 선별 창구가 신뢰를 깎았다, 출구는 원래 못 믿던 사람이 창구에 갔다. 핸들을 꺾는 차가 연구자입니다. 저자들은 355쪽에서 반대 방향이 언제나 가능하다고 썼습니다. 어느 쪽이 그럴듯한지, 그리고 그 판단을 뒤집으려면 어떤 자료가 있어야 하는지 말씀해 주십시오. 2부에서 각자 고를 자료에 그 변수가 있는지가 바로 다음 시간의 일입니다.")
    photo("sweden_office", "복지 창구에서 서류 넷을 내고 한 달을 기다렸다.", "신뢰 −.26. 보편 창구였다면 +.07(Table 5).", '''첫 논문이 943쪽에서 이 논문을 인용했다. 신뢰받는 공공기관이 사회자본을 키운다는 가설의 근거로. 그리고 950쪽에서 그 가설을 기각했다. 정부 신뢰는 7년 뒤 마을의 사회자본과 무관했다. 두 논문이 잰 것이 다르다. Krishna는 같은 제도 아래 61개 마을의 집합행동 성향을, Kumlin과 Rothstein은 한 지역 안에서 창구 종류별 개인의 신뢰를 쟀다. 다섯 편은 서로 반박한 것이 아니라 서로 다른 칸을 쟀다. 저자들이 355쪽에서 바란 것은 실험 자료였다. 한국은 2018년 9월에 소득 하위 90%만 받는 아동수당을 시작했고 2019년 1월부터 심사를 없앴다. 같은 급여를 두 해에 걸쳐 다른 창구로 받은 사람들이 복지패널에 있다.''', "카드의 마지막 한 줄입니다. 복지 창구에서 서류 넷을 내고 한 달을 기다렸다. 첫 장면으로 돌아가면, 80억 분의 1에는 이 선택지가 없습니다. 게임은 이걸 안 잽니다. 첫 논문이 이 논문을 인용하고 기각했다는 것도 말씀드려야겠습니다. 두 논문이 잰 것이 다릅니다. 다섯 편은 서로 반박한 게 아니라 다른 칸을 쟀습니다. 그리고 저자들이 바란 실험 자료에 가장 가까운 것이 한국에 있습니다. 2018년 9월 선별로 시작해 2019년 1월 보편이 된 아동수당입니다. 그 자료로 2부에서 각자 잽니다.")

    # ───────── 엔딩 ─────────
    slide("지정문헌 종속변수 비교", "",
          '''<table><tr><th>논문</th><th>종속변수</th><th>출처</th><th>신뢰의 자리</th></tr>
<tr><td>Krishna</td><td>집합행동 성향 6문항 지수 0~100</td><td>944~946</td><td>지수 안의 한 문항</td></tr>
<tr><td>Freitag</td><td>결사체 4문항 주성분, 칸톤 평균</td><td>127, 각주 2</td><td>통제변수, 다변량에서 비유의</td></tr>
<tr><td>Lowndes &amp; Wilson</td><td>Putnam 혼합 정의 + 잠재/동원</td><td>630, 638</td><td>측정 없음</td></tr>
<tr><td>Mettler</td><td>단체 가입 수(4유형) + 정치활동 6종</td><td>356</td><td>측정 없음</td></tr>
<tr><td>Kumlin &amp; Rothstein</td><td>대인신뢰 0~10 단일 문항</td><td>344, Figure 1</td><td>종속변수. 참여는 통제</td></tr></table>
<p class="take" style="margin-top:18px">결사체를 재면 국가가 만들고, 신뢰를 재면 국가가 부순다. 다섯 편이 반대 결론을 낸 것이 아니라 다른 것을 쟀다.<small>Freitag의 다변량에서 신뢰 → 참여가 비유의였다는 점을 덧붙이면 더 정확하다(Table 6 Model 4).</small></p>''',
          "",
          "다섯 편을 한 표로 접으면 이렇습니다. 셋째 열, 신뢰의 자리를 보십시오. 지수 안의 한 문항, 통제변수, 없음, 없음, 종속변수. 결사체를 재면 국가가 만들고 신뢰를 재면 국가가 부순다는 결론은 다섯 편이 서로 반박한 게 아니라 다른 것을 쟀기 때문에 나옵니다.")
    slide("토론 정리", "쟁점별로 많았던 쪽에 표시",
          '''<div class="two" style="align-items:start"><table style="font-size:14.5px"><tr><th>#</th><th>쟁점</th><th>찬</th><th>반</th></tr>
<tr><td>1</td><td>정부가 만든 모임은 사회자본을 못 키우는가</td><td class="ck">□</td><td class="ck">□</td></tr><tr><td>2</td><td>7년 변화로 역사 의존을 기각할 수 있는가</td><td class="ck">□</td><td class="ck">□</td></tr>
<tr><td>3</td><td>참여 제도가 참여를 만드는가, 그 반대인가</td><td class="ck">□</td><td class="ck">□</td></tr><tr><td>4</td><td>모임만 늘고 신뢰가 그대로면 사회자본이 만들어진 것인가</td><td class="ck">□</td><td class="ck">□</td></tr>
<tr><td>5</td><td>답하지 않을 공청회는 열지 않는 편이 나은가</td><td class="ck">□</td><td class="ck">□</td></tr></table>
<table style="font-size:14.5px"><tr><th>#</th><th>쟁점</th><th>찬</th><th>반</th></tr>
<tr><td>6</td><td>설계로 사회자본을 만들 수 있다는 믿음은 어디까지인가</td><td class="ck">□</td><td class="ck">□</td></tr><tr><td>7</td><td>국가에 빚졌다는 감정이 시민을 만드는가</td><td class="ck">□</td><td class="ck">□</td></tr>
<tr><td>8</td><td>심사 없는 급여가 심사 있는 급여보다 시민을 더 만드는가</td><td class="ck">□</td><td class="ck">□</td></tr><tr><td>9</td><td>복지는 신뢰의 문제인가, 효율과 형평의 문제인가</td><td class="ck">□</td><td class="ck">□</td></tr>
<tr><td>10</td><td>신뢰가 낮은 사람이 선별 창구에 가는 것은 아닌가</td><td class="ck">□</td><td class="ck">□</td></tr></table></div>''',
          "토론 계획서의 번호와 같다. 체크는 발제자가 토론 중 즉석에서.",
          "오늘 던진 쟁점 열 개입니다. 토론에서 갈린 쪽에 표시해 두었습니다. 반이 많았던 쟁점은 그 논문의 자료가 답을 못 낸 자리이고, 2부에서 각자 자료를 고를 때 그 변수가 있는지 확인할 자리입니다.")
    slide("주차별 주제와 11주차", "",
          '''<div class="two" style="grid-template-columns:1.2fr 1fr;align-items:start"><table style="font-size:14.5px"><tr><th>시기</th><th>무엇을 물었나</th><th>이 강좌의 문헌</th></tr>
<tr><td>1960~80s</td><td>왜 합리적 개인은 협력하지 않는가</td><td>Olson, Hardin, Coase, Ostrom (2주)</td></tr>
<tr><td>1986~2000</td><td>협력을 가능하게 하는 자본은 무엇인가</td><td>Bourdieu, Coleman, Fukuyama, Putnam (3주)</td></tr>
<tr><td>1973~2002</td><td>자원은 관계 구조의 어디에 있나</td><td>Granovetter, Burt, Lin (5주)</td></tr>
<tr><td>2002~2008</td><td>어디서 오나: 문화·개인 투자·지역·결사체</td><td>Guiso, Glaeser, Rupasingha, Wollebaek &amp; Selle (4주)</td></tr>
<tr><td>1997~2026</td><td>사회자본이 무엇을 낳나</td><td>Paxton, Boix &amp; Posner, Tavits, Knack, Knack &amp; Keefer (6~10주)</td></tr>
<tr style="background:var(--greent)"><td>2001~2007</td><td><b>국가가 사회자본을 만드나</b></td><td><b>오늘 다섯 편</b></td></tr>
<tr><td>1995~2007</td><td>신뢰는 사회자본과 같은가</td><td>Mayer, Rousseau, Hardin, Tyler, Keele (12~13주)</td></tr>
<tr><td>2000~2021</td><td>누구의 사회자본인가</td><td>Putnam 22장, Compton &amp; Meier, Gidengil (14주)</td></tr></table>
<div><div class="quote" style="font-size:15.5px">"두 개념(집단 지향과 개인 지향)은 문헌에 둘 다 있지만, 둘 사이에 다리가 놓인 적이 없고, 같은 개념을 가리키는지도 분명치 않다."<small>Krishna 2007: 942, 각주 2 (발제자 번역)</small></div><p style="font-size:15px;margin-top:14px;line-height:1.6">오늘 다섯 편은 전부 집단 지향, Putnam 쪽이다. 12~13주차의 신뢰 문헌은 그 안에서 신뢰만 떼어 묻고, 14주차는 누구의 것인지를 묻는다. 오늘 쟁점 4·9·10이 그쪽으로 간다.</p></div></div>''',
          "",
          "11주차까지의 지도입니다. 오늘이 초록 줄입니다. 2주차 질문에서 시작해 3주차에 이름이 붙고, 6주차부터는 원인이었던 사회자본이 오늘 처음 결과가 됐습니다. 다음 주부터는 그 안에서 신뢰만 떼어 묻습니다. 오늘 쟁점 중 신뢰를 건드린 셋이 그쪽으로 넘어갑니다.")
    photo("korea_seoul_street", "2부에서는 각자 국내 자료로 같은 모형을 만든다.", "다섯 편 중 넷이 한 나라 한 시점 자료였다. 국내 조사 8종, 전체 문항 5,636개, 선행연구 7,690편.", "각자 국내 자료에서 창구 변수 하나와 신뢰 문항 하나를 고르면, 그 사이에 무엇을 통제할지가 오늘 쟁점 9와 10이다. 5-jihwan.github.io/week11-seminar/model/canvas.html · 노트북 권장", "교수님 설명 뒤 2부입니다. 다섯 편 중 넷이 한 나라 한 시점 자료였습니다. 이제 각자 국내 자료에서 창구 변수 하나와 신뢰 문항 하나를 고릅니다. 그 사이에 무엇을 통제할지가 방금 토론한 아홉 번째, 열 번째 쟁점입니다. 교수님.", "2부로")
    # ───────── 부록 ─────────
    for t, sub, key, cap in [("Krishna Table 2 원문", "949쪽", "krishna_t2", "N 61/60, R² .23/.79"), ("Freitag Table 7 원문", "142쪽 · 공선 변수를 분리한 네 모형", "freitag_t7", "M1 제도 셋 R² .75 · M2 도시화·언어권 .79 · M3 직접민주주의·도시화 .77 · M4 합의·지방자치·언어권 .78"),
                             ("Mettler Table 7 원문", "362쪽 · 정치참여, 생활수준 × 이용 상호작용", "mettler_t7", "저 .17(.57) · 저중 .40(.03) · 중 .27(.13) · 중고·고 1.22(.00)"), ("Kumlin &amp; Rothstein Table 3 원문", "352쪽 · 선별 접촉 수별 평균 신뢰", "kr_t3", "0/1/2+ → 6.7/6.0/5.7, r=−.14"),
                             ("Kumlin &amp; Rothstein Table 7 원문", "358쪽 · 기관별 이용자 안에서 공정 대우 지각 → 신뢰", "kr_t7", "보건 .31*** · 보육 .12 · 교통 .27*** · 사회부조 .30** · 고용 .13* · 주거수당 −.02")]:
        slide(t, sub, f'<div style="display:flex;justify-content:center;height:470px"><img class="shot" src="{FIG[key]}" alt="{t}"></div>', cap, "", ap=True)

    html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>국가는 사회자본을 만들 수 있는가</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"><script>function noimg(m){{const w=m.closest('.mw');w.style.display='none';w.nextElementSibling.style.display='grid';}}</script><style>{face(''.join(h for h, _ in S) + '국가는 사회자본을 만들 수 있는가 ←/→ 이동 · N 노트 · F 전체화면 노트 없음 A0123456789')}{CSS.replace('__FAMILY__', FAMILY)}</style></head><body><div id="stage">
{"".join(h for h, _ in S)}
</div><div id="notes"></div><div id="help">←/→ 이동 · N 노트 · F 전체화면</div>
<script>
const S=[...document.querySelectorAll('.slide')];let i=0;const N=document.getElementById('notes');
function fit(){{const sc=Math.min(innerWidth/1280,innerHeight/720);S.forEach(s=>s.style.transform=`scale(${{sc}})`);}}
function grow(s){{const bd=s.querySelector('.bd'),n=s.querySelector('.in');if(!bd||!n||n.dataset.z||s.querySelector('.map')||document.readyState!=='complete')return;let z=1.3;for(;z>1.001;z-=.05){{n.style.zoom=z;if(n.getBoundingClientRect().height<=bd.getBoundingClientRect().height&&n.scrollWidth<=n.clientWidth+1)break;}}n.style.zoom=n.dataset.z=Math.max(1,z).toFixed(2);}}
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
