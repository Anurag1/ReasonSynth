"""Paired evaluation and JSON summary."""
from collections import defaultdict
from .data import build_cases
from .representations import build_view
from .solver import predict
ARMS=("text","graph","structured_text","graph_ablation")

def evaluate():
    cases=build_cases(); rows=[]; counts=defaultdict(lambda:{"correct":0,"total":0})
    for case in cases:
        for arm in ARMS:
            view=build_view(case,arm); result=predict(case,arm); correct=result["prediction"]==case.gold
            counts[arm]["total"]+=1; counts[arm]["correct"]+=int(correct)
            rows.append({"case_id":case.case_id,"category":case.category,"arm":arm,"gold":case.gold,"prediction":result["prediction"],"correct":correct,"explanation":result["explanation"],"evidence_count":len(case.claims),"view":view})
    summary={arm:{"correct":v["correct"],"total":v["total"],"accuracy":round(v["correct"]/v["total"],4),"interpretation":"synthetic software smoke-test only"} for arm,v in counts.items()}
    return {"benchmark":"UNSEEN-Smoke-12","status":"illustrative_not_scientific","case_count":len(cases),"arm_count":len(ARMS),"summary":summary,"paired_graph_minus_text_accuracy":round(summary["graph"]["accuracy"]-summary["text"]["accuracy"],4),"cases":rows,"limitations":["Synthetic cases only; no independently annotated benchmark.","Deterministic heuristic solver, not a foundation model.","Small sample; no confirmatory inference.","Results validate pipeline, not graph superiority."]}
