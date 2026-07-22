from src.agents.memory.services.memory_intelligence import (
    MemoryIntelligence
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


def test_should_analyze_memory():

    intelligence = MemoryIntelligence(
        RelevanceAnalyzer()
    )


    memory = MemoryEntry(
        memory_id="001",
        content="User likes technical answers.",
        memory_type=MemoryType.LONG_TERM
    )


    result = intelligence.analyze(
        memory
    )


    assert result.memory_id == "001"

    assert result.score > 0

    assert result.factors