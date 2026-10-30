# Russell-Inspired Prompt Evaluation

A small, transparent benchmark for testing whether a structured prompt inspired by Walter Russell's philosophical themes improves problem-solving over a conventional prompt.

**Research status:** benchmark scaffold. No comparative model results are claimed by this repository yet.

## Research question

Given the same model, task, evidence, and generation settings, does a Russell-inspired prompt improve the quality of answers compared with a conventional prompt?

This evaluates a **prompting technique**, not a new LLM architecture. Architectural claims require a separate training experiment.

## Design

- Eight initial synthetic cases across anomaly detection, causal reasoning, contradiction detection, and experiment design.
- Two prompt conditions: standard and Russell-inspired.
- Blind scoring on four dimensions, each 0–2:
  - accuracy
  - reasoning quality
  - testability
  - uncertainty calibration
- Paired comparison by case, model, and repetition.
- Keep model/version, task evidence, decoding settings, and tool access identical across conditions.
- Randomize response order and hide condition labels from scorers where possible.

The included cases are a smoke-test set, not a statistically representative benchmark. Expand the dataset before drawing broad conclusions.

## Files

- `cases.jsonl`: cases and scoring criteria.
- `prompts/standard.md`: baseline instruction.
- `prompts/russell_inspired.md`: experimental instruction.
- `score.py`: summarizes a scored CSV and paired differences.
- `test_score.py`: standard-library unit tests.

## Run

Python 3.10+; no third-party packages required.

```bash
python -m unittest benchmark/russell_prompt_eval/test_score.py
```

Prepare `scores.csv` with these columns:

```csv
case_id,model,run,condition,accuracy,reasoning,testability,calibration
case_01,model-name,1,standard,2,1,1,2
case_01,model-name,1,russell,2,2,2,2
```

Each score must be an integer from 0 to 2. Each case/model/run should have both conditions for a paired comparison.

```bash
python benchmark/russell_prompt_eval/score.py scores.csv
```

The script reports condition means and paired score differences. It does not establish statistical significance or causality. For serious claims, collect enough independent cases and repetitions, report uncertainty intervals, preregister primary outcomes, and inspect failures.

## Experimental protocol

1. Freeze the cases, rubric, and primary metric before running the models.
2. Use the same model version and settings for both conditions.
3. Save raw prompts and raw responses with timestamps and model identifiers.
4. Blind response labels before scoring.
5. Score each dimension against the case-specific criteria; use two independent scorers if feasible.
6. Report all cases, missing runs, exclusions, and cost/latency.
7. Replicate across models before making claims about modern AI generally.

## Interpretation

A higher score in a small pilot is a preliminary observation, not proof of general superiority. Russell's concepts are philosophical inspiration; this benchmark tests the operational prompt, not the truth of Russell's worldview.

Never fabricate runs, scores, API calls, or results. Clearly distinguish planned, executed, and verified experiments.
