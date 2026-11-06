# -*- coding: utf-8 -*-
"""2부 캔버스 데모 v3(Galpi 방식 + 원래 컨셉): 자료(조사) 먼저 고르기 → 그 조사의 문항 카드를 끌어다 놓기(빈 곳=새 변수, 변수 위=묶기) → 이름·역할은 학생이 → 탭으로 잇기
→ 3초 멈추면 검증 패널(오류·경고·내 정의·계보·닮은 선행연구·리뷰·가설). 화면 틀은 canvas_v3.html.tpl. catalog·규칙은 build_index.py와 같은 것을 심는다(file://로 열림, localStorage 저장).
실행: python model/build_canvas.py → model/canvas.html"""
import csv, json, os, re, sys, importlib.util
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
# 선행연구(corpus/studies.csv, 규칙 코딩·미검수). 화면에 필요한 칸만 심는다. 수업판은 verified=TRUE만 남긴다(가드레일 2).
def _au(a):  # "홍길동(대학); 김철수(대학)" 또는 "Smith, J.; Lee, K." → 첫 저자 성 + 외
    first = re.split(r"[;,]", a)[0].strip(); first = re.sub(r"\(.*?\)", "", first).strip()
    return (first.split(" ")[-1] if re.search(r"[A-Za-z]", first) else first) + (" 외" if re.search(r"[;,]", a) else "")
STUDIES = [{"id": r["id"], "src": r.get("src", "openalex"), "au": _au(r["authors"]) if r["authors"] else "", "y": r["year"], "t": r["title"], "j": r["journal"],
            "link": r["link"], "comps": [c for c in r["dv_components"].split("|") if c], "unit": r["unit"], "data": r.get("data", ""), "kr": r.get("country", "") == "KR", "dv": r.get("sc_dv", "") == "Y",
            "inst": r["iv_institution"] == "Y", "reg": r["iv_region"] == "Y", "net": r["iv_network"] == "Y", "med": r["mediator"] == "Y", "lin": r["lineage"], "line": r["measure_line"], "design": r["design"], "ok": r["verified"] == "TRUE"}
           for r in csv.DictReader(open(os.path.join(HERE, "..", "corpus", "studies.csv"), encoding="utf-8-sig"))]  # 346편 전부. 구성 요소가 비면 그물망 바깥 껍질에만 뜬다
_seen = set()  # 같은 논문이 두 출처(출판본·워킹페이퍼)로 들어온 것은 제목으로 한 번만
STUDIES = [s for s in STUDIES if not (s["t"].lower().strip().rstrip(".") in _seen or _seen.add(s["t"].lower().strip().rstrip(".")))]
spec = importlib.util.spec_from_file_location("bi", os.path.join(HERE, "build_index.py"))
# build_index.py는 import 시 index.html을 다시 쓴다(부작용 무해). REVIEWS·COND·PAPERS·CAT를 재사용.
bi = importlib.util.module_from_spec(spec); spec.loader.exec_module(bi)

CLASS = "--class" in sys.argv  # 수업판: verified=TRUE만 심고 DEMO=false(가드레일 2). 기본은 데모(전부, 미검수 표시)
if CLASS:
    STUDIES = [s for s in STUDIES if s["ok"]]
    assert STUDIES, "수업판인데 verified=TRUE가 0편. corpus/studies.csv의 verified 열을 먼저 채우십시오"
DEMO = "false" if CLASS else "true"
# 조사표 전체 문항(model/full_items.json, parse_*_full.py가 만든다): 기본 화면엔 안 보이고 「전체 문항」·검색에서만. 주제별 의사 개념 full_XX에 차원·원인 축을 붙인다
FULLC = {"TR": ("신뢰 (조사표)", "cognitive", ""), "NW": ("참여·관계 (조사표)", "structural", ""), "FA": ("공정성 (조사표)", "", "institution"), "IN": ("제도·서비스 경험 (조사표)", "", "institution"),
         "RG": ("지역 (조사표)", "", "context"), "DM": ("개인 특성 (조사표)", "", "individual"), "ET": ("기타 문항 (조사표)", "", "")}
CATX = json.loads(json.dumps(bi.CAT))
for k, (lab, dim, src) in FULLC.items():
    CATX["concepts"].append({"id": "full_" + k, "label": lab, "role": "full", "lineage": "", "dim": dim, "src": src, "paper_measure": "조사표 전체 문항. 1부 다섯 편에는 없음"})
fp = os.path.join(HERE, "full_items.json")
FULL = json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else {}
_norm = lambda q: re.sub(r"[\s\W_]+", "", q)[:22]
_have = {(i["survey"], _norm(i["question"])) for i in CATX["items"]}  # 요약 문항의 (조사, 문장 앞 22자)
for sv, its in FULL.items():
    for i in its:
        if (sv, _norm(i["question"])) in _have:
            continue  # 요약 문항에 이미 같은 문장이 있다 → 전체 목록에서 뺀다(완전 중복)
        CATX["items"].append({"concept": "full_" + i["theme"], "survey": sv, "wave": i["wave"], "var": i["var"], "question": i["question"], "scale": i["scale"], "unit": i["unit"], "note": "조사표 전체", "full": 1})
print("조사표 전체 문항", {k: len(v) for k, v in FULL.items()})
CAT, PAPERS = json.dumps(CATX, ensure_ascii=False), json.dumps(bi.PAPERS, ensure_ascii=False)
HTML = open(os.path.join(HERE, "canvas_v5.html.tpl"), encoding="utf-8").read()  # v5: 개념화 단계·역할 자유(문항에 역할 없음)·조절·통제·분류 틀(원인 축×종속 차원) + Galpi 화면 구조
out = (HTML.replace("__CAT__", CAT).replace("__REV__", json.dumps({"base": bi.REVIEWS, "cond": bi.COND}, ensure_ascii=False))
       .replace("__PAPERS__", PAPERS).replace("__STUDIES__", json.dumps(STUDIES, ensure_ascii=False)).replace("__DEMO__", DEMO))
open(os.path.join(HERE, "canvas.html"), "w", encoding="utf-8").write(out)
print(("수업판 " if CLASS else "데모 ") + "canvas.html", len(out) // 1024, "KB · 선행연구", len(STUDIES), "편(구성 요소 있는 것", sum(1 for s in STUDIES if s["comps"]), ")")
# 관리자 대시보드(제출 목록·자료 빈도·정의 구성·계보·spotlight). 데모는 같은 브라우저 localStorage 'w11_model'을 storage 이벤트로 읽는다.
dash = open(os.path.join(HERE, "dashboard.html.tpl"), encoding="utf-8").read().replace("__CAT__", CAT).replace("__PAPERS__", PAPERS).replace("__STUDIES__", json.dumps(STUDIES, ensure_ascii=False)).replace("__DEMO__", DEMO)
open(os.path.join(HERE, "dashboard.html"), "w", encoding="utf-8").write(dash)
print("dashboard.html", len(dash) // 1024, "KB")
