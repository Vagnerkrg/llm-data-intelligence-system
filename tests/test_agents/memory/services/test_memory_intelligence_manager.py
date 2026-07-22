from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)

from src.agents.memory.services.memory_intelligence_manager import (
    MemoryIntelligenceManager
)



def create_manager():

    return MemoryIntelligenceManager()



def test_should_analyze_memory_intelligence():

    manager = create_manager()


    memory = MemoryEntry(
        memory_id="001",
        content=(
            "User prefers technical "
            "architecture explanations."
        ),
        memory_type=MemoryType.LONG_TERM,
        metadata={
            "importance": "high"
        }
    )


    result = manager.analyze(
        memory
    )


    assert result.memory_id == "001"

    assert result.relevance_score > 0

    assert (
        "memory_type"
        in result.factors
    )



def test_should_fail_with_invalid_memory():

    manager = create_manager()


    result = manager.analyze(
        None
    )


    assert result.memory_id == ""

    assert result.relevance_score == 0.0