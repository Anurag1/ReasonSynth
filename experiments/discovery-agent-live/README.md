# Discovery Agent Live Benchmark

A controlled prototype for testing a multi-agent discovery loop against a simple predictive baseline.

## Pipeline

```text
Unknown-structure detection
        ↓
Representation search
        ↓
Contradiction test
        ↓
Latent-variable search
        ↓
Experiment selection
        ↓
Improved explanatory model
```

## Live result

The benchmark was run on 20 independent random seeds:

- Interaction `A*C` discovered: **20/20**
- Correct `A` intervention selected: **20/20**
- Specialized pipeline beat the baseline on MSE: **20/20**
- Representative seed 7 baseline MSE: **5.7766**
- Representative seed 7 pipeline MSE: **1.5280**

## Important limitation

This is a **synthetic controlled benchmark**. The hidden mechanism was deliberately constructed by the benchmark author. Therefore the result demonstrates that the software loop can detect a deliberately hidden interaction/latent structure; it does **not** establish autonomous scientific discovery or superiority over modern research agents.

## Run

```bash
python discovery_agents.py
```

## Next experiment

Replace the synthetic generator with a real, held-out scientific dataset and compare:

1. Standard LLM baseline
2. Search/retrieval research agent
3. This discovery-agent pipeline

Evaluate novelty, correctness, information gain, reproducibility, calibration, and compute cost.
