from src.agents.memory.domain.retrieval_result import (
    RetrievalResult
)


def test_should_create_retrieval_result():

    result = RetrievalResult(
        query="dados anteriores",
        score=0.95
    )


    assert result.query == (
        "dados anteriores"
    )

    assert result.score == 0.95

    assert result.memories == []