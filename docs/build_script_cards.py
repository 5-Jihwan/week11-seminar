# -*- coding: utf-8 -*-
"""발표자 노트북용 대본 카드(자립 HTML 한 파일). 장마다 카드 하나, 덱 장 번호와 같다.
원본: deck/part1_script.json(리스트, 순서=장 번호), deck/part2_script.json(제목→대본, 순서=장 번호).
실행: python docs/build_script_cards.py [출력 경로]"""
import html, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "..", "deck")
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, "대본_카드.html")
p1 = json.load(open(os.path.join(D, "part1_script.json"), encoding="utf-8"))
p2 = json.load(open(os.path.join(D, "part2_script.json"), encoding="utf-8"))


def paras_of(text):  # 2부 대본은 문자열 하나. 쉼 지시만 따로 떼어 낸다
    out_ = []
    for chunk in re.split(r"\s*(\(잠깐 쉬고\))\s*", text):
        if chunk.strip(): out_.append(chunk.strip())
    return out_


main1 = [x for x in p1 if not x["title"].endswith("원문")]; app1 = [x for x in p1 if x["title"].endswith("원문")]
decks = {"1부": [{"no": str(i + 1), "t": x["title"], "p": x["paras"]} for i, x in enumerate(main1)] + [{"no": f"A{i + 1}", "t": x["title"], "p": x["paras"]} for i, x in enumerate(app1)],
         "2부": [{"no": str(i + 1), "t": t, "p": paras_of(s)} for i, (t, s) in enumerate(p2.items())]}
