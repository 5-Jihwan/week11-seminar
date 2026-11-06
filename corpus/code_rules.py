# -*- coding: utf-8 -*-
"""선행연구 후보를 API 없이 키워드 규칙으로 코딩한다(미검수). 입력은 셋을 합친다: candidates_quant.csv(초기 346, 5편 인용망), candidates_kci.csv(국내 전수), candidates_oa.csv(해외 전수).
칸은 code_studies.py(API)와 같고 coder=rules, verified=FALSE. 국내 초록은 자료명(사회통합실태조사 등)이 나오는 편이라 data 칸을 채우고 country=KR.
실행: python corpus/code_rules.py → corpus/studies.csv"""
import csv, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
H = Path(__file__).parent; DST = H / "studies.csv"

COMP = [  # (구성 요소, 패턴) — 영문·국문
    ("generalized_trust", r"generali[sz]ed trust|social trust|interpersonal trust|trust in (other )?people|most people can be trusted|일반\s*신뢰|대인\s*신뢰|사회\s*적?\s*신뢰|타인\s*신뢰|일반화된 신뢰"),
    ("institutional_trust", r"institutional trust|political trust|trust in (the )?(government|institutions|state|police|parliament)|confidence in (government|institutions)|기관\s*신뢰|정부\s*신뢰|정치\s*신뢰|제도\s*신뢰|공공기관.{0,6}신뢰"),
    ("neighbor_trust", r"neigh?bou?rhood trust|trust in neigh?bou?rs|neighbou?rs? (can be )?trust|이웃\s*신뢰|이웃에 대한 신뢰|지역사회 신뢰|동네 신뢰"),
    ("participation", r"associational|voluntary (association|organi[sz]ation)|civic (engagement|participation)|group membership|membership in|organi[sz]ational membership|단체\s*참여|결사체|시민\s*참여|단체\s*활동|조직\s*참여|사회참여|모임 참여"),
    ("volunteer_donate", r"volunteer|donat|charit|자원봉사|기부|후원"),
    ("network", r"social network|network (size|ties|density)|ties with|weak ties|연결망|네트워크|사회적 관계망|관계망|교류"),
    ("reciprocity", r"reciprocit|mutual (help|aid|assistance)|help(ing)? (each other|neighbo)|informal (help|support)|호혜|상호부조|상호\s*호혜|이웃 간 도움|도움을 주고받"),
    ("political_participation", r"political participation|voting|voter turnout|turnout|protest|petition|정치\s*참여|투표|집회|서명"),
]
UNIT = [("country", r"cross-national|cross-country|countries|nations?\b|국가\s*비교|국가\s*간|국가\s*수준"), ("region", r"\bregion|county|counties|municipalit|provinc|canton|neighbou?rhoods?|지역\s*수준|시군구|지자체|시·?도|읍면동|동네|마을"), ("individual", r"individual-level|individuals|respondents|survey of|설문|응답자|개인\s*수준")]
DESIGN = [("experiment", r"randomi[sz]ed|field experiment|lab experiment|실험\s*(집단|설계|연구)"), ("quasi_experiment", r"quasi-experiment|natural experiment|difference-in-differences|regression discontinuity|instrumental variable|자연실험|준실험|이중차분|도구변수|회귀불연속"),
          ("panel", r"\bpanel\b|longitudinal|fixed effects|two waves|over time|패널|종단|고정효과"), ("cross_section", r"cross-sectional|survey data|횡단|설문조사|실태조사")]
IV = {"iv_institution": r"welfare state|welfare (program|benefit|polic)|means-test|universal(ism)?|social polic|public polic|policy feedback|government (quality|performance)|institution(al)? (quality|design|trust)|decentrali[sz]|direct democracy|local government|participatory budget|복지|제도|정책|지방정부|분권|주민참여|공공서비스|행정서비스|정부",
      "iv_network": r"associational|membership|voluntary|network|결사체|단체|연결망|네트워크|모임", "iv_region": r"regional|county|neighbou?rhood|municipal|urban|rural|지역|도시|농촌|시군구|마을|동네",
      "iv_individual": r"education|income|age|gender|socio-?economic|학력|소득|연령|성별|교육수준|경제활동"}
LINEAGE = [("kr", r"welfare state|welfare (program|benefit|institution|polic)|means-test|universal|복지|수급"), ("mettler", r"policy feedback|G\.?I\.? Bill|program (participation|use)|beneficiar|정책환류|수혜|정책 경험"),
           ("freitag", r"direct democracy|political institution|federal|canton|decentrali|consensus democracy|직접민주|정치제도|주민투표|분권"), ("lw", r"local government|local governance|institutional design|municipal|participatory|지방정부|거버넌스|제도설계|지방자치|주민참여"),
           ("krishna", r"village|community (organi|develop|initiative)|self-help|local leader|collective action|마을|공동체|집합행동|마을만들기|주민조직")]
