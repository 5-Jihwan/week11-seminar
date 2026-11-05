# -*- coding: utf-8 -*-
"""선행연구 후보 346편을 API 없이 키워드 규칙으로 코딩한다(데모용). 칸은 code_studies.py(API)와 같고 coder=rules, verified=FALSE.
초록에 단서가 없으면 빈칸. 실행: python corpus/code_rules.py → corpus/studies.csv"""
import csv, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(__file__).with_name("candidates_quant.csv"); DST = Path(__file__).with_name("studies.csv")

COMP = [  # (구성 요소, 패턴)
    ("generalized_trust", r"generali[sz]ed trust|social trust|interpersonal trust|trust in (other )?people|most people can be trusted|일반신뢰|대인신뢰|사회적 신뢰|사회신뢰"),
    ("institutional_trust", r"institutional trust|political trust|trust in (the )?(government|institutions|state|police|parliament)|confidence in (government|institutions)|기관신뢰|정부신뢰|정치신뢰|제도신뢰"),
    ("neighbor_trust", r"neigh?bou?rhood trust|trust in neigh?bou?rs|neighbou?rs? (can be )?trust|이웃 신뢰|이웃신뢰"),
    ("participation", r"associational|voluntary (association|organi[sz]ation)|civic (engagement|participation)|group membership|membership in|organi[sz]ational membership|단체 참여|결사체|시민참여|단체참여"),
    ("volunteer_donate", r"volunteer|donat|charit|자원봉사|기부"),
    ("network", r"social network|network (size|ties|density)|ties with|weak ties|연결망|네트워크"),
    ("reciprocity", r"reciprocit|mutual (help|aid|assistance)|help(ing)? (each other|neighbo)|informal (help|support)|호혜|상호부조|이웃 간 도움"),
    ("political_participation", r"political participation|voting|voter turnout|turnout|protest|petition|정치참여|투표"),
]
UNIT = [("country", r"cross-national|cross-country|countries|nations?\b|국가 비교|국가간"), ("region", r"\bregion|county|counties|municipalit|provinc|canton|neighbou?rhoods?|지역|시군구|지자체"), ("individual", r"individual-level|individuals|respondents|survey of|설문|응답자")]
DESIGN = [("experiment", r"randomi[sz]ed|field experiment|lab experiment|실험"), ("quasi_experiment", r"quasi-experiment|natural experiment|difference-in-differences|regression discontinuity|instrumental variable|자연실험|준실험"),
          ("panel", r"\bpanel\b|longitudinal|fixed effects|two waves|over time|패널|종단"), ("cross_section", r"cross-sectional|survey data|횡단")]
IV = {"iv_institution": r"welfare state|welfare (program|benefit|polic)|means-test|universal(ism)?|social polic|public polic|policy feedback|government (quality|performance)|institution(al)? (quality|design|trust)|decentrali[sz]|direct democracy|local government|participatory budget|복지|제도|정책|지방정부|분권|주민참여",
      "iv_network": r"associational|membership|voluntary|network|결사체|단체|연결망", "iv_region": r"regional|county|neighbou?rhood|municipal|urban|rural|지역|도시|농촌|시군구",
      "iv_individual": r"education|income|age|gender|socio-?economic|학력|소득|연령|성별"}
LINEAGE = [("kr", r"welfare state|welfare (program|benefit|institution|polic)|means-test|universal|복지"), ("mettler", r"policy feedback|G\.?I\.? Bill|program (participation|use)|beneficiar|정책환류|수혜"),
           ("freitag", r"direct democracy|political institution|federal|canton|decentrali|consensus democracy|직접민주|정치제도"), ("lw", r"local government|local governance|institutional design|municipal|participatory|지방정부|거버넌스|제도설계"),
           ("krishna", r"village|community (organi|develop|initiative)|self-help|local leader|collective action|마을|공동체|집합행동")]
COMP_KO = {"generalized_trust": "일반신뢰", "institutional_trust": "기관신뢰", "neighbor_trust": "이웃 신뢰", "participation": "단체 참여", "volunteer_donate": "봉사·기부", "network": "연결망", "reciprocity": "호혜", "political_participation": "정치 참여"}
UNIT_KO = {"individual": "개인", "region": "지역", "country": "국가", "mixed": "다수준", "": ""}


