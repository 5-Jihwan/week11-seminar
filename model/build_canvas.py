# -*- coding: utf-8 -*-
"""2부 캔버스 데모(Galpi 방식): 팔레트 → 역할 고르기 → IV|MV|DV 열 자동 배치 → 탭으로 잇기 → 3초 멈추면 검증 패널(오류·경고·계보·리뷰·가설)
→ 노드 탭하면 '왜 이 역할인가' + 문항 고르기. catalog·규칙은 build_index.py와 같은 것을 심는다(file://로 열림, localStorage 저장).
실행: python model/build_canvas.py → model/canvas.html"""
import csv, json, os, sys, importlib.util
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
# 선행연구(corpus/studies.csv, 규칙 코딩·미검수). 화면에 필요한 칸만 심는다. 수업판은 verified=TRUE만 남긴다(가드레일 2).
STUDIES = [{"id": r["id"], "au": (r["authors"].split(",")[0].split(" ")[-1] if r["authors"] else "") + (" 외" if "," in r["authors"] else ""), "y": r["year"], "t": r["title"], "j": r["journal"],
            "link": r["link"], "comps": [c for c in r["dv_components"].split("|") if c], "unit": r["unit"], "inst": r["iv_institution"] == "Y", "reg": r["iv_region"] == "Y",
            "net": r["iv_network"] == "Y", "med": r["mediator"] == "Y", "lin": r["lineage"], "line": r["measure_line"], "design": r["design"], "ok": r["verified"] == "TRUE"}
           for r in csv.DictReader(open(os.path.join(HERE, "..", "corpus", "studies.csv"), encoding="utf-8-sig")) if r["dv_components"]]
spec = importlib.util.spec_from_file_location("bi", os.path.join(HERE, "build_index.py"))
# build_index.py는 import 시 index.html을 다시 쓴다(부작용 무해). REVIEWS·COND·PAPERS·CAT를 재사용.
bi = importlib.util.module_from_spec(spec); spec.loader.exec_module(bi)

