# Missing Connection Engine

An explainable MVP for discovering **candidate relationships between concepts**.

## Why

The long-term research hypothesis is:

> useful discoveries may exist in relationships that are weakly represented or absent from a knowledge graph.

This repository does **not** claim that a detected connection is novel or scientifically true. It produces candidates and explicit hypotheses that require evidence-based validation.

## Pipeline

```text
Concepts
   ↓
Term / attribute extraction
   ↓
Pairwise relationship scoring
   ↓
Candidate connection
   ↓
Hypothesis
   ↓
External evidence validation (future)
```

## Run

From the repository root:

```bash
python -m missing_connection_engine.demo
```

## Next research stages

1. Replace lexical overlap with embeddings and graph topology.
2. Ingest papers, patents, and datasets with provenance.
3. Detect contradictory claims and missing edges.
4. Rank candidates by novelty, evidence, feasibility, and commercial relevance.
5. Build reproducible benchmarks against existing knowledge-discovery systems.
