from missing_connection_engine import Concept, MissingConnectionEngine


def test_discover_returns_ranked_connection():
    concepts = [
        Concept("A", "graph patterns inference relationships"),
        Concept("B", "scientific patterns inference evidence"),
    ]
    result = MissingConnectionEngine(min_score=0.05).discover(concepts)
    assert result
    assert result[0].left == "A"
    assert result[0].right == "B"
    assert "patterns" in result[0].shared_terms


def test_empty_concepts_is_safe():
    assert MissingConnectionEngine().discover([]) == []
