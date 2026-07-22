from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)


def test_relevance_result_creation():

    result = RelevanceResult(
        memory_id="memory_001",
        score=0.85,
        factors={
            "importance": 0.9
        },
        explanation="Relevant memory"
    )

    assert result.memory_id == "memory_001"
    assert result.score == 0.85
    assert result.factors["importance"] == 0.9
    assert result.explanation == "Relevant memory"


def test_relevance_result_defaults():

    result = RelevanceResult(
        memory_id="memory_002"
    )

    assert result.score == 0.0
    assert result.factors == {}
    assert result.explanation == ""