DATA = r"World Values Survey|\bWVS\b|European Social Survey|\bESS\b|General Social Survey|\bGSS\b|Eurobarometer|Afrobarometer|Latinobar[oó]metro|\bSOEP\b|\bKGSS\b|KoWePS|\bKLIPS\b|한국복지패널|복지패널|사회통합실태조사|지역사회건강조사|한국종합사회조사|사회조사|청년\s*삶\s*실태조사|노인실태조사|노동패널|가계금융복지조사|서울\s*서베이|서울서베이|주거실태조사|청소년패널|아동패널|여성가족패널|고령화연구패널|KLoSA|Social Capital Community Benchmark|Current Population Survey|Add Health|British Household Panel|Swiss Household Panel|Understanding Society|\bISSP\b|Asian Barometer|아시아 바로미터|\bKSDC\b|\bKLoSA\b"
SC_DV = r"determinants? of (social capital|trust)|(sources|origins|production|formation|creation) of (social capital|trust)|(what|how).{0,40}(shape|build|produce|generate|erode|undermine|affect|influence).{0,20}(social capital|trust)|(social capital|trust) as (a )?dependent|(effects?|impact|influence) (of .{0,60})?on (social capital|(social |generalized )?trust)|사회\s*적?\s*자본(의|에)\s*(결정|영향|형성|미치는)|사회\s*적?\s*자본\s*형성|사회\s*적?\s*자본에\s*미치는|신뢰(의|에)\s*(결정|영향|미치는)|사회\s*적?\s*자본을\s*종속"
COMP_KO = {"generalized_trust": "일반신뢰", "institutional_trust": "기관신뢰", "neighbor_trust": "이웃 신뢰", "participation": "단체 참여", "volunteer_donate": "봉사·기부", "network": "연결망", "reciprocity": "호혜", "political_participation": "정치 참여"}
UNIT_KO = {"individual": "개인", "region": "지역", "country": "국가", "mixed": "다수준", "": ""}


def hit(pat, t): return re.search(pat, t, re.I) is not None


def code(r, src):
    t = " ".join([r.get("title", ""), r.get("title_en", ""), r.get("abstract", ""), r.get("abstract_en", "")])
    comps = [c for c, p in COMP if hit(p, t)]
    units = [u for u, p in UNIT if hit(p, t)]
    unit = "mixed" if len(units) > 1 and "individual" in units else (units[0] if units else "")
    design = next((d for d, p in DESIGN if hit(p, t)), "")
    iv = {k: ("Y" if hit(p, t) else "") for k, p in IV.items()}
    lineage = next((l for l, p in LINEAGE if hit(p, t)), "none")
    sc_dv = hit(SC_DV, t)
    dv_type = ("multiple" if len(comps) > 1 else {"generalized_trust": "generalized_trust", "institutional_trust": "institutional_trust", "neighbor_trust": "generalized_trust",
               "participation": "participation", "volunteer_donate": "participation", "political_participation": "participation", "network": "other", "reciprocity": "other"}.get(comps[0], "other")) if comps else ""
    m = re.search(DATA, t); data = m.group(0) if m else ""
    data = {"복지패널": "한국복지패널", "KoWePS": "한국복지패널", "KGSS": "한국종합사회조사", "KLIPS": "노동패널", "서울 서베이": "서울서베이"}.get(data, data)
    mediator = "Y" if hit(r"mediat|매개", t) else ""; moderator = "Y" if hit(r"moderat|interaction effect|조절\s*효과|조절변수|집단\s*(간|별)\s*(차이|비교)", t) else ""
    country = "KR" if src == "kci" or hit(r"\bKorea|한국|우리나라", t) else ""
    line = (f"이 연구는 사회자본을 {'·'.join(COMP_KO[c] for c in comps)}{'(' + data + ')' if data else ''}로 {UNIT_KO[unit] + ' 단위에서 ' if unit else ''}쟀다" if comps else "초록에 측정 방식이 없다")
    return {"country": country, "data": data, "unit": unit, "dv_type": dv_type, "dv_measure": ", ".join(COMP_KO[c] for c in comps), "dv_components": "|".join(comps), "measure_line": line, "sc_dv": "Y" if sc_dv else "",
            **iv, "mediator": mediator, "moderator": moderator, "design": design, "result_direction": "", "lineage": lineage, "verified": "FALSE", "coder": "rules", "src": src,
            "notes": ("초록에 '사회자본·신뢰의 결정요인·형성' 단서 있음. " if sc_dv else "") + "키워드 규칙 코딩(미검수). 초록 기준."}


cols = "id,src,authors,year,title,journal,link,country,data,unit,dv_type,dv_measure,dv_components,measure_line,sc_dv,iv_institution,iv_individual,iv_region,iv_network,mediator,moderator,design,result_direction,lineage,verified,coder,notes,seeds,cited_by".split(",")
SRCS = [("candidates_quant.csv", "openalex"), ("candidates_oa.csv", "openalex"), ("candidates_kci.csv", "kci")]
seen, out, stat = set(), [], {"kci": 0, "openalex": 0, "comps": 0, "sc_dv": 0, "data": 0}
for fn, src in SRCS:
    p = H / fn
    if not p.exists():
        continue
    for r in csv.DictReader(open(p, encoding="utf-8-sig")):
        key = (r.get("doi") or r["id"]).lower()
        if key in seen:
            continue
        seen.add(key); c = code(r, src)
        link = ("https://doi.org/" + r["doi"]) if r.get("doi") else (r.get("url") or (f"https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId={r['id']}" if src == "kci" else ""))
        out.append({**c, "id": r["id"], "authors": r.get("authors", ""), "year": r.get("year", ""), "title": r.get("title", ""), "journal": r.get("venue") or r.get("journal", ""), "link": link, "seeds": r.get("seeds", ""), "cited_by": r.get("cited_by") or r.get("cited", "")})
        stat[src] += 1; stat["comps"] += bool(c["dv_components"]); stat["sc_dv"] += bool(c["sc_dv"]); stat["data"] += bool(c["data"])
with open(DST, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
print(f"{len(out)}편 → {DST.name} · 국내 {stat['kci']} · 해외 {stat['openalex']} · 구성요소 있음 {stat['comps']} · 종속 단서 {stat['sc_dv']} · 자료명 {stat['data']}")
