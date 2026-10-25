"""Text and graph representations from canonical claims."""
from .data import Case

def text_view(case: Case):
    return {"mode":"text","question":case.question,"evidence":[f"[{c.source_id}/{c.claim_id}] {c.text} Conditions={c.conditions}; reliability={c.reliability}" for c in case.claims]}

def structured_text_view(case: Case):
    return {"mode":"structured_text","question":case.question,"claims":[c.to_dict() for c in case.claims]}

def graph_view(case: Case, ablate: bool=False):
    nodes,edges=[],[]
    for claim in case.claims:
        nodes.append({"id":claim.claim_id,"type":"claim","source_id":claim.source_id,"subject":claim.subject,"predicate":claim.predicate,"value":claim.value,"conditions":claim.conditions,"reliability":claim.reliability})
        nodes.append({"id":claim.source_id,"type":"source"})
        edges.append({"from":claim.source_id,"to":claim.claim_id,"type":"SUPPORTS"})
    if not ablate:
        for i,a in enumerate(case.claims):
            for b in case.claims[i+1:]:
                same=(a.subject,a.predicate,a.conditions)==(b.subject,b.predicate,b.conditions)
                if same and a.value!=b.value: edges.append({"from":a.claim_id,"to":b.claim_id,"type":"CONTRADICTS"})
                elif a.subject==b.subject and a.predicate==b.predicate and a.value!=b.value: edges.append({"from":a.claim_id,"to":b.claim_id,"type":"QUALIFIES"})
    return {"mode":"graph_ablation" if ablate else "graph","question":case.question,"nodes":nodes,"edges":edges}

def build_view(case: Case, arm: str):
    if arm=="text": return text_view(case)
    if arm=="graph": return graph_view(case)
    if arm=="structured_text": return structured_text_view(case)
    if arm=="graph_ablation": return graph_view(case,True)
    raise ValueError(f"Unknown arm: {arm}")
