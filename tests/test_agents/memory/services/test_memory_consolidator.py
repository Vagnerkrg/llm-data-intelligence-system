from src.agents.memory.services.memory_consolidator import (
    MemoryConsolidator
)

from src.agents.memory.services.relevance_analyzer import (
    RelevanceAnalyzer
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def create_consolidator():

    return MemoryConsolidator(
        RelevanceAnalyzer()
    )



def test_should_consolidate_memory():

    consolidator = create_consolidator()


    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    result = consolidator.consolidate(
        memory
    )


    assert result.memory_id == "001"

    assert result.score > 0

    assert result.consolidated is True



def test_should_fail_with_invalid_memory():

    consolidator = create_consolidator()


    result = consolidator.consolidate(
        None
    )


    assert result.memory_id == ""

    assert result.score == 0.0

    assert result.consolidated is False