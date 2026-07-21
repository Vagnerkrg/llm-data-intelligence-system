from src.agents.memory.integration.runtime_memory_adapter import (
    RuntimeMemoryAdapter
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



def test_runtime_should_store_memory():

    adapter = RuntimeMemoryAdapter(
        StorageAdapter(
            InMemoryStore()
        )
    )


    memory = MemoryEntry(
        memory_id="001",
        content="runtime memory",
        memory_type=MemoryType.LONG_TERM
    )


    adapter.remember(
        memory
    )


    result = adapter.recall(
        "001"
    )


    assert result == memory