"""Synthetic cases for smoke-testing the UNSEEN pipeline."""
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class Claim:
    claim_id: str
    source_id: str
    subject: str
    predicate: str
    value: str
    conditions: dict[str, str]
    reliability: str = "medium"
    text: str = ""
    def to_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class Case:
    case_id: str
    category: str
    question: str
    claims: tuple[Claim, ...]
    gold: str
    rationale: str
    def to_dict(self):
        return {"case_id":self.case_id,"category":self.category,"question":self.question,
                "claims":[c.to_dict() for c in self.claims],"gold":self.gold,"rationale":self.rationale}

def c(cid,src,subj,pred,value,conditions,reliability="medium",text=""):
    return Claim(cid,src,subj,pred,value,conditions,reliability,text or f"{subj} {pred} {value} under {conditions}.")

def build_cases() -> list[Case]:
    return [
      Case("C01","direct_conflict","Which value is supported for Device A in test T?",(c("c1","s1","Device A","accuracy","91%",{"test":"T","date":"2026-01"},"high"),c("c2","s2","Device A","accuracy","78%",{"test":"T","date":"2026-01"},"high")),"unresolved","Same conditions, incompatible values, no adjudicating evidence."),
      Case("C02","direct_conflict","Is the exact lab measurement established?",(c("c1","s1","Sample","measurement","5",{"unit":"mg"},"high"),c("c2","s2","Sample","measurement","7",{"unit":"mg"},"high")),"unresolved","Two equally specified sources conflict."),
      Case("C03","context_mismatch","Did System X perform worse in the second report?",(c("c1","s1","System X","accuracy","91%",{"dataset":"D1","date":"Jan"},"high"),c("c2","s2","System X","accuracy","78%",{"dataset":"D2","date":"Mar"},"high")),"insufficient","Datasets differ; decline is not established."),
      Case("C04","context_mismatch","Do the two reports contradict each other?",(c("c1","s1","Treatment Q","success_rate","80%",{"population":"adults"},"high"),c("c2","s2","Treatment Q","success_rate","60%",{"population":"children"},"high")),"no_conflict","Different populations need not conflict."),
      Case("C05","time_change","What is the current policy status?",(c("c1","s1","Policy P","status","active",{"date":"2024-01"},"high"),c("c2","s2","Policy P","status","retired",{"date":"2026-01"},"high")),"conditional","Newer status may supersede older status for current queries."),
      Case("C06","time_change","Was Policy P active in 2024?",(c("c1","s1","Policy P","status","active",{"date":"2024-01"},"high"),c("c2","s2","Policy P","status","retired",{"date":"2026-01"},"high")),"supported","The dated source supports the 2024 status."),
      Case("C07","missing_evidence","Did the intervention improve outcomes?",(c("c1","s1","Intervention B","outcome","not_reported",{"study":"S1"},"medium"),),"insufficient","No comparative result is supplied."),
      Case("C08","missing_evidence","Can we conclude Device Z is safe?",(c("c1","s1","Device Z","safety","not_assessed",{"study":"S2"},"medium"),),"insufficient","No assessment does not establish safety or harm."),
      Case("C09","multi_hop","Is the proposed causal conclusion established?",(c("c1","s1","A","associated_with","B",{"study":"S1"},"medium"),c("c2","s2","B","associated_with","C",{"study":"S2"},"medium")),"insufficient","Associations do not establish transitive causation."),
      Case("C10","multi_hop","Is Claim K fully established by the source chain?",(c("c1","s1","Source S","supports","Claim K",{"span":"p1"},"high"),c("c2","s2","Source S","withdrawn","true",{"date":"2026-02"},"high")),"conditional","Source status and independent evidence require review."),
      Case("C11","source_reliability","Should conflict be resolved solely by source prestige?",(c("c1","s1","Compound R","effect","positive",{"design":"small_uncontrolled"},"low"),c("c2","s2","Compound R","effect","null",{"design":"randomized_controlled"},"high")),"conditional","Design quality matters but details are necessary."),
      Case("C12","source_reliability","Is a finding definitely false because one source is low reliability?",(c("c1","s1","Finding J","result","positive",{"replicated":"unknown"},"low"),c("c2","s2","Finding J","result","unknown",{"replicated":"unknown"},"high")),"insufficient","Low reliability alone does not prove falsity.")
    ]
