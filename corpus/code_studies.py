"""선행연구 후보(candidates_quant.csv)를 PLAN §5-2 스키마로 코딩한다. Claude 배치 API(50% 비용).

사용:
  python -I corpus/code_studies.py dry      corpus/candidates_quant.csv            # 요청 1건 미리보기, API 없음
  python corpus/code_studies.py submit   corpus/candidates_quant.csv            # 배치 제출 → corpus/.batch_id
  python corpus/code_studies.py collect  corpus/candidates_quant.csv corpus/studies.csv   # 결과 수거 → studies.csv
키는 환경변수 ANTHROPIC_API_KEY (레포에 넣지 않는다). anthropic SDK는 사용자 site-packages에 있어 submit/collect는 -I 없이 실행.
"""
import csv, json, sys, time
from pathlib import Path

MODEL = "claude-opus-5-5"
BATCH_ID_FILE = Path(__file__).with_name(".batch_id")

ENUM = {
    "unit": ["individual", "region", "country", "mixed", ""],
    "dv_type": ["generalized_trust", "institutional_trust", "participation", "multiple", "other", ""],
    "design": ["cross_section", "panel", "quasi_experiment", "experiment", "other", ""],
    "result_direction": ["positive", "negative", "mixed", "null", ""],
    "lineage": ["krishna", "freitag", "lw", "mettler", "kr", "none"],
}
SCHEMA = {
    "type": "object",
    "properties": {
        "is_quant": {"type": "boolean", "description": "경험적 자료로 통계 분석을 한 연구이면 true. 이론·리뷰·서평이면 false"},
        "country": {"type": "string", "description": "자료의 국가. 다국가면 'multi'. 모르면 빈 문자열"},
        "data": {"type": "string", "description": "자료 이름(WVS, ESS, 자체 설문 등). 초록에 없으면 빈 문자열"},
        "unit": {"type": "string", "enum": ENUM["unit"], "description": "분석 단위"},
        "dv_type": {"type": "string", "enum": ENUM["dv_type"], "description": "사회자본 종속변수의 종류. 사회자본이 독립변수이면 other"},
        "dv_measure": {"type": "string", "description": "종속변수 측정 방식 한 구절(예: 일반신뢰 단일 문항 0-10)"},
        "iv_institution": {"type": "string", "description": "제도·정책 독립변수. 없으면 빈 문자열"},
        "iv_individual": {"type": "string", "description": "개인 특성 독립변수. 없으면 빈 문자열"},
        "iv_region": {"type": "string", "description": "지역·국가 특성 독립변수. 없으면 빈 문자열"},
        "iv_network": {"type": "string", "description": "연결망·결사체 독립변수. 없으면 빈 문자열"},
        "mediator": {"type": "string", "description": "매개변수. 없으면 빈 문자열"},
        "moderator": {"type": "string", "description": "조절변수. 없으면 빈 문자열"},
        "design": {"type": "string", "enum": ENUM["design"]},
        "result_direction": {"type": "string", "enum": ENUM["result_direction"], "description": "제도·정책 변수가 사회자본과 맺는 관계의 방향"},
        "lineage": {"type": "string", "enum": ENUM["lineage"], "description": "가장 가까운 지정문헌. krishna=공동체 내부 노력, freitag=정치제도→결사체, lw=지방정부 제도설계, mettler=정책환류→참여, kr=복지제도 설계→신뢰. 해당 없으면 none"},
        "notes": {"type": "string", "description": "한국어 한 문장. 인과 표현 금지('영향을 미친다' 대신 '관련이 있다')"},
    },
    "required": list(["is_quant", "country", "data", "unit", "dv_type", "dv_measure", "iv_institution", "iv_individual",
                      "iv_region", "iv_network", "mediator", "moderator", "design", "result_direction", "lineage", "notes"]),
    "additionalProperties": False,
}
SYSTEM = """당신은 사회자본 연구를 코딩하는 연구 보조원이다. 제목과 초록만 보고 아래 칸을 채운다.
규칙: 초록에 없는 내용은 빈 문자열로 둔다. 추측하지 않는다. 논문을 지어내지 않는다.
사회자본(신뢰·참여·연결망)이 종속변수인지 먼저 판단한다. 독립변수이면 dv_type=other.
notes는 한국어 한 문장, 인과 표현 금지."""


def build_request(r):
    return {
        "custom_id": r["id"],
        "params": {
            "model": MODEL,
            "max_tokens": 2000,
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
            "system": SYSTEM,
            "messages": [{"role": "user", "content": f"제목: {r['title']}\n연도: {r['year']}\n학술지: {r['venue']}\n초록: {r['abstract']}"}],
        },
    }


def load(src):
    return list(csv.DictReader(open(src, encoding="utf-8-sig")))


def dry(src):
    print(json.dumps(build_request(load(src)[0]), ensure_ascii=False, indent=1)[:3000])


def submit(src):
    import anthropic
    client = anthropic.Anthropic()
    rows = load(src)
    batch = client.messages.batches.create(requests=[build_request(r) for r in rows])
    BATCH_ID_FILE.write_text(batch.id)
    print(f"batch {batch.id} submitted, {len(rows)} requests → {BATCH_ID_FILE}", file=sys.stderr)


def collect(src, dst):
    import anthropic
    client = anthropic.Anthropic()
    bid = BATCH_ID_FILE.read_text().strip()
    while (b := client.messages.batches.retrieve(bid)).processing_status != "ended":
        print(f"{b.processing_status}: {b.request_counts}", file=sys.stderr); time.sleep(60)
    coded = {}
    for res in client.messages.batches.results(bid):
        if res.result.type == "succeeded":
            msg = res.result.message
            if msg.stop_reason == "refusal":
                continue
            text = next((blk.text for blk in msg.content if blk.type == "text"), "")
            try:
                coded[res.custom_id] = json.loads(text)
            except json.JSONDecodeError:
                pass
        else:
            print(f"{res.custom_id}: {res.result.type}", file=sys.stderr)
    cols = "id,authors,year,title,journal,link,country,data,unit,dv_type,dv_measure,iv_institution,iv_individual,iv_region,iv_network,mediator,moderator,design,result_direction,lineage,verified,notes,seeds,cited_by".split(",")
    n = 0
    with open(dst, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in load(src):
            c = coded.get(r["id"])
            if not c or not c["is_quant"]:
                continue
            w.writerow({**{k: c.get(k, "") for k in cols}, "id": r["id"], "authors": r["authors"], "year": r["year"], "title": r["title"],
                        "journal": r["venue"], "link": ("https://doi.org/" + r["doi"]) if r["doi"] else "", "verified": "FALSE",
                        "seeds": r["seeds"], "cited_by": r["cited_by"]})
            n += 1
    print(f"{n} coded rows → {dst} ({len(coded)} returned, {b.request_counts.errored} errored)", file=sys.stderr)


if __name__ == "__main__":
    sys.stderr.reconfigure(encoding="utf-8"); sys.stdout.reconfigure(encoding="utf-8")
    cmd, *args = sys.argv[1:]
    {"dry": dry, "submit": submit, "collect": collect}[cmd](*args)
