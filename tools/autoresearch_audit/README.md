# Autoresearch Results Audit

A dependency-free utility for checking the integrity of the `results.tsv` files used by [karpathy/autoresearch](https://github.com/karpathy/autoresearch). It is an adjacent auditing tool; it does not alter `train.py`, the evaluation harness, or the experiment-selection policy.

## Usage

```bash
python tools/autoresearch_audit/autoresearch_audit.py results.tsv
python tools/autoresearch_audit/autoresearch_audit.py results.tsv --json
python -m unittest discover -s tools/autoresearch_audit/tests -v
```

The input TSV is expected to contain these columns:

```text
commit  val_bpb  memory_gb  status  description
```

(tab-separated, not spaces). The auditor checks required fields, accepted statuses (`keep`, `discard`, `crash`), finite/non-negative metrics, duplicate commit identifiers, and the documented zero-metric convention for crashed runs. It then reports counts and the lowest `val_bpb` among valid `keep` rows. Lower `val_bpb` is better in autoresearch.

Exit codes: `0` means all rows passed validation, `1` means one or more rows failed validation, and `2` means the input could not be read or its header is invalid. JSON mode emits the report to standard output; input errors are written to standard error.

This validates log consistency only. It does not verify commit contents, reproduce training, estimate statistical significance, or establish that an experiment's result generalizes.
