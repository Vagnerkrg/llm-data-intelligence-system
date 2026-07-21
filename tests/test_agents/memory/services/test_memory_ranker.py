from src.agents.memory.services.memory_ranker import (
    MemoryRanker
)

from src.agents.memory.domain.retrieval_result import (
    RetrievalResult
)


class FakeMemory:

    def __init__(
        self,
        memory_id,
        score
    ):
        self.memory_id = memory_id
        self.score = score



def test_should_rank_memories():

    result = RetrievalResult(
        query="test",
        memories=[
            FakeMemory("001", 0.40),
            FakeMemory("002", 0.95),
            FakeMemory("003", 0.70),
        ]
    )

    ranker = MemoryRanker()

    ranked = ranker.rank(
        result
    )

    assert ranked.success is True

    assert ranked.memories[0].memory_id == "002"

    assert ranked.memories[1].memory_id == "003"

    assert ranked.memories[2].memory_id == "001"



def test_should_fail_with_invalid_result():

    ranker = MemoryRanker()

    result = ranker.rank(
        None
    )

    assert result.success is False