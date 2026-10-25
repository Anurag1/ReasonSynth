# UNSEEN Experiment Protocol: Graph vs Text

## Question
Does explicit graph structure improve contradiction-resolution accuracy over text-only evidence under matched model, source, prompt, token and tool budgets?

## Hypotheses
H1 (primary): graph improves case-level resolution accuracy vs text. H2: improves source attribution. H3: lowers unsupported conclusions. H4: gain increases with evidence complexity. H5: improves uncertainty handling without excessive abstention.

## Arms
A text-only with source IDs. B graph nodes and provenance-linked typed edges. C structured text/JSON with same claims and relationships. D graph with selected edge types ablated.

## Data
Combine public fact-verification and multi-hop datasets such as FEVER and HotpotQA with a custom contradiction set. Proposed custom set: 600 cases across direct conflict, context mismatch, time changes, missing evidence, multi-hop conflict and source reliability; initial 360/120/120 development/validation/locked-test split, finalized after prospective power analysis. Keep related scenarios and paraphrases in one split. Two annotators label independently; a third adjudicates.

## Controls
Same pinned model, output schema, decoding settings, source evidence, tool access and matched context/compute budgets. Record tokens, calls, latency and cost. Blind evaluators to arm; audit graph extraction separately.

## Metrics
Primary: accuracy of evidence-supported conclusion including correct uncertainty labels. Secondary: evidence precision/recall, contradiction macro-F1, unsupported conclusion rate, abstention quality, Brier score, graph extraction F1, latency and cost.

## Statistics
Primary B-A paired accuracy difference, 95% CI, McNemar test (exact version for sparse discordant pairs), two-sided alpha 0.05. Power using development-set discordance and a preregistered useful effect. Correct secondary confirmatory tests for multiplicity. Do not repeatedly inspect the locked test while tuning.

## Product gate (proposed, not universal)
At least +5 percentage points accuracy with 95% CI excluding zero, without material degradation in unsupported conclusions, abstention quality or cost. To claim graph-specific benefit, compare B with C too.

## Falsification
Reject the graph-specific claim if adequately powered tests find no meaningful gain over matched structured text, if gains vanish on held-out real-world cases, or gains are offset by unsupported certainty or unacceptable cost/latency. A nonsignificant result alone is not proof of equivalence.

## Current status
Protocol written. Bundled 12-case fixtures and deterministic heuristic solver are for software smoke tests only; they cannot establish superiority over modern AI.
