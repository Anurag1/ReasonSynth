#!/usr/bin/env python3
"""Summarize blinded paired prompt-evaluation scores using only the standard library."""
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

DIMENSIONS = ("accuracy", "reasoning", "testability", "calibration")
CONDITIONS = ("standard", "russell")


def load_scores(path):
    rows = []
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"case_id", "model", "run", "condition", *DIMENSIONS}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        for line, row in enumerate(reader, start=2):
            if row["condition"] not in CONDITIONS:
                raise ValueError(f"Line {line}: condition must be one of {CONDITIONS}")
            try:
                scores = {d: int(row[d]) for d in DIMENSIONS}
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Line {line}: scores must be integers 0, 1, or 2") from exc
            if any(v not in (0, 1, 2) for v in scores.values()):
                raise ValueError(f"Line {line}: scores must be 0, 1, or 2")
            rows.append({**row, **scores, "total": sum(scores.values())})
    return rows


def summarize(rows):
    grouped = defaultdict(dict)
    totals = defaultdict(list)
    dimensions = defaultdict(lambda: defaultdict(list))
    for row in rows:
        key = (row["case_id"], row["model"], row["run"])
        condition = row["condition"]
        if condition in grouped[key]:
            raise ValueError(f"Duplicate row for {key} condition={condition}")
        grouped[key][condition] = row
        totals[condition].append(row["total"])
        for d in DIMENSIONS:
            dimensions[condition][d].append(row[d])

    paired = []
    incomplete = 0
    for key, pair in grouped.items():
        if all(c in pair for c in CONDITIONS):
            paired.append(pair["russell"]["total"] - pair["standard"]["total"])
        else:
            incomplete += 1

    report = []
    for condition in CONDITIONS:
        vals = totals[condition]
        report.append(f"{condition}: n={len(vals)}")
        if vals:
            report.append(f"  total mean (0-8): {statistics.mean(vals):.3f}")
            for d in DIMENSIONS:
                report.append(f"  {d} mean (0-2): {statistics.mean(dimensions[condition][d]):.3f}")
    report.append(f"paired comparisons: {len(paired)}")
    report.append(f"incomplete case/model/run pairs: {incomplete}")
    if paired:
        report.append(f"paired mean difference (russell - standard; -8 to +8): {statistics.mean(paired):.3f}")
        report.append(f"paired wins/ties/losses: {sum(x > 0 for x in paired)}/{sum(x == 0 for x in paired)}/{sum(x < 0 for x in paired)}")
    report.append("Interpretation: descriptive pilot statistics only; no significance or general-superiority claim is implied.")
    return "\n".join(report)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python score.py scores.csv")
    print(summarize(load_scores(sys.argv[1])))


if __name__ == "__main__":
    main()
