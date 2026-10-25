# UNSEEN execution status

This branch was initialized from the ReasonSynth repository because no existing UNSEEN repository was found in the accessible repositories.

## Status

- Experimental design: documented in `EXPERIMENT_PROTOCOL.md`.
- Python prototype modules are present under `unseen/` from the current branch scaffolding; inspect the recursive tree before treating the package as complete.
- The `unseen/web.py` file must be reviewed before use: prior write attempts left a basic placeholder implementation in the file.
- Full end-to-end test execution has not yet been verified in a local runtime or GitHub Actions.

## Required validation

1. Verify that `unseen/data.py`, `unseen/representations.py`, `unseen/solver.py`, `unseen/benchmark.py`, `unseen/cli.py`, `tests/test_pipeline.py`, `pyproject.toml` and `.github/workflows/ci.yml` exist and match the protocol.
2. Run `pip install -e ".[dev]"`, `pytest`, and `python -m unseen.cli evaluate --out results/demo.json`.
3. Inspect GitHub Actions logs before claiming test success.
4. Treat all synthetic-case scores as pipeline smoke results, not evidence that a graph system outperforms modern LLMs.
