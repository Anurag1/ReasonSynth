# UNSEEN — contradiction discovery prototype

UNSEEN compares text-only reasoning with graph-structured evidence on contradiction-heavy cases.

## Quick start
Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m unseen.cli evaluate --out results/demo.json
pytest
python -m unseen.web
```

Open http://127.0.0.1:8000.

## What this prototype includes
- 12 synthetic, source-linked cases.
- Four arms: text, graph, structured text and graph ablation.
- Deterministic solver, CLI JSON report, local evidence-review web UI, unit tests and CI.

## Scientific limitation
This is a software prototype, not proof that knowledge graphs outperform modern AI. Its cases are synthetic and the solver is a transparent heuristic, not an LLM. Use the preregistered protocol in `docs/EXPERIMENT_PROTOCOL.md` before making any performance claim.

## Roadmap
1. Annotated held-out benchmark based on public and custom cases.
2. Pinned model adapter across all arms.
3. Confidence intervals, paired significance tests and cost accounting.
4. Native SwiftUI client after the evidence schema stabilizes.
