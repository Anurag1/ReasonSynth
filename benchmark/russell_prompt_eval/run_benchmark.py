#!/usr/bin/env python3
"""Run paired standard-vs-Russell prompt trials against an OpenAI-compatible API.

Requires OPENAI_API_KEY and OPENAI_MODEL. Saves raw responses to results.jsonl.
No scores are fabricated: score responses separately using the rubric.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "cases.jsonl"
PROMPTS = ROOT / "prompts"
OUT = Path(os.environ.get("RESULTS_FILE", str(ROOT / "results.jsonl")))
API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_MODEL")
REPETITIONS = int(os.environ.get("REPETITIONS", "1"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0"))
CONDITIONS = {
    "standard": (PROMPTS / "standard.md").read_text(encoding="utf-8"),
    "russell": (PROMPTS / "russell_inspired.md").read_text(encoding="utf-8"),
}


def request_completion(prompt, retries=3):
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_BASE + "/chat/completions",
        data=payload,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
            choice = data["choices"][0]
            return {
                "response": choice["message"]["content"],
                "model_returned": data.get("model"),
                "usage": data.get("usage"),
                "finish_reason": choice.get("finish_reason"),
                "provider_response_id": data.get("id"),
            }
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"API HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"API request failed: {exc}") from exc


def main():
    if not API_KEY or not MODEL:
        sys.exit("Set OPENAI_API_KEY and OPENAI_MODEL. No model calls were made.")
    if REPETITIONS < 1:
        sys.exit("REPETITIONS must be >= 1.")
    cases = [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line.strip()]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = len(cases) * len(CONDITIONS) * REPETITIONS
    completed = 0
    with OUT.open("w", encoding="utf-8") as f:
        for case in cases:
            for run in range(1, REPETITIONS + 1):
                # Alternate condition order to reduce systematic order effects.
                order = list(CONDITIONS)
                if (cases.index(case) + run) % 2:
                    order.reverse()
                for condition in order:
                    prompt = CONDITIONS[condition].replace("{problem}", case["problem"])
                    result = request_completion(prompt)
                    row = {
                        "case_id": case["case_id"],
                        "domain": case["domain"],
                        "run": run,
                        "condition": condition,
                        "model_requested": MODEL,
                        "temperature": TEMPERATURE,
                        "problem": case["problem"],
                        **result,
                    }
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                    f.flush()
                    completed += 1
                    print(f"[{completed}/{total}] {case['case_id']} run={run} condition={condition}", flush=True)
    print(f"Saved {completed} raw responses to {OUT}")
    print("No quality scores were assigned. Blind and score the responses using the case-specific rubric.")


if __name__ == "__main__":
    main()
