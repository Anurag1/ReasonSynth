import csv
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import load_scores, summarize


class ScoreTests(unittest.TestCase):
    def write_csv(self, rows):
        temp = tempfile.NamedTemporaryFile(mode="w", newline="", encoding="utf-8", suffix=".csv", delete=False)
        with temp:
            writer = csv.DictWriter(temp, fieldnames=["case_id", "model", "run", "condition", "accuracy", "reasoning", "testability", "calibration"])
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))
        return temp.name

    def test_paired_difference(self):
        path = self.write_csv([
            {"case_id":"a","model":"m","run":"1","condition":"standard","accuracy":1,"reasoning":1,"testability":1,"calibration":1},
            {"case_id":"a","model":"m","run":"1","condition":"russell","accuracy":2,"reasoning":1,"testability":2,"calibration":1},
        ])
        result = summarize(load_scores(path))
        self.assertIn("paired comparisons: 1", result)
        self.assertIn("paired mean difference (russell - standard; -8 to +8): 2.000", result)

    def test_reject_out_of_range_score(self):
        path = self.write_csv([
            {"case_id":"a","model":"m","run":"1","condition":"standard","accuracy":3,"reasoning":1,"testability":1,"calibration":1},
        ])
        with self.assertRaises(ValueError):
            load_scores(path)

    def test_duplicate_condition_rejected(self):
        path = self.write_csv([
            {"case_id":"a","model":"m","run":"1","condition":"standard","accuracy":1,"reasoning":1,"testability":1,"calibration":1},
            {"case_id":"a","model":"m","run":"1","condition":"standard","accuracy":1,"reasoning":1,"testability":1,"calibration":1},
        ])
        with self.assertRaises(ValueError):
            summarize(load_scores(path))


if __name__ == "__main__":
    unittest.main()
