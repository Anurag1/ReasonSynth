# Demo result interpretation

Run `python -m unseen.cli evaluate --out results/demo.json` to regenerate aggregate and per-case JSON output.

Current pipeline: 12 synthetic cases, four representation arms, deterministic heuristic solver. It does not call a foundation model and is not an independent scientific benchmark. Aggregate accuracy tests prototype behavior only; it cannot substantiate superiority or generalization. See `EXPERIMENT_PROTOCOL.md` for confirmatory requirements.
