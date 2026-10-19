import tempfile
import unittest
from pathlib import Path

from autoresearch_audit import audit_results, render_text

HEADER = "commit\tval_bpb\tmemory_gb\tstatus\tdescription\n"


class AuditResultsTests(unittest.TestCase):
    def write_tsv(self, body: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".tsv", delete=False)
        tmp.write(body)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink, missing_ok=True)
        return Path(tmp.name)

    def test_valid_rows_and_best_kept_run(self):
        path = self.write_tsv(HEADER +
            "abc1234\t1.25\t8.0\tkeep\tbaseline\n" +
            "def5678\t1.10\t8.2\tkeep\tlower validation bpb\n" +
            "ghi9012\t1.40\t8.0\tdiscard\tworse\n")
        report = audit_results(path)
        self.assertEqual(report["rows"], 3)
        self.assertEqual(report["invalid_rows"], 0)
        self.assertEqual(report["best_kept_run"]["commit"], "def5678")
        self.assertEqual(report["status_counts"]["discard"], 1)

    def test_blank_lines_are_ignored(self):
        path = self.write_tsv(HEADER + "\nabc1234\t1.25\t8.0\tkeep\tbaseline\n\n")
        self.assertEqual(audit_results(path)["rows"], 1)

    def test_missing_columns_raise(self):
        path = self.write_tsv("commit\tstatus\nabc\tkeep\n")
        with self.assertRaisesRegex(ValueError, "missing required column"):
            audit_results(path)

    def test_invalid_status_reported(self):
        path = self.write_tsv(HEADER + "abc\t1.0\t2.0\tmaybe\tbad status\n")
        report = audit_results(path)
        self.assertEqual(report["invalid_rows"], 1)
        self.assertIn("status must be one of", report["errors"][0]["errors"][0])

    def test_non_finite_metric_rejected(self):
        path = self.write_tsv(HEADER + "abc\tNaN\t2.0\tkeep\tbad metric\n")
        report = audit_results(path)
        self.assertEqual(report["invalid_rows"], 1)
        self.assertTrue(any("finite non-negative" in e for e in report["errors"][0]["errors"]))

    def test_duplicate_commit_rejected(self):
        path = self.write_tsv(HEADER + "abc\t1.0\t2.0\tkeep\tone\nabc\t0.9\t2.0\tkeep\ttwo\n")
        report = audit_results(path)
        self.assertTrue(any("duplicate commit" in e for e in report["errors"][0]["errors"]))

    def test_crash_metrics_follow_convention(self):
        path = self.write_tsv(HEADER + "abc\t0.0\t0.0\tcrash\tOOM\n")
        self.assertEqual(audit_results(path)["invalid_rows"], 0)
        path2 = self.write_tsv(HEADER + "abc\t1.2\t8.0\tcrash\tOOM\n")
        self.assertEqual(audit_results(path2)["invalid_rows"], 1)

    def test_text_summary_without_kept_rows(self):
        path = self.write_tsv(HEADER + "abc\t0.0\t0.0\tcrash\tOOM\n")
        summary = render_text(audit_results(path))
        self.assertIn("Best valid kept run: none", summary)


if __name__ == "__main__":
    unittest.main()
