# CIB-01 — Creator Intelligence Benchmark

A reproducible benchmark for **Knowledge → Framework → Content** transformation.

This benchmark measures whether a system can turn an observed knowledge problem into a useful, non-copying knowledge product while preserving evidence, identifying tensions, and proposing validation experiments.

## Scope

CIB-01 is inspired by publicly observable creator-system patterns such as:

- problem-first positioning
- counterintuitive hooks
- named frameworks
- practical tools
- evidence + story
- explicit experiments

It does **not** reproduce creator scripts, titles, or copyrighted passages.

## Pipeline

```text
Input knowledge
    ↓
Problem extraction
    ↓
Tension / contradiction detection
    ↓
Hypothesis generation
    ↓
Framework synthesis
    ↓
Content packaging
    ↓
Validation experiment
```

## Metrics

Each case receives 0–100 points:

- Problem clarity: 0–20
- Tension quality: 0–15
- Hypothesis quality: 0–15
- Framework quality: 0–20
- Practicality: 0–15
- Validation design: 0–15

The scoring implementation is deterministic so regression tests can run without an LLM.

## Run

```bash
python -m unittest discover -s tests -v
python scripts/run_benchmark.py
```

## Baseline

The repository ships with a hand-authored baseline dataset and a deterministic evaluator. This first milestone is intentionally model-independent. A later adapter can feed an LLM-generated result into the exact same evaluator.
