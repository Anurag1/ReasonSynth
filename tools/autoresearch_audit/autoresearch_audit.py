#!/usr/bin/env python3
"""Validate and summarize autoresearch-style results.tsv files.

Uses only the Python standard library. It does not change experiment results,
select experiments, or make claims about model quality beyond recorded metrics.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = ("commit", "val_bpb", "memory_gb", "status", "description")
VALID_STATUSES = {"keep", "discard", "crash"}


def audit_results(path: str | Path) -> dict[str, Any]:
    """Read and audit a tab-separated autoresearch results log."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"results file not found: {source}")

    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing:
            raise ValueError("missing required column(s): " + ", ".join(missing))

        rows: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        seen_commits: dict[str, int] = {}
        status_counts: Counter[str] = Counter()

        for line_number, raw in enumerate(reader, start=2):
            if not raw or not any((value or "").strip() for value in raw.values()):
                continue

            row_errors: list[str] = []
            commit = (raw.get("commit") or "").strip()
            status = (raw.get("status") or "").strip().lower()
            description = (raw.get("description") or "").strip()

            if not commit:
                row_errors.append("commit is empty")
            elif commit in seen_commits:
                row_errors.append(f"duplicate commit (first seen on line {seen_commits[commit]})")
            else:
                seen_commits[commit] = line_number

            if status not in VALID_STATUSES:
                row_errors.append("status must be one of: keep, discard, crash")
            else:
                status_counts[status] += 1

            metrics: dict[str, float | None] = {}
            for field in ("val_bpb", "memory_gb"):
                raw_value = (raw.get(field) or "").strip()
                try:
                    number = float(raw_value)
                    if not math.isfinite(number):
                        raise ValueError
                    if number < 0:
                        row_errors.append(f"{field} cannot be negative")
                        metrics[field] = number
                    else:
                        metrics[field] = number
                except ValueError:
                    row_errors.append(f"{field} must be a finite non-negative number")
                    metrics[field] = None

            if status == "crash":
                if metrics["val_bpb"] not in (0.0, None):
                    row_errors.append("crash rows should use val_bpb=0.0 per the results.tsv convention")
                if metrics["memory_gb"] not in (0.0, None):
                    row_errors.append("crash rows should use memory_gb=0.0 per the results.tsv convention")

            item = {
                "line": line_number,
                "commit": commit,
                "val_bpb": metrics["val_bpb"],
                "memory_gb": metrics["memory_gb"],
                "status": status,
                "description": description,
                "errors": row_errors,
            }
            rows.append(item)
            if row_errors:
                errors.append({"line": line_number, "commit": commit, "errors": row_errors})

    kept = [r for r in rows if r["status"] == "keep" and not r["errors"] and r["val_bpb"] is not None]
    best = min(kept, key=lambda r: r["val_bpb"], default=None)
    valid_rows = sum(not row["errors"] for row in rows)
    return {
        "file": str(source),
        "rows": len(rows),
        "valid_rows": valid_rows,
        "invalid_rows": len(errors),
        "status_counts": {status: status_counts.get(status, 0) for status in ("keep", "discard", "crash")},
        "best_kept_run": None if best is None else {
            "commit": best["commit"], "val_bpb": best["val_bpb"],
            "memory_gb": best["memory_gb"], "description": best["description"],
        },
        "errors": errors,
    }


def render_text(report: dict[str, Any]) -> str:
    """Render a compact, human-readable audit summary."""
    counts = report["status_counts"]
    lines = [
        f"File: {report['file']}",
        f"Rows: {report['rows']} total; {report['valid_rows']} valid; {report['invalid_rows']} invalid",
        f"Statuses: keep={counts['keep']}, discard={counts['discard']}, crash={counts['crash']}",
    ]
    best = report["best_kept_run"]
    if best:
        lines.append(
            f"Best valid kept run: {best['commit']} (val_bpb={best['val_bpb']:.6f}, "
            f"memory_gb={best['memory_gb']:.1f}) — {best['description']}"
        )
    else:
        lines.append("Best valid kept run: none")
    for entry in report["errors"]:
        lines.append(f"Line {entry['line']} ({entry['commit'] or '<empty commit>'}): " + "; ".join(entry["errors"]))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", help="path to results.tsv")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        report = audit_results(args.results)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"audit error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return 1 if report["invalid_rows"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