def hit(pat, t): return re.search(pat, t, re.I) is not None


def code(r):
    t = (r["title"] + " " + r["abstract"])
    comps = [c for c, p in COMP if hit(p, t)]
    units = [u for u, p in UNIT if hit(p, t)]
    unit = "mixed" if len(units) > 1 and "individual" in units else (units[0] if units else "")
    design = next((d for d, p in DESIGN if hit(p, t)), "")
    iv = {k: ("Y" if hit(p, t) else "") for k, p in IV.items()}
    lineage = next((l for l, p in LINEAGE if hit(p, t)), "none")
    sc_dv = hit(r"determinants? of (social capital|trust)|(sources|origins|production|formation|creation) of (social capital|trust)|(what|how).{0,40}(shape|build|produce|generate|erode|undermine).{0,20}(social capital|trust)|(social capital|trust) as (a )?dependent|effects? on (social capital|trust)|사회자본의 결정요인|신뢰의 결정요인|사회자본 형성", t)
    # 종속 여부는 초록만으로 못 가르는 편이 많아(후보는 모두 다섯 편의 인용 논문) 구성 요소로 유형을 매기고, 종속 단서는 notes에만 남긴다
    dv_type = ("multiple" if len(comps) > 1 else {"generalized_trust": "generalized_trust", "institutional_trust": "institutional_trust", "neighbor_trust": "generalized_trust",
               "participation": "participation", "volunteer_donate": "participation", "political_participation": "participation", "network": "other", "reciprocity": "other"}.get(comps[0], "other")) if comps else ""
    data = next((m.group(0) for m in [re.search(r"World Values Survey|WVS|European Social Survey|ESS|General Social Survey|GSS|Eurobarometer|Afrobarometer|Latinobarómetro|SOEP|KGSS|KoWePS|한국복지패널|사회통합실태조사|지역사회건강조사|Social Capital Community Benchmark|Current Population Survey|Add Health|British Household Panel|Swiss Household Panel|Understanding Society|ISSP", t)] if m), "")
    mediator = "Y" if hit(r"mediat|매개", t) else ""
    line = (f"이 연구는 사회자본을 {'·'.join(COMP_KO[c] for c in comps)}{'(' + data + ')' if data else ''}로 {UNIT_KO[unit] + ' 단위에서 ' if unit else ''}쟀다"
            if comps else "초록에 측정 방식이 없다")
    return {"country": "", "data": data, "unit": unit, "dv_type": dv_type, "dv_measure": ", ".join(COMP_KO[c] for c in comps), "dv_components": "|".join(comps), "measure_line": line,
            **iv, "mediator": mediator, "moderator": "", "design": design, "result_direction": "", "lineage": lineage, "verified": "FALSE", "coder": "rules",
            "notes": ("초록에 '사회자본·신뢰의 결정요인·형성' 단서 있음. " if sc_dv else "") + "키워드 규칙 코딩(미검수). 초록 기준."}


cols = "id,authors,year,title,journal,link,country,data,unit,dv_type,dv_measure,dv_components,measure_line,iv_institution,iv_individual,iv_region,iv_network,mediator,moderator,design,result_direction,lineage,verified,coder,notes,seeds,cited_by".split(",")
rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
out, stat = [], {"comps": 0, "dv": 0, "unit": 0, "design": 0}
with open(DST, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows:
        c = code(r)
        stat["comps"] += bool(c["dv_components"]); stat["dv"] += c["dv_type"] not in ("", "other"); stat["unit"] += bool(c["unit"]); stat["design"] += bool(c["design"])
        w.writerow({**c, "id": r["id"], "authors": r["authors"], "year": r["year"], "title": r["title"], "journal": r["venue"], "link": ("https://doi.org/" + r["doi"]) if r["doi"] else "", "seeds": r["seeds"], "cited_by": r["cited_by"]})
print(f"{len(rows)}편 → {DST.name} · 구성요소 있음 {stat['comps']} · 사회자본이 종속 {stat['dv']} · 단위 {stat['unit']} · 설계 {stat['design']}")
assert len(rows) == 346
