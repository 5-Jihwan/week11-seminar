"""후보 표(candidates_kci.csv · candidates_oa.csv · candidates_quant.csv)의 초록을 Haiku 5.5 배치 API로 구조 코딩한다(규칙 코딩과 같은 칸 + 사회자본이 종속인가).

사용:
  python -I corpus/code_studies.py dry                 # 요청 1건 미리보기, API 없음
  python corpus/code_studies.py submit [N] [kci|oa]    # 배치 제출(N편만, 출처만 고를 수 있음) → corpus/.batch_id 에 id 누적
  python corpus/code_studies.py collect                # 모든 배치 결과 수거 → corpus/studies_haiku.csv, studies.csv에 합침(haiku가 규칙을 덮음)
키는 환경변수 ANTHROPIC_API_KEY(레포에 넣지 않는다). anthropic SDK는 사용자 site-packages에 있어 submit/collect는 -I 없이 실행.
"""
import csv, json, os, sys, time
from pathlib import Path

MODEL = "claude-haiku-5-5"  # 수업 때 17명 이상이 같은 모델을 쓰므로 코딩도 같은 모델로 고정(11-05 Ji)
H = Path(__file__).parent; BATCH_ID_FILE = H / ".batch_id"; OUT = H / "studies_haiku.csv"; MERGED = H / "studies.csv"
SRCS = [("candidates_kci.csv", "kci"), ("candidates_oa.csv", "openalex"), ("candidates_quant.csv", "openalex")]
ENUM = {
    "unit": ["individual", "region", "country", "mixed", ""],
    "design": ["cross_section", "panel", "quasi_experiment", "experiment", "other", ""],
    "result_direction": ["positive", "negative", "mixed", "null", ""],
    "component": ["generalized_trust", "institutional_trust", "neighbor_trust", "participation", "volunteer_donate", "network", "reciprocity", "political_participation"],
}
SCHEMA = {
    "type": "object",
    "properties": {
        "is_quant": {"type": "boolean", "description": "경험적 자료로 통계 분석을 한 연구이면 true. 이론·리뷰·서평·메타분석이면 false"},
        "sc_dv": {"type": "boolean", "description": "사회자본(또는 그 구성 요소인 신뢰·참여·호혜·연결망)이 종속변수(결과)로 분석되면 true. 독립·매개·조절로만 쓰이면 false"},
        "country": {"type": "string", "description": "자료의 국가. 한국이면 'KR', 다국가면 'multi'. 모르면 빈 문자열"},
        "data": {"type": "string", "description": "자료 이름(사회통합실태조사, 한국복지패널, WVS, ESS, 자체 설문 등). 초록에 없으면 빈 문자열"},
        "unit": {"type": "string", "enum": ENUM["unit"], "description": "분석 단위"},
        "dv_components": {"type": "array", "items": {"type": "string", "enum": ENUM["component"]}, "description": "사회자본 측정에 묶인 구성 요소 전부(종속이든 아니든 사회자본을 잰 방식). 초록에 없으면 빈 배열"},
        "dv_measure": {"type": "string", "description": "사회자본 측정 방식 한 구절(예: 일반신뢰 단일 문항 4점). 없으면 빈 문자열"},
        "measure_line": {"type": "string", "description": "학생 화면에 붙일 한국어 한 문장: '이 연구는 사회자본을 ○○(자료·문항·단위)로 쟀다'. 측정 정보가 없으면 '초록에 측정 방식이 없다'"},
        "iv_institution": {"type": "boolean", "description": "제도·정책·정부·복지·공공서비스가 독립변수에 있으면 true"},
        "iv_individual": {"type": "boolean", "description": "개인 특성(소득·학력·연령 등)이 독립변수에 있으면 true"},
        "iv_region": {"type": "boolean", "description": "지역·국가 수준 특성이 독립변수에 있으면 true"},
        "iv_network": {"type": "boolean", "description": "결사체·연결망·공동체 활동이 독립변수에 있으면 true"},
        "mediator": {"type": "boolean"}, "moderator": {"type": "boolean"},
        "design": {"type": "string", "enum": ENUM["design"]},
        "result_direction": {"type": "string", "enum": ENUM["result_direction"], "description": "제도·정책 변수가 사회자본과 맺는 관계의 방향. 해당 없으면 빈 문자열"},
        "notes": {"type": "string", "description": "한국어 한 문장. 인과 표현 금지('영향을 미친다' 대신 '관련이 있다')"},
    },
    "required": ["is_quant", "sc_dv", "country", "data", "unit", "dv_components", "dv_measure", "measure_line", "iv_institution", "iv_individual", "iv_region", "iv_network", "mediator", "moderator", "design", "result_direction", "notes"],
    "additionalProperties": False,
}
SYSTEM = """당신은 사회자본 연구를 코딩하는 연구 보조원이다. 제목과 초록만 보고 아래 칸을 채운다.
규칙: 초록에 없는 내용은 빈 값으로 둔다. 추측하지 않는다. 논문을 지어내지 않는다.
먼저 양적 연구인지, 다음으로 사회자본(신뢰·참여·호혜·연결망)이 종속변수인지 판단한다. 사회자본이 건강·성과 등의 원인으로만 쓰였으면 sc_dv=false.
국문 초록과 영문 초록이 둘 다 있으면 둘을 합쳐 본다. notes는 한국어 한 문장, 인과 표현 금지."""
COLS = "id,src,authors,year,title,journal,link,country,data,unit,dv_type,dv_measure,dv_components,measure_line,sc_dv,iv_institution,iv_individual,iv_region,iv_network,mediator,moderator,design,result_direction,lineage,verified,coder,notes,seeds,cited_by".split(",")


