from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cib01 import evaluate_case  # noqa: E402


def main() -> int:
    data_path = ROOT / "data" / "cases.json"
    cases = json.loads(data_path.read_text(encoding="utf-8"))
    results = [evaluate_case(case) for case in cases]

    print("CIB-01 Creator Intelligence Benchmark")
    print("=" * 42)
    for result in results:
        score = result["score"]
        print(f"{result['id']}: {score['total']}/100 [{result['status']}]")
        print(f"  breakdown: {score}")

    mean_score = sum(r["score"]["total"] for r in results) / len(results)
    passed = sum(r["status"] == "PASS" for r in results)
    print("-" * 42)
    print(f"mean: {mean_score:.1f}/100")
    print(f"passed: {passed}/{len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
