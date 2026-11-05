<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>연구모형 캔버스</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css">
<style>
:root{--ink:#15203a;--sub:#5a6577;--line:#e2e6ec;--navy:#072A60;--tint:#e9eef6;--green:#4F7F1C;--gtint:#f0f7e6;--orange:#D9640F;--otint:#fdf1e7;--paper:#fafaf7}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:#fff;color:var(--ink);font-family:Pretendard,"Noto Sans KR",sans-serif;font-size:15px;line-height:1.5;display:flex;flex-direction:column;overscroll-behavior:none}
.top{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:2px solid var(--navy)}
.top b{color:var(--navy)}.top input{font:inherit;border:1px solid var(--line);padding:4px 8px;width:100px}.top span{color:var(--sub);font-size:12.5px;margin-left:auto;text-align:right}
.wrap{flex:1;display:flex;min-height:0;position:relative}
.pal{width:240px;border-right:1px solid var(--line);overflow-y:auto;padding:10px;touch-action:pan-y}
.pal h4{margin:12px 0 6px;font-size:12px;color:var(--sub);font-weight:700}.pal .k{font-size:12px;color:var(--sub)}
.card{border:1px solid var(--line);border-left:3px solid var(--navy);padding:7px 9px;margin:0 0 6px;background:#fff;font-size:13px;user-select:none;cursor:grab;touch-action:none}
.card small{display:block;color:var(--sub);font-size:11.5px}.card.used{opacity:.4;border-left-color:var(--line)}.card .c{font-size:11px;color:var(--green)}
.ghost{position:fixed;pointer-events:none;z-index:50;background:var(--tint);border:1px solid var(--navy);padding:6px 9px;font-size:12.5px;max-width:220px;opacity:.95}
.cv{flex:1;position:relative;background:var(--paper);background-image:radial-gradient(circle at 1px 1px,rgba(60,64,75,.16) 1px,transparent 0);background-size:20px 20px;overflow:hidden;touch-action:none}
svg{width:100%;height:100%;display:block}
.node{cursor:pointer}.node rect{fill:#fff;stroke:var(--navy);stroke-width:1.3}.node.dv rect{fill:var(--tint);stroke-width:1.8}.node.cv rect{stroke:var(--sub);stroke-dasharray:3 2}.node.sel rect{stroke-width:3}.node.over rect{stroke:var(--green);stroke-width:3}
.node text{font-size:12.5px;fill:var(--ink);pointer-events:none}.node .r{font-size:10px;fill:var(--sub)}.node .s{font-size:10px;fill:var(--green)}
.edge{stroke:var(--navy);stroke-width:1.4;fill:none}.edge.bad{stroke:var(--orange);stroke-dasharray:4 3}
.bar{position:absolute;top:10px;left:50%;transform:translateX(-50%);background:var(--navy);color:#fff;font-size:12.5px;padding:5px 12px;pointer-events:none}
.hint{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#9aa2ae;font-size:14px;text-align:center;pointer-events:none;padding:20px;line-height:1.7}
.tools{position:absolute;left:10px;top:10px;display:flex;gap:6px}.tools button{font:inherit;font-size:12px;border:1px solid var(--line);background:#fff;color:var(--sub);padding:3px 9px;cursor:pointer}
.badge{position:absolute;left:50%;transform:translateX(-50%);bottom:14px;background:var(--navy);border:2px solid var(--navy);color:#fff;font:inherit;font-size:15px;font-weight:700;padding:11px 26px;cursor:pointer;min-width:260px}.badge.bad{background:#fff;border-color:var(--orange);color:var(--orange)}.badge small{display:block;font-weight:400;font-size:11.5px;opacity:.85}
.panel{position:relative;width:340px;flex:none;background:#fff;border-left:1px solid var(--line);overflow-y:auto;padding:14px 16px 80px;display:none;z-index:5}
.panel.on{display:block}.panel h3{margin:0 0 4px;font-size:16px;color:var(--navy)}.panel h3::before{content:"";display:block;width:28px;height:3px;background:#8DC63F;margin-bottom:8px}
.panel .x{position:absolute;right:10px;top:8px;border:0;background:none;font-size:18px;cursor:pointer;color:var(--sub)}
.iss{border-left:3px solid var(--navy);padding:6px 10px;margin:8px 0;font-size:13.5px;background:#fff}.iss.err{border-left-color:var(--orange);background:var(--otint)}.iss.warn{border-left-color:var(--orange)}.iss.ok{border-left-color:var(--green);background:var(--gtint)}
.iss small{display:block;color:var(--sub);font-size:12.5px;margin-top:2px}.iss b.w{color:var(--navy)}.iss a{color:var(--navy)}
.k{font-size:12.5px;color:var(--sub)}.sec{margin-top:16px;font-size:12.5px;color:var(--sub);font-weight:700}
.opt{display:block;width:100%;text-align:left;background:#fff;border:1px solid var(--line);border-left:3px solid var(--line);padding:8px 10px;margin:0 0 6px;font:inherit;font-size:13px;cursor:pointer}.opt.sel{border-left-color:var(--navy);background:var(--tint)}.opt small{display:block;color:var(--sub);font-size:11.5px}
.row{display:flex;gap:6px;flex-wrap:wrap}.row button{font:inherit;font-size:12.5px;border:1px solid var(--navy);background:#fff;color:var(--navy);padding:4px 10px;cursor:pointer}.row button.on{background:var(--navy);color:#fff}
.item{display:flex;gap:8px;align-items:flex-start;border-bottom:1px solid var(--line);padding:6px 0;font-size:13px}.item button{border:0;background:none;color:var(--sub);cursor:pointer;font-size:14px}
input.q,input.nm{width:100%;font:inherit;font-size:14px;padding:8px;border:1px solid var(--line);margin:6px 0}
.btn{font:inherit;padding:9px 16px;border:1px solid var(--navy);background:var(--navy);color:#fff;cursor:pointer}.btn.sec2{background:#fff;color:var(--navy)}
.agg .b{display:flex;align-items:center;gap:8px;margin:3px 0;font-size:12.5px}.agg i{display:block;height:10px;background:var(--navy)}.agg span{width:130px}
.foot{font-size:11px;color:var(--sub);text-align:center;padding:3px;border-top:1px solid var(--line)}
.gate{position:absolute;inset:0;background:#fff;z-index:20;overflow-y:auto;padding:24px 20px 60px}.gate h2{font-size:20px;color:var(--navy);margin:0 0 4px}.gate h2::before{content:"";display:block;width:32px;height:3px;background:#8DC63F;margin-bottom:10px}
.gate .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin-top:14px}.gate .opt{margin:0;padding:12px}.gate .opt b{display:block;font-size:15px;color:var(--navy)}
.paltog{display:none;font:inherit;font-size:12.5px;border:1px solid var(--navy);background:#fff;color:var(--navy);padding:3px 8px;cursor:pointer}
@media (max-width:720px){.pal{position:absolute;left:0;top:0;bottom:0;z-index:4;background:#fff;transform:translateX(-100%);transition:transform .2s;width:240px}.pal.on{transform:none}.paltog{display:inline-block}.panel{position:absolute;right:0;top:0;bottom:0;width:92%}}
</style></head><body>
<div class="top"><b>연구모형 캔버스</b><input id="nick" placeholder="별명" maxlength="12"><button class="paltog" id="paltog">문항</button><span id="status"></span></div>
<div class="wrap">
<div class="gate" id="gate"></div>
<aside class="pal" id="pal"></aside>
<div class="cv" id="cv">
<svg id="svg" viewBox="0 0 640 400" preserveAspectRatio="xMidYMid meet"><defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#072A60"/></marker><marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#D9640F"/></marker></defs>
<g id="edges"></g><g id="nodes"></g></svg>
<div class="hint" id="hint">왼쪽 문항을 끌어다 놓으십시오.<br>빈 곳에 놓으면 새 변수, 다른 변수 위에 놓으면 거기에 묶입니다.<br>변수를 누르고 다른 변수를 누르면 화살표가 생깁니다.</div>
<div class="tools"><button id="auto">열 맞춰 배치</button><button id="resv">자료 바꾸기</button></div>
<div class="bar" id="bar" style="display:none"></div>
<button class="badge" id="badge" style="display:none"></button>
<div class="pop" id="pop" style="display:none"></div>
</div>
<div class="panel" id="npanel"><button class="x" data-x="npanel">×</button><div id="nbody"></div></div>
<div class="panel" id="vpanel"><button class="x" data-x="vpanel">×</button><div id="vbody"></div></div>
</div>
<div class="foot">선택은 이 수업 안에서만 쓰고 끝나면 지웁니다 · 계수는 계산하지 않습니다 · 모형 그림은 행정학 관행 형식</div>
<script>
const CAT=__CAT__, REV=__REV__, PAPERS=__PAPERS__, STUDIES=__STUDIES__, SAVE_URL="", DEMO=true;
const S=CAT.surveys, C=CAT.concepts, IT=CAT.items;
const ROLE={DV:"종속변수",IV:"독립변수",MV:"매개변수",CV:"통제변수"};
const COMP_OF={trust_general:"generalized_trust",trust_social:"generalized_trust",trust_neighbor:"neighbor_trust",trust_institution:"institutional_trust",participation:"participation",volunteer_donate:"volunteer_donate",network_reciprocity:"reciprocity",political_participation:"political_participation"};
const COMP_KO={generalized_trust:"일반신뢰",institutional_trust:"기관신뢰",neighbor_trust:"이웃 신뢰",participation:"단체 참여",volunteer_donate:"봉사·기부",network:"연결망",reciprocity:"호혜",political_participation:"정치 참여"};
const PAPER_OF={trust_general:"K&R 0~10 단일 문항",trust_social:"K&R 변형",trust_neighbor:"Krishna 마을 신뢰",trust_institution:"Krishna의 독립변수",participation:"Freitag 4문항 / Mettler 가입 수",volunteer_donate:"Mettler",network_reciprocity:"Krishna 6문항",political_participation:"Mettler 6종",fairness:"K&R 매개",welfare_selective:"K&R 선별 7기관",welfare_universal:"K&R 보편 / Mettler G.I. Bill",public_service_experience:"L&W 반응성",institution_participation:"Freitag 직접민주주의",region:"Freitag 칸톤"};
const okItem=i=>!(i.concept==='region'&&/확인 필요|소속감/.test(i.question||''));
let st={survey:null,nodes:[],edges:[],sel:null,q:""}, idle=null, uid=0;
const $=id=>document.getElementById(id), cname=id=>(C.find(c=>c.id===id)||{}).label||id, sname=k=>(S[k]||{}).name||k, crole=id=>(C.find(c=>c.id===id)||{}).role;
const comps=n=>[...new Set(n.items.map(k=>COMP_OF[IT[k].concept]).filter(Boolean))];
const dvNode=()=>st.nodes.find(n=>n.role==="DV");
const dvComps=()=>{const d=dvNode();return d?comps(d):[]};
const nodeConcepts=n=>[...new Set(n.items.map(k=>IT[k].concept))];
const defLine=()=>{const d=dvNode();if(!d||!d.items.length)return'';const its=d.items.map(k=>IT[k]);const cs={};its.forEach(i=>(cs[i.concept]=cs[i.concept]||0,cs[i.concept]++));
  return `${/^(내|나의)/.test(d.name)?'':'당신의 '}${d.name} = ${sname(st.survey)} ${its[0].wave||''} · ${Object.entries(cs).map(([c,n])=>cname(c)+(n>1?' '+n+'문항':'')).join(' + ')} · ${[...new Set(its.map(i=>i.unit).filter(Boolean))].join('·')||'개인'} 단위`};
/* ── 자료 고르기 ── */
function gate(){const svs=Object.keys(S).filter(s=>IT.some(i=>i.survey===s&&okItem(i)));
  $('gate').innerHTML=`<h2>어떤 자료로 연구하시겠습니까</h2><span class="k">조사를 고르면 그 조사의 문항만 보입니다. 같은 사람에게 물은 문항끼리만 한 모형에 들어갑니다.</span><div class="grid">`+
  svs.map(s=>{const its=IT.filter(i=>i.survey===s&&okItem(i)),dv=its.filter(i=>crole(i.concept)==='dv').length,iv=its.filter(i=>crole(i.concept)==='iv').length;
    return `<button class="opt" data-s="${s}"><b>${S[s].name}</b><small>${S[s].unit} · ${S[s].best_wave||''}</small><small>사회자본 문항 ${dv} · 원인 문항 ${iv} · 매개 ${its.filter(i=>crole(i.concept)==='med').length} · 지역 ${its.filter(i=>i.concept==='region').length}</small><small>${S[s].why||''}</small></button>`}).join('')+`</div>`;
  $('gate').onclick=e=>{const b=e.target.closest('.opt');if(!b)return;st.survey=b.dataset.s;st.nodes=[];st.edges=[];st.sel=null;$('gate').style.display='none';$('status').textContent=`자료: ${sname(st.survey)} · ${S[st.survey].unit}`;palette();draw();};
  $('gate').style.display='block';}
/* ── 팔레트: 고른 조사의 문항 카드 ── */
function palette(){const its=IT.map((i,k)=>({i,k})).filter(x=>x.i.survey===st.survey&&okItem(x.i));const used=new Set(st.nodes.flatMap(n=>n.items));
  const groups=[["사회자본 후보 — 끌어다 놓고 묶으십시오",x=>crole(x.i.concept)==='dv'],["원인 후보",x=>crole(x.i.concept)==='iv'],["매개 후보",x=>crole(x.i.concept)==='med'],["지역",x=>x.i.concept==='region']];
  $('pal').innerHTML=`<span class="k">${sname(st.survey)} · 문항 ${its.length}개</span>`+groups.map(([h,f])=>{const g=its.filter(f);return g.length?`<h4>${h}</h4>`+g.map(x=>`<div class="card ${used.has(x.k)?'used':''}" data-k="${x.k}" draggable="false"><span class="c">${cname(x.i.concept)}${PAPER_OF[x.i.concept]?' · 1부 '+PAPER_OF[x.i.concept]:''}</span><br>${x.i.question}<small>${x.i.wave||''} · ${x.i.scale||''}${x.i.unit?' · '+x.i.unit:''}</small></div>`).join(''):''}).join('')+
  `<h4>개인 특성</h4><div class="card used" style="opacity:.7;cursor:default">연령·교육·소득·고용<small>모든 모형에 통제로 들어갑니다</small></div>`;}
/* ── 끌어다 놓기(포인터) ── */
let drag=null;
$('pal').addEventListener('pointerdown',e=>{const c=e.target.closest('.card');if(!c||c.classList.contains('used')||c.dataset.k==null)return;drag={k:+c.dataset.k,text:IT[+c.dataset.k].question,moved:false,x0:e.clientX,y0:e.clientY};const g=document.createElement('div');g.className='ghost';g.textContent=drag.text.slice(0,40);document.body.appendChild(g);drag.g=g;g.style.left=e.clientX+8+'px';g.style.top=e.clientY+8+'px';c.setPointerCapture?.(e.pointerId);});
document.addEventListener('pointermove',e=>{if(drag){drag.moved=true;drag.g.style.left=e.clientX+8+'px';drag.g.style.top=e.clientY+8+'px';hover(e.clientX,e.clientY);}
  if(mv){const p=svgPt(e.clientX,e.clientY);if(Math.hypot(e.clientX-mv.x0,e.clientY-mv.y0)>6)mv.moved=true;if(mv.moved){mv.n.x=Math.max(0,Math.min(640-150,p.x-mv.dx));mv.n.y=Math.max(0,Math.min(400-46,p.y-mv.dy));draw(false);}}});
document.addEventListener('pointerup',e=>{if(drag){drag.g.remove();const k=drag.k,moved=drag.moved;drag=null;clearHover();const t=nodeAt(e.clientX,e.clientY);const inCv=document.elementFromPoint(e.clientX,e.clientY)?.closest('#cv');
    if(t&&t.role!=="CV"){t.items.push(k);$('pal').classList.remove('on');touch();openNodePanel(t.id);} else if(inCv||!moved&&window.innerWidth<=720){const p=inCv?svgPt(e.clientX,e.clientY):{x:60+Math.random()*300,y:40+Math.random()*250};newNode(k,p);} return;}
  if(mv){const n=mv.n,moved=mv.moved;mv=null;if(!moved)tapNode(n.id);else touch();}});
function svgPt(cx,cy){const r=$('svg').getBoundingClientRect();const sc=Math.min(r.width/640,r.height/400),ox=(r.width-640*sc)/2,oy=(r.height-400*sc)/2;return {x:(cx-r.left-ox)/sc,y:(cy-r.top-oy)/sc};}
function nodeAt(cx,cy){const p=svgPt(cx,cy);return st.nodes.find(n=>p.x>=n.x&&p.x<=n.x+150&&p.y>=n.y&&p.y<=n.y+46);}
function hover(cx,cy){const t=nodeAt(cx,cy);document.querySelectorAll('.node').forEach(g=>g.classList.toggle('over',!!t&&g.dataset.id===t.id&&t.role!=="CV"));}
function clearHover(){document.querySelectorAll('.node.over').forEach(g=>g.classList.remove('over'));}
function newNode(k,p){const i=IT[k],r=crole(i.concept);const role=r==='dv'?(dvNode()?'IV':'DV'):r==='med'?'MV':'IV';
  const n={id:'n'+(++uid),name:cname(i.concept),role,items:[k],x:Math.max(0,Math.min(490,p.x-75)),y:Math.max(0,Math.min(354,p.y-23))};st.nodes.push(n);$('pal').classList.remove('on');touch();openNodePanel(n.id);}
/* ── 노드 이동·탭 ── */
let mv=null;
$('svg').addEventListener('pointerdown',e=>{const g=e.target.closest('.node');if(!g)return;const n=st.nodes.find(x=>x.id===g.dataset.id);const p=svgPt(e.clientX,e.clientY);mv={n,dx:p.x-n.x,dy:p.y-n.y,x0:e.clientX,y0:e.clientY,moved:false};});
$('svg').addEventListener('click',e=>{if(!e.target.closest('.node')){st.sel=null;draw();}});
function tapNode(id){if(!st.sel){st.sel=id;draw();openNodePanel(id);return;}if(st.sel===id){st.sel=null;draw();return;}
  if(!st.edges.some(x=>x.from===st.sel&&x.to===id))st.edges.push({from:st.sel,to:id});st.sel=null;closePanels();touch();}
/* ── 그리기 ── */
function autoLayout(){const col={IV:60,MV:250,DV:440,CV:60},cnt={};st.nodes.forEach(n=>{const k=n.role;cnt[k]=(cnt[k]||0)+1;n.x=col[k];n.y=(k==="CV"?250:40)+(cnt[k]-1)*62;});draw();}
function draw(val=true){$('hint').style.display=st.nodes.length?'none':'flex';
  $('nodes').innerHTML=st.nodes.map(n=>{const cls=`node ${n.role.toLowerCase()} ${st.sel===n.id?'sel':''}`;const l1=n.name.length>14?n.name.slice(0,13)+'…':n.name;
    return `<g class="${cls}" data-id="${n.id}" transform="translate(${n.x},${n.y})"><rect width="150" height="46" rx="2"/><text x="8" y="17" class="r">${n.role} · ${ROLE[n.role]}</text><text x="8" y="34">${l1}</text><text x="142" y="17" class="s" text-anchor="end">${n.items.length}문항</text></g>`}).join('');
  $('edges').innerHTML=st.edges.map(e=>{const a=st.nodes.find(n=>n.id===e.from),b=st.nodes.find(n=>n.id===e.to);if(!a||!b)return'';const rev=a.role==="DV"||(a.role==="MV"&&b.role==="IV");const L=a.x+150<=b.x,x1=L?a.x+150:a.x,x2=L?b.x:b.x+150,y1=a.y+23,y2=b.y+23;
    return `<path class="edge ${rev?'bad':''}" d="M${x1},${y1} C${x1+(L?40:-40)},${y1} ${x2+(L?-40:40)},${y2} ${x2},${y2}" marker-end="url(#${rev?'ahb':'ah'})"/>`}).join('');
  if(!val)return;palette();const iss=validate(),errs=iss.filter(i=>i.l==='err').length,warns=iss.filter(i=>i.l==='warn').length;
  $('badge').style.display=st.nodes.length?'block':'none';$('badge').className='badge'+(errs?' bad':'');$('badge').innerHTML=errs?`먼저 고칠 것 ${errs} ›<small>${warns?warns+' 경고 · ':''}Enter</small>`:`선행연구와 비교 ›<small>${warns?warns+' 경고 · ':''}내 정의 · 계보 · 닮은 연구 · 가설 · Enter</small>`;
  $('bar').style.display=st.sel?'block':'none';$('bar').textContent='이을 변수를 누르십시오 · 같은 변수를 다시 누르면 취소';}
function touch(){draw();clearTimeout(idle);if(st.nodes.length>=2&&st.edges.length>=1)idle=setTimeout(()=>{if(!$('npanel').classList.contains('on'))openValidator();},3000);}
/* ── 노드 패널: 이름·역할·묶인 문항 ── */
function openNodePanel(id){const n=st.nodes.find(x=>x.id===id);if(!n)return;$('vpanel').classList.remove('on');$('npanel').classList.add('on');const cs=nodeConcepts(n);
  $('nbody').innerHTML=`<h3>${n.name}</h3><span class="k">${n.role} · ${ROLE[n.role]} · ${sname(st.survey)}</span>
  <div class="sec">이름</div><input class="nm" id="nm" value="${n.name.replace(/"/g,'&quot;')}" maxlength="24">
  <div class="sec">역할</div><div class="row">${["DV","IV","MV","CV"].map(r=>`<button data-r="${r}" class="${n.role===r?'on':''}">${r} ${ROLE[r]}</button>`).join('')}</div>
  ${n.role==="DV"&&n.items.length?`<div class="iss ok">${defLine()}<small>구성 요소: ${comps(n).map(c=>COMP_KO[c]).join(' · ')||'—'}</small></div>`:''}
  ${cs.length?`<div class="iss">1부에서 이 자리: ${cs.map(c=>PAPER_OF[c]||cname(c)).join(' / ')}<small>${cs.filter(c=>crole(c)==='dv').length&&n.role!=="DV"?'1부에서는 종속변수였던 문항입니다. 원인 자리에 두면 설계가 바뀝니다(Krishna의 정부 신뢰처럼).':''}</small></div>`:''}
  <div class="sec">묶인 문항 ${n.items.length} <span class="k" style="font-weight:400">· 팔레트에서 이 변수 위로 끌어오면 더 묶입니다</span></div>`+
  n.items.map(k=>`<div class="item"><div style="flex:1">${IT[k].question}<br><span class="k">${cname(IT[k].concept)} · ${IT[k].scale||''}</span></div><button data-rm="${k}" title="빼기">×</button></div>`).join('')+
  `<div class="sec"></div><button class="btn sec2" id="del">이 변수 지우기</button>`;
  $('nm').oninput=e=>{n.name=e.target.value.trim()||n.name;draw(false);};$('nm').onchange=()=>draw();
  $('nbody').onclick=e=>{const r=e.target.closest('[data-r]');if(r){if(r.dataset.r==="DV"&&dvNode()&&dvNode().id!==n.id){$('status').textContent='종속변수는 하나만. 기존 종속변수의 역할을 먼저 바꾸십시오.';return;}n.role=r.dataset.r;touch();openNodePanel(id);return;}
    const rm=e.target.closest('[data-rm]');if(rm){n.items=n.items.filter(k=>k!==+rm.dataset.rm);touch();openNodePanel(id);return;}
    if(e.target.id==='del'){st.nodes=st.nodes.filter(x=>x.id!==id);st.edges=st.edges.filter(x=>x.from!==id&&x.to!==id);st.sel=null;closePanels();touch();}};}
function closePanels(){$('npanel').classList.remove('on');$('vpanel').classList.remove('on');}
document.querySelectorAll('.x').forEach(b=>b.onclick=()=>{$(b.dataset.x).classList.remove('on');st.sel=null;draw();});
/* ── 검증 ── */
function validate(){const o=[],N=st.nodes,E=st.edges;if(!N.length)return o;const dv=N.filter(n=>n.role==="DV"),iv=N.filter(n=>n.role==="IV");
  if(!dv.length)o.push({l:'err',m:'종속변수가 없습니다.',d:'사회자본으로 쓸 문항을 묶은 변수를 하나 골라 역할을 DV로 두십시오. 1부 다섯 편도 여기서 갈렸습니다.'});
  if(!iv.length)o.push({l:'err',m:'독립변수가 없습니다.',d:'무엇이 그것을 바꾼다고 보는지 하나 이상.'});
  if(N.length>=2&&!E.length)o.push({l:'warn',m:'화살표가 없습니다.',d:'변수를 누르고 다른 변수를 누르면 이어집니다.'});
  N.filter(n=>!n.items.length).forEach(n=>o.push({l:'err',m:`${n.name}에 문항이 없습니다.`,d:'팔레트에서 문항을 끌어다 이 변수 위에 놓으십시오.'}));
  dv.forEach(d=>{const mixed=nodeConcepts(d).filter(c=>crole(c)!=='dv');if(mixed.length)o.push({l:'warn',m:`${d.name}에 사회자본이 아닌 문항이 섞여 있습니다: ${mixed.map(cname).join(', ')}`,d:'종속변수 정의에는 사회자본 문항만. 원인 문항은 따로 변수를 만드십시오.'});});
  const units=[...new Set(N.flatMap(n=>n.items).map(k=>IT[k].unit).filter(Boolean))];if(units.length>1)o.push({l:'warn',m:`단위가 다릅니다: ${units.join(' / ')}`,d:'가구 수급을 가구원 신뢰에 붙이는 결정이 필요합니다(spotlight ①).'});
  E.forEach(e=>{const a=N.find(n=>n.id===e.from),b=N.find(n=>n.id===e.to);if(!a||!b)return;if(a.role==="DV")o.push({l:'err',m:`${a.name}(DV) → ${b.name}: 방향이 거꾸로입니다.`,d:'종속변수에서 나가는 화살표는 역인과 가설입니다. 5장 저자도 "반대는 늘 가능하다"고 썼지만, 모형에는 한 방향만.'});
    if(a.role==="MV"&&b.role==="IV")o.push({l:'err',m:`${a.name}(MV) → ${b.name}(IV): 매개가 원인을 가리킵니다.`,d:'IV → MV → DV 순서로.'});
    if(a.role==="IV"&&b.role==="IV")o.push({l:'warn',m:`${a.name} → ${b.name}: 독립변수끼리 이었습니다.`,d:'둘 중 하나를 매개로 바꾸거나 화살표를 지우십시오.'});});
  const conn=new Set(E.flatMap(e=>[e.from,e.to]));N.filter(n=>n.role!=="CV"&&!conn.has(n.id)).forEach(n=>o.push({l:'warn',m:`${n.name}이 이어져 있지 않습니다.`,d:'화살표가 없는 변수는 모형 밖입니다.'}));
  N.filter(n=>n.role==="MV").forEach(m=>{if(!E.some(e=>e.to===m.id)||!E.some(e=>e.from===m.id))o.push({l:'warn',m:`${m.name}은 매개인데 들어오는 화살표와 나가는 화살표가 다 있어야 합니다.`,d:'IV → MV, MV → DV 둘 다.'});});
  return o;}
function ivConcepts(){return [...new Set(st.nodes.filter(n=>n.role==="IV").flatMap(nodeConcepts))];}
function medConcept(){const m=st.nodes.find(n=>n.role==="MV");return m?(nodeConcepts(m)[0]||null):null;}
function dvConcept(){const d=dvNode();if(!d)return null;const cs=comps(d);return cs.some(c=>/trust/.test(c))?(cs.includes('neighbor_trust')&&!cs.includes('generalized_trust')?'trust_neighbor':'trust_general'):cs.some(c=>/participation|volunteer/.test(c))?'participation':cs.length?'network_reciprocity':null;}
function lineage(){const dv=dvConcept(),iv=ivConcepts(),med=medConcept();if(!dv)return null;
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
function match(){const cs=dvComps();if(!cs.length)return[];const iv=ivConcepts(),med=!!st.nodes.find(n=>n.role==="MV");
  const myUnit=iv.includes('region')&&st.survey==='chs'?'region':'individual',myInst=iv.some(g=>/welfare|public_service|institution/.test(g)),myReg=iv.includes('region');
  const linMap={'5장 K&R':'kr','5장 K&R 매개':'kr','5장 K&R 기제 1(일선 관료)':'kr','2장 Freitag':'freitag','3장 L&W':'lw','4장 Mettler':'mettler','4장 Mettler · 5장 K&R 교차':'mettler','1장 Krishna':'krishna'},myLin=linMap[(lineage()||[])[1]]||null;
  return STUDIES.filter(s=>DEMO||s.ok).map(s=>{const inter=s.comps.filter(c=>cs.includes(c)),uni=[...new Set([...s.comps,...cs])];let sc=3*inter.length/uni.length;
    if(s.unit===myUnit||s.unit==='mixed')sc+=1;if(myInst&&s.inst)sc+=1;if(myReg&&s.reg)sc+=1;if(med&&s.med)sc+=1;if(myLin&&s.lin===myLin)sc+=1.5;
    return {s,sc,inter,only:s.comps.filter(c=>!cs.includes(c)),miss:cs.filter(c=>!s.comps.includes(c))};}).filter(x=>x.inter.length).sort((a,b)=>b.sc-a.sc).slice(0,5);}
/* ── 조작적 정의를 바꾸면: 문항 하나 빼기·더하기, 같은 개념을 다른 조사로 ── */
function topFor(cs){const base=dvComps();const m=STUDIES.filter(s=>DEMO||s.ok).map(s=>{const inter=s.comps.filter(c=>cs.includes(c)),uni=[...new Set([...s.comps,...cs])];return {s,sc:3*inter.length/uni.length+(s.unit==='individual'||s.unit==='mixed'?1:0),inter};}).filter(x=>x.inter.length).sort((a,b)=>b.sc-a.sc)[0];return m?`${m.s.au} (${m.s.y})`:'없음';}
function altDefs(){const d=dvNode();if(!d||!d.items.length)return[];const out=[],cs=comps(d),now=topFor(cs);const compsOf=ks=>[...new Set(ks.map(k=>COMP_OF[IT[k].concept]).filter(Boolean))];
  if(d.items.length>1){const k=d.items[d.items.length-1],c2=compsOf(d.items.filter(x=>x!==k));out.push({t:`「${IT[k].question.slice(0,28)}…」을 빼면`,d:`구성 요소 ${c2.map(c=>COMP_KO[c]).join('·')||'—'} → 닮은 연구 1위 ${topFor(c2)}${topFor(c2)===now?' (그대로)':''}`});}
  const extra=IT.map((i,k)=>({i,k})).find(x=>x.i.survey===st.survey&&crole(x.i.concept)==='dv'&&!d.items.includes(x.k)&&!cs.includes(COMP_OF[x.i.concept]));
  if(extra){const c2=compsOf([...d.items,extra.k]);out.push({t:`「${extra.i.question.slice(0,28)}…」을 더하면`,d:`구성 요소 ${c2.map(c=>COMP_KO[c]).join('·')} → 닮은 연구 1위 ${topFor(c2)}${topFor(c2)===now?' (그대로)':''}`});}
  const c0=IT[d.items[0]].concept,other=IT.find(i=>i.concept===c0&&i.survey!==st.survey&&okItem(i));
  if(other){const i0=IT[d.items[0]];out.push({t:`같은 ${cname(c0)}을 ${sname(other.survey)}로 재면`,d:`${i0.scale||'척도 미상'}(${i0.unit||'개인'}) → ${other.scale||'척도 미상'}(${other.unit||S[other.survey].unit}) · ${other.wave||''}. 같은 이름, 다른 조작적 정의입니다. 1부 다섯 편도 여기서 갈렸습니다.`});}
  return out;}
function review(){const sv=st.survey;if(!sv||!dvNode())return[];const dv=dvConcept(),iv=ivConcepts(),med=medConcept(),o=[];
  const b=REV.base[sv];if(b)o.push(['약한 고리',b[0]],['한 단계',b[1]]);const c=Object.fromEntries(REV.cond),add=k=>o.push(['덧붙임',c[k]]);
  if(med)add('med_any');if(med==='fairness'&&sv==='kipa')add('med_fair_kipa');if(dv==='trust_institution')add('dv_inst');
  if(iv.includes('welfare_selective')&&sv==='koweps')add('iv_sel_koweps');if(iv.includes('welfare_selective')&&sv==='chs')add('iv_sel_chs');if(iv.includes('institution_participation')&&sv==='kipa')add('iv_inst_kipa');
  if(iv.includes('region'))add(sv==='chs'?'region_sgg':'region_wide');if(/영향/.test(st.q))add('q_cause');if(dv==='trust_neighbor'&&(iv.includes('welfare_selective')||iv.includes('welfare_universal')))add('neighbor_welfare');return o;}
function hyps(){const N=st.nodes,E=st.edges,h=[];let k=1;E.forEach(e=>{const a=N.find(n=>n.id===e.from),b=N.find(n=>n.id===e.to);if(!a||!b||a.role==="DV")return;h.push(`H${k++}. ${a.name}은(는) ${b.name}와(과) 관련이 있을 것이다.`);});
  N.filter(n=>n.role==="MV").forEach(m=>{const ins=E.filter(e=>e.to===m.id).map(e=>N.find(n=>n.id===e.from)),out=E.find(e=>e.from===m.id);if(out)ins.forEach(a=>a&&h.push(`H${k++}. ${a.name}과(와) ${N.find(n=>n.id===out.to).name}의 관계를 ${m.name}이(가) 매개할 것이다.`));});return h;}
const B=t=>t.replace(/\((\d장[^)]*)\)/g,'(<b class="w">$1</b>)');
function openValidator(){$('npanel').classList.remove('on');$('vpanel').classList.add('on');const iss=validate(),lin=lineage(),rv=review(),hy=hyps(),errs=iss.filter(i=>i.l==='err').length,m=match();
  $('vbody').innerHTML=`<h3>모형 검증</h3><span class="k">${sname(st.survey)} · 변수 ${st.nodes.length} · 화살표 ${st.edges.length}</span>`+
  (iss.length?iss.map(i=>`<div class="iss ${i.l}">${i.m}<small>${i.d}</small></div>`).join(''):`<div class="iss ok">구조는 맞습니다.</div>`)+
  (defLine()?`<div class="sec">내 정의</div><div class="iss ok">${defLine()}<small>구성 요소: ${dvComps().map(c=>COMP_KO[c]).join(' · ')||'—'}</small></div>`:'')+
  (lin?`<div class="sec">어느 논리인가</div><div class="iss ok"><b>${lin[0]}</b><small>${lin[1]==='밖'?'1부에 없던 조합입니다. 선행연구가 없어서일 수도, 자료가 없어서일 수도 있습니다.':'1부 '+lin[1]+'에서 본 논리입니다.'}</small></div>`:'')+
  (m.length?`<div class="sec">닮은 선행연구 ${DEMO?'<span class="k" style="font-weight:400">· 규칙 코딩, 미검수(데모)</span>':''}</div>`+m.map(x=>`<div class="iss"><b>${x.s.au} (${x.s.y})</b> ${x.s.t}<small>${x.s.line}${x.s.design?' · '+x.s.design:''}</small><small>닮은 점: ${x.inter.map(c=>COMP_KO[c]).join('·')}${x.s.unit?' · '+({individual:'개인',region:'지역',country:'국가',mixed:'다수준'})[x.s.unit]+' 단위':''}${x.only.length?' / 그 연구에만: '+x.only.map(c=>COMP_KO[c]).join('·'):''}${x.miss.length?' / 당신에게만: '+x.miss.map(c=>COMP_KO[c]).join('·'):''}</small>${x.s.link?`<small><a href="${x.s.link}" target="_blank" rel="noopener">${x.s.j||x.s.link}</a></small>`:''}</div>`).join(''):'')+
  (()=>{const a=altDefs();return a.length?`<div class="sec">조작적 정의를 바꾸면</div>`+a.map(x=>`<div class="iss"><b>${x.t}</b><small>${x.d}</small></div>`).join('')+`<div class="k" style="margin:4px 0 0">같은 자료라도 어떤 문항을 묶느냐에 따라 닮은 연구와 계보가 바뀝니다. 이것이 조작적 정의입니다.</div>`:''})()+
  (rv.length?`<div class="sec">약한 고리와 한 단계</div>`+rv.map(([k,t])=>`<div class="iss"><span class="k">${k}</span><br>${B(t)}</div>`).join(''):'')+
  (hy.length?`<div class="sec">가설(관련형)</div>`+hy.map(h=>`<div class="iss">${h}</div>`).join(''):'')+
  `<div class="sec">연구질문 한 줄</div><input class="q" id="q" value="${st.q.replace(/"/g,'&quot;')}" placeholder="~는 ~와 관련이 있는가"><button class="btn" id="submit" ${errs?'disabled':''}>${errs?'오류를 고친 뒤 제출':'제출'}</button><div class="agg" id="agg"></div>
  <div class="sec">1부 다섯 편이 잰 것</div>`+PAPERS.map(p=>`<div class="iss"><b>${p[0]}</b> ${p[1]}<small>신뢰의 자리: ${p[2]}</small></div>`).join('');
  $('q').oninput=e=>st.q=e.target.value;$('submit').onclick=()=>{save();$('submit').textContent='제출됨';$('submit').disabled=true;agg();};agg();}
$('badge').onclick=()=>$('vpanel').classList.contains('on')?$('vpanel').classList.remove('on'):openValidator();
function save(){const d=dvNode();const row={ts:new Date().toISOString(),nick:$('nick').value.trim(),stage:'model',key:'submit',value:{survey:st.survey,dv:dvConcept(),dv_name:d.name,items:d.items,definition:defLine(),comps:dvComps(),iv:ivConcepts(),med:medConcept(),edges:st.edges.length,q:st.q,lineage:(lineage()||[])[1],matches:match().map(x=>x.s.id)}};
  try{const a=JSON.parse(localStorage.getItem('w11_model')||'[]');a.push(row);localStorage.setItem('w11_model',JSON.stringify(a));}catch(e){}
  if(SAVE_URL)fetch(SAVE_URL,{method:'POST',mode:'no-cors',body:JSON.stringify(row)}).catch(()=>{});}
function agg(){let a=[];try{a=JSON.parse(localStorage.getItem('w11_model')||'[]')}catch(e){}const el=$('agg');if(!el||a.length<2){if(el)el.innerHTML='';return;}
  const cnt={};a.forEach(r=>cnt[r.value.dv]=(cnt[r.value.dv]||0)+1);const mx=Math.max(...Object.values(cnt));
  el.innerHTML=`<div class="sec">이 브라우저의 제출 ${a.length}건(데모 집계)</div>`+Object.entries(cnt).map(([c,v])=>`<div class="b"><span>${cname(c)}</span><i style="width:${v/mx*150}px"></i>${v}</div>`).join('');}
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&!/INPUT/.test(e.target.tagName)&&st.nodes.length){e.preventDefault();openValidator();}});
$('paltog').onclick=()=>$('pal').classList.toggle('on');$('auto').onclick=autoLayout;$('resv').onclick=()=>{if(!st.nodes.length||confirm('자료를 바꾸면 캔버스가 비워집니다.'))gate();};
gate();draw();
</script></body></html>
