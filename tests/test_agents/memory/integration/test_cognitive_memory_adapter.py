from src.agents.memory.integration.cognitive_memory_adapter import (
    CognitiveMemoryAdapter
)

from src.agents.memory.storage.storage_adapter import (
    StorageAdapter
)

from src.agents.memory.storage.in_memory_store import (
    InMemoryStore
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_cognitive_should_store_learning():

    adapter = CognitiveMemoryAdapter(
        StorageAdapter(
            InMemoryStore()
        )
    )


    memory = MemoryEntry(
        memory_id="learning-001",
        content="Improvement cycle completed",
        memory_type=MemoryType.LONG_TERM
    )


    adapter.store_learning(
        memory
    )


    result = adapter.retrieve_learning(
        "learning-001"
    )


    assert result == memory