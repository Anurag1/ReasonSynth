import json
from unseen.benchmark import ARMS,evaluate
from unseen.data import build_cases
from unseen.representations import graph_view
from unseen.solver import predict

def test_dataset_shape():
    cases=build_cases(); assert len(cases)==12; assert len({c.case_id for c in cases})==12; assert all(c.gold for c in cases)

def test_graph_provenance_and_conflict_edge():
    case=build_cases()[0]; view=graph_view(case); ids={c.claim_id for c in case.claims}
    assert all(e["to"] in ids for e in view["edges"] if e["type"]=="SUPPORTS")
    assert any(e["type"]=="CONTRADICTS" for e in view["edges"])

def test_ablation_removes_contradiction_edges():
    case=build_cases()[0]; assert any(e["type"]=="CONTRADICTS" for e in graph_view(case)["edges"]); assert not any(e["type"]=="CONTRADICTS" for e in graph_view(case,True)["edges"])

def test_all_arms_return_valid_labels():
    allowed={"supported","refuted","unresolved","insufficient","no_conflict","conditional"}
    for case in build_cases():
      for arm in ARMS:
        out=predict(case,arm); assert out["prediction"] in allowed and out["source_ids"]

def test_evaluation_reproducible_and_complete():
    a=evaluate(); assert a==evaluate(); assert a["case_count"]==12 and len(a["cases"])==48; assert set(a["summary"])==set(ARMS); assert all(x["total"]==12 for x in a["summary"].values()); assert a["status"]=="illustrative_not_scientific"

def test_results_json_serializable():
    assert json.loads(json.dumps(evaluate()))["benchmark"]=="UNSEEN-Smoke-12"