def load():
    rows, seen = [], set()
    for fn, src in SRCS:
        p = H / fn
        if not p.exists():
            continue
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            key = (r.get("doi") or r["id"]).lower()
            if key in seen or not (r.get("abstract") or r.get("abstract_en")):
                continue
            seen.add(key); r["_src"] = src; rows.append(r)
    return rows


def build_request(r):
    ab = r.get("abstract", "") + (("\n[영문 초록] " + r["abstract_en"]) if r.get("abstract_en") else "")
    return {"custom_id": r["id"][:64], "params": {"model": MODEL, "max_tokens": 1200, "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}}, "system": SYSTEM,
            "messages": [{"role": "user", "content": f"제목: {r.get('title','')}{(' / ' + r['title_en']) if r.get('title_en') else ''}\n연도: {r.get('year','')}\n학술지: {r.get('venue') or r.get('journal','')}\n초록: {ab[:6000]}"}]}}


def dry():
    rows = load(); print(len(rows), "rows"); print(json.dumps(build_request(rows[0]), ensure_ascii=False, indent=1)[:2500])


def submit(n=None, only=None):
    import anthropic
    client = anthropic.Anthropic()
    rows = [r for r in load() if not only or r["_src"] == ("openalex" if only == "oa" else only)]
    done = set(json.loads(l)["id"] for l in open(H / ".submitted.jsonl", encoding="utf-8")) if (H / ".submitted.jsonl").exists() else set()
    rows = [r for r in rows if r["id"][:64] not in done]
    if n and str(n).isdigit() and int(n) > 0: rows = rows[:int(n)]  # 0·all 이면 전부
    if not rows:
        print("nothing to submit", file=sys.stderr); return
    ids = []
    for i in range(0, len(rows), 10000):  # 배치당 1만 건
        chunk = rows[i:i + 10000]; batch = client.messages.batches.create(requests=[build_request(r) for r in chunk]); ids.append(batch.id)
        with open(H / ".submitted.jsonl", "a", encoding="utf-8") as f:
            for r in chunk: f.write(json.dumps({"id": r["id"][:64], "batch": batch.id}) + "\n")
        print(f"batch {batch.id}: {len(chunk)} requests", file=sys.stderr)
    with open(BATCH_ID_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(ids) + "\n")


