import importlib.util
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cib01 import evaluate_case, score_response  # noqa: E402


class CIB01Tests(unittest.TestCase):
    def test_complete_response_scores_100(self) -> None:
        response = {
            "problem": "A clear problem statement that is long enough to satisfy the structural rubric.",
            "tension": "A useful tension between two competing effects that the system should investigate.",
            "hypothesis": "A testable hypothesis describing an intervention and its expected effect on an outcome.",
            "framework": "ASK: Assign the task, Surface assumptions, Keep the decision.",
            "practicality": "Use the framework before accepting an AI-generated recommendation or decision.",
            "experiment": "Compare two groups with and without checkpoints and measure speed, errors, and confidence.",
        }
        self.assertEqual(score_response(response).total, 100)

    def test_incomplete_response_is_flagged(self) -> None:
        response = {"problem": "Too short"}
        self.assertLess(score_response(response).total, 85)

    def test_seed_cases_pass_structural_gate(self) -> None:
        cases = json.loads((ROOT / "data" / "cases.json").read_text(encoding="utf-8"))
        results = [evaluate_case(case) for case in cases]
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result["status"] == "PASS" for result in results))
        self.assertTrue(all(result["score"]["total"] == 100 for result in results))


if __name__ == "__main__":
    unittest.main()
