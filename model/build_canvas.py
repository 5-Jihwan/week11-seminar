# -*- coding: utf-8 -*-
"""2부 캔버스 데모 v3(Galpi 방식 + 원래 컨셉): 자료(조사) 먼저 고르기 → 그 조사의 문항 카드를 끌어다 놓기(빈 곳=새 변수, 변수 위=묶기) → 이름·역할은 학생이 → 탭으로 잇기
→ 3초 멈추면 검증 패널(오류·경고·내 정의·계보·닮은 선행연구·리뷰·가설). 화면 틀은 canvas_v3.html.tpl. catalog·규칙은 build_index.py와 같은 것을 심는다(file://로 열림, localStorage 저장).
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

CAT, PAPERS = json.dumps(bi.CAT, ensure_ascii=False), json.dumps(bi.PAPERS, ensure_ascii=False)
HTML = open(os.path.join(HERE, "canvas_v4.html.tpl"), encoding="utf-8").read()  # v4: Galpi 화면 구조(헤더·역할색 노드·존·조절 서랍·검증 배지) + v3 흐름(자료 먼저 → 끌어 묶기 → 정의 → 비교)
out = (HTML.replace("__CAT__", CAT).replace("__REV__", json.dumps({"base": bi.REVIEWS, "cond": bi.COND}, ensure_ascii=False))
       .replace("__PAPERS__", PAPERS).replace("__STUDIES__", json.dumps(STUDIES, ensure_ascii=False)))
open(os.path.join(HERE, "canvas.html"), "w", encoding="utf-8").write(out)
print("canvas.html", len(out) // 1024, "KB · 선행연구", len(STUDIES), "편(구성 요소 있는 것)")
# 관리자 대시보드(제출 목록·자료 빈도·정의 구성·계보·spotlight). 데모는 같은 브라우저 localStorage 'w11_model'을 storage 이벤트로 읽는다.
dash = open(os.path.join(HERE, "dashboard.html.tpl"), encoding="utf-8").read().replace("__CAT__", CAT).replace("__PAPERS__", PAPERS)
open(os.path.join(HERE, "dashboard.html"), "w", encoding="utf-8").write(dash)
print("dashboard.html", len(dash) // 1024, "KB")