def collect():
    import anthropic
    client = anthropic.Anthropic()
    bids = [b for b in BATCH_ID_FILE.read_text().split() if b]
    coded = json.load(open(H / ".coded.json", encoding="utf-8")) if (H / ".coded.json").exists() else {}
    def get(bid):  # 핫스팟 끊김 등 연결 오류는 포기하지 않고 다시 시도
        while True:
            try: return client.messages.batches.retrieve(bid)
            except anthropic.APIConnectionError as e: print(f"connection error, retry in 60s: {e}", file=sys.stderr); time.sleep(60)
    for bid in bids:
        b = get(bid)
        while b.processing_status != "ended":
            print(f"{bid} {b.processing_status}: {b.request_counts}", file=sys.stderr, flush=True); time.sleep(60); b = get(bid)
        for res in client.messages.batches.results(bid):
            if res.result.type != "succeeded": continue
            msg = res.result.message
            if msg.stop_reason == "refusal": continue
            text = next((blk.text for blk in msg.content if blk.type == "text"), "")
            try: coded[res.custom_id] = json.loads(text)
            except json.JSONDecodeError: pass
        print(f"{bid}: {b.request_counts}", file=sys.stderr)
    json.dump(coded, open(H / ".coded.json", "w", encoding="utf-8"), ensure_ascii=False)
    Y = lambda v: "Y" if v else ""
    comp_type = lambda cs: "multiple" if len(cs) > 1 else {"generalized_trust": "generalized_trust", "institutional_trust": "institutional_trust", "neighbor_trust": "generalized_trust", "participation": "participation", "volunteer_donate": "participation", "political_participation": "participation"}.get(cs[0], "other") if cs else ""
    out, n = {}, 0
    for r in load():
        c = coded.get(r["id"][:64])
        if not c or not c["is_quant"]: continue
        cs = c.get("dv_components") or []
        link = ("https://doi.org/" + r["doi"]) if r.get("doi") else (r.get("url") or (f"https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId={r['id']}" if r["_src"] == "kci" else ""))
        out[r["id"]] = {"id": r["id"], "src": r["_src"], "authors": r.get("authors", ""), "year": r.get("year", ""), "title": r.get("title", ""), "journal": r.get("venue") or r.get("journal", ""), "link": link,
                        "country": c.get("country", ""), "data": c.get("data", ""), "unit": c.get("unit", ""), "dv_type": comp_type(cs), "dv_measure": c.get("dv_measure", ""), "dv_components": "|".join(cs), "measure_line": c.get("measure_line", ""),
                        "sc_dv": Y(c.get("sc_dv")), "iv_institution": Y(c.get("iv_institution")), "iv_individual": Y(c.get("iv_individual")), "iv_region": Y(c.get("iv_region")), "iv_network": Y(c.get("iv_network")),
                        "mediator": Y(c.get("mediator")), "moderator": Y(c.get("moderator")), "design": c.get("design", ""), "result_direction": c.get("result_direction", ""), "lineage": "", "verified": "FALSE", "coder": "haiku-5.5",
                        "notes": c.get("notes", ""), "seeds": r.get("seeds", ""), "cited_by": r.get("cited_by") or r.get("cited", "")}; n += 1
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(out.values())
    # 합치기: 규칙 코딩 studies.csv 위에 haiku 행을 덮는다(id 기준). 규칙 lineage는 유지
    if MERGED.exists():
        base = {r["id"]: r for r in csv.DictReader(open(MERGED, encoding="utf-8-sig"))}
        for k, v in out.items():
            if k in base: v["lineage"] = base[k].get("lineage", "")
            base[k] = v
        with open(MERGED, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(base.values())
    print(f"{n} haiku-coded quant rows → {OUT.name}; merged into {MERGED.name} ({len(coded)} returned)", file=sys.stderr)


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8"); sys.stdout.reconfigure(encoding="utf-8")
    cmd, *args = sys.argv[1:]
    {"dry": dry, "submit": submit, "collect": collect}[cmd](*args)
