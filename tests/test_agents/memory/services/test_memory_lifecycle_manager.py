from src.agents.memory.services.memory_lifecycle_manager import (
    MemoryLifecycleManager
)

from src.agents.memory.services.memory_consolidator import (
    MemoryConsolidator
)

from src.agents.memory.services.memory_decay import (
    MemoryDecay
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



def create_lifecycle_manager():

    analyzer = RelevanceAnalyzer()


    consolidator = MemoryConsolidator(
        relevance_analyzer=analyzer
    )


    return MemoryLifecycleManager(
        consolidator=consolidator,
        decay=MemoryDecay()
    )



def test_should_manage_memory_lifecycle():

    manager = create_lifecycle_manager()


    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    result = manager.process(
        memory
    )


    assert result.memory_id == "001"

    assert result.consolidated is True

    assert result.decayed is True



def test_should_fail_lifecycle_with_invalid_memory():

    manager = create_lifecycle_manager()


    result = manager.process(
        None
    )


    assert result.memory_id == ""

    assert result.consolidated is False

    assert result.decayed is False