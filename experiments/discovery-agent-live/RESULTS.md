# Live Results

Date: 2026-08-28

## Benchmark

Synthetic hidden-variable discovery problem with 300 observations per run. The evaluator hides the latent mechanism from the agents.

True generating structure contains a latent variable approximately related to `C` and `D`, with the target depending strongly on an `A × H` interaction.

## 20-seed result

| Metric | Result |
|---|---:|
| Seeds | 20 |
| `A*C` interaction discovered | 20/20 |
| `A` intervention selected | 20/20 |
| Pipeline MSE better than baseline | 20/20 |

Representative seed 7:

| Model | MSE |
|---|---:|
| Baseline single-marginal predictor | 5.7766 |
| Additive model | 5.7006 |
| Specialized interaction model | 1.5280 |

The latent-variable search estimated a structure close to `H ~= -0.8*C + 0.5*D` in this run.

## Interpretation

The specialized pipeline successfully performed the intended sequence:

1. Detect weak marginal explanation.
2. Search alternative representations.
3. Identify a strong interaction.
4. Search for a latent representation.
5. Select a discriminating intervention.
6. Produce a lower-error explanatory model.

## Claim boundary

The benchmark is intentionally synthetic. It cannot establish that the system discovers previously unknown real-world science. The next validation stage must use held-out real scientific data and a blind evaluation protocol.
