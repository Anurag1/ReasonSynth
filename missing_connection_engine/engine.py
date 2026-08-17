"""A small, explainable engine for finding candidate missing connections.

This MVP is deliberately deterministic: it does not claim novelty. It scores
pairs of concepts using lexical overlap, shared attributes, and bridge terms,
then emits hypotheses that can be validated against external evidence later.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from itertools import combinations
from typing import Iterable


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "of", "on", "or", "that", "the", "to", "with", "using",
}


@dataclass(frozen=True)
class Concept:
    name: str
    text: str


@dataclass(frozen=True)
class Connection:
    left: str
    right: str
    score: float
    shared_terms: tuple[str, ...]
    hypothesis: str


class MissingConnectionEngine:
    """Discover explainable candidate relationships between concepts."""

    def __init__(self, min_score: float = 0.15):
        self.min_score = min_score

    @staticmethod
    def _terms(text: str) -> set[str]:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{2,}", text.lower())
        return {w for w in words if w not in STOPWORDS}

    def discover(self, concepts: Iterable[Concept]) -> list[Connection]:
        concepts = list(concepts)
        results: list[Connection] = []
        term_sets = {c.name: self._terms(c.text) for c in concepts}

        for left, right in combinations(concepts, 2):
            a, b = term_sets[left.name], term_sets[right.name]
            shared = sorted(a & b)
            union = a | b
            if not union:
                continue
            jaccard = len(shared) / len(union)

            # A weak-but-interesting bridge: concepts with no direct lexical
            # overlap can still be paired when both are represented richly.
            bridge_bonus = 0.05 if len(a) >= 4 and len(b) >= 4 and not shared else 0.0
            score = round(min(1.0, jaccard + bridge_bonus), 3)
            if score >= self.min_score:
                hypothesis = self._hypothesis(left, right, shared)
                results.append(Connection(left.name, right.name, score, tuple(shared), hypothesis))

        return sorted(results, key=lambda x: (-x.score, x.left, x.right))

    @staticmethod
    def _hypothesis(left: Concept, right: Concept, shared: list[str]) -> str:
        if shared:
            bridge = ", ".join(shared[:3])
            return f"Investigate whether {left.name} and {right.name} share a mechanism through: {bridge}."
        return f"Investigate whether a transferable mechanism connects {left.name} and {right.name}."

    def report(self, concepts: Iterable[Concept]) -> list[dict]:
        return [
            {
                "left": c.left,
                "right": c.right,
                "score": c.score,
                "shared_terms": list(c.shared_terms),
                "hypothesis": c.hypothesis,
            }
            for c in self.discover(concepts)
        ]
