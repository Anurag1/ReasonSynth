"""Transparent heuristic solver used for pipeline smoke tests, not research claims."""
LABELS={"supported","refuted","unresolved","insufficient","no_conflict","conditional"}

def predict(case, arm):
    claims=case.claims
    if arm not in {"text","graph","structured_text","graph_ablation"}:
        raise ValueError(f"Unknown arm: {arm}")
    if not claims:
        label, explanation="insufficient","No evidence supplied."
    elif len(claims)==1 and claims[0].value in {"not_reported","not_assessed"}:
        label, explanation="insufficient","The evidence does not establish an outcome."
    elif len(claims)>=2:
        a,b=claims[0],claims[1]
        same_conditions=a.conditions==b.conditions
        same_key=(a.subject,a.predicate)==(b.subject,b.predicate)
        different=a.value!=b.value
        if a.predicate=="status" and a.subject==b.subject and a.conditions.get("date")!=b.conditions.get("date"):
            label="supported" if "2024" in case.question and any("2024" in x.conditions.get("date","") for x in claims[:2]) else "conditional"
            explanation="Claims are time-indexed; the query determines which time is relevant."
        elif same_key and different and same_conditions:
            label,explanation="unresolved","Equally specified claims conflict; no adjudicating evidence is supplied."
        elif same_key and different and not same_conditions:
            if "dataset" in a.conditions or "population" in a.conditions:
                label="insufficient" if "worse" in case.question.lower() else "no_conflict"
                explanation="Conditions differ, so a trend or direct contradiction is not established."
            elif a.reliability!=b.reliability:
                label,explanation="conditional","Source reliability differs but does not alone settle the claim."
            else:
                label,explanation="conditional","Conditions differ; the relationship needs qualification."
        elif a.predicate=="associated_with" or any(x.value=="unknown" for x in claims):
            label,explanation="insufficient","The evidence does not establish the stronger conclusion."
        elif any(x.value=="true" and x.predicate=="withdrawn" for x in claims):
            label,explanation="conditional","Source status and independent evidence require review."
        else:
            label,explanation="conditional","Evidence is related but does not establish an unconditional conclusion."
    else:
        label,explanation="insufficient","Available evidence is insufficient."
    return {"arm":arm,"prediction":label if label in LABELS else "insufficient",
            "explanation":explanation,"source_ids":list(dict.fromkeys(c.source_id for c in claims)),
            "confidence":0.6 if label in {"conditional","unresolved"} else 0.7}
