from .engine import Concept, MissingConnectionEngine


CONCEPTS = [
    Concept("Leonardo observation", "visual observation, geometry, anatomy, patterns, experiment"),
    Concept("Knowledge graphs", "entities, relationships, graph structure, inference, patterns"),
    Concept("Contradiction discovery", "assumptions, contradictions, hypotheses, evidence, patterns"),
    Concept("Scientific research", "hypothesis, experiment, evidence, inference, discovery"),
]


if __name__ == "__main__":
    engine = MissingConnectionEngine(min_score=0.05)
    for row in engine.report(CONCEPTS):
        print(f"{row['left']} <-> {row['right']} | score={row['score']}")
        print(f"  {row['hypothesis']}")
