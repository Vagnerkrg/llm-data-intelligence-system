from src.agents.memory.services.memory_relevance import (
    MemoryRelevance
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_should_evaluate_memory_relevance():

    service = MemoryRelevance()


    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations about AI systems.",
        memory_type=MemoryType.LONG_TERM
    )


    result = service.evaluate(
        memory
    )


    assert result.memory_id == "001"

    assert result.score > 0

    assert result.explanation != ""



def test_should_fail_with_invalid_memory():

    service = MemoryRelevance()


    result = service.evaluate(
        None
    )


    assert result.score == 0.0