from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Evaluation:
    problem: int
    tension: int
    hypothesis: int
    framework: int
    practicality: int
    experiment: int

    @property
    def total(self) -> int:
        return self.problem + self.tension + self.hypothesis + self.framework + self.practicality + self.experiment

    def as_dict(self) -> Dict[str, int]:
        return {
            "problem": self.problem,
            "tension": self.tension,
            "hypothesis": self.hypothesis,
            "framework": self.framework,
            "practicality": self.practicality,
            "experiment": self.experiment,
            "total": self.total,
        }


def score_response(response: Dict[str, str]) -> Evaluation:
    """Deterministic structural score for a CIB-01 response.

    This is a baseline quality gate, not a claim of semantic truth.
    A production evaluator should add human/LLM rubric review and evidence checks.
    """
    values = {k: (response.get(k) or "").strip() for k in (
        "problem", "tension", "hypothesis", "framework", "practicality", "experiment"
    )}

    def present(key: str, minimum: int) -> bool:
        return len(values[key]) >= minimum

    return Evaluation(
        problem=20 if present("problem", 25) else 0,
        tension=15 if present("tension", 30) else 0,
        hypothesis=15 if present("hypothesis", 30) else 0,
        framework=20 if present("framework", 12) else 0,
        practicality=15 if present("practicality", 25) else 0,
        experiment=15 if present("experiment", 35) else 0,
    )


def evaluate_case(case: Dict) -> Dict[str, object]:
    expected = case["expected"]
    evaluation = score_response(expected)
    return {"id": case["id"], "score": evaluation.as_dict(), "status": "PASS" if evaluation.total >= 85 else "REVIEW"}