assert len(decks["1부"]) == 70 and len(decks["2부"]) == 9
DATA = json.dumps(decks, ensure_ascii=False)
doc = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>11주차 대본 카드</title><style>
:root{--bg:#f4f6f9;--card:#fff;--ink:#15203a;--sub:#5a6577;--line:#dfe4ec;--navy:#072A60;--cue:#eef1f5;--fs:23px}
:root[data-theme=dark]{--bg:#0f141c;--card:#171e29;--ink:#e6e9ef;--sub:#9aa5b5;--line:#2a3342;--navy:#9fbaf0;--cue:#1f2733}
*{box-sizing:border-box}html,body{margin:0;height:100%}body{background:var(--bg);color:var(--ink);font-family:Pretendard,"Malgun Gothic","Apple SD Gothic Neo",sans-serif;display:flex;flex-direction:column}
header{display:flex;align-items:center;gap:10px;padding:10px 18px;border-bottom:1px solid var(--line);background:var(--card);flex-wrap:wrap}
header .tab{border:1px solid var(--line);background:none;color:var(--ink);padding:6px 14px;border-radius:6px;font:inherit;font-size:14px;cursor:pointer}header .tab.on{background:var(--navy);border-color:var(--navy);color:var(--card)}
header .pos{font-size:14px;color:var(--sub);margin-left:6px}header .sp{flex:1}header .btn{border:1px solid var(--line);background:none;color:var(--sub);padding:5px 10px;border-radius:6px;font:inherit;font-size:13px;cursor:pointer}
main{flex:1;overflow:auto;padding:22px 18px 10px;display:flex;justify-content:center}
.card{width:100%;max-width:1100px;background:var(--card);border:1px solid var(--line);border-top:4px solid var(--navy);border-radius:8px;padding:26px 34px 30px;align-self:flex-start}
.card .no{font-size:15px;color:var(--sub)}.card h1{margin:4px 0 18px;font-size:calc(var(--fs) + 3px);line-height:1.4;color:var(--navy);word-break:keep-all}
.card p{margin:0 0 16px;font-size:var(--fs);line-height:1.85;word-break:keep-all}
.card .cue{display:inline-block;margin:2px 0 16px;padding:5px 12px;background:var(--cue);color:var(--sub);border-radius:5px;font-size:calc(var(--fs) * .68);line-height:1.5}
footer{display:flex;align-items:center;gap:12px;padding:10px 18px;border-top:1px solid var(--line);background:var(--card);font-size:14px;color:var(--sub)}
footer .nx{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}footer button{border:1px solid var(--line);background:none;color:var(--ink);padding:6px 16px;border-radius:6px;font:inherit;cursor:pointer}
#list{display:none;position:fixed;inset:54px 0 0 0;background:var(--bg);overflow:auto;padding:14px 18px 40px;z-index:3}#list.on{display:block}
#list .grid{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px}
#list button{text-align:left;border:1px solid var(--line);background:var(--card);color:var(--ink);padding:10px 12px;border-radius:6px;font:inherit;font-size:14px;line-height:1.4;cursor:pointer}#list button b{color:var(--navy);margin-right:6px}#list button.on{border-color:var(--navy)}
@media (max-width:700px){.card{padding:18px 18px 22px}:root{--fs:19px}}
</style></head><body>
<header><button class="tab" data-d="1부">1부</button><button class="tab" data-d="2부">2부</button><span class="pos" id="pos"></span><span class="sp"></span>
<button class="btn" id="bl" title="L">목록</button><button class="btn" id="bm" title="-">글자 −</button><button class="btn" id="bp" title="+">글자 +</button><button class="btn" id="bd" title="D">밝기</button></header>
<main><article class="card" id="card"></article></main>
<footer><button id="prev">← 이전</button><span class="nx" id="nx"></span><button id="next">다음 →</button></footer>
<div id="list"><div class="grid" id="grid"></div></div>
<script>
const DECKS=__DATA__;const $=id=>document.getElementById(id);const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'})[c]);
const st=(()=>{try{return JSON.parse(localStorage.getItem('w11cards')||'{}')}catch(e){return{}}})();let deck=st.deck||'1부',i=st.i||0,fs=st.fs||23;
const save=()=>{try{localStorage.setItem('w11cards',JSON.stringify({deck,i,fs,theme:document.documentElement.dataset.theme||''}))}catch(e){}};
if(st.theme)document.documentElement.dataset.theme=st.theme;
function render(){const L=DECKS[deck];i=Math.max(0,Math.min(i,L.length-1));const c=L[i];
 document.documentElement.style.setProperty('--fs',fs+'px');
 document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('on',b.dataset.d===deck));
 $('card').innerHTML=`<div class="no">${deck} · ${/^A/.test(c.no)?'부록 '+c.no:c.no+'장'}</div><h1>${esc(c.t)}</h1>`+c.p.map(p=>p.startsWith('(')?`<div><span class="cue">${esc(p)}</span></div>`:`<p>${esc(p)}</p>`).join('');
 $('pos').textContent=`${i+1} / ${L.length}`;const n=L[i+1];$('nx').textContent=n?`다음 ${/^A/.test(n.no)?'부록 '+n.no:n.no+'장'} · ${n.t}`:'마지막 장';
 $('grid').innerHTML=L.map((x,k)=>`<button data-k="${k}" class="${k===i?'on':''}"><b>${x.no}</b>${esc(x.t)}</button>`).join('');
 document.querySelector('main').scrollTop=0;save();}
const go=d=>{i+=d;render();};
$('prev').onclick=()=>go(-1);$('next').onclick=()=>go(1);
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{if(deck!==b.dataset.d){deck=b.dataset.d;i=0;render();}});
$('bl').onclick=()=>$('list').classList.toggle('on');$('grid').onclick=e=>{const b=e.target.closest('button');if(b){i=+b.dataset.k;$('list').classList.remove('on');render();}};
$('bm').onclick=()=>{fs=Math.max(15,fs-2);render();};$('bp').onclick=()=>{fs=Math.min(40,fs+2);render();};
$('bd').onclick=()=>{const r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'':'dark';save();};
addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return;const k=e.key;
 if(k==='ArrowRight'||k===' '||k==='PageDown'){e.preventDefault();go(1);}else if(k==='ArrowLeft'||k==='PageUp'){e.preventDefault();go(-1);}
 else if(k==='l'||k==='L')$('list').classList.toggle('on');else if(k==='Escape')$('list').classList.remove('on');
 else if(k==='+'||k==='=')$('bp').click();else if(k==='-')$('bm').click();else if(k==='d'||k==='D')$('bd').click();
 else if(k==='1'||k==='2'){deck=k+'부';i=0;render();}else if(k==='Home'){i=0;render();}else if(k==='End'){i=1e9;render();}});
render();
</script></body></html>""".replace("__DATA__", DATA)
open(out, "w", encoding="utf-8").write(doc); print(out, len(doc) // 1024, "KB · 1부", len(decks["1부"]), "장 · 2부", len(decks["2부"]), "장")
