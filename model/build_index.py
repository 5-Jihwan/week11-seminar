# -*- coding: utf-8 -*-
"""2부 학생 화면 데모 생성: catalog.json + 리뷰 규칙(PART2_v2 §6) + 계보 규칙(§5)을 한 HTML에 심는다(file://로 열림).
저장은 localStorage(데모). Apps Script 저장은 SAVE_URL을 채우면 켜진다. 실행: python model/build_index.py → model/index.html, model/reviews.json"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CAT = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8"))

REVIEWS = {  # 조사별 기본 카드: [약한 고리, 한 단계]
  "koweps": ["16차는 아동수당이 이미 보편인 해라 심사 효과의 변이가 없습니다. 신뢰는 가구원, 수급은 가구라 단위가 다릅니다.", "14차(2018, 선별 시기)와 16차를 같은 사람으로 이으면 전환 전후 설계(5장 연구자 자리 B)가 됩니다."],
  "kipa": ["한 해 횡단면이라 신뢰가 낮아서 접촉을 피했을 가능성(5장 역인과, 355쪽)을 못 가릅니다. 수급 문항이 없어 제도 설계 효과는 못 잽니다.", "2021~2025 다섯 해를 쌓아 추세를 보거나, 공공서비스 만족(5점)을 K&R 매개 자리에 둡니다."],
  "kgss": ["수급 문항이 없어 '제도 → 신뢰'가 아니라 '공정성 → 신뢰'만 됩니다(3장 실증 부재와 같은 자리). 공정성 문항은 2011·2012·2014뿐입니다.", "2012년 한 해로 좁히고 지역 집단토론 참여(참여 제도)를 넣으면 L&W 설계에 가장 가깝습니다."],
  "kostat_social": ["참여는 가장 상세하지만 수급도 대인신뢰도 없습니다.", "시도 단위로 가계금융복지조사의 수급률과 결합하면 Freitag처럼 17개 단위 비교가 됩니다(2장 N=24의 벽)."],
  "chs": ["신뢰가 '동네 사람' 예/아니오라 K&R의 0~10과 대상·척도가 다릅니다(1장 측정이 결론을 정한다).", "시군구 226개로 Freitag의 24개 한계를 넘습니다. 다만 수도권 교란(2장 언어권)은 그대로 만납니다."],
  "youth2022": ["19~34세만이라 결과를 전 연령으로 옮길 수 없습니다(1장 외적 타당성, 라자스탄 2%).", "같은 0~10 사회 신뢰가 있는 KGSS와 연령대를 맞춰 비교합니다."],
  "elderly2023": ["65세 이상만, 그리고 기관신뢰 문항 원문이 보고서 표 기준이라 확인이 필요합니다(4장 회고·보고 편의).", "기초연금(하위 70% 선별)과 국민연금(보편)을 한 사람에게서 비교하면 K&R의 선별/보편 대비가 됩니다."],
}
COND = [  # (조건 키, 문장)
  ("med_any", "매개를 넣으면 세 화살표가 모두 같은 해 자료입니다. K&R도 그래서 '어느 정도'라고만 썼습니다(356쪽)."),
  ("med_fair_kipa", "이 문항은 '복지혜택을 받을 기회가 공정한가'입니다. K&R의 '받을 자격이 있는 것을 받았나'는 내 경험, 이것은 사회 평가입니다."),
  ("dv_inst", "기관신뢰는 1부에서 종속변수가 아니라 Krishna의 독립변수였습니다. 어느 쪽에 두느냐가 설계입니다."),
  ("iv_sel_koweps", "신청했으나 탈락한 집단이 보입니다. 심사 경험을 수급 여부와 떼어 잴 수 있는 국내 유일한 변수입니다."),
  ("iv_sel_chs", "'과거에 수급자였다'를 심사·탈락 경험의 대용으로 쓰는 것입니다. 대용임을 밝혀야 합니다."),
  ("iv_inst_kipa", "참여 제도 항목은 2023 이후 삭제되어 최근 해로는 못 합니다."),
  ("region_sgg", "시군구 평균은 개인 응답의 합산입니다(1부 집계 규칙). 시군구 안 분포도 봐야 합니다."),
  ("region_wide", "7권역·17시도로는 Freitag의 24개보다 적습니다. 지역 효과는 기술 통계로만."),
  ("q_cause", "이 자료로는 '관련이 있는가'까지입니다. 1부 다섯 편 중 '영향'을 쓸 수 있는 설계는 없었습니다."),
  ("neighbor_welfare", "이웃 신뢰는 마을 수준 개념(Krishna), 수급은 개인·가구 경험(K&R)입니다. 수준이 다릅니다."),
]
PAPERS = [["Krishna", "집합행동 성향 6문항 지수 0–100", "지수 안의 1문항"], ["Freitag", "결사체 4문항 주성분, 칸톤 평균", "통제변수, 다변량에서 비유의"],
          ["L&W", "Putnam 혼합 정의 + 잠재/동원", "측정 없음"], ["Mettler", "단체 가입 수(4유형) + 정치활동 6종", "측정 없음"], ["K&R", "대인신뢰 0–10 단일 문항", "종속변수. 참여는 통제"]]
json.dump({"base": REVIEWS, "cond": COND}, open(os.path.join(HERE, "reviews.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

HTML = r"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>내 연구모형</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.css">
<style>
:root{--ink:#15203a;--sub:#5a6577;--line:#e2e6ec;--navy:#072A60;--tint:#e9eef6;--green:#4F7F1C;--gtint:#f0f7e6}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font-family:Pretendard,"Noto Sans KR",sans-serif;font-size:16px;line-height:1.55}
main{max-width:640px;margin:0 auto;padding:20px 16px 90px}
.top{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--navy);padding-bottom:6px;margin-bottom:18px}
.top b{color:var(--navy)}.top span{color:var(--sub);font-size:13px}
h2{font-size:19px;color:var(--navy);margin:0 0 4px}h2::before{content:"";display:block;width:28px;height:3px;background:#8DC63F;margin-bottom:8px}
p.help{color:var(--sub);font-size:14px;margin:0 0 14px}
.scr{display:none}.scr.on{display:block}
.opt{display:block;width:100%;text-align:left;background:#fff;border:1px solid var(--line);border-left:3px solid var(--line);padding:11px 12px;margin:0 0 8px;font:inherit;color:var(--ink);cursor:pointer}
.opt small{display:block;color:var(--sub);font-size:13px;margin-top:2px}
.opt.sel{border-left-color:var(--navy);background:var(--tint)}
.opt.grey{color:#9aa2ae;border-style:dashed}.opt.grey small{color:#b3b9c3}
.opt .tag{float:right;color:var(--sub);font-size:12px;white-space:nowrap}
.srv{margin:14px 0 4px;font-size:14px;color:var(--navy);font-weight:700}
.why{border-left:3px solid var(--navy);background:var(--tint);padding:8px 12px;font-size:14px;margin:8px 0 12px}
input[type=text]{width:100%;font:inherit;padding:10px;border:1px solid var(--line)}
.nav{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--line);padding:10px 16px;display:flex;gap:8px;justify-content:space-between}
.nav button{font:inherit;padding:10px 18px;border:1px solid var(--navy);background:#fff;color:var(--navy);cursor:pointer}
.nav button.pri{background:var(--navy);color:#fff}.nav button:disabled{opacity:.35;cursor:default}
.card{border-top:2px solid var(--navy);padding:14px 0 6px;margin-top:18px}.card h3{margin:0 0 8px;font-size:17px;color:var(--navy)}
.card .k{font-size:13px;color:var(--sub)}.card b.w{color:var(--navy)}
.lin{background:var(--gtint);border-left:3px solid var(--green);padding:8px 12px;margin:8px 0}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin:8px 0}th{text-align:left;color:var(--sub);border-bottom:2px solid var(--navy);padding:6px 4px;font-weight:700}td{border-bottom:1px solid var(--line);padding:6px 4px;vertical-align:top}
.foot{position:fixed;left:0;right:0;bottom:54px;text-align:center;font-size:11px;color:var(--sub);background:#fff;padding:2px}
svg text{font-family:inherit}
.agg{margin-top:30px;border-top:1px dashed var(--line);padding-top:12px;font-size:14px;color:var(--sub)}
.bar{display:flex;align-items:center;gap:8px;margin:3px 0}.bar i{display:block;height:12px;background:var(--navy)}.bar span{width:150px}
</style></head><body><main>
<div class="top"><b>내 연구모형</b><span id="step"></span></div>

<section class="scr on" id="s0"><h2>별명</h2><p class="help">1부에서 쓴 별명이 있으면 그대로. 선택은 이 수업 안에서만 쓰고 끝나면 지웁니다.</p>
<input type="text" id="nick" placeholder="별명" maxlength="12"><p class="help" style="margin-top:8px"><a href="#" id="nonick">별명 없이 계속</a></p></section>

<section class="scr" id="s1"><h2>무엇을 사회자본으로 재겠습니까</h2><p class="help">1부 다섯 편도 여기서 갈렸습니다. 하나만 고릅니다.</p><div id="dv"></div></section>

<section class="scr" id="s2"><h2>그 개념을 묻는 문항</h2><p class="help">조사마다 다릅니다. 하나를 고르면 그 조사가 당신의 자료가 됩니다.</p><div id="items"></div></section>

<section class="scr" id="s3"><h2>무엇이 그것을 바꾼다고 보십니까</h2><p class="help">하나 이상. 흐린 묶음은 당신이 고른 조사에 없는 것입니다. 연령·교육·소득·고용은 모든 모형에 들어갑니다.</p><div id="iv"></div><div id="ivwhy"></div></section>

<section class="scr" id="s4"><h2>가운데 무엇을 거친다고 보십니까</h2><p class="help">없어도 됩니다.</p><div id="med"></div></section>

<section class="scr" id="s5"><h2>연구질문 한 줄</h2><p class="help">예: 기초생활보장 수급 심사 경험은 대인신뢰와 관련이 있는가. 비워도 됩니다.</p><input type="text" id="q" placeholder="~는 ~와 관련이 있는가" maxlength="120"></section>

<section class="scr" id="s6"><h2>당신의 모형</h2><p class="help">제출하면 고칠 수 없습니다.</p><div id="diagram"></div><p class="help" id="unit"></p></section>

<section class="scr" id="s7"><div id="cards"></div>
<div class="card"><h3>1부 다섯 편이 사회자본을 잰 것</h3><table><tr><th>논문</th><th>종속변수</th><th>신뢰의 자리</th></tr>__PAPERS__</table></div>
<div class="agg" id="agg"></div></section>
</main>
<div class="foot">선택은 이 수업 안에서만 쓰고 끝나면 지웁니다 · 계수는 계산하지 않습니다</div>
<div class="nav"><button id="back">이전</button><button id="next" class="pri" disabled>다음</button></div>
<script>
const CAT=__CAT__, REV=__REV__, SAVE_URL="";
const S=CAT.surveys, C=CAT.concepts, IT=CAT.items;
const IVG=[["welfare_selective","선별 수급 경험(자산조사)"],["welfare_universal","보편 수급·서비스 경험"],["public_service_experience","공공서비스 접촉 경험"],["institution_participation","참여 제도 경험"],["region","지역"]];
const MED=[["fairness","공정성 지각"],["trust_institution","기관신뢰"],[null,"없음"]];
let st={nick:"",dv:null,item:null,iv:[],med:undefined,q:"",survey:null}, cur=0;
const $=id=>document.getElementById(id), cname=id=>(C.find(c=>c.id===id)||{}).label||id, sname=k=>(S[k]||{}).name||k;
// 지역은 공개 변수가 확인된 조사만 켠다(복지패널·사회통합은 catalog에 '확인 필요' 메모만 있음 → 회색)
const avail=(concept,survey)=>IT.filter(i=>i.concept===concept&&i.survey===survey&&!(concept==='region'&&/확인 필요|미확인/.test((i.question||'')+(i.note||''))));
const ivWhy=(g)=>{const where=[...new Set(IT.filter(i=>i.concept===g).map(i=>sname(i.survey)))];return `이 두 문항은 같은 사람에게 없습니다. ${cname(st.dv)}은 ${sname(st.survey)}에, ${cname(g)}은 ${where.join('·')||'다른 조사'}에 있습니다.`};
function render(){
  document.querySelectorAll('.scr').forEach((s,i)=>s.classList.toggle('on',i===cur));
  $('step').textContent=cur===0?'':cur<7?`${cur}/6`:'결과';
  $('back').style.visibility=cur===0||cur===7?'hidden':'visible';
  $('next').textContent=cur===6?'제출':cur===7?'처음으로':'다음';
  if(cur===1){$('dv').innerHTML=C.filter(c=>c.role==='dv').map(c=>`<button class="opt ${st.dv===c.id?'sel':''}" data-v="${c.id}">${c.label}<small>1부: ${c.paper_measure}</small></button>`).join('');
    $('dv').onclick=e=>{const b=e.target.closest('.opt');if(!b)return;st.dv=b.dataset.v;st.item=null;st.survey=null;st.iv=[];st.med=undefined;render();};}
  if(cur===2){const its=IT.filter(i=>i.concept===st.dv),bys={};its.forEach(i=>(bys[i.survey]=bys[i.survey]||[]).push(i));
    $('items').innerHTML=Object.entries(bys).map(([s,arr])=>`<div class="srv">${sname(s)} <span style="font-weight:400;color:var(--sub)">· ${S[s].unit}</span></div>`+arr.map(i=>{const k=IT.indexOf(i);return `<button class="opt ${st.item===k?'sel':''}" data-k="${k}"><span class="tag">${i.wave||''}</span>${i.question}<small>${i.scale||''}${i.note?' · '+i.note:''}</small></button>`}).join('')).join('');
    $('items').onclick=e=>{const b=e.target.closest('.opt');if(!b)return;st.item=+b.dataset.k;st.survey=IT[st.item].survey;st.iv=[];st.med=undefined;render();};}
  if(cur===3){$('iv').innerHTML=IVG.map(([g,l])=>{const a=avail(g,st.survey),ok=a.length>0,on=st.iv.includes(g);
      return `<button class="opt ${on?'sel':''} ${ok?'':'grey'}" data-g="${g}">${l}<small>${ok?a.slice(0,2).map(i=>i.question).join(' / ')+(a.length>2?' 외 '+(a.length-2):''):sname(st.survey)+'에 없음'}</small></button>`}).join('');
    $('ivwhy').innerHTML='';
    $('iv').onclick=e=>{const b=e.target.closest('.opt');if(!b)return;const g=b.dataset.g;if(b.classList.contains('grey')){$('ivwhy').innerHTML=`<div class="why">${ivWhy(g)}</div>`;return;}
      st.iv=st.iv.includes(g)?st.iv.filter(x=>x!==g):[...st.iv,g];render();};}
  if(cur===4){$('med').innerHTML=MED.filter(([m])=>!(m==='trust_institution'&&st.dv==='trust_institution')).map(([m,l])=>{const ok=m===null||avail(m,st.survey).length>0;
      return `<button class="opt ${st.med===m?'sel':''} ${ok?'':'grey'}" data-m="${m===null?'':m}">${l}<small>${m===null?'':ok?avail(m,st.survey)[0].question:sname(st.survey)+'에 없음'}</small></button>`}).join('');
    $('med').onclick=e=>{const b=e.target.closest('.opt');if(!b||b.classList.contains('grey'))return;st.med=b.dataset.m||null;render();};}
  if(cur===6){st.q=$('q').value.trim();$('diagram').innerHTML=diagram();const it=IT[st.item],units=[...new Set([it.unit,...st.iv.flatMap(g=>avail(g,st.survey).map(i=>i.unit))].filter(Boolean))];
    $('unit').textContent=`자료: ${sname(st.survey)} ${it.wave||''} · 단위: ${units.length>1?'종속 '+it.unit+' / 독립 '+units.filter(u=>u!==it.unit).join('·'):units[0]||'개인'}`;}
  if(cur===7){$('cards').innerHTML=cards();agg();}
  $('next').disabled=[true,!st.dv,st.item===null,st.iv.length===0,st.med===undefined,false,false,false][cur]===true;
  if(cur===0)$('next').disabled=false;
  window.scrollTo(0,0);
}
function diagram(){const boxes=[...st.iv.map(g=>cname(g)),'개인 특성(연령·교육·소득·고용)'],h=Math.max(150,boxes.length*44+20),w=600;
  let s=`<svg viewBox="0 0 ${w} ${h}" width="100%" style="max-height:320px">`;
  boxes.forEach((b,i)=>{const y=10+i*44;s+=`<rect x="4" y="${y}" width="200" height="34" fill="#fff" stroke="#072A60" stroke-width="1.2"/><text x="104" y="${y+22}" font-size="12" text-anchor="middle" fill="#15203a">${b.length>18?b.slice(0,17)+'…':b}</text><line x1="204" y1="${y+17}" x2="${st.med?236:356}" y2="${h/2}" stroke="#5a6577" stroke-width="1"/>`});
  if(st.med)s+=`<rect x="238" y="${h/2-17}" width="120" height="34" fill="#f0f7e6" stroke="#4F7F1C" stroke-width="1.2"/><text x="298" y="${h/2+5}" font-size="12" text-anchor="middle">${cname(st.med)}</text><line x1="358" y1="${h/2}" x2="396" y2="${h/2}" stroke="#5a6577"/>`;
  s+=`<polygon points="390,${h/2-5} 398,${h/2} 390,${h/2+5}" fill="#5a6577"/><rect x="398" y="${h/2-17}" width="198" height="34" fill="#e9eef6" stroke="#072A60" stroke-width="1.6"/><text x="497" y="${h/2+5}" font-size="12.5" font-weight="700" text-anchor="middle" fill="#072A60">${cname(st.dv)}</text></svg>`;return s;}
function lineage(){const dv=st.dv,iv=st.iv,med=st.med,T=['trust_general','trust_social','trust_institution','trust_neighbor'],P=['participation','volunteer_donate','political_participation'];
  const has=g=>iv.includes(g),wel=has('welfare_selective')||has('welfare_universal');
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
function review(){const it=IT[st.item],s=st.survey,out=[];const b=REV.base[s];if(b)out.push(['약한 고리',b[0]],['한 단계',b[1]]);
  const c=Object.fromEntries(REV.cond);const add=k=>out.push(['덧붙임',c[k]]);
  if(st.med)add('med_any');if(st.med==='fairness'&&s==='kipa')add('med_fair_kipa');if(st.dv==='trust_institution')add('dv_inst');
  if(st.iv.includes('welfare_selective')&&s==='koweps')add('iv_sel_koweps');if(st.iv.includes('welfare_selective')&&s==='chs')add('iv_sel_chs');
  if(st.iv.includes('institution_participation')&&s==='kipa')add('iv_inst_kipa');
  if(st.iv.includes('region'))add(s==='chs'?'region_sgg':'region_wide');if(/영향/.test(st.q))add('q_cause');
  if(st.dv==='trust_neighbor'&&(st.iv.includes('welfare_selective')||st.iv.includes('welfare_universal')))add('neighbor_welfare');return out;}
const B=t=>t.replace(/\((\d장[^)]*)\)/g,'(<b class="w">$1</b>)');
function cards(){const it=IT[st.item],[lt,ch]=lineage(),rv=review();
  return `<div class="card"><h3>① 당신의 모형</h3>${diagram()}<p class="k">종속: ${it.question} (${it.scale||''}) · ${sname(st.survey)} ${it.wave||''}</p>${st.iv.map(g=>`<p class="k">독립 ${cname(g)}: ${avail(g,st.survey).map(i=>i.question).join(' / ')}</p>`).join('')}${st.med?`<p class="k">매개 ${cname(st.med)}: ${avail(st.med,st.survey).map(i=>i.question).join(' / ')}</p>`:''}${st.q?`<p class="k">질문: ${st.q}</p>`:''}</div>
  <div class="card"><h3>② 어느 논리인가</h3><div class="lin"><b>${lt}</b><br><span class="k">${ch==='밖'?'1부에 없던 조합입니다. 선행연구가 없어서일 수도, 자료가 없어서일 수도 있습니다.':'1부 '+ch+'에서 본 논리입니다.'}</span></div></div>
  <div class="card"><h3>③ 약한 고리와 한 단계</h3>${rv.map(([k,t])=>`<p><span class="k">${k}</span><br>${B(t)}</p>`).join('')}</div>`;}
function save(){const row={ts:new Date().toISOString(),nick:st.nick,stage:'model',key:'submit',value:{dv:st.dv,item:st.item,survey:st.survey,iv:st.iv,med:st.med,q:st.q,lineage:lineage()[1]}};
  try{const a=JSON.parse(localStorage.getItem('w11_model')||'[]');a.push(row);localStorage.setItem('w11_model',JSON.stringify(a));}catch(e){}
  if(SAVE_URL)fetch(SAVE_URL,{method:'POST',mode:'no-cors',body:JSON.stringify(row)}).catch(()=>{});}
function agg(){let a=[];try{a=JSON.parse(localStorage.getItem('w11_model')||'[]')}catch(e){}if(a.length<2)return $('agg').innerHTML='';
  const cnt={};a.forEach(r=>cnt[r.value.dv]=(cnt[r.value.dv]||0)+1);const mx=Math.max(...Object.values(cnt));
  $('agg').innerHTML=`<b>이 브라우저의 제출 ${a.length}건(데모 집계)</b>`+C.filter(c=>c.role==='dv').map(c=>`<div class="bar"><span>${c.label}</span><i style="width:${(cnt[c.id]||0)/mx*300}px"></i>${cnt[c.id]||0}</div>`).join('')+`<p><a href="#" id="clr">집계 지우기</a></p>`;$('clr').onclick=e=>{e.preventDefault();localStorage.removeItem('w11_model');agg();};}
$('next').onclick=()=>{if(cur===0)st.nick=$('nick').value.trim();if(cur===6)save();if(cur===7){st={nick:st.nick,dv:null,item:null,iv:[],med:undefined,q:"",survey:null};$('q').value='';cur=1;}else cur++;render();};
$('back').onclick=()=>{cur=Math.max(1,cur-1);render();};
$('nonick').onclick=e=>{e.preventDefault();st.nick='';cur=1;render();};
render();
</script></body></html>"""
papers_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in PAPERS)
out = HTML.replace("__CAT__", json.dumps(CAT, ensure_ascii=False)).replace("__REV__", json.dumps({"base": REVIEWS, "cond": COND}, ensure_ascii=False)).replace("__PAPERS__", papers_rows)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("index.html", len(out) // 1024, "KB · 리뷰 기본", len(REVIEWS), "조건", len(COND))