HTML = r"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>연구모형 캔버스</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css">
<style>
:root{--ink:#15203a;--sub:#5a6577;--line:#e2e6ec;--navy:#072A60;--tint:#e9eef6;--green:#4F7F1C;--gtint:#f0f7e6;--orange:#D9640F;--otint:#fdf1e7;--paper:#fafaf7}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:#fff;color:var(--ink);font-family:Pretendard,"Noto Sans KR",sans-serif;font-size:15px;line-height:1.5;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:2px solid var(--navy)}
.top b{color:var(--navy)}.top input{font:inherit;border:1px solid var(--line);padding:4px 8px;width:110px}.top span{color:var(--sub);font-size:12.5px;margin-left:auto}
.wrap{flex:1;display:flex;min-height:0}
.pal{width:230px;border-right:1px solid var(--line);overflow-y:auto;padding:10px}
.pal h4{margin:10px 0 6px;font-size:12px;color:var(--sub);font-weight:700;letter-spacing:.02em}
.card{border:1px solid var(--line);border-left:3px solid var(--navy);padding:7px 9px;margin:0 0 6px;cursor:pointer;background:#fff;font-size:13.5px;user-select:none}
.card small{display:block;color:var(--sub);font-size:11.5px}.card.used{opacity:.45;border-left-color:var(--line)}
.cv{flex:1;position:relative;background:var(--paper);background-image:radial-gradient(circle at 1px 1px,rgba(60,64,75,.16) 1px,transparent 0);background-size:20px 20px;overflow:hidden}
svg{width:100%;height:100%;display:block}
.node{cursor:pointer}.node rect{fill:#fff;stroke:var(--navy);stroke-width:1.3}.node.dv rect{fill:var(--tint);stroke-width:1.8}.node.cv rect{stroke:var(--sub);stroke-dasharray:3 2}.node.sel rect{stroke-width:3}.node.bad rect{stroke:var(--orange)}
.node text{font-size:12.5px;fill:var(--ink)}.node .r{font-size:10px;fill:var(--sub)}.node .s{font-size:10px;fill:var(--green)}
.edge{stroke:var(--navy);stroke-width:1.4;fill:none}.edge.bad{stroke:var(--orange);stroke-dasharray:4 3}
.bar{position:absolute;top:10px;left:50%;transform:translateX(-50%);background:var(--navy);color:#fff;font-size:12.5px;padding:5px 12px}
.hint{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#9aa2ae;font-size:14px;text-align:center;pointer-events:none;padding:20px}
.badge{position:absolute;right:12px;bottom:12px;background:#fff;border:2px solid var(--navy);color:var(--navy);font:inherit;font-size:13px;font-weight:700;padding:7px 14px;cursor:pointer}
.badge.bad{border-color:var(--orange);color:var(--orange)}
.panel{position:relative;width:340px;flex:none;background:#fff;border-left:1px solid var(--line);overflow-y:auto;padding:14px 16px 80px;display:none;z-index:5}
.panel.on{display:block}.panel h3{margin:0 0 4px;font-size:16px;color:var(--navy)}.panel h3::before{content:"";display:block;width:28px;height:3px;background:#8DC63F;margin-bottom:8px}
.panel .x{position:absolute;right:10px;top:8px;border:0;background:none;font-size:18px;cursor:pointer;color:var(--sub)}
.iss{border-left:3px solid var(--navy);padding:6px 10px;margin:8px 0;font-size:13.5px;background:#fff}.iss.err{border-left-color:var(--orange);background:var(--otint)}.iss.warn{border-left-color:var(--orange)}.iss.ok{border-left-color:var(--green);background:var(--gtint)}
.iss small{display:block;color:var(--sub);font-size:12.5px;margin-top:2px}.iss b.w{color:var(--navy)}
.k{font-size:12.5px;color:var(--sub)}.sec{margin-top:16px;font-size:12.5px;color:var(--sub);font-weight:700}
.opt{display:block;width:100%;text-align:left;background:#fff;border:1px solid var(--line);border-left:3px solid var(--line);padding:8px 10px;margin:0 0 6px;font:inherit;font-size:13px;cursor:pointer}
.opt.sel{border-left-color:var(--navy);background:var(--tint)}.opt.grey{color:#9aa2ae;border-style:dashed}.opt small{display:block;color:var(--sub);font-size:11.5px}
.srv{margin:10px 0 4px;font-size:12.5px;color:var(--navy);font-weight:700}
.pop{position:absolute;background:#fff;border:1px solid var(--navy);padding:10px 12px;z-index:6;width:230px}.pop b{display:block;margin-bottom:6px;font-size:13px}
.pop button{display:block;width:100%;text-align:left;font:inherit;font-size:13px;padding:6px 8px;margin:0 0 4px;border:1px solid var(--line);background:#fff;cursor:pointer}.pop button:hover{background:var(--tint)}
.btn{font:inherit;padding:9px 16px;border:1px solid var(--navy);background:var(--navy);color:#fff;cursor:pointer}.btn.sec2{background:#fff;color:var(--navy)}
input.q{width:100%;font:inherit;font-size:13.5px;padding:8px;border:1px solid var(--line);margin:6px 0}
.agg .b{display:flex;align-items:center;gap:8px;margin:3px 0;font-size:12.5px}.agg i{display:block;height:10px;background:var(--navy)}.agg span{width:130px}
.foot{font-size:11px;color:var(--sub);text-align:center;padding:3px;border-top:1px solid var(--line)}
@media (max-width:720px){.pal{position:absolute;left:0;top:0;bottom:0;z-index:4;background:#fff;transform:translateX(-100%);transition:transform .2s;width:240px}.pal.on{transform:none}.paltog{display:inline-block}.panel{position:absolute;right:0;top:0;bottom:0;width:92%}.wrap{position:relative}}
.paltog{display:none;font:inherit;font-size:12.5px;border:1px solid var(--navy);background:#fff;color:var(--navy);padding:3px 8px;cursor:pointer}
</style></head><body>
<div class="top"><b>연구모형 캔버스</b><input id="nick" placeholder="별명" maxlength="12"><button class="paltog" id="paltog">개념</button><span id="status">개념을 눌러 캔버스에 놓으십시오</span></div>
<div class="wrap">
<aside class="pal" id="pal"></aside>
<div class="cv" id="cv">
<svg id="svg" viewBox="0 0 640 400" preserveAspectRatio="xMidYMid meet"><defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#072A60"/></marker><marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#D9640F"/></marker></defs>
<g id="edges"></g><g id="nodes"></g></svg>
<div class="hint" id="hint">왼쪽 개념을 누르면 역할을 묻고 자리에 놓습니다.<br>노드를 누르고 다른 노드를 누르면 화살표가 생깁니다.<br>3초 멈추면 검증 패널이 열립니다.</div>
<div class="bar" id="bar" style="display:none"></div>
<button class="badge" id="badge" style="display:none"></button>
<div class="pop" id="pop" style="display:none"></div>
</div>
<div class="panel" id="npanel"><button class="x" data-x="npanel">×</button><div id="nbody"></div></div>
<div class="panel" id="vpanel"><button class="x" data-x="vpanel">×</button><div id="vbody"></div></div>
</div>
<div class="foot">선택은 이 수업 안에서만 쓰고 끝나면 지웁니다 · 계수는 계산하지 않습니다 · 모형 그림은 행정학 관행 형식</div>
<script>
const CAT=__CAT__, REV=__REV__, PAPERS=__PAPERS__, STUDIES=__STUDIES__, SAVE_URL="", DEMO=true; // DEMO=false면 verified만
const S=CAT.surveys, C=CAT.concepts, IT=CAT.items;
const ROLE={DV:"종속변수",IV:"독립변수",MV:"매개변수",CV:"통제변수"};
const SCDEF={id:"sc_def",label:"사회자본(내 정의)",role:"dv",paper_measure:"한 조사의 문항을 묶어 직접 정의한다. 1부 다섯 편도 각자 다르게 정의했다"};
const COMP_OF={trust_general:"generalized_trust",trust_social:"generalized_trust",trust_neighbor:"neighbor_trust",trust_institution:"institutional_trust",participation:"participation",volunteer_donate:"volunteer_donate",network_reciprocity:"reciprocity",political_participation:"political_participation"};
const COMP_KO={generalized_trust:"일반신뢰",institutional_trust:"기관신뢰",neighbor_trust:"이웃 신뢰",participation:"단체 참여",volunteer_donate:"봉사·기부",network:"연결망",reciprocity:"호혜",political_participation:"정치 참여"};
const PAL=[["종속변수 후보",[SCDEF,...C.filter(c=>c.role==="dv")]],["독립변수 후보",C.filter(c=>c.role==="iv")],["매개변수 후보",C.filter(c=>c.role==="med")],["지역·통제",[...C.filter(c=>c.role==="ctl"),{id:"demo",label:"개인 특성(연령·교육·소득·고용)",paper_measure:"모든 모형에 들어감"}]]];
let st={nodes:[],edges:[],sel:null,q:"",nick:""}, idle=null, openNode=null;
const $=id=>document.getElementById(id), cname=id=>id==="sc_def"?SCDEF.label:(C.find(c=>c.id===id)||{label:"개인 특성(연령·교육·소득·고용)"}).label;
const availFor=(concept,survey)=>IT.filter(i=>i.concept===concept&&i.survey===survey&&!(concept==='region'&&/확인 필요|소속감/.test(i.question||'')));
const nodeItems=n=>n.concept==="sc_def"?(n.items||[]):(n.item!=null?[n.item]:[]);
const surveyOf=()=>{const d=st.nodes.find(n=>n.role==="DV"&&nodeItems(n).length);return d?IT[nodeItems(d)[0]].survey:null};
const dvComps=()=>{const d=st.nodes.find(n=>n.role==="DV");return d?[...new Set(nodeItems(d).map(k=>COMP_OF[IT[k].concept]).filter(Boolean))]:[]};
const defLine=()=>{const d=st.nodes.find(n=>n.role==="DV"&&n.concept==="sc_def");if(!d||!nodeItems(d).length)return'';const its=nodeItems(d).map(k=>IT[k]);const cs={};its.forEach(i=>(cs[i.concept]=cs[i.concept]||0,cs[i.concept]++));
  return `당신의 사회자본 = ${sname(its[0].survey)} ${its[0].wave||''} · ${Object.entries(cs).map(([c,n])=>cname(c)+(n>1?' '+n+'문항':'')).join(' + ')} · ${[...new Set(its.map(i=>i.unit).filter(Boolean))].join('·')||'개인'} 단위`};
const sname=k=>(S[k]||{}).name||k;
/* ── 팔레트 ── */
function palette(){$('pal').innerHTML=PAL.map(([h,arr])=>`<h4>${h}</h4>`+arr.map(c=>`<div class="card ${st.nodes.some(n=>n.concept===c.id)?'used':''}" data-c="${c.id}">${c.label}<small>${c.paper_measure||''}</small></div>`).join('')).join('');}
$('pal').onclick=e=>{const d=e.target.closest('.card');if(!d||d.classList.contains('used'))return;const c=d.dataset.c;
  const conc=c==="sc_def"?SCDEF:C.find(x=>x.id===c);const roles=c==="demo"?["CV"]:c==="sc_def"?["DV"]:conc.role==="dv"?["DV","IV"]:conc.role==="iv"?["IV","MV"]:conc.role==="med"?["MV","DV","IV"]:["IV","CV"];
  if(roles.length===1)return addNode(c,roles[0]);
  const r=d.getBoundingClientRect(),cv=$('cv').getBoundingClientRect();const p=$('pop');p.style.display='block';p.style.left=Math.max(8,Math.min(r.right-cv.left+6,cv.width-240))+'px';p.style.top=Math.max(8,r.top-cv.top)+'px';
  p.innerHTML=`<b>${conc.label}</b><span class="k">이 개념의 역할</span>`+roles.map(x=>`<button data-r="${x}">${x} · ${ROLE[x]}</button>`).join('');
  p.onclick=ev=>{const b=ev.target.closest('button');if(!b)return;p.style.display='none';addNode(c,b.dataset.r);};
  $('pal').classList.remove('on');};
function addNode(concept,role){if(role==="DV"&&st.nodes.some(n=>n.role==="DV")){$('status').textContent='종속변수는 하나만. 기존 노드를 지우고 놓으십시오.';return;}
  st.nodes.push({id:concept+'-'+Date.now(),concept,role,item:null,items:[]});st.sel=null;touch();const n=st.nodes[st.nodes.length-1];if(role!=="CV")openNodePanel(n.id);}
/* ── 배치·그리기 ── */
function layout(){const col={IV:60,MV:250,DV:440,CV:60},cnt={};st.nodes.forEach(n=>{const k=n.role;cnt[k]=(cnt[k]||0)+1;n.x=col[k];n.y=(k==="CV"?250:40)+(cnt[k]-1)*62;});}
function draw(){layout();$('hint').style.display=st.nodes.length?'none':'flex';const sv=surveyOf();
  $('nodes').innerHTML=st.nodes.map(n=>{const ks=nodeItems(n),it=ks.length?IT[ks[0]]:null,bad=it&&sv&&it.survey!==sv,cls=`node ${n.role.toLowerCase()} ${st.sel===n.id?'sel':''} ${bad?'bad':''}`;
    const lab=n.concept==="sc_def"&&ks.length?`내 정의 · ${ks.length}문항`:cname(n.concept),l1=lab.length>16?lab.slice(0,15)+'…':lab;return `<g class="${cls}" data-id="${n.id}" transform="translate(${n.x},${n.y})"><rect width="150" height="46" rx="2"/><text x="8" y="17" class="r">${n.role} · ${ROLE[n.role]}</text><text x="8" y="34">${l1}</text>${it?`<text x="142" y="17" class="s" text-anchor="end">${sname(it.survey).slice(0,8)}</text>`:n.role==="CV"?'':`<text x="142" y="17" class="s" text-anchor="end" fill="#D9640F">문항 없음</text>`}</g>`}).join('');
  $('edges').innerHTML=st.edges.map(e=>{const a=st.nodes.find(n=>n.id===e.from),b=st.nodes.find(n=>n.id===e.to);if(!a||!b)return'';const rev=a.role==="DV"||(a.role==="MV"&&b.role==="IV");
    const x1=a.x+150,y1=a.y+23,x2=b.x,y2=b.y+23;return `<path class="edge ${rev?'bad':''}" d="M${x1},${y1} C${x1+40},${y1} ${x2-40},${y2} ${x2},${y2}" marker-end="url(#${rev?'ahb':'ah'})"/>`}).join('');
  palette();const iss=validate();const errs=iss.filter(i=>i.l==='err').length,warns=iss.filter(i=>i.l==='warn').length;
  $('badge').style.display=st.nodes.length?'block':'none';$('badge').className='badge'+(errs?' bad':'');$('badge').textContent=errs||warns?`${errs?errs+' 오류':''}${errs&&warns?' · ':''}${warns?warns+' 경고':''} ›`:'검증 ›';
  $('bar').style.display=st.sel?'block':'none';$('bar').textContent='이을 노드를 누르십시오 · 같은 노드를 다시 누르면 취소';}
$('svg').onclick=e=>{const g=e.target.closest('.node');if(!g){st.sel=null;draw();return;}const id=g.dataset.id;
  if(!st.sel){st.sel=id;draw();openNodePanel(id);return;}
  if(st.sel===id){st.sel=null;draw();return;}
  if(!st.edges.some(x=>x.from===st.sel&&x.to===id))st.edges.push({from:st.sel,to:id});st.sel=null;closePanels();touch();};
function touch(){draw();clearTimeout(idle);if(st.nodes.length>=2&&st.edges.length>=1)idle=setTimeout(()=>{if(!$('npanel').classList.contains('on'))openValidator();},3000);}
/* ── 노드 패널: 왜 이 역할인가 + 문항 ── */
function openNodePanel(id){const n=st.nodes.find(x=>x.id===id);if(!n)return;openNode=id;$('vpanel').classList.remove('on');$('npanel').classList.add('on');const sv=surveyOf();
  if(n.concept==="sc_def")return defPanel(n,sv);const conc=C.find(c=>c.id===n.concept);
  let items=IT.filter(i=>i.concept===n.concept&&!(n.concept==='region'&&/확인 필요|소속감/.test(i.question||'')));const bys={};items.forEach(i=>(bys[i.survey]=bys[i.survey]||[]).push(i));
  const why=n.role==="DV"?`1부에서 이 개념을 종속변수로 잰 것: ${conc.paper_measure}`:n.role==="MV"?`1부에서 매개로 쓴 자리: ${conc.paper_measure}`:`1부에서 원인 자리에 둔 것: ${conc.paper_measure}`;
  $('nbody').innerHTML=`<h3>${cname(n.concept)}</h3><span class="k">${n.role} · ${ROLE[n.role]}</span><div class="iss">${why}</div>
  ${conc.role==="dv"&&n.role!=="DV"?`<div class="iss warn">1부에서는 종속변수였던 개념입니다. 원인 자리에 두면 설계가 바뀝니다(Krishna의 정부 신뢰처럼).<small>어느 쪽에 두느냐가 설계입니다.</small></div>`:''}
  <div class="sec">이 개념을 묻는 문항 ${sv?`<span class="k">· 자료는 ${sname(sv)}</span>`:''}</div>`+
  (items.length?Object.entries(bys).map(([s,arr])=>`<div class="srv">${sname(s)} <span class="k">· ${S[s].unit}</span></div>`+arr.map(i=>{const k=IT.indexOf(i),grey=sv&&s!==sv&&n.role!=="DV";return `<button class="opt ${n.item===k?'sel':''} ${grey?'grey':''}" data-k="${k}">${i.question}<small>${i.wave||''} · ${i.scale||''}</small></button>`}).join('')).join(''):`<div class="iss err">이 개념을 묻는 문항이 메뉴에 없습니다.</div>`)+
  `<div class="sec"></div><button class="btn sec2" id="del">이 노드 지우기</button>`;
  $('nbody').onclick=e=>{const b=e.target.closest('.opt');if(b){if(b.classList.contains('grey')){const i=IT[+b.dataset.k];b.insertAdjacentHTML('afterend',`<div class="iss err">이 두 문항은 같은 사람에게 없습니다. ${cname(st.nodes.find(x=>x.role==="DV").concept)}은 ${sname(sv)}에, 이 문항은 ${sname(i.survey)}에 있습니다.</div>`);return;}
      n.item=+b.dataset.k;closePanels();touch();return;}
    if(e.target.id==='del'){st.nodes=st.nodes.filter(x=>x.id!==id);st.edges=st.edges.filter(x=>x.from!==id&&x.to!==id);st.sel=null;closePanels();touch();}};}
/* ── 정의 노드 패널: 조사 고르기 → 그 조사의 사회자본 문항을 묶기 ── */
function defPanel(n,sv){const dvC=C.filter(c=>c.role==="dv").map(c=>c.id);const its=IT.filter(i=>dvC.includes(i.concept));const cur=n.items.length?IT[n.items[0]].survey:null;
  const head=`<h3>${SCDEF.label}</h3><span class="k">DV · 종속변수</span><div class="iss">${SCDEF.paper_measure}<small>1부: Krishna 6문항 지수 / Freitag 결사체 4문항 / Mettler 단체 가입 수 / K&R 대인신뢰 0~10</small></div>`;
  if(!cur){const svs=[...new Set(its.map(i=>i.survey))];$('nbody').innerHTML=head+`<div class="sec">먼저 조사를 고르십시오. 한 조사 안의 문항만 묶을 수 있습니다.</div>`+svs.map(s=>`<button class="opt" data-s="${s}">${sname(s)}<small>${S[s].unit} · 사회자본 문항 ${its.filter(i=>i.survey===s).length}개 · ${S[s].why||''}</small></button>`).join('');
    $('nbody').onclick=e=>{const b=e.target.closest('.opt');if(b){n._survey=b.dataset.s;defPanel2(n);}};return;}
  defPanel2(n);}
function defPanel2(n){const s=n._survey||IT[n.items[0]].survey;const dvC=C.filter(c=>c.role==="dv").map(c=>c.id);const its=IT.filter(i=>dvC.includes(i.concept)&&i.survey===s);const byc={};its.forEach(i=>(byc[i.concept]=byc[i.concept]||[]).push(i));
  $('nbody').innerHTML=`<h3>${SCDEF.label}</h3><span class="k">DV · ${sname(s)} · ${S[s].unit}</span>`+(n.items.length?`<div class="iss ok">${defLine()}</div>`:`<div class="iss warn">문항을 하나 이상 고르면 정의 문장이 생깁니다.</div>`)+
    Object.entries(byc).map(([c,arr])=>`<div class="srv">${cname(c)}</div>`+arr.map(i=>{const k=IT.indexOf(i);return `<button class="opt ${n.items.includes(k)?'sel':''}" data-k="${k}">${i.question}<small>${i.wave||''} · ${i.scale||''}</small></button>`}).join('')).join('')+
    `<div class="sec"></div><button class="btn sec2" id="resv">조사 바꾸기</button> <button class="btn sec2" id="del">이 노드 지우기</button>`;
  $('nbody').onclick=e=>{const b=e.target.closest('.opt');if(b){const k=+b.dataset.k;n.items=n.items.includes(k)?n.items.filter(x=>x!==k):[...n.items,k];draw();defPanel2(n);clearTimeout(idle);return;}
    if(e.target.id==='resv'){n.items=[];n._survey=null;draw();defPanel(n,null);return;}
    if(e.target.id==='del'){st.nodes=st.nodes.filter(x=>x.id!==n.id);st.edges=st.edges.filter(x=>x.from!==n.id&&x.to!==n.id);st.sel=null;closePanels();touch();}};}
function closePanels(){$('npanel').classList.remove('on');$('vpanel').classList.remove('on');openNode=null;}
document.querySelectorAll('.x').forEach(b=>b.onclick=()=>{$(b.dataset.x).classList.remove('on');st.sel=null;draw();});
/* ── 검증 ── */
function validate(){const o=[],N=st.nodes,E=st.edges,sv=surveyOf();if(!N.length)return o;
  const dv=N.filter(n=>n.role==="DV"),iv=N.filter(n=>n.role==="IV");
  if(!dv.length)o.push({l:'err',m:'종속변수가 없습니다.',d:'무엇을 사회자본으로 재는지가 먼저입니다. 1부 다섯 편도 여기서 갈렸습니다.'});
  if(dv.length>1)o.push({l:'warn',m:'종속변수가 둘입니다.',d:'한 모형에 하나만. 둘째는 다른 모형으로 두십시오.'});
  if(!iv.length)o.push({l:'err',m:'독립변수가 없습니다.',d:'무엇이 그것을 바꾼다고 보는지 하나 이상.'});
  if(N.length>=2&&!E.length)o.push({l:'warn',m:'화살표가 없습니다.',d:'노드를 누르고 다른 노드를 누르면 이어집니다.'});
  N.filter(n=>n.role!=="CV"&&!nodeItems(n).length).forEach(n=>o.push({l:'err',m:`${cname(n.concept)}에 문항이 없습니다.`,d:'노드를 눌러 조사 문항을 고르십시오. 개념이 아니라 문항이 모형을 만듭니다.'}));
  N.filter(n=>nodeItems(n).length&&sv&&IT[nodeItems(n)[0]].survey!==sv).forEach(n=>o.push({l:'err',m:`${cname(n.concept)}은 ${sname(IT[nodeItems(n)[0]].survey)}, 종속변수는 ${sname(sv)}입니다.`,d:'같은 사람에게 없는 두 문항은 한 모형에 못 들어갑니다. 이것이 오늘 데이터의 첫 번째 사실입니다.'}));
  const units=[...new Set(N.flatMap(n=>nodeItems(n)).map(k=>IT[k].unit).filter(Boolean))];if(units.length>1)o.push({l:'warn',m:`단위가 다릅니다: ${units.join(' / ')}`,d:'가구 수급을 가구원 신뢰에 붙이는 결정이 필요합니다(spotlight ①).'});
  E.forEach(e=>{const a=N.find(n=>n.id===e.from),b=N.find(n=>n.id===e.to);if(!a||!b)return;if(a.role==="DV")o.push({l:'err',m:`${cname(a.concept)}(DV) → ${cname(b.concept)}: 방향이 거꾸로입니다.`,d:'종속변수에서 나가는 화살표는 역인과 가설입니다. 5장 저자도 "반대는 늘 가능하다"고 썼지만, 모형에는 한 방향만.'});
    if(a.role==="MV"&&b.role==="IV")o.push({l:'err',m:`${cname(a.concept)}(MV) → ${cname(b.concept)}(IV): 매개가 원인을 가리킵니다.`,d:'IV → MV → DV 순서로.'});
    if(a.role==="IV"&&b.role==="IV")o.push({l:'warn',m:`${cname(a.concept)} → ${cname(b.concept)}: 독립변수끼리 이었습니다.`,d:'둘 중 하나를 매개로 바꾸거나 화살표를 지우십시오.'});});
  const conn=new Set(E.flatMap(e=>[e.from,e.to]));N.filter(n=>n.role!=="CV"&&!conn.has(n.id)).forEach(n=>o.push({l:'warn',m:`${cname(n.concept)}이 이어져 있지 않습니다.`,d:'화살표가 없는 노드는 모형 밖입니다.'}));
  N.filter(n=>n.role==="MV").forEach(m=>{if(!E.some(e=>e.to===m.id)||!E.some(e=>e.from===m.id))o.push({l:'warn',m:`${cname(m.concept)}은 매개인데 들어오는 화살표와 나가는 화살표가 다 있어야 합니다.`,d:'IV → MV, MV → DV 둘 다.'});});
  return o;}
function dvConcept(){const d=st.nodes.find(n=>n.role==="DV");if(!d)return null;if(d.concept!=="sc_def")return d.concept;const cs=dvComps();
  return cs.some(c=>/trust/.test(c))?(cs.includes('neighbor_trust')&&!cs.includes('generalized_trust')?'trust_neighbor':'trust_general'):cs.some(c=>/participation|volunteer/.test(c))?'participation':cs.length?'network_reciprocity':null;}
function lineage(){const dv=dvConcept(),iv=st.nodes.filter(n=>n.role==="IV").map(n=>n.concept),med=(st.nodes.find(n=>n.role==="MV")||{}).concept||null;if(!dv)return null;
  const T=['trust_general','trust_social','trust_institution','trust_neighbor'],P=['participation','volunteer_donate','political_participation'],has=g=>iv.includes(g),wel=has('welfare_selective')||has('welfare_universal');
  if(['trust_general','trust_social'].includes(dv)&&wel)return['복지국가 설계가 신뢰를 만들고 부순다','5장 K&R'];
  if(T.includes(dv)&&dv!=='trust_neighbor'&&has('public_service_experience')&&med==='fairness')return['접촉의 공정성이 신뢰로','5장 K&R 매개'];
  if(P.includes(dv)&&(has('institution_participation')||has('region')))return['참여 제도가 결사체를 키운다','2장 Freitag'];
  if(P.includes(dv)&&has('welfare_universal'))return['정책 수혜가 참여를 만든다','4장 Mettler'];
  if(P.includes(dv)&&has('welfare_selective'))return['Mettler의 반대 설계(심사형)','4장 Mettler · 5장 K&R 교차'];
  if(['network_reciprocity','trust_neighbor'].includes(dv)&&(has('region')||has('public_service_experience')))return['지역 맥락이 협력 성향을 만든다','1장 Krishna'];
  if(has('institution_participation')&&(med==='fairness'||med==='trust_institution'))return['반응하는 제도가 사회자본을 꺼낸다','3장 L&W'];
  if(dv==='trust_institution'&&has('public_service_experience'))return['서비스 경험이 기관신뢰로','5장 K&R 기제 1(일선 관료)'];
  if(T.includes(dv)&&has('institution_participation'))return['Freitag의 종속변수를 신뢰로 바꾼 조합. Freitag은 신뢰를 재지 않았다','2장 밖'];
  if(['network_reciprocity','trust_neighbor'].includes(dv)&&wel)return["K&R의 독립변수에 Krishna의 종속변수",'1·5장 밖'];
  return['1부 다섯 편 밖의 조합','밖'];}
/* ── 닮은 선행연구: 정의 구성 요소 겹침 + 단위 + 독립 묶음 + 매개 + 계보 ── */
function match(){const cs=dvComps();if(!cs.length)return[];const sv=surveyOf(),iv=st.nodes.filter(n=>n.role==="IV").map(n=>n.concept),med=!!st.nodes.find(n=>n.role==="MV");
  const myUnit=iv.includes('region')&&sv==='chs'?'region':'individual',myInst=iv.some(g=>/welfare|public_service|institution/.test(g)),myReg=iv.includes('region');
  const linMap={'5장 K&R':'kr','5장 K&R 매개':'kr','5장 K&R 기제 1(일선 관료)':'kr','2장 Freitag':'freitag','3장 L&W':'lw','4장 Mettler':'mettler','4장 Mettler · 5장 K&R 교차':'mettler','1장 Krishna':'krishna'},myLin=linMap[(lineage()||[])[1]]||null;
  return STUDIES.filter(s=>DEMO||s.ok).map(s=>{const inter=s.comps.filter(c=>cs.includes(c)),uni=[...new Set([...s.comps,...cs])];let sc=3*inter.length/uni.length;
    if(s.unit===myUnit||s.unit==='mixed')sc+=1;if(myInst&&s.inst)sc+=1;if(myReg&&s.reg)sc+=1;if(med&&s.med)sc+=1;if(myLin&&s.lin===myLin)sc+=1.5;
    return {s,sc,inter,only:s.comps.filter(c=>!cs.includes(c)),miss:cs.filter(c=>!s.comps.includes(c))};}).filter(x=>x.inter.length).sort((a,b)=>b.sc-a.sc).slice(0,5);}
function review(){const sv=surveyOf();if(!sv)return[];const dv=dvConcept(),iv=st.nodes.filter(n=>n.role==="IV").map(n=>n.concept),med=(st.nodes.find(n=>n.role==="MV")||{}).concept||null,o=[];
  const b=REV.base[sv];if(b)o.push(['약한 고리',b[0]],['한 단계',b[1]]);const c=Object.fromEntries(REV.cond),add=k=>o.push(['덧붙임',c[k]]);
  if(med)add('med_any');if(med==='fairness'&&sv==='kipa')add('med_fair_kipa');if(dv==='trust_institution')add('dv_inst');
  if(iv.includes('welfare_selective')&&sv==='koweps')add('iv_sel_koweps');if(iv.includes('welfare_selective')&&sv==='chs')add('iv_sel_chs');if(iv.includes('institution_participation')&&sv==='kipa')add('iv_inst_kipa');
  if(iv.includes('region'))add(sv==='chs'?'region_sgg':'region_wide');if(/영향/.test(st.q))add('q_cause');if(dv==='trust_neighbor'&&(iv.includes('welfare_selective')||iv.includes('welfare_universal')))add('neighbor_welfare');return o;}
function hyps(){const N=st.nodes,E=st.edges,h=[];let k=1;E.forEach(e=>{const a=N.find(n=>n.id===e.from),b=N.find(n=>n.id===e.to);if(!a||!b||a.role==="DV")return;h.push(`H${k++}. ${cname(a.concept)}은(는) ${cname(b.concept)}와(과) 관련이 있을 것이다.`);});
  N.filter(n=>n.role==="MV").forEach(m=>{const ins=E.filter(e=>e.to===m.id).map(e=>N.find(n=>n.id===e.from)),out=E.find(e=>e.from===m.id);if(out)ins.forEach(a=>a&&h.push(`H${k++}. ${cname(a.concept)}과(와) ${cname(N.find(n=>n.id===out.to).concept)}의 관계를 ${cname(m.concept)}이(가) 매개할 것이다.`));});return h;}
const B=t=>t.replace(/\((\d장[^)]*)\)/g,'(<b class="w">$1</b>)');
function openValidator(){$('npanel').classList.remove('on');$('vpanel').classList.add('on');const iss=validate(),lin=lineage(),rv=review(),hy=hyps(),errs=iss.filter(i=>i.l==='err').length;
  $('vbody').innerHTML=`<h3>모형 검증</h3><span class="k">노드 ${st.nodes.length} · 화살표 ${st.edges.length}</span>`+
  (iss.length?iss.map(i=>`<div class="iss ${i.l}">${i.m}<small>${i.d}</small></div>`).join(''):`<div class="iss ok">구조는 맞습니다.</div>`)+
  (defLine()?`<div class="sec">내 정의</div><div class="iss ok">${defLine()}<small>구성 요소: ${dvComps().map(c=>COMP_KO[c]).join(' · ')}</small></div>`:'')+
  (lin?`<div class="sec">어느 논리인가</div><div class="iss ok"><b>${lin[0]}</b><small>${lin[1]==='밖'?'1부에 없던 조합입니다. 선행연구가 없어서일 수도, 자료가 없어서일 수도 있습니다.':'1부 '+lin[1]+'에서 본 논리입니다.'}</small></div>`:'')+
  (()=>{const m=match();return m.length?`<div class="sec">닮은 선행연구 ${DEMO?'<span class="k" style="font-weight:400">· 규칙 코딩, 미검수(데모)</span>':''}</div>`+m.map(x=>`<div class="iss"><b>${x.s.au} (${x.s.y})</b> ${x.s.t}<small>${x.s.line}${x.s.design?' · '+x.s.design:''}</small><small>닮은 점: ${x.inter.map(c=>COMP_KO[c]).join('·')}${x.s.unit?' · '+({individual:'개인',region:'지역',country:'국가',mixed:'다수준'})[x.s.unit]+' 단위':''}${x.only.length?' / 그 연구에만: '+x.only.map(c=>COMP_KO[c]).join('·'):''}${x.miss.length?' / 당신에게만: '+x.miss.map(c=>COMP_KO[c]).join('·'):''}</small>${x.s.link?`<small><a href="${x.s.link}" target="_blank" rel="noopener">${x.s.j||x.s.link}</a></small>`:''}</div>`).join(''):''})()+
  (rv.length?`<div class="sec">약한 고리와 한 단계</div>`+rv.map(([k,t])=>`<div class="iss"><span class="k">${k}</span><br>${B(t)}</div>`).join(''):'')+
  (hy.length?`<div class="sec">가설(관련형)</div>`+hy.map(h=>`<div class="iss">${h}</div>`).join(''):'')+
  `<div class="sec">연구질문 한 줄</div><input class="q" id="q" value="${st.q.replace(/"/g,'&quot;')}" placeholder="~는 ~와 관련이 있는가"><button class="btn" id="submit" ${errs?'disabled':''}>${errs?'오류를 고친 뒤 제출':'제출'}</button><div class="agg" id="agg"></div>
  <div class="sec">1부 다섯 편이 잰 것</div>`+PAPERS.map(p=>`<div class="iss"><b>${p[0]}</b> ${p[1]}<small>신뢰의 자리: ${p[2]}</small></div>`).join('');
  $('q').oninput=e=>st.q=e.target.value;$('submit').onclick=()=>{save();$('submit').textContent='제출됨';$('submit').disabled=true;agg();};agg();}
$('badge').onclick=()=>$('vpanel').classList.contains('on')?$('vpanel').classList.remove('on'):openValidator();
function save(){const dv=st.nodes.find(n=>n.role==="DV");const row={ts:new Date().toISOString(),nick:$('nick').value.trim(),stage:'model',key:'submit',value:{dv:dvConcept(),items:nodeItems(dv),definition:defLine(),comps:dvComps(),matches:match().map(x=>x.s.id),survey:surveyOf(),iv:st.nodes.filter(n=>n.role==="IV").map(n=>n.concept),med:(st.nodes.find(n=>n.role==="MV")||{}).concept||null,edges:st.edges.length,q:st.q,lineage:(lineage()||[])[1]}};
  try{const a=JSON.parse(localStorage.getItem('w11_model')||'[]');a.push(row);localStorage.setItem('w11_model',JSON.stringify(a));}catch(e){}
  if(SAVE_URL)fetch(SAVE_URL,{method:'POST',mode:'no-cors',body:JSON.stringify(row)}).catch(()=>{});}
function agg(){let a=[];try{a=JSON.parse(localStorage.getItem('w11_model')||'[]')}catch(e){}const el=$('agg');if(!el||a.length<2){if(el)el.innerHTML='';return;}
  const cnt={};a.forEach(r=>cnt[r.value.dv]=(cnt[r.value.dv]||0)+1);const mx=Math.max(...Object.values(cnt));
  el.innerHTML=`<div class="sec">이 브라우저의 제출 ${a.length}건(데모 집계)</div>`+C.filter(c=>c.role==='dv').map(c=>`<div class="b"><span>${c.label}</span><i style="width:${(cnt[c.id]||0)/mx*150}px"></i>${cnt[c.id]||0}</div>`).join('');}
$('paltog').onclick=()=>$('pal').classList.toggle('on');
palette();draw();
</script></body></html>"""
out = (HTML.replace("__CAT__", json.dumps(bi.CAT, ensure_ascii=False)).replace("__REV__", json.dumps({"base": bi.REVIEWS, "cond": bi.COND}, ensure_ascii=False))
       .replace("__PAPERS__", json.dumps(bi.PAPERS, ensure_ascii=False)).replace("__STUDIES__", json.dumps(STUDIES, ensure_ascii=False)))
open(os.path.join(HERE, "canvas.html"), "w", encoding="utf-8").write(out)
print("canvas.html", len(out) // 1024, "KB · 선행연구", len(STUDIES), "편(구성 요소 있는 것)")
