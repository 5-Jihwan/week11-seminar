# -*- coding: utf-8 -*-
"""catalog.json에 ① 차원(dim: cognitive/structural/both, Uphoff) ② 원인 축(src: institution/society/individual/context, Hooghe & Stolle 2003 + 개인 자원)
③ 인구 특성 문항(성별·연령·학력·소득·경제활동·거주지 유형, 조사마다 6개)을 더한다. 한 번만 실행(멱등). 실행: python model/patch_catalog.py"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog.json")
c = json.load(open(P, encoding="utf-8"))
DIM = {"trust_general": "cognitive", "trust_social": "cognitive", "trust_neighbor": "cognitive", "trust_institution": "cognitive", "participation": "structural",
       "volunteer_donate": "structural", "political_participation": "structural", "network_reciprocity": "both"}
SRC = {"welfare_selective": "institution", "welfare_universal": "institution", "public_service_experience": "institution", "institution_participation": "institution",
       "region": "context", "fairness": "institution"}
DEMO = [("demo_gender", "성별", "성별", "남/여"), ("demo_age", "연령", "만 나이", "연속"), ("demo_edu", "학력", "최종 학력", "범주(무학~대학원)"),
        ("demo_income", "소득", "가구 월평균 소득", "연속 또는 구간"), ("demo_employ", "경제활동", "현재 경제활동 상태", "범주(취업/실업/비경활)"), ("demo_area", "거주지 유형", "거주 지역 유형(동/읍·면)", "2범주")]
for k in c["concepts"]:
    k["dim"] = DIM.get(k["id"], ""); k["src"] = SRC.get(k["id"], "")
have = {k["id"] for k in c["concepts"]}
for cid, label, _, _ in DEMO:
    if cid not in have:
        c["concepts"].append({"id": cid, "label": label, "role": "demo", "lineage": "", "dim": "", "src": "individual", "paper_measure": "Mettler·K&R 통제변수. Bourdieu·Lin에서는 개인 자원(원인)"})
if not any(i["concept"] == "demo_gender" for i in c["items"]):
    for s, sv in c["surveys"].items():
        if not any(i["survey"] == s for i in c["items"]):
            continue
        for cid, _, q, sc in DEMO:
            c["items"].append({"concept": cid, "survey": s, "wave": sv.get("best_wave", ""), "var": "", "question": q, "scale": sc, "unit": sv.get("unit", "개인"), "note": "기본 인구 문항(변수명은 조사표 확인)"})
json.dump(c, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("concepts", len(c["concepts"]), "items", len(c["items"]))